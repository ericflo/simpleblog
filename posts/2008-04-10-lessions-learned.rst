---
layout: post
title: "Lessons Learned"
date: 2008-04-10T12:08:40-05:00
comments: false
categories: [Django, Eric S. Raymond, George Patton, Reusable Apps, Software Development, Wisdom]
published: true
alias: [/blog/post/lessions-learned]
---

Yesterday I came across a quote from `George Patton`_ (via_), which stuck me as really insightful, but later something burned the quote directly into my brain.

  --  A good plan, violently executed now, is better than a perfect plan next week.--  

It's a quote which rings quite similar to the commonly-said open source phrase, coined by `Eric S. Raymond`_ in his article `The Cathedral and the Bazaar`_.

  "Release early.  Release often."

The thing which burned these ideas into my brain is the discovery of djangoplugables.com_.  Simply put: this is an excellent site, which follows the ideas that I mentioned above completely.  The premise behind it is essentially to list all of the available django reusable applications on google code, and to display a bit of information about each app.

A group of about 5 people, including myself, have been silently working on a very similar site for the past month or so (the bulk of our work took place during PyCon), but we utterly failed to follow the above sentiment.  We debated for hours over how users would be able to submit applications, claim them, and how we could ensure that those claims were accurate.  We had tagging, voting, comments, voting ON comments, graphs detailing how "hot" each application was (based on a frequency analysis of the votes over time), and OpenID integration.

But all of this functionality took time, and we implemented it behind closed doors, in a vacuum--without ever seriously focusing on the user interface.  I don't know yet what will become of all of our work, but I have a feeling that it will be discontinued in favor of the much better-looking and simpler djangoplugables.com_.  Maybe we'll see parts of it resurface again, but that's not really the message behind this post.  The real message to take away from this experience is that we should practice what we so often preach.  In the case of web development, execute the good plan now and iterate, versus trying to perfect everything before release.

The upside of all of this is that our goal has been achieved.  What we really wanted to accomplish is what now exists: an excellent resource for finding reusable django applications, and no matter who implements it, that's a win for everyone!

.. _`George Patton`: http://en.wikipedia.org/wiki/George_S._Patton
.. _via: http://www.37signals.com/svn/posts/944-george-patton-quotes
.. _`Eric S. Raymond`: http://www.catb.org/~esr/
.. _`The Cathedral and the Bazaar`: http://www.firstmonday.org/issues/issue3_3/raymond/#d4
.. _djangoplugables.com: http://djangoplugables.com/