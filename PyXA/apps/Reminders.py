""".. versionadded:: 0.0.1

Control the macOS Reminders application using JXA-like syntax.
"""

from datetime import datetime
from typing import List, Literal, Union, Tuple

import EventKit
from AppKit import NSURL, NSArray

from PyXA import XABase
from PyXA import XABaseScriptable
    

class XARemindersApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    """A class for managing and interacting with scripting elements of the Reminders application.

    .. seealso:: :class:`XARemindersAccount`, :class:`XARemindersList`, :class:`XARemindersReminder`

    .. versionchanged:: 0.0.6
       Added XARemindersAccount class

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XARemindersWindow
        self.pasteboard_types = {
            "com.apple.reminders.reminderCopyPaste": self._get_clipboard_reminder,
        }
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

        self.defaultAccount: XARemindersAccount #: The default account in the Reminders application
        self.defaultList: XARemindersList #: The default list in the Reminders application

    @property
    def defaultAccount(self) -> 'XARemindersAccount':
        return self._new_element(self.xa_elem.defaultAccount(), XARemindersAccount)

    @property
    def defaultList(self) -> 'XARemindersList':
        return self._new_element(self.xa_elem.defaultList(), XARemindersList)

    def _get_clipboard_reminder(self, reminder_name: str) -> 'XARemindersReminder':
        return self.reminders({"name": reminder_name})[0]

    def documents(self, filter: Union[dict, None] = None) -> 'XARemindersDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XARemindersDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XARemindersDocumentList, filter)

    def accounts(self, filter: Union[dict, None] = None) -> 'XARemindersAccountList':
        """Returns a list of accounts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned accounts will have, or None
        :type filter: Union[dict, None]
        :return: The list of accounts
        :rtype: XARemindersAccountList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.accounts(), XARemindersAccountList, filter)

    def lists(self, filter: Union[dict, None] = None) -> 'XARemindersListList':
        """Returns a list of reminder lists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lists will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminder lists
        :rtype: XARemindersListList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.lists(), XARemindersListList, filter)

    def reminders(self, filter: Union[dict, None] = None) -> 'XARemindersReminderList':
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.reminders(), XARemindersReminderList, filter)

    def new_list(self, name: str = "New List", color: str = "#FF0000", emblem: str = "symbol0") -> 'XARemindersList':
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

        .. versionadded:: 0.0.1
        """
        new_list = self.make("list", {"name": name, "color": color, "emblem": emblem})
        self.lists().push(new_list)
        return self.lists()[-1]

    def new_reminder(self, name: str = "New Reminder", due_date: datetime = None, reminder_list: 'XARemindersList' = None) -> 'XARemindersReminder':
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
        new_reminder = self.make("reminder", {"name": name, "dateDate": due_date})
        if reminder_list is None:
            self.reminders().push(new_reminder)
            return self.reminders()[-1]
        reminder_list.push(new_reminder)
        return reminder_list.reminders()[-1]

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.6
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XARemindersDocument)
        elif specifier == "list":
            return self._new_element(obj, XARemindersList)
        elif specifier == "reminder":
            return self._new_element(obj, XARemindersReminder)


