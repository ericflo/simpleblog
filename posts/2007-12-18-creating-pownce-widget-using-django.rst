---
layout: post
title: "Creating a Pownce Widget Using Django"
date: 2007-12-18T12:37:52-06:00
comments: false
categories: [Django, Programming, Python, Javascript, Pownce, Widget]
published: true
alias: [/blog/post/creating-pownce-widget-using-django]
---

Widgets are everywhere!  It seems that every blog these days has at least a couple of widgets on their sidebar.  Yesterday I realized that I had never written one, and probably more importantly, I really had no concrete idea how they worked.  Using Django and a bit of Javascript, it turned out to be quite easy!  I'm going to show you the basics of how to write a widget yourself, but if enough people would like the source code to mine, I'll happily open source it.

Before starting on creating a widget, we've got to make sure that it has an API of some sort.  In the case of Pownce, there some `Community Documentation`_ about the various things that can be done with its API.  For a simple widget, all we really need is to be able to `fetch some public notes.`_

Our API call will be: ``http://api.pownce.com/1.1/public_note_lists.json``

Now that we've determined where to get our data, let's parse it and do something with it.

.. code-block:: python

    from urllib2 import urlopen
    from django.utils import simplejson
    from django.template import loader, Context
    from django.http import HttpResponse
    def pownce_widget(request):
        api_call = "http://api.pownce.com/1.1/public_note_lists.json"
        notes = simplejson.loads(urlopen(api_call).read())['notes']
        t = loader.get_template('powncewidget/widget_content.html')
        c = Context({'notes' : notes})
        return HttpResponse(t.render(c))

Now you may be noticing that I'm not using the simpler ``django.shortcuts.render_to_response``.  That's because we're going to use the content that we've rendered here as context for another template which we'll use in a moment.  Also note that if you were to do this in a production environment, using a simple urlopen is not considered good practice.  See `chapter 11`_ in `Mark Pilgrim's`_ excellent `Dive Into Python`_ for more information about what to do instead.

Now let's create a template:

.. code-block:: html+django

    <ul id="pownce_widget">
        {% for note in notes %}
            <li><a href="{{ note.permalink }}">{{ note.body|slice:":30" }}</a></li>
        {% endfor %}
    </ul>

What we've done here is iterated over the public notes, and simply created an unordered list with the first 30 or less words from the note.  Also, we've provided a link to Pownce for each note listed.

If browsers could make cross-domain requests, we'd be done now: you could embed a small Javascript file which would asynchronously request this page and update the DOM accordingly.  However, this is not possible, so I've come up with a way to do it instead.  I'm not sure if it's a best practice--it sure seems to me like it's not--but it works, which is probably more important anyway.

So let's modify our view:

.. code-block:: python

    from urllib2 import urlopen
    from django.utils import simplejson
    from django.template import loader, Context, RequestContext
    from django.http import HttpResponse
    from django.shortcuts import render_to_response
    def pownce_widget(request):
        api_call = "http://api.pownce.com/1.1/public_note_lists"
        notes = simplejson.loads(urlopen(api_call).read())['notes']
        t = loader.get_template('powncewidget/widget_content.html')
        c = Context({'notes' : notes})
        context = {"widget_content" : t.render(c))}
        return render_to_response("powncewidget/widget.html", context, context_instance=RequestContext(request))

We've taken the rendered output from ``widget_content.html`` and used it as context for another template, ``widget.html``, which we return as an ``HttpResponse`` to the browser.  This doesn't make much sense until we've seen what that ``widget.html`` template contains.  Here it is:

.. code-block:: html+django

    {% load stripwhitespace %}
    
    var _cssNode = document.createElement('link');
    _cssNode.type = 'text/css';
    _cssNode.rel = 'stylesheet';
    _cssNode.href = '{{ MEDIA_URL }}css/powncewidgetstyle.css';
    _cssNode.media = 'screen';
    document.getElementsByTagName("head")[0].appendChild(cssNode);
    document.write('{{ widget_content|stripwhitespace|safe }}');

What we're doing here is dynamically creating Javascript using Django's templating system which injects your rendered HTML into the page.  The first few lines add a new stylesheet to the page, and the last one writes your content to the page.  But what is this stripwhitespace filter that we see?  Javascript does not like multi-line string declarations such as what ``widget_content`` produces.  With Django, it's easy to write a simple filter to make it all exist on one line:

.. code-block:: python

    from django import template
    import re
    inbetween = re.compile('>[ \r\n]+<')
    newlines = re.compile('\r|\n')
    register = template.Library()
    def stripwhitespace(value):
        return newlines.sub('', inbetween.sub('><', value))
    register.filter('stripwhitespace', stripwhitespace)

With that, we've pretty much finished up on creating our widget.  There are lots of customization options from here: GET arguments, different API endpoints, etc.  Not only that, but there's lots of room for visual customization using CSS.  What we're doing is effectively generating Javascript, so anything that you'd like to do using Javascript is fair game as well.

The result after tweaking for a bit is what you see at the right under my "Widgets" links.  Here is a picture in case it stops working for some reason:

.. image:: http://media.eflorenzano.com/img/powncesample.png
    :target: http://media.eflorenzano.com/static/powncecreate.html

If you'd like to create a pownce widget of your own by simply adding a snippet to your site, I've provided a `Pownce Widget Creator`_ for your convenience.  

I think that it was fairly easy to do this using Django and Python, and if you've got any tips on best practices, please let me know so that I can code a better widget!

.. _`Community Documentation`: http://pownce.pbwiki.com/API+Documentation1-1
.. _`fetch some public notes.`: http://pownce.pbwiki.com/API+Documentation1-1#PublicNoteList
.. _`chapter 11`: http://www.diveintopython.org/http_web_services/review.html
.. _`Mark Pilgrim's`: http://diveintomark.org/
.. _`Dive Into Python`: http://www.diveintopython.org/toc/index.html
.. _`Pownce Widget Creator`: http://media.eflorenzano.com/static/powncecreate.html