slimage
=======

A tool for managing softlayer images.

Setup
=====

After installing slimage you'll need to setup the softlayer client credentials.
This is normally done by creating a ~/.softlayer file, but you can read the
full details here:

https://softlayer-python.readthedocs.io/en/latest/config_file.html

After you set that up you'll also need your IBM Cloud Swift username. This can
be found when looking at the softlayer/IBM Cloud dashboard under the object
storage account you want to use.

With these things setup you can initialize a SLImages() object to handle
interacting with imges. For example::

    from slimage import sl_api

    swift_username = IBM1231-5@1234_username
    slimage = sl_api.SLImages(swift_username)

You can optionally specify a different swift public authentication endpoint
by using the ``swift_auth_url`` kwarg. By default it uses the dal05 region's
endpoint. If you need to change this the endpoint will be specified in your
swift credentials under the web UI.

Usage
=====

To boot an image first you need to upload that into the swift object storage.
You can do this with the SLImages.upload_file() method. This method takes 3
pieces of information to be used, ``path`` which is the path to your image file,
``name`` which is the name to use for your image object. In most cases you
just want this to be the file name. To make this work as an image. You must
make sure you're using a VHD image format and that the name ends with *.vhd*.
If you have an image of another type you can use the:
slimage.img_convert.covert_to_vhd() function to convert the image into a vhd
format. The last piece of required information is the ``container`` which is the
container you will use to store the object in swift. For example::

    from slimage import sl_api

    swift_username = IBM1231-5@1234_username
    slimage_client = sl_api.SLImages(swift_username)
    my_image = '/path/to/my_image.vhd'
    name = 'my_image.vhd'
    container = 'images'
    slimage_client.upload_file(my_image, name, container)

Then once your image upload completes you can create a softlayer image template
from that. To do this you can leverage the SLImages.create_image() function.
To do this you'll need to provide a few pieces of information. First is a name
for the image, this can be any descriptive name you want to use. Then you
provide the swift information for where the object lives in swift, the
object name, the container, and the cluster. With this information you can
optionally provide a plain text description of the image with the ``desc`` kwarg
and also specify an os_code for the image with the ``os_type`` kwarg. Note
if you don't specify an os_type it will default to using DEBIAN_8_64, which
doesn't have any licensing associated with it.

Putting this all together you'd get something like::

    from slimage import sl_api

    swift_username = IBM1231-5@1234_username
    slimage_client = sl_api.SLImages(swift_username)
    my_image = '/path/to/my_image.vhd'
    name = 'my_image.vhd'
    container = 'images'
    slimage_client.upload_file(my_image, name, container)
    image = slimage_client.create_image('My-Special-Image, name, container,
                                        cluster='dal05',
                                        desc='My personal image')

Which will create a new image name My-Special-Image.

Then you can use ``image['id']`` as the image_id filed in a create server
request. There is a create_server function in the SLImages class to do this,
but it likely doesn't work and hasn't been tested yet. One other thing to note
here is that if your image uses cloud-init there is a metadata flag for
indicating that. As of yet I haven't found a method in the API to set this flag
so you'll have to manually update the image's metadata to say it uses
cloud-init. If you don't have this set the image will not boot.

.. note:: Softlayer's virtual server service is very finicky about what kind
    of images you can boot. Even if the boot works and you're able to access it
    the softlayer support team watches things closely and if they detect any
    anomolies in the boot process they will likely delete your server and make
    the uploaded image inactive. Refer to softlayer support for more information
    on this.
