""".. versionadded:: 0.0.1

Control the macOS Notes application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import List, Tuple, Union
from AppKit import NSURL
from numpy import isin

from ScriptingBridge import SBElementArray

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XANotesApplication(XABaseScriptable.XASBApplication, XABase.XACanOpenPath):
    """A class for interacting with Notes.app.

    .. seealso:: :class:`XANotesWindow`, :class:`XANote`, :class:`XANotesFolder`, :class:`XANotesAccount`

    .. versionchanged:: 0.0.3

       Added :func:`accounts`, :func:`attachments`, and related methods

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = OSType('yes ') #: Save the file
        NO  = OSType('no  ') #: Do not save the file
        ASK = OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    class FileFormat(Enum):
        NATIVE = OSType('item') #: The native Notes format

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XANotesWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Notes is the active application
        self.version: str #: The version number of Notes.app
        self.default_account: XANotesAccount #: The account that new notes are created in by default
        self.selection: XANoteList #: A list of currently selected notes

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def default_account(self) -> 'XANotesAccount':
        return self._new_element(self.xa_scel.defaultAccount(), XANotesAccount)
        
    @property
    def selection(self) -> 'XANoteList':
        return self._new_element(self.xa_scel.selection(), XANoteList)

    def documents(self, filter: Union[dict, None] = None) -> 'XANotesDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.documents(), XANotesDocumentList, filter)

    def notes(self, filter: Union[dict, None] = None) -> 'XANoteList':
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        :Example 1: Retrieve the name of each note

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> print(app.notes().name())
        ['ExampleName1', 'ExampleName2', 'ExampleName3', ...]

        :Example 2: Retrieve notes by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> print(app.notes({"name": ["contains", "fancy"]}))
        [('ExampleName1', 'x-coredata://213D109C-B439-42A0-96EC-380DE31393E2/ICNote/p2964'), ('ExampleName11', 'x-coredata://213D109C-B439-42A0-96EC-380DE31393E2/ICNote/p2963'), ...]

        :Example 3: Iterate over each note

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> for note in app.notes():
        >>>     print(note.name)
        ExampleName1
        ExampleName2
        ExampleName3
        ...

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.notes(), XANoteList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XANotesFolderList':
        """Returns a list of Notes folders, as PyXA objects, matching the given filter.

        :Example 1: Retrieve the name of each folder

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> print(app.folders().name())
        ['ExampleFolder1', 'ExampleFolder2', 'ExampleFolder3', ...]

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesFolderList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.folders(), XANotesFolderList, filter)

    def accounts(self, filter: Union[dict, None] = None) -> 'XANotesAccountList':
        """Returns a list of Notes accounts, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.accounts(), XANotesAccountList, filter)

    def attachments(self, filter: Union[dict, None] = None) -> 'XANotesAttachmentList':
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.attachments(), XANotesAttachmentList, filter)
        
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
        >>> print(note)
        <<class 'PyXA.apps.Notes.XANote'>PyXA Notes, x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p3388>

        .. seealso:: :class:`XANote`, :func:`new_folder`

        .. versionadded:: 0.0.1
        """
        if note_folder is None:
            note_folder = self
        name = name.replace('\n', '<br />')
        body = body.replace('\n', '<br />')
        properties = {
            "body": f"<b>{name}</b><br />{body}",
        }
        note = self.make("note", properties)
        note_folder.notes().push(note)
        return note

    def new_folder(self, name: str = "New Folder", account: 'XANotesAccount' = None) -> 'XANotesFolder':
        """Creates a new Notes folder with the given name.

        :param name: The name of the folder, defaults to "New Folder"
        :type name: str, optional
        :return: A reference to the newly created folder.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> folder = app.new_folder("PyXA Notes Folder")
        >>> print(folder)
        <<class 'PyXA.apps.Notes.XANotesFolder'>PyXA Notes Folder, x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3389>

        .. seealso:: :class:`XANotesFolder`, :func:`new_note`

        .. versionadded:: 0.0.1
        """
        if account is None:
            account = self
        properties = {
            "name": name,
        }
        folder = self.make("folder", properties)
        account.folders().push(folder)
        return folder

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new folder and add a new note to that folder

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> new_folder = app.make("folder", {"name": "Example Folder"})
        >>> new_note = app.make("note", {"name": "Example Note"})
        >>> app.folders().push(new_folder)
        >>> new_folder.notes().push(new_note)

        .. versionadded:: 0.0.3
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "note":
            return self._new_element(obj, XANote)
        elif specifier == "account":
            return self._new_element(obj, XANotesAccount)
        elif specifier == "folder":
            return self._new_element(obj, XANotesFolder)
        elif specifier == "attachment":
            return self._new_element(obj, XANoteAttachment)


class XANoteList(XABase.XAList):
    """A wrapper around a list of notes.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANote, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def body(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("body"))

    def plaintext(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("plaintext"))

    def creation_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def password_protected(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def shared(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> 'XANotesFolderList':
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANotesFolderList)

    def attachments(self) -> 'XANotesAttachmentList':
        ls = self.xa_elem.arrayByApplyingSelector_("attachments")
        return self._new_element(ls, XANotesAttachmentList)

    def by_name(self, name: str) -> 'XANote':
        return self.by_property("name", name)

    def by_id(self, id: str) -> 'XANote':
        return self.by_property("id", id)

    def by_body(self, body: str) -> 'XANote':
        return self.by_property("body", body)

    def by_plaintext(self, plaintext: str) -> 'XANote':
        return self.by_property("plaintext", plaintext)

    def by_creation_date(self, creation_date: datetime) -> 'XANote':
        return self.by_property("creationDate", creation_date)

    def by_modification_date(self, modification_date: datetime) -> 'XANote':
        return self.by_property("modificationDate", modification_date)

    def by_password_protected(self, password_protected: bool) -> 'XANote':
        return self.by_property("passwordProtected", password_protected)

    def by_shared(self, shared: bool) -> 'XANote':
        return self.by_property("shared", shared)

    def by_container(self, container: 'XANotesFolder') -> 'XANote':
        return self.by_property("container", container.value)

    def show_separately(self) -> 'XANoteList':
        """Shows each note in the list in a separate window.

        :Example 1: Show the currently selected notes in separate windows

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> notes = app.selection.show_separately()
        
        .. versionadded:: 0.0.4
        """
        for note in self.xa_elem:
            note.showSeparately_(True)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesDocumentList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesDocument, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def by_name(self, name: str) -> 'XANotesDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XANotesDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XANotesDocument':
        return self.by_property("file", file)


class XANotesAccountList(XABase.XAList):
    """A wrapper around a list of accounts.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesAccount, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def upgraded(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("upgraded"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def default_folder(self) -> 'XANotesFolderList':
        ls = self.xa_elem.arrayByApplyingSelector_("defaultFolder")
        return self._new_element(ls, XANotesFolderList)

    def notes(self) -> 'XANoteList':
        ls = self.xa_elem.arrayByApplyingSelector_("notes")
        return self._new_element(ls, XANoteList)

    def folders(self) -> 'XANotesFolderList':
        ls = self.xa_elem.arrayByApplyingSelector_("folders")
        return self._new_element(ls, XANotesFolderList)

    def by_name(self, name: str) -> 'XANotesAccount':
        return self.by_property("name", name)

    def by_upgraded(self, upgraded: bool) -> 'XANotesAccount':
        return self.by_property("upgraded", upgraded)

    def by_id(self, id: str) -> 'XANotesAccount':
        return self.by_property("id", id)

    def by_default_folder(self, default_folder: 'XANotesFolder') -> 'XANotesAccount':
        return self.by_property("defaultFolder", default_folder.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesFolderList(XABase.XAList):
    """A wrapper around a list of Notes folders.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesFolder, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def shared(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> XANotesAccountList:
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANotesAccountList)

    def folders(self) -> 'XANotesFolderList':
        ls = self.xa_elem.arrayByApplyingSelector_("folders")
        return self._new_element(ls, XANotesFolderList)

    def notes(self) -> XANoteList:
        ls = self.xa_elem.arrayByApplyingSelector_("notes")
        return self._new_element(ls, XANoteList)

    def by_name(self, name: str) -> 'XANotesFolder':
        return self.by_property("name", name)

    def by_id(self, id: str) -> 'XANotesFolder':
        return self.by_property("id", id)

    def by_shared(self, shared: bool) -> 'XANotesFolder':
        return self.by_property("shared", shared)

    def by_container(self, container: 'XANotesAccount') -> 'XANotesFolder':
        return self.by_property("container", container.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesAttachmentList(XABase.XAList):
    """A wrapper around a list of attachments.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANoteAttachment, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def content_identifier(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("contentIdentifier"))

    def creation_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def shared(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> XANoteList:
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANoteList)

    def by_name(self, name: str) -> 'XANoteAttachment':
        return self.by_property("name", name)

    def by_id(self, id: str) -> 'XANoteAttachment':
        return self.by_property("id", id)

    def by_content_identifier(self, content_identifier: str) -> 'XANoteAttachment':
        return self.by_property("contentIdentifier", content_identifier)

    def by_creation_date(self, creation_date: datetime) -> 'XANoteAttachment':
        return self.by_property("creationDate", creation_date)

    def by_modification_date(self, modification_date: datetime) -> 'XANoteAttachment':
        return self.by_property("modificationDate", modification_date)

    def by_url(self, url: str) -> 'XANoteAttachment':
        return self.by_property("URL", url)

    def by_shared(self, shared: bool) -> 'XANoteAttachment':
        return self.by_property("shared", shared)

    def by_container(self, container: 'XANote') -> 'XANoteAttachment':
        return self.by_property("container", container.value)

    def save(self, directory: str) -> 'XANotesAttachmentList':
        """Saves all attachments in the list in the specified directory.

        :param directory: The directory to store the saved attachments in
        :type directory: str
        :return: A reference to the attachment list object
        :rtype: XANotesAttachmentList

        :Example 1: Save the attachments in currently selected notes to the downloads folder

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> app.selection.attachments().save("/Users/exampleuser/Downloads/")

        .. versionadded:: 0.0.4
        """
        for attachment_ls in self.xa_elem:
            if isinstance(attachment_ls, SBElementArray):
                for attachment in attachment_ls:
                    url = NSURL.alloc().initFileURLWithPath_(directory + attachment.name())
                    attachment.saveIn_as_(url, XANotesApplication.FileFormat.NATIVE.value)
            else:
                url = NSURL.alloc().initFileURLWithPath_(directory + attachment_ls.name())
                attachment_ls.saveIn_as_(url, XANotesApplication.FileFormat.NATIVE.value)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesWindow(XABaseScriptable.XASBWindow, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with windows of Notes.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The full title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: 'XANotesDocument' #: The active document

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def id(self) -> int:
        return self.xa_scel.id()

    @property
    def index(self) -> int:
        return self.xa_scel.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_scel.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_scel.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_scel.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_scel.miniaturized()

    @property
    def resizable(self) -> bool:
        return self.xa_scel.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_scel.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_scel.zoomed()

    @property
    def document(self) -> 'XANotesDocument':
        return self._new_element(self.xa_scel.document(), XANotesDocument)


class XANotesFolder(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with Notes folders and their contents.

    .. seealso:: class:`XANote`

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the folder
        self.id: str #: The unique identifier for the folder
        self.shared: bool #: Whether the folder is shared
        self.container: XANotesAccount #: The account the folder belongs to

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @property
    def container(self) -> 'XANotesAccount':
        return self._new_element(self.xa_elem.container(), XANotesAccount)

    def show(self) -> 'XANotesFolder':
        """Shows the folder in the main Notes window.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def notes(self, filter: Union[dict, None] = None) -> 'XANoteList':
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.notes(), XANoteList, filter)

    def delete(self):
        """Permanently deletes the folder.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"


class XANotesDocument(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with documents in Notes.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since the last save
        self.file: str #: The location of the document on the disk, if one exists

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        return self.xa_elem.file()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XANote(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with notes in the Notes application.

    .. seealso:: :class:`XANotesFolder`

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the note (generally the first line of the body)
        self.id: str #: The unique identifier for the note
        self.body: str #: The HTML content of the note
        self.plaintext: str #: The plaintext content of the note
        self.creation_date: datetime #: The date and time the note was created
        self.modification_date: datetime #: The date and time the note was last modified
        self.password_protected: bool #: Whether the note is password protected
        self.shared: bool #: Whether the note is shared
        self.container: XANotesFolder #: The folder that the note is in

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def body(self) -> str:
        return self.xa_elem.body()

    @property
    def plaintext(self) -> str:
        return self.xa_elem.plaintext()

    @property
    def creation_date(self) -> datetime:
        return self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def password_protected(self) -> bool:
        return self.xa_elem.passwordProtected()

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @property
    def container(self) -> XANotesFolder:
        return self._new_element(self.xa_elem.container(), XANotesFolder)

    def show(self) -> 'XANote':
        """Shows the note in the main Notes window.

        :return: A reference to the note object
        :rtype: XANote
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> 'XANote':
        """Shows the note in a separate window.

        :return: A reference to the note object
        :rtype: XANote
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(True)
        return self

    def attachments(self, filter: Union[dict, None] = None) -> 'XANotesAttachmentList':
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter attachments by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of attachments
        :rtype: XANotesAttachmentList
        
        :Example 1: List all attachments of a note

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> note = app.notes()[-4]
        >>> print(note.attachments())
        <<class 'PyXA.apps.Notes.XANotesAttachmentList'>[('Example.pdf, 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICAttachment/p526')]>

        :Example 2: Save the attachments of a note to the Downloads folder

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> note = app.notes()[0]
        >>> print(note.attachments().save("/Users/exampleuser/Downloads/"))

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesAttachmentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.attachments(), XANotesAttachmentList, filter)

    def delete(self):
        """Permanently deletes the note.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def move_to(self, folder: 'XANotesFolder') -> 'XANote':
        """Moves the note to the specified folder.

        :param folder: The folder to move the note to
        :type folder: XANotesFolder
        :return: A reference to the note object
        :rtype: XANote
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.moveTo_(folder.xa_elem)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"


class XANoteAttachment(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with attachments in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the attachment
        self.id: str #: The unique identifier for the attachment
        self.content_identifier: str #: The content ID of the attachment in the note's HTML
        self.creation_date: datetime #: The date the attachment was created
        self.modification_date: datetime #: The date the attachment was last modified
        self.url: str #: The URL that the attachment represents, if any
        self.shared: bool #: Whether the attachment is shared
        self.container: XANote #: The note containing the attachment

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def content_identifier(self) -> str:
        return  self.xa_elem.contentIdentifier()

    @property
    def creation_date(self) -> datetime:
        return  self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @property
    def container(self) -> 'XANote':
        return self._new_element(self.xa_elem.container(), XANote)

    def show(self) -> 'XANoteAttachment':
        """Shows the attachment in the main Notes window.

        :return: A reference to the attachment object
        :rtype: XANoteAttachment
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> 'XANoteAttachment':
        """Shows the attachment in a separate window.

        :return: A reference to the attachment object
        :rtype: XANoteAttachment
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(True)
        return self

    def save(self, directory: str) -> 'XANoteAttachment':
        """Saves the attachment to the specified directory.

        :param directory: The directory to store the saved attachment in
        :type directory: str
        :return: A reference to the attachment object
        :rtype: XANoteAttachment

        .. versionadded:: 0.0.4
        """
        url = NSURL.alloc().initFileURLWithPath_(directory + self.name)
        self.xa_elem.saveIn_as_(url, XANotesApplication.FileFormat.NATIVE.value)
        return self

    def delete(self):
        """Permanently deletes the attachment.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"


class XANotesAccount(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with accounts in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the account
        self.upgraded: bool #: Whether the account is upgraded
        self.id: str #: The unique identifier of the account
        self.default_folder: XANotesFolder #: The default folder for creating new notes

    @property
    def name(self) -> str:
        return self.xa_elem.name()
    @property
    def upgraded(self) -> bool:
        return self.xa_elem.upgraded()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def default_folder(self) -> 'XANotesFolder':
        return self._new_element(self.xa_elem.defaultFolder(), XANotesFolder)

    def show(self) -> 'XANotesAccount':
        """Shows the first folder belonging to the account.

        :return: A reference to the account object
        :rtype: XANotesAccount
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def notes(self, filter: Union[dict, None] = None) -> 'XANoteList':
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        :Example 1: List all notes belonging to an account

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> account = app.accounts()[0]
        >>> print(account.notes())
        <<class 'PyXA.apps.Notes.XANoteList'>[('PyXA Stuff', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p3380'), ('Important Note', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p614'), ...]>

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.notes(), XANoteList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XANotesFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of folders
        :rtype: XANotesFolderList

        :Example 1: List all folders belonging to an account

        >>> import PyXA
        >>> app = PyXA.application("Notes")
        >>> account = app.accounts()[0]
        >>> print(account.folders())
        <<class 'PyXA.apps.Notes.XANotesFolderList'>[('Imported Notes', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3104'), ('Notes', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3123'), ...]>

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesFolderList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.folders(), XANotesFolderList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"