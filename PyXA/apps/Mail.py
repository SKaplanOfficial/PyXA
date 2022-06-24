""".. versionadded:: 0.0.4

Control the macOS Mail application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from pprint import pprint
from typing import List, Tuple, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray, NSArray

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XAMailApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Mail.app.

    .. versionadded:: 0.0.4
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = OSType('yes ') #: Save the file
        NO  = OSType('no  ') #: Do not save the file
        ASK = OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Mail is the active application
        self.version: str #: The version number of Mail.app
        self.always_bcc_myself: bool #: Whether the user's email address will be included in the Bcc: field of composed messages
        self.always_cc_myself: bool #: Whether the user's email address will be included in the Cc: field of composed messages
        self.selection: XAMailMessageList #: The list of messages currently selected by the user
        self.application_version: str #: The build number of Mail.app
        self.fetch_interval: int #: The number of minutes between automatic fetches for new mail (-1 = use automatically determined interval)
        self.background_activity_count: int #: The number of background activities currently running in Mail
        self.choose_signature_when_composing: bool #: Whether the user can choose a signature directly in a new compose window
        self.color_quoted_text: bool #: Whether quoted text should be colored
        self.default_message_format: str #: The default format for messages being composed
        self.download_html_attachments: bool #: Whether images and attachments in HTML messages should be downloaded and displayed
        self.drafts_mailbox: XAMailbox #: The top-level drafts mailbox
        self.expand_group_addresses: bool #: Whether group addresses should be expanded when entered into the address fields of a new message
        self.fixed_width_font: str #: The name of the font used for plain text messages
        self.fixed_width_font_size: float #: The font size for plain text messages
        self.inbox: XAMailbox #: The top-level inbox
        self.include_all_original_message_text: bool #: Whether all text of the original message will be quoted or only text the user selects
        self.quote_original_message: bool #: Whether the text of the original message should be included in replies
        self.check_spelling_while_typing: bool #: Whether spelling is checked automatically while composing messages
        self.junk_mailbox: XAMailbox #: The top-level junk mailbox
        self.level_one_quoting_color: str #; Color for quoted text with one level of indentation
        self.level_two_quoting_color: str #: Color for quoted text with two levels of indentation
        self.level_three_quoting_color: str #: Color for quoted text with three levels of indentation
        self.message_font: str #: The name of the font for messages
        self.message_font_size: float #: The font size for messages
        self.message_list_font: str #: The name of the font for the message list
        self.message_list_font_size: float #: The font size for the message list
        self.new_mail_sound: str #: The name of the sound that plays when new mail is received, or "None"
        self.outbox: XAMailbox #: The top-level outbox
        self.should_play_other_mail_sounds: bool #: Whether sounds will be played for actions and events other than receiving email
        self.same_reply_format: bool #: Whether replies will be in the same text format as the message to which the user is replying
        self.selected_signature: str #: The name of the currently selected signature (or "randomly", "sequentially", or "none")
        self.sent_mailbox: XAMailbox #: The top-level sent mailbox
        self.fetches_automatically: bool #: Whether mail will automatically be fetched a t a specific interval
        self.highlight_selected_conversation: bool #: Whether messages in conversations should be highlighted in the Mail viewer window when not grouped
        self.trash_mailbox: XAMailbox #: The top-level trash mailbox
        self.use_fixed_width_font: bool #: Whether a fixed-width font should be used for plain text messages
        self.primary_email: str #: The user's primary email address

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
    def always_bcc_myself(self) -> bool:
        return self.xa_scel.alwaysBccMyself()

    @property
    def always_cc_myself(self) -> bool:
        return self.xa_scel.alwaysCcMySelf()

    @property
    def selection(self) -> 'XAMailMessageList':
        return self._new_element(self.xa_scel.selection(), XAMailMessageList)
        
    # TODO

class XAMailWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Mail documents.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The full title of the window
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
        self.document: XAMailDocument # The current document

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @property
    def document(self) -> 'XAMailDocument':
        doc_obj = self.xa_elem.document()
        return self._new_element(doc_obj, XAMailDocument)


class XAMailMessageViewer(XABaseScriptable.XASBObject):
    """A class for managing and interacting with the message viewer window in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.drafts_mailbox: XAMailbox
        self.inbox: XAMailbox
        self.junk_mailbox: XAMailbox
        self.outbox: XAMailbox
        self.sent_mailbox: XAMailbox
        self.trash_mailbox: XAMailbox
        self.sort_column: str
        self.sorted_ascending: bool
        self.mailbox_list_visible: bool
        self.visible_columns: List[str]
        self.id: int
        self.visible_messages: List[XAMailMessage]
        self.selected_messages: List[XAMailMessage]
        self.selected_mailboxes: List[XAMailbox]
        self.window: XAMailWindow

    @property
    def drafts_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.draftsMailbox(), XAMailbox)

    @property
    def inbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.inbox(), XAMailbox)

    @property
    def junk_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.junkMailbox(), XAMailbox)

    @property
    def outbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.outbox(), XAMailbox)

    @property
    def sent_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.sentMailbox(), XAMailbox)

    @property
    def trashMailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.trashMailbox(), XAMailbox)

    @property
    def sort_column(self) -> str:
        return self.xa_elem.sortColumn()

    @property
    def sort_ascending(self) -> bool:
        return self.xa_elem.sortAscending()

    @property
    def mailbox_list_visible(self) -> bool:
        return self.xa_elem.mailboxListVisible()

    @property
    def visible_columns(self) -> List[str]:
        return self.xa_elem.visibleColumns()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def visible_messages(self) -> List['XAMailMessage']:
        return self.xa_elem.visibleMessages()

    @property
    def selected_messages(self) -> List['XAMailMessage']:
        return self.xa_elem.selectedMessages()

    @property
    def selected_mailboxes(self) -> List['XAMailbox']:
        return self.xa_elem.selectedMailboxes()

    @property
    def window(self) -> XAMailWindow:
        return self._new_element(self.xa_elem.window(), XAMailWindow)

