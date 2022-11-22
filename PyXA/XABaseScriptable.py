from enum import Enum
from pprint import pprint
from typing import List, Tuple, Union, Self
import threading
import AppKit
import ScriptingBridge

from PyXA import XABase

import signal

from .XAProtocols import XACloseable
from .XATypes import XAPoint, XARectangle

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




class XASBApplication(XASBObject, XABase.XAApplication):
    """An application class for scriptable applications.

    .. seealso:: :class:`XABase.XAApplication`, :class:`XABase.XAWindow`
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = XABase.OSType('yes ') #: Save the file
        NO  = XABase.OSType('no  ') #: Do not save the file
        ASK = XABase.OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_scel = ScriptingBridge.SBApplication.alloc().initWithURL_(self.xa_elem.bundleURL())
        self.xa_wcls = XASBWindow

    @property
    def front_window(self) -> 'XASBWindow':
        """The front window of the application.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.windows()[0], self.xa_wcls)

    def windows(self, filter: dict = None) -> 'XASBWindowList':
        try:
            return self._new_element(self.xa_scel.windows(), XASBWindowList)
        except AttributeError:
            return self._new_element([], XASBWindowList)




class XASBWindowList(XABase.XAList):
    """A wrapper around a list of windows.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, None, filter)
        self.xa_ocls = self.xa_prnt.xa_wcls

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    # TODO

    def collapse(self):
        """Collapses all windows in the list.

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.collapse()

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of each window in the list.

        When the clipboard content is set to a list of windows, the name of each window is added to the clipboard.

        :return: A list of window names
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASBWindow(XASBObject, XACloseable):
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The title of the window.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def id(self) -> str:
        """The unique identifier for the window.
        """
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        """The index of the window, ordered front to back.
        """
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def bounds(self) -> XARectangle:
        """The bounding rectangle of the window.
        """
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return XARectangle(origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: Union[tuple[int, int, int, int], XARectangle]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        """Whether the window has a close button.
        """
        return self.xa_elem.closeable()

    @property
    def resizable(self) -> bool:
        """Whether the window can be resized.
        """
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        """Whether the window is currently visible.
        """
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        """Whether the window has a zoom button.
        """
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        """Whether the window is currently zoomed.
        """
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def miniaturizable(self) -> bool:
        """Whether the window can be miniaturized.
        """
        try:
            return self.xa_elem.miniaturizable()
        except Exception as e:
            print(e)

    @property
    def miniaturized(self) -> bool:
        """Whether the window is currently miniaturized.
        """
        try:
            return self.xa_elem.miniaturized()
        except Exception as e:
            print(e)

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        try:
            self.set_property("miniaturized", miniaturized)
        except Exception as e:
            print(e)

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

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the window.

        When the clipboard content is set to a window, the name of the window is added to the clipboard.

        :return: The name of the window
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"