
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

    # TODO: Update properties to new format
    @property
    def properties(self) -> dict:
        """All properties of the VLC application.
        """
        return self.xa_elem.properties()

    @property
    def frontmost(self) -> bool:
        """Whether VLC is the active application.
        """
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of VLC.app.
        """
        return self.xa_scel.version()

    @property
    def audio_desync(self) -> int:
        """The audio desynchronization preference from -2147483648 to 2147483647, where 0 is default.
        """
        return self.xa_scel.audioDesync()

    @audio_desync.setter
    def audio_desync(self, audio_desync: int):
        self.set_property("audioDesync", audio_desync)

    @property
    def audio_volume(self) -> int:
        """The volume of the current playlist item from 0 to 512, where 256 is 100%.
        """
        return self.xa_scel.audioVolume()

    @audio_volume.setter
    def audio_volume(self, audio_volume: int):
        self.set_property("audioVolume", audio_volume)

    @property
    def current_time(self) -> int:
        """The current time of the current playlist item in seconds.
        """
        return self.xa_scel.currentTime()

    @current_time.setter
    def current_time(self, current_time: int):
        self.set_property("currentTime", current_time)

    @property
    def duration_of_current_item(self) -> int:
        """The duration of the current playlist item in seconds.
        """
        return self.xa_scel.durationOfCurrentItem()

    @property
    def fullscreen_mode(self) -> bool:
        """Indicates whether fullscreen is enabled or not.
        """
        return self.xa_scel.fullscreenMode()

    @fullscreen_mode.setter
    def fullscreen_mode(self, fullscreen_mode: bool):
        self.set_property("fullscreenMode", fullscreen_mode)

    @property
    def muted(self) -> bool:
        """Is VLC currently muted?
        """
        return self.xa_scel.muted()

    @property
    def name_of_current_item(self) -> str:
        """Name of the current playlist item.
        """
        return self.xa_scel.nameOfCurrentItem()

    @property
    def path_of_current_item(self) -> XABase.XAPath:
        """Path to the current playlist item.
        """
        return XABase.XAPath(self.xa_scel.pathOfCurrentItem())

    @property
    def playback_shows_menu(self) -> bool:
        """Indicates whether a DVD menu is currently being shown.
        """
        return self.xa_scel.playbackShowsMenu()

    @property
    def playing(self) -> bool:
        """Is VLC playing an item?
        """
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

    @property
    def properties(self) -> dict:
        """All properties of the document.
        """
        return self.xa_elem.properties()

    @property
    def modified(self) -> bool:
        """Has the document been modified since the last save?
        """
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        """The document's name.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> XABase.XAPath:
        """The document's path.
        """
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

    @property
    def document(self) -> XAVLCDocument:
        """The document whose contents are being displayed in the window.
        """
        return self.xa_elem.document()

    @document.setter
    def document(self, document: XAVLCDocument):
        self.set_property("document", document.xa_elem)

    @property
    def floating(self) -> bool:
        """Whether the window floats.
        """
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is the application's current modal window.
        """
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar.
        """
        return self.xa_elem.titled()