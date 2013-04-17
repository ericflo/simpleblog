---
layout: post
title: "Tagging cache keys for O(1) batch invalidation"
date: 2009-03-01T22:46:37-06:00
comments: false
categories: [Memcached, Python, Django, Programming, Software Development]
published: true
alias: [/blog/post/tagging-cache-keys-o1-batch-invalidation]
---

Recently I've been spending some quality time trying to decrease page load times and decrease the number of database accesses on a site I'm working on.    As you would probably suspect, that means dealing with caching.  One common thing that I need to do, however, is invalidate a large group of cache keys when some action takes place.  I've devised a pattern for doing this, and while I'm sure it's not novel, I haven't seen any recent write-ups of this technique.  The base idea is that we're going to add another thin cache layer, and use the value from that first layer in the key to the second layer.

First, let me give a concrete example of the problem that I'm trying to solve.  I'm going to use Django/Python from here on in, but you could substitute anything else, as this pattern should work across other frameworks and even other languages.

.. code-block:: python

    import datetime
    from django.db import models

    class Favorite(models.Model):
        user = models.ForeignKey(User)
        item = models.ForeignKey(Item)
        date_added = models.DateTimeField(default=datetime.datetime.now)

        def __unicode__(self):
            return u'%s has favorited %s' % (self.user, self.item)

Given this model, now let's say that we have a function that gets the Favorite instances for a given user, which might look like this:

.. code-block:: python

    def get_favorites(user, start=None, end=None):
        faves = Favorite.objects.filter(user=user)
        return list(faves[start:end])

There's not much here yet--we're simply filtering to only include the Favorite instances for the given user, slicing it based on the given start and end numbers, and forcing evaluation before returning a list.  Now let's start thinking about how we will cache this.  We'll start by just implementing a naive cache strategy, which in this case simply means that the cache is never invalidated:

.. code-block:: python

    from django.core.cache import cache

    def get_favorites(user, start=None, end=None):
        key = 'get_favorites-%s-%s-%s' % (user.id, start, end)
        faves = cache.get(key)
        if faves is not None:
            return faves
        faves = Favorite.objects.filter(user=user)[start:end]
        cache.set(key, list(faves), 86400 * 7)
        return faves

Now we come to the hard part: how do we invalidate those cache keys?  It's especially tricky because we don't know exactly what keys have been created.  What combinations of start/end have been given? We could invalidate all combinations of start/end up to some number, but that's horribly inefficient and wasteful.  So what do we do?  My solution is to introduce another layer.  Let me explain with code:

.. code-block:: python

    import uuid
    from django.core.cache import cache

    def favorite_list_hash(user):
        key = 'favorite-list-hash-%s' % (user.id,)
        cached_key_hash = cache.get(key)
        if cached_key_hash:
            key_hash = cached_key_hash
        else:
            key_hash = str(uuid.uuid4())
            cache.set(key, key_hash, 86400 * 7)
        return (key_hash, not cached_key_hash)

Essentially what this gives us is a temporary unique identifier for each user, that's either stored in cache or generated and stuffed into the cache.  How does this help?  We can use this identifier in the *keys* to the ``get_favorites`` function:

.. code-block:: python

    from django.core.cache import cache

    def get_favorites(user, start=None, end=None):
        key_hash, created = favorite_list_hash(user)
        key = 'get_favorites-%s-%s-%s-%s' % (user.id, start, end, key_hash)
        if not created:
            faves = cache.get(key)
            if faves is not None:
                return faves
        faves = Favorite.objects.filter(user=user)[start:end]
        cache.set(key, list(faves), 86400 * 7)
        return faves

As you can see, the first thing we do is grab that hash for the user, then we use it as the last part of the key for the function.  The whole ``if not created`` thing is just an optimization that helps to avoid cache fetches when we know they will fail.  Here's the great thing now: invalidating all of the different cached versions of ``get_favorite`` for a given user is a single function call:

.. code-block:: python

    from django.core.cache import cache

    def clear_favorite_cache(user):
        cache.delete('favorite-list-hash-%s' % (user.id,))

By deleting that single key, the next time ``get_favorites`` is called, it will call ``favorite_list_hash`` which will result in a cache miss, which will mean it will generate a new unique identifier and stuff it in cache, meaning that all of the keys for ``get_favorites`` are instantly different.  I think that this is a powerful pattern that allows for coarser-grained caching without really sacrificing much of anything.

There is one aspect of this technique that some people will not like: it leaves old cache keys around taking up memory.  I don't consider this a problem because memory is cheap these days and Memcached is generally smart about evicting the least recently used data.

I'm interested though, since I don't see people posting much about nontrivial cache key generation and invalidation.  How are you doing this type of thing?  Are most people just doing naive caching and calling that good enough?