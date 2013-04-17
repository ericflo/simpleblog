---
layout: post
title: "Making Django Imports Less Painful"
date: 2008-11-10T21:25:58-06:00
comments: false
categories: [Python, Django, Programming]
published: true
alias: [/blog/post/making-django-imports-less-painful]
---

Way back in the early days of Django, it used to magically import certain functions before any views were ever run.  At some point that bit of magic got stripped out and now we have to explicitly import the things that we are going to use...much like everything else in Python.  One thing that `Simon Willison`_ suggested at DjangoCon is that the core developers might think about including a common set of functions that could be imported and used as shortcuts instead of importing everything again and again.

I shrugged it off at the time, thinking it was a solution in search of a problem, but wanting to keep an open mind, I wanted to try it out in one app to see how it would look.  In this spirit, I created a file called ``dj.py`` inside of a project of mine, `django-avatar`_.  I looked around at what some of the most commonly used functions were, and came up with a ``dj.py`` file that looked something like this:

.. code-block:: python

    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from django.contrib.auth.decorators import login_required
    from django.contrib.auth.models import User
    from django.utils.translation import ugettext as _
    from django import forms
    from django.utils.safestring import mark_safe

Then I went through and deleted all of these imports from throughout the project, and replaced it with a single import:

.. code-block:: python

    from avatar import dj

Now we have that shortcut module loaded, we can use it.  Here's an example of what one view looked like before:

.. code-block:: python

    from django.contrib.auth.decorators import login_required
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from django.utils.translation import ugettext as _
    from django.http import HttpResponseRedirect

    def delete(request, extra_context={}, next_override=None):
        avatars = Avatar.objects.filter(user=request.user).order_by('-primary')
        if avatars.count() > 0:
            avatar = avatars[0]
        else:
            avatar = None
        delete_avatar_form = DeleteAvatarForm(request.POST or None, user=request.user)
        if request.method == 'POST':
            if delete_avatar_form.is_valid():
                ids = delete_avatar_form.cleaned_data['choices']
                Avatar.objects.filter(id__in=ids).delete()
                request.user.message_set.create(
                    message=_("Successfully deleted the requested avatars."))
                return HttpResponseRedirect(next_override or _get_next(request))
        return render_to_response(
            'avatar/confirm_delete.html',
            extra_context,
            context_instance = RequestContext(
                request,
                { 'avatar': avatar, 
                  'avatars': avatars,
                  'delete_avatar_form': delete_avatar_form,
                  'next': next_override or _get_next(request), }
            )
        )
    change = login_required(change)

And here's what the code looked like afterward:

.. code-block:: python

    from avatar import dj

    def delete(request, extra_context={}, next_override=None):
        avatars = Avatar.objects.filter(user=request.user).order_by('-primary')
        if avatars.count() > 0:
            avatar = avatars[0]
        else:
            avatar = None
        delete_avatar_form = DeleteAvatarForm(request.POST or None, user=request.user)
        if request.method == 'POST':
            if delete_avatar_form.is_valid():
                ids = delete_avatar_form.cleaned_data['choices']
                Avatar.objects.filter(id__in=ids).delete()
                request.user.message_set.create(
                    message=dj._("Successfully deleted the requested avatars."))
                return dj.HttpResponseRedirect(next_override or _get_next(request))
        return dj.render_to_response(
            'avatar/confirm_delete.html',
            extra_context,
            context_instance = dj.RequestContext(
                request,
                { 'avatar': avatar, 
                  'avatars': avatars,
                  'delete_avatar_form': delete_avatar_form,
                  'next': next_override or _get_next(request), }
            )
        )
    change = dj.login_required(change)

It works!  Although after all of that, I have decided that in my opinion it's just not worth the effort.  It adds an extra level of indirection when tracing through the code, it litters the view with the ``dj`` namespace, and it's harder to know what you have available to you.  Maybe you like this style better, though.  If so, what about this style do you like?

.. _`Simon Willison`: http://simonwillison.net/
.. _`django-avatar`: http://code.google.com/p/django-avatar/