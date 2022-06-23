from typing import List, Union
import threading
import ScriptingBridge
from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase

import signal

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class XASBObject(XABase.XAObject):
    """A class for PyXA objects scriptable with AppleScript/JXA.

    .. seealso:: :class:`XABase.XAObject`
    """
    def __init__(self, properties):
        super().__init__(properties)

    def set_property(self, property_name, value):
        parts = property_name.split("_")
        titled_parts = [part.title() for part in parts[1:]]
        property_name = parts[0] + "".join(titled_parts)
        self.xa_scel.setValue_forKey_(value, property_name)

class XAHasScriptableElements(XABase.XAObject):
    def scriptable_elements(self, specifier, filter, obj_type):
        self.elements = []
        ls = self.xa_scel.__getattribute__(specifier)()
        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            ls = ls.filteredArrayUsingPredicate_(predicate)

        def append_with_timeout(obj: ScriptingBridge.SBObject, index: int, stop: bool):
            with timeout(seconds = 2):
                properties = {
                    "parent": self,
                    "appspace": self.xa_apsp,
                    "workspace": self.xa_wksp,
                    "element": obj,
                    "scriptable_element": obj,
                    "appref": self.xa_aref,
                    "system_events": self.xa_sevt,
                }
                self.elements.append(obj_type(properties))

        ls.enumerateObjectsUsingBlock_(append_with_timeout)
        return self.elements

    def scriptable_element_with_properties(self, specifier, filter, obj_type):
        if isinstance(filter, int):
            element = self.xa_scel.__getattribute__(specifier)()[filter]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "scriptable_element": element,
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
            "scriptable_element": element,
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
            "scriptable_element": element,
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
        self.name = self.xa_scel.name() #: The title of the window
        self.id = self.xa_scel.id() #: The unique identifier for the window
        self.index = self.xa_scel.index() #: The index of the window, ordered front to back
        self.bounds = self.xa_scel.bounds() #: The bounding rectangle of the window
        self.closeable = self.xa_scel.closeable() #: Whether the window has a close button
        self.resizable = self.xa_scel.resizable() #: Whether the window can be resized
        self.visible = self.xa_scel.visible() #: Whether the window is currently visible
        self.zoomable = self.xa_scel.zoomable() #: Whether the window has a zoom button
        self.zoomed = self.xa_scel.zoomed() #: Whether the window is currently zoomed
        self.__document = None #: The current document displayed in the window

    def collapse(self) -> 'XABase.XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XABase.XAWindow
        """
        self.miniaturized = True
        self.set_property("miniaturized", True)
        return self

    def uncollapse(self) -> 'XABase.XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XABase.XAWindow
        """
        self.miniaturized = False
        self.set_property("miniaturized", False)
        return self

    def toggle_zoom(self) -> 'XABase.XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XABase.XAWindow
        """
        self.zoomed = not self.zoomed
        self.set_property("zoomed", self.zoomed)
        return self

    # TODO:
    # def fullscreen(self):
    #     print(dir(self.element))