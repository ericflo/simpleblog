---
layout: post
title: "Getting Involved in the Django Project"
date: 2007-12-07T12:24:10-06:00
comments: false
categories: [Django, Open Source]
published: true
alias: [/blog/post/getting-involved-django-project]
---

Getting involved in an open source project is hard.  I've been working with Django_ since early 2006 and doing so makes me want to contribute back to the project.  Several times now I've made attempts to do so, but all of them have failed.  Looking back it's easy to see where I, as a newcomer to the open source world, went wrong.  So let's start out with what **not** to do, by example.  After that I'll give some suggestions on what I think is the right way to go about it.

Don't do these things:
----------------------

1. Don't bite off more than you can chew
    As a newcomer to both Python and Django, and to web development in general, one thing that I
    constantly needed to do was redefine my models slightly differently as I discovered flaws in my 
    previous designs.  Django does not make this easy, as you either have to manually migrate your 
    SQL or you have to delete all of your data.  Can you see where this is going?  I thought, "Perfect, 
    there's a way that I can contribute!  I'll add schema evolution to Django!"  This was a huge 
    undertaking, it took a long time, and it eventually flopped because I simply didn't have the 
    experience at that point necessary to accomplish this task.

2. Don't work privately
    The other problem with tackling schema evolution was that I had contacted off-list another person 
    who was enthusiastic about the idea, `Victor NG`_.  Now  he's a great coder and did a lot of the 
    work on that project, but he wasn't an established member of the community.  We had set up a 
    completely separate SVN (actually SVK_) server and everything.  The result was that we were 
    completely shut off from the rest of the development community, and didn't get any input or insight 
    from the people who were really running the project.

3. As a newcomer, don't work on a community project
    The next thing that I tried working on was a "DjangoForge" project.  I worked very hard for almost a 
    month--the month leading up to PyCon--and got a complete prototype up and running.  When I got 
    to PyCon, I expected to make a big debut and everyone would instantly love it and jump on board.  
    Wow, was that naive!  Nobody knew who I was, and everyone had different ideas about what a 
    community portal, a "DjangoForge", would need to be.


Do these things:
----------------

1. Start without code
    Start on documentation.  There are two reasons that this is a good idea.  Firstly, those people who 
    are checking in tickets will start to recognize your name and will see that you're interested in 
    contributing.  Secondly, you will begin to understand more and more about the internals of the 
    framework as you see how people are adding features.  I think that writing documentation is boring, 
    but what's more boring is not knowing the codebase well enough and writing bad code as a result.

2. Then do test code
    After documenting some of the underpinnings of the framework, you now have a pretty good idea 
    about how it *should* behave.  Now make sure it really behaves that way.  Many people don't follow 
    the `Code Unit Test First`_ or test-driven development methodology.  That is, they write the code 
    and submit the patch without formal tests.  These patches usually can't be checked in to Django 
    without test code, as a lot of people rely on the trunk to be stable.  So you can do a lot of good by 
    simply writing test code, and it will earn you a lot of gratitude from the folks trying to get things 
    done.  On top of being helpful and earning gratitude, it helps you to learn the framework that much 
    better.

3. Work on already-submitted tickets.
    It can be tempting to work on a pet-feature that you would like to have done.  This is not a bad 
    temptation, but for someone who is trying to become part of the community, it may be better to look 
    at what the core developers are anxious to have done.  This is where I am currently, working on 
    tickets_ `that the`_ `core devs`_ `have filed`_.  They have good reasons for filing these tickets: 
    they have deemed it a wanted feature or bug, they have determined that it's a solvable idea or 
    problem, and they may even have insights in how to implement it!  These tickets can range from 
    small-scale to large-scale and now is when you can really start to show your stuff as a programmer.

4. Read django-dev mailing list
    There's nothing more helpful than tracking where Django is going and what ideas are being kicked 
    around on that list.  Many times an idea has been brought up, fleshed out, and eventually decided 
    upon.  This doesn't always happen in the ticket tracker, and it shouldn't.  Whenever discussion is 
    needed, the mailing lists are a much better forum for that discussion to take place.  This is also a 
    good place to ping the community on tickets that you're interested in or have worked on.  Just 
    *please* don't spam the list, as nothing will make people more upset at you than a whiny spammer 
    on the django-dev mailing list.

...and beyond
-------------

After that, I have no more solid advice.  That's where I'm sitting right now with the Django project.  I'd like to become even more involved.  I'll probably will go about doing so by starting to propose new features, jumping in on the conversation, attending PyCon 2008, and working on spinoff projects like the excellent django-evolution_.  But I'd like to know how other people have done it.  **How have you gotten involved in the Django project?**

**Update:** `Adrian Holovaty`_ makes a great point in mentioning to check out the `Contributing to Django`_ section of the Django documentation, with gives a plethora of guidelines and tips for doing just that.  Thanks, Adrian!

.. _Django: http://www.djangoproject.com
.. _`Victor NG`: http://www.crankycoder.com/
.. _SVK: http://svk.bestpractical.com/view/HomePage
.. _`Code Unit Test First`: http://c2.com/cgi/wiki?CodeUnitTestFirst
.. _tickets: http://code.djangoproject.com/ticket/6095
.. _`that the`: http://code.djangoproject.com/ticket/6064
.. _`core devs`: http://code.djangoproject.com/ticket/6066
.. _`have filed`: http://code.djangoproject.com/ticket/6092
.. _django-evolution: http://code.google.com/p/django-evolution/
.. _`Adrian Holovaty`: http://www.holovaty.com/
.. _`Contributing to Django`: http://www.djangoproject.com/documentation/contributing/