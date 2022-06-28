""".. versionadded:: 0.0.4

Control the macOS Mail application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import List, Tuple, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA.XABase import OSType, unOSType
from PyXA import XABaseScriptable
from PyXA.XAEvents import event_from_str

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

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = OSType('lwst') #: Standard PostScript error handling
        DETAILED = OSType('lwdt') #: Detailed PostScript error handling

    class Format(Enum):
        """Options for file and message formats.
        """
        NATIVE          = OSType('item')
        PLAIN_MESSAGE   = OSType('dmpt')
        RICH_MESSAGE    = OSType('dmrt')

    class QuotingColor(Enum):
        """Options for colors to use when quoting text.
        """
        BLUE    = OSType('ccbl')
        GREEN   = OSType('ccgr')
        ORANGE  = OSType('ccor')
        OTHER   = OSType('ccot')
        PURPLE  = OSType('ccpu')
        RED     = OSType('ccre')
        YELLOW  = OSType('ccye')

    class ViewerColumn(Enum):
        """Columns in message viewer windows.
        """
        ATTACHMENTS     = OSType('ecat') #: Column containing the number of attachments a message contains
        MESSAGE_COLOR   = OSType('eccl') #: Used to indicate sorting should be done by color
        DATE_RECEIVED   = OSType('ecdr') #: Column containing the date a message was received
        DATE_SENT       = OSType('ecds') #: Column containing the date a message was sent
        FLAGS           = OSType('ecfl') #: Column containing the flags of a message
        FROM            = OSType('ecfr') #: Column containing the sender's name
        MAILBOX         = OSType('ecmb') #: Column containing the name of the mailbox or account a message is in
        MESSAGE_STATUS  = OSType('ecms') #: Column indicating a messages status (read, unread, replied to, forwarded, etc)
        NUMBER          = OSType('ecnm') #: Column containing the number of a message in a mailbox
        SIZE            = OSType('ecsz') #: Column containing the size of a message
        SUBJECT         = OSType('ecsu') #: Column containing the subject of a message
        RECIPIENTS      = OSType('ecto') #: Column containing the recipients of a message
        DATE_LAST_SAVED = OSType('ecls') #: Column containing the date a draft message was saved

    class AuthenticationMethod(Enum):
        """Options for Mail account authentication methods.
        """
        PASSWORD    = OSType('axct') #: Clear text password
        APOP        = OSType('aapo') #: APOP
        KERBEROS5   = OSType('axk5') #: Kerberos V5 (GSSAPI)
        NTLM        = OSType('axnt') #: NTLM
        MD5         = OSType('axmd') #: CRAM-MD5
        EXTERNAL    = OSType('aext') #: External authentication (TLS client certificate)
        APPLE_TOKEN = OSType('atok') #: Apple token
        NONE        = OSType('ccno') #: None

    class HighlightColor(Enum):
        """Options for colors to use when highlighting text.
        """
        BLUE    = OSType('ccbl')
        GRAY    = OSType('ccgy')
        GREEN   = OSType('ccgr')
        NONE    = OSType('ccno')
        ORANGE  = OSType('ccor')
        OTHER   = OSType('ccot')
        PURPLE  = OSType('ccpu')
        RED     = OSType('ccre')
        YELLOW  = OSType('ccye')

    class CachingPolicy(Enum):
        DO_NOT_KEEP_COPIES_OF_ANY_MESSAGES  = OSType('x9no') #: Do not use this option (deprecated). If you do, Mail will use the 'all messages but omit attachments' policy
        ONLY_MESSAGES_I_HAVE_READ           = OSType('x9wr') #: Do not use this option (deprecated). If you do, Mail will use the 'all messages but omit attachments' policy
        ALL_MESSAGES_BUT_OMIT_ATTACHMENTS   = OSType('x9bo') #: All messages but omit attachments
        ALL_MESSAGES_AND_THEIR_ATTACHMENTS  = OSType('x9al') #: All messages and their attachments

    class RuleQualifier(Enum):
        """Options for how Mail rules are qualified.
        """
        BEGINS_WITH_VALUE       = OSType('rqbw')
        DOES_CONTAIN_VALUE      = OSType('rqco')
        DOES_NOT_CONTAIN_VALUE  = OSType('rqdn')
        ENDS_WITH_VALUE         = OSType('rqew')
        EQUAL_TO_VALUE          = OSType('rqie')
        LESS_THAN_VALUE         = OSType('rqlt')
        GREATER_THAN_VALUE      = OSType('rqgt')
        NONE                    = OSType('rqno') #: Indicates no qualifier is applicable 

    class RuleType(Enum):
        """Types of rules in Mail.app.
        """
        ACCOUNT                                     = OSType('tacc') #: Account
        ANY_RECIPIENT                               = OSType('tanr') #: Any recipient
        CC_HEADER                                   = OSType('tccc') #: Cc header
        MATCHES_EVERY_MESSAGE                       = OSType('tevm') #: Every message
        FROM_HEADER                                 = OSType('tfro') #: From header
        HEADER_KEY                                  = OSType('thdk') #: An arbitrary header key
        MESSAGE_CONTENT                             = OSType('tmec') #: Message content 
        MESSAGE_IS_JUNK_MAIL                        = OSType('tmij') #: Message is junk mail 
        SENDER_IS_IN_MY_CONTACTS                    = OSType('tsii') #: Sender is in my contacts 
        SENDER_IS_IN_MY_PREVIOUS_RECIPIENTS         = OSType('tsah') #: Sender is in my previous recipients 
        SENDER_IS_MEMBER_OF_GROUP                   = OSType('tsim') #: Sender is member of group 
        SENDER_IS_NOT_IN_MY_CONTACTS                = OSType('tsin') #: Sender is not in my contacts 
        SENDER_IS_NOT_IN_MY_PREVIOUS_RECIPIENTS     = OSType('tnah') #: sender is not in my previous recipients 
        SENDER_IS_NOT_MEMBER_OF_GROUP               = OSType('tsig') #: Sender is not member of group 
        SENDER_IS_VIP                               = OSType('tsig') #: Sender is VIP 
        SUBJECT_HEADER                              = OSType('tsub') #: Subject header 
        TO_HEADER                                   = OSType('ttoo') #: To header 
        TO_OR_CC_HEADER                             = OSType('ttoc') #: To or Cc header 
        ATTACHMENT_TYPE                             = OSType('tatt') #: Attachment Type

    class AccountType(Enum):
        """Options for Mail account types.
        """
        POP     = OSType('etpo')
        SMTP    = OSType('etsm')
        IMAP    = OSType('etim')
        ICLOUD  = OSType('etit')
        UNKNOWN = OSType('etun')

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
        self.default_message_format: XAMailApplication.Format #: The default format for messages being composed
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
        self.level_one_quoting_color: XAMailApplication.QuotingColor #; Color for quoted text with one level of indentation
        self.level_two_quoting_color: XAMailApplication.QuotingColor #: Color for quoted text with two levels of indentation
        self.level_three_quoting_color: XAMailApplication.QuotingColor #: Color for quoted text with three levels of indentation
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

    @property
    def application_version(self) -> str:
        return self.xa_scel.applicationVersion()

    @property
    def fetch_interval(self) -> int:
        return self.xa_scel.fetchInterval()

    @property
    def background_activity_count(self) -> int:
        return self.xa_scel.backgroundActivityCount()

    @property
    def choose_signature_when_composing(self) -> bool:
        return self.xa_scel.chooseSignatureWhenComposing()

    @property
    def color_quoted_text(self) -> bool:
        return self.xa_scel.colorQuotedText()

    @property
    def default_message_format(self) -> 'XAMailApplication.Format':
        return XAMailApplication.Format(OSType(self.xa_scel.defaultMessageFormat().stringValue()))

    @property
    def download_html_attachments(self) -> bool:
        return self.xa_scel.downloadHtmlAttachments()

    @property
    def drafts_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.draftsMailbox(), XAMailbox)

    @property
    def expand_group_addresses(self) -> bool:
        return self.xa_scel.expandGroupAddresses()

    @property
    def fixed_width_font(self) -> str:
        return self.xa_scel.fixedWidthFont()

    @property
    def fixed_width_font_size(self) -> int:
        return self.xa_scel.fixedWidthFontSize()

    @property
    def inbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.inbox(), XAMailbox)

    @property
    def include_all_original_message_text(self) -> bool:
        return self.xa_scel.includeAllOriginalMessageText()

    @property
    def quote_original_message(self) -> bool:
        return self.xa_scel.quoteOriginalMessage()

    @property
    def check_spelling_while_typing(self) -> bool:
        return self.xa_scel.checkSpellingWhileTyping()

    @property
    def junk_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.junkMailbox(), XAMailbox)

    @property
    def level_one_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelOneQuotingColor().stringValue()))

    @property
    def level_two_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelTwoQuotingColor().stringValue()))

    @property
    def level_three_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelThreeQuotingColor().stringValue()))

    @property
    def message_font(self) -> str:
        return self.xa_scel.messageFont()

    @property
    def message_font_size(self) -> float:
        return self.xa_scel.messageFontSize()

    @property
    def message_list_font(self) -> str:
        return self.xa_scel.messageListFont()

    @property
    def message_list_font_size(self) -> float:
        return self.xa_scel.messageListFontSize()
        
    @property
    def new_mail_sound(self) -> str:
        return self.xa_scel.newMailSound()

    @property
    def outbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.outbox(), XAMailbox)

    @property
    def should_play_other_mail_sounds(self) -> bool:
        return self.xa_scel.shouldPlayOtherMailSounds()

    @property
    def same_reply_format(self) -> bool:
        return self.xa_scel.sameReplyFormat()

    @property
    def selected_signature(self) -> str:
        return self.xa_scel.selectedSignature()

    @property
    def sent_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.sentMailbox(), XAMailbox)

    @property
    def fetches_automatically(self) -> bool:
        return self.xa_scel.fetchesAutomatically()

    @property
    def highlight_selected_conversation(self) -> bool:
        return self.xa_scel.highlightSelectedConversation()

    @property
    def trash_mailbox(self) -> 'XAMailbox':
        return self._new_element(self.xa_scel.trashMailbox(), XAMailbox)

    @property
    def use_fixed_width_font(self) -> bool:
        return self.xa_scel.useFixedWidthFont()

    @property
    def primary_email(self) -> str:
        return self.xa_scel.primaryEmail()

    def check_for_new_mail(self, account: 'XAMailAccount') -> 'XAMailApplication':
        self.xa_scel.checkForNewMailFor_(account.xa_elem)
        return self

    def import_mailbox(self, file_path: Union[str, NSURL]) -> 'XAMailApplication':
        self.xa_scel.importMailMailboxAt_(file_path)
        return self

    def synchronize(self, account: 'XAMailAccount') -> 'XAMailApplication':
        self.xa_scel.synchronizeWith_(account.xa_elem)
        return self

    def accounts(self, filter: dict = None) -> 'XAMailAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.accounts(), XAMailPOPAccountList, filter)

    def pop_accounts(self, filter: dict = None) -> 'XAMailAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.popAccounts(), XAMailPOPAccountList, filter)

    def imap_accounts(self, filter: dict = None) -> 'XAMailIMAPAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.imapAccounts(), XAMailIMAPAccountList, filter)

    def imap_accounts(self, filter: dict = None) -> 'XAMailAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.icloudAccounts(), XAMailICloudAccountList, filter)

    def smtp_servers(self, filter: dict = None) -> 'XAMailAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.smtpServers(), XAMailSMTPServerList, filter)

    def outgoing_messages(self, filter: dict = None) -> 'XAMailAccountList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.outgoingMessages(), XAMailOutgoingMessageList, filter)

    def mailboxes(self, filter: dict = None) -> 'XAMailboxList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.mailboxes(), XAMailboxList, filter)

    def message_viewers(self, filter: dict = None) -> 'XAMailMessageViewerList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.messageViewers(), XAMailMessageViewerList, filter)

    def rules(self, filter: dict = None) -> 'XAMailRuleList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.rules(), XAMailRuleList, filter)

    def signatures(self, filter: dict = None) -> 'XAMailSignatureList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.signatures(), XAMailSignatureList, filter)


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


class XAMailMessageViewerList(XABase.XAList):
    """A wrapper around lists of mail signatures that employs fast enumeration techniques.

    All properties of signatures can be called as methods on the wrapped list, returning a list containing each signature's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailDocument, filter)

    def drafts_mailbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("draftsMailbox")
        return self._new_element(ls, XAMailboxList)

    def inbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("inbox")
        return self._new_element(ls, XAMailboxList)

    def junk_mailbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("junkMailbox")
        return self._new_element(ls, XAMailboxList)

    def outbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("outbox")
        return self._new_element(ls, XAMailboxList)

    def sent_mailbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("sentMailbox")
        return self._new_element(ls, XAMailboxList)

    def trash_mailbox(self) -> 'XAMailboxList':
        ls = self.xa_elem.arrayByApplyingSelector_("trashMailbox")
        return self._new_element(ls, XAMailboxList)

    def sort_column(self) -> List[XAMailApplication.ViewerColumn]:
        ls = self.xa_elem.arrayByApplyingSelector_("sortColumns")
        return [XAMailApplication.ViewerColumn(OSType(x.stringValue())) for x in ls]

    def sorted_ascending(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortedAscending"))

    def mailbox_list_visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("mailboxListVisible"))

    def preview_pane_is_visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("previewPaneIsVisible"))

    def visible_columns(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("visibleColumns"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def visible_messages(self) -> List['XAMailMessageList']:
        message_lists = self.xa_elem.arrayByApplyingSelector_("visibleMessages")
        return [self._new_element(ls, XAMailMessageList) for ls in message_lists]

    def selected_messages(self) -> List['XAMailMessageList']:
        message_lists = self.xa_elem.arrayByApplyingSelector_("selectedMessages")
        return [self._new_element(ls, XAMailMessageList) for ls in message_lists]

    def selected_mailboxes(self) -> List['XAMailboxList']:
        mailbox_lists = self.xa_elem.arrayByApplyingSelector_("selectedMailboxes")
        return [self._new_element(ls, XAMailboxList) for ls in mailbox_lists]

    def window(self) -> List[XAMailWindow]:
        # TODO: Create WindowList class (in XABase.py)
        windows = self.xa_elem.arrayByApplyingSelector_("window")
        return [self._new_element(window) for window in windows]

    def by_drafts_mailbox(self, drafts_mailbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("draftsMailbox", drafts_mailbox)

    def by_inbox(self, inbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("inbox", inbox)

    def by_junk_mailbox(self, junk_mailbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("junkMailbox", junk_mailbox)

    def by_outbox(self, outbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("outbox", outbox)

    def by_sent_mailbox(self, sent_mailbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("sentMailbox", sent_mailbox)

    def by_trash_mailbox(self, trash_mailbox: 'XAMailbox') -> 'XAMailMessageViewer':
        return self.by_property("trashMailbox", trash_mailbox.xa_elem)

    def by_sort_column(self, sort_column: XAMailApplication.ViewerColumn) -> 'XAMailMessageViewer':
        return self.by_property("sortColumn", event_from_str(unOSType(sort_column.value)))

    def by_sorted_ascending(self, sorted_ascending: bool) -> 'XAMailMessageViewer':
        return self.by_property("sortedAscending", sorted_ascending)

    def by_mailbox_list_visible(self, mailbox_list_visible: bool) -> 'XAMailMessageViewer':
        return self.by_property("mailboxListVisible", mailbox_list_visible)

    def by_preview_pane_is_visible(self, preview_pane_is_visible: bool) -> 'XAMailMessageViewer':
        return self.by_property("previewPaneIsVisible", preview_pane_is_visible)

    def by_visible_columns(self, visible_columns: List[str]) -> 'XAMailMessageViewer':
        return self.by_property("visibleColumns", visible_columns)

    def by_id(self, id: int) -> 'XAMailMessageViewer':
        return self.by_property("id", id)

    def by_visible_messages(self, visible_messages: 'XAMailMessageList') -> 'XAMailMessageViewer':
        return self.by_property("visibleMessages", visible_messages.xa_elem)

    def by_selected_messages(self, selected_messages: 'XAMailMessageList') -> 'XAMailMessageViewer':
        return self.by_property("selectedMessages", selected_messages.xa_elem)

    def by_selected_mailboxes(self, selected_mailboxes: 'XAMailboxList') -> 'XAMailMessageViewer':
        return self.by_property("selectedMailboxes", selected_mailboxes.xa_elem)

    def by_window(self, window: XAMailWindow) -> 'XAMailMessageViewer':
        return self.by_property("window", window.xa_scel)

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
        self.sort_column: XAMailApplication.ViewerColumn
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
    def sort_column(self) -> XAMailApplication.ViewerColumn:
        return XAMailApplication.ViewerColumn(OSType(self.xa_elem.sortColumn().stringValue()))

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

    def messages(self, filter: dict = None) -> 'XAMailMessageList':
        """Returns a list of messages matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.messages(), XAMailMessageList, filter)


class XAMailSignatureList(XABase.XAList):
    """A wrapper around lists of mail signatures that employs fast enumeration techniques.

    All properties of signatures can be called as methods on the wrapped list, returning a list containing each signature's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailDocument, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def content(self) -> List[XABase.XAText]:
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return self._new_element(ls, XABase.XATextList)

    def by_name(self, name: str) -> 'XAMailSignature':
        return self.by_property("name", name)

    def by_content(self, content: XABase.XAText) -> 'XAMailSignature':
        return self.by_property("content", content.xa_elem)

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

    def delete(self):
        """Permanently deletes the signature.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAMailAccountList(XABase.XAList):
    """A wrapper around lists of mail accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, object_class = None, filter: Union[dict, None] = None):
        if object_class is None:
            object_class = XAMailAccount
        super().__init__(properties, object_class, filter)

    def delivery_account(self) -> 'XAMailSMTPServerList':
        ls = self.xa_elem.arrayByApplyingSelector_("deliveryAccount")
        return self._new_element(ls, XAMailSMTPServerList)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def authentication(self) -> List[XAMailApplication.AuthenticationMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("authentication")
        return [XAMailApplication.AuthenticationMethod(OSType(x.stringValue())) for x in ls]

    def account_type(self) -> List[XAMailApplication.AccountType]:
        ls = self.xa_elem.arrayByApplyingSelector_("accountType")
        return [XAMailApplication.AccountType(OSType(x.stringValue())) for x in ls]

    def email_addresses(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("emailAddresses"))

    def full_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullName"))

    def empty_junk_messages_frequency(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("emptyJunkMessagesFrequency"))

    def empty_trash_frequency(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("emptyTrashFrequency"))

    def empty_junk_messages_on_quit(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("emptyJunkMessagesOnQuit"))

    def empty_trash_on_quit(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("emptyTrashOnQuit"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def user_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userName"))

    def account_directory(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("accountDirectory"))

    def port(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("port"))

    def server_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("serverName"))

    def move_deleted_messages_to_trash(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("moveDeletedMessagesToTrash"))

    def uses_ssl(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("usesSsl"))

    def by_delivery_account(self, delivery_account: 'XAMailSMTPServer') -> 'XAMailAccount':
        return self.by_property("deliveryAccount", delivery_account.xa_elem)

    def by_name(self, name: str) -> 'XAMailAccount':
        return self.by_property("name", name)

    def by_id(self, id: str) -> 'XAMailAccount':
        return self.by_property("id", id)

    def by_authentication(self, authentication: XAMailApplication.AuthenticationMethod) -> 'XAMailAccount':
        return self.by_property("authentication", event_from_str(unOSType(authentication.value)))

    def by_account_type(self, account_type: XAMailApplication.AccountType) -> 'XAMailAccount':
        return self.by_property("accountType", event_from_str(unOSType(account_type.value)))

    def by_email_addresses(self, email_addresses: List[str]) -> 'XAMailAccount':
        return self.by_property("emailAddresses", email_addresses)

    def by_full_name(self, full_name: str) -> 'XAMailAccount':
        return self.by_property("fullName", full_name)

    def by_empty_junk_messages_frequency(self, empty_junk_messages_frequency: int) -> 'XAMailAccount':
        return self.by_property("emptyJunkMessagesFrequency", empty_junk_messages_frequency)

    def by_empty_trash_frequency(self, empty_trash_frequency: int) -> 'XAMailAccount':
        return self.by_property("emptyTrashFrequency", empty_trash_frequency)

    def by_empty_junk_messages_on_quit(self, empty_junk_messages_on_quit: bool) -> 'XAMailAccount':
        return self.by_property("emptyJunkMessagesOnQuit", empty_junk_messages_on_quit)

    def by_empty_trash_on_quit(self, empty_trash_on_quit: bool) -> 'XAMailAccount':
        return self.by_property("emptyTrashOnQuit", empty_trash_on_quit)

    def by_enabled(self, enabled: bool) -> 'XAMailAccount':
        return self.by_property("enabled", enabled)

    def by_user_name(self, user_name: str) -> 'XAMailAccount':
        return self.by_property("userName", user_name)

    def by_account_directory(self, account_directory: str) -> 'XAMailAccount':
        return self.by_property("accountDirectory", account_directory)

    def by_port(self, port: int) -> 'XAMailAccount':
        return self.by_property("port", port)

    def by_server_name(self, server_name: str) -> 'XAMailAccount':
        return self.by_property("serverName", server_name)

    def by_move_deleted_messages_to_trash(self, move_deleted_messages_to_trash: bool) -> 'XAMailAccount':
        return self.by_property("moveDeletedMessagesToTrash", move_deleted_messages_to_trash)

    def by_uses_ssl(self, uses_ssl: bool) -> 'XAMailAccount':
        return self.by_property("usesSsl", uses_ssl)

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
        self.authentication: XAMailApplication.AuthenticationMethod #: The preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none"
        self.account_type: XAMailApplication.AccountType #: The type of the account, either: "pop", "smtp", "imap", or "iCloud"
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
    def authentication(self) -> XAMailApplication.AuthenticationMethod:
        return XAMailApplication.AuthenticationMethod(OSType(self.xa_elem.authentication().stringValue()))

    @property
    def account_type(self) -> XAMailApplication.AccountType:
        return XAMailApplication.AccountType(OSType(self.xa_elem.accountType().stringValue()))

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

    def mailboxes(self, filter: dict = None) -> 'XAMailboxList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.mailboxes(), XAMailboxList, filter)


class XAMailIMAPAccountList(XAMailAccountList):
    """A wrapper around lists of mail documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailPOPAccount, filter)

    def compact_mailboxes_when_closing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("compactMailboxesWhenClosing"))

    def message_caching(self) -> List[XAMailApplication.CachingPolicy]:
        ls = self.xa_elem.arrayByApplyingSelector_("messageCaching")
        return [XAMailApplication.CachingPolicy(OSType(x.stringValue())) for x in ls]

    def store_drafts_on_server(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeDraftsOnServer"))

    def store_junk_mail_on_server(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeJunkMailOnServer"))

    def store_sent_messages_on_server(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeSentMessagesOnServer"))

    def store_deleted_messages_on_server(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeDeletedMessagesOnServer"))

    def by_compact_mailboxes_when_closing(self, compact_mailboxes_when_closing: bool) -> 'XAMailPOPAccount':
        return self.by_property("compactMailboxesWhenClosing", compact_mailboxes_when_closing)

    def by_message_caching(self, message_caching: XAMailApplication.CachingPolicy) -> 'XAMailPOPAccount':
        return self.by_property("messageCaching", event_from_str(unOSType(message_caching.value)))

    def by_store_drafts_on_server(self, store_drafts_on_server: bool) -> 'XAMailPOPAccount':
        return self.by_property("storeDraftsOnServer", store_drafts_on_server)

    def by_store_junk_mail_on_server(self, store_junk_mail_on_server: bool) -> 'XAMailPOPAccount':
        return self.by_property("storeJunkMailOnServer", store_junk_mail_on_server)

    def by_store_sent_messages_on_server(self, store_sent_messages_on_server: bool) -> 'XAMailPOPAccount':
        return self.by_property("storeSentMessagesOnServer", store_sent_messages_on_server)

    def by_store_deleted_messages_on_server(self, store_deleted_messages_on_server: bool) -> 'XAMailPOPAccount':
        return self.by_property("storeDeletedMessagesOnServer", store_deleted_messages_on_server)

class XAMailIMAPAccount(XAMailAccount):
    """A class for managing and interacting with IMAP accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.compact_mailboxes_when_closing: bool #: Whether an IMAP mailbox is automatically compacted when the user quits Mail.app or switches to another mailbox
        self.message_caching: XAMailApplication.CachingPolicy #: The message caching setting for the account
        self.store_drafts_on_server: bool #: Whether draft messages will be stored on the IMAP server
        self.store_junk_mail_on_server: bool #: Whether junk mail will be stored on the IMAP server
        self.store_sent_messages_on_server: bool #: Whether sent messages will be stored on the IMAP server
        self.store_deleted_messages_on_server: bool #: Whether deleted messages will be stored on the IMAP server

    @property
    def compact_mailboxes_when_closing(self) -> bool:
        return self.xa_elem.compactMailboxesWhenClosing()

    @property
    def message_caching(self) -> XAMailApplication.CachingPolicy:
        return XAMailApplication.CachingPolicy(OSType(self.xa_elem.messageCaching().stringValue()))

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


class XAMailICloudAccountList(XAMailAccountList):
    """A wrapper around lists of iCloud accounts that employs fast enumeration techniques.

    All properties of iCloud accounts can be called as methods on the wrapped list, returning a list containing each accounts's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailICloudAccount, filter)

class XAMailICloudAccount(XAMailAccount):
    """A class for managing and interacting with iCloud accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailPOPAccountList(XAMailAccountList):
    """A wrapper around lists of mail documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailPOPAccount, filter)

    def big_message_warning_size(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("bigMessageWarningSize"))

    def delayed_message_deletion_interval(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("delayedMessageDeletionInterval"))

    def delete_mail_on_server(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("deleteMailOnServer"))

    def delete_messages_when_moved_from_inbox(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("deleteMessagesWhenMovedFromInbox"))

    def by_big_message_warning_size(self, big_message_warning_size: int) -> 'XAMailPOPAccount':
        return self.by_property("bigMessageWarningSize", big_message_warning_size)

    def by_delayed_message_deletion_interval(self, delayed_message_deletion_interval: int) -> 'XAMailPOPAccount':
        return self.by_property("delayedMessageDeletionInterval", delayed_message_deletion_interval)

    def by_delete_mail_on_server(self, delete_mail_on_server: bool) -> 'XAMailPOPAccount':
        return self.by_property("deleteMailOnServer", delete_mail_on_server)

    def by_delete_messages_when_moved_from_inbox(self, delete_messages_when_moved_from_inbox: bool) -> 'XAMailPOPAccount':
        return self.by_property("deleteMessagesWhenMovedFromInbox", delete_messages_when_moved_from_inbox)

class XAMailPOPAccount(XAMailAccount):
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


class XAMailSMTPServerList(XABase.XAList):
    """A wrapper around lists of SMTP servers that employs fast enumeration techniques.

    All properties of SMTP servers can be called as methods on the wrapped list, returning a list containing each SMTP server's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailSMTPServer, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def authentication(self) -> List[XAMailApplication.AuthenticationMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("authentication")
        return [XAMailApplication.AuthenticationMethod(OSType(x.stringValue())) for x in ls]

    def account_type(self) -> List[XAMailApplication.AccountType]:
        ls = self.xa_elem.arrayByApplyingSelector_("accountType")
        return [XAMailApplication.AccountType(OSType(x.stringValue())) for x in ls]

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def user_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userName"))

    def port(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("port"))

    def server_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("serverName"))

    def uses_ssl(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("usesSsl"))

    def by_name(self, name: str) -> 'XAMailAccount':
        return self.by_property("name", name)

    def by_authentication(self, authentication: XAMailApplication.AuthenticationMethod) -> 'XAMailAccount':
        return self.by_property("authentication", event_from_str(unOSType(authentication.value)))

    def by_account_type(self, account_type: XAMailApplication.AccountType) -> 'XAMailAccount':
        return self.by_property("accountType", event_from_str(unOSType(account_type.value)))

    def by_enabled(self, enabled: bool) -> 'XAMailAccount':
        return self.by_property("enabled", enabled)

    def by_user_name(self, user_name: str) -> 'XAMailAccount':
        return self.by_property("userName", user_name)

    def by_port(self, port: int) -> 'XAMailAccount':
        return self.by_property("port", port)

    def by_server_name(self, server_name: str) -> 'XAMailAccount':
        return self.by_property("serverName", server_name)

    def by_uses_ssl(self, uses_ssl: bool) -> 'XAMailAccount':
        return self.by_property("usesSsl", uses_ssl)

class XAMailSMTPServer(XAMailAccount):
    """A class for managing and interacting with SMTP servers in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the account
        self.password: str #: The password for the account
        self.account_type: XAMailApplication.AccountType #: The type of the account, either: "pop", "smtp", "imap", or "iCloud"
        self.authentication: XAMailApplication.AuthenticationMethod #: The preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none"
        self.enabled: bool #: Whether the account is enabled
        self.user_name: str #: The user name used to connect to the account
        self.port: int #: The port used to connect to the account
        self.server_name: str #: The host named used to connect to the account
        self.uses_ssl: bool #: Whether SSL is enabled for this receiving account

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def account_type(self) -> XAMailApplication.AccountType:
        return XAMailApplication.AccountType(OSType(self.xa_elem.accountType().stringValue()))

    @property
    def authentication(self) -> XAMailApplication.AuthenticationMethod:
        return XAMailApplication.AuthenticationMethod(OSType(self.xa_elem.authentication().stringValue()))

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


class XAMailDocumentList(XABase.XAList):
    """A wrapper around lists of mail documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailDocument, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def by_name(self, name: str) -> 'XAMailDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAMailDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XAMailDocument':
        return self.by_property("file", file)

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

    def delete(self):
        """Permanently deletes the document.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAMailboxList(XABase.XAList):
    """A wrapper around lists of mailboxes that employs fast enumeration techniques.

    All properties of mailboxes can be called as methods on the wrapped list, returning a list containing each mailbox's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailbox, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def unread_count(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("unread_count"))

    def account(self) -> XAMailAccountList:
        ls = self.xa_elem.arrayByApplyingSelector_("account")
        return self._new_element(ls, XAMailAccountList)

    def container(self) -> 'XAMailContainerList':
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XAMailContainerList)

    def by_name(self, name: str) -> 'XAMailbox':
        return self.by_property("name", name)

    def by_unread_count(self, unread_count: int) -> 'XAMailbox':
        return self.by_property("unreadCount", unread_count)

    def by_account(self, account: XAMailAccount) -> 'XAMailbox':
        return self.by_property("account", account.xa_elem)

    def by_container(self, container: 'XAMailContainer') -> 'XAMailbox':
        return self.by_property("container", container.xa_elem)

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

    def delete(self):
        """Permanently deletes the mailboxs.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAMailContainerList(XAMailboxList):
    """A wrapper around lists of mail headers that employs fast enumeration techniques.

    All properties of headers can be called as methods on the wrapped list, returning a list containing each header's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailContainer, filter)

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

    def background_color(self) -> List[XAMailApplication.HighlightColor]:
        ls = [x.backgroundColor() for x in self.xa_elem]
        return [XAMailApplication.HighlightColor(OSType(x.stringValue())) for x in ls]

    def mailbox(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("mailbox")
        return self._new_element(ls, XAMailboxList)

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

    def by_background_color(self, background_color: XAMailApplication.HighlightColor) -> 'XAMailMessage':
        return self.by_property("backgroundColor", event_from_str(unOSType(background_color.value)))

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
        self.background_color: XAMailApplication.HighlightColor #: The background color of the message
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
    def background_color(self) -> XAMailApplication.HighlightColor:
        return XAMailApplication.HighlightColor(OSType(self.xa_elem.backroundColor().stringValue()))

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

    def delete(self):
        """Permanently deletes the message.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def bcc_recipients(self, filter: dict = None) -> 'XAMailBccRecipientList':
        """Returns a list of Bcc recipients matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.bccRecipients(), XAMailBccRecipientList, filter)

    def cc_recpients(self, filter: dict = None) -> 'XAMailCcRecipientList':
        """Returns a list of Cc recipients matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.ccRecipients(), XAMailCcRecipientList, filter)

    def recipients(self, filter: dict = None) -> 'XAMailRecipientList':
        """Returns a list of mail recipients matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.recipients(), XAMailRecipientList, filter)

    def to_recipients(self, filter: dict = None) -> 'XAMailToRecipientList':
        """Returns a list of primary recipients matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.toRecipients(), XAMailToRecipientList, filter)

    def headers(self, filter: dict = None) -> 'XAMailHeaderList':
        """Returns a list of message headers matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.headers(), XAMailHeaderList, filter)

    def mail_attachments(self, filter: dict = None) -> 'XAMailAttachmentList':
        """Returns a list of message attachments matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.mailAttachments(), XAMailAttachmentList, filter)


class XAMailOutgoingMessageList(XABase.XAList):
    """A wrapper around lists of outgoing messages that employs fast enumeration techniques.

    All properties of outgoing messages can be called as methods on the wrapped list, returning a list containing each messages's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailHeader, filter)

    def sender(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sender"))

    def subject(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subject"))

    def content(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return self._new_element(ls, XABase.XATextList)

    def visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def message_signature(self) -> XAMailSignatureList:
        ls = self.xa_elem.arrayByApplyingSelector_("messageSignature")
        return self._new_element(ls, XAMailSignatureList)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def by_sender(self, sender: str) -> 'XAMailOutgoingMessage':
        return self.by_property("sender", sender)

    def by_subject(self, subject: str) -> 'XAMailOutgoingMessage':
        return self.by_property("subject", subject)

    def by_content(self, content: XABase.XAText) -> 'XAMailOutgoingMessage':
        return self.by_property("content", content.xa_elem)

    def by_visible(self, visible: bool) -> 'XAMailOutgoingMessage':
        return self.by_property("visible", visible)

    def by_message_signature(self, message_signature: XAMailSignature) -> 'XAMailOutgoingMessage':
        return self.by_property("messageSignature", message_signature.xa_elem)

    def by_id(self, id: int) -> 'XAMailOutgoingMessage':
        return self.by_property("id", id)

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
        self.xa_elem.saveIn_as_(None, XAMailApplication.Format.NATIVE)

    def close(self, save: XAMailApplication.SaveOption = XAMailApplication.SaveOption.YES):
        self.xa_elem.closeSaving_savingIn_(save.value, None)

    def delete(self):
        """Permanently deletes the outgoing message.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAMailRecipientList(XABase.XAList):
    """A wrapper around lists of mail recipients that employs fast enumeration techniques.

    All properties of recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, object_class = None, filter: Union[dict, None] = None):
        if object_class is None:
            object_class = XAMailRecipient
        super().__init__(properties, object_class, filter)

    def address(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_address(self, address: str) -> 'XAMailRecipient':
        return self.by_property("address", address)

    def by_name(self, name: str) -> 'XAMailRecipient':
        return self.by_property("name", name)

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


class XAMailBccRecipientList(XAMailRecipientList):
    """A wrapper around lists of mail Bcc recipients that employs fast enumeration techniques.

    All properties of Bcc recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailBccRecipient, filter)

class XAMailBccRecipient(XAMailRecipient):
    """A class for managing and interacting with BCC recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailCcRecipientList(XAMailRecipientList):
    """A wrapper around lists of mail Cc recipients that employs fast enumeration techniques.

    All properties of Cc recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailCcRecipient, filter)

class XAMailCcRecipient(XAMailRecipient):
    """A class for managing and interacting with CC recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailToRecipientList(XAMailRecipientList):
    """A wrapper around lists of mail primary (to) recipients that employs fast enumeration techniques.

    All properties of primary recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailToRecipient, filter)

class XAMailToRecipient(XAMailRecipient):
    """A class for managing and interacting with the primary (to) recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAMailHeaderList(XABase.XAList):
    """A wrapper around lists of mail headers that employs fast enumeration techniques.

    All properties of headers can be called as methods on the wrapped list, returning a list containing each header's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailHeader, filter)

    def content(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("content"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_content(self, content: str) -> 'XAMailHeader':
        return self.by_property("content", content)

    def by_name(self, name: str) -> 'XAMailHeader':
        return self.by_property("name", name)

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


class XAMailAttachmentList(XABase.XAList):
    """A wrapper around lists of attachments that employs fast enumeration techniques.

    All properties of attachments can be called as methods on the wrapped list, returning a list containing each attachment's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailAttachment, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def mime_type(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("mimeType"))

    def file_size(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileSize"))

    def downloaded(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("downloaded"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def by_name(self, name: str) -> 'XAMailAttachment':
        return self.by_property("name", name)

    def by_mime_type(self, mime_type: str) -> 'XAMailAttachment':
        return self.by_property("mimeType", mime_type)

    def by_file_size(self, file_size: int) -> 'XAMailAttachment':
        return self.by_property("fileSize", file_size)

    def by_downloaded(self, downloaded: bool) -> 'XAMailAttachment':
        return self.by_property("downloaded", downloaded)

    def by_id(self, id: str) -> 'XAMailAttachment':
        return self.by_property("id", id)

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

    def delete(self):
        """Permanently deletes the attachment.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAMailRuleList(XABase.XAList):
    """A wrapper around lists of rules that employs fast enumeration techniques.

    All properties of rules can be called as methods on the wrapped list, returning a list containing each rule's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    def color_message(self) -> List[XAMailApplication.HighlightColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("colorMessage")
        return [XAMailApplication.HighlightColor(OSType(x.stringValue())) for x in ls]

    def delete_message(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("deleteMessage"))

    def forward_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("forwardText"))

    def forward_message(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("forwardMessage"))

    def mark_flagged(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("markFlagged"))

    def mark_flag_index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("markFlagIndex"))

    def mark_read(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("markRead"))

    def play_sound(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("playSound"))

    def redirect_message(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("redirectMessage"))

    def reply_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("replyText"))

    def run_script(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("runScript"))

    def all_conditions_must_be_met(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("allConditionsMustBeMet"))

    def copy_message(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("copyMessage")
        return self._new_element(ls, XAMailboxList)

    def move_message(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("moveMessage")
        return self._new_element(ls, XAMailboxList)

    def highlight_text_using_color(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("highlightTextUsingColor"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def should_copy_message(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shouldCopyMessage"))

    def should_move_message(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shouldMoveMessage"))

    def stop_evaluating_rules(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("stopEvaluatingRules"))

    def by_color_message(self, color_message: XAMailApplication.HighlightColor) -> 'XAMailRule':
        return self.by_property("name", event_from_str(unOSType(color_message.value)))

    def by_delete_message(self, deleteMessage: bool) -> 'XAMailRule':
        return self.by_property("deleteMessage", deleteMessage)

    def by_forward_text(self, forward_text: str) -> 'XAMailRule':
        return self.by_property("forwardText", forward_text)

    def by_forward_message(self, forward_message: str) -> 'XAMailRule':
        return self.by_property("forwardMessage", forward_message)

    def by_mark_flagged(self, mark_flagged: bool) -> 'XAMailRule':
        return self.by_property("markFlagged", mark_flagged)

    def by_mark_flag_index(self, mark_flag_index: int) -> 'XAMailRule':
        return self.by_property("markFlagIndex", mark_flag_index)

    def by_mark_read(self, mark_read: bool) -> 'XAMailRule':
        return self.by_property("markRead", mark_read)

    def by_play_sound(self, play_sound: str) -> 'XAMailRule':
        return self.by_property("playSound", play_sound)

    def by_redirect_message(self, redirect_message: str) -> 'XAMailRule':
        return self.by_property("redirectMessage", redirect_message)

    def by_reply_text(self, reply_text: str) -> 'XAMailRule':
        return self.by_property("replyText", reply_text)

    def by_run_script(self, run_script: str) -> 'XAMailRule':
        return self.by_property("runScript", run_script)

    def by_all_conditions_must_be_met(self, all_conditions_must_be_met: bool) -> 'XAMailRule':
        return self.by_property("allConditionsMustBeMet", all_conditions_must_be_met)

    def by_copy_message(self, copy_message: XAMailbox) -> 'XAMailRule':
        return self.by_property("copMessage", copy_message.xa_elem)

    def by_move_message(self, move_message: XAMailbox) -> 'XAMailRule':
        return self.by_property("moveMessage", move_message.xa_elem)

    def by_highlight_text_using_color(self, highlight_text_using_color: bool) -> 'XAMailRule':
        return self.by_property("highlightTextUsingColor", highlight_text_using_color)

    def by_enabled(self, enabled: bool) -> 'XAMailRule':
        return self.by_property("enabled", enabled)

    def by_name(self, name: str) -> 'XAMailRule':
        return self.by_property("name", name)

    def by_should_copy_message(self, should_copy_message: bool) -> 'XAMailRule':
        return self.by_property("shouldCopyMessage", should_copy_message)

    def by_should_move_message(self, should_move_message: bool) -> 'XAMailRule':
        return self.by_property("shouldMoveMessage", should_move_message)

    def by_stop_evaluating_rules(self, stop_evaluating_rules: bool) -> 'XAMailRule':
        return self.by_property("stopEvaluatingRules", stop_evaluating_rules)

class XAMailRule(XABaseScriptable.XASBObject):
    """A class for managing and interacting with rules in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.color_message: XAMailApplication.HighlightColor #: If the rule matches, apply this color
        self.delete_message: bool #: If the rule matches, delete the message
        self.forward_text: str #: If the rule matches, prepend the provided text to the forwarded message
        self.forward_message: str #: If the rule matches, forward the message to the specified addresses, separated by commas
        self.mark_flagged: bool #: If the rule matches, mark the message as flagged
        self.mark_flag_index: int #: If the rule matches, mark the message with the specified flag (-1 = disabled)
        self.mark_read: bool #: If the rule matches, mark the message as read
        self.play_sound: str #: If the rule matches, play the sound specified by name or path
        self.redirect_message: str #: If the rule matches, redirect the message to the supplied addresses, separated by commas
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
    def color_message(self) -> XAMailApplication.HighlightColor:
        return XAMailApplication.HighlightColor(OSType(self.xa_elem.colorMessage().stringValue()))

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

    def delete(self):
        """Permanently deletes the rule.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def rule_conditions(self, filter: dict = None) -> 'XAMailRuleConditionList':
        """Returns a list of rule conditions matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.ruleConditions(), XAMailRuleConditionList, filter)

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

    def qualifier(self) -> List[XAMailApplication.RuleQualifier]:
        ls = self.xa_elem.arrayByApplyingSelector_("qualifier")
        return [XAMailApplication.RuleQualifier(OSType(x.stringValue())) for x in ls]

    def rule_type(self) -> List[XAMailApplication.RuleType]:
        ls = self.xa_elem.arrayByApplyingSelector_("ruleType")
        return [XAMailApplication.RuleType(OSType(x.stringValue())) for x in ls]

    def by_expression(self, expression: str) -> 'XAMailRuleCondition':
        return self.by_property("expression", expression)

    def by_header(self, header: str) -> 'XAMailRuleCondition':
        return self.by_property("header", header)

    def by_qualifier(self, qualifier: XAMailApplication.RuleQualifier) -> 'XAMailRuleCondition':
        return self.by_property("qualifier", event_from_str(unOSType(qualifier.value)))

    def by_rule_type(self, rule_type: XAMailApplication.RuleType) -> 'XAMailRuleCondition':
        return self.by_property("ruleType", event_from_str(unOSType(rule_type.value)))

class XAMailRuleCondition(XABaseScriptable.XASBObject):
    """A class for managing and interacting with rule conditions in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.expression: str #: The rule expression field
        self.header: str #: The rule header key
        self.qualifier: XAMailApplication.RuleQualifier #: The qualifier for the rule
        self.rule_type: XAMailApplication.RuleType #: The type of the rule
    
    @property
    def expression(self) -> str:
        return self.xa_elem.expression()

    @property
    def header(self) -> str:
        return self.xa_elem.header()

    @property
    def qualifier(self) -> XAMailApplication.RuleQualifier:
        return XAMailApplication.RuleQualifier(OSType(self.xa_elem.qualifier().stringValue()))

    @property
    def rule_type(self) -> XAMailApplication.RuleType:
        return XAMailApplication.RuleType(OSType(self.xa_elem.ruleType().stringValue()))

    def delete(self):
        """Permanently deletes the rule condition.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()