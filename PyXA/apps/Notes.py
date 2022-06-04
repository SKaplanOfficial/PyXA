""".. versionadded:: 0.0.1

Control the macOS Notes application using JXA-like syntax.
"""

from typing import List, Union
from Foundation import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

class XANotesApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for interacting with Notes.app.

    .. seealso:: :class:`XANotesWindow`, :class:`XANote`, :class:`XANotesFolder`, :class:`XANotesAccount`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.properties["window_class"] = XANotesWindow
        default_account_obj = self.properties["sb_element"].defaultAccount()
        self.default_account = self._new_element(default_account_obj, XANotesAccount)

        selection_obj = self.properties["sb_element"].selection()
        self.selection = self._new_element(selection_obj, XANote)

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
    def folders(self) -> List['XANotesFolder']:
        """Returns a list of Notes folders, as PyXA objects, matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("folders", XANotesFolder)

    def folder(self, properties: dict) -> List['XANotesFolder']:
        """Returns Notes folders matching the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_element_with_properties("folders", properties, XANotesFolder)

    def first_folder(self) -> 'XANotesFolder':
        """Returns the Notes folder at the zero index of the folders array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("folders", XANotesFolder)

    def last_folder(self) -> 'XANotesFolder':
        """Returns the Notes folder at the last (-1) index of the folders array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("folders", XANotesFolder)

    def new_note(self, name = "New Note", body = "", note_folder: 'XANotesFolder' = None) -> 'XANote':
        """Creates a new note with the given name and body text in the given folder.
        If no folder is provided, the note is created in the default Notes folder.

        :param name: The name of the note, defaults to "New Note"
        :type name: str, optional
        :param body: The initial body text of the note, defaults to ""
        :type body: str, optional
        :param note_folder: The folder to create the new note in, defaults to None
        :type note_folder: XANotesFolder, optional
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
        name = name.replace("\n", "<br />")
        body = body.replace("\n", "<br />")
        return self.push("note", {"body": f"<b>{name}</b><br />{body}"}, note_folder.properties["sb_element"].notes())

    def new_folder(self, name: str = "New Folder") -> 'XANotesFolder':
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

        .. seealso:: :class:`XANotesFolder`, :func:`new_note`

        .. versionadded:: 0.0.1
        """
        return self.push("folder", {"name": name}, self.properties["sb_element"].folders())


class XANotesWindow(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with windows of Notes.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

class XANotesFolder(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with Notes folders and their contents.

    .. seealso:: class:`XANote`, :class:`XABase.XACanConstructElement`

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

    ## Notes
    def notes(self, filter: dict = None) -> List['XANote']:
        """Returns a list of notes, as PyXA objects, matching the given filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("notes", filter, XANote)

    def note(self, filter: Union[int, dict]) -> 'XANote':
        """Returns the first note matching the given filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element_with_properties("notes", filter, XANote)

    def first_note(self) -> 'XANote':
        """Returns the note at the zero index of the notes array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("notes", XANote)

    def last_note(self) -> 'XANote':
        """Returns the note at the last (-1) index of the notes array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("notes", XANote)

    def __repr__(self):
        return self.name


class XANote(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with notes in the Notes application.

    .. seealso:: :class:`XANotesFolder`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    ## Attachments
    def attachments(self, filter: dict = None) -> List['XANoteAttachment']:
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("attachments", filter, XANoteAttachment)

    def attachment(self, filter: Union[int, dict]) -> 'XANoteAttachment':
        """Returns the first attachment matching the given filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element_with_properties("attachments", filter, XANoteAttachment)

    def first_attachment(self) -> 'XANoteAttachment':
        """Returns the attachment at the zero index of the attachments array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("attachments", XANoteAttachment)

    def last_attachment(self) -> 'XANoteAttachment':
        """Returns the attachment at the last (-1) index of the attachments array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("attachments", XANoteAttachment)

class XANoteAttachment(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with attachments in the Notes application.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

class XANotesAccount(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with accounts in the Notes application.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        folder_obj = self.properties["element"].defaultFolder()
        self.default_folder = self._new_element(folder_obj, XANotesFolder)

    ## Notes
    def notes(self, filter: dict = None) -> List['XANote']:
        """Returns a list of notes, as PyXA objects, matching the given filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("notes", filter, XANote)

    def note(self, filter: Union[int, dict]) -> 'XANote':
        """Returns the first note matching the given filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element_with_properties("notes", filter, XANote)

    def first_note(self) -> 'XANote':
        """Returns the note at the zero index of the notes array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("notes", XANote)

    def last_note(self) -> 'XANote':
        """Returns the note at the last (-1) index of the notes array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("notes", XANote)

    ## Folders
    def folders(self) -> List['XANotesFolder']:
        """Returns a list of Notes folders, as PyXA objects, matching the given filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("folders", XANotesFolder)

    def folder(self, properties: dict) -> List['XANotesFolder']:
        """Returns Notes folders matching the given filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element_with_properties("folders", properties, XANotesFolder)

    def first_folder(self) -> 'XANotesFolder':
        """Returns the Notes folder at the zero index of the folders array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("folders", XANotesFolder)

    def last_folder(self) -> 'XANotesFolder':
        """Returns the Notes folder at the last (-1) index of the folders array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("folders", XANotesFolder)