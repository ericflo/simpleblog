---
layout: post
title: "The most widely available virtual machine"
date: 2008-11-22T23:37:57-06:00
comments: false
categories: [Javascript, Programming, Python, John Resig, Ruby, Virtual Machines]
published: true
alias: [/blog/post/most-widely-available-virtual-machine]
---

A few months back, I had a bit of an epiphany.  I suspect I was about 5 years
too late with this epiphany, but nevertheless here it is: Microsoft,
Sun, and Adobe all have these virtual machines that they want everyone to
develop on top of.  For Microsoft it's the CLR_, for Sun it's the JVM_, and for
Adobe it's AVM_.  The problem that each of them have is that not everyone goes
out of their way to install all of these VMs, so each vendor only has a subset
of the entire computing space.

My epiphany was that there is one VM which nearly every modern computer has
access to.  It's JavaScript.  Every browser developed in the past 10 years
ships with some variation of it, and some systems even come with it as a
command-line option.  Whilst they do have a big problem in terms of
standardization (or lack thereof), there is certainly a lowest common
denominator that could be useful for writing apps on top of.

That being the case, why don't we see more language implementations on top of 
JavaScript?  There is Processing.js_, a port of the Processing_ programming
language.  There is also `Objective J and Cappuccino`_, a port of Objective C
and Cocoa, respectively.  Each of those language implementations have received
quite a bit of attention (both positive and negative, mind you).

So why don't we see Ruby, Python, or other languages implemented on top of
JavaScript?  For that matter, why don't we see more ports of apps to JavaScript?
I know that in the Python world, PyPy has a JavaScript backend, but to the best
of my knowledge that backend has been all-but-abandoned.  I think it would be
really cool if we were to see more applications and programming languages
targeting the most widely adopted virtual machine ever: JavaScript.

.. _CLR: http://en.wikipedia.org/wiki/Common_Language_Runtime
.. _JVM: http://en.wikipedia.org/wiki/Java_virtual_machine
.. _AVM: http://www.adobe.com/devnet/actionscript/
.. _Processing.js: http://ejohn.org/blog/processingjs/
.. _Processing: http://processing.org/
.. _`Objective J and Cappuccino`: http://cappuccino.org/