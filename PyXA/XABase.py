""".. versionadded:: 0.0.1

General classes and methods applicable to any PyXA object.
"""

import importlib
import logging
import math
import os
import random
import subprocess
import sys
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from enum import Enum
from pprint import pprint
from typing import Any, Callable, Iterator, Literal, Self, Union

import AppKit
import appscript
import AVFoundation
import CoreLocation
import CoreMedia
import Foundation
import LatentSemanticMapping
import NaturalLanguage
import objc
import Quartz
import requests
import ScriptingBridge
import Speech
import Vision
from bs4 import BeautifulSoup, element
from CoreLocation import CLLocation
from PyObjCTools import AppHelper
from Quartz import (CFDataRef, CGImageSourceCreateWithData, CGImageSourceRef, CGRectMake)
from ScriptingBridge import SBApplication, SBElementArray

from PyXA.apps import application_classes
from PyXA.XAErrors import InvalidPredicateError

from .XAProtocols import XACanOpenPath, XAClipboardCodable, XAPathLike


def OSType(s: str):
    return int.from_bytes(s.encode("UTF-8"), "big")

def unOSType(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()


PYXA_VERSION = "0.1.0"

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")
    
logging.basicConfig(
    filename="logs/pyxa_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)

###############
### General ###
###############
# XAObject, XAApplication
class XAObject():
    """A general class for PyXA scripting objects.

    .. seealso:: :class:`XABaseScriptable.XASBObject`

    .. versionadded:: 0.0.1
    """
    _xa_sevt = None
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
            self._xa_apsp = properties.get("appspace", None)
            self.xa_wksp = properties.get("workspace", None)
            self.xa_elem = properties.get("element", None)
            self.xa_scel = properties.get("scriptable_element", None)
            self.xa_aref = properties.get("appref", None)

        self.properties: dict #: The scriptable properties dictionary for the object

    @property
    def xa_apsp(self):
        if not isinstance(self.__xa_apsp, AppKit.NSApplication):
            self.__xa_apsp = list(self.__xa_apsp)[0]
        return self.__xa_apsp

    @property
    def xa_sevt(self):
        if XAObject._xa_sevt is None:
            XAObject._xa_sevt = SBApplication.alloc().initWithBundleIdentifier_("com.apple.systemevents")
        return XAObject._xa_sevt

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

    def _new_element(self, obj: AppKit.NSObject, obj_class: type = 'XAObject', *args: list[Any]) -> 'XAObject':
        """Wrapper for creating a new PyXA object.

        :param folder_obj: The Objective-C representation of an object.
        :type folder_obj: NSObject
        :return: The PyXA representation of the object.
        :rtype: XAObject
        
        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self._xa_apsp,
            "workspace": getattr(self, "xa_wksp", None),
            "element": obj,
            "appref": getattr(self, "xa_aref", None),
        }
        return obj_class(properties, *args)

    def _spawn_thread(self, function: Callable[..., Any], args: Union[list[Any], None] = None, kwargs: Union[list[Any], None] = None, daemon: bool = True) -> threading.Thread:
        """Spawns a new thread running the specified function.

        :param function: The function to run in the new thread
        :type function: Callable[..., Any]
        :param args: Arguments to pass to the function
        :type args: list[Any]
        :param kwargs: Keyword arguments to pass to the function
        :type kwargs: list[Any]
        :param daemon: Whether the thread should be a daemon thread, defaults to True
        :type daemon: bool, optional
        :return: The thread object
        :rtype: threading.Thread

        .. versionadded:: 0.0.9
        """
        new_thread = threading.Thread(target=function, args=args or [], kwargs=kwargs or {}, daemon=daemon)
        new_thread.start()
        return new_thread

    def has_element(self) -> bool:
        """Whether this object has an AppleScript/JXA/Objective-C scripting element associated with it.

        :return: True if this object's element attribute is set, False otherwise.
        :rtype: bool

        .. deprecated:: 0.0.9
        
           Perform this check manually instead.

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

        .. deprecated:: 0.0.9
        
           Set the element attribute directly instead.

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

    def set_scriptable_property(self, property_name: str, value: Any) -> 'XAObject':
        """Updates the value of a single scriptable element property of the scripting element associated with this object.

        :param property: The name of the property to assign a new value to.
        :type property: str
        :param value: The value to assign to the specified property.
        :type value: Any
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.1.0
        """
        parts = property_name.split("_")
        titled_parts = [part.title() for part in parts[1:]]
        property_name = parts[0] + "".join(titled_parts)
        self.xa_scel.setValue_forKey_(value, property_name)
        return self

    def __eq__(self, other: 'XAObject'):
        if other is None:
            return False

        if self.xa_elem == other.xa_elem:
            return True
        return self.xa_elem.get() == other.xa_elem.get()



class XAApplication(XAObject, XAClipboardCodable):
    """A general application class for both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XASBApplication`, :class:`XAWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAWindow
        self.__xa_prcs = None

        self.xa_apsc: appscript.GenericApp

    @property
    def xa_prcs(self):
        if self.__xa_prcs == None:
            predicate = AppKit.NSPredicate.predicateWithFormat_("displayedName == %@", self.xa_elem.localizedName())
            process = self.xa_sevt.processes().filteredArrayUsingPredicate_(predicate)[0]
        
            properties = {
                "parent": self,
                "appspace": self._xa_apsp,
                "workspace": self.xa_wksp,
                "element": process,
                "appref": self.xa_aref,
                "window_class": self.xa_wcls
            }
            self.__xa_prcs = XAProcess(properties)
        return self.__xa_prcs

    def __getattr__(self, attr):
        if attr in self.__dict__:
            # If possible, use PyXA attribute
            return super().__getattribute__(attr)
        else:
            # Otherwise, fall back to appscript
            return getattr(self.xa_apsc, attr)

    @property
    def xa_apsc(self) -> appscript.GenericApp:
        return appscript.app(self.bundle_url.path())

    @property
    def bundle_identifier(self) -> str:
        """The bundle identifier for the application.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.bundleIdentifier()

    @property
    def bundle_url(self) -> str:
        """The file URL of the application bundle.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.bundleURL()

    @property
    def executable_url(self) -> str:
        """The file URL of the application's executable.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.executableURL()

    @property
    def frontmost(self) -> bool:
        """Whether the application is the active application.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.isActive()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        if frontmost is True:
            self.xa_elem.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)

    @property
    def launch_date(self) -> datetime:
        """The date and time that the application was launched.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.launchDate()

    @property
    def localized_name(self) -> str:
        """The application's name.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.localizedName()

    @property
    def owns_menu_bar(self) -> bool:
        """Whether the application owns the top menu bar.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.ownsMenuBar()

    @property
    def process_identifier(self) -> str:
        """The process identifier for the application instance.

        .. versionadded:: 0.0.1
        """
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
        >>> safari = PyXA.Application("Safari")
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
        >>> safari = PyXA.Application("Safari")
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
        >>> safari = PyXA.Application("Safari")
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
        >>> safari = PyXA.Application("Safari")
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
        >>> safari = PyXA.Application("Safari")
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
        >>> safari = PyXA.Application("Safari")
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

    def windows(self, filter: dict = None) -> list['XAWindow']:
        return self.xa_prcs.windows(filter)

    @property
    def front_window(self) -> 'XAWindow':
        return self.xa_prcs.front_window

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_prcs.xa_elem.menuBars(), XAUIMenuBarList, filter)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL, AppKit.NSImage]]:
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
        :rtype: list[Union[str, AppKit.NSURL, AppKit.NSImage]]

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem.localizedName(), self.xa_elem.bundleURL(), self.xa_elem.icon()]




