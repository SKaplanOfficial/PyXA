from typing import List, Tuple, Union
import threading
import ScriptingBridge

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
        if self.xa_scel is not None:
            self.xa_scel.setValue_forKey_(value, property_name)
        else:
            self.xa_elem.setValue_forKey_(value, property_name)

class XAHasScriptableElements(XABase.XAObject):
    def scriptable_elements(self, specifier, filter, obj_type):
        self.elements = []
        ls = self.xa_scel.__getattribute__(specifier)()
        if filter is not None:
            ls = XABase.XAPredicate().from_dict(filter).evaluate(ls)

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




class XASBApplication(XASBObject, XABase.XAApplication, XAHasScriptableElements):
    """An application class for scriptable applications.

    .. seealso:: :class:`XABase.XAApplication`, :class:`XABase.XAWindow`
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_scel = ScriptingBridge.SBApplication.alloc().initWithBundleIdentifier_(self.xa_elem.bundleIdentifier())
        self.xa_wcls = XASBWindow

    def windows(self, filter: dict = None) -> 'XASBWindowList':
        return self._new_element(self.xa_scel.windows(), XASBWindowList)

    def front_window(self) -> 'XASBWindow':
        return self._new_element(self.xa_scel.windows()[0], self.xa_wcls)




class XASBWindowList(XABase.XAList):
    """A wrapper around a list of windows.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, None, filter)
        self.xa_ocls = self.xa_prnt.xa_wcls

    # def name(self) -> List[str]:
    #     return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def collapse(self):
        """Collapses all windows in the list.

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.collapse()

class XASBWindow(XASBObject):
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: str #: The unique identifier for the window
        self.index: int #: The index of the window, ordered front to back
        self.bounds: Tuple[Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window has a zoom button
        self.zoomed: bool  #: Whether the window is currently zoomed

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def id(self) -> str:
        return self.xa_scel.id()

    @property
    def index(self) -> int:
        return self.xa_scel.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int]]:
        return self.xa_scel.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_scel.closeable()

    @property
    def resizable(self) -> bool:
        return self.xa_scel.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_scel.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_scel.zoomed()

    def collapse(self) -> 'XABase.XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XABase.XAWindow
        """
        try:
            self.set_property("miniaturized", True)
        except:
            try:
                self.set_property("minimized", True)
            except:
                self.set_property("collapsed", True)
        return self

    def uncollapse(self) -> 'XABase.XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XABase.XAWindow
        """
        try:
            self.set_property("miniaturized", False)
        except:
            try:
                self.set_property("minimized", False)
            except:
                self.set_property("collapsed", False)
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