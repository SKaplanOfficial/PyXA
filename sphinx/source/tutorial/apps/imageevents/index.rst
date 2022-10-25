Image Events Module Overview
============================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA supports the full scripting dictionary for Image Events, and some additional image manipulation features have been implemented using Objective-C APIs.

Image Events Tutorials
######################

Tutorial 1 - Basic Image-Related Tasks
*************************************

Reading Image Properties
------------------------

Similar to many other PyXA classes, the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class provides several convenient ways to access various attributes (or properties) of images. To get an overview of all properties, you can access the :attribute:`~PyXA.apps.ImageEvents.XAImageEventsImage.properties` attribute. This will provide a dictionary containing many details, with elements elevated to PyXA objects or types where appropriate.

.. code-block:: python

    import PyXA
    app = PyXA.Application("Image Events")
    app.launch()
    image = app.open("/Users/exampleUser/Desktop/Example1.png")

    # Show all properties of the image
    print(image.properties)

    # {'color_space': <ColorSpace.RGB: 1380401696>, 'image_file': <<class 'PyXA.apps.ImageEvents.XAImageEventsFile'>Example1.png>, 'bit_depth': <BitDepth.MILLIONS_OF_COLORS: 1835625580>, 'dimensions': (1106, 278), 'location': <<class 'PyXA.apps.ImageEvents.XAImageEventsFolder'>Desktop>, 'embedded_profile': <<class 'PyXA.apps.ImageEvents.XAImageEventsProfile'>sRGB IEC61966-2.1>, 'file_type': <FileType.PNG: 1347307366>, 'class': 'image', 'name': 'Example1.png', 'resolution': (72.0, 72.0)}

In many cases, it is faster or simply more convenient to access properties directly. All properties in the dictionary above can also be accessed as attributes of the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class, as we do below:

.. code-block:: python

    print(image.color_space)
    print(image.image_file)
    print(image.dimensions)
    print(image.resolution)
    print(image.name)

    # ColorSpace.RGB
    # <<class 'PyXA.apps.ImageEvents.XAImageEventsFile'>Example1.png>
    # (1106, 278)
    # (72.0, 72.0)
    # Example1.png

Manipulating Images
-------------------

Unlike other PyXA classes, most of these attributes are read-only and cannot be changed by simply setting them equal to a new value. Instead, the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class has several methods that perform image manipulation operations, in turn altering the properties of the image. For example, to change the color space of an image to grayscale, you would embed a gray color profile in it, as done in the code block below:

.. code-block:: python

    gray_profile = app.profiles().by_name("Generic Gray Profile")
    image.embed_profile(gray_profile)

Note how we obtain a reference to the desired color profile by name. This is likely to be the most straightforward way of referencing profiles. You can view a list of all profile names by simply printing the result of the :func:`PyXA.apps.ImageEvents.XAImageEventsApplication.profiles` method.

To alter the dimensions of an images, use the :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.crop`, :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.scale`, and :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.pad` methods of the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class. Cropping will isolate a section of the image, discarding content outside that area and decreasing the width and/or height of the image. Scaling maintains the image's content while uniformly increasing or decreasing the dimensions of the image. Padding an image will add a border of a specified thickness and color around the image, increasing its dimensions in the process. 

.. code-block:: python

    # Cropping
    image.crop((300, 300))  # Crop to +/- 150 pixels horizontally, +/- 50 pixels vertically from the center of the image

    # Scaling
    image.scale(2, 2)   # Scale the image up 3x
    image.scale(0.25)   # Scale the image down to 1/4 the size

    # Padding
    image.pad(100, 100)                     # Add a 100 pixel wide white border around the entire image
    image.pad(50, 0, PyXA.XAColor(0, 0, 0)) # Add a 50 pixel black border on only the left and ride sides
    image.pad(0, 25, PyXA.XAColor(1, 0, 0)) # Add a 25 pixel red border only on the top and bottom

    image.show_in_preview()

In addition to cropping, scaling, and padding, the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class provides methods for rotating and flipping images, namely :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.rotate`, :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.flip_horizontally`, and :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.flip_vertically`.

After manipulating an image, use the :func:`~PyXA.apps.ImageEvents.XAImageEventsImage.save` method to save the modified image to the disk. Without any parameters, this method will save the image in-place, overriding the existing image file.

.. code-block:: python

    image.save() # Save the image in-place (override original)
    image.save(file_path="/Users/exampleUser/Desktop/Example2.png") # Save to specific file path (override any file at that location)

The :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class implemented the :class:`~PyXA.XAProtocols.XAClipboardCodable` protocol, so you can also save image modifications directly to the clipboard, as done in the code below. This will copy the modified image's raw data to the clipboard without creating a permanent file on the disk. You can then paste the image, with all modifications included, into other applications.

.. code-block:: python

    image.scale(0.25)
    image.pad(50, 50, PyXA.XAColor(0, 0, 1))
    PyXA.XAClipboard().content = image

Tutorial 2 - Working With Lists of Images
*****************************************

