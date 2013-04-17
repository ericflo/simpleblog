---
layout: post
title: "Interesting Discussion, Nginx"
date: 2007-08-08T00:09:21-05:00
comments: false
categories: [Eflorenzano.com, Django, Python, Templating, nginx]
published: true
alias: [/blog/post/interesting-discussion-nginx]
---

`Very interesting discussion`_ going on right now about Django's templating language and whether to split it off into its own separate library.  One of the justifications is that it will "feel" easier to plug in other template languages into Django itself.  Funny how `I just blogged about how easy this is already`_.

Also, previously this site was run with apache2 and perlbal.  Now it's running apache2 and nginx.  At some point I'm going to make the switch to having all of the media pointing to an nginx-only server which short circuits the mod_python (also soon to be mod_wsgi, lol) handlers altogether.

Sorry that this is another in a line of short posts, but I expect this trend will continue as I move twice in the next 2 weeks.  Crazy stuff happening in my life right now!

.. _`Very interesting discussion`: http://groups.google.com/group/django-developers/browse_thread/thread/37801d8c2f46a313/a002ad9645e64e0a#a002ad9645e64e0a
.. _`I just blogged about how easy this is already`: http://www.eflorenzano.com/blog/cheetah-and-django/