class XAMailSignature(XABaseScriptable.XASBObject):
    """A class for managing and interacting with email signatures in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.content: XABase.XAText #: The content of the email signature
        self.name: str #: The name of the signature

    @property
    def content(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @property
    def name(self) -> str:
        return self.xa_elem.name()


class XAMailAccount(XABaseScriptable.XASBObject):
    """A class for managing and interacting with accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.delivery_account: XAMailSMTPServer #: The delivery account use when sending messages from the account
        self.name: str #: The name of the account
        self.id: str #: The unique identifier for the account
        self.password: str #: The password for the account
        self.authentication: str #: The preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none"
        self.account_type: str #: The type of the account, either: "pop", "smtp", "imap", or "iCloud"
        self.email_addresses: List[str] #: The list of email addresses associated with the account
        self.full_name: str #: The user's full name associated with the account
        self.empty_junk_messages_frequency: int #: Number of days before junk messages are deleted (0 = delete on quit, -1 = never delete)
        self.empty_trash_frequency: int #: Number of days before messages in the trash are deleted (0 = delete on quit, -1 = never delete)
        self.empty_junk_messages_on_quit: bool #: Whether messages marked as junk are deleted upon quitting Mail.app
        self.empty_trash_on_quit: bool #: Whether messages in the trash are permanently deleted upon quitting Mail.app
        self.enabled: bool #: Whether the account is enabled
        self.user_name: str #: The user name used to connect to the account
        self.account_directory: str #: The directory where the account stores items on the disk
        self.port: int #: The port used to connect to the account
        self.server_name: str #: The host named used to connect to the account
        self.move_deleted_messages_to_trash: bool #: Whether messages are moved to the trash mailbox upon deletion
        self.uses_ssl: bool #: Whether SSL is enabled for this receiving account

    @property
    def delivery_account(self) -> 'XAMailSMTPServer':
        return self._new_element(self.xa_elem.deliveryAccount(), XAMailSMTPServer)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def authentication(self) -> str:
        return self.xa_elem.authentication()

    @property
    def account_type(self) -> str:
        return self.xa_elem.accountType()

    @property
    def email_addresses(self) -> List[str]:
        return self.xa_elem.emailAddresses()

    @property
    def full_name(self) -> str:
        return self.xa_elem.fullName()

    @property
    def empty_junk_messages_frequency(self) -> int:
        return self.xa_elem.emptyJunkMessagesFrequency()

    @property
    def empty_trash_frequency(self) -> int:
        return self.xa_elem.emptyTrashFrequency()

    @property
    def empty_junk_messages_on_quit(self) -> bool:
        return self.xa_elem.emptyJunkMessagesOnQuit()

    @property
    def empty_trash_on_quit(self) -> bool:
        return self.xa_elem.emptyTrashOnQuit()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def user_name(self) -> str:
        return self.xa_elem.userName()

    @property
    def account_directory(self) -> str:
        return self.xa_elem.accountDirectory()

    @property
    def port(self) -> int:
        return self.xa_elem.port()

    @property
    def server_name(self) -> str:
        return self.xa_elem.serverName()

    @property
    def move_deleted_messages_to_trash(self) -> bool:
        return self.xa_elem.moveDeletedMessagesToTrash()

    @property
    def uses_ssl(self) -> bool:
        return self.xa_elem.usesSsl()


