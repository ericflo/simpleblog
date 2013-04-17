---
layout: post
title: "Fun Way of Displaying a Blogroll"
date: 2007-12-05T21:33:14-06:00
comments: false
categories: [Eflorenzano.com, Django, Programming, Python, Design]
published: true
alias: [/blog/post/fun-way-displaying-blogroll]
---

I've just relaunched the redesign of this site.  Nothing major is different, but one fun thing that I'd like to highlight is the way the blogroll is displayed.  I got the idea from `Motel de Moka`_, which has more links to work with than I do.

First, I set up a very simple model:

.. code-block:: python

    class BlogRollLink(models.Model):
        name = models.CharField(max_length=128)
        date_added = models.DateTimeField(default=datetime.now)
        url = models.URLField()

But we've got a problem at this point: we can't order this by the number of characters in the name.  So we must modify our model to have an integer called ``name_size``, and then override ``BlogRollLink``'s save function to fill in that field any time the model is saved.  Our final model is below:

.. code-block:: python

    class BlogRollLink(models.Model):
        name = models.CharField(max_length=128)
        name_size = models.IntegerField(editable=False)
        date_added = models.DateTimeField(default=datetime.now)
        url = models.URLField()
        
        def save(self):
            self.name_size = len(self.name)
            super(BlogRollLink, self).save()
        
        def __unicode__(self):
            return self.name
        
        def get_absolute_url(self):
            return self.url
        
        class Admin:
            pass

Now to display this on every page, I've created a context processor named ``blogroll_processor``.  It looks like this:

.. code-block:: python

    def blogroll_processor(request):
        blogrolls = cache.get('blogrolls', None)
        if blogrolls == None:
            blogrolls = list(BlogRollLink.objects.all().order_by('name_size'))
            cache.set('blogrolls', blogrolls)
        return {'blogrolls' : blogrolls}

And we're done!  A nifty "waterfall" of blogs.  Let me know what you think about this technique.  Is it stupid?

.. _`Motel de Moka`: http://www.moteldemoka.com/