---
layout: post
title: "Information has a Long Way to Go"
date: 2007-07-31T22:29:33-05:00
comments: false
categories: [Python, Secret Project, Musicbrainz, amazon, iTunes]
published: true
alias: [/blog/post/information-has-long-way-go]
---

I don't know how Google_ manages to `do it`_!  They've linked music track/artist/album to online music vendors, a deceivingly simple-sounding task which has been the bane of my existence for the last two weeks.

Let's start with two of the big players:

iTunes
------

iTunes has a terrible API: You go to `iTunes Link Maker`_ and type in the keywords of your choice.  You can come up with a programmatic way to access this but it involves parsing invalid HTML.

Amazon
------

Amazon's API is a good programmatic interface to its own internal service, but unfortunately that service is TERRIBLE.  Take this_, for example: a CD from a wonderful band called Rodrigo y Gabriela.  One of the songs on it is named "Ixtapa", so let's do a search for "Ixtapa Rodrigo y Gabriela."  Makes sense, right?  Apparently not to Amazon's search.  In fact, amazon's search really has no concept of the song.  It's not something that they sell. Amazon knows all about album titles and artists, but not about the song itself.  This renders it useless for linking song to vendor!

But what about open source?

MusicBrainz
-----------

So the next thing that I try is using MusicBrainz_, an open source database of music metadata, which seems to have Amazon.com linking information built right in.  However, reading through the wiki, for hours, and hours, and hours, is not fun.  They have bits and pieces from all different times of the project's lifecycle, most of which is irrelevant.  But after a while I find out that to get access to the web services, you either need to limit your requests to 1 per second (unacceptable in my case), or you have to set up your own MusicBrainz server.  OK, let's do that!

Oh wait, they forgot to mention that it's the most rediculous dependency-ridden piece of bloatware ever.  It's so bad that they don't even really have a guide on how to set it up--they've given up and just created a virtual machine for people to download.  OK, well fine, let's download that and go from there.  What's this?  There's more setup?  Apparently so, because I had to leave my computer to import data and compute indexes for 3 days straight.  

Finally, finally, I am ready to start accessing that music -> amazon.com data, when I notice something: Non-Commercial license.  After all of this, the AMAZON SPECIFIC PORTION ONLY is licensed differently, and I cannot use it.  I am disappointed with this service, to say the least.  MusicBrainz needs a major overhaul in its software dependencies (Hint: Use Python, it's got batteries included.)  It also needs to take a serious look at its licensing scheme.  If it can address these two things, it will be much further along in its goal to make a great community database.

Information has a long way to go.  Music metadata and the ability to link to different music vendors should be ubiquitous and available in a standard way.  Nobody is benefiting by putting a `lock and key`_ on this sort of data.  The people who really lose, in the end, is the music vendors who get ultimately less sales.  Hopefully someday soon they see the light, and fight to make this information accessible.

.. _Google: http://www.google.com/musica?aid=CthfGxkPMTB
.. _`do it`: http://www.google.com/musicl?lid=1SpDWykV7NL&aid=CthfGxkPMTB
.. _`iTunes Link Maker`: http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/itmsLinkMaker
.. _this: http://www.amazon.com/Rodrigo-y-Gabriela-Bonus-DVD/dp/B000HKDEE2/ref=pd_bbs_sr_1/102-5025068-6051344?ie=UTF8&s=music&qid=1185941115&sr=8-1
.. _MusicBrainz: http://musicbrainz.org/
.. _`lock and key`: http://www.gracenote.com/