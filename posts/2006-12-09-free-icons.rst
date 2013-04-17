---
layout: post
title: "Free Icons!"
date: 2006-12-09T03:25:04-06:00
comments: false
categories: [Famfamfam.com, Programming, Pygments, Django, Eflorenzano.com]
published: true
alias: [/blog/post/free-icons]
---

If you have noticed, there are now icons next to each comments link.  These are provided, free of cost, by famfamfam.com_.  If some 16x16 icons are needed, and you are not graphically or creatively inclined, this is your one-stop-shop.

In other news, a Speed graph has been added to the running page as well as a distance graph.  In doing that, I ran into a problem which was hard to debug, since it only happens on the live site.  In Django, trying to serialize a Numeric data type with simplejson will not work, so make sure to cast it to a python-native data type first.

Problem code:

.. code-block:: python

    i = 0
    for run in runs:
        distance = run.distance()
        speed_data.append((i,distance/run.time))
        distance_data.append((i,distance))
        i = i + 1

Solution:

.. code-block:: python

    i = 0
    for run in runs:
        distance = run.distance()
        speed_data.append((i,distance/float(run.time)))
        distance_data.append((i,distance))
        i = i + 1

I also noticed a problem with my Pygments function, due to the regular expression, where it only allowed me to post one code snippet.  As you can see in this post, that has been fixed (although it was another particularly nasty bug to track down, and required a complete refactoring of my code in the end).

.. _famfamfam.com: http://www.famfamfam.com