######################
### PyXA Utilities ###
######################
# SDEFParser, XAList, XAPredicate, XAURL, XAPath
class SDEFParser(XAObject):
    def __init__(self, sdef_file: Union['XAPath', str]):
        if isinstance(sdef_file, str):
            sdef_file = XAPath(sdef_file)
        self.file = sdef_file #: The full path to the SDEF file to parse

        self.app_name = ""
        self.scripting_suites = []

    def parse(self):
        app_name = self.file.path.split("/")[-1][:-5].title()
        xa_prefix = "XA" + app_name

        tree = ET.parse(self.file.path)

        suites = []

        scripting_suites = tree.findall("suite")
        for suite in scripting_suites:
            classes = []
            commands = {}

            ### Class Extensions
            class_extensions = suite.findall("class-extension")
            for extension in class_extensions:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + extension.attrib.get("extends", "").title()
                class_comment = extension.attrib.get("description", "")

                ## Class Extension Properties
                class_properties = extension.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Extension Elements
                class_elements = extension.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Extension Responds-To Commands
                class_responds_to_commands = extension.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })

            ### Classes
            scripting_classes = suite.findall("class")
            for scripting_class in scripting_classes:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + scripting_class.attrib.get("name", "").title()
                class_comment = scripting_class.attrib.get("description", "")

                ## Class Properties
                class_properties = scripting_class.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Elements
                class_elements = scripting_class.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Responds-To Commands
                class_responds_to_commands = scripting_class.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })


            ### Commands
            script_commands = suite.findall("command")
            for command in script_commands:
                command_name = command.attrib.get("name", "").lower().replace(" ", "_")
                command_comment = command.attrib.get("description", "")

                parameters = []
                direct_param = command.find("direct-parameter")
                if direct_param is not None:
                    direct_parameter_type = direct_param.attrib.get("type", "")
                    if direct_parameter_type == "specifier":
                        direct_parameter_type = "XABase.XAObject"

                    direct_parameter_comment = direct_param.attrib.get("description")

                    parameters.append({
                        "name": "direct_param",
                        "type": direct_parameter_type,
                        "comment": direct_parameter_comment
                    })

                if not "_" in command_name and len(parameters) > 0:
                    command_name += "_"

                command_parameters = command.findall("parameter")
                for parameter in command_parameters:
                    parameter_type = parameter.attrib.get("type", "")
                    if parameter_type == "specifier":
                        parameter_type = "XAObject"

                    parameter_name = parameter.attrib.get("name", "").lower().replace(" ", "_")
                    parameter_comment = parameter.attrib.get("description", "")

                    parameters.append({
                        "name": parameter_name,
                        "type": parameter_type,
                        "comment": parameter_comment,
                    })

                commands[command_name] = {
                    "name": command_name,
                    "comment": command_comment,
                    "parameters": parameters
                }

            suites.append({
                "classes": classes,
                "commands": commands
            })

        self.scripting_suites = suites
        return suites

    def export(self, output_file: Union['XAPath', str]):
        if isinstance(output_file, XAPath):
            output_file = output_file.path

        lines = []

        lines.append("from typing import Any, Callable, Union")
        lines.append("\nfrom PyXA import XABase")
        lines.append("from PyXA.XABase import OSType")
        lines.append("from PyXA import XABaseScriptable")

        for suite in self.scripting_suites:
            for scripting_class in suite["classes"]:
                lines.append("\n\n")
                lines.append("class " + scripting_class["name"].replace(" ", "") + "List:")
                lines.append("\t\"\"\"A wrapper around lists of " + scripting_class["name"].lower() + "s that employs fast enumeration techniques.")
                lines.append("\n\tAll properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.")
                lines.append("\n\t.. versionadded:: " + PYXA_VERSION)
                lines.append("\t\"\"\"")

                lines.append("\tdef __init__(self, properties: dict, filter: Union[dict, None] = None):")
                lines.append("\t\tsuper().__init__(properties, " + scripting_class["name"].replace(" ", "") + ", filter)")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef " + property["name"] + "(self) -> list['" + property["type"].replace(" ", "") + "']:")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + PYXA_VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn list(self.xa_elem.arrayByApplyingSelector_(\"" + property["name"] + "\"))")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef by_" + property["name"] + "(self, " + property["name"] + ") -> '" + scripting_class["name"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Retrieves the " + scripting_class["comment"] + "whose " + property["name"] + " matches the given " + property["name"] + ".\n\n\t\t.. versionadded:: " + PYXA_VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.by_property(\"" + property["name"] + "\", " + property["name"] + ")")


                lines.append("")
                lines.append("class " + scripting_class["name"].replace(" ", "") + ":")
                lines.append("\t\"\"\"" + scripting_class["comment"] + "\n\n\t.. versionadded:: " + PYXA_VERSION + "\n\t\"\"\"")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\t@property")
                    lines.append("\tdef " + property["name"] + "(self) -> '" + property["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + PYXA_VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.xa_elem." + property["name"] + "()")

                for element in scripting_class["elements"]:
                    lines.append("")
                    lines.append("\tdef " + element["name"].replace(" ", "") + "(self, filter: Union[dict, None] = None) -> '" + element["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Returns a list of " + element["name"] + ", as PyXA objects, matching the given filter.")
                    lines.append("\n\t\t.. versionadded:: " + PYXA_VERSION)
                    lines.append("\t\t\"\"\"")
                    lines.append("\t\tself._new_element(self.xa_elem." + element["name"] + "(), " + element["type"].replace(" ", "") + "List, filter)")

                for command in scripting_class["responds-to"]:
                    if command in suite["commands"]:
                        lines.append("")
                        command_str = "\tdef " + suite["commands"][command]["name"] + "(self, "

                        for parameter in suite["commands"][command]["parameters"]:
                            command_str += parameter["name"] + ": '" + parameter["type"] + "', "

                        command_str = command_str[:-2] + "):"
                        lines.append(command_str)

                        lines.append("\t\t\"\"\"" + suite["commands"][command]["comment"])
                        lines.append("\n\t\t.. versionadded:: " + PYXA_VERSION)
                        lines.append("\t\t\"\"\"")

                        cmd_call_str = "self.xa_elem." + suite["commands"][command]["name"] + "("

                        if len(suite["commands"][command]["parameters"]) > 0:
                            for parameter in suite["commands"][command]["parameters"]:
                                cmd_call_str += parameter["name"] + ", "
                            
                            cmd_call_str = cmd_call_str[:-2] + ")"
                        else:
                            cmd_call_str += ")"

                        lines.append("\t\t" + cmd_call_str)

        data = "\n".join(lines)
        with open(output_file, "w") as f:
            f.write(data)

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

        if not isinstance(self.xa_elem, AppKit.NSArray):
            self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(self.xa_elem)

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
        >>> app = PyXA.Application("Photos")
        >>> photo = app.media_items().by_property("id", "CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001")
        >>> print(photo)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001>

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        # if hasattr(ls, "get"):
        #     ls = predicate.evaluate(self.xa_elem).get()

        if len(ls) == 0:
            return None

        obj = ls[0]
        return self._new_element(obj, self.xa_ocls)

    def equalling(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value equals the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("TV")
        >>> print(app.tracks().equalling("playedCount", 0))
        <<class 'PyXA.apps.TV.XATVTrackList'>['Frozen', 'Sunshine', 'The Hunger Games: Mockingjay - Part 2', ...]>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def not_equalling(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value does not equal the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("TV")
        >>> print(app.tracks().not_equalling("playedCount", 0))
        <<class 'PyXA.apps.TV.XATVTrackList'>['The Avatar State', 'The Cave of Two Lovers', 'Return to Omashu', ...]>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_neq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def containing(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value contains the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Reminders")
        >>> print(app.reminders().containing("name", "PyXA"))
        <<class 'PyXA.apps.Reminders.XARemindersReminderList'>['PyXA v0.1.0 release']>

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_contains_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def not_containing(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value does not contain the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Reminders")
        >>> print(app.reminders().not_containing("name", " "))
        <<class 'PyXA.apps.Reminders.XARemindersReminderList'>['Trash', 'Thing', 'Reminder', ...]>

        .. versionadded:: 0.1.0
        """
        ls = XAPredicate.evaluate_with_format(self.xa_elem, f"NOT {property} CONTAINS \"{value}\"")
        return self._new_element(ls, self.__class__)

    def beginning_with(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value begins with the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("System Events")
        >>> print(app.downloads_folder.files().beginning_with("name", "Example"))
        <<class 'PyXA.apps.SystemEvents.XASystemEventsFileList'>['Example.png', 'ExampleImage.png', ...]>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_begins_with_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def ending_with(self, property: str, value: str) -> XAObject:
        """Retrieves all elements whose property value ends with the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("System Events")
        >>> print(app.downloads_folder.files().ending_with("name", ".png"))
        <<class 'PyXA.apps.SystemEvents.XASystemEventsFileList'>['Example.png', 'Image.png', ...]>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_ends_with_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def greater_than(self, property: str, value: Union[int, float]) -> XAObject:
        """Retrieves all elements whose property value is greater than the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to compare against
        :type value: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> print(app.media_items().greater_than("altitude", 10000)[0].spotlight())
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=53B0F28E-0B39-446B-896C-484CD0DC2D3C/L0/001>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_gt_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def less_than(self, property: str, value: Union[int, float]) -> XAObject:
        """Retrieves all elements whose property value is less than the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to compare against
        :type value: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> app = PyXA.Application("Music")
        >>> tracks = app.tracks()
        >>> print(tracks.less_than("playedCount", 5).name())
        ['Outrunning Karma', 'Death of a Hero', '1994', 'Mind Is a Prison']

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_lt_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def between(self, property: str, value1: Union[int, float], value2: Union[int, float]) -> XAObject:
        """Retrieves all elements whose property value is between the given values.

        :param property: The property to match
        :type property: str
        :param value1: The lower-end of the range to match
        :type value1: Union[int, float]
        :param value2: The upper-end of the range to match
        :type value2: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> from datetime import datetime, timedelta
        >>> 
        >>> app = PyXA.Application("Calendar")
        >>> events = app.calendars()[3].events()
        >>> now = datetime.now()
        >>> print(events.between("startDate", now, now + timedelta(days=1)))
        <<class 'PyXA.apps.Calendar.XACalendarEventList'>['Capstone Meeting', 'Lunch with Dan']>

        .. versionadded:: 0.1.0
        """
        predicate = XAPredicate()
        predicate.add_gt_condition(property, value1)
        predicate.add_lt_condition(property, value2)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

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
        >>> app = PyXA.Application("Messages")
        >>> last_file_transfer = app.file_transfers().filter("direction", "==", app.MessageDirection.OUTGOING)[-1]
        >>> print(last_file_transfer)
        <<class 'PyXA.apps.Messages.XAMessagesFileTransfer'>Test.jpg>

        :Example 2: Get the list of favorite photos/videos from Photos.app

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> favorites = app.media_items().filter("favorite", "==", True)
        >>> print(favorites)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItemList'>['CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001', 'EFEB7F37-8373-4972-8E43-21612F597185/L0/001', ...]>

        .. note::
        
           For properties that appear to be boolean but fail to return expected filter results, try using the corresponding 0 or 1 value instead.

        :Example 3: Provide a custom format string

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
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
            return super()._new_element(filtered_list, self.__class__)
        else:
            filtered_list = XAPredicate.evaluate_with_format(self.xa_elem, filter)
            return super()._new_element(filtered_list, self.__class__)

    def at(self, index: int) -> XAObject:
        """Retrieves the element at the specified index.

        :param index: The index of the desired element
        :type index: int
        :return: The PyXA-wrapped element object
        :rtype: XAObject

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem[index], self.xa_ocls)

    @property
    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.firstObject(), self.xa_ocls)

    @property
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
        try:
            self.xa_elem = self.xa_elem.shuffledArray()
        except AttributeError:
            random.shuffle(self.xa_elem)
        return self

    def push(self, *elements: list[XAObject]) -> Union[XAObject, list[XAObject], None]:
        """Appends the object referenced by the provided PyXA wrapper to the end of the list.

        .. versionadded:: 0.0.3
        """
        objects = []
        for element in elements:
            len_before = len(self.xa_elem)
            self.xa_elem.addObject_(element.xa_elem)

            if len(self.xa_elem) == len_before:
                # Object wasn't added -- try force-getting the list before adding
                self.xa_elem.get().addObject_(element.xa_elem)

            if len(self.xa_elem) > len_before:
                objects.append(self[len(self.xa_elem) - 1])
        
        if len(objects) == 1:
            return objects[0]

        if len(objects) == 0:
            return None

        return objects

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

    def count(self, count_function: Callable[[object], bool]):
        count = 0
        for index in range(len(self)):
            in_count = False
            try:
                in_count = count_function(self.xa_elem[index])
            except:
                # TODO: Add logging message here
                pass

            if not in_count:
                try:
                    in_count = count_function(self[index])
                except:
                    pass
            
            if in_count:
                count += 1
        return count

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            arr = AppKit.NSMutableArray.alloc().initWithArray_([self.xa_elem[index] for index in range(key.start, key.stop, key.step or 1)])
            return self._new_element(arr, self.__class__)
        if key < 0:
            key = self.xa_elem.count() + key
        return self._new_element(self.xa_elem.objectAtIndex_(key), self.xa_ocls)

    def __len__(self):
        return len(self.xa_elem)

    def __reversed__(self):
        self.xa_elem = self.xa_elem.reverseObjectEnumerator().allObjects()
        return self

    def __iter__(self):
        return (self._new_element(object, self.xa_ocls) for object in self.xa_elem.objectEnumerator())

    def __contains__(self, item):
        if isinstance(item, XAObject):
            item = item.xa_elem
        return item in self.xa_elem

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPredicate(XAObject, XAClipboardCodable):
    """A predicate used to filter arrays.

    .. versionadded:: 0.0.4
    """
    def __init__(self):
        self.keys: list[str] = []
        self.operators: list[str] = []
        self.values: list[str] = []

    def from_dict(self, ref_dict: dict) -> 'XAPredicate':
        """Populates the XAPredicate object from the supplied dictionary.

        The predicate will use == for all comparisons.

        :param ref_dict: A specification of key, value pairs
        :type ref_dict: dict
        :return: The populated predicate object
        :rtype: XAPredicate

        .. versionadded:: 0.0.4
        """
        for key, value in ref_dict.items():
            self.keys.append(key)
            self.operators.append("==")
            self.values.append(value)
        return self

    def from_args(self, *args) -> 'XAPredicate':
        """Populates the XAPredicate object from the supplied key, value argument pairs.

        The number of keys and values must be equal. The predicate will use == for all comparisons.

        :raises InvalidPredicateError: Raised when the number of keys does not match the number of values
        :return: The populated predicate object
        :rtype: XAPredicate

        .. versionadded:: 0.0.4
        """
        arg_num = len(args)
        if arg_num % 2 != 0:
            raise InvalidPredicateError("The number of keys and values must be equal; the number of arguments must be an even number.")
        
        for index, value in enumerate(args):
            if index % 2 == 0:
                self.keys.append(value)
                self.operators.append("==")
                self.values.append(args[index + 1])
        return self

    def evaluate(self, target: Union[AppKit.NSArray, XAList]) -> AppKit.NSArray:
        """Evaluates the predicate on the given array.

        :param target: The array to evaluate against the predicate
        :type target: AppKit.NSArray
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        placeholders = ["%@"] * len(self.values)
        expressions = [" ".join(expr) for expr in zip(self.keys, self.operators, placeholders)]
        format = "( " + " ) && ( ".join(expressions) + " )"

        predicate = AppKit.NSPredicate.predicateWithFormat_(format, *self.values)
        ls = target_list.filteredArrayUsingPredicate_(predicate)

        if len(ls) == 0:
            try:
                # Not sure why this is necessary sometimes, but it is.
                predicate = str(predicate)
                ls = target_list.filteredArrayUsingPredicate_(AppKit.NSPredicate.predicateWithFormat_(predicate))
            except ValueError:
                pass

        if isinstance(target, XAList):
            return target.__class__({
                "parent": target,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": ls,
                "appref": self.xa_aref,
            })
        return ls

    def evaluate_with_format(target: Union[AppKit.NSArray, XAList], fmt: str) -> AppKit.NSArray:
        """Evaluates the specified array against a predicate with the given format.

        :param target: The array to filter
        :type target: AppKit.NSArray
        :param fmt: The format string for the predicate
        :type fmt: str
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        predicate = AppKit.NSPredicate.predicateWithFormat_(fmt)
        ls = target_list.filteredArrayUsingPredicate_(predicate)

        if isinstance(target, XAList):
            return target.__class__({
                "parent": target,
                "appspace": AppKit.NSApplication.sharedApplication(),
                "workspace": AppKit.NSWorkspace.sharedWorkspace(),
                "element": ls,
                "appref": AppKit.NSApplication.sharedApplication(),
            })
        return ls

    def evaluate_with_dict(target: Union[AppKit.NSArray, XAList], properties_dict: dict) -> AppKit.NSArray:
        """Evaluates the specified array against a predicate constructed from the supplied dictionary.

        The predicate will use == for all comparisons.

        :param target: The array to filter
        :type target: AppKit.NSArray
        :param properties_dict: The specification of key, value pairs
        :type properties_dict: dict
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        fmt = ""
        for key, value in properties_dict.items():
            if isinstance(value, str):
                value = "'" + value + "'"
            fmt += f"( {key} == {value} ) &&"

        predicate = AppKit.NSPredicate.predicateWithFormat_(fmt[:-3])
        ls = target_list.filteredArrayUsingPredicate_(predicate)

        if isinstance(target, XAList):
            return target.__class__({
                "parent": target,
                "appspace": AppKit.NSApplication.sharedApplication(),
                "workspace": AppKit.NSWorkspace.sharedWorkspace(),
                "element": ls,
                "appref": AppKit.NSApplication.sharedApplication(),
            })
        return ls

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
    def add_between_condition(self, property: str, value1: Union[int, float], value2: Union[int, float]):
        """Appends a `BETWEEN` condition to the end of the predicate format.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value1: The lower target value of the condition
        :type value1: Union[int, float]
        :param value2: The upper target value of the condition
        :type value2: Union[int, float]

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("BETWEEN")
        self.values.append([value1, value2])

    def insert_between_condition(self, index: int, property: str, value1: Union[int, float], value2: Union[int, float]):
        """Inserts a `BETWEEN` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value1: The lower target value of the condition
        :type value1: Union[int, float]
        :param value2: The upper target value of the condition
        :type valu2e: Union[int, float]

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




class XAURL(XAObject, XAClipboardCodable):
    """A URL using any scheme recognized by the system. This can be a file URL.

    .. versionadded:: 0.0.5
    """
    def __init__(self, url: Union[str, AppKit.NSURL, 'XAURL', 'XAPath']):
        super().__init__()
        self.parameters: str #: The query parameters of the URL
        self.scheme: str #: The URI scheme of the URL
        self.fragment: str #: The fragment identifier following a # symbol in the URL
        self.port: int #: The port that the URL points to
        self.html: element.tag #: The html of the URL
        self.title: str #: The title of the URL
        self.soup: BeautifulSoup = None #: The bs4 object for the URL, starts as None until a bs4-related action is made
        self.url: str #: The string form of the URL

        if isinstance(url, str):
            logging.debug("Initializing XAURL from string")
            # URL-encode spaces
            url = url.replace(" ", "%20")

            if url.startswith("/"):
                # Prepend file scheme
                url = "file://" + url
            elif url.replace(".", "").isdecimal():
                # URL is an IP -- must add http:// prefix
                if ":" not in url:
                    # No port provided, add port 80 by default
                    url = "http://" + url + ":80"
                else:
                    url = "http://" + url
            elif "://" not in url:
                # URL is not currently valid, try prepending http://
                url = "http://" + url
            
            self.url = url
            url = AppKit.NSURL.alloc().initWithString_(url)
        elif isinstance(url, XAURL) or isinstance(url, XAPath):
            logging.debug("Initializing XAURL from XAURL/XAPath")
            self.url = url.url
            url = url.xa_elem

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
        """Opens the URL in the appropriate default application.

        .. versionadded:: 0.0.5
        """
        AppKit.NSWorkspace.sharedWorkspace().openURL_(self.xa_elem)

    def extract_text(self) -> list[str]:
        """Extracts the visible text from the webpage that the URL points to.

        :return: The list of extracted lines of text
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        if self.soup is None:
            self.__get_soup()
        return self.soup.get_text().splitlines()

    def extract_images(self) -> list['XAImage']:
        """Extracts all images from HTML of the webpage that the URL points to.

        :return: The list of extracted images
        :rtype: list[XAImage]

        .. versionadded:: 0.0.8
        """
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

    def get_clipboard_representation(self) -> list[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the URL.

        When the clipboard content is set to a URL, the raw URL data and the string representation of the URL are added to the clipboard.

        :return: The clipboard-codable form of the URL
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, str(self.xa_elem)]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPath(XAObject, XAClipboardCodable):
    """A path to a file on the disk.

    .. versionadded:: 0.0.5
    """
    def __init__(self, path: Union[str, AppKit.NSURL]):
        super().__init__()
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_elem = path
        self.path = path.path() #: The path string without the file:// prefix
        self.url = str(self.xa_elem) #: The path string with the file:// prefix included
        self.xa_wksp = AppKit.NSWorkspace.sharedWorkspace()

    def open(self):
        """Opens the file in its default application.

        .. versionadded: 0.0.5
        """
        self.xa_wksp.openURL_(self.xa_elem)

    def show_in_finder(self):
        """Opens a Finder window showing the folder containing this path, with the associated file selected. Synonymous with :func:`select`.

        .. versionadded: 0.0.9
        """
        self.select()

    def select(self):
        """Opens a Finder window showing the folder containing this path, with the associated file selected. Synonymous with :func:`show_in_finder`.

        .. versionadded: 0.0.5
        """
        self.xa_wksp.activateFileViewerSelectingURLs_([self.xa_elem])

    def get_clipboard_representation(self) -> list[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the path.

        When the clipboard content is set to a path, the raw file URL data and the string representation of the path are added to the clipboard.

        :return: The clipboard-codable form of the path
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.xa_elem.path()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"




########################
### Interoperability ###
########################
# AppleScript
class AppleScript(XAObject):
    """A class for constructing and executing AppleScript scripts.

    .. versionadded:: 0.0.5
    """
    def __init__(self, script: Union[str, list[str], None] = None):
        """Creates a new AppleScript object.

        :param script: A string or list of strings representing lines of AppleScript code, or the path to a script plaintext file, defaults to None
        :type script: Union[str, list[str], None], optional

        .. versionadded:: 0.0.5
        """
        self.script: list[str] #: The lines of AppleScript code contained in the script
        self.last_result: Any #: The return value of the last execution of the script
        self.file_path: XAPath #: The file path of this script, if one exists

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

    @property
    def last_result(self) -> Any:
        return self.__last_result

    @property
    def file_path(self) -> 'XAPath':
        return self.__file_path

    def add(self, script: Union[str, list[str], 'AppleScript']):
        """Adds the supplied string, list of strings, or script as a new line entry in the script.

        :param script: The script to append to the current script string.
        :type script: Union[str, list[str], AppleScript]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript("tell application \"Safari\"")
        >>> script.add("print the document of window 1")
        >>> script.add("end tell")
        >>> script.run()

        .. versionadded:: 0.0.5
        """
        if isinstance(script, str):
            self.script.append(script)
        elif isinstance(script, list):
            self.script.extend(script)
        elif isinstance(script, AppleScript):
            self.script.extend(script.script)

    def insert(self, index: int, script: Union[str, list[str], 'AppleScript']):
        """Inserts the supplied string, list of strings, or script as a line entry in the script starting at the given line index.

        :param index: The line index to begin insertion at
        :type index: int
        :param script: The script to insert into the current script
        :type script: Union[str, list[str], AppleScript]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> script.insert(1, "activate")
        >>> script.run()

        .. versionadded:: 0.0.9
        """
        if isinstance(script, str):
            self.script.insert(index, script)
        elif isinstance(script, list):
            for line in script:
                self.script.insert(index, line)
                index += 1
        elif isinstance(script, AppleScript):
            for line in script.script:
                self.script.insert(index, line)
                index += 1

    def pop(self, index: int = -1) -> str:
        """Removes the line at the given index from the script.

        :param index: The index of the line to remove
        :type index: int
        :return: The text of the removed line
        :rtype: str

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.pop(1))
            get chats

        .. versionadded:: 0.0.9
        """
        return self.script.pop(index)

    def load(path: Union['XAPath', str]) -> 'AppleScript':
        """Loads an AppleScript (.scpt) file as a runnable AppleScript object.

        :param path: The path of the .scpt file to load
        :type path: Union[XAPath, str]
        :return: The newly loaded AppleScript object
        :rtype: AppleScript

        :Example 1: Load and run a script

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.run())
        {
            'string': None,
            'int': 0, 
            'bool': False,
            'float': 0.0,
            'date': None,
            'file_url': None,
            'type_code': 845507684,
            'data': {length = 8962, bytes = 0x646c6532 00000000 6c697374 000022f2 ... 6e756c6c 00000000 },
            'event': <NSAppleEventDescriptor: [ 'obj '{ ... } ]>
        }

        :Example 2: Load, modify, and run a script

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> script.pop(1)
        >>> script.insert(1, "activate")
        >>> script.run()

        .. versionadded:: 0.0.8
        """
        if isinstance(path, str):
            path = XAPath(path)
        script = AppKit.NSAppleScript.alloc().initWithContentsOfURL_error_(path.xa_elem, None)[0]

        attributed_string = script.richTextSource()
        attributed_string = str(attributed_string).split("}")
        parts = []
        for x in attributed_string:
            parts.extend(x.split("{"))

        for x in parts:
            if "=" in x:
                parts.remove(x)

        script = AppleScript("".join(parts).split("\n"))
        script.__file_path = path
        return script

    def save(self, path: Union['XAPath', str, None] = None):
        """Saves the script to the specified file path, or to the path from which the script was loaded.

        :param path: The path to save the script at, defaults to None
        :type path: Union[XAPath, str, None], optional

        :Example 1: Save the script to a specified path

        >>> import PyXA
        >>> script = PyXA.AppleScript(f\"\"\"
        >>>     tell application "Safari"
        >>>         activate
        >>>     end tell
        >>> \"\"\")
        >>> script.save("/Users/exampleUser/Downloads/Example.scpt")

        :Example 2: Load a script, modify it, then save it

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/steven/Downloads/Example.scpt")
        >>> script.insert(2, "delay 2")
        >>> script.insert(3, "set the miniaturized of window 1 to true")
        >>> script.save()

        .. versionadded:: 0.0.9
        """
        if path is None and self.file_path is None:
            print("No path to save script to!")
            return
        
        if isinstance(path, str):
            path = XAPath(path)

        script = ""
        for line in self.script:
            script += line + "\n"
        script = AppKit.NSAppleScript.alloc().initWithSource_(script)
        script.compileAndReturnError_(None)
        source = (script.richTextSource().string())

        if path is not None:
            self.__file_path = path

        with open(self.file_path.xa_elem.path(), "w") as f:
            f.write(source)

    def parse_result_data(result: dict) -> list[tuple[str, str]]:
        """Extracts string data from an AppleScript execution result dictionary.

        :param result: The execution result dictionary to extract data from
        :type result: dict
        :return: A list of responses contained in the result structured as tuples
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.script)
        >>> result = script.run()
        >>> print(PyXA.AppleScript.parse_result_data(result))
        ['tell application "Messages"', '\\tget chats', 'end tell']
        [('ID', 'iMessage;-;+12345678910'), ('ID', 'iMessage;-;+12345678911'), ('ID', 'iMessage;-;example@icloud.com'), ...]

        .. versionadded:: 0.0.9
        """
        result = result["event"]
        response_objects = []
        num_responses = result.numberOfItems()
        for response_index in range(1, num_responses + 1):
            response = result.descriptorAtIndex_(response_index)

            data = ()
            num_params = response.numberOfItems()
            if num_params == 0:
                data = response.stringValue().strip()

            else:
                for param_index in range(1, num_params + 1):
                    param = response.descriptorAtIndex_(param_index).stringValue()
                    if param is not None:
                        data += (param.strip(), )
            response_objects.append(data)

        return response_objects

    def run(self) -> Any:
        """Compiles and runs the script, returning the result.

        :return: The return value of the script.
        :rtype: Any

        :Example:

        import PyXA
        script = PyXA.AppleScript(f\"\"\"tell application "System Events"
            return 1 + 2
        end tell
        \"\"\")
        print(script.run())
        {
            'string': '3',
            'int': 3,
            'bool': False,
            'float': 3.0,
            'date': None,
            'file_url': None,
            'type_code': 3,
            'data': {length = 4, bytes = 0x03000000},
            'event': <NSAppleEventDescriptor: 3>
        }
        
        .. versionadded:: 0.0.5
        """
        script = ""
        for line in self.script:
            script += line + "\n"
        script = AppKit.NSAppleScript.alloc().initWithSource_(script)
        
        result = script.executeAndReturnError_(None)[0]
        if result is not None:
            self.__last_result = {
                "string": result.stringValue(),
                "int": result.int32Value(),
                "bool": result.booleanValue(),
                "float": result.doubleValue(),
                "date": result.dateValue(),
                "file_url": result.fileURLValue(),
                "type_code": result.typeCodeValue(),
                "data": result.data(),
                "event": result,
            }
            return self.last_result

    def __repr__(self):
        return "<" + str(type(self)) + str(self.script) + ">"




########################
### System Utilities ###
########################
# XAClipboard, XANotification, XAProcess, XACommandDetector, XASpeechRecognizer, XASpeech, XASpotlight
class XAClipboard(XAObject):
    """A wrapper class for managing and interacting with the system clipboard.

    .. versionadded:: 0.0.5
    """
    def __init__(self):
        self.xa_elem = AppKit.NSPasteboard.generalPasteboard()
        self.content #: The content of the clipboard

    @property
    def content(self) -> dict[str, list[Any]]:
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
    def content(self, value: list[Any]):
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

    def get_strings(self) -> list[str]:
        """Retrieves string type data from the clipboard, if any such data exists.

        :return: The list of strings currently copied to the clipboard
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        items = []
        for item in self.xa_elem.pasteboardItems():
            string = item.stringForType_(AppKit.NSPasteboardTypeString)
            if string is not None:
                items.append(string)
        return items

    def get_urls(self) -> list['XAURL']:
        """Retrieves URL type data from the clipboard, as instances of :class:`XAURL` and :class:`XAPath`, if any such data exists.

        :return: The list of file URLs and web URLs currently copied to the clipboard
        :rtype: list[XAURL]

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

    def get_images(self) -> list['XAImage']:
        """Retrieves image type data from the clipboard, as instances of :class:`XAImage`, if any such data exists.

        :return: The list of images currently copied to the clipboard
        :rtype: list[XAImage]

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

    def set_contents(self, content: list[Any]):
        """Sets the content of the clipboard

        :param content: A list of the content to add fill the clipboard with.
        :type content: list[Any]

        .. deprecated:: 0.0.8
           Set the :ivar:`content` property directly instead.
        
        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()
        self.xa_elem.writeObjects_(content)




class XANotification(XAObject):
    """A class for managing and interacting with notifications.

    .. versionadded:: 0.0.9
    """
    def __init__(self, text: str, title: Union[str, None] = None, subtitle: Union[str, None] = None, sound_name: Union[str, None] = None):
        """Initializes a notification object.

        :param text: The main text of the notification
        :type text: str
        :param title: The title of the notification, defaults to None
        :type title: Union[str, None], optional
        :param subtitle: The subtitle of the notification, defaults to None
        :type subtitle: Union[str, None], optional
        :param sound_name: The sound to play when the notification is displayed, defaults to None
        :type sound_name: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.text = text
        self.title = title
        self.subtitle = subtitle
        self.sound_name = sound_name

    def display(self):
        """Displays the notification.

        .. todo::
        
           Currently uses :func:`subprocess.Popen`. Should use UserNotifications in the future.

        .. versionadded:: 0.0.9
        """
        script = AppleScript()
        script.add(f"display notification \\\"{self.text}\\\"")

        if self.title is not None:
            script.add(f"with title \\\"{self.title}\\\"")
        
        if self.subtitle is not None:
            script.add(f"subtitle \\\"{self.subtitle}\\\"")

        if self.sound_name is not None:
            script.add(f"sound name \\\"{self.sound_name}\\\"")

        cmd = "osascript -e \"" + " ".join(script.script) + "\""
        subprocess.Popen([cmd], shell=True)




class XAProcess(XAObject):
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = properties["window_class"]

        self.front_window: XAWindow #: The front window of the application process

    @property
    def front_window(self) -> 'XAWindow':
        return self._new_element(self.xa_elem.windows()[0], XAWindow)

    def windows(self, filter: dict = None) -> 'XAWindowList':
        return self._new_element(self.xa_elem.windows(), XAWindowList, filter)

    def menu_bars(self, filter: dict = None) -> 'XAUIMenuBarList':
        return self._new_element(self.xa_elem.menuBars(), XAUIMenuBarList, filter)




class XACommandDetector(XAObject):
    """A command-based query detector.

    .. versionadded:: 0.0.9
    """
    def __init__(self, command_function_map: Union[dict[str, Callable[[], Any]], None] = None):
        """Creates a command detector object.

        :param command_function_map: A dictionary mapping command strings to function objects
        :type command_function_map: dict[str, Callable[[], Any]]

        .. versionadded:: 0.0.9
        """
        self.command_function_map = command_function_map or {} #: The dictionary of commands and corresponding functions to run upon detection

    def on_detect(self, command: str, function: Callable[[], Any]):
        """Adds or replaces a command to listen for upon calling :func:`listen`, and associates the given function with that command.

        :param command: The command to listen for
        :type command: str
        :param function: The function to call when the command is heard
        :type function: Callable[[], Any]

        :Example:

        >>> detector = PyXA.XACommandDetector()
        >>> detector.on_detect("go to google", PyXA.XAURL("http://google.com").open)
        >>> detector.listen()

        .. versionadded:: 0.0.9
        """
        self.command_function_map[command] = function

    def listen(self) -> Any:
        """Begins listening for the specified commands.

        :return: The execution return value of the corresponding command function
        :rtype: Any

        :Example:

        >>> import PyXA
        >>> PyXA.speak("What app do you want to open?")
        >>> PyXA.XACommandDetector({
        >>>     "safari": PyXA.Application("Safari").activate,
        >>>     "messages": PyXA.Application("Messages").activate,
        >>>     "shortcuts": PyXA.Application("Shortcuts").activate,
        >>>     "mail": PyXA.Application("Mail").activate,
        >>>     "calendar": PyXA.Application("Calendar").activate,
        >>>     "notes": PyXA.Application("Notes").activate,
        >>>     "music": PyXA.Application("Music").activate,
        >>>     "tv": PyXA.Application("TV").activate,
        >>>     "pages": PyXA.Application("Pages").activate,
        >>>     "numbers": PyXA.Application("Numbers").activate,
        >>>     "keynote": PyXA.Application("Keynote").activate,
        >>> }).listen()

        .. versionadded:: 0.0.9
        """
        command_function_map = self.command_function_map
        return_value = None
        class NSSpeechRecognizerDelegate(AppKit.NSObject):
            def speechRecognizer_didRecognizeCommand_(self, recognizer, cmd):
                return_value = command_function_map[cmd]()
                AppHelper.stopEventLoop()

        recognizer = AppKit.NSSpeechRecognizer.alloc().init()
        recognizer.setCommands_(list(command_function_map.keys()))
        recognizer.setBlocksOtherRecognizers_(True)
        recognizer.setDelegate_(NSSpeechRecognizerDelegate.alloc().init().retain())
        recognizer.startListening()
        AppHelper.runConsoleEventLoop()

        return return_value




class XASpeechRecognizer(XAObject):
    """A rule-based query detector.

    .. versionadded:: 0.0.9
    """
    def __init__(self, finish_conditions: Union[None, dict[Callable[[str], bool], Callable[[str], bool]]] = None):
        """Creates a speech recognizer object.

        By default, with no other rules specified, the Speech Recognizer will timeout after 10 seconds once :func:`listen` is called.

        :param finish_conditions: A dictionary of rules and associated methods to call when a rule evaluates to true, defaults to None
        :type finish_conditions: Union[None, dict[Callable[[str], bool], Callable[[str], bool]]], optional

        .. versionadded:: 0.0.9
        """
        default_conditions = {
            lambda x: self.time_elapsed > timedelta(seconds = 10): lambda x: self.spoken_query,
        }
        self.finish_conditions: Callable[[str], bool] = finish_conditions or default_conditions #: A dictionary of rules and associated methods to call when a rule evaluates to true
        self.spoken_query: str = "" #: The recognized spoken input
        self.start_time: datetime #: The time that the Speech Recognizer begins listening
        self.time_elapsed: timedelta #: The amount of time passed since the start time

    def __prepare(self):
        # Request microphone access if we don't already have it
        Speech.SFSpeechRecognizer.requestAuthorization_(None)

        # Set up audio session
        self.audio_session = AVFoundation.AVAudioSession.sharedInstance()
        self.audio_session.setCategory_mode_options_error_(AVFoundation.AVAudioSessionCategoryRecord, AVFoundation.AVAudioSessionModeMeasurement, AVFoundation.AVAudioSessionCategoryOptionDuckOthers, None)
        self.audio_session.setActive_withOptions_error_(True, AVFoundation.AVAudioSessionSetActiveOptionNotifyOthersOnDeactivation, None)

        # Set up recognition request
        self.recognizer = Speech.SFSpeechRecognizer.alloc().init()
        self.recognition_request = Speech.SFSpeechAudioBufferRecognitionRequest.alloc().init()
        self.recognition_request.setShouldReportPartialResults_(True)

        # Set up audio engine
        self.audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self.input_node = self.audio_engine.inputNode()
        recording_format = self.input_node.outputFormatForBus_(0)
        self.input_node.installTapOnBus_bufferSize_format_block_(0, 1024, recording_format,
            lambda buffer, _when: self.recognition_request.appendAudioPCMBuffer_(buffer))
        self.audio_engine.prepare()
        self.audio_engine.startAndReturnError_(None)

    def on_detect(self, rule: Callable[[str], bool], method: Callable[[str], bool]):
        """Sets the given rule to call the specified method if a spoken query passes the rule.

        :param rule: A function that takes the spoken query as a parameter and returns a boolean value depending on whether the query passes a desired rule
        :type rule: Callable[[str], bool]
        :param method: A function that takes the spoken query as a parameter and acts on it
        :type method: Callable[[str], bool]

        .. versionadded:: 0.0.9
        """
        self.finish_conditions[rule] = method

    def listen(self) -> Any:
        """Begins listening for a query until a rule returns True.

        :return: The value returned by the method invoked upon matching some rule
        :rtype: Any

        .. versionadded:: 0.0.9
        """
        self.start_time = datetime.now()
        self.time_elapsed = None
        self.__prepare()

        old_self = self
        def detect_speech(transcription, error):
            if error is not None:
                print("Failed to detect speech. Error: ", error)
            else:
                old_self.spoken_query = transcription.bestTranscription().formattedString()
                print(old_self.spoken_query)

        recognition_task = self.recognizer.recognitionTaskWithRequest_resultHandler_(self.recognition_request, detect_speech)
        while self.spoken_query == "" or not any(x(self.spoken_query) for x in self.finish_conditions):
            self.time_elapsed = datetime.now() - self.start_time
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.5))

        self.audio_engine.stop()
        for rule, method in self.finish_conditions.items():
            if rule(self.spoken_query):
                return method(self.spoken_query)




class XASpeech(XAObject):
    def __init__(self, message: str = "", voice: Union[str, None] = None, volume: float = 0.5, rate: int = 200):
        self.message: str = message #: The message to speak
        self.voice: Union[str, None] = voice #: The voice that the message is spoken in
        self.volume: float = volume #: The speaking volume
        self.rate: int = rate #: The speaking rate

    def voices(self) -> list[str]:
        """Gets the list of voice names available on the system.

        :return: The list of voice names
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> speaker = PyXA.XASpeech()
        >>> print(speaker.voices())
        ['Agnes', 'Alex', 'Alice', 'Allison',

        .. versionadded:: 0.0.9
        """
        ls = AppKit.NSSpeechSynthesizer.availableVoices()
        return [x.replace("com.apple.speech.synthesis.voice.", "").replace(".premium", "").title() for x in ls]
    
    def speak(self, path: Union[str, XAPath, None] = None):
        """Speaks the provided message using the desired voice, volume, and speaking rate. 

        :param path: The path to a .AIFF file to output sound to, defaults to None
        :type path: Union[str, XAPath, None], optional

        :Example 1: Speak a message aloud

        >>> import PyXA
        >>> PyXA.XASpeech("This is a test").speak()

        :Example 2: Output spoken message to an AIFF file

        >>> import PyXA
        >>> speaker = PyXA.XASpeech("Hello, world!")
        >>> speaker.speak("/Users/steven/Downloads/Hello.AIFF")

        :Example 3: Control the voice, volume, and speaking rate

        >>> import PyXA
        >>> speaker = PyXA.XASpeech(
        >>>     message = "Hello, world!",
        >>>     voice = "Alex",
        >>>     volume = 1,
        >>>     rate = 500
        >>> )
        >>> speaker.speak()

        .. versionadded:: 0.0.9
        """
        # Get the selected voice by name
        voice = None
        for v in AppKit.NSSpeechSynthesizer.availableVoices():
            if self.voice.lower() in v.lower():
                voice = v

        # Set up speech synthesis object
        synthesizer = AppKit.NSSpeechSynthesizer.alloc().initWithVoice_(voice)
        synthesizer.setVolume_(self.volume)
        synthesizer.setRate_(self.rate)

        # Start speaking
        if path is None:
            synthesizer.startSpeakingString_(self.message)
        else:
            if isinstance(path, str):
                path = XAPath(path)
            synthesizer.startSpeakingString_toURL_(self.message, path.xa_elem)

        # Wait for speech to complete
        while synthesizer.isSpeaking():
            time.sleep(0.01)




class XASpotlight(XAObject):
    """A Spotlight query for files on the disk.

    .. versionadded:: 0.0.9
    """
    def __init__(self, *query: list[Any]):
        self.query: list[Any] = query #: The query terms to search
        self.timeout: int = 10 #: The amount of time in seconds to timeout the search after
        self.predicate: Union[str, XAPredicate] = None #: The predicate to filter search results by
        self.results: list[XAPath] #: The results of the search
        self.__results = None

        self.query_object = AppKit.NSMetadataQuery.alloc().init()
        nc = AppKit.NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(self, '_queryNotification:', None, self.query_object)

    @property
    def results(self) -> list['XAPath']:
        if len(self.query) == 0 and self.predicate is None:
            return []
        self.run()
        total_time = 0
        while self.__results is None and total_time < self.timeout:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.01))
            total_time += 0.01
        if self.__results is None:
            return []
        return self.__results

    def run(self):
        """Runs the search.

        :Example:

        >>> import PyXA
        >>> from datetime import date, datetime, time
        >>> date1 = datetime.combine(date(2022, 5, 17), time(0, 0, 0))
        >>> date2 = datetime.combine(date(2022, 5, 18), time(0, 0, 0))
        >>> search = PyXA.XASpotlight(date1, date2)
        >>> print(search.results)
        [<<class 'PyXA.XAPath'>file:///Users/exampleUser/Downloads/>, <<class 'PyXA.XAPath'>file:///Users/exampleUser/Downloads/Example.txt>, ...]

        .. versionadded:: 0.0.9
        """
        if self.predicate is not None:
            # Search with custom predicate
            if isinstance(self.predicate, XAPredicate):
                self.predicate = self.predicate.get_clipboard_representation()
            self.__search_with_predicate(self.predicate)
        elif len(self.query) == 1 and isinstance(self.query[0], datetime):
            # Search date + or - 24 hours
            self.__search_by_date(self.query)
        elif len(self.query) == 2 and isinstance(self.query[0], datetime) and isinstance(self.query[1], datetime):
            # Search date range
            self.__search_by_date_range(self.query[0], self.query[1])
        elif all(isinstance(x, str) or isinstance(x, int) or isinstance(x, float) for x in self.query):
            # Search matching multiple strings
            self.__search_by_strs(self.query)
        elif isinstance(self.query[0], datetime) and all(isinstance(x, str) or isinstance(x, int) or isinstance(x, float) for x in self.query[1:]):
            # Search by date and string
            self.__search_by_date_strings(self.query[0], self.query[1:])
        elif isinstance(self.query[0], datetime) and isinstance(self.query[1], datetime) and all(isinstance(x, str) or isinstance(x, int) or isinstance(x, float) for x in self.query[2:]):
            # Search by date range and string
            self.__search_by_date_range_strings(self.query[0], self.query[1], self.query[2:])

        AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.01))

    def show_in_finder(self):
        """Shows the search in Finder. This might not reveal the same search results.

        .. versionadded:: 0.0.9
        """
        AppKit.NSWorkspace.sharedWorkspace().showSearchResultsForQueryString_(str(self.query))

    def __search_by_strs(self, terms: tuple[str]):
        expanded_terms = [[x]*3 for x in terms]
        expanded_terms = [x for sublist in expanded_terms for x in sublist]
        format = "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND " * len(terms)
        self.__search_with_predicate(format[:-5], *expanded_terms)

    def __search_by_date(self, date: datetime):
        self.__search_with_predicate(f"((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@))", *[date - timedelta(hours=12), date + timedelta(hours=12)]*5)

    def __search_by_date_range(self, date1: datetime, date2: datetime):
        self.__search_with_predicate(f"((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@))", *[date1, date2]*5)

    def __search_by_date_strings(self, date: datetime, terms: tuple[str]):
        expanded_terms = [[x]*3 for x in terms]
        expanded_terms = [x for sublist in expanded_terms for x in sublist]
        format = "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND " * len(terms)
        format += "(((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@)))"
        self.__search_with_predicate(format, *expanded_terms, *[date - timedelta(hours=12), date + timedelta(hours=12)]*5)

    def __search_by_date_range_strings(self, date1: datetime, date2: datetime, terms: tuple[str]):
        expanded_terms = [[x]*3 for x in terms]
        expanded_terms = [x for sublist in expanded_terms for x in sublist]
        format = "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND " * len(terms)
        format += "(((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@)))"
        self.__search_with_predicate(format, *expanded_terms, *[date1, date2]*5)

    def __search_with_predicate(self, predicate_format: str, *args: list[Any]):
        predicate = AppKit.NSPredicate.predicateWithFormat_(predicate_format, *args)
        self.query_object.setPredicate_(predicate)
        self.query_object.startQuery()

    def _queryNotification_(self, notification):
        if notification.name() == AppKit.NSMetadataQueryDidFinishGatheringNotification:
            self.query_object.stopQuery()
            results = notification.object().results()
            self.__results = [XAPath(x.valueForAttribute_(AppKit.NSMetadataItemPathKey)) for x in results]




