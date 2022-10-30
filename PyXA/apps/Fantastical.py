""".. versionadded:: 0.0.9

Control Fantastical using JXA-like syntax.
"""

from datetime import datetime
from typing import Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable, XACloseable, XADeletable, XAPrintable

class XAFantasticalApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Fantastical.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFantasticalWindow
        
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Fantastical is the active application
        self.version: str #: The version of Fantastical.app

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: frontmost):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def parse_sentence(self, sentence: str, notes: str = "", calendar: Union[str, 'XAFantasticalCalendar', None] = None, add_immediately: bool = True, add_attendees: bool = False):
        """Parses the given sentences and creates a corresponding calendar item based on the parsing result.

        :param sentence: The sentence to parse
        :type sentence: str
        :param notes: Notes to attach to the calendar item, defaults to ""
        :type notes: str, optional
        :param calendar: The calendar to add the item to, defaults to None
        :type calendar: Union[str, XAFantasticalCalendar, None], optional
        :param add_immediately: Whether to add the item without displaying an event editing dialog, defaults to True
        :type add_immediately: bool, optional
        :param add_attendees: Whether to invite attendees parsed from the sentence, defaults to False
        :type add_attendees: bool, optional

        :Example 1: Add simple events to calendars

        >>> # Create an event on the default calendar
        >>> import PyXA
        >>> app = PyXA.Application("Fantastical")
        >>> app.parse_sentence("Event 1")
        >>> 
        >>> # Create an event on a calendar specified by a calendar object
        >>> cal = app.calendars().by_title("PyXA Development")
        >>> app.parse_sentence("Event 2", calendar = cal)
        >>> 
        >>> # Create an event on a calendar specified by a string
        >>> app.parse_sentence("Event 3", calendar = "Testing")
        
        :Example 2: Use Fantastical's query parsing to adjust calendar item settings

        >>> # Automatically set the time of a task to 8am, show event editing dialog
        >>> app.parse_sentence("Wake up at 8am", add_immediately = False)
        >>> 
        >>> # Create a todo
        >>> app.parse_sentence("todo today Learn PyXA")
        >>> 
        >>> # Create an event at a location, with an alert, repeating weekly
        >>> app.parse_sentence("Meet with Example Person at 10am at 1 Infinite Loop, Cupertino, CA with alert 30 minutes before repeat weekly")
        >>> 
        >>> # Create an event spanning a week
        >>> app.parse_sentence("PyXA stuff August 22 to August 29")

        .. versionadded:: 0.0.9
        """
        if isinstance(calendar, XAFantasticalCalendar):
            self.xa_scel.parseSentence_notes_calendar_calendarName_addImmediately_addAttendees_(sentence, notes, calendar.xa_elem, None, add_immediately, add_attendees)
        elif isinstance(calendar, str):
            self.xa_scel.parseSentence_notes_calendar_calendarName_addImmediately_addAttendees_(sentence, notes, None, calendar, add_immediately, add_attendees)
        else:
            self.xa_scel.parseSentence_notes_calendar_calendarName_addImmediately_addAttendees_(sentence, notes, None, None, add_immediately, add_attendees)

    def show_mini_view(self, date: Union[str, datetime, None] = None):
        """Shows the mini calendar view, optionally showing a specific date.

        :param date: The date to display, defaults to None
        :type date: Union[str, datetime, None], optional

        .. versionadded:: 0.0.9
        """
        if date is None:
            date = ""
        if isinstance(date, datetime):
            date = date.strftime("%Y-%m-%d")

        print(date)
        XABase.XAURL(f"x-fantastical3://show/mini/{date}").open()

    def show_calendar_view(self, date: Union[str, datetime, None] = None):
        """Shows the (large) calendar view, optionally showing a specific date.

        :param date: The date to display, defaults to None
        :type date: Union[str, datetime, None], optional

        .. versionadded:: 0.0.9
        """
        if date is None:
            date = ""
        if isinstance(date, datetime):
            date = date.strftime("%Y-%m-%d")

        print(date)
        XABase.XAURL(f"x-fantastical3://show/calendar/{date}").open()

    def documents(self, filter: dict = None) -> 'XAFantasticalDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.documents(), XAFantasticalDocumentList, filter)

    def calendars(self, filter: dict = None) -> 'XAFantasticalCalendarList':
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.calendars(), XAFantasticalCalendarList, filter)

    def selected_calendar_items(self, filter: dict = None) -> 'XAFantasticalSelectedCalendarItemList':
        """Returns a list of selected calendar items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.selectedCalendarItems(), XAFantasticalSelectedCalendarItemList, filter)
    

    

class XAFantasticalDocumentList(XABase.XAList):
    """A wrapper around lists of Fantastical documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFantasticalDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[XABase.XAPath]:
        """Gets the path of each document in the list.

        :return: A list of document paths
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def by_name(self, name: str) -> 'XAFantasticalDocument':
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAFantasticalDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAFantasticalDocument':
        """Retrieves the tab whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAFantasticalDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAPath) -> 'XAFantasticalDocument':
        """Retrieves the document whose file matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAFantasticalDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFantasticalDocument(XABase.XAObject, XACloseable, XADeletable, XAPrintable, XAClipboardCodable):
    """A document in Fantastical.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The document's name
        self.modified: bool #: Whether the document has been modified since it was last saved
        self.file: XABase.XAPath #: The document's path

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.file())

    @file.setter
    def file(self, file: Union[str, XABase.XAPath]):
        if isinstance(file, str):
            file = XABase.XAPath(file)
        self.set_property("file", file.xa_elem)

    def print(self, print_properties: Union[dict, None] = None, show_dialog: bool = True) -> 'XAPrintable':
        """Prints the object.

        Child classes of XAPrintable should override this method as necessary.

        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :return: A reference to the PyXA object that called this method.
        :rtype: XACanPrintPath

        .. versionadded:: 0.0.9
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.print_printDialog_withProperties_(self.xa_elem, show_dialog, print_properties)
        return self

    def get_clipboard_representation(self) -> list[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a Fantastical document, the document's URL and source code are added to the clipboard.

        :return: The document's path and text content
        :rtype: list[Union[AppKit.NSURL, str]]

        .. versionadded:: 0.0.9
        """
        return [self.path.xa_elem, str(self.text)]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
    