class XAMailIMAPAccount(XAMailAccount):
    """A class for managing and interacting with IMAP accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.compact_mailboxes_when_closing: bool #: Whether an IMAP mailbox is automatically compacted when the user quits Mail.app or switches to another mailbox
        self.message_caching: str #: The message caching setting for the account
        self.store_drafts_on_server: bool #: Whether draft messages will be stored on the IMAP server
        self.store_junk_mail_on_server: bool #: Whether junk mail will be stored on the IMAP server
        self.store_sent_messages_on_server: bool #: Whether sent messages will be stored on the IMAP server
        self.store_deleted_messages_on_server: bool #: Whether deleted messages will be stored on the IMAP server

    @property
    def compact_mailboxes_when_closing(self) -> bool:
        return self.xa_elem.compactMailboxesWhenClosing()

    @property
    def message_caching(self) -> str:
        return self.xa_elem.messageCaching()

    @property
    def store_drafts_on_server(self) -> bool:
        return self.xa_elem.storeDraftsOnServer()
    
    @property
    def store_junk_mail_on_server(self) -> bool:
        return self.xa_elem.storeJunkMailOnServer()

    @property
    def store_sent_messages_on_server(self) -> bool:
        return self.xa_elem.storeSentMessagesOnServer()

    @property
    def store_deleted_messages_on_server(self) -> bool:
        return self.xa_elem.storeDeletedMessagesOnServer()


class XAMailICloudAccount(XAMailAccount):
    """A class for managing and interacting with iCloud accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailPOPdAccount(XAMailAccount):
    """A class for managing and interacting with POP accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.big_message_warning_size: int #: The max amount of bytes a message can be before Mail will prompt the user before downloading the message (-1 = do not prompt)
        self.delayed_message_deletion_interval: int #: The number of days before messages that have been downloaded will be deleted from the server (0 = delete immediately after downloading)
        self.delete_mail_on_server: bool #: Whether the POP account deletes messages on the server after downloading
        self.delete_messages_when_moved_from_inbox: bool #: Whether messages will be deleted from the server when moved from the POP inbox

    @property
    def big_message_warning_size(self) -> int:
        return self.xa_elem.bigMessageWarningSize()

    @property
    def delayed_message_deletion_interval(self) -> int:
        return self.xa_elem.delayedMessageDeletionInterval()

    @property
    def delete_mail_on_server(self) -> bool:
        return self.xa_elem.deleteMailOnServer()

    @property
    def delete_messages_when_moved_from_inbox(self) -> bool:
        return self.xa_elem.deleteMessagesWhenMovedFromInbox()


class XAMailSMTPServer(XAMailAccount):
    """A class for managing and interacting with SMTP servers in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the account
        self.password: str #: The password for the account
        self.account_type: str #: The type of the account, either: "pop", "smtp", "imap", or "iCloud"
        self.authentication: str #: The preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none"
        self.enabled: bool #: Whether the account is enabled
        self.user_name: str #: The user name used to connect to the account
        self.port: int #: The port used to connect to the account
        self.server_name: str #: The host named used to connect to the account
        self.uses_ssl: bool #: Whether SSL is enabled for this receiving account

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def account_type(self) -> str:
        return self.xa_elem.accountType()

    @property
    def authentication(self) -> str:
        return self.xa_elem.authentication()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def user_name(self) -> str:
        return self.xa_elem.userName()

    @property
    def port(self) -> int:
        return self.xa_elem.port()

    @property
    def server_name(self) -> str:
        return self.xa_elem.serverName()

    @property
    def uses_ssl(self) -> bool:
        return self.xa_elem.usesSsl()


