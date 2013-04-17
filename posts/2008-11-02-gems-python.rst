---
layout: post
title: "Gems of Python"
date: 2008-11-02T16:04:42-06:00
comments: false
categories: [Python, Programming]
published: true
alias: [/blog/post/gems-python]
---

I've been using Python for a few years now, and continue to love it.  But the language is large enough that it seems every project that I look at uses a different subset of the language's features.  The nice thing is that by reading different people's code, you can find out about some real gems in the Python programming language.  Some of these tips are extremely obvious, and some are more obscure.  In any case, here are what I consider to be some real gems:

1.  filter_  This is one of Python's built-in functions, which allows you to remove unwanted items from a list.  It's very useful and highly overlooked.  Here's an example of how to use it:

    .. code-block:: pycon

        >>> lst = ['1', '2', '3', '4', 'asdf', '5']
        >>> def is_int_string(i):
        ...     try:
        ...         int(i)
        ...         return True
        ...     except ValueError:
        ...         return False
        ...
        >>> int_string_list = filter(is_int_string, lst)
        >>> int_string_list
        ['1', '2', '3', '4', '5']


    But there is a really neat filter shortcut, too.  You can have it filter out any values which evaluate to False.


    .. code-block:: pycon

        >>> lst = [0, 2, '', 'asdf', None, [], (), 'fdsa']
        >>> filter(None, lst)
        [2, 'asdf', 'fdsa']

    This is really great for filtering out unwanted values in a list.  I use it actually quite frequently and hope to see it in more python projects.

2.  itertools.chain_  I often have a list of lists, and want to run some operation on each item in that list of lists.  itertools.chain allows that to happen.  Let me demonstrate with an example:

    .. code-block:: pycon
        
        >>> import itertools
        >>> lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> list(itertools.chain(*lst))
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> sum(itertools.chain(*lst))
        45

    **itertools.chain** has become a major part of my day-to-day coding toolbox, and it's a real python gem.

3.  setdefault_ Do you find yourself writing this type of ``try..except KeyError`` pattern often?

    .. code-block:: pycon

        >>> dct = {}
        >>> items = ['anne', 'david', 'kevin', 'eric', 'anthony', 'andrew']
        ... for name in items:
        ...     try:
        ...         dct[name[0]].append(name)
        ...     except KeyError:
        ...         dct[name[0]] = [name]
        >>> dct
        {'a': ['anne', 'anthony', 'andrew'], 'k': ['kevin'], 'e': ['eric'], 'd': ['david']}

    That's a lot of boilerplate code for something that seems like it should be much easier.  Thankfully, this can be solved much  more easily by using **setdefault**, like so:

    .. code-block:: pycon

        >>> dct = {}
        >>> items = ['anne', 'david', 'kevin', 'eric', 'anthony', 'andrew']
        >>> for name in items:
        ...     dct.setdefault(name[0], []).append(name)
        ...
        >>> dct
        {'a': ['anne', 'anthony', 'andrew'], 'k': ['kevin'], 'e': ['eric'], 'd': ['david']}

    Much better, isn't it?

4.  defaultdict_ Given `setdefault`, it still seems like there should be a better way.  If you know upfront that you will be setting everything to an empty list if it isn't found, you should be able to specify that and have it just Do The Right Thing.  Thankfully, **defaultdict** does just that:

    .. code-block:: pycon

        >>> from collections import defaultdict
        >>> dct = defaultdict(list)
        >>> items = ['anne', 'david', 'kevin', 'eric', 'anthony', 'andrew']
        >>> for name in items:
        ...     dct[name[0]].append(name)
        ...
        >>> dct
        defaultdict(<type 'list'>, {'a': ['anne', 'anthony', 'andrew'], 'k': ['kevin'], 'e': ['eric'], 'd': ['david']})
        >>> dict(dct)
        {'a': ['anne', 'anthony', 'andrew'], 'k': ['kevin'], 'e': ['eric'], 'd': ['david']}

    I usually end up converting the defaultdict back to a regular dict before passing it around, but other than that, it's quite a useful tool to use.

5.  zip_ This is one that most people usually know, but still I find that sometimes people do strange things where a zip would be much easier.

    .. code-block:: pycon

        >>> numbers = [1, 2, 3, 4, 5]
        >>> letters = ['a', 'b', 'c', 'd', 'e']
        >>> for num, let in zip(numbers, letters):
        ...     print "Letter %d is '%s'" % (num, let)
        ...
        Letter 1 is 'a'
        Letter 2 is 'b'
        Letter 3 is 'c'
        Letter 4 is 'd'
        Letter 5 is 'e'

    Pretty simple, very common, and yet sometimes coders seem to work around it.  Also worth mentioning is that there's an iterable version of this, izip_, which is located in itertools.

6.  title_  I wrote some little function to turn a string of lower case text into a 'titleized' string at work, and a few coworkers laughed and said,  "why didn't you just use title"?  The answer: I didn't know about it.  It's not something you run into every day, but when you need it, it's super useful.  Here's an example:

    .. code-block:: pycon

        >>> s = 'the little green men'
        >>> s.title()
        'The Little Green Men'

    It's that easy!  Next time you need to turn something into a title, look for this method on strings first.

That's all I've got for now.  There are many more gems in the Python programming language, but these are some that I think are especially useful.  Please share in the comments if you have any other gems that you have found in your uses of Python.

**UPDATE**: Eric Holscher has posted `a list of his Python gems as well`_, and it's got some great stuff on it.  Check it out!

.. _filter: http://docs.python.org/library/functions.html?highlight=filter#filter
.. _itertools.chain: http://docs.python.org/library/itertools.html?highlight=itertools#itertools.chain
.. _setdefault: http://docs.python.org/library/stdtypes.html?highlight=setdefault#dict.setdefault
.. _defaultdict: http://docs.python.org/library/collections.html?highlight=defaultdict#collections.defaultdict
.. _zip: http://docs.python.org/library/functions.html?highlight=zip#zip
.. _izip: http://docs.python.org/library/itertools.html?highlight=izip#itertools.izip
.. _title: http://docs.python.org/library/stdtypes.html?highlight=title#str.title
.. _`a list of his Python gems as well`: http://ericholscher.com/blog/2008/nov/3/python-gems-my-own/