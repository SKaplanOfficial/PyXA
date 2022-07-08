from datetime import datetime
from enum import Enum
import os
from time import sleep
from typing import Any, Callable, List, Union
import threading
from numpy import isin
import yaml

import AppKit
from AppKit import (
    NSWorkspace,
    NSApplication,
    NSSound,
    NSPasteboard,
    NSArray,
    NSPasteboardTypeString,
    NSAppleScript,
    NSAlert, NSAlertStyleCritical, NSAlertStyleInformational, NSAlertStyleWarning,
    NSColorPanel
)
from Foundation import NSURL, NSBundle

from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

from .XABase import *
from .XAErrors import ApplicationNotFoundError
from .apps import application_classes

VERSION = "0.0.5"
DATE = str(datetime.now())

appspace = NSApplication.sharedApplication()
workspace = NSWorkspace.sharedWorkspace()
apps = []

def _get_path_to_app(app_identifier: str) -> str:
    if not app_identifier.endswith(".app"):
            app_identifier += ".app"

    def _check(path, _index, _stop):
        nonlocal app_identifier
        current_path = path + "/" + app_identifier
        if os.path.exists(current_path):
            app_identifier = current_path

    if not app_identifier.startswith("/"):
        locations = AppKit.NSMutableArray.arrayWithArray_(workspace._locationsForApplications())
        locations.insertObject_atIndex_("/System/Applications", 0)
        locations.insertObject_atIndex_("/Applications", 0)
        locations.enumerateObjectsUsingBlock_(_check)

    if os.path.exists(app_identifier):
        return app_identifier

    raise ApplicationNotFoundError(app_identifier)

def running_applications() -> List[XAApplication]:
    """Gets PyXA references to all currently running applications whose app bundles are stored in typical application directories.

    :return: A list of PyXA application objects.
    :rtype: List[XAApplication]
    
    .. versionadded:: 0.0.1
    """
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    ls = XAPredicate.evaluate_with_format(windows, "kCGWindowIsOnscreen == 1 && kCGWindowLayer == 0")
    properties = {
        "parent": None,
        "appspace": appspace,
        "workspace": workspace,
        "element": ls,
    }
    arr = XAApplicationList(properties, XAApplication)
    return arr

class XAApplicationList(XAList):
    """A wrapper around a list of applications.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAApplication, filter)
        
    def __init__(self, properties, object_class = None, filter: Union[dict, None] = None):
        super().__init__(properties)
        self.xa_ocls = object_class

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def by_property(self, property: str, value: Any) -> XAObject:
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        self.xa_elem = predicate.evaluate(self.xa_elem)
        obj = self.xa_elem[0]
        return self._new_element(obj, self.xa_ocls)

    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(0)

    def last(self) -> XAObject:
        """Retrieves the last element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(-1)

    def pop(self, index: int = -1) -> XAObject:
        """Removes the object at the specified index from the list and returns it.

        .. versionadded:: 0.0.5
        """
        removed = self.xa_elem.lastObject()
        self.xa_elem.removeLastObject()
        app_name = removed["kCGWindowOwnerName"]
        return application(app_name)

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            arr = AppKit.NSArray.alloc().initWithArray_([self.xa_elem[index] for index in range(key.start, key.stop, key.step or 1)])
            return self._new_element(arr, self.__class__)
        app_name = self.xa_elem[key]["kCGWindowOwnerName"]
        return application(app_name)

    def bundle_identifier(self) -> List[str]:
        return [app.bundle_identifier for app in self]

    def bundle_url(self) -> List[str]:
        return [app.bundle_url for app in self]

    def executable_url(self) -> List[str]:
        return [app.executable_url for app in self]

    def launch_date(self) -> List[datetime]:
        return [app.launch_date for app in self]

    def localized_name(self) -> List[str]:
        return [x.get("kCGWindowOwnerName") for x in self.xa_elem]

    def process_identifier(self) -> List[str]:
        return [x.get("kCGWindowOwnerPID") for x in self.xa_elem]

    def hide(self):
        for app in self:
            app.hide()

    def unhide(self):
        for app in self:
            app.unhide()

    def terminate(self):
        for app in self:
            app.terminate()

    def quit(self):
        for app in self:
            app.terminate()

    def __iter__(self):
        return (application(object["kCGWindowOwnerName"]) for object in self.xa_elem.objectEnumerator())

    def __repr__(self):
        return "<" + str(type(self)) + str(self.localized_name()) + ">"

