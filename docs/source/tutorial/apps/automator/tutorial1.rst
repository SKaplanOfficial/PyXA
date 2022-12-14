Making a Combined Workflow for Creating Image Mosaic
====================================================

Overview
########
Automation scripts can ask users for many different kinds of input, and different automation technologies are particularly suited to handling some types of inputs over others. Moreover, prompting users for different kinds of input may be easier using one automation technology over another. For example, Python has specialized tools for working with command-line arguments, so you might use PyXA over other automation technologies when looking to create a command-line automation script. Comparatively, Shortcuts and Automator provide highly intuitive ways to get non-text input from users, so you might opt to use one of them instead when looking to handle image, video, and other media data. When working on automation scripts, you can combine all of these technologies and use them in tandem, enabling you to always utilize the best tool for the task. In this tutorial, we combine the abilities of PyXA and Automator, producing a combined workflow to create a mosaic of selected images using the `Pillow <https://pypi.org/project/Pillow/>`_ library for Python.

Part 1 - Getting User Input
###########################
To create our combined automation workflow, let's first think about its component parts. We know that Automator has actions for user input, so you might be able to guess that there is a dedicated "Ask For Photos" action. It's unlikely that Apple would expose the direct NSImage objects via that action, so we can assume that the action outputs either image file paths or image IDs. This is something that we'll need to check in a moment. The Python Image Library (Pillow) primarily operates on images loaded from files, and Python is slower than Automator at retrieving UI element property values, so ideally we'll have the PyXA side of the automation script working with file paths. Let's create a workflow in Automator that prompts the user to select photos as input and outputs image file paths.

This can be accomplished with a single action: "Ask For Photos". This action already outputs file paths, so there is no need for an additional action to extract that data. You can confirm this by adding the action (dragging it from the left-side sidebar into the main work area, then dropping it), then pressing the "run" button in the top right corner. The workflow will prompt you to select images. After clicking "Choose", click the "Results" button on the action and open the tab labelled "{}" for "Raw Data". You should see an image file path -- hooray! When this workflow is run from PyXA, the execution return value will be in the same format as the raw data displayed.

Save the workflow as "Ask For Photos.workflow" in a location of your choosing. This tutorial assumes that the workflow was saved in the Automator folder of iCloud, but this does not need to be the case -- just make sure to change the path in the PyXA code.

With the workflow saved, we can move on to the PyXA script. Since we're working with Automator, we need to initialize the Automator application object. Next, we instruct Automator to open a workflow from a specified file path. This provides a reference to the now-open workflow element, which we can execute. As test, let's print the output of the execution. Our code is thus:

.. code-block:: python
    :linenos:

    import PyXA
    automator = PyXA.application("Automator")
    workflow = automator.open("/Users/exampleuser/Library/Mobile Documents/com~apple~Automator/Documents/Ask For Photos.workflow")
    print(workflow.execute())

If you run the PyXA script now, you should again be prompted to select photos, and you should see that the paths to each image you selected, if any, were printed by the PyXA script.


Part 2 - Creating A Mosaic
##########################
The goal of this tutorial is to highlight the ability to intertwine PyXA and Automator -- believe it or not, we're done with that! The rest of this part looks at how to using the Pillow library to create a mosaic of images; it has nothing to do with PyXA, apart from that we used PyXA to execute an Automator workflow. To run the rest of this tutorial, you'll need to adjust your imports to the following:

.. code-block:: python

    import PyXA, math
    from PIL import Image

We start by setting a base width and height for each image within the mosaic. We choose 400x200 for simplicity, but you can choose any size. Each image in the mosaic will have those dimensions or smaller. 

.. code-block:: python

    base_width = 400
    base_height = 200

Next, we calculate the root of the number of image paths we have. For simplicity, we are creating an NxN mosaic, where N is the integer root of the total number of images. This tutorial forgoes error checking and other niceties that you might wish to include in your remake of this automation.

.. code-block:: python

    root = int(math.sqrt(len(image_paths)))

With the root and base dimensions set, we can create the canvas for our mosaic. The canvas is initially an empty image with the size of the final image we intend to create.

.. code-block:: python

    dim = (root * base_width, root * base_width)
    mosaic = Image.new("RGB", dim)

To populate the image, we place scaled down versions of the images we selected at calculated locations. This is done by looping over each row and column of the mosaic and pasting the scaled down image at the appropriate location. Since we are making a square mosaic, the number of rows and columns both goes from 0 to the root defined previously. The path of each image then sits at index `row + col * root`. We load the image at that path, then resize it while maintaining proportions. We then paste the resized image at the slot defined by the row, column, and base dimensions.

.. code-block:: python

    for row in range(0, root):
        for col in range(0, root):
            path = image_paths[row + col * root]
            img = Image.open(path)

            width = int(max(base_width, base_width/img.size[0] * img.size[1]))
            img = img.resize((base_width, width), Image.ANTIALIAS)
            mosaic.paste(img, (base_width * col, base_width * row))

Finally, we use the `show` method to show the mosaic in Preview.

.. code-block:: python

    mosaic.show()

Conclusion
##########
The full code for this tutorial:

.. code-block:: python
    :linenos:

    import PyXA, math
    from PIL import Image

    # Execute Automator workflow and receive list of image paths
    automator = PyXA.application("Automator")
    workflow = automator.open("/Users/steven/Library/Mobile Documents/com~apple~Automator/Documents/Ask For Photos.workflow")
    image_paths = workflow.execute()

    # Set base dimensions of mosaic images
    base_width = 400
    base_height = 200

    # Get number of rows and columns
    root = int(math.sqrt(len(image_paths)))

    # Create empty canvas
    dim = (root * base_width, root * base_width)
    mosaic = Image.new("RGB", dim)

    # Populate the canvas
    for row in range(0, root):
        for col in range(0, root):
            # Load image from path
            path = image_paths[row + col * root]
            img = Image.open(path)

            # Resize proportionally
            width = int(max(base_width, base_width/img.size[0] * img.size[1]))
            img = img.resize((base_width, width), Image.ANTIALIAS)
            mosaic.paste(img, (base_width * col, base_width * row))

    mosaic.show()

See Also
########

.. .. toctree::
..    :maxdepth: 1

..     tutorial2
..    ../shortcuts/tutorial1
