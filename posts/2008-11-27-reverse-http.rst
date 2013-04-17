---
layout: post
title: "Reverse HTTP"
date: 2008-11-27T12:31:05-06:00
comments: false
categories: [Reverse HTTP, HTTP, Web Hooks, Programming]
published: true
alias: [/blog/post/reverse-http]
---

Yesterday I `wrote about Web Hooks`_ and how powerful it could be if one web
service sends HTTP requests to another web service.  Today I want to take that
concept one step further.  What if you tell that service that you would like it
to send a POST request back to **you**, whenever an event happens?  This slight
modification makes for a very powerful tool.

Let's take the example of popular real-time web applications like Facebook's
instant messenger or FriendFeed's "Real-time" view.  Both of these services make
use of a technique called `long polling`_, where the client sends an HTTP
request and the server does not respond until it has some event to deliver.  The
client can only keep the request open for so long, so it periodically times out
and re-sends the request. (It also re-sends the request if it does receive some
data).

The problem with this technique is that it's really trying to turn a client into
a server.  It's really fighting against the way that HTTP wants to work.  So why
fight it?  Imagine that all of our browsers have simple, lightweight, HTTP
servers installed.  The client could request to upgrade to reverse HTTP, and
then the *server* could initiate a connection with the *client*.  Now, as events
come in to the web service, the service could directly send those updates to the
client.

Going back to the example of Facebook IM, here's how that would work: When I
open a Facebook page, my client sends a request to Facebook's IM server.
Facebook's IM server sends a response with the HTTP/1.1 Upgrade header reading
"PTTH/0.9"  (funny, huh?).  Then, the client knows to accept an HTTP connection
from Facebook's IM server.  Facebook's IM server then opens that connection with
the client, and sends HTTP POSTs every time it receives a new instant message
that the client should receive.  The client's web browser would have some
JavaScript hooks to parse the body of those requests, so that it could update
the content of the instant message window on the page.

Isn't this brilliant?  It directly meshes with the HTTP protocol, and makes this
system which seems like a hack right now, instantly become an elegant solution.
I really wish I could take credit for thinking this up, but I did not.  My
coworker `Donovan Preston`_ blew my mind with this a few weeks back.  If you're
looking for a more visual example of how this might work, or a reference
implementation of the protocol in action, check out `this wiki page`_.

.. _`wrote about Web Hooks`: http://www.eflorenzano.com/blog/post/web-hooks/
.. _`long polling`: http://cometdaily.com/2007/11/16/more-on-long-polling/
.. _`Donovan Preston`: http://ulaluma.com/pyx/
.. _`this wiki page`: http://wiki.secondlife.com/wiki/Reverse_HTTP