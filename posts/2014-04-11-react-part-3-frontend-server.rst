---
layout: post
title: "Server/Client With React, Part 3: Frontend Server"
date: 2014-04-11T12:29:00-08:00
comments: false
categories: [React, ReactJS, Programming, Server, Client, Javascript]
published: true
---

In the past two posts, we `started writing the client code`_, and then
`made it build`_.  What's stopping us from loading it in our browser?  It's not
being served yet!  Let's fix that, starting with installing Connect_ -- the
middleware we'll use to build our http server.

.. code-block:: console

    npm install --save connect

Why not some other thing like Koa_, hapi_, or mach_?  Literally no reason.  Our
needs are simple and any one of those would work great.  I chose Connect_
because it's popular, it'd been around a while, and it seemed to work well
enough.

Now let's create a file ``server.js`` right at the root of our project,
starting with the basics, and we'll fill in more as we go:

.. code-block:: js

    var connect = require('connect');

    // Set up the application and run it
    var server = connect();
      .use(connect.static(__dirname + '/build'))
      .use(connect.logger())
      .use(connect.csrf())
      .use(connect.urlencoded())
      .use(connect.query())
      .use(connect.json())
      .listen(5000);

Running this file will start up a server listening on port 5000, serving any
static files that are found in /build, which knows how to parse querystrings,
form submissions, and json, and is protected against CSRF attacks.  So far, so
easy.  Now let's add cookie sessions, which for some reason requires a bit of a
hack:

.. code-block:: js

    var connect = require('connect');

    var IRLMOJI_COOKIE_SECRET = process.env['IRLMOJI_COOKIE_SECRET'];

    function fixConnectCookieSessionHandler(req, res, next) {
      req.session.cookie.maxAge = 365 * 24 * 60 * 60 * 1000;
      return next();
    }

    // Set up the application and run it
    var server = connect();
      .use(connect.static(__dirname + '/build'))
      .use(connect.logger())
      .use(connect.cookieParser())
      .use(connect.cookieSession({
        secret: IRLMOJI_COOKIE_SECRET,
        cookie: {maxAge: 365 * 24 * 60 * 60 * 1000, proxy: true}
      }))
      .use(fixConnectCookieSessionHandler)
      .use(connect.csrf())
      .use(connect.urlencoded())
      .use(connect.query())
      .use(connect.json())
      .listen(5000);

Now we're up and running with a cookie-based session system, which we're not
using.  In fact, we're not using any of this yet, because we're not rendering
or serving the main site yet.  We can write that now:

.. code-block:: js

    // Note that we're importing from the build directory
    var makeRouter = require('./build/javascript/router').makeRouter;
    var routes = require('./build/javascript/routes');

    function reactHandler(req, res, next) {
      // Render implemented here so it can capture req/res in its closure
      function render(reactComp, opts) {
        // We'll implement this next
      }

      var app = {
        render: render,
        isServer: function() {
          return true;
        },
        getUrl: function() {
          var proto = req.headers['x-forwarded-proto'] || 'http';
          return proto + '://' + req.headers.host + req.url;
        },
        getPath: function() {
          return req.url;
        }
      };

      var router = makeRouter(
        routes.getRoutes(app),
        routes.getNotFound(app)
      );

      router.go(app.getPath());
    }

    // ...

    // Set up the application and run it
    var server = connect();
      .use(connect.static(__dirname + '/build'))
      .use(connect.logger())
      // ...
      .use(reactHandler)
      .listen(5000);

The basic idea here is to build an ``app`` object that exactly mimics the
functionality available on the app object in ``frontend/javascript/client.js``
that we built in `part 1`_.  To do so, we create this object on-the-fly using
the information available to us from the request.  Then we import that same
simple router we used before, and tell the router to route and render its
contents by calling the ``go`` function with the current path as a parameter.

How do we actually render it though?  We left that function blank.  Before we
work on that though, we need some sort of HTML template to work from.   Let's
build our basic HTML page template in ``frontend/page.html``:

.. code-block:: html+django

    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible">
      <meta name="description" content="Take a pic that looks like an emoji!">
      <meta name="author" content="IRLMoji">
      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
      <meta content="yes" name="apple-mobile-web-app-capable">
      <title>{{ PAGE_TITLE }}</title>
      <script src="//cdnjs.cloudflare.com/ajax/libs/es5-shim/2.2.0/es5-shim.min.js"></script>
      <script src="//cdnjs.cloudflare.com/ajax/libs/es5-shim/2.2.0/es5-sham.min.js"></script>
      <link href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.0.3/css/font-awesome.min.css" rel="stylesheet">
      <link href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
      <link href="{{ STYLE_PATH }}" rel="stylesheet" media="screen">
    </head>
    <body class="{{ BODY_CLASS }}">
      <div id="react-root">{{ BODY_CONTENT }}</div>
      <input style="display: none" type="hidden" id="csrftoken" name="csrf" value="{{ CSRF_TOKEN }}" />
      <script src="{{ SCRIPT_PATH }}"></script>
    </body>
    </html>

