from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Tuple, Union

import EventKit
from AppKit import NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

class XACalendarApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with scripting elements of the macOS Calendar application.

    .. seealso:: Classes :class:`XACalendarCalendar`, :class:`XACalendarEvent`

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for what to do when calling a save event.
        """
        SAVE_FILE   = XABase.OSType('yes ') #: Save the file. 
        DONT_SAVE   = XABase.OSType('no  ') #: Do not save the file. 
        ASK         = XABase.OSType('ask ') #: Ask the user whether or not to save the file. 

    class PrintSetting(Enum):
        """Options to use when printing.
        """
        STANDARD_ERROR_HANDLING = XABase.OSType('lwst') #: Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = XABase.OSType('lwdt') #: print a detailed report of PostScript errors

    class ParticipationStatus(Enum):
        """Event participation statuses.
        """
        UNKNOWN     = XABase.OSType('E6na') #: No answer yet
        ACCEPTED    = XABase.OSType('E6ap') #: Invitation has been accepted
        DECLINED    = XABase.OSType('E6dp') #: Invitation has been declined
        TENTATIVE   = XABase.OSType('E6tp') #: Invitation has been tentatively accepted

    class EventStatus(Enum):
        """Event confirmation statuses.
        """
        CANCELLED   = XABase.OSType('E4ca') #: A cancelled event
        CONFIRMED   = XABase.OSType('E4cn') #: A confirmed event
        NONE        = XABase.OSType('E4no') #: An event without a status
        TENTATIVE   = XABase.OSType('E4te') #: A tentative event

    class Priority(Enum):
        """Event priorities.
        """
        NONE    = XABase.OSType('tdp0') #: No priority assigned
        LOW     = XABase.OSType('tdp9') #: Low priority
        MEDIUM  = XABase.OSType('tdp5') #: Medium priority
        HIGH    = XABase.OSType('tdp1') #: High priority

    class ViewType(Enum):
        """Views in Calendar.app.
        """
        DAY     = XABase.OSType('E5da') #: The iCal day view
        WEEK    = XABase.OSType('E5we') #: The iCal week view
        MONTH   = XABase.OSType('E5mo') #: The iCal month view
        YEAR    = XABase.OSType('E5ye') #: The iCal year view

    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_wcls = XACalendarWindow
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

        self.properties: dict #: All properties of the application
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Calendar is the frontmost application
        self.version: str #: The version of the Calendar application
        self.default_calendar: XACalendarCalendar #: The calendar that events are added to by default

    @property
    def properties(self) -> dict:
        return self.xa_scel.properties()

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
    def default_calendar(self) -> 'XACalendarCalendar':
        calendar_obj = self.xa_estr.defaultCalendarForNewEvents()
        return self.calendars().by_name(calendar_obj.title())

    def reload_calendars(self) -> 'XACalendarApplication':
        """Reloads the contents of all calendars.

        :return: The application object
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.reloadCalendars()
        return self

    def switch_view_to(self, view: 'XACalendarApplication.ViewType') -> 'XACalendarApplication':
        """Switches to the target calendar view.

        :param view: The view to switch to.
        :type view: XACalendarApplication.ViewType
        :return: The application object
        :rtype: XACalendarApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> app.switch_view_to(app.ViewType.WEEK)
        >>> app.switch_view_to(app.ViewType.DAY)
        >>> app.switch_view_to(app.ViewType.MONTH)
        >>> app.switch_view_to(app.ViewType.YEAR)

        .. versionadded:: 0.0.1
        """
        if view == XACalendarApplication.ViewType.YEAR:
            self.xa_estr.showDateInCalendar_inView_(0, 3)
        else:
            self.xa_scel.switchViewTo_(view.value)
        return self

    def view_calendar_at(self, date: datetime, view: Union[None, 'XACalendarApplication.ViewType'] = None) -> 'XACalendarApplication':
        """Displays the calendar at the provided date.

        :param date: The date to display.
        :type date: datetime
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        :Example:

        >>> import PyXA
        >>> from datetime import date
        >>> app = PyXA.application("Calendar")
        >>> date1 = date(2022, 7, 20)
        >>> app.view_calendar_at(date1)

        .. versionadded:: 0.0.1
        """
        if view is None:
            self.xa_estr.showDateInCalendar_inView_(date, 1)
        elif view == XACalendarApplication.ViewType.YEAR:
            self.xa_estr.showDateInCalendar_inView_(date, 3)
        else:
            self.xa_estr.showDateInCalendar_inView_(date, 0)
            self.xa_scel.switchViewTo_(view.value)
        return self

    def subscribe_to(self, url: str) -> 'XACalendarCalendar':
        """Subscribes to the calendar at the specified URL.

        :param url: The URL of the calendar (in iCal format) to subscribe to
        :type url: str
        :return: The newly created calendar object
        :rtype: XACalendarCalendar

        .. versionadded:: 0.0.1
        """
        self.xa_scel.GetURL_(url)
        return self.calendars()[-1]

    def documents(self, filter: Union[dict, None] = None) -> 'XACalendarDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XARemindersDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XACalendarDocumentList, filter)

    def calendars(self, filter: Union[dict, None] = None) -> 'XACalendarCalendarList':
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned calendars will have, or None
        :type filter: Union[dict, None]
        :return: The list of calendars
        :rtype: XACalendarCalendarList

        :Example 1: Get all calendars

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> print(app.calendars())
        <<class 'PyXA.apps.Calendar.XACalendarCalendarList'>['Calendar', 'Calendar2', 'Calendar3', ...]>

        :Example 2: Get calendars using a filter

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> print(app.calendars({"name": "Calendar"})[0])
        <<class 'PyXA.apps.Calendar.XACalendarCalendar'>Calendar>

        :Example 3: Get calendars using list methods

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> print(app.calendars().by_name("Calendar"))
        <<class 'PyXA.apps.Calendar.XACalendarCalendar'>Calendar>

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.calendars(), XACalendarCalendarList, filter)

    def new_calendar(self, name: str = "New Calendar") -> 'XACalendarCalendar':
        """Creates a new calendar with the given name.

        :param name: The name of the calendar, defaults to "New Calendar"
        :type name: str, optional
        :return: The newly created calendar object
        :rtype: XACalendarCalendar

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> app.new_calendar("PyXA Development")

        .. versionadded:: 0.0.1
        """
        new_calendar = self.make("calendar", {"name": name})
        self.calendars().push(new_calendar)
        
        desc = new_calendar.xa_elem.description()
        id = desc[desc.index("id") + 4: desc.index("of app") - 3]
        return reversed(self.calendars()).by_name(name)

    def new_event(self, summary: str, start_date: datetime, end_date: datetime, calendar: Union['XACalendarCalendar', None] = None) -> 'XACalendarEvent':
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
        >>> app.new_event("Learn about PyXA", start_date, end_date)

        :Example: Create event on a specific calendar

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> calendar = app.calendars()[-1]
        >>> app.new_event("Learn about PyXA", start_date, end_date, calendar)

        .. versionadded:: 0.0.1
        """
        if calendar is None:
            calendar = self.default_calendar
        new_event = self.make("event", {"summary": summary, "startDate": start_date, "endDate": end_date})
        calendar.events().push(new_event)
        return calendar.events().by_uid(new_event.uid)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new calendar

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> new_calendar = app.make("calendar", {"name": "PyXA Development"})
        >>> app.calendars().push(new_calendar)

        :Example 2: Make a new event

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.make("event", {"summary": "Work on PyXA", "startDate": start_date, "endDate": end_date})
        >>> app.default_calendar.events().push(new_event)

        .. versionadded:: 0.0.6
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XACalendarDocument)
        elif specifier == "calendar":
            return self._new_element(obj, XACalendarCalendar)
        elif specifier == "event":
            return self._new_element(obj, XACalendarEvent)
        elif specifier == "displayAlarm":
            return self._new_element(obj, XACalendarDisplayAlarm)
        elif specifier == "mailAlarm":
            return self._new_element(obj, XACalendarMailAlarm)
        elif specifier == "soundAlarm":
            return self._new_element(obj, XACalendarSoundAlarm)
        elif specifier == "openFileAlarm":
            return self._new_element(obj, XACalendarOpenFileAlarm)




class XACalendarWindow(XABaseScriptable.XASBWindow):
    """A window of Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.properties: dict #: All properties of the window
        self.name: str #: The name of the window
        self.id: str #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XACalendarDocument #: The current document displayed in the window

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
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
    def document(self) -> 'XACalendarDocument':
        return self._new_element(self.xa_elem.document(), XACalendarDocument)




class XACalendarDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarDocument, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))
        
    def name(self) -> List[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of document file paths
        :rtype: List[XABase.XAPath]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def by_properties(self, properties: dict) -> Union['XACalendarDocument', None]:
        """Retrieves the document whose properties matches the given properties dictionary, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACalendarDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union['XACalendarDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACalendarDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XACalendarDocument', None]:
        """Retrieves the document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACalendarDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAPath) -> Union['XACalendarDocument', None]:
        """Retrieves the document whose file matches the given file path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACalendarDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XACalendarDocument(XABaseScriptable.XASBObject):
    """A document in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since it was last saved
        self.file: XABase.XAPath #: The location of the document on disk, if it has one

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.file())




class XACalendarCalendarList(XABase.XAList):
    """A wrapper around lists of calendars that employs fast enumeration techniques.

    All properties of calendars can be called as methods on the wrapped list, returning a list containing each calendar's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarCalendar, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each calendar in the list.

        :return: A list of calendar properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        """Gets the name of each calendar in the list.

        :return: A list of calendar names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def color(self) -> List[str]:
        """Gets the color of each calendar in the list.

        :return: A list of calendar color strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("color")
        return [XABase.XAColor(x) for x in ls]

    def calendar_identifier(self) -> List[str]:
        """Gets the ID of each calendar in the list.

        :return: A list of calendar IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("calendarIdentifier"))

    def writable(self) -> List[bool]:
        """Gets the writable status of each calendar in the list.

        :return: A list of calendar writable status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("writable"))

    def description(self) -> List[str]:
        """Gets the description of each calendar in the list.

        :return: A list of calendar descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("description"))

    def events(self) -> 'XACalendarEventList':
        """Gets the events of each calendar in the list.

        :return: A list of calendar events
        :rtype: XACalendarEventList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("events")
        return self._new_element(ls, XACalendarEventList)

    def by_properties(self, properties: dict) -> Union['XACalendarCalendar', None]:
        """Retrieves the calendar whose properties matches the given properties dictionary, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union['XACalendarCalendar', None]:
        """Retrieves the calendar whose name matches the given name, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_color(self, color: XABase.XAColor) -> Union['XACalendarCalendar', None]:
        """Retrieves the first calendar whose color matches the given color string, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("color", color.xa_elem)

    def by_calendar_identifier(self, calendar_identifier: str) -> Union['XACalendarCalendar', None]:
        """Retrieves the calendar whose ID matches the given ID, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("calendarIdentifier", calendar_identifier)

    def by_writable(self, writable: bool) -> Union['XACalendarCalendar', None]:
        """Retrieves the first calendar whose writable status matches the given boolean value, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("writable", writable)

    def by_description(self, description: str) -> Union['XACalendarCalendar', None]:
        """Retrieves the calendar whose description matches the given description string, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XACalendarCalendar, None]
        
        .. versionadded:: 0.0.6
        """
        for calendar in self:
            if calendar.description == description:
                return calendar

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XACalendarCalendar(XABaseScriptable.XASBObject):
    """A calendar in Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

        self.properties: dict #: All properties of the calendar
        self.name: str #: The name of the calendar
        self.color: XABase.XAColor #: The color of the calendar
        self.calendar_identifier: str #: The unique identifier for the calendar
        self.writable: bool #: Whether the calendar is writable
        self.description: str #: The description of the calendar

        if hasattr(self.xa_elem, "name"):
            calendars = self.xa_estr.allCalendars()
            predicate = XABase.XAPredicate()
            predicate.add_eq_condition("title", self.name)
            self.calendar_obj = predicate.evaluate(calendars)

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.color())

    @property
    def calendar_identifier(self) -> str:
        return self.xa_elem.calendarIdentifier()

    @property
    def writable(self) -> bool:
        return self.xa_elem.writable()

    @property
    def description(self) -> str:
        return self.xa_elem.description()

    def delete(self) -> 'XACalendarEvent':
        """Deletes the calendar.

        .. versionadded:: 0.0.2
        """
        self.xa_estr.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, None)
        self.xa_calendar.markAsDeleted()
        self.xa_estr.deleteCalendar_forEntityType_error_(self.xa_calendar, EventKit.EKEntityTypeEvent, None)

    def events_in_range(self, start_date: datetime, end_date: datetime) -> 'XACalendarEventList':
        """Gets a list of events occurring between the specified start and end datetimes.

        :param start_date: The earliest date an event in the list should begin.
        :type start_date: datetime
        :param end_date: The latest date an event in the list should end.
        :type end_date: datetime
        :return: The list of events.
        :rtype: XACalendarEventList

        :Example:

        >>> from datetime import date
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar
        >>> start_date = date(2022, 6, 4)
        >>> end_date = date(2022, 6, 6)
        >>> print(calendar.events_in_range(start_date, end_date))
        [<PyXA.apps.Calendar.XACalendarEvent object at 0x105b83d90>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90bb0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90dc0>]

        .. note::

           Querying events from a wide date range can take significant time. If you are looking for a specific subset of events within a large date range, it *might* be faster to use :func:`events` with a well-constructed filter and then iterate through the resulting array of objects, parsing out events outside of the desired date range.

        .. versionadded:: 0.0.2
        """
        predicate = XABase.XAPredicate()
        predicate.add_geq_condition("startDate", start_date)
        predicate.add_leq_condition("endDate", end_date)
        events_in_range = predicate.evaluate(self.xa_elem.events())
        return self._new_element(events_in_range, XACalendarEventList)

    def events_today(self) -> 'XACalendarEventList':
        """Gets a list of all events in the next 24 hours.

        :return: The list of events.
        :rtype: XACalendarEventList

        .. seealso:: :func:`week_events`

        .. versionadded:: 0.0.2
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 1)
        return self.events_in_range(start_date, end_date)

    def week_events(self) -> 'XACalendarEventList':
        """Gets a list of events occurring in the next 7 days.

        :return: The list of events.
        :rtype: XACalendarEventList

        .. seealso:: :func:`events_today`

        .. versionadded:: 0.0.2
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 7)
        return self.events_in_range(start_date, end_date)

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

        .. versionadded:: 0.0.1
        """
        return self.xa_prnt.xa_prnt.new_event(name, start_date, end_date, self)

    def events(self, filter: Union[dict, None] = None) -> 'XACalendarEventList':
        """Returns a list of events, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned events will have, or None
        :type filter: Union[dict, None]
        :return: The list of events
        :rtype: XACalendarEventList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.events(), XACalendarEventList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"




class XACalendarAlarm(XABaseScriptable.XASBObject):
    """An event alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.properties: dict #: All properties of the alarm
        self.trigger_interval: int #: The interval in minutes between the event and the alarm
        self.trigger_date: datetime #: The date of the alarm

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def trigger_interval(self) -> int:
        return self.xa_elem.triggerInterval()

    @property
    def trigger_date(self) -> datetime:
        return self.xa_elem.triggerDate()




