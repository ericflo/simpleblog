---
layout: post
title: "Django Tip: A Denormalization Alternative"
date: 2008-02-15T15:28:06-06:00
comments: false
categories: [Caching, Django, HTML, Restructured Text, Python]
published: true
alias: [/blog/post/django-tip-denormalization-alternative]
---

In creating an any website with textual content, you have the choice of either writing plaintext or writing in a markup language of some kind.  The immediately obvious choice for markup language is HTML (or XHTML), but HTML is not as human-readable as something like Textile_, Markdown_, or `Restructured Text`_.  The advantage of choosing one of those human-readable alternatives is that content encoded using one of them can be translated very easily into HTML.

When one of my friends_ started designing his blog using Django, it got me thinking about how best to deal with that translated HTML.  It seems like a waste to keep re-translating it every time a visitor views the page, but it also seems like it's redundant to keep the translated HTML stored in the database.

Here's my solution to the problem: **cache it**.  For a month.  Here's an example, using Restructured Text:

.. code-block:: python

    from django.db import models
    from django.contrib.markup.templatetags.markup import restructuredtext
    from django.core.cache import cache
    from django.utils.safestring import mark_safe

    class MyContent(models.Model):
        content = models.TextField()

        def _get_content_html(self):
            key = 'mycontent_html_%s' % str(self.pk)
            html = cache.get(key)
            if not html:
                html = restructuredtext(self.content)
                cache.set(key, html, 60*60*24*30)
            return mark_safe(html)
        content_html = property(_get_content_html)

        def save(self):
            if self.id:
                cache.delete('mycontent_html_%s' % str(self.pk))
            super(MyContent, self).save()

What I'm doing here is writing a method which either gets the translated HTML from the cache, or translates it and stores it in the cache for a month.  Then, it returns it as safe HTML to display in a template.  The last thing that we do is override the save method on the model, so that whenever the model is re-saved, the cache is deleted.

There we go!  We now have the HTML-rendered data that we want, and no duplicated data in the database.  Keep in mind that this way of doing things becomes more and more useful the more RAM that your webserver has.

.. _Textile: http://www.textism.com/tools/textile/
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _`Restructured Text`: http://docutils.sourceforge.net/rst.html
.. _friends: http://thauber.com/