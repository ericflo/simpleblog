---
layout: post
title: "Using Twitter's iOS5 Integration for Single Sign-On"
date: 2012-04-18T16:34:47-06:00
comments: false
categories: [Login, Programming, Registration, Sign-On, Twitter, iOS]
published: true
---

Apple has included integration with Twitter in iOS5, which can be really handy to allow your users to easily tweet or log in. The only problem is that, as far as documentation of this feature is concerned, you're largely on your own. This blog post is an attempt to correct that, at least in the case of sign-on.

Add the Twitter and Accounts libraries to your project
------------------------------------------------------

Click on your project file, and then on your build target. Make sure you're on the "build phases" tab. Under the "Link Binary With Libraries" section, click the plus symbol to the bottom left, and search for ``Accounts.framework`` and add it. Then do the same for ``Twitter.framework``. This will link all of the necessary libraries into your project so that we can use the Twitter integration.

Requesting access to a user's twitter account
---------------------------------------------

The first thing to do when you want to let a user sign-on with Twitter is to create a long-lived (save it as an instance variable, for example) instance of ACAccountStore and request access to the Twitter accounts contained within:

.. code-block:: objc

    ACAccountStore *store = [[ACAccountStore alloc] init]; // Long-lived
    ACAccountType *twitterType = [store accountTypeWithAccountTypeIdentifier:ACAccountTypeIdentifierTwitter];
    [store requestAccessToAccountsWithType:twitterType withCompletionHandler:^(BOOL granted, NSError *error) {
        if(granted) {
            // Access has been granted, now we can access the accounts
        }
        // Handle any error state here as you wish
    }];

What do we do once we have access to the accounts? Well, we get a list of 'em. If they don't have any accounts, then we can show a dialog asking them to connect one in the iOS settings app:

.. code-block:: objc

    // Remember that twitterType was instantiated above
    NSArray *twitterAccounts = [store accountsWithType:twitterType];

    // If there are no accounts, we need to pop up an alert
    if(twitterAccounts != nil && [twitterAccounts count] == 0) {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"No Twitter Accounts"
                                                        message:@"There are no Twitter accounts configured. You can add or create a Twitter account in Settings."
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
        [alert release];
    } else {
        ACAccount *account = [twitterAccounts objectAtIndex:0];
        // Do something with their Twitter account
    }

Now what?
---------

Well, now you have an access token to read some information about the user from their Twitter stream. The vast majority of apps will just want to grab the user's basic info to get things like a username, real name, and maybe their location. Here's how that would look:

.. code-block:: objc

    NSURL *url = [NSURL URLWithString:@"http://api.twitter.com/1/account/verify_credentials.json"];
    TWRequest *req = [[TWRequest alloc] initWithURL:url
                                         parameters:nil
                                      requestMethod:TWRequestMethodGET];

    // Important: attach the user's Twitter ACAccount object to the request
    req.account = account;

    [req performRequestWithHandler:^(NSData *responseData,
                                     NSHTTPURLResponse *urlResponse,
                                     NSError *error) {

        // If there was an error making the request, display a message to the user
        if(error != nil) {
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Twitter Error"
                                                            message:@"There was an error talking to Twitter. Please try again later."
                                                           delegate:nil
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles:nil];
            [alert show];
            [alert release];
            return;
        }

        // Parse the JSON response
        NSError *jsonError = nil;
        id resp = [NSJSONSerialization JSONObjectWithData:responseData
                                                          options:0
                                                            error:&jsonError];

        // If there was an error decoding the JSON, display a message to the user
        if(jsonError != nil) {
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Twitter Error"
                                                            message:@"Twitter is not acting properly right now. Please try again later."
                                                           delegate:nil
                                                  cancelButtonTitle:@"OK"
                                                  otherButtonTitles:nil];
            [alert show];
            [alert release];
            return;
        }

        NSString *screenName = [resp objectForKey:@"screen_name"];
        NSString *fullName = [resp objectForKey:@"name"];
        NSString *location = [resp objectForKey:@"location"];

        // Make sure to perform our operation back on the main thread
        dispatch_async(dispatch_get_main_queue(), ^{
            // Do something with the fetched data
        });
    }];

Most of the code here is actually error handling code. The meat of what we're doing is simply fetching the user's credentials from Twitter, parsing the JSON, and doing something with it. (What exactly you want to do with the username and name data is left as an excercise for the reader.)

That's it?
----------

Yep, that's it. You should be able to implement Twitter sign-on for your app with the simple code I've shown here. The only bummer is the case when the user doesn't have a Twitter account registered. We're `not allowed`_ to help the user out by sending them to the Settings app. All we can do is tell users to go there and hope they can figure it out.

Any other tips or tricks you have for implementing sign-on with Twitter on iOS? Be sure to `tweet me`_ about it!

P.S. If you're building mobile apps, my startup `clutch.io`_ can help you build and iterate faster on them. Check us out :)

.. _`not allowed`: http://stackoverflow.com/questions/10055853/opening-ios-settings-preferences
.. _`tweet me`: http://twitter.com/ericflo
.. _`clutch.io`: https://clutch.io/