---
layout: post
title: "Server/Client With React, Part 2: The Build System"
date: 2014-04-10T12:12:00-08:00
comments: false
categories: [React, ReactJS, Programming, Server, Client, Javascript]
published: true
---

In the `last post`_, we started writing the client glue code and our first React
component.  But we're using things like ``require()`` for something that should
be run on the client, how will that work?  Browserify_ can take a look at our
``client.js``, walk the dependencies, and spit out something that browsers can
actually execute.  Let's set that up!

But first a bit about we'll structure the app.  This is how things look
currently::

    frontend/
        javascript/
            client.js
            routes.js
            components/
                common.js

But these JavaScript files need processing.  Some of them have JSX in them,
which needs to be converted to pure JavaScript.  It all needs to be transformed
to work in the browser.  Additionally, we may have other non-JS files that we
want to preprocess.  To address this, we'll do all this processing and save it
in a directory adjacent to ``frontend`` named ``build``.

Here's the basic idea of how things will look after this blog post::

    build/
        images/
        javascript/
            compiled.js
            compiled.min.js
            client.js
            client.min.js
            routes.js
            routes.min.js
            components/
                common.js
                common.min.js
        styles/
            main.js
            main.min.js
    frontend/
        images/
        javascript/
            client.js
            routes.js
            components/
                common.js
        styles/
            main.less
        tests/
    gulpfile.js
    package.json

First make sure you have a ``package.json`` file.  If you're not familiar with
this file, here's `some light reading`_ about it.  We're going to use Gulp_ to
do our processing, and we need a number of plugins to make that work.  These
commands should get you started:

.. code-block:: console

    npm install --save react react-tools lodash
    npm install --save-dev browserify envify gulp gulp-util gulp-uglify \
        gulp-clean gulp-rename gulp-browserify gulp-less gulp-react \
        gulp-minify-css gulp-nodemon

Now that we have the dependencies installed, let's create a file named
``gulpfile.js`` which will describe to Gulp_ how to build the app:

.. code-block:: js

    var gulp = require('gulp');
    var clean = require('gulp-clean');

    gulp.task('clean', function() {
      return gulp.src(['build/*'], {read: false}).pipe(clean());
    });

So far it's not that impressive, all we're doing is deleting anything inside
the ``build/``, directory, which doesn't even exist.  We noted earlier that
some of the JavaScript had JSX in it, and would need to be processed, so let's
set that up by adding this to ``gulpfile.js``:

.. code-block:: js

    var react = require('gulp-react');
    var uglify = require('gulp-uglify');
    var rename = require('gulp-rename');

    // Parse and compress JS and JSX files

    gulp.task('javascript', function() {
      // Listen to every JS file in ./frontend/javascript
      return gulp.src('frontend/javascript/**/*.js')
        // Turn React JSX syntax into regular javascript
        .pipe(react())
        // Output each file into the ./build/javascript/ directory
        .pipe(gulp.dest('build/javascript/'))
        // Optimize each JavaScript file
        .pipe(uglify())
        // Add .min.js to the end of each optimized file
        .pipe(rename({suffix: '.min'}))
        // Output each optimized .min.js file into the ./build/javascript/ dir
        .pipe(gulp.dest('build/javascript/'));
    });

Now let's set up browserify to transform the ``require()`` calls into
JavaScript the browser understands.  You'll notice this matches the structure
of the previous code block almost exactly, except we're swapping out a
call to ``browserify()`` instead of a call to ``react()``:

.. code-block:: js

    var browserify = require('gulp-browserify');

    gulp.task('browserify', ['javascript'], function() {
      return gulp.src('build/javascript/client.js')
        .pipe(browserify({transform: ['envify']}))
        .pipe(rename('compiled.js'))
        .pipe(gulp.dest('build/javascript/'))
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('build/javascript/'));
    });

And like I mentioned, there are things other than JavaScript which need to be
processed too!

.. code-block:: js

    var less = require('gulp-less');
    var minifycss = require('gulp-minify-css');

    gulp.task('styles', function() {
      return gulp.src('frontend/**/*.less')
        .pipe(less())
        .pipe(gulp.dest('build/'))
        .pipe(minifycss())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('build/'));
    });

But no ``gulpfile.js`` is complete without a ``default`` task that will run
when the user types just ``gulp`` in their console:

.. code-block:: js

    gulp.task('default', ['clean'], function() {
      return gulp.start('browserify', 'styles');
    });

This says to run ``clean`` as a dependency, then to run the ``browserify`` and
``styles`` tasks in parallel, and finish when everything returns.  So just to
hammer this point home, all you need to do to build everything is to open
a terminal, navigate to your project directory and type:

.. code-block:: console

    gulp


Local Development
-----------------

Doing local development is slightly more tricky, but not so bad to set up.
What we'd like is to be able to run a command, and then have it watch for
changes and automatically rebuild the parts that have changed.  Let's add a
``watch`` task which does this:

.. code-block:: js

    var nodemon = require('gulp-nodemon');

    gulp.task('watch', ['clean'], function() {
      var watching = false;
      gulp.start('browserify', 'styles', function() {
        // Protect against this function being called twice. (Bug?)
        if (!watching) {
          watching = true;
          
          // Watch for changes in frontend js and run the 'javascript' task
          gulp.watch('frontend/**/*.js', ['javascript']);

          // Run the 'browserify_nodep' task when client.js changes
          gulp.watch('build/javascript/client.js', ['browserify_nodep']);
          
          // Watch for .less file changes and re-run the 'styles' task
          gulp.watch('frontend/**/*.less', ['styles']);

          // Start up the server and have it reload when anything in the
          // ./build/ directory changes
          nodemon({script: 'server.js', watch: 'build'});
        }
      });
    });

Most of this is fairly self-explanatory except two things:

* What is 'browserify_nodep'?
* We haven't built ``server.js`` yet.

The latter we'll tackle in the next post, but the reason for 'browserify_nodep'
is that we don't need/want all the javascript to be rebuilt every time just
client.js changes.  We have something already watching for that.  So let's
modify our ``browserify`` task and split it into ``browserify`` and
``browserify_nodep``:

.. code-block:: js

    function browserifyTask() {
      return gulp.src('build/javascript/client.js')
        .pipe(browserify({
          transform: ['envify']
        }))
        .pipe(rename('compiled.js'))
        .pipe(gulp.dest('build/javascript/'))
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('build/javascript/'));
    }

    gulp.task('browserify', ['javascript'], browserifyTask);
    gulp.task('browserify_nodep', browserifyTask);

This is why it's awesome that Gulpfiles are just javascript files: we can break
out common functionality into a function, and apply it to different tasks.  If
you ever want to see the fully finished gulpfile.js for the final project, you
can `check it out here`_.

What's Next?
------------

* Write the ``server.js`` that mimics the ``client.js`` we've been building and
  acts as http server.
* Build the communications layer between the frontend and the API
* Ensure that the client re-uses the same data the server used when it rendered
* Oh yeah, write our app :)

.. _`last post`: http://eflorenzano.com/blog/2014/04/09/react-part-1-getting-started/
.. _Browserify: http://browserify.org/
.. _`some light reading`: http://docs.nodejitsu.com/articles/getting-started/npm/what-is-the-file-package-json
.. _Gulp: http://gulpjs.com/
.. _`check it out here`: https://github.com/ericflo/irlmoji/blob/master/gulpfile.js