######################
### User Interface ###
######################
class XAUIElementList(XAList):
    """A wrapper around a list of UI elements.

    All properties of UI elements can be accessed via methods on this list, returning a list of the method's return value for each element in the list.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_type = None):
        if obj_type is None:
            obj_type = XAUIElement
        super().__init__(properties, obj_type, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def accessibility_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("accessibilityDescription"))

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def entire_contents(self) -> list[list[Any]]:
        return list(self.xa_elem.arrayByApplyingSelector_("entireContents"))

    def focused(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("focused"))

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def position(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def size(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def maximum_value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximumValue"))

    def minimum_value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("minimumValue"))

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def role(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("role"))

    def role_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("roleDescription"))

    def subrole(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subrole"))

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected"))

    def by_properties(self, properties: dict) -> 'XAUIElement':
        return self.by_property("properties", properties)

    def by_accessibility_description(self, accessibility_description: str) -> 'XAUIElement':
        return self.by_property("accessibilityDescription", accessibility_description)

    def by_entire_contents(self, entire_contents: list[Any]) -> 'XAUIElement':
        return self.by_property("entireContents", entire_contents)

    def by_focused(self, focused: bool) -> 'XAUIElement':
        return self.by_property("focused", focused)

    def by_name(self, name: str) -> 'XAUIElement':
        return self.by_property("name", name)

    def by_title(self, title: str) -> 'XAUIElement':
        return self.by_property("title", title)

    def by_position(self, position: tuple[tuple[int, int], tuple[int, int]]) -> 'XAUIElement':
        return self.by_property("position", position)

    def by_size(self, size: tuple[int, int]) -> 'XAUIElement':
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
        self.position: tuple[int, int] #: The position of the top left corner of the element
        self.size: tuple[int, int] #: The width and height of the element, in pixels
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
    def entire_contents(self) -> list[XAObject]:
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
    def position(self) -> tuple[int, int]:
        return self.xa_elem.position()

    @property
    def size(self) -> tuple[int, int]:
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

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().collapse()

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.collapse()

    def uncollapse(self):
        """Uncollapses all windows in the list.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().uncollapse()

        .. versionadded:: 0.0.6
        """
        for window in self:
            window.uncollapse()

    def close(self):
        """Closes all windows in the list.add()

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().close()
        
        .. versionadded:: 0.0.6
        """
        for window in self:
            window.close()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAWindow(XAUIElement):
    """A general window class for windows of both officially scriptable and non-scriptable applications.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def close(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.close()

        .. versionadded:: 0.0.1
        """
        close_button = self.buttons({"subrole": "AXCloseButton"})[0]
        close_button.click()
        return self

    def collapse(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.collapse()

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

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.uncollapse()

        .. versionadded:: 0.0.1
        """
        ls = self.xa_sevt.applicationProcesses()
        dock_process = XAPredicate.evaluate_with_format(ls, "name == 'Dock'")[0]

        ls = dock_process.lists()[0].UIElements()
        name = self.name

        app_icon = XAPredicate.evaluate_with_format(ls, f"name == '{name}'")[0]
        app_icon.actions()[0].perform()
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"




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


############
### Text ###
############
class XATextDocumentList(XAList, XAClipboardCodable):
    """A wrapper around lists of text documents that employs fast enumeration techniques.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATextDocument
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("properties")
        return [dict(x) for x in ls]

    def text(self) -> 'XATextList':
        """Gets the text of each document in the list.

        :return: A list of document texts
        :rtype: XATextList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("text")
        return self._new_element(ls, XATextList)

    def by_properties(self, properties: dict) -> Union['XATextDocument', None]:
        """Retrieves the document whose properties match the given properties dictionary, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XATextDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("properties", properties)

    def by_text(self, text: str) -> Union['XATextDocument', None]:
        """Retrieves the first documents whose text matches the given text.

        :return: The desired document, if it is found
        :rtype: Union[XATextDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("text", text)

    def paragraphs(self) -> 'XAParagraphList':
        """Gets the paragraphs of each document in the list.

        :return: A combined list of all paragraphs in each document of the list
        :rtype: XAParagraphList
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("paragraphs")
        return self._new_element([plist for plist in ls], XAParagraphList)

    def words(self) -> 'XAWordList':
        """Gets the words of each document in the list.

        :return: A combined list of all words in each document of the list
        :rtype: XAWordList
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("words")
        return [self._new_element([plist for plist in ls], XAWordList)]

    def characters(self) -> 'XACharacterList':
        """Gets the characters of each document in the list.

        :return: A combined list of all characters in each document of the list
        :rtype: XACharacterList
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("characters")
        return [self._new_element([plist for plist in ls], XACharacterList)]

    def attribute_runs(self) -> 'XAAttributeRunList':
        """Gets the attribute runs of each document in the list.

        :return: A combined list of all attribute runs in each document of the list
        :rtype: XAAttributeRunList
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("attributeRuns")
        return [self._new_element([plist for plist in ls], XAAttributeRunList)]

    def attachments(self) -> 'XAAttachmentList':
        """Gets the attachments of each document in the list.

        :return: A combined list of all attachments in each document of the list
        :rtype: XAAttachmentList
        
        .. versionadded:: 0.0.3
        """
        ls = self.xa_elem.arrayByApplyingSelector_("attachments")
        return [self._new_element([plist for plist in ls], XAAttachmentList)]

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, each documents's file URL and name are added to the clipboard.

        :return: A list of each document's file URL and name
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [str(x) for x in self.text()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.text()) + ">"

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

    @text.setter
    def text(self, text: str):
        self.set_property("text", text)

    def prepend(self, text: str) -> 'XATextDocument':
        """Inserts the provided text at the beginning of the document.

        :param text: The text to insert.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`append`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = str(self.text)
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
        old_text = str(self.text)
        self.set_property("text", old_text + text)
        return self

    def reverse(self) -> 'XATextDocument':
        """Reverses the text of the document.

        :return: A reference to the document object.
        :rtype: XATextDocument

        .. versionadded:: 0.0.4
        """
        self.set_property("text", reversed(str(self.text)))
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

    def paragraphs(self, filter: dict = None) -> 'XAParagraphList':
        """Gets the paragraphs of every text item in the list.

        :return: The list of paragraphs
        :rtype: XAParagraphList

        .. versionadded:: 0.0.1
        """
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("paragraphs")
        else:
            ls = [x.xa_elem.split("\n") for x in self]
        ls = [paragraph for paragraphlist in ls for paragraph in paragraphlist if paragraph.strip() != '']
        return self._new_element(ls, XAParagraphList, filter)

    def sentences(self) -> 'XASentenceList':
        """Gets the sentences of every text item in the list.

        :return: The list of sentences
        :rtype: XASentenceList

        .. versionadded:: 0.1.0
        """
        ls = [x.sentences() for x in self]
        ls = [sentence for sentencelist in ls for sentence in sentencelist]
        return self._new_element(ls, XASentenceList)

    def words(self, filter: dict = None) -> 'XAWordList':
        """Gets the words of every text item in the list.

        :return: The list of words
        :rtype: XAWordList

        .. versionadded:: 0.0.1
        """
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("words")
        else:
            ls = [x.xa_elem.split() for x in self]
        ls = [word for wordlist in ls for word in wordlist]
        return self._new_element(ls, XAWordList, filter)

    def characters(self, filter: dict = None) -> 'XACharacterList':
        """Gets the characters of every text item in the list.

        :return: The list of characters
        :rtype: XACharacterList

        .. versionadded:: 0.0.1
        """
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("characters")
        else:
            ls = [list(x.xa_elem) for x in self]
        ls = [character for characterlist in ls for character in characterlist]
        return self._new_element(ls, XACharacterList, filter)

    def attribute_runs(self, filter: dict = None) -> 'XAAttributeRunList':
        """Gets the attribute runs of every text item in the list.

        :return: The list of attribute runs
        :rtype: XAAttributeRunList

        .. versionadded:: 0.0.1
        """
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("attributeRuns")
        ls = [attribute_run for attribute_run_list in ls for attribute_run in attribute_run_list]
        return self._new_element(ls, XAAttributeRunList, filter)

    def attachments(self, filter: dict = None) -> 'XAAttachmentList':
        """Gets the attachments of every text item in the list.

        :return: The list of attachments
        :rtype: XAAttachmentList

        .. versionadded:: 0.0.1
        """
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("attachments")
        ls = [attachment for attachment_list in ls for attachment in attachment_list]
        return self._new_element(ls, XAAttachmentList, filter)

    def __repr__(self):
        try:
            if isinstance(self.xa_elem[0], ScriptingBridge.SBObject):
                # List items will not resolved to text upon dereferencing the list; need to resolve items individually
                count = self.xa_elem.count()
                if count <= 500:
                    # Too many unresolved pointers, save time by just reporting the length
                    return "<" + str(type(self)) + str([x.get() for x in self.xa_elem]) + ">"
                return "<" + str(type(self)) + "length: " + str(self.xa_elem.count()) + ">"

            # List items will resolve to text upon dereferencing the list
            return "<" + str(type(self)) + str(self.xa_elem.get()) + ">"
        except:
            return "<" + str(type(self)) + str(list(self.xa_elem)) + ">" 

class XAText(XAObject):
    """A class for managing and interacting with the text of documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        if isinstance(properties, dict):
            super().__init__(properties)
        elif isinstance(properties, str):
            super().__init__({"element": properties})

        self.text: str #: The plaintext contents of the rich text
        self.color: XAColor #: The color of the first character
        self.font: str #: The name of the font of the first character
        self.size: int #: The size in points of the first character

    @property
    def text(self) -> str:
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        else:
            return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        if isinstance(self.xa_elem, str):
            self.xa_elem = text
        else:
            self.set_property("text", text)

    @property
    def color(self) -> 'XAColor':
        if isinstance(self.xa_elem, str):
            return None
        else:
            return XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: 'XAColor'):
        if isinstance(self.xa_elem, str):
            self.color = color.xa_elem
        else:
            self.set_property("color", color.xa_elem)

    @property
    def font(self) -> str:
        if isinstance(self.xa_elem, str):
            return None
        else:
            return self.xa_elem.font()

    @font.setter
    def font(self, font: str):
        if isinstance(self.xa_elem, str):
            self.font = font
        else:
            self.set_property("font", font)

    @property
    def size(self) -> int:
        if isinstance(self.xa_elem, str):
            return 0
        else:
            return self.xa_elem.size()

    @size.setter
    def size(self, size: int):
        if isinstance(self.xa_elem, str):
            self.size = size
        else:
            self.set_property("size", size)

    # def spelling_suggestions(self):
    #     suggestions = []
    #     text = str(self.xa_elem)
    #     spellchecker = AppKit.NSSpellChecker.sharedSpellChecker()

    #     orthography = None
    #     word_count = 0

    #     pprint(dir(LatentSemanticMapping.LSMMapCreate(None, 0)))

    #     # c = spellchecker.checkString_range_types_options_inSpellDocumentWithTag_orthography_wordCount_(text, (0, len(text)), AppKit.NSTextCheckingTypeSpelling | AppKit.NSTextCheckingTypeGrammar | AppKit.NSTextCheckingTypeCorrection, {}, 0, orthography, None)
    #     # print(c[1].languageMap())

    #     for word in text.split():
    #         completions = spellchecker.completionsForPartialWordRange_inString_language_inSpellDocumentWithTag_((0, len(word)), word, "", 0)
    #         suggestions.append(completions)

    #     # for word in text.split():
    #     #     guesses = spellchecker.guessesForWordRange_inString_language_inSpellDocumentWithTag_((0, len(word)), word, "", 0)
    #     #     suggestions.append(guesses)
    #     return suggestions

    def tag_parts_of_speech(self, unit: Literal["word", "sentence", "paragraph", "document"] = "word") -> list[tuple[str, str]]:
        """Tags each word of the text with its associated part of speech.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its part of speech
        :rtype: list[tuple[str, str]]

        :Example 1: Extract nouns from a text

        >>> import PyXA
        >>> text = PyXA.XAText("Here’s to the crazy ones. The misfits. The rebels.")
        >>> nouns = [pos[0] for pos in text.tag_parts_of_speech() if pos[1] == "Noun"]
        >>> print(nouns)
        ['ones', 'misfits', 'rebels']

        .. versionadded:: 0.1.0
        """
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLexicalClass])
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument
        
        tagged_pos = []
        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[token_range.location:token_range.location + token_range.length]
            tagged_pos.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(str(self.xa_elem))), unit, NaturalLanguage.NLTagSchemeLexicalClass, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_pos

    def tag_languages(self, unit: Literal["word", "sentence", "paragraph", "document"] = "paragraph") -> list[tuple[str, str]]:
        """Tags each paragraph of the text with its language.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "paragraph"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each paragraph of the text and its language
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> text = PyXA.XAText("This is English.\nQuesto è Italiano.\nDas ist deutsch.\nこれは日本語です。")
        >>> print(text.tag_languages())
        [('This is English.\n', 'en'), ('Questo è Italiano.\n', 'it'), ('Das ist deutsch.\n', 'de'), ('これは日本語です。', 'ja')]

        .. versionadded:: 0.1.0
        """
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLanguage])
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument
        
        tagged_languages = []
        def apply_tags(tag, token_range, error):
            paragraph = str(self.xa_elem)[token_range.location:token_range.location + token_range.length]
            if paragraph.strip() != "":
                tagged_languages.append((paragraph, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(str(self.xa_elem))), unit, NaturalLanguage.NLTagSchemeLanguage, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_languages

    def tag_entities(self, unit: Literal["word", "sentence", "paragraph", "document"] = "word") -> list[tuple[str, str]]:
        """Tags each word of the text with either the category of entity it represents (i.e. person, place, or organization) or its part of speech.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its entity category or part of speech
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> text = PyXA.XAText("Tim Cook is the CEO of Apple.")
        >>> print(text.tag_entities())
        [('Tim', 'PersonalName'), ('Cook', 'PersonalName'), ('is', 'Verb'), ('the', 'Determiner'), ('CEO', 'Noun'), ('of', 'Preposition'), ('Apple', 'OrganizationName')]

        .. versionadded:: 0.1.0
        """
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass])
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument
        
        tagged_languages = []
        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[token_range.location:token_range.location + token_range.length]
            if word_phrase.strip() != "":
                tagged_languages.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(str(self.xa_elem))), unit, NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_languages

    def tag_lemmas(self, unit: Literal["word", "sentence", "paragraph", "document"] = "word") -> list[tuple[str, str]]:
        """Tags each word of the text with its stem word.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its stem words
        :rtype: list[tuple[str, str]]

        :Example 1: Lemmatize each word in a text

        >>> import PyXA
        >>> text = PyXA.XAText("Here’s to the crazy ones. The misfits. The rebels.")
        >>> print(text.tag_lemmas())
        [('Here’s', 'here'), ('to', 'to'), ('the', 'the'), ('crazy', 'crazy'), ('ones', 'one'), ('The', 'the'), ('misfits', 'misfit'), ('The', 'the'), ('rebels', 'rebel')]

        :Example 2: Combine parts of speech tagging and lemmatization

        >>> import PyXA
        >>> text = PyXA.XAText("The quick brown fox tries to jump over the sleeping lazy dog.")
        >>> verbs = [pos[0] for pos in text.tag_parts_of_speech() if pos[1] == "Verb"]
        >>> for index, verb in enumerate(verbs):
        >>>     print(index, PyXA.XAText(verb).tag_lemmas())
        0 [('tries', 'try')]
        1 [('jump', 'jump')]
        2 [('sleeping', 'sleep')]

        .. versionadded:: 0.1.0
        """
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLemma])
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument
        
        tagged_lemmas = []
        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[token_range.location:token_range.location + token_range.length]
            if word_phrase.strip() != "":
                tagged_lemmas.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(str(self.xa_elem))), unit, NaturalLanguage.NLTagSchemeLemma, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace | NaturalLanguage.NLTaggerJoinContractions, apply_tags)
        return tagged_lemmas

    def tag_sentiments(self, sentiment_scale: list[str] = None, unit: Literal["word", "sentence", "paragraph", "document"] = "paragraph") -> list[tuple[str, str]]:
        """Tags each paragraph of the text with a sentiment rating.

        :param sentiment_scale: A list of terms establishing a range of sentiments from most negative to most postive
        :type sentiment_scale: list[str]
        :param unit: The grammatical unit to divide the text into for tagging, defaults to "paragraph"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each paragraph of the text and its sentiment rating
        :rtype: list[tuple[str, str]]

        :Example 1: Assess the sentiment of a string

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\nBut this is great!")
        >>> print(text.tag_sentiments())
        [('This sucks.\n', 'Negative'), ('But this is great!', 'Positive')]

        :Example 2: Use a custom sentiment scale

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\nBut this is good!\nAnd this is great!")
        >>> print(text.tag_sentiments(sentiment_scale=["Very Negative", "Negative", "Somewhat Negative", "Neutral", "Somewhat Positive", "Positive", "Very Positive"]))
        [('This sucks.\n', 'Very Negative'), ('But this is good!\n', 'Neutral'), ('And this is great!', 'Very Positive')]

        :Example 3: Use other tag units

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\nBut this is good!\nAnd this is great!")
        >>> print(1, text.tag_sentiments())
        >>> print(2, text.tag_sentiments(unit="word"))
        >>> print(3, text.tag_sentiments(unit="document"))
        1 [('This sucks.\n', 'Negative'), ('But this is good!\n', 'Neutral'), ('And this is great!', 'Positive')]
        2 [('This', 'Negative'), ('sucks', 'Negative'), ('.', 'Negative'), ('But', 'Neutral'), ('this', 'Neutral'), ('is', 'Neutral'), ('good', 'Neutral'), ('!', 'Neutral'), ('And', 'Positive'), ('this', 'Positive'), ('is', 'Positive'), ('great', 'Positive'), ('!', 'Positive')]
        3 [('This sucks.\nBut this is good!\nAnd this is great!', 'Neutral')]

        .. versionadded:: 0.1.0
        """
        if sentiment_scale is None or len(sentiment_scale) == 0:
            sentiment_scale = ["Negative", "Neutral", "Positive"]

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeSentimentScore])
        tagger.setString_(str(self.xa_elem))
        
        tagged_sentiments = []
        def apply_tags(tag, token_range, error):
            paragraph = str(self.xa_elem)[token_range.location:token_range.location + token_range.length]
            if paragraph.strip() != "":
                # Map raw tag value to range length
                raw_value = float(tag or 0)
                scaled = (raw_value + 1.0) / 2.0 * (len(sentiment_scale) - 1)

                label = sentiment_scale[int(scaled)]
                tagged_sentiments.append((paragraph, label))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(self.xa_elem)), unit, NaturalLanguage.NLTagSchemeSentimentScore, 0, apply_tags)
        return tagged_sentiments

    def paragraphs(self, filter: dict = None) -> 'XAParagraphList':
        """Gets a list of paragraphs in the text.

        :param filter: The properties and associated values to filter paragraphs by, defaults to None
        :type filter: dict, optional
        :return: The list of paragraphs
        :rtype: XAParagraphList

        :Example 1: Get paragraphs of a text string

        >>> import PyXA
        >>> string = \"\"\"This is the first paragraph.
        >>> 
        >>> This is the second paragraph.\"\"\"
        >>> text = PyXA.XAText(string)
        >>> print(text.paragraphs())
        <<class 'PyXA.XAWordList'>['This is the first paragraph.', 'This is the second paragraph. Neat! Very cool.']>

        :Example 2: Get paragraphs of a Note

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.paragraphs())
        <<class 'PyXA.XAWordList'>['This is the first paragraph.', 'This is the second paragraph. Neat! Very cool.']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = [x for x in self.xa_elem.split("\n") if x.strip() != '']
            return self._new_element(ls, XAWordList, filter)
        else:
            return self._new_element(self.xa_elem.paragraphs(), XAParagraphList, filter)

    def sentences(self) ->  'XASentenceList':
        """Gets a list of sentences in the text.

        :return: The list of sentencnes
        :rtype: XASentenceList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.sentences())
        <<class 'PyXA.XASentenceList'>['This is the first paragraph.\\n', '\\n', 'This is the second paragraph. ', 'Neat! ', 'Very cool.']>

        .. versionadded:: 0.1.0
        """
        raw_string = self.xa_elem
        if hasattr(self.xa_elem, "get"):
            raw_string = self.xa_elem.get()

        sentences = []
        tokenizer = AppKit.NLTokenizer.alloc().initWithUnit_(AppKit.kCFStringTokenizerUnitSentence)
        tokenizer.setString_(raw_string)
        for char_range in tokenizer.tokensForRange_((0, len(raw_string))):
            start = char_range.rangeValue().location
            end = start + char_range.rangeValue().length
            sentences.append(raw_string[start:end])
            
        ls = AppKit.NSArray.alloc().initWithArray_(sentences)
        return self._new_element(sentences, XASentenceList) 

    def words(self, filter: dict = None) -> 'XAWordList':
        """Gets a list of words in the text.

        :return: The list of words
        :rtype: XAWordList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.words())
        <<class 'PyXA.XAWordList'>['This', 'is', 'the', 'first', 'paragraph.', 'This', 'is', 'the', 'second', 'paragraph.', 'Neat!', 'Very', 'cool.']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = self.xa_elem.split()
            return self._new_element(ls, XAWordList, filter)
        else:
            return self._new_element(self.xa_elem.words(), XAWordList, filter)

    def characters(self, filter: dict = None) -> 'XACharacterList':
        """Gets a list of characters in the text.

        :return: The list of characters
        :rtype: XACharacterList

        :Example 1: Get all characters in a text

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.characters())
        <<class 'PyXA.XACharacterList'>['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 't', 'h', 'e', ' ', 'f', 'i', 'r', 's', 't', ' ', 'p', 'a', 'r', 'a', 'g', 'r', 'a', 'p', 'h', '.', '\n', '\n', 'T', 'h', 'i', 's', ' ', 'i', 's', ' ', 't', 'h', 'e', ' ', 's', 'e', 'c', 'o', 'n', 'd', ' ', 'p', 'a', 'r', 'a', 'g', 'r', 'a', 'p', 'h', '.', ' ', 'N', 'e', 'a', 't', '!', ' ', 'V', 'e', 'r', 'y', ' ', 'c', 'o', 'o', 'l', '.']>

        :Example 2: Get the characters of the first word in a text

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.words()[0].characters())
        <<class 'PyXA.XACharacterList'>['T', 'h', 'i', 's']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = list(self.xa_elem)
            return self._new_element(ls, XACharacterList, filter) 
        else:
            return self._new_element(self.xa_elem.characters().get(), XACharacterList, filter)

    def attribute_runs(self, filter: dict = None) -> 'XAAttributeRunList':
        """Gets a list of attribute runs in the text. For formatted text, this returns all sequences of characters sharing the same attributes.

        :param filter: The properties and associated values to filter attribute runs by, defaults to None
        :type filter: dict, optional
        :return: The list of attribute runs
        :rtype: XAAttributeRunList

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            return []
        else:
            return self._new_element(self.xa_elem.attributeRuns(), XAAttributeRunList, filter)

    def attachments(self, filter: dict = None) -> 'XAAttachmentList':
        """Gets a list of attachments of the text.

        :param filter: The properties and associated values to filter attachments by, defaults to None
        :type filter: dict, optional
        :return: The list of attachments
        :rtype: XAAttachmentList

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            return []
        else:
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



class XASentenceList(XATextList):
    """A wrapper around lists of sentences that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASentence)

