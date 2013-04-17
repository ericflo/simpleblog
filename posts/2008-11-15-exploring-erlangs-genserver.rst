---
layout: post
title: "Exploring Erlang's gen_server"
date: 2008-11-15T22:20:40-06:00
comments: false
categories: [gen_server, Presence, Erlang, Programming]
published: true
alias: [/blog/post/exploring-erlangs-genserver]
---

Today I found myself at `Super Happy Dev House`_, amongst a whole house full
of geeks (I say this in the most friendly way possible).  I thought for a while
about working on Pinax_ project, which is what I really wanted to do.  However,
it didn't seem geeky enough for the occasion.

No, today the call of the geek was too strong.  There was only one place to turn
to achieve maximal geekiness: functional programming.  Not only functional
programming, but I thought this occasion called for a concurrency-oriented
programming language. Yes, today was the perfect day for some Erlang.

I've done a few small projects with Erlang, but never before have I used OTP_.
So the goal is to write an OTP ``gen_server`` which would store a user's
"presence" (think Twitter_, Pownce_, etc.) in memory.  No, it's not a good idea.
Yes, it's kind of fun.  So here we go!

First we need to decide on an API:

.. code-block:: erlang

    start_link() ->
        gen_server:start_link({local, ?SERVER}, ?MODULE, [], []).

    post_presence(UserID, Presence) ->
        gen_server:cast(?SERVER, {post_presence, UserID, Presence}).

    list_presence(UserID) ->
        gen_server:call(?SERVER, {list_presence, UserID}).

    list_presence(UserID, Limit) ->
        gen_server:call(?SERVER, {list_presence, UserID, Limit}).

    public_list(Limit) ->
        gen_server:call(?SERVER, {public_list, Limit}).
    
``start_link`` will start the server.  ``post_presence`` will post a user's
current presence to the server.  ``list_presence`` with one argument gets all
of the specified user's presence information.  With a second argument, it limits
the amount of returned presence information to the specified number. Calling
``public_list`` means that you're getting the latest posts from anyone.

Before that, though, let's get some of the ``gen_server`` cruft out of the way:

.. code-block:: erlang

    -module(presence_database).
    -behavior(gen_server).

    -define(SERVER, ?MODULE).

    %% gen_server API
    -export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2,
        code_change/3]).

    %% presence API
    -export([start_link/0, post_presence/2, list_presence/1, list_presence/2,
        public_list/1]).

    handle_info(_Info, State) ->
        {noreply, State}.

    terminate(_Reason, _State) ->
        ok.

    code_change(_OldVersion, State, _Extra) ->
        {ok, State}.

    init([]) ->
        {ok, dict:new()}.

These are mostly things that we need to have in order for things to work.  We
define our module name, the behavior that this module mimics, and define a
constant.  Then, we export the required functions for gen_server and export
our public presence api functions.  Finally we implement really simple functions
for those gen_server functions that we don't care much about.

Now since I couldn't figure out how to slice a list in Erlang, I wrote my own
slice function.  Make sure to flame me for this.

.. code-block:: erlang

    slice(List, Start, End) ->
        slice(List, Start, End, 0, []).

    slice([], _Start, _End, _Index, Acc) ->
        lists:reverse(Acc);
    slice([Item | Rest], Start, End, Index, Acc) ->
        case Index >= Start of
            true ->
                case Index < End of
                    true ->
                        slice(Rest, Start, End, Index + 1, [Item | Acc]);
                    false ->
                        slice(Rest, Start, End, Index + 1, Acc)
                end;
            _ ->
                slice(Rest, Start, End, Index + 1, Acc)
        end.

...and I'm pretty sure that using `guard expressions`_ this could be done in one
case statement.  Or maybe it could be done in a single list comprehension.  I
don't know.  This works for our purposes.

Now we have to write functions called ``handle_cast`` and ``handle_call``.
``handle_cast`` is essentially a server function which you don't expect a
response from.  Messages can queue up to this function and they will be handled
sequentially but never return any value to the caller.  ``handle_call`` is
exactly the opposite.  The caller is expecting a response, so this is a blocking
operation.

Let's use ``handle_cast`` to accept new presence notifications:

.. code-block:: erlang

    handle_cast({post_presence, UserID, Presence}, State) ->
        case dict:is_key(UserID, State) of
            true ->
                {noreply, dict:append(UserID, {erlang:now(), Presence}, State)};
            _ ->
                {noreply, dict:store(UserID, [{erlang:now(), Presence}], State)}
        end;
    handle_cast(_Msg, State) ->
        {noreply, State}.

