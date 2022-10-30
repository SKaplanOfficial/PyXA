
from time import sleep
from typing import Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable, XACloseable

class XAVLCApplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """VLC's top level scripting object.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAVLCWindow
        
        self.properties: dict #: All properties of VLC
        self.frontmost: bool #: Whether VLC is the active application
        self.name: str #: The name of the application
        self.version: str #: The version of VLC.app
        self.audio_desync: int #: The audio desynchronization preference from -2147483648 to 2147483647, where 0 is default.
        self.audio_volume: int #: The volume of the current playlist item from 0 to 512, where 256 is 100%.
        self.current_time: int #: The current time of the current playlist item in seconds.
        self.duration_of_current_item: int #: The duration of the current playlist item in seconds.
        self.fullscreen_mode: bool #: Indicates wheter fullscreen is enabled or not.
        self.muted: bool #: Is VLC currently muted?
        self.name_of_current_item: str #: Name of the current playlist item.
        self.path_of_current_item: XABase.XAPath #: Path to the current playlist item.
        self.playback_shows_menu: bool #: Indicates whether a DVD menu is currently being shown.
        self.playing: bool #: Is VLC playing an item?

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def audio_desync(self) -> int:
        return self.xa_scel.audioDesync()

    @audio_desync.setter
    def audio_desync(self, audio_desync: int):
        self.set_property("audioDesync", audio_desync)

    @property
    def audio_volume(self) -> int:
        return self.xa_scel.audioVolume()

    @audio_volume.setter
    def audio_volume(self, audio_volume: int):
        self.set_property("audioVolume", audio_volume)

    @property
    def current_time(self) -> int:
        return self.xa_scel.currentTime()

    @current_time.setter
    def current_time(self, current_time: int):
        self.set_property("currentTime", current_time)

    @property
    def duration_of_current_item(self) -> int:
        return self.xa_scel.durationOfCurrentItem()

    @property
    def fullscreen_mode(self) -> bool:
        return self.xa_scel.fullscreenMode()

    @fullscreen_mode.setter
    def fullscreen_mode(self, fullscreen_mode: bool):
        self.set_property("fullscreenMode", fullscreen_mode)

    @property
    def muted(self) -> bool:
        return self.xa_scel.muted()

    @property
    def name_of_current_item(self) -> str:
        return self.xa_scel.nameOfCurrentItem()

    @property
    def path_of_current_item(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_scel.pathOfCurrentItem())

    @property
    def playback_shows_menu(self) -> bool:
        return self.xa_scel.playbackShowsMenu()

    @property
    def playing(self) -> bool:
        return self.xa_scel.playing()

    def open(self, target: Union[XABase.XAURL, XABase.XAPath, str]) -> None:
        """Opens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to open.
        :type target: Union[XABase.XAURL, XABase.XAPath, str]

        :Example 1: Open files from file paths

        >>> import PyXA
        >>> app = PyXA.Application("VLC")
        >>> app.open("/Users/exampleUser/Downloads/Example.avi")
        >>> 
        >>> path = PyXA.XAPath("/Users/exampleUser/Documents/Example.m4v")
        >>> app.open(path)

        :Example 2: Open URLs

        >>> import PyXA
        >>> app = PyXA.Application("VLC")
        >>> app.open("https://upload.wikimedia.org/wikipedia/commons/transcoded/0/0f/Baby_pelican.ogg/Baby_pelican.ogg.mp3")
        >>> 
        >>> url = PyXA.XAURL("https://www.youtube.com/watch?v=e9B3E_DnnWw")
        >>> app.open(url)

        .. versionadded:: 0.0.8
        """
        if isinstance(target, str):
            if target.startswith("/"):
                target = XABase.XAPath(target)
            else:
                target = XABase.XAURL(target)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([target.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)

    def activate_menu_item(self):
        """Activates the currently focused menu item.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.activateMenuItem()

    def fullscreen(self):
        """Toggle between fullscreen and windowed mode.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.fullscreen()
    
    def get_url(self, url: Union[XABase.XAURL, XABase.XAPath, str]):
        """Get a URL without playing it.

        .. versionadded:: 0.0.8
        """
        self.open(url)
        sleep(0.01)
        self.stop()
    
    def move_menu_focus_down(self):
        """Moves the menu focus down.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.moveMenuFocusDown()
    
    def move_menu_focus_left(self):
        """Moves the menu focus to the left.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.moveMenuFocusLeft()
    
    def move_menu_focus_right(self):
        """Moves the menu focus to the right.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.moveMenuFocusRight()
    
    def move_menu_focus_up(self):
        """Moves the menu focus up.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.moveMenuFocusUp()
    
    def mute(self):
        """Mute the audio of the item or unmute it if it was muted.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.mute()
    
    def next(self):
        """Go to the next item in the playlist or the next chapter in the DVD/VCD.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.next()
    
    def open_url(self, url: Union[XABase.XAURL, XABase.XAPath, str]):
        """Open a media URL.

        .. versionadded:: 0.0.8
        """
        self.open(url)
    
    def play(self):
        """Start playing the current playlistitem or pause it when it is already playing.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.play()
    
    def previous(self):
        """Go to the previous item in the playlist or the previous chapter in the DVD/VCD.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.previous()
    
    def step_backward(self):
        """Step the current playlist item backward the specified step width (default is 2) (1=extraShort, 2=short, 3=medium, 4=long).

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.stepBackward()
    
    def step_forward(self):
        """Step the current playlist item forward the specified step width (default is 2) (1=extraShort, 2=short, 3=medium, 4=long).

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.stepForward()
    
    def stop(self):
        """Stop playing the current playlist item.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.stop()
    
    def volume_down(self):
        """Bring the volume down by one step. There are 32 steps from 0 to 400% volume.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.volumeDown()
    
    def volume_up(self):
        """Bring the volume up by one step. There are 32 steps from 0 to 400% volume.

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.volumeUp()

    def documents(self, filter: Union[dict, None] = None) -> 'XAVLCDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter documents by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of documents
        :rtype: XAVLCDocumentList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.documents(), XAVLCDocumentList, filter)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        .. versionadded:: 0.0.9
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XAVLCDocument)



