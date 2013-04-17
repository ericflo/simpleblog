---
layout: post
title: "What's Next?"
date: 2008-11-01T20:24:11-05:00
comments: false
categories: [Python, Django, Programming]
published: true
alias: [/blog/post/whats-next]
---

A few days ago, someone asked me "What's the next big thing?"  The context was a discussion of web development tools, as they exist today.  At first I laughed and brushed off the question as clichA, because everyone seems to have a different answer and almost nobody ends up being correct.  But it is a good question to ask oneself, and I'm noticing that more and more people seem to be searching for that "next big thing".  

The standard response du jour seems to be "cloud computing".  However with a term like that, you can understand why there are disagreements as to what exactly cloud computing is.  I'm not so convinced.  I'm not convinced that thick client computing will come back, either, but certainly the thought of distributed computing will continue to resurface--which is quite directly at odds with the concept of cloud computing (depending on how you define cloud computing, of course).

Examining today's problems
----------------------------------------

Before we can talk about what will emerge as the next big thing, we need to first look at what sucks right now:

1.  **Concurrency.**  Do I even need to spell out why this sucks right now?  It's easy to get wrong, and anyone who thinks that it isn't, is probably getting it wrong.

2.  **Database technology, specifically relational databases.**  This area of study is a proven and well-understood area of computer science, and for simple tasks, using a database could not get any easier.  Especially with the advance of `object relational mappers`_ that are starting to generate really good SQL, it's easier than ever to set up some data structures to store and retrieve data from a database.  Try to start scaling this solution, as many_ people_ are_, and you'll see why this technology (as it is today) doesn't hold up.

3.  **Push.**  With the emergence of data whose value is highly time dilated (think Twitter_, FriendFeed_, etc.), systems which operate under a "pull"-only interface are growing long in the tooth.  In fact, FriendFeed_ has a post explaining `just how hard this is for them`_ (and proposing their own protocol which hasn't seemed to get any traction).

Those next big things
--------------------------------------

Given the aforementioned problems facing developers today, is the outlook bleak?  Is there no hope for the future?  Of course not!  As always, there are some exciting new technologies that are addressing these very problems.

1. `Erlang`_.  People who hype it up will tell you that this magically solves all concurrency problems, and they are simply being overzealous.  That being said, erlang encourages a style of programming that is extremely conducive to writing highly scalable applications.  Not only that, but there are over 20 years worth of experience and effort that have gone into making this language rock solid.  We've seen, over the past few years, an uptake in the number of applications that are written in erlang.  I expect that trend to continue, and as our need for highly concurrent applications increases, that rate will increase as well.  It's a good time to be an erlang programmer!

2.  `CouchDB`_.  This is a system which, from the ground up, was designed for scale.  Built upon the aforementioned Erlang programming language, and upon the well tested and trusted OTP_ methodology, CouchDB takes a completely new approach to databases.  It is a document-oriented database, which means that it's best suited towards those documents which can easily be written down on a piece of paper.  (A business card is the prototypical example of a type of document that would be great to store in CouchDB.)  It's a blog post unto itself, but the forward-looking nature of CouchDB, along with it's adherence to the fundamentals of what makes the web work so well, has gotten a lot of people interested in the project.  I'd bet my career on CouchDB becoming a Very Big Deal.

3. XMPP_.  Let's first start with the bad things about it.  It's complicated, overly abstract, obtuse, and there doesn't seem to be a succinct definition of what it is.  You may disagree with any or all of those points, but one thing is clear: what it does well, it does better than anything else, and that is push communication.  Look for laconi.ca and twitter to be early leaders in this field, and for the technology to be simplified and clarified.  If you're not subscribed to `Jack Moffitt`_'s blog, do so.  Now.  He has pretty much single handedly rekindled my excitement for this technology, and with a few more people like him, we'll see this technology execute on its vast potential.

4. Python_ and Django_.  Of course I'm biased due to my closeness to these projects, and these are already big deals really.  But I think they will continue to further distinguish themselves from the competition.  Both projects have a reputation for not making important design decisions rashly and for sticking to their ideals.  As long as this trend continues, I believe the number of people flocking to these technologies will continue to grow.

What do you think?
--------------------------------------

I suspect I won't meet a lot of resistance on these choices.  But I hope I do!  What do you think about these choices?  Is there something that I'm missing?  Please share your thoughts in a blog post or in the comments.

An aside
--------------------------------------

I'm going to try to post one blog post each day of the month of November, as a challenge to myself and with some of my friends.  Others participating are:

*  `Brian Rosner`_.
*  `James Tauber`_.
*  `Eric Holscher`_.
*  `Greg Newman`_.
*  `Justin Lilly`_.
*  `Adam Gomaa`_.
* `Jannis Leidel`_.

Please check out their blogs and see all of the amazing content that they're already creating.

.. _`object relational mappers`: http://en.wikipedia.org/wiki/Object-relational_mapping
.. _many: http://twitter.com/
.. _people: http://mahalo.com/
.. _are: http://digg.com/
.. _Twitter: http://twitter.com/
.. _FriendFeed: http://friendfeed.com/
.. _`just how hard this is for them`: http://blog.friendfeed.com/2008/08/simple-update-protocol-fetch-updates.html
.. _`Erlang`: http://erlang.org/
.. _`CouchDB`: http://incubator.apache.org/couchdb/
.. _OTP: http://spawnlink.com/articles/introduction-to-the-open-telecom-platform/
.. _XMPP: http://xmpp.org/
.. _`Jack Moffitt`: http://metajack.im/
.. _Python: http://python.org/
.. _Django: http://djangoproject.com/
.. _`Brian Rosner`: http://oebfare.com/
.. _`James Tauber`: http://jtauber.com/blog/
.. _`Eric Holscher`: http://ericholscher.com/
.. _`Greg Newman`: http://www.20seven.org/
.. _`Justin Lilly`: http://justinlilly.com/
.. _`Adam Gomaa`: http://adam.gomaa.us/blog/
.. _`Jannis Leidel`: http://jannisleidel.com/