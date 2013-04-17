---
layout: post
title: "How do we kick our synchronous addiction?"
date: 2010-02-09T00:15:31-06:00
comments: false
categories: [Django, Asynchronous, Threads, Processes, Coroutines, Erlang, Python]
published: true
alias: [/blog/post/how-do-we-kick-our-synchronous-addiction]
---

Asynchronous programming is superior `both in memory usage and in overall throughput`_ when compared to synchronous programming .  We've `known this fact for years`_.  If we look at Django or Ruby on Rails, arguably the two most promising new web application frameworks to emerge in the past few years, both of them are written in such a way that synchronous programming  is assumed. Why is it that even in 2010 we're still writing programs that rely on synchronous programming ?

The reason that we're stuck on synchronous programming  is twofold.  Firstly, the programming model required for straightforward asynchronous implementations is inconvenient.  Secondly, popular and/or mainstream languages lack the built-in language constructs that are needed to implement a less-straightforward approach to asynchronous programming.

Asynchronous programming is too hard
--------------------------------------

Let's first examine the straightforward implementation: an event loop.  In this programming model, we have a single process with a single loop that runs continuously.  Functionality is achieved by writing functions to execute small tasks quickly, and inserting those functions into that event loop.  One of those functions might read some bytes from a socket, while another function might write a few bytes to a file, and yet another function might do something computational like calculating an XOR on the data that's been buffered from that first socket.

The most important part about this event loop is that only one thing is ever happening at a time.  That means that you really have to break your logic up into small chunks that can be performed incrementally.  If any one of our functions blocks, it hogs the event loop and nothing else can execute during that time.

We have some really great frameworks geared towards making this event loop model easier to work with.  In Python, there's Twisted_ and, more recently, Tornado_.  In Ruby there's EventMachine_.  In PERL there's POE_.  What these frameworks do is twofold: provide constructs for more easily working with an event loop (e.g. Deferreds_ or Promises_), and provide asynchronous implementations of common tasks (e.g. HTTP clients and DNS resolution).

But these frameworks stop very short of making asynchronous programming easy for two reasons.  The first reason is that we really do have to completely change our coding style.  Consider what it would take to render a simple blog web page with comments.  Here's some JavaScript code to demonstrate how this might work in a synchronous framework:

.. code-block:: javascript

    function handleBlogPostRequest(request, response, postSlug) {
        var db = new DBClient();
        var post = db.getBlogPost(postSlug);
        var comments = db.getComments(post.id);
        var html = template.render('blog/post.html',
            {'post': post, 'comments': comments});
        response.write(html);
        response.close();
    }

Now here's some JavaScript code to demonstrate how this might look in an asynchronous framework.  Note several things here: We've specifically written this in such a way that it doesn't become nested four levels deep.  We've also written these callback functions inside of the ``handleBlogPostRequest`` function to take advantage of closure so as to retain access to the request and response objects, the template context, and the database client. Both the desire to avoid nesting and the closure are things that we need to think about as we write this code, that were not even considerations in the synchronous version:

.. code-block:: javascript

    function handleBlogPostRequest(request, response, postSlug) {
        var context = {};
        var db = new DBClient();
        function pageRendered(html) {
            response.write(html);
            response.close();
        }
        function gotComments(comments) {
            context['comments'] = comments;
            template.render('blog/post.html', context).addCallback(pageRendered);
        }
        function gotBlogPost(post) {
            context['post'] = post;
            db.getComments(post.id).addCallback(gotComments);
        }
        db.getBlogPost(postSlug).addCallback(gotBlogPost);
    }

I've chosen JavaScript here to prove a point, by the way.  People are very excited about `node.js`_ right now, and it's a very cool framework, but it doesn't hide all of the complexities involved in doing things asynchronously.  It only hides some of the implementation details of the event loop.

The second reason why these frameworks fall short is because not all IO can be handled properly by a framework, and in these cases we have to resort to bad hacks.  For example, MySQL does not offer an asynchronous database driver, so most of the major frameworks end up using threads to ensure that this communication happens out of band.

Given the inconvenient API, the added complexity, and the simple fact that most developers haven't switched to using this style of programming, leads us to the conclusion that this type of framework is not a desirable final solution to the problem (even though I do concede that you can get Real Work done today using these techniques, and many people do).  That being the case, what other options do we have for asynchronous programming? Coroutines and lightweight processes, which brings us to our next major problem.

Languages don't support easier asynchronous paradigms
------------------------------------------------------

