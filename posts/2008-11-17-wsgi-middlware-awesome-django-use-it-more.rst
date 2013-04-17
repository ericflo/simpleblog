---
layout: post
title: "WSGI middleware is awesome, and Django should use it more"
date: 2008-11-17T21:26:48-06:00
comments: false
categories: [Python, Django, Programming, WSGI, Repoze]
published: true
alias: [/blog/post/wsgi-middlware-awesome-django-use-it-more]
---

Most people in the Django community are deploying their apps these days with
`mod_wsgi`_.  If not, then you're at least using WSGI_ as a communication layer
with your application server, in one way or another.  The great thing about
WSGI is that it gives everyone a common interface through which to talk.  It
also has the added benefit of being a common abstraction that many people have
built these great, really useful tools on top of.

Consider Repoze_.  If you navigate to the `middleware section`_ of their
website, they have some really cool stuff available!  There are utilities for
logging, authentication, security, profiling, templating, etc.  All of these
pieces of middleware are designed to be totally pluggable, because they are
designed to work solely based on what's available through WSGI.

My personal favorite of that lot is ``repoze.profile``.  It accumulates
Python profiling information about whatever app is being run, and allows you to
view that profile information via a web interface by visiting a special URL.
There is absolutely no reason that the Pylons, TurboGears, or CherryPy guys
should be able to get away with keeping this stuff for themselves, so I want to
show just how easy it is to integrate this profiling module with Django.

First, though, here's a typical .wsgi file that might be used in conjunction
with ``mod_wsgi``:

.. code-block:: python

    import os, sys
    sys.stdout = sys.stderr

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()

There's really nothing special going on here, and if you would like to learn
more about how to set up this WSGI file, visit
`mod_wsgi's documentation on the subject`_.  Now if you'll notice,
``application`` is simply an instance of ``WSGIHandler``, which is simply a
callable.  A WSGI middleware is just a wrapper around that callable.  Here's how
easy it is to add the profiling middleware:

.. code-block:: python

    from repoze.profile.profiler import AccumulatingProfileMiddleware
    application = AccumulatingProfileMiddleware(
        application,
        log_filename='/tmp/djangoprofile.log',
        discard_first_request=True,
        flush_at_shutdown=True,
        path='/__profile__')

There we go!  We have imported the profiling middleware, and passed the Django
WSGI application as the first argument.  The rest is just setting options for
the middleware.  You can restart apache and the WSGI profiling middleware is
already working.

Sometimes, though, you don't want all of Apache just to run some middleware.
You want to be able to do the same thing, but locally.  Believe it or not,
Django's local development server is just a WSGI server itself, so one option
would be to do the wrapping directly in django, `right here`_.  But you really
don't want to be hacking inside of Django internals if you don't have to.
Fortunately there are many alternative WSGI servers out there.  Brian Rosner
has created a custom management command to use the excellent CherryPy WSGI
server with Django, on `his blog`_.

Let's say you just want to try this out quickly after reading this blog post,
though.  If you're running Python 2.5 or greater, you're in luck, because a
script less than 10 lines long can get you up and running:

.. code-block:: python

    #!/usr/bin/env python

    import sys
    from wsgiref.simple_server import make_server

    if __name__ == "__main__":
        execfile(sys.argv[1])
        httpd = make_server('', 8000, application)
        httpd.serve_forever()

Now, to run it, simply invoke it like this:

.. code-block:: bash

    python runserver.py my_wsgi_file.wsgi

Now, navigate around your app for a little bit and then point your browser to
`the profile url`_ and see how freaking awesome middleware can be.

I'm not trying to stir up any controversy, I'm not saying we should stop making
Django middleware or anything like that.  But I seriously, seriously hope that
someone tries this out and realizes the multitudes of great WSGI apps out there
that can be taken advantage of.  `Mark Ramm`_ wasn't full of hot air when he
talked about this at DjangoCon or `blogged about it`_ later.  He was right, and
I for one wish I had listened sooner.

.. _`mod_wsgi`: http://code.google.com/p/modwsgi/
.. _WSGI: http://wsgi.org/wsgi/
.. _Repoze: http://repoze.org/
.. _`middleware section`: http://repoze.org/repoze_components.html#middleware
.. _`mod_wsgi's documentation on the subject`: http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
.. _`right here`: http://code.djangoproject.com/browser/django/trunk/django/core/management/commands/runserver.py#L60
.. _`his blog`: http://oebfare.com/blog/2008/nov/03/writing-custom-management-command/
.. _`the profile url`: http://localhost:8000/__profile__
.. _`Mark Ramm`: http://compoundthinking.com/blog/
.. _`blogged about it`: http://compoundthinking.com/blog/index.php/2008/10/06/wsgi-middleare-is-cool/