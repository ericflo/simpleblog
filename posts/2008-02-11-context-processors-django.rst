---
layout: post
title: "On Context Processors in Django"
date: 2008-02-11T14:20:01-06:00
comments: false
categories: [Context Processors, Django, James Bennett, Python]
published: true
alias: [/blog/post/context-processors-django]
---

This started out as a response in the comments to James Bennett's `latest post`_, but I think that there's enough here to warrant its own post.  If you haven't yet read it, then I suggest you do--it's a well-put argument for Django's application-level modularity and pluggability.

But I do disagree with him on one point.  One of the things that he highlights is about *"how easy it is for one Django application to expose functionality to others through things like context processors".*  I don't find this to be true.  Currently there are only two ways of adding processors to the list of ``context_processors`` for a particular view:

1. Adding them as an argument to the RequestContext (per-view).
2. Adding them to the global context processors list in settings.py (global).

What these methods lack is a middle ground: per-app specification of context processors.  This is what  James Bennett seemingly alludes to which simply doesn't exist. What if I'd like all of the views in my blog app, and all views in flatpages to get a certain context processor list?  Currently in Django that is not possible.  I do think that there is demand for this, and it's something that probably wouldn't be too hard to add to trunk.

But really, if I can think of this particular use case of context processor loading, I'm sure there are other people who could think of others.  For example, what about a different set of processors based on URL, or based on IP address, or something even more strange?  What Django really needs is a pluggable context processor loader similar to how it loads session backends, authentication backends, database backends, urls, etc.  That way, people could provide their own loaders to do any kind of context processing differentiation that they want.

The only thing that this could do is make Django applications more pluggable--and that's always a good thing!  The good news is that PyCon is coming up, and I can try to tackle this during the sprinting days.

**UPDATE:**  `Malcolm Tredinnick`_ has posted an excellent followup to this post that suggests a simple solution for those who want to do something similar to application-level context processor loading right now.

.. _`latest post`: http://www.b-list.org/weblog/2008/feb/11/integrity/
.. _`Malcolm Tredinnick`: http://www.pointy-stick.com/blog/2008/02/12/django-tip-application-level-context-processors/