class XARemindersWindow(XABase.XAObject):
    """A window of the Reminders application.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The title of the window.
        self.id: int #: The unique identifier of the window.
        self.index: int #: The index of the window, ordered front to back.
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window.
        self.closeable: bool #: Does the window have a close button?
        self.miniaturizable: bool #: Does the window have a minimize button?
        self.miniaturized: bool #: Is the window minimized right now?
        self.resizable: bool #: Can the window be resized?
        self.visible: bool #: Is the window visible right now?
        self.zoomable: bool #: Does the window have a zoom button?
        self.zoomed: bool #: Is the window zoomed right now?
        self.document: XARemindersDocument #: The document whose contents are displayed in the window.

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
    def document(self) -> 'XARemindersDocument':
        return self._new_element(self.xa_elem.document(), XARemindersDocument)

    def close(self, save: bool = True) -> None:
        """Closes the window.

        :param save: Whether to save the current document before closing, defaults to True
        :type save: bool, optional
        :return: The window object
        :rtype: XARemindersDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.closeSaving_savingIn_(save, None)
    
    def save(self) -> 'XARemindersWindow':
        """Saves the current document of the window.

        :return: The window object
        :rtype: XARemindersWindow

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.saveIn_as_(None, None)
    
    def print(self, properties: dict, show_dialog: bool = True) -> 'XARemindersWindow':
        """Prints the window.

        :param properties: The settings to pre-populate the print dialog with
        :type properties: dict
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: The window object
        :rtype: XARemindersWindow

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.printWithProperties_printDialog_(properties, show_dialog)

    def lists(self, filter: Union[dict, None] = None) -> 'XARemindersListList':
        """Returns a list of reminder lists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lists will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminder lists
        :rtype: XARemindersListList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.lists(), XARemindersListList, filter)

    def reminders(self, filter: Union[dict, None] = None) -> 'XARemindersReminderList':
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.reminders(), XARemindersReminderList, filter)




class XARemindersDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersDocument, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[dict]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[dict]:
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

    def by_properties(self, properties: dict) -> Union['XARemindersDocument', None]:
        """Retrieves the document whose properties matches the given properties dictionary, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XARemindersDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union['XARemindersDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XARemindersDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XARemindersDocument', None]:
        """Retrieves the document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XARemindersDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAPath) -> Union['XARemindersDocument', None]:
        """Retrieves the document whose file matches the given file path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XARemindersDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XARemindersDocument(XABase.XAObject):
    """A document in the Reminders application.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
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

    def close(self, save: bool = True, location: Union[str, NSURL] = None) -> None:
        """Closes a document.
        """
        file_path = XABase.XAPath(location).xa_elem
        return self.xa_elem.closeSaving_savingIn_(save, file_path)
    
    def save(self) -> None:
        """Saves a document.
        """
        return self.xa_elem.saveIn_as_(...)
    
    def print(self, properties: dict, show_dialog: bool = True) -> None:
        """Prints a document.
        """
        return self.xa_elem.printWithProperties_printDialog_(properties, show_dialog)
    
    def delete(self) -> None:
        """Deletes the document.
        """
        return self.xa_elem.delete()
    
    def duplicate(self) -> None:
        """Copies an object.
        """
        return self.xa_elem.duplicateTo_withProperties_(...)
    
    def move_to(self, window: XARemindersWindow) -> None:
        """Move an object to a new location.
        """
        return self.xa_elem.moveTo_(window.xa_elem)




class XARemindersAccountList(XABase.XAList):
    """A wrapper around lists of accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersAccount, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each account in the list.

        :return: A list of account properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def id(self) -> List[str]:
        """Gets the ID of each account in the list.

        :return: A list of account IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        """Gets the name of each account in the list.

        :return: A list of account names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_properties(self, properties: dict) -> Union['XARemindersAccount', None]:
        """Retrieves the account whose properties matches the given properties dictionary, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XARemindersAccount, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_id(self, id: str) -> Union['XARemindersAccount', None]:
        """Retrieves the account whose ID matches the given ID, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XARemindersAccount, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XARemindersAccount', None]:
        """Retrieves the account whose name matches the given name, if one exists.

        :return: The desired account, if it is found
        :rtype: Union[XARemindersAccount, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XARemindersAccount(XABase.XAObject):
    """An account in the Reminders application.
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the account
        self.id: str #: The unique identifier of the account
        self.name: str #: The name of the account

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def show(self) -> 'XARemindersAccount':
        """Shows the account in the front window.

        :return: The account object
        :rtype: XARemindersAccount
        
        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()




class XARemindersListList(XABase.XAList):
    """A wrapper around lists of reminder lists that employs fast enumeration techniques.

    All properties of reminder lists can be called as methods on the wrapped list, returning a list containing each list's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersList, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each reminder list in the list.

        :return: A list of reminder list properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def id(self) -> List[str]:
        """Gets the ID of each reminder list in the list.

        :return: A list of reminder list IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[dict]:
        """Gets the name of each reminder list in the list.

        :return: A list of reminder list names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def container(self) -> XARemindersAccountList:
        """Gets the parent container of each reminder list in the list.

        :return: A list of accounts
        :rtype: XARemindersAccountList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XARemindersAccountList)

    def color(self) -> List[dict]:
        """Gets the color of each reminder list in the list.

        :return: A list of reminder list colors
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("color"))

    def emblem(self) -> List[dict]:
        """Gets the emblem name of each reminder list in the list.

        :return: A list of reminder list emblems
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("emblem"))

    def reminders(self) -> 'XARemindersReminderList':
        """Gets the reminders of each reminder list in the list.

        :return: A list of reminders
        :rtype: XARemindersReminderList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("reminders")
        return self._new_element(ls, XARemindersReminderList)

    def by_properties(self, properties: dict) -> Union['XARemindersListList', None]:
        """Retrieves the list whose properties matches the given properties dictionary, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_id(self, id: str) -> Union['XARemindersListList', None]:
        """Retrieves the list whose ID matches the given ID, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XARemindersListList', None]:
        """Retrieves the list whose name matches the given name, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_container(self, container: 'XARemindersList') -> Union['XARemindersListList', None]:
        """Retrieves the list whose parent container matches the given account, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("container", container.xa_elem)

    def by_color(self, color: str) -> Union['XARemindersListList', None]:
        """Retrieves the list whose color matches the given color, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("color", color)

    def by_emblem(self, emblem: str) -> Union['XARemindersListList', None]:
        """Retrieves the list whose emblem matches the given emblem, if one exists.

        :return: The desired list, if it is found
        :rtype: Union[XARemindersListList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("emblem", emblem)

    def delete(self):
        """Deletes all reminder lists in the list.

        .. versionadded:: 0.0.6
        """
        [x.delete() for x in self.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XARemindersList(XABase.XAObject):
    """A class for...
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        # Scripting Properties
        self.properties: dict #: All properties of the list
        self.id: str #: The unique identifier of the list
        self.name: str #: The name of the list
        self.container: Union[XARemindersAccount, XARemindersList] #: The container of the list
        self.color: str #: The color of the list
        self.emblem: str #: The emblem icon name of the list

        # EventKit Properties
        xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)
        lists = XABase.XAPredicate().from_args("calendarIdentifier", self.xa_elem.id()).evaluate(xa_estr.allCalendars())
        if len(lists) > 0:
            elem = lists[0]

            self.summary = elem.summary() #: An overview of the list's information
            self.subscription_url = elem.subscriptionURL() #: The URL of the list used to subscribe to it
            self.sharing_status: bool = elem.sharingStatus() #: Whether the list is shared
            self.sharees = elem.sharees() #: A list of individuals with whom the list is shared with

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def container(self) -> Union[XARemindersAccount, 'XARemindersList']:
        return self._new_element(self.xa_elem.container(), XARemindersAccount)

    @property
    def color(self) -> str:
        return self.xa_elem.color()

    @property
    def emblem(self) -> str:
        return self.xa_elem.emblem()

    def delete(self) -> None:
        """Deletes the list.

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.delete()

    def show(self) -> 'XARemindersList':
        """Shows the list in the front Reminders window.

        :return: The list object
        :rtype: XARemindersList

        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()
        return self

    def reminders(self, filter: Union[dict, None] = None) -> 'XARemindersReminderList':
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.reminders(), XARemindersReminderList, filter)





class XARemindersReminderList(XABase.XAList):
    """A wrapper around lists of reminders that employs fast enumeration techniques.

    All properties of reminders can be called as methods on the wrapped list, returning a list containing each reminder's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersReminder, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each reminder in the list.

        :return: A list of reminder properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        """Gets the name of each reminder in the list.

        :return: A list of reminder names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[str]:
        """Gets the ID of each reminder in the list.

        :return: A list of reminder IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def container(self) -> XARemindersListList:
        """Gets the parent list of each reminder in the list.

        :return: A list of reminder lists
        :rtype: XARemindersListList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("creationDate")
        return self._new_element(ls, XARemindersListList)

    def creation_date(self) -> List[datetime]:
        """Gets the creation date of each reminder in the list.

        :return: A list of creation dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        """Gets the last modification date of each reminder in the list.

        :return: A list of modification dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def body(self) -> List[str]:
        """Gets the body text of each reminder in the list.

        :return: A list of reminder body texts
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("body"))

    def completed(self) -> List[bool]:
        """Gets the completed status of each reminder in the list.

        :return: A list of reminder completed status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("completed"))

    def completion_date(self) -> List[datetime]:
        """Gets the completion date of each reminder in the list.

        :return: A list of completion dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("completionDate"))

    def due_date(self) -> List[datetime]:
        """Gets the due date of each reminder in the list.

        :return: A list of due dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dueDate"))

    def allday_due_date(self) -> List[datetime]:
        """Gets the allday due date of each reminder in the list.

        :return: A list of allday due dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("alldayDueDate"))

    def remind_me_date(self) -> List[datetime]:
        """Gets the remind me date of each reminder in the list.

        :return: A list of remind me dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("remindMeDate"))

    def priority(self) -> List[int]:
        """Gets the priority of each reminder in the list.

        :return: A list of reminder priorities
        :rtype: List[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("priority"))

    def flagged(self) -> List[bool]:
        """Gets the flagged status of each reminder in the list.

        :return: A list of reminder flagged status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("flagged"))

    def alarms(self) -> List['XARemindersAlarmList']:
        """Gets the alarms of each reminder in the list.

        :return: A list of lists of alarms
        :rtype: List[XARemindersAlarmList]
        
        .. versionadded:: 0.0.6
        """
        return [x.alarms() for x in self]

    def by_properties(self, properties: dict) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose properties matches the given properties dictionary, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose name matches the given name, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose ID matches the given ID, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_container(self, container: 'XARemindersList') -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose parent container matches the given list, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("container", container.xa_elem)

    def by_creation_date(self, creation_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose creation date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("creationDate", creation_date)

    def by_modification_date(self, modification_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose modification date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("modificationDate", modification_date)

    def by_body(self, body: str) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose body content matches the given string, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("body", body)

    def by_completed(self, completed: bool) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose completed status matches the given boolean value, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("completed", completed)

    def by_completion_date(self, completed_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose completion date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("completedDate", completed_date)

    def by_due_date(self, due_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose due date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("dueDate", due_date)

    def by_allday_due_date(self, allday_due_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose allday due date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("alldayDueDate", allday_due_date)

    def by_remind_me_date(self, remind_me_date: datetime) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose remind me date matches the given date, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("remindMeDate", remind_me_date)

    def by_priority(self, priority: int) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose priority matches the given priority, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("priority", priority)

    def by_flagged(self, flagged: bool) -> Union['XARemindersReminderList', None]:
        """Retrieves the reminder whose flagged status matches the given boolean value, if one exists.

        :return: The desired reminder, if it is found
        :rtype: Union[XARemindersReminderList, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("flagged", flagged)

    def delete(self):
        """Deletes all reminders in the list.

        .. versionadded:: 0.0.6
        """
        [x.delete() for x in self.xa_elem]

    def move_to(self, list: XARemindersList):
        """Moves all reminders in the list to the specified reminder list.

        :param list: The list to move reminders into
        :type list: XARemindersList

        .. versionadded:: 0.0.6
        """
        [x.moveTo_(list.xa_elem) for x in self.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XARemindersReminder(XABase.XAObject):
    """A class for...
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        # Scripting Properties
        self.properties: dict #: All properties of the reminder.
        self.name: str #: The name of the reminder
        self.id: str #: The unique identifier of the reminder
        self.container: Union[XARemindersList, XARemindersReminder] #: The container of the reminder
        self.creation_date: datetime #: The creation date of the reminder
        self.modification_date: datetime #: The modification date of the reminder
        self.body: str #: The notes attached to the reminder
        self.completed: bool #: Whether the reminder is completed
        self.completion_date: datetime #: The completion date of the reminder
        self.due_date: datetime #: The due date of the reminder; will set both date and time
        self.allday_due_date: datetime #: The all-day due date of the reminder; will only set a date
        self.remind_me_date: datetime #: The remind date of the reminder
        self.priority: int #: The priority of the reminder; 0: no priority, 1–4: high, 5: medium, 6–9: low
        self.flagged: bool #: Whether the reminder is flagged

        # EventKit Properties
        self.recurrence_rule #: The recurrence rule for the reminder
        self.all_day: bool #: Whether the reminder is all day or a specific time
        self.notes: str #: User-inputted notes for this reminder
        self.url #: The URL attached to the reminder, if there is one

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
    def container(self) -> Union[XARemindersList, 'XARemindersReminder']:
        return self._new_element(self.xa_elem.container(), XARemindersList)

    @property
    def creationDate(self) -> datetime:
        return self.xa_elem.creationDate()

    @property
    def modificationDate(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def body(self) -> str:
        return self.xa_elem.body()

    @property
    def completed(self) -> bool:
        return self.xa_elem.completed()

    @property
    def completionDate(self) -> datetime:
        return self.xa_elem.completionDate()

    @property
    def dueDate(self) -> datetime:
        return self.xa_elem.dueDate()

    @property
    def alldayDueDate(self) -> datetime:
        return self.xa_elem.alldayDueDate()

    @property
    def remindMeDate(self) -> datetime:
        return self.xa_elem.remindMeDate()

    @property
    def priority(self) -> int:
        return self.xa_elem.priority()

    @property
    def flagged(self) -> bool:
        return self.xa_elem.flagged()

    @property
    def all_day(self) -> bool:
        reminder = self.__get_ek_reminder()
        return reminder.allDay() == 1

    @property
    def notes(self) -> str:
        reminder = self.__get_ek_reminder()
        return reminder.notes()

    @property
    def url(self) -> XABase.XAURL:
        reminder = self.__get_ek_reminder()
        return XABase.XAURL(reminder.URL())

    @property
    def recurrence_rule(self) -> 'XARemindersRecurrenceRule':
        reminder = self.__get_ek_reminder()
        if reminder.recurrenceRule() is not None:
            return self._new_element(reminder.recurrenceRule(), XARemindersRecurrenceRule)

    def __get_ek_reminder(self) -> EventKit.EKReminder:
        xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)
        predicate = xa_estr.predicateForRemindersInCalendars_(None)
        reminders = xa_estr.remindersMatchingPredicate_(predicate)
        reminder_id = self.xa_elem.id()
        if reminder_id is not None:
            reminders = XABase.XAPredicate().from_args("calendarItemIdentifier", reminder_id[19:]).evaluate(reminders)
            if len(reminders) > 0:
                return reminders[0]
    
    def delete(self) -> None:
        """Deletes the reminder.

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.delete()
    
    def move_to(self, list: XARemindersList) -> 'XARemindersReminder':
        """Moves the reminder to the specified list.

        :param list: The list to move the reminder to
        :type list: XARemindersList
        :return: The moved reminder object
        :rtype: XARemindersReminder

        .. versionadded:: 0.0.6
        """
        self.xa_elem.moveTo_(list.xa_elem)
        return list.reminders()[-1]

    def show(self) -> 'XARemindersReminder':
        """Shows the reminder in the front Reminders window.

        :return: The reminder object
        :rtype: XARemindersReminder

        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()
        return self

    def alarms(self, filter: Union[dict, None] = None) -> 'XARemindersAlarmList':
        """Returns a list of alarms, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned alarms will have, or None
        :type filter: Union[dict, None]
        :return: The list of alarms
        :rtype: XARemindersAlarmList

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        return self._new_element(reminder.alarms() or NSArray.alloc().initWithArray_([]), XARemindersAlarmList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"




class XARemindersRecurrenceRule(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersReminder`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

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




class XARemindersAlarmList(XABase.XAList):
    """A wrapper around lists of reminder alarms that employs fast enumeration techniques.

    All properties of alarms can be called as methods on the wrapped list, returning a list containing each alarm's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersAlarm, filter)

    def id(self) -> List[str]:
        """Gets the ID of each alarm in the list.

        :return: A list of alarm IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sharedUID"))

    def snoozed(self) -> List[bool]:
        """Gets the snoozed status of each alarm in the list.

        :return: A list of alarm snoozed status boolean values
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("isSnoozed"))

    def date(self) -> List[datetime]:
        """Gets the date of each alarm in the list.

        :return: A list of alarm dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("absoluteDate"))

    def proximity_direction(self) -> List[str]:
        """Gets the proximity direction of each alarm in the list.

        :return: A list of directions
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("proximityString"))

    def location(self) -> List[XABase.XALocation]:
        """Gets the location of each alarm in the list.

        :return: A list of alarm locations
        :rtype: List[XABase.XALocation]
        
        .. versionadded:: 0.0.6
        """
        return [x.location for x in self]

    def by_id(self, id: str) -> Union['XARemindersAlarm', None]:
        """Retrieves the alarm whose ID matches the given ID, if one exists.

        :return: The desired alarm, if it is found
        :rtype: Union[XARemindersAlarm, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("sharedUID", id)

    def by_snoozed(self, snoozed: bool) -> Union['XARemindersAlarm', None]:
        """Retrieves the alarm whose snoozed status matches the given boolean value, if one exists.

        :return: The desired alarm, if it is found
        :rtype: Union[XARemindersAlarm, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("isSnoozed", snoozed)

    def by_date(self, date: datetime) -> Union['XARemindersAlarm', None]:
        """Retrieves the alarm whose date matches the given date, if one exists.

        :return: The desired alarm, if it is found
        :rtype: Union[XARemindersAlarm, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("absoluteDate", date)

    def by_proximity_direction(self, proximity_direction: str) -> Union['XARemindersAlarm', None]:
        """Retrieves the alarm whose proximity direction matches the given direction, if one exists.

        :return: The desired alarm, if it is found
        :rtype: Union[XARemindersAlarm, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("proximityString", proximity_direction)

    def by_location(self, location: XABase.XALocation) -> Union['XARemindersAlarm', None]:
        """Retrieves the alarm whose location matches the given location, if one exists.

        :return: The desired alarm, if it is found
        :rtype: Union[XARemindersAlarm, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("structuredLocation", location.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XARemindersAlarm(XABase.XAObject):
    """An alarm attached to a reminder.

    .. seealso:: :class:`XARemindersReminder`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)

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