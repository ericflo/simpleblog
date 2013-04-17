---
layout: post
title: "Why CouchDB Rocks"
date: 2008-11-29T16:31:31-06:00
comments: false
categories: [CouchDB, Programming]
published: true
alias: [/blog/post/why-couchdb-rocks]
---

Last week I wrote an article called `Why CouchDB Sucks`_, which many people
correctly said should have been called "What CouchDB Sucks at Doing".  Nearly
everyone pointed out that it was not designed to do the things that I was
mentioning in the article.  This time around, I'd like to focus on some of the
features about CouchDB that I think absolutely rock.

CouchDB is schema-free
----------------------

One of the most annoying parts of dealing with a traditional SQL database is
that you invariably need to change your schemata. This can be done usually with
some ``ALTER TABLE`` statements, but other times it requires scripts and careful
use of transactions, etc.  In CouchDB, the solution is to just start using your
new schema.  No migration needed.  If it's a significant change, then you might
need to change your views slightly, but nothing as annoying as what would be
needed with SQL.

The other advantage of having no schema is that some types of data just aren't
well suited to having a strict schema enforced upon them.  My CouchDB-based
`lifestreaming application`_ is a perfect example of the inherent flexibility of
CouchDB's schemaless design is that all kinds of disparate information can be
stored alongside each other and sorted and aggregated.  There's also no reason
that you need to use its schema-free nature this way.  You could, for example,
manually enforce a schema for certain databases, if needed.

CouchDB is RESTFUL HTTP
-----------------------

When is the last time you tried to install MySQL or PostgreSQL drivers for your
web development platform of choice?  If you're using ``apt-get`` it's not so
bad, but for just about every other platform, it's a total pain to get these
drivers up and running.  With CouchDB, there's no need.  It speaks HTTP.  Want
to create a new database?  Send an HTTP PUT request.  Want to retrieve a
document from the database?  Send an HTTP GET.  Want to delete a database?  Send
an HTTP DELETE.  As you can see, the API is quite straightforward and if a
client library doesn't already exist for your language of choice (hint:
`it does`_), then it will take you only a few minutes to write one.

But the best part about this is that we already have so many amazing and
well-tested tools to deal with HTTP.  For example, let's say you want to store
one database on one server and another database on another server?  It's as
simple as setting up nginx_ or perlbal_ or varnish_ as a reverse proxy and
having each URL go to a different machine.  The same thing goes for transparent
caching, etc.  Oh, and also, web browsers know how to speak HTTP, too.  You
could easily write `whole web apps served only from CouchDB`_.

Map/Reduce
----------

    Map/Reduce will kill every traditional data warehousing vendor in the
    market.  Those who adapt to it as a design/deployment pattern will survive,
    the rest won't.

Sounds like someone from Google must have said this, or some Hadoop evangelist,
or maybe someone who works on CouchDB.  In fact, this comes from `Brian Aker`_,
a MySQL hacker who was Director of Architecture at MySQL AB and is now
developing the open source fork of MySQL named Drizzle_ (also a very exciting
project in its own right).  He's right, too.  Google was on to something in a
big way when they unveiled their whitepaper on `Map/Reduce`_.  It's not the
be-all end-all for processing and generating large data sets, but it certainly
is a proven technology for that task.

Brian_ talks about massively multi-core machines which seem the inevitability
these days, and we will need to start writing logic that is massively
parallelizable to take advantage of these masses of CPUs.  Map/Reduce is one
way to force ourselves to write logic that can be parallelized.  It is a good
choice for any new database system to adopt for this reason, and that's why
it's great to see that CouchDB has adopted it.  It's just one more reason why
CouchDB rocks.

So much more
------------

I could talk about how it can handle 2,500 concurrent requests in 10mb of
resident memory usage.  I could talk about its pluggable view server backends,
so that instead of writing views in JavaScript you can write them in Python or
any other language (given the correct bindings).  I could talk about CouchDBX_,
which makes installing it on the Mac, quite literally, one click.  I could even
talk about how it's written in Erlang, with an eye towards scalability.  Or
maybe about how its database store is append-only.

I could talk about any of those things, and more.  It just comes down to this:
CouchDB rocks.  But don't take my word for it--try it out for yourself!

.. _`Why CouchDB Sucks`: http://www.eflorenzano.com/blog/post/why-couchdb-sucks/
.. _CouchDB: http://incubator.apache.org/couchdb/
.. _`lifestreaming application`: http://github.com/ericflo/django-couch-lifestream/tree/master
.. _`it does`: http://wiki.apache.org/couchdb/Basics
.. _nginx: http://wiki.codemongers.com/Main
.. _perlbal: http://www.danga.com/perlbal/
.. _varnish: http://varnish.projects.linpro.no/
.. _`whole web apps served only from CouchDB`: http://jchris.mfdz.com/code/2008/11/my_couch_or_yours__shareable_ap
.. _`Brian Aker`: http://krow.livejournal.com/622006.html
.. _Drizzle: http://drizzle.org/wiki/Main_Page
.. _`Map/Reduce`: http://labs.google.com/papers/mapreduce.html
.. _Brian: http://krow.livejournal.com/622006.html
.. _CouchDBX: http://jan.prima.de/~jan/plok/archives/142-CouchDBX-Revival.html