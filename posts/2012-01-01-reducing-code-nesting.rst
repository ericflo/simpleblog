---
layout: post
title: "Reducing Code Nesting"
date: 2012-01-01T18:00:00-08:00
comments: false
categories: [Programming, Observations]
published: true
---

"This guy's code sucks!"  It's something we've all said or thought when we run
into code we don't like.  Sometimes it's because it's buggy, sometimes it's
because it conforms to a style we don't like, and sometimes it's because it
just feels wrong.  Recently I found myself thinking this, and automatically
jumping to the conclusion that the developer who wrote it was a novice.  The
code had a distinct property that I dislike: lots of nesting.  But the more I
think about it, the more I realized that it's not really something I've heard
discussed much.

So let's talk about it.  I'm going to first talk about what I mean by nesting,
why I think it's a bad quality, and then I'm going to go over some tricks I've
learned over the years to reduce it.


What do I mean by code nesting, and why is it bad?
--------------------------------------------------

It's easier to demonstrate rather than talk about it.  This is what I mean by
deep code nesting, with my apologies for the contrived example:
 
.. code-block:: python

    def get_cached_user(user_id=None, username=None):
        """
        Returns a cached user object either by their user_id or by their username.
        """
        user = cache.get_user_by_id(user_id)
        if not user:
            user = cache.get_user_by_username(username)
            if not user:
                user = db.get_user_by_id(user_id)
                if not user:
                    user = db.get_user_by_username(username)
                    if not user:
                        raise ValueError('User not found')
                cache.set_user(user, id=user.id, username=user.username)
        return user


You can see in this Python code just by looking at the indentation level that
there's lots of nesting.  Before we can determine that the user was not found,
we must pass through four conditionals, and each conditional is nested within
the previous conditional.