class XASentence(XAText):
    """A class for managing and interacting with sentences in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




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




class XALSM(XAObject):
    def __init__(self, dataset: Union[dict[str, list[str]], None] = None, from_file: bool = False):
        """Initializes a Latent Semantic Mapping environment.

        :param dataset: The initial dataset, specified as a dictionary where keys are categories and values are list of corresponding texts, defaults to None. Cannot be None if from_file is False.
        :type dataset: Union[dict[str, list[str]], None], optional
        :param from_file: Whether the LSM is being loaded from a file, defaults to False. Cannot be False is dataset is None.
        :type from_file: bool, optional
        :raises ValueError: Either you must provide a dataset, or you must load an existing map from an external file

        :Example 1: Classify emails based on subject line

        >>> import PyXA
        >>> lsm = PyXA.XALSM({
        >>>     # 1
        >>>     "spam": ["Deals", "Holiday playbook", "Spend and save. You know the drill.", "Don't miss these holiday deals!", "GOOD NEWS", "you will never have an opportunity of this kind again", "Your Long Overdue Compensation Funds; Totally", "US $25,000,000.00", "goog day", "GOOD DAY, I am Mike Paul I have a", "enron methanol; meter # : 988291 this is a follow up to the note i gave you on monday , 4...", "hpl nom for january 9, see attached file : hplnol 09. xls", "neon retreat ho ho ho, we're around to that most wonderful time of the year", "photoshop, windows, office cheap, main trending abasements, darer prudently fortuitous", "re: indian springs this deal is to book the teco pvr revenue. it is my understanding that...", "noms / actual flow for 2 / we agree", "nominations for oct 21 - 23"],
        >>> 
        >>>     # 2
        >>>     "kayak": ["Price Alert: Airfare holding steady for your trip", "Prices going down for your Boston to Dublin flight", "Price Increase: Boston to Dublin airfare up $184", "Flight Alert: #37 decrease on your flight to Dublin.", "Flight Alert: It's time to book your flight to Dublin", "Price Alert: Airfare holding steady for your Bangor, ME to...", "Ready to explore the world again?"],
        >>> 
        >>>     # 3
        >>>     "lenovo": ["Doorbuster deals up to 70% off", "Visionary, On-Demand Content. Lenovo Tech World '22 is starting", "Up to 70% off deals 9 AM", "TGIF! Here's up to 70% off to jumpstart your weekend", "Top picks to refresh your workspace", "This only happens twice a year", "Think about saving on a Think PC", "Deep deals on Summer Clearance", "Save up to 67% + earn rewards", "Unlock up to 61% off Think PCs", "Giveaway alert!", "Annual Sale Sneak Peak Unlocked!"],
        >>> 
        >>>     # 4
        >>>     "linkedin": ["Here is the latest post trending amongst your coworkers", "Stephen, add Sean Brown to your network", "Share thoughts on LinkedIn", "Top companies are hiring", "Linkedin is better on the app", "Here is the latest post trending amongst your coworkers", "Stephen, add Ronald McDonald to your network", "James Smith shared a post for the first time in a while", "Here is the latest post trending amongst your coworkers", "You appeared in 13 searches this week", "you're on a roll with your career!", "You appeared in 16 searches this week", "18 people notices you", "You appeared in 10 searches this week", "Stephen, add Joe Shmoe to your network", "Your network is talking: The Center for Oceanic Research...", "thanks for being a valued member"]
        >>> })
        >>> print(lsm.categorize_query("New! Weekend-only deals"))
        >>> print(lsm.categorize_query("Stephen, redeem these three (3) unlocked courses"))
        >>> print(lsm.categorize_query("Round Trip From San Francisco to Atlanta"))
        [(3, 0.9418474435806274)]
        [(4, 0.9366401433944702)]
        [(2, 0.9944692850112915)]

        :Example 2: Use the Mail module to automate dataset construction

        >>> import PyXA
        >>> app = PyXA.Application("Mail")
        >>> junk_subject_lines = app.accounts()[0].mailboxes().by_name("Junk").messages().subject()
        >>> other_subject_lines = app.accounts()[0].mailboxes().by_name("INBOX").messages().subject()
        >>> 
        >>> dataset = {
        >>>     "junk": junk_subject_lines,
        >>>     "other": other_subject_lines
        >>> }
        >>> lsm = PyXA.XALSM(dataset)
        >>> 
        >>> query = "Amazon Web Services Billing Statement Available"
        >>> category = list(dataset.keys())[lsm.categorize_query(query)[0][0] - 1]
        >>> print(query, "- category:", category)
        >>> 
        >>> query = "Complete registration form asap receive your rewards"
        >>> category = list(dataset.keys())[lsm.categorize_query(query)[0][0] - 1]
        >>> print(query, "- category:", category)
        Amazon Web Services Billing Statement Available - category: other
        Complete registration form asap receive your rewards - category: junk

        .. versionadded:: 0.1.0
        """
        self.__categories = {}
        if dataset is None and not from_file:
            raise ValueError("You must either load a map from an external file or provide an initial dataset.")
        elif dataset is None:
            # Map will be loaded from external file -- empty dataset is temporary
            self.__dataset = {}
        else:
            # Create new map
            self.__dataset = dataset

            self.map = LatentSemanticMapping.LSMMapCreate(None, 0)
            LatentSemanticMapping.LSMMapStartTraining(self.map)
            LatentSemanticMapping.LSMMapSetProperties(self.map, {
                LatentSemanticMapping.kLSMSweepCutoffKey: 0,
                # LatentSemanticMapping.kLSMPrecisionKey: LatentSemanticMapping.kLSMPrecisionDouble,
                LatentSemanticMapping.kLSMAlgorithmKey: LatentSemanticMapping.kLSMAlgorithmSparse,
            })

            for category in dataset:
                self.__add_category(category)

            LatentSemanticMapping.LSMMapCompile(self.map)

    def __add_category(self, category: str) -> int:
        loc = Foundation.CFLocaleGetSystem()
        category_ref = LatentSemanticMapping.LSMMapAddCategory(self.map)
        self.__categories[category] = category_ref
        self.__categories[category_ref] = category_ref
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(self.__dataset[category]), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
        LatentSemanticMapping.LSMMapAddText(self.map, text_ref, category_ref)
        return category_ref

    def save(self, file_path: Union[XAPath, str]) -> bool:
        """Saves the map to an external file.

        :param file_path: The path to save the map at
        :type file_path: Union[XAPath, str]
        :return: True if the map was saved successfully
        :rtype: bool

        :Example: Create a Reddit post classifier for gaming vs. productivity posts

        >>> import PyXA
        >>> lsm = PyXA.XALSM({
        >>>     # 1
        >>>     "gaming": ["If you could vote on the 2017 Mob Vote again, which mob would you choose this time and why?", "Take your time, you got this", "My parents (late 70s) got me a ps5 controller for Christmas. I do not own a playstation 5...", "I got off the horse by accident right before a cutscene in red dead", "boy gamer", "Minesweeper 99 x 99, 1500 mines. Took me about 2.5 hours to finish, nerve-wracking. No one might care, but just wanted to share this.", "The perfect cosplay doesn’t ex...", "'Play until we lose'", "Can we please boycott Star Wars battlefront 2", "EA removed the refund button on their webpage, and now you have to call them and wait to get a refund.", "Train Simulator is so immersive!", "Been gaming with this dude for 15 years. Since Rainbow Six Vegas on 360. I have some good gaming memories with him. He tried but couldn’t get one. Little did he know I was able to get him one. Looking forward to playing another generation with him.", "EA will no longer have exclusive rights of the Star Wars games", "A ziplining contraption I created with 1000+ command blocks", "The steepest walkable staircase possible in 1.16", "I made a texture pack that gives mobs different facial expressions. Should I keep going?"],
        >>> 
        >>>     # 2
        >>>     "productivity": ["Looking for an alarm app that plays a really small alarm, doesn’t need to be switched off and doesn’t repeat.", "I want to build a second brain but I'm lost and don't know where to start.", "noise cancelling earplugs", "I have so much to do but I don't know where to start", "How to handle stressful work calls", "time tracking app/platform", "We just need to find ways to cope and keep moving forward.", "Ikigai - A Reason for Being", "Minimalist Productivity Tip: create two users on your computer ➞ One for normal use and leisure ➞ One for business/work only. I have nothing except the essentials logged in on my work user. Not even Messages or YouTube. It completely revolutionized my productivity 💸", "Trick yourself into productivity the same way you trick yourself into procrastination", "I spent 40 hours sifting through research papers to fix my mental clarity, focus, and productivity - I ended up going down a rabbit hole and figuring out it was all tied to sleep, even though I felt I sleep well - here's what I found.", "The Cycle of Procrastination. Always a good reminder", "'Most people underestimate what they can do in a year, and overestimate what they can do in a day' - When you work on getting 1% better each day you won't even recognize yourself in a year."],
        >>> })
        >>> lsm.save("/Users/steven/Downloads/gaming-productivity.map")

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        status = LatentSemanticMapping.LSMMapWriteToURL(self.map, file_path.xa_elem, 0)
        if status == 0:
            return True
        return False

    def load(file_path: Union[XAPath, str]) -> 'XALSM':
        """Loads a map from an external file.

        :param file_path: The file path for load the map from
        :type file_path: Union[XAPath, str]
        :return: The populated LSM object
        :rtype: XALSM

        :Example: Using the gaming vs. productivity Reddit post map

        >>> import PyXA
        >>> lsm = PyXA.XALSM.load("/Users/steven/Downloads/gaming-productivity.map")
        >>> print(lsm.categorize_query("Hidden survival base on our server"))
        >>> print(lsm.categorize_query("Your memory is FAR more powerful than you think… school just never taught us to use it properly."))
        [(1, 0.7313863635063171)]
        [(2, 0.9422407150268555)]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        new_lsm = XALSM(from_file=True)
        new_lsm.map = LatentSemanticMapping.LSMMapCreateFromURL(None, file_path.xa_elem, LatentSemanticMapping.kLSMMapLoadMutable)
        new_lsm.__dataset = {i: [] for i in range(LatentSemanticMapping.LSMMapGetCategoryCount(new_lsm.map))}
        new_lsm.__categories = {i: i for i in range(LatentSemanticMapping.LSMMapGetCategoryCount(new_lsm.map))}
        LatentSemanticMapping.LSMMapCompile(new_lsm.map)
        return new_lsm

    def add_category(self, name: str, initial_data: Union[list[str], None] = None) -> int:
        """Adds a new category to the map, optionally filling the category with initial text data.

        :param name: The name of the category
        :type name: str
        :param initial_data: _description_
        :type initial_data: list[str]
        :return: The ID of the new category
        :rtype: int

        :Example: Add a category for cleaning-related Reddit posts to the previous example

        >>> import PyXA
        >>> lsm = PyXA.XALSM.load("/Users/steven/Downloads/gaming-productivity.map")
        >>> lsm.add_category("cleaning", ["Curtains stained from eyelet reaction at dry cleaner", "How do I get these stains out of my pink denim overalls? from a black denim jacket that was drying next to them", "Cleaned my depression room after months 🥵", "Tip: 30 minute soak in Vinegar", "Regular floor squeegee pulled a surprising amount of pet hair out of my carpet!", "Before and after…", "It actually WORKS", "CLR is actually magic. (With some elbow grease)", "It was 100% worth it to scrape out my old moldy caulk and replace it. $5 dollars and a bit of time to make my shower look so much cleaner!", "Thanks to the person who recommended the Clorox Foamer. Before and after pics", "TIL you can dissolve inkstains with milk.", "Fixing cat scratch marks to couch using felting needle: Before and After", "Turns out BKF isn't a meme! Really satisfied with this stuff"])
        >>> print(lsm.categorize_query("Hidden survival base on our server"))
        >>> print(lsm.categorize_query("Your memory is FAR more powerful than you think… school just never taught us to use it properly."))
        >>> print(lsm.categorize_query("A carpet rake will change your life."))
        [(1, 0.7474805116653442)]
        [(2, 0.7167008519172668)]
        [(3, 0.797333300113678)]

        .. versionadded:: 0.1.0
        """
        LatentSemanticMapping.LSMMapStartTraining(self.map)

        if initial_data is None:
            initial_data = []

        if name in self.__dataset:
            raise ValueError("The category name must be unique.")

        self.__dataset[name] = initial_data
        category_ref = self.__add_category(name)
        LatentSemanticMapping.LSMMapCompile(self.map)
        return category_ref

    def add_data(self, data: dict[Union[int, str], list[str]]) -> list[int]:
        """Adds the provided data, organized by category, to the active map.

        :param data: A dictionary specifying new or existing categories along with data to input into them
        :type data: dict[Union[int, str], list[str]]
        :return: A list of newly created category IDs
        :rtype: int

        :Example: Classify text by language

        >>> import PyXA
        >>> lsm = PyXA.XALSM({})
        >>> lsm.add_data({
        >>>     # 1
        >>>     "english": ["brilliance outer jacket artist flat mosquito recover restrict official gas ratio publish domestic realize pure offset obstacle thigh favorite demonstration revive nest reader slide pudding symptom ballot auction characteristic complete Mars ridge student explosion dive emphasis the buy perfect motif penny a errand to fur far spirit random integration of with"],
        >>> 
        >>>     # 2
        >>>     "italian": ["da piazza proposta di legge legare nazionale a volte la salute bar farti farmi il pane aggiunta valore artista chiamata settentrionale scuro buio classe signori investitore in grado di fidanzato tagliare arriva successo altrimenti speciale esattamente definizione sorriso chiamo madre pulire esperto rurale vedo malattia era amici libertà l'account immaginare lingua soldi più perché"],
        >>> })
        >>> print(lsm.categorize_query("Here's to the crazy ones"))
        >>> print(lsm.categorize_query("Potete parlarmi in italiano"))
        [(1, 1.0)]
        [(2, 1.0)]

        .. versionadded:: 0.1.0
        """
        category_refs = []
        LatentSemanticMapping.LSMMapStartTraining(self.map)
        for category in data:
            if category not in self.__dataset:
                self.__dataset[category] = data[category]
                category_refs.append(self.__add_category(category))
            else:
                loc = Foundation.CFLocaleGetSystem()
                text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
                LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(data[category]), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
                LatentSemanticMapping.LSMMapAddText(self.map, text_ref, self.__categories[category])
        LatentSemanticMapping.LSMMapCompile(self.map)
        return category_refs

    def add_text(self, text: str, category: Union[int, str], weight: float = 1):
        """Adds the given text to the specified category, applying an optional weight.

        :param text: The text to add to the dataset
        :type text: str
        :param category: The category to add the text to
        :type category: Union[int, str]
        :param weight: The weight to assign to the text entry, defaults to 1
        :type weight: float, optional
        :raises ValueError: The specified category must be a valid category name or ID

        :Example:

        >>> import PyXA
        >>> lsm = PyXA.XALSM({"colors": [], "numbers": ["One", "Two", "Three"]})
        >>> lsm.add_text("red orange yellow green blue purple", "colors")
        >>> lsm.add_text("white black grey gray brown pink", 1)
        >>> print(lsm.categorize_query("pink"))

        .. versionadded:: 0.1.0
        """
        LatentSemanticMapping.LSMMapStartTraining(self.map)
        if category not in self.__dataset and category not in self.__categories:
            raise ValueError(f"Invalid category: {category}")
            
        loc = Foundation.CFLocaleGetSystem()
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, text, loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
        LatentSemanticMapping.LSMMapAddTextWithWeight(self.map, text_ref, self.__categories[category], weight)
        LatentSemanticMapping.LSMMapCompile(self.map)

    def categorize_query(self, query: str, num_results: int = 1) -> list[tuple[int, float]]:
        """Categorizes the query based on the current weights in the map.

        :param query: The query to categorize
        :type query: str
        :param num_results: The number of categorizations to show, defaults to 1
        :type num_results: int, optional
        :return: A list of tuples identifying categories and their associated score. A higher score indicates better fit. If not matching categorization is found, the list will be empty.
        :rtype: list[tuple[int, float]]

        :Example:

        >>> import PyXA
        >>> dataset = {
        >>>     # 1
        >>>     "color": ["red", "orange", "yellow", "green", "emerald", "blue", "purple", "white", "black", "brown", "pink", "grey", "gray"],
        >>> 
        >>>     # 2
        >>>     "number": ["One Two Three Four Five Six Seven Eight Nine Ten"]
        >>> }
        >>> lsm = PyXA.XALSM(dataset)
        >>> queries = ["emerald green three", "one hundred five", "One o' clock", "sky blue", "ninety nine", "purple pink"]
        >>> 
        >>> for query in queries:
        >>>     category = "Unknown"
        >>>     categorization_tuple = lsm.categorize_query(query)
        >>>     if len(categorization_tuple) > 0:
        >>>         category = list(dataset.keys())[categorization_tuple[0][0] - 1]
        >>>     print(query, "is a", category)
        emerald green three is a color
        one hundred five is a number
        One o' clock is a number
        sky blue is a color
        ninety nine is a number
        purple pink is a color

        .. versionadded:: 0.1.0
        """
        loc = Foundation.CFLocaleGetSystem()
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, query, loc, 0)
        rows = LatentSemanticMapping.LSMResultCreate(None, self.map, text_ref, 10, LatentSemanticMapping.kLSMTextPreserveAcronyms)

        categorization = []
        num_results = min(num_results, LatentSemanticMapping.LSMResultGetCount(rows))
        for i in range(0, num_results):
            category_num = LatentSemanticMapping.LSMResultGetCategory(rows, i)
            score = LatentSemanticMapping.LSMResultGetScore(rows, i)
            categorization.append((category_num, score))
        return categorization




class XAColorList(XATextList):
    """A wrapper around lists of colors that employs fast enumeration techniques.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAColor, filter)

class XAColor(XAObject, XAClipboardCodable):
    def __init__(self, *args):
        if len(args) == 0:
            # No color specified -- default to white
            self.xa_elem = XAColor.white_color().xa_elem
        elif len(args) == 1 and isinstance(args[0], AppKit.NSColor):
            # Initialize copy of non-mutable NSColor object
            self.copy_color(args[0])
        elif len(args) == 1 and isinstance(args[0], XAColor):
            # Initialize copy of another XAColor object
            self.copy_color(args[0].xa_elem)
        else:
            # Initialize from provided RGBA values
            red = args[0] if len(args) >= 0 else 255
            green = args[1] if len(args) >= 1 else 255
            blue = args[2] if len(args) >= 3 else 255
            alpha = args[3] if len(args) == 4 else 1.0
            self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)

    def red() -> 'XAColor':
        """Initializes and returns a pure red :class:`XAColor` object.

        .. versionadded:: 0.1.0
        """
        return XAColor(65535, 0, 0)

    def orange() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (1.0, 0.5, 0.0).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.orangeColor())

    def yellow() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (1.0, 1.0, 0.0).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.yellowColor())

    def green() -> 'XAColor':
        """Initializes and returns a pure green :class:`XAColor` object.

        .. versionadded:: 0.1.0
        """
        return XAColor(0, 65535, 0)

    def cyan() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (0.0, 1.0, 1.0).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.cyanColor())

    def blue() -> 'XAColor':
        """Initializes and returns a pure blue :class:`XAColor` object.

        .. versionadded:: 0.1.0
        """
        return XAColor(0, 0, 65535)

    def magenta() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (1.0, 0.0, 1.0).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.magentaColor())

    def purple() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (0.5, 0.0, 0.5).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.purpleColor())

    def brown() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (0.6, 0.4, 0.2).

        .. versionadded:: 0.1.0
        """
        return XAColor(AppKit.NSColor.brownColor())

    def white() -> 'XAColor':
        """Initializes and returns a pure white :class:`XAColor` object.

        .. versionadded:: 0.1.0
        """
        return XAColor(65535, 65535, 65535)

    def gray() -> 'XAColor':
        """Initializes and returns an :class:`XAColor` object whose RGB values are (0.5, 0.5, 0.5).

        .. versionadded:: 0.1.0
        """
        return XAColor(0.5, 0.5, 0.5)

    def black() -> 'XAColor':
        """Initializes and returns a pure black :class:`XAColor` object.

        .. versionadded:: 0.1.0
        """
        return XAColor(0, 0, 0)

    def clear() -> 'XAColor':
        """Initializes and returns a an :class:`XAColor` object whose alpha value is 0.0.

        .. versionadded:: 0.1.0
        """
        return XAColor(0, 0, 0, 0)

    @property
    def red_value(self) -> float:
        """The red value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.redComponent()

    @red_value.setter
    def red_value(self, red_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red_value, self.green_value, self.blue_value, self.alpha_value)

    @property
    def green_value(self) -> float:
        """The green value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.greenComponent()

    @green_value.setter
    def green_value(self, green_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, green_value, self.blue_value, self.alpha_value)

    @property
    def blue_value(self) -> float:
        """The blue value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.blueComponent()

    @blue_value.setter
    def blue_value(self, blue_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, self.green_value, blue_value, self.alpha_value)

    @property
    def alpha_value(self) -> float:
        """The alpha value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.alphaComponent()

    @alpha_value.setter
    def alpha_value(self, alpha_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, self.green_value, self.blue_value, alpha_value)

    @property
    def hue_value(self):
        """The hue value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.hueComponent()

    @hue_value.setter
    def hue_value(self, hue_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(hue_value, self.saturation_value, self.brightness_value, self.alpha_value)

    @property
    def saturation_value(self):
        """The staturation value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.saturationComponent()

    @saturation_value.setter
    def saturation_value(self, saturation_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(self.hue_value, saturation_value, self.brightness_value, self.alpha_value)

    @property
    def brightness_value(self):
        """The brightness value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.brightnessComponent()

    @brightness_value.setter
    def brightness_value(self, brightness_value: float):
        self.xa_elem = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(self.hue_value, self.saturation_value, brightness_value, self.alpha_value)

    def copy_color(self, color: AppKit.NSColor) -> 'XAColor':
        """Initializes a XAColor copy of an NSColor object.

        :param color: The NSColor to copy
        :type color: AppKit.NSColor
        :return: The newly created XAColor object
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(
            color.redComponent(),
            color.greenComponent(),
            color.blueComponent(),
            color.alphaComponent()
        )
        return self
    
    def set_rgba(self, red: float, green: float, blue: float, alpha: float) -> 'XAColor':
        """Sets the RGBA values of the color.

        :param red: The red value of the color, from 0.0 to 1.0
        :type red: float
        :param green: The green value of the color, from 0.0 to 1.0
        :type green: float
        :param blue: The blue value of the color, from 0.0 to 1.0
        :type blue: float
        :param alpha: The opacity of the color, from 0.0 to 1.0
        :type alpha: float
        :return: The XAColor object
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        self.xa_elem = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)
        return self

    def set_hsla(self, hue: float, saturation: float, brightness: float, alpha: float) -> 'XAColor':
        """Sets the HSLA values of the color.

        :param hue: The hue value of the color, from 0.0 to 1.0
        :type hue: float
        :param saturation: The saturation value of the color, from 0.0 to 1.0
        :type saturation: float
        :param brightness: The brightness value of the color, from 0.0 to 1.0
        :type brightness: float
        :param alpha: The opacity of the color, from 0.0 to 1.0
        :type alpha: float
        :return: The XAColor object
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        self.xa_elem = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha)
        return self

    def mix_with(self, color: 'XAColor', fraction: int = 0.5) -> 'XAColor':
        """Blends this color with the specified fraction of another.

        :param color: The color to blend this color with
        :type color: XAColor
        :param fraction: The fraction of the other color to mix into this color, from 0.0 to 1.0, defaults to 0.5
        :type fraction: int, optional
        :return: The resulting color after mixing
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        new_color = self.xa_elem.blendedColorWithFraction_ofColor_(fraction, color.xa_elem)
        return XAColor(new_color.redComponent(), new_color.greenComponent(), new_color.blueComponent(), new_color.alphaComponent())

    def brighten(self, fraction: float = 0.5) -> 'XAColor':
        """Brightens the color by mixing the specified fraction of the system white color into it.

        :param fraction: The amount (fraction) of white to mix into the color, defaults to 0.5
        :type fraction: float, optional
        :return: The resulting color after brightening
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        self.xa_elem = self.xa_elem.highlightWithLevel_(fraction)
        return self

    def darken(self, fraction: float = 0.5) -> 'XAColor':
        """Darkens the color by mixing the specified fraction of the system black color into it.

        :param fraction: The amount (fraction) of black to mix into the color, defaults to 0.5
        :type fraction: float, optional
        :return: The resulting color after darkening
        :rtype: XAColor

        .. versionadded:: 0.1.0
        """
        self.xa_elem = self.xa_elem.shadowWithLevel_(fraction)
        return self

    def make_swatch(self, width: int = 100, height: int = 100) -> 'XAImage':
        """Creates an image swatch of the color with the specified dimensions.

        :param width: The width of the swatch image, in pixels, defaults to 100
        :type width: int, optional
        :param height: The height of the swatch image, in pixels, defaults to 100
        :type height: int, optional
        :return: The image swatch as an XAImage object
        :rtype: XAImage

        :Example: View swatches in Preview

        >>> import PyXA
        >>> from time import sleep
        >>> 
        >>> blue = PyXA.XAColor.blue()
        >>> red = PyXA.XAColor.red()
        >>> 
        >>> swatches = [
        >>>     blue.make_swatch(),
        >>>     blue.darken(0.5).make_swatch(),
        >>>     blue.mix_with(red).make_swatch()
        >>> ]
        >>> 
        >>> for swatch in swatches:
        >>>     swatch.show_in_preview()
        >>>     sleep(0.2)

        .. versionadded:: 0.1.0
        """
        img = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(width, height))
        img.lockFocus()
        self.xa_elem.drawSwatchInRect_(AppKit.NSMakeRect(0, 0, width, height))
        img.unlockFocus()
        return XAImage(img)

    def get_clipboard_representation(self) -> AppKit.NSColor:
        """Gets a clipboard-codable representation of the color.

        When the clipboard content is set to a color, the raw color data is added to the clipboard.

        :return: The raw color data
        :rtype: AppKit.NSColor

        .. versionadded:: 0.1.0
        """
        return self.xa_elem

    def __repr__(self):
        return f"<{str(type(self))}r={str(self.red_value)}, g={self.green_value}, b={self.blue_value}, a={self.alpha_value}>"




# TODO: Init NSLocation object
class XALocation(XAObject):
    """A location with a latitude and longitude, along with other data.

    .. versionadded:: 0.0.2
    """
    current_location: 'XALocation' #: The current location of the device

    def __init__(self, raw_value: CoreLocation.CLLocation = None, title: str = None, latitude: float = 0, longitude: float = 0, altitude: float = None, radius: int = 0, address: str = None):
        self.raw_value = raw_value #: The raw CLLocation object
        self.title = title #: The name of the location
        self.latitude = latitude #: The latitude of the location
        self.longitude = longitude #: The longitude of the location
        self.altitude = altitude #: The altitude of the location
        self.radius = radius #: The horizontal accuracy of the location measurement
        self.address = address #: The addres of the location

    @property
    def raw_value(self) -> CoreLocation.CLLocation: 
        return self.__raw_value

    @raw_value.setter
    def raw_value(self, raw_value: CoreLocation.CLLocation):
        self.__raw_value = raw_value
        if raw_value is not None:
            self.latitude = raw_value.coordinate()[0]
            self.longitude = raw_value.coordinate()[1]
            self.altitude = raw_value.altitude()
            self.radius = raw_value.horizontalAccuracy()

    @property
    def current_location(self) -> 'XALocation':
        self.raw_value = None
        self._spawn_thread(self.__get_current_location)
        while self.raw_value is None:
            time.sleep(0.01)
        return self

    def show_in_maps(self):
        """Shows the location in Maps.app.

        .. versionadded:: 0.0.6
        """
        XAURL(f"maps://?q={self.title},ll={self.latitude},{self.longitude}").open()

    def __get_current_location(self):
        location_manager = CoreLocation.CLLocationManager.alloc().init()
        old_self = self
        class CLLocationManagerDelegate(AppKit.NSObject):
            def locationManager_didUpdateLocations_(self, manager, locations):
                if locations is not None:
                    old_self.raw_value = locations[0]
                    AppHelper.stopEventLoop()

            def locationManager_didFailWithError_(self, manager, error):
                print(manager, error)

        location_manager.requestWhenInUseAuthorization()
        location_manager.setDelegate_(CLLocationManagerDelegate.alloc().init().retain())
        location_manager.requestLocation()

        AppHelper.runConsoleEventLoop()

    def __repr__(self):
        return "<" + str(type(self)) + str((self.latitude, self.longitude)) + ">"
        
    


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
        self.buttons: list[str] = buttons

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
    def __init__(self, text: str = "", title: Union[str, None] = None, buttons: Union[None, list[Union[str, int]]] = None, hidden_answer: bool = False, default_button: Union[str, int, None] = None, cancel_button: Union[str, int, None] = None, icon: Union[Literal["stop", "note", "caution"], None] = None, default_answer: Union[str, int, None] = None):
        super().__init__()
        self.text: str = text
        self.title: str = title
        self.buttons: Union[None, list[Union[str, int]]] = buttons or []
        self.hidden_answer: bool = hidden_answer
        self.icon: Union[str, None] = icon
        self.default_button: Union[str, int, None] = default_button
        self.cancel_button: Union[str, int, None] = cancel_button
        self.default_answer: Union[str, int, None] = default_answer

    def display(self) -> Union[str, int, None, list[str]]:
        """Displays the dialog, waits for the user to select an option or cancel, then returns the selected button or None if cancelled.

        :return: The selected button or None if no value was selected
        :rtype: Union[str, int, None, list[str]]

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

        script = AppleScript(f"""
        tell application "Terminal"
            display dialog \"{self.text}\" with title \"{self.title}\" buttons {buttons} {default_button_str} {cancel_button_str} {icon_str} {default_answer_str} hidden answer {self.hidden_answer}
        end tell
        """)

        result = script.run()["event"]
        if result is not None:
            if result.numberOfItems() > 1:
                return [result.descriptorAtIndex_(1).stringValue(), result.descriptorAtIndex_(2).stringValue()]
            else:
                return result.descriptorAtIndex_(1).stringValue()
                



