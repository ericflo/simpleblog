---
layout: post
title: "My Awesome Regex Snippet"
date: 2008-05-06T03:24:07-05:00
comments: false
categories: [Programming, Python, Regex]
published: true
alias: [/blog/post/my-awesome-regex-snippet]
---

There are many times when the programming task at hand is to iterate over some semi-structured text, transform parts of that text in some way, and reintegrate those transformed parts back into the original text.

Typically using a regular expression with re.sub and a callback function, but sometimes you want a bit more control of the process (especially over those parts that *dont* match the regex). Usually my solution is to write a one-off function that does it, but today I had to write that function yet again and decided to generalize it and post it here.

To be completely honest, this post is more for my own archival purposes than for the internet as a whole, but if anyone else finds it useful, then I'm ecstatic.

.. code-block:: python

    def re_parts(regex_list, text):
        """
        An iterator that returns the entire text, but split by which regex it 
        matched, or none at all.  If it did, the first value of the returned tuple 
        is the index into the regex list, otherwise -1.
        
        >>> first_re = re.compile('asdf')
        >>> second_re = re.compile('an')
        >>> list(re_parts([first_re, second_re], 'This is an asdf test.'))
        [(-1, 'This is '), (1, 'an'), (-1, ' '), (0, 'asdf'), (-1, ' test.')]
        
        >>> list(re_parts([first_re, second_re], 'asdfasdfasdf'))
        [(0, 'asdf'), (0, 'asdf'), (0, 'asdf')]
        
        >>> list(re_parts([], 'This is an asdf test.'))
        [(-1, 'This is an asdf test.')]
        
        >>> third_re = re.compile('sdf')
        >>> list(re_parts([first_re, second_re, third_re], 'This is an asdf test.'))
        [(-1, 'This is '), (1, 'an'), (-1, ' '), (0, 'asdf'), (-1, ' test.')]
        """
        def match_compare(x, y):
            return x.start() - y.start()
        prev_end = 0
        iters = [r.finditer(text) for r in regex_list]
        matches = []
        while iters:
            if matches:
                match = matches.pop(0)
                (start, end) = match.span()
                if start > prev_end:
                    yield (-1, text[prev_end:start])
                    yield (regex_list.index(match.re), text[start:end])
                elif start == prev_end:
                    yield (regex_list.index(match.re), text[start:end])
                prev_end = end
            else:
                matches = []
                for iterator in iters:
                    try:
                        matches.append(iterator.next())
                    except StopIteration:
                        iters.remove(iterator)
                matches = sorted(matches, match_compare)
        last_bit = text[prev_end:]
        if len(last_bit) > 0:
            yield (-1, last_bit)