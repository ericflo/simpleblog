---
layout: post
title: "Syntax Highlighting"
date: 2008-02-21T19:12:01-06:00
comments: false
categories: [Python, Restructured Text, Syntax Highlighting]
published: true
alias: [/blog/post/syntax-highlighting]
---

Over the past week, I've had several people write me asking how I prefer to do syntax highlighting.  It's funny that this question cropped up now, just as I changed the way that it's handled on this blog.  The way that I used to do it was what I `posted to djangosnippets`_ almost a year ago: use a regular expression to parse out ``<code></code>`` blocks, highlight the stuff in-between, and spit it back out.

The problem with that method was that that would require some more sophisticated logic now that I'm using RestructuredText_ to write all of my posts.  Unwilling to think any harder than necessary, I did a quick `google search`_, and the second result was exactly what I was looking for: a RestructuredText directive_, ready-made by the Pygments_ people.

The trick is to put `this file`_ somewhere on your python path.  Then, in the ``__init__.py`` of one of the Django apps that will use syntax highlighting, just import the file.  It's **that simple**!  (I love RestructuredText.)  But it's not only RestructuredText that benefits from this style of plugin.  Markdown_, too, has a `similar plugin`_--again provided by the Pygments people.

.. code-block:: restructuredtext

    .. code-block:: python

        print "This is an example of how to use RestructuredText's new directive."

I hope that this answers some of the questions that people had.  On a similar note, I'm extremely happy to see that people have been finding the `Contact Me`_ link on the right side of the page.  Please continue to send me any questions and comments that you have for me!

.. _`posted to djangosnippets`: http://www.djangosnippets.org/snippets/25/
.. _RestructuredText: http://docutils.sourceforge.net/rst.html
.. _`google search`: http://www.google.com/search?q=restructured+text+pygments
.. _directive: http://docutils.sourceforge.net/docs/ref/rst/directives.html
.. _Pygments: http://pygments.org/
.. _`this file`: http://dev.pocoo.org/projects/pygments/browser/external/rst-directive.py
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _`similar plugin`: http://dev.pocoo.org/projects/pygments/browser/external/markdown-processor.py
.. _`Contact Me`: http://www.eflorenzano.com/contact/