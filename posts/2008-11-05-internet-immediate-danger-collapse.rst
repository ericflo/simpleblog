---
layout: post
title: "The internet is in immediate danger of collapse"
date: 2008-11-05T23:38:48-06:00
comments: false
categories: [amazon, Web Services, internet, Google, Programming]
published: true
alias: [/blog/post/internet-immediate-danger-collapse]
---

Wow, that's quite a title!  You're already probably queuing up all of your
counterpoints and your rebuttals.  In fact it's not quite that serious, but a
seriously worrying trend is emerging that I'd like to address.

The Problem
-----------

Today many sites are so totally dependent on 3rd-party services that when
certain services go down, a chain of outages end up knocking out many of the
sites that we use on a daily basis--some for critical business applications.
But I'm being too abstract, so let's take a concrete example of this: Google
Analytics.  

Back in late 2007, `Google's analytics and monitoring service`_ went
down with no explanation.  Most sites at that time had installed a line of
Javascript in their HTML ``head`` element which made a call to
``document.write``.  This causes the **rest of the site to stop and wait for
Google's servers**.  Normally this is not a bad thing, because Google has some
pretty fast and reliable web servers.  But in this 24 hour period, anyone who
had this code in their ``head`` element had an absolutely broken site.  Users
could not see their site at all.  And was no fault of either the site developers
or of the users--just Google's fault.

Another example: Earlier this year, Amazon had an outage in their popular S3_
file storage service for several hours.  At the time, you didn't need to be very
tech savvy or know much about computers to know that something was seroiusly
wrong with the internet.  Sites from across the net were throwing 500 errors,
looking completely awful without their media files, and the internet simply
became a pretty awful place to get things done.  From one company.  Having a
problem with one service.

And since then we have become even more dependent on 3rd party services for
even more widgets, "cloud computing", and more.  Frankly this "cloud computing"
craze scares the hell out of me.  The more interconnected our various bits of
HTML and HTTP are, the more chances there are for massive catastrophe.  Just
look at the credit default swaps problem we're having in the USA for another
concrete example of how this type of interdependence can fail in catastrophic
ways.

The Solution
------------

Services like S3, Google Analytics, and even Twitter are great services.  They
add lots of value for larger businesses and even more for a startup, so there's
a large incentive to use them.  I think that's absolutely fine and is actually
a good idea.  That being said, we need to manage our use of these services in a
responsible way.  Instead of storing data directly to S3, store it on a server
and asynchronously upload it to S3.  That way, you can set up an S3-pinger and
if it goes down you can have the server automatically switch to serving the
media itself.

We need to build standardized tools that fetch data from webservices locally,
from which they are served to the user.  We need to build systems that
asynchronously sync data bidirectionally from all of these different webservers
and ensure that the integrity of our data on the web is sound.  Right now this
is a tedious, and error-prone task, but we can do better.  We can build
cross-platform tools and libraries that will solve this problem, allow us to
use 3rd-party services, and rest sound knowing that tomorrow no matter what
happens to Amazon, the internet will still be around.

DISCLAIMER: This is almost entirely a ripoff of a talk given by `Timothy Fitz`_
at `Super Happy Dev House`_ last month in San Francisco.  While I think it's a
really good point I can't take credit for having been the first to worry about
it.

.. _`Google's analytics and monitoring service`: http://www.google.com/analytics
.. _S3: http://aws.amazon.com/s3/
.. _`Timothy Fitz`: Timothy Fitz
.. _`Super Happy Dev House`: http://superhappydevhouse.org/