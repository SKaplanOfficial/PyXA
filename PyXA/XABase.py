""".. versionadded:: 0.0.1

General classes and methods applicable to any PyXA object.
"""

from datetime import datetime
from enum import Enum
from pprint import pprint
import tempfile
import time, os, sys
from typing import Any, Callable, Literal, Tuple, Union, List, Dict
import threading
from bs4 import BeautifulSoup, element
import requests

from PyObjCTools import AppHelper

import AppKit
import Quartz
import WebKit
import CoreServices
from Quartz import CGImageSourceRef, CGImageSourceCreateWithData, CFDataRef
from CoreLocation import CLLocation
from ScriptingBridge import SBApplication, SBElementArray
import ScriptingBridge

import threading, signal

from PyXA.XAErrors import InvalidPredicateError
from .XAProtocols import XAClipboardCodable

def OSType(s: str):
    return int.from_bytes(s.encode("UTF-8"), "big")

def unOSType(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()




class XAObject():
    """A general class for PyXA scripting objects.

    .. seealso:: :class:`XABaseScriptable.XASBObject`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict = None):
        """Instantiates a PyXA scripting object.

        :param properties: A dictionary of properties to assign to this object.
        :type properties: dict, optional

        .. versionchanged:: 0.0.3
           Removed on-the-fly creation of class attributes. All objects should concretely define their properties.

        .. versionadded:: 0.0.1
        """
        if properties is not None:
            self.xa_prnt = properties.get("parent", None)
            self.xa_apsp = properties.get("appspace", None)
            self.xa_wksp = properties.get("workspace", None)
            self.xa_elem = properties.get("element", None)
            self.xa_scel = properties.get("scriptable_element", None)
            self.xa_aref = properties.get("appref", None)
            self.xa_sevt = properties.get("system_events", SBApplication.alloc().initWithBundleIdentifier_("com.apple.systemevents"))

        self.properties: dict #: The scriptable properties dictionary for the object

    def _exec_suppresed(self, f: Callable[..., Any], *args: Any) -> Any:
        """Silences unwanted and otherwise unavoidable warning messages.

        Taken from: https://stackoverflow.com/a/3946828
        
        :param f: The function to execute
        :type f: Callable[...]
        :param args: The parameters to pass to the specified function
        :type args: Any
        :raises error: Any exception that occurs while trying to run the specified function
        :return: The value returned by the specified function upon execution
        :rtype: Any

        .. versionadded:: 0.0.2
        """
        error = None
        value = None

        old_stderr = os.dup(sys.stderr.fileno())
        fd = os.open('/dev/null', os.O_CREAT | os.O_WRONLY)
        os.dup2(fd, sys.stderr.fileno())
        try:
            value = f(*args)
        except Exception as e:
            error = e
        os.dup2(old_stderr, sys.stderr.fileno())

        if error is not None:
            raise error
        return value

    def _new_element(self, obj: AppKit.NSObject, obj_class: type = 'XAObject', *args: List[Any]) -> 'XAObject':
        """Wrapper for creating a new PyXA object.

        :param folder_obj: The Objective-C representation of an object.
        :type folder_obj: NSObject
        :return: The PyXA representation of the object.
        :rtype: XAObject
        
        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_class(properties, *args)

    def has_element(self) -> bool:
        """Whether this object has an AppleScript/JXA/Objective-C scripting element associated with it.

        :return: True if this object's element attribute is set, False otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.xa_elem is not None

    def has_element_properties(self) -> bool:
        """Whether the scripting element associated with this object has properties attached to it.

        :return: True if this object's properties attribute is set, False otherwise.
        :rtype: bool

        .. deprecated:: 0.0.8
           All elements now have a properties dictionary, even if it is empty.

        .. versionadded:: 0.0.1
        """
        return self.element_properties != None

    def set_element(self, element: 'XAObject') -> 'XAObject':
        """Sets the element attribute to the supplied element and updates the properties attribute accordingly.

        :param element: The new scripting element to reference via the element attribute.
        :type element: XAObject
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem = element
        return self

    def set_properties(self, properties: dict) -> 'XAObject':
        """Updates the value of multiple properties of the scripting element associated with this object.

        :param properties: A dictionary defining zero or more property names and updated values as key-value pairs.
        :type properties: dict
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        property_dict = {}
        for key in properties:
            parts = key.split("_")
            titled_parts = [part.title() for part in parts[1:]]
            property_name = parts[0] + "".join(titled_parts)
            property_dict[property_name] = properties[key]
        self.xa_elem.setValuesForKeysWithDictionary_(property_dict)
        return self

    def set_property(self, property_name: str, value: Any) -> 'XAObject':
        """Updates the value of a single property of the scripting element associated with this object.

        :param property: The name of the property to assign a new value to.
        :type property: str
        :param value: The value to assign to the specified property.
        :type value: Any
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        parts = property_name.split("_")
        titled_parts = [part.title() for part in parts[1:]]
        property_name = parts[0] + "".join(titled_parts)
        self.xa_elem.setValue_forKey_(value, property_name)
        return self
    



class AppleScript(XAObject):
    """A class for constructing and executing AppleScript scripts.

    .. versionadded:: 0.0.5
    """
    def __init__(self, script: Union[str, List[str], None] = None):
        if isinstance(script, str):
            if script.startswith("/"):
                with open(script, 'r') as f:
                    script = f.readlines()
            else:
                self.script = [script]
        elif isinstance(script, list):
            self.script = script
        elif script == None:
            self.script = []

    def add(self, script: Union[str, List[str], 'AppleScript']):
        """Adds the supplied string, list of strings, or script as a new line entry in the script.

        :param script: The script to append to the current script string.
        :type script: Union[str, List[str], AppleScript]

        .. versionadded:: 0.0.5
        """
        if isinstance(script, str):
            self.script.append(script)
        elif isinstance(script, list):
            self.script.extend(script)
        elif isinstance(script, AppleScript):
            self.script.extend(script.script)

    def run(self) -> Any:
        """Compiles and runs the script, returning the result.

        :return: The return value of the script.
        :rtype: Any
        
        .. versionadded:: 0.0.5
        """
        value = None
        script = ""
        for line in self.script:
            script += line + "\n"
        script = AppKit.NSAppleScript.alloc().initWithSource_(script)
        result = script.executeAndReturnError_(None)[0]

        print(result)
        
        if result is not None:
            # if result.descriptorType() == OSType('obj '):
            #     form = result.descriptorForKeyword_(OSType("form"))
            #     want = result.descriptorForKeyword_(OSType("want"))
            #     seld = result.descriptorForKeyword_(OSType("seld"))
                
            #     if want.data().decode() == "niwc":
            #         # Window
            #         print("hi")
            return result.stringValue()




class XAClipboard(XAObject):
    """A wrapper class for managing and interacting with the system pasteboard

    .. versionadded:: 0.0.5
    """
    def __init__(self):
        self.xa_elem = AppKit.NSPasteboard.generalPasteboard()
        self.content #: The content of the clipboard

    @property
    def content(self) -> Dict[str, List[Any]]:
        info_by_type = {}
        for item in self.xa_elem.pasteboardItems():
            for item_type in item.types():
                info_by_type[item_type] = {
                    "data": item.dataForType_(item_type),
                    "properties": item.propertyListForType_(item_type),
                    "strings": item.stringForType_(item_type),
                }
        return info_by_type

    @content.setter
    def content(self, value: List[Any]):
        if not isinstance(value, list):
            value = [value]
        self.xa_elem.clearContents()
        for index, item in enumerate(value):
            if item == None:
                value[index] = ""
            elif isinstance(item, XAObject):
                if not isinstance(item, XAClipboardCodable):
                    print(item, "is not a clipboard-codable object.")
                    continue
                if isinstance(item.xa_elem, ScriptingBridge.SBElementArray) and item.xa_elem.get() is None:
                    value[index] = ""
                else:
                    content = item.get_clipboard_representation()
                    if isinstance(content, list):
                        value.pop(index)
                        value += content
                    else:
                        value[index] = content
            elif isinstance(item, int) or isinstance(item, float):
                value[index] = str(item)
        self.xa_elem.writeObjects_(value)

    def clear(self):
        """Clears the system clipboard.
        
        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()

    def get_strings(self) -> List[str]:
        """Retrieves string type data from the clipboard, if any such data exists.

        :return: The list of strings currently copied to the clipboard
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        items = []
        for item in self.xa_elem.pasteboardItems():
            string = item.stringForType_(AppKit.NSPasteboardTypeString)
            if string is not None:
                items.append(string)
        return items

    def get_urls(self) -> List['XAURL']:
        """Retrieves URL type data from the clipboard, as instances of :class:`XAURL` and :class:`XAPath`, if any such data exists.

        :return: The list of file URLs and web URLs currently copied to the clipboard
        :rtype: List[XAURL]

        .. versionadded:: 0.0.8
        """
        items = []
        for item in self.xa_elem.pasteboardItems():
            url = None
            string = item.stringForType_(AppKit.NSPasteboardTypeURL)
            if string is None:
                string = item.stringForType_(AppKit.NSPasteboardTypeFileURL)
                if string is not None:
                    url = XAPath(XAURL(string).xa_elem)
            else:
                url = XAURL(string)
                
            if url is not None:
                items.append(url)
        return items

    def get_images(self) -> List['XAImage']:
        """Retrieves image type data from the clipboard, as instances of :class:`XAImage`, if any such data exists.

        :return: The list of images currently copied to the clipboard
        :rtype: List[XAImage]

        .. versionadded:: 0.0.8
        """
        image_types = [AppKit.NSPasteboardTypePNG, AppKit.NSPasteboardTypeTIFF, 'public.jpeg', 'com.apple.icns']
        items = []
        for item in self.xa_elem.pasteboardItems():
            for image_type in image_types:
                if image_type in item.types():
                    img = XAImage(data = item.dataForType_(image_type))
                    items.append(img)
        return items

    def set_contents(self, content: List[Any]):
        """Sets the content of the clipboard

        :param content: A list of the content to add fill the clipboard with.
        :type content: List[Any]

        .. deprecated:: 0.0.8
           Set the :ivar:`content` property directly instead.
        
        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()
        self.xa_elem.writeObjects_(content)




class XAList(XAObject):
    """A wrapper around NSArray and NSMutableArray objects enabling fast enumeration and lazy evaluation of Objective-C objects.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, object_class: type = None, filter: Union[dict, None] = None):
        """Creates an efficient wrapper object around a list of scriptable elements.

        :param properties: PyXA properties passed to this object for utility purposes
        :type properties: dict
        :param object_class: _description_, defaults to None
        :type object_class: type, optional
        :param filter: A dictionary of properties and values to filter items by, defaults to None
        :type filter: Union[dict, None], optional

        .. versionchanged:: 0.0.8
           The filter property is deprecated and will be removed in a future version. Use the :func:`filter` method instead.

        .. versionadded:: 0.0.3
        """
        super().__init__(properties)
        self.xa_ocls = object_class

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def by_property(self, property: str, value: Any) -> XAObject:
        """Retrieves the first element whose property value matches the given value, if one exists.

        :param property: The property to match
        :type property: str
        :param value: The value to match
        :type value: Any
        :return: The matching element, if one is found
        :rtype: XAObject

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> photo = app.media_items().by_property("id", "CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001")
        >>> print(photo)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001>

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        obj = ls[0]
        return self._new_element(obj, self.xa_ocls)

    def containing(self, property: str, value: str) -> XAObject:
        """Retrieves the element whose property value contains the given value, if one exists.

        :param property: The property match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The matching element, if one is found
        :rtype: XAObject

        .. deprecated:: 0.0.8
           Use :func:`filter` instead.

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_contains_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        obj = ls[0]
        return self._new_element(obj, self.xa_ocls)

    def filter(self, filter: str, comparison_operation: Union[str, None] = None, value1: Union[Any, None] = None, value2: Union[Any, None] = None) -> 'XAList':
        """Filters the list by the given parameters.

        The filter may be either a format string, used to create an NSPredicate, or up to 4 arguments specifying the filtered property name, the comparison operation, and up to two values to compare against.

        :param filter: A format string or a property name
        :type filter: str
        :param comparison_operation: The symbol or name of a comparison operation, such as > or <, defaults to None
        :type comparison_operation: Union[str, None], optional
        :param value1: The first value to compare each list item's property value against, defaults to None
        :type value1: Union[Any, None], optional
        :param value2: The second value to compare each list item's property value against, defaults to None
        :type value2: Union[Any, None], optional
        :return: The filter XAList object
        :rtype: XAList

        :Example 1: Get the last file sent by you (via this machine) in Messages.app

        >>> import PyXA
        >>> app = PyXA.application("Messages")
        >>> last_file_transfer = app.file_transfers().filter("direction", "==", app.MessageDirection.OUTGOING)[-1]
        >>> print(last_file_transfer)
        <<class 'PyXA.apps.Messages.XAMessagesFileTransfer'>Test.jpg>

        :Example 2: Get the list of favorite photos/videos from Photos.app

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> favorites = app.media_items().filter("favorite", "==", True)
        >>> print(favorites)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItemList'>['CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001', 'EFEB7F37-8373-4972-8E43-21612F597185/L0/001', ...]>

        .. note::
        
           For properties that appear to be boolean but fail to return expected filter results, try using the corresponding 0 or 1 value instead.

        :Example 3: Provide a custom format string

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> photo = app.media_items().filter("id == 'CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001'")[0]
        >>> print(photo)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001>

        .. versionadded:: 0.0.8
        """
        if comparison_operation is not None and value1 is not None:
            predicate = XAPredicate()
            if comparison_operation in ["=", "==", "eq", "EQ", "equals", "EQUALS"]:
                predicate.add_eq_condition(filter, value1)
            elif comparison_operation in ["!=", "!==", "neq", "NEQ", "not equal to", "NOT EQUAL TO"]:
                predicate.add_neq_condition(filter, value1)
            elif comparison_operation in [">", "gt", "GT", "greater than", "GREATER THAN"]:
                predicate.add_gt_condition(filter, value1)
            elif comparison_operation in ["<", "lt", "LT", "less than", "LESS THAN"]:
                predicate.add_lt_condition(filter, value1)
            elif comparison_operation in [">=", "geq", "GEQ", "greater than or equal to", "GREATER THAN OR EQUAL TO"]:
                predicate.add_geq_condition(filter, value1)
            elif comparison_operation in ["<=", "leq", "LEQ", "less than or equal to", "LESS THAN OR EQUAL TO"]:
                predicate.add_leq_condition(filter, value1)
            elif comparison_operation in ["begins with", "beginswith", "BEGINS WITH", "BEGINSWITH"]:
                predicate.add_begins_with_condition(filter, value1)
            elif comparison_operation in ["contains", "CONTAINS"]:
                predicate.add_contains_condition(filter, value1)
            elif comparison_operation in ["ends with", "endswith", "ENDS WITH", "ENDSWITH"]:
                predicate.add_ends_with_condition(filter, value1)
            elif comparison_operation in ["between", "BETWEEN"]:
                predicate.add_between_condition(filter, value1, value2)
            elif comparison_operation in ["matches", "MATCHES"]:
                predicate.add_match_condition(filter, value1)

            filtered_list = predicate.evaluate(self.xa_elem)
            return self._new_element(filtered_list, self.__class__)
        else:
            filtered_list = XAPredicate.evaluate_with_format(self.xa_elem, filter)
            return self._new_element(filtered_list, self.__class__)

    def at(self, index: int) -> XAObject:
        """Retrieves the element at the specified index.

        :param index: The index of the desired element
        :type index: int
        :return: The PyXA-wrapped element object
        :rtype: XAObject

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem[index], self.xa_ocls)

    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.firstObject(), self.xa_ocls)

    def last(self) -> XAObject:
        """Retrieves the last element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.lastObject(), self.xa_ocls)

    def shuffle(self) -> 'XAList':
        """Randomizes the order of objects in the list.

        :return: A reference to the shuffled XAList
        :rtype: XAList

        .. versionadded:: 0.0.3
        """
        self.xa_elem = self.xa_elem.shuffledArray()
        return self

    def push(self, element: XAObject):
        """Appends the object referenced by the provided PyXA wrapper to the end of the list.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.addObject_(element.xa_elem)

    def insert(self, element: XAObject, index: int):
        """Inserts the object referenced by the provided PyXA wrapper at the specified index.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.insertObject_atIndex_(element.xa_elem, index)

    def pop(self, index: int = -1) -> XAObject:
        """Removes the object at the specified index from the list and returns it.

        .. versionadded:: 0.0.3
        """
        removed = self.xa_elem.lastObject()
        self.xa_elem.removeLastObject()
        return self._new_element(removed, self.xa_ocls)

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            arr = AppKit.NSMutableArray.alloc().initWithArray_([self.xa_elem[index] for index in range(key.start, key.stop, key.step or 1)])
            return self._new_element(arr, self.__class__)
        return self._new_element(self.xa_elem[key], self.xa_ocls)

    def __len__(self):
        if hasattr(self.xa_elem, "count"):
            return self.xa_elem.count()
        return len(self.xa_elem)

    def __reversed__(self):
        self.xa_elem = self.xa_elem.reverseObjectEnumerator().allObjects()
        return self

    def __iter__(self):
        return (self._new_element(object, self.xa_ocls) for object in self.xa_elem.objectEnumerator())

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAProcess(XAObject):
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = properties["window_class"]
        self.id = self.xa_elem.id()
        self.unix_id = self.xa_elem.unixId()

        self.front_window: XAWindow #: The front window of the application process

    @property
    def front_window(self) -> 'XAWindow':
        return self._new_element(self.xa_elem.windows()[0], XAWindow)

    def windows(self, filter: dict = None) -> 'XAWindowList':
        return self._new_element(self.xa_elem.windows(), XAWindowList, filter)

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_elem.menuBars(), XAUIMenuBarList, filter)




