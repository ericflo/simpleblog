---
layout: post
title: "Why node.js disappoints me"
date: 2010-09-27T03:23:47-05:00
comments: false
categories: [Javascript, Node, Programming]
published: true
alias: [/blog/post/why-node-disappoints-me]
---

`Node.js`_ is currently at the center of a huge cyclone of hype.  At this point it's clear that Node is going to be a major player in the next few years of web development.  It's no wonder, either!  It represents a fresh start, one with no legacy synchronous baggage in our increasingly asynchronous, increasingly real-time web. And it's accessible to anyone who's written JavaScript (read: all web developers.)

Oh, and those benchmarks!  Compared trivially to the currently popular web technologies, it seems an obvious leap forward.

Yet one of Node's advantages that you'll hear repeated again and again by its proponents is that you can now code in One Language, and you won't have to deal with the cognitive load of context switching between different languages.  Especially as ORMs and NoSQL continue to rise in popularity, there's no need to even deal with SQL. At the end of the day you're writing JavaScript, HTML, and CSS, and that's it.

Seeing this happen with all of these pieces falling into place--a fresh start with a unified language--I started to get excited.  This would change the way we thought about our web code.  The frontend is the backend is the query language is the storage layer is JavaScript!  It's a revolution.

And then I saw what people did with this opportunity.  They effectively ported Sinatra/Django/Rails to JavaScript--and did it in such a way that it would only run on the server, with a specific feature set of JavaScript that only Node can reasonably understand.

Not exactly the revolution I was hoping for.

Instead of coding in one language, we're actually coding in two. One is the subset JavaScript that can be run in all browsers, and another is the set of JavaScript that can be run by Node.  Knowing the difference between the two languages and context switching between them is simply a required skill.

You know what would be awesome? If we wrote our libraries so that they could run either on the server or on the client, and they did so in a transparent way.  Maybe it would help to give a concrete example of how this could be awesome.  Let's talk about HTML templating.

Imagine a framework where the first page-load was always rendered server-side, meaning the client gets a single fully-rendered page.  Then for desktop browsers, browsing around the site just made calls to API endpoints returning JSON or XML, and the client rendered the templates for the changed portions of the page.  For mobile browsers with less power or for search engines, the rendering would always be done on the server.  Imagine that the templating library could record some key metrics to determine how long things were taking to render, and dynamically switch between rendering on the server and client based on server load or client speed.

Imagine a case where a back-end service fails temporarily.  In this case the rendering of that particular component could be deferred, the browser could be told to poll a resource.  When the back-end service is recovered, it could send the data for the client to render on its own.

How awesome would that be?

It's not just HTML templating, either.  This same principle could be applied to any number of things: URL routing, form validation, hell even most application logic could be done using this style.

But it's going to take discipline.  Instead of reaching for those fancy V8 features, code will need to be written in a strict subset of the JavaScript that's available.  Maybe Node could detect incompatible code and throw warnings, that would be cool.

I just really hope that someday we stop re-inventing the same exact wheel, and instead build something substantially different and better.

.. _`Node.js`: http://nodejs.org/