""".. versionadded:: 0.0.1

Control the macOS Messages application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import List, Tuple, Union

from PyXA import XABase
from PyXA import XAEvents
from PyXA import XABaseScriptable


class XAMessagesApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with Messages.app

    .. seealso:: :class:`XAChat`, :class:`XAMessagesFileTransfer`, :class:`XAMessagesParticipant`, :class:`XAMessagesAccount`

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = XABase.OSType('yes ') #: Save the file
        NO  = XABase.OSType('no  ') #: Do not save the file
        ASK = XABase.OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    class ServiceType(Enum):
        """Options for services types supported by Messages.app.
        """
        SMS         = XABase.OSType('ssms')
        IMESSAGE    = XABase.OSType('sims')

    class MessageDirection(Enum):
        """Options for the direction of a message.
        """
        INCOMING = XABase.OSType('FTic')
        OUTGOING = XABase.OSType('FTog')

    class TransferStatus(Enum):
        """Options for the transfer stage/status of a message."""
        PREPARING       = XABase.OSType('FTsp')
        WAITING         = XABase.OSType('FTsw')
        TRANSFERRING    = XABase.OSType('FTsg')
        FINALIZING      = XABase.OSType('FTsz')
        FINISHED        = XABase.OSType('FTsf')
        FAILED          = XABase.OSType('FTSe')

    class ConnectionStatus(Enum):
        """Options for the connection status of Messages.app to message transfer servers.
        """
        DISCONNECTING   = XABase.OSType('dcng')
        CONNECTED       = XABase.OSType('conn')
        CONNECTING      = XABase.OSType('cong')
        DISCONNECTED    = XABase.OSType('dcon')

    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Messages is the active application
        self.version: str #: The version of Messages.app

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def send(self, message, chat):
        self.xa_scel.send_to_(message, chat)

    def print(self, object: XABase.XAObject, show_dialog: bool = True):
        self.xa_scel.print_withProperties_printDialog_(object.xa_elem, None, show_dialog)

    def documents(self, filter: Union[dict, None] = None) -> 'XAMessagesDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.documents(), XAMessagesDocumentList, filter)

    def chats(self, filter: Union[dict, None] = None) -> 'XAMessagesChatList':
        """Returns a list of chats, as PyXA objects, matching the given filter.

        :Example 1: List all chats

        >>> import PyXA
        >>> app = PyXA.application("Messages")
        >>> print(app.chats())
        <<class 'PyXA.apps.Messages.XAMessagesChatList'>['iMessage;-;+11234567891', 'SMS;-;+12234567891', ...]

        :Example 2: List the names of all named chats

        >>> import PyXA
        >>> app = PyXA.application("Messages")
        >>> print(app.chats().name())
        ['PyXA Group', 'Dev Chat']

        :Example 3: List the information, including participants, of every chat

        >>> import PyXA
        >>> app = PyXA.application("Messages")
        >>> chats = app.chats()
        >>> for chat in chats:
        >>>     print("\n")
        >>>     print("Name:", chat.name)
        >>>     print("ID:", chat.id)
        >>>     print("Account:", chat.account)
        >>>     print("Participants:", chat.participants())
        Name: None
        ID: iMessage;-;+11234567891
        Account: <PyXA.apps.Messages.XAMessagesAccount object at 0x10871e100>
        Participants: <<class 'PyXA.apps.Messages.XAMessagesParticipantList'>['+1 (123) 456-7891']>
        ...

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.chats(), XAMessagesChatList, filter)

    def participants(self, filter: Union[dict, None] = None) -> 'XAMessagesParticipantList':
        """Returns a list of participants, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.participants(), XAMessagesParticipantList, filter)

    def accounts(self, filter: Union[dict, None] = None) -> 'XAMessagesAccountList':
        """Returns a list of accounts, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.accounts(), XAMessagesAccountList, filter)

    def file_transfers(self, filter: Union[dict, None] = None) -> 'XAMessagesFileTransferList':
        """Returns a list of file transfers, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.fileTransfers(), XAMessagesFileTransferList, filter)


class XAMessagesWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Messages windows.
    
    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XAMessagesDocument #: The document currently displayed in the window

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
    def document(self) -> 'XAMessagesDocument':
        return self._new_element(self.xa_scel.document(), XAMessagesDocument)


class XAMessagesDocumentList(XABase.XAList):
    """A wrapper around a list of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesDocument, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def by_name(self, name: str) -> 'XAMessagesDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAMessagesDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XAMessagesDocument':
        return self.by_property("file", file)

