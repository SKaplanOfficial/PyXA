""".. versionadded:: 0.0.1

Control the macOS Messages application using JXA-like syntax.
"""

from typing import List, Union

import XABase
import XABaseScriptable

_YES = 2036691744
_NO = 1852776480
_ASK = 1634954016
_STANDARD_ERRORS = 1819767668
_DETAILED_ERRORS = 1819763828
_TYPE_SMS = 1936944499
_TYPE_IMESSAGE = 1936289139
_INCOMING = 1179937123
_OUTGOING = 1179938663
_STATUS_PREPARING = 1179939696
_STATUS_WAITING = 1179939703
_STATUS_TRANSFERRING = 1179939687
_STATUS_FINALIZING = 1179939706
_STATUS_FINISHED = 1179939686
_STATUS_FAILED = 1179939685
_STATUS_DISCONNECTING = 1684237927
_STATUS_CONNECTED = 1668247150
_STATUS_CONNECTING = 1668247143
_STATUS_DISCONNECTED = 1684238190

class _XAHasChats(XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with chats in the Messages application.

    .. versionadded:: 0.0.1
    """
    def chats(self, filter: dict = None) -> List['XAChat']:
        """Returns a list of chats matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("chats", filter, XAChat)

    def chat(self, filter: Union[int, dict]) -> 'XAChat':
        """Returns the first chat that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("chats", filter, XAChat)

    def first_chat(self) -> 'XAChat':
        """Returns the chat at the first index of the chats array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("chats", XAChat)

    def last_chat(self) -> 'XAChat':
        """Returns the chat at the last (-1) index of the chats array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("chats", XAChat)


class _XAHasFileTransfers(XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with file transfers in the Messages application.

    .. versionadded:: 0.0.1
    """
    def file_transfers(self, filter: dict = None) -> List['XAMessagesFileTransfer']:
        """Returns a list of file transfers matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("fileTransfers", filter, XAMessagesFileTransfer)

    def file_transfer(self, filter: Union[int, dict]) -> 'XAMessagesFileTransfer':
        """Returns the first file transfer that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("fileTransfers", filter, XAMessagesFileTransfer)

    def first_file_transfer(self) -> 'XAMessagesFileTransfer':
        """Returns the file transfer at the first index of the file transfers array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("fileTransfers", XAMessagesFileTransfer)

    def last_file_transfer(self) -> 'XAMessagesFileTransfer':
        """Returns the file transfer at the last (-1) index of the file transfers array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("fileTransfers", XAMessagesFileTransfer)


class _XAHasParticipants(XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with participants in the Messages application.

    .. versionadded:: 0.0.1
    """
    def participants(self, filter: dict = None) -> List['XAMessagesParticipant']:
        """Returns a list of participants matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("participants", filter, XAMessagesParticipant)

    def participant(self, filter: Union[int, dict]) -> 'XAMessagesParticipant':
        """Returns the first participant that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("participants", filter, XAMessagesParticipant)

    def first_participant(self) -> 'XAMessagesParticipant':
        """Returns the participant at the first index of the participants array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("participants", XAMessagesParticipant)

    def last_participant(self) -> 'XAMessagesParticipant':
        """Returns the participant at the last (-1) index of the participants array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("participants", XAMessagesParticipant)


class _XAHasMessagesAccounts(XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with accounts in the Messages application.

    .. versionadded:: 0.0.1
    """
    def accounts(self, filter: dict = None) -> List['XAMessagesAccount']:
        """Returns a list of accounts matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("accounts", filter, XAMessagesAccount)

    def account(self, filter: Union[int, dict]) -> 'XAMessagesAccount':
        """Returns the first account that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("accounts", filter, XAMessagesAccount)

    def first_account(self) -> 'XAMessagesAccount':
        """Returns the account at the first index of the accounts array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("accounts", XAMessagesAccount)

    def last_account(self) -> 'XAMessagesAccount':
        """Returns the account at the last (-1) index of the accounts array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("accounts", XAMessagesAccount)


class XAMessagesApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, _XAHasChats, _XAHasFileTransfers, _XAHasParticipants, _XAHasMessagesAccounts):
    """A class for managing and interacting with Messages.app

     .. seealso:: :class:`XAChat`, :class:`XAMessagesFileTransfer`, :class:`XAMessagesParticipant`, :class:`XAMessagesAccount`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def send(self, message, chat):
        self.properties["sb_element"].send_to_(message, chat)


class XAChat(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, _XAHasParticipants):
    def __init__(self, properties):
        super().__init__(properties)

    def send(self, message):
        self.properties["parent"].send(message, self.properties["element"])


class XAMessagesFileTransfer(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    def __init__(self, properties):
        super().__init__(properties)

    def __repr__(self):
        return self.name


class XAMessagesParticipant(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    def __init__(self, properties):
        super().__init__(properties)

    def __repr__(self):
        return self.fullName


class XAMessagesAccount(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, _XAHasChats, _XAHasParticipants):
    def __init__(self, properties):
        super().__init__(properties)