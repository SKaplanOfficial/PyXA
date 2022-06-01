""".. versionadded:: 0.0.1

Control the macOS Calendar application using JXA-like syntax.
"""

from datetime import datetime, timedelta
from typing import List, Literal, Union

from ScriptingBridge import SBObject
from XABase import XAApplication, XAHasElements, XAShowable, XAWindow, XAObject
from XABaseScriptable import XASBApplication, XASBDeletable, XASBObject, XASBPrintable
from mixins.XAActions import XACanConstructElement, XAAcceptsPushedElements

class XACalendarApplication(XASBApplication, XACanConstructElement, XAAcceptsPushedElements):
    """A class for managing and interacting with scripting elements of the macOS Calendar application.

    .. seealso:: Classes :class:`XACalendar`, :class:`XACalendarEvent`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def reload_calendars(self) -> 'XACalendarApplication':
        self.properties["sb_element"].reloadCalendars()
        return self

    def switch_view_to(self, view: Literal["day", "week", "month"]):
        view_ids = {
            "day": 1161127009,
            "week": 1161131877,
            "month": 1161129327,
        }
        self.properties["sb_element"].switchViewTo_(view_ids[view])
        return self

    def view_calendar_at(self, date: datetime) -> 'XACalendarApplication':
        self.properties["sb_element"].viewCalendarAt_(date)
        return self

    def calendars(self, filter: dict = None) -> List['XACalendar']:
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("calendars", filter, XACalendar)

    def calendar(self, filter: Union[int, dict]) -> 'XACalendar':
        """Returns the first calendar matching the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_element_with_properties("calendars", filter, XACalendar)

    def first_calendar(self) -> 'XACalendar':
        """Returns the calendar at the zero index of the calendars array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("calendars", XACalendar)

    def last_calendar(self) -> 'XACalendar':
        """Returns the calendar at the last (-1) index of the calendars array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("calendars", XACalendar)

    def default_calendar(self) -> 'XACalendar':
        """Returns the calendar at the zero index of the calendars array. Synonymous with first_calendar().

        .. seealso:: :func:`first_calendar`

        .. versionadded:: 0.0.1
        """
        return self.first_calendar()

    def new_calendar(self, name: str = "New Calendar") -> 'XACalendar':
        """Creates a new calendar with the given name.

        :param name: The name of the calendar, defaults to "New Calendar"
        :type name: str, optional
        :return: A reference to the newly created calendar.
        :rtype: XACalendar

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> new_cal = app.new_calendar("Work")
        >>> print(new_cal.element.name())
        Work

        .. seealso:: :class:`XACalendar`

        .. versionadded:: 0.0.1
        """
        return self.push("calendar", {"name": name}, self.properties["sb_element"].calendars(), XACalendar)

    def new_event(self, name: str, start_date: datetime, end_date: datetime, calendar: Union['XACalendar', None] = None) -> 'XACalendarEvent':
        """Creates a new event with the given name and start/end dates in the specified calendar. If no calendar is specified, the default calendar is used.

        :param name: The name of the event
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

        .. seealso:: :class:`XACalendarEvent`

        .. versionadded:: 0.0.1
        """
        if calendar is None:
            return self.push("event", {"summary": name, "startDate": start_date, "endDate": end_date}, self.default_calendar().properties["element"].events(), XACalendarEvent)
        return self.push("event", {"summary": name, "startDate": start_date, "endDate": end_date}, calendar.properties["element"].events(), XACalendarEvent)


class XACalendar(XAHasElements, XAAcceptsPushedElements, XASBPrintable):
    """A class for interacting with calendars.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def events(self, filter: dict = None) -> List['XACalendarEvent']:
        """Returns a list of events, as PyXA objects, matching the given filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("events", filter, XACalendarEvent)

    def event(self, filter: Union[int, dict]) -> 'XACalendarEvent':
        """Returns the first event matching the given filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element_with_properties("events", filter, XACalendarEvent)

    def first_event(self) -> 'XACalendarEvent':
        """Returns the event at the zero index of the events array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("events", XACalendarEvent)

    def last_event(self) -> 'XACalendarEvent':
        """Returns the event at the last (-1) index of the events array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("events", XACalendarEvent)

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
        return super().push(element, None, self.properties["element"].events(), XACalendarEvent)

    def new_event(self, name: str, start_date: datetime, end_date: datetime) -> 'XACalendarEvent':
        """Create a new event and push it onto this calendar's events array.

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
        return self.properties["parent"].new_event(name, start_date, end_date, self)

    def __repr__(self):
        return self.properties["element"].name()


class XACalendarEvent(XASBObject, XAShowable, XASBDeletable):
    """A class for interacting with calendar events.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)