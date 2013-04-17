---
layout: post
title: "Writing a Gallery App in Django, Part I"
date: 2006-12-19T22:28:17-06:00
comments: false
categories: [Gallery, Programming, Django]
published: true
alias: [/blog/post/writing-gallery-app-part-one]
---

One thing that I see the need for on almost every site is a place to put images.  Whether it's a band website, a personal homepage, or a school newspaper, there will be a need for a photo gallery.  The easy way to do that is to use an open source package available already like Gallery2.  But that's written in PHP and it won't integrate easily with the rest of your site--especially if you use Django as the framework for the rest of your site.

The solution: write a gallery application for use in your website.  At first it may seem like a daunting task to create, but as I've found out, it can be quite easy.  My implementation is not completely up and running yet, but that's due to design issues with the rest of the site, not the photo gallery app itself.  With no further adieu, let's dive in and see how this can work.

.. code-block:: python

    class Album(models.Model):
        name = models.CharField(maxlength=128)
        slug = models.SlugField(prepopulate_from=("name",))
        summary = models.TextField()
        date_created = models.DateTimeField(auto_now_add=True)
        date_modified = models.DateTimeField(auto_now=True)

As you can see, this is the Album object which contains information about a set of associated photos.  But wait, we don't have photos created yet!  Let's do that now.

.. code-block:: python

    class Photo(models.Model):
        title = models.CharField(maxlength=256)
        summary = models.TextField(blank=True, null=True)
        date_created = models.DateTimeField(auto_now_add=True)
        date_modified = models.DateTimeField(auto_now=True)
        image = models.ImageField(upload_to='photos/%Y/%m')
        album = models.ForeignKey(Album)
        is_cover_photo = models.BooleanField()

Ok so now we have albums which have photos, and photos have a lot of information like a file which contains an image, a title, and a summary.

Now that we have these objects, we have some choices to make.  The images need to be resized into medium and small images for display on the list and detail pages, respectively.  This can be done several ways:

1. Use the HTML width and height attributes to resize the images.
2. Create a Django view with width and height parameters to both resize and serve the images.  (Lazy computation)
3. Resize the images on upload and store them to disk.  (Upfront computation)

The first way is not optimal for two reasons.  Firstly each picture must be downloaded in it's entirety.  This is inefficient and could upset people with less bandwidth or bandwidth limits.  Secondly, when most browsers resize images, they do so using poor quality filters, resulting in a low quality representation of an image.

The second way is the most flexible, since the height and the width can be changed in a template or in a view and the resized images will change accordingly.  However, there is more on-the-fly computation with this way, possibly increasing page load times.  Also, Django is not designed to be used to serve binary files directly, so there could be unforseen consequences with handling a large number of photos this way.

The third way is less flexible, but it has one key advantage: it's fast.  Since the computation is done on upload, Apache or any other http media server can be used instead, completely removing the need to use the Django framework at all.  Let's implement it this way.

First, we'll need to overload the save function of the Photo model:

.. code-block:: python

    def save(self):
        if self.is_cover_photo:
            other_cover_photo = Photo.objects.filter(album=self.album).filter(is_cover_photo = True)
            for photo in other_cover_photo:
                photo.is_cover_photo = False
                photo.save()
        filename = self.get_image_filename()
        if not filename == '':
            img = Image.open(filename)
            img.thumbnail((512,512), Image.ANTIALIAS)
            img.save(self.get_medium_filename())
            img.thumbnail((150,150), Image.ANTIALIAS)
            img.save(self.get_small_filename())
        super(Photo, self).save()

Before I talk about the thumbnailing aspect of this function, I'd like to briefly explain what's going on with the cover_photo aspect of Photo objects.  Each Album has a cover photo, so if the Album needs to be represented, it can be represented by one special photo.  This is just part of the way that I have designed my object, and can easily be removed.  However, there is a small bit of obligatory boilerplate code in this save function which sets any other is_cover_photo attributes to False if necessary.  (There can only be one cover photo per album, after all).  I'll come back to dealing with cover photos later.

First off, the ``if not filename == ''`` statement is needed because save is sometimes called with no image data, and that can and will throw exceptions if PIL is used on a None object.  Then, it resizes a medium-sized (512px by 512px) image and saves it to a location provided by get_medium_filename.  I leave it to you to define your own get_medium_filename and get_small_filename with your own naming convention.  I followed Flickr's example of an underscore followed by an argument (image001.jpg becomes image001_m.jpg for medium and image001_s.jpg for small).  Finally, this method must call the it's parent save method so that all of the other attributes are saved correctly.

Now that we've overloaded the save functionality, we are going to have a problem with deletion.  Django will automatically delete the original image, but the resized thumbnails will be left on the disk forever.  This is not a huge problem, but we don't want that to happen anyways.  So let's take care of that by also overloading the delete function of Photo's model:

.. code-block:: python

    def delete(self):
        filename = self.get_image_filename()
        try:
            os.remove(self.get_medium_filename())
            os.remove(self.get_small_filename())
        except:
            pass
        super(Photo, self).delete()

Simply put, it deletes the thumbnail files and then calls it's parent's delete, which will in turn delete it's original file.

Aside from creating some optional helper functions like ``get_small_image_url`` and/or ``get_medium_image_url``, there's not much more to be done with the Photo model.  What can be done still, however, is in Album.  We now have zero or one cover photos for each Album, but it's going to be tricky to query for this each time, so let's create a function in Album to help us retrieve the associated cover_photo Photo object:

.. code-block:: python

    def get_cover_photo(self):
        if self.photo_set.filter(is_cover_photo=True).count() > 0:
            return self.photo_set.filter(is_cover_photo=True)[0]
        elif self.photo_set.all().count() > 0:
            return self.photo_set.all()[0]
        else:
            return None

That is, if the Album has a photo with ``is_cover_photo == True``, then grab it, otherwise grab the first image.  If there are no images in the album, return None.  That's it for the models.  Easy, huh?  Just run ``manage.py syncdb``, and let Django do the heavy lifting for you.

That's all for part one of this series on writing a gallery application with Django.  Next up: writing the views, urlconfs, and putting it all together.  Templating will be left up to you, since there are so many ways to display this information, but some examples will be given to point you in the right direction.

Note to purists:  I know that some of the functionality that is being implemented as helper functions in the models would be better implemented as custom template tags, but I find it easier to take a less philosophical stance on the "right" way to do things and sometimes do what's more practical.  In this case, writing model functions is a much easier solution than creating completely new template tags.  In either case, moving to a new site will require a rewrite, so I'm not even convinced that it hurts reusability.