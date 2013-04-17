---
layout: post
title: "First Two Django Screencasts"
date: 2008-07-12T22:09:49-05:00
comments: false
categories: [Python, Django, Screencast, Programming]
published: true
alias: [/blog/post/first-two-django-screencasts]
---

It's always been a goal of mine to post screencasts here on my blog, but for whatever reason I never ended up getting around to it.  Today, that all changes as I have created two new screencasts.  Of course, this space is already very well-covered by both `Michael Trier`_ and `Brian Rosner`_, so hopefully this adds something new to the conversation.

Setting up a Django Development Environment
----------------------------------------------------------

In this screencast I show how I typically set up my Django development environment.  It goes through installing Django by checking out the latest development version and linking it to the correct places on your system.  It also talks about how to install reusable applications.  Finally, it covers how to update all of those projects and keep a toolbox of snippets for your personal use.

.. raw:: html
    
    <embed src="http://blip.tv/play/AcH7agA" type="application/x-shockwave-flash" width="720" height="510" allowscriptaccess="always" allowfullscreen="true"></embed>

The simple pylink command that I use in the screencast is this:

.. code-block:: python

    #!/bin/bash
    ln -s `pwd`/$1 `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/$1

**UPDATE:** `Joshua Uziel`_ has sent me a much more robust version of this script, which handles the edge cases much better.  I highly recommend using this version instead of my one-liner.

.. code-block:: bash

    #!/bin/bash

    SITE_PACKAGES="$HOME/prog/python/site-packages"

    if [ ! $SITE_PACKAGES ]
    then
        SITE_PACKAGES=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
    fi

    BASE=`basename $1`
    DIR=`dirname $1`

    cd $DIR
    ln -sfnv `pwd`/$BASE $SITE_PACKAGES/$BASE

**UPDATE2:** `Zachary Voase`_ has updated this new version, and it seems to be even more improved.  I'm loving this!  He has also written a "pyunlink" script, which can be found here_.

Please let me know in the comments if you have any other tips and tricks for setting up a development environment for Django.

Using Django-Pagination
------------------------

Django-pagination_ is an application that I wrote and released a while ago, which I use *all the time*, but that hasn't really seen much attention.  In this screencast, I show how to take an existing project with too much data on one page, and use django-pagination_ to quickly and easily paginate the items on the page.  There is a bit more documentation for the project that's available in the project directory if you do a subversion checkout, and docstrings throughout the source code, if you're interested in how it works.

.. raw:: html
    
    <embed src="http://blip.tv/play/AcH4UAA" type="application/x-shockwave-flash" width="720" height="510" allowscriptaccess="always" allowfullscreen="true"></embed>

Keep in Mind
------------

These are my very first screencasts, ever.  I'm not entirely sure what I'm doing yet, and the only way I can improve is by your feedback.  If you have any advice and/or criticisms of these screencasts, please don't keep your mouth shut--speak up, and let me know in the comments.  Hopefully someone finds these useful, and thanks for watching!

.. _`Michael Trier`: http://blog.michaeltrier.com/screencasts
.. _`Brian Rosner`: http://oebfare.com/blog/2008/jan/23/using-git-django-screencast/
.. _Django-pagination: http://code.google.com/p/django-pagination/
.. _django-pagination: http://code.google.com/p/django-pagination/
.. _`Joshua Uziel`: http://www.uzix.org/
.. _`Zachary Voase`: http://gist.github.com/21649
.. _here: http://gist.github.com/21650