class XACalendarDisplayAlarm(XACalendarAlarm):
    """A display alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)




class XACalendarMailAlarm(XACalendarAlarm):
    """A mail alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)




class XACalendarSoundAlarm(XACalendarAlarm):
    """A sound alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.sound_name: str #: The system sound name to be used for the alarm
        self.sound_file: str #: The path to the sound file to be used for the alarm

    @property
    def sound_name(self) -> str:
        return self.xa_elem.soundName()

    @property
    def sound_file(self) -> str:
        return self.xa_elem.soundFile()




class XACalendarOpenFileAlarm(XACalendarAlarm):
    """An open file alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.file_path: str #: The path to be opened by the alarm

    @property
    def file_path(self) -> str:
        return self.xa_elem.filePath()




class XACalendarAttendeeList(XABase.XAList):
    """A wrapper around lists of attendees that employs fast enumeration techniques.

    All properties of attendees can be called as methods on the wrapped list, returning a list containing each attendee's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarEvent, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each attendee in the list.

        :return: A list of attendee properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def display_name(self) -> List[str]:
        """Gets the display name of each attendee in the list.

        :return: A list of attendee first and last names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayName"))

    def email(self) -> List[str]:
        """Gets the email address of each attendee in the list.

        :return: A list of attendee email addresses
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("email"))

    def participation_status(self) -> List[XACalendarApplication.ParticipationStatus]:
        """Gets the participation status of each attendee in the list.

        :return: A list of attendee participation statuses
        :rtype: List[XACalendarApplication.ParticipationStatus]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("participationStatus")
        return [XACalendarApplication.ParticipationStatus(XABase.OSType(x.stringValue())) for x in ls]

    def by_properties(self, properties: dict) -> Union['XACalendarAttendee', None]:
        """Retrieves the attendee whose properties matches the given properties dictionary, if one exists.

        :return: The desired attendee, if it is found
        :rtype: Union[XACalendarAttendee, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_display_name(self, display_name: str) -> Union['XACalendarAttendee', None]:
        """Retrieves the attendee whose display name matches the given first and last names, if one exists.

        :return: The desired attendee, if it is found
        :rtype: Union[XACalendarAttendee, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("displayName", display_name)

    def by_email(self, email: str) -> Union['XACalendarAttendee', None]:
        """Retrieves the attendee whose email address matches the given email address, if one exists.

        :return: The desired attendee, if it is found
        :rtype: Union[XACalendarAttendee, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("email", email)

    def by_participation_status(self, participation_status: XACalendarApplication.ParticipationStatus) -> Union['XACalendarAttendee', None]:
        """Retrieves the attendee whose participation status matches the given status, if one exists.

        :return: The desired attendee, if it is found
        :rtype: Union[XACalendarAttendee, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("participationStatus", participation_status.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.display_name()) + ">"

class XACalendarAttendee(XABaseScriptable.XASBObject):
    """An event attendee in Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.properties: dict #: All properties of the attendee
        self.display_name: str #: The first and last name of the attendee
        self.email: str #: The email address of the attendee
        self.participation_status: XACalendarApplication.ParticipationStatus #: The invitation status for the attendee

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def email(self) -> str:
        return self.xa_elem.email()

    @property
    def participation_status(self) -> XACalendarApplication.ParticipationStatus:
        return XACalendarApplication.ParticipationStatus(self.xa_elem.participationStatus())




class XACalendarEventList(XABase.XAList):
    """A wrapper around lists of events that employs fast enumeration techniques.

    All properties of events can be called as methods on the wrapped list, returning a list containing each event's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarEvent, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each event in the list.

        :return: A list of event properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def description(self) -> List[str]:
        """Gets the description of each event in the list.

        :return: A list of event descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("description"))

    def start_date(self) -> List[datetime]:
        """Gets the start date of each event in the list.

        :return: A list of event start dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("startDate"))

    def properties(self) -> List[datetime]:
        """Gets the end date of each event in the list.

        :return: A list of event end dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("endDate"))

    def allday_event(self) -> List[bool]:
        """Gets the all-day status of each event in the list.

        :return: A list of event all-day status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("alldayEvent"))

    def recurrence(self) -> List[str]:
        """Gets the recurrence string of each event in the list.

        :return: A list of event recurrence strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("recurrence"))

    def sequence(self) -> List[int]:
        """Gets the version of each event in the list.

        :return: A list of event versions
        :rtype: List[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sequence"))

    def stamp_date(self) -> List[datetime]:
        """Gets the modification date of each event in the list.

        :return: A list of event modification dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("stampDate"))

    def excluded_dates(self) -> List[List[datetime]]:
        """Gets the excluded dates of each event in the list.

        :return: A list of event excluded dates
        :rtype: List[List[datetime]]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("excludedDates"))

    def status(self) -> List[XACalendarApplication.EventStatus]:
        """Gets the status of each event in the list.

        :return: A list of event statuses
        :rtype: List[XACalendarApplication.EventStatus]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("status")
        return [XACalendarApplication.EventStatus(XABase.OSType(x.stringValue())) for x in ls]

    def summary(self) -> List[str]:
        """Gets the summary of each event in the list.

        :return: A list of event summaries
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("summary"))

    def location(self) -> List[str]:
        """Gets the location string of each event in the list.

        :return: A list of event locations
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("location"))

    def uid(self) -> List[str]:
        """Gets the unique identifier of each event in the list.

        :return: A list of event IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("uid"))

    def url(self) -> List[str]:
        """Gets the URL associated to each event in the list.

        :return: A list of event URLs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def by_properties(self, properties: dict) -> Union['XACalendarEvent', None]:
        """Retrieves the event whose properties matches the given properties dictionary, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_description(self, description: str) -> Union['XACalendarEvent', None]:
        """Retrieves the event whose description matches the given description string, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("description", description)

    def by_start_date(self, start_date: datetime) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose start date matches the given date, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("startDate", start_date)

    def by_end_date(self, end_date: datetime) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose end date matches the given date, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("endDate", end_date)

    def by_allday_event(self, allday_event: bool) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose all-day even status matches the given boolean value, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("alldayEvent", allday_event)

    def by_recurrence(self, recurrence: str) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose recurrence string matches the given string, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("recurrence", recurrence)

    def by_sequence(self, sequence: int) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose sequence (version) matches the given sequence number, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("sequence", sequence)

    def by_stamp_date(self, stamp_date: datetime) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose stamp date matches the given date, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("stampDate", stamp_date)

    def by_excluded_dates(self, excluded_dates: List[datetime]) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose excluded dates date matches the given list of dates, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("excludedDates", excluded_dates)

    def by_status(self, status: XACalendarApplication.EventStatus) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose status matches the given status, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]

        
        .. versionadded:: 0.0.6
        """
        return self.by_property("status", status.value)

    def by_summary(self, summary: str) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose summary matches the given string, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("summary", summary)

    def by_location(self, location: str) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose location string matches the given location, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("location", location)

    def by_uid(self, uid: str) -> Union['XACalendarEvent', None]:
        """Retrieves the event whose unique identifier matches the given ID string, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("uid", uid)

    def by_url(self, url: str) -> Union['XACalendarEvent', None]:
        """Retrieves the first event whose associated URL matches the given URL string, if one exists.

        :return: The desired event, if it is found
        :rtype: Union[XACalendarEvent, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("URL", url)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.summary()) + ">"

