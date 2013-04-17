---
layout: post
title: "AJAX, Voting, and Some Nicer CSS: Putting django-threadedcomments to the Test"
date: 2008-01-30T12:02:13-06:00
comments: false
categories: [Django, Programming, Python, jquery, Javascript, django-threadedcomments, Reddit]
published: true
alias: [/blog/post/ajax-voting-nicer-css-threadedcomments-test]
---

It's an interesting feeling open-sourcing an application that you've developed for your own purposes.  Will people use it?  Will people find major design flaws?  Is it just a big waste of time?  These were the questions that were going through my mind before open-sourcing django-threadedcomments_.  Fortunately, my worries were quelled almost instantly as a people reacted quite positively to the application.  There was one recurring comment, however, that almost everyone who tried the sample implementation said: **those colors are hideous**.

Beyond even that though, it seems that people saw the sample implementation and got the impression that django-threadedcomments = that sample implementation.  To me, that's an underestimation of the power of the modular django app.  I think that `James Bennett`_ hits the nail on the head when he says that:

    "Rather than a single definitive 'Django blog' application, for example, I think it--  s much more likely 
    we--  ll see a collection of applications which, taken together, provide all the key 
    functionality..."

It was this sentiment that pervaded nearly all of the design decisions behind django-threadedcomments: it should be flexible, modular, and reusable so that, taken together with other similarly-designed apps, it can provide some compelling functionality at a fraction of the effort.  Now we most assuredly didn't achieve all of those design goals fully, but I believe we're headed in at least the right direction with its development.

To prove my point, I decided to create an improved Digg/Reddit comment system clone using `Jonathan Buchanan`_'s wonderful django-voting_ application, alongside django-threadedcomments_, and a fair bit of jQuery_.  Being almost completely new to Javascript, I was pleasantly surprised by how easy it was to not only integrate all of these technologies and use extensive client- and server-side scripting, but also to achieve a compelling commenting system in well under a week of spare time.  Oh, and this time there was actually some effort in making the look and feel of the commenting system acceptable!  As with the first example, this one is completely open sourced and available in the django-threadedcomments SVN repository.

Without further ado, the `Example Digg/Reddit Comment Clone Plus Focus`_.

.. _django-threadedcomments: http://code.google.com/p/django-threadedcomments/
.. _`James Bennett`: http://www.b-list.org/weblog/2007/nov/29/django-blog/
.. _`Jonathan Buchanan`: http://insin.webfactional.com/weblog/
.. _django-voting: http://code.google.com/p/django-voting/
.. _jQuery: http://jquery.com/
.. _`Example Digg/Reddit Comment Clone Plus Focus`: http://www.eflorenzano.com/threadexample/blog/