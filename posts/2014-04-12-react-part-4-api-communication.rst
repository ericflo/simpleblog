---
layout: post
title: "Server/Client With React, Part 4: API Communication"
date: 2014-04-12T12:29:00-08:00
comments: false
categories: [React, ReactJS, Programming, Server, Client, Javascript]
published: false
---

There is one thing that you'll need to do: build your app in two parts.  One
part will be the API and another part will be the frontend, which can be
rendered either on the server or on the client.  This may seem like a burden,
but in my experience, it's better to start this way anyway, because it can be
*really hard* to split a monolithic codebase into services later.  Plus, if you
want to build a mobile app, now you've already got an API layer.

For the purposes of this post, let's assume that you already have an API that
talks to your database and takes care of business logic.  In our example app's
case, the API looks like this::

    GET    /api/v1/users/current.json
    Requests the current user, or null if the current user is not authed.

    POST   /api/v1/users/twitter.json
    Submit a Twitter access token and secret to create a user account for the
    requesting client.

    GET    /api/v1/timelines/home.json
    Requests a list of IRLMoji that makes up the home timeline.
    
    GET    /api/v1/timelines/user/username/:username.json
    Requests a list of IRLMoji posted by the given username.
    
    GET    /api/v1/timelines/emoji/:emoji.json
    Requests a list of IRLMoji posted about a particular emoji character.
    
    GET    /api/v1/irlmoji/id/:irlmojiId.json
    Requests a particular IRLMoji by id, including the list of people who
    have hearted that IRLMoji.
    
    DELETE /api/v1/irlmoji/id/:irlmojiId.json
    Deletes the IRLMoji by id, as long as you're the one who posted it.

    POST   /api/v1/irlmoji.json
    Creates a new IRLMoji.

    POST   /api/v1/irlmoji/id/:irlmojiId/heart.json
    Toggles whether a heart is placed on the indicated emoji for the
    requesting user.

    POST   /upload
    Receives and stores image uploads.

If you're interested in checking out more of the API code, it's all open source
`here`_, and I'd suggest starting with the `server.go`_ file.

.. _`here`: https://github.com/ericflo/irlmoji/tree/master/src
.. _`server.go`: https://github.com/ericflo/irlmoji/blob/master/src/server.go#L113