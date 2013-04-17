---
layout: post
title: "Flojax: A unobtrusive and easy strategy for creating AJAX-style web applications"
date: 2009-04-02T21:05:18-05:00
comments: false
categories: [Javascript, Python, Django, AJAX, Programming]
published: true
alias: [/blog/post/flojax-unobtrusive-and-easy-strategy-creating-ajax]
---

Writing AJAX-style web applications can be very tedious.  If you're using XML
as your transport layer, you have to parse the XML before you can work with it.
It's a bit easier if you're using JSON, but once you have parsed the data, the
data still needs to be turned into HTML markup that matches the current markup
on the page.  Finally, the newly created markup needs to be inserted into the
correct place in the DOM, and any event handlers need to be attached to the
appropriate newly-inserted markup.

So there's the parsing, the markup assembly, the DOM insertion, and finally the
event handler attachment.  Most of the time, people tend to write custom code
for each element that needs asynchronous updating.  There are several drawbacks
with this scenario, but the most frustrating part is probably that the
presentation logic is implemented twice--once in a templating language on the
server which is designed specifically for outputting markup, and again on the
client with inline Javascript.  This leads to problems both in the agility and
in the maintainability of this type of application.

With flojax, this can all be  accomplished with one generalized implementation.
The same server-side logic that generates the data for the first synchronous
request can be used to respond to subsequent asynchronous requests, and
unobtrusive attributes specify what to do for the rest.


The Basics
----------

The first component for creating an application using the flojax strategy is to
break up the content that you would like to reload asynchronously into smaller
fragments.  As a basic example of this, let's examine the case where there is a
panel of buttons that you would like to turn into asynchronous requests instead
of full page reloads.

The rendered markup for a fragment of buttons could look something like this:

.. code-block:: html

    <div class="buttons">
        <a href="/vote/up/item1/">Vote up</a>
        <a href="/vote/down/item1/">Vote down</a>
        <a href="/favorite/item1/">Add to your favorites</a>
    </div>


In a templating language, the logic might look something like this:

.. code-block:: html

    <div class="buttons">
        {% if voted %}
            <a href="/vote/clear/{{ item.id }}/">Clear your vote</a>
        {% else %}
            <a href="/vote/up/{{ item.id }}/">Vote up</a>
            <a href="/vote/down/{{ item.id }}/">Vote down</a>
        {% endif %}
        {% if favorited %}
            <a href="/favorite/{{ item.id }}/">Add to your favorites</a>
        {% else %}
            <a href="/unfavorite/{{ item.id }}/">Remove from your favorites</a>
        {% endif %}
    </div>

