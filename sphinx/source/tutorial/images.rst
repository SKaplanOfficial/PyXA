Working with Images
===================

PyXA uses the :class:`~PyXA.XABase.XAImage` class to provide a standard, convenient way to interact with images stored in files, images created by other PyXA operations, and images managed by applications such as Photos or Image Events. Using this class, you can:

- Load and save images
- Access information about images, such as whether they contain transparent pixels
- Copy images to the clipboard
- Set image attributes such as vibrance and temperature
- Apply filters and distortions
- Create composite images or blend images together using composition filters
- Stitch images together
- Extract text contained in images

The :class:`~PyXA.XABase.XAImage` class aims to simplify complex Objective-C implementations of image manipulation down to just a few lines of code for PyXA users. As a result, creating scripts to operate on images can be done quickly and without needing to understand the underlying mechanisms as work. You can then intuitively utilize images elsewhere in your automation scripts. Some ideas for automation include:

- Download images from an online API, extract text from them, and store the text in a note
- Find images containing a certain word or phrase and sort them into an album in Photos
- Create a mosaic of all images in a particular photo album, or of all images taken in the last year
- Auto-enhance all images stored in a particular folder
- Store images files sent to you in a particular folder immediately after receiving them
- Overlay the songs of a Music playlist onto a mosaic of all the songs' album artworks

...and many more! What will you come up with?

The rest of this page describes the various features of the :class:`~PyXA.XABase.XAImage` class and provides several examples for you to reference.

Loading Images
--------------