class XACalendarEvent(XABaseScriptable.XASBObject):
    """An event in Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

        self.properties: dict #: All properties of the event
        self.description: str #: The event's notes
        self.start_date: datetime #: The start date and time of the event
        self.end_date: datetime #: The end date and time of the event
        self.allday_event: bool #: Whether the event is an all-day event
        self.recurrence: str #: A string describing the event recurrence
        self.sequence: int #: The event version
        self.stamp_date: date #: The date the event was last modified
        self.excluded_dates: List[datetime] #: The exception dates for the event
        self.status: XACalendarApplication.EventStatus #: The status of the event
        self.summary: str #: The summary (title) of the event
        self.location: str #: The location of the event
        self.uid: str #: A unique identifier for the event
        self.url: str #: The URL associated with the event

        if hasattr(self.xa_elem, "uid"):
            events = NSMutableArray.arrayWithArray_([])
            for year in range(2006, datetime.now().year + 4, 4):
                start_date = date(year, 1, 1)
                end_date = start_date + timedelta(days = 365 * 4)
                predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, None)
                events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
            self.xa_event_obj = XABase.XAPredicate.evaluate_with_dict(events, {"calendarItemIdentifier": self.uid})[0]

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def description(self) -> str:
        return self.xa_elem.description()

    @property
    def start_date(self) -> datetime:
        return self.xa_elem.startDate()

    @property
    def end_date(self) -> datetime:
        return self.xa_elem.endDate()

    @property
    def allday_event(self) -> bool:
        return self.xa_elem.alldayEvent()

    @property
    def recurrence(self) -> str:
        return self.xa_elem.recurrence()

    @property
    def sequence(self) -> int:
        return self.xa_elem.sequence()

    @property
    def stamp_date(self) -> datetime:
        return self.xa_elem.stampDate()

    @property
    def excluded_dates(self) -> List[datetime]:
        return self.xa_elem.excludedDates()

    @property
    def status(self) -> XACalendarApplication.EventStatus:
        return XACalendarApplication.EventStatus(XABase.OSType(self.xa_elem.status().stringValue())) 

    @property
    def summary(self) -> str:
        return self.xa_elem.summary()

    @property
    def location(self) -> str:
        return self.xa_elem.location()

    @property
    def uid(self) -> str:
        return self.xa_elem.uid()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    def show(self) -> 'XACalendarEvent':
        """Shows the event in the front calendar window.

        :return: The event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_elem.show()
        return self

    def delete(self):
        """Deletes the event.

        .. versionadded:: 0.0.1
        """
        self.xa_estr.removeEvent_span_error_(self.xa_event_obj, EventKit.EKSpanThisEvent, None)

    def duplicate(self) -> 'XACalendarEvent':
        """Duplicates the event, placing the copy on the same calendar.

        :return:The newly created event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        new_event = self.xa_event_obj.duplicate()
        self.xa_estr.saveEvent_span_error_(new_event, EventKit.EKSpanThisEvent, None)

    def duplicate_to(self, calendar: XACalendarCalendar) -> 'XACalendarEvent':
        """Duplicates the event, placing the copy on the same calendar.

        :return: The event object that this method was called from
        :rtype: XACalendarEvent

        :Example: Copy today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[2]
        >>> event = calendar.events_today()[0]
        >>> event.duplicate_to(calendar2)

        .. seealso:: :func:`duplicate`, :func:`move_to`

        .. versionadded:: 0.0.1
        """
        calendars = self.xa_estr.allCalendars()
        calendar_obj = XABase.XAPredicate.evaluate_with_dict(calendars, {"title": calendar.name})[0]

        self.xa_event_obj.copyToCalendar_withOptions_(calendar_obj, 1)
        self.xa_estr.saveCalendar_commit_error_(calendar_obj, True, None)
        return self

    def move_to(self, calendar: XACalendarCalendar) -> 'XACalendarEvent':
        """Moves this event to the specified calendar.

        :param calendar: The calendar to move the event to.
        :type calendar: XACalendar
        :return: A reference to the moved event object.
        :rtype: XACalendarEvent

        :Example: Move today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[2]
        >>> event = calendar.events_today()[0]
        >>> event.move_to(calendar2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.2
        """
        self.duplicate_to(calendar)
        self.delete()

    def add_attachment(self, path: str) -> 'XACalendarEvent':
        """Adds the file at the specified path as an attachment to the event.

        :param path: The path of the file to attach to the event.
        :type path: str
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[1]
        >>> event = calendar.events_today()[0]
        >>> event.add_attachment("/Users/exampleuser/Image.png")

        .. versionadded:: 0.0.2
        """
        file_url = XABase.XAPath(path).xa_elem
        attachment = EventKit.EKAttachment.alloc().initWithFilepath_(file_url)
        self.xa_elem.addAttachment_(attachment)
        self.xa_estr.saveEvent_span_error_(self.xa_event_obj, EventKit.EKSpanThisEvent, None)
        return self

    def attendees(self, filter: Union[dict, None] = None) -> 'XACalendarAttendeeList':
        """Returns a list of attendees, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned attendees will have, or None
        :type filter: Union[dict, None]
        :return: The list of attendees
        :rtype: XACalendarAttendeeList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.attendees(), XACalendarAttendeeList, filter)

    def attachments(self, filter: dict = None) -> 'XACalendarAttachmentList':
        """"Returns a list of attachments, as PyXA objects, matching the given filter.

        :return: The list of attachments.
        :rtype: XACalendarAttachmentList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_event_obj.attachments(), XACalendarAttachmentList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.summary) + ">"




class XACalendarAttachmentList(XABase.XAList):
    """A wrapper around lists of event attachments that employs fast enumeration techniques.

    All properties of attachments can be called as methods on the wrapped list, returning a list containing each attachment's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarAttachment, filter)

    def type(self) -> List[str]:
        """Gets the type of each attachment in the list.

        :return: A list of attachment types
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("type"))

    def file_name(self) -> List[str]:
        """Gets the file name of each attachment in the list.

        :return: A list of attachment file names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("filename"))

    def file(self) -> List[XABase.XAPath]:
        """Gets the file path of each attachment in the list.

        :return: A list of attachment file paths
        :rtype: List[XABase.XAPath]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def url(self) -> List[XABase.XAURL]:
        """Gets the URL of each attachment in the list.

        :return: A list of attachment file URLs
        :rtype: List[XABase.XAURL]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("URL")
        return [XABase.XAURL(x) for x in ls]

    def uuid(self) -> List[str]:
        """Gets the UUID of each attachment in the list.

        :return: A list of attachment UUIDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("uuid"))

    def by_type(self, type: str) -> Union['XACalendarAttachment', None]:
        """Retrieves the first attachment whose type matches the given type, if one exists.

        :return: The desired attachment, if it is found
        :rtype: Union[XACalendarAttachment, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("type", type)

    def by_file_name(self, file_name: str) -> Union['XACalendarAttachment', None]:
        """Retrieves the first attachment whose file name matches the given file name, if one exists.

        :return: The desired attachment, if it is found
        :rtype: Union[XACalendarAttachment, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("filename", file_name)

    def by_file(self, file: XABase.XAPath) -> Union['XACalendarAttachment', None]:
        """Retrieves the first attachment whose file path matches the given path, if one exists.

        :return: The desired attachment, if it is found
        :rtype: Union[XACalendarAttachment, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("file", file.xa_elem)

    def by_url(self, url: XABase.XAURL) -> Union['XACalendarAttachment', None]:
        """Retrieves the first attachment whose URL matches the given URL, if one exists.

        :return: The desired attachment, if it is found
        :rtype: Union[XACalendarAttachment, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("URL", url.xa_elem)

    def by_url(self, uuid: str) -> Union['XACalendarAttachment', None]:
        """Retrieves the attachment whose UUID matches the given UUID, if one exists.

        :return: The desired attachment, if it is found
        :rtype: Union[XACalendarAttachment, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("uuid", uuid)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XACalendarAttachment(XABase.XAObject):
    """A class for interacting with calendar event attachments.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties: dict):
        super().__init__(properties)
        self.type: str #: The content type of the attachment, e.g. `image/png`
        self.file_name: str#: The filename of the original document
        self.file: XABase.XAPath #: The location of the attachment on the local disk
        self.url: XABase.XAURL #: The iCloud URL of the attachment
        self.uuid: str #: A unique identifier for the attachment

    @property
    def type(self) -> str:
        return self.xa_elem.contentType()

    @property
    def file_name(self) -> str:
        return self.xa_elem.filenameSuggestedByServer()

    @property
    def file(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.urlOnDisk())

    @property
    def url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.urlOnServer())

    @property
    def uuid(self) -> str:
        return self.xa_elem.uuid()

    def open(self) -> 'XACalendarAttachment':
        """Opens the attachment in its default application.

        :return: A reference to the attachment object.
        :rtype: XACalendarAttachment
        
        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> calendar = app.default_calendar
        >>> event = calendar.events_today()[0]
        >>> event.attachments()[0].open()

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.openURL_(self.file)
        return self