class XAMessagesDocument(XABaseScriptable.XASBObject):
    """A class for managing and interacting with documents in Messages.app.
    
    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the document
        self.modified: bool #: Whether the document has been modified since its last save
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


class XAMessagesChatList(XABase.XAList):
    """A wrapper around a list of chats that employs fast enumeration techniques.

    All properties of chats can be called as methods on the wrapped list, returning a list containing each chat's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesChat, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def account(self) -> 'XAMessagesAccountList':
        ls = self.xa_elem.arrayByApplyingSelector_("account")
        return self._new_element(ls, XAMessagesAccountList)

    def by_id(self, id: str) -> 'XAMessagesChat':
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAMessagesChat':
        return self.by_property("name", name)

    def by_account(self, account: 'XAMessagesAccount') -> 'XAMessagesChat':
        return self.by_property("account", account.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XAMessagesChat(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with chats in Messages.app
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the chat
        self.name: str #: The name of the chat as it appears in the chat list
        self.account: XAMessagesAccount #: The account that is participating in the chat

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def account(self) -> 'XAMessagesAccount':
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    def send(self, message):
        """Sends a message to the chat.

        _extended_summary_

        :param message: _description_
        :type message: _type_

        :Example 1: Send an SMS to a chat based on the chat ID

        >>> import PyXA
        >>> app = PyXA.application("Messages")
        >>> chat = app.chats().by_id("SMS;-;+11234567891")
        >>> chat.send("Hello!")

        .. versionaddedd:: 0.0.4
        """
        self.xa_prnt.xa_prnt.send(message, self.xa_elem)

    def participants(self, filter: Union[dict, None] = None) -> 'XAMessagesParticipantList':
        """Returns a list of participants, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.participants(), XAMessagesParticipantList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.participants()) + ">"


class XAMessagesFileTransferList(XABase.XAList):
    """A wrapper around a list of file transfers that employs fast enumeration techniques.

    All properties of file transfers can be called as methods on the wrapped list, returning a list containing each file transfer's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesFileTransfer, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def file_path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file_path"))

    def direction(self) -> List[XAMessagesApplication.MessageDirection]:
        ls = self.xa_elem.arrayByApplyingSelector_("direction")
        return [XAMessagesApplication.MessageDirection(x) for x in ls]

    def account(self) -> 'XAMessagesAccountList':
        ls = self.xa_elem.arrayByApplyingSelector_("account")
        return self._new_element(ls, XAMessagesAccountList)

    def account(self) -> 'XAMessagesParticipantList':
        ls = self.xa_elem.arrayByApplyingSelector_("participant")
        return self._new_element(ls, XAMessagesParticipantList)

    def file_size(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileSize"))

    def file_progress(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileProgress"))

    def transfer_status(self) -> List[XAMessagesApplication.TransferStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("transferStatus")
        return [XAMessagesApplication.TransferStatus(x) for x in ls]

    def started(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("started"))

    def by_id(self, id: str) -> 'XAMessagesFileTransfer':
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAMessagesFileTransfer':
        return self.by_property("name", name)

    def by_file_path(self, file_path: str) -> 'XAMessagesFileTransfer':
        return self.by_property("filePath", file_path)

    def by_direction(self, direction: XAMessagesApplication.MessageDirection) -> 'XAMessagesFileTransfer':
        return self.by_property("direction", direction.value)

    def by_account(self, account: 'XAMessagesAccount') -> 'XAMessagesFileTransfer':
        return self.by_property("account", account.xa_elem)

    def by_participant(self, participant: 'XAMessagesParticipant') -> 'XAMessagesFileTransfer':
        return self.by_property("participant", participant.xa_elem)

    def by_file_size(self, file_size: int) -> 'XAMessagesFileTransfer':
        return self.by_property("fileSize", file_size)

    def by_file_progress(self, file_progress: int) -> 'XAMessagesFileTransfer':
        return self.by_property("fileProgress", file_progress)

    def by_transfer_status(self, transfer_status: XAMessagesApplication.TransferStatus) -> 'XAMessagesFileTransfer':
        return self.by_property("transferStatus", transfer_status.value)

    def by_started(self, started: bool) -> 'XAMessagesFileTransfer':
        return self.by_property("started", started)

class XAMessagesFileTransfer(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with file transfers in Messages.app
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the file transfer
        self.name: str #: The name of the file
        self.file_path: str #: The local page to the file being transferred
        self.direction: XAMessagesApplication.MessageDirection #: The direction that the file is being sent
        self.account: XAMessagesAccount #: The account on which the file transfer is taking place
        self.participant: XAMessagesParticipant #: The other participant in the file transfer
        self.file_size: int #: The total size of the file transfers in bytes
        self.file_progress: int #: The number of bytes that have been transferred
        self.transfer_status: XAMessagesApplication.TransferStatus #: The current status of the file transfer
        self.started: datetime #: The date and time that the file transfer started

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def file_path(self) -> str:
        return self.xa_elem.filePath()

    @property
    def direction(self) -> XAMessagesApplication.MessageDirection:
        return XAMessagesApplication.MessageDirection(self.xa_elem.direction())

    @property
    def account(self) -> 'XAMessagesAccount':
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    @property
    def participant(self) -> 'XAMessagesParticipant':
        return self._new_element(self.xa_elem.participant(), XAMessagesParticipant)

    @property
    def file_size(self) -> int:
        return self.xa_elem.fileSize()

    @property
    def file_progress(self) -> int:
        return self.xa_elem.fileProgress()

    @property
    def transfer_status(self) -> XAMessagesApplication.TransferStatus:
        return XAMessagesApplication.TransferStatus(self.xa_elem.transferStatus())

    @property
    def started(self) -> datetime:
        return self.xa_elem.started()

    def __repr__(self):
        return self.name


class XAMessagesParticipantList(XABase.XAList):
    """A wrapper around a list of participants that employs fast enumeration techniques.

    All properties of participants can be called as methods on the wrapped list, returning a list containing each participant's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesParticipant, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def account(self) -> 'XAMessagesAccountList':
        ls = self.xa_elem.arrayByApplyingSelector_("account")
        return self._new_element(ls, XAMessagesAccountList)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def handle(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("handle"))

    def first_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("firstName"))

    def last_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("lastName"))

    def full_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullName"))

    def by_id(self, id: str) -> 'XAMessagesParticipant':
        return self.by_property("id", id)

    def by_account(self, account: 'XAMessagesAccount') -> 'XAMessagesParticipant':
        return self.by_property("account", account.xa_elem)

    def by_name(self, name: str) -> 'XAMessagesParticipant':
        return self.by_property("name", name)

    def by_handle(self, handle: str) -> 'XAMessagesParticipant':
        return self.by_property("handle", handle)

    def by_first_name(self, first_name: str) -> 'XAMessagesParticipant':
        return self.by_property("firstName", first_name)

    def by_last_name(self, last_name: str) -> 'XAMessagesParticipant':
        return self.by_property("lastName", last_name)

    def by_full_name(self, full_name: str) -> 'XAMessagesParticipant':
        return self.by_property("fullName", full_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMessagesParticipant(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with chat participants in Messages.app
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the participant
        self.account: XAMessagesAccount #: The account for the participant
        self.name: str #: The name of the participant as it appears in the participant list
        self.handle: str #: The participant's handle
        self.first_name: str #: The first name of the participant, taken from their contact card (if available)
        self.last_name: str #: The last name of the participant, taken from their contact card (if available)
        self.full_name: str #: The full name of the participant, taken from their contact card (if available)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def account(self) -> 'XAMessagesAccount':
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def handle(self) -> str:
        return self.xa_elem.handle()

    @property
    def first_name(self) -> str:
        return self.xa_elem.firstName()

    @property
    def last_name(self) -> str:
        return self.xa_elem.lastName()

    @property
    def full_name(self) -> str:
        return self.xa_elem.fullName()

    def __repr__(self):
        return "<" + str(type(self)) + self.full_name + ">"


class XAMessagesAccountList(XABase.XAList):
    """A wrapper around a list of accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesAccount, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def object_description(self) -> List[str]:
        return list(self.xa_elem.get().arrayByApplyingSelector_("objectDescription"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def connection_status(self) -> List[XAMessagesApplication.ConnectionStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("connectionStatus")
        return [XAMessagesApplication.ConnectionStatus(XABase.OSType(x.stringValue())) for x in ls]

    def service_type(self) -> List[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("serviceType")
        return [XAMessagesApplication.ServiceType(XABase.OSType(x.stringValue())) for x in ls]

    def by_id(self, id: str) -> 'XAMessagesAccount':
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> 'XAMessagesAccount':
        return self.by_property("objectDescription", object_description)

    def by_enabled(self, enabled: bool) -> 'XAMessagesAccount':
        return self.by_property("enabled", enabled)

    def by_connection_status(self, connection_status: XAMessagesApplication.ConnectionStatus) -> 'XAMessagesAccount':
        return self.by_property("connectionStatus", connection_status.value)

    def by_service_type(self, service_type: XAMessagesApplication.ServiceType) -> 'XAMessagesAccount':
        return self.by_property("serviceType", service_type.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.service_type()) + ">"


class XAMessagesAccount(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with accounts in Messages.app
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the account
        self.object_description: str #: The name of the account as defined in the Account Preferences description field
        self.enabled: bool #: Whether the account is currently enabled
        self.connection_status: XAMessagesApplication.ConnectionStatus #: The connection status for the account
        self.service_type: XAMessagesApplication.ServiceType #: The type of service for the account

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def connection_status(self) -> XAMessagesApplication.ConnectionStatus:
        return XAMessagesApplication.ConnectionStatus(self.xa_elem.connectionStatus())

    @property
    def service_type(self) -> XAMessagesApplication.ServiceType:
        return XAMessagesApplication.ServiceType(self.xa_elem.serviceType())

    def chats(self, filter: Union[dict, None] = None) -> XAMessagesChatList:
        """Returns a list of chats, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.chats(), XAMessagesChatList, filter)

    def participants(self, filter: Union[dict, None] = None) -> XAMessagesParticipantList:
        """Returns a list of participants, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.participants(), XAMessagesParticipantList, filter)