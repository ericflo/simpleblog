---
layout: post
title: "Inheritance vs. Composition"
date: 2008-05-04T18:12:38-05:00
comments: false
categories: [Django, Java, Object Oriented Programming, Programming, Python]
published: true
alias: [/blog/post/inheritance-vs-composition]
---

Lately there's been a lot of discussion in certain programming communities about which method of object extension makes more sense: inheritance, or composition.  Most of the time these discussions turn into debates, and when that happens developers tend to "take sides"--often moving towards extremist positions on the issue.  I've been sort of quietly thinking about it all lately, trying to determine which use case warrants which approach.  Here I show examples of both, explore some properties and consequences of both composition and inheritance, and finally talk about my own preferences.

Examples of Composition and Inheritance
---------------------------------------

Before talking about the consequences of inheritance vs. composition, some simple examples of both are needed.  Here's a simplistic example of object composition (using Python, of course, as our demonstration language):

.. code-block:: python

    class UserDetails(object):
        email = "floguy@gmail.com"
        homepage = "http://www.eflorenzano.com"

    class User(object):
        first_name = "Eric"
        last_name = "Florenzano"
        details = UserDetails()

Obviously these are not very useful classes, but the essential point is that we have created a namespace for each User object, "details", which contains the extra information about that particular user.

An example of the same objects, modified to use object inheritance might look as follows:

.. code-block:: python

    class User(object):
        first_name = "Eric"
        last_name = "Florenzano"

    class UserDetails(User):
        email = "floguy@gmail.com"
        homepage = "http://www.eflorenzano.com"

Now we have a flat namespace, which contains all of the attributes from both of the objects.  In the case of any collisions, Python will take the attribute from UserDetails.

Consequences
------------

From a pure programming language complexity standpoint, object composition is the simpler of the two methods.  In fact, the word "object" may not even apply here, as it's possible to achieve this type of composition using structs in C, which are clearly not objects in the sense that we think of them today.

Another immediate thing to notice is that with composition, there's no possibility of namespace clashes.  There's no need to determine which attribute should "win", between the object and the composed object, as each attribute remains readily available.

The composed object, more often than not, has no knowledge about its containing class, so it can completely encapsulate its particular functionality.  This also means that it cannot make any assumptions about its containing class, and the entire scheme can be considered less brittle.  Change an attribute or method on ``User``? That's fine, since ``UserDetails`` doesn't know or care about ``User`` at all.

That being said, object inheritance is arguably more straightforward.  After all, an e-mail address isn't a logical property of some real-world object called a "UserDetails".  No--it's a property of a user--so it makes more sense to make it an attribute on our virtual equivalent, the ``User`` class.

Object inheritance is also a more commonly-understood idea.  Asking a typical developer about object composition will most likely result in some mumbling and deflection, whereas the same question about object inheritance will probably reveal a whole host of opinions and experience.  That's not to say that composition is some sort of dark art, but simply that it's less commonly talked about in so many words.

As more of a sidenote than anything else, inheritance can be speedier in some compiled languages due to some compile-time optimizations vs. the dynamic lookup that composition requires.  Of course, in Java you can't escape the dynamic method lookup, and in Python it's all a moot point.

My Preferences
--------------

In general, I find object composition to be desirable.  I've seen too many projects get incredibly (and unnecessarily) confusing due to complicated inheritance hierarchies.  However, there are some cases where inheritance simply makes more sense logically and programmatically.  These are typically the cases where an object has been broken into so many subcomponents that it doesn't make sense any more as an object itself.

The Django_ web framework has an interesting way of dealing with model inheritance, and I think that more projects should follow its example.  It uses composition behind the scenes, and then flattens the namespace according to typical inheritance rules.  However, that composition still exists under the covers, so that that method may be used instead.

The answer is not going to be "composition always" or "inheritance always" or even any combination of the two, "always".  Each has its own drawbacks and advantages and those should be considered before choosing an approach.  More research needs to be done on the hybrid approaches, as well, because things like what Django is doing will provide more answers to more people than traditional approaches.  Cheers to continued thought about these problems and to challenging conventional thought!

.. _Django: http://www.djangoproject.com/