def current_application() -> XAApplication:
    """Retrieves a PyXA representation of the frontmost application.

    :return: A PyXA application object referencing the current application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """
    app = workspace.frontmostApplication()
    properties = {
        "parent": None,
        "appspace": appspace,
        "workspace": workspace,
        "element": app,
        "appref": app,
    }
    app = application_classes.get(app.localizedName().lower(), XAApplication)(properties)
    apps.append(app)
    return app

def application(app_identifier: str) -> XAApplication:
    """Retrieves a PyXA application object representation of the target application without launching or activating the application.

    :param app_identifier: The name of the application to get an object of.
    :type app_identifier: str
    :return: A PyXA application object referencing the target application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """

    def _match_open_app(obj, index, stop):
        return (obj.localizedName() == app_identifier, stop)

    idx_set = workspace.runningApplications().indexesOfObjectsPassingTest_(_match_open_app)
    if idx_set.count() == 1:
        index = idx_set.firstIndex()
        app = workspace.runningApplications()[index]
        properties = {
            "parent": None,
            "appspace": appspace,
            "workspace": workspace,
            "element": app,
            "appref": app,
        }
        app_ref = application_classes.get(app_identifier.lower(), XAApplication)(properties)
        apps.append(app_ref)
        return app_ref

    app_path = _get_path_to_app(app_identifier)
    bundle = NSBundle.alloc().initWithPath_(app_path)
    url = workspace.URLForApplicationWithBundleIdentifier_(bundle.bundleIdentifier())

    config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
    config.setActivates_(False)
    config.setHides_(True)

    app_ref = None
    def _launch_completion_handler(app, _error):
        nonlocal app_ref
        properties = {
            "parent": None,
            "appspace": appspace,
            "workspace": workspace,
            "element": app,
            "appref": app,
        }
        app = application_classes.get(app_identifier.lower(), XAApplication)(properties)
        apps.append(app)
        app_ref = app

    
    workspace.openApplicationAtURL_configuration_completionHandler_(url, config, _launch_completion_handler)
    while app_ref is None:
        sleep(0.01)
    return app_ref

def open_url(path: Union[str, NSURL]) -> None:
    """Opens the document at the given URL in its default application.

    :param path: The path of the item to open. This can be a file path, folder path, web address, or application URL.
    :type path: Union[str, NSURL]

    .. deprecated:: 0.0.5
       Use :class:`XAURL` instead.

    .. versionadded:: 0.0.2
    """
    url = path
    if isinstance(path, str):
        url = NSURL.alloc().initWithString_(path)
    if not url.path().startswith("/"):
        url = NSURL.alloc().initFileURLWithPath_(url.path())
    workspace.openURL_(url)

def get_clipboard() -> List[bytes]:
    """Returns the byte representation of all items on the clipboard.

    :return: A list of items currently on the clipboard in their byte representation.
    :rtype: List[bytes]

    .. seealso:: :func:`get_clipboard_strings`, :func:`set_clipboard`

    .. deprecated:: 0.0.5
       Use :ivar:`XABase.XAClipboard.content` instead.

    .. versionadded:: 0.0.1
    """
    items = []
    pb = NSPasteboard.generalPasteboard()
    for item in pb.pasteboardItems():
        for item_type in item.types():
            items.append(item.dataForType_(item_type))
    return items