class XAMenu(XAObject):
    """A custom list item selection menu.

    .. versionadded:: 0.0.8
    """
    def __init__(self, menu_items: list[Any], title: str = "Select Item", prompt: str = "Select an item", default_items: Union[list[str], None] = None, ok_button_name: str = "Okay", cancel_button_name: str = "Cancel", multiple_selections_allowed: bool = False, empty_selection_allowed: bool = False):
        super().__init__()
        self.menu_items: list[Union[str, int]] = menu_items #: The items the user can choose from
        self.title: str = title #: The title of the dialog window
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.default_items: list[str] = default_items or [] #: The items to initially select
        self.ok_button_name: str = ok_button_name #: The name of the OK button
        self.cancel_button_name: str = cancel_button_name #: The name of the Cancel button
        self.multiple_selections_allowed: bool = multiple_selections_allowed #: Whether multiple items can be selected
        self.empty_selection_allowed: bool = empty_selection_allowed #: Whether the user can click OK without selecting anything

    def display(self) -> Union[str, int, bool, list[str], list[int]]:
        """Displays the menu, waits for the user to select an option or cancel, then returns the selected value or False if cancelled.

        :return: The selected value or False if no value was selected
        :rtype: Union[str, int, bool, list[str], list[int]]

        .. versionadded:: 0.0.8
        """
        menu_items = [x.replace("'", "") for x in self.menu_items]
        menu_items = str(menu_items).replace("'", '"')
        default_items = str(self.default_items).replace("'", '"')
        script = AppleScript(f"""
        tell application "Terminal"
            choose from list {menu_items} with title \"{self.title}\" with prompt \"{self.prompt}\" default items {default_items} OK button name \"{self.ok_button_name}\" cancel button name \"{self.cancel_button_name}\" multiple selections allowed {self.multiple_selections_allowed} empty selection allowed {self.empty_selection_allowed}
        end tell
        """)
        result = script.run()["event"]
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
    def __init__(self, prompt: str = "Choose File", types: list[str] = None, default_location: Union[str, None] = None, show_invisibles: bool = False, multiple_selections_allowed: bool = False, show_package_contents: bool = False):
        super().__init__()
        self.prompt: str = prompt #: The prompt to display in the dialog box
        self.types: list[str] = types #: The file types/type identifiers to allow for selection
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

        script = AppleScript(f"""
        tell application "Terminal"
            choose file with prompt \"{self.prompt}\" {types_str}{default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """)
        result = script.run()["event"]

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

        script = AppleScript(f"""
        tell application "Terminal"
            choose folder with prompt \"{self.prompt}\" {default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """)
        result = script.run()["event"]
        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(XAPath(desc.fileURLValue()))
                return values
            else:
                return XAPath(result.fileURLValue())




class XAApplicationPicker(XAObject):
    """An application selection window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, title: Union[str, None] = None, prompt: Union[str, None] = None, multiple_selections_allowed: bool = False):
        super().__init__()
        self.title: str = title #: The dialog window title
        self.prompt: str = prompt #: The prompt to be displayed in the dialog box
        self.multiple_selections_allowed: bool = multiple_selections_allowed #: Whether to allow multiple items to be selected

    def display(self) -> str:
        """Displays the application chooser, waits for the user to select an application or cancel, then returns the selected application's name or None if cancelled.

        :return: The name of the selected application
        :rtype: str

        .. versionadded:: 0.0.8
        """

        script = AppleScript("tell application \"Terminal\"")
        dialog_str = "choose application "
        if self.title is not None:
            dialog_str += f"with title \"{self.title}\" "
        if self.prompt is not None:
            dialog_str += f"with prompt \"{self.prompt}\""
        dialog_str += f"multiple selections allowed {self.multiple_selections_allowed} "
        script.add(dialog_str)
        script.add("end tell")

        return script.run()["string"]




class XAFileNameDialog(XAObject):
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

        script = AppleScript(f"""
        tell application "Terminal"
            choose file name with prompt \"{self.prompt}\" default name \"{self.default_name}\" {default_location_str}
        end tell
        """)
        result = script.run()["event"]
        if result is not None:
            return XAPath(result.fileURLValue())




class XAMenuBar(XAObject):
    def __init__(self):
        """Creates a new menu bar object for interacting with the system menu bar.

        .. versionadded:: 0.0.9
        """
        self._menus = {}
        self._menu_items = {}
        self._methods = {}

        detector = self
        class MyApplicationAppDelegate(AppKit.NSObject):
            start_time = datetime.now()

            def applicationDidFinishLaunching_(self, sender):
                for item_name, status_item in detector._menus.items():
                    menu = status_item.menu()

                    menuitem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
                    menu.addItem_(menuitem)

            def action_(self, menu_item):
                selection = menu_item.title()
                for item_name in detector._methods:
                    if selection == item_name:
                        detector._methods[item_name]()

        app = AppKit.NSApplication.sharedApplication()
        app.setDelegate_(MyApplicationAppDelegate.alloc().init().retain())

    def add_menu(self, title: str, image: Union['XAImage', None] = None, tool_tip: Union[str, None] = None, img_width: int = 30, img_height: int = 30):
        """Adds a new menu to be displayed in the system menu bar.

        :param title: The name of the menu
        :type title: str
        :param image: The image to display for the menu, defaults to None
        :type image: Union[XAImage, None], optional
        :param tool_tip: The tooltip to display on hovering over the menu, defaults to None
        :type tool_tip: Union[str, None], optional
        :param img_width: The width of the image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> img = PyXA.XAImage("/Users/steven/Downloads/Blackness.jpg")
        >>> menu_bar.add_menu("Menu 1", image=img, img_width=100, img_height=100)
        >>> menu_bar.display()

        .. versionadded:: 0.0.9
        """
        status_bar = AppKit.NSStatusBar.systemStatusBar()
        status_item = status_bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength).retain()
        status_item.setTitle_(title)
       
        if isinstance(image, XAImage):
            img = image.xa_elem.copy()
            img.setScalesWhenResized_(True)
            img.setSize_((img_width, img_height))
            status_item.button().setImage_(img)

        status_item.setHighlightMode_(objc.YES)

        if isinstance(tool_tip, str):
            status_item.setToolTip_(tool_tip)

        menu = AppKit.NSMenu.alloc().init()
        status_item.setMenu_(menu)

        status_item.setEnabled_(objc.YES)
        self._menus[title] = status_item

    def add_item(self, menu: str, item_name: str, method: Union[Callable[[], None], None] = None, image: Union['XAImage', None] = None, img_width: int = 20, img_height: int = 20):
        """Adds an item to a menu, creating the menu if necessary.

        :param menu: The name of the menu to add an item to, or the name of the menu to create
        :type menu: str
        :param item_name: The name of the item
        :type item_name: str
        :param method: The method to associate with the item (the method called when the item is clicked)
        :type method: Callable[[], None]
        :param image: The image for the item, defaults to None
        :type image: Union[XAImage, None], optional
        :param img_width: The width of image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> 
        >>> menu_bar.add_menu("Menu 1")
        >>> menu_bar.add_item(menu="Menu 1", item_name="Item 1", method=lambda : print("Action 1"))
        >>> menu_bar.add_item(menu="Menu 1", item_name="Item 2", method=lambda : print("Action 2"))
        >>> 
        >>> menu_bar.add_item(menu="Menu 2", item_name="Item 1", method=lambda : print("Action 1"))
        >>> img = PyXA.XAImage("/Users/exampleUser/Downloads/example.jpg")
        >>> menu_bar.add_item("Menu 2", "Item 1", lambda : print("Action 1"), image=img, img_width=100)
        >>> menu_bar.display()

        .. versionadded:: 0.0.9
        """
        item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(item_name, 'action:', '')
        
        if isinstance(image, XAImage):
            img = image.xa_elem.copy()
            img.setScalesWhenResized_(True)
            img.setSize_((img_width, img_height))
            item.setImage_(img)
        
        if menu not in self._menus:
            self.add_menu(menu)
        self._menu_items[item_name] = item
        self._menus[menu].menu().addItem_(item)
        self._methods[item_name] = method

    def set_image(self, item_name: str, image: 'XAImage', img_width: int = 30, img_height: int = 30):
        """Sets the image displayed for a menu or menu item.

        :param item_name: The name of the item to update
        :type item_name: str
        :param image: The image to display
        :type image: XAImage
        :param img_width: The width of the image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example: Set Image on State Change

        >>> import PyXA
        >>> current_state = True # On
        >>> img_on = PyXA.XAImage("/Users/exampleUser/Documents/on.jpg")
        >>> img_off = PyXA.XAImage("/Users/exampleUser/Documents/off.jpg")
        >>> menu_bar = PyXA.XAMenuBar()
        >>> menu_bar.add_menu("Status", image=img_on)
        >>> 
        >>> def update_state():
        >>>     global current_state
        >>>     if current_state is True:
        >>>         # ... (Actions for turning off)
        >>>         menu_bar.set_text("Turn off", "Turn on")
        >>>         menu_bar.set_image("Status", img_off)
        >>>         current_state = False
        >>>     else:
        >>>         # ... (Actions for turning on)
        >>>         menu_bar.set_text("Turn off", "Turn off")
        >>>         menu_bar.set_image("Status", img_on)
        >>>         current_state = True

        menu_bar.add_item("Status", "Turn off", update_state)
        menu_bar.display()

        .. versionadded:: 0.0.9
        """
        img = image.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_((img_width, img_height))
        if item_name in self._menus:
            self._menus[item_name].button().setImage_(img)
        elif item_name in self._methods:
            self._menu_items[item_name].setImage_(img)

    def set_text(self, item_name: str, text: str):
        """Sets the text displayed for a menu or menu item.

        :param item_name: The name of the item to update
        :type item_name: str
        :param text: The new text to display
        :type text: str

        :Example: Random Emoji Ticker

        >>> import PyXA
        >>> import random
        >>> import threading
        >>> 
        >>> menu_bar = PyXA.XAMenuBar()
        >>> menu_bar.add_menu("Emoji")
        >>>
        >>> emojis = ["😀", "😍", "🙂", "😎", "🤩", "🤯", "😭", "😱", "😴", "🤒", "😈", "🤠"]
        >>>
        >>> def update_display():
        >>>     while True:
        >>>         new_emoji = random.choice(emojis)
        >>>         menu_bar.set_text("Emoji", new_emoji)
        >>>         sleep(0.25)
        >>> 
        >>> emoji_ticker = threading.Thread(target=update_display)
        >>> emoji_ticker.start()
        >>> menu_bar.display()

        .. versionadded:: 0.0.9
        """
        if item_name in self._menus:
            self._menus[item_name].setTitle_(text)
        elif item_name in self._methods:
            self._menu_items[item_name].setTitle_(text)
            self._methods[text] = self._methods[item_name]

    def display(self):
        """Displays the custom menus on the menu bar.

        :Example:

        >>> import PyXA
        >>> mbar = PyXA.XAMenuBar()
        >>> mbar.add_menu("🔥")
        >>> mbar.display()

        .. versionadded:: 0.0.9
        """
        try:
            AppHelper.runEventLoop(installInterrupt=True)
        except Exception as e:
            print(e)




#############################
### System / Image Events ###
#############################
# ? Move into separate XAFileSystemBase.py file?
class XAEventsApplication(XACanOpenPath):
    """A base class for the System and Image events applications.

    .. versionadded:: 0.1.0
    """
    class Format(Enum):
        """Disk format options.
        """
        APPLE_PHOTO     = OSType("dfph")
        APPLESHARE      = OSType("dfas")
        AUDIO           = OSType("dfau")
        HIGH_SIERRA     = OSType("dfhs")
        ISO_9660        = OSType("fd96")
        MACOS_EXTENDED  = OSType("dfh+")
        MACOS           = OSType("dfhf")
        MSDOS           = OSType("dfms")
        NFS             = OSType("dfnf")
        PRODOS          = OSType("dfpr")
        QUICKTAKE       = OSType("dfqt")
        UDF             = OSType("dfud")
        UFS             = OSType("dfuf")
        UNKNOWN         = OSType("df$$")
        WEBDAV          = OSType("dfwd")

class XADiskItemList(XAList):
    """A wrapper around lists of disk items that employs fast enumeration techniques.

    All properties of disk items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XADiskItem
        super().__init__(properties, object_class, filter)

    def busy_status(self) -> list['bool']:
        """Retrieves the busy status of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("busyStatus"))

    def container(self) -> 'XADiskItemList':
        """Retrieves the containing folder or disk of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XADiskItemList)

    def creation_date(self) -> list['datetime']:
        """Retrieves the creation date of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def displayed_name(self) -> list['str']:
        """Retrieves the displayed name of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def id(self) -> list['str']:
        """Retrieves the unique ID of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def modification_date(self) -> list['datetime']:
        """Retrieves the last modified date of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def name(self) -> list['str']:
        """Retrieves the name of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def name_extension(self) -> list['str']:
        """Retrieves the name extension of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("nameExtension"))

    def package_folder(self) -> list['bool']:
        """Retrieves the package folder status of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("packageFolder"))

    def path(self) -> list['XAPath']:
        """Retrieves the file system path of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XAPath(x) for x in ls]

    def physical_size(self) -> list['int']:
        """Retrieves the actual disk space used by each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize"))

    def posix_path(self) -> list[XAPath]:
        """Retrieves the POSIX file system path of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("POSIXPath")
        return [XAPath(x) for x in ls]

    def size(self) -> list['int']:
        """Retrieves the logical size of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def url(self) -> list['XAURL']:
        """Retrieves the URL of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("URL")
        return [XAURL(x) for x in ls]

    def visible(self) -> list['bool']:
        """Retrieves the visible status of each item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def volume(self) -> list['str']:
        """Retrieves the volume on which each item in the list resides.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("volume"))

    def by_busy_status(self, busy_status: bool) -> 'XADiskItem':
        """Retrieves item whose busy status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("busyStatus", busy_status)

    def by_container(self, container: 'XADiskItem') -> 'XADiskItem':
        """Retrieves item whose container matches the given disk item.

        .. versionadded:: 0.1.0
        """
        return self.by_property("container", container.xa_elem)

    def by_creation_date(self, creation_date: datetime) -> 'XADiskItem':
        """Retrieves item whose creation date matches the given date.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creationDate", creation_date)

    def by_displayed_name(self, displayed_name: str) -> 'XADiskItem':
        """Retrieves item whose displayed name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("displayedName", displayed_name)

    def by_id(self, id: str) -> 'XADiskItem':
        """Retrieves item whose ID matches the given ID.

        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_modification_date(self, modification_date: datetime) -> 'XADiskItem':
        """Retrieves item whose date matches the given date.

        .. versionadded:: 0.1.0
        """
        return self.by_property("modificationDate", modification_date)

    def by_name(self, name: str) -> 'XADiskItem':
        """Retrieves item whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_name_extension(self, name_extension: str) -> 'XADiskItem':
        """Retrieves item whose name extension matches the given extension.

        .. versionadded:: 0.1.0
        """
        return self.by_property("nameExtension", name_extension)

    def by_package_folder(self, package_folder: bool) -> 'XADiskItem':
        """Retrieves item whose package folder status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("packageFolder", package_folder)

    def by_path(self, path: Union[XAPath, str]) -> 'XADiskItem':
        """Retrieves item whose path matches the given path.

        .. versionadded:: 0.1.0
        """
        if isinstance(path, XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_physical_size(self, physical_size: int) -> 'XADiskItem':
        """Retrieves item whose physical size matches the given size.

        .. versionadded:: 0.1.0
        """
        return self.by_property("physicalSize", physical_size)

    def by_posix_path(self, posix_path: Union[XAPath, str]) -> 'XADiskItem':
        """Retrieves item whose POSIX path matches the given POSIX path.

        .. versionadded:: 0.1.0
        """
        if isinstance(posix_path, XAPath):
            posix_path = posix_path.path
        return self.by_property("POSIXPath", posix_path)

    def by_size(self, size: int) -> 'XADiskItem':
        """Retrieves item whose size matches the given size.

        .. versionadded:: 0.1.0
        """
        return self.by_property("size", size)

    def by_url(self, url: XAURL) -> 'XADiskItem':
        """Retrieves the item whose URL matches the given URL.

        .. versionadded:: 0.1.0
        """
        return self.by_property("URL", url.xa_elem)

    def by_visible(self, visible: bool) -> 'XADiskItem':
        """Retrieves the item whose visible status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("visible", visible)

    def by_volume(self, volume: str) -> 'XADiskItem':
        """Retrieves the item whose volume matches the given volume.

        .. versionadded:: 0.1.0
        """
        return self.by_property("volume", volume)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XADiskItem(XAObject, XAPathLike):
    """An item stored in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def busy_status(self) -> 'bool':
        """Whether the disk item is busy.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.busyStatus()

    @property
    def container(self) -> 'XADiskItem':
        """The folder or disk which has this disk item as an element.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.container(), XADiskItem)

    @property
    def creation_date(self) -> 'datetime':
        """The date on which the disk item was created.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creationDate()

    @property
    def displayed_name(self) -> 'str':
        """The name of the disk item as displayed in the User Interface.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.displayedName()

    @property
    def id(self) -> 'str':
        """The unique ID of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def modification_date(self) -> 'datetime':
        """The date on which the disk item was last modified.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.modificationDate()

    @property
    def name(self) -> 'str':
        """The name of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def name_extension(self) -> 'str':
        """The extension portion of the name.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.nameExtension()

    @property
    def package_folder(self) -> 'bool':
        """Whether the disk item is a package.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.packageFolder()

    @property
    def path(self) -> 'XAPath':
        """The file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAPath(self.xa_elem.path())

    @property
    def physical_size(self) -> 'int':
        """The actual space used by the disk item on disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.physicalSize()

    @property
    def posix_path(self) -> XAPath:
        """The POSIX file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAPath(self.xa_elem.POSIXPath())

    @property
    def size(self) -> 'int':
        """The logical size of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.size()

    @property
    def url(self) -> 'XAURL':
        """The URL of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAURL(self.xa_elem.URL())

    @property
    def visible(self) -> 'bool':
        """Whether the disk item is visible.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.visible()

    @property
    def volume(self) -> 'str':
        """The volume on which the disk item resides.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.volume()

    def get_path_representation(self) -> XAPath:
        return self.posix_path

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAAliasList(XADiskItemList):
    """A wrapper around lists of aliases that employs fast enumeration techniques.

    All properties of aliases can be called as methods on the wrapped list, returning a list containing each alias' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAlias)

    def creator_type(self) -> list['str']:
        """Retrieves the OSType identifying the application that created each alias in the list

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def default_application(self) -> 'XADiskItemList':
        """Retrieves the applications that will launch if each alias in the list is opened.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication")
        return self._new_element(ls, XADiskItemList)

    def file_type(self) -> list['str']:
        """Retrieves the OSType identifying the type of data contained in each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def kind(self) -> list['str']:
        """Retrieves the kind of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def product_version(self) -> list['str']:
        """Retrieves the product version of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def short_version(self) -> list['str']:
        """Retrieves the short version of the application bundle referenced by each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion"))

    def stationery(self) -> list['bool']:
        """Retrieves the stationery status of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def type_identifier(self) -> list['str']:
        """Retrieves the type identifier of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier"))

    def version(self) -> list['str']:
        """Retrieves the version of the application bundle referenced by each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_creator_type(self, creator_type: str) -> 'XAAlias':
        """Retrieves the alias whose creator type matches the given creator type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creatorType", creator_type)

    def by_default_application(self, default_application: 'XADiskItem') -> 'XAAlias':
        """Retrieves the alias whose default application matches the given application.

        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> 'XAAlias':
        """Retrieves the alias whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> 'XAAlias':
        """Retrieves the alias whose kind matches the given kind.

        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> 'XAAlias':
        """Retrieves the alias whose product version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> 'XAAlias':
        """Retrieves the alias whose short version matches the given text.

        .. versionadded:: 0.1.0
        """
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> 'XAAlias':
        """Retrieves the alias whose stationery status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> 'XAAlias':
        """Retrieves the alias whose type identifier matches the given type identifier.

        .. versionadded:: 0.1.0
        """
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> 'XAAlias':
        """Retrieves the alias whose version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("version", version)

class XAAlias(XADiskItem):
    """An alias in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> 'str':
        """The OSType identifying the application that created the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> 'XADiskItem':
        """The application that will launch if the alias is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XADiskItem)

    @property
    def file_type(self) -> 'str':
        """The OSType identifying the type of data contained in the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> 'str':
        """The kind of alias, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> 'str':
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> 'str':
        """The short version of the application bundle referenced by the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> 'bool':
        """Whether the alias is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> 'str':
        """The type identifier of the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> 'str':
        """The version of the application bundle referenced by the alias (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()

    def aliases(self, filter: Union[dict, None] = None) -> 'XAAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XADiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)




class XADiskList(XADiskItemList):
    """A wrapper around lists of disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XADisk)

    def capacity(self) -> list['float']:
        """Retrieves the total number of bytes (free or used) on each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("capacity"))

    def ejectable(self) -> list['bool']:
        """Retrieves the ejectable status of each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable"))

    def format(self) -> list['XAEventsApplication.Format']:
        """Retrieves the file system format of each disk in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAEventsApplication.Format(OSType(x.stringValue())) for x in ls]

    def free_space(self) -> list['float']:
        """Retrieves the number of free bytes left on each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace"))

    def ignore_privileges(self) -> list['bool']:
        """Retrieves the ignore privileges status for each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ignorePrivileges"))

    def local_volume(self) -> list['bool']:
        """Retrieves the local volume status for each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume"))

    def server(self) -> list['str']:
        """Retrieves the server on which each disk in the list resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("server"))

    def startup(self) -> list['bool']:
        """Retrieves the startup disk status of each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("startup"))

    def zone(self) -> list['str']:
        """Retrieves the zone in which each disk's server resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zone"))

    def by_capacity(self, capacity: float) -> 'XADisk':
        """Retrieves the disk whose capacity matches the given capacity.

        .. versionadded:: 0.1.0
        """
        return self.by_property("capacity", capacity)

    def by_ejectable(self, ejectable: bool) -> 'XADisk':
        """Retrieves the disk whose ejectable status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("ejectable", ejectable)

    def by_format(self, format: 'XAEventsApplication.Format') -> 'XADisk':
        """Retrieves the disk whose format matches the given format.

        .. versionadded:: 0.1.0
        """
        return self.by_property("format", format.value)

    def by_free_space(self, free_space: float) -> 'XADisk':
        """Retrieves the disk whose free space matches the given amount.

        .. versionadded:: 0.1.0
        """
        return self.by_property("freeSpace", free_space)

    def by_ignore_privileges(self, ignore_privileges: bool) -> 'XADisk':
        """Retrieves the disk whose ignore privileges status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("ignorePrivileges", ignore_privileges)

    def by_local_volume(self, local_volume: bool) -> 'XADisk':
        """Retrieves the disk whose local volume status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("localVolume", local_volume)

    def by_server(self, server: str) -> 'XADisk':
        """Retrieves the disk whose server matches the given server.

        .. versionadded:: 0.1.0
        """
        return self.by_property("server", server)

    def by_startup(self, startup: bool) -> 'XADisk':
        """Retrieves the disk whose startup status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("startup", startup)

    def by_zone(self, zone: str) -> 'XADisk':
        """Retrieves the disk whose zone matches the given zone.

        .. versionadded:: 0.1.0
        """
        return self.by_property("zone", zone)

