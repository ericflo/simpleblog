---
layout: post
title: "Introducing django_simpleaggregation"
date: 2007-07-30T03:44:58-05:00
comments: false
categories: [Django, Python, SimpleAggregation]
published: true
alias: [/blog/post/introducing-django_simpleaggregation]
---

I have just released version 0.1 of a spinoff project I did today.  I've been working on a side project which I'm not ready to talk about yet, and one of the things that I have consistently  needed was simple aggregation on Django models.  Nothing complicated like what we'll start to see with the new aggregation framework, but just simple things like counts on objects based on the uniqueness of certain fields of a model.

So check that out: Here_  I'd really appreciate any feedback or comments you can give me.

So, that actually took quite a bit of time an energy to write, document, create a google project, package and upload, etc.  More time than I would have liked, but if it helps even one person, then it's worth it.

In other news, I have tried out mod_wsgi_ for Python and hosting my Django stuff, and WOW I must say that I'm quite impressed.  I haven't done any formal testing on it like `Graham Dumpleton, the creator, has done`_, but from my own informal observations I've noticed a good bump up in the snappiness of the app that I'm working on.

.. _Here: http://code.google.com/p/django-simpleaggregation/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _`Graham Dumpleton, the creator, has done`: http://code.google.com/p/modwsgi/wiki/PerformanceEstimates