This "template" has no fancy logic or anything, it's just a frame, so we can
use basic variable substitution -- in this case, in the style of Django
templates.  So that's what our render function will have to do: determine what
should be inserted for e.g. ``BODY_CONTENT`` and ``PAGE_TITLE``, render the
template with that content, and serve it up to the user.  Here's a first stab
at it:

.. code-block:: js

    var fs = require('fs');
    var _ = require('lodash/dist/lodash.underscore');

    var NODE_ENV = process.env['NODE_ENV'];
    var PROD = NODE_ENV === 'production';

    // Read the whole template into memory, no need to re-read it every request
    var PAGE_TEMPLATE = fs.readFileSync('frontend/page.html');

    function render(reactComp, opts) {
        opts = opts || {};

        // Render the React component to a string
        var bodyContent = React.renderComponentToString(reactComp);

        // Build up the list of variable substitutions
        var sub = {
          BODY_CLASS: opts.bodyClass || '',
          BODY_CONTENT: bodyContent,
          CSRF_TOKEN: req.csrfToken(),
          SCRIPT_PATH: '/javascript/compiled' + (PROD ? '.min' : '') + '.js',
          STYLE_PATH: '/styles/main' + (PROD ? '.min' : '') + '.css',
          PAGE_TITLE: opts.title || 'IRLMoji'
        };

        // Create a regex out of the variable substituion object
        var re = new RegExp('{{ (' + _.keys(sub).join('|') + ') }}', 'g');

        // Start the response
        res.writeHead(opts.statusCode || 200, {'Content-Type': 'text/html'});

        // Substitute all the variables and write it to the response to finish
        res.end(('' + PAGE_TEMPLATE).replace(re, function(m) {
          return sub[m.substring(3, m.length - 3)];
        }));
    }

We honestly could have used any templating language, but as you can see, most
of what's going on happens inside of ``react-root``, so this is all we'll need.

Hey, we're live!  If we start up our server by running::

    gulp watch

We'll see build directory cleaned up, then the files generated, then the server
will start up.  Cool!  Let's open the browser to `http://127.0.0.1:5000`_, and
it should say "Hello, World!", as that's what we have in our ``handleIndex()``
function in ``frontend/javascript/routes.js``.

You can check out what the fully-built demo site is doing in ``server.js`` by
`visiting the code on github`_.

What is happening here?
-----------------------

Now that we've got the basic structure of our site set up, what all is
happening?

* The server looks at the URL, routes to the right React component, and renders
  our hello world component to a string.
* Then it interpolates that string into the html page template and servers it
  up to the user.
* In that template, we've told the browser to load a script which is the
  browserified (and potentially minified) version of ``client.js``, which is an
  implementation of the app that was used to render the page. (Whoa.)
* The browser downloads and executes that script, which in turn runs its router
  on the client side and routes to the same component.
* React does a fast checksum and notices that, hey, the markup we just
  generated on the client matches what was just served from the server, so it
  doesn't change the DOM.

So now we've loaded a javascript implementation of the website frontend, and
attached it to the existing markup that was served down the wire.  Pretty cool,
but right now we're not taking advantage of that.  Soon we will :)

What's Next?
------------

* Build the communications layer between the frontend and the API
* Ensure that the client re-uses the same data the server used when it rendered
* Build a basic IRLMoji timeline
* Implement camera upload by interfacing with non-React JavaScript
  `Dropzone.js`_
* Finish building the app and deploy it

.. _`started writing the client code`: http://eflorenzano.com/blog/2014/04/09/react-part-1-getting-started/
.. _`made it build`: http://eflorenzano.com/blog/2014/04/10/react-part-2-build-system/
.. _Connect: http://www.senchalabs.org/connect/
.. _Koa: http://koajs.com/
.. _hapi: https://github.com/spumko/hapi
.. _mach: https://github.com/mjijackson/mach
.. _`part 1`: http://eflorenzano.com/blog/2014/04/09/react-part-1-getting-started/
.. _`http://127.0.0.1:5000`: http://127.0.0.1:5000
.. _`visiting the code on github`: https://github.com/ericflo/irlmoji/blob/master/server.js
.. _`Dropzone.js`: http://www.dropzonejs.com/