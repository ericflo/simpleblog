---
layout: post
title: "Drop-dead simple Django caching"
date: 2008-11-28T23:30:13-06:00
comments: false
categories: [Python, Django, Caching, Programming]
published: true
alias: [/blog/post/drop-dead-simple-django-caching]
---

Caching is easy to screw up.  Usually it's a manual process which is error-prone
and tedious.  It's actually quite easy to cache, but knowing when to invalidate
which caches becomes a lot harder.  There is a subset of caching the caching
problem that, with Django, can be done quite easily.  The underlying idea is
that every Django model has a primary key, which makes for an excellent key to
a cache.  Using this basic idea, we can cover a fairly large use case for
caching, automatically, in a much more deterministic way.  Let's begin.

First, we need to decide upon a setting for how long each individual item should
be saved in the cache.  I'm going to call that ``SIMPLE_CACHE_SECONDS`` and
grab it like so:

.. code-block:: python

    from django.conf import settings
    
    SIMPLE_CACHE_SECONDS = getattr(settings, 'SIMPLE_CACHE_SECONDS', 2592000)

The next thing we need to do is be able to generate a cache key from an instance
of a model.  Thanks to Django's ``_meta`` information, we can get the app label
and model name, plus the primary key, and we're all set.

.. code-block:: python

    def key_from_instance(instance):
        opts = instance._meta
        return '%s.%s:%s' % (opts.app_label, opts.module_name, instance.pk)

So now let's start setting the cache!  My preferred way to do it is via a
signal, but you could do it in a less generic way by overriding ``save`` on a
model.  My signal looks like this:

.. code-block:: python

    from django.core.cache import cache
    from django.db.models.signals import post_save
    
    def post_save_cache(sender, instance, **kwargs):
        cache.set(key_from_instance(instance), instance, SIMPLE_CACHE_SECONDS)
    post_save.connect(post_save_cache)

Now that we're putting items in the cache, we should probably delete them from
the cache when the model instance is deleted:

.. code-block:: python

    from django.db.models.signals import pre_delete
    
    def pre_delete_uncache(sender, instance, **kwargs):
        cache.delete(key_from_instance(instance))
    pre_delete.connect(pre_delete_uncache)

This is all good and well, but right now we don't really have a way to get at
that information.  Cache is pretty useless if we never use it!  Our interface to
the database is through the model's ``QuerySet``, so let's make sure that our
QuerySet is making good use of our newly-populated cache.  To do so, we'll
subclass ``QuerySet``:

.. code-block:: python

    from django.db.models.query import QuerySet

    class SimpleCacheQuerySet(QuerySet):
        def filter(self, *args, **kwargs):
            pk = None
            for val in ('pk', 'pk__exact', 'id', 'id__exact'):
                if val in kwargs:
                    pk = kwargs[val]
                    break
            if pk is not None:
                opts = self.model._meta
                key = '%s.%s:%s' % (opts.app_label, opts.module_name, pk)
                obj = cache.get(key)
                if obj is not None:
                    self._result_cache = [obj]
            return super(SimpleCacheQuerySet, self).filter(*args, **kwargs)

The only method that we really need to overwrite is ``filter``, since ``get``
and ``get_or_create`` both just rely on filter anyway.  The first ``for`` loop
in the filter method just checks to see if there is a query by ``id`` or ``pk``,
and if so, then we construct a key and try to fetch it from the cache.  If we
found the item in the cache, then we place it into Django's internal result
cache.  At that point we're as good as done.  Then we just let Django do the
rest!

This ``SimpleCacheQuerySet`` won't be used all on its own though, we need to
actually force a model to use it.  How do we do that?  We create a manager:

.. code-block:: python

    from django.db import models

    class SimpleCacheManager(models.Manager):
        def get_query_set(self):
            return SimpleCacheQuerySet(self.model)

Now that we have this transparent caching library set up, we can go around to
all of our models and import it and attach it as needed.  Here's how that might
look:

.. code-block:: python

    from django.db import models
    from django_simplecache import SimpleCacheManager
    
    class BlogPost(models.Model):
        title = models.TextField()
        body = models.TextField()

        objects = SimpleCacheManager()

That's it!  Just by attaching this manager to our model we're getting all the
benefits of per-object caching right away. Of course, this isn't comprehensive.
It does hit the vast majority of use cases, though.  If you were to use this for
a real site, however, then you wouldn't be able to use ``update`` method.  It's 
a little bit trickier since there's no ``post_update`` signal, but it's nowhere
near impossible. Let's just say that, for now, it's being left unimplemented as
an exercise for the reader. ``in_bulk`` would be actually quite fun to 
implement, too, because you could get all of the results possible from cache, 
and all the rest could be gotten from the database, then merge those two
dictionaries before returning.

I think this would be a really good reusable Django application.  Essentially,
we've grown a library from the ground up that really isn't all that much code.
I think it took me 20 minutes to write the actual code, but with some serious
polish and love, this library could evolve into something that I think many
reusable apps would use to great benefit.  What do you think?  What should a
good, simple, Django caching library have?