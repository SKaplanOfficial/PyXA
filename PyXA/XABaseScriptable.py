from typing import List, Union
import threading
import ScriptingBridge
from AppKit import NSPredicate

from PyXA import XABase

class XASBObject(XABase.XAObject):
    """A class for PyXA objects scriptable with AppleScript/JXA.

    .. seealso:: :class:`XABase.XAObject`
    """
    def __init__(self, properties):
        super().__init__(properties)

    def set_property(self, property_name, value):
        self.xa_scel._scriptingSetValue_forKey_(value, property_name)

class XAHasScriptableElements(XABase.XAObject):
    def scriptable_elements(self, specifier, filter, obj_type):
        ls = self.xa_scel.__getattribute__(specifier)()
        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            ls = ls.filteredArrayUsingPredicate_(predicate)

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

    def scriptable_element_with_properties(self, specifier, filter, obj_type):
        if isinstance(filter, int):
            element = self.xa_scel.__getattribute__(specifier)()[filter]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            return obj_type(properties)
        return self.scriptable_elements(specifier, filter, obj_type)[0]

    def first_scriptable_element(self, specifier, obj_type):
        element = self.xa_scel.__getattribute__(specifier)()[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)

    def last_scriptable_element(self, specifier, obj_type):
        element = self.xa_scel.__getattribute__(specifier)()[-1]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)

### Mixins
## Property Mixins
class XASBCloseable(XABase.XAObject):
    def close(self) -> XABase.XAObject:
        """Closes a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XABase.XAObject
        """
        saving_options = {
            'yes': 0x79657320,
            'no':  0x6E6F2020,
            'ask': 0x61736B20,
        }
        self.xa_elem.closeSaving_savingIn_(saving_options["no"], "~")
        return self

# TODO: FIX THIS
class XASBSaveable(XABase.XAObject):
    def save(self, location: str = None) -> XABase.XAObject:
        """Saves a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XABase.XAObject
        """
        if location is None:
            location = "/Users/steven/Downloads/test.pdf"
        self.xa_elem.saveIn_as_(None, None)
        return self

class XASBPrintable(XABase.XAObject):
    def __print_dialog(self, show_prompt: bool = True):
        """Displays a print dialog."""
        try:
            if self.xa_scel is not None:
                self.xa_scel.printWithProperties_(None)
            else:
                self.xa_elem.printWithProperties_(None)
        except:
            try:
                if self.xa_scel is not None:
                    self.xa_scel.print_withProperties_printDialog_(self.xa_scel, None, show_prompt)
                else:
                    self.xa_elem.print_withProperties_printDialog_(self.xa_elem, None, show_prompt)
            except:
                if self.xa_scel is not None:
                    self.xa_scel.print_printDialog_withProperties_(self.xa_scel, show_prompt, None)
                else:
                    self.xa_elem.print_printDialog_withProperties_(self.xa_elem, show_prompt, None)

    def print(self, properties: dict = None, print_dialog = None) -> XABase.XAObject:
        """Prints a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XABase.XAObject

        .. versionchanged:: 0.0.2
           Printing now initialized from a separate thread to avoid delaying main thread

        .. versionadded:: 0.0.1
        """
        print_thread = threading.Thread(target=self.__print_dialog, name="Print", daemon=True)
        print_thread.start()
        return self

class XASBDeletable(XABase.XAObject):
    def delete(self):
        self.xa_elem.delete()

class XASBApplication(XASBObject, XABase.XAApplication, XAHasScriptableElements):
    """An application class for scriptable applications.

    .. seealso:: :class:`XABase.XAApplication`, :class:`XABase.XAWindow`
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_scel = ScriptingBridge.SBApplication.alloc().initWithBundleIdentifier_(self.xa_elem.bundleIdentifier())
        self.xa_wcls = XASBWindow

        self.element_properties = self.xa_scel.properties()
        self.name = self.xa_scel.name()
        self.frontmost = self.xa_scel.frontmost()
        self.version = self.xa_scel.version()

    ### Windows
    def windows(self, filter: dict = None) -> List['XASBWindow']:
        return super().scriptable_elements("windows", filter, self.xa_wcls)

    def window(self, filter: Union[int, dict]) -> 'XASBWindow':
        return super().scriptable_element_with_properties("windows", filter, self.xa_wcls)

    def front_window(self) -> 'XABase.XAWindow':
        return super().first_scriptable_element("windows", self.xa_wcls)


class XASBWindow(XASBObject):
    def __init__(self, properties):
        super().__init__(properties)

    def collapse(self) -> 'XABase.XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XABase.XAWindow
        """
        self.set_property("miniaturized", True)
        return self

    def uncollapse(self) -> 'XABase.XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XABase.XAWindow
        """
        self.set_property("miniaturized", False)
        return self

    # TODO:
    # def fullscreen(self):
    #     print(dir(self.element))