class XAApplication(XAObject, XAClipboardCodable):
    """A general application class for both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XASBApplication`, :class:`XAWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAWindow

        predicate = AppKit.NSPredicate.predicateWithFormat_("displayedName == %@", self.xa_elem.localizedName())
        process = self.xa_sevt.processes().filteredArrayUsingPredicate_(predicate)[0]

        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": process,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "window_class": self.xa_wcls
        }
        self.xa_prcs = XAProcess(properties)

        self.bundle_identifier: str #: The bundle identifier for the application
        self.bundle_url: str #: The file URL of the application bundle
        self.executable_url: str #: The file URL of the application's executable
        self.frontmost: bool #: Whether the application is the active application
        self.launch_date: datetime #: The date and time that the application was launched
        self.localized_name: str #: The application's name
        self.owns_menu_bar: bool #: Whether the application owns the top menu bar
        self.process_identifier: str #: The process identifier for the application instance

    @property
    def bundle_identifier(self) -> str:
        return self.xa_elem.bundleIdentifier()

    @property
    def bundle_url(self) -> str:
        return self.xa_elem.bundleURL()

    @property
    def executable_url(self) -> str:
        return self.xa_elem.executableURL()

    @property
    def frontmost(self) -> bool:
        return self.xa_elem.isActive()

    @property
    def launch_date(self) -> datetime:
        return self.xa_elem.launchDate()

    @property
    def localized_name(self) -> str:
        return self.xa_elem.localizedName()

    @property
    def owns_menu_bar(self) -> bool:
        return self.xa_elem.ownsMenuBar()

    @property
    def process_identifier(self) -> str:
        return self.xa_elem.processIdentifier()

    def activate(self) -> 'XAApplication':
        """Activates the application, bringing its window(s) to the front and launching the application beforehand if necessary.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        .. seealso:: :func:`terminate`, :func:`unhide`, :func:`focus`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        return self

    def terminate(self) -> 'XAApplication':
        """Quits the application. Synonymous with quit().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.terminate()

        .. seealso:: :func:`quit`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def quit(self) -> 'XAApplication':
        """Quits the application. Synonymous with terminate().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.quit()

        .. seealso:: :func:`terminate`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def hide(self) -> 'XAApplication':
        """Hides all windows of the application.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.hide()

        .. seealso:: :func:`unhide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.hide()
        return self

    def unhide(self) -> 'XAApplication':
        """Unhides (reveals) all windows of the application, but does not does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.unhide()

        .. seealso:: :func:`hide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.unhide()
        return self

    def focus(self) -> 'XAApplication':
        """Hides the windows of all applications except this one.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.focus()

        .. seealso:: :func:`unfocus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
            if app.localizedName() != self.xa_elem.localizedName():
                app.hide()
            else:
                app.unhide()
        return self

    def unfocus(self) -> 'XAApplication':
        """Unhides (reveals) the windows of all other applications, but does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.unfocus()

        .. seealso:: :func:`focus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
                app.unhide()
        return self

    def _get_processes(self, processes):
        for process in self.xa_sevt.processes():
            processes.append(process)

    def windows(self, filter: dict = None) -> List['XAWindow']:
        return self.xa_prcs.windows(filter)

    @property
    def front_window(self) -> 'XAWindow':
        return self.xa_prcs.front_window

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_prcs.xa_elem.menuBars(), XAUIMenuBarList, filter)

    def get_clipboard_representation(self) -> List[Union[str, AppKit.NSURL, AppKit.NSImage]]:
        """Gets a clipboard-codable representation of the application.

        When the clipboard content is set to an application, three items are placed on the clipboard:
        1. The application's name
        2. The URL to the application bundle
        3. The application icon

        After copying an application to the clipboard, pasting will have the following effects:
        - In Finder: Paste a copy of the application bundle in the current directory
        - In Terminal: Paste the name of the application followed by the path to the application
        - In iWork: Paste the application name
        - In Safari: Paste the application name
        - In Notes: Attach a copy of the application bundle to the active note
        The pasted content may different for other applications.

        :return: The clipboard-codable representation
        :rtype: List[Union[str, AppKit.NSURL, AppKit.NSImage]]

        .. versionadded:: 0.0.8
        """
        print(type(self.xa_elem.icon()))
        return [self.xa_elem.localizedName(), self.xa_elem.bundleURL(), self.xa_elem.icon()]




class XASound(XAObject, XAClipboardCodable):
    """A wrapper class for NSSound objects and associated methods.

    .. versionadded:: 0.0.1
    """
    def __init__(self, sound_file: Union[str, AppKit.NSURL]):
        if isinstance(sound_file, str):
            if "/" in sound_file:
                sound_file = XAPath(sound_file)
            else:
                sound_file = XAPath("/System/Library/Sounds/" + sound_file + ".aiff")
        self.file = sound_file
        self.xa_elem = AppKit.NSSound.alloc()
        self.xa_elem.initWithContentsOfURL_byReference_(sound_file.xa_elem, True)

    def play(self) -> 'XASound':
        """Plays the sound from the beginning.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.play()

        .. seealso:: :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.stop()
        self.xa_elem.play()
        time.sleep(self.xa_elem.duration())
        return self

    def pause(self) -> 'XASound':
        """Pauses the sound.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.pause()

        .. seealso:: :func:`resume`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.pause()
        return self

    def resume(self) -> 'XASound':
        """Plays the sound starting from the time it was last paused at.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.resume()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.resume()
        return self

    def stop(self) -> 'XASound':
        """Stops playback of the sound and rewinds it to the beginning.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.stop()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.stop()
        return self

    def set_volume(self, volume: int) -> 'XASound':
        """Sets the volume of the sound.

        :param volume: The desired volume of the sound in the range [0.0, 1.0].
        :type volume: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.set_volume(1.0)

        .. seealso:: :func:`volume`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.setVolume_(volume)
        return self

    def volume(self) -> float:
        """Returns the current volume of the sound.

        :return: The volume level of the sound.
        :rtype: int

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> print(glass_sound.volume())
        1.0

        .. seealso:: :func:`set_volume`

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.volume()

    def loop(self, times: int) -> 'XASound':
        """Plays the sound the specified number of times.

        :param times: The number of times to loop the sound.
        :type times: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.loop(10)

        .. versionadded:: 0.0.1
        """
        self.xa_elem.setLoops_(times)
        self.xa_elem.play()
        time.sleep(self.xa_elem.duration() * times)
        self.xa_elem.stop()
        self.xa_elem.setLoops_(0)
        return self

    def get_clipboard_representation(self) -> List[Union[AppKit.NSSound, AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the sound.

        When the clipboard content is set to a sound, the raw sound data, the associated file URL, and the path string of the file are added to the clipboard.

        :return: The clipboard-codable form of the sound
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.file.xa_elem, self.file.xa_elem.path()]




class XAURL(XAObject, XAClipboardCodable):
    def __init__(self, url: Union[str, AppKit.NSURL]):
        super().__init__()
        self.parameters: str #: The query parameters of the URL
        self.scheme: str #: The URI scheme of the URL
        self.fragment: str #: The fragment identifier following a # symbol in the URL
        self.port: int #: The port that the URL points to
        self.html: element.tag #: The html of the URL
        self.title: str #: The title of the URL
        self.soup: BeautifulSoup = None #: The bs4 object for the URL, starts as None until a bs4-related action is made

        if isinstance(url, str):
            url = url.replace(" ", "%20")
            url = AppKit.NSURL.alloc().initWithString_(url)
        self.xa_elem = url

    @property
    def base_url(self) -> str:
        return self.xa_elem.host()

    @property
    def parameters(self) -> str:
        return self.xa_elem.query()

    @property
    def scheme(self) -> str:
        return self.xa_elem.scheme()

    @property
    def fragment(self) -> str:
        return self.xa_elem.fragment()

    @property
    def html(self) -> element.Tag:
        if self.soup is None:
            self.__get_soup()
        return self.soup.html

    @property
    def title(self) -> str:
        if self.soup is None:
            self.__get_soup()
        return self.soup.title.text

    def __get_soup(self):
        req = requests.get(str(self.xa_elem))
        self.soup = BeautifulSoup(req.text, "html.parser")

    def open(self):
        AppKit.NSWorkspace.sharedWorkspace().openURL_(self.xa_elem)

    def extract_text(self) -> List[str]:
        if self.soup is None:
            self.__get_soup()
        return self.soup.get_text().splitlines()

    def extract_images(self) -> List['XAImage']:
        data = AppKit.NSData.alloc().initWithContentsOfURL_(AppKit.NSURL.URLWithString_(str(self.xa_elem)))
        image = AppKit.NSImage.alloc().initWithData_(data)

        if image is not None:
            image_object = XAImage(image, name = self.xa_elem.pathComponents()[-1])
            return [image_object]
        else:
            if self.soup is None:
                self.__get_soup()

            images = self.soup.findAll("img")
            image_objects = []
            for image in images:
                image_src = image["src"]
                if image_src.startswith("/"):
                    image_src = str(self) + str(image["src"])

                data = AppKit.NSData.alloc().initWithContentsOfURL_(AppKit.NSURL.URLWithString_(image_src))
                image = AppKit.NSImage.alloc().initWithData_(data)
                if image is not None:
                    image_object = XAImage(image, name = XAURL(image_src).xa_elem.pathComponents()[-1])
                    image_objects.append(image_object)

            return image_objects

    def get_clipboard_representation(self) -> List[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the URL.

        When the clipboard content is set to a URL, the raw URL data and the string representation of the URL are added to the clipboard.

        :return: The clipboard-codable form of the URL
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, str(self.xa_elem)]

    def __str__(self):
        return str(self.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPath(XAObject, XAClipboardCodable):
    def __init__(self, path: Union[str, AppKit.NSURL]):
        super().__init__()
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_elem = path
        self.path = path.path()
        self.xa_wksp = AppKit.NSWorkspace.sharedWorkspace()

    def open(self):
        print(self.xa_elem)
        self.xa_wksp.openURL_(self.xa_elem)

    def select(self):
        self.xa_wksp.selectFile_inFileViewerRootedAtPath_(self.xa_elem)

    def get_clipboard_representation(self) -> List[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the path.

        When the clipboard content is set to a path, the raw file URL data and the string representation of the path are added to the clipboard.

        :return: The clipboard-codable form of the path
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.xa_elem.path()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPredicate(XAObject, XAClipboardCodable):
    def __init__(self):
        self.keys: List[str] = []
        self.operators: List[str] = []
        self.values: List[str] = []

    def from_dict(self, ref_dict: dict) -> 'XAPredicate':
        for key, value in ref_dict.items():
            self.keys.append(key)
            self.operators.append("==")
            self.values.append(value)
        return self

    def from_args(self, *args):
        arg_num = len(args)
        if arg_num % 2 != 0:
            raise InvalidPredicateError("The number of keys and values must be equal; the number of arguments must be an even number.")
        
        for index, value in enumerate(args):
            if index % 2 == 0:
                self.keys.append(value)
                self.operators.append("==")
                self.values.append(args[index + 1])
        return self

    def evaluate(self, target: AppKit.NSArray) -> AppKit.NSArray:
        placeholders = ["%@"] * len(self.values)
        expressions = [" ".join(expr) for expr in zip(self.keys, self.operators, placeholders)]
        format = "( " + " ) && ( ".join(expressions) + " )"
        predicate = AppKit.NSPredicate.predicateWithFormat_(format, *self.values)
        return target.filteredArrayUsingPredicate_(predicate)

    def evaluate_with_format(target: AppKit.NSArray, fmt: str) -> AppKit.NSArray:
        predicate = AppKit.NSPredicate.predicateWithFormat_(fmt)
        return target.filteredArrayUsingPredicate_(predicate)

    def evaluate_with_dict(target: AppKit.NSArray, properties_dict: dict) -> AppKit.NSArray:
        fmt = ""
        for key, value in properties_dict.items():
            if isinstance(value, str):
                value = "'" + value + "'"
            fmt += f"( {key} == {value} ) &&"
        predicate = AppKit.NSPredicate.predicateWithFormat_(fmt[:-3])
        return target.filteredArrayUsingPredicate_(predicate)

    # EQUAL
    def add_eq_condition(self, property: str, value: Any):
        """Appends an `==` condition to the end of the predicate format.

        The added condition will have the form `property == value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("==")
        self.values.append(value)

    def insert_eq_condition(self, index: int, property: str, value: Any):
        """Inserts an `==` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property == value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "==")
        self.values.insert(index, value)

    # NOT EQUAL
    def add_neq_condition(self, property: str, value: Any):
        """Appends a `!=` condition to the end of the predicate format.

        The added condition will have the form `property != value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("!=")
        self.values.append(value)

    def insert_neq_condition(self, index: int, property: str, value: Any):
        """Inserts a `!=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property != value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "!=")
        self.values.insert(index, value)

    # GREATER THAN OR EQUAL
    def add_geq_condition(self, property: str, value: Any):
        """Appends a `>=` condition to the end of the predicate format.

        The added condition will have the form `property >= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append(">=")
        self.values.append(value)

    def insert_geq_condition(self, index: int, property: str, value: Any):
        """Inserts a `>=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property >= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, ">=")
        self.values.insert(index, value)

    # LESS THAN OR EQUAL
    def add_leq_condition(self, property: str, value: Any):
        """Appends a `<=` condition to the end of the predicate format.

        The added condition will have the form `property <= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("<=")
        self.values.append(value)

    def insert_leq_condition(self, index: int, property: str, value: Any):
        """Inserts a `<=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property <= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "<=")
        self.values.insert(index, value)

    # GREATER THAN
    def add_gt_condition(self, property: str, value: Any):
        """Appends a `>` condition to the end of the predicate format.

        The added condition will have the form `property > value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append(">")
        self.values.append(value)

    def insert_gt_condition(self, index: int, property: str, value: Any):
        """Inserts a `>` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property > value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, ">")
        self.values.insert(index, value)

    # LESS THAN
    def add_lt_condition(self, property: str, value: Any):
        """Appends a `<` condition to the end of the predicate format.

        The added condition will have the form `property < value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("<")
        self.values.append(value)

    def insert_lt_condition(self, index: int, property: str, value: Any):
        """Inserts a `<` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property < value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "<")
        self.values.insert(index, value)

    # BETWEEN
    def add_between_condition(self, property: str, value1: Any, value2: Any):
        """Appends a `BETWEEN` condition to the end of the predicate format.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("BETWEEN")
        self.values.append([value1, value2])

    def insert_between_condition(self, index: int, property: str, value1: Any, value2: Any):
        """Inserts a `BETWEEN` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "BETWEEN")
        self.values.insert(index, [value1, value2])

    # BEGINSWITH
    def add_begins_with_condition(self, property: str, value: Any):
        """Appends a `BEGINSWITH` condition to the end of the predicate format.

        The added condition will have the form `property BEGINSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("BEGINSWITH")
        self.values.append(value)

    def insert_begins_with_condition(self, index: int, property: str, value: Any):
        """Inserts a `BEGINSWITH` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property BEGINSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "BEGINSWITH")
        self.values.insert(index, value)

    # ENDSWITH
    def add_ends_with_condition(self, property: str, value: Any):
        """Appends a `ENDSWITH` condition to the end of the predicate format.

        The added condition will have the form `property ENDSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("ENDSWITH")
        self.values.append(value)

    def insert_ends_with_condition(self, index: int, property: str, value: Any):
        """Inserts a `ENDSWITH` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property ENDSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "ENDSWITH")
        self.values.insert(index, value)

    # CONTAINS
    def add_contains_condition(self, property: str, value: Any):
        """Appends a `CONTAINS` condition to the end of the predicate format.

        The added condition will have the form `property CONTAINS value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("CONTAINS")
        self.values.append(value)

    def insert_contains_condition(self, index: int, property: str, value: Any):
        """Inserts a `CONTAINS` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property CONTAINS value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "CONTAINS")
        self.values.insert(index, value)

    # MATCHES
    def add_match_condition(self, property: str, value: Any):
        """Appends a `MATCHES` condition to the end of the predicate format.

        The added condition will have the form `property MATCHES value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("MATCHES")
        self.values.append(value)

    def insert_match_condition(self, index: int, property: str, value: Any):
        """Inserts a `MATCHES` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property MATCHES value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "MATCHES")
        self.values.insert(index, value)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the predicate.

        When a predicate is copied to the clipboard, the string representation of the predicate is added to the clipboard.

        :return: The string representation of the predicate
        :rtype: str

        .. versionadded:: 0.0.8
        """
        placeholders = ["%@"] * len(self.values)
        expressions = [" ".join(expr) for expr in zip(self.keys, self.operators, placeholders)]
        format = "( " + " ) && ( ".join(expressions) + " )"
        predicate = AppKit.NSPredicate.predicateWithFormat_(format, *self.values)
        return predicate.predicateFormat()




class XAUIElementList(XAList):
    """A wrapper around a list of UI elements.

    All properties of UI elements can be accessed via methods on this list, returning a list of the method's return value for each element in the list.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_type = None):
        if obj_type is None:
            obj_type = XAUIElement
        super().__init__(properties, obj_type, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def accessibility_description(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("accessibilityDescription"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def entire_contents(self) -> List[List[Any]]:
        return list(self.xa_elem.arrayByApplyingSelector_("entireContents"))

    def focused(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("focused"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def position(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def size(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def maximum_value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximumValue"))

    def minimum_value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("minimumValue"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def role(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("role"))

    def role_description(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("roleDescription"))

    def subrole(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subrole"))

    def selected(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected"))

    def by_properties(self, properties: dict) -> 'XAUIElement':
        return self.by_property("properties", properties)

    def by_accessibility_description(self, accessibility_description: str) -> 'XAUIElement':
        return self.by_property("accessibilityDescription", accessibility_description)

    def by_entire_contents(self, entire_contents: List[Any]) -> 'XAUIElement':
        return self.by_property("entireContents", entire_contents)

    def by_focused(self, focused: bool) -> 'XAUIElement':
        return self.by_property("focused", focused)

    def by_name(self, name: str) -> 'XAUIElement':
        return self.by_property("name", name)

    def by_title(self, title: str) -> 'XAUIElement':
        return self.by_property("title", title)

    def by_position(self, position: Tuple[Tuple[int, int], Tuple[int, int]]) -> 'XAUIElement':
        return self.by_property("position", position)

    def by_size(self, size: Tuple[int, int]) -> 'XAUIElement':
        return self.by_property("size", size)

    def by_maximum_value(self, maximum_value: Any) -> 'XAUIElement':
        return self.by_property("maximumValue", maximum_value)

    def by_minimum_value(self, minimum_value: Any) -> 'XAUIElement':
        return self.by_property("minimumValue", minimum_value)

    def by_value(self, value: Any) -> 'XAUIElement':
        return self.by_property("value", value)

    def by_role(self, role: str) -> 'XAUIElement':
        return self.by_property("role", role)

    def by_role_description(self, role_description: str) -> 'XAUIElement':
        return self.by_property("roleDescription", role_description)

    def by_subrole(self, subrole: str) -> 'XAUIElement':
        return self.by_property("subrole", subrole)

    def by_selected(self, selected: bool) -> 'XAUIElement':
        return self.by_property("selected", selected)

class XAUIElement(XAObject):
    def __init__(self, properties):
        super().__init__(properties)

        self.properties: dict #: All properties of the UI element
        self.accessibility_description: str #: The accessibility description of the element
        self.enabled: bool #: Whether the UI element is currently enabled
        self.entire_contents: Any #: The entire contents of the element
        self.focused: bool #: Whether the window is the currently element
        self.name: str #: The name of the element
        self.title: str #: The title of the element (often the same as its name)
        self.position: Tuple[int, int] #: The position of the top left corner of the element
        self.size: Tuple[int, int] #: The width and height of the element, in pixels
        self.maximum_value: Any #: The maximum value that the element can have
        self.minimum_value: Any #: The minimum value that the element can have
        self.value: Any #: The current value of the element
        self.role: str #: The element's role
        self.role_description: str #: The description of the element's role
        self.subrole: str #: The subrole of the UI element
        self.selected: bool #: Whether the element is currently selected

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def accessibility_description(self) -> str:
        return self.xa_elem.accessibilityDescription()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def entire_contents(self) -> List[XAObject]:
        ls = self.xa_elem.entireContents()
        return [self._new_element(x, XAUIElement) for x in ls]

    @property
    def focused(self) -> bool:
        return self.xa_elem.focused()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    @property
    def size(self) -> Tuple[int, int]:
        return self.xa_elem.size()

    @property
    def maximum_value(self) -> Any:
        return self.xa_elem.maximumValue()

    @property
    def minimum_value(self) -> Any:
        return self.xa_elem.minimumValue()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @property
    def role(self) -> str:
        return self.xa_elem.role()

    @property
    def role_description(self) -> str:
        return self.xa_elem.roleDescription()

    @property
    def subrole(self) -> str:
        return self.xa_elem.subrole()

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    def ui_elements(self, filter: dict = None) -> 'XAUIElementList':
        return self._new_element(self.xa_elem.UIElements(), XAUIElementList, filter)

    def windows(self, filter: dict = None) -> 'XAWindowList':
        return self._new_element(self.xa_elem.windows(), XAWindowList, filter)

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_elem.menuBars(), XAUIMenuBarList, filter)

    def menu_bar_items(self, filter: dict = None) -> 'XAUIMenuBarItemList':
        return self._new_element(self.xa_elem.menuBarItems(), XAUIMenuBarItemList, filter)

    def menus(self, filter: dict = None) -> 'XAUIMenuList':
        return self._new_element(self.xa_elem.menus(), XAUIMenuList, filter)

    def menu_items(self, filter: dict = None) -> 'XAUIMenuItemList':
        return self._new_element(self.xa_elem.menuItems(), XAUIMenuItemList, filter)

    def splitters(self, filter: dict = None) -> 'XAUISplitterList':
        return self._new_element(self.xa_elem.splitters(), XAUISplitterList, filter)

    def toolbars(self, filter: dict = None) -> 'XAUIToolbarList':
        return self._new_element(self.xa_elem.toolbars(), XAUIToolbarList, filter)

    def tab_groups(self, filter: dict = None) -> 'XAUITabGroupList':
        return self._new_element(self.xa_elem.tabGroups(), XAUITabGroupList, filter)

    def scroll_areas(self, filter: dict = None) -> 'XAUIScrollAreaList':
        return self._new_element(self.xa_elem.scrollAreas(), XAUIScrollAreaList, filter)

    def groups(self, filter: dict = None) -> 'XAUIGroupList':
        return self._new_element(self.xa_elem.groups(), XAUIGroupList, filter)

    def buttons(self, filter: dict = None) -> 'XAButtonList':
        return self._new_element(self.xa_elem.buttons(), XAButtonList, filter)

    def radio_buttons(self, filter: dict = None) -> 'XAUIRadioButtonList':
        return self._new_element(self.xa_elem.radioButtons(), XAUIRadioButtonList, filter)

    def actions(self, filter: dict = None) -> 'XAUIActionList':
        return self._new_element(self.xa_elem.actions(), XAUIActionList, filter)

    def text_fields(self, filter: dict = None) -> 'XAUITextfieldList':
        return self._new_element(self.xa_elem.textFields(), XAUITextfieldList, filter)

    def static_texts(self, filter: dict = None) -> 'XAUIStaticTextList':
        return self._new_element(self.xa_elem.staticTexts(), XAUIStaticTextList, filter)




class XAWindowList(XAUIElementList):
    """A wrapper around a list of windows.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAWindow)

    def collapse(self):
        """Collapses all windows in the list.

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.collapse()

    def uncollapse(self):
        """Uncollapses all windows in the list.

        .. versionadded:: 0.0.6
        """
        for window in self:
            window.uncollapse()

    def close(self):
        """Closes all windows in the list.add()
        
        .. versionadded:: 0.0.6
        """
        for window in self:
            window.close()

class XAWindow(XAUIElement):
    """A general window class for windows of both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XAApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def close(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        close_button = self.button({"subrole": "AXCloseButton"})
        close_button.click()
        return self

    def collapse(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        if hasattr(self.xa_elem.properties(), "miniaturized"):
            self.xa_elem.setValue_forKey_(True, "miniaturized")
        else:
            close_button = self.buttons({"subrole": "AXMinimizeButton"})[0]
            close_button.click()
        return self

    def uncollapse(self) -> 'XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        ls = self.xa_sevt.applicationProcesses()
        dock_process = XAPredicate.evaluate_with_format(ls, "name == 'Dock'")[0]

        ls = dock_process.lists()[0].UIElements()
        name = self.xa_prnt.xa_prnt.xa_elem.localizedName()
        app_icon = XAPredicate.evaluate_with_format(ls, f"name == '{name}'")[0]
        app_icon.actions()[0].perform()
        return self




class XAUIMenuBarList(XAUIElementList):
    """A wrapper around a list of menu bars.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIMenuBar)

class XAUIMenuBar(XAUIElement):
    """A menubar UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIMenuBarItemList(XAUIElementList):
    """A wrapper around a list of menu bar items.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIMenuBarItem)

class XAUIMenuBarItem(XAUIElement):
    """A menubar item UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIMenuList(XAUIElementList):
    """A wrapper around a list of menus.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIMenu)

class XAUIMenu(XAUIElement):
    """A menu UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIMenuItemList(XAUIElementList):
    """A wrapper around a list of menu items.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIMenuItem)

class XAUIMenuItem(XAUIElement):
    """A menu item UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def click(self) -> 'XAUIMenuItem':
        """Clicks the menu item. Synonymous with :func:`press`.

        :return: The menu item object.
        :rtype: XAUIMenuItem

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXPress"})[0].perform()
        return self

    def press(self) -> 'XAUIMenuItem':
        """Clicks the menu item. Synonymous with :func:`click`.

        :return: The menu item object.
        :rtype: XAUIMenuItem

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXPress"})[0].perform()
        return self




class XAUISplitterList(XAUIElementList):
    """A wrapper around a list of splitters.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUISplitter)

class XAUISplitter(XAUIElement):
    """A splitter UI element.
    
    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIToolbarList(XAUIElementList):
    """A wrapper around a list of toolbars.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIToolbar)

class XAUIToolbar(XAUIElement):
    """A toolbar UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIGroupList(XAUIElementList):
    """A wrapper around a list of UI element groups.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIGroup)

class XAUIGroup(XAUIElement):
    """A group of UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUITabGroupList(XAUIElementList):
    """A wrapper around a list of UI element tab groups.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUITabGroup)

class XAUITabGroup(XAUIElement):
    """A tab group UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIScrollAreaList(XAUIElementList):
    """A wrapper around a list of scroll areas.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIScrollArea)

class XAUIScrollArea(XAUIElement):
    """A scroll area UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAButtonList(XAUIElementList):
    """A wrapper around lists of buttons that employs fast enumeration techniques.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAButton)

class XAButton(XAUIElement):
    """A button UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def click(self) -> 'XAButton':
        """Clicks the button. Synonymous with :func:`press`.

        :return: The button object
        :rtype: XAButton

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXPress"})[0].perform()
        return self

    def press(self) -> 'XAButton':
        """Clicks the button. Synonymous with :func:`click`.

        :return: The button object
        :rtype: XAButton

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXPress"})[0].perform()
        return self

    def option_click(self) -> 'XAButton':
        """Option-Clicks the button.

        :return: The button object
        :rtype: XAButton

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXZoomWindow"})[0].perform()
        return self

    def show_menu(self) -> 'XAButton':
        """Right clicks the button, invoking a menu.

        :return: The button object
        :rtype: XAButton

        .. versionadded:: 0.0.2
        """
        self.actions({"name": "AXShowMenu"})[0].perform()
        return self




class XAUIRadioButtonList(XAUIElementList):
    """A wrapper around lists of radio buttons that employs fast enumeration techniques.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIRadioButton)

class XAUIRadioButton(XAUIElement):
    """A radio button UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIActionList(XAUIElementList):
    """A wrapper around a list of UI element actions.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIAction)

class XAUIAction(XAUIElement):
    """An action associated with a UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def perform(self):
        """Executes the action.
    
        .. versionadded:: 0.0.2
        """
        self.xa_elem.perform()




class XAUITextfieldList(XAUIElementList):
    """A wrapper around a list of textfields.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUITextfield)

class XAUITextfield(XAUIElement):
    """A textfield UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUIStaticTextList(XAUIElementList):
    """A wrapper around a list of static text elements.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAUIStaticText)

class XAUIStaticText(XAUIElement):
    """A static text UI element.
    
    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XATextDocument(XAObject):
    """A class for managing and interacting with text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.text: XAText #: The text of the document.

    @property
    def text(self) -> 'XAText':
        return self._new_element(self.xa_elem.text(), XAText)

    def set_text(self, new_text: str) -> 'XATextDocument':
        """Sets the text of the document.

        :param new_text: The new text of the document
        :type new_text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`prepend`, :func:`append`

        .. versionadded:: 0.0.1
        """
        self.set_property("text", new_text)
        return self

    def prepend(self, text: str) -> 'XATextDocument':
        """Inserts the provided text at the beginning of the document.

        :param text: The text to insert.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`append`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = self.text
        self.set_property("text", text + old_text)
        return self

    def append(self, text: str) -> 'XATextDocument':
        """Appends the provided text to the end of the document.

        :param text: The text to append.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`prepend`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = self.text
        self.set_property("text", old_text + text)
        return self

    def reverse(self) -> 'XATextDocument':
        """Reverses the text of the document.

        :return: A reference to the document object.
        :rtype: XATextDocument

        .. versionadded:: 0.0.4
        """
        self.set_property("text", reversed(self.text))
        return self

    def paragraphs(self, filter: dict = None) -> 'XAParagraphList':
        return self.text.paragraphs(filter)

    def sentences(self, filter: dict = None) -> 'XASentenceList':
        return self.text.sentences(filter)

    def words(self, filter: dict = None) -> 'XAWordList':
        return self.text.words(filter)

    def characters(self, filter: dict = None) -> 'XACharacterList':
        return self.text.characters(filter)

    def attribute_runs(self, filter: dict = None) -> 'XAAttributeRunList':
        return self.text.attribute_runs(filter)

    def attachments(self, filter: dict = None) -> 'XAAttachmentList':
        return self.text.attachments(filter)




class XATextList(XAList):
    """A wrapper around lists of text objects that employs fast enumeration techniques.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAText
        super().__init__(properties, obj_class, filter)

    def paragraphs(self, filter: dict = None) -> List['XAParagraphList']:
        ls = self.xa_elem.arrayByApplyingSelector_("paragraphs")
        return [self._new_element(x, XAParagraphList) for x in ls]

    def sentences(self, filter: dict = None) -> List['XASentenceList']:
        return [x.sentences() for x in self]

    def words(self, filter: dict = None) -> List['XAWordList']:
        ls = self.xa_elem.arrayByApplyingSelector_("words")
        return [self._new_element(x, XAWordList) for x in ls]

    def characters(self, filter: dict = None) -> List['XACharacterList']:
        ls = self.xa_elem.arrayByApplyingSelector_("characters")
        return [self._new_element(x, XACharacterList) for x in ls]

    def attribute_runs(self, filter: dict = None) -> List['XAAttributeRunList']:
        ls = self.xa_elem.arrayByApplyingSelector_("attributeRuns")
        return [self._new_element(x, XAAttributeRunList) for x in ls]

    def attachments(self, filter: dict = None) -> List['XAAttachmentList']:
        ls = self.xa_elem.arrayByApplyingSelector_("attachments")
        return [self._new_element(x, XAAttachmentList) for x in ls]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem.get()) + ">"

class XAText(XAObject):
    """A class for managing and interacting with the text of documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def paragraphs(self, filter: dict = None) -> 'XAParagraphList':
        return self._new_element(self.xa_elem.paragraphs(), XAParagraphList, filter)

    def sentences(self, filter: dict = None) ->  List[str]:
        raw_string = self.xa_elem.get()
        sentences = []
        tokenizer = AppKit.NLTokenizer.alloc().initWithUnit_(AppKit.kCFStringTokenizerUnitSentence)
        tokenizer.setString_(raw_string)
        for char_range in tokenizer.tokensForRange_((0, len(raw_string))):
            start = char_range.rangeValue().location
            end = start + char_range.rangeValue().length
            sentences.append(raw_string[start:end])
        # TODO: Only use Python/ObjC methods, not ScriptingBridge, to handle this -> 0.0.7
        # ls = AppKit.NSArray.alloc().initWithArray_(sentences)
        # return self._new_element(sentences, XASentenceList, filter) 
        return sentences

    def words(self, filter: dict = None) -> 'XAWordList':
        return self._new_element(self.xa_elem.words(), XAWordList, filter)

    def characters(self, filter: dict = None) -> 'XACharacterList':
        return self._new_element(self.xa_elem.characters().get(), XACharacterList, filter)

    def attribute_runs(self, filter: dict = None) -> 'XAAttributeRunList':
        return self._new_element(self.xa_elem.attributeRuns(), XAAttributeRunList, filter)

    def attachments(self, filter: dict = None) -> 'XAAttachmentList':
        return self._new_element(self.xa_elem.attachments(), XAAttachmentList, filter)

    def __len__(self):
        return len(self.xa_elem.get())

    def __str__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())

    def __repr__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())




class XAParagraphList(XATextList):
    """A wrapper around lists of paragraphs that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAParagraph)

class XAParagraph(XAText):
    """A class for managing and interacting with paragraphs in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)



# class XASentenceList(XATextList):
#     """A wrapper around lists of sentences that employs fast enumeration techniques.

#     .. versionadded:: 0.0.5
#     """
#     def __init__(self, properties: dict, filter: Union[dict, None] = None):
#         super().__init__(properties, XASentence, filter)

# class XASentence(XAText):
#     """A class for managing and interacting with sentences in text documents.

#     .. versionadded:: 0.0.1
#     """
#     def __init__(self, properties):
#         super().__init__(properties)

#     def words(self, filter: dict = None) -> 'XAWordList':
#         ls = AppKit.NSArray.alloc().initWithArray_(self.xa_elem.split(" "))
#         return self._new_element(ls, XAWordList, filter)




class XAWordList(XATextList):
    """A wrapper around lists of words that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAWord)

class XAWord(XAText):
    """A class for managing and interacting with words in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XACharacterList(XATextList):
    """A wrapper around lists of characters that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XACharacter)

class XACharacter(XAText):
    """A class for managing and interacting with characters in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAAttributeRunList(XATextList):
    """A wrapper around lists of attribute runs that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAttributeRun)

class XAAttributeRun(XAText):
    """A class for managing and interacting with attribute runs in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAAttachmentList(XATextList):
    """A wrapper around lists of text attachments that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAttachment)

class XAAttachment(XAObject):
    """A class for managing and interacting with attachments in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)



class XAColorList(XATextList):
    """A wrapper around lists of colors that employs fast enumeration techniques.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAColor, filter)

class XAColor(XAObject):
    def __init__(self, *args):
        if len(args) == 1:
            self.copy_color(args[0])
        else:
            red = args[0] if len(args) > 1 else 255
            green = args[1] if len(args) > 2 else 255
            blue = args[2] if len(args) > 3 else 255
            alpha = args[3] if len(args) == 4 else 1.0
            self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)

    def copy_color(self, color: AppKit.NSColor) -> 'XAColor':
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(
            color.redComponent(),
            color.greenComponent(),
            color.blueComponent(),
            color.alphaComponent()
        )
        return self
    
    def set_rgba(self, red, green, blue, alpha):
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)
        return self

    def red(self):
        return self.xa_elem.redComponent()

    def green(self):
        return self.xa_elem.greenComponent()

    def blue(self):
        return self.xa_elem.blueComponent()

    def alpha(self):
        return self.xa_elem.alphaComponent()

    def set_hsla(self, hue, saturation, brightness, alpha):
        # Alpha is 0.0 to 1.0
        self.xa_elem = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha)
        return self

    def hue(self):
        return self.xa_elem.hueComponent()

    def saturation(self):
        return self.xa_elem.saturationComponent()

    def brightness(self):
        return self.xa_elem.brightnessComponent()

    def mix_with(self, color: 'XAColor', fraction: int = 0.5) -> 'XAColor':
        new_color = self.xa_elem.blendedColorWithFraction_ofColor_(fraction, color.xa_elem)
        return XAColor(new_color.redComponent(), new_color.greenComponent(), new_color.blueComponent(), new_color.alphaComponent())

    def brighten(self, amount: float = 0.5) -> 'XAColor':
        self.xa_elem.highlightWithLevel_(amount)
        return self

    def darken(self, amount: float = 0.5) -> 'XAColor':
        self.xa_elem.shadowWithLevel_(amount)
        return self

    def __repr__(self):
        return f"<{str(type(self))}r={str(self.red())}, g={self.green()}, b={self.blue()}, a={self.alpha()}>"




class XAImageList(XAList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImage, filter)

class XAImage(XAObject, XAClipboardCodable):
    """A wrapper around NSImage with specialized automation methods.

    .. versionadded:: 0.0.2
    """
    def __init__(self, file: Union[str, AppKit.NSURL, AppKit.NSImage, None] = None, data: Union[AppKit.NSData, None] = None, name: Union[str, None] = None):
        self.size: Tuple[int, int] #: The dimensions of the image
        self.name: str #: The name of the image

        if data is not None:
            self.xa_elem = AppKit.NSImage.alloc().initWithData_(data)
        else:
            if file is None:
                self.xa_elem = AppKit.NSImage.alloc().init()
            else:
                if isinstance(file, AppKit.NSImage):
                    self.xa_elem = AppKit.NSImage.alloc().initWithData_(file.TIFFRepresentation())
                else:
                    if isinstance(file, str):
                        if file.startswith("/"):
                            file = XAPath(file)
                        else:
                            file = XAURL(file)
                    self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(file.xa_elem)
        self.name = name or "image"

    @property
    def size(self):
        return self.xa_elem.size()

    def show_in_preview(self):
        """Opens the image in preview.

        .. versionadded:: 0.0.8
        """
        tmp_file = tempfile.NamedTemporaryFile(suffix = self.name)
        with open(tmp_file.name, 'wb') as f:
            f.write(self.xa_elem.TIFFRepresentation())

        AppKit.NSWorkspace.sharedWorkspace().openFile_withApplication_(tmp_file.name, "Preview")
        time.sleep(0.1)

    def get_clipboard_representation(self) -> AppKit.NSImage:
        return self.xa_elem




# TODO: Init NSLocation object
class XALocation(XAObject):
    """A location with a latitude and longitude, along with other data.

    .. versionadded:: 0.0.2
    """
    def __init__(self, raw_value: Any = None, title: str = None, latitude: float = 0, longitude: float = 0, altitude: float = None, radius: int = 0, address: str = None, url: str = None, route_type: str = None, handle: str = None):
        self.raw_value = raw_value
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.radius = radius
        self.address = address
        self.url = url
        self.route_type = route_type
        self.handle = handle

    def set_raw_value(self, raw_value: Any):
        self.raw_value = raw_value

    def prepare_for_export(self):
        self.raw_value.setTitle_(self.title)
        self.raw_value.setGeoLocation_(CLLocation.alloc().initWithLatitude_longitude_(self.latitude, self.longitude))
        self.raw_value.setRadius_(self.radius)
        self.raw_value.setAddress_(self.address)
        self.raw_value.setGeoURLString_(self.url)
        self.raw_value.setRouteType_(self.route_type)
        self.raw_value.setMapKitHandle_(self.handle)

    def show_in_maps(self):
        """Shows the location in Maps.app.

        .. versionadded:: 0.0.6
        """
        XAURL(f"maps://?q={self.title},ll={self.latitude},{self.longitude}").open()

    


class XAAlertStyle(Enum):
    """Options for which alert style an alert should display with.
    """
    INFORMATIONAL   = AppKit.NSAlertStyleInformational
    WARNING         = AppKit.NSAlertStyleWarning
    CRITICAL        = AppKit.NSAlertStyleCritical

class XAAlert(XAObject):
    """A class for creating and interacting with an alert dialog window.

    .. versionadded:: 0.0.5
    """
    def __init__(self, title: str = "Alert!", message: str = "", style: XAAlertStyle = XAAlertStyle.INFORMATIONAL, buttons = ["Ok", "Cancel"]):
        super().__init__()
        self.title: str = title
        self.message: str = message
        self.style: XAAlertStyle = style
        self.buttons: List[str] = buttons

    def display(self) -> int:
        """Displays the alert.

        :return: A number representing the button that the user selected, if any
        :rtype: int

        .. versionadded:: 0.0.5
        """
        alert = AppKit.NSAlert.alloc().init()
        alert.setMessageText_(self.title)
        alert.setInformativeText_(self.message)
        alert.setAlertStyle_(self.style.value)

        for button in self.buttons:
            alert.addButtonWithTitle_(button)
        return alert.runModal()




class XAColorPickerStyle(Enum):
    """Options for which tab a color picker should display when first opened.
    """
    GRAYSCALE       = AppKit.NSColorPanelModeGray
    RGB_SLIDERS     = AppKit.NSColorPanelModeRGB
    CMYK_SLIDERS    = AppKit.NSColorPanelModeCMYK
    HSB_SLIDERS     = AppKit.NSColorPanelModeHSB
    COLOR_LIST      = AppKit.NSColorPanelModeColorList
    COLOR_WHEEL     = AppKit.NSColorPanelModeWheel
    CRAYONS         = AppKit.NSColorPanelModeCrayon
    IMAGE_PALETTE   = AppKit.NSColorPanelModeCustomPalette

class XAColorPicker(XAObject):
    """A class for creating and interacting with a color picker window.

    .. versionadded:: 0.0.5
    """
    def __init__(self, style: XAColorPickerStyle = XAColorPickerStyle.GRAYSCALE):
        super().__init__()
        self.style = style

    def display(self) -> XAColor:
        """Displays the color picker.

        :return: The color that the user selected
        :rtype: XAColor

        .. versionadded:: 0.0.5
        """
        panel = AppKit.NSColorPanel.sharedColorPanel()
        panel.setMode_(self.style.value)
        panel.setShowsAlpha_(True)

        def run_modal(panel):
                initial_color = panel.color()
                time.sleep(0.5)
                while panel.isVisible() and panel.color() == initial_color:
                    time.sleep(0.01)
                AppKit.NSApp.stopModal()

        modal_thread = threading.Thread(target=run_modal, args=(panel, ), name="Run Modal", daemon=True)
        modal_thread.start()

        AppKit.NSApp.runModalForWindow_(panel)
        return XAColor(panel.color())




class XADialog(XAObject):
    """A custom dialog window.

    .. versionadded:: 0.0.8
    """
    def __init__(self, text: str = "", title: str = "", buttons: Union[None, List[Union[str, int]]] = None, hidden_answer: bool = False, default_button: Union[str, int, None] = None, cancel_button: Union[str, int, None] = None, icon: Union[Literal["stop", "note", "caution"], None] = None, default_answer: Union[str, int, None] = None):
        super().__init__()
        self.text: str = text
        self.title: str = title
        self.buttons: Union[None, List[Union[str, int]]] = buttons or []
        self.hidden_answer: bool = hidden_answer
        self.icon: Union[str, None] = icon
        self.default_button: Union[str, int, None] = default_button
        self.cancel_button: Union[str, int, None] = cancel_button
        self.default_answer: Union[str, int, None] = default_answer

    def display(self) -> Union[str, int, None, List[str]]:
        """Displays the dialog, waits for the user to select an option or cancel, then returns the selected button or None if cancelled.

        :return: The selected button or None if no value was selected
        :rtype: Union[str, int, None, List[str]]

        .. versionadded:: 0.0.8
        """
        buttons = [x.replace("'", "") for x in self.buttons]
        buttons = str(buttons).replace("'", '"')

        default_button = str(self.default_button).replace("'", "")
        default_button_str = "default button \"" + default_button + "\"" if self.default_button is not None else ""

        cancel_button = str(self.cancel_button).replace("'", "")
        cancel_button_str = "cancel button \"" + cancel_button + "\"" if self.cancel_button is not None else ""

        icon_str = "with icon " + self.icon + "" if self.icon is not None else ""

        default_answer = str(self.default_answer).replace("'", '"')
        default_answer_str = "default answer \"" + default_answer + "\"" if self.default_answer is not None else ""

        script = AppKit.NSAppleScript.alloc().initWithSource_(f"""
        tell application "Terminal"
            display dialog \"{self.text}\" with title \"{self.title}\" buttons {buttons} {default_button_str} {cancel_button_str} {icon_str} {default_answer_str} hidden answer {self.hidden_answer}
        end tell
        """)
        result = script.executeAndReturnError_(None)[0]
        if result is not None:
            if result.numberOfItems() > 1:
                return [result.descriptorAtIndex_(1).stringValue(), result.descriptorAtIndex_(2).stringValue()]
            else:
                return result.descriptorAtIndex_(1).stringValue()
                



class XAMenu(XAObject):
    """A custom list item selection menu.

    .. versionadded:: 0.0.8
    """
    def __init__(self, menu_items: List[Any], title: str = "Select Item", prompt: str = "Select an item", default_items: Union[List[str], None] = None, ok_button_name: str = "Okay", cancel_button_name: str = "Cancel", multiple_selections_allowed: bool = False, empty_selection_allowed: bool = False):
        super().__init__()
        self.menu_items: List[Union[str, int]] = menu_items #: The items the user can choose from
        self.title: str = title #: The title of the dialog window
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.default_items: List[str] = default_items or [] #: The items to initially select
        self.ok_button_name: str = ok_button_name #: The name of the OK button
        self.cancel_button_name: str = cancel_button_name #: The name of the Cancel button
        self.multiple_selections_allowed: bool = multiple_selections_allowed #: Whether multiple items can be selected
        self.empty_selection_allowed: bool = empty_selection_allowed #: Whether the user can click OK without selecting anything

    def display(self) -> Union[str, int, bool, List[str], List[int]]:
        """Displays the menu, waits for the user to select an option or cancel, then returns the selected value or False if cancelled.

        :return: The selected value or False if no value was selected
        :rtype: Union[str, int, bool, List[str], List[int]]

        .. versionadded:: 0.0.8
        """
        menu_items = [x.replace("'", "") for x in self.menu_items]
        menu_items = str(menu_items).replace("'", '"')
        default_items = str(self.default_items).replace("'", '"')
        script = AppKit.NSAppleScript.alloc().initWithSource_(f"""
        tell application "Terminal"
            choose from list {menu_items} with title \"{self.title}\" with prompt \"{self.prompt}\" default items {default_items} OK button name \"{self.ok_button_name}\" cancel button name \"{self.cancel_button_name}\" multiple selections allowed {self.multiple_selections_allowed} empty selection allowed {self.empty_selection_allowed}
        end tell
        """)
        result = script.executeAndReturnError_(None)[0]
        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(desc.stringValue())
                return values
            else:
                if result.stringValue() == "false":
                    return False
                return result.stringValue()




class XAFilePicker(XAObject):
    """A file selection window.

    .. versionadded:: 0.0.8
    """
    def __init__(self, prompt: str = "Choose File", types: List[str] = None, default_location: Union[str, None] = None, show_invisibles: bool = False, multiple_selections_allowed: bool = False, show_package_contents: bool = False):
        super().__init__()
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.types: List[str] = types #: The file types/type identifiers to allow for selection
        self.default_location: Union[str, None] = default_location #: The default file location
        self.show_invisibles: bool = show_invisibles #: Whether invisible files and folders are shown
        self.multiple_selections_allowed: bool = multiple_selections_allowed #: Whether the user can select multiple files
        self.show_package_contents: bool = show_package_contents #: Whether to show the contents of packages

    def display(self) -> Union[XAPath, None]:
        """Displays the file chooser, waits for the user to select a file or cancel, then returns the selected file URL or None if cancelled.

        :return: The selected file URL or None if no file was selected
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """
        types = [x.replace("'", "") for x in self.types]
        types = str(types).replace("'", '"')
        types_str = "of type " + types if self.types is not None else ""

        default_location_str = "default location \"" + self.default_location + "\"" if self.default_location is not None else ""

        script = AppKit.NSAppleScript.alloc().initWithSource_(f"""
        tell application "Terminal"
            choose file with prompt \"{self.prompt}\" {types_str}{default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """)
        result = script.executeAndReturnError_(None)[0]

        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(XAPath(desc.fileURLValue()))
                return values
            else:
                return XAPath(result.fileURLValue())




class XAFolderPicker(XAObject):
    """A folder selection window.

    .. versionadded:: 0.0.8
    """
    def __init__(self, prompt: str = "Choose Folder", default_location: Union[str, None] = None, show_invisibles: bool = False, multiple_selections_allowed: bool = False, show_package_contents: bool = False):
        super().__init__()
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.default_location: Union[str, None] = default_location #: The default folder location
        self.show_invisibles: bool = show_invisibles #: Whether invisible files and folders are shown
        self.multiple_selections_allowed: bool = multiple_selections_allowed #: Whether the user can select multiple folders
        self.show_package_contents: bool = show_package_contents #: Whether to show the contents of packages

    def display(self) -> Union[XAPath, None]:
        """Displays the folder chooser, waits for the user to select a folder or cancel, then returns the selected folder URL or None if cancelled.

        :return: The selected folder URL or None if no folder was selected
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """

        default_location_str = "default location \"" + self.default_location + "\"" if self.default_location is not None else ""

        script = AppKit.NSAppleScript.alloc().initWithSource_(f"""
        tell application "Terminal"
            choose folder with prompt \"{self.prompt}\" {default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """)
        result = script.executeAndReturnError_(None)[0]
        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(XAPath(desc.fileURLValue()))
                return values
            else:
                return XAPath(result.fileURLValue())




class XAFileNameDialog(object):
    """A file name input window.

    .. versionadded:: 0.0.8
    """
    def __init__(self, prompt: str = "Specify file name and location", default_name: str = "New File", default_location: Union[str, None] = None):
        super().__init__()
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.default_name: str = default_name #: The default name for the new file
        self.default_location: Union[str, None] = default_location #: The default file location

    def display(self) -> Union[XAPath, None]:
        """Displays the file name input window, waits for the user to input a name and location or cancel, then returns the specified file URL or None if cancelled.

        :return: The specified file URL or None if no file name was inputted
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """

        default_location_str = "default location \"" + self.default_location + "\"" if self.default_location is not None else ""

        script = AppKit.NSAppleScript.alloc().initWithSource_(f"""
        tell application "Terminal"
            choose file name with prompt \"{self.prompt}\" default name \"{self.default_name}\" {default_location_str}
        end tell
        """)
        result = script.executeAndReturnError_(None)[0]
        if result is not None:
            return XAPath(result.fileURLValue())