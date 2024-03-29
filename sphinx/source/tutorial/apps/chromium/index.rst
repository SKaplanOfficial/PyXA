Chromium Module Overview
========================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA has full support for Chromium and Chromium derivatives such as Google Chrome, Opera, Brave, Vivaldi, and Microsoft Edge. Some additional convenience methods, such as :func:`PyXA.apps.Chromium.XAChromiumApplication.new_tab`, are provided to simplify common scripting tasks. 

Windows and Tabs
****************
PyXA allows full control over Chromium windows and tabs, as well as full access to their properties. Opening a webpage in Chromium (or any Chromium derivative) is accomplished by calling :func:`PyXA.apps.Chromium.XAChromiumApplication.open` and providing a URL as an argument. The URL can be either a string or an :class:`PyXA.XABase.XAURL` object. The URL must be a full URL—that is, it must follow the structure of "scheme://host/relativeURI".

New windows can be created using the :func:`PyXA.apps.Chromium.XAChromiumApplication.new_window` method, and a URL can be passed as an argument to open a window at the specified URL. Similarly, new tabs can be created using :func:`PyXA.apps.Chromium.XAChromiumApplication.new_tab`, and again a URL can be specified. :func:`PyXA.apps.Chromium.XAChromiumApplication.make` can be used to manually create a new window or tab object without adding it to the UI until :func:`PyXA.XABaseScriptable.XASBWindowList.push` or :func:`PyXA.apps.Chromium.XAChromiumTabList.push` is called, allowing you to split the construction of an element across portions of your script. This ability is likely most useful when the window's or tab's properties are influenced by the result of multiple logical operations.

Bookmarks
*********
Using PyXA, you can obtain a list of bookmarks in Chromium, bookmark folders, and their associated data. To get a list of bookmark folders, use :func:`PyXA.apps.Chromium.XAChromiumApplication.bookmark_folders`. Use :func:`PyXA.apps.Chromium.XAChromiumBookmarkFolder.bookmark_items` to list the individual bookmarks contained in a folder. :attr:`PyXA.apps.Chromium.XAChromiumApplication.bookmarks_bar` and :attr:`PyXA.apps.Chromium.XAChromiumApplication.other_bookmarks` can be used to access bookmarks on the bookmarks bar and in all other folders, respectively.

It is not currently possible to create bookmark folders or bookmark items via PyXA (or AppleScript) as that functionality is not made available by the Chromium developers. Despite this lack of support, bookmark and bookmark folder creation via UI scripting is planned for a future release.

Chromium Tutorials
##################
There are currently no tutorials for the Chromium module.

Chromium Examples
#################
The examples below provide an overview of the capabilities of the Chromium module. They do not provide any output. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Chromium Tutorials`).

Example 1 - Opening and saving a webpage
****************************************

The example below activates Chromium.app, opens Apple's website in a new tab, waits for the tab to finish loading, then saves the site's resources (e.g. HTML, CSS, JavaScript, and images) to a location on the disk. Note the use of a full URL, beginning with "http", as well as a full file path, beginning with "/". Both a full URL and full file path are necessary in order for this example to operate successfully. 

.. code-block:: python
   :linenos:

   import PyXA
   from time import sleep

   # Open URL in new tab
   app = PyXA.Application("Chromium")
   app.activate()
   app.open("http://apple.com")

   # Wait for tab to finish loading
   tab = app.front_window().tabs().last()
   while tab.loading:
      sleep(0.1)

   # Save the tab's content
   tab.save("/Users/exampleuser/Downloads/apple-site")

Example 2 - Making new windows and tabs
***************************************

This example shows how to manually create new windows and tabs in Chromium. The general logic for this is to create a new object of the specified type, then push that object onto the relevant list. Alternatively, you can use the :func:`PyXA.apps.Chromium.XAChromiumApplication.new_window` and :func:`PyXA.apps.Chromium.XAChromiumApplication.new_tab` methods.

.. code-block:: python
   :linenos:

   import PyXA

   app = PyXA.Application("Chromium")
   app.activate()

   # Make a new window using the convenience method
   app.new_window("http://www.apple.com")

   # Make a new tab using the convenience method
   app.new_tab("http://www.apple.com")

   # Make a new window manually
   window = app.make("window")
   app.windows().push(window)

   # Make a new tab manually
   tab = app.make("tab", {"URL": "http://www.apple.com"})
   window.tabs().push(tab)

Chromium Resources
##################
- `Chromium Quick Start Guide <https://www.chromium.org/chromium-os/quick-start-guide/>`_

For all classes, methods, and inherited members of the Chromium module, see the :ref:`Chromium Module Reference`.