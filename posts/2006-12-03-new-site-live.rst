---
layout: post
title: "New Site Live!"
date: 2006-12-03T16:23:54-06:00
comments: false
categories: [Pygments, AJAX, Flickr, Digg, Django, Eflorenzano.com, Programming]
published: true
alias: [/blog/post/new-site-live]
---

Hello all!  I have finally put my new website up for the world to see!  I'm still not much for designing the look and feel of websites, but after learning all about Django, I felt like I just had to update my website to use Django.

Under the hood, there is low-level caching being done on both the Digg RSS feed and the Yahoo Flickr feed.  There are two RSS feeds available for the site: new blog posts, and new run information.  To show the graph under runs, I've used some AJAX to get the running data dynamically and create the graph with javascript.  Finally, I've created a custom Django template tag to allow me to post syntax-highlighted code using Pygments.

Example of pygmentized code (the one from this site, actually, that gets my latest digg articles):

.. code-block:: python

    def get_digg_rss():
        d = feedparser.parse('http://www.digg.com/rss/floguy/index2.xml')
        dugg_dicts = cache.get('dugg_dicts')
        if dugg_dicts == None:
            print "Had to re-fetch digg links"
            dugg_dicts = []
            for entry in d.entries:
                dugg_dicts.append({'title':entry.title, 'link':entry.link})
            cache.set('dugg_dicts', dugg_dicts, 60*60)
        return dugg_dicts


I hope that you all enjoy the website, and I also hope that you'll begin to frequent it, because I'll be keeping it up-to-date with the goings-on of my professional life.