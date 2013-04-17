---
layout: post
title: "Intermediary Models and PyMag"
date: 2008-07-30T01:11:17-05:00
comments: false
categories: [Python, Django, django-threadedcomments, PyMag, Awesome]
published: true
alias: [/blog/post/intermediary-models-and-pymag]
---

Journey to Intermediary Models
------------------------------

It's been around an 8 month journey in adding intermediary model support to Django, starting with `a ticket`_ opened during a sprint by `Jacob Kaplan-Moss`_.  Earlier that month I had been wrestling with several pretty nasty models, each with two foreign keys and many extra properties on that relation.  I kept thinking that Django makes everything else so easy, but that in at least this one aspect, it doesn't make things easy enough.  When Jacob posted his API idea, I was hooked.

I quickly posted some thoughts and asked for a bit of clarification, and volunteered to write the patch.  Jacob responded saying he was glad to help me out.  It was only then that I actually delved into the code to see how it could be done.  It was only then that I realized that I had absolutely no knowledge or familiarity with that portion of the codebase--a portion that is nontrivial, to say the least.  But that's the good thing about committing to something: you feel pressure to follow through.

Despite my incredible NaA-vitA, the patch got to a rudimentary usable state very quickly, and then started to flounder.  It was then that `Russell Keith-Magee`_ came into the picture, continually prodding me to add more tests, and thinking up many different test cases that I would have never come up with on my own.  I'm 100% certain that if Russ had not lent his expertise and guidance on this patch, it would have gotten lost and forgotten for a long time until someone more capable came along to take a look at it.

A few hours ago, Russ `committed the patch to trunk`_.  It's interesting to see the `reactions`_ that `some people have`_, but on any project like this you'll always be scrutinized.  In any case, check out the `two`_ new bits of `documentation`_, and see if intermediary models are right for your project.  After having this great experience with working on a patch for Django, I'll definitely be looking to help out in other places as well.  My advice for anyone looking to get involved with the project is to, well, get involved!  Jump in over your head.  It's more fun that way.

PyMag
-----

For around as long as I have been working on intermediary model support, I've been supporting another Django project of mine: django-threadedcomments_.  One of the things that I noticed a few months into maintaining the project is that outside of a few people who were actively using it, not many people really knew about its existence.  So when `Doug Hellmann` (of the famously excellent PyMOTW_ series) contacted me about writing an article for PyMag_, it was immediately apparent what I would love to write about.  Over 4000 words later, between finals and school projects and moving across state boundaries, the article was written.

To be honest, I had almost completely forgotten about having written it, aside from one short e-mail conversation with the technical editor.  It turns out that the July 2008 edition of PyMag_ has arrived and my article is listed under "featured articles".  How cool is that!?  I'm quite proud of the article, and really hope that it helps some people out with their Django websites.  If you aren't a PyMag_ subscriber, then what are you waiting for?

This post seems to be doing a lot of self-promotion--sorry for that.  But these two things really made my day, and to me, blogging is about sharing those awesome days with others.

.. _`a ticket`: http://code.djangoproject.com/ticket/6095
.. _`Jacob Kaplan-Moss`: http://www.jacobian.org/
.. _`Russell Keith-Magee`: http://djangopeople.net/freakboy3742/
.. _`committed the patch to trunk`: http://code.djangoproject.com/changeset/8136
.. _`reactions`: http://www.reddit.com/comments/6tzig/django_gets_intermediate_models/
.. _`some people have`: http://www.reddit.com/comments/6ty8n/extra_fields_on_m2m_relationships_has_landed_in/
.. _`two`: http://www.djangoproject.com/documentation/model-api/#extra-fields-on-many-to-many-relationships
.. _PyMag: http://pymag.phparch.com/
.. _`documentation`: http://www.djangoproject.com/documentation/admin/#working-with-many-to-many-intermediary-models
.. _django-threadedcomments: http://code.google.com/p/django-threadedcomments/
.. _PyMOTW: http://blog.doughellmann.com/search/label/PyMOTW