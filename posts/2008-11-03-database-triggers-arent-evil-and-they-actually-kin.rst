---
layout: post
title: "Database triggers aren't evil, and they actually kind of rock"
date: 2008-11-03T20:44:19-06:00
comments: false
categories: [Databases, Django, Programming, Triggers, Python]
published: true
alias: [/blog/post/database-triggers-arent-evil-and-they-actually-kin]
---

Who says they suck?
-------------------

Nobody that I've seen has come out and actually said that they don't like
database triggers, but at the same time, Python (Django) programmers like to
program in Python.  And PL/pgSQL certainly is not Python.  There's a tendency to
do everything in Python--especially with the use of Django's dispatcher.

But there's some serious overhead with that approach, and roundtrips, and race
conditions, etc.  If you're using a good database, there's an alternative:
you guessed it, database triggers.

Let's set up some models
------------------------

Here will be our models for the remainder of this post:

.. code-block:: python

    class Bookmark(models.Model):
        title = models.CharField(max_length=100)
        url = models.URLField(max_length=255)
    
        num_votes = models.PositiveIntegerField(null=True, blank=True, default=0)
        score = models.IntegerField(null=True, blank=True, default=0)

    class Vote(models.Model):
        bookmark = models.ForeignKey(Bookmark, related_name='votes')
        value = models.IntegerField()

As you can tell, we have a straightforward ``Bookmark`` and ``Vote`` models here.
But there are also two denormalized fields: ``num_votes``, and ``score``.

Doing it in Python
------------------

The advantage of doing this in Python is that it's simple and Django supports
it out of the box.  Here's how the code for that would look:

.. code-block:: python

    from django.db.models import signals

    def update_bookmark_aggregate(sender, instance, **kwargs):
        bmark = instance.bookmark
        bmark.num_votes = bmark.votes.count()
        bmark.score = sum(bmark.votes.values_list('value', flat=True))
        bmark.save(force_update=True)
    signals.post_save.connect(update_bookmark_aggregate, sender=Vote)

Very simply, every time a vote is saved, the ``update_bookmark_aggregate``
function is called which updates the bookmark with its new score and num_votes.

Doing it in Pl/pgSQL
--------------------

Create a new file, named ``management.py`` under your bookmarks app directory.
Its contents will be as follows:

.. code-block:: python

    from django.db.models import signals
    from bookmarks import models

    sql = """
    CREATE LANGUAGE plpgsql;
    CREATE OR REPLACE FUNCTION update_bookmark_aggregate_trigger()
        RETURNS "trigger" AS '
        DECLARE
            new_score INTEGER;
            new_num_votes INTEGER;
        BEGIN
            SELECT COUNT(*) INTO STRICT new_num_votes FROM bookmarks_vote
                WHERE bookmark_id = NEW.bookmark_id;
            SELECT COALESCE(SUM(value), 0) INTO STRICT new_score FROM bookmarks_vote
                WHERE bookmark_id = NEW.bookmark_id;
        UPDATE bookmarks_bookmark 
            SET
                score = new_score,
                num_votes = new_num_votes
            WHERE id = NEW.bookmark_id;
        RETURN NEW;
        END;' LANGUAGE 'plpgsql' VOLATILE;

    CREATE TRIGGER update_bookmark_aggregate_trigger AFTER INSERT OR UPDATE
        ON bookmarks_vote FOR EACH ROW
        EXECUTE PROCEDURE update_bookmark_aggregate_trigger();
    """
    
    def create_trigger(app, created_models, verbosity, **kwargs):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
    signals.post_syncdb.connect(create_trigger, sender=models)

In this file we have declared two variables, ``new_score``, and
``new_num_votes``.  We do two queries to get the aggregate data.  And then we
update the bookmark to reflect the new aggregated values.  This script is
executed once when the bookmarks models are first loaded into the database, and
we're all set!

Let's see how it works
----------------------

.. code-block:: pycon

    >>> from bookmarks.models import Bookmark, Vote
    >>> b = Bookmark.objects.create(title="Blog", url='http://eflorenzano.com/')
    >>> b.num_votes
    0
    >>> b.score
    0
    # There is no aggregate data yet
    >>> Vote.objects.create(bookmark=b, value=1)
    <Vote: Vote object>
    >>> Vote.objects.create(bookmark=b, value=2)
    <Vote: Vote object>
    # We need to re-query for the bookmark, due to no identity map in Django.
    >>> b = Bookmark.objects.all()[0]
    >>> b.num_votes
    2
    >>> b.score
    3

Voila!  This was all done in the database behind the scenes.  Very cool, very
fast, and it kind of rocks.