class XAMailDocument(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Mail documents.

    .. versionadded:: 0.0.4
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


class XAMailbox(XABaseScriptable.XASBObject):
    """A class for managing and interacting with mailboxes in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the mailbox
        self.unread_count: int #: The number of unread messages in the mailbox
        self.account: XAMailAccount #: The parent account of the mailbox
        self.container: XAMailbox #: The parent mailbox of the mailbox

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def unread_count(self) -> int:
        return self.xa_elem.unreadCount()

    @property
    def account(self) -> XAMailAccount:
        return self._new_element(self.xa_elem.account(), XAMailAccount)

    @property
    def container(self) -> 'XAMailbox':
        return self._new_element(self.xa_elem.container(), XAMailbox)


class XAMailContainer(XAMailbox):
    """A class for managing and interacting with containers in Mail.app. Containers are mailboxes that contain other mailboxes.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailMessageList(XABase.XAList):
    """A wrapper around lists of messages that employs fast enumeration techniques.

    All properties of messages can be called as methods on the wrapped list, returning a list containing each message's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    def id(self) -> List[int]:
        # Objc method caused segfault, not sure why
        return [x.id() for x in self.xa_elem]

    def all_headers(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("allHeaders"))

    def background_color(self) -> List[str]:
        return [x.backgroundColor() for x in self.xa_elem]

    def mailbox(self) -> List[XAMailbox]:
        # TODO
        return list(self.xa_elem.arrayByApplyingSelector_("mailbox"))

    def content(self) -> List[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return list(ls.arrayByApplyingSelector_("get"))

    def date_received(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dateReceived"))

    def date_sent(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dateSent"))

    def deleted_status(self) -> List[bool]:
        return [x.deletedStatus() for x in self.xa_elem]

    def flagged_status(self) -> List[bool]:
        return [x.flaggedStatus() for x in self.xa_elem]

    def flag_index(self) -> List[int]:
        return [x.flagIndex() for x in self.xa_elem]

    def junk_mail_status(self) -> List[bool]:
        return [x.junkMailStatus() for x in self.xa_elem]

    def read_status(self) -> List[bool]:
        return [x.readStatus() for x in self.xa_elem]

    def message_id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("messageId"))
    
    def source(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("source"))

    def reply_to(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("replyTo"))

    def message_size(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("messageSize"))

    def sender(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sender"))

    def subject(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subject"))

    def was_forwarded(self) -> List[bool]:
        return [x.wasForwarded() for x in self.xa_elem]

    def was_redirected(self) -> List[bool]:
        return [x.wasRedirected() for x in self.xa_elem]

    def was_replied_to(self) -> List[bool]:
        return [x.wasRepliedTo() for x in self.xa_elem]

    def by_id(self, id: int) -> 'XAMailMessage':
        return self.by_property("id", id)

    def by_all_headers(self, all_headers: str) -> 'XAMailMessage':
        return self.by_property("allHeaders", all_headers)

    def by_background_color(self, background_color: str) -> 'XAMailMessage':
        return self.by_property("backgroundColor", background_color)

    def by_mailbox(self, mailbox: XAMailbox) -> 'XAMailMessage':
        return self.by_property("mailbox", mailbox.xa_elem)

    def by_content(self, content: XABase.XAText) -> 'XAMailMessage':
        return self.by_property("content", content.xa_elem)

    def by_date_received(self, date_received: datetime) -> 'XAMailMessage':
        return self.by_property("dateReceived", date_received)

    def by_date_sent(self, date_sent: datetime) -> 'XAMailMessage':
        return self.by_property("dateSent", date_sent)

    def by_deleted_status(self, deleted_status: bool) -> 'XAMailMessage':
        return self.by_property("deletedStatus", deleted_status)

    def by_flagged_status(self, flagged_status: bool) -> 'XAMailMessage':
        return self.by_property("flaggedStatus", flagged_status)

    def by_flag_index(self, flag_index: int) -> 'XAMailMessage':
        return self.by_property("flagIndex", flag_index)

    def by_junk_mail_status(self, junk_mail_status: bool) -> 'XAMailMessage':
        return self.by_property("junkMailStatus", junk_mail_status)

    def by_read_status(self, read_status: bool) -> 'XAMailMessage':
        return self.by_property("readStatus", read_status)

    def by_message_id(self, message_id: str) -> 'XAMailMessage':
        return self.by_property("messageId", message_id)

    def by_source(self, source: str) -> 'XAMailMessage':
        return self.by_property("source", source)

    def by_reply_to(self, reply_to: str) -> 'XAMailMessage':
        return self.by_property("replyTo", reply_to)

    def by_message_size(self, message_size: int) -> 'XAMailMessage':
        return self.by_property("messageSize", message_size)

    def by_sender(self, sender: str) -> 'XAMailMessage':
        return self.by_property("sender", sender)

    def by_subject(self, subject: str) -> 'XAMailMessage':
        return self.by_property("subject", subject)

    def by_was_forwarded(self, was_forwarded: bool) -> 'XAMailMessage':
        return self.by_property("wasForwarded", was_forwarded)

    def by_was_redirected(self, was_redirected: bool) -> 'XAMailMessage':
        return self.by_property("wasRedirected", was_redirected)

    def by_was_replied_to(self, was_replied_to: bool) -> 'XAMailMessage':
        return self.by_property("wasRepliedTo", was_replied_to)

class XAMailMessage(XABaseScriptable.XASBObject):
    """A class for managing and interacting with messages in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier for the message
        self.all_headers: str #: The headers of the message
        self.background_color: str #: The background color of the message
        self.mailbox: XAMailbox #: The mailbox in which the message is located
        self.content: XABase.XAText #: The contents of the message
        self.date_received: datetime #: The date and time that the message was received
        self.date_sent: datetime #: The date and time that the message was sent
        self.deleted_status: bool #: Whether the message is deleted
        self.flagged_status: bool #: Whether the message is flagged
        self.flag_index: int #: The flag on the message, or -1 if the message is not flagged
        self.junk_mail_status: bool #: Whether the message is marked as junk
        self.read_status: bool #: Whether the message has been read
        self.message_id: str #: The unique message ID string
        self.source: str #: The raw source of the message
        self.reply_to: str #: The address that replies should be sent to
        self.message_size: int #: The size of the message in bytes
        self.sender: str #: The address of the sender of the message
        self.subject: str #: The subject string of the message
        self.was_forwarded: bool #: Whether the message was forwarded
        self.was_redirected: bool #: Whether the message was redirected
        self.was_replied_to: bool #: Whether the message was replied to

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def all_headers(self) -> str:
        return self.xa_elem.allHeaders()

    @property
    def background_color(self) -> str:
        return self.xa_elem.backroundColor()

    @property
    def mailbox(self) -> XAMailbox:
        return self._new_element(self.xa_elem.mailbox(), XAMailbox)

    @property
    def content(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @property
    def date_received(self) -> datetime:
        return self.xa_elem.dateReceived()

    @property
    def date_sent(self) -> datetime:
        return self.xa_elem.dateSent()

    @property
    def deleted_status(self) -> bool:
        return self.xa_elem.deletedStatus()

    @property
    def flagged_status(self) -> bool:
        return self.xa_elem.flaggedStatus()

    @property
    def flag_index(self) -> int:
        return self.xa_elem.flagIndex()

    @property
    def junk_mail_status(self) -> bool:
        return self.xa_elem.junkMailStatus()

    @property
    def read_status(self) -> bool:
        return self.xa_elem.readStatus()

    @property
    def message_id(self) -> int:
        return self.xa_elem.messageId()

    @property
    def source(self) -> str:
        return self.xa_elem.source()

    @property
    def reply_to(self) -> str:
        return self.xa_elem.replyTo()

    @property
    def message_size(self) -> int:
        return self.xa_elem.messageSize()

    @property
    def sender(self) -> str:
        return self.xa_elem.sender()

    @property
    def subject(self) -> str:
        return self.xa_elem.subject()

    @property
    def was_forward(self) -> bool:
        return self.xa_elem.wasForwarded()

    @property
    def was_redirected(self) -> bool:
        return self.xa_elem.wasRedirected()

    @property
    def was_replied_to(self) -> bool:
        return self.xa_elem.wasRepliedTo()

    def open(self) -> 'XAMailMessage':
        """Opens the message in a separate window.

        :return: A reference to the message object.
        :rtype: XAMailMessage

        .. versionadded:: 0.0.4
        """
        self.xa_elem.open_(self.xa_elem)
        return self

    def forward(self, open_window: bool = True) -> 'XAMailOutgoingMessage':
        msg = self.xa_elem.forwardOpeningWindow_(open_window)
        return self._new_element(msg, XAMailOutgoingMessage)

    def redirect(self, open_window: bool = True) -> 'XAMailOutgoingMessage':
        msg = self.xa_elem.redirectOpeningWindow_(open_window)
        return self._new_element(msg, XAMailOutgoingMessage)

    def reply(self, open_window: bool = True, reply_all: bool = False) -> 'XAMailOutgoingMessage':
        msg = self.xa_elem.replyOpeningWindow_replyToAll_(open_window, reply_all)
        return self._new_element(msg, XAMailOutgoingMessage)

class XAMailOutgoingMessage(XABaseScriptable.XASBObject):
    """A class for managing and interacting with outgoing messages in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.sender: str #: The address of the message sender
        self.subject: str #: The subject string of the message
        self.content: XABase.XAText #: The contents of the message
        self.visible: bool #: Whether the message window is shown on screen
        self.message_signature: XAMailSignature #: The signature of the message
        self.id: int #: The unique identifier for the message

    @property
    def sender(self) -> str:
        return self.xa_elem.sender()

    @property
    def subject(self) -> str:
        return self.xa_elem.subject()

    @property
    def content(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def message_signature(self) -> XAMailSignature:
        return self._new_element(self.xa_elem.messageSignature(). XAMailSignature)

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    def send(self) -> bool:
        return self.xa_elem.send()

    def save(self):
        # TODO
        self.xa_elem.saveIn_as_(None, None)

    def close(self, save: XAMailApplication.SaveOption = XAMailApplication.SaveOption.YES):
        self.xa_elem.closeSaving_savingIn_(save.value, None)


class XAMailRecipient(XABaseScriptable.XASBObject):
    """A class for managing and interacting with recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: str #: The recipient's email address
        self.name: str #: The name used for display

    @property
    def address(self) -> str:
        return self.xa_elem.address()

    @property
    def name(self) -> str:
        return self.xa_elem.name()


class XAMailBccRecipient(XAMailRecipient):
    """A class for managing and interacting with BCC recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailCcRecipient(XAMailRecipient):
    """A class for managing and interacting with CC recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailToRecipient(XAMailRecipient):
    """A class for managing and interacting with the primary (to) recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailHeader(XABaseScriptable.XASBObject):
    """A class for managing and interacting with message headers in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.content: str #: The contents of the header
        self.name: str #: The name of the header value

    @property
    def content(self) -> str:
        return self.xa_elem.content()

    @property
    def name(self) -> str:
        return self.xa_elem.name()


class XAMailAttachment(XABaseScriptable.XASBObject):
    """A class for managing and interacting with message attachments in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the attachment
        self.mime_type: str #: The MIME type of the attachment, e.g. text/plain
        self.file_size: int #: The approximate size of the attachment in bytes
        self.downloaded: bool #: Whether the attachment has been downloaded
        self.id: str #: The unique identifier for the attachment

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def mime_type(self) -> str:
        return self.xa_elem.mimeType()

    @property
    def file_size(self) -> int:
        return self.xa_elem.fileSize()

    @property
    def downloaded(self) -> bool:
        return self.xa_elem.downloaded()

    @property
    def id(self) -> str:
        return self.xa_elem.id()


class XAMailRuleList(XABase.XAList):
    """A wrapper around lists of rules that employs fast enumeration techniques.

    All properties of rules can be called as methods on the wrapped list, returning a list containing each rule's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    # TODO
    # def expression(self) -> List[str]:
    #     return list(self.xa_elem.arrayByApplyingSelector_("expression"))

    # def by_expression(self, expression: str) -> 'XAMailRuleCondition':
    #     return self.by_property("expression", expression)

class XAMailRule(XABaseScriptable.XASBObject):
    """A class for managing and interacting with rules in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.color_message: str #: If the rule matches, apply this color
        self.delete_message: bool #: If the rule matches, delete the message
        self.forward_text: str #: If the rule matches, prepend the provided text to the forwarded message
        self.forward_message: str #: If the rule matches, forward the message to the specified addresses, separated by commas
        self.mark_flagged: bool #: If the rule matches, mark the message as flagged
        self.mark_flag_index: int #: If the rule matches, mark the message with the specified flag (-1 = disabled)
        self.mark_read: bool #: If the rule matches, mark the message as read
        self.play_sound: str #: If the rule matches, play the sound specified by name or path
        self.redirect_message: str #: If the rule matches, redirect  the message to the supplied addresses, separated by commas
        self.reply_text: str #: If the rule matches, reply to the message and prepend the provided text
        self.run_script: str #: If the rule matches, run the supplied AppleScript file
        self.all_conditions_must_be_met: bool #: Whether all conditions must be met for the rule to execute
        self.copy_message: XAMailbox #: If the rule matches, copy the message to the specified mailbox
        self.move_message: XAMailbox #: If the rule matches, move the message to the specified mailbox
        self.highlight_text_using_color: bool #: Whether the color will be used to highlight the text of background of a message
        self.enabled: bool #: Whether the rule is enabled
        self.name: str #: The name of the rule
        self.should_copy_message: bool #: Whether the rule has a copy action
        self.should_move_message: bool #: Whether the rule has a move action
        self.stop_evaluating_rules: bool #: If the rule matches, stop rule evaluation for the message

    @property
    def color_message(self) -> str:
        return self.xa_elem.colorMessage()

    @property
    def delete_message(self) -> bool:
        return self.xa_elem.deleteMessage()

    @property
    def forward_text(self) -> str:
        return self.xa_elem.forwardText()

    @property
    def forward_message(self) -> str:
        return self.xa_elem.forwardMessage()

    @property
    def mark_flagged(self) -> bool:
        return self.xa_elem.markFlagged()

    @property
    def mark_flag_index(self) -> int:
        return self.xa_elem.markFlagIndex()

    @property
    def mark_read(self) -> bool:
        return self.xa_elem.markRead()

    @property
    def play_sound(self) -> str:
        return self.xa_elem.playSound()

    @property
    def redirect_message(self) -> str:
        return self.xa_elem.redirectMessage()

    @property
    def reply_text(self) -> str:
        return self.xa_elem.replyText()

    @property
    def run_script(self) -> str:
        return self.xa_elem.runScript()

    @property
    def all_conditions_must_be_met(self) -> bool:
        return self.xa_elem.allConditionsMustBeMet()

    @property
    def copy_message(self) -> XAMailbox:
        return self._new_element(self.xa_elem.copyMessage(), XAMailbox)

    @property
    def move_message(self) -> XAMailbox:
        return self._new_element(self.xa_elem.moveMessage(), XAMailbox)

    @property
    def hightlight_text_using_color(self) -> bool:
        return self.xa_elem.highlightTextUsingColor()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def should_copy_message(self) -> bool:
        return self.xa_elem.shouldCopyMessage()

    @property
    def should_move_message(self) -> bool:
        return self.xa_elem.shouldMoveMessage()

    @property
    def stop_evaluating_rule(self) -> bool:
        return self.xa_elem.stopEvaluatingRule()


class XAMailRuleConditionList(XABase.XAList):
    """A wrapper around lists of rule conditions that employs fast enumeration techniques.

    All properties of rule conditions can be called as methods on the wrapped list, returning a list containing each rule conditions's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    def expression(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("expression"))

    def header(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("header"))

    def qualifier(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("qualifier"))

    def rule_type(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ruleType"))

    def by_expression(self, expression: str) -> 'XAMailRuleCondition':
        return self.by_property("expression", expression)

    def by_header(self, header: str) -> 'XAMailRuleCondition':
        return self.by_property("header", header)

    def by_qualifier(self, qualifier: str) -> 'XAMailRuleCondition':
        return self.by_property("qualifier", qualifier)

    def by_rule_type(self, rule_type: str) -> 'XAMailRuleCondition':
        return self.by_property("ruleType", rule_type)

class XAMailRuleCondition(XABaseScriptable.XASBObject):
    """A class for managing and interacting with rule conditions in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.expression: str #: The rule expression field
        self.header: str #: The rule header key
        self.qualifier: str #: The qualifier for the rule
        self.rule_type: str #: The type of the rule
    
    @property
    def expression(self) -> str:
        return self.xa_elem.expression()

    @property
    def header(self) -> str:
        return self.xa_elem.header()

    @property
    def qualifier(self) -> str:
        return self.xa_elem.qualifier()

    @property
    def rule_type(self) -> str:
        return self.xa_elem.ruleType()