(Typically you wouldn't use anchors to do operations that can change state on
the server, so you can imagine this would be accomplished using forms.  However,
for demonstration and clarity purposes I'm going to leave these as links.)

Now that we have written a fragment, we can start using it in our larger
templates by way of an include, which might look something like this:

.. code-block:: html

    ...
    <p>If you like this item, consider favoriting or voting on it:</p>
    {% include "fragments/buttons.html" %}
    ...


To change this from being standard links to being asynchronously updated, we
just need to annotate a small amount of data onto the relevant links in the
fragment.

.. code-block:: html

    <div class="buttons">
        {% if voted %}
            <a href="/vote/clear/{{ item.id }}/" class="flojax" rel="buttons">Clear your vote</a>
        {% else %}
            <a href="/vote/up/{{ item.id }}/" class="flojax" rel="buttons">Vote up</a>
            <a href="/vote/down/{{ item.id }}/" class="flojax" rel="buttons">Vote down</a>
        {% endif %}
        {% if favorited %}
            <a href="/favorite/{{ item.id }}/" class="flojax" rel="buttons">Add to your favorites</a>
        {% else %}
            <a href="/unfavorite/{{ item.id }}/" class="flojax" rel="buttons">Remove from your favorites</a>
        {% endif %}
    </div>


That's it!  At this point, all of the click events that happen on these links
will be changed into POST requests, and the response from the server will be
inserted into the DOM in place of this div with the class of "buttons".  If you
didn't catch it, all that was done was to add the "flojax" class onto each of
the links, and add a rel attribute that refers to the class of the parent node
in the DOM to be replaced--in this case, "buttons".

Of course, there needs to be a server side component to this strategy, so that
instead of rendering the whole page, the server just renders the fragment.  Most
modern Javascript frameworks add a header to the request to let the server know
that the request was made asynchronously from Javascript.  Here's how the code
on the server to handle the flojax-style request might look (in a kind of
non-web-framework-specific Python code):

.. code-block:: python

    def vote(request, direction, item_id):
        item = get_item(item_id)
        
        if direction == 'clear':
            clear_vote(request.user, item)
        elif direction == 'up':
            vote_up(request.user, item)
        elif direction == 'down':
            vote_down(request.user, item)
        
        context = {'voted': direction != 'clear', 'item': item}
        
        if request.is_ajax():
            return render_to_response('fragments/buttons.html', context)
        
        # ... the non-ajax implementation details go here
        
        return render_to_response('items/item_detail.html', context)


There are several advantages to writing your request handlers in this way.
First, note that we were able to totally reuse the same templating logic from
before--we just render out the fragment instead of including it in a larger
template.  Second, we have provided a graceful degradation path where users
without javascript are able to interact with the site as well, albeit with a
worse user experience.

That's really all there is to writing web applications using the flojax
strategy.


Implementation Details
----------------------

I don't believe that the Javascript code for this method can be easily reused,
because each web application tends to have a different way of showing errors and
other such things to the user.  In this post, I'm going to provide a reference
implementation (using jQuery) that can be used as a starting point for writing
your own versions.  The bulk of the work is done in a function that is called on
every page load, called ``flojax_init``.

.. code-block:: javascript

    function flojax_clicked() {
        var link = $(this);
        var parent = link.parents('.' + link.attr('rel'));
        
        function successCallback(data, textStatus) {
            parent.replaceWith(data);
            flojax_init();
        }
        function errorCallback(request, textStatus, errorThrown) {
            alert('There was an error in performing the requested operation');
        }
        
        $.ajax({
            'url': link.attr('href'),
            'type': 'POST',
            'data': '',
            'success': successCallback,
            'error': errorCallback
        });
        
        return false;
    }

    function flojax_init() {
        $('a.flojax').live('click', flojax_clicked);
    }


There's really not a lot of code there.  It POSTS to the given URL and replaces
the specified parent class with the content of the response, and then
re-initializes the flojax handler.  The re-initialization could even be done in
a smarter way, as well, by targeting only the newly inserted content.  Also, you
might imagine that an alert message probably wouldn't be such a great user
experience, so you could integrate error messages into some sort of Javascript
messaging or growl-style system.


Extending Flojax
----------------

Often times you'll want to do other things on the page when the asynchronous
request happens.  For our example, maybe there is some kind of vote counter that
needs to be updated or some other messages that need to be displayed.

In these cases, I have found that using hidden input elements in the fragments
can be useful for transferring that information from the server to the client.
As long as the value in the hidden elements adheres to some predefined structure
that your client knows about (it could even be something like JSON if you need
to go that route).

If what you want can't be done by extending the fragments in this way, then
flojax isn't the right strategy for that particular feature.


Limitations
-----------

This technique cannot solve all of the world's problems.  It can't even solve
all of the problems involved in writing an AJAX-style web application.  It can,
however, handle a fair amount of simple cases where all you want to do is
quickly set up a way for a user's action to replace content on a page.

Some specific examples of things that flojax can't help with are if a user
action can possibly update many items on a page, or if something needs to happen
without a user clicking on a link.  In these situations, you are better off
coding a custom solution instead of trying to shoehorn it into the flojax
workflow.


Conclusion
----------

Writing AJAX-style web applications is usually tedious, but using the techniques
that I've described, a large majority of the tedious work can be reduced.  By
using the same template code for rendering the page initially as with subsequent
asynchronous requests, you ensure that code is not duplicated.  By rendering HTML
fragments, the client doesn't have to go through the effort of parsing the
output and converting the result into correct DOM objects.  Finally, by using a
few unobtrusive conventions (like the ``rel`` attribute and the ``flojax``
class), the Javascript code that a web application developer writes is able to
be reused again and again.

I don't believe that any of the details that I'm describing are new.  In fact,
people have been doing most of these things for years.  What I think may in fact
be new is the generalization of the sum of these techniques in this way.  It's
still very much a work in progress, though.  As I use flojax more and more, I
hope to find not only places where it can be extended to cover more use cases,
but also its limitations and places where it makes more sense to use another
approach.

What do you think about this technique?  Are you using any techniques like this
for your web applications?  If so, how do they differ from what I've described?