I argue that this is bad code.  Every added level of nesting is another piece
of context that your brain has to keep track of.  Each nested block is one you
have to line up by eye to see what conditional it lines up with (even if your
editor helps at this with visuals, it doesn't remove the issue entirely.)  And
this is just a straightforward example where we just return the user at the
end, let's take a look at an example that does something more complicated:

.. code-block:: python

    def get_media_details(media):
        """
        Returns a dictionary of extra data about the given media object.
        """
        data = {}
        if media.is_video:
            data['kind'] = 'video'
            if media.is_youtube:
                data['url'] = 'http://youtube.com/'
            if media.is_vimeo:
                data['vimeo'] = True
                if media.vimeo_version == 2:
                    data['url'] = 'http://vimeo.com/v2/'
            if 'url' in data:
                data['secure_url'] = data['url'].replace('http:', 'https:')
        elif media.is_audio:
            data['kind'] = 'audio'
        elif media.is_text:
            data['kind'] = 'text'
        if 'kind' in data:
            data['kind_verbose'] = {
                'video': 'Video Stream',
                'audio': 'Audio File',
                'text': 'Text Content',
            }[data['kind']]
        return data

It was unbelievably hard for me to even write that last example.  It's
obviously contrived and such, but the point is that it's so difficult to
even understand what it's doing.  Unlike the previous example, this doesn't
simply nest and then return; it nests and then un-nests, and then nests again,
and then finally returns.


How to Avoid Nesting
--------------------

The best way that I've discovered to avoid nesting is to return early.  Caching
is the perfect example of this.  Instead of testing for a cache failure and
fetching from the database inside the conditional, check for cache success and
return that early.

So this code:

.. code-block:: python

    def get_cached_user(user_id):
        user = cache.get_user_by_id(user_id)
        # The main logic all happens in this nested block
        if not user:
            user = db.get_user_by_id(user_id)
            cache.set_user_for_id(user_id, user)
        return user

Becomes this:

.. code-block:: python

    def get_cached_user(user_id):
        user = cache.get_user_by_id(user_id)
        if user:
            return user
        # The main logic happens outside of the nested block
        user = db.get_user_by_id(user_id)
        cache.set_user_for_id(user_id, user)
        return user

In the simple case, it doesn't seem to improve much, but what happens if we
apply this technique to our first example?  It's dramatically improved:

.. code-block:: python

    def get_cached_user(user_id, username):
        # First check the cache by id
        user = cache.get_user_by_id(user_id)
        if user:
            return user
        
        # Now check the cache by username
        user = cache.get_user_by_username(username)
        if user:
            return user
        
        # Both caches failed, so try hitting the db for the id
        user = db.get_user_by_id(user_id)
        if user:
            cache.set_user(user, id=user.id, username=user.username)
            return user
        
        # Looks like that didn't exist, try the username
        user = db.get_user_by_username(username)
        if not user:
            raise ValueError('User not found')
        
        # Cache our final user value for future use
        cache.set_user(user, id=user.id, username=user.username)
        return user


Not only does it make it easier to read top-to-bottom, and force us to keep
track of way less context, and make our code editors do less line wrapping,
but it also makes it easier to separate the blocks of code and more easily
comment them.

So what other techniques can we use?  It starts to depend more on the
situation.  Are you nesting because you're writing a bunch of callbacks?  If
so, you can usually restructure your code to use named functions instead of
anonymous functions.  Here's how that would might look before refactoring:

.. code-block:: javascript

    function getCachedUser(userId, callback) {
        cache.getUser(userId, function(user) {
            if(user) {
                return callback(user);
            }
            db.getUser(userId, function(user) {
                cache.setUser(userId, user, function() {
                    callback(user);
                });
            });
        });
    }

Note that in this example we even applied the technique of returning early in
the first callback function, but as you can see there's still a bunch of
nesting going on.  Now if we switch to using named functions?

.. code-block:: javascript

    function curry(fn) {
        var slice = Array.prototype.slice;
        var args = slice.apply(arguments, [1]);
        return function () {
            return fn.apply(null, args.concat(slice.apply(arguments)));
        };
    }

    function final(callback, user) {
        callback(user);
    }

    function dbResult(callback, userId, user) {
        cache.setUser(userId, user, curry(final, callback, user));
    }

    function cacheResult(callback, userId, user) {
        if(user) {
            return callback(user);
        }
        db.getUser(userId, curry(dbResult, callback, userId));
    }

    function getCachedUser(userId, callback) {
        cache.getUser(userId, curry(cacheResult, callback, userId));
    }

This is a lot better in terms of nesting.  Unfortunately we had to write a
helper function called curry, but that only has to be written once and can be
re-used for all code written in this style.  Also unfortunately I still find
this kind of code difficult to follow, which is why I avoid writing much
callback-style code.  However, at least you can reduce the nesting.  In all
honesty, there are probably better ways of reducing nesting that I'm not aware
of.  If you can rewrite the ``getCachedUser`` function in JS in a better way,
please blog it!

Another way to reduce nesting is to assign an intermediate variable.  Here's
an example in Erlang of some file function that nests a case statement within
another case statement.

.. code-block:: erlang

    do_some_file_thing(File) ->
        case file:open(File, [raw, binary, read]) of
            {ok, Fd} ->
                Start = now(),
                case process_file_data(Fd) of
                    {ok, Processed} ->
                        {ok, Start, now(), Processed};
                    Error ->
                        Error
                end;
            Error ->
                Error
        end.

We can assign to an intermediate "Resp" variable, and bring that second case
statement out into the function's main code block, like so:

.. code-block:: erlang

    do_some_file_thing(File) ->
        Resp = case file:open(File, [raw, binary, read]) of
            {ok, Fd} ->
                {timestamp, now(), process_file_data(Fd)};
            Error ->
                Error
        end,
        case Resp of
            {timestamp, Start, {ok, Processed}} ->
                {ok, Start, now(), Processed};
            {timestamp, Start, Error} ->
                Error;
            Error ->
                Error
        end.


What does this all mean?
------------------------

At the end of the day, this isn't going to make or break you as a programmer.
In fact, nothing I've mentioned even changes the code's logic, but simply its
implementation.  It's simply something to think about as you code, as you read
other people's code.  Hopefully you agree with me that less nesting is an
admirable goal, and you find more and more ways to achieve it.

Discuss this post `on Hacker News`_.

.. _`on Hacker News`: http://news.ycombinator.com/item?id=3414526