""".. versionadded:: 0.0.1

Control the macOS Reminders application using JXA-like syntax.
"""

from datetime import datetime, timedelta
from typing import List, Literal, Union

import EventKit
import sys
import os

from AppKit import NSPredicate

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
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

    def _get_clipboard_reminder(self, reminder_name: str) -> 'XAReminder':
        return self.reminder({"name": reminder_name})

    ## Lists
    def __new_list(self, list_obj: EventKit.EKCalendar) -> 'XAReminderList':
        """Wrapper for creating a new XAReminder object.

        :param calender_obj: The EKCalendar object to wrap.
        :type calender_obj: EventKit.EKCalendar
        :return: A reference to the newly created PyXA reminder list object.
        :rtype: XAReminderList

        .. versionadded:: 0.0.2
        """
        scriptable_list = XABase.XAPredicate().from_args("id", list_obj.calendarIdentifier()).evaluate(self.xa_scel.lists())[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": list_obj,
            "scriptable_element": scriptable_list,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XAReminderList(properties)

    def lists(self, filter: dict = None) -> List['XAReminderList']:
        """Returns a list of reminder lists matching the filter.

        :param filter: The properties and desired values to filter reminder lists by.
        :type filter: dict
        :return: The list of reminder lists.
        :rtype: List[XAReminderList]

        :Example 1: Get all lists

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.lists())
        [<<class 'PyXA.apps.Reminders.XAReminderList'>General, id=22A058B0-5C62-4DE7-82CD-27DF96C3C354>, <<class 'PyXA.apps.Reminders.XAReminderList'>Shopping List, id=17D1D37C-4703-4E8A-98D8-968E4A639A5A>, ...]

        :Example 2: Get lists using a filter

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.lists({"title": "General"}))
        [<<class 'PyXA.apps.Reminders.XAReminderList'>General, id=22A058B0-5C62-4DE7-82CD-27DF96C3C354>]

        .. versionadded:: 0.0.1
        """
        lists = XABase.XAPredicate().from_args("allowReminders", True).evaluate(self.xa_estr.allCalendars())

        if filter is not None:
            if "id" in filter:
                filter["calendarIdentifier"] = filter["id"]
                filter.pop("id")
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            lists = lists.filteredArrayUsingPredicate_(predicate)

        elements = []
        for ls in lists:
            elements.append(self.__new_list(ls))
        return elements

    def list(self, filter: Union[int, dict]) -> 'XAReminderList':
        """Returns the first reminder list that matches the filter.

        :param filter: The properties and desired values to filter reminder lists by.
        :type filter: dict
        :return: The first reminder list that matches the filter.
        :rtype: XAReminderList

        :Example 1: Getting a list by index

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.list(0))
        <<class 'PyXA.apps.Reminders.XAReminderList'>General, id=22A058B0-5C62-4DE7-82CD-27DF96C3C354>

        :Example 2: Retrieving a list by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.list({"id": "17D1D37C-4703-4E8A-98D8-968E4A639A5A"}))
        <<class 'PyXA.apps.Reminders.XAReminderList'>Shopping List, id=17D1D37C-4703-4E8A-98D8-968E4A639A5A>

        .. versionadded:: 0.0.1
        """
        lists = self.xa_estr.allCalendars()
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_or_predicate_format([("allowReminders", True)]))
        lists = lists.filteredArrayUsingPredicate_(predicate)

        if isinstance(filter, int):
            return self.__new_list(lists[filter])

        if "id" in filter:
            filter["calendarIdentifier"] = filter["id"]
            filter.pop("id")
        
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
        lists = lists.filteredArrayUsingPredicate_(predicate)

        if len(lists) > 0:
            return self.__new_list(lists[0])

    def first_list(self) -> 'XAReminderList':
        """Returns the reminder list at the zero index of the lists array.

        :return: A reference to the first reminder list object.
        :rtype: XAReminderList

        .. versionadded:: 0.0.1
        """
        lists = self.xa_estr.allCalendars()
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_or_predicate_format([("allowReminders", True)]))
        lists = lists.filteredArrayUsingPredicate_(predicate)
        if len(lists) > 0:
            return self.__new_list(lists[0])

    def last_list(self) -> 'XAReminderList':
        """Returns the reminder list at the last (-1) index of the lists array.

        :return: A reference to the last reminder list object.
        :rtype: XAReminderList

        .. versionadded:: 0.0.1
        """
        lists = self.xa_estr.allCalendars()
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_or_predicate_format([("allowReminders", True)]))
        lists = lists.filteredArrayUsingPredicate_(predicate)
        if len(lists) > 0:
            return self.__new_list(lists[-1])

    ## Reminders
    def __new_reminder(self, reminder_obj: EventKit.EKReminder) -> 'XAReminder':
        """Wrapper for creating a new XAReminder object.

        :param calender_obj: The EKReminder object to wrap.
        :type calender_obj: EventKit.EKReminder
        :return: A reference to the newly created PyXA reminder object.
        :rtype: XAReminder

        .. versionadded:: 0.0.2
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": reminder_obj.localUID()}))
        scriptable_reminders = self.xa_scel.reminders()
        scriptable_reminder = scriptable_reminders.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": reminder_obj,
            "scriptable_element": scriptable_reminder,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XAReminder(properties)

    def reminders(self, filter: dict = None) -> List['XAReminder']:
        """Returns a list of reminders matching the filter.

        :param filter: The properties and desired values to filter reminders by.
        :type filter: dict
        :return: The list of reminders
        :rtype: List[XAReminder]

        :Example 1: Listing all reminders

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.reminders())
        [<<class 'PyXA.apps.Reminders.XAReminder'>Learn PyXA, id=3D50F4A6-826E-44D3-B6D7-E25EAEF24DD1>, <<class 'PyXA.apps.Reminders.XAReminder'>Make a PyXA Script, id=4419C590-235E-4D16-AB32-7B291626827D>, ...]

        :Example 2: Listing reminders by applying a filter

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.reminders({"title": "Learn PyXA"}))
        [<<class 'PyXA.apps.Reminders.XAReminder'>Learn PyXA, id=3D50F4A6-826E-44D3-B6D7-E25EAEF24DD1>]

        .. versionadded:: 0.0.1
        """
        
        predicate = self.xa_estr.predicateForRemindersInCalendars_(None)
        reminders = self.xa_estr.remindersMatchingPredicate_(predicate)

        if filter is not None:
            if "id" in filter:
                filter["calendarItemIdentifier"] = filter["id"]
                filter.pop("id")
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            reminders = reminders.filteredArrayUsingPredicate_(predicate)

        elements = []
        for reminder in reminders:
            elements.append(self.__new_reminder(reminder))
        return elements

    def reminder(self, filter: Union[int, dict]) -> 'XAReminder':
        """Returns the first reminder that matches the filter.

        :param filter: The properties and desired values to filter reminders by.
        :type filter: dict
        :return: The first reminder that matches the filter
        :rtype: XAReminder

        :Example 1: Getting a reminder by index

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.reminder(0))
        <<class 'PyXA.apps.Reminders.XAReminder'>Learn PyXA, id=3D50F4A6-826E-44D3-B6D7-E25EAEF24DD1>

        :Example 2: Getting a reminder by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Reminders")
        >>> print(app.reminder({"id": "4419C590-235E-4D16-AB32-7B291626827D"}))
        <<class 'PyXA.apps.Reminders.XAReminder'>Make a PyXA Script, id=4419C590-235E-4D16-AB32-7B291626827D>

        .. versionadded:: 0.0.1
        """
        predicate = self.xa_estr.predicateForRemindersInCalendars_(None)
        reminders = self.xa_estr.remindersMatchingPredicate_(predicate)

        if isinstance(filter, int):
            return self.__new_reminder(reminders[filter])

        if "id" in filter:
            filter["calendarItemIdentifier"] = filter["id"]
            filter.pop("id")
        
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
        reminders = reminders.filteredArrayUsingPredicate_(predicate)

        if len(reminders) > 0:
            return self.__new_reminder(reminders[0])

    def first_reminder(self) -> 'XAReminder':
        """Returns the reminder at the zero index of the reminders array.

        :return: A reference to the first reminder object.
        :rtype: XAReminderList

        .. versionadded:: 0.0.1
        """
        predicate = self.xa_estr.predicateForRemindersInCalendars_(None)
        reminders = self.xa_estr.remindersMatchingPredicate_(predicate)
        if len(reminders) > 0:
            return self.__new_reminder(reminders[0])

    def last_reminder(self) -> 'XAReminder':
        """Returns the reminder at the last (-1) index of the reminders array.

        :return: A reference to the last reminder object.
        :rtype: XAReminderList

        .. versionadded:: 0.0.1
        """
        predicate = self.xa_estr.predicateForRemindersInCalendars_(None)
        reminders = self.xa_estr.remindersMatchingPredicate_(predicate)
        if len(reminders) > 0:
            return self.__new_reminder(reminders[-1])

    def new_list(self, title: str = "New List", color: str = "#FF0000", emblem: str = "<null>") -> 'XAReminderList':
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.

        If no list is provided, the reminder is created in the default list.

        :param title: The name of the list, defaults to "New List"
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
        >>> print(new_list.id)
        6251B0DD-3770-410D-8601-1B33403F3595

        .. seealso:: :class:`XAReminderList`, :func:`new_reminder`

        .. versionadded:: 0.0.1
        """
        source = self.xa_estr.defaultCalendarForNewReminders().source()
        new_list = EventKit.EKCalendar.calendarForEntityType_eventStore_(EventKit.EKEntityTypeReminder, self.xa_estr)
        new_list.setTitle_(title)
        new_list.setColorString_(color)
        new_list.setSource_(source)
        self.xa_estr.saveCalendar_commit_error_(new_list, True, None)
        element = self.__new_list(new_list)
        element.xa_scel.setValue_forKey_(emblem, "emblem")
        return element

    def new_reminder(self, title: str = "New Reminder", notes: str = "", due_date: datetime = None, reminder_list: 'XAReminderList' = None) -> 'XAReminder':
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.
        If no list is provided, the reminder is created in the default list.

        :param title: The name of the reminder, defaults to "New Reminder"
        :type title: str, optional
        :param notes: The text notes attached to the reminder, defaults to ""
        :type notes: str, optional
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
        >>> print(reminder.id)
        B0DD7836-7C05-48D4-B806-D6A76317452E

        .. seealso:: :class:`XAReminder`, :func:`new_list`

        .. versionadded:: 0.0.1
        """
        if reminder_list is None:
            reminder_list = self.list(0)
        new_reminder = EventKit.EKReminder.reminderWithEventStore_(self.xa_estr)
        new_reminder.setCalendar_(reminder_list.xa_elem)
        new_reminder.setTitle_(title)
        new_reminder.setNotes_(notes)
        if due_date is not None:
            new_reminder.setDueDate_(due_date)
        self.xa_estr.saveReminder_commit_error_(new_reminder, True, None)
        return self.__new_reminder(new_reminder)


class XAReminderList(XABase.XAObject):
    """A class for interacting with Reminders lists.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminder`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.id = self.xa_elem.calendarIdentifier() #: A unique identifier for this list
        self.title = self.xa_elem.title() #: The name of the reminders list
        self.summary = self.xa_elem.summary() #: An overview of the list's information
        self.subscription_url = self.xa_elem.subscriptionURL() #: The URL of the list used to subscribe to it
        self.sharing_status: bool = self.xa_elem.sharingStatus() #: Whether the list is shared
        self.color: str = self.xa_elem.colorString() #: The HEX color of the list
        self.type = self.xa_elem.typeString() #: The list/calendar format
        self.notes = self.xa_elem.notes() #: Notes associated with the list
        self.sharees = self.xa_elem.sharees() #: A list of individuals with whom the list is shared with

    def show(self):
        """Shows the reminders list in Reminders.app.

        .. versionadded:: 0.0.2
        """
        self.xa_scel.show()

    def delete(self):
        """Deletes the list.

        .. versionadded:: 0.0.2
        """
        self.xa_estr.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
        self.xa_elem.markAsDeleted()
        self.xa_estr.deleteCalendar_forEntityType_error_(self.xa_elem, EventKit.EKEntityTypeReminder, None)

    def __repr__(self):
        return "<" + str(type(self)) + self.title + ", id=" + self.id + ">"


class XAReminder(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminderList`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.id: str = self.xa_elem.calendarItemIdentifier() #: A unique identifier for this reminder
        self.title: str = self.xa_elem.title() #: The name of the reminder
        self.all_day: bool = self.xa_elem.allDay() == 1 #: Whether the reminder is all day or a specific time
        self.creation_date: datetime = self.xa_elem.creationDate() #: The date the reminder was created
        self.modification_date: datetime = self.xa_elem.lastModifiedDate() #: The date the reminder was last modified
        self.notes: str = self.xa_elem.notes() #: User-inputted notes for this reminder
        self.priority: int = self.xa_elem.priorityNumber() #: A number representing the priority of the reminder
        self.url = self.xa_elem.URL() #: The URL attached to the reminder, if there is one
        self.completion_date: datetime = self.xa_elem.completionDate() #: The date the reminder should be completed by
        self.due_date: datetime = self.xa_elem.dueDateUnadjustedFromUTC() #: The date the reminder is due
        self.completion_status: bool = self.xa_elem.isCompleted() #: Whether the reminder has been completed

        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": self.xa_elem.recurrenceRule(),
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        if self.xa_elem.recurrenceRule() is None:
            self.recurrence_rule = None
        else:
            self.recurrence_rule = XAReminderRecurrenceRule(properties)

        alarms = []
        if self.xa_elem.alarms() is not None:
            for alarm in self.xa_elem.alarms():
                properties["element"] = alarm
                alarms.append(XAReminderAlarm(properties))
        self.alarms = alarms

    def show(self):
        """Shows the reminder in Reminders.app.

        .. versionadded:: 0.0.2
        """
        self.xa_estr.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, None)
        self.xa_scel.show()

    def delete(self):
        """Deletes the reminder.

        .. versionadded:: 0.0.2
        """
        self.xa_estr.removeReminder_commit_error_(self.xa_elem, True, None)

    def __repr__(self):
        return "<" + str(type(self)) + self.title + ", id=" + self.id + ">"


