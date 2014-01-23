---
layout: post
title: "React: Finally, a great server/client web stack"
date: 2013-01-23T12:29:00-08:00
comments: false
categories: [React, ReactJS, Programming, Server, Client, Javascript]
published: true
---

We started with static websites, simple pages that could link between each
other.  Then we started constructing those pages on demand, customizing the
contents of the page for each individual user.  Next we started using
Javascript to add more interactivity, and these pages started to become more
like applications.  But now we have XMLHttpRequest, and most new projects are
moving towards building their pages entirely in the browser.

But when we do it purely in the browser, we have to make quite a few
concessions: search engines have a hard time indexing that content, for
example. It also takes longer for users to see the rendered content (not in
every case, but in many, many cases.)  Also if you're using a lot of plugins
for your favorite library, or a heavyweight MVC framework, sometimes it can
slow down interactivity.

I've thought for a long time (`and blogged about it previously`_) that the
ideal solution would fully render the markup on the server, deliver it to the
client so that it can be shown to the user instantly.  Then it would
asynchronously load some Javascript that would attach to the rendered markup,
and invisibly promote the page into a full app that can render its own markup.
This code would also have to be fast enough to meet or exceed the performance
of other modern solutions, or it won't be worth it.

What I've discovered is that enough of the pieces have come together, that this
futuristic-sounding web environment is actually surprisingly easy to do now
with `React.js`_.  React isn't a full-fledged framework, it's a library, so
you'll have to build your own foundation and write some glue code.  I've been
rewriting an existing website in React (usually a terrible idea, we'll see
about this time), and now that the code is settling down a little bit, I'd like
to share how it works.  This post will just be an overview, but up next I'll
share some of my glue code and lessons learned etc.

`React.js`_
===========

First, a bit about React.  It was released by Facebook and was apparently a
collaboration between the Instagram and Facebook web engineers.  It looks
similar in shape but not in size to Angular.js, but even though it looks
similar, it has a very different philosophy underneath.  React has a few key
ideas: a virtual DOM, a component framework, and a Javascript syntax extension.

Virtual DOM
~~~~~~~~~~~

The key innovation of React is that it has a pure-Javascript reimplementation
of the browser's DOM.  It builds the DOM tree in Javascript and then has two
options for output: a root browser element, or a string.  How can it output
to a root browser element without having horrible performance?  Core to React
is a tree diffing algorithm that can look at the in-memory virtual DOM, and the
real browser DOM, and build the optimal diff.  Then it applies that diff to the
browser's DOM.

The second option for output is equally interesting to me though.  If you can
walk this virtual DOM tree and render to a string, then you can do that all
on the server and then send it down to the client.  And since it's a tree,
React simply stores a checksum in a data attribute on the root node, and if
those checksums match, then React will simply attach its event handlers and do
nothing more.

Component Framework
~~~~~~~~~~~~~~~~~~~

React's component framework is how you construct that virtual DOM.  Each
component has a ``render()`` function which returns a virtual DOM node with any
number of children and event handlers attached.  So at its core, React
components are widgets that can render themselves and react to user input.  At
render time, components should only access two instance objects: ``props``, and
``state``.

Props are passed-in and are immutable, whereas state is assigned and updated
entirely by the component itself.  Callback functions can be passed from parent
node to child node, as ``props``, and attached directly to the virtual DOM
nodes in the ``render()`` function.  In fact, that's the primary way that
components communicate with each other.

These components have a lifecycle, and ways to hook into state and prop
changes.  They also support mixins, which can hook into the component lifecycle
and take care of things easily, like canceling timers when a component is
removed from the DOM, for example.

JSX (A Javascript syntax extension)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSX lets you write components without pulling your hair out.  Instead of
writing tedious code like this:

.. code-block:: js

    React.DOM.a({href: '/about'}, 'About this site')

It allows you to just write this right alongside your javascript:

.. code-block:: html

    <a href="/about">About this site</a>

The transformer is smart enough to not need any special indicators about where
the markup blocks are, but it also allows you to drop into Javascript, like
so:

.. code-block:: html

    <a href={this.props.aboutUrl}>About this site</a>

You can choose to use this, but after getting over my initial distaste for it
("Ack! Who got markup in my code!"), I could never go back to not using it.

Next
~~~~

In a future post, I'll talk about all the other parts you'll need to pull in to
build a fuller framework for your site.

* HTTP middleware and server (Connect_)
* API client (Superagent_ and optionally `node-http-proxy`_)
* URL routing (Director_)
* Asset management
* Interfacing with legacy Javascript
* Useful mixins for components

Also, I'm not sure if this is interesting for anyone else other than myself, so
let me know if I should post that stuff, or any other feedback.  I'm always
yapping on Twitter, so `catch me over there`_!

.. _`and blogged about it previously`: http://eflorenzano.com/blog/2010/09/27/why-node-disappoints-me/
.. _`React.js`: http://facebook.github.io/react/
.. _Connect: http://www.senchalabs.org/connect/
.. _Superagent: http://visionmedia.github.io/superagent/
.. _`node-http-proxy`: https://github.com/nodejitsu/node-http-proxy
.. _Director: https://github.com/flatiron/director
.. _`catch me over there`: https://twitter.com/ericflo