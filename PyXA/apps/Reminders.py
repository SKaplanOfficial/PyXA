""".. versionadded:: 0.0.1

Control the macOS Reminders application using JXA-like syntax.
"""

from datetime import datetime
from typing import List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

_YES = 2036691744
_NO = 1852776480
_ASK = 1634954016
_STANDARD_ERROR_HANDLING = 1819767668
_DETAILED_ERROR_HANDLING = 1819763828
_SAVABLE_FILE_FORMAT = 1668577396

class XARemindersApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with scripting elements of the Reminders application.

    .. seealso:: :class:`XAReminderList`, :class:`XAReminder`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.pasteboard_types = {
            "com.apple.reminders.reminderCopyPaste": self._get_clipboard_reminder,
        }

    def _get_clipboard_reminder(self, reminder_name: str) -> 'XAReminder':
        return self.reminder({"name": reminder_name})

    ## Lists
    def lists(self, filter: dict = None) -> List['XAReminderList']:
        """Returns a list of reminder lists matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("lists", filter, XAReminderList)

    def list(self, filter: Union[int, dict]) -> 'XAReminderList':
        """Returns the first reminder list that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("lists", filter, XAReminderList)

    def first_list(self) -> 'XAReminderList':
        """Returns the reminder list at the zero index of the lists array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("lists", XAReminderList)

    def last_list(self) -> 'XAReminderList':
        """Returns the reminder list at the last (-1) index of the lists array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("lists", XAReminderList)

    ## Reminders
    def reminders(self, filter: dict = None) -> List['XAReminder']:
        """Returns a list of reminders matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("reminders", filter, XAReminder)

    def reminder(self, filter: Union[int, dict]) -> 'XAReminder':
        """Returns the first reminder that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("reminders", filter, XAReminder)

    def first_reminder(self) -> 'XAReminder':
        """Returns the reminder at the zero index of the reminders array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("reminders", XAReminder)

    def last_reminder(self) -> 'XAReminder':
        """Returns the reminder at the last (-1) index of the reminders array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("reminders", XAReminder)

    def new_list(self, name: str = "New List", color: str = "#FF0000", emblem: str = "<null>") -> 'XAReminderList':
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.
        If no list is provided, the reminder is created in the default list.

        :param name: The name of the list, defaults to "New List"
        :type name: str, optional
        :param color: The HEX color of the list's icon.
        :type color: str, optional
        :param emblem: The symbol to use as the list's icon.
        :type emblem: str, optional
        :return: A reference to the newly created list.
        :rtype: XAReminderList

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Reminder")
        >>> new_list = app.new_reminder("Things To Do", "#336699", "symbol5")
        >>> print(new_list.properties)
        {
            color = "#336699";
            container = "<SBObject @0x600002c55cb0: <class 'acct'> id \"DCC06027-D549-4B64-9104-F08BF0BE0428\" of application \"Reminders\" (85867)>";
            emblem = symbol5;
            id = "749F2C11-19E2-4733-809C-8A8B3CF2534D";
            name = "Things To Do";
        }

        .. seealso:: :class:`XAReminderList`, :func:`new_reminder`

        .. versionadded:: 0.0.1
        """
        return self.push("list", {"name": name, "color": color, "emblem": emblem}, self.properties["sb_element"].lists(), XAReminderList)

    def new_reminder(self, name: str = "New Reminder", body: str = "", due_date: datetime = None, reminder_list: 'XAReminderList' = None) -> 'XAReminder':
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.
        If no list is provided, the reminder is created in the default list.

        :param name: The name of the reminder, defaults to "New Reminder"
        :type name: str, optional
        :param body: The body text of the reminder, defaults to ""
        :type body: str, optional
        :param due_date: The date and time when the reminder will be due.
        :type due_date: datetime, optional
        :param reminder_list: The list that the new reminder will be added to.
        :type reminder_list: XAReminderList, optional
        :return: A reference to the newly created reminder.
        :rtype: XAReminder

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Reminder")
        >>> due_date = datetime.now() + timedelta(hours = 1)
        >>> reminder = app.new_reminder("Read PyXA listation", "Complete 1 tutorial", due_date)
        >>> print(reminder.properties)
        {
            alldayDueDate = "2022-05-30 04:00:00 +0000";
            body = "Complete 1 tutorial";
            completed = 0;
            completionDate = "<null>";
            container = "<SBObject @0x600000af4030: <class 'list'> id \"22A058B0-5C62-4DE7-82CD-27DF96C3C354\" of application \"Reminders\" (83492)>";
            creationDate = "2022-05-30 19:53:29 +0000";
            dueDate = "2022-05-30 20:53:29 +0000";
            flagged = 0;
            id = "x-apple-reminder://0ADEF0EC-D08C-4594-975C-96D688520BFE";
            modificationDate = "2022-05-30 19:53:29 +0000";
            name = "Read PyXA listation";
            priority = 0;
            remindMeDate = "2022-05-30 20:53:29 +0000";
        }

        .. seealso:: :class:`XAReminder`, :func:`new_list`

        .. versionadded:: 0.0.1
        """
        if reminder_list is None:
            reminder_list = self.properties["sb_element"].reminders()
        else:
            reminder_list = reminder_list.properties["element"].reminders()

        if due_date is None:
            return self.push("reminder", {"name": name, "body": body}, reminder_list, XAReminder)
        return self.push("reminder", {"name": name, "body": body, "dueDate": due_date}, reminder_list, XAReminder)

class XAReminderList(XABase.XAObject):
    """A class for interacting with Reminders lists.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminder`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def __repr__(self):
        return self.name

class XAReminder(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminderList`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def __repr__(self):
        return self.name