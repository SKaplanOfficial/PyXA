""".. versionadded:: 0.0.1

Control the macOS Calendar application using JXA-like syntax.
"""

from datetime import datetime, timedelta, date
from typing import List, Literal, Union

from ScriptingBridge import SBObject

import EventKit

from Foundation import NSURL
from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

# Calendar Constants
_YES = 2036691744
_NO = 2036691744
_ASK = 1634954016
_STANDARD_ERRORS = 1819767668
_DETAILED_ERRORS = 1819763828
_PARTICIPATION_UNKNOWN = 1161195105
_PARTICIPATION_ACCEPTED = 1161191792
_PARTICIPATION_DECLINED = 1161192560
_PARTICIPATION_TENTATIVE = 1161196656
_STATUS_CANCELLED = 1161061217
_STATUS_CONFIRMED = 1161061230
_STATUS_NONE = 1161064047
_STATUS_TENTATIVE = 1161065573
_NO_PRIORITY = 1952739376
_LOW_PRIORITY = 1952739385
_MEDIUM_PRIORITY = 1952739381
_HIGH_PRIORITY = 1952739377
_DAY_VIEW = 1161127009
_WEEK_VIEW = 1161131877
_MONTH_VIEW = 1161129327


class XACalendarApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with scripting elements of the macOS Calendar application.

    .. seealso:: Classes :class:`XACalendar`, :class:`XACalendarEvent`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_wcls = XACalendarWindow
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

    def reload_calendars(self) -> 'XACalendarApplication':
        """Reloads the contents of all calendars.

        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.reloadCalendars()
        return self

    def switch_view_to(self, view: Literal["day", "week", "month", "year"]) -> 'XACalendarApplication':
        """Switches to the target calendar view.

        :param view: The view to switch to.
        :type view: Literal["day", "week", "month"]
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        view_ids = {
            "day": _DAY_VIEW,
            "week": _WEEK_VIEW,
            "month": _MONTH_VIEW,
            "year": 3,
        }
        if view == "year":
            self.xa_estr.showDateInCalendar_inView_(0, view_ids[view])
        else:
            self.xa_scel.switchViewTo_(view_ids[view])
        return self

    def view_calendar_at(self, date: datetime, view: Literal["day", "week", "month", "year"] = "day") -> 'XACalendarApplication':
        """Displays the calendar at the provided date.

        :param date: The date to display.
        :type date: datetime
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        view_ids = {
            "day": 1,
            "week": 5,
            "month": 2,
            "year": 3,
        }
        self.xa_estr.showDateInCalendar_inView_(date, view_ids[view])
        return self

    def subscribe_to(self, url: str) -> 'XACalendarApplication':
        """Subscribes to the calendar at the specified URL.

        :param url: The URL of the calendar (in iCal format) to subscribe to.
        :type url: str
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.GetURL_(url)
        return self

    def __new_calendar(self, calender_obj: EventKit.EKCalendar) -> 'XACalendar':
        """Wrapper for creating a new XACalendar object.

        :param calender_obj: The EKCalendar object to wrap.
        :type calender_obj: EventKit.EKCalendar
        :return: A reference to the newly created PyXA calendar object.
        :rtype: XACalendar

        .. versionadded:: 0.0.1
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"name": calender_obj.title()}))
        scriptable_calendars = self.xa_scel.calendars()
        scriptable_calendar = scriptable_calendars.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": calender_obj,
            "scriptable_element": scriptable_calendar,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XACalendar(properties)

    def calendars(self, filter: dict = None) -> List['XACalendar']:
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        :param filter: A dictionary of property names and desired values that calendars in the resulting list will have.
        :type filter: dict
        :return: The list of calendar objects.
        :rtype: List[XACalendar]

        :Example: List all calendars

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendars = app.calendars()
        >>> print(calendars)
        [<PyXA.apps.Calendar.XACalendar object at 0x1046912e0>, <PyXA.apps.Calendar.XACalendar object at 0x1050912e0>, <PyXA.apps.Calendar.XACalendar object at 0x106ac9040>]

        :Example: Apply a simple filter

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendars = app.calendars({"name": "Calendar})
        >>> print(calendars)
        [<PyXA.apps.Calendar.XACalendar object at 0x1046912e0>]

        :Example: Filter with multiple parameters

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendars = app.calendars({"name": "Calendar", "calendarIdentifier": "4CF26E76-33D1-253D-A35E-147E66C2DF24"})
        >>> print(calendars)
        [<PyXA.apps.Calendar.XACalendar object at 0x1046912e0>]

        .. seealso:: :func:`calendar`

        .. versionadded:: 0.0.1
        """
        calendars = self.xa_estr.allCalendars()
        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            calendars = calendars.filteredArrayUsingPredicate_(predicate)

        elements = []
        for calendar in calendars:
            elements.append(self.__new_calendar(calendar))
        return elements

    def calendar(self, filter: Union[int, dict]) -> 'XACalendar':
        """Returns the first calendar matching the given filter.

        :param filter: A dictionary of property names and desired values that calendars in the returned calendar will have.
        :type filter: dict
        :return: The PyXA representation of the identified calendar.
        :rtype: XACalendar

        :Example 1: Get the calendar at a specific index

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.calendar(0)
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x1046912e0>

        :Example 2: Get a calendar by name

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.calendar({"title": "Calendar"})
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x1046912e0>

        :Example 3: Get a calendar by name and identifier

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.calendar({"title": "Calendar", "calendarIdentifier": "4CF26E76-33D1-253D-A35E-147E66C2DF24"})
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x1046912e0>

        .. note::
        
           If multiple calendars share the same property value, filtering by that value alone is not guaranteed to have a consistent return value. In such situations, you should supply multiple filter parameters to narrow the search to a single calendar item.

        .. seealso:: :func:`calendars`

        .. versionadded:: 0.0.1
        """
        calendar = None
        calendars = self.xa_estr.allCalendars()
        if isinstance(filter, int):
            calendar = calendars[filter]
        else:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            calendar = calendars.filteredArrayUsingPredicate_(predicate)[0]
        return self.__new_calendar(calendar)

    def first_calendar(self) -> 'XACalendar':
        """Returns the calendar at the zero index of the calendars array.

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.first_calendar()
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x1046912e0>

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.calendarsForEntityType_(0)[0]
        return self.__new_calendar(calendar)

    def last_calendar(self) -> 'XACalendar':
        """Returns the calendar at the last (-1) index of the calendars array.

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.last_calendar()
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x1050912e0>

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.calendarsForEntityType_(0)[-1]
        return self.__new_calendar(calendar)

    def default_calendar(self) -> 'XACalendar':
        """Returns the calendar that events are added to by default.

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> print(calendar)
        <PyXA.apps.Calendar.XACalendar object at 0x106ac9040>

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.defaultCalendarForNewEvents()
        return self.__new_calendar(calendar)

    def new_calendar(self, title: str = "New Calendar") -> 'XACalendar':
        """Creates a new calendar with the given name.

        :param name: The name of the calendar, defaults to "New Calendar"
        :type name: str, optional
        :return: A reference to the newly created calendar.
        :rtype: XACalendar

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> new_cal = app.new_calendar("Work")
        >>> print(new_cal.title)
        Work

        .. seealso:: :class:`XACalendar`

        .. versionadded:: 0.0.1
        """
        source = self.xa_estr.defaultCalendarForNewEvents().source()
        new_calendar = EventKit.EKCalendar.calendarForEntityType_eventStore_(EventKit.EKEntityTypeEvent, self.xa_estr)
        new_calendar.setTitle_(title)
        new_calendar.setSource_(source)
        self.xa_estr.saveCalendar_commit_error_(new_calendar, True, None)
        return self.__new_calendar(new_calendar)

    def __new_event(self, event_obj: EventKit.EKEvent, calendar: EventKit.EKCalendar) -> 'XACalendarEvent':
        """Wrapper for creating a new XACalendarEvent object.

        :param event_obj: The EKEvent object to wrap.
        :type event_obj: EventKit.EKEvent
        :param calendar: The EKCalendar object to create the event in.
        :type calendar: EventKit.EKCalendar
        :return: A reference to a PyXA calendar event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.2
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"title": calendar.title()}))
        calendar = self.xa_scel.calendars().filteredArrayUsingPredicate_(predicate)[0]

        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"uid": event_obj.localUID()}))
        scriptable_events = calendar.events()
        scripable_event = scriptable_events.filteredArrayUsingPredicate_(predicate)[0]

        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": event_obj,
            "scriptable_element": scripable_event,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XACalendarEvent(properties)

    def new_event(self, title: str, start_date: datetime, end_date: datetime, calendar: Union['XACalendar', None] = None) -> 'XACalendarEvent':
        """Creates a new event with the given name and start/end dates in the specified calendar. If no calendar is specified, the default calendar is used.

        :param name: The name of the event
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example: Create event on the default calendar

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.new_event("Learn about PyXA", start_date, end_date)
        >>> print(new_event)
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        :Example: Create event on a specific calendar

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> calendar = app.last_calendar()
        >>> new_event = app.new_event("Learn about PyXA", start_date, end_date, calendar)
        >>> print(new_event)
        <apps.Calendar.XACalendarEvent object at 0x105d063e0>

        .. seealso:: :class:`XACalendarEvent`

        .. versionadded:: 0.0.1
        """
        if calendar is None:
            calendar = self.default_calendar()
        new_event = EventKit.EKEvent.eventWithEventStore_(self.xa_estr)
        new_event.setCalendar_(calendar.xa_elem)
        new_event.setTitle_(title)
        new_event.setStartDate_(start_date)
        new_event.setEndDate_(end_date)
        self.xa_estr.saveEvent_span_commit_error_(new_event, EventKit.EKSpanThisEvent, True, None)
        return self.__new_event(new_event, calendar.xa_elem)


