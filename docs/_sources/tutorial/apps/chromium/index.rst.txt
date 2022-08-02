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
Using PyXA, you can obtain a list of bookmarks in Chromium, bookmark folders, and their associated data. To get a list of bookmark folders, use :func:`PyXA.apps.Chromium.XAChromiumApplication.bookmark_folders`. Use :func:`PyXA.apps.Chromium.XAChromiumBookmarkFolder.bookmark_items` to list the individual bookmarks contained in a folder. :attribute:`PyXA.apps.Chromium.XAChromiumApplication.bookmarks_bar` and :attribute:`PyXA.apps.Chromium.XAChromiumApplication.other_bookmarks` can be used to access bookmarks on the bookmarks bar and in all other folders, respectively.

It is not currently possible to create bookmark folders or bookmark items via PyXA (or AppleScript) as that functionality is not made available by the Chromium developers. Despite this lack of support, bookmark and bookmark folder creation via UI scripting is planned for a future release.

Chromium Tutorials
##################
There are currently no tutorials for the Chromium module.

Examples
########
The examples below provide an overview of the capabilities of the Chromium module. They do not provide any output. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Chromium Tutorials`).

Example 1 - Opening and saving a webpage
****************************************

The example below activates Chromium.app, opens Apple's website in a new tab, waits for the tab to finish loading, then saves the site's resources (e.g. HTML, CSS, JavaScript, and images) to a location on the disk. Note the use of a full URL, beginning with "http", as well as a full file path, beginning with "/". Both a full URL and full file path are necessary in order for this example to operate successfully. 

.. code-block:: python
   :linenos:

   import PyXA
   from time import sleep

   # Open URL in new tab
   app = PyXA.application("Chromium")
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

   app = PyXA.application("Chromium")
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

Chromium Classes and Methods
############################

Classes
*******
   
.. autosummary:: PyXA.apps.Chromium
   :nosignatures:

   ~PyXA.apps.Chromium.XAChromiumApplication
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolder
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList
   ~PyXA.apps.Chromium.XAChromiumBookmarkItem
   ~PyXA.apps.Chromium.XAChromiumTabList
   ~PyXA.apps.Chromium.XAChromiumTab
   ~PyXA.apps.Chromium.XAChromiumWindow

XAChromiumApplication Methods
*****************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumApplication
   :nosignatures:


   ~PyXA.apps.Chromium.XAChromiumApplication.open
   ~PyXA.apps.Chromium.XAChromiumApplication.bookmark_folders
   ~PyXA.apps.Chromium.XAChromiumApplication.make
   ~PyXA.apps.Chromium.XAChromiumApplication.new_tab
   ~PyXA.apps.Chromium.XAChromiumApplication.new_window
   
XAChromiumBookmarkFolderList Methods
************************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumBookmarkFolderList
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.id
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.title
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.index
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.by_id
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.by_title
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolderList.by_index

XAChromiumBookmarkFolder Methods
********************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumBookmarkFolder
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolder.bookmark_folders
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolder.bookmark_items
   ~PyXA.apps.Chromium.XAChromiumBookmarkFolder.delete

XAChromiumBookmarkItemList Methods
**********************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumBookmarkItemList
   :nosignatures:

   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.id
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.title
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.url
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.index
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.by_id
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.by_title
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.by_url
   ~PyXA.apps.Chromium.XAChromiumBookmarkItemList.by_index

XAChromiumBookmarkItem Methods
******************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumBookmarkItem
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumBookmarkItem.delete

XAChromiumTabList Methods
*************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumTabList
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumTabList.id
   ~PyXA.apps.Chromium.XAChromiumTabList.title
   ~PyXA.apps.Chromium.XAChromiumTabList.url
   ~PyXA.apps.Chromium.XAChromiumTabList.loading
   ~PyXA.apps.Chromium.XAChromiumTabList.by_id
   ~PyXA.apps.Chromium.XAChromiumTabList.by_title
   ~PyXA.apps.Chromium.XAChromiumTabList.by_url
   ~PyXA.apps.Chromium.XAChromiumTabList.by_loading

XAChromiumTab Methods
*********************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumTab
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumTab.undo
   ~PyXA.apps.Chromium.XAChromiumTab.redo
   ~PyXA.apps.Chromium.XAChromiumTab.cut_selection
   ~PyXA.apps.Chromium.XAChromiumTab.copy_selection
   ~PyXA.apps.Chromium.XAChromiumTab.paste_selection
   ~PyXA.apps.Chromium.XAChromiumTab.select_all
   ~PyXA.apps.Chromium.XAChromiumTab.go_back
   ~PyXA.apps.Chromium.XAChromiumTab.go_forward
   ~PyXA.apps.Chromium.XAChromiumTab.reload
   ~PyXA.apps.Chromium.XAChromiumTab.stop
   ~PyXA.apps.Chromium.XAChromiumTab.print
   ~PyXA.apps.Chromium.XAChromiumTab.view_source
   ~PyXA.apps.Chromium.XAChromiumTab.save
   ~PyXA.apps.Chromium.XAChromiumTab.close
   ~PyXA.apps.Chromium.XAChromiumTab.execute
   ~PyXA.apps.Chromium.XAChromiumTab.move_to
   ~PyXA.apps.Chromium.XAChromiumTab.duplicate_to

XAChromiumWindow Methods
************************
   
.. autosummary:: PyXA.apps.Chromium.XAChromiumWindow
   :nosignatures:
   
   ~PyXA.apps.Chromium.XAChromiumWindow.new_tab
   ~PyXA.apps.Chromium.XAChromiumWindow.tabs

For all classes, methods, and inherited members on one page, see the :ref:`Chromium Module Reference`