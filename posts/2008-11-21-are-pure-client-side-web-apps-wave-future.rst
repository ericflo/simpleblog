---
layout: post
title: "Are pure client-side web apps the wave of the future?"
date: 2008-11-21T21:11:49-06:00
comments: false
categories: [Javascript, Programming, CouchDB]
published: true
alias: [/blog/post/are-pure-client-side-web-apps-wave-future]
---

It seems that the world of computing is always oscillating between offloading
more work to the server, and offloading more work to the client.  In the very
early days of dumb terminals, we had most of the actual computation being done
on big mainframes.  Then personal computers became more powerful, allowing for
much richer applications to be created.

With the advent of the internet, the landscape of computing architectures
shifted again to being done focused on the server.  Now, however, JavaScript has
become more powerful.  Combined with things like SVG and the canvas tag, we can
create extremely rich applications that take place solely in the browser.

Projects like CouchDB_ are even starting to open the door for
`truly peer-to-peer web applications`_.  With all of this taking place, it seems
that client-side web applications are poised to see some fairly strong growth.
This is especially evident now that companies as big as Google seem interested
in the idea, with its `Google Gears`_ product that allows you to "work offline".
But there are certain things that need to be satisfied first.

We need a way of enforcing security across these apps.  It looks like some
combination of OpenID and OAuth are going to be the winners in this space, but
I've never seen a seamless implementation of either of these protocols, even by
the companies most invested in the technology.  There is a lot of work to go on
usability before authentication and authorization are ubiquitous through these
open protocols.

We also need to standardize more on the data interchange formats that we use to
shuttle information back and forth between these different apps.  Atom_ goes a
long way towards describing the data that we use, but its adoption is nowhere
near ubiquitous, and some sites still rely on older, more outdated, RSS
syndication formats that aren't quite up to the task.

But even if we standardize on some application platform (be it Google Gears or
CouchDB or some other container), security, and data interchange formats, there
are certain things that need to be considered.  For one, there are some
applications that just aren't practical to be implemented on the client.  Video
editing comes to mind (and I would know, considering I interned for eyespot_, a
company which was attempting to do just that).

Another concern is that, as we've seen with the emergence of standards for CSS
and HTML, a certain amount of rigidness is good, but a strict conformist
attitude leads to significantly stifled innovation.  If you were to write an app
that doesn't fall within the boundaries of what's possible given the agreed-upon
standards, would you still be able to go forward with the development of the
app, or would you run into resistance from those who have a stake in those
standards?

In all, I have a feeling that we are going to move more and more to a hybrid
approach, with much more logic being computed on the side of the client
(especially in terms of visual components and interactivity), and that much more
of the server side is going to be involved in slicing and serving up just the
raw data.  We can see this happening today with technologies like AJAX being
touted as the centerpiece of some "Web Two Point Oh" sites.  I'm excited to see
where this will all go, and more than excited that, being a developer during
this time, get to help shape that direction.

.. _CouchDB: http://incubator.apache.org/couchdb/
.. _`truly peer-to-peer web applications`: http://jchris.mfdz.com/code/2008/11/my_couch_or_yours__shareable_ap
.. _`Google Gears`: http://gears.google.com/
.. _Atom: http://en.wikipedia.org/wiki/Atom_(standard)
.. _eyespot: http://eyespot.com/