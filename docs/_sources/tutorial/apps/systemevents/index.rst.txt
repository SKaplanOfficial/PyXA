System Events Module Overview
=============================

The Terminal module enables control over Terminal.app from within Python, including the ability to run Terminal script and receive the execution return value.

System Events Examples
######################

Example 1 - Sorting the Desktop
*******************************

.. code-block:: python

    import PyXA
    app = PyXA.Application("System Events")

    # Set the desktop picture
    app.current_desktop.picture = "/Users/exampleUser/Desktop/Images/Background.png"

    # Toggle darkmode
    app.appearance_preferences.dark_mode = not app.appearance_preferences.dark_mode 

    # # Add a login item -- This opens the Documents folder upon login
    new_item = app.make("login item", {"path": "/Users/exampleUser/Documents"})
    app.login_items().push(new_item)

    # Start the current screensaver
    app.current_screen_saver.start()

This example uses PyXA to sort files on the desktop into appropriate category folders.

.. code-block:: python

    import PyXA
    app = PyXA.Application("System Events")

    desktop_files = app.desktop_folder.files()
    desktop_folders = app.desktop_folder.folders()

    # Create sorting bin folders
    images_folder = app.make("folder", {"name": "Images"})
    videos_folder = app.make("folder", {"name": "Videos"})
    audio_folder = app.make("folder", {"name": "Audio"})
    documents_folder = app.make("folder", {"name": "Documents"})
    desktop_folders.push(images_folder, videos_folder, audio_folder, documents_folder)

    # Sort images
    image_predicate = "name ENDSWITH '.png' OR name ENDSWITH '.jpg' OR name ENDSWITH '.jpeg' OR name ENDSWITH '.aiff'"
    image_files = desktop_files.filter(image_predicate)
    image_files.move_to(images_folder)

    # Sort videos
    video_predicate = "name ENDSWITH '.mov' OR name ENDSWITH '.mp4' OR name ENDSWITH '.avi' OR name ENDSWITH '.m4v'"
    video_files = desktop_files.filter(video_predicate)
    video_files.move_to(videos_folder)

    # Sort audio
    audio_predicate = "name ENDSWITH '.mp3' OR name ENDSWITH '.ogg'"
    audio_files = desktop_files.filter(audio_predicate)
    audio_files.move_to(audio_folder)

    # Sort remaining (documents)
    desktop_files.move_to(documents_folder)

System Events Resources
#######################
- `System Events - AppleScript: The Definitive Guide <https://www.oreilly.com/library/view/applescript-the-definitive/0596102119/ch23s02s03.html>`_

For all classes, methods, and inherited members of the System Events module, see the :ref:`System Events Module Reference`.