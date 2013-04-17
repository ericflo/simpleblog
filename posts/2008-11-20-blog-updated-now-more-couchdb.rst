---
layout: post
title: "Blog Updated (now with more CouchDB)"
date: 2008-11-20T23:56:20-06:00
comments: false
categories: [Eflorenzano.com, Django, Programming, Python]
published: true
alias: [/blog/post/blog-updated-now-more-couchdb]
---

I posted a while back about `using CouchDB with Django`_, talking about how one might build a lifestreaming application combining the flexibility and power of CouchDB_ with the ease of use and utility of Django_.  I even linked to `the project on github`_.  At the time I was taking a hard look at the Django-based software that was running this blog.  It needed some work, to say the least.  So I did a bit of cleanup, a LOT of reorganization, and integrated this CouchDB-based lifestreaming application into the mix.

There's no visual refresh--that will come some other time.  For right now, it's just a backend refresh, so for the most part nobody will notice anything.  But I can rest much easier knowing that the backend is just a little bit less of a mess.  It's also a LOT easier to deploy.  I've integrated a Fabric_ deployment script so that all I need to do is type:

.. code-block:: bash

    fab deploy

And everything gets zipped up, sent to the server, unziped, and all of the relevant processes get restarted.  Pretty cool!  That's going to allow for much more rapid iteration on the site, so changes can come more often and bugs can be fixed.

Because of that, expect more experimentation.  As I'm experimenting with Django stuff, I'll do a lot more public demos where the experimentations are public for the world to see and play around with.  I've got lots of ideas for Django-y experiments and it's going to be really fun to see how they shape up.

So what do you think?  Is the new lifestreaming stuff annoying or cool?

.. _`using CouchDB with Django`: http://www.eflorenzano.com/blog/post/using-couchdb-django/
.. _CouchDB: http://incubator.apache.org/couchdb/
.. _Django: http://www.djangoproject.com/
.. _`the project on github`: http://github.com/ericflo/django-couch-lifestream/tree/master
.. _Fabric: http://www.nongnu.org/fab/