---
layout: post
title: "An idea for an alternative Android hybrid native/html approach"
date: 2014-04-12T12:29:00-08:00
comments: false
categories: [React, ReactJS, Programming, Android]
published: true
---

I've been doing Android development again recently, and right after doing so
much work using React.js, it's made me really aware of how we handle state and
state transitions.  The way React handles it is handy and I was thinking, it
would be nice if there were something in the Android world to help manage that.

Then I went to edit one of my layout XML files and had an epiphany: React.js
renders out HTML to be interpreted by the browser, but these layout XML files
aren't very different at all from HTML.  If we could just write a diff engine
on the Android side to apply view hierarchy changes, we could render fully
native widgets with React.js components.

Here's an example layout XML file that could come from some kind of funny
images app, where it shows an image alongside some text representing that
image's 'tags':

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:paddingLeft="64dp"
        android:paddingRight="64dp"
        android:paddingTop="4dp"
        android:paddingBottom="16dp">
        <ImageView
          android:id="@+id/image"
          android:layout_width="match_parent"
          android:layout_height="wrap_content"
          android:scaleType="centerCrop" />
        <TextView
          android:id="@+id/tags"
          android:layout_width="match_parent"
          android:layout_height="wrap_content"
          android:layout_below="@id/image"
          android:gravity="center" />
    </RelativeLayout>

Android developers write Java classes which inflate this XML, attach to the
subviews it cares about ('image' and 'tags', in this case) and set the correct
text and image bitmaps.  Here's a simple version of what that looks like:

.. code-block:: java

  public class FunnyImage extendds RelativeLayout {
    private ImageView mImage;
    private TextView mTags;

    public FunnyImage(Context context) {
      super(context);
      final LayoutInflater inflater = (LayoutInflater)
        context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
      inflater.inflate(R.layout.funny_image, this, true);
      mImage = (ImageView) findViewById(R.id.image);
      mTags = (TextView) findViewById(R.id.tags);
    }

    public void setTags(String tags) {
      mTags.setText(tags);
    }

    public void setImageBitmap(Bitmap bitmap) {
      mImage.setImageBitmap(bitmap);
    }
  }

What if we could write this same thing in React.js style?

.. code-block:: as

  var FunnyImage = React.createComponent({
    render: function() {
      return (
        <RelativeLayout
          layoutWidth="match_parent"
          layoutHeight="match_parent"
          paddingLeft="64dp"
          paddingRight="64dp"
          paddingTop="4dp"
          paddingBottom="16dp">
          <ImageView
            id="@+id/image"
            layoutWidth="match_parent"
            layoutHeight="wrap_content"
            scaleType="centerCrop"
            src={this.props.image.bitmap} />
          <TextView
            layoutWidth="match_parent"
            layoutHeight="wrap_content"
            layoutBelow="@id/image"
            gravity="center"
            text={this.props.image.tags} />
        </RelativeLayout>
      );
    }
  });

I quite like this declarative style.  But we haven't really accomplished much
here yet.  How about we take it further, and take a URL and load a bitmap,
updating the state and using a loading drawable in the meantime:

.. code-block:: as

  var FunnyImage = React.createComponent({
    getInitialData: function() {
      return {bitmap: null};
    },

    componentDidMount: function() {
      HttpUtils.getImageBitmap(this.props.image.url, this.handleBitmapLoaded);
    },

    handleBitmapLoaded: function(error, bitmap) {
      this.setState({bitmap: bitmap});
    },

    getLoadingDrawable: function() {
      return ResourceUtils.getDrawable(this.props.loading);
    },

    render: function() {
      return (
        <RelativeLayout
          layoutWidth="match_parent"
          layoutHeight="match_parent"
          paddingLeft="64dp"
          paddingRight="64dp"
          paddingTop="4dp"
          paddingBottom="16dp">
          <ImageView
            id="@+id/image"
            layoutWidth="match_parent"
            layoutHeight="wrap_content"
            scaleType="centerCrop"
            src={this.state.bitmap || this.getLoadingDrawable()} />
          <TextView
            layoutWidth="match_parent"
            layoutHeight="wrap_content"
            layoutBelow="@id/image"
            gravity="center"
            text={this.props.image.tags} />
        </RelativeLayout>
      );
    }
  });

Let's pull it all together and create an app that fetches these images from
a public data feed:

.. code-block:: as

  var FunnyImages = React.createComponent({
    getInitialData: function() {
      return {images: []};
    },

    componentDidMount: function() {
      HttpUtils.getJSON('http://puppygifs.net/api/read/json',
        this.handleImagesLoaded);
    },

    handleImagesLoaded: function(error, data) {
      if (error) {
        return AlertDialog.show('Could not fetch puppies: ' + error);
      }
      var images = [];
      data.posts.forEach(function(post) {
        var image = post['photo-url-500'];
        if (image) {
          images.push({url: image, tags: post.tags.join(', ')});
        }
      });
      this.setState({images: images});
    },

    render: function() {
      return (
        <RelativeLayout
          layoutWidth="match_parent"
          layoutHeight="match_parent">
          {this.state.images.forEach(function(image) {
            return (
              <FunnyImage
                key={image.url}
                image={image}
                loading="@drawable/loading" />;
            );
          })}
        </RelativeLayout>
      );
    }
  });

Alas this is it for now.  I haven't written that diff engine to prove this is
even possible.  Hopefully on a rainy day I'll have a chance to hack on it and
see whether there's merit.  But for now, I just had to get the idea out of my
brain and at least into words and pseudocode, and to get feedback.  Am I off my
rocker here, or does this sound genuinely cool?