class XAFantasticalWindow(XABaseScriptable.XASBWindow, XAPrintable, XACloseable):
    """A class for...
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The full title of the window.
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XAFantasticalDocument #: The document currently displayed in the window

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return (origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: tuple[int, int, int, int]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property("miniaturized", miniaturized)

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def document(self) -> XAFantasticalDocument:
        return self._new_element(self.xa_elem.document(), XAFantasticalDocument)

    @document.setter
    def document(self, document: XAFantasticalDocument):
        self.set_property("document", document.xa_elem)


    

class XAFantasticalCalendarList(XABase.XAList):
    """A wrapper around lists of Fantastical calendars that employs fast enumeration techniques.

    All properties of calendars can be called as methods on the wrapped list, returning a list containing each calendar's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFantasticalCalendar, filter)

    def title(self) -> list[str]:
        """Gets the title of each calendar in the list.

        :return: A list of calendar titles
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def id(self) -> list[str]:
        """Gets the ID of each calendar in the list.

        :return: A list of calendar IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def by_title(self, title: str) -> 'XAFantasticalCalendar':
        """Retrieves the calendar whose title matches the given title, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XAFantasticalCalendar, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("title", title)

    def by_id(self, id: str) -> 'XAFantasticalCalendar':
        """Retrieves the calendar whose ID matches the given ID, if one exists.

        :return: The desired calendar, if it is found
        :rtype: Union[XAFantasticalCalendar, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("id", id)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAFantasticalCalendar(XABase.XAObject):
    """A class in Fantastical.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.title: str #: The calendar's title
        self.id: str #: The unique identifier for the calendar

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property("title", title)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"




class XAFantasticalCalendarItemList(XABase.XAList):
    """A wrapper around lists of Fantastical calendar items that employs fast enumeration techniques.

    All properties of calendar items can be called as methods on the wrapped list, returning a list containing each calendar item's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAFantasticalCalendarItem
        super().__init__(properties, obj_class, filter)

    def id(self) -> list[str]:
        """Gets the ID of each calendar item in the list.

        :return: A list of calendar item IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> list[str]:
        """Gets the title of each calendar item in the list.

        :return: A list of calendar item titles
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def start_date(self) -> list[datetime]:
        """Gets the start date of each calendar item in the list.

        :return: A list of calendar item IDs
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("startDate"))

    def end_date(self) -> list[datetime]:
        """Gets the end date of each calendar item in the list.

        :return: A list of calendar item IDs
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("endDate"))

    def notes(self) -> list[str]:
        """Gets the notes of each calendar item in the list.

        :return: A list of calendar item notes
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("notes"))

    def url(self) -> list[XABase.XAURL]:
        """Gets the URL of each calendar item in the list.

        :return: A list of calendar item URLs
        :rtype: list[XABase.XAURL]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("URL")
        return [XABase.XAURL(x) for x in ls]

    def show_url(self) -> list[XABase.XAURL]:
        """Gets the show URL of each calendar item in the list.

        :return: A list of calendar item show URLs
        :rtype: list[XABase.XAURL]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("showURL"))

    def is_recurring(self) -> list[bool]:
        """Gets the recurring status of each calendar item in the list.

        :return: A list of calendar item recurring statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("isRecurring"))

    def is_all_day(self) -> list[bool]:
        """Gets the all day status of each calendar item in the list.

        :return: A list of calendar item all day statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("isAllDay"))

    def by_id(self, id: str) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose ID matches the given ID, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose title matches the given title, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("title", title)

    def by_start_date(self, start_date: datetime) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose start date matches the given date, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("startDate", start_date)

    def by_end_date(self, end_date: datetime) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose end date matches the given date, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("endDate", end_date)

    def by_notes(self, notes: str) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose notes match the given notes, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("notes", notes)

    def by_url(self, url: XABase.XAURL) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose URL matches the given URL, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("URL", url.xa_elem)

    def by_show_url(self, show_url: XABase.XAURL) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose show URL matches the given URL, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("showURL", show_url.xa_elem)

    def by_is_recurring(self, is_recurring: bool) -> 'XAFantasticalCalendarItem':
        """Retrieves the first calendar item whose recurring status matches the given boolean value, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("isRecurring", is_recurring)

    def by_is_all_day(self, is_all_day: bool) -> 'XAFantasticalCalendarItem':
        """Retrieves the calendar item whose all day status matches the given boolean value, if one exists.

        :return: The desired calendar item, if it is found
        :rtype: Union[XAFantasticalCalendarItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("isAllDay", is_all_day)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAFantasticalCalendarItem(XABase.XAObject):
    """An insertion point between two objects in Fantastical.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.id: str #: The unique identifier for the item
        self.title: str #: The event title
        self.start_date: datetime #: The start date of the event
        self.end_date: datetime #: The end date of the event
        self.notes: str #: The notes for the event
        self.url: XABase.XAURL #: The related URL for the event
        self.show_url: XABase.XAURL #: The show URL for the event
        self.is_recurring: bool #: True if the item is a recurring item
        self.is_all_day: bool #: True if the item spans an entire day

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def start_date(self) -> datetime:
        return self.xa_elem.startDate()

    @property
    def end_date(self) -> datetime:
        return self.xa_elem.endDate()

    @property
    def notes(self) -> str:
        return self.xa_elem.notes() or ""

    @property
    def url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def show_url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.showURL())

    @property
    def is_recurring(self) -> bool:
        return self.xa_elem.isRecurring()

    @property
    def is_all_day(self) -> bool:
        return self.xa_elem.isAllDay()

    def save(self):
        self.xa_elem.saveIn_as_(None, 0)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"




class XAFantasticalSelectedCalendarItemList(XAFantasticalCalendarItemList):
    """A wrapper around lists of Fantastical selected calendar items that employs fast enumeration techniques.

    All properties of selected calendar items can be called as methods on the wrapped list, returning a list containing each items's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFantasticalSelectedCalendarItem)

class XAFantasticalSelectedCalendarItem(XAFantasticalCalendarItem):
    def __init__(self, properties):
        super().__init__(properties)




class XAFantasticalCalendarEvent(XAFantasticalCalendarItem):
    def __init__(self, properties):
        super().__init__(properties)

        self.location: str #: The event location

    @property
    def location(self) -> str:
        return self.xa_elem.location()

    @location.setter
    def location(self, location: str):
        self.set_property("location", location)




class XAFantasticalTaskItem(XAFantasticalCalendarItem):
    def __init__(self, properties):
        super().__init__(properties)

        self.priority: int #: The event priority; higher number means lower priority

    @property
    def priority(self) -> int:
        return self.xa_elem.priority()

    @priority.setter
    def priority(self, priority: int):
        self.set_property("priority", priority)