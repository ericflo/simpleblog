---
layout: post
title: "Server/Client With React, Part 1: Getting Started"
date: 2014-04-09T13:00:00-08:00
comments: false
categories: [React, ReactJS, Programming, Server, Client, Javascript]
alias: [/blog/2014/04/09/react-part-1-getting-started]
published: true
---

A few months ago `I wrote about`_ how React.js has made it possible (and
relatively easy) to write code that renders markup quickly on the server, and
also can be executed on the client to perform all page updates.  Now that we
know what the goal is, we can explore how to put all these pieces together, or
how I've managed to do it anyway.

Let's Build Something!
----------------------

It's easiest to talk about concepts if we can also work on something concrete,
so in the next few posts we'll build a little example site called IRLMoji,
which asks users to post pictures that look like emoji.  All credit goes to
`@dwiskus`_ for originally starting this `meme on Twitter`_.  But we're going
to turn it into its own app for demo purposes, which will look something like
this:

.. image:: http://eflorenzano.com.s3-us-west-2.amazonaws.com/irlmoji-screenshot.jpg
    :alt: A screenshot of what we are building
    :target: https://www.irlmoji.com/
    :width: 200px

It's definitely not pretty (sorry), but it's got all the stuff we need to learn
about React including auth, content creation, server communication, integration
with third-party JS libraries, etc.  If you'd like to follow along and see the
code for the finished site, it's all up on GitHub:
`https://github.com/ericflo/irlmoji`_.


Let's Begin
-----------

There will be two entry points to our app: ``server.js``, which will sit at the
project's top level, and ``frontend/javascript/client.js``.  Let's start with
the client, because it's a bit simpler.  First let's start small and build a
``render()`` function, which will take a React component and some options, and
render it to the page:

.. code-block:: js

    function render(reactComp, opts) {
      opts = opts || {};
      var elt = document.getElementById('react-root');
      React.renderComponent(reactComp, elt);
    }

All we're doing here is calling ``React.renderComponent`` on the component that
was passed in, rendering the component into that `#react-root` DOM element.
We'll end up making this function do a bit more work in a future post, but for
now let's move on to writing some handlers, and hooking them up to URL routes.

In the past I've used `director`_ to handle URL routing, but eventually I wrote
`a small router`_ which escews `hashbang-style`_ URLs in favor of HTML5
pushState.  If needed, we can always fall back to full page reloads, rather
than resort to hashbangs.  Now we've got this router to work with, let's put it
to use, starting with a new file at ``frontend/javascript/routes.js``:

.. code-block:: as

    /** @jsx React.DOM */

    // Lodash is a fast/light underscore replacement that works better for me
    var _ = require('lodash/dist/lodash.underscore');
    var common = require('./components/common');

    // Renders the index page, for now just "Hello, World!"
    function handleIndex(app) {
      app.render(<p>Hello, World!</p>, {
        title: 'Welcome',
      });
    }

    // Prepares a handler for use. For now all we're doing is making sure
    // that 'app' is passed as the first argument to the handler function.
    function prepareHandler(app, handler) {
      return _.partial(handler, app);
    }

    // Gets a list of routes to be passed to the router 
    function getRoutes(app) {
      return [
        ['/', prepareHandler(app, handleIndex)]
      ];
    }

    // Gets a function that should be called when no routes match
    function getNotFound(app) {
      return function() {
        // At the time this post was written, JSX does not allow namespacing,
        // so we need to grab a reference to the NotFound component class.
        var NotFound = common.NotFound;
        app.render(<NotFound />, {statusCode: 404});
      };
    }

    module.exports = {
      getRoutes: getRoutes,
      getNotFound: getNotFound
    };

"Wait a minute," you may be thinking.  What is this ``app`` thing that every
function seems to refer to?  The ``app`` is what I've chosen to call the object
that is used to tie everything together.  It's because of this object that
we're able to use one codebase for both server and client.  Right now all we're
using is the ``render`` function that we created earlier, but through the
interface of this ``app`` object.  Let's go back to ``client.js`` and create
a basic app object.

.. code-block:: js

    var app = {
      render: render,
      isServer: function() {
        return false;
      },
      getUrl: function() {
        return '' + window.location;
      },
      getPath: function() {
        return window.location.pathname + window.location.search;
      }
    };

Here we've got a basic ``app`` object, with access to a render function and a
few helpers like the ability to get the current path or get the full URL or to
detect whether we're on the server or the client.  We're building this in
``client.js``, so we know we're not on the server, and can just return false.

Now that we have our app, and our routes, let's tie them together:

.. code-block:: js

    // Import the routes we created earlier
    var routes = require('./routes');
    // ...and the simple router we're using
    var makeRouter = require('./router').makeRouter;

    app.router = makeRouter(routes.getRoutes(app), routes.getNotFound(app));
    app.router.start();

To finish up this part, we still have to create that NotFound React component,
so let's create a new file in ``frontend/javascript/components/common.js`` with
this as its content:

.. code-block:: as

    /** @jsx React.DOM */

    var React = require('react/addons');

    var NotFound = React.createClass({
      render: function() {
        return <p>That page could not be found.</p>;
      }
    });

    module.exports = {NotFound: NotFound};

What's Next?
------------

It would be great if we could fire up our browsers now and see in action what
we've built so far.  Unfortunately, however, we haven't built the server yet.
Here are some of the high level things that we're going to cover next:

* Set up Gulp_ and Browserify_ to compile our node JavaScript into Browser JS
* Write the ``server.js`` that mimics the ``client.js`` we've been building and
  acts as http server.
* Build the communications layer between the frontend and the API
* Ensure that the client re-uses the same data the server used when it rendered
* Oh yeah, write our app :)

.. _`I wrote about`: http://eflorenzano.com/blog/2014/01/23/react-finally-server-client
.. _`@dwiskus`: https://twitter.com/dwiskus
.. _`meme on Twitter`: http://betterelevation.com/irlmoji/
.. _`https://github.com/ericflo/irlmoji`: https://github.com/ericflo/irlmoji
.. _`a small router`: https://github.com/ericflo/irlmoji/blob/master/frontend/javascript/router.js
.. _`hashbang-style`: http://www.webmonkey.com/2011/02/gawker-learns-the-hard-way-why-hash-bang-urls-are-evil/
.. _`director`: https://github.com/flatiron/director
.. _Gulp: http://gulpjs.com/
.. _Browserify: http://browserify.org/