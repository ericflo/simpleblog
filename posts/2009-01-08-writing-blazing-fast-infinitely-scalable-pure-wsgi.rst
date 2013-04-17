---
layout: post
title: "Writing Blazing Fast, Infinitely Scalable, Pure-WSGI Utilities"
date: 2009-01-08T04:29:10-06:00
comments: false
categories: [Python, Django, Scalability, WSGI]
published: true
alias: [/blog/post/writing-blazing-fast-infinitely-scalable-pure-wsgi]
---

Lately I've really fallen in love with writing utilities whose interface is
simply HTTP.  By making it accessible via HTTP, it's really easy to write
clients that talk to the utility and, if the need arises, there are lots of
tools that already exist for doing things with HTTP, like load balancing and
caching, etc.

While it would be easy to use a framework to build these utilities, lately I've
been choosing not to do so.  Web frameworks like Django_ and Pylons_ are great
when you need to build a fully-featured web application that will be accessible
by people.  When it will only be computers talking to the service, however, a
lot of the machinery provided by frameworks is unneeded and will only slow your
utility down.  Instead of using a framework, we're going to write a pure WSGI_
application.

An Example: Music Discovery Website
------------------------------------

This has all been very abstract, so let's take an example: Suppose you run a
music discovery website that lets you play songs online.  Next to each song, you
simply want to display how many times the song has been played.

One solution to that problem could be to have a ``play_count`` column on the
table where the song metadata is stored.  Every time someone plays the song, you
could issue an ``UPDATE`` on the row and increase the ``play_count`` by one.
This solution will work while your site is small, but as more and more people
begin using the application, the number of writes to your database is going to
kill its performance.

A much more robust and scalable solution is to append a new line to a text
log file every time a song is played, and have a process run regularly to scoop
up all of the log files and update those ``play_count`` fields in the database.

However, even if you have that regular process run once every hour, there's
still too great a lag time between when a user takes an action and when they see
the results of that action.  This is where our WSGI utility comes into play. It
can serve as a realtime play counter to count the plays in between the time when
the logs are analyzed and the ``play_count`` columns updated.

Song Play Counter
------------------

We can design the interface for our WSGI song play counter utility any way that
we like, but I'm going to try to keep it as RESTful_ as I can.  The interface
will look like this:

* ``GET /song/SONGID`` will return the current play count of the given song
* ``POST /song/SONGID`` will increment the play count of the given song by one, and return its new value
* ``GET /`` will return a mapping of all songs registered to their respective play counts
* ``DELETE /`` will clear the whole mapping

So let's get started.  First, I always like to start with a very basic skeleton:

.. code-block:: python

    def application(environ, start_response):
        start_response('200 OK', [('content-type', 'text/plain')])
        return ('Hello world!',)

This does what you would imagine, returns ``Hello world!`` to each and every
request that it receives.  Not very useful, so let's make it more interesting:

.. code-block:: python

    from collections import defaultdict
    counts = defaultdict(int)

    def application(environ, start_response):
        global counts
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if path.startswith('/song/'):
            song_id = path[6:]
            if method == 'GET':
                start_response('200 OK', [('content-type', 'text/plain')])
                return (str(counts[song_id]),)
            elif method == 'POST':
                counts[song_id] += 1
                start_response('200 OK', [('content-type', 'text/plain')])
                return (str(counts[song_id]),)
            else:
                start_response('405 METHOD NOT ALLOWED', [('content-type', 'text/plain')])
                return ('Method Not Allowed',)
        start_response('404 NOT FOUND', [('content-type', 'text/plain')])
        return ('Not Found',)

We've now added the data structure that we're using to keep track of the counts,
which in this case is a ``defaultdict(int)``.  We're also now looking at the
request path and method, as well.  If it's a GET starting with /song/, we look
up the count and return it, and if it's a POST starting with /song/, we
increment it by one before returning it.  Also, we're doing the proper thing if
we detect a method that's not allowed: we're returning HTTP error code 405.

Now let's add the final bit of functionality:

.. code-block:: python

    from collections import defaultdict
    counts = defaultdict(int)

    def application(environ, start_response):
        # ... start of app
        if path.startswith('/song/'):
            # ... song-specific logic
        elif path == '/':
            if method == 'GET':
                res = ','.join(['%s=%s' % (k, v) for k, v in counts.iteritems()])
                start_response('200 OK', [('content-type', 'text/plain')])
                return (res,)
            elif method == 'DELETE':
                counts = defaultdict(int)
                start_response('200 OK', [('content-type', 'text/plain')])
                return ('OK',)
            else:
                start_response('405 METHOD NOT ALLOWED', [('content-type', 'text/plain')])
                return ('Method Not Allowed',)
        # ... rest of app

We've done basically the same thing here as we did with the previous example: we
are looking at the request path and method and doing the appropriate action.
There really is nothing very tricky going on here.  We're inventing our own
format for the case where we return the counts for all songs, but it's nothing
that will be hard to parse.

**NOTE:** Generally you would want to use some sort of threading lock primitive
before accessing a global dictionary like this.  I will be using Spawning_ to
run this WSGI_ application, with a threadpool size of 0 to use cooperative
coroutines instead of standard threads, so I am able to get away without locks
for this application.  To install Spawning_ for yourself, just type:

.. code-block:: bash

    sudo easy_install Spawning

Running the Utility
--------------------

Let's just take a quick look at how this utility works, from the command line:

.. code-block:: bash

    $ spawn -t 0 -p 8000 counter.application

...and in another window:

