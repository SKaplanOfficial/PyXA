""".. versionadded:: 0.0.1

Control the macOS Notes application using JXA-like syntax.
"""

from datetime import datetime
from typing import List, Union
from Foundation import NSURL, NSArray

from ScriptingBridge import SBObject

from PyXA import XABase
from PyXA import XABaseScriptable

class XANotesApplication(XABaseScriptable.XASBApplication, XABase.XACanOpenPath):
    """A class for interacting with Notes.app.

    .. seealso:: :class:`XANotesWindow`, :class:`XANote`, :class:`XANotesFolder`, :class:`XANotesAccount`

    .. versionchanged:: 0.0.3

       Added :func:`accounts`, :func:`attachments`, and related methods

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XANotesWindow
        self.default_account = self._new_element(self.xa_scel.defaultAccount(), XANotesAccount)
        self.__selection = None
        
    @property
    def selection(self) -> 'XANoteList':
        if self.__selection is None:
            self.__selection = self._new_element(self.xa_scel.selection(), XANoteList)
        return self.__selection

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
        example here

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
        >>> folder = app.new_folder("PyXA Notes")
        >>> print(folder.element_properties)
        example here

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
        """Retrieves the names of all notes in the list.

        :return: The list of names
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        """Retrieves the IDs of all notes in the list.

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def body(self) -> List[str]:
        """Retrieves the body HTML of all notes in the list.

        :return: The list of HTML strings
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("body"))

    def plaintext(self) -> List[str]:
        """Retrieves the plaintext of all notes in the list.

        :return: The list of plaintext strings
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("plaintext"))

    def creation_date(self) -> List[datetime]:
        """Retrieves the creation date of all notes in the list.

        :return: The list of creation dates
        :rtype: List[datetime]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        """Retrieves the last modification date of all notes in the list.

        :return: The list of modification dates
        :rtype: List[datetime]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def password_protected(self) -> List[bool]:
        """Retrieves the password protection status of all notes in the list.

        :return: The list of password protect statuses
        :rtype: List[bool]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def shared(self) -> List[bool]:
        """Retrieves the shared status of all notes in the list.

        :return: The list of shared statuses
        :rtype: List[bool]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> 'XANotesFolderList':
        """Retrieves the containing folder of each note in the list.

        :return: The list of folders
        :rtype: XANotesFolderList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANotesFolderList)

    def attachments(self) -> 'XANotesAttachmentList':
        """Retrieves the attachments of all notes in the list.

        :return: The list of attachments
        :rtype: XANotesAttachmentList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("attachments")
        return self._new_element(ls, XANotesAttachmentList)

    def __repr__(self):
        return str(list(zip(self.name(), self.id())))


class XANotesAccountList(XABase.XAList):
    """A wrapper around a list of accounts.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesAccount, filter)

    def name(self) -> List[str]:
        """Retrieves the name of each account in the list.

        :return: The list of names
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def upgraded(self) -> List[bool]:
        """Retrieves the upgrade status of each account in the list.

        :return: The list of upgrade statuses
        :rtype: List[bool]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("upgraded"))

    def id(self) -> List[str]:
        """Retrieves the ID of each account in the list.

        :return: The list of IDs
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def default_folder(self) -> 'XANotesFolderList':
        """Retrieves the default folder of each account in the list.

        :return: The list of default folders
        :rtype: XANotesFolderList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("defaultFolder")
        return self._new_element(ls, XANotesFolderList)

    def notes(self) -> 'XANoteList':
        """Retrieves all notes of each account in the list.

        :return: The list of notes
        :rtype: XANoteList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("notes")
        return self._new_element(ls, XANoteList)

    def folders(self) -> 'XANotesFolderList':
        """Retrieves all folders of each account in the list.

        :return: The list of folders
        :rtype: XANotesFolderList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("folders")
        return self._new_element(ls, XANotesFolderList)

    def __repr__(self):
        return str(list(zip(self.name(), self.id())))