class XADisk(XADiskItem):
    """A disk in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def capacity(self) -> 'float':
        """The total number of bytes (free or used) on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.capacity()

    @property
    def ejectable(self) -> 'bool':
        """Whether the media can be ejected (floppies, CD's, and so on).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ejectable()

    @property
    def format(self) -> 'XAEventsApplication.Format':
        """The file system format of the disk.

        .. versionadded:: 0.1.0
        """
        return XAEventsApplication.Format(self.xa_elem.format())

    @property
    def free_space(self) -> 'float':
        """The number of free bytes left on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.freeSpace()

    @property
    def ignore_privileges(self) -> 'bool':
        """Whether to ignore permissions on this disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ignorePrivileges()

    @property
    def local_volume(self) -> 'bool':
        """Whether the media is a local volume (as opposed to a file server).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.localVolume()

    @property
    def server(self) -> 'str':
        """The server on which the disk resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.server()

    @property
    def startup(self) -> 'bool':
        """Whether this disk is the boot disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.startup()

    @property
    def zone(self) -> 'str':
        """The zone in which the disk's server resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.zone()

    def aliases(self, filter: Union[dict, None] = None) -> 'XAAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XADiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.fileOackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)




class XADomainList(XAList):
    """A wrapper around lists of domains that employs fast enumeration techniques.

    All properties of domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADomain, filter)

    def id(self) -> list['str']:
        """Retrieves the unique identifier of each domain in the list

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list['str']:
        """Retrieves the name of each domain in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XADomain':
        """Retrieves the domain whose ID matches the given ID.

        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XADomain':
        """Retrieves the domain whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XADomain(XAObject):
    """A domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def application_support_folder(self) -> 'XAFolder':
        """The Application Support folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationSupportFolder(), XAFolder)

    @property
    def applications_folder(self) -> 'XAFolder':
        """The Applications folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationsFolder(), XAFolder)

    @property
    def desktop_pictures_folder(self) -> 'XAFolder':
        """The Desktop Pictures folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopPicturesFolder(), XAFolder)

    @property
    def folder_action_scripts_folder(self) -> 'XAFolder':
        """The Folder Action Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folderActionScriptsFolder(), XAFolder)

    @property
    def fonts_folder(self) -> 'XAFolder':
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAFolder)

    @property
    def id(self) -> 'str':
        """The unique identifier of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def library_folder(self) -> 'XAFolder':
        """The Library folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.libraryFolder(), XAFolder)

    @property
    def name(self) -> 'str':
        """The name of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def preferences_folder(self) -> 'XAFolder':
        """The Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAFolder)

    @property
    def scripting_additions_folder(self) -> 'XAFolder':
        """The Scripting Additions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingAdditionsFolder(), XAFolder)

    @property
    def scripts_folder(self) -> 'XAFolder':
        """The Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptsFolder(), XAFolder)

    @property
    def shared_documents_folder(self) -> 'XAFolder':
        """The Shared Documents folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sharedDocumentsFolder(), XAFolder)

    @property
    def speakable_items_folder(self) -> 'XAFolder':
        """The Speakable Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.speakableItemsFolder(), XAFolder)

    @property
    def utilities_folder(self) -> 'XAFolder':
        """The Utilities folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.utilitiesFolder(), XAFolder)

    @property
    def workflows_folder(self) -> 'XAFolder':
        """The Automator Workflows folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.workflowsFolder(), XAFolder)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAClassicDomainObject(XADomain):
    """The Classic domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def apple_menu_folder(self) -> 'XAFolder':
        """The Apple Menu Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.appleMenuFolder(), XAFolder)

    @property
    def control_panels_folder(self) -> 'XAFolder':
        """The Control Panels folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlPanelsFolder(), XAFolder)

    @property
    def control_strip_modules_folder(self) -> 'XAFolder':
        """The Control Strip Modules folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlStripModulesFolder(), XAFolder)

    @property
    def desktop_folder(self) -> 'XAFolder':
        """The Classic Desktop folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAFolder)

    @property
    def extensions_folder(self) -> 'XAFolder':
        """The Extensions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.extensionsFolder(), XAFolder)

    @property
    def fonts_folder(self) -> 'XAFolder':
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAFolder)

    @property
    def launcher_items_folder(self) -> 'XAFolder':
        """The Launcher Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.launcherItemsFolder(), XAFolder)

    @property
    def preferences_folder(self) -> 'XAFolder':
        """The Classic Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAFolder)

    @property
    def shutdown_folder(self) -> 'XAFolder':
        """The Shutdown Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.shutdownFolder(), XAFolder)

    @property
    def startup_items_folder(self) -> 'XAFolder':
        """The StartupItems folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.startupItemsFolder(), XAFolder)

    @property
    def system_folder(self) -> 'XAFolder':
        """The System folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.systemFolder(), XAFolder)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)