There are a few language constructs that, if implemented properly in modern programming languages, could pave the way for alternative methods of doing asynchronous programming that don't have the drawbacks of the event loop.  These constructs are coroutines and lightweight processes.

A coroutine is a function that can suspend and resume its execution at certain, programmatically specified, locations.  This simple concept can serve to transform blocking-looking code to be non-blocking.  At certain critical points in your IO library code, the low-level functions that are doing IO can choose to "cooperate".  That is, it can choose to suspend execution in order for another function to resume execution and continue on.

Here's an example (it's Python, but fairly understandable for all I hope):

.. code-block:: python

    def download_pages():
        google = urlopen('http://www.google.com/').read()
        yahoo = urlopen('http://www.yahoo.com/').read()

Normally the way this would work is that a socket would be opened, connected to Google, an HTTP request sent, and the full response would be read, buffered, and assigned to the ``google`` variable, and then in turn the same series of steps would be taken for the ``yahoo`` variable.

Ok, now imagine that the underlying socket implementation were built using coroutines that cooperated with each other.  This time, just like before, the socket would be opened and a connection would be made to Google, and then a request would be fired off.  This time, however, after sending the request, the socket implementation suspends its own execution.

Having suspended its execution (but not yet having returned a value), execution continues on to the next line.  The same thing happens on the Yahoo line: once its request has been fired off, the Yahoo line suspends its execution.  But now there's something else to cooperate with--there's actually some data ready to be read on the Google socket--so it resumes execution at that point.  It reads some data from the Gooogle socket, and then suspends its execution again.

It jumps back and forth between the two coroutines until one has finished.  Let's say that the Yahoo socket has finished, but the Google one has not.  In this case, the Google socket just continues to read from its socket until it has completed, because there are no other coroutines to cooperate with.  Once the Google socket is finally finished, the function returns with all of the buffered data.

Then the Yahoo line returns with all of its buffered data.

We've preserved the style of our blocking code, but we've used asynchronous programming to do it.  Best of all, we've preserved our original program flow--the ``google`` variable is assigned first, and then the ``yahoo`` variable is assigned.  In truth, we've got a smart event loop going on underneath the covers to control who gets to execute, but it's hidden from us due to the fact that coroutines are in play.

Languages like PHP, Python, Ruby, and Perl simply don't have built-in coroutines that are robust enough to implement this kind of behind-the-scenes transformation.  So what about these lightweight processes?

Lightweight processes are what Erlang uses as its main concurrency primitive.  Essentially these are processes that are mostly implemented in the Erlang VM itself.  Each process has approximately 300 words of overhead and its execution is scheduled primarily by the Erlang VM, sharing no state at all amongst processes.  Essentially, we don't have to think twice about spawning a process, as it's essentially free.  The catch is that these processes can only communicate via message passing.

Implementing these lightweight processes at the VM level gets rid of the memory overhead, the context switching, and the relative sluggishness of interprocess communication provided by the operating system.  Since the VM also has insight into the memory stack of each process, it can freely move or resize those processes and their stacks.  That's something that the OS simply cannot do.

With this model of lightweight processes, it's possible to again revert back to the convenient model of using a separate process for all of our asynchronous programming needs.  The question becomes this: can this notion of lightweight processes be implemented in languages other than Erlang?  The answer to that is "I don't know."  To my knowledge, Erlang takes advantage of some features of the language itself (such as having no mutable data structures) in its lightweight process implementation.

Where do we go from here?
--------------------------

The key to moving forward is to drop the notion that developers need to learn to think about all of their code in terms of callbacks and asynchrony, as the asynchronous event loop frameworks require them to do.  Over the past ten years, we can see that most developers, when faced with that decision, simply choose to ignore it.  They continue to use the inferior blocking methodologies of yesteryear.

We need to look at these alternative implementations like coroutines and lightweight processes, so that we can make asynchronous programming as easy as synchronous programming.  Only then will we be able to kick this synchronous addiction.

.. _`both in memory usage and in overall throughput`: http://blog.webfaction.com/a-little-holiday-present
.. _`known this fact for years`: http://www.kegel.com/c10k.html
.. _Twisted: http://twistedmatrix.com/trac/
.. _Tornado: http://www.tornadoweb.org/
.. _EventMachine: http://rubyeventmachine.com/
.. _Deferreds: http://twistedmatrix.com/documents/current/core/howto/defer.html
.. _Promises: http://en.wikipedia.org/wiki/Futures_and_promises
.. _POE: http://poe.perl.org/
.. _`node.js`: http://nodejs.org/