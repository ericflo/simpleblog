---
layout: post
title: "Hosting a Django Site with Pure Python"
date: 2008-02-22T14:47:48-06:00
comments: false
categories: [CherryPy, Django, Programming, Python]
published: true
alias: [/blog/post/hosting-django-site-pure-python]
---

Developing a site with Django is usually a breeze.  You've set up your models, created some views and used some generic views, and you've even created some spiffy templates.  Now it's time to publish that site for everyone to see.  Now if you're not already familiar with Apache, Lighttpd, or Nginx, you're stuck trying to figure out complicated configuration files and settings directives.  "Why can't deployment be just as easy as running the development server?", you scream.

It's tempting to just attempt to use the development server in production.  But then you read the documentation (you do read the documentation, right?) and it clearly says:

    DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or 
    performance tests. (And that--  s how it--  s gonna stay. We--  re in the business of making Web 
    frameworks, not Web servers, so improving this server to be able to handle a production 
    environment is outside the scope of Django.)

Looks like it's time to fire up Apache, right?  Wrong.  At least, you don't have to.

CherryPy to the Rescue
----------------------

One of the features that CherryPy_ touts quite highly is that they include ``"A fast, HTTP/1.1-compliant, WSGI thread-pooled webserver"``, however a lesser known fact about that webserver is that it can be run completely independently of the rest of CherryPy--it's a standalone WSGI server.

So let's grab a copy of the CherryPy WSGI webserver:

.. code-block:: bash

    wget http://svn.cherrypy.org/trunk/cherrypy/wsgiserver/__init__.py -O wsgiserver.py

Now that you've got a copy of the server, let's write a script to start it up.  Your choices may vary depending on how many threads you want to run, etc.

.. code-block:: python

    import wsgiserver
    #This can be from cherrypy import wsgiserver if you're not running it standalone.
    import os
    import django.core.handlers.wsgi
    
    if __name__ == "__main__":
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        server = wsgiserver.CherryPyWSGIServer(
            ('0.0.0.0', 8000), 
            django.core.handlers.wsgi.WSGIHandler(),
            server_name='www.django.example',
            numthreads = 20,
        )
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()

Consequences
------------

Now you've got the server up and running, lets talk about some consequences of this approach.

1.  This is a multithreaded server.  Django is not guaranteed to be completely thread safe.  Many people seem to be running it fine in multithreaded environments, but thread safety may break at any time without notice.  It might be an interesting project to convert cherrypy.wsgiserver to use processing_ instead of threading_ and see how the performance changes.

2. This server is written in Python, and as with any other Python program, it will be difficult for it to match the speed of pure C.  For exactly this reason, mod_wsgi_ is probably always going to be faster than this solution.

3. You can have a completely self-contained server environment that can be run on Mac, Windows, and Linux with only Python and a few Python libraries installed.  Distributing this wsgiserver.py script along with your Django project (or with a Django app, even) could be a great way of keeping the entire program self-contained.

Conclusion
----------

Would I use this instead of a fully-featured web server like Apache or Nginx?  Probably not.  I would, however, use it for an intranet which demands more performance and security than the built-in development server.  In any case, it's a nice nugget of information to have in your deployment toolbox.

.. _CherryPy: http://www.cherrypy.org/
.. _processing: http://pyprocessing.berlios.de/
.. _threading: http://www.python.org/doc/lib/module-threading.html
.. _mod_wsgi: http://code.google.com/p/modwsgi/