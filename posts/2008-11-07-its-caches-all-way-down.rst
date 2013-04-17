---
layout: post
title: "It's Caches All the Way Down"
date: 2008-11-07T23:52:53-06:00
comments: false
categories: [Memcached, Caching, Programming]
published: true
alias: [/blog/post/its-caches-all-way-down]
---

A few years back a non-technical person asked me to explain what, exactly, the
operating system did.  I first started out by speaking in broad generalities,
saying that it takes care of the basic needs of the computer and that it helps
one thing talk to another.  But that answer wasn't good enough.  This person
wanted me to go into more detail.  What happens when I'm in the calculator
application and I type 1+1 and hit enter?  What things need to happen?

That really tripped me up.  It's hard to even know where to start when someone
who's curious like that asks a relatively innocent question like that.  So I
decided to just start from the basics.  "A processor has these things called
registers", I said.  "And they store a tiny little amount of information, which
they can do things with, like add and subtract."  That seemed to basically
satisfy them, but not me.

I made sure to say that, "You can't just keep everything in registers, because
there are only a few of those.  So you have to keep some data stored
in this place with more space for data but it's slower."  To which they
responded, "Oh, so is that why when I add more RAM my computer gets faster?"
"No," I said, "this is all still on the processor."  "OK, so what's RAM then
and why is it supposed to help?" they asked.  "Because we can't store everything
on the processor itself, because there's not enough space for data, so we have
to store it in this place with much more space for data, but which is slower."

At this point I realized how redundant this conversation was going to get.  It's
the same thing for the hard drive, and (if you're old-school) tape drive or (if
you're new-school) the internet.  At the same point that person seemed to get
bored--that moment of curiosity had passed.  Computers just do their thing
and we really didn't have to do anything special for all of that data movement
to take place.

That's what struck me.  When you come down to it, computers are just a waterfall
of different caches, with systems that determine what piece of data goes where
and when.  For the most part, in user space, we don't care about much of that
either.  When writing a web application or even a desktop application, we don't
much care whether a bit is in the register, the L1 or L2 cache, RAM, or if it's
being swapped to disk.  We just care that whatever system is managing that data,
it's doing the best it can to make our application fast.

But then another thing struck me.  Most web developers *DO* have to worry about
the cache.  We do it every day.  Whether you're using memcached or velocity or
some other caching system, everyone's manually moving data from the database
to a cache layer, and back again.  Sometimes we do clever things to make sure
this cached data is correct, but sometimes we do some braindead things.  We
certainly manage the cache keys ourselves and we come up with systems again and
again to do the same thing.

Does this strike anyone else as inconsistent?  For practically every cache layer
down the chain, a system (whose algorithms are usually the result of years and
years of work and testing) automatically determines how to best utilize that
cache, yet we do not yet have a **good** system for doing that with databases.
Why do you think that is?  Is it truly one of the two hard problems of
computer science?  Is it impossible to do this automatically?  I honestly don't
have the answers, but I'm interested if you do.