class XAFileList(XADiskItemList):
    """A wrapper around lists of files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XAFile
        super().__init__(properties, filter, object_class)

    def creator_type(self) -> list['str']:
        """Retrieves the OSType identifying the application that created each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def default_application(self) -> 'XADiskItemList':
        """Retrieves the applications that will launch if each file in the list is opened.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication")
        return self._new_element(ls, XADiskItemList)

    def file_type(self) -> list['str']:
        """Retrieves the OSType identifying the type of data contained in each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def kind(self) -> list['str']:
        """Retrieves the kind of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def product_version(self) -> list['str']:
        """Retrieves the product version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def short_version(self) -> list['str']:
        """Retrieves the short version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion"))

    def stationery(self) -> list['bool']:
        """Retrieves the stationery status of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def type_identifier(self) -> list['str']:
        """Retrieves the type identifier of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier"))

    def version(self) -> list['str']:
        """Retrieves the version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_creator_type(self, creator_type: str) -> 'XAFile':
        """Retrieves the file whose creator type matches the given creator type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creatorType", creator_type)

    def by_default_application(self, default_application: 'XADiskItem') -> 'XAFile':
        """Retrieves the file whose default application matches the given application.

        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> 'XAFile':
        """Retrieves the file whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> 'XAFile':
        """Retrieves the file whose kind matches the given kind.

        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> 'XAFile':
        """Retrieves the file whose product version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> 'XAFile':
        """Retrieves the file whose short version matches the given text.

        .. versionadded:: 0.1.0
        """
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> 'XAFile':
        """Retrieves the file whose stationery status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> 'XAFile':
        """Retrieves the file whose type identifier matches the given type identifier.

        .. versionadded:: 0.1.0
        """
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> 'XAFile':
        """Retrieves the file whose version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("version", version)

class XAFile(XADiskItem):
    """A file in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> 'str':
        """The OSType identifying the application that created the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> 'XADiskItem':
        """The application that will launch if the file is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XADiskItem)

    @default_application.setter
    def default_application(self, default_application: XADiskItem):
        self.set_property('defaultApplication', default_application.xa_elem)

    @property
    def file_type(self) -> 'str':
        """The OSType identifying the type of data contained in the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> 'str':
        """The kind of file, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> 'str':
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> 'str':
        """The short version of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> 'bool':
        """Whether the file is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> 'str':
        """The type identifier of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> 'str':
        """The version of the file (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()




class XAFilePackageList(XAFileList):
    """A wrapper around lists of file packages that employs fast enumeration techniques.

    All properties of file packages can be called as methods on the wrapped list, returning a list containing each package's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFilePackage)

class XAFilePackage(XAFile):
    """A file package in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> 'XAAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XADiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)




class XAFolderList(XADiskItemList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folder's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFolder)

class XAFolder(XADiskItem):
    """A folder in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> 'XAAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XADiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XAFolderList

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAFolderList, filter)




class XALocalDomainObject(XADomain):
    """The local domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XANetworkDomainObject(XADomain):
    """The network domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XASystemDomainObject(XADomain):
    """The system domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAUserDomainObject(XADomain):
    """The user domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def desktop_folder(self) -> 'XAFolder':
        """The user's Desktop folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAFolder)

    @property
    def documents_folder(self) -> 'XAFolder':
        """The user's Documents folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.documentsFolder(), XAFolder)

    @property
    def downloads_folder(self) -> 'XAFolder':
        """The user's Downloads folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.downloadsFolder(), XAFolder)

    @property
    def favorites_folder(self) -> 'XAFolder':
        """The user's Favorites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.favoritesFolder(), XAFolder)

    @property
    def home_folder(self) -> 'XAFolder':
        """The user's Home folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.homeFolder(), XAFolder)

    @property
    def movies_folder(self) -> 'XAFolder':
        """The user's Movies folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.moviesFolder(), XAFolder)

    @property
    def music_folder(self) -> 'XAFolder':
        """The user's Music folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.musicFolder(), XAFolder)

    @property
    def pictures_folder(self) -> 'XAFolder':
        """The user's Pictures folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.picturesFolder(), XAFolder)

    @property
    def public_folder(self) -> 'XAFolder':
        """The user's Public folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.publicFolder(), XAFolder)

    @property
    def sites_folder(self) -> 'XAFolder':
        """The user's Sites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sitesFolder(), XAFolder)

    @property
    def temporary_items_folder(self) -> 'XAFolder':
        """The Temporary Items folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.temporaryItemsFolder(), XAFolder)




#############
### Media ###
#############
class XAImageList(XAList, XAClipboardCodable):
    """A wrapper around lists of images that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAImage
        super().__init__(properties, obj_class, filter)

        self.modified = False #: Whether the list of images has been modified since it was initialized

    def __partial_init(self):
        images = [None] * self.xa_elem.count()

        def init_images(ref, index, stop):
            if isinstance(ref, str):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(XAPath(ref).xa_elem)
            elif isinstance(ref, ScriptingBridge.SBObject):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(XAPath(ref.imageFile().POSIXPath()).xa_elem)
            elif isinstance(ref, XAObject):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(ref.image_file.posix_path.xa_elem)
            images[index] = ref

        self.xa_elem.enumerateObjectsUsingBlock_(init_images)
        return AppKit.NSMutableArray.alloc().initWithArray_(images)

    def __apply_filter(self, filter_block, *args):
        images = self.__partial_init()

        filtered_images = [None] * images.count()
        def filter_image(image, index, *args):
            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = filter_block(image, *args)
            filter.setValue_forKey_(img, "inputImage")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2))

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            filtered_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(filter_image, [image, index, *args])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(filtered_images)
        return self

    def file(self) -> list[XAPath]:
        return [x.file for x in self]

    def horizontal_stitch(self) -> 'XAImage':
        """Horizontally stacks each image in the list.

        The first image in the list is placed at the left side of the resulting image.

        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return XAImage.horizontal_stitch(self)

    def vertical_stitch(self) -> 'XAImage':
        """Vertically stacks each image in the list.

        The first image in the list is placed at the bottom side of the resulting image.

        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return XAImage.vertical_stitch(self)

    def additive_composition(self) -> 'XAImage':
        """Creates a composition image by adding the color values of each image in the list.

        :param images: The images to add together
        :type images: list[XAImage]
        :return: The resulting image composition
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image_data = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            if isinstance(image, str):
                image = AppKit.NSImage.alloc().initWithContentsOfURL_(XAPath(image).xa_elem)
            image_data[index] = Quartz.CIImage.imageWithData_(image.TIFFRepresentation())

        current_composition = None
        while len(image_data) > 1:
            img1 = image_data.pop(0)
            img2 = image_data.pop(0)
            composition_filter = Quartz.CIFilter.filterWithName_("CIAdditionCompositing")
            composition_filter.setDefaults()
            composition_filter.setValue_forKey_(img1, "inputImage")
            composition_filter.setValue_forKey_(img2, "inputBackgroundImage")
            current_composition = composition_filter.outputImage()
            image_data.insert(0, current_composition)
            
        composition_rep = AppKit.NSCIImageRep.imageRepWithCIImage_(current_composition)
        composition = AppKit.NSImage.alloc().initWithSize_(composition_rep.size())
        composition.addRepresentation_(composition_rep)
        return XAImage(composition)

    def subtractive_composition(self) -> 'XAImage':
        """Creates a composition image by subtracting the color values of each image in the list successively.

        :param images: The images to create the composition from
        :type images: list[XAImage]
        :return: The resulting image composition
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image_data = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            if isinstance(image, str):
                image = AppKit.NSImage.alloc().initWithContentsOfURL_(XAPath(image).xa_elem)
            image_data[index] = Quartz.CIImage.imageWithData_(image.TIFFRepresentation())

        current_composition = None
        while len(image_data) > 1:
            img1 = image_data.pop(0)
            img2 = image_data.pop(0)
            composition_filter = Quartz.CIFilter.filterWithName_("CISubtractBlendMode")
            composition_filter.setDefaults()
            composition_filter.setValue_forKey_(img1, "inputImage")
            composition_filter.setValue_forKey_(img2, "inputBackgroundImage")
            current_composition = composition_filter.outputImage()
            image_data.insert(0, current_composition)
            
        composition_rep = AppKit.NSCIImageRep.imageRepWithCIImage_(current_composition)
        composition = AppKit.NSImage.alloc().initWithSize_(composition_rep.size())
        composition.addRepresentation_(composition_rep)
        return XAImage(composition)

    def edges(self, intensity: float = 1.0) -> 'XAImageList':
        """Detects the edges in each image of the list and highlights them colorfully, blackening other areas of the images.

        :param intensity: The degree to which edges are highlighted. Higher is brighter. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIEdges")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def gaussian_blur(self, intensity: float = 10) -> 'XAImageList':
        """Blurs each image in the list using a Gaussian filter.

        :param intensity: The strength of the blur effect, defaults to 10
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIGaussianBlur")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def reduce_noise(self, noise_level: float = 0.02, sharpness: float = 0.4) -> 'XAImageList':
        """Reduces noise in each image of the list by sharpening areas with a luminance delta below the specified noise level threshold.

        :param noise_level: The threshold for luminance changes in an area below which will be considered noise, defaults to 0.02
        :type noise_level: float
        :param sharpness: The sharpness of the resulting images, defaults to 0.4
        :type sharpness: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, noise_level, sharpness):
            filter = Quartz.CIFilter.filterWithName_("CINoiseReduction")
            filter.setDefaults()
            filter.setValue_forKey_(noise_level, "inputNoiseLevel")
            filter.setValue_forKey_(sharpness, "inputSharpness")
            return filter

        return self.__apply_filter(filter_block, noise_level, sharpness)

    def pixellate(self, pixel_size: float = 8.0) -> 'XAImageList':
        """Pixellates each image in the list.

        :param pixel_size: The size of the pixels, defaults to 8.0
        :type pixel_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, pixel_size):
            filter = Quartz.CIFilter.filterWithName_("CIPixellate")
            filter.setDefaults()
            filter.setValue_forKey_(pixel_size, "inputScale")
            return filter

        return self.__apply_filter(filter_block, pixel_size)

    def outline(self, threshold: float = 0.1) -> 'XAImageList':
        """Outlines detected edges within each image of the list in black, leaving the rest transparent.

        :param threshold: The threshold to use when separating edge and non-edge pixels. Larger values produce thinner edge lines. Defaults to 0.1
        :type threshold: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, threshold):
            filter = Quartz.CIFilter.filterWithName_("CILineOverlay")
            filter.setDefaults()
            filter.setValue_forKey_(threshold, "inputThreshold")
            return filter

        return self.__apply_filter(filter_block, threshold)

    def invert(self) -> 'XAImageList':
        """Inverts the colors of each image in the list.

        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image):
            filter = Quartz.CIFilter.filterWithName_("CIColorInvert")
            filter.setDefaults()
            return filter

        return self.__apply_filter(filter_block)
    
    def sepia(self, intensity: float = 1.0) -> 'XAImageList':
        """Applies a sepia filter to each image in the list; maps all colors of the images to shades of brown.

        :param intensity: The opacity of the sepia effect. A value of 0 will have no impact on the image. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CISepiaTone")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def vignette(self, intensity: float = 1.0) -> 'XAImageList':
        """Applies vignette shading to the corners of each image in the list.

        :param intensity: The intensity of the vignette effect, defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIVignette")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def depth_of_field(self, focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None] = None, intensity: float = 10.0, focal_region_saturation: float = 1.5) -> 'XAImageList':
        """Applies a depth of field filter to each image in the list, simulating a tilt & shift effect.

        :param focal_region: Two points defining a line within each image to focus the effect around (pixels around the line will be in focus), or None to use the center third of the image, defaults to None
        :type focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None]
        :param intensity: Controls the amount of distance around the focal region to keep in focus. Higher values decrease the distance before the out-of-focus effect starts. Defaults to 10.0
        :type intensity: float
        :param focal_region_saturation: Adjusts the saturation of the focial region. Higher values increase saturation. Defaults to 1.5 (1.5x default saturation)
        :type focal_region_saturation: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, focal_region, intensity, focal_region_saturation):
            if focal_region is None:
                center_top = Quartz.CIVector.vectorWithX_Y_(image.size().width / 2, image.size().height / 3)
                center_bottom = Quartz.CIVector.vectorWithX_Y_(image.size().width / 2, image.size().height / 3 * 2)
                focal_region = (center_top, center_bottom)
            else:
                point1 = Quartz.CIVector.vectorWithX_Y_(focal_region[0])
                point2 = Quartz.CIVector.vectorWithX_Y_(focal_region[1])
                focal_region = (point1, point2)

            filter = Quartz.CIFilter.filterWithName_("CIDepthOfField")
            filter.setDefaults()
            filter.setValue_forKey_(focal_region[0], "inputPoint0")
            filter.setValue_forKey_(focal_region[1], "inputPoint1")
            filter.setValue_forKey_(intensity, "inputRadius")
            filter.setValue_forKey_(focal_region_saturation, "inputSaturation")
            return filter

        return self.__apply_filter(filter_block, focal_region, intensity, focal_region_saturation)

    def crystallize(self, crystal_size: float = 20.0) -> 'XAImageList':
        """Applies a crystallization filter to each image in the list. Creates polygon-shaped color blocks by aggregating pixel values.

        :param crystal_size: The radius of the crystals, defaults to 20.0
        :type crystal_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, crystal_size):
            filter = Quartz.CIFilter.filterWithName_("CICrystallize")
            filter.setDefaults()
            filter.setValue_forKey_(crystal_size, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, crystal_size)

    def comic(self) -> 'XAImageList':
        """Applies a comic filter to each image in the list. Outlines edges and applies a color halftone effect.

        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image):
            filter = Quartz.CIFilter.filterWithName_("CIComicEffect")
            filter.setDefaults()
            return filter

        return self.__apply_filter(filter_block)

    def pointillize(self, point_size: float = 20.0) -> 'XAImageList':
        """Applies a pointillization filter to each image in the list.

        :param crystal_size: The radius of the points, defaults to 20.0
        :type crystal_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, point_size):
            filter = Quartz.CIFilter.filterWithName_("CIPointillize")
            filter.setDefaults()
            filter.setValue_forKey_(point_size, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, point_size)

    def bloom(self, intensity: float = 0.5) -> 'XAImageList':
        """Applies a bloom effect to each image in the list. Softens edges and adds a glow.

        :param intensity: The strength of the softening and glow effects, defaults to 0.5
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIBloom")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def monochrome(self, color: XAColor, intensity: float = 1.0) -> 'XAImageList':
        """Remaps the colors of each image in the list to shades of the specified color.

        :param color: The color of map each images colors to
        :type color: XAColor
        :param intensity: The strength of recoloring effect. Higher values map colors to darker shades of the provided color. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        ci_color = Quartz.CIColor.alloc().initWithColor_(color.xa_elem)

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIColorMonochrome")
            filter.setDefaults()
            filter.setValue_forKey_(ci_color, "inputColor")
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def bump(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, curvature: float = 0.5) -> 'XAImageList':
        """Adds a concave (inward) or convex (outward) bump to each image in the list at the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The radius of the bump in pixels, defaults to 300.0
        :type radius: float
        :param curvature: Controls the direction and intensity of the bump's curvature. Positive values create convex bumps while negative values create concave bumps. Defaults to 0.5
        :type curvature: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        bumped_images = [None] * images.count()
        def bump_image(image, index, center, radius, curvature):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(image.size().width / 2, image.size().height / 2)
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CIBumpDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(radius, "inputRadius")
            filter.setValue_forKey_(curvature, "inputScale")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2))

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            bumped_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(bump_image, [image, index, center, radius, curvature])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(bumped_images)
        return self

    def pinch(self, center: Union[tuple[int, int], None] = None, intensity: float = 0.5) -> 'XAImageList':
        """Adds an inward pinch distortion to each image in the list at the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param intensity: Controls the scale of the pinch effect. Higher values stretch pixels away from the specified center to a greater degree. Defaults to 0.5
        :type intensity: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        pinched_images = [None] * images.count()
        def pinch_image(image, index, center, intensity):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(image.size().width / 2, image.size().height / 2)
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CIPinchDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(intensity, "inputScale")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2))

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            pinched_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(pinch_image, [image, index, center, intensity])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(pinched_images)
        return self

    def twirl(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, angle: float = 3.14) -> 'XAImageList':
        """Adds a twirl distortion to each image in the list by rotating pixels around the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
        :type radius: float
        :param angle: The angle of the twirl in radians, defaults to 3.14
        :type angle: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        twirled_images = [None] * images.count()
        def twirl_image(image, index, center, radius, angle):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(image.size().width / 2, image.size().height / 2)
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CITwirlDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(radius, "inputRadius")
            filter.setValue_forKey_(angle, "inputAngle")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2))

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            twirled_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(twirl_image, [image, index, center, radius, angle])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(twirled_images)
        return self

    def auto_enhance(self, correct_red_eye: bool = False, crop_to_features: bool = False, correct_rotation: bool = False) -> 'XAImageList':
        """Attempts to enhance each image in the list by applying suggested filters.

        :param correct_red_eye: Whether to attempt red eye removal, defaults to False
        :type correct_red_eye: bool, optional
        :param crop_to_features: Whether to crop the images to focus on their main features, defaults to False
        :type crop_to_features: bool, optional
        :param correct_rotation: Whether attempt perspective correction by rotating the images, defaults to False
        :type correct_rotation: bool, optional
        :return: The list of enhanced images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        enhanced_images = [None] * images.count()
        def enhance_image(image, index):
            ci_image = Quartz.CIImage.imageWithCGImage_(image.CGImage())

            options = {
                Quartz.kCIImageAutoAdjustRedEye: correct_red_eye,
                Quartz.kCIImageAutoAdjustCrop: crop_to_features,
                Quartz.kCIImageAutoAdjustLevel: correct_rotation
            }

            enhancements = ci_image.autoAdjustmentFiltersWithOptions_(options)
            for filter in enhancements:
                filter.setValue_forKey_(ci_image, "inputImage")
                ci_image = filter.outputImage()

            # Crop the result to the original image size
            cropped = ci_image.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2))

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            enhanced_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(enhance_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(enhanced_images)
        return self

    def flip_horizontally(self) -> 'XAImageList':
        """Flips each image in the list horizontally.

        :return: The list of flipped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()
            
        flipped_images = [None] * images.count()
        def flip_image(image, index):
            flipped_image = AppKit.NSImage.alloc().initWithSize_(image.size())
            imageBounds = AppKit.NSMakeRect(0, 0, image.size().width, image.size().height)

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(image.size().width, 0)
            transform.scaleXBy_yBy_(-1, 1)

            flipped_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
            flipped_image.unlockFocus()
            flipped_images[index] = flipped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(flip_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(flipped_images)
        return self

    def flip_vertically(self) -> 'XAImageList':
        """Flips each image in the list vertically.

        :return: The list of flipped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()
            
        flipped_images = [None] * images.count()
        def flip_image(image, index):
            flipped_image = AppKit.NSImage.alloc().initWithSize_(image.size())
            imageBounds = AppKit.NSMakeRect(0, 0, image.size().width, image.size().height)

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(0, image.size().height)
            transform.scaleXBy_yBy_(1, -1)

            flipped_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
            flipped_image.unlockFocus()
            flipped_images[index] = flipped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(flip_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(flipped_images)
        return self

    def rotate(self, degrees: float) -> 'XAImageList':
        """Rotates each image in the list by the specified amount of degrees.

        :param degrees: The number of degrees to rotate the images by
        :type degrees: float
        :return: The list of rotated images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        sinDegrees = abs(math.sin(degrees * math.pi / 180.0))
        cosDegrees = abs(math.cos(degrees * math.pi / 180.0))

        images = self.__partial_init()
            
        rotated_images = [None] * images.count()
        def rotate_image(image, index):
            new_size = Quartz.CGSizeMake(image.size().height * sinDegrees + image.size().width * cosDegrees, image.size().width * sinDegrees + image.size().height * cosDegrees)
            rotated_image = AppKit.NSImage.alloc().initWithSize_(new_size)

            imageBounds = Quartz.CGRectMake((new_size.width - image.size().width) / 2, (new_size.height - image.size().height) / 2, image.size().width, image.size().height)

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(new_size.width / 2, new_size.height / 2)
            transform.rotateByDegrees_(degrees)
            transform.translateXBy_yBy_(-new_size.width / 2, -new_size.height / 2)

            rotated_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
            rotated_image.unlockFocus()

            rotated_images[index] = rotated_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(rotate_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(rotated_images)
        return self

    def crop(self, size: tuple[int, int], corner: Union[tuple[int, int], None] = None) -> 'XAImageList':
        """Crops each image in the list to the specified dimensions.

        :param size: The dimensions to crop each image to
        :type size: tuple[int, int]
        :param corner: The bottom-left location to crom each image from, or None to use (0, 0), defaults to None
        :type corner: Union[tuple[int, int], None]
        :return: The list of cropped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if corner is None:
            # No corner provided -- use (0,0) by default
            corner = (0, 0)

        images = self.__partial_init()
            
        cropped_images = [None] * images.count()
        def crop_image(image, index):
            cropped_image = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(size[0], size[1]))
            imageBounds = AppKit.NSMakeRect(corner[0], corner[1], image.size().width, image.size().height)

            cropped_image.lockFocus()
            image.drawInRect_(imageBounds)
            cropped_image.unlockFocus()
            cropped_images[index] = cropped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(crop_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(cropped_images)
        return self

    def scale(self, scale_factor_x: float, scale_factor_y: Union[float, None] = None) -> 'XAImageList':
        """Scales each image in the list by the specified horizontal and vertical factors.

        :param scale_factor_x: The factor by which to scale each image in the X dimension
        :type scale_factor_x: float
        :param scale_factor_y: The factor by which to scale each image in the Y dimension, or None to match the horizontal factor, defaults to None
        :type scale_factor_y: Union[float, None]
        :return: The list of scaled images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if scale_factor_y is None:
            scale_factor_y = scale_factor_x

        images = self.__partial_init()
            
        scaled_images = [None] * self.xa_elem.count()
        def scale_image(image, index):
            scaled_image = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(image.size().width * scale_factor_x, image.size().height * scale_factor_y))
            imageBounds = AppKit.NSMakeRect(0, 0, image.size().width, image.size().height)

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.scaleXBy_yBy_(scale_factor_x, scale_factor_y)

            scaled_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
            scaled_image.unlockFocus()
            scaled_images[index] = scaled_image

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(scale_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(scaled_images)
        return self

    def pad(self, horizontal_border_width: int = 50, vertical_border_width: int = 50, pad_color: Union[XAColor, None] = None) -> 'XAImageList':
        """Pads each image in the list with the specified color; add a border around each image in the list with the specified vertical and horizontal width.

        :param horizontal_border_width: The border width, in pixels, in the x-dimension, defaults to 50
        :type horizontal_border_width: int
        :param vertical_border_width: The border width, in pixels, in the y-dimension, defaults to 50
        :type vertical_border_width: int
        :param pad_color: The color of the border, or None for a white border, defaults to None
        :type pad_color: Union[XAColor, None]
        :return: The list of padded images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if pad_color is None:
            # No color provided -- use white by default
            pad_color = XAColor.white()

        images = self.__partial_init()

        padded_images = [None] * images.count()
        def pad_image(image, index):
            new_width = image.size().width + horizontal_border_width * 2
            new_height = image.size().height + vertical_border_width * 2
            color_swatch = pad_color.make_swatch(new_width, new_height)

            color_swatch.xa_elem.lockFocus()
            bounds = AppKit.NSMakeRect(horizontal_border_width, vertical_border_width, image.size().width, image.size().height)
            image.drawInRect_(bounds)
            color_swatch.xa_elem.unlockFocus()
            padded_images[index] = color_swatch.xa_elem
        
        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(pad_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(padded_images)
        return self

    def overlay_image(self, image: 'XAImage', location: Union[tuple[int, int], None] = None, size: Union[tuple[int, int], None] = None) -> 'XAImageList':
        """Overlays an image on top of each image in the list, at the specified location, with the specified size.

        :param image: The image to overlay on top of each image in the list
        :type image: XAImage
        :param location: The bottom-left point of the overlaid image in the results, or None to use the bottom-left point of each background image, defaults to None
        :type location: Union[tuple[int, int], None]
        :param size: The width and height of the overlaid image, or None to use the overlaid's images existing width and height, or (-1, -1) to use the dimensions of each background images, defaults to None
        :type size: Union[tuple[int, int], None]
        :return: The list of images with the specified image overlaid on top of them
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use the bottom-left point of the background image by default
            location = (0, 0)

        images = self.__partial_init()
        overlayed_images = [None] * images.count()
        def overlay_image(img, index, image, size, location):
            if size is None:
                # No dimensions provided -- use size of overlay image by default
                size = image.size
            elif size == (-1, -1):
                # Use remaining width/height of background image
                size = (img.size().width - location[0], img.size().height - location[1])
            elif size[0] == -1:
                # Use remaining width of background image + provided height
                size = (img.size().width - location[0], size[1])
            elif size[1] == -1:
                # Use remaining height of background image + provided width
                size = (size[1], img.size().width - location[1])

            img.lockFocus()
            bounds = AppKit.NSMakeRect(location[0], location[1], size[0], size[1])
            image.xa_elem.drawInRect_(bounds)
            img.unlockFocus()
            overlayed_images[index] = img
        
        threads = [None] * images.count()
        for index, img in enumerate(images):
            threads[index] = self._spawn_thread(overlay_image, [img, index, image, size, location])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(overlayed_images)
        return self

    def overlay_text(self, text: str, location: Union[tuple[int, int], None] = None, font_size: float = 12, font_color: Union[XAColor, None] = None) -> 'XAImageList':
        """Overlays text of the specified size and color at the provided location within each image of the list.

        :param text: The text to overlay onto each image of the list
        :type text: str
        :param location: The bottom-left point of the start of the text, or None to use (5, 5), defaults to None
        :type location: Union[tuple[int, int], None]
        :param font_size: The font size, in pixels, of the text, defaults to 12
        :type font_size: float
        :param font_color: The color of the text, or None to use black, defaults to None
        :type font_color: XAColor
        :return: The list of images with the specified text overlaid on top of them
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use (5, 5) by default
            location = (5, 5)

        if font_color is None:
            # No color provided -- use black by default
            font_color = XAColor.black()

        font = AppKit.NSFont.userFontOfSize_(font_size)
        images = self.__partial_init()
        overlayed_images = [None] * self.xa_elem.count()
        def overlay_text(image, index):
            textRect = Quartz.CGRectMake(location[0], 0, image.size().width - location[0], location[1])
            attributes = {
                AppKit.NSFontAttributeName: font,
                AppKit.NSForegroundColorAttributeName: font_color.xa_elem
            }

            image.lockFocus()
            AppKit.NSString.alloc().initWithString_(text).drawInRect_withAttributes_(textRect, attributes)
            image.unlockFocus()
            overlayed_images[index] = image

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(overlay_text, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(overlayed_images)
        return self

    def extract_text(self) -> list[str]:
        """Extracts and returns a list of all visible text in each image of the list.

        :return: The array of extracted text strings
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> test = PyXA.XAImage("/Users/ExampleUser/Downloads/Example.jpg")
        >>> print(test.extract_text())
        ["HERE'S TO THE", 'CRAZY ONES', 'the MISFITS the REBELS', 'THE TROUBLEMAKERS', ...]

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        extracted_strings = [None] * self.xa_elem.count()
        def get_text(image, index):
            # Prepare CGImage
            ci_image = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            context = Quartz.CIContext.alloc().initWithOptions_(None)
            img = context.createCGImage_fromRect_(ci_image, ci_image.extent())

            # Handle request completion
            image_strings = []
            def recognize_text_handler(request, error):
                observations = request.results()
                for observation in observations:
                    recognized_strings = observation.topCandidates_(1)[0].string()
                    image_strings.append(recognized_strings)

            # Perform request and return extracted text
            request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)
            request_handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None)
            request_handler.performRequests_error_([request], None)
            extracted_strings[index] = image_strings

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(get_text, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        return extracted_strings

    def show_in_preview(self):
        """Opens each image in the list in Preview.

        .. versionadded:: 0.1.0
        """
        for image in self:
            image.show_in_preview()

    def save(self, file_paths: list[Union[XAPath, str]]):
        """Saves each image to a file on the disk.

        :param file_path: The path at which to save the image file. Any existing file at that location will be overwritten, defaults to None
        :type file_path: Union[XAPath, str, None]

        .. versionadded:: 0.1.0
        """
        for index, image in enumerate(self):
            path = None
            if len(file_paths) > index:
                path = file_paths[index]
            image.save(path)

    def get_clipboard_representation(self) -> list[AppKit.NSImage]:
        """Gets a clipboard-codable representation of each image in the list.

        When the clipboard content is set to a list of image, the raw data of each image is added to the clipboard. You can then 

        :return: A list of media item file URLs
        :rtype: list[NSURL]

        .. versionadded:: 0.0.8
        """
        data = []
        for image in self.__partial_init():
            if image.TIFFRepresentation():
                data.append(image)
        return data

class XAImage(XAObject, XAClipboardCodable):
    """A wrapper around NSImage with specialized automation methods.

    .. versionadded:: 0.0.2
    """

    def __init__(self, image_reference: Union[str, XAPath, AppKit.NSURL, AppKit.NSImage, None] = None, data: Union[AppKit.NSData, None] = None):
        self.size: tuple[int, int] #: The dimensions of the image
        self.file: Union[XAPath, None] = None #: The path to the image file, if one exists
        self.data: str #: The TIFF representation of the image
        self.modified: bool = False #: Whether the image data has been modified since the object was originally created

        self.xa_elem = None

        self.__vibrance = None
        self.__gamma = None
        self.__tint = None
        self.__temperature = None
        self.__white_point = None
        self.__highlight = None
        self.__shadow = None

        if data is not None:
            # Deprecated as of 0.1.0 -- Pass data as the image_reference instead
            logging.warning("Setting the data parameter when initalizing an XAImage is deprecated functionality and will be removed in a future release")
            self.xa_elem = AppKit.NSImage.alloc().initWithData_(data)
        else:
            self.file = image_reference
            match image_reference:
                case None:
                    logging.debug("Image ref is none -- use empty NSImage")
                    self.xa_elem = AppKit.NSImage.alloc().init()

                case {"element": str(ref)}:
                    logging.debug("Image ref is string from XAList --> Reinit XAImage with string")
                    self.file = ref
                    self.xa_elem = XAImage(ref).xa_elem

                case {"element": XAImage() as image}:
                    logging.debug("Image ref is XAImage from XAList --> Set xa_elem to that image's xa_elem")
                    self.file = image.file
                    self.xa_elem = image.xa_elem

                case {"element": AppKit.NSImage() as image}:
                    logging.debug("Image ref is NSImage from XAList --> Set xa_elem to that image")
                    self.xa_elem = image

                case str() as ref if "://" in ref:
                    logging.debug("Image ref is web/file URL string --> Init NSImage with URL")
                    url = XAURL(ref).xa_elem
                    self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(url)

                case str() as ref if os.path.exists(ref) or os.path.exists(os.getcwd() + "/" + ref):
                    logging.debug("Image ref is file path string --> Init NSImage with path URL")
                    path = XAPath(ref).xa_elem
                    self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(path)

                case XAPath() as path:
                    logging.debug("Image ref is file path object --> Init NSImage with path URL")
                    self.file = path.path
                    self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(path.xa_elem)

                case XAURL() as url:
                    logging.debug("Image ref is web/file URL object --> Init NSImage with URL")
                    self.file = url.url
                    self.xa_elem = AppKit.NSImage.alloc().initWithContentsOfURL_(url.xa_elem)

                case str() as raw_string:
                    logging.debug("Image ref is raw string --> Make image from string")
                    font = AppKit.NSFont.monospacedSystemFontOfSize_weight_(15, AppKit.NSFontWeightMedium)
                    text = AppKit.NSString.alloc().initWithString_(raw_string)
                    attributes = {
                        AppKit.NSFontAttributeName: font,
                        AppKit.NSForegroundColorAttributeName: XAColor.black().xa_elem
                    }
                    text_size = text.sizeWithAttributes_(attributes)

                    # Make a white background to overlay the text on
                    swatch = XAColor.white().make_swatch(text_size.width + 20, text_size.height + 20)
                    text_rect = AppKit.NSMakeRect(10, 10, text_size.width, text_size.height)

                    # Overlay the text
                    swatch.xa_elem.lockFocus()                        
                    text.drawInRect_withAttributes_(text_rect, attributes)
                    swatch.xa_elem.unlockFocus()
                    self.xa_elem = swatch.xa_elem

                case XAImage() as image:
                    self.file = image.file
                    self.xa_elem = image.xa_elem

                case XAObject():
                    logging.debug("Image ref is XAObject --> Obtain proper ref via XAImageLike protocol")
                    self.xa_elem = XAImage(image_reference.get_image_representation()).xa_elem

                case AppKit.NSData() as data:
                    logging.debug("Image ref is NSData --> Init NSImage with data")
                    self.xa_elem = AppKit.NSImage.alloc().initWithData_(data)

                case AppKit.NSImage() as image:
                    logging.debug("Image ref is NSImage --> Set xa_elem to that image")
                    self.xa_elem = image

                case _:
                    logging.debug(f"Image ref is of unaccounted for type {type(image_reference)} --> Raise TypeError")
                    raise TypeError(f"Error: Cannot initialize XAImage using {type(image_reference)} type.")

    def __update_image(self, modified_image: Quartz.CIImage) -> 'XAImage':
        # Crop the result to the original image size
        cropped = modified_image.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, self.size[0] * 2, self.size[1] * 2))

        # Convert back to NSImage
        rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
        result = AppKit.NSImage.alloc().initWithSize_(rep.size())
        result.addRepresentation_(rep)

        # Update internal data
        self.xa_elem = result
        self.modified = True
        return self

    @property
    def size(self) -> tuple[int, int]:
        """The dimensions of the image, in pixels.

        .. versionadded:: 0.1.0
        """
        return tuple(self.xa_elem.size())

    @property
    def data(self) -> AppKit.NSData:
        return self.xa_elem.TIFFRepresentation()

    @property
    def has_alpha_channel(self) -> bool:
        """Whether the image has an alpha channel or not.

        .. versionadded:: 0.1.0
        """
        reps = self.xa_elem.representations()
        if len(reps) > 0:
            return reps[0].hasAlpha()
        # TODO: Make sure this is never a false negative
        return False

    @property
    def is_opaque(self) -> bool:
        """Whether the image contains transparent pixels or not.

        .. versionadded:: 0.1.0
        """
        reps = self.xa_elem.representations()
        if len(reps) > 0:
            return reps[0].isOpaque()
        # TODO: Make sure this is never a false negative
        return False

    @property
    def color_space_name(self) -> Union[str, None]:
        """The name of the color space that the image currently uses.

        .. versionadded:: 0.1.0
        """
        reps = self.xa_elem.representations()
        if len(reps) > 0:
            return reps[0].colorSpaceName()
        # TODO: Make sure this is never a false negative
        return None

    @property
    def gamma(self) -> float:
        """The gamma value for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__gamma is not None:
            return self.__gamma
        return -1

    @gamma.setter
    def gamma(self, gamma: float):
        self.__gamma = gamma
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIGammaAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(gamma, "inputPower")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def vibrance(self) -> Union[float, None]:
        """The vibrance value for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__vibrance is not None:
            return self.__vibrance
        return -1

    @vibrance.setter
    def vibrance(self, vibrance: float = 1):
        self.__vibrance = vibrance
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIVibrance")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(vibrance, "inputAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    @property
    def tint(self) -> Union[float, None]:
        """The tint setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__tint is not None:
            return self.__tint
        return -1

    @tint.setter
    def tint(self, tint: float):
        # -100 to 100
        temp_and_tint = Quartz.CIVector.vectorWithX_Y_(6500, tint)
        self.__tint = tint
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CITemperatureAndTint")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(temp_and_tint, "inputTargetNeutral")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def temperature(self) -> Union[float, None]:
        """The temperature setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__temperature is not None:
            return self.__temperature
        return -1

    @temperature.setter
    def temperature(self, temperature: float):
        # 2000 to inf
        temp_and_tint = Quartz.CIVector.vectorWithX_Y_(temperature, 0)
        self.__temperature = temperature
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CITemperatureAndTint")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(temp_and_tint, "inputTargetNeutral")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def white_point(self) -> Union['XAColor', None]:
        """The white point setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__white_point is not None:
            return self.__white_point
        return -1

    @white_point.setter
    def white_point(self, white_point: XAColor):
        self.__white_point = white_point
        ci_white_point = Quartz.CIColor.alloc().initWithColor_(white_point.xa_elem)
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIWhitePointAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(ci_white_point, "inputColor")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def highlight(self) -> float:
        """The highlight setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__highlight is not None:
            return self.__highlight
        return -1

    @highlight.setter
    def highlight(self, highlight: float):
        self.__highlight = highlight
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIHighlightShadowAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(highlight, "inputHighlightAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def shadow(self) -> float:
        """The shadow setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.1.0
        """
        if self.__shadow is not None:
            return self.__shadow
        return -1

    @shadow.setter
    def shadow(self, shadow: float):
        self.__shadow = shadow
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIHighlightShadowAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(self.__highlight or 1, "inputHighlightAmount")
        filter.setValue_forKey_(shadow, "inputShadowAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    def open(*images: Union[str, XAPath, list[Union[str, XAPath]]]) -> Union['XAImage', XAImageList]:
        """Initializes one or more images from files.

        :param images: The image(s) to open
        :type images: Union[str, XAPath, list[Union[str, XAPath]]]
        :return: The newly created image object, or a list of image objects
        :rtype: Union[XAImage, XAImageList]

        .. versionadded:: 0.1.0
        """
        if len(images) == 1:
            images = images[0]

        if isinstance(images, list) or isinstance(images, tuple):
            return XAImageList({"element": images})
        else:
            return XAImage(images)

    @staticmethod
    def image_from_text(text: str, font_size: int = 15, font_name: str = "Menlo", font_color: XAColor = XAColor.black(), background_color: XAColor = XAColor.white(), inset: int = 10) -> 'XAImage':
        """Initializes an image of the provided text overlaid on the specified background color.

        :param text: The text to create an image of
        :type text: str
        :param font_size: The font size of the text, defaults to 15
        :type font_size: int, optional
        :param font_name: The color of the text, defaults to XAColor.black()
        :type font_name: str, optional
        :param font_color: The name of the font to use for the text, defaults to ".SF NS Mono Light Medium"
        :type font_color: XAColor, optional
        :param background_color: The color to overlay the text on top of, defaults to XAColor.white()
        :type background_color: XAColor, optional
        :param inset: The width of the space between the text and the edge of the background color in the resulting image, defaults to 10
        :type inset: int, optional
        :return: XAImage
        :rtype: The resulting image object

        .. versionadded:: 0.1.0
        """
        font = AppKit.NSFont.fontWithName_size_(font_name, font_size)
        print(font.displayName())
        text = AppKit.NSString.alloc().initWithString_(text)
        attributes = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: font_color.xa_elem
        }
        text_size = text.sizeWithAttributes_(attributes)

        # Make a white background to overlay the text on
        swatch = background_color.make_swatch(text_size.width + inset * 2, text_size.height + inset * 2)
        text_rect = AppKit.NSMakeRect(inset, inset, text_size.width, text_size.height)

        # Overlay the text
        swatch.xa_elem.lockFocus()                        
        text.drawInRect_withAttributes_(text_rect, attributes)
        swatch.xa_elem.unlockFocus()
        return swatch
    
    def edges(self, intensity: float = 1.0) -> 'XAImage':
        """Detects the edges in the image and highlights them colorfully, blackening other areas of the image.

        :param intensity: The degree to which edges are highlighted. Higher is brighter. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIEdges")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(intensity, "inputIntensity")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def gaussian_blur(self, intensity: float = 10) -> 'XAImage':
        """Blurs the image using a Gaussian filter.

        :param intensity: The strength of the blur effect, defaults to 10
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIGaussianBlur")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(intensity, "inputRadius")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def reduce_noise(self, noise_level: float = 0.02, sharpness: float = 0.4) -> 'XAImage':
        """Reduces noise in the image by sharpening areas with a luminance delta below the specified noise level threshold.

        :param noise_level: The threshold for luminance changes in an area below which will be considered noise, defaults to 0.02
        :type noise_level: float
        :param sharpness: The sharpness of the resulting image, defaults to 0.4
        :type sharpness: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CINoiseReduction")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(noise_level, "inputNoiseLevel")
        filter.setValue_forKey_(sharpness, "inputSharpness")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def pixellate(self, pixel_size: float = 8.0) -> 'XAImage':
        """Pixellates the image.

        :param pixel_size: The size of the pixels, defaults to 8.0
        :type pixel_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIPixellate")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(pixel_size, "inputScale")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def outline(self, threshold: float = 0.1) -> 'XAImage':
        """Outlines detected edges within the image in black, leaving the rest transparent.

        :param threshold: The threshold to use when separating edge and non-edge pixels. Larger values produce thinner edge lines. Defaults to 0.1
        :type threshold: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CILineOverlay")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(threshold, "inputThreshold")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def invert(self) -> 'XAImage':
        """Inverts the color of the image.

        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIColorInvert")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)
    
    def sepia(self, intensity: float = 1.0) -> 'XAImage':
        """Applies a sepia filter to the image; maps all colors of the image to shades of brown.

        :param intensity: The opacity of the sepia effect. A value of 0 will have no impact on the image. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CISepiaTone")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(intensity, "inputIntensity")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def vignette(self, intensity: float = 1.0) -> 'XAImage':
        """Applies vignette shading to the corners of the image.

        :param intensity: The intensity of the vignette effect, defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIVignette")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(intensity, "inputIntensity")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def depth_of_field(self, focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None] = None, intensity: float = 10.0, focal_region_saturation: float = 1.5) -> 'XAImage':
        """Applies a depth of field filter to the image, simulating a tilt & shift effect.

        :param focal_region: Two points defining a line within the image to focus the effect around (pixels around the line will be in focus), or None to use the center third of the image, defaults to None
        :type focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None]
        :param intensity: Controls the amount of distance around the focal region to keep in focus. Higher values decrease the distance before the out-of-focus effect starts. Defaults to 10.0
        :type intensity: float
        :param focal_region_saturation: Adjusts the saturation of the focial region. Higher values increase saturation. Defaults to 1.5 (1.5x default saturation)
        :type focal_region_saturation: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if focal_region is None:
            center_top = Quartz.CIVector.vectorWithX_Y_(self.size[0] / 2, self.size[1] / 3)
            center_bottom = Quartz.CIVector.vectorWithX_Y_(self.size[0] / 2, self.size[1] / 3 * 2)
            focal_region = (center_top, center_bottom)
        else:
            point1 = Quartz.CIVector.vectorWithX_Y_(focal_region[0])
            point2 = Quartz.CIVector.vectorWithX_Y_(focal_region[1])
            focal_region = (point1, point2)

        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIDepthOfField")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(focal_region[0], "inputPoint0")
        filter.setValue_forKey_(focal_region[1], "inputPoint1")
        filter.setValue_forKey_(intensity, "inputRadius")
        filter.setValue_forKey_(focal_region_saturation, "inputSaturation")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def crystallize(self, crystal_size: float = 20.0) -> 'XAImage':
        """Applies a crystallization filter to the image. Creates polygon-shaped color blocks by aggregating pixel values.

        :param crystal_size: The radius of the crystals, defaults to 20.0
        :type crystal_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CICrystallize")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(crystal_size, "inputRadius")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def comic(self) -> 'XAImage':
        """Applies a comic filter to the image. Outlines edges and applies a color halftone effect.

        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIComicEffect")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def pointillize(self, point_size: float = 20.0) -> 'XAImage':
        """Applies a pointillization filter to the image.

        :param crystal_size: The radius of the points, defaults to 20.0
        :type crystal_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIPointillize")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(point_size, "inputRadius")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def bloom(self, intensity: float = 0.5) -> 'XAImage':
        """Applies a bloom effect to the image. Softens edges and adds a glow.

        :param intensity: The strength of the softening and glow effects, defaults to 0.5
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIBloom")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(intensity, "inputIntensity")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def monochrome(self, color: XAColor, intensity: float = 1.0) -> 'XAImage':
        """Remaps the colors of the image to shades of the specified color.

        :param color: The color of map the image's colors to
        :type color: XAColor
        :param intensity: The strength of recoloring effect. Higher values map colors to darker shades of the provided color. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        ci_color = Quartz.CIColor.alloc().initWithColor_(color.xa_elem)
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIColorMonochrome")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(ci_color, "inputColor")
        filter.setValue_forKey_(intensity, "inputIntensity")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def bump(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, curvature: float = 0.5) -> 'XAImage':
        """Creates a concave (inward) or convex (outward) bump at the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The radius of the bump in pixels, defaults to 300.0
        :type radius: float
        :param curvature: Controls the direction and intensity of the bump's curvature. Positive values create convex bumps while negative values create concave bumps. Defaults to 0.5
        :type curvature: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if center is None:
            center = Quartz.CIVector.vectorWithX_Y_(self.size[0] / 2, self.size[1] / 2)
        else:
            center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIBumpDistortion")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(center, "inputCenter")
        filter.setValue_forKey_(radius, "inputRadius")
        filter.setValue_forKey_(curvature, "inputScale")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def pinch(self, center: Union[tuple[int, int], None] = None, intensity: float = 0.5) -> 'XAImage':
        """Creates an inward pinch distortion at the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param intensity: Controls the scale of the pinch effect. Higher values stretch pixels away from the specified center to a greater degree. Defaults to 0.5
        :type intensity: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if center is None:
            center = Quartz.CIVector.vectorWithX_Y_(self.size[0] / 2, self.size[1] / 2)
        else:
            center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIPinchDistortion")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(center, "inputCenter")
        filter.setValue_forKey_(intensity, "inputScale")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def twirl(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, angle: float = 3.14) -> 'XAImage':
        """Creates a twirl distortion by rotating pixels around the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
        :type radius: float
        :param angle: The angle of the twirl in radians, defaults to 3.14
        :type angle: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if center is None:
            center = Quartz.CIVector.vectorWithX_Y_(self.size[0] / 2, self.size[1] / 2)
        else:
            center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CITwirlDistortion")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(center, "inputCenter")
        filter.setValue_forKey_(radius, "inputRadius")
        filter.setValue_forKey_(angle, "inputAngle")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    def auto_enhance(self, correct_red_eye: bool = False, crop_to_features: bool = False, correct_rotation: bool = False) -> 'XAImage':
        """Attempts to enhance the image by applying suggested filters.

        :param correct_red_eye: Whether to attempt red eye removal, defaults to False
        :type correct_red_eye: bool, optional
        :param crop_to_features: Whether to crop the image to focus on the main features with it, defaults to False
        :type crop_to_features: bool, optional
        :param correct_rotation: Whether attempt perspective correction by rotating the image, defaults to False
        :type correct_rotation: bool, optional
        :return: The resulting image after applying the enchantments
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        ci_image = Quartz.CIImage.imageWithData_(self.data)
        options = {
            Quartz.kCIImageAutoAdjustRedEye: correct_red_eye,
            Quartz.kCIImageAutoAdjustCrop: crop_to_features,
            Quartz.kCIImageAutoAdjustLevel: correct_rotation
        }
        enhancements = ci_image.autoAdjustmentFiltersWithOptions_(options)
        print(enhancements)
        for filter in enhancements:
            filter.setValue_forKey_(ci_image, "inputImage")
            ci_image = filter.outputImage()
        return self.__update_image(ci_image)

    def flip_horizontally(self) -> 'XAImage':
        """Flips the image horizontally.

        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        flipped_image = AppKit.NSImage.alloc().initWithSize_(self.xa_elem.size())
        imageBounds = AppKit.NSMakeRect(0, 0, self.size[0], self.size[1])

        transform = AppKit.NSAffineTransform.alloc().init()
        transform.translateXBy_yBy_(self.size[0], 0)
        transform.scaleXBy_yBy_(-1, 1)

        flipped_image.lockFocus()
        transform.concat()
        self.xa_elem.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
        flipped_image.unlockFocus()
        self.xa_elem = flipped_image
        self.modified = True
        return self

    def flip_vertically(self) -> 'XAImage':
        """Flips the image vertically.

        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        flipped_image = AppKit.NSImage.alloc().initWithSize_(self.xa_elem.size())
        imageBounds = AppKit.NSMakeRect(0, 0, self.size[0], self.size[1])

        transform = AppKit.NSAffineTransform.alloc().init()
        transform.translateXBy_yBy_(0, self.size[1])
        transform.scaleXBy_yBy_(1, -1)

        flipped_image.lockFocus()
        transform.concat()
        self.xa_elem.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
        flipped_image.unlockFocus()
        self.xa_elem = flipped_image
        self.modified = True
        return self

    def rotate(self, degrees: float) -> 'XAImage':
        """Rotates the image clockwise by the specified number of degrees.

        :param degrees: The number of degrees to rotate the image by
        :type degrees: float
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        sinDegrees = abs(math.sin(degrees * math.pi / 180.0))
        cosDegrees = abs(math.cos(degrees * math.pi / 180.0))
        newSize = Quartz.CGSizeMake(self.size[1] * sinDegrees + self.size[0] * cosDegrees, self.size[0] * sinDegrees + self.size[1] * cosDegrees)
        rotated_image = AppKit.NSImage.alloc().initWithSize_(newSize)

        imageBounds = Quartz.CGRectMake((newSize.width - self.size[0]) / 2, (newSize.height - self.size[1]) / 2, self.size[0], self.size[1])

        transform = AppKit.NSAffineTransform.alloc().init()
        transform.translateXBy_yBy_(newSize.width / 2, newSize.height / 2)
        transform.rotateByDegrees_(degrees)
        transform.translateXBy_yBy_(-newSize.width / 2, -newSize.height / 2)

        rotated_image.lockFocus()
        transform.concat()
        self.xa_elem.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
        rotated_image.unlockFocus()
        self.xa_elem = rotated_image
        self.modified = True
        return self

    def crop(self, size: tuple[int, int], corner: Union[tuple[int, int], None] = None) -> 'XAImage':
        """Crops the image to the specified dimensions.

        :param size: The width and height of the resulting image
        :type size: tuple[int, int]
        :param corner: The bottom-left corner location from which to crop the image, or None to use (0, 0), defaults to None
        :type corner: Union[tuple[int, int], None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if corner is None:
            # No corner provided -- use (0,0) by default
            corner = (0, 0)

        cropped_image = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(size[0], size[1]))
        imageBounds = AppKit.NSMakeRect(corner[0], corner[1], self.size[0], self.size[1])

        cropped_image.lockFocus()
        self.xa_elem.drawInRect_(imageBounds)
        cropped_image.unlockFocus()
        self.xa_elem = cropped_image
        self.modified = True
        return self

    def scale(self, scale_factor_x: float, scale_factor_y: Union[float, None] = None) -> 'XAImage':
        """Scales the image by the specified horizontal and vertical factors.

        :param scale_factor_x: The factor by which to scale the image in the X dimension
        :type scale_factor_x: float
        :param scale_factor_y: The factor by which to scale the image in the Y dimension, or None to match the horizontal factor, defaults to None
        :type scale_factor_y: Union[float, None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if scale_factor_y is None:
            scale_factor_y = scale_factor_x

        scaled_image = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(self.size[0] * scale_factor_x, self.size[1] * scale_factor_y))
        imageBounds = AppKit.NSMakeRect(0, 0, self.size[0], self.size[1])

        transform = AppKit.NSAffineTransform.alloc().init()
        transform.scaleXBy_yBy_(scale_factor_x, scale_factor_y)

        scaled_image.lockFocus()
        transform.concat()
        self.xa_elem.drawInRect_fromRect_operation_fraction_(imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
        scaled_image.unlockFocus()
        self.xa_elem = scaled_image
        self.modified = True
        return self

    def pad(self, horizontal_border_width: int = 50, vertical_border_width: int = 50, pad_color: Union[XAColor, None] = None) -> 'XAImage':
        """Pads the image with the specified color; adds a border around the image with the specified vertical and horizontal width.

        :param horizontal_border_width: The border width, in pixels, in the x-dimension, defaults to 50
        :type horizontal_border_width: int
        :param vertical_border_width: The border width, in pixels, in the y-dimension, defaults to 50
        :type vertical_border_width: int
        :param pad_color: The color of the border, or None for a white border, defaults to None
        :type pad_color: Union[XAColor, None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if pad_color is None:
            # No color provided -- use white by default
            pad_color = XAColor.white()

        new_width = self.size[0] + horizontal_border_width * 2
        new_height = self.size[1] + vertical_border_width * 2
        color_swatch = pad_color.make_swatch(new_width, new_height)

        color_swatch.xa_elem.lockFocus()
        bounds = AppKit.NSMakeRect(horizontal_border_width, vertical_border_width, self.size[0], self.size[1])
        self.xa_elem.drawInRect_(bounds)
        color_swatch.xa_elem.unlockFocus()
        self.xa_elem = color_swatch.xa_elem
        self.modified = True
        return self

    def overlay_image(self, image: 'XAImage', location: Union[tuple[int, int], None] = None, size: Union[tuple[int, int], None] = None) -> 'XAImage':
        """Overlays an image on top of this image, at the specified location, with the specified size.

        :param image: The image to overlay on top of this image
        :type image: XAImage
        :param location: The bottom-left point of the overlaid image in the result, or None to use the bottom-left point of the background image, defaults to None
        :type location: Union[tuple[int, int], None]
        :param size: The width and height of the overlaid image, or None to use the overlaid's images existing width and height, or (-1, -1) to use the dimensions of the background image, defaults to None
        :type size: Union[tuple[int, int], None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use the bottom-left point of the background image by default
            location = (0, 0)

        if size is None:
            # No dimensions provided -- use size of overlay image by default
            size = image.size
        elif size == (-1, -1):
            # Use remaining width/height of background image
            size = (self.size[0] - location[0], self.size[1] - location[1])
        elif size[0] == -1:
            # Use remaining width of background image + provided height
            size = (self.size[0] - location[0], size[1])
        elif size[1] == -1:
            # Use remaining height of background image + provided width
            size = (size[1], self.size[1] - location[1])

        self.xa_elem.lockFocus()
        bounds = AppKit.NSMakeRect(location[0], location[1], size[0], size[1])
        image.xa_elem.drawInRect_(bounds)
        self.xa_elem.unlockFocus()
        self.modified = True
        return self.xa_elem

    def overlay_text(self, text: str, location: Union[tuple[int, int], None] = None, font_size: float = 12, font_color: Union[XAColor, None] = None) -> 'XAImage':
        """Overlays text of the specified size and color at the provided location within the image.

        :param text: The text to overlay onto the image
        :type text: str
        :param location: The bottom-left point of the start of the text, or None to use (5, 5), defaults to None
        :type location: Union[tuple[int, int], None]
        :param font_size: The font size, in pixels, of the text, defaults to 12
        :type font_size: float
        :param font_color: The color of the text, or None to use black, defaults to None
        :type font_color: XAColor
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use (5, 5) by default
            location = (5, 5)

        if font_color is None:
            # No color provided -- use black by default
            font_color = XAColor.black()

        font = AppKit.NSFont.userFontOfSize_(font_size)
        textRect = Quartz.CGRectMake(location[0], 0, self.size[0] - location[0], location[1])
        attributes = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: font_color.xa_elem
        }

        self.xa_elem.lockFocus()
        AppKit.NSString.alloc().initWithString_(text).drawInRect_withAttributes_(textRect, attributes)
        self.xa_elem.unlockFocus()
        self.modified = True
        return self

    def extract_text(self) -> list[str]:
        """Extracts and returns all visible text in the image.

        :return: The array of extracted text strings
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> test = PyXA.XAImage("/Users/ExampleUser/Downloads/Example.jpg")
        >>> print(test.extract_text())
        ["HERE'S TO THE", 'CRAZY ONES', 'the MISFITS the REBELS', 'THE TROUBLEMAKERS', ...]

        .. versionadded:: 0.1.0
        """
        # Prepare CGImage
        ci_image = Quartz.CIImage.imageWithData_(self.data)
        context = Quartz.CIContext.alloc().initWithOptions_(None)
        img = context.createCGImage_fromRect_(ci_image, ci_image.extent())

        # Handle request completion
        extracted_strings = []
        def recognize_text_handler(request, error):
            observations = request.results()
            for observation in observations:
                recognized_strings = observation.topCandidates_(1)[0].string()
                extracted_strings.append(recognized_strings)

        # Perform request and return extracted text
        request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)
        request_handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None)
        request_handler.performRequests_error_([request], None)
        return extracted_strings

    def show_in_preview(self):
        """Opens the image in preview.

        .. versionadded:: 0.0.8
        """
        if not self.modified and self.file is not None and isinstance(self.file, XAPath):
            AppKit.NSWorkspace.sharedWorkspace().openFile_withApplication_(self.file.path, "Preview")
        else:
            tmp_file = tempfile.NamedTemporaryFile()
            with open(tmp_file.name, 'wb') as f:
                f.write(self.xa_elem.TIFFRepresentation())

            img_url = XAPath(tmp_file.name).xa_elem
            preview_url = XAPath("/System/Applications/Preview.app/").xa_elem
            AppKit.NSWorkspace.sharedWorkspace().openURLs_withApplicationAtURL_configuration_completionHandler_([img_url], preview_url, None, None)
            time.sleep(1)

    def save(self, file_path: Union[XAPath, str, None] = None):
        """Saves the image to a file on the disk. Saves to the original file (if there was one) by default.

        :param file_path: The path at which to save the image file. Any existing file at that location will be overwritten, defaults to None
        :type file_path: Union[XAPath, str, None]

        .. versionadded:: 0.1.0
        """
        if file_path is None and self.file is not None:
            file_path = self.file.path
        elif isinstance(file_path, XAPath):
            file_path = file_path.path
        fm = AppKit.NSFileManager.defaultManager()
        fm.createFileAtPath_contents_attributes_(file_path, self.xa_elem.TIFFRepresentation(), None)

    def get_clipboard_representation(self) -> AppKit.NSImage:
        """Gets a clipboard-codable representation of the iimage.

        When the clipboard content is set to an image, the image itself, including any modifications, is added to the clipboard. Pasting will then insert the image into the active document.

        :return: The raw NSImage object for this XAIMage
        :rtype: AppKit.NSImage

        .. versionadded:: 0.1.0
        """
        return self.xa_elem

    def __eq__(self, other):
        return self.xa_elem.TIFFRepresentation() == other.xa_elem.TIFFRepresentation()




