Safari Module Overview
======================

.. contents:: Table of Contents
   :depth: 3
   :local:

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

Classes
*******
   
.. autosummary:: PyXA.apps.Safari
   :nosignatures:

   ~PyXA.apps.Safari.XASafariApplication
   ~PyXA.apps.Safari.XASafariGeneric
   ~PyXA.apps.Safari.XASafariDocumentList
   ~PyXA.apps.Safari.XASafariDocument
   ~PyXA.apps.Safari.XASafariTabList
   ~PyXA.apps.Safari.XASafariTab
   ~PyXA.apps.Safari.XASafariWindow

XASafariApplication Methods
***************************
   
.. autosummary:: PyXA.apps.XASafariApplication
   :nosignatures:

   ~PyXA.apps.Safari.XASafariApplication.open
   ~PyXA.apps.Safari.XASafariApplication.show_bookmarks
   ~PyXA.apps.Safari.XASafariApplication.add_to_reading_list
   ~PyXA.apps.Safari.XASafariApplication.search
   ~PyXA.apps.Safari.XASafariApplication.search_in_tab
   ~PyXA.apps.Safari.XASafariApplication.do_javascript
   ~PyXA.apps.Safari.XASafariApplication.email
   ~PyXA.apps.Safari.XASafariApplication.make

XASafariGeneric Methods
***********************
   
.. autosummary:: PyXA.apps.XASafariGeneric
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariGeneric.search
   ~PyXA.apps.Safari.XASafariGeneric.add_to_reading_list
   ~PyXA.apps.Safari.XASafariGeneric.do_javascript
   ~PyXA.apps.Safari.XASafariGeneric.email
   ~PyXA.apps.Safari.XASafariGeneric.reload

XASafariDocumentList Methods
****************************
   
.. autosummary:: PyXA.apps.XASafariDocumentList
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariDocumentList.name
   ~PyXA.apps.Safari.XASafariDocumentList.modified
   ~PyXA.apps.Safari.XASafariDocumentList.file
   ~PyXA.apps.Safari.XASafariDocumentList.source
   ~PyXA.apps.Safari.XASafariDocumentList.url
   ~PyXA.apps.Safari.XASafariDocumentList.text
   ~PyXA.apps.Safari.XASafariDocumentList.by_name
   ~PyXA.apps.Safari.XASafariDocumentList.by_modified
   ~PyXA.apps.Safari.XASafariDocumentList.by_file
   ~PyXA.apps.Safari.XASafariDocumentList.by_source
   ~PyXA.apps.Safari.XASafariDocumentList.by_url
   ~PyXA.apps.Safari.XASafariDocumentList.by_text
   ~PyXA.apps.Safari.XASafariDocumentList.reload
   ~PyXA.apps.Safari.XASafariDocumentList.add_to_reading_list
   ~PyXA.apps.Safari.XASafariDocumentList.email
   ~PyXA.apps.Safari.XASafariDocumentList.do_javascript
   ~PyXA.apps.Safari.XASafariDocumentList.search
   ~PyXA.apps.Safari.XASafariDocumentList.close

XASafariDocument Methods
************************
   
.. autosummary:: PyXA.apps.XASafariDocument
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariDocument.print

XASafariTabList Methods
***********************
   
.. autosummary:: PyXA.apps.XASafariTabList
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariTabList.source
   ~PyXA.apps.Safari.XASafariTabList.url
   ~PyXA.apps.Safari.XASafariTabList.index
   ~PyXA.apps.Safari.XASafariTabList.text
   ~PyXA.apps.Safari.XASafariTabList.visible
   ~PyXA.apps.Safari.XASafariTabList.name
   ~PyXA.apps.Safari.XASafariTabList.by_source
   ~PyXA.apps.Safari.XASafariTabList.by_url
   ~PyXA.apps.Safari.XASafariTabList.by_index
   ~PyXA.apps.Safari.XASafariTabList.by_text
   ~PyXA.apps.Safari.XASafariTabList.by_visible
   ~PyXA.apps.Safari.XASafariTabList.by_name
   ~PyXA.apps.Safari.XASafariTabList.reload
   ~PyXA.apps.Safari.XASafariTabList.add_to_reading_list
   ~PyXA.apps.Safari.XASafariTabList.email
   ~PyXA.apps.Safari.XASafariTabList.do_javascript
   ~PyXA.apps.Safari.XASafariTabList.search
   ~PyXA.apps.Safari.XASafariTabList.move_to
   ~PyXA.apps.Safari.XASafariTabList.duplicate_to
   ~PyXA.apps.Safari.XASafariTabList.close

XASafariTab Methods
*******************
   
.. autosummary:: PyXA.apps.XASafariTab
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariTab.move_to
   ~PyXA.apps.Safari.XASafariTab.duplicate_to

XASafariWindow Methods
**********************
   
.. autosummary:: PyXA.apps.XASafariWindow
   :nosignatures:
   
   ~PyXA.apps.Safari.XASafariWindow.tabs

For all classes, methods, and inherited members on one page, see the :ref:`Safari Module Reference`