---
layout: post
title: "My Thoughts on NoSQL"
date: 2009-07-21T08:44:17-05:00
comments: false
categories: [Databases, Editorial, NoSQL, Programming]
published: true
alias: [/blog/post/my-thoughts-nosql]
---

Over the past few years, relational databases have fallen out of favor for a
number of influential people in our industry.  I'd like to weigh in on that,
but before doing so, I'd like to give my executive summary of the events leading up to
this movement:

In the late nineties and early thousands, websites were mostly read-only--a
publisher would create some content and users would consume that content.
The data access patterns for these types of applications became very
well-understood, and as a result many tools were created and much research and
development was done to further develop these technologies.

As the web has grown more social, however, more and more it's the people
themselves who have become the publishers.  And with that fundamental shift
away from read-heavy architectures to read/write and write-heavy
architectures, a lot of the way that we think about storing and retrieving
data needed to change.

Most people have done this by relying less on the features provided by
traditional relational databases and engineering more database logic in their
application code.  Essentially, they stop using relational databases the way
they were intended to be used, and they instead use them as dumb data stores.

Other people have engineered new database systems from the ground up, each
with a different set of tradeoffs and differences from their relational
database brethren.  It's these new databases that have some in our industry
excited, and it's these databases that I'm going to focus on primarily in this
post.

(By the way, there's a whole lot more theory behind the movement away from
SQL.  Primarily of interest is the CAP theorem and the Dynamo paper.  Both of
these illustrate the necessary tradeoffs of between different approaches to
designing databases.)

Let's get this out of the way
------------------------------

I love SQL.  More than even that, I love my precious ORM and being able to
query for whatever information I want whenever I want it.  For the vast
majority of sites out there (we're talking 99.9% of the sites out there,
folks) it suits their needs very well, providing a good balance of ease of use
and performance.

There's no reason for them to switch away from SQL, and there's no way they
will.  If there's one thing I *don't* like about this whole NoSQL movement,
it's the presumption that everyone who's interested in alternative databases
hates the status quo.  That's simply not true.

But we're not talking about most sites out there, we're not talking about the
status quo, we're talking about the few applications that need something
totally different.

Tokyo Cabinet / Tokyo Tyrant
-----------------------------

Tokyo Cabinet (and its network interface, Tokyo Tyrant) is the logical
successor to Berkeley DB--a blazing fast, open-source, embeddable key-value
store that does just about what you would expect from its description.  It
supports 3 modes of operation: hashtable mode, b-tree mode, and table mode.

(Table mode still pretty much sucks, and I'm not convinced it's a good idea
for the project since it's added bloat and other systems like RDBMs are
probably better for storing tabular data, so I'm going to skip it.)

Essentially, the API into Tokyo Cabinet is that of a gigantic associative
array.  You give it a key and a value, and then later, given a key, it will
give you back the value you put in.  Its largest assets are that it's fast and
straightforward.

If your problem is such that you have a small to medium-sized amount of data,
which needs to be updated rapidly, and can be easily modeled in
terms of keys and values (almost all scenarios can be rewritten in terms of
keys and values, but some problems are easier to convert than others), then
Tokyo Cabinet and Tokyo Tyrant are the way to go.

CouchDB
--------

CouchDB is similar to Tokyo Cabinet in that it essentially maps keys to data,
but CouchDB's philosophy is completely different. Instead of arbitrary data,
its data has structure--it's a JSON object.  Instead of only being able to
query by keys, you can upload functions that index your data for you and then
you can call those functions.  All of this is done over a very simple REST
interface.

But none of this really matters.  None of these really set CouchDB apart,
because you could just encode JSON data and store it in Tokyo Cabinet, you can
maintain your own indexes of data fairly easily, and you can build a simple
REST API in a matter of days, if not hours.

What really sets CouchDB apart from the pack is it's innovative replication
strategy.  It was written in such a way that nodes which are disconnected for
long periods of time can reconnect, sync with each other, and reconcile their
differences in a way that no other database (since Lotus Notes?) could do.

It's functionality that allows for interesting and new distributed types of
applications and data that I think could possibly change the way we take our
applications offline.  I imagine that some day every computer will come with
CouchDB pre-installed and it'll be a data store that we use without even
knowing that we're using it.

However, I wouldn't choose it for a super high scalability site with lots of
data and sharding and replication and high availability and all those
buzzwords, because I'm not convinced it's the right tool for that job, but I
am convinced that its replication strategy will keep it relevant for years to
come.

Redis
------

Wow, looking at the bullet points this database seems to do just about
everything, perfectly!  Yeah, it's a bit prone to hyperbole and there are some
great things about it, but a lot of it is hot air.  For example, it claims to
support sharding but really all it does is have the client run a hash function
on its key and use that to determine which server to send its value to.  This
is something that any database can do.

When you get down to it, Redis is a key-value store which provides a richer
API than something like Tokyo Cabinet.  It does more operations in memory,
only periodically flushing to disk, so there's more of a risk that you could
lose data on a crash.  The tradeoff is that it's extremely fast, and it does
some neat things like allow you to append a value to the end of a list of
items already stored for a given key.

It also has atomic operations.  This is honestly the only reason I find this
project interesting, because the atomic operation support that it has means
that it can be turned into a best-of-breed tally server.  If you are building
a server to keep real-time counts of various things, you would be remiss to
overlook Redis as a very viable option.

Cassandra
----------

It's good to save the best for last, and that's exactly what I've done as I
find Cassandra to be easily the most interesting non-relational database out
there today.  Originally developed by Facebook, it was developed by some of
the key engineers behind Amazon's famous Dynamo database.

Cassandra can be thought of as a huge 4-or-5-level associative array, where
each dimension of the array gets a free index based on the keys in that level.
The real power comes from that optional 5th level in the associative array,
which can turn a simple key-value architecture into an architecture where you
can now deal with sorted lists, based on an index of your own specification.
That 5th level is called a SuperColumn, and it's one of the reasons that
Cassandra stands out from the crowd.

Cassandra has no single points of failure, and can scale from one machine to
several thousands of machines clustered in different data centers.  It has no
central master, so any data can be written to any of the nodes in the cluster,
and can be read likewise from any other node in the cluster.

It provides knobs that can be tweaked to slide the scale between consistency
and availability, depending on your particular application and problem domain.
And it provides a high availability guarantee, that if one node goes down,
another node will step in to replace it smoothly.

Writing about all the features of Cassandra is a whole different post, but I
am convinced that its data model is rich enough to support a wide variety of
applications while providing the kind of extreme scalability and high
availability features that few other databases can achieve--all while
maintaining a lower latency than other solutions out there.

Conclusion
----------

There are many other non-relational databases out there: HBase and Hypertable,
which are replicating Google's BigTable despite its complexity and problems
with single points of failure.  MongoDB is another database that has been
getting some traction, but it seems to be a jack of all trades, master of
none.  In short, the above databases are the ones that I find interesting
right now, and I would use each of them for different use cases.

What do you all think about this whole non-relational database thing?  Do you
agree with my thoughts or do you think I'm full of it?