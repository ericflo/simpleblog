---
layout: post
title: "The Technology Behind Convore"
date: 2011-02-16T14:29:35-06:00
comments: false
categories: [Django, Python, PostgreSQL, Convore, Realtime, Redis, Haystack, Solr, Eventlet]
published: true
alias: [/blog/post/technology-behind-convore]
---

We launched Convore_ last week, and the first question developers tend to ask
when they find Convore_ is "what technology powers this site?"  It is asked so
often, in fact, that we have started to copy and paste the same short response
again and again.  That response was good enough to satisfy people who simply
wanted to know if we were Rails or Django, or whether we were using node.js for
the real-time stuff, but this article will expand upon that--  not only giving
more details for the curious, but also giving us a link to point people at when
they ask the question in the future.  I always wish other people were totally
open about their architectures, so that I can learn from their good choices and
their bad, so I'd like to be as open as possible about ours.  Let's dive in!

The basics
----------

All of our application code is powered by Python.  Our front-end html page
generation is done by Django, which we use in a surprisingly traditional way
given the real-time nature of Convore as a product.  Everything is assembled
at once: all messages, the sidebar, and the header are all rendered on the
server instead of being pulled in after-the-fact with JavaScript.  All of the
important data is canonically stored in PostgreSQL, including messages, topics,
groups, unread counts, and user profiles.  Search functionality is provided by
Solr, which is interfaced into our application by way of the handy Haystack
Django application.


The message lifecycle
---------------------

When a new message comes into the system, first it's parsed by a series of
regular expressions designed to pull out interesting bits of information from
the message.  Right now all we're looking for is username references and
links (and further, whether those links point at images which should be
rendered in-line.)  At the end of this parsing stage, we have a structured
message parse list, which is converted into JSON.

So, for example if someone posted the message:

.. code-block:: text

    @ericflo @simonw Here's how we connect/disconnect from Redis in production: http://dpaste.com/406797/

The resulting JSON parse list would look like this:

.. code-block:: text

    [
        {
            "type": "username",
            "user_id": 1, 
            "username": "ericflo",
            "markup": "<a href=\"/users/ericflo/\">@ericflo</a>"
        }, 
        {
            "type": "username", 
            "user_id": 56, 
            "username": "simonw",
            "markup": " <a href=\"/users/simonw/\">@simonw</a>"
        }, 
        {
            "type": "text",
            "markup": " Here&#39;s how we connect/disconnect from Redis in production: "
        }, 
        {
            "type": "url", 
            "url": "http://dpaste.com/406797/",
            "markup": "<a href=\"http://dpaste.com/406797/\" target=\"_blank\">http://dpaste.com/406797/</a>"
        }
    ]

After this is constructed, we log all our available information about this
message, and then save to the database--  both the raw message as it was received,
and the JSON-encoded parsed node list.

Now a task is sent to Celery (by way of Redis) notifying it that this new
message has been received.  This Celery task now increments the unread count
for everyone who has access to the topic that the message was posted in, and
then it publishes to a Redis pub/sub for the group that the message was posted
to.  Finally, the task scans through the message, looking for any users that
were mentioned in the message, and writes entries to the database for every
mention.

On the other end of that pub/sub are the many open http requests that our users
have initiated, which are waiting for any new messages or information.  Those
all simultaneously return the new message information, at which point they
reconnect again, waiting for the next message to arrive.


The real-time endpoint
----------------------

Our live updates endpoint is actually a very simple and lightweight pure-WSGI
Python application, hosted using Eventlet.  It spawns off a coroutine for each
request, and in that coroutine, it looks up all the groups that a user is a
member of, and then opens a connection to Redis subscribing to all of those
channels.  Each of these Eventlet-hosted Python applications has the ability to
host hundreds-to-thousands of open connections, and we run several instances
on each of our front-end machines.  It has a few more responsibilities, like
marking a topic as read before it returns a response, but the most important
thing is to be a bridge between the user and Redis pub/sub.


Future improvements
-------------------

There are so many places where our architecture can be improved.  This is our
first version, and now that real users are using the system, already some of
our initial assumptions are being challenged.  For instance, we thought that
pub/sub to a channel per group would be enough, but what that means is that
everyone in a group sees the exact same events as everyone else in that group.

This means we don't have the ability to customize each user's experience based
on their preferences--no way to put a user on ignore, filter certain messages,
etc.  It also means that we aren't able to sync up a user's experience across
tabs or browsers, since we don't really want to broadcast to everyone in the
group that one user has visited a topic, thereby removing any unread messages
in that topic.  So going forward we're going to have to break up that per-group
pub/sub into per-user pub/sub.

Another area that could be improved is our unread counts.  Right now they're
stored as rows in our PostgreSQL database, which makes it extremely easy to
batch update them and do aggregate queries on them, but the number of these
rows is increasing rapidly, and without some kind of sharding scheme, it will
at some point become more difficult to work with such a large amount of rows.
My feeling is that this will eventually need to be moved into a non-relational
data store, and we'll need to write a service layer in front of it to deal with
pre-aggregating and distributing updates, but nothing is set in stone just yet.

Finally, Python may not be the best language for this real-time endpoint.
Eventlet is a fantastic Python library and it allowed us to build something
extremely fast that has scaled to several thousand concurrent connections
without breaking a sweat on launch day, but it has its limits.  There is a
large body of work out there on handling a large number of open connections,
using Java's NIO framework, Erlang's mochiweb, or node.js.


That's all folks
----------------

We're pretty proud of what we've built in a very short time, and we're glad
it has held up as well as it has on our launch day and afterwards.  We're
excited about the problems we're now being faced with, both scaling the
technology, and scaling the product.  I hope this article has quenched any
curiosity out there about how Convore works.  If there are any questions,
feel free to join Convore_ and ask away!

(Or discuss it `on Hacker News`_)

.. _Convore: https://convore.com/
.. _`on Hacker News`: http://news.ycombinator.com/item?id=2228137