.. code-block:: bash

    $ curl http://127.0.0.1:8000/song/1
    0
    $ curl -X POST http://127.0.0.1:8000/song/1
    1
    $ curl http://127.0.0.1:8000/song/1
    1
    $ curl -X POST http://127.0.0.1:8000/song/5
    1
    $ curl -X POST http://127.0.0.1:8000/song/5
    2
    $ curl http://127.0.0.1:8000/
    1=1,5=2
    $ curl -X DELETE http://127.0.0.1:8000/
    OK

As you can see, it seems to be working correctly. The play counter is behaving
as expected.

Writing a Client to Talk to our Utility
----------------------------------------

Now that we have our WSGI utility written to keep track of the counts on our
songs, we should write a client library to communicate with this server.

.. code-block:: python

    import httplib

    class CountClient(object):
        def __init__(self, servers=['127.0.0.1:8000']):
            self.servers = servers
        
        def _get_server(self, song_id):
            return self.servers[song_id % len(self.servers)]
        
        def _song_request(self, song_id, method):
            conn = httplib.HTTPConnection(self._get_server(song_id))
            conn.request(method, '/song/%s' % (song_id,))
            resp = conn.getresponse()
            play_count = int(resp.read()) 
            conn.close()
            return play_count
        
        def get_play_count(self, song_id):
            return self._song_request(song_id, 'GET')
        
        def increment_play_count(self, song_id):
            return self._song_request(song_id, 'POST')
        
        def get_all_play_counts(self):
            dct = {}
            for server in self.servers:
                conn = httplib.HTTPConnection(server)
                conn.request('GET', '/')
                counts = conn.getresponse().read()
                conn.close()
                if not counts:
                    continue
                dct.update(dict([map(int, pair.split('=')) for pair in counts.split(',')]))
            return dct
        
        def reset_all_play_counts(self):
            status = True
            for server in self.servers:
                conn = httplib.HTTPConnection(server)
                conn.request('DELETE', '/')
                resp = conn.getresponse().read()
                if resp != 'OK':
                    status = False
                conn.close()
            return status

What we have here is a simple class that converts Python method calls to the
RESTful HTTP equivalents that we have written for our WSGI utility.  The best
part about this setup, though, is that it uses a hash based on the song_id to
determine which server to connect to.  If you only ever do per-song operations,
this setup is quite literally infinitely scalable.  You could have thousands of
servers keeping track of song counts, none of them knowing about each other.
Since the decision about which server to talk to happens on the client side,
there needs to be no communication between the servers whatsoever.

However, if you start to use the ``get_all_play_counts`` and
``reset_all_play_counts``, then eventually after many many servers are added it
will start to get slower.

Let's explore this client:

.. code-block:: pycon

    >>> from countclient import CountClient
    >>> c = CountClient()
    >>> c.get_play_count(1)
    0
    >>> c.increment_play_count(1)
    1
    >>> c.increment_play_count(1)
    2
    >>> c.get_play_count(1)
    2
    >>> c.increment_play_count(5)
    1
    >>> c.get_all_play_counts()
    {1: 2, 5: 1}
    >>> c.reset_all_play_counts()
    True
    >>> c.get_all_play_counts()
    {}

Benchmarks!
-----------

I'm not a benchmarking nut in any way, shape, or form these days.  However, in
Python it's quite tough to beat pure-WSGI applications for raw speed.  Using my
MacBook Pro with a 2.5GHz Intel Core 2 Duo and 2 GB 667 MHz DDR2 SDRAM I got
these results from ApacheBench::

    e:Desktop ericflo$ ab -n 10000 http://127.0.0.1:8000/song/1
    ...
    Concurrency Level:      1
    Time taken for tests:   7.792 seconds
    Complete requests:      10000
    Failed requests:        0
    Write errors:           0
    Total transferred:      1020000 bytes
    HTML transferred:       10000 bytes
    Requests per second:    1283.31 [#/sec] (mean)
    Time per request:       0.779 [ms] (mean)
    Time per request:       0.779 [ms] (mean, across all concurrent requests)
    Transfer rate:          127.83 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.1      0       2
    Processing:     0    1   0.8      1      43
    Waiting:        0    1   0.5      0      43
    Total:          1    1   0.8      1      43

Take these results with a huge grain of salt, but suffice it to say, it's fast.
It would probably be even faster using `mod_wsgi`_ instead of Spawning_.

Drawing Conclusions From This Exercise
---------------------------------------

I don't want to misconstrue my standpoint on this: frameworks definitely have
their place.  There's no way you would want to write an entire user-facing
application with pure WSGI unless you were using lots of middleware and stuff
and at some point you're just recreating Pylons_.  But when you're writing a
HTTP utility like we did here, then I think that pure-WSGI is the way to go.

I'd like to touch on one more nice side effect of using pure-WSGI: You can run
it in any application server that supports WSGI.  That means
`Google App Engine`_, Apache, Spawning, CherryPy, and many other containers. It
can easily be served by pure python so even on very restrictive shared hosting
it's possible to run your utility.

What do you think of pure-WSGI utilities?  Are you using them in your app? I'd
love to hear about it--leave me a comment and tell me your thoughts on this
subject.

.. _Django: http://www.djangoproject.com/
.. _Pylons: http://pylonshq.com/
.. _WSGI: http://wsgi.org/wsgi/
.. _RESTful: http://en.wikipedia.org/wiki/Representational_State_Transfer
.. _Spawning: http://pypi.python.org/pypi/Spawning/0.7
.. _`mod_wsgi`: http://code.google.com/p/modwsgi/
.. _`Google App Engine`: http://code.google.com/appengine/