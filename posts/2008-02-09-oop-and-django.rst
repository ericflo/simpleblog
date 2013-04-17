---
layout: post
title: "OOP and Django"
date: 2008-02-09T01:06:52-06:00
comments: false
categories: [Django, Python, Object Oriented Programming]
published: true
alias: [/blog/post/oop-and-django]
---

Being a senior in college means many things.  It means job interviews and upper-level classes, emotional instability and independent living.  It also means countless hours of sitting in uninteresting classes whose sole purpose is to fulfill some graduation requirement.  For me, that means lots of daydreaming--about anything other than that class.  Recently however, during one daydream, I had a brain wave worth typing up: What's the deal with Object-Oriented Programming and Django?

The Convention
--------------

Browsing through the ``views.py`` file in just about any publicly-available Django-based application will almost certainly reveal nothing more than a bunch of functions.  These functions are undeniably specialized: they take in an ``HttpRequest`` object (plus possibly some more information), and they return an ``HttpResponse`` object.  Although these functions may be specialized, nevertheless they are still just functions.

This should come as no surprise to anyone who has used the framework--in fact, it's encouraged by common convention!  Not only does `the tutorial`_ use plain functions for views, but also the `Django Book`_, and just_ about_ every_ other_ application_ out_ there_.  The question now becomes "why"?  Why, in a language that seems to be "objects all the way down", does a paradigm emerge for this domain (Django views) wherein functions are used almost exclusively in lieu of objects?

That's not entirely true, sir...
--------------------------------

Any time a broad statement like "just about any" is used, the exceptions are what become interesting.  The admin application (both newforms-admin and old) is probably the most notable and interesting exception to my earlier broad statement.  It's interesting because it's Django's shining star!  Other applications which use object orientation: databrowse and formtools.  These are some great Django apps which use Object-Orientation in the views.

Looking at those apps which use OOP and those which don't reveals an interesting idea: those apps which strive to go above-and-beyond in terms of modularity tend to be those who end up using classes and their methods for views.  Now this same functionality could be accomplished by using plain functions, but they haven't--their functionality was accomplished using classes and methods.

Please keep in mind that what I'm not trying to do is make a value judgement on Object-Oriented programming vs. functional programming vs. any other `programming paradigm`_.  Instead, I'm providing an observation about the emergence of a common practice, and trying to analyze its implications.

But wait!
---------

What really is the difference between writing a plain function as a view and Object-Oriented programming?  It's completely reasonable to argue that writing a plain function for a view **is**, in fact, Object-Oriented programming.  All class methods take in self as their first positional argument, and all views take in request as their first positional argument.  Taking in this argument allows access to state which would otherwise be difficult to access.  Changing the order of urlpatterns is equivalent to changing the polymorphic properties of a class and dynamic method lookup.  

In essence, one could argue that **using a plain function as a view is strictly equivalent to writing a method on the HttpRequest object**.  Thinking about it in this way, writing a Django application is really nothing more than building up a monolithic ``HttpRequest`` object which the user can call different methods on using its API: the URL.  To me, this is a really interesting idea!  

Off My Rocker
-------------

This is the result of extreme classroom boredom--so maybe posts here will continue down this slightly-more-esoteric road for a while.  But honestly this was an interesting thought-experiment, and I'd like to get some feedback on what people think as well.   Am I totally off base with this analysis?  Moreover, do you use true Python "classes" as your views?  If so, what benefits does it bring to the table?

.. _`the tutorial`: http://www.djangoproject.com/documentation/tutorial03/
.. _`Django Book`: http://djangobook.com/en/1.0/chapter08/
.. _just: http://code.google.com/p/django-voting/
.. _about: http://code.google.com/p/django-registration/
.. _every: http://code.google.com/p/django-profiles/
.. _other: http://code.google.com/p/django-tagging/
.. _application: http://code.google.com/p/django-openid/
.. _out: http://code.google.com/p/django-threadedcomments/
.. _there: http://code.google.com/p/django-contact-form/
.. _`programming paradigm`: http://en.wikipedia.org/wiki/Programming_paradigm