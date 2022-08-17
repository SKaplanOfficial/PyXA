
from time import sleep
from typing import Tuple, Union, List

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable

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
        self.path_of_current_item: str #: Path to the current playlist item.
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

    @property
    def audio_volume(self) -> int:
        return self.xa_scel.audioVolume()

    @property
    def current_time(self) -> int:
        return self.xa_scel.currentTime()

    @property
    def duration_of_current_item(self) -> int:
        return self.xa_scel.durationOfCurrentItem()

    @property
    def fullscreen_mode(self) -> bool:
        return self.xa_scel.fullscreenMode()

    @property
    def muted(self) -> bool:
        return self.xa_scel.muted()

    @property
    def name_of_current_item(self) -> str:
        return self.xa_scel.nameOfCurrentItem()

    @property
    def path_of_current_item(self) -> str:
        return self.xa_scel.pathOfCurrentItem()

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
        """Get a URL.

        .. versionadded:: 0.0.8
        """
        self.open(url)
        sleep(0.1)
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


class XAVLCDocumentList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAVLCDocument, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def by_name(self, name: str) -> Union['XAVLCDocument', None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAVLCDocument', None]:
        return self.by_property("modified", modified)

    def by_path(self, path: str) -> Union['XAVLCDocument', None]:
        return self.by_property("path", path)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, the name of each document is added to the clipboard.

        :return: A list of document names
        :rtype: List[str]

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
        
        self.modified: bool #: Has the document been modified since the last save?
        self.name: str #: The document's name.
        self.path: str #: The document's path.

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAVLCWindow(XABaseScriptable.XASBWindow):
    """A window of VLC.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window.
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
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def document(self) -> XAVLCDocument:
        return self.xa_elem.document()

    @property
    def floating(self) -> bool:
        return self.xa_elem.floating()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @property
    def modal(self) -> bool:
        return self.xa_elem.modal()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def titled(self) -> bool:
        return self.xa_elem.titled()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()