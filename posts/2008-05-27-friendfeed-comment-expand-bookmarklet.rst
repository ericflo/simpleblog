---
layout: post
title: "FriendFeed Comment Expand Bookmarklet"
date: 2008-05-27T02:47:57-05:00
comments: false
categories: [jquery, FriendFeed, Bookmarklet, Javascript]
published: true
alias: [/blog/post/friendfeed-comment-expand-bookmarklet]
---

Recently I've been using a lot of FriendFeed_ lately, and found it a bit annoying to expand comments one-by-one, so I wrote a quick bookmarklet to automatically expand all comments out.

Drag this bookmarklet to your bookmarks toolbar to get in on the action:

`Show All Comments`_

By the way, feel free to `follow me`_ on FriendFeed as well to see my various online activities.  I'm in the habit of following people who follow me.

.. _FriendFeed: http://friendfeed.com/
.. _`Show All Comments`: javascript: (function(A){A.parents(".commentexpander").hide();A.parents(".comments").show().find(".hiddencomments").show(100)})(jQuery('.l_showcomments'))
.. _`follow me`: http://friendfeed.com/ericflo