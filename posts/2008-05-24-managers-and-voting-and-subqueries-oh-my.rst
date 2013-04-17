---
layout: post
title: "Managers and Voting and Subqueries, Oh My!"
date: 2008-05-24T18:12:19-05:00
comments: false
categories: [Django, Programming, Python]
published: true
alias: [/blog/post/managers-and-voting-and-subqueries-oh-my]
---

Recently I launched Peevalizer_, a website for talking about your pet peeves, which of course was written in Python using the Django web framework.  In fact, it was the culmination of my efforts to `teach myself design`_, and while I made some progress, it's clear that I'll never be a designer.  Anyway, part of Peevalizer_ is that users can vote on different pet peeves, and view the peeves with the highest score.  I used `django-voting`_ as the application to enable this functionality, and it provides a manager on the ``Vote`` object with methods for getting the top N results, where N is a positive integer.  

One of the reasons for custom manager on ``Vote`` is because `aggregate support`_ has not yet been finished.  However with Django's built-in Pagination_ support, it's necessary to retrieve not only a list of the top N voted pet peeves, but a list of all of the pet peeves, ordered by score.  How is this possible?  Specifically, how is this possible without forking `django-voting`_?  Here is the solution that I came up with:

.. code-block:: python

    class VoteAwareManager(models.Manager):
        def _get_score_annotation(self):
            model_type = ContentType.objects.get_for_model(self.model)
            table_name = self.model._meta.db_table
            return self.extra(select={
                'score': 'SELECT COALESCE(SUM(vote),0) FROM %s WHERE content_type_id=%d AND object_id=%s.id' % 
                    (Vote._meta.db_table, int(model_type.id), table_name)}
            )

        def most_hated(self):
            return self._get_score_annotation().order_by('-score')
    
        def most_loved(self):
            return self._get_score_annotation().order_by('score')

Then I assigned that manager onto all of the objects that could be voted on.  What that's doing is literally issuing a subquery for every row, doing an aggregate on all of the votes for that row, and assigning it to an attribute named *score*.

However, we also wanted to allow for voting on ``User`` objects, which is built in to Django and cannot be easily changed.  How do we add this manager to user?  I spent a while thinking about that before realizing that it's not the right question to ask.  The right question to ask is, how can we associate the ``User`` model with this manager?  A quick look through some Django source code revealed this to be an absolutely trivial task.  Here's how it goes in our code:

.. code-block:: python

    from django.contrib.auth.models import User
    manager = VoteAwareManager()
    manager.model = User

    for user in manager.most_hated():
        # Do something with user's score

There are a few things to note about this implementation.  Firstly, it can be much more computationally expensive to use this method instead of using `django-voting`_'s method (which executes some custom SQL), so either be aware of that or use aggressive caching strategies to overcome this shortcoming.  The other thing is if you're not using a manager like this on multiple models, and since managers mostly just proxy to ``QuerySet`` anyway, it might be simpler to just acquire a ``QuerySet`` on the model that you would like to get, and run the ``extra()`` method in the calling function.

.. _Peevalizer: http://peevalizer.com/
.. _`teach myself design`: http://www.eflorenzano.com/blog/post/learning-design/
.. _`django-voting`: http://code.google.com/p/django-voting/
.. _`aggregate support`: http://code.google.com/p/django-aggregation/
.. _Pagination: http://www.djangoproject.com/documentation/pagination/