To initialize an :class:`~PyXA.XABase.XAImage` object, you provide some kind of reference to an image via the `image_reference` parameter (the first parameter of XAImage's init method). This parameter accepts data in many forms, including: a raw string file path (with any image file extension), a web or filesystem URL, an :class:`~PyXA.XABase.XAPath` or :class:`~PyXA.XABase.XAURL` object, another :class:`~PyXA.XABase.XAImage` object, and any object whose class implements the :class:`~PyXA.XAProtocols.XAImageLike` protocol, such as :class:`~PyXA.apps.PhotosApp.XAPhotosMediaItem`. The code below shows how to use these different kinds of image references.

.. code-block:: python

    import PyXA
    # Load a single image file
    img = PyXA.XAImage("/Users/exampleUser/Desktop/PyXALogoTransparent.png")
    print(img)
    # <PyXA.XABase.XAImage object at 0x104b385b0>

    # Load an image from a web URL
    img = PyXA.XAImage("https://raw.githubusercontent.com/SKaplanOfficial/PyXA/main/docs/_static/assets/PyXALogoTransparent.png")
    img.show_in_preview()

    # Load images from a XAURL or XAPath
    path = PyXA.XAPath("/Users/exampleUser/Desktop/PyXALogoTransparent.png")
    url = PyXA.XAURL("https://raw.githubusercontent.com/SKaplanOfficial/PyXA/main/docs/_static/assets/PyXALogoTransparent.png")
    img1 = PyXA.XAImage(path)
    img2 = PyXA.XAImage(url)

    # Initialize an image from another image
    img1 = PyXA.XAImage("/Users/exampleUser/Desktop/PyXALogoTransparent.png")
    img2 = PyXA.XAImage(img1)

    # Get an image from Photos
    photos = PyXA.Application("Photos")
    img = PyXA.XAImage(photos.media_items().by_title("PyXA Logo"))

Additionally, some apps such as Image Events utilize subclasses of :class:`~PyXA.XABase.XAImage` to afford a more direct connection between their content and the functionality of XAImages. In the case of Image Events, an image opened using :func:`PyXA.apps.ImageEvents.XAImageEventsApplication.open` is an instance of :func:`PyXA.apps.ImageEvents`.XAImageEventsImage`, a subclass of `:class:`~PyXA.XABase.XAImage`, and has access to both XAImage's methods as well as methods specific to the Image Events context.

.. code-block:: python

    import PyXA
    ie = PyXA.Application("Image Events")
    ie_img = ie.open("/Users/steven/Desktop/PyXALogoTransparent.png")

    # Use XAImageEventsImage methods
    profile = ie.profiles().by_name("Generic Gray Profile")
    ie_img.embed_profile(profile)

    # Use XAList methods
    ie_img.pad(50, 50, PyXA.XAColor.black()).rotate(45)
    ie_img.gaussian_blur().bloom().show_in_preview()

You can also use the :func:`~PyXA.XABase.XAImage.open` method to open one or more image files or URLs. When opening multiple images at a time, this method returns an :class:`~PyXA.XABase.XAImageList` object -- more on that later.

Accessing Image Information
---------------------------

.. code-block:: python

    import PyXA
    image = PyXA.XAImage.open("/Users/steven/Desktop/PyXALogoTransparent.png")

    # Check if image has alpha channel
    if image.has_alpha_channel:
        # Check if image contains transparent pixels
        if image.is_opaque:
            print("Image is capable of having transparent pixels, but does not have any right now")
        else:
            print("Image contains transparent pixels")
    else:
        print("Image cannot contain transparent pixels in its current format")

    # Print other attributes
    print(image.color_space_name)
    print(image.size)
    print(image.data)

Modifying Image Attributes
--------------------------

In addition to accessing information attributes, you can use PyXA to concisely set image attributes such as the vibrance, tint, and temperature of an image. The mutable attributes are:

- :attr:`~PyXA.XABase.XAImage.gamma`
- :attr:`~PyXA.XABase.XAImage.vibrance`
- :attr:`~PyXA.XABase.XAImage.tint`
- :attr:`~PyXA.XABase.XAImage.temperature`
- :attr:`~PyXA.XABase.XAImage.white_point`
- :attr:`~PyXA.XABase.XAImage.highlight`
- :attr:`~PyXA.XABase.XAImage.shadow`

.. code-block:: python

    import PyXA
    image = PyXA.XAImage.open("/Users/steven/Downloads/Owl.png")
    image.vibrance = 0.1
    image.highlight = 0
    image.shadow = 1
    image.tint = 200
    image.temperature = 12000
    image.gamma = 10
    image.show_in_preview()

Basics of Image Manipulation
----------------------------

In addition to modifiable attributes, PyXA provides several method for basic image manipulation, including: :func:`~PyXA.XABase.XAImage.flip_horizontally`, :func:`~PyXA.XABase.XAImage.flip_vertically`, :func:`~PyXA.XABase.XAImage.rotate`, :func:`~PyXA.XABase.XAImage.scale`, :func:`~PyXA.XABase.XAImage.crop`, and :func:`~PyXA.XABase.XAImage.pad`.

.. code-block:: python

    import PyXA

    # Apply individual modifications
    image = PyXA.XAImage("/Users/steven/Desktop/cat2.jpeg")
    image.crop((600, 600))
    image.scale(2, 2)
    image.show_in_preview()

    # Apply modifications using method chaining
    image.pad(pad_color=PyXA.XAColor.red()).rotate(45).flip_horizontally()
    image.show_in_preview()

Applying Filters
----------------

PyXA provides easy-access to several common image filters that might be useful for automation workflows; for more advanced use cases, a dedicated image manipulation library is recommended. The provided filter methods are:

- :func:`~PyXA.XABase.XAImage.bloom`
- :func:`~PyXA.XABase.XAImage.crystallize`
- :func:`~PyXA.XABase.XAImage.comic`
- :func:`~PyXA.XABase.XAImage.depth_of_field`
- :func:`~PyXA.XABase.XAImage.edges`
- :func:`~PyXA.XABase.XAImage.gaussian_blur`
- :func:`~PyXA.XABase.XAImage.invert`
- :func:`~PyXA.XABase.XAImage.monochrome`
- :func:`~PyXA.XABase.XAImage.outline`
- :func:`~PyXA.XABase.XAImage.pixellate`
- :func:`~PyXA.XABase.XAImage.pointillize`
- :func:`~PyXA.XABase.XAImage.reduce_noise`
- :func:`~PyXA.XABase.XAImage.sepia`
- :func:`~PyXA.XABase.XAImage.vignette`

.. code-block:: python

    import PyXA
    image = PyXA.XAImage("/Users/steven/Desktop/cat2.jpeg")
    image.pixellate().sepia().vignette(5).show_in_preview()

Adding Distortions
------------------

In addition to filters, PyXA provided a few methods for adding distortions to images. These methods include :func:`~PyXA.XABase.XAImage.bump`, :func:`~PyXA.XABase.XAImage.pinch`, and :func:`~PyXA.XABase.XAImage.twirl`.

.. code-block:: python

    import PyXA
    image = PyXA.XAImage("/Users/steven/Downloads/Owl.png")
    image.bump(radius=800, curvature=1).pinch((871, 871), intensity=1).twirl().show_in_preview()

Composite Operations
--------------------

PyXA currently supports four composite operations (operations that merge many images into a single, composite image): :func:`~PyXA.XABase.XAImageList.horizontal_stitch`, :func:`~PyXA.XABase.XAImageList.vertical_stitch`, :func:`~PyXA.XABase.XAImageList.additive_composition`, and :func:`~PyXA.XABase.XAImageList.subtractive_composition`. The first two are image concatenation operations which "stitch" together a series of images either vertically or horizontally, one on top of or next to another, to form a single combined imaged, while the other two produce an image by overlaying images and applying a specific blend filter.

The composite image operations noted above are methods of the :class:`~PyXA.XABase.XAImageList` class.

.. code-block:: python

    import PyXA
    images = PyXA.XAImage.open("/Users/steven/Downloads/Owl.png", "/Users/steven/Desktop/PyXALogoTransparent.png")

    images.additive_composition().show_in_preview()
    images.subtractive_composition().show_in_preview()
    images.horizontal_stitch().show_in_preview()
    images.vertical_stitch().show_in_preview()

Text Extraction
---------------

With PyXA, you can extract text from images using just one method call. When working with a single :class:`~PyXA.XABase.XAImage` object , calling the object's :func:`~PyXA.XABase.XAImage.extract_text` method will return a list of all text contained within the image, separated by newline characters. Likewise, when calling :func:`~PyXA.XABase.XAImageList.extract_text` on an :class:`~PyXA.XABase.XAImageList` object, you will get a list of lists of strings, with each image's text organized into its own entry.

.. code-block:: python

    import PyXA
    # Extract text from one image
    image = PyXA.XAImage("/Users/steven/Desktop/handwritingImage.png")
    print(images.extract_text())
    # ["This is a handwritten note"]

    # Extract text from multiple images at a time
    images = PyXA.XAImage.open("/Users/steven/Desktop/codeImage.png", "/Users/steven/Desktop/handwritingImage.png", "/Users/steven/Desktop/signImage.jpeg")
    texts = images.extract_text()
    print(texts)
    # [
    #   ["import PyXA", 'PyXA.Application("Music").play()'],
    #   ["This is a handwritten note"],
    #   ["KEEP", "RIGHT"],
    # ]

This functionality allows you to quickly and easily obtain the text within an image, then use that text elsewhere in your automation scripts. For example, the code below rotates or scales images according to the text found within them:

.. code-block:: python

    import PyXA
    import os

    sample_folder = "/Users/steven/Desktop/samples/"
    output_folder = "/Users/steven/Desktop/output/"

    # Create output folder if necessary
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # Loop through source images
    for index, sample in enumerate(os.listdir(sample_folder)):
        print(f"Analyzing sample {index + 1}...")
        image = PyXA.XAImage(sample_folder + sample)

        # Extract image text -- each image source is known to have two lines
        image_text = image.extract_text()
        operation = image_text[0]
        arg = int(image_text[1])

        # Apply appropriate operation
        if operation == "rotate":
            image.rotate(arg)
        elif operation == "scale":
            image.scale(arg, arg)

        # Save modified image to file in output folder
        print("\tWriting to disk...")
        image.save(output_folder + sample)

Working with Lists of Images
----------------------------

As with many other PyXA classes, :class:`~PyXA.XABase.XAImage` has an associated :class:`~PyXA.XABase.XAImageList` class that provides both convenience and performance improvements over standard lists. For example, :func:`PyXA.XABase.XAImageList.flip_horizontally` method performs over twice as fast as iterating over the same size list of individual  :class:`PyXA.XABase.XAImage` objects and calling the  :func:`PyXA.XABase.XAImage.flip_horizontally` method on each list item, as seen in the example code below:

.. code-block:: python

    import PyXA
    from timeit import timeit

    def without_xalist():
        images = [PyXA.XAImage("/Users/steven/Desktop/dog1.JPG"), PyXA.XAImage("/Users/steven/Desktop/dog1.JPG"), PyXA.XAImage("/Users/steven/Desktop/dog1.JPG")]
        flipped_images = []
        for image in images:
            flipped_images.append(image.flip_vertically())
        return flipped_images

    def with_xalist():
        images = PyXA.XAImage.open("/Users/steven/Desktop/dog1.JPG", "/Users/steven/Desktop/dog1.JPG", "/Users/steven/Desktop/dog1.JPG")
        flipped_images = images.flip_vertically()
        return flipped_images

    t1 = timeit(without_xalist, number=100)
    t2 = timeit(with_xalist, number=100)
    print("Non-XAList avg over 100 trials:", t1 / 50.0)
    print("XAList avg over 100 trials:", t2 / 50.0 )
    # Non-XAList avg over 100 trials: 1.53993887584
    # XAList avg over 100 trials: 0.6404187591799999

A relationship exists for all of the :class:`~PyXA.XABase.XAImage` and :class:`~PyXA.XABase.XAImageList` methods. Thus, generally speaking, you'll want to make use of :class:`~PyXA.XABase.XAImageList` objects any time you work with several or more images.