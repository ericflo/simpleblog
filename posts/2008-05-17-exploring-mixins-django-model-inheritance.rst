---
layout: post
title: "Exploring Mixins with Django Model Inheritance"
date: 2008-05-17T02:24:03-05:00
comments: false
categories: [Django, Object Oriented Programming, Programming, Python]
published: true
alias: [/blog/post/exploring-mixins-django-model-inheritance]
---

Django_ now supports `Model Inheritance`_, and one of the coolest new opportunities that model inheritance brings is the possibility of the creation of mixins_, so in this post I'll walk through the steps I went through to create some simple examples. This is just an excercise (although it could be modified to be more robust)--and right now there are better ways to achieve all of the effects of the following mixins.  (See django-mptt_, for example).

Model and Field Setup
---------------------

First let's just set up two basic models.  The first will be our mixin, ``NaiveHierarchy``, which has a single field, ``parent``, which is a reference to itself.  Using this, we can traverse the tree and find all sorts of fun hierarchical information.  Also, we'll create the canonical example model: the blog post.  Our models start out looking something like this:

.. code-block:: python

    from django.db import models

    class NaiveHierarchy(models.Model):
        parent = models.ForeignKey('self', null=True)

        class Meta:
            abstract = True

    class BlogPost(NaiveHierarchy):
        title = models.CharField(max_length = 128)
        body = models.TextField()

        def __unicode__(self):
            return self.title

Now let's test to make sure that worked.  We'll create some data and test that ``parent`` exists on the instances.

.. code-block:: pycon

    >>> from mixins.models import BlogPost
    >>> bp = BlogPost.objects.create(title="post1", body="First post!")
    >>> bp2 = BlogPost.objects.create(title="post2", body="Second post!", parent=bp)
    >>> bp3 = BlogPost.objects.create(title="post3", body="Third post!", parent=bp2)
    >>> bp.parent
    >>> bp2.parent
    <BlogPost: post1>

Inherited Class-Level Methods
-----------------------------

So as you can see, everything is working correctly!  But that really doesn't save us much time yet, as it's fairly easy to copy and paste fields onto new models, and we still have to write methods which take advantage of those new fields.  In this case, I already know that I'm going to want to get the related children and descendants of my blogposts.  So why not write those methods on the abstract model?  Thanks to inheritance, those methods will apply to the new model as well.

.. code-block:: python

    class NaiveHierarchy(models.Model):
        parent = models.ForeignKey('self', null=True)
    
        def get_children(self):
            return self._default_manager.filter(parent=self)

        def get_descendants(self):
            descs = set(self.get_children())
            for node in list(descs):
                descs.update(node.get_descendants())
            return descs

        class Meta:
            abstract = True

Now, getting all the children or descendents of a particular node is easy:

.. code-block:: pycon

    >>> bp.get_children()
    [<BlogPost: post2>]
    >>> bp.get_descendants()
    set([<BlogPost: post2>, <BlogPost: post3>])

Now this ``NaiveHierarchy`` mixin is starting to become quite useful!  But what happens if I want to get all of the BlogPosts that have no parents?  It's really manager-level functionality.  So let's write a manager which defines a ``get_roots`` function.  Unfortunately, using abstract managers doesn't quite work yet (it works for non-abstract inheritance), but it probably will in future versions of Django.  In fact, by applying the latest patch on either Django ticket 7252_ or 7154_, it will work today. Let's see how this would look:

.. code-block:: python

    class NaiveHierarchyManager(models.Manager):
        def get_roots(self):
            return self.get_query_set().filter(parent__isnull=True)
    
    class NaiveHierarchy(models.Model):
        parent = models.ForeignKey('self', null=True)
        
        tree = NaiveHierarchyManager()
        
        def get_children(self):
            return self._default_manager.filter(parent=self)
        
        def get_descendants(self):
            descs = set(self.get_children())
            for node in list(descs):
                descs.update(node.get_descendants())
            return descs
        
        class Meta:
            abstract = True
    
    class BlogPost(NaiveHierarchy):
        title = models.CharField(max_length = 128)
        body = models.TextField()
        
        objects = models.Manager()
        
        def __unicode__(self):
            return self.title

Note that we needed to explicitly define objects as the basic manager, because once a parent class specifies a manager, it gets set as the default manager on all inherited subclasses.  This would play out exactly how you would expect:

.. code-block:: pycon

    >>> BlogPost.tree.get_roots()
    [<BlogPost: post1>]
    >>> BlogPost.tree.all()
    [<BlogPost: post1>, <BlogPost: post2>, <BlogPost: post3>]

Advanced Stuff
--------------

So now I really wanted to push the limit, and write a mixin which would enhance one of the basic methods of all ``Model`` classes: ``save()``.  This would be a DateMixin which would contain ``date_added`` and ``date_modified``, where ``date_modified`` was updated on each save.  To my surprise, this *Just Worked*.  Let's see the final result:

.. code-block:: python

    import datetime
    from django.db import models
        
    class DateMixin(models.Model):
        date_added = models.DateTimeField(default=datetime.datetime.now)
        date_modified = models.DateTimeField()
        
        def save(self):
            self.date_modified = datetime.datetime.now()
            super(DateMixin, self).save()
    
    class NaiveHierarchyManager(models.Manager):
        def get_roots(self):
            return self.get_query_set().filter(parent__isnull=True)
    
    class NaiveHierarchy(models.Model):
        parent = models.ForeignKey('self', null=True)
        
        tree = NaiveHierarchyManager()
        
        def get_children(self):
            return self._default_manager.filter(parent=self)
        
        def get_descendants(self):
            descs = set(self.get_children())
            for node in list(descs):
                descs.update(node.get_descendants())
            return descs
        
        class Meta:
            abstract = True
    
    class BlogPost(NaiveHierarchy, DateMixin):
        title = models.CharField(max_length = 128)
        body = models.TextField()
        
        objects = models.Manager()
        
        def __unicode__(self):
            return self.title

Conclusions
-----------

Mixins_ can be powerful tools, but there are some hazards in using mixins, which all boil down to the same basic problem:  unexpected consequences.  In the case of the ``DateMixin``, if any other class has defined a ``save()`` method, our custom ``save()`` method simply won't be called unless called explicitly.  Perhaps this is a documentation problem, but perhaps it's a fault in the idea of a date mixin altogether.

So all that being said, I'm not suggesting to go off and start using any of the mixins that I have provided here, but rather to illustrate how a mixin can be constructed with Django_'s new `Model Inheritance`_.  I do hope that a reusable app emerges with some great mixins that are useful for a large variety of tasks.  Because mixins are powerful, and new shiny things that Django can do, and new shiny things are worth being explored!

.. _Django: http://www.djangoproject.com/
.. _`Model Inheritance`: http://www.djangoproject.com/documentation/model-api/#model-inheritance
.. _mixins: http://en.wikipedia.org/wiki/Mixin
.. _django-mptt: http://code.google.com/p/django-mptt/
.. _7252: http://code.djangoproject.com/ticket/7252
.. _7154: http://code.djangoproject.com/ticket/7154
.. _Mixins: http://en.wikipedia.org/wiki/Mixin