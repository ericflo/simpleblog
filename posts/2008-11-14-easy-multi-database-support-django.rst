---
layout: post
title: "Easy Multi-Database Support for Django"
date: 2008-11-14T23:51:44-06:00
comments: false
categories: [Django, Programming, Databases, Multiple Databases, Database Sharding, Database Partitioning, Python]
published: true
alias: [/blog/post/easy-multi-database-support-django]
---

Background
----------

One of the most requested features in Django is that it support connecting to
multiple databases at once.  This can come in several flavors, but the two
most common cases are sharding_, and (vertical) partitioning_.  If you've been
waching closely, some of the core developers have been saying in various places
for a few months now that this is technically possible, right now, in Django 1.0.

Of course, being technically possible is a long way from being easy.  Right now
there is no public API for dealing with multiple databases.  So why do the
developers say that it's possible to do?  The answer is simple: shortly before
Django 1.0 was released, much of the internals of QuerySet objects (Django's
interface to the database) were refactored to use object state-level connection
objects instead of a global connection object.

This seemingly-small change opens the doors for multiple databases, even if
there is no API in front of it.  So let's create an API.  We're going to be
focusing on vertical partitioning, since it's slightly easier, but the technique
demonstrated here will be illustrative when implementing sharding as well.  Oh,
and since we're poking deep into the core of Django's internals, I'm obliged to
give the standard disclaimer: this is not supported and may break in future
versions of Django, so use these techniques at your own risk.

First things first
------------------

The first thing that needs to be done when implementing multiple database
support is to supply Django with the information about all of the databases
that you would like to connect to.  Here's how that should look in
``settings.py``:

.. code-block:: python

    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'primary.db'
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_HOST = ''
    DATABASE_PORT = ''

    DATABASES = dict(
        primary = dict(
            DATABASE_ENGINE=DATABASE_ENGINE,
            DATABASE_NAME=DATABASE_NAME,
            DATABASE_USER=DATABASE_USER,
            DATABASE_PASSWORD=DATABASE_PASSWORD,
            DATABASE_HOST=DATABASE_HOST,
            DATABASE_PORT=DATABASE_PORT,
        ),
        secondary = dict(
            DATABASE_ENGINE=DATABASE_ENGINE,
            DATABASE_NAME='secondary.db',
            DATABASE_USER=DATABASE_USER,
            DATABASE_PASSWORD=DATABASE_PASSWORD,
            DATABASE_HOST=DATABASE_HOST,
            DATABASE_PORT=DATABASE_PORT,
        ),
    )

We have not only created the typical database information that Django
requires, but we've also created a dictionary containing information about all
of the databases that we intend to connect to.  In this case, we are connecting
to two sqlite databases in the same directory, named ``primary.db`` and
``secondary.db``.

Let's now create an app, named ``blog`` (I know, I know, very unoriginal).  The
``models.py`` will look like this:

.. code-block:: python

    import datetime
    from django.db import models

    class Post(models.Model):
        title = models.TextField()
        body = models.TextField()
        date_submitted = models.DateTimeField(default=datetime.datetime.now)

    class Link(models.Model):
        url = models.URLField()
        description = models.TextField(null=True, blank=True)
        date_submitted = models.DateTimeField(default=datetime.datetime.now)

And we hook it up to the admin and settings.py in the normal manner.  For more
information on how to do this, follow `the official tutorial`_.  We're going to
be storing the ``Post`` objects in the primary database, and the ``Link``
objects in the secondary database.  Since they don't have any foreign keys, we
don't have to worry about joins. (They are possible, but not easy to describe
in one post.)

Multiple databases
------------------

We should probably write some code that will inspect all of our models and
create only the tables that we want in each database.  For the sake of
simplicity and practicality of a blog post, we're not going to do that.
Instead, we will simply create all of the schema on both databases.  The
management command to do so might look something like this (I called it
multi_syncdb):

.. code-block:: python

    from django.core.management.base import NoArgsCommand
    from django.core.management import call_command
    from django.conf import settings

    class Command(NoArgsCommand):
        help = "Sync multiple databases."
    
        def handle_noargs(self, **options):
            for name, database in settings.DATABASES.iteritems():
                print "Running syncdb for %s" % (name,)
                for key, value in database.iteritems():
                    setattr(settings, key, value)
                call_command('syncdb')

