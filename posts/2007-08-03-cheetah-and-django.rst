---
layout: post
title: "Cheetah and Django"
date: 2007-08-03T22:18:41-05:00
comments: false
categories: [Django, Python, Cheetah, Templating]
published: true
alias: [/blog/post/cheetah-and-django]
---

Django is my preferred web development framework.  As such, I like it as a total solution: ORM, Template System, and Request/Response Mechanisms.  One of the criticisms that gets tossed around regarding Django is that it's a monolithic web framework, and as such it is not loosely coupled.  I would argue that while it is a monolithic framework, it is still loosely coupled, and I'll prove it by showing just how easy it is to replace the templating system.

After a quick google search for django and cheetah, I was surprised to find that there seem to be no really great examples online of the replacement of the template part of the Django stack.  That being the case, I have decided to provide some examples of how that can be accomplished.  In short, I'm going to demonstrate how to use the `Cheetah template language`_ with the `Django web framework`_.

Before we delve into how to integrate Cheetah with Django, first let's look at some basic Cheetah syntax.  Basically all placeholders in cheetah templates are prefixed by $, and all control flow logic is prefaced by #.  Beyond that, mostly the syntax follows normal Python syntax. 

If there's a python object ``test = [1, 2, "3.1415", 4, range]``, the Cheetah placeholder ``$test[0]`` would return 1, ``$test[2]`` would return 3.1415, and ``$test[4](0,$test[1])`` would return ``[0, 1]``.  To learn about control flow or any of the more advanced topics, you'll have to visit `the excellent Cheetah Users Guide`_.

To demonstrate using Cheetah with Django, we're going to use the canonical example: the blog.  First, the model (about the most simplistic one I could think of for a blog):

.. code-block:: python

    from django.db import models
    
    class BlogPost(models.Model):
        title = models.CharField(maxlength = 128)
        body = models.TextField()
        
        def __unicode__(self):
            return self.title

Now, let's make sure to add a template folder to TEMPLATE_DIRS in settings.py:

.. code-block:: python

    TEMPLATE_DIRS = (
        '/path/to/myproject/templates',
    )

Now, one aspect of Django that I've gotten really accustomed to is the render_to_response method.  It's nice to be able to specify a template name and pass in some context, and get an ``HttpResponse`` object back.  So we'll start by replacing that method, but for cheetah:

.. code-block:: python

    import os.path
    from Cheetah.Template import Template
    from django.conf import settings
    from django.http import HttpResponse
    def render_to_response(template_name, context, **kwargs):
        for template_dir in settings.TEMPLATE_DIRS:
            path = os.path.join(template_dir, template_name)
            if os.path.exists(path):
                template = Template(file = path, searchList = (context,))
                return HttpResponse(unicode(template), **kwargs)
        raise ValueError, 'Could not find template for %s' % template_name

This code snippet can go anywhere, but to make it easy you can just put it in your ``views.py``.  As for how it works: basically we're just iterating over each template directory in ``TEMPLATE_DIRS``.  If we find that a file exists, we create a cheetah Template object with that file as its base and with the specified context as its search list.  Then, we simply render the result into an ``HttpResponse`` object.  I feel that this solution is both simple and robust--two concepts that usually exclude each other.

So, how would a simple view look using our new helper render_to_response?

.. code-block:: python

    from myproject.blog.models import BlogPost
    def index(request):
        blogs = BlogPost.objects.all()
        context = { 'blogs' : blogs }
        return render_to_response('index.tmpl', context)

Ok, it's going to take a bit of explaining for that last snippet.  There's a lot of advanced things going on that make it look totally unfamiliar.  But actually that's just one big lie: this looks EXACTLY like any other Django view!  We've just completely and transparently replaced the templating system of Django, and all it took was a 7-line helper function.  But we're not done yet.  We still have to write the template:

.. code-block:: html

    <html>
        <head><title>I can has cheetah templates!</title></head>
        <body>
        #for $post in $blogs
        <div class="blogpost">
            <h1>$post.title</h1>
            <p>$post.body</p>
        </div>
        #end for
        </body>
    </html>

Now point a url to the example view, and watch the magic unfold.  I'm not a Cheetah user normally, so I can't really comment about some of the more complex features of that language, but I can't imagine that enabling them would be much more difficult than what we've already done here.  So, that means I'm totally aware that there may be some naivity in my implementation.  If so, please comment and I'll change it accordingly.

.. _`Cheetah template language`: http://www.cheetahtemplate.org/
.. _`Django web framework`: http://www.djangoproject.com/
.. _`the excellent Cheetah Users Guide`: http://www.cheetahtemplate.org/docs/users_guide_html/users_guide.html