def get_clipboard_strings() -> List[str]:
    """Returns the string representation all items on the clipboard that can be represented as strings.

    :return: A list of items currently on the clipboard in their string representation.
    :rtype: List[str]

    .. seealso:: :func:`get_clipboard`, :func:`set_clipboard`

    .. deprecated:: 0.0.5
       Use :ivar:`XABase.XAClipboard.content` instead.

    .. versionadded:: 0.0.1
    """
    items = []
    pb = NSPasteboard.generalPasteboard()
    for item in pb.pasteboardItems():
        if NSPasteboardTypeString in item.types():
            decoded_item = item.dataForType_(NSPasteboardTypeString).decode()
            if "\r" in decoded_item:
                items.extend(decoded_item.split("\r"))
            elif "\n" in decoded_item:
                items.extend(decoded_item.split("\n"))
            else:
                items.append(decoded_item)
    return items

def set_clipboard(content: Any) -> None:
    """Sets the clipboard to the specified content.

    :param content: The item or object to set the clipboard to. Can be a list of items.
    :type content: Any

    .. seealso:: :func:`get_clipboard`, :func:`get_clipboard_strings`

    .. deprecated:: 0.0.5
       Use :func:`XABase.XAClipboard.set_content` instead.

    .. versionadded:: 0.0.1
    """
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    pb.writeObjects_(NSArray.arrayWithObject_(content))

def run_applescript(source: Union[str, NSURL]) -> Any:
    """Runs AppleScript and returns its result.

    :param source: Either AppleScript code as text or the path to a .scpt file.
    :type source: Union[str, NSURL]
    :return: The value returned from the script upon completing execution.
    :rtype: Any

    .. versionadded:: 0.0.1
    """
    script = None
    if source.startswith("/"):
        source = NSURL.fileURLWithPath_(source)
        script = NSAppleScript.initWithContentsOfURL_error_(source, None)
    elif isinstance(source, NSURL):
        script = NSAppleScript.initWithContentsOfURL_error_(source, None)
    else:
        script = NSAppleScript.alloc().initWithSource_(source)


class PyXAAction(object):
    """A class representing a single method call in a larger PyXA script.

    .. versionadded:: 0.0.5
    """
    def __init__(self, method: Union[Callable[..., Any], str], args: List[Any] = None, specifier_names: List[str] = None, return_object_specifier: str = None):
        self.method = method
        self.args = args or []
        self.specifier_names = specifier_names or []
        self.return_object_specifier = return_object_specifier

