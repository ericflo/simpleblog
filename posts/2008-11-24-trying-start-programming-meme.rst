---
layout: post
title: "Trying to Start a Programming Meme"
date: 2008-11-24T23:13:18-06:00
comments: false
categories: [Python, Meme, Programming]
published: true
alias: [/blog/post/trying-start-programming-meme]
---

I've never tried to start a meme before, but since I don't really have anything
great to post about, I'd like to try to start one.  I think this one could be
particularly fun because it encourages implementation of a basic program in many
different languages.

Rules:

1. Implement a program that takes in a user's name and their age, and prints
   hello to them once for every year that they have been alive.

2. Post these rules, the source code for your solution, and the following list
   (with you included) on your blog.

3. Bonus points if you implement it in a language not yet seen on the following
   list!

The List:

1. [Python] http://www.eflorenzano.com/blog/post/trying-start-programming-meme
2. [Bash] http://aartemenko.com/texts/bash-meme/
3. [C] http://dakrauth.com/media/site/text/hello.c
4. [Java] http://adoleo.com/blog/2008/nov/25/programming-meme/
5. [Python 3] http://mikewatkins.ca/2008/11/25/hello-meme/
6. [Ruby] http://stroky.l.googlepages.com/gem
7. [Ruby] http://im.camronflanders.com/archive/meme/
8. [Lisp] http://justinlilly.com/blog/2008/nov/25/back-on-the-horse/
9. [Lua] http://aartemenko.com/texts/lua-hello-meme/
10. [Functional Python] http://aartemenko.com/texts/python-functional-hello-meme/
11. [Erlang] http://surfacedepth.blogspot.com/2008/11/erics-programming-meme-in-erlang.html
12. [Haskell] http://jasonwalsh.us/meme.html
13. [PHP] http://fitzgeraldsteele.wordpress.com/2008/11/25/memeing-in-php-2/
14. [Javascript] http://www.taylanpince.com/blog/posts/responding-to-a-programming-meme/
15. [Single-File Django] http://www.pocketuniverse.ca/archive/2008/november/27/florenzano-factor/

(...and make sure to check out the comments on this post for some other fun implementations!)

And here's my implementation:

.. code-block:: python

    name = raw_input('Please enter your name: ')
    age = int(raw_input('Please enter your age: '))

    for i in xrange(age):
        print "%2d) Hello, %s" % (i, name)

And its output:

.. code-block:: bash

    Please enter your name: Eric Florenzano
    Please enter your age: 22
     0) Hello, Eric Florenzano
     1) Hello, Eric Florenzano
     2) Hello, Eric Florenzano
     3) Hello, Eric Florenzano
     4) Hello, Eric Florenzano
     5) Hello, Eric Florenzano
     6) Hello, Eric Florenzano
     7) Hello, Eric Florenzano
     8) Hello, Eric Florenzano
     9) Hello, Eric Florenzano
    10) Hello, Eric Florenzano
    11) Hello, Eric Florenzano
    12) Hello, Eric Florenzano
    13) Hello, Eric Florenzano
    14) Hello, Eric Florenzano
    15) Hello, Eric Florenzano
    16) Hello, Eric Florenzano
    17) Hello, Eric Florenzano
    18) Hello, Eric Florenzano
    19) Hello, Eric Florenzano
    20) Hello, Eric Florenzano
    21) Hello, Eric Florenzano

Well there you have it, my attempt at a programming meme.  I hope someone enjoys it!