In essence, we check to see if the user has registered their presence, and if
so, we add their presence to their presence list.  If they haven't submitted
their presence before, we create a new presence list for them and add their
submitted presence to that list.  We have also generated a catchall version
of the function for when the call doesn't match the signature
``{post_presence, UserID, Presence}`` for some reason.

Now let's do the harder one: the call to get various presence information from
our server:

.. code-block:: erlang

    userfy_list(User, List) ->
        lists:map(fun({Time, Msg}) -> {User, Time, Msg} end, List).

    handle_call({list_presence, UserID}, _From, State) ->
        case dict:find(UserID, State) of
            {ok, Value} ->
                {reply, Value, State};
            error ->
                {reply, {error, user_does_not_exist}, State}
        end;
    handle_call({list_presence, UserID, Limit}, _From, State) ->
        case dict:find(UserID, State) of
            {ok, Value} ->
                {reply, lists:nthtail(Limit, Value), State};
            error ->
                {reply, {error, user_does_not_exist}, State}
        end;
    handle_call({public_list, Limit}, _From, State) ->
        LatestEntries = lists:flatten([userfy_list(User, List) || {User, List} <- dict:to_list(State)]),
        Sorted = lists:sort(fun({_, A, _}, {_, B, _}) -> A > B end, LatestEntries),
        {reply, slice(Sorted, 0, Limit), State};
    handle_call(_Request, _From, State) ->
        {reply, ok, State}.

The first version of ``handle_call`` is very straightforward.  It simply looks
up the list of presence information for a given user and returns that in
the reply.  The second version does a similar thing, but calls ``lists:nthtail``
on the value to limit the number of presence data that is included in that list.

The final version of ``handle_call`` is the most complicated, because we want to
get information about everyone, order it by the date that it was posted, and
limit the number of returned results by the specified limit.  An added
complexity is that we have to change the data format to include the name of the
user who posted it.

First it uses a list comprehension to take the state dictionary and run our
``userfy_list`` function on every User/List pair.  This will add the user to the
presence tuple.  Then we flatten that list to be just a single list of userfied
tuples.  Then, we sort that by the middle value (the timestamp of the presence).
Finally, we use our newly-created slice function to take just the slice of
information that we care about and return it to the user.  Again, there is a
catchall ``handle_call`` which discards incorrectly-formatted messages.

Demo
----

.. code-block:: erlang

    1> c(presence_database).
    {ok,presence_database}
    2> presence_database:start_link().
    {ok,<0.37.0>}
    3> presence_database:post_presence("ericflo", "I am at Super Happy Dev House").
    ok
    4> presence_database:post_presence("ericflo", "I am writing erlang code").
    ok
    5> presence_database:post_presence("dreid", "I am having fun at SHDH").
    ok
    6> presence_database:list_presence("ericflo").
    [{{1226,816100,955},"I am at Super Happy Dev House"},
     {{1226,816113,249498},"I am writing erlang code"}]
    7> presence_database:list_presence("dreid").
    [{{1226,816135,937300},"I am having fun at SHDH"}]
    8> presence_database:public_list(5).
    [{"dreid",{1226,816135,937300},"I am having fun at SHDH"},
     {"ericflo",{1226,816113,249498},"I am writing erlang code"},
     {"ericflo",
      {1226,816100,955},
      "I am at Super Happy Dev House"}]
    9> presence_database:public_list(2).
    [{"dreid",{1226,816135,937300},"I am having fun at SHDH"},
     {"ericflo",{1226,816113,249498},"I am writing erlang code"}]

Conclusions
-----------

This really isn't robust.  If we wanted it to be more robust, we should use
some sort of persistent storage, we should use more than one process and do some
sort of consistent hashing to distribute the load, and we should have a
supervisor process to ensure that crashed processes restart correctly and reload
their data.

All of that is the case, but yet through this simple exercise I've learned a ton
about Erlang's ``gen_server`` module.  I don't know if my explanations will do
people any good, but hopefully they give a glimpse into the world of Erlang.  So
now that all of that is said, show me how to slice in Erlang!

**EDIT:** Commenter *Mihai* has made me aware of the ``lists:sublist`` function, which does exactly what I want.  I can now discard my crappy slice function.

.. _`Super Happy Dev House`: http://superhappydevhouse.org/
.. _Pinax: http://pinaxproject.com/
.. _OTP: http://www.erlang.org/doc/design_principles/part_frame.html
.. _Twitter: http://twitter.com/
.. _Pownce: http://pownce.com/
.. _`guard expressions`: http://www.erlang.org/doc/reference_manual/expressions.html#guards