class PyXAScript(object):
    """A class for creating, saving, and loading PyXA scripts that execute upon calling run().

    :Example 1: Creating a script to search input on Google

    >>> script = PyXA.PyXAScript()
    >>> script.set_specifier("url_base", "https://www.google.com/search?q=")
    >>> script.add_call(PyXA.open_url, ["<<url_base>><<input>>"])
    >>> script.save("/Users/exampleuser/Documents/pyxa_scripts/search_google")

    :Example 2: Loading and running the script from Example 1

    >>> script = PyXA.PyXAScript().load("/Users/exampleuser/Documents/pyxa_scripts/search_google")
    >>> script.run("Testing 1 2 3")

    .. versionadded:: 0.0.5
    """
    def __init__(self, actions: List[PyXAAction] = None, specifiers: dict = None, name: str = None):
        """Initializes a new PyXA script.

        :param actions: The actions to include in this script, defaults to None
        :type actions: List[PyXAAction], optional
        :param specifiers: The specifiers to predefine for the script, defaults to None
        :type specifiers: dict, optional
        :param name: The name of the script, defaults to None
        :type name: str, optional

        .. versionadded:: 0.0.5
        """
        super().__init__()
        self.specifiers = {}
        self.actions = []
        if specifiers is not None:
            self.specifiers = specifiers
        if actions is not None:
            self.actions = actions
        self.name = name

    def set_specifier(self, name: str, value: Any):
        """Sets a specifier for use when the script is called via run().

        :param name: The name of the specifier
        :type name: str
        :param value: The value of the specifier
        :type value: Any

        .. versionadded:: 0.0.5
        """
        self.specifiers[name] = value

    def add_action(self, action: PyXAAction):
        """Adds an existing action to the script.

        :param action: The action to add
        :type action: PyXAAction

        .. versionadded:: 0.0.5
        """
        self.actions.append(action)

    def add_call(self, method: Union[Callable[..., Any], str], args: List[Any] = None, specifier_names: List[str] = None, return_object_specifier: str = None):
        """Creates a new action and adds it to the script.

        :param method: The method that this action invokes
        :type method: Union[Callable[..., Any], str]
        :param args: The arguments to pass to the method, defaults to None
        :type args: List[Any], optional
        :param specifier_names: The specifiers to save the action's results to, defaults to None
        :type specifier_names: List[str], optional
        :param return_object_specifier: If applicable, the specifier for the object that the method is called from, defaults to None
        :type return_object_specifier: str, optional

        .. versionadded:: 0.0.5
        """
        self.actions.append(PyXAAction(method, args, specifier_names, return_object_specifier))

    def run(self, input: Union[Any, List[Any]] = None) -> Any:
        """Runs the script.

        :param input: The input(s) to pass to the script's method calls, defaults to None
        :type input: Union[Any, List[Any]], optional
        :raises ReferenceError: The script failed to run due to referencing a specifier that doesn't exist
        :return: The value returned from the final method call
        :rtype: Any

        .. versionadded:: 0.0.5
        """
        specifiers = self.specifiers

        for action in self.actions:
            method = action.method
            args = action.args
            specifier_names = action.specifier_names
            object_specifier = action.return_object_specifier

            for index, arg in enumerate(args):
                if isinstance(arg, str):
                    if "<<"+arg+">>" in specifiers:
                        args[index] = specifiers[arg]
                    elif arg == "<<input>>":
                        if isinstance(input, list):
                            args[index] = input[0]
                            input.pop(0)
                        else:
                            args[index] = input
                    else:
                        for key, value in specifiers.items():
                            if "<<"+key+">>" in arg:
                                args[index] = arg.replace("<<"+key+">>", value)
                            if "<<input>>" in arg:
                                if input is None:
                                    raise ValueError("Input expected")
                                if isinstance(input, list):
                                    args[index] = args[index].replace("<<input>>", input[0])
                                    input.pop(0)
                                else:
                                    args[index] = args[index].replace("<<input>>", input)
            result = None
            if object_specifier is not None:
                if object_specifier in specifiers:
                    result = specifiers[object_specifier].__getattribute__(method)(*args)
                else:
                    raise ReferenceError("Object specifier not found")
            else:
                result = method(*args)
        
            if len(specifier_names) > 0:
                name = specifier_names[0]
            else:
                name = "specifier" + str(len(specifiers))
            specifiers[name] = result
        return result

    def save(self, file_path: str):
        """Saves a .pyxa script file.

        If the file path does not end in .pyxa, the extension will be appended.

        :param file_path: The path to save the script at.
        :type file_path: str

        .. versionadded:: 0.0.5
        """
        self.version = VERSION
        self.date = DATE
        if not file_path.endswith(".pyxa"):
            file_path = file_path + ".pyxa"
        with open(file_path, 'w') as f:
            yaml.dump(self, f)

    def load(self, file_path: str) -> 'PyXAScript':
        """Loads a .pyxa script file into this PyXAScript object.

        If the file path does not end in .pyxa, the extension will be appended.

        :param file_path: The path to the script.
        :type file_path: str
        :return: The loaded script object
        :rtype: PyXAScript

        .. versionadded:: 0.0.5
        """
        if not file_path.endswith(".pyxa"):
            file_path = file_path + ".pyxa"
        with open(file_path, 'r') as f:
            loaded_script = yaml.load(f, Loader=yaml.Loader)
            self.__dict__.update(loaded_script.__dict__)
        if self.version != VERSION:
            print(f"Warning: Script was made with PyXA {self.version}, but the installed version is {VERSION}. Proceed with caution.")
        return self
