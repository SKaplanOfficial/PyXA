from enum import Enum
from pprint import pprint
from typing import List, Tuple, Union
import threading
import ScriptingBridge

from PyXA import XABase

import signal

from .XAProtocols import XACloseable

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
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

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