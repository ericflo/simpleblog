---
layout: post
title: "Simple Random Character Function"
date: 2007-04-16T00:27:22-05:00
comments: false
categories: [Python]
published: true
alias: [/blog/post/simple-random-character-function]
---

I use this function all the time, most recently for some anti-spam techniques, and it's worth posting somewhere.  It's modified from an entry on the activestate cookbook.

.. code-block:: python

    def random_chars(length):
        import random
        allowed_chars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789"
        word = ""
        for i in xrange(0, length):
            word = word + allowed_chars[random.randint(0,0xffffff) % len(allowed_chars)]
        return word

Also, for anyone who knows me and is interested: my surgery went well and I'm recovering faster than I would have expected.  Hopefully I'll be back to 100% speed in the next few days!

Anyways, hopefully this small code snippet is useful to someone else, as well!