class XACalendarWindow(XABase.XAWindow):
    """A class for interacting with windows of Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)


class XACalendar(XABase.XAHasElements, XABase.XAAcceptsPushedElements, XABaseScriptable.XASBPrintable):
    """A class for interacting with calendars.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.id = self.xa_elem.calendarIdentifier() #: A unique identifier for the calendar
        self.title = self.xa_elem.title() #: The name of the calendar
        self.summary = self.xa_elem.summary() #: An overview of the calendar's information
        self.subscription_url = self.xa_elem.subscriptionURL() #: The URL of the calendar used to subscribe to it
        self.sharing_status: bool = self.xa_elem.sharingStatus() #: Whether the calendar is shared
        self.color: str = self.xa_elem.colorString() #: The HEX color of the calendar
        self.type = self.xa_elem.typeString() #: The calendar format
        self.notes = self.xa_elem.notes() #: Notes associated with the calendar
        self.sharees = self.xa_elem.sharees() #: A list of individuals with whom the calendar is shared with

    def delete(self):
        """Deletes the calendar.

        .. versionadded:: 0.0.2
        """
        self.xa_estr.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, None)
        self.xa_elem.markAsDeleted()
        self.xa_estr.deleteCalendar_forEntityType_error_(self.xa_elem, EventKit.EKEntityTypeEvent, None)

    def __new_event(self, event_obj) -> 'XACalendarEvent':
        """Wrapper for creating a new XACalendarEvent object.

        :param event_obj: The EKEvent object to wrap.
        :type event_obj: EventKit.EKEvent
        :return: A reference to a PyXA event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.2
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"uid": event_obj.localUID()}))
        scriptable_events = self.xa_scel.events()
        scripable_event = scriptable_events.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": event_obj,
            "scriptable_element": scripable_event,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XACalendarEvent(properties)

    def events(self, filter: dict = None) -> List['XACalendarEvent']:
        """Returns a list of events, as PyXA objects, matching the given filter.

        :param filter: The properties and desired values to filter events by.
        :type filter: dict
        :return: The list of events.
        :rtype: List[XACalendarEvent]

        :Example: Listing all events (not recommended)

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> print(calendar.events())
        [<PyXA.apps.Calendar.XACalendarEvent object at 0x108e71bb0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x108e7f9a0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x108e7fb80>, <PyXA.apps.Calendar.XACalendarEvent object at 0x108e7fd60>, ...]

        .. note::

           Querying for many events at a time can take considerable time. To avoid this, use filters to reduce the number of requested events or use a more specific method of this class that conducts a more narrow event search (see :func:`events_today`, :func:`week_events`, and :func:`events_in_range`).

        :Example: Listing filtered events (preferred)

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> print(calendar.events({"title": "Learn PyXA"}))
        [<PyXA.apps.Calendar.XACalendarEvent object at 0x108e71bb0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x108e7f9a0>]

        .. seealso:: :func:`event`

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))

        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            events = events.filteredArrayUsingPredicate_(predicate)

        elements = []
        for event in events:
            elements.append(self.__new_event(event))
        return elements

    def events_today(self) -> List['XACalendarEvent']:
        """Gets a list of all events in the next 24 hours.

        :return: The list of events.
        :rtype: List[XACalendarEvent]

        .. seealso:: :func:`week_events`

        .. versionadded:: 0.0.2
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 1)
        return self.events_in_range(start_date, end_date)

    def week_events(self) -> List['XACalendarEvent']:
        """Gets a list of events occurring in the next 7 days.

        :return: The list of events.
        :rtype: List[XACalendarEvent]

        .. seealso:: :func:`events_today`

        .. versionadded:: 0.0.2
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 7)
        return self.events_in_range(start_date, end_date)

    def events_in_range(self, start_date: datetime, end_date: datetime) -> List['XACalendarEvent']:
        """Gets a list of events occurring between the specified start and end datetimes.

        :param start_date: The earliest date an event in the list should begin.
        :type start_date: datetime
        :param end_date: The latest date an event in the list should end.
        :type end_date: datetime
        :return: The list of events.
        :rtype: List[XACalendarEvent]

        :Example:

        >>> from datetime import date
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> start_date = date(2022, 6, 4)
        >>> end_date = date(2022, 6, 6)
        >>> print(calendar.events_in_range(start_date, end_date))
        [<PyXA.apps.Calendar.XACalendarEvent object at 0x105b83d90>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90bb0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90dc0>]

        .. note::

           Querying events from a wide date range can take significant time. If you are looking for a specific subset of events within a large date range, it *might* be faster to use :func:`events` with a well-constructed filter and then iterate through the resulting array of objects, parsing out events outside of the desired date range.

        .. versionadded:: 0.0.2
        """
        calendar = self.xa_elem
        predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
        events = self.xa_estr.eventsMatchingPredicate_(predicate)

        elements = []
        for event in events:
            elements.append(self.__new_event(event))
        return elements

    def event(self, filter: Union[int, dict]) -> 'XACalendarEvent':
        """Returns the first event matching the given filter.

        :param filter: The properties and desired values to filter events by.
        :type filter: datetime
        :return: The list of events.
        :rtype: List['XACalendarEvent']

        :Example 1: Get an event by index

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> event = calendar.event(0)
        >>> print(event)
        <PyXA.apps.Calendar.XACalendarEvent object at 0x107b22d60>

        :Example 2: Get an event by matching filter parameters

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> event = calendar.event({"title": "Learn PyXA"})
        >>> print(event)
        <PyXA.apps.Calendar.XACalendarEvent object at 0x1049fad60>

        .. seealso:: :func:`events`

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
        
        event = None
        if isinstance(filter, int):
            event = events[filter]
        else:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            event = events.filteredArrayUsingPredicate_(predicate)[0]
        return self.__new_event(event)
        
    def first_event(self) -> 'XACalendarEvent':
        """Returns the event at the zero index of the events array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
            if len(events) > 0:
                break
        return self.__new_event(events[0])

    def last_event(self) -> 'XACalendarEvent':
        """Returns the event at the last (-1) index of the events array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(datetime.now().year, 2002, -4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
            if len(events) > 0:
                break
        return self.__new_event(events[0])

    def push(self, element: SBObject) -> 'XACalendarEvent':
        """Push a new element onto this calendar's list of events.

        :param element_specifier: An element created via this object's :func:`construct` method.
        :type element_specifier: SBObject
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.construct("event", {"summary": "Learn about PyXA", "startDate": start_date, "endDate": end_date})
        >>> print(cal.push(new_event))
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        .. seealso:: :func:`new_event`, :func:`construct`

        .. versionadded:: 0.0.1
        """
        return super().push(element, None, self.xa_elem.events(), XACalendarEvent)

    def new_event(self, name: str, start_date: datetime, end_date: datetime) -> 'XACalendarEvent':
        """Creates a new event and pushes it onto this calendar's events array.

        :param name: The name of the event.
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.new_event("Learn about PyXA", start_date, end_date)
        >>> print(new_event)
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        .. seealso:: :func:`push`, :func:`construct`

        .. versionadded:: 0.0.1
        """
        return self.xa_prnt.new_event(name, start_date, end_date, self)


class XACalendarEvent(XABase.XAObject):
    """A class for interacting with calendar events.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]
        
        self.description: str = self.xa_elem.description() #: An overview of the calendar's information
        self.creation_date: datetime = self.xa_elem.creationDate() #: The creation date adjusted for UTC offset
        self.start_date: datetime = self.xa_elem.startDate() #: The start date adjusted for UTC offset
        self.end_date: datetime = self.xa_elem.endDate() #: The end date adjusted for UTC offset
        self.all_day_event: bool = self.xa_elem.allDay() == 1 #: Whether the event is all day or not
        self.recurrence: str = self.xa_elem.recurrenceRuleString() #: A string describing the recurrence pattern of the event
        self.stamp_date: datetime = self.xa_elem.lastModifiedDate() #: The date the event was last modified
        self.status: str = self.xa_elem.status() #: The event's invite status, e.g. tentative or cancelled
        self.title: str = self.xa_elem.title() #: The name of the event
        self.location: str = self.xa_elem.location() #: The location associated with the event
        self.travel_duration: float = self.xa_elem.travelDuration() #: The time needed to get to the event in seconds
        self.duration: float = self.xa_elem.duration() #: The duration of the event in seconds
        self.uid: str = self.xa_elem.localUID() #: A unique identifier for the event
        self.identifier: str = self.xa_elem.calendarItemIdentifier() #: The unique identifier for the calendar the event belongs to
        self.url: NSURL = self.xa_elem.URL() #: The iCloud URL of the event
        self.notes: str = self.xa_elem.notes() #: Notes associated with the event
        self.organizer_name: str = self.xa_elem.organizerName() #: The name of the person who made the event
        self.organizer_email: str = self.xa_elem.organizerEmail() #: The email of the person who made the event
        self.organizer_phone_number: str = self.xa_elem.organizerPhoneNumber() #: The phone number of the person who made the event
        self.availability: bool = self.xa_elem.availability() #: Whether the event time is marked as `busy` or `available`.

    def rename(self, new_title: str) -> 'XACalendarEvent':
        """Renames the event.

        :param new_title: The new title of the event
        :type new_title: str
        :return: A reference to the event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.2
        """
        self.xa_scel.setValue_forKey_(new_title, "summary")
        return self

    def show(self) -> 'XACalendarEvent':
        """Shows the event in a calendar window.

        :return: A reference to the event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_scel.show()

    def delete(self):
        """Deletes the event.

        .. versionadded:: 0.0.1
        """
        self.xa_elem.markAsDeleted()
        self.xa_estr.removeEvent_span_error_(self.xa_elem, EventKit.EKSpanThisEvent, None)

    def duplicate(self) -> 'XACalendarEvent':
        """Duplicates the event, placing the copy on the same calendar.

        :return: A reference to the newly created event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        new_event = self.xa_elem.duplicate()
        self.xa_estr.saveEvent_span_error_(new_event, EventKit.EKSpanThisEvent, None)
        return new_event

    def copy_to(self, calendar: XACalendar) -> 'XACalendarEvent':
        """Makes a copy of this event and places it on the specified calendar.

        :param calendar: The calendar to copy the event to.
        :type calendar: XACalendar
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        :Example: Copy today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> calendar2 = app.calendar(2)
        >>> event = calendar.events_today()[0]
        >>> event.copy_to(calendar2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.2
        """
        self.xa_elem.copyToCalendar_withOptions_(calendar.xa_elem, 1)
        self.xa_estr.saveCalendar_commit_error_(calendar.xa_elem, True, None)
        return self

    def move_to(self, calendar: XACalendar) -> 'XACalendarEvent':
        """Moves this event to the specified calendar.

        :param calendar: The calendar to move the event to.
        :type calendar: XACalendar
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        :Example: Move today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> calendar2 = app.calendar(2)
        >>> event = calendar.events_today()[0]
        >>> event.move_to(calendar2)

        .. seealso:: :func:`copy_to`

        .. versionadded:: 0.0.2
        """
        self.copy_to(calendar)
        self.delete()
        return self

    def add_attachment(self, path: Union[str, NSURL]) -> 'XACalendarEvent':
        """Adds the file at the specified path as an attachment to the event.

        :param path: The path of the file to attach to the event.
        :type path: Union[str, NSURL]
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> calendar2 = app.calendar(1)
        >>> event = calendar.events_today()[0]
        >>> event.add_attachment("/Users/exampleuser/Image.png")

        .. versionadded:: 0.0.2
        """
        if isinstance(path, str):
            url = NSURL.alloc().initFileURLWithPath_(path)
        attachment = EventKit.EKAttachment.alloc().initWithFilepath_(url)
        self.xa_elem.addAttachment_(attachment)
        self.xa_estr.saveEvent_span_error_(self.xa_elem, EventKit.EKSpanThisEvent, None)
        return self

    # Attachments
    def __new_attachment(self, attachment_obj: EventKit.EKAttachment) -> 'XACalendarAttachment':
        """Wrapper for creating a new PyXA attachment object.

        :param attachment_obj: The EKAttachment object to wrap
        :type attachment_obj: EKAttachment
        :return: The PyXA object representation of the attachment
        :rtype: XACalendarAttachment

        .. versionadded:: 0.0.2
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": attachment_obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XACalendarAttachment(properties)

    def attachments(self, filter: dict = None) -> List['XACalendarAttachment']:
        """"Returns a list of attachments, as PyXA objects, matching the given filter.

        :return: The list of attachments.
        :rtype: List[XACalendarAttachment]

        .. versionadded:: 0.0.2
        """
        attachments = self.xa_elem.attachments()
        if len(attachments) == 0:
            return []

        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            attachments = attachments.filteredArrayUsingPredicate_(predicate)

        elements = []
        for attachment in attachments:
            elements.append(self.__new_attachment(attachment))
        return elements

    # Attendees
    def __new_attendee(self, attendee_obj: EventKit.EKAttendee) -> 'XACalendarAttendee':
        """Wrapper for creating a new PyXA attachment object.

        :param attendee_obj: The EKAttendee object to wrap
        :type attendee_obj: EKAttendee
        :return: The PyXA object representation of the attendee
        :rtype: XACalendarAttendee

        .. versionadded:: 0.0.2
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": attendee_obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XACalendarAttendee(properties)

    def attendees(self, filter: dict = None) -> List['XACalendarAttendee']:
        """"Returns a list of attendees, as PyXA objects, matching the given filter.

        :return: The list of attendees.
        :rtype: List[XACalendarAttendee]

        .. versionadded:: 0.0.2
        """
        attendees = self.xa_elem.attendees()
        if len(attendees) == 0:
            return []

        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            attendees = attendees.filteredArrayUsingPredicate_(predicate)

        elements = []
        for attendee in attendees:
            elements.append(self.__new_attendee(attendee))
        return elements

    # def display_alarms():
    #     pass

    # def mail_alarms():
    #     pass

    # def open_file_alarms():
    #     pass

    # def sound_alarms():
    #     pass

