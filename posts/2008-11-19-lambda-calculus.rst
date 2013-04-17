---
layout: post
title: "Lambda Calculus"
date: 2008-11-19T23:00:09-06:00
comments: false
categories: [Theory, Lambda Calculus, Programming, Python]
published: true
alias: [/blog/post/lambda-calculus]
---

It seems that people either love things like `lambda calculus`_ and eat it up,
or their eyes gloss over and they don't care or want to learn about it.  I was
firmly part of the latter group, until I took a class in college that forced
me to learn about it.  The thing is, once you learn more about a subject like
this, the less you'll understand why you were so averse to learning about it.

In the spirit of broadening our horizons, let's explore the lambda calculus and
see if it's as hard as it's cracked up to be.  I don't claim to be a wizard at
this stuff, and by no means am I a theoretical computer scientist, but that's
not the goal.  The goal is to cut down on the formality and see if we can expore
this stuff a bit.  First, let's look at a very basic function: addition.  In
lambda calculus it looks like this:

.. code-block:: text

    >> x. x + 1

That is, a function whose argument is named ``x``, returns the value ``x + 1``.
This looks really similar to some syntax that we have in Python.  Let's see
if we can find a corollary to help make things easier:

.. code-block:: python

    lambda x: x + 1

Surprisingly, the syntax is almost the same!  It's an anonymous function which
takes ``x`` as its one argument and returns ``x + 1``.  Lambda calculus doesn't
have powerful enough syntax for talking about functions with multiple arguments,
though, so you may think that it's not very powerful.  Thanks to a technique
called currying_, however, we can express functions with infinite numbers of
arguments.  This is how that might look:

.. code-block:: text

    >> x. >> y. x + y

This is where I think the syntax starts to get in the way of readability.  Let's
see what this would look like in Python:

.. code-block:: python

    lambda x: lambda y: x + y

Hmmm...it's not much more readable, but at least we can open up an interactive
interpreter to see what we're doing.  Basically what we're doing is creating a
function which returns another function.  That inner function then has access
not only to its single argument, but to its parent's argument as well.  Let's
demonstrate that this works:

.. code-block:: pycon

    >>> add = lambda x: lambda y: x + y
    >>> add(5)(4)
    9

Now does this work if we start to change the variable names?  What if I just
decide that I can't stand the letter ``x`` and don't want it inside any more of
my functions.  Well I can simply change the variable name, as long as I change
any uses of that variable.  It would work just the same:

.. code-block:: pycon

    >>> add = lambda z: lambda y: z + y
    >>> add(5)(4)
    9

In this instance, we have changed all of our instances of ``x`` with ``z``.
This ability to change the names of bound variables is the first rule of lambda
calculus, and it's called ?-conversion.

As developers, we intuitively understand the idea of function application.  We
understand that a function which takes in an argument replaces all references
to that argument with the given value, and returns a result.  For example, in
the addition function, lets go through the steps for function application:

.. code-block:: pycon

    >>> add = lambda x: lambda y: x + y
    >>> add5 = add(5)
    # We can envision what's happening here by replacing x with 5
    # add5 = lambda 5: lambda y: 5 + y
    # add5 = lambda y: 5 + y
    >>> add5(4)
    # And now the final function application, resulting in a value
    # lambda 4: 5 + 4
    9

This idea of function application, in lambda calculus is given the name
2-reduction.  To review, in lambda calculus syntax that process would look like
so:

.. code-block:: text

    (>> x. >> y. x + y) 5
    (>> y. 5 + y) 4
    5 + 4
    9

Something that we also intuitively know as developers is that functions can do
the exact thing, but have very different implementations.  For example this
function:

.. code-block:: python

    >> x. x + x

...will give the same results for all values as this function:

.. code-block:: python

    >> x. x * 2

We understand that code which uses the former function can easily swap out the
latter and expect the program the function correctly.  This idea is called
.-conversion in lambda calculus.

See, this is pretty simple stuff!  Obviously there are subtleties that I didn't
go into, and it gets a bit more confusing when we start to try to figure out
formally which variables occur bound and which occur free, and as we attempt to
preserve that status while doing ?-conversion, 2-reduction, and .-conversion.

Here's some really mind bending food for thought:

.. code-block:: text

    (>> x. x x) (>> x. x x)

Think about how this would reduce:

.. code-block:: text

    (>> x. x x) (>> x. x x)
    (>> (>> x. x x). (>> x. x x) (>> x. x x))
    (>> x. x x) (>> x. x x)

As you can see, we could do this forever.  This is called the ? combinator,
and it lets us do some really cool things with recursion. Maybe more on that in
a later blog post.

What is all of this good for?  Well, with only this very simple, rigidly
defined ruleset, we can express every possible computer program.  That makes it
very good for doing mathematical proofs and other various scholarly things
when we want to explore algorithms.  It also forms the basis of all programming
languages, and especially functional programming languages.

Of particular interest to me is that we can actually represent numbers, truth,
and logic using only these very basic primitives.  I'll explore that in another
post.  To me, all of this is fascinating, and it's hard to believe that before
my teacher forced me to learn it, I actively didn't want to know about it.

.. _`lambda calculus`: http://en.wikipedia.org/wiki/Lambda_calculus
.. _currying: http://en.wikipedia.org/wiki/Currying