---
layout: post
title: "SimpleAggregation update, Eyespot"
date: 2007-08-02T22:06:05-05:00
comments: false
categories: [Eflorenzano.com, Django, Programming, Python, SimpleAggregation, eyespot]
published: true
alias: [/blog/post/simpleaggregation-update-eyespot]
---

django-simpleaggregation
------------------------

I have just released Version 0.2 of django-simpleaggregation_.  Updates in this release:

* The detection of an update on a unique field was not being correctly computed.  It used to use the addition of an id field to determine whether an aggregate should be incremented, but now it uses another hook into the dispatcher to annotate pre-save the model instance with some metadata related to aggregation.
* The old helper functions which were used to get aggregate data have now been replaced with an object which is smarter and cleaner.  I suspect there will be a few more cleanup changes to the implementation of this, but the API should now stay fairly stable.
* Pagination is now usable.  In 0.1, some rudimentary pagination abilities existed, but now it supports most of the same pagination data that a generic view gives a template.

Eflorenzano.com
---------------

I've updated this site to use freecomment and the excellent django-comment-utils_ by `James Bennett`_, which allows me to automatically use Akismet to block spam.  Hopefully this will solve the problems that I've been having with comment spam, despite the efforts that I've made in the past to combat it programmaticaly.  

Eyespot
-------

My internship at eyespot_ is coming to an end in a little over a week.  It's really bittersweet for me:  it has been such a great experience, moving out to California and working on the "Web too pwoint oahh" craziness, but I miss my friends from the midwest.  I was a little nervous to take this internship, because of the technologies that I knew eyespot was using (notably, Perl), but my experience this summer only reinforces my original thought: programming language doesn't matter, it's people who matter.

If it's people who matter, eyespot matters a whole lot, because there has been no other time when I have respected the people around me even close to as much as I respect those at eyespot.  I've never seen someone who can come up with the solution to a problem as I'm still trying to grasp the idea of the problem itself.  I've never seen people so willing to listen to and implement the ideas of an intern.  I've never seen a group of coworkers who were more welcoming and tight-knit, hanging out after work as much as during.  And most of all, I've never seen a group of people who were more skilled at their craft, as the people at eyespot.

Sure, there are some things that I think could be done better at eyespot.  Sometimes, frankly, I'm surprised that it all works.  But I'm not going to go into those things, however, because it's actually not relevant to my point.

So, all said, I'm excited for what the future holds for me and eyespot, my working life after college, etc.  But to bring it back to my earlier point, I'm also excited for my last year in college.  Being away from home and family and friends has made me realize just how much I appreciate all of them on a daily basis, and perhaps just how much I take them for granted.  I could care less about going back to learn computer science--I'm going back for the people (is this a recurring theme, or what?)

I'm going to carpe diem this next school year, because it's the last one I've got.

.. _django-simpleaggregation: http://code.google.com/p/django-simpleaggregation/
.. _django-comment-utils: http://code.google.com/p/django-comment-utils/
.. _`James Bennett`: http://www.b-list.org/
.. _eyespot: http://www.eyespot.com/