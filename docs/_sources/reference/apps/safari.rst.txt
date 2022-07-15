Safari Module
===============

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
########
PyXA has full nearly complete feature support for Safari, but some functionalities, such as saving a document, are currently unavailable. These will be implemented in future versions of the Safari module.


Safari Tutorials
##################
There are currently no tutorials for the Safari module.

Examples
########
The examples below provide an overview of the capabilities of the Safari module. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Safari Tutorials`).

Example 1 - Using Safari Methods and Attributes
*****************************************************

This example provides an overview of the most common methods and attributes of the Safari module. 

.. code-block:: python
   :linenos:

   import PyXA

   # Open URL in new tab
   safari = PyXA.application("Safari")

   # Get open windows, documents, and tabs
   window1 = safari.front_window()
   window2 = safari.windows()[1]
   documents = safari.documents()
   current_doc = safari.current_document
   tabs = window1.tabs()
   current_tab = window1.current_tab

   # Get properties of documents
   urls = documents.url()
   names = documents.name()
   html = current_doc.source()

   # Get properties of tabs
   urls = tabs.url()
   texts = tabs.text()
   name = current_tab.name()

   # Filter documents and tabs
   doc1 = documents.by_url("https://apple.com")
   doc2 = documents.by_name("Apple")
   tab1 = tabs.by_index(1)
   tab2 = tabs.by_visible(True)

   # Bulk document operations
   documents.add_to_reading_list()
   documents.email()
   documents.do_javascript("alert('Testing 1 2 3');")
   documents.search("Example")

   # Bulk tab operations
   tabs.reload()
   tabs.add_to_reading_list()
   tabs.email()
   tabs.do_javascript("alert('Hello!');")
   tabs.search("Example")
   tabs.move_to(window2)
   tabs.duplicate_to(window2)

   # Sub-array operations
   some_tabs = tabs[3:5]
   some_tabs.close()

Safari Resources
##################
- `Safari Quick Start Guide <https://www.safari.org/safari-os/quick-start-guide/>`_

Safari Classes and Methods
############################
.. toctree::
   :maxdepth: 1
   :caption: Classes

   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList
   ../api/apps/safari/XASafariDocument/PyXA.apps.Safari.XASafariDocument
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList
   ../api/apps/safari/XASafariTab/PyXA.apps.Safari.XASafariTab
   ../api/apps/safari/XASafariWindow/PyXA.apps.Safari.XASafariWindow

.. toctree::
   :maxdepth: 1
   :caption: Methods

   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.open
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.show_bookmarks
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.add_to_reading_list
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.search
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.search_in_tab
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.do_javascript
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.email
   ../api/apps/safari/XASafariApplication/PyXA.apps.Safari.XASafariApplication.make

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric.search
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric.add_to_reading_list
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric.do_javascript
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric.email
   ../api/apps/safari/XASafariGeneric/PyXA.apps.Safari.XASafariGeneric.reload

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.name
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.modified
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.file
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.source
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.url
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.text
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_name
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_modified
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_file
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_source
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_url
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.by_text
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.reload
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.add_to_reading_list
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.email
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.do_javascript
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.search
   ../api/apps/safari/XASafariDocumentList/PyXA.apps.Safari.XASafariDocumentList.close

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariDocument/PyXA.apps.Safari.XASafariDocument.print

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.source
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.url
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.index
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.text
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.visible
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.name
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_source
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_url
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_index
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_text
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_visible
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.by_name
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.reload
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.add_to_reading_list
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.email
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.do_javascript
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.search
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.move_to
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.duplicate_to
   ../api/apps/safari/XASafariTabList/PyXA.apps.Safari.XASafariTabList.close

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariTab/PyXA.apps.Safari.XASafariTab.move_to
   ../api/apps/safari/XASafariTab/PyXA.apps.Safari.XASafariTab.duplicate_to

.. toctree::
   :maxdepth: 1
   
   ../api/apps/safari/XASafariWindow/PyXA.apps.Safari.XASafariWindow.tabs

For all classes, methods, and inherited members on one page, see the :ref:`Complete Safari API`