All of this has been fine, but the real workhorse of multiple database support
lies in the model's ``Manager``.  Let's write a multi-db aware manager right
now:

.. code-block:: python

    from django.db import models
    from django.conf import settings
    from django.db.models import sql
    from django.db.transaction import savepoint_state

    try:
        import thread
    except ImportError:
        import dummy_thread as thread

    class MultiDBManager(models.Manager):
        def __init__(self, database, *args, **kwargs):
            self.database = database
            super(MultiDBManager, self).__init__(*args, **kwargs)
        
        def get_query_set(self):
            qs = super(MultiDBManager, self).get_query_set()
            qs.query.connection = self.get_db_wrapper()
            return qs
    
        def get_db_wrapper(self):
            database = settings.DATABASES[self.database]
            backend = __import__('django.db.backends.' + database['DATABASE_ENGINE']
                + ".base", {}, {}, ['base'])
            backup = {}
            for key, value in database.iteritems():
                backup[key] = getattr(settings, key)
                setattr(settings, key, value)
            wrapper = backend.DatabaseWrapper()
            wrapper._cursor(settings)
            for key, value in backup.iteritems():
                setattr(settings, key, value)
            return wrapper
    
        def _insert(self, values, return_id=False, raw_values=False):
            query = sql.InsertQuery(self.model, self.get_db_wrapper())
            query.insert_values(values, raw_values)
            ret = query.execute_sql(return_id)
            query.connection._commit()
            thread_ident = thread.get_ident()
            if thread_ident in savepoint_state:
                del savepoint_state[thread_ident]
            return ret

I know that's a lot of code!  Let's go through each piece one-by-one.  In the
``__init__`` function, we're just taking in the name of the database that we
want to use, and passing the rest into the inherited ``__init__`` function.

``get_query_set`` gets the ``QuerySet`` instance that it would have gotten, but
replaces the connection on the query object with one provided by the manager,
before returning the ``QuerySet``.  In essence, this ``get_db_wrapper`` function
is doing the bulk of the work.

``get_db_wrapper`` first gets the dictionary of the database connection
information for the given database name (captured from ``__init__``), then
dynamically imports the correct database backend from Django.  It then sets
the global settings to the values that they should be for that database (while
backing up the original settings for restoration later).  Then, it initializes
that database connection, and restores the settings to their original values.

Most of the database operations are done through the ``QuerySet``, there is
still one operation which takes place elsewhere--saving.  To account for that,
we needed to override the ``_insert`` method on the manager.  In fact, all we're
doing here is providing the ``InsertQuery`` with the correct connection and
executing that query.  Then, we need to ensure that the query is committed and
do any transaction management that's necessary.

That's it!

How do we specify that one ore more models will use another database then?
Because so far all that we have done is write this ``MultiDBManager``.  We will
just add one line assigning the manager to our ``Link`` model.  The model
now looks like this:

.. code-block:: python

    class Link(models.Model):
        url = models.URLField()
        description = models.TextField(null=True, blank=True)
        date_submitted = models.DateTimeField(default=datetime.datetime.now)
    
        _default_manager = MultiDBManager('secondary')

Conclusion
----------

The ``MultiDBManager`` can be re-used for any number of models to be partitioned
on to any number of databases.  The hard part is making sure that none of the
models in one database reference any models in the other database.  It's
possible to do it, by storing the foreign key as a regular integer and querying
for all of the referenced model instances through Python instead of using the
database (for obvious reasons), but then it becomes much harder.

It will be great when Django provides a public API for doing this in a more
transparent way, but for now this works.  Please let me know if you use any
of these techniques for large scale Django deployments, and if so, what were the
problems that were encountered along the way?

.. _sharding: http://en.wikipedia.org/wiki/Shard_(database_architecture)
.. _partitioning: http://en.wikipedia.org/wiki/Partition_(database)
.. _`the official tutorial`: http://docs.djangoproject.com/en/dev/#tutorial-writing-your-first-django-application