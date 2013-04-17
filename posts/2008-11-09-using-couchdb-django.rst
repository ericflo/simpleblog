---
layout: post
title: "Using CouchDB with Django"
date: 2008-11-09T23:59:59-06:00
comments: false
categories: [Python, Django, CouchDB]
published: true
alias: [/blog/post/using-couchdb-django]
---

Ahhh, Django_: my favorite web framework.  And CouchDB_: my favorite new
database technology.  How can I pair these two awesomes together to make an
awesome-er?

One of the features that I would like to add to this site when it's time for an
upgrade is a lifestream.  It seems like everyone is doing it these days (isn't
this great logic!), so I probably should too.  Originally this was going to be
written in the standard Django way--write some models, fill it with data, and
slice and dice that data to make it pretty.

After thinking about it, I decided not to go that route.  Why?  Well, let's go
over it: There needs to be a Twitter_ model, that's for sure.  I also want a
Pownce_ model, and a Flickr_ model.  Already this is becoming tedious!  At this
point we have two options: continue creating these individual models and fill
them with data, or try to find the common bits and group them into Ubermodels
of some sort, with some type of field to use as a discriminator.  Ugh.

This is the perfect use case for a schemaless database, and CouchDB_ fits that
bill just perfectly.  Plus its `python support`_ is actually quite mature, and
running it on a mac is, quite literally, `one click`_.  So now that we've all
agreed (we all agree, right?) that we want to use CouchDB_ with Django_, how
can we make it happen?

First let's set some database settings:

.. code-block:: python

    COUCHDB_HOST = 'http://localhost:5984/'
    TWITTER_USERNAME = 'ericflo'

So far, so good.  Now let's write some initialization code and put it in to an
application in the ``__init__.py``:

.. code-block:: python

    from couchdb import client
    from django.conf import settings

    class CouchDBImproperlyConfigured(Exception):
        pass

    try:
        HOST = settings.COUCHDB_HOST
    except AttributeError:
        raise CouchDBImproperlyConfigured("Please ensure that COUCHDB_HOST is " + \
            "set in your settings file.")

    DATABASE_NAME = getattr(settings, 'COUCHDB_DATABASE_NAME', 'couch_lifestream')
    COUCHDB_DESIGN_DOCNAME = getattr(settings, 'COUCHDB_DESIGN_DOCNAME',
        'couch_lifestream-design')

    if not hasattr(settings, 'couchdb_server'):
        server = client.Server(HOST)
        settings.couchdb_server = server

    if not hasattr(settings, 'couchdb_db'):
        try:
            db = server.create(DATABASE_NAME)
        except client.ResourceConflict:
            db = server[DATABASE_NAME]
        settings.couchdb_db = db

In this code, we're loading the CouchDB client and either creating or
connecting to a database.  We do a bit of error checking to ensure that if we
forgot to add ``COUCHDB_HOST`` in our settings file, it will yell at us. So how
do we use this?  Let's write some data importing stuff!

.. code-block:: python

    try:
        import simplejson as json
    except ImportError:
        import json
    
    TWITTER_USERNAME = getattr(settings, 'TWITTER_USERNAME', None)

    fetched = urlopen('http://twitter.com/statuses/user_timeline.json?id=%s' % (
        TWITTER_USERNAME,)).read()
    data = json.loads(fetched)
    map_fun = 'function(doc) { emit(doc.id, null); }'
    for item in data:
        item['item_type'] = 'twitter'
        if len(db.query(map_fun, key=item['id'])) == 0:
            db.create(item)

This can go inside a Django management command or in a standalone script.
Essentially what we're doing is loading the timeline for a user, and then for
each item in that response we're setting the ``item_type`` to 'twitter'.  Then
we're checking to see if an item with that current twitter id already exists,
and if not, we're creating it.

Now we need a way to query this data.  In CouchDB_, the way to query for data is
using views_.  Views are stored in the database, so they can be entered
manually, but I much prefer to manage views programmatically.  Thankfully,
Python's CouchDB library and Django give us all we need to make this very, very
easy:

.. code-block:: python

    from django.db.models import signals
    from couch_lifestream import models, db, COUCHDB_DESIGN_DOCNAME
    from couchdb.design import ViewDefinition
    from textwrap import dedent

    by_date = ViewDefinition(COUCHDB_DESIGN_DOCNAME, 'by_date',
        dedent("""
        function(doc) {
            emit(doc.couch_lifestream_date, null);
        }
    """))

    def create_couchdb_views(app, created_models, verbosity, **kwargs):
        ViewDefinition.sync_many(db, [by_date])
    signals.post_syncdb.connect(create_couchdb_views, sender=models)

Make sure that this is placed somewhere that will be loaded when Django's
``manage.py`` is called.  In this case, I put it in the ``__init__.py`` file
under ``management/``.  What we're doing is creating two views--one which is
keyed by the ``item_type`` (we set this earlier to be 'twitter'), and another
which is keyed simply by date.  When we run ``python manage.py syncdb``, these
views will automatically be re-synced with the database.  Using this method, we
are able to manage these views quickly and easily, and distribute them in a
reusable way.

Now let's create some Django views so that we can visualize this data:

.. code-block:: python

    from couch_lifestream import db, COUCHDB_DESIGN_DOCNAME
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from django.http import Http404
    from couchdb import client

    def item(request, id):
        try:
            obj = db[id]
        except client.ResourceNotFound:
            raise Http404
        context = {
            'item': obj,
        }
        return render_to_response(
            'couch_lifestream/item.html',
            context,
            context_instance=RequestContext(request)
        )

    def items(request):
        item_type_viewname = '%s/by_date' % (COUCHDB_DESIGN_DOCNAME,)
        lifestream_items = db.view(item_type_viewname, descending=True)
        context = {
            'items': list(lifestream_items),
        }
        return render_to_response(
            'couch_lifestream/list.html',
            context,
            context_instance=RequestContext(request)
        )

The ``item`` view is fairly self-explanatory.  We query the db for the object of
the specified id, and if it doesn't exist, we throw a 404.  If it does exist, we
throw it into the context and let the template render the page.  The ``items``
view is slightly more interesting.  In this case, we're using that CouchDB view
that we created to query the database by date, and passing that list into the
context.

Obviously there's a ton more that we could cover, but these basic building
blocks that I've demonstrated are enough to get you started.  After this it's
mostly all presentational work.  I've open sourced all of the code that has been
written so far for the upcoming lifestream portion of this site, even though
right now it only supports Twitter_ and Pownce_.  I plan on continuing work
on it to support all of the services that I use.  You can track my progress
at the `project's page`_.

I'll make sure to blog about this again once the project is more mature, but for
now it should be fun to play around with.  Are you using CouchDB with Django?
If yes, then how are you dealing with that interaction?

.. _Django: http://www.djangoproject.com/
.. _CouchDB: http://incubator.apache.org/couchdb/
.. _Twitter: http://twitter.com/
.. _Pownce: http://pownce.com/
.. _Flickr: http://flickr.com/
.. _`python support`: http://code.google.com/p/couchdb-python/
.. _`one click`: http://jan.prima.de/~jan/plok/archives/142-CouchDBX-Revival.html
.. _views: http://wiki.apache.org/couchdb/Views
.. _`project's page`: http://github.com/ericflo/django-couch-lifestream/tree/master