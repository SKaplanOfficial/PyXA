Notes Module Overview
=====================

Notes Tutorials
###############

Tutorial 1 - Interacting with Notes
***********************************

Accessing Notes.app Objects
---------------------------

.. code-block:: python

    import PyXA
    from datetime import datetime, timedelta

    app = PyXA.Application("Notes")

    # Get top-level lists of objects
    print(app.accounts())
    print(app.folders())
    print(app.notes())
    print(app.attachments())
    # <<class 'PyXA.apps.Notes.XANotesAccountList'>[('iCloud', 'x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICAccount/p3'), ...]>
    # <<class 'PyXA.apps.Notes.XANotesFolderList'>[('COS 573 - Computer Vision', 'x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICFolder/p4176'), ...]>
    # <<class 'PyXA.apps.Notes.XANoteList'>['x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p5232', ...]>
    # <<class 'PyXA.apps.Notes.XANotesAttachmentList'>[('hello, world', 'x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICAttachment/p4122'), ...]>

    # Use chaining to get objects organized by container
    print(app.folders().notes())
    # <<class 'PyXA.apps.Notes.XANoteList'>[(
    #     "x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p4174"
    # ), (
    #     "x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p4175"
    # ), (
    #     "x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p5232",
    #     "x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p4827",
    #     "x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p4935",
    #     ...
    # )]>

    # Get attachments organized per note, per folder, per account
    print(app.accounts().folders().notes().attachments())

    # Get notes by attributes
    note1 = app.notes().by_name("PyXA Ideas")
    note2 = app.notes().containing("plaintext", "random note text")
    recently_edited = app.notes().greater_than("modificationDate", datetime.now() - timedelta(hours=5))

    # Get attachments on a specific notes
    note1_attachments = note1.attachments()

    # Get notes in a specific folder
    fnotes = app.folders()[1].notes()

Accessing Attributes of Notes.app Objects
-----------------------------------------

Access individual attributes

.. code-block:: python

    import PyXA
    app = PyXA.Application("Notes")
    notes = app.notes()

    # Access attributes of accounts
    account = app.accounts().first
    print(account.name)
    print(account.default_folder)
    # iCloud
    # <<class 'PyXA.apps.Notes.XANotesFolder'>Notes, x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICFolder/p1>

    # Access attributes of folders
    folder = app.folders()[0]
    print(folder.name)
    print(folder.id)
    # COS 573 - Computer Vision
    # x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICFolder/p4176

    # Access attributes of notes
    note = app.notes().by_name("Important Note")
    print("Name:", note.name)
    print("\nBody:", note.body)
    print("\nPlaintext:", note.plaintext)
    print("\nCreation Date:", note.creation_date)
    print("Modification Date:", note.modification_date)
    print("\nID:", note.id)
    # Name: Important Note
    #
    # Body: <div><b><span style="font-size: 24px">Important Note</span></b></div>
    # <div><br></div>
    # <div>Important note text</div>
    # <div><br></div>
    # <div><img style="max-width: 100%; max-height: 100%;" src="data:image/png;base64,
    # ...
    #
    # Plaintext: Important Note
    #
    # Important note text
    # ...
    #
    # Creation Date: 2022-10-25 09:32:00 +0000
    # Modification Date: 2022-10-25 10:38:16 +0000
    #
    # ID: x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICNote/p5303

    # Access attributes of attachments
    attachment = note.attachments().last
    print(attachment.name)
    print(attachment.content_identifier)
    print(attachment.container)
    # Owl.png
    # cid:64D2B218-576E-405F-A147-34D2C8B86E6B@icloud.apple.com
    # <<class 'PyXA.apps.Notes.XANote'>>

Access attributes in bulk

.. code-block:: python

    PyXA
    app = PyXA.Application("Notes")

    accounts = app.accounts()
    print(accounts.name())
    print(accounts.upgraded())
    # ['iCloud']
    # [True]

    folders = app.folders()
    print(folders.name())
    print(folders.shared())
    print(folders.id())
    # ['COS 573 - Computer Vision', 'COS 598 - NLP', 'Imported Notes', 'Notes', 'Quick Notes', 'Raycast', 'Recently Deleted']
    # [False, False, False, False, False, True, False]
    # ['x-coredata://234D909C-B445-42A0-967L-380DF21392D2/ICFolder/p4176', ...]

    notes = app.notes()
    print(notes.name())
    print(notes.plaintext())
    # ['Important Note', 'PyXA 0.1.0', 'Lecture 12', 'Random Python Notes', ...]
    # ['Important Note\n\nImportant note text\n\n\n', 'PyXA 0.1.0\n\nSupport for New Applications\nAdobe Acrobat Reader\nAmphetamine\nBike\nFlow\nImage Events\niTerm\nRStudio\nSpotify\nSystem Events\n\n\nAdditions\nXALSM — A class for convenient text classification...', ...]

    attachments = app.attachments()
    print(attachments.name())
    print(attachments.url())
    # ['Pasted Graphic 1.tiff', 'Pasted Graphic 2.tiff', 'Pasted Graphic 3.tiff', 'Owl.png', ...]
    # ['https://books.apple.com/us/book/applescript/id383961702', 'https://books.apple.com/us/book/applescript-questions-and-answers-2020-edition/id1491304822', ...]

Creating New Folders, Notes, and Attachments
--------------------------------------------

.. code-block:: python

    import PyXA
    app = PyXA.Application("Notes")

    # Add a folder via push() method
    new_folder_1 = app.make("folder", {"name": "New Folder 3"})
    app.folders().push(new_folder_1)

    # Add a folder via new_folder() method
    new_folder_2 = app.new_folder("New Folder 4", account=app.accounts()[0])

    # Add a note via push() method
    new_note_1 = app.make("note", {"body": "<h1>New Note!</h1><br/>Hello, world!"})
    app.folders().by_name("New Folder 3").notes().push(new_note_1)

    # Add a note via new_note() method
    new_note_2 = app.new_note("New Note Title", "New note text", folder=new_folder_2)

    # Add an attachment to a note
    note = app.notes().by_name("Important Note")
    new_attachment = app.make("attachment", data="/Users/steven/Downloads/Important Document.pdf")
    note.attachments().push(new_attachment)

Notes Examples
##############
The examples below show some simple use cases for the Notes module that might help you spark an idea. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Notes Tutorials`).

Example 1 - Saving Safari Tab Text to a Note
********************************************

.. code-block:: python

    #!/usr/bin/env python

    import PyXA
    safari = PyXA.Application("Safari")
    current_tab = safari.front_window.current_tab
    tab_name = current_tab.name
    tab_text = current_tab.text

    notes = PyXA.Application("Notes")
    folder = notes.folders().by_name("Saved Websites")
    notes.new_note(tab_name, tab_text, folder)

For all classes, methods, and inherited members of the Notes module, see the :ref:`Notes Module Reference`.