class XAVLCDocumentList(XABase.XAList, XACloseable, XAClipboardCodable):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAVLCDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def path(self) -> list[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XABase.XAPath(x) for x in ls]

    def by_name(self, name: str) -> Union['XAVLCDocument', None]:
        """Retrieves the first document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAVLCDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAVLCDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAVLCDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("modified", modified)

    def by_path(self, path: Union[str, XABase.XAPath]) -> Union['XAVLCDocument', None]:
        """Retrieves the first document whose file path matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAVLCDocument, None]
        
        .. versionadded:: 0.0.9
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        return self.by_property("path", path.xa_elem)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, the name of each document is added to the clipboard.

        :return: A list of document names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAVLCDocument(XABase.XAObject):
    """A document open in VLC.app.
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the document
        self.modified: bool #: Has the document been modified since the last save?
        self.name: str #: The document's name.
        self.path: XABase.XAPath #: The document's path.

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: Union[str, XABase.XAPath]):
        if isinstance(path, str):
            path = XABase.XAPath(path)
        self.path = path
        self.set_property("path", path.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAVLCWindow(XABaseScriptable.XASBWindow):
    """A window of VLC.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.bounds: tuple[tuple[int, int], tuple[int, int]] #: The bounding rectangle of the window.
        self.closeable: bool #: Whether the window has a close box.
        self.document: XAVLCDocument #: The document whose contents are being displayed in the window.
        self.floating: bool #: Whether the window floats.
        self.id: int #: The unique identifier of the window.
        self.index: int #: The index of the window, ordered front to back.
        self.miniaturizable: bool #: Whether the window can be miniaturized.
        self.miniaturized: bool #: Whether the window is currently miniaturized.
        self.modal: bool #: Whether the window is the application's current modal window.
        self.name: str #: The full title of the window.
        self.resizable: bool #: Whether the window can be resized.
        self.titled: bool #: Whether the window has a title bar.
        self.visible: bool #: Whether the window is currently visible.
        self.zoomable: bool #: Whether the window can be zoomed.
        self.zoomed: bool #: Whether the window is currently zoomed.

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        bounds = self.xa_elem.bounds()
        origin = bounds.origin
        size = bounds.size
        return (origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: tuple[int, int, int, int]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def document(self) -> XAVLCDocument:
        return self.xa_elem.document()

    @document.setter
    def document(self, document: XAVLCDocument):
        self.set_property("document", document.xa_elem)

    @property
    def floating(self) -> bool:
        return self.xa_elem.floating()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property("miniaturized", miniaturized)

    @property
    def modal(self) -> bool:
        return self.xa_elem.modal()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def titled(self) -> bool:
        return self.xa_elem.titled()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)