The Image Events module has been designed around convenience, and a key aspect of that is the ability to conduct bulk operations with :class:`~PyXA.XABase.XAList` objects, in particular by using the :class:`~PyXA.apps.ImageEvents.XAImageEventsImageList` class. In addition to general syntactic convenience, :class:`~PyXA.apps.ImageEvents.XAImageEventsImageList` objects provide significant performance improvements over conventional looping operations. Since XALists do not spend time dereferencing PyObjC/ScriptingBridge pointers, they send far fewer Apple Events, leading to much faster execution. This is evidenced by the code below:

.. code-block:: python

    from timeit import timeit
    import PyXA
    app = PyXA.Application("Image Events")

    def without_xalist():
        img_data = []
        images = [app.open("/Users/exampleUser/Desktop/Example1.jpeg"), app.open("/Users/exampleUser/Desktop/Example2.jpeg"), app.open("/Users/exampleUser/Desktop/Example3.jpeg")]
        for image in images:
            image.scale(3)
            image.rotate(45)
            img_data.append(image.get_clipboard_representation())
        PyXA.XAClipboard().content = img_data

    def with_xalist():
        images = app.open("/Users/exampleUser/Desktop/Example1.jpeg", "/Users/exampleUser/Desktop/Example2.jpeg", "/Users/exampleUser/Desktop/Example3.jpeg")
        PyXA.XAClipboard().content = images.scale(3).rotate(45)

    r1 = timeit(without_xalist, number=100)
    r2 = timeit(with_xalist, number=100)

    print("Non-XAList avg over 100 trials:", r1 / 100)
    # ~3.835 seconds per iteration (on M1 Pro MacBook Pro)

    print("XAList avg over 100 trials:", r2 / 100)
    # ~0.076 seconds per iteration (on M1 Pro MacBook Pro)

In the XAList-equipped function, `app.open` yeilds an :class:`~PyXA.apps.ImageEvents.XAImageEventsImageList` object. We then scale and rotate all images in the list The code above also highlights the concise coding style supported by :class:`~PyXA.apps.ImageEvents.XAImageEventsImageList` objects. Method chaining as done here is entirely optional, but some may prefer this approach due to its similarity to JXA and JavaScript at large.

All attributes and methods of the :class:`~PyXA.apps.ImageEvents.XAImageEventsImage` class can be called on :class:`~PyXA.apps.ImageEvents.XAImageEventsImageList` objects as well. 

images = app.open("/Users/exampleUser/Desktop/Example1.jpeg", "/Users/exampleUser/Desktop/Example2.jpeg", "/Users/exampleUser/Desktop/Example3.jpeg")
# # print(images[0].rotate(30).image_with_modifications.show_in_preview())
# print(images.original_images()[0].show_in_preview())

.. code-block:: python

    # Access Attributes in Bulk
    print(images.properties())
    print(images.bit_depth(), images.color_space())
    print(images.dimensions(), images.resolution())
    print(images.file_type(), images.image_file(), images.name())

    # Retrieve Images By Attribute Value
    print(images.by_name("Example.png"))
    print(images.by_dimensions((2022, 1542)))
    print(images.by_file_type(app.FileType.JPEG))
    print(images.by_color_space(app.ColorSpace.RGB))
    print(images.by_bit_depth(app.BitDepth.MILLIONS_OF_COLORS))

    # Perform Bulk Manipulation Operations
    images.rotate(45).scale(2)
    images.flip_horizontally()
    images.embed_profile(app.profiles().by_name("Generic CMYK Profile"))
    images.save(file_paths=["/Users/exampleUser/Desktop/NewExample1.jpeg", "/Users/exampleUser/Desktop/NewExample2.jpeg", "/Users/exampleUser/Desktop/NewExample3.jpeg"])
    PyXA.XAClipboard().content = images

Image Events Examples
#####################
The examples below provide an overview of the capabilities of the Image Events module. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Image Events Tutorials`).

Example 1 - Using Image Events Alongside Other PyXA Features
************************************************************

Combining Image Events, XAImages, Photos.app, and more
------------------------------------------------------

The functionality of the Image Events module can be easily extended by intertwining it with other PyXA features. The :class:`~PyXA.XABase.XAImage` class is a key example of this. In fact, you can easily convert images managed by Image Events into XAImages, giving you full access to all features thereof. In the code below, we first use Image Events to rotate an image, then we use the :func:`~PyXA.XABase.XAImage.extract_text` method from :class:`~PyXA.XABase.XAImage` to retrieve text contained within. We also open the original and modified images in preview, copy the raw data of the modified image's TIFF representation to the clipboard, and save the modified image to a file on the disk.

.. code-block:: python

    import PyXA
    app = PyXA.Application("Image Events")
    image = app.open("/Users/steven/Desktop/code.png").rotate(45)
    modified_image = image.modified_image_object
    print(modified_image.extract_text())

    image.original_image_object.show_in_preview()
    modified_image.show_in_preview()

    PyXA.XAClipboard().contents = str(modified_image.data)
    modified_image.save("/Users/exampleUser/Desktop/NewExample4.png")






Image Events Resources
######################
- `Mac Automation Scripting Guide - Manipulating Images <https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/ManipulateImages.html>`_

For all classes, methods, and inherited members of the Image Events module, see the :ref:`Image Events Module Reference`.