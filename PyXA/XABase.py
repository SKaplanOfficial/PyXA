""".. versionadded:: 0.0.1

General classes and methods applicable to any PyXA object.
"""

from datetime import datetime
from enum import Enum
import time, os, sys
from typing import Any, Callable, Tuple, Union, List, Dict
import threading

import AppKit
from CoreLocation import CLLocation
from ScriptingBridge import SBApplication, SBElementArray

import threading, signal

from PyXA.XAErrors import InvalidPredicateError

def OSType(s: str):
    return int.from_bytes(s.encode("UTF-8"), "big")

def unOSType(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()




class AppleScript():
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




class XAObject():
    """A general class for PyXA scripting objects.

    .. seealso:: :class:`XASBObject`

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
        self.xa_prnt = properties.get("parent", None)
        self.xa_apsp = properties.get("appspace", None)
        self.xa_wksp = properties.get("workspace", None)
        self.xa_elem = properties.get("element", None)
        self.xa_scel = properties.get("scriptable_element", None)
        self.xa_aref = properties.get("appref", None)
        self.xa_sevt = properties.get("system_events", SBApplication.alloc().initWithBundleIdentifier_("com.apple.systemevents"))

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
        self.element_properties = element.properties()
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

    def set_clipboard(self, content: Any) -> None:
        """Sets the clipboard to the specified content.

        :param content: The item or object to set the clipboard to. Can be a list of items.
        :type content: Any

        .. seealso:: :func:`get_clipboard`, :func:`get_clipboard_strings`

        .. deprecated:: 0.0.5
           Use :func:`XAClipboard.set_contents` instead

        .. versionadded:: 0.0.1
        """
        pb = AppKit.NSPasteboard.generalPasteboard()
        pb.clearContents()
        if isinstance(content, list):
            pb.writeObjects_(content)
        else:
            pb.writeObjects_(AppKit.NSArray.arrayWithObject_(content))
    



class XAClipboard(XAObject):
    """A wrapper class for managing and interacting with the system pasteboard

    .. versionadded:: 0.0.5
    """
    def __init__(self):
        self.xa_elem = AppKit.NSPasteboard.generalPasteboard()
        self.content #: The content of the clipboard

    @property
    def content(self) -> Any:
        items = []
        for item in self.xa_elem.pasteboardItems():
            for item_type in item.types():
                items.append(item.dataForType_(item_type))
        return items

    def clear(self):
        """Clears the system clipboard.
        
        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()

    def set_contents(self, content: List[Any]):
        self.xa_elem.clearContents()
        self.xa_elem.writeObjects_(content)




class XAList(XAObject):
    """A wrapper around NSArray and NSMutableArray objects enabling fast enumeration and lazy evaluation of Objective-C objects.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties, object_class = None, filter: Union[dict, None] = None):
        super().__init__(properties)
        self.xa_ocls = object_class

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def by_property(self, property: str, value: Any) -> XAObject:
        """Retrieves the element whose property value matches the given value, if one exists.

        :param property: The property to match
        :type property: str
        :param value: The value to match
        :type value: Any
        :return: The matching element, if one is found
        :rtype: XAObject

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

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_contains_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        obj = ls[0]
        return self._new_element(obj, self.xa_ocls)

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


### Mixins
## Action Mixins
class XACanPrintPath(XAObject):
    """A class for scriptable objects that can print the file at a given path.
    """
    def print(self, target: Union[str, AppKit.NSURL]) -> XAObject:
        """pens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to print.
        :type target: Union[str, AppKit.NSURL]
        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. note::
        
            The implementation of a printing method various across applications, and some do not have the same method signature. If this presents a problem for a specific application, a custom print method should be defined for that application class.

        .. versionadded:: 0.0.1
        """
        if not isinstance(target, AppKit.NSURL):
            target = XAPath(target)
        self.xa_elem.print(target)
        return self

class XACanOpenPath(XAObject):
    """A class for scriptable objects that can open an item at a given path (either in its default application or in an application whose PyXA object extends this class).
    
    .. seealso:: :class:`XABaseScriptable.XASBPrintable`

    .. versionadded:: 0.0.1
    """
    def open(self, path: Union[str, AppKit.NSURL]) -> XAObject:
        """Opens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to open.
        :type target: Union[str, AppKit.NSURL]
        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        if not isinstance(path, AppKit.NSURL):
            path = XAPath(path)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self

class XAAcceptsPushedElements(XAObject):
    """A class for scriptable objects that either have lists or are themselves lists that other scriptable objects can be pushed onto.

    .. versionadded:: 0.0.1
    """
    def push(self, element_specifier: Union[str, AppKit.NSObject], properties: dict, location: SBElementArray, object_class = XAObject) -> XAObject:
        """Appends the supplied element or an element created from the supplied specifier and properties to the scriptable object list at the specified location.

        :param element_specifier: Either the scripting class to create a new object of or an existing instance of a scripting class.
        :type element_specifier: Union[str, NSObject]
        :param properties: _description_
        :type properties: dict
        :param location: _description_
        :type location: SBElementArray'
        :param object_class: The PyXA class to wrap the newly created object in, defaults to XAObject
        :type object_class: type
        :return: A reference to the new created PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        if isinstance(element_specifier, str):
            element_specifier = self.construct(element_specifier, properties)
        location.addObject_(element_specifier)
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element_specifier,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return object_class(properties)


class XACanConstructElement(XAObject):
    """A class for scriptable objects that are able to create new scriptable objects.

    .. versionadded:: 0.0.1
    """
    def construct(self, specifier: str, properties: dict) -> AppKit.NSObject:
        """Initializes a new NSObject of the given specifier class with the supplied dictionary of properties.

        :param specifier: The scripting class to create a new object of.
        :type specifier: str
        :param properties: A dictionary of property names and values appropriate for the specified scripting class.
        :type properties: dict
        :return: A reference to the newly created NSObject.
        :rtype: NSObject

        .. versionadded:: 0.0.1
        """
        if self.xa_scel is not None:
            return self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)
        return self.xa_elem.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)
        
