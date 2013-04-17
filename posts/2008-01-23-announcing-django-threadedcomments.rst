---
layout: post
title: "Announcing django-threadedcomments"
date: 2008-01-23T11:26:04-06:00
comments: false
categories: [Django, Digg, Programming, Python, Open Source, django-threadedcomments, Reddit]
published: true
alias: [/blog/post/announcing-django-threadedcomments]
---

Django-threadedcomments_ is a simple yet flexible threaded commenting system for Django.  What I mean when I say threaded is that commenters can reply not only to the original item, but to other comments as well.  It is very similar to what Reddit or Digg have in their comments sections.

The idea for this application started about a month and a half ago, when my good friend Tony Hauber asked if I would work with him on a project idea that he had (more info on this in the future).  One of the major components of the project would need to be threaded comments.  Naturally, the first thing that I did was attempt to make ``django.contrib.comments`` work for this purpose.  In the end, however, I kept running into problems which all basically boiled down to the fact that ``django.contrib.comments`` was never meant for this purpose.

So I used ``django.contrib.comments`` as a starting point, brought in some of the best features of the excellent django-comment-utils_ (In fact, django-threadedcomments_ actually provides a fair amount of compatiblity with the Managers from django-comment-utils), and added a bit of my own alchemy.  This is the result of those things.

A lot of effort has gone into documentation on this project: inline documentation, `a tutorial on setting it up with a blog`_, and `complete API documentation`_.  In fact, to see what you'll get after completing `the tutorial`_, head on over to `this page`_.  Please excuse my color scheme there--It's the comments that I'm trying to show off, not my design skills (or lack thereof).

If you're worried about the hassle of writing a script to migrate all of your ``django.contrib.comments`` comments to this new system, then fear not: there's an included migration script and you'll only need to run ``python manage.py migratecomments`` and the migration is automatically taken care of for you.

I really hope that this can be a useful tool for people looking to add a threaded commenting system to a project of theirs.  `Check it out`_ and see if it's right for you!

.. _Django-threadedcomments: http://code.google.com/p/django-threadedcomments/
.. _django-comment-utils: http://code.google.com/p/django-comment-utils/
.. _django-threadedcomments: http://code.google.com/p/django-threadedcomments/
.. _`a tutorial on setting it up with a blog`: http://api.rst2a.com/1.0/rst2/html?uri=http%3A//django-threadedcomments.googlecode.com/svn/trunk/docs/tutorial.txt&style=zope
.. _`complete API documentation`: http://api.rst2a.com/1.0/rst2/html?uri=http%3A//django-threadedcomments.googlecode.com/svn/trunk/docs/api.txt&style=zope
.. _`the tutorial`: http://api.rst2a.com/1.0/rst2/html?uri=http%3A//django-threadedcomments.googlecode.com/svn/trunk/docs/tutorial.txt&style=zope
.. _`this page`: http://www.eflorenzano.com/threadedcomments/example/
.. _`Check it out`: http://code.google.com/p/django-threadedcomments/