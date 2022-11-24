""".. versionadded:: 0.0.4

Control the macOS Mail application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Union

import AppKit
import logging

from PyXA import XABase
from PyXA.XABase import OSType, unOSType
from PyXA import XABaseScriptable
from PyXA.XAEvents import event_from_str

logger = logging.getLogger("mail")

class XAMailApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Mail.app.

    .. versionadded:: 0.0.4
    """
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
        logger.debug("Initialized XAMailApplication")

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Mail is the active application.
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of Mail.app.
        """
        return self.xa_scel.version()

    @property
    def always_bcc_myself(self) -> bool:
        """ Whether the user's email address will be included in the Bcc: field of composed messages.
        """
        return self.xa_scel.alwaysBccMyself()

    @always_bcc_myself.setter
    def always_bcc_myself(self, always_bcc_myself: bool):
        self.set_property('alwaysBccMyself', always_bcc_myself)

    @property
    def always_cc_myself(self) -> bool:
        """Whether the user's email address will be included in the Cc: field of composed messages.
        """
        return self.xa_scel.alwaysCcMySelf()

    @always_cc_myself.setter
    def always_cc_myself(self, always_cc_myself: bool):
        self.set_property('alwaysCcMyself', always_cc_myself)

    @property
    def selection(self) -> 'XAMailMessageList':
        """The list of messages currently selected by the user.
        """
        return self._new_element(self.xa_scel.selection(), XAMailMessageList)

    @property
    def application_version(self) -> str:
        """The build number of Mail.app.
        """
        return self.xa_scel.applicationVersion()

    @property
    def fetch_interval(self) -> int:
        """The number of minutes between automatic fetches for new mail (-1 = use automatically determined interval).
        """
        return self.xa_scel.fetchInterval()

    @fetch_interval.setter
    def fetch_interval(self, fetch_interval: int):
        self.set_property('fetchInterval', fetch_interval)

    @property
    def background_activity_count(self) -> int:
        """The number of background activities currently running in Mail.
        """
        return self.xa_scel.backgroundActivityCount()

    @property
    def choose_signature_when_composing(self) -> bool:
        """Whether the user can choose a signature directly in a new compose window.
        """
        return self.xa_scel.chooseSignatureWhenComposing()

    @choose_signature_when_composing.setter
    def choose_signature_when_composing(self, choose_signature_when_composing: bool):
        self.set_property('chooseSignatureWhenComposing', choose_signature_when_composing)

    @property
    def color_quoted_text(self) -> bool:
        """Whether quoted text should be colored.
        """
        return self.xa_scel.colorQuotedText()

    @color_quoted_text.setter
    def color_quoted_text(self, color_quoted_text: bool):
        self.set_property('colorQuotedText', color_quoted_text)

    @property
    def default_message_format(self) -> 'XAMailApplication.Format':
        """The default format for messages being composed.
        """
        return XAMailApplication.Format(OSType(self.xa_scel.defaultMessageFormat().stringValue()))

    @default_message_format.setter
    def default_message_format(self, default_message_format: 'XAMailApplication.Format'):
        self.set_property('defaultMessageFormat', default_message_format.value)

    @property
    def download_html_attachments(self) -> bool:
        """Whether images and attachments in HTML messages should be downloaded and displayed.
        """
        return self.xa_scel.downloadHtmlAttachments()

    @download_html_attachments.setter
    def download_html_attachments(self, download_html_attachments: bool):
        self.set_property('downloadHtmlAttachments', download_html_attachments)

    @property
    def drafts_mailbox(self) -> 'XAMailbox':
        """The top-level drafts mailbox.
        """
        return self._new_element(self.xa_scel.draftsMailbox(), XAMailbox)

    @property
    def expand_group_addresses(self) -> bool:
        """Whether group addresses should be expanded when entered into the address fields of a new message.
        """
        return self.xa_scel.expandGroupAddresses()

    @expand_group_addresses.setter
    def expand_group_addresses(self, expand_group_addresses: bool):
        self.set_property('expandGroupAddresses', expand_group_addresses)

    @property
    def fixed_width_font(self) -> str:
        """The name of the font used for plain text messages.
        """
        return self.xa_scel.fixedWidthFont()

    @fixed_width_font.setter
    def fixed_width_font(self, fixed_width_font: str):
        self.set_property('fixedWidthFont', fixed_width_font)

    @property
    def fixed_width_font_size(self) -> int:
        """The font size for plain text messages.
        """
        return self.xa_scel.fixedWidthFontSize()

    @fixed_width_font_size.setter
    def fixed_width_font_size(self, fixed_width_font_size: int):
        self.set_property('fixedWidthFontSize', fixed_width_font_size)

    @property
    def inbox(self) -> 'XAMailbox':
        """The top-level inbox.
        """
        return self._new_element(self.xa_scel.inbox(), XAMailbox)

    @property
    def include_all_original_message_text(self) -> bool:
        """Whether all text of the original message will be quoted or only text the user selects.
        """
        return self.xa_scel.includeAllOriginalMessageText()

    @include_all_original_message_text.setter
    def include_all_original_message_text(self, include_all_original_message_text: bool):
        self.set_property('includeAllOriginalMessageText', include_all_original_message_text)

    @property
    def quote_original_message(self) -> bool:
        """Whether the text of the original message should be included in replies.
        """
        return self.xa_scel.quoteOriginalMessage()

    @quote_original_message.setter
    def quote_original_message(self, quote_original_message: bool):
        self.set_property('quoteOriginalMessage', quote_original_message)

    @property
    def check_spelling_while_typing(self) -> bool:
        """Whether spelling is checked automatically while composing messages.
        """
        return self.xa_scel.checkSpellingWhileTyping()

    @check_spelling_while_typing.setter
    def check_spelling_while_typing(self, check_spelling_while_typing: bool):
        self.set_property('checkSpellingWhileTyping', check_spelling_while_typing)

    @property
    def junk_mailbox(self) -> 'XAMailbox':
        """The top-level junk mailbox.
        """
        return self._new_element(self.xa_scel.junkMailbox(), XAMailbox)

    @property
    def level_one_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        """Color for quoted text with one level of indentation.
        """
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelOneQuotingColor().stringValue()))

    @level_one_quoting_color.setter
    def level_one_quoting_color(self, level_one_quoting_color: 'XAMailApplication.QuotingColor'):
        self.set_property('levelOneQuotingColor', level_one_quoting_color)

    @property
    def level_two_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        """Color for quoted text with two levels of indentation.
        """
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelTwoQuotingColor().stringValue()))

    @level_two_quoting_color.setter
    def level_two_quoting_color(self, level_two_quoting_color: 'XAMailApplication.QuotingColor'):
        self.set_property('levelTwoQuotingColor', level_two_quoting_color)

    @property
    def level_three_quoting_color(self) -> 'XAMailApplication.QuotingColor':
        """Color for quoted text with three levels of indentation.
        """
        return XAMailApplication.QuotingColor(OSType(self.xa_scel.levelThreeQuotingColor().stringValue()))

    @level_three_quoting_color.setter
    def level_three_quoting_color(self, level_three_quoting_color: 'XAMailApplication.QuotingColor'):
        self.set_property('levelThreeQuotingColor', level_three_quoting_color)

    @property
    def message_font(self) -> str:
        """The name of the font for messages.
        """
        return self.xa_scel.messageFont()

    @message_font.setter
    def message_font(self, message_font: str):
        self.set_property('messageFont', message_font)

    @property
    def message_font_size(self) -> float:
        """The font size for messages.
        """
        return self.xa_scel.messageFontSize()

    @message_font_size.setter
    def message_font_size(self, message_font_size: int):
        self.set_property('messageFontSize', message_font_size)

    @property
    def message_list_font(self) -> str:
        """The name of the font for the message list.
        """
        return self.xa_scel.messageListFont()

    @message_list_font.setter
    def message_list_font(self, message_list_font: str):
        self.set_property('messageListFont', message_list_font)

    @property
    def message_list_font_size(self) -> float:
        """The font size for the message list.
        """
        return self.xa_scel.messageListFontSize()

    @message_list_font_size.setter
    def message_list_font_size(self, message_list_font_size: int):
        self.set_property('messageListFontSize', message_list_font_size)
        
    @property
    def new_mail_sound(self) -> str:
        """The name of the sound that plays when new mail is received, or "None".
        """
        return self.xa_scel.newMailSound()

    @new_mail_sound.setter
    def new_mail_sound(self, new_mail_sound: str):
        self.set_property('newMailSound', new_mail_sound)

    @property
    def outbox(self) -> 'XAMailbox':
        """The top-level outbox.
        """
        return self._new_element(self.xa_scel.outbox(), XAMailbox)

    @property
    def should_play_other_mail_sounds(self) -> bool:
        """Whether sounds will be played for actions and events other than receiving email.
        """
        return self.xa_scel.shouldPlayOtherMailSounds()

    @should_play_other_mail_sounds.setter
    def should_play_other_mail_sounds(self, should_play_other_mail_sounds: bool):
        self.set_property('shouldPlayOtherMailSounds', should_play_other_mail_sounds)

    @property
    def same_reply_format(self) -> bool:
        """Whether replies will be in the same text format as the message to which the user is replying.
        """
        return self.xa_scel.sameReplyFormat()

    @same_reply_format.setter
    def same_reply_format(self, same_reply_format: bool):
        self.set_property('sameReplyFormat', same_reply_format)

    @property
    def selected_signature(self) -> str:
        """The name of the currently selected signature (or "randomly", "sequentially", or "none").
        """
        return self.xa_scel.selectedSignature()

    @selected_signature.setter
    def selected_signature(self, selected_signature: str):
        self.set_property('selectedSignature', selected_signature)

    @property
    def sent_mailbox(self) -> 'XAMailbox':
        """The top-level sent mailbox.
        """
        return self._new_element(self.xa_scel.sentMailbox(), XAMailbox)

    @property
    def fetches_automatically(self) -> bool:
        """Whether mail will automatically be fetched at a specific interval.
        """
        return self.xa_scel.fetchesAutomatically()

    @fetches_automatically.setter
    def fetches_automatically(self, fetches_automatically: bool):
        self.set_property('fetchesAutomatically', fetches_automatically)

    @property
    def highlight_selected_conversation(self) -> bool:
        """Whether messages in conversations should be highlighted in the Mail viewer window when not grouped.
        """
        return self.xa_scel.highlightSelectedConversation()

    @highlight_selected_conversation.setter
    def highlight_selected_conversation(self, highlight_selected_conversation: bool):
        self.set_property('highlightSelectedConversation', highlight_selected_conversation)

    @property
    def trash_mailbox(self) -> 'XAMailbox':
        """The top-level trash mailbox.
        """
        return self._new_element(self.xa_scel.trashMailbox(), XAMailbox)

    @property
    def use_fixed_width_font(self) -> bool:
        """Whether a fixed-width font should be used for plain text messages.
        """
        return self.xa_scel.useFixedWidthFont()

    @use_fixed_width_font.setter
    def use_fixed_width_font(self, use_fixed_width_font: bool):
        self.set_property('useFixedWidthFont', use_fixed_width_font)

    @property
    def primary_email(self) -> str:
        """The user's primary email address.
        """
        return self.xa_scel.primaryEmail()

    def check_for_new_mail(self, account: 'XAMailAccount') -> 'XAMailApplication':
        self.xa_scel.checkForNewMailFor_(account.xa_elem)
        return self

    def import_mailbox(self, file_path: Union[str, AppKit.NSURL]) -> 'XAMailApplication':
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

    @property
    def document(self) -> 'XAMailDocument':
        """The current document.
        """
        doc_obj = self.xa_elem.document()
        return self._new_element(doc_obj, XAMailDocument)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailMessageViewerList(XABase.XAList):
    """A wrapper around lists of mail signatures that employs fast enumeration techniques.

    All properties of signatures can be called as methods on the wrapped list, returning a list containing each signature's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessageViewer, filter)

    def drafts_mailbox(self) -> 'XAMailboxList':
        """Gets the draft mailbox of each message viewer in the list.

        :return: A list of draft mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("draftsMailbox")
        return self._new_element(ls, XAMailboxList)

    def inbox(self) -> 'XAMailboxList':
        """Gets the inbox mailbox of each message viewer in the list.

        :return: A list of inbox mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("inbox")
        return self._new_element(ls, XAMailboxList)

    def junk_mailbox(self) -> 'XAMailboxList':
        """Gets the junk mailbox of each message viewer in the list.

        :return: A list of junk mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("junkMailbox")
        return self._new_element(ls, XAMailboxList)

    def outbox(self) -> 'XAMailboxList':
        """Gets the outbox mailbox of each message viewer in the list.

        :return: A list of outbox mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("outbox")
        return self._new_element(ls, XAMailboxList)

    def sent_mailbox(self) -> 'XAMailboxList':
        """Gets the sent mailbox of each message viewer in the list.

        :return: A list of sent mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("sentMailbox")
        return self._new_element(ls, XAMailboxList)

    def trash_mailbox(self) -> 'XAMailboxList':
        """Gets the trash mailbox of each message viewer in the list.

        :return: A list of trash mailboxes
        :rtype: XAMailboxList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("trashMailbox")
        return self._new_element(ls, XAMailboxList)

    def sort_column(self) -> list[XAMailApplication.ViewerColumn]:
        """Gets the sort column of each message viewer in the list.

        :return: A list of sort columns
        :rtype: list[XAMailApplication.ViewerColumn]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("sortColumns")
        return [XAMailApplication.ViewerColumn(OSType(x.stringValue())) for x in ls]

    def sorted_ascending(self) -> list[bool]:
        """Gets the sort ascending status of each message viewer in the list.

        :return: A list of sort ascending status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortedAscending"))

    def mailbox_list_visible(self) -> list[bool]:
        """Gets the mailbox list visible status of each message viewer in the list.

        :return: A list of mailbox list visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("mailboxListVisible"))

    def preview_pane_is_visible(self) -> list[bool]:
        """Gets the preview pane visible status of each message viewer in the list.

        :return: A list of preview pane visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("previewPaneIsVisible"))

    def visible_columns(self) -> list[list[str]]:
        """Gets the visible columns of each message viewer in the list.

        :return: A list of visible column names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visibleColumns"))

    def id(self) -> list[str]:
        """Gets the ID of each message viewer in the list.

        :return: A list of message viewer IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def visible_messages(self) -> list['XAMailMessageList']:
        """Gets the visible messages of each message viewer in the list.

        :return: A list of visible messages
        :rtype: list['XAMailMessageList']
        
        .. versionadded:: 0.0.4
        """
        message_lists = self.xa_elem.arrayByApplyingSelector_("visibleMessages")
        return [self._new_element(ls, XAMailMessageList) for ls in message_lists]

    def selected_messages(self) -> list['XAMailMessageList']:
        """Gets the selected messages of each message viewer in the list.

        :return: A list of selected messages
        :rtype: list['XAMailMessageList']
        
        .. versionadded:: 0.0.4
        """
        message_lists = self.xa_elem.arrayByApplyingSelector_("selectedMessages")
        return [self._new_element(ls, XAMailMessageList) for ls in message_lists]

    def selected_mailboxes(self) -> list['XAMailboxList']:
        """Gets the selected mailboxes of each message viewer in the list.

        :return: A list of selected mailboxes
        :rtype: list['XAMailMessageList']
        
        .. versionadded:: 0.0.4
        """
        mailbox_lists = self.xa_elem.arrayByApplyingSelector_("selectedMailboxes")
        return [self._new_element(ls, XAMailboxList) for ls in mailbox_lists]

    def window(self) -> XABaseScriptable.XASBWindowList:
        """Gets the window of each message viewer in the list.

        :return: A list of message viewer windows
        :rtype: list['XAMailMessageList']
        
        .. versionadded:: 0.0.4
        """
        windows = self.xa_elem.arrayByApplyingSelector_("window")
        return self._new_element(windows, XABaseScriptable.XASBWindowList)

    def by_drafts_mailbox(self, drafts_mailbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose drafts mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("draftsMailbox", drafts_mailbox)

    def by_inbox(self, inbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose inbox mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("inbox", inbox)

    def by_junk_mailbox(self, junk_mailbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose junk mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("junkMailbox", junk_mailbox)

    def by_outbox(self, outbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose outbox mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("outbox", outbox)

    def by_sent_mailbox(self, sent_mailbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose sent mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("sentMailbox", sent_mailbox)

    def by_trash_mailbox(self, trash_mailbox: 'XAMailbox') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose trash mailbox matches the given mailbox, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("trashMailbox", trash_mailbox.xa_elem)

    def by_sort_column(self, sort_column: XAMailApplication.ViewerColumn) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose sort column matches the given sort column, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("sortColumn", event_from_str(unOSType(sort_column.value)))

    def by_sorted_ascending(self, sorted_ascending: bool) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose sort ascending status matches the given boolean value, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("sortedAscending", sorted_ascending)

    def by_mailbox_list_visible(self, mailbox_list_visible: bool) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose mailbox list visible status matches the given boolean value, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("mailboxListVisible", mailbox_list_visible)

    def by_preview_pane_is_visible(self, preview_pane_is_visible: bool) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose preview pane visible status matches the given boolean value, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("previewPaneIsVisible", preview_pane_is_visible)

    def by_visible_columns(self, visible_columns: list[str]) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose list of visible columns matches the given list, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("visibleColumns", visible_columns)

    def by_id(self, id: int) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose ID matches the given ID, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_visible_messages(self, visible_messages: 'XAMailMessageList') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose list of visible messages matches the given list, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("visibleMessages", visible_messages.xa_elem)

    def by_selected_messages(self, selected_messages: 'XAMailMessageList') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose list of selected messages matches the given list, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("selectedMessages", selected_messages.xa_elem)

    def by_selected_mailboxes(self, selected_mailboxes: 'XAMailboxList') -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose list of selected mailboxes matches the given list, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("selectedMailboxes", selected_mailboxes.xa_elem)

    def by_window(self, window: XAMailWindow) -> Union['XAMailMessageViewer', None]:
        """Retrieves the first message viewer whose window matches the given window, if one exists.

        :return: The desired message viewer, if it is found
        :rtype: Union[XAMailMessageViewer, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("window", window.xa_scel)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XAMailMessageViewer(XABase.XAObject):
    """A class for managing and interacting with the message viewer window in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def drafts_mailbox(self) -> 'XAMailbox':
        """The top-level Drafts mailbox.
        """
        return self._new_element(self.xa_elem.draftsMailbox(), XAMailbox)

    @property
    def inbox(self) -> 'XAMailbox':
        """The top-level Inbox mailbox.
        """
        return self._new_element(self.xa_elem.inbox(), XAMailbox)

    @property
    def junk_mailbox(self) -> 'XAMailbox':
        """The top-level Junk mailbox.
        """
        return self._new_element(self.xa_elem.junkMailbox(), XAMailbox)

    @property
    def outbox(self) -> 'XAMailbox':
        """The top-level Out mailbox.
        """
        return self._new_element(self.xa_elem.outbox(), XAMailbox)

    @property
    def sent_mailbox(self) -> 'XAMailbox':
        """The top-level Sent mailbox.
        """
        return self._new_element(self.xa_elem.sentMailbox(), XAMailbox)

    @property
    def trash_mailbox(self) -> 'XAMailbox':
        """The top-level Trash mailbox.
        """
        return self._new_element(self.xa_elem.trashMailbox(), XAMailbox)

    @property
    def sort_column(self) -> XAMailApplication.ViewerColumn:
        """The column that is currently sorted in the viewer.
        """
        return XAMailApplication.ViewerColumn(OSType(self.xa_elem.sortColumn().stringValue()))

    @sort_column.setter
    def sort_column(self, sort_column: XAMailApplication.ViewerColumn):
        self.set_property('sortColumn', sort_column.value)

    @property
    def sort_ascending(self) -> bool:
        """Whether the viewer is sorted ascending or not.
        """
        return self.xa_elem.sortAscending()

    @sort_ascending.setter
    def sort_ascending(self, sort_ascending: bool):
        self.set_property('sortAscending', sort_ascending)

    @property
    def mailbox_list_visible(self) -> bool:
        """Controls whether the list of mailboxes is visible or not.
        """
        return self.xa_elem.mailboxListVisible()

    @mailbox_list_visible.setter
    def mailbox_list_visible(self, mailbox_list_visible: bool):
        self.set_property('mailboxListVisible', mailbox_list_visible)

    @property
    def preview_pane_is_visible(self) -> bool:
        """Controls whether the preview pane of the message viewer window is visible or not.
        """
        return self.xa_elem.previewPaneIsVisible()

    @preview_pane_is_visible.setter
    def preview_pane_is_visible(self, preview_pane_is_visible: bool):
        self.set_property('previewPaneIsVisible', preview_pane_is_visible)

    @property
    def visible_columns(self) -> list[str]:
        """List of columns that are visible. The subject column and the message status column will always be visible.
        """
        return self.xa_elem.visibleColumns()

    @visible_columns.setter
    def visible_columns(self, visible_columns: list[XAMailApplication.ViewerColumn]):
        visible_columns = [x.value for x in visible_columns]
        self.set_property('visibleColumns', visible_columns)

    @property
    def id(self) -> int:
        """The unique identifier of the message viewer.
        """
        return self.xa_elem.id()

    @property
    def visible_messages(self) -> 'XAMailMessageList':
        """List of messages currently being displayed in the viewer.
        """
        return self._new_element(self.xa_elem.visibleMessages(), XAMailMessageList)

    @visible_messages.setter
    def visible_messages(self, visible_messages: Union['XAMailMessageList', list['XAMailMessage']]):
        if isinstance(visible_messages, list):
            visible_messages = [x.xa_elem for x in visible_messages]
            self.set_property('visibleMessages', visible_messages)
        else:
            self.set_property('visibleMessages', visible_messages.xa_elem)

    @property
    def selected_messages(self) -> 'XAMailMessageList':
        """List of messages currently selected.
        """
        return self._new_element(self.xa_elem.selectedMessages(), XAMailMessageList)

    @selected_messages.setter
    def selected_messages(self, selected_messages: Union['XAMailMessageList', list['XAMailMessage']]):
        if isinstance(selected_messages, list):
            selected_messages = [x.xa_elem for x in selected_messages]
            self.set_property('visibleMessages', selected_messages)
        else:
            self.set_property('visibleMessages', selected_messages.xa_elem)

    @property
    def selected_mailboxes(self) -> 'XAMailboxList':
        """List of mailboxes currently selected in the list of mailboxes.
        """
        return self._new_element(self.xa_elem.selectedMailboxes(), XAMailboxList)

    @selected_mailboxes.setter
    def selected_mailboxes(self, selected_mailboxes: Union['XAMailboxList', list['XAMailbox']]):
        if isinstance(selected_mailboxes, list):
            selected_mailboxes = [x.xa_elem for x in selected_mailboxes]
            self.set_property('visibleMessages', selected_mailboxes)
        else:
            self.set_property('visibleMessages', selected_mailboxes.xa_elem)

    @property
    def window(self) -> XAMailWindow:
        """The window for the message viewer.
        """
        return self._new_element(self.xa_elem.window(), XAMailWindow)

    @window.setter
    def window(self, window: XAMailWindow):
        self.set_property('window', window)

    def messages(self, filter: dict = None) -> 'XAMailMessageList':
        """Returns a list of messages matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.messages(), XAMailMessageList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id) + ">"




class XAMailSignatureList(XABase.XAList):
    """A wrapper around lists of mail signatures that employs fast enumeration techniques.

    All properties of signatures can be called as methods on the wrapped list, returning a list containing each signature's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each signature in the list.

        :return: A list of signature names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def content(self) -> list[XABase.XAText]:
        """Gets the text content of each signature in the list.

        :return: A list of signature text contents
        :rtype: list[XABase.XAText]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return self._new_element(ls, XABase.XATextList)

    def by_name(self, name: str) -> Union['XAMailSignature', None]:
        """Retrieves the signature whose name matches the given name, if one exists.

        :return: The desired signature, if it is found
        :rtype: Union[XAMailSignature, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def by_content(self, content: XABase.XAText) -> Union['XAMailSignature', None]:
        """Retrieves the signature whose content matches the given content, if one exists.

        :return: The desired signature, if it is found
        :rtype: Union[XAMailSignature, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("content", content.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailSignature(XABase.XAObject):
    """A class for managing and interacting with email signatures in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def content(self) -> XABase.XAText:
        """The content of the email signature.
        """
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @content.setter
    def content(self, content: str):
        self.set_property('content', content)

    @property
    def name(self) -> str:
        """The name of the signature.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    def delete(self):
        """Permanently deletes the signature.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailAccountList(XABase.XAList):
    """A wrapper around lists of mail accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XAMailAccount
        super().__init__(properties, object_class, filter)

    def delivery_account(self) -> 'XAMailSMTPServerList':
        """Gets the delivery account of each account in the list.

        :return: A list of delivery accounts
        :rtype: XAMailSMTPServerList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("deliveryAccount")
        return self._new_element(ls, XAMailSMTPServerList)

    def name(self) -> list[str]:
        """Gets the name of each account in the list.

        :return: A list of account names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each account in the list.

        :return: A list of account IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def authentication(self) -> list[XAMailApplication.AuthenticationMethod]:
        """Gets the authentication method of each account in the list.

        :return: A list of account authentication methods
        :rtype: list[XAMailApplication.AuthenticationMethod]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("authentication")
        return [XAMailApplication.AuthenticationMethod(OSType(x.stringValue())) for x in ls]

    def account_type(self) -> list[XAMailApplication.AccountType]:
        """Gets the type of each account in the list.

        :return: A list of account types
        :rtype: list[XAMailApplication.AccountType]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("accountType")
        return [XAMailApplication.AccountType(OSType(x.stringValue())) for x in ls]

    def email_addresses(self) -> list[list[str]]:
        """Gets the email addresses of each account in the list.

        :return: A list of email addresses
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emailAddresses"))

    def full_name(self) -> list[str]:
        """Gets the full name of each account in the list.

        :return: A list of account full names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fullName"))

    def empty_junk_messages_frequency(self) -> list[int]:
        """Gets the empty junk message frequency of each account in the list.

        :return: A list of account empty junk message frequency settings
        :rtype: list[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emptyJunkMessagesFrequency"))

    def empty_trash_frequency(self) -> list[int]:
        """Gets the empty trash frequency of each account in the list.

        :return: A list of account empty trash frequency settings
        :rtype: list[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emptyTrashFrequency"))

    def empty_junk_messages_on_quit(self) -> list[bool]:
        """Gets the empty junk messages on quit setting of each account in the list.

        :return: A list of account empty junk messages on quit setting booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emptyJunkMessagesOnQuit"))

    def empty_trash_on_quit(self) -> list[bool]:
        """Gets the empty trash on quit setting of each account in the list.

        :return: A list of account empty trash on quit setting booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emptyTrashOnQuit"))

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each account in the list.

        :return: A list of account enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def user_name(self) -> list[str]:
        """Gets the user name of each account in the list.

        :return: A list of account user names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("userName"))

    def account_directory(self) -> list[str]:
        """Gets the account directory of each account in the list.

        :return: A list of account directories
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("accountDirectory"))

    def port(self) -> list[int]:
        """Gets the port of each account in the list.

        :return: A list of account ports
        :rtype: list[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("port"))

    def server_name(self) -> list[str]:
        """Gets the server name of each account in the list.

        :return: A list of account server names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("serverName"))

    def move_deleted_messages_to_trash(self) -> list[bool]:
        """Gets the move deleted messages to trash setting of each account in the list.

        :return: A list of account move deleted messages to trash setting booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("moveDeletedMessagesToTrash"))

    def uses_ssl(self) -> list[bool]:
        """Gets the SSL setting of each account in the list.

        :return: A list of account SSL setting booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("usesSsl"))

    def by_delivery_account(self, delivery_account: 'XAMailSMTPServer') -> Union['XAMailAccount', None]:
        """Retrieves the first account whose delivery account matches the given account, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("deliveryAccount", delivery_account.xa_elem)

    def by_name(self, name: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose name matches the given name, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose ID matches the given ID, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_authentication(self, authentication: XAMailApplication.AuthenticationMethod) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose authentication method matches the given authentication method, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("authentication", event_from_str(unOSType(authentication.value)))

    def by_account_type(self, account_type: XAMailApplication.AccountType) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose type matches the given type, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("accountType", event_from_str(unOSType(account_type.value)))

    def by_email_addresses(self, email_addresses: list[str]) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose list of email addresses matches the given list, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("emailAddresses", email_addresses)

    def by_full_name(self, full_name: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose full name matches the given full name, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("fullName", full_name)

    def by_empty_junk_messages_frequency(self, empty_junk_messages_frequency: int) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose empty junk messages frequency matches the given frequency, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("emptyJunkMessagesFrequency", empty_junk_messages_frequency)

    def by_empty_trash_frequency(self, empty_trash_frequency: int) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose empty trash frequency matches the given frequency, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("emptyTrashFrequency", empty_trash_frequency)

    def by_empty_junk_messages_on_quit(self, empty_junk_messages_on_quit: bool) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose empty junk messages on quit setting matches the given boolean value, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("emptyJunkMessagesOnQuit", empty_junk_messages_on_quit)

    def by_empty_trash_on_quit(self, empty_trash_on_quit: bool) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose empty trash on quit setting matches the given boolean value, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("emptyTrashOnQuit", empty_trash_on_quit)

    def by_enabled(self, enabled: bool) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose enabled status matches the given boolean value, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("enabled", enabled)

    def by_user_name(self, user_name: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose user name matches the given user name, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("userName", user_name)

    def by_account_directory(self, account_directory: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose account directory matches the given directory, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("accountDirectory", account_directory)

    def by_port(self, port: int) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose port number matches the given port, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("port", port)

    def by_server_name(self, server_name: str) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose server name matches the given server name, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("serverName", server_name)

    def by_move_deleted_messages_to_trash(self, move_deleted_messages_to_trash: bool) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose move deleted messages to trash setting matches the given boolean value, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("moveDeletedMessagesToTrash", move_deleted_messages_to_trash)

    def by_uses_ssl(self, uses_ssl: bool) -> Union['XAMailAccount', None]:
        """Retrieves the first account whose uses SSL setting matches the given boolean value, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XAMailAccount, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("usesSsl", uses_ssl)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailAccount(XABase.XAObject):
    """A class for managing and interacting with accounts in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def delivery_account(self) -> 'XAMailSMTPServer':
        """The delivery account use when sending messages from the account.
        """
        return self._new_element(self.xa_elem.deliveryAccount(), XAMailSMTPServer)

    @delivery_account.setter
    def delivery_account(self, delivery_account: 'XAMailSMTPServer'):
        self.set_property('deliveryAccount', delivery_account.xa_elem)

    @property
    def name(self) -> str:
        """The name of the account.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def id(self) -> str:
        """The unique identifier for the account.
        """
        return self.xa_elem.id()

    @property
    def password(self) -> None:
        """The password for the account.
        """
        return

    @password.setter
    def password(self, password: str):
        self.set_property('password', password)

    @property
    def authentication(self) -> XAMailApplication.AuthenticationMethod:
        """he preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none".
        """
        return XAMailApplication.AuthenticationMethod(OSType(self.xa_elem.authentication().stringValue()))

    @authentication.setter
    def authentication(self, authentication: XAMailApplication.AuthenticationMethod):
        self.set_property('authentication', authentication.value)

    @property
    def account_type(self) -> XAMailApplication.AccountType:
        """The type of the account, either: "pop", "smtp", "imap", or "iCloud".
        """
        return XAMailApplication.AccountType(OSType(self.xa_elem.accountType().stringValue()))

    @property
    def email_addresses(self) -> list[str]:
        """The list of email addresses associated with the account.
        """
        return self.xa_elem.emailAddresses()

    @email_addresses.setter
    def email_addresses(self, email_addresses: list[str]):
        self.set_property('emailAddresses', email_addresses)

    @property
    def full_name(self) -> str:
        """The user's full name associated with the account.
        """
        return self.xa_elem.fullName()

    @full_name.setter
    def full_name(self, full_name: str):
        self.set_property('fullName', full_name)

    @property
    def empty_junk_messages_frequency(self) -> int:
        """Number of days before junk messages are deleted (0 = delete on quit, -1 = never delete).
        """
        return self.xa_elem.emptyJunkMessagesFrequency()

    @empty_junk_messages_frequency.setter
    def empty_junk_messages_frequency(self, empty_junk_messages_frequency: int):
        self.set_property('emptyJunkMessagesFrequency', empty_junk_messages_frequency)

    @property
    def empty_trash_frequency(self) -> int:
        """Number of days before messages in the trash are deleted (0 = delete on quit, -1 = never delete).
        """
        return self.xa_elem.emptyTrashFrequency()

    @empty_trash_frequency.setter
    def empty_trash_frequency(self, empty_trash_frequency: type):
        self.set_property('empty_trash_frequency', empty_trash_frequency)

    @property
    def empty_junk_messages_on_quit(self) -> bool:
        """Whether messages marked as junk are deleted upon quitting Mail.app.
        """
        return self.xa_elem.emptyJunkMessagesOnQuit()

    @empty_junk_messages_on_quit.setter
    def empty_junk_messages_on_quit(self, empty_junk_messages_on_quit: bool):
        self.set_property('emptyJunkMessagesOnQuit', empty_junk_messages_on_quit)

    @property
    def empty_trash_on_quit(self) -> bool:
        """Whether messages in the trash are permanently deleted upon quitting Mail.app.
        """
        return self.xa_elem.emptyTrashOnQuit()

    @empty_trash_on_quit.setter
    def empty_trash_on_quit(self, empty_trash_on_quit: bool):
        self.set_property('emptyTrashOnQuit', empty_trash_on_quit)

    @property
    def enabled(self) -> bool:
        """Whether the account is enabled.
        """
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def user_name(self) -> str:
        """The user name used to connect to the account.
        """
        return self.xa_elem.userName()

    @user_name.setter
    def user_name(self, user_name: str):
        self.set_property('userName', user_name)

    @property
    def account_directory(self) -> str:
        """The directory where the account stores items on the disk.
        """
        return self.xa_elem.accountDirectory()

    @property
    def port(self) -> int:
        """The port used to connect to the account.
        """
        return self.xa_elem.port()

    @port.setter
    def port(self, port: int):
        self.set_property('port', port)

    @property
    def server_name(self) -> str:
        """The host name used to connect to the account.
        """
        return self.xa_elem.serverName()

    @server_name.setter
    def server_name(self, server_name: str):
        self.set_property('serverName', server_name)

    @property
    def move_deleted_messages_to_trash(self) -> bool:
        """Whether messages are moved to the trash mailbox upon deletion.
        """
        return self.xa_elem.moveDeletedMessagesToTrash()

    @move_deleted_messages_to_trash.setter
    def move_deleted_messages_to_trash(self, move_deleted_messages_to_trash: bool):
        self.set_property('moveDeletedMessagesToTrash', move_deleted_messages_to_trash)

    @property
    def uses_ssl(self) -> bool:
        """Whether SSL is enabled for this receiving account.
        """
        return self.xa_elem.usesSsl()

    @uses_ssl.setter
    def uses_ssl(self, uses_ssl: bool):
        self.set_property('usesSsl', uses_ssl)

    def mailboxes(self, filter: dict = None) -> 'XAMailboxList':
        """Returns a list of mail accounts matching the filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.mailboxes(), XAMailboxList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailIMAPAccountList(XAMailAccountList):
    """A wrapper around lists of mail documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMailPOPAccount)

    def compact_mailboxes_when_closing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("compactMailboxesWhenClosing"))

    def message_caching(self) -> list[XAMailApplication.CachingPolicy]:
        ls = self.xa_elem.arrayByApplyingSelector_("messageCaching")
        return [XAMailApplication.CachingPolicy(OSType(x.stringValue())) for x in ls]

    def store_drafts_on_server(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeDraftsOnServer"))

    def store_junk_mail_on_server(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeJunkMailOnServer"))

    def store_sent_messages_on_server(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("storeSentMessagesOnServer"))

    def store_deleted_messages_on_server(self) -> list[bool]:
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

    @property
    def compact_mailboxes_when_closing(self) -> bool:
        """Whether an IMAP mailbox is automatically compacted when the user quits Mail.app or switches to another mailbox.
        """
        return self.xa_elem.compactMailboxesWhenClosing()

    @compact_mailboxes_when_closing.setter
    def compact_mailboxes_when_closing(self, compact_mailboxes_when_closing: bool):
        self.set_property('compactMailboxesWhenClosing', compact_mailboxes_when_closing)

    @property
    def message_caching(self) -> XAMailApplication.CachingPolicy:
        """The message caching setting for the account.
        """
        return XAMailApplication.CachingPolicy(OSType(self.xa_elem.messageCaching().stringValue()))

    @message_caching.setter
    def message_caching(self, message_caching: XAMailApplication.CachingPolicy):
        self.set_property('message_caching', message_caching.value)

    @property
    def store_drafts_on_server(self) -> bool:
        """Whether draft messages will be stored on the IMAP server.
        """
        return self.xa_elem.storeDraftsOnServer()

    @store_drafts_on_server.setter
    def store_drafts_on_server(self, store_drafts_on_server: bool):
        self.set_property('storeDraftsOnServer', store_drafts_on_server)
    
    @property
    def store_junk_mail_on_server(self) -> bool:
        """Whether junk mail will be stored on the IMAP server.
        """
        return self.xa_elem.storeJunkMailOnServer()

    @store_junk_mail_on_server.setter
    def store_junk_mail_on_server(self, store_junk_mail_on_server: bool):
        self.set_property('storeJunkMailOnServer', store_junk_mail_on_server)

    @property
    def store_sent_messages_on_server(self) -> bool:
        """Whether sent messages will be stored on the IMAP server.
        """
        return self.xa_elem.storeSentMessagesOnServer()

    @store_sent_messages_on_server.setter
    def store_sent_messages_on_server(self, store_sent_messages_on_server: bool):
        self.set_property('storeSentMessagesOnServer', store_sent_messages_on_server)

    @property
    def store_deleted_messages_on_server(self) -> bool:
        """Whether deleted messages will be stored on the IMAP server.
        """
        return self.xa_elem.storeDeletedMessagesOnServer()

    @store_deleted_messages_on_server.setter
    def store_deleted_messages_on_server(self, store_deleted_messages_on_server: bool):
        self.set_property('storeDeletedMessagesOnServer', store_deleted_messages_on_server)




class XAMailICloudAccountList(XAMailAccountList):
    """A wrapper around lists of iCloud accounts that employs fast enumeration techniques.

    All properties of iCloud accounts can be called as methods on the wrapped list, returning a list containing each accounts's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMailICloudAccount)

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
        super().__init__(properties, filter, XAMailPOPAccount)

    def big_message_warning_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("bigMessageWarningSize"))

    def delayed_message_deletion_interval(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("delayedMessageDeletionInterval"))

    def delete_mail_on_server(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("deleteMailOnServer"))

    def delete_messages_when_moved_from_inbox(self) -> list[bool]:
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

    @property
    def big_message_warning_size(self) -> int:
        """The max amount of bytes a message can be before Mail will prompt the user before downloading the message (-1 = do not prompt).
        """
        return self.xa_elem.bigMessageWarningSize()

    @big_message_warning_size.setter
    def big_message_warning_size(self, big_message_warning_size: int):
        self.set_property('bigMessageWarningSize', big_message_warning_size)

    @property
    def delayed_message_deletion_interval(self) -> int:
        """The number of days before messages that have been downloaded will be deleted from the server (0 = delete immediately after downloading).
        """
        return self.xa_elem.delayedMessageDeletionInterval()

    @delayed_message_deletion_interval.setter
    def delayed_message_deletion_interval(self, delayed_message_deletion_interval: int):
        self.set_property('delayedMessageDeletionInterval', delayed_message_deletion_interval)

    @property
    def delete_mail_on_server(self) -> bool:
        """Whether the POP account deletes messages on the server after downloading.
        """
        return self.xa_elem.deleteMailOnServer()

    @delete_mail_on_server.setter
    def delete_mail_on_server(self, delete_mail_on_server: bool):
        self.set_property('deleteMailOnServer', delete_mail_on_server)

    @property
    def delete_messages_when_moved_from_inbox(self) -> bool:
        """Whether messages will be deleted from the server when moved from the POP inbox.
        """
        return self.xa_elem.deleteMessagesWhenMovedFromInbox()

    @delete_messages_when_moved_from_inbox.setter
    def delete_messages_when_moved_from_inbox(self, delete_messages_when_moved_from_inbox: bool):
        self.set_property('deleteMessagesWhenMovedFromInbox', delete_messages_when_moved_from_inbox)




class XAMailSMTPServerList(XABase.XAList):
    """A wrapper around lists of SMTP servers that employs fast enumeration techniques.

    All properties of SMTP servers can be called as methods on the wrapped list, returning a list containing each SMTP server's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailSMTPServer, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def authentication(self) -> list[XAMailApplication.AuthenticationMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("authentication")
        return [XAMailApplication.AuthenticationMethod(OSType(x.stringValue())) for x in ls]

    def account_type(self) -> list[XAMailApplication.AccountType]:
        ls = self.xa_elem.arrayByApplyingSelector_("accountType")
        return [XAMailApplication.AccountType(OSType(x.stringValue())) for x in ls]

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def user_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userName"))

    def port(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("port"))

    def server_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("serverName"))

    def uses_ssl(self) -> list[bool]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailSMTPServer(XABase.XAObject):
    """A class for managing and interacting with SMTP servers in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the account.
        """
        return self.xa_elem.name()

    @property
    def password(self) -> None:
        """The password for the account.
        """
        return

    @password.setter
    def password(self, password: str):
        self.set_property('password', password)

    @property
    def account_type(self) -> XAMailApplication.AccountType:
        """The type of the account, either: "pop", "smtp", "imap", or "iCloud".
        """
        return XAMailApplication.AccountType(OSType(self.xa_elem.accountType().stringValue()))

    @property
    def authentication(self) -> XAMailApplication.AuthenticationMethod:
        """The preferred authentication scheme for the account, either: "password", "apop", "kerberos 5", "ntlm", "md5", "external", "Apple token", or "none".
        """
        return XAMailApplication.AuthenticationMethod(OSType(self.xa_elem.authentication().stringValue()))

    @authentication.setter
    def authentication(self, authentication: XAMailApplication.AuthenticationMethod):
        self.set_property('authentication', authentication.value)

    @property
    def enabled(self) -> bool:
        """Whether the account is enabled.
        """
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def user_name(self) -> str:
        """The user name used to connect to the account.
        """
        return self.xa_elem.userName()

    @user_name.setter
    def user_name(self, user_name: str):
        self.set_property('userName', user_name)

    @property
    def port(self) -> int:
        """The port used to connect to the account.
        """
        return self.xa_elem.port()

    @port.setter
    def port(self, port: int):
        self.set_property('port', port)

    @property
    def server_name(self) -> str:
        """The host name used to connect to the account.
        """
        return self.xa_elem.serverName()

    @server_name.setter
    def server_name(self, server_name: str):
        self.set_property('serverName', server_name)

    @property
    def uses_ssl(self) -> bool:
        """Whether SSL is enabled for this receiving account.
        """
        return self.xa_elem.usesSsl()

    @uses_ssl.setter
    def uses_ssl(self, uses_ssl: bool):
        self.set_property('usesSsl', uses_ssl)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailDocumentList(XABase.XAList):
    """A wrapper around lists of mail documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def by_name(self, name: str) -> 'XAMailDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAMailDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XAMailDocument':
        return self.by_property("file", file)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailDocument(XABase.XAObject):
    """A class for managing and interacting with Mail documents.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the document.
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since the last save.
        """
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        """The location of the document on the disk, if one exists.
        """
        return self.xa_elem.file()

    def delete(self):
        """Permanently deletes the document.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailboxList(XABase.XAList):
    """A wrapper around lists of mailboxes that employs fast enumeration techniques.

    All properties of mailboxes can be called as methods on the wrapped list, returning a list containing each mailbox's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMailbox
        super().__init__(properties, obj_class, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def unread_count(self) -> list[str]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailbox(XABase.XAObject):
    """A class for managing and interacting with mailboxes in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the mailbox.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def unread_count(self) -> int:
        """The number of unread messages in the mailbox.
        """
        return self.xa_elem.unreadCount()

    @property
    def account(self) -> XAMailAccount:
        """The parent account of the mailbox.
        """
        return self._new_element(self.xa_elem.account(), XAMailAccount)

    @property
    def container(self) -> 'XAMailbox':
        """The parent mailbox of the mailbox.
        """
        return self._new_element(self.xa_elem.container(), XAMailbox)

    def delete(self):
        """Permanently deletes the mailboxs.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def mailboxes(self, filter: dict = None) -> 'XAMailboxList':
        """Returns a list of mailboxes matching the filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.mailboxes(), XAMailboxList, filter)

    def messages(self, filter: dict = None) -> 'XAMailMessageList':
        """Returns a list of messages matching the filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.messages(), XAMailMessageList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailContainerList(XAMailboxList):
    """A wrapper around lists of mail headers that employs fast enumeration techniques.

    All properties of headers can be called as methods on the wrapped list, returning a list containing each header's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMailContainer)

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

    def id(self) -> list[int]:
        # Objc method caused segfault, not sure why
        return [x.id() for x in self.xa_elem]

    def all_headers(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("allHeaders"))

    def background_color(self) -> list[XAMailApplication.HighlightColor]:
        ls = [x.backgroundColor() for x in self.xa_elem]
        return [XAMailApplication.HighlightColor(OSType(x.stringValue())) for x in ls]

    def mailbox(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("mailbox")
        return self._new_element(ls, XAMailboxList)

    def content(self) -> list[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return list(ls.arrayByApplyingSelector_("get"))

    def date_received(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dateReceived"))

    def date_sent(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dateSent"))

    def deleted_status(self) -> list[bool]:
        return [x.deletedStatus() for x in self.xa_elem]

    def flagged_status(self) -> list[bool]:
        return [x.flaggedStatus() for x in self.xa_elem]

    def flag_index(self) -> list[int]:
        return [x.flagIndex() for x in self.xa_elem]

    def junk_mail_status(self) -> list[bool]:
        return [x.junkMailStatus() for x in self.xa_elem]

    def read_status(self) -> list[bool]:
        return [x.readStatus() for x in self.xa_elem]

    def message_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("messageId"))
    
    def source(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("source"))

    def reply_to(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("replyTo"))

    def message_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("messageSize"))

    def sender(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sender"))

    def subject(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subject"))

    def was_forwarded(self) -> list[bool]:
        return [x.wasForwarded() for x in self.xa_elem]

    def was_redirected(self) -> list[bool]:
        return [x.wasRedirected() for x in self.xa_elem]

    def was_replied_to(self) -> list[bool]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.subject()) + ">"

class XAMailMessage(XABase.XAObject):
    """A class for managing and interacting with messages in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique identifier for the message.
        """
        return self.xa_elem.id()

    @property
    def all_headers(self) -> str:
        """The headers of the message.
        """
        return self.xa_elem.allHeaders()

    @property
    def background_color(self) -> XAMailApplication.HighlightColor:
        """The background color of the message.
        """
        return XAMailApplication.HighlightColor(OSType(self.xa_elem.backroundColor().stringValue()))

    @background_color.setter
    def background_color(self, background_color: XAMailApplication.HighlightColor):
        self.set_property('backgroundColor', background_color.value)

    @property
    def mailbox(self) -> XAMailbox:
        """The mailbox in which the message is located.
        """
        return self._new_element(self.xa_elem.mailbox(), XAMailbox)

    @mailbox.setter
    def mailbox(self, mailbox: XAMailbox):
        self.set_property('mailbox', mailbox.xa_elem)

    @property
    def content(self) -> XABase.XAText:
        """The contents of the message.
        """
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @content.setter
    def content(self, content: Union[XABase.XAText, str]):
        if isinstance(content, str):
            self.set_property('content', content)
        else:
            self.set_property('content', content.xa_elem)

    @property
    def date_received(self) -> datetime:
        """The date and time that the message was received.
        """
        return self.xa_elem.dateReceived()

    @property
    def date_sent(self) -> datetime:
        """The date and time that the message was sent.
        """
        return self.xa_elem.dateSent()

    @property
    def deleted_status(self) -> bool:
        """Whether the message is deleted.
        """
        return self.xa_elem.deletedStatus()

    @deleted_status.setter
    def deleted_status(self, deleted_status: bool):
        self.set_property('deletedStatus', deleted_status)

    @property
    def flagged_status(self) -> bool:
        """Whether the message is flagged.
        """
        return self.xa_elem.flaggedStatus()

    @flagged_status.setter
    def flagged_status(self, flagged_status: bool):
        self.set_property('flaggedStatus', flagged_status)

    @property
    def flag_index(self) -> int:
        """The flag on the message, or -1 if the message is not flagged.
        """
        return self.xa_elem.flagIndex()

    @flag_index.setter
    def flag_index(self, flag_index: int):
        self.set_property('flagIndex', flag_index)

    @property
    def junk_mail_status(self) -> bool:
        """Whether the message is marked as junk.
        """
        return self.xa_elem.junkMailStatus()

    @junk_mail_status.setter
    def junk_mail_status(self, junk_mail_status: bool):
        self.set_property('junkMailStatus', junk_mail_status)

    @property
    def read_status(self) -> bool:
        """Whether the message has been read.
        """
        return self.xa_elem.readStatus()

    @read_status.setter
    def read_status(self, read_status: bool):
        self.set_property('readStatus', read_status)

    @property
    def message_id(self) -> int:
        """The unique message ID string.
        """
        return self.xa_elem.messageId()

    @property
    def source(self) -> str:
        """The raw source of the message.
        """
        return self.xa_elem.source()

    @property
    def reply_to(self) -> str:
        """The address that replies should be sent to.
        """
        return self.xa_elem.replyTo()

    @property
    def message_size(self) -> int:
        """The size of the message in bytes.
        """
        return self.xa_elem.messageSize()

    @property
    def sender(self) -> str:
        """The address of the sender of the message.
        """
        return self.xa_elem.sender()

    @property
    def subject(self) -> str:
        """The subject string of the message.
        """
        return self.xa_elem.subject()

    @property
    def was_forward(self) -> bool:
        """Whether the message was forwarded.
        """
        return self.xa_elem.wasForwarded()

    @property
    def was_redirected(self) -> bool:
        """Whether the message was redirected.
        """
        return self.xa_elem.wasRedirected()

    @property
    def was_replied_to(self) -> bool:
        """Whether the message was replied to.
        """
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.subject) + ">"




class XAMailOutgoingMessageList(XABase.XAList):
    """A wrapper around lists of outgoing messages that employs fast enumeration techniques.

    All properties of outgoing messages can be called as methods on the wrapped list, returning a list containing each messages's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailHeader, filter)

    def sender(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sender"))

    def subject(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subject"))

    def content(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("content")
        return self._new_element(ls, XABase.XATextList)

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def message_signature(self) -> XAMailSignatureList:
        ls = self.xa_elem.arrayByApplyingSelector_("messageSignature")
        return self._new_element(ls, XAMailSignatureList)

    def id(self) -> list[int]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.subject()) + ">"

class XAMailOutgoingMessage(XABase.XAObject):
    """A class for managing and interacting with outgoing messages in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def sender(self) -> str:
        """The address of the message sender.
        """
        return self.xa_elem.sender()

    @sender.setter
    def sender(self, sender: str):
        self.set_property('sender', sender)

    @property
    def subject(self) -> str:
        """The subject string of the message.
        """
        return self.xa_elem.subject()

    @subject.setter
    def subject(self, subject: str):
        self.set_property('subject', subject)

    @property
    def content(self) -> XABase.XAText:
        """The contents of the message.
        """
        return self._new_element(self.xa_elem.content(), XABase.XAText)

    @content.setter
    def content(self, content: Union[XABase.XAText, str]):
        if isinstance(content, str):
            self.set_property('content', content)
        else:
            self.set_property('content', content.xa_elem)

    @property
    def visible(self) -> bool:
        """Whether the message window is shown on screen.
        """
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property('visible', visible)

    @property
    def message_signature(self) -> XAMailSignature:
        """The signature of the message.
        """
        return self._new_element(self.xa_elem.messageSignature(). XAMailSignature)

    @message_signature.setter
    def message_signature(self, message_signature: XAMailSignature):
        self.set_property('messageSignature', message_signature.xa_elem)

    @property
    def id(self) -> int:
        """The unique identifier for the message.
        """
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.subject) + ">"




class XAMailRecipientList(XABase.XAList):
    """A wrapper around lists of mail recipients that employs fast enumeration techniques.

    All properties of recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XAMailRecipient
        super().__init__(properties, object_class, filter)

    def address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_address(self, address: str) -> 'XAMailRecipient':
        return self.by_property("address", address)

    def by_name(self, name: str) -> 'XAMailRecipient':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailRecipient(XABase.XAObject):
    """A class for managing and interacting with recipients in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def address(self) -> str:
        """The recipient's email address.
        """
        return self.xa_elem.address()

    @address.setter
    def address(self, address: str):
        self.set_property('address', address)

    @property
    def name(self) -> str:
        """The name used for display.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailBccRecipientList(XAMailRecipientList):
    """A wrapper around lists of mail Bcc recipients that employs fast enumeration techniques.

    All properties of Bcc recipients can be called as methods on the wrapped list, returning a list containing each recipients's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMailBccRecipient)

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
        super().__init__(properties, filter, XAMailCcRecipient)

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
        super().__init__(properties, filter, XAMailToRecipient)

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

    def content(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("content"))

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_content(self, content: str) -> 'XAMailHeader':
        return self.by_property("content", content)

    def by_name(self, name: str) -> 'XAMailHeader':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailHeader(XABase.XAObject):
    """A class for managing and interacting with message headers in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def content(self) -> str:
        """The contents of the header.
        """
        return self.xa_elem.content()

    @content.setter
    def content(self, content: str):
        self.set_property('content', content)

    @property
    def name(self) -> str:
        """The name of the header value.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailAttachmentList(XABase.XAList):
    """A wrapper around lists of attachments that employs fast enumeration techniques.

    All properties of attachments can be called as methods on the wrapped list, returning a list containing each attachment's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailAttachment, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def mime_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("mimeType"))

    def file_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileSize"))

    def downloaded(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("downloaded"))

    def id(self) -> list[str]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailAttachment(XABase.XAObject):
    """A class for managing and interacting with message attachments in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the attachment.
        """
        return self.xa_elem.name()

    @property
    def mime_type(self) -> str:
        """The MIME type of the attachment, e.g. text/plain.
        """
        return self.xa_elem.mimeType()

    @property
    def file_size(self) -> int:
        """The approximate size of the attachment in bytes.
        """
        return self.xa_elem.fileSize()

    @property
    def downloaded(self) -> bool:
        """Whether the attachment has been downloaded.
        """
        return self.xa_elem.downloaded()

    @property
    def id(self) -> str:
        """The unique identifier for the attachment.
        """
        return self.xa_elem.id()

    def delete(self):
        """Permanently deletes the attachment.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAMailRuleList(XABase.XAList):
    """A wrapper around lists of rules that employs fast enumeration techniques.

    All properties of rules can be called as methods on the wrapped list, returning a list containing each rule's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    def color_message(self) -> list[XAMailApplication.HighlightColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("colorMessage")
        return [XAMailApplication.HighlightColor(OSType(x.stringValue())) for x in ls]

    def delete_message(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("deleteMessage"))

    def forward_text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("forwardText"))

    def forward_message(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("forwardMessage"))

    def mark_flagged(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("markFlagged"))

    def mark_flag_index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("markFlagIndex"))

    def mark_read(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("markRead"))

    def play_sound(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("playSound"))

    def redirect_message(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("redirectMessage"))

    def reply_text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("replyText"))

    def run_script(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("runScript"))

    def all_conditions_must_be_met(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("allConditionsMustBeMet"))

    def copy_message(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("copyMessage")
        return self._new_element(ls, XAMailboxList)

    def move_message(self) -> XAMailboxList:
        ls = self.xa_elem.arrayByApplyingSelector_("moveMessage")
        return self._new_element(ls, XAMailboxList)

    def highlight_text_using_color(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("highlightTextUsingColor"))

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def should_copy_message(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shouldCopyMessage"))

    def should_move_message(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shouldMoveMessage"))

    def stop_evaluating_rules(self) -> list[bool]:
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMailRule(XABase.XAObject):
    """A class for managing and interacting with rules in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def color_message(self) -> XAMailApplication.HighlightColor:
        """If the rule matches, apply this color.
        """
        return XAMailApplication.HighlightColor(OSType(self.xa_elem.colorMessage().stringValue()))

    @color_message.setter
    def color_message(self, color_message: XAMailApplication.HighlightColor):
        self.set_property('colorMessage', color_message.value)

    @property
    def delete_message(self) -> bool:
        """If the rule matches, delete the message.
        """
        return self.xa_elem.deleteMessage()

    @delete_message.setter
    def delete_message(self, delete_message: bool):
        self.set_property('deleteMessage', delete_message)

    @property
    def forward_text(self) -> str:
        """If the rule matches, prepend the provided text to the forwarded message.
        """
        return self.xa_elem.forwardText()

    @forward_text.setter
    def forward_text(self, forward_text: str):
        self.set_property('forwardText', forward_text)

    @property
    def forward_message(self) -> str:
        """If the rule matches, forward the message to the specified addresses, separated by commas.
        """
        return self.xa_elem.forwardMessage()

    @forward_message.setter
    def forward_message(self, forward_message: str):
        self.set_property('forwardMessage', forward_message)

    @property
    def mark_flagged(self) -> bool:
        """If the rule matches, mark the message as flagged.
        """
        return self.xa_elem.markFlagged()

    @mark_flagged.setter
    def mark_flagged(self, mark_flagged: bool):
        self.set_property('markFlagged', mark_flagged)

    @property
    def mark_flag_index(self) -> int:
        """If the rule matches, mark the message with the specified flag (-1 = disabled).
        """
        return self.xa_elem.markFlagIndex()

    @mark_flag_index.setter
    def mark_flag_index(self, mark_flag_index: int):
        self.set_property('markFlagIndex', mark_flag_index)

    @property
    def mark_read(self) -> bool:
        """If the rule matches, mark the message as read.
        """
        return self.xa_elem.markRead()

    @mark_read.setter
    def mark_read(self, mark_read: bool):
        self.set_property('markRead', mark_read)

    @property
    def play_sound(self) -> str:
        """If the rule matches, play the sound specified by name or path.
        """
        return self.xa_elem.playSound()

    @play_sound.setter
    def play_sound(self, play_sound: str):
        self.set_property('playSound', play_sound)

    @property
    def redirect_message(self) -> str:
        """If the rule matches, redirect the message to the supplied addresses, separated by commas.
        """
        return self.xa_elem.redirectMessage()

    @redirect_message.setter
    def redirect_message(self, redirect_message: str):
        self.set_property('redirectMessage', redirect_message)

    @property
    def reply_text(self) -> str:
        """If the rule matches, reply to the message and prepend the provided text.
        """
        return self.xa_elem.replyText()

    @reply_text.setter
    def reply_text(self, reply_text: str):
        self.set_property('replyText', reply_text)

    # TODO
    @property
    def run_script(self) -> str:
        """If the rule matches, run the supplied AppleScript file.
        """
        return self.xa_elem.runScript()

    @run_script.setter
    def run_script(self, run_script: str):
        self.set_property('runScript', run_script)

    @property
    def all_conditions_must_be_met(self) -> bool:
        """Whether all conditions must be met for the rule to execute.
        """
        return self.xa_elem.allConditionsMustBeMet()

    @all_conditions_must_be_met.setter
    def all_conditions_must_be_met(self, all_conditions_must_be_met: bool):
        self.set_property('allConditionsMustBeMet', all_conditions_must_be_met)

    @property
    def copy_message(self) -> XAMailbox:
        """If the rule matches, copy the message to the specified mailbox.
        """
        return self._new_element(self.xa_elem.copyMessage(), XAMailbox)

    @copy_message.setter
    def copy_message(self, copy_message: XAMailbox):
        self.set_property('copyMessage', copy_message.xa_elem)

    @property
    def move_message(self) -> XAMailbox:
        """If the rule matches, move the message to the specified mailbox.
        """
        return self._new_element(self.xa_elem.moveMessage(), XAMailbox)

    @move_message.setter
    def move_message(self, move_message: XAMailbox):
        self.set_property('moveMessage', move_message.xa_elem)

    @property
    def highlight_text_using_color(self) -> bool:
        """Whether the color will be used to highlight the text of background of a message.
        """
        return self.xa_elem.highlightTextUsingColor()

    @highlight_text_using_color.setter
    def highlight_text_using_color(self, highlight_text_using_color: bool):
        self.set_property('highlightTextUsingColor', highlight_text_using_color)

    @property
    def enabled(self) -> bool:
        """Whether the rule is enabled.
        """
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def name(self) -> str:
        """The name of the rule.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def should_copy_message(self) -> bool:
        """Whether the rule has a copy action.
        """
        return self.xa_elem.shouldCopyMessage()

    @should_copy_message.setter
    def should_copy_message(self, should_copy_message: bool):
        self.set_property('shouldCopyMessage', should_copy_message)

    @property
    def should_move_message(self) -> bool:
        """Whether the rule has a move action.
        """
        return self.xa_elem.shouldMoveMessage()

    @should_move_message.setter
    def should_move_message(self, should_move_message: bool):
        self.set_property('shouldMoveMessage', should_move_message)

    @property
    def stop_evaluating_rules(self) -> bool:
        """If the rule matches, stop rule evaluation for the message"""
        return self.xa_elem.stopEvaluatingRules()

    @stop_evaluating_rules.setter
    def stop_evaluating_rule(self, stop_evaluating_rules: bool):
        self.set_property('stopEvaluatingRules', stop_evaluating_rules)

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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"





class XAMailRuleConditionList(XABase.XAList):
    """A wrapper around lists of rule conditions that employs fast enumeration techniques.

    All properties of rule conditions can be called as methods on the wrapped list, returning a list containing each rule conditions's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMailMessage, filter)

    def expression(self) -> list[str]:
        """Gets the rule expression field of each rule condition in the list.

        :return: A list of rule expression field values
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("expression"))

    def header(self) -> list[str]:
        """Gets the rule header key of each rule condition in the list.

        :return: A list of rule header keys
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("header"))

    def qualifier(self) -> list[XAMailApplication.RuleQualifier]:
        """Gets the rule qualifier of each rule condition in the list.

        :return: A list of rule qualifiers
        :rtype: list[XAMailApplication.RuleQualifier]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("qualifier")
        return [XAMailApplication.RuleQualifier(OSType(x.stringValue())) for x in ls]

    def rule_type(self) -> list[XAMailApplication.RuleType]:
        """Gets the rule type of each rule condition in the list.

        :return: A list of rule types
        :rtype: list[XAMailApplication.RuleType]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("ruleType")
        return [XAMailApplication.RuleType(OSType(x.stringValue())) for x in ls]

    def by_expression(self, expression: str) -> Union['XAMailRuleCondition', None]:
        """Retrieves the first rule condition whose expression matches the given expression, if one exists.

        :return: The desired rule condition, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("expression", expression)

    def by_header(self, header: str) -> Union['XAMailRuleCondition', None]:
        """Retrieves the first rule condition whose header key matches the given key, if one exists.

        :return: The desired rule condition, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("header", header)

    def by_qualifier(self, qualifier: XAMailApplication.RuleQualifier) -> Union['XAMailRuleCondition', None]:
        """Retrieves the first rule condition whose qualifier matches the given qualifier, if one exists.

        :return: The desired rule condition, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("qualifier", event_from_str(unOSType(qualifier.value)))

    def by_rule_type(self, rule_type: XAMailApplication.RuleType) -> Union['XAMailRuleCondition', None]:
        """Retrieves the first rule condition whose type matches the given type, if one exists.

        :return: The desired rule condition, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("ruleType", event_from_str(unOSType(rule_type.value)))

class XAMailRuleCondition(XABase.XAObject):
    """A class for managing and interacting with rule conditions in Mail.app.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
    
    @property
    def expression(self) -> str:
        """The rule expression field.
        """
        return self.xa_elem.expression()

    @expression.setter
    def expression(self, expression: str):
        self.set_property('expression', expression)

    @property
    def header(self) -> str:
        """The rule header key.
        """
        return self.xa_elem.header()

    @header.setter
    def header(self, header: str):
        self.set_property('header', header)

    @property
    def qualifier(self) -> XAMailApplication.RuleQualifier:
        """The qualifier for the rule.
        """
        return XAMailApplication.RuleQualifier(OSType(self.xa_elem.qualifier().stringValue()))

    @qualifier.setter
    def qualifier(self, qualifier: XAMailApplication.RuleQualifier):
        self.set_property('qualifier', qualifier.value)

    @property
    def rule_type(self) -> XAMailApplication.RuleType:
        """The type of the rule.
        """
        return XAMailApplication.RuleType(OSType(self.xa_elem.ruleType().stringValue()))

    @rule_type.setter
    def rule_type(self, rule_type: XAMailApplication.RuleType):
        self.set_property('ruleType', rule_type.value)

    def delete(self):
        """Permanently deletes the rule condition.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()