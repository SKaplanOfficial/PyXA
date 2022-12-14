Safari Module Overview
======================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA has full nearly complete feature support for Safari, but some functionalities, such as saving a document, are currently unavailable. These will be implemented in future versions of the Safari module.


Safari Tutorials
##################
There are currently no tutorials for the Safari module.

Safari Examples
###############
The examples below provide an overview of the capabilities of the Safari module. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Safari Tutorials`).

Example 1 - Using Safari Methods and Attributes
***********************************************

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

For all classes, methods, and inherited members of the Safari module, see the :ref:`Safari Module Reference`.