## Relation Mixins
class XAHasElements(XAObject):
    def elements(self, specifier, filter, obj_type):
        ls = self.xa_elem.__getattribute__(specifier)()
        if filter is not None:
            ls = XAPredicate.evaluate_with_dict(ls, filter)

        elements = []
        for element in ls:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            elements.append(obj_type(properties))
        return elements

    def element_with_properties(self, specifier, filter, obj_type):
        if isinstance(filter, int):
            element = self.xa_elem.__getattribute__(specifier)()[filter]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            return obj_type(properties)
        return self.elements(specifier, filter, obj_type)[0]

    def first_element(self, specifier, obj_type):
        element = self.xa_elem.__getattribute__(specifier)()[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)

    def last_element(self, specifier, obj_type):
        element = self.xa_elem.__getattribute__(specifier)()[-1]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)


class XAShowable(XAObject):
    def show(self) -> XAObject:
        """Shows a document, window, or item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.show()

class XASelectable(XAObject):
    def select(self) -> XAObject:
        """Selects a document or item. This may open a new window, depending on which kind of object and application it acts on.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()

class XADeletable(XAObject):
    def delete(self) -> XAObject:
        """Deletes a document or item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        deletion_thread = threading.Thread(target=self.xa_elem.delete, name="Delete", daemon=True)
        deletion_thread.start()




### Elements
class XAProcess(XAHasElements):
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = properties["window_class"]
        self.id = self.xa_elem.id()
        self.unix_id = self.xa_elem.unixId()

    def windows(self, filter: dict = None) -> 'XAWindowList':
        return self._new_element(self.xa_elem.windows(), XAWindowList, filter)

    def front_window(self) -> 'XAWindow':
        return self._new_element(self.xa_elem.windows()[0], XAWindow)

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_elem.menuBars(), XAUIMenuBarList, filter)




class XAApplication(XAObject):
    """A general application class for both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XASBApplication`, :class:`XAWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAWindow

        predicate = AppKit.NSPredicate.predicateWithFormat_("name == %@", self.xa_elem.localizedName())
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

    def front_window(self) -> 'XAWindow':
        return self.xa_prcs.front_window()

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_prcs.xa_elem.menuBars(), XAUIMenuBarList, filter)




class XASound(XAObject):
    """A wrapper class for NSSound objects and associated methods.

    .. versionadded:: 0.0.1
    """
    def __init__(self, sound_file: Union[str, AppKit.NSURL]):
        if isinstance(sound_file, str):
            if "/" in sound_file:
                sound_file = XAPath(sound_file)
            else:
                sound_file = XAPath("/System/Library/Sounds/" + sound_file + ".aiff")
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




class XAURL(object):
    def __init__(self, url: Union[str, AppKit.NSURL]):
        super().__init__()
        if isinstance(url, str):
            url = url.replace(" ", "%20")
            url = AppKit.NSURL.alloc().initWithString_(url)
        self.xa_elem = url

    def open(self):
        AppKit.NSWorkspace.sharedWorkspace().openURL_(self.xa_elem)

