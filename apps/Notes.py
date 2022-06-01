""".. versionadded:: 0.0.1

Control the macOS Notes application using JXA-like syntax.
"""

from typing import List, Union

from XABaseScriptable import XASBApplication
from mixins.XAActions import XACanConstructElement, XAAcceptsPushedElements, XACanOpenPath

class XANotesApplication(XASBApplication, XACanConstructElement, XAAcceptsPushedElements, XACanOpenPath):
    """A class for interacting with Notes.app.

    .. seealso:: :class:`XANote`, :class:`XANoteFolder`, :class:`XASBApplication`, :class:`XACanConstructElement`, :class:`XACanOpenPath`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.default_account = self.properties["sb_element"].defaultAccount()
        self.selection = self.properties["sb_element"].selection()

    ## Notes
    def notes(self, filter: dict = None) -> List['XANote']:
        """Returns a list of notes, as PyXA objects, matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("notes", filter, XANote)

    def note(self, filter: Union[int, dict]) -> 'XANote':
        """Returns the first note matching the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_element_with_properties("notes", filter, XANote)

    def first_note(self) -> 'XANote':
        """Returns the note at the zero index of the notes array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("notes", XANote)

    def last_note(self) -> 'XANote':
        """Returns the note at the last (-1) index of the notes array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("notes", XANote)

    ## Folders
    def folders(self) -> List['XANoteFolder']:
        """Returns a list of Notes folders, as PyXA objects, matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("folders", XANoteFolder)

    def folder(self, properties: dict) -> List['XANoteFolder']:
        """Returns Notes folders matching the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_element_with_properties("folders", properties, XANoteFolder)

    def first_folder(self) -> 'XANoteFolder':
        """Returns the Notes folder at the zero index of the folders array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("folders", XANoteFolder)

    def last_folder(self) -> 'XANoteFolder':
        """Returns the Notes folder at the last (-1) index of the folders array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("folders", XANoteFolder)

    def new_note(self, name = "New Note", body = "", note_folder: 'XANoteFolder' = None) -> 'XANote':
        """Creates a new note with the given name and body text in the given folder.
        If no folder is provided, the note is created in the default Notes folder.

        :param name: The name of the note, defaults to "New Note"
        :type name: str, optional
        :param body: The initial body text of the note, defaults to ""
        :type body: str, optional
        :param note_folder: The folder to create the new note in, defaults to None
        :type note_folder: XANoteFolder, optional
        :return: A reference to the newly created note.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> note = app.new_note("PyXA Notes", "Example text of new note.")
        >>> print(note.element_properties)
        {
            shared = 0;
            1885564019 = "<NSAppleEventDescriptor: 'note'>";
            modificationDate = "2022-05-30 20:33:00 +0000";
            creationDate = "2022-05-30 20:33:00 +0000";
            id = "x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICNote/p3025";
            container = "<SBObject @0x600003a74150: <class 'cfol'> id \"x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICFolder/p1\" of application \"Notes\" (84870)>";
            plaintext = "PyXA Notes\nExample text of new note.";
            passwordProtected = 0;
            body = "<div><b>PyXA Notes</b><br></div>\n<div>Example text of new note.</div>\n";
            name = PyXA Notes;
        }

        .. seealso:: :class:`XANote`, :func:`new_folder`

        .. versionadded:: 0.0.1
        """
        if note_folder is None:
            note_folder = self
        return self.push("note", {"body": f"<b>{name}</b><br />{body}"}, note_folder.properties["sb_element"].notes())

    def new_folder(self, name: str = "New Folder") -> 'XANoteFolder':
        """Creates a new Notes folder with the given name.

        :param name: The name of the folder, defaults to "New Folder"
        :type name: str, optional
        :return: A reference to the newly created folder.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> folder = app.new_folder("PyXA Notes")
        >>> print(folder.element_properties)
        {
            id = "x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICFolder/p3026";
            1885564019 = "<NSAppleEventDescriptor: 'cfol'>";
            container = "<SBObject @0x6000032f18f0: <class 'acct'> id \"x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICAccount/p3\" of application \"Notes\" (84870)>";
            shared = 0;
            name = "Pyxa Notes";
        }

        .. seealso:: :class:`XANoteFolder`, :func:`new_note`

        .. versionadded:: 0.0.1
        """
        return self.push("folder", {"name": name}, self.properties["sb_element"].folders())


class XANoteFolder(XACanConstructElement, XAAcceptsPushedElements):
    """A class for interacting with Notes folders and their contents.

    .. seealso:: :class:`XANotesApplication`, :class:`XANote`, :class:`XACanConstructElement`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def new_note(self, name = "New Note", body = "") -> 'XANote':
        """Creates a new note with the given name and body text in this folder.

        :param name: The name of the note, defaults to "New Note"
        :type name: str, optional
        :param body: The initial body text of the note, defaults to ""
        :type body: str, optional
        :return: A reference to the newly created note.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> folder = PyXA.first_folder()
        >>> note = folder.new_note("Another Note, "Example text of new note within folder.")
        >>> print(note.element_properties)
        {
            shared = 0;
            1885564019 = "<NSAppleEventDescriptor: 'note'>";
            modificationDate = "2022-05-30 20:33:00 +0000";
            creationDate = "2022-05-30 20:33:00 +0000";
            id = "x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICNote/p3025";
            container = "<SBObject @0x600003a74150: <class 'cfol'> id \"x-coredata://214D909C-D549-42A0-96EC-380EE21392E2/ICFolder/p1\" of application \"Notes\" (84870)>";
            plaintext = "Another Note\nExample text of new note within folder.";
            passwordProtected = 0;
            body = "<div><b>Another Note</b><br></div>\n<div>Example text of new note within folder.</div>\n";
            name = PyXA Notes;
        }

        .. seealso:: :class:`XANote`

        .. versionadded:: 0.0.1
        """
        return self.push("note", {"body": f"<b>{name}</b><br />{body}"}, self.properties["element"].notes())

    def __repr__(self):
        return self.name


class XANote(XACanConstructElement, XAAcceptsPushedElements):
    """A class for interacting with notes in the Notes application.

    .. seealso:: :class:`XANotesApplication`, :class:`XANoteFolder`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)