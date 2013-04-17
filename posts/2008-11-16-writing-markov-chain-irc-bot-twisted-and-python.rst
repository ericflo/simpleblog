---
layout: post
title: "Writing an Markov-Chain IRC Bot with Twisted and Python"
date: 2008-11-16T23:59:34-06:00
comments: false
categories: [Python, Twisted, IRC, Markov Chains, Bot]
published: true
alias: [/blog/post/writing-markov-chain-irc-bot-twisted-and-python]
---

Twisted_ is one of Python's great secret weapons.  It is an absolute workhorse,
allowing for insanely fast network applications to be written with very little
effort.  So let's do what everyone does when they want to learn more about
Twisted: let's write an IRC bot!  This bot is going to use `Markov Chains`_ to
simulate human speech.  For whatever reason, I named this bot "YourMomDotCom".

First let's create a skeleton on top of which the rest of the bot will be
created:

.. code-block:: python

    from twisted.words.protocols import irc
    from twisted.internet import protocol

    class MomBot(irc.IRCClient):
        def _get_nickname(self):
            return self.factory.nickname
        nickname = property(_get_nickname)

        def signedOn(self):
            self.join(self.factory.channel)
            print "Signed on as %s." % (self.nickname,)

        def joined(self, channel):
            print "Joined %s." % (channel,)

        def privmsg(self, user, channel, msg):
            print msg

    class MomBotFactory(protocol.ClientFactory):
        protocol = MomBot

        def __init__(self, channel, nickname='YourMomDotCom'):
            self.channel = channel
            self.nickname = nickname

        def clientConnectionLost(self, connector, reason):
            print "Lost connection (%s), reconnecting." % (reason,)
            connector.connect()

        def clientConnectionFailed(self, connector, reason):
            print "Could not connect: %s" % (reason,)

We've now created an ``IRCClient`` subclass which will hold our application
logic, and we've also written a factory class which will create instances of
that ``MomBot`` client.  Let's tie these together and start the event loop:

.. code-block:: python

    import sys
    from twisted.internet import reactor

    if __name__ == "__main__":
        chan = sys.argv[1]
        reactor.connectTCP('irc.freenode.net', 6667, MomBotFactory('#' + chan))
        reactor.run()

Now already we have a complete working IRC bot.  Right now all it will do is
connect to an IRC channel and echo all of the output to the command line.  Not
bad for how little code we've written. Now all we have to do is implement our
application logic.  Let's first start by creating the 'brain' of our Markov
chain responder, and adding a function to train the brain:

.. code-block:: python

    from collections import defaultdict

    markov = defaultdict(list)
    STOP_WORD = "\n"

    def add_to_brain(msg, chain_length, write_to_file=False):
        if write_to_file:
            f = open('training_text.txt', 'a')
            f.write(msg + '\n')
            f.close()
        buf = [STOP_WORD] * chain_length
        for word in msg.split():
            markov[tuple(buf)].append(word)
            del buf[0]
            buf.append(word)
        markov[tuple(buf)].append(STOP_WORD)

In this, we are creating a defaultdict of lists.  For every n-word sliding
window, the word after that window is appended to the list of possible words.
Here's an image which hopefully depicts better than words how the algorithm
populates the brain:

.. image:: http://media.eflorenzano.com/img/markov.png

But what good is a brain like this if we can't get words back from it.  We're
going to need to write a function to generate sentences from that brain:

.. code-block:: python

    def generate_sentence(msg, chain_length, max_words=10000):
        buf = msg.split()[:chain_length]
        if len(msg.split()) > chain_length:
            message = buf[:]
        else:
            message = []
            for i in xrange(chain_length):
                message.append(random.choice(markov[random.choice(markov.keys())]))
        for i in xrange(max_words):
            try:
                next_word = random.choice(markov[tuple(buf)])
            except IndexError:
                continue
            if next_word == STOP_WORD:
                break
            message.append(next_word)
            del buf[0]
            buf.append(next_word)
        return ' '.join(message)

