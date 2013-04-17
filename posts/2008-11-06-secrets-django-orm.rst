---
layout: post
title: "Secrets of the Django ORM"
date: 2008-11-06T11:14:54-06:00
comments: false
categories: [Databases, Django, Programming, Python]
published: true
alias: [/blog/post/secrets-django-orm]
---

You won't see this in the Django documentation, you won't see it mentioned on
other blogs, and you certainly won't hear the core developers of Django boasting
about it, but Django's ORM has a secret weapon: it supports SQL *group_by* and
*having* clauses, and it has for quite some time.

It's not part of the public ``QuerySet`` API, but rather a part of the private
``Query`` API.  But just because it's not part of the public API doesn't mean
that it's not easy to use--it just means that it might change in the future.
So it's really a "use at your own risk" type of deal now.  If you're up for
keeping on top of things so that you know what to change when the next version
of Django comes out, then read on.  First, let's start with some model
definition:

.. code-block:: python

    class TumbleItem(models.Model):
        title = models.CharField(max_length=255)
        item_type = models.CharField(max_length=50)

        def __unicode__(self):
            return '%s: "%s"' % (self.item_type, self.title)

A simple tumblog item.  Very simple, as in, not really useful at all.  But
that's OK since this is just a demonstration.  To demonstrate, let's create
some data:

.. code-block:: pycon

    >>> ti1 = TumbleItem.objects.create(title='Blog Post 1', item_type='blog')
    >>> ti2 = TumbleItem.objects.create(title='Blog Post 2', item_type='blog')
    >>> ti3 = TumbleItem.objects.create(title='Blog Post 3', item_type='blog')
    >>> ti4 = TumbleItem.objects.create(title='Article Dugg 1', item_type='digg')
    >>> ti5 = TumbleItem.objects.create(title='Article Dugg 2', item_type='digg')
    >>> ti6 = TumbleItem.objects.create(title='Link Saved 1', item_type='link')

OK now that we've loaded some data, let's use the group_by functionality!

.. code-block:: pycon

    >>> qs = TumbleItem.objects.all()
    >>> qs.query.group_by = ['item_type']
    >>> item_types = [i.item_type for i in qs]
    >>> item_types
    [u'blog', u'digg', u'link']

There we go, it's quick, easy, and it seems to Just Work. But let's try to grab
only the item_types which have more than one item:

.. code-block:: pycon

    >>> qs = TumbleItem.objects.all()
    >>> qs.query.group_by = ['item_type']
    >>> qs.query.having = ['COUNT(item_type) > 1']
    >>> item_types = [i.item_type for i in qs]
    >>> item_types
    [u'blog', u'digg']

And now we've successfully used the group_by and having functionality in the
Django ORM.  I'm excited for some aggregation functionality to start being
exposed as a public API, as I'm sure it will be more elegant than this solution,
but at the same time this is a neat hidden secret in the Django ORM.  Well now
you have the knowledge, so you have the power, and it's up to you to use it wisely!