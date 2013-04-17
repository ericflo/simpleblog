---
layout: post
title: "April Fools"
date: 2008-04-01T01:14:03-05:00
comments: false
categories: [April 1st, Django, Python]
published: true
alias: [/blog/post/april-fools]
---

April Fool's Day rocks!  Maybe I enjoy it because it happens to share the same day as my birthday, but I think it's more to do with the fact that everyone's having fun, being lighthearted, and simply not taking things too seriously.  Last year the blog wasn't in any shape to do anything fun for the occasion, but this year it took me about 10 minutes to whip up some middleware fun.  That's right, if you can read and understand this right now, the secret is out: a bit of Django middleware is all that's needed to turn your blog into l33t-sp34k central.

I'll even go one step further than telling you how I did it, I'll give you the code:

.. code-block:: python

    import re
    import lxml.html

    trans = {
        'cks': r'xxors',
        'lol': r'r0flc0pt3r',
        'the': r'teh',
        'a': r'4',
        'e': r'3',
        'f': r'ph',
        'g': r'6',
        'h': r'|-|',
        'i': r'1',
        'o': r'0',
        's': r'5',
    }

    def is_code_block(node):
        return node.attrib.get('class', None) == 'highlight'

    def recursive_leetifier(node):
        for child in node.iterchildren():
            if child.text and not is_code_block(child):
                for pattern in trans.iterkeys():
                    child.text = re.compile(pattern, re.I).sub(trans[pattern], child.text)
            if not is_code_block(child):
                recursive_leetifier(child)
    
    class LeetSpeakMiddleware(object):
        def process_response(self, request, response):
            try:
                html = lxml.html.fromstring(response.content)
                recursive_leetifier(html)
                response.content = lxml.html.tostring(html)
            except:
                pass
            return response

The idea behind it is simple: Let the request go completely through Django's request/response cycle, and just before returning the correct response, parse the HTML and convert all of the actual content to l33t by doing some simple regular expression substitution.  I'm using lxml.html_ simply because I attended `Ian Bicking's talk at Pycon 2008`_ and was intrigued.  I must say that the familiar ElementTree_ interface helped a lot in getting this code up and running in a short amount of time.

Hopefully you all find this holiday to be as fun as I do, and maybe I'll see some more l33t next year!

.. _lxml.html: http://codespeak.net/lxml/parsing.html#parsing-html
.. _`Ian Bicking's talk at Pycon 2008`: http://blog.ianbicking.org/2008/03/21/pycon-talks/
.. _ElementTree: http://docs.python.org/lib/module-xml.etree.ElementTree.html