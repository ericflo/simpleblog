---
layout: post
title: "Ideas and Execution"
date: 2008-03-12T05:57:30-05:00
comments: false
categories: [Django, django-threadedcomments, Python]
published: true
alias: [/blog/post/ideas-and-execution]
---

After my `last post about django-threadedcomments`_, there have been several new releases.  We've integrated completely with comment_utils_, added support for gravatar_, and added some internationalization (I love that we abbreviate this as i18n) support as well.  Every day more and more people seem to be adding bug reports, patches, and feature requests to the ticket tracker.  This couldn't make me happier, and I hope to see it continue.  But what does this have to do with ideas?  It's the first programming idea that I've taken through conception, execution and all the way to support.  After django-threadedcomments_, I've decided to change my outlook on how to organize and deal with ideas that I get every day.

Supporting a Project
--------------------

There sure is a thrill to just sitting down and quickly hammering out the solution to a problem.  Who cares if it's hacky and incomplete?  You just proved that your idea was doable and you did it.  It instills quite the sense of accomplishment.  That's the style of project that I've worked on until now (aside from work).  With django-threadedcomments_, however, there's a completely different feeling that's just as thrilling:  people are actually using it.  It gives a completely different and stronger sense of accomplishment.  The reason is because I made a conscious effort to support the application after its initial release, for my own benefit and for others'.

Admittedly it can be tedious at first.  I'm convinced that nobody enjoys writing test code, and writing documentation can take as long as writing the code itself (especially if you delete and re-write as much as I do), but being able to apply patches that people submit and actually *ghasp* re-use your own code in other projects is where the reward really lies.

Ideas
-----

I have ideas all the time--as I think most people do.  Whether it be while writing code for one project, sitting idly in class, or even eating my cereal in the morning, ideas for nifty programs or websites or APIs just sort of pop into my head.  What do I do with them?  Until recently, what happened is that I'd start working on it and lose interest after a while.  Over the last few months, however, I've begun to form a list instead of starting on the projects.

Why make a list?  Looking at my track record of starting and abandoning projects--and assuming that I'd like to do that far less often--it seems that something needs to change.  The change that I've settled on is to put them on a list instead of hastily implementing them.  When I attack one of these ideas, I'll attack it fully and correctly; bringing it from conception to implementation, and finally to support.  The reasons for this are three-fold:

1.  It's a good incubation period.  After a while, some ideas seem stupid, while others keep begging to be solved.

2.  It allows for a greater sense of accomplishment.  Once you cross out a few items on your list, you'll realize that what you've done is quite a feat.

3.  You can simply remember all those crazy ideas that you have had.

What is on my List?
-------------------

I'm sure many of you may be asking what, specifically, I have on my list.  django-threadedcomments_ is on there, and my next project is django-simplestats_.  The latter is not ready for public consumption yet, but check it out if you'd like to see a sneak peek.  There are also several other items, but I'm not going to talk about them because it would take all the fun away from me!  Honestly though, don't ask me for my list.  Come up with your own and work through it for yourself.

And You
-------

Enough about me in this rambling post, what about you--how do you deal with ideas that you get every day?  Am I crazy for actually enjoying supporting a project?  Do you have any tips for me in my organizational endeavours?  Please respond in the comment section below.

.. _`last post about django-threadedcomments`: /blog/post/ajax-voting-nicer-css-threadedcomments-test/
.. _comment_utils: http://code.google.com/p/django-comment-utils/
.. _gravatar: http://site.gravatar.com/
.. _django-threadedcomments: http://code.google.com/p/django-threadedcomments/
.. _django-simplestats: http://code.google.com/p/django-simplestats/