We start out our seed buffer with the first few words of the message, and if the
message wasn't long enough, we fill the seed buffer with some random words from
the markov's brain.  Then we use the buffer as a key into the markov brain and
randomly pick one of the values as our next word.  Then we slide that buffer
so that the chosen word is now the next word in the buffer (ejecting the oldest
word in the buffer).  If we ever see a stop word, we stop and return the
generated sentence.

Now it's a matter of expanding our bot to take advantage of our markov brain.
The first change we will need to make is to modify the ``MomBotFactory`` to take
more parameters in its ``__init__`` method:

.. code-block:: python

    class MomBotFactory(protocol.ClientFactory):
        protocol = MomBot
    
        def __init__(self, channel, nickname='YourMomDotCom', chain_length=3,
            chattiness=1.0, max_words=10000):
            self.channel = channel
            self.nickname = nickname
            self.chain_length = chain_length
            self.chattiness = chattiness
            self.max_words = max_words
        
        # ...

Now that it has all of that new information, we can add the final bit of
functionality to ``MomBot`` responding using sentences generated from the
markov brain by updating the ``privmsg`` method:

.. code-block:: python

    class MomBot(irc.IRCClient):

        # ...
    
        def privmsg(self, user, channel, msg):
            if not user:
                return
            if self.nickname in msg:
                msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
                prefix = "%s: " % (user.split('!', 1)[0], )
            else:
                prefix = ''
            add_to_brain(msg, self.factory.chain_length, write_to_file=True)
            if prefix or random.random() <= self.factory.chattiness:
                sentence = generate_sentence(msg, self.factory.chain_length,
                    self.factory.max_words)
                if sentence:
                    self.msg(self.factory.channel, prefix + sentence)

If it gets a message from a non-user, we don't care about it, so we just
disregard that message.  Otherwise, if it's a message directed at the bot, we
want to respond to the sending user so we add the user as a prefix to our next
message.  Then we grab a sentence from the markov brain and send it to the
channel.

Not so bad.  Now lets modify our startup portion of the script to re-train the
brain with anything learned during the course of the bot's life.  Here's how
the new script will look:

.. code-block:: python

    if __name__ == "__main__":
        try:
            chan = sys.argv[1]
        except IndexError:
            print "Please specify a channel name."
            print "Example:"
            print "  python yourmomdotcom.py django-hotclub"
        if os.path.exists('training_text.txt'):
            f = open('training_text.txt', 'r')
            for line in f:
                add_to_brain(line, chain_length)
            print 'Brain Reloaded'
            f.close()
        reactor.connectTCP('irc.freenode.net', 6667, MomBotFactory('#' + chan, 
            'YourMomDotCom', 2, chattiness=0.05))
        reactor.run()

I have found personally that, counter-intuitively, a length of **2** seems to
produce the most realistic-looking responses.  We've really accomplished a lot
in a very little amount of code.  Instead of my normal closing remarks, let me
simply close with a snippet of conversation recently had with YourMomDotCom::

    [9:57pm] ericflo: YourMomDotCom: Hello, I'd like to show you off for the readers of my blog.
    [9:57pm] YourMomDotCom: ericflo: Hello, I'd like to do, after checking with another.
    [9:57pm] ericflo: YourMomDotCom: I'm not exactly sure what you mean by that.
    [9:57pm] YourMomDotCom: ericflo: I'm not sure, but I'm in "Easter mode" already I think.
    [9:58pm] ericflo: YourMomDotCom: That's funny since we aren't really very close to easter.
    [9:58pm] YourMomDotCom: ericflo: That's funny since i missed much of a ForeignKey field?
    [9:58pm] ericflo: YourMomDotCom: I miss ForeignKey fields all the time
    [9:58pm] YourMomDotCom: ericflo: I miss that 
    [9:58pm] ericflo: YourMomDotCom: We both agree, then.
    [9:58pm] YourMomDotCom: ericflo: We both agree, then.
    [9:58pm] ericflo: YourMomDotCom: yay!

.. _Twisted: http://twistedmatrix.com/trac/
.. _`Markov Chains`: http://en.wikipedia.org/wiki/Markov_chain