class XACalendarAttachment(XABase.XAObject):
    """A class for interacting with calendar event attachments.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.type = self.xa_elem.contentType() #: The content type of the attachment, e.g. `image/png`
        self.filename = self.xa_elem.filenameSuggestedByServer() #: The filename of the original document
        self.file = self.xa_elem.urlOnDisk() #: The location of the attachment on the local disk
        self.url = self.xa_elem.urlOnServer() #: The iCloud URL of the attachment
        self.uuid = self.xa_elem.uuid() #: A unique identifier for the attachment

    def open(self) -> 'XACalendarAttachment':
        """Opens the attachment in its default application.

        :return: A reference to the attachment object.
        :rtype: XACalendarAttachment
        
        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar()
        >>> event = calendar.events_today()[0]
        >>> event.attachments()[0].open()

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.openURL_(self.file)
        return self

class XACalendarAttendee(XABase.XAObject):
    """A class for interacting with calendar event attendees.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.name = self.xa_elem.name() #: The attendee's full name
        self.first_name = self.xa_elem.firstName()
        self.last_name = self.xa_elem.lastName()
        self.email_address = self.xa_elem.emailAddress()
        self.phone_number = self.xa_elem.phoneNumber()
        self.invited_by = self.xa_elem.inviterNameString() #: The name of the person who invited the attendee
