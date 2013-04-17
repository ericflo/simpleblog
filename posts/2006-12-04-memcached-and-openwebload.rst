---
layout: post
title: "Memcached and OpenWebLoad"
date: 2006-12-04T15:46:58-06:00
comments: false
categories: [Eflorenzano.com, Programming, Memcached, Wil Wheaton]
published: true
alias: [/blog/post/memcached-and-openwebload]
---

There has been a somewhat minor update to the site.  Now almost all of the site is cached.  That is, there is a memcached_ backend running on the server, and this website can take advantage of that.

To test out the site's load capabilities, I used an open source program called OpenWebLoad_.  It's quite impressive in its simplicity and utility.  With it, I was able to test a load of over 50 simultaneous users to the website.  Surprisingly, the site handled it with flying colors.

On a side note, I went to `Wil Wheaton's site`_ after a long stint of not visiting it, and it's still as good as it's ever been.  There's an almost tangible difference between a writer's website and a blogger's website.  I think that it boils down to the fact that using only words, Wil can make you feel the emotion that he wants you to feel.

.. _memcached: http://www.danga.com/memcached/
.. _OpenWebLoad: http://sourceforge.net/projects/openwebload/
.. _`Wil Wheaton's site`: http://wilwheaton.typepad.com/