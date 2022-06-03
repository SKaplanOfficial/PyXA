import os
from typing import List, Literal, Union
import ScriptingBridge
from AppKit import NSPredicate
from XABase import XAApplication, XAObject, XAWindow, XAHasElements, xa_predicate_format

import threading

class XASBObject(XAObject):
    """A class for PyXA objects scriptable with AppleScript/JXA.

    .. seealso:: :class:`XAObject`
    """
    def __init__(self, properties):
        super().__init__(properties)

    def set_property(self, property_name, value):
        self.properties["sb_element"]._scriptingSetValue_forKey_(value, property_name)

class XAHasScriptableElements(XAObject):
    def scriptable_elements(self, specifier, filter, obj_type):
        ls = self.properties["sb_element"].__getattribute__(specifier)()
        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(xa_predicate_format(filter))
            ls = ls.filteredArrayUsingPredicate_(predicate)

        elements = []
        for element in ls:
            properties = {
                "parent": self,
                "appspace": self.properties["appspace"],
                "workspace": self.properties["workspace"],
                "element": element,
                "appref": self.properties["appref"],
                "system_events": self.properties["system_events"],
            }
            elements.append(obj_type(properties))
        return elements

    def scriptable_element_with_properties(self, specifier, filter, obj_type):
        if isinstance(filter, int):
            element = self.properties["sb_element"].__getattribute__(specifier)()[filter]
            properties = {
                "parent": self,
                "appspace": self.properties["appspace"],
                "workspace": self.properties["workspace"],
                "element": element,
                "appref": self.properties["appref"],
                "system_events": self.properties["system_events"],
            }
            return obj_type(properties)
        return self.scriptable_elements(specifier, filter, obj_type)[0]

    def first_scriptable_element(self, specifier, obj_type):
        element = self.properties["sb_element"].__getattribute__(specifier)()[0]
        properties = {
            "parent": self,
            "appspace": self.properties["appspace"],
            "workspace": self.properties["workspace"],
            "element": element,
            "appref": self.properties["appref"],
            "system_events": self.properties["system_events"],
        }
        return obj_type(properties)

    def last_scriptable_element(self, specifier, obj_type):
        element = self.properties["sb_element"].__getattribute__(specifier)()[-1]
        properties = {
            "parent": self,
            "appspace": self.properties["appspace"],
            "workspace": self.properties["workspace"],
            "element": element,
            "appref": self.properties["appref"],
            "system_events": self.properties["system_events"],
        }
        return obj_type(properties)

### Mixins
## Property Mixins
class XASBCloseable(XAObject):
    def close(self) -> XAObject:
        """Closes a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XAObject
        """
        saving_options = {
            'yes': 0x79657320,
            'no':  0x6E6F2020,
            'ask': 0x61736B20,
        }
        self.properties["element"].closeSaving_savingIn_(saving_options["no"], "~")
        return self

# TODO: FIX THIS
class XASBSaveable(XAObject):
    def save(self, location: str = None) -> XAObject:
        """Saves a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XAObject
        """
        if location is None:
            location = "/Users/steven/Downloads/test.pdf"
        self.properties["element"].saveIn_as_(None, None)
        return self

class XASBPrintable(XAObject):
    def __print_dialog(self, show_prompt: bool = True):
        """Displays a print dialog."""
        try:
            if "sb_element" in self.properties:
                self.properties["sb_element"].printWithProperties_(None)
            else:
                self.properties["element"].printWithProperties_(None)
        except:
            try:
                if "sb_element" in self.properties:
                    self.properties["sb_element"].print_withProperties_printDialog_(self.properties["sb_element"], None, show_prompt)
                else:
                    self.properties["element"].print_withProperties_printDialog_(self.properties["element"], None, show_prompt)
            except:
                if "sb_element" in self.properties:
                    self.properties["sb_element"].print_printDialog_withProperties_(self.properties["sb_element"], show_prompt, None)
                else:
                    self.properties["element"].print_printDialog_withProperties_(self.properties["element"], show_prompt, None)

    def print(self, properties: dict = None, print_dialog = None) -> XAObject:
        """Prints a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XAObject

        .. versionchanged:: 0.0.2
           Printing now initialized from a separate thread to avoid delaying main thread

        .. versionadded:: 0.0.1
        """
        print_thread = threading.Thread(target=self.__print_dialog, name="Print", daemon=True)
        print_thread.start()
        return self

class XASBDeletable(XAObject):
    def delete(self):
        self.properties["element"].delete()

class XASBApplication(XASBObject, XAApplication, XAHasScriptableElements):
    """An application class for scriptable applications.

    .. seealso:: :class:`XAApplication`, :class:`XAWindow`
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties["sb_element"] = ScriptingBridge.SBApplication.alloc().initWithBundleIdentifier_(properties["element"].bundleIdentifier())
        self.properties["window_class"] = XASBWindow

        self.element_properties = self.properties["sb_element"].properties()
        self.name = self.properties["sb_element"].name()
        self.frontmost = self.properties["sb_element"].frontmost()
        self.version = self.properties["sb_element"].version()

    ### Windows
    def windows(self, filter: dict = None) -> List['XASBWindow']:
        return super().scriptable_elements("windows", filter, self.properties["window_class"])

    def window(self, filter: Union[int, dict]) -> 'XASBWindow':
        return super().scriptable_element_with_properties("windows", filter, self.properties["window_class"])

    def front_window(self) -> 'XAWindow':
        return super().first_scriptable_element("windows", self.properties["window_class"])


class XASBWindow(XASBObject):
    def __init__(self, properties):
        super().__init__(properties)

    def collapse(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow
        """
        self.set_property("miniaturized", True)
        return self

    def uncollapse(self) -> 'XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XAWindow
        """
        self.set_property("miniaturized", False)
        return self

    # TODO:
    # def fullscreen(self):
    #     print(dir(self.element))