class XAReminderRecurrenceRule(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminderList`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.frequency = self.xa_elem.frequencyNumber() #: Specifier for the base unit of recurrence, i.e. daily, weekly, monthly, or yearly
        self.interval = self.xa_elem.intervalNumber() #: The number of frequency units between recurrences
        self.end_date = self.xa_elem.endDate() #: The end date and time of recurrence

    def set_frequency(self, frequency: Literal["daily", "weekly", "monthly", "yearly"]):
        """Sets the frequency of recurrence.

        :param frequency: A specifier for the base unit of recurrence.
        :type frequency: Literal["daily", "weekly", "monthly", "yearly"]

        .. versionadded:: 0.0.2
        """
        freq_ids = {
            "daily": 0,
            "weekly": 1,
            "monthly": 2,
            "yearly": 3,
        }
        self.xa_elem.setFrequency_(freq_ids[frequency])
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def set_interval(self, interval: int):
        """Sets the interval of recurrence.

        :param interval: The interval; the number of frequency units between recurrences.
        :type interval: int

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setInterval_(interval)
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def set_end_date(self, end_date: datetime):
        """Sets the date and time when the recurrence ends.

        :param end_date: The absolute end day of recurrence.
        :type end_date: datetime

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setEndDate_(end_date)
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def __repr__(self):
        return "<" + str(type(self)) + f"freq={self.xa_elem.frequencyString()}, interval={self.interval}, end_date={self.end_date}, id={self.id}>"


class XAReminderAlarm(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersApplication`, :class:`XAReminderList`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.id: str = self.xa_elem.sharedUID() #: A unique identifier for this alarm
        self.snoozed: bool = self.xa_elem.isSnoozed() #: Whether the alarm is snoozed
        self.date: datetime = self.xa_elem.absoluteDate() #: The date and time of a date-based alarm
        self.proximity_direction: str = self.xa_elem.proximityString() #: Whether a location-based alarm is for arriving or departing


        location = self.xa_elem.structuredLocation()
        self.location = None #: The location of a location-based alarm
        if location is not None:
            self.location = XABase.XALocation(
                title = location.title(),
                latitude = location.geoLocation().coordinate()[0],
                longitude = location.geoLocation().coordinate()[1],
                radius = location.radiusNumber() or 0,
                raw_value = location
            )

    def set_date(self, date: datetime):
        """Sets the date and time of the alarm.

        :param date: The absolute date that the alarm will go off.
        :type date: datetime

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setAbsoluteDate_(date)
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def set_location(self, location: XABase.XALocation):
        """Sets the location and radius of the alarm.

        :param location: The location (with specified radius) that the alarm will go off.
        :type location: XABase.XALocation

        .. versionadded:: 0.0.2
        """
        location.raw_value = self.location.raw_value
        location.prepare_for_export()
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def __repr__(self):
        return "<" + str(type(self)) + "id=" + self.id + ">"