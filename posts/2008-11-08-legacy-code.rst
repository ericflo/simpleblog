---
layout: post
title: "Legacy Code"
date: 2008-11-08T20:45:13-06:00
comments: false
categories: [Python, Django, Programming]
published: true
alias: [/blog/post/legacy-code]
---

Prompted by this whole blog post-per-day thing, I've begun looking at the source
code for this site again.  It was my first real Django project in early 2006,
and I was excited about all of the features that it gave me.  The community was
much smaller then, and although I suspect the guys from Lawrence_ had a good
idea of where site logic should go, at that time there was not the
widespread_ knowledge_ of best_ practices_.

No knowledge of best practices, still learning Django, and being a relative
web development newbie, means that the code ended up being quite bad.  It was
all under one application, named 'blog'.  All of the content loaded into the
sidebar was done via context processors (one processor called back to this
``get_digg_rss`` function that I `blogged about`_, for example), and all the
templates were housed under that application.

Yeah.  It was that bad.

But over the years, Django evolved, and some code that this blog used were
deprecated while new functionality was added.  Over time as things broke, little
by little things were fixed and broken out into their own apps.  In short, the
site got better.  It was always organic improvement, though, and never a
deliberate effort.  Meaning that while it's better than it was, it's still not
very good.

Browsing through the code gives me a bit of nostalgia, but overwhelmingly my
urge is to just delete the entire thing and start over, picking from the best
reusable apps and migrating data as needed.  After some consideration, I don't
think that urge is a good urge to act upon.  While it would take me a few
afternoons to fix the code of the site, it would take several days to start
from scratch.

This is one of my biggest faults as a programmer.  Instead of working with ugly
code and molding it into better code, I always enjoy starting from a clean slate
and building it up from there--so much so that I'll sacrifice productivity to
do so.  I'm going to attempt to face this fault by not giving in to the
temptation to rebuild, and instead to work with what I've got.  Who knows, maybe
I'll even open-source it.  I won't open-source it unless its quality is up to
par with the other open source apps in the Django reusable app ecosystem.

How do you deal with legacy code?  Do you have any tips or tricks on how to do
it?  Do you think that it's better to just start from scratch?

.. _Lawrence: http://www.mediaphormedia.com/
.. _widespread: http://www.b-list.org/weblog/2007/mar/27/reusable-django-apps/
.. _knowledge: http://pinaxproject.com/
.. _best: http://apress.com/book/view/1590599969
.. _practices: http://www.djangobook.com/
.. _`blogged about`: http://www.eflorenzano.com/blog/post/new-site-live/