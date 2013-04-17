---
layout: post
title: "Why CouchDB Sucks"
date: 2008-11-23T13:14:12-06:00
comments: false
categories: [CouchDB, Programming]
published: true
alias: [/blog/post/why-couchdb-sucks]
---

CouchDB_ really sucks at doing some things.  That should come as no surprise, as
every technology has its advantages and its drawbacks.  The thing is, when a new
technology comes out that looks really promising and cool, everyone writes about
all of its advantages, and none of its drawbacks.  Then, people start to use it
for things it isn't very good at, and they are disappointed.  In that spirit, I
would like to talk about some of the things that (in my experience) CouchDB is
absolutely not good at, and that you shouldn't try to use it for.

First, it doesn't support transactions in the way that most people typically
think about them.  That means, enforcing uniqueness of one field across all
documents is not safe.  A classic example of this would be enforcing that a
username is unique.  You can check whether a username exists, and if not, create
a new one.  There is no guarantee, however, that between the time that your app
has checked for its existence, and the time that you write the new user to the
database, that some other instance of your app hasn't beat you to that write.

Another consequence of CouchDB's inability to support the typical notion of a
transaction is that things like inc/decrementing a value and saving it back are
also dangerous.  Fortunately there aren't many instances that you would want to
simply inc/decrement some value where you couldn't just store the individual
documents separately and aggregate them with a view.

Secondly, CouchDB sucks at dealing with relational data.  If your data makes a
lot of sense to be in `3rd normal form`_, and you try to follow that form in
CouchDB, you're going to run into a lot of trouble.  Yes, it's probably possible
with tricks with view collations, but you're constantly going to be fighting
with the system.  If your data can be reformatted to be much more denormalized,
then CouchDB will work fine.

Thirdly, CouchDB sucks at being a data warehouse.  In every data warehouse that
I've ever run into, people have all kinds of different requests for how to slice
the data.  And they all want it to be done, yesterday.  The problem with this is
that temporary views in CouchDB on large datasets are really slow, because it
can't use any of its normal indexing tricks.  If you by some chance have a very
rigid way of looking at your data, using CouchDB and permanent views could work
quite well.  But in 99% of cases, a `Column-Oriented Database`_ of some sort is
a much better tool for the data warehousing job.

So does CouchDB suck?  No, it's by far my favorite new database technology on
the block.  What it's good at doing, it's *great* at doing, but that doesn't
mean that it should be used for everything.  With the kinds of scaling issues
that we're seeing with today's highly-interactive web applications, we need to
make use of a broad range of technologies, and use each one for its greatest
strengths.  That's called using the right tool for the job, and that's never
gone out of style.

.. _CouchDB: http://couchdb.org/
.. _`3rd normal form`: http://en.wikipedia.org/wiki/Third_normal_form
.. _`Column-Oriented Database`: http://en.wikipedia.org/wiki/Column-oriented_DBMS