class XANotesFolderList(XABase.XAList):
    """A wrapper around a list of Notes folders.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesFolder, filter)

    def name(self) -> List[str]:
        """Retrieves the name of each folder in the list.

        :return: The list of names
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        """Retrieves the ID of each folder in the list.

        :return: The list of IDs
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def shared(self) -> List[bool]:
        """Retrieves the shared status of each folder in the list.

        :return: The list of shared statuses
        :rtype: List[bool]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> XANotesAccountList:
        """Retrieves the containing account of each folder in the list.

        :return: The list of accounts
        :rtype: List[XANotesAccount]

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANotesAccountList)

    def notes(self) -> XANoteList:
        """Retrieves all notes of each folders in the list.

        :return: The list of notes
        :rtype: XANoteList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("notes")
        return self._new_element(ls, XANoteList)

    def __repr__(self):
        return str(list(zip(self.name(), self.id())))


class XANotesAttachmentList(XABase.XAList):
    """A wrapper around a list of attachments.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANoteAttachment, filter)

    def name(self) -> List[str]:
        """Retrieves the name of each attachment in the list.

        :return: The list of names
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        """Retrieves the ID of each attachment in the list.

        :return: The list of IDs
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def content_identifier(self) -> List[str]:
        """Retrieves the content identifier of each attachment in the list.

        :return: The list of content identifiers
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("contentIdentifier"))

    def creation_date(self) -> List[datetime]:
        """Retrieves the creation date of each attachment in the list.

        :return: The list of creation dates
        :rtype: List[datetime]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        """Retrieves the last modification date of each attachment in the list.

        :return: The list of modification dates
        :rtype: List[datetime]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def url(self) -> List[str]:
        """Retrieves the URL of each attachment in the list.

        :return: The list of URLs
        :rtype: List[str]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def shared(self) -> List[bool]:
        """Retrieves the shared status of each attachment in the list.

        :return: The list of shared statuses
        :rtype: List[bool]

        .. versionadded:: 0.0.3
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def container(self) -> XANoteList:
        """Retrieves the containing note of each attachment in the list.

        :return: The list of notes
        :rtype: XANoteList

        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XANoteList)

    def __repr__(self):
        return str(list(zip(self.name(), self.id())))


class XANotesWindow(XABase.XAWindow, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with windows of Notes.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XANotesFolder(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with Notes folders and their contents.

    .. seealso:: class:`XANote`, :class:`XABase.XACanConstructElement`

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__name: str = None #: The name of the folder
        self.__id: str = None #: The unique identifier for the folder
        self.__shared: bool = None #: Whether the folder is shared
        self.__container = None #: The account the folder belongs to

    @property
    def name(self) -> str:
        if self.__name is None:
            self.__name = self.xa_elem.name()
        return self.__name

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = self.xa_elem.id()
        return self.__id

    @property
    def shared(self) -> bool:
        if self.__shared is None:
            self.__shared = self.xa_elem.shared()
        return self.__shared

    @property
    def container(self) -> 'XANotesAccount':
        if self.__container == None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.container(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__container = XANotesAccount(properties)
        return self.__container

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


class XANote(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with notes in the Notes application.

    .. seealso:: :class:`XANotesFolder`

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__name: str = None #: The name of the note (generally the first line of the body)
        self.__id: str = None #: The unique identifier for the note
        self.__body: str = None #: The HTML content of the note
        self.__plaintext: str = None #: The plaintext content of the note
        self.__creation_date: datetime = None #: The date and time the note was created
        self.__modification_date: datetime = None #: The date and time the note was last modified
        self.__password_protected: bool = None #: Whether the note is password protected
        self.__shared: bool = None #: Whether the note is shared
        self.__container = None #: The folder that the note is in

    @property
    def name(self) -> str:
        if self.__name is None:
            self.__name = self.xa_elem.name()
        return self.__name

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = self.xa_elem.id()
        return self.__id

    @property
    def body(self) -> str:
        if self.__body is None:
            self.__body = self.xa_elem.body()
        return self.__body

    @property
    def plaintext(self) -> str:
        if self.__plaintext is None:
            self.__plaintext = self.xa_elem.plaintext()
        return self.__plaintext

    @property
    def creation_date(self) -> datetime:
        if self.__creation_date is None:
            self.__creation_date = self.xa_elem.creationDate()
        return self.__creation_date

    @property
    def modification_date(self) -> datetime:
        if self.__modification_date is None:
            self.__modification_date = self.xa_elem.modificationDate()
        return self.__modification_date

    @property
    def password_protected(self) -> bool:
        if self.__password_protected is None:
            self.__password_protected = self.xa_elem.passwordProtected()
        return self.__password_protected

    @property
    def shared(self) -> bool:
        if self.__shared is None:
            self.__shared = self.xa_elem.shared()
        return self.__shared

    @property
    def container(self) -> 'XANotesFolder':
        if self.__container == None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.container(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__container = XANotesFolder(properties)
        return self.__container

    def show(self) -> 'XANote':
        """Shows the note in the main Notes window.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> 'XANote':
        """Shows the note in a separate window.
        
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

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesAttachmentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.attachments(), XANotesAttachmentList, filter)


class XANoteAttachment(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for interacting with attachments in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__name: str = None #: The name of the attachment
        self.__id: str = None #: The unique identifier for the attachment
        self.__content_identifier: str = None #: The content ID of the attachment in the note's HTML
        self.__creation_date: datetime = None #: The date the attachment was created
        self.__modification_date: datetime = None #: The date the attachment was last modified
        self.__url: str = None #: The URL that the attachment represents, if any
        self.__shared: bool = None #: Whether the attachment is shared
        self.__container: XANote = None #: The note containing the attachment

    @property
    def name(self) -> str:
        if self.__name is None:
            self.__name = self.xa_elem.name()
        return self.__name

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = self.xa_elem.id()
        return self.__id

    @property
    def content_identifier(self) -> str:
        if self.__content_identifier is None:
            self.__content_identifier = self.xa_elem.contentIdentifier()
        return self.__content_identifier

    @property
    def creation_date(self) -> datetime:
        if self.__creation_date is None:
            self.__creation_date = self.xa_elem.creationDate()
        return self.__creation_date

    @property
    def modification_date(self) -> datetime:
        if self.__modification_date is None:
            self.__modification_date = self.xa_elem.modificationDate()
        return self.__modification_date

    @property
    def url(self) -> str:
        if self.__url is None:
            self.__url = self.xa_elem.URL()
        return self.__url

    @property
    def shared(self) -> bool:
        if self.__shared is None:
            self.__shared = self.xa_elem.shared()
        return self.__shared

    @property
    def container(self) -> 'XANote':
        if self.__container == None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.container(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__container = XANote(properties)
        return self.__container

    def show(self) -> 'XANoteAttachment':
        """Shows the attachment in the main Notes window.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> 'XANoteAttachment':
        """Shows the attachment in a separate window.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(True)
        return self


class XANotesAccount(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XAHasElements):
    """A class for interacting with accounts in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__name: str = None #: The name of the account
        self.__upgraded: bool = None #: Whether the account is upgraded
        self.__id: str = None #: The unique identifier of the account
        self.__default_folder: XANotesFolder = None #: The default folder for creating new notes

    @property
    def name(self) -> str:
        if self.__name is None:
            self.__name = self.xa_elem.name()
        return self.__name

    @property
    def upgraded(self) -> str:
        if self.__upgraded is None:
            self.__upgraded = self.xa_elem.upgraded()
        return self.__upgraded

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = self.xa_elem.id()
        return self.__id

    @property
    def default_folder(self) -> 'XANotesFolder':
        if self.__default_folder == None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.defaultFolder(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__default_folder = XANotesFolder(properties)
        return self.__default_folder

    def show(self) -> 'XANoteAttachment':
        """Shows the first folder belonging to the account.
        
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

    def folders(self, filter: Union[dict, None] = None) -> 'XANotesFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of folders
        :rtype: XANotesFolderList

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesFolderList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.folders(), XANotesFolderList, filter)