def xa_url(url: str) -> AppKit.NSURL:
    """Converts a string-type URL into an NSURL object.

    :param url: The filepath or URL to convert.
    :type url: str
    :return: The NSURL form of the supplied filepath/URL.
    :rtype: AppKit.NSURL

    :Example:

    >>> from XABase import xa_url
    >>> url = xa_url("https://www.google.com")
    >>> print(type(url))
    # TODO: This

    .. seealso:: :func:`xa_path`

    .. deprecated:: 0.0.5
       Use :class:`XAURL` instead.

    .. versionadded:: 0.0.1
    """
    return AppKit.NSURL.alloc().initWithString_(url)




class XAPath(object):
    def __init__(self, path: Union[str, AppKit.NSURL]):
        super().__init__()
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_elem = path
        self.xa_wksp = AppKit.NSWorkspace.sharedWorkspace()

    def open(self):
        self.xa_wksp.openURL_(self.xa_elem)

    def select(self):
        self.xa_wksp.selectFile_inFileViewerRootedAtPath_(self.xa_elem)

def xa_path(filepath: str):
    """Converts a string-type filepath into an NSURL object.

    :param url: The filepath or URL to convert.
    :type url: str
    :return: The NSURL form of the supplied filepath/URL.
    :rtype: AppKit.NSURL

    .. deprecated:: 0.0.5
       Use :class:`XAPath` instead.

    .. versionadded:: 0.0.1
    """
    return AppKit.NSURL.alloc().initWithString_(filepath)




class XAPredicate():
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
    def add_end_with_condition(self, property: str, value: Any):
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




class XAUIElementList(XAList):
    """A wrapper around a list of UI elements.

    All properties of UI elements can be accessed via methods on this list, returning a list of the method's return value for each element in the list.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, obj_type = None, filter: Union[dict, None] = None):
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

class XAUIElement(XAHasElements):
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
        super().__init__(properties, XAWindow, filter)

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
        super().__init__(properties, XAUIMenuBar, filter)

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
        super().__init__(properties, XAUIMenuBarItem, filter)

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
        super().__init__(properties, XAUIMenu, filter)

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
        super().__init__(properties, XAUIMenuItem, filter)

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




class XAUIToolbarList(XAUIElementList):
    """A wrapper around a list of toolbars.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAUIToolbar, filter)

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
        super().__init__(properties, XAUIGroup, filter)

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
        super().__init__(properties, XAUIGroup, filter)

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
        super().__init__(properties, XAUIGroup, filter)

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
        super().__init__(properties, XAButton, filter)

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
        super().__init__(properties, XAButton, filter)

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
        super().__init__(properties, XAUIAction, filter)

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
        super().__init__(properties, XAUITextfield, filter)

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
        super().__init__(properties, XAUIStaticText, filter)

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
    def __init__(self, properties: dict, obj_class = None, filter: Union[dict, None] = None):
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
        super().__init__(properties, XAParagraph, filter)

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
        super().__init__(properties, XAWord, filter)

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
        super().__init__(properties, XACharacter, filter)

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
        super().__init__(properties, XAAttributeRun, filter)

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
        super().__init__(properties, XAAttachment, filter)

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

class XAColor():
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

class XAImage():
    def __init__(self, file_url: Union[str, AppKit.NSURL, None] = None):
        if file_url is None:
            self.xa_elem = AppKit.NSImage.alloc().init()
        else:
            if isinstance(file_url, AppKit.NSImage):
                self.xa_elem = AppKit.NSImage.alloc().initWithData_(file_url.TIFFRepresentation())
            else:
                if isinstance(file_url, str):
                    if file_url.startswith("/"):
                        file_url = XAPath(file_url)
                    else:
                        file_url = XAURL(file_url)
                self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(file_url.xa_elem)

    def size(self):
        return self.xa_elem.size()



# TODO: Init NSLocation object
class XALocation():
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

class XAAlert(object):
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

    def package_for_script(self) -> 'XAAlert':
        return self




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

class XAColorPicker(object):
    """A class for creating and interacting with a color picker window.

    .. versionadded:: 0.0.5
    """
    def __init__(self, style: XAColorPickerStyle = XAColorPickerStyle.GRAYSCALE):
        super().__init__()
        self.style = style

    def display(self) -> XAColor:
        """Displays the color picket.

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