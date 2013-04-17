---
layout: post
title: "Looking Forward: Upcoming Django Developments Worth Waiting For"
date: 2007-12-10T14:18:26-06:00
comments: false
categories: [Django, Python]
published: true
alias: [/blog/post/looking-forward-upcoming-django-developments-worth]
---

1. Newforms-Admin_
    Started soon after the newforms package started to become stable, the newforms-admin branch 
    allows for a much more modular and flexible admin application.  The amount of flexibility allowed in 
    this branch extends to permissions, allowing for user-defined permissions schemes--can you say 
    'row-level permissions'?  It's even flexible enough to require no permissions at all: I needed a quick 
    display interface for work this past summer, and I used some of the hooks in the newforms-admin 
    branch to disable login and permissions and simply display some data publicly.

    Also, multiple different admin interfaces are easy with newforms-admin.  Group your apps into 
    functional sets and give each functional set its own admin interface.  Those who are using this 
    branch know that once you've gone newforms-admin, you'll never go back!

2. GeoDjango_
    This one flew under my radar until very recently.  Their stated goal is "to make it as easy as 
    possible to build GIS web applications and harness the power of spatially enabled data."  These guys 
    have done some really amazing things with this branch, including linking of the geographic data to 
    cool widgets that can be displayed in the admin interface (think google maps, openlayers, and more 
    to come as time goes on).  I don't personally have a need for any of the capabilities being added in 
    this project, but the scope and quality of what is being produced is impressive to say the least.

3. Queryset-Refactoring_
    As code grows and evolves, it's difficult to stop at a certain point and say, "this code doesn't fit the 
    bill anymore."  `Malcolm Tredinnick`_ was the one who stopped and said it.  Already at this stage, 
    `many many bugs`_ have been fixed by this branch.  Queryset-refactoring is not just for fixing 
    bugs.  Once it's completed, database backends will have a much easier time of customizing their 
    generated SQL.  With each change like this, Django becomes more modular.

4. `Manually-Specified Intermediary Model Support`_
    OK I'm biased on this one.  This is the patch that I've been working on lately.  It's because every 
    time I create an Django application, I start out with a ManyToManyField and end up breaking that off 
    into a separate model.  Once that's done, I have to change all of my code so that it doesn't use the 
    convenient ManyToManyField helpers.  Once this patch is complete, you'll be able to specify an 
    intermediary model which will act as the storage for your m2m data.  In this way, extra information 
    can be attached to each relationship.

5. `Fixing app_label`_
    We're entering into 2008 soon, and that will mean that Django has been public for over two years.  
    Some of the core developers have been using it internally for even longer than that.  So one of the 
    things which people have started running into, is that app_labels have started clashing.  There hasn't 
    been any definitive decision on how to avoid these clashes, but there have been several promising 
    proposals.  In any case, expect this functionality to change somewhat in the next few months, so 
    that 'ellington.search' can coexist alongside 'chicagocrime.search'.  No longer will you have to worry 
    about naming everything differently!

These are just a few of the developments that are going on which seem interesting and promising.  I hope that each and every one of these developing features eventually makes it into trunk, so that everyone can benefit from the hard work that people have put into the project.  Also, if you've got a feature that you're excited about, let me know through the comments.

.. _Newforms-Admin: http://code.djangoproject.com/wiki/NewformsAdminBranch
.. _GeoDjango: http://code.djangoproject.com/wiki/GeoDjango
.. _Queryset-Refactoring: http://code.djangoproject.com/wiki/QuerysetRefactorBranch
.. _`Malcolm Tredinnick`: http://www.pointy-stick.com/blog/
.. _`many many bugs`: http://code.djangoproject.com/query?status=new&status=assigned&status=reopened&keywords=%7Eqs-rf&order=priority
.. _`Manually-Specified Intermediary Model Support`: http://code.djangoproject.com/ticket/6095
.. _`Fixing app_label`: http://groups.google.com/group/django-developers/browse_thread/thread/d1eca0f5dca49a07/8aea3e9ece9835ec#8aea3e9ece9835ec
