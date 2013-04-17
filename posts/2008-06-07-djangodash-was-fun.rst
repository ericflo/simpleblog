---
layout: post
title: "Djangodash was Fun!"
date: 2008-06-07T03:05:00-05:00
comments: false
categories: [Django, Django Dash, Feedalizer, Programming, Python]
published: true
alias: [/blog/post/djangodash-was-fun]
---

Djangodash_, a two-day two-person sprint to create a project using Django, took place last weekend.  To be honest, I wasn't expecting it to be much fun, but it ended up being an absolute blast!

Feedalizer.net_
---------------

Before getting too far into this post mortem, I'm going to just get it out of the way and shamelessly promote the site that Tony and I created during the dash: feedalizer.net_.  The idea behind the site is that it's a feed aggregator, but people vote on the feeds.  The higher the feed's score, the more likely items from that feed will bubble up to the top of the list.  There's also the concept of a "channel", which only aggregates feeds for a specific area.  For example, there's a Humor channel, a Django channel, and a Python channel.  You can also subscribe to channels to create your own "station", which aggregates the content from the channels that you care about.

The idea came to me when a friend of mine asked me *"I've never used a feed reader before, but I want to get started and subscribe to programming feeds.  What are some good ones for me to subscribe to?"*  It took me about 30 minutes to cull through my feeds and produce a list of the best.  But it shouldn't have taken me any time at all--there should have been a site out there to do this for him!

OK, enough shameless self-promotion.

The Dash
--------

`52 teams`_ registered for the dash, so watching the commit activity at the turn of the clock was pretty crazy.  Unfortunately, Tony was driving from 4 hours away and he hadn't arrived yet.  When he did arrive, we both wanted to spend some time catching up and talking about non-Django things.  So we didn't even get started until about 3:30AM.  Getting started mainly consisted of frantically checking in 3rd party projects that we thought we would use, and talking about architecture, and writing a few cron jobs.  Not much code got written that night (morning?), since we still had a lot of planning to do.

The next day, all of a sudden our commits weren't working!  We went to the website to see what was going on, and the website wasn't responding to our requests.  Something was definitely going on, and it was slowing down our progress significantly.  We tried working on our own separate parts of the project, but at this early stage there was simply too much overlap.  We found out later in the night that there were problems at `Webfaction's`_ data warehouse,`The Planet`_, where a transformer quite literally exploded.

This severely slowed us down, because we ended up having to switch to git, and then once we got everything into our git repository, we had tons of merge conflicts.  We got an e-mail saying that the due date would be postponed, so we decided to take the afternoon and night off to do other things.

The next day we did the brunt of our work.  I had the task of designing the frontend, so I opened up my trusty text editor and hammered out the worst-looking CSS file you'll ever see in your life, producing some of the worst-looking pages you'll ever see in your life.  This changed over the course of the day, but not by much as you'll see if you visit the site.  This same day, Tony was working on some of the harder queries etc.

The final day (the deadline had been extended, remember) was all about integration.  There was nothing really notable about this, but it took all day to get everything working properly together.  I ended up writing a bunch of Javascript to make the client experience more enjoyable, and Tony had the chance to debug his views now that I had templates and we had sample data.  It was a crunch to make the deadline, but we tried to do the little important extra details like write an "about" page, a README file, etc.

Conclusion
----------

Whether we win or lose, and despite the technical difficulties that `The Planet`_ suffered, I had a blast doing the competition.  I think that our idea is novel, and Tony and I got to work on something once more post-graduation.  (Nothing like a programming competition to bring people together, I always say.)  In fact, we'll probably continue to work on it for the months to come, especially in upgrading its graphics.  It's going to be really awesome to see what everyone else produced this year.  I encourage anyone who thought about participating this year, or anyone who even considers it as a possibility, to sign up and **just do it** next year!

.. _Djangodash: http://djangodash.com/
.. _Feedalizer.net: http://feedalizer.net/
.. _feedalizer.net: http://feedalizer.net/
.. _someone: http://ejohn.org/
.. _`52 teams`: http://djangodash.com/contest/team/
.. _`Webfaction's`: http://www.webfaction.com/
.. _`The Planet`: http://www.theplanet.com/