class XASoundList(XAList, XAClipboardCodable):
    """A wrapper around lists of sounds that employs fast enumeration techniques.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASound, filter)

    def get_clipboard_representation(self) -> list[Union[AppKit.NSSound, AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of each sound in the list.

        When the clipboard content is set to a list of sounds, each sound's raw sound data, its associated file URL, and its file path string are added to the clipboard.

        :return: The clipboard-codable form of the sound
        :rtype: Any

        .. versionadded:: 0.1.0
        """
        return [self.xa_elem, self.file.xa_elem, self.file.xa_elem.path()]

class XASound(XAObject, XAClipboardCodable):
    """A class for playing and interacting with audio files and data.

    .. versionadded:: 0.0.1
    """
    def __init__(self, sound_reference: Union[str, XAURL, XAPath]):
        self.file = None

        match sound_reference:
            case str() as ref if "://" in ref:
                logging.debug(f"Sound ref is web/file URL --> Set file to URL")
                self.file = XAURL(ref)

            case str() as ref if os.path.exists(ref):
                logging.debug(f"Sound ref is file path --> Set file to path")
                self.file = XAPath(sound_reference)

            case str() as ref:
                logging.debug(f"Sound ref is raw string --> Set file to path of sound with ref name")
                self.file = XAPath("/System/Library/Sounds/" + ref + ".aiff")

            case {"element": str() as ref}:
                logging.debug(f"Sound ref is string from XASoundList --> Reinit with string")
                self.file = XASound(ref).file

            case XAPath() as ref:
                logging.debug(f"Sound ref is path object --> Set file to path")
                self.file = ref

            case XAURL() as ref:
                logging.debug(f"Sound ref is web/file URL object --> Set file to URL")
                self.file = ref

            case XASound() as sound:
                logging.debug(f"Sound ref is another XASound object --> Set file to that sound's file")
                self.file = sound.file

        self.duration: float #: The duration of the sound in seconds

        self.__audio_file = AVFoundation.AVAudioFile.alloc().initForReading_error_(self.file.xa_elem if self.file is not None else None, None)[0]

        self.__audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self.__player_node = AVFoundation.AVAudioPlayerNode.alloc().init()
        self.__audio_engine.attachNode_(self.__player_node)

        self.__audio_engine.connect_to_format_(self.__player_node, self.__audio_engine.mainMixerNode(), self.__audio_file.processingFormat())

        self.__player_node.stop()
        self.__audio_engine.stop()

        self.xa_elem = self.__audio_file

    @property
    def num_sample_frames(self) -> int:
        """The number of sample frames in the audio file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.length()

    @property
    def sample_rate(self) -> float:
        """The sample rate for the sound format, in hertz.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.processingFormat().sampleRate()

    @property
    def duration(self) -> float:
        """The duration of the sound in seconds.

        .. versionadded:: 0.1.0
        """
        return self.num_sample_frames / self.sample_rate

    def open(*sound_references: Union[str, XAPath, list[Union[str, XAPath]]]) -> Union['XASound', XASoundList]:
        """Initializes one or more sounds from files.

        :param sound_references: The sound(s) to open
        :type sound_references: Union[str, XAPath, list[Union[str, XAPath]]]
        :return: The newly created sound object, or a list of sound objects
        :rtype: Union[XASound, XASoundList]

        .. versionadded:: 0.1.0
        """
        if len(sound_references) == 1:
            sound_references = sound_references[0]

        if isinstance(sound_references, list) or isinstance(sound_references, tuple):
            return XASoundList({"element": sound_references})
        else:
            return XASound(sound_references)

    def beep():
        """Plays the system Beep sound.

        .. versionadded:: 0.1.0
        """
        AppleScript("""
            beep
            delay 0.5
        """).run()

    def play(self) -> Self:
        """Plays the sound from the beginning.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :return: A reference to this sound object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> import time
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.play()
        >>> time.sleep(glass_sound.duration)

        .. seealso:: :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        def play_sound(self):
            logging.debug(f"Playing XASound audio in new thread")
            self.__player_node.scheduleFile_atTime_completionHandler_(self.xa_elem, None, None)
            self.__audio_engine.startAndReturnError_(None)
            self.__player_node.play()
            while self.__player_node.isPlaying():
                AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.1))

        self._spawn_thread(play_sound, [self])
        return self

    def pause(self) -> Self:
        """Pauses the sound.

        :return: A reference to this sound object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.pause()

        .. seealso:: :func:`resume`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.__player_node.pause()
        return self

    def resume(self) -> Self:
        """Plays the sound starting from the time it was last paused at.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :return: A reference to this sound object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.resume()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        def play_sound(self):
            self.__player_node.scheduleFile_atTime_completionHandler_(self.xa_elem, None, None)
            self.__audio_engine.startAndReturnError_(None)
            self.__player_node.play()
            while self.__player_node.isPlaying():
                AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.1))

        self._spawn_thread(play_sound, [self])
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
        self.__audio_engine.stop()
        return self

    def set_volume(self, volume: float) -> Self:
        """Sets the volume of the sound.

        :param volume: The desired volume of the sound in the range [0.0, 1.0].
        :type volume: int
        :return: A reference to this sound object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.set_volume(1.0)

        .. seealso:: :func:`volume`

        .. versionadded:: 0.0.1
        """
        self.__audio_engine.mainMixerNode().setOutputVolume_(volume)
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
        return self.__audio_engine.mainMixerNode().volume()

    def loop(self, times: int) -> Self:
        """Plays the sound the specified number of times.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :param times: The number of times to loop the sound.
        :type times: int
        :return: A reference to this sound object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> import time
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.loop(10)
        >>> time.sleep(glass_sound.duration * 10)

        .. versionadded:: 0.0.1
        """
        def play_sound():
            num_plays = 0
            while num_plays < times:
                sound = XASound(self.file)
                sound.play()
                num_plays += 1
                time.sleep(self.duration)

        self._spawn_thread(play_sound)
        return self

    def trim(self, start_time: float, end_time: float) -> Self:
        """Trims the sound to the specified start and end time, in seconds.

        This will create a momentary sound data file in the current working directory for storing the intermediary trimmed sound data.

        :param start_time: The start time in seconds
        :type start_time: float
        :param end_time: The end time in seconds
        :type end_time: float
        :return: The updated sound object
        :rtype: Self

        .. versionadded:: 0.1.0
        """
        # Clear the temp data path
        file_path = "sound_data_tmp.m4a"
        if os.path.exists(file_path):
            AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(file_path, None)

        # Configure the export session
        asset = AVFoundation.AVAsset.assetWithURL_(self.file.xa_elem)
        export_session = AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(asset, AVFoundation.AVAssetExportPresetAppleM4A)

        start_time = CoreMedia.CMTimeMake(start_time * 100, 100)
        end_time = CoreMedia.CMTimeMake(end_time * 100, 100)
        time_range =  CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time);

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(XAPath(file_path).xa_elem)
        export_session.setOutputFileType_(AVFoundation.AVFileTypeAppleM4A)

        # Export to file path
        waiting = False
        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)

        while not waiting:
            time.sleep(0.01)

        # Load the sound file back into active memory
        self.__audio_file = AVFoundation.AVAudioFile.alloc().initForReading_error_(XAPath(file_path).xa_elem, None)[0]
        self.xa_elem = self.__audio_file
        AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(file_path, None) 
        return self

    def save(self, file_path: Union[XAPath, str]):
        """Saves the sound to the specified file path.

        :param file_path: The path to save the sound to
        :type file_path: Union[XAPath, str]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        # Configure the export session
        asset = AVFoundation.AVAsset.assetWithURL_(self.file.xa_elem)
        export_session = AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(asset, AVFoundation.AVAssetExportPresetAppleM4A)

        start_time = CoreMedia.CMTimeMake(0, 100)
        end_time = CoreMedia.CMTimeMake(self.duration * 100, 100)
        time_range =  CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time);

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(file_path.xa_elem)
        # export_session.setOutputFileType_(AVFoundation.AVFileTypeAppleM4A)

        # Export to file path
        waiting = False
        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)
        
        while not waiting:
            time.sleep(0.01)

    def get_clipboard_representation(self) -> list[Union[AppKit.NSSound, AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the sound.

        When the clipboard content is set to a sound, the raw sound data, the associated file URL, and the path string of the file are added to the clipboard.

        :return: The clipboard-codable form of the sound
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.file.xa_elem, self.file.xa_elem.path()]



class XAVideo(XAObject):
    """A class for interacting with video files and data.

    .. versionadded:: 0.1.0
    """
    def __init__(self, video_reference: Union[str, XAURL, XAPath]):
        if isinstance(video_reference, str):
            # References is to some kind of path or URL
            if "://" in video_reference:
                video_reference = XAURL(video_reference)
            else:
                video_reference = XAPath(video_reference)

        self.xa_elem = AVFoundation.AVURLAsset.alloc().initWithURL_options_(video_reference.xa_elem, { AVFoundation.AVURLAssetPreferPreciseDurationAndTimingKey: objc.YES })

    def reverse(self, output_file: Union[XAPath, str]):
        """Reverses the video and exports the result to the specified output file path.

        :param output_file: The file to export the reversed video to
        :type output_file: Union[XAPath, str]

        .. versionadded:: 0.1.0
        """
        if isinstance(output_file, str):
            output_file = XAPath(output_file)
        output_url = output_file.xa_elem

        reader = AVFoundation.AVAssetReader.alloc().initWithAsset_error_(self.xa_elem, None)[0]

        video_track = self.xa_elem.tracksWithMediaType_(AVFoundation.AVMediaTypeVideo)[-1]
        
        reader_output = AVFoundation.AVAssetReaderTrackOutput.alloc().initWithTrack_outputSettings_(video_track, { Quartz.CoreVideo.kCVPixelBufferPixelFormatTypeKey: Quartz.CoreVideo.kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange })

        reader.addOutput_(reader_output)
        reader.startReading()

        samples = []
        while sample := reader_output.copyNextSampleBuffer():
            samples.append(sample)

        writer = AVFoundation.AVAssetWriter.alloc().initWithURL_fileType_error_(output_url, AVFoundation.AVFileTypeMPEG4, None)[0]

        writer_settings = {
            AVFoundation.AVVideoCodecKey: AVFoundation.AVVideoCodecTypeH264,
            AVFoundation.AVVideoWidthKey: video_track.naturalSize().width,
            AVFoundation.AVVideoHeightKey: video_track.naturalSize().height,
            AVFoundation.AVVideoCompressionPropertiesKey: { AVFoundation.AVVideoAverageBitRateKey: video_track.estimatedDataRate() }
        }

        format_hint = video_track.formatDescriptions()[-1]
        writer_input = AVFoundation.AVAssetWriterInput.alloc().initWithMediaType_outputSettings_sourceFormatHint_(AVFoundation.AVMediaTypeVideo, writer_settings, format_hint)

        writer_input.setExpectsMediaDataInRealTime_(False)

        pixel_buffer_adaptor = AVFoundation.AVAssetWriterInputPixelBufferAdaptor.alloc().initWithAssetWriterInput_sourcePixelBufferAttributes_(writer_input, None)
        writer.addInput_(writer_input)
        writer.startWriting()
        writer.startSessionAtSourceTime_(CoreMedia.CMSampleBufferGetPresentationTimeStamp(samples[0]))

        for index, sample in enumerate(samples):
            presentation_time = CoreMedia.CMSampleBufferGetPresentationTimeStamp(sample)

            image_buffer_ref = CoreMedia.CMSampleBufferGetImageBuffer(samples[len(samples) - index - 1])
            if image_buffer_ref is not None:
                pixel_buffer_adaptor.appendPixelBuffer_withPresentationTime_(image_buffer_ref, presentation_time)

            while not writer_input.isReadyForMoreMediaData():
                time.sleep(0.1)

        self._spawn_thread(writer.finishWriting)
        return AVFoundation.AVAsset.assetWithURL_(output_url)

    def show_in_quicktime(self):
        """Shows the video in QuickTime Player.

        This will create a momentary video data file in the current working directory to store intermediary video data.

        .. versionadded:: 0.1.0
        """
        self.save("video-data-tmp.mp4")

        video_url = XAPath(os.getcwd() + "/video-data-tmp.mp4").xa_elem
        quicktime_url = XAPath("/System/Applications/QuickTime Player.app").xa_elem
        AppKit.NSWorkspace.sharedWorkspace().openURLs_withApplicationAtURL_configuration_completionHandler_([video_url], quicktime_url, None, None)
        time.sleep(1)

        AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(video_url.path(), None) 

    def save(self, file_path: Union[XAPath, str]):
        """Saves the video at the specified file path.

        :param file_path: The path to save the video at
        :type file_path: Union[XAPath, str]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        # Configure the export session
        export_session = AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(self.xa_elem, AVFoundation.AVAssetExportPresetHighestQuality)

        start_time = CoreMedia.CMTimeMake(0, 100)
        end_time = CoreMedia.CMTimeMake(self.xa_elem.duration().value * self.xa_elem.duration().timescale, 100)
        time_range =  CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time);

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(file_path.xa_elem)

        # Export to file path
        waiting = False
        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)
        
        while not waiting:
            time.sleep(0.01)
    