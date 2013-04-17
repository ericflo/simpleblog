---
layout: post
title: "Spawning + Django"
date: 2008-07-30T23:51:17-05:00
comments: false
categories: [Python, Django, Eventlet, Spawning]
published: true
alias: [/blog/post/spawning-django]
---

Yesterday `Donovan Preston`_ released new versions of both eventlet_ and Spawning_.  What are those, you ask?  Eventlet_ is a networking library written using coroutines instead of normal subroutes, which makes writing networked non-blocking IO applications much much simpler.  Spawning is a WSGI_ server, written using eventlet_, which supports all of the things you'd expect of a good WSGI_ server: multiple processes, multiple threads, etc.

Considering that I sit next to Donovan at work all day, I've overheard him extolling the numerous advantages to using a server such as Spawning_--the most obvious of which is completely graceful code reloading.  Donovan has given a presentation explaining how all of this works, the `slides of which`_ probably explain it better than I could.  When he told me that he'd added the ability to easily run Django apps with Spawning, I decided to check it out.

First, I installed spawning:

.. code-block:: bash

    sudo easy_install Spawning

And away setuptools went and installed all of the prerequisites and the package itself.  (I have had problems with this in the past, but grabbing greenlet, eventlet, simplejson, PasteDeploy, and Spawning and installing them individually does the trick).

The next thing to do is go to the directory which holds your settings.py, or at least make setup.py available on the Python path.  I tend to find it easier to just go to the directory.  Then type the following:

.. code-block:: bash

    spawn --factory=spawning.django_factory.config_factory settings --port 9090 -s 4 -t 100

This starts up a Spawning server with 4 processes and 100 threads.  I chose those numbers almost completely arbitrarily.  (Well, that's not entirely true, my Apache setup previously had 4 processes and 100 requests per child.  I know that requests per child doesn't map at all to threads, but that's where I got the number.)  The next thing to do is visit your site, but instead of visiting the normal port 80 or 8000, visit port 9090.  If you're running it on your own box, that should be http://127.0.0.1:9090/.

For me, it worked like a charm.  It felt like my server was responding faster than ever, but at that point it was just a feeling.  To get some quantitative analysis, I ran apachebench_ with 20 concurrent requests for a total of 10000 requests.  On my Apache + mod_wsgi_ setup, I got **235.65** requests per second.  That was really good, I thought!  However, with the Spawning setup, I got **347.20** requests per second.  I would need to test this much more in-depth if I were a statistician, but it's good enough for me as it did confirm my qualitative analysis.

If you're viewing this on my website directly, then you've already used Spawning, as I've switched over this blog to use the new server.  Let me know what you think!  Has my site slowed to a crawl?  Is it going faster than ever (because I know everyone remembers the speed at which eflorenzano.com loads)?

In all, it was an extremely easy upgrade.  I would recommend that everyone who has an interest in these types of things at least try it--especially if you're looking into other pure-python WSGI servers like CherryPy_.

**UPDATE**: If you were having troubles reaching the site before, it's because I was having problems with my database due to another app on the same server, not due to anything that Spawning was doing wrong.

.. _`Donovan Preston`: http://ulaluma.com/pyx/
.. _eventlet: http://pypi.python.org/pypi/eventlet/0.7
.. _Spawning: http://pypi.python.org/pypi/Spawning/0.7
.. _Eventlet: http://pypi.python.org/pypi/eventlet/0.7
.. _WSGI: http://www.wsgi.org/wsgi/
.. _`slides of which`: http://soundfarmer.com/content/slides/coroutines-nonblocking-io-eventlet-spawning/coros,%20nonblocking%20i:o,%20eventlet,%20spawning.pdf
.. _apachebench: http://en.wikipedia.org/wiki/ApacheBench
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _CherryPy: http://www.cherrypy.org/