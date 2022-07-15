TextEdit Module
===============

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
########
TextEdit is fully supported in PyXA.

TextEdit Tutorials
##################
There are currently no tutorials for the Shortcuts module.

Examples
########
The examples below provide an overview of the capabilities of the TextEdit module. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`TextEdit Tutorials`).

Example 1 - Using TextEdit methods and attributes
*************************************************

This example utilizes most of the methods provided in the TextEdit module, and it shows how to accomplish common tasks such as retrieving the currently opened documents, opening documents, creating new documents, and editing documents.

.. code-block:: python
   :linenos:

   import PyXA
   textedit = PyXA.application("TextEdit")
   textedit.activate()

   # Opening existing documents
   document = textedit.open("/Users/steven/Documents/Example.txt")
   document = textedit.documents().first
   document = textedit.front_window().document

   # Creating new documents
   textedit.new_document("new_doc_1.txt", location="/Users/exampleuser/Documents/")
   new_doc_2 = textedit.make("document", {"path": "/Users/exampleuser/Documents/NewDocument2.txt"})
   textedit.documents().push(new_doc_2)

   # Accessing top-level text elements
   paragraphs = document.paragraphs()
   sentences = document.sentences()
   words = document.words()
   characters = document.characters()

   # Conducting bulk operations with XAList objects
   combined_words = paragraphs[3:8].words()
   print(paragraphs.sentences())
   textedit.documents().append("\\nA new line in each open document")

   # Text elements are parents of text elements
   # Note: Words/characters are currently children of paragraphs, not sentences.
   sentences2 = paragraphs[0].sentences()
   words2 = paragraphs[0].words()
   characters2 = words2[0].characters()

   # Saving and closing documents
   document.save()
   document.close()

Example 2 - Creating documents from text returned by other PyXA methods
***********************************************************************

The example below implements a crude yet functional automatic flashcard generator that uses the text content of a webpage to create a randomized set of flashcards. The first half of the code uses the :mod:`PyXA.Safari` module to extract the visible text of a Wikipedia page, then saves that text to the disk. The second half then uses the TextEdit module to obtain a list of paragraphs in the text, from which five are randomly selected. The first sentence of each selected paragraphs is used as the hint for the flashcard. This could have use as a study tool or as a way to quickly summarize a topic, in addition to other potential uses.

.. code-block:: python
   :linenos:

   import os
   from pprint import pprint
   import PyXA
   import random
   from time import sleep

   # Open a URL and wait for it to load
   safari = PyXA.application("Safari")
   safari.open("https://en.wikipedia.org/wiki/Computer")
   sleep(1)

   # Get the text of the document, then close the tab
   doc_text = safari.current_document.text
   safari.front_window().current_tab.close()

   # Create folder path if it doesn't already exist
   folder_path = "/Users/steven/Documents/articles/"
   os.makedirs(folder_path, exist_ok=True)

   # Save the document text to a file on the disk
   file_path = folder_path + "Wikipedia-Computer.txt"
   with open(file_path, "w") as file:
      file.write(doc_text)

   # Open the document and get its paragraphs
   textedit = PyXA.application("TextEdit")
   textedit.open(file_path)
   doc = textedit.front_window().document
   paragraphs = doc.paragraphs()

   # Create 5 random (sentence, paragraph) 'flashcards'
   flashcards = []
   while len(flashcards) < 5:
      paragraph = random.choice(paragraphs)
      if len(paragraph) > 200:
         sentence = random.choice(paragraph.sentences())
         flashcards.append((sentence, paragraph))
      
   pprint(flashcards)

TextEdit Resources
##################
- `TextEdit User Guide - Apple Support <https://support.apple.com/guide/textedit/welcome/mac>`_

TextEdit Classes and Methods
############################
.. toctree::
   :maxdepth: 1
   :caption: Classes

   ../api/apps/textedit/XATextEditApplication/PyXA.apps.TextEdit.XATextEditApplication
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList
   ../api/apps/textedit/XATextEditDocument/PyXA.apps.TextEdit.XATextEditDocument
   ../api/apps/textedit/XATextEditWindow/PyXA.apps.TextEdit.XATextEditWindow

.. toctree::
   :maxdepth: 1
   :caption: Methods

   ../api/apps/textedit/XATextEditApplication/PyXA.apps.TextEdit.XATextEditApplication.print
   ../api/apps/textedit/XATextEditApplication/PyXA.apps.TextEdit.XATextEditApplication.documents
   ../api/apps/textedit/XATextEditApplication/PyXA.apps.TextEdit.XATextEditApplication.new_document
   ../api/apps/textedit/XATextEditApplication/PyXA.apps.TextEdit.XATextEditApplication.make
   
.. toctree::
   :maxdepth: 1
   
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.properties
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.path
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.name
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.text
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.paragraphs
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.words
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.characters
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.attribute_runs
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.attachments
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.modified
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.by_properties
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.by_path
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.by_name
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.by_modified
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.prepend
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.append
   ../api/apps/textedit/XATextEditDocumentList/PyXA.apps.TextEdit.XATextEditDocumentList.reverse

.. toctree::
   :maxdepth: 1
   
   ../api/apps/textedit/XATextEditDocument/PyXA.apps.TextEdit.XATextEditDocument.close
   ../api/apps/textedit/XATextEditDocument/PyXA.apps.TextEdit.XATextEditDocument.save
   ../api/apps/textedit/XATextEditDocument/PyXA.apps.TextEdit.XATextEditDocument.copy

For all classes, methods, and inherited members on one page, see the :ref:`Complete TextEdit API`