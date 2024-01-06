""".. versionadded:: 0.0.1

Control the macOS TV application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Union

import ScriptingBridge

from PyXA import XABase
from PyXA import XABaseScriptable
from PyXA.XAProtocols import XACanOpenPath
from PyXA.XAEvents import event_from_str


class TVObjectClass(Enum):
    APPLICATION = "capp"
    ARTWORK = "cArt"
    BROWSER_WINDOW = "cBrW"
    ENCODER = "cEnc"
    FILE_TRACK = "cFlT"
    FOLDER_PlAYLIST = "cFoP"
    ITEM = "cobj"
    LIBRARY_PLAYLIST = "cLiP"
    MINIPLAYER_WINDOW = "cMPW"
    PLAYLIST = "cPly"
    PLAYLIST_WINDOW = "cPlW"
    SHARED_TRACK = "cShT"
    SOURCE = "cSrc"
    TRACK = "cTrk"
    URL_TRACK = "cURT"
    USER_PLAYLIST = "cUsP"
    VIDEO_WINDOW = "cNPW"
    WINDOW = "cwin"


class XATVApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XATVWindow`, class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """Object types able to be created by the application."""

        PLAYLIST = "playlist"
        USER_PLAYLIST = "user_playlist"
        FOLDER_PLAYLIST = "folder_playlist"
        LIBRARY_PLAYLIST = "library_playlist"
        TRACK = "track"
        URL_TRACK = "url_track"
        SHARED_TRACK = "shared_track"
        FILE_TRACK = "file_track"
        ARTWORK = "artwork"
        WINDOW = "window"
        BROWSER_WINDOW = "browser_window"
        PLAYLIST_WINDOW = "playlist_window"
        VIDEO_WINDOW = "video_window"
        SOURCE = "source"

    class PlayerState(Enum):
        """States of the music player."""

        STOPPED = XABase.OSType("kPSS")  #: The player is stopped
        PLAYING = XABase.OSType("kPSP")  #: The player is playing
        PAUSED = XABase.OSType("kPSp")  #: The player is paused
        FAST_FORWARDING = XABase.OSType("kPSF")  #: The player is fast forwarding
        REWINDING = XABase.OSType("kPSR")  #: The player is rewinding

    class SourceKind(Enum):
        """Types of sources for media items."""

        LIBRARY = XABase.OSType("kLib")  #: A library source
        SHARED_LIBRARY = XABase.OSType("kShd")  #: A shared library source
        ITUNES_STORE = XABase.OSType("kITS")  #: The iTunes Store source
        UNKNOWN = XABase.OSType("kUnk")  #: An unknown source

    class SearchFilter(Enum):
        """Filter restrictions on search results."""

        ALBUMS = XABase.OSType("kSrL")  #: Search albums
        ALL = XABase.OSType("kAll")  #: Search all
        ARTISTS = XABase.OSType("kSrR")  #: Search artists
        DISPLAYED = XABase.OSType("kSrV")  #: Search the currently displayed playlist
        NAMES = XABase.OSType("kSrS")  #: Search track names only

    class PlaylistKind(Enum):
        """Types of special playlists."""

        NONE = XABase.OSType("kNon")  #: An unknown playlist kind
        UNKNOWN = 0  #: An unknown playlist kind
        FOLDER = XABase.OSType("kSpF")  #: A folder
        LIBRARY = XABase.OSType("kSpL")  #: The system library playlist
        MOVIES = XABase.OSType("kSpI")  #: A playlist containing movie items
        TV_SHOWS = XABase.OSType("kSpT")  #: A playlist containing TV show items

    class MediaKind(Enum):
        """Types of media items."""

        HOME_VIDEO = XABase.OSType("kVdH")  #: A home video track
        MOVIE = XABase.OSType("kVdM")  #: A movie track
        TV_SHOW = XABase.OSType("kVdT")  #: A TV show track
        UNKNOWN = XABase.OSType("kUnk")  #: An unknown media item kind

    class RatingKind(Enum):
        """Types of ratings for media items."""

        USER = XABase.OSType("kRtU")  #: A user-inputted rating
        COMPUTED = XABase.OSType("kRtC")  #: A computer generated rating

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATVWindow

    @property
    def current_playlist(self) -> "XATVPlaylist":
        """The playlist containing the currently targeted track."""
        return self._new_element(self.xa_scel.currentPlaylist(), XATVPlaylist)

    @property
    def current_stream_title(self) -> str:
        """The name of the currently streaming track."""
        return self.xa_scel.currentStreamTitle()

    @property
    def current_stream_url(self) -> str:
        """The URL of the currently streaming track."""
        return self.xa_scel.currentStreamURL()

    @property
    def current_track(self) -> "XATVTrack":
        """The currently targeted track."""
        return self._new_element(self.xa_scel.currentTrack(), XATVTrack)

    @property
    def fixed_indexing(self) -> bool:
        """Whether the track indices are independent of the order of the current playlist or not."""
        return self.xa_scel.fixedIndexing()

    @fixed_indexing.setter
    def fixed_indexing(self, fixed_indexing: bool):
        self.set_property("fixedIndexing", fixed_indexing)

    @property
    def frontmost(self) -> bool:
        """Whether the application is active or not."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def full_screen(self) -> bool:
        """Whether the app is fullscreen or not."""
        return self.xa_scel.fullScreen()

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.set_property("fullScreen", full_screen)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def mute(self) -> bool:
        """Whether sound output is muted or not."""
        return self.xa_scel.mute()

    @mute.setter
    def mute(self, mute: bool):
        self.set_property("mute", mute)

    @property
    def player_position(self) -> float:
        """The time elapsed in the current track."""
        return self.xa_scel.playerPosition()

    @player_position.setter
    def player_position(self, player_position: float):
        self.set_property("playerPosition", player_position)

    @property
    def player_state(self) -> "XATVApplication.PlayerState":
        """Whether the player is playing, paused, stopped, fast forwarding, or rewinding."""
        return XATVApplication.PlayerState(self.xa_scel.playerState())

    @property
    def selection(self) -> "XATVItemList":
        """The selected media items."""
        return self._new_element(self.xa_scel.selection().get(), XATVTrackList)

    @property
    def sound_volume(self) -> int:
        """The sound output volume."""
        return self.xa_scel.soundVolume()

    @sound_volume.setter
    def sound_volume(self, sound_volume: int):
        self.set_property("soundVolume", sound_volume)

    @property
    def version(self) -> str:
        """The version of the application."""
        return self.xa_scel.version()

    def play(
        self, item: "XATVItem" = None, play_once: bool = True
    ) -> "XATVApplication":
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XATVItem, optional
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        if item is None:
            self.xa_scel.playOnce_(play_once)
        else:
            self.xa_scel.play_once_(item.xa_elem, play_once)
        return self

    def playpause(self) -> "XATVApplication":
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> "XATVApplication":
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> "XATVApplication":
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> "XATVApplication":
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> "XATVApplication":
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> "XATVApplication":
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> "XATVApplication":
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> "XATVApplication":
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> "XATVApplication":
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> "XATVApplication":
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XATVApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> "XATVApplication":
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def current_track(self) -> "XATVTrack":
        """Returns the currently playing (or paused but not stopped) track.

        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "element": self.xa_scel.currentTrack(),
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XATVTrack(properties)

    def browser_windows(
        self, filter: Union[dict, None] = None
    ) -> "XATVBrowserWindowList":
        """Returns a list of browser windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browser windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVBrowserWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.browserWindows(), XATVBrowserWindowList, filter
        )

    def playlists(self, filter: Union[dict, None] = None) -> "XATVPlaylistList":
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XATVPlaylistList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlists(), XATVPlaylistList, filter)

    def library_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XATVLibraryPlaylistList":
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XATVLibraryPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.libraryPlaylists(), XATVLibraryPlaylistList, filter
        )

    def playlist_windows(
        self, filter: Union[dict, None] = None
    ) -> "XATVPlaylistWindowList":
        """Returns a list of playlist windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVPlaylistWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.playlistWindows(), XATVPlaylistWindowList, filter
        )

    def sources(self, filter: Union[dict, None] = None) -> "XATVSourceList":
        """Returns a list of sources, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sources will have, or None
        :type filter: Union[dict, None]
        :return: The list of sources
        :rtype: XATVSourceList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.sources(), XATVSourceList, filter)

    def tracks(self, filter: Union[dict, None] = None) -> "XATVTrackList":
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XATVTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XATVTrackList, filter)

    def file_tracks(self, filter: Union[dict, None] = None) -> "XATVFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XATVFileTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(self.xa_scel.fileTracks(), XATVFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> "XATVURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XATVURLTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(self.xa_scel.URLTracks(), XATVURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> "XATVSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XATVSharedTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.sharedTracks(), XATVSharedTrackList, filter
        )

    def video_windows(self, filter: Union[dict, None] = None) -> "XATVVideoWindowList":
        """Returns a list of video windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVVideoWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.videoWindows(), XATVVideoWindowList, filter
        )

    def make(
        self,
        specifier: Union[str, "XATVApplication.ObjectType"],
        properties: dict,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list. Valid specifiers are: playlist, user playlist, folder playlist, library playlist, track, URL track, shared track, file track, artwork, window, browser window, playlist window, video window, or source.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XATVApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to initialize the object with, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example: Make a new folder playlist and push it onto the list of playlists

        >>> import PyXA
        >>> app = PyXA.Music()
        >>> new_playlist = app.make("folder_playlist", {"name": "Example Playlist"})
        >>> app.playlists().push(new_playlist)

        .. versionadded:: 0.2.2
        """
        if isinstance(specifier, XATVApplication.ObjectType):
            specifier = specifier.value

        if data is None:
            camelized_properties = {}

            if properties is None:
                properties = {}

            for key, value in properties.items():
                if key == "url":
                    key = "URL"

                camelized_properties[XABase.camelize(key)] = value

            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithProperties_(camelized_properties)
            )
        else:
            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithData_(data)
            )

        if specifier == "playlist":
            return self._new_element(obj, XATVPlaylist)
        elif specifier == "user_playlist":
            return self._new_element(obj, XATVUserPlaylist)
        elif specifier == "folder_playlist":
            return self._new_element(obj, XATVFolderPlaylist)
        elif specifier == "library_playlist":
            return self._new_element(obj, XATVLibraryPlaylist)
        elif specifier == "track":
            return self._new_element(obj, XATVTrack)
        elif specifier == "url_track":
            return self._new_element(obj, XATVURLTrack)
        elif specifier == "shared_track":
            return self._new_element(obj, XATVSharedTrack)
        elif specifier == "file_track":
            return self._new_element(obj, XATVFileTrack)
        elif specifier == "artwork":
            return self._new_element(obj, XATVArtwork)
        elif specifier == "window":
            return self._new_element(obj, XATVWindow)
        elif specifier == "browser_window":
            return self._new_element(obj, XATVBrowserWindow)
        elif specifier == "playlist_window":
            return self._new_element(obj, XATVPlaylistWindow)
        elif specifier == "source":
            return self._new_element(obj, XATVSource)
        elif specifier == "video_window":
            return self._new_element(obj, XATVVideoWindow)


class XATVItemList(XABase.XAList):
    """A wrapper around lists of music items that employs fast enumeration techniques.

    All properties of music items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATVItem
        super().__init__(properties, obj_class, filter)

    def container(self) -> list[XABase.XAObject]:
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XABase.XAList)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def persistent_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("persistentID") or [])

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def by_container(self, container: XABase.XAObject) -> Union["XATVItem", None]:
        return self.by_property("container", container.xa_elem)

    def by_id(self, id: int) -> Union["XATVItem", None]:
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union["XATVItem", None]:
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union["XATVItem", None]:
        return self.by_property("name", name)

    def by_persistent_id(self, persistent_id: str) -> Union["XATVItem", None]:
        return self.by_property("persistentID", persistent_id)

    def by_properties(self, properties: dict) -> Union["XATVItem", None]:
        return self.by_property("properties", properties)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each music item in the list.

        When a list of music items is copied to the clipboard, the name of each item is added to the clipboard.

        :return: A list of track names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self.xa_elem)) + ">"


class XATVItem(XABase.XAObject):
    """A generic class with methods common to the various playable media classes in media apps.

    .. seealso:: :class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_class(self):
        return TVObjectClass(
            XABase.unOSType(self.xa_elem.objectClass().typeCodeValue())
        )

    @property
    def container(self) -> XABase.XAObject:
        """The container of the item."""
        return self._new_element(self.xa_elem.container(), XABase.XAObject)

    @property
    def id(self) -> int:
        """The ID of the item."""
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        """The index of the item in the internal application order."""
        return self.xa_elem.index()

    @property
    def name(self) -> str:
        """The name of the item."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def persistent_id(self) -> str:
        """The constant unique identifier for the item."""
        return self.xa_elem.persistentID()

    @property
    def properties(self) -> dict:
        """Every property of the item."""
        return self.xa_elem.properties()

    def download(self) -> "XATVItem":
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> "XATVItem":
        """Reveals the item in the media apps window.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. seealso:: :func:`select`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.reveal()
        return self

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the music item.

        When a music item is copied to the clipboard, the name of the music item is added to the clipboard.

        :return: The name of the music item
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name


class XATVArtworkList(XATVItemList):
    """A wrapper around lists of music artworks that employs fast enumeration techniques.

    All properties of music artworks can be called as methods on the wrapped list, returning a list containing each artworks's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVArtwork)

    def data(self) -> list[XABase.XAImage]:
        ls = self.xa_elem.arrayByApplyingSelector_("data") or []
        return [XABase.XAImage(x) for x in ls]

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def downloaded(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("downloaded") or [])

    def format(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("format") or [])

    def kind(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def raw_data(self) -> list[bytes]:
        return list(self.xa_elem.arrayByApplyingSelector_("rawData") or [])

    def by_data(self, data: XABase.XAImage) -> Union["XATVArtwork", None]:
        return self.by_property("data", data.xa_elem)

    def by_object_description(
        self, object_description: str
    ) -> Union["XATVArtwork", None]:
        return self.by_property("objectDescription", object_description)

    def by_downloaded(self, downloaded: bool) -> Union["XATVArtwork", None]:
        return self.by_property("downloaded", downloaded)

    def by_format(self, format: int) -> Union["XATVArtwork", None]:
        return self.by_property("format", format)

    def by_kind(self, kind: int) -> Union["XATVArtwork", None]:
        return self.by_property("kind", kind)

    def by_raw_data(self, raw_data: bytes) -> Union["XATVArtwork", None]:
        return self.by_property("rawData", raw_data)


class XATVArtwork(XATVItem):
    """An artwork in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def data(self) -> XABase.XAImage:
        """The data for the artwork in the form of a picture."""
        return XABase.XAImage(self.xa_elem.data())

    @data.setter
    def data(self, data: XABase.XAImage):
        self.set_property("data", data.xa_elem)

    @property
    def object_description(self) -> str:
        """The string description of the artwork."""
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property("objectDescription", object_description)

    @property
    def downloaded(self) -> bool:
        """Whether the artwork was downloaded by media apps."""
        return self.xa_elem.downloaded()

    @property
    def format(self) -> int:
        """The data format for the artwork."""
        return self.xa_elem.format()

    @property
    def kind(self) -> int:
        """The kind/purpose of the artwork."""
        return self.xa_elem.kind()

    @kind.setter
    def kind(self, kind: int):
        self.set_property("kind", kind)

    @property
    def raw_data(self) -> bytes:
        """The data for the artwork in original format."""
        return self.xa_elem.rawData()

    @raw_data.setter
    def raw_data(self, raw_data: str):
        self.set_property("rawData", raw_data)


class XATVPlaylistList(XATVItemList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATVPlaylist
        super().__init__(properties, filter, obj_class)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def duration(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("duration") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def parent(self) -> "XATVPlaylistList":
        ls = self.xa_elem.arrayByApplyingSelector_("parent") or []
        return self._new_element(ls, XATVPlaylistList)

    def size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def special_kind(self) -> list[XATVApplication.PlaylistKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("specialKind") or []
        return [
            XATVApplication.PlaylistKind(XABase.OSType(x.stringValue())) for x in ls
        ]

    def time(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("time") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def by_object_description(
        self, object_description: str
    ) -> Union["XATVPlaylist", None]:
        return self.by_property("objectDescription", object_description)

    def by_duration(self, duration: int) -> Union["XATVPlaylist", None]:
        return self.by_property("duration", duration)

    def by_name(self, name: str) -> Union["XATVPlaylist", None]:
        return self.by_property("name", name)

    def by_parent(self, parent: "XATVPlaylist") -> Union["XATVPlaylist", None]:
        return self.by_property("parent", parent.xa_elem)

    def by_size(self, size: int) -> Union["XATVPlaylist", None]:
        return self.by_property("size", size)

    def by_special_kind(
        self, special_kind: XATVApplication.PlaylistKind
    ) -> Union["XATVPlaylist", None]:
        return self.by_property(
            "specialKind", event_from_str(XABase.unOSType(special_kind.value))
        )

    def by_time(self, time: str) -> Union["XATVPlaylist", None]:
        return self.by_property("time", time)

    def by_visible(self, visible: bool) -> Union["XATVPlaylist", None]:
        return self.by_property("visible", visible)

    def push(
        self, *elements: list["XATVPlaylist"]
    ) -> Union["XATVPlaylist", list["XATVPlaylist"], None]:
        old_list = [x.id for x in self]
        super().push(*elements)
        new_list = [x.id for x in self if not x.id in old_list]
        if len(new_list) == 1:
            return self.by_id(new_list[0])
        return [self.by_id(id) for id in new_list]

    def _format_for_filter(self, filter, value1, value2=None):
        if filter == "special_kind" or filter == "specialKind":
            if isinstance(value1, XATVApplication.PlaylistKind):
                value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XATVPlaylist(XATVItem):
    """A playlist in media apps.

    .. seealso:: :class:`XATVLibraryPlaylist`, :class:`XATVUserPlaylist`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        if isinstance(self.xa_elem, ScriptingBridge.SBProxyByCode):
            return

        if not hasattr(self, "xa_specialized"):
            if (
                self.special_kind == XATVApplication.PlaylistKind.LIBRARY
                or self.special_kind == XATVApplication.PlaylistKind.USER_LIBRARY
            ):
                self.__class__ = XATVLibraryPlaylist

            elif self.special_kind == XATVApplication.PlaylistKind.FOLDER:
                self.__class__ = XATVFolderPlaylist

            elif (
                self.special_kind == XATVApplication.PlaylistKind.USER
                or self.special_kind == XATVApplication.PlaylistKind.NONE
            ):
                self.__class__ = XATVUserPlaylist

            self.xa_specialized = True
            self.__init__(properties)

    @property
    def object_description(self) -> str:
        """The string description of the playlist."""
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property("objectDescription", object_description)

    @property
    def duration(self) -> int:
        """The total length of all tracks in seconds."""
        return self.xa_elem.duration()

    @property
    def name(self) -> str:
        """The name of the playlist."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def parent(self) -> "XATVPlaylist":
        """The folder containing the playlist, if any."""
        return self._new_element(self.xa_elem.parent(), XATVPlaylist)

    @property
    def size(self) -> int:
        """The total size of all tracks in the playlist in bytes."""
        return self.xa_elem.size()

    @property
    def special_kind(self) -> XATVApplication.PlaylistKind:
        """The special playlist kind."""
        return XATVApplication.PlaylistKind(self.xa_elem.specialKind())

    @property
    def time(self) -> str:
        """The length of all tracks in the playlist in MM:SS format."""
        return self.xa_elem.time()

    @property
    def visible(self) -> bool:
        """Whether the playlist is visible in the source list."""
        return self.xa_elem.visible()

    def move_to(self, parent_playlist):
        self.xa_elem.moveTo_(parent_playlist.xa_elem)

    def play(self):
        """Starts playback of the playlist, beginning with the first track in the list.

        .. versionadded:: 0.2.1
        """
        self.xa_elem.playOnce_(True)

    def add_tracks(self, *tracks: Union["XATVTrackList", list["XATVTrack"]]):
        """Add one or more tracks to this playlist.

        :param tracks: The list of tracks to add to this playlist
        :type tracks: Union[XATVTrackList, list[XATVTrack]]

        .. versionadded:: 0.2.2
        """
        if len(tracks) == 1 and isinstance(tracks[0], XATVTrackList):
            tracks = tracks[0].xa_elem
        elif len(tracks) == 1 and isinstance(tracks[0], list):
            tracks = [x.xa_elem for x in tracks[0]]
        else:
            tracks = [x.xa_elem for x in tracks]

        for track in tracks:
            track.duplicateTo_(self.xa_elem)

    def search(
        self,
        query: str,
        type: Literal["all", "artists", "albums", "displayed", "tracks"] = "displayed",
    ):
        search_ids = {
            "all": XATVApplication.SearchFilter.ALL,
            "artists": XATVApplication.SearchFilter.ARTISTS,
            "albums": XATVApplication.SearchFilter.ALBUMS,
            "displayed": XATVApplication.SearchFilter.DISPLAYED,
            "tracks": XATVApplication.SearchFilter.NAMES,
        }

        items = []
        results = self.xa_elem.searchFor_only_(query, search_ids[type])
        for result in results:
            properties = {
                "parent": self,
                "element": result,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            items.append(XATVTrack(properties))
        return items

    def move(self, location: Union["XATVSource", "XATVFolderPlaylist"]):
        """Moves the playlist to the specified source or folder playlist.

        :param location: The source or folder playlist to move this playlist to
        :type location: Union[XATVSource, XATVFolderPlaylist]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.moveTo_(location.xa_elem)

    def duplicate(
        self, location: Union["XATVSource", "XATVFolderPlaylist", None] = None
    ):
        """Duplicates the playlist to the specified source or folder playlist.

        :param location: The source or folder playlist to duplicate this playlist to, or None to duplicate into the parent of this playlist, defaults to None
        :type location: Union[XATVSource, XATVFolderPlaylist, None], optional

        .. versionadded:: 0.2.2
        """
        if location is None:
            location = self.xa_prnt
        self.xa_elem.duplicateTo_(location.xa_elem)

    def tracks(self, filter: Union[dict, None] = None) -> "XATVTrackList":
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XATVTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.tracks(), XATVTrackList, filter)

    def artworks(self, filter: Union[dict, None] = None) -> "XATVArtworkList":
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XATVArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.artworks(), XATVArtworkList, filter)


class XATVLibraryPlaylistList(XATVPlaylistList):
    """A wrapper around lists of library playlists that employs fast enumeration techniques.

    All properties of library playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVLibraryPlaylist)


class XATVLibraryPlaylist(XATVPlaylist):
    """The library playlist in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> "XATVFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XATVFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.fileTracks(), XATVFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> "XATVURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XATVURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XATVURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> "XATVSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XATVSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.sharedTracks(), XATVSharedTrackList, filter
        )


class XATVSourceList(XATVItemList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATVSource
        super().__init__(properties, filter, obj_class)

    def capacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity") or [])

    def free_space(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace") or [])

    def kind(self) -> list[XATVApplication.SourceKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("kind") or []
        return [XATVApplication.SourceKind(XABase.OSType(x.stringValue())) for x in ls]

    def by_capacity(self, capacity: int) -> Union["XATVSource", None]:
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union["XATVSource", None]:
        return self.by_property("freeSpace", free_space)

    def by_kind(self, kind: XATVApplication.SourceKind) -> Union["XATVSource", None]:
        return self.by_property("kind", event_from_str(XABase.unOSType(kind.value)))

    def _format_for_filter(self, filter, value1, value2=None):
        if filter == "kind":
            if isinstance(value1, XATVApplication.SourceKind):
                value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XATVSource(XATVItem):
    """A media source in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def capacity(self) -> int:
        """The total size of the source, if it has a fixed size."""
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        """The free space on the source, if it has a fixed size."""
        return self.xa_elem.freeSpace()

    @property
    def kind(self) -> XATVApplication.SourceKind:
        """The source kind."""
        return XATVApplication.SourceKind(self.xa_elem.kind())

    def library_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XATVLibraryPlaylistList":
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned library playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XATVLibraryPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.libraryPlaylists(), XATVLibraryPlaylistList, filter
        )

    def playlists(self, filter: Union[dict, None] = None) -> "XATVPlaylistList":
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XATVPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.playlists(), XATVPlaylistList, filter)

    def user_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XATVUserPlaylistList":
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned user playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XATVUserPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.userPlaylists(), XATVUserPlaylistList, filter
        )


class XATVTrackList(XATVItemList):
    """A wrapper around lists of music tracks that employs fast enumeration techniques.

    All properties of music tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATVTrack
        super().__init__(properties, filter, obj_class)

    def album(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("album") or [])

    def album_rating(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("albumRating") or [])

    def album_rating_kind(self) -> list[XATVApplication.RatingKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("albumRatingKind") or []
        return [XATVApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def bit_rate(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("bitRate") or [])

    def bookmark(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("bookmark") or [])

    def bookmarkable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("bookmarkable") or [])

    def category(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("category") or [])

    def comment(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment") or [])

    def database_id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("databaseID") or [])

    def date_added(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dateAdded") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def disc_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("discCount") or [])

    def disc_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("discNumber") or [])

    def downloader_apple_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderAppleID") or [])

    def downloader_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderName") or [])

    def duration(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("duration") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def episode_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("episodeID") or [])

    def episode_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("episodeNumber") or [])

    def finish(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("finish") or [])

    def genre(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("genre") or [])

    def grouping(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("grouping") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def long_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("longDescription") or [])

    def media_kind(self) -> list[XATVApplication.MediaKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("mediaKind") or []
        return [XATVApplication.MediaKind(XABase.OSType(x.stringValue())) for x in ls]

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def played_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("playedCount") or [])

    def played_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("playedDate") or [])

    def purchaser_apple_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserAppleID") or [])

    def purchaser_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserName") or [])

    def rating(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rating") or [])

    def rating_kind(self) -> list[XATVApplication.RatingKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("ratingKind") or []
        return [XATVApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def release_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("releaseDate") or [])

    def sample_rate(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("sampleRate") or [])

    def season_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("seasonNumber") or [])

    def skipped_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("skippedCount") or [])

    def skipped_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("skippedDate") or [])

    def show(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("show") or [])

    def sort_album(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortAlbum") or [])

    def sort_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortName") or [])

    def sort_show(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortShow") or [])

    def size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def start(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("start") or [])

    def time(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("time") or [])

    def track_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("trackCount") or [])

    def track_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("trackNumber") or [])

    def unplayed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("unplayed") or [])

    def volume_adjustment(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("volumeAdjustment") or [])

    def year(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("year") or [])

    def sort_director(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortDirector") or [])

    def by_sort_director(self, sort_director: str) -> Union["XATVTrack", None]:
        return self.by_property("sortDirector", sort_director)

    def by_album(self, album: str) -> Union["XATVTrack", None]:
        return self.by_property("album", album)

    def by_album_rating(self, album_rating: int) -> Union["XATVTrack", None]:
        return self.by_property("albumRating", album_rating)

    def by_album_rating_kind(
        self, album_rating_kind: XATVApplication.RatingKind
    ) -> Union["XATVTrack", None]:
        return self.by_property(
            "albumRatingKind", event_from_str(XABase.unOSType(album_rating_kind.value))
        )

    def by_bit_rate(self, bit_rate: int) -> Union["XATVTrack", None]:
        return self.by_property("bitRate", bit_rate)

    def by_bookmark(self, bookmark: float) -> Union["XATVTrack", None]:
        return self.by_property("bookmark", bookmark)

    def by_bookmarkable(self, bookmarkable: bool) -> Union["XATVTrack", None]:
        return self.by_property("bookmarkable", bookmarkable)

    def by_category(self, category: str) -> Union["XATVTrack", None]:
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> Union["XATVTrack", None]:
        return self.by_property("comment", comment)

    def by_database_id(self, database_id: int) -> Union["XATVTrack", None]:
        return self.by_property("databaseID", database_id)

    def by_date_added(self, date_added: datetime) -> Union["XATVTrack", None]:
        return self.by_property("dateAdded", date_added)

    def by_object_description(
        self, object_description: str
    ) -> Union["XATVTrack", None]:
        return self.by_property("objectDescription", object_description)

    def by_disc_count(self, disc_count: int) -> Union["XATVTrack", None]:
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union["XATVTrack", None]:
        return self.by_property("discNumber", disc_number)

    def by_downloader_apple_id(
        self, downloader_apple_id: str
    ) -> Union["XATVTrack", None]:
        return self.by_property("downloaderAppleID", downloader_apple_id)

    def by_downloader_name(self, downloader_name: str) -> Union["XATVTrack", None]:
        return self.by_property("downloaderName", downloader_name)

    def by_duration(self, duration: float) -> Union["XATVTrack", None]:
        return self.by_property("duration", duration)

    def by_enabled(self, enabled: bool) -> Union["XATVTrack", None]:
        return self.by_property("enabled", enabled)

    def by_episode_id(self, episode_id: str) -> Union["XATVTrack", None]:
        return self.by_property("episodeID", episode_id)

    def by_episode_number(self, episode_number: int) -> Union["XATVTrack", None]:
        return self.by_property("episodeNumber", episode_number)

    def by_finish(self, finish: float) -> Union["XATVTrack", None]:
        return self.by_property("finish", finish)

    def by_genre(self, genre: str) -> Union["XATVTrack", None]:
        return self.by_property("genre", genre)

    def by_grouping(self, grouping: str) -> Union["XATVTrack", None]:
        return self.by_property("grouping", grouping)

    def by_kind(self, kind: str) -> Union["XATVTrack", None]:
        return self.by_property("kind", kind)

    def by_long_description(self, long_description: str) -> Union["XATVTrack", None]:
        return self.by_property("longDescription", long_description)

    def by_media_kind(
        self, media_kind: XATVApplication.MediaKind
    ) -> Union["XATVTrack", None]:
        return self.by_property(
            "mediaKind", event_from_str(XABase.unOSType(media_kind.value))
        )

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XATVTrack", None]:
        return self.by_property("modificationDate", modification_date)

    def by_played_count(self, played_count: int) -> Union["XATVTrack", None]:
        return self.by_property("playedCount", played_count)

    def by_played_date(self, played_date: datetime) -> Union["XATVTrack", None]:
        return self.by_property("playedDate", played_date)

    def by_purchaser_apple_id(
        self, purchaser_apple_id: str
    ) -> Union["XATVTrack", None]:
        return self.by_property("purchaserAppleID", purchaser_apple_id)

    def by_purchaser_name(self, purchaser_name: str) -> Union["XATVTrack", None]:
        return self.by_property("purchaserName", purchaser_name)

    def by_rating(self, rating: int) -> Union["XATVTrack", None]:
        return self.by_property("rating", rating)

    def by_rating_kind(
        self, rating_kind: XATVApplication.RatingKind
    ) -> Union["XATVTrack", None]:
        return self.by_property(
            "ratingKind", event_from_str(XABase.unOSType(rating_kind.value))
        )

    def by_release_date(self, release_date: datetime) -> Union["XATVTrack", None]:
        return self.by_property("releaseDate", release_date)

    def by_sample_rate(self, sample_rate: int) -> Union["XATVTrack", None]:
        return self.by_property("sampleRate", sample_rate)

    def by_season_number(self, season_number: int) -> Union["XATVTrack", None]:
        return self.by_property("seasonNumber", season_number)

    def by_skipped_count(self, skipped_count: int) -> Union["XATVTrack", None]:
        return self.by_property("skippedCount", skipped_count)

    def by_skipped_date(self, skipped_date: datetime) -> Union["XATVTrack", None]:
        return self.by_property("skippedDate", skipped_date)

    def by_show(self, show: str) -> Union["XATVTrack", None]:
        return self.by_property("show", show)

    def by_sort_album(self, sort_album: str) -> Union["XATVTrack", None]:
        return self.by_property("sortAlbum", sort_album)

    def by_sort_name(self, sort_name: str) -> Union["XATVTrack", None]:
        return self.by_property("sortName", sort_name)

    def by_sort_show(self, sort_show: str) -> Union["XATVTrack", None]:
        return self.by_property("sortShow", sort_show)

    def by_size(self, size: int) -> Union["XATVTrack", None]:
        return self.by_property("size", size)

    def by_start(self, start: float) -> Union["XATVTrack", None]:
        return self.by_property("start", start)

    def by_time(self, time: str) -> Union["XATVTrack", None]:
        return self.by_property("time", time)

    def by_track_count(self, track_count: int) -> Union["XATVTrack", None]:
        return self.by_property("trackCount", track_count)

    def by_track_number(self, track_number: int) -> Union["XATVTrack", None]:
        return self.by_property("trackNumber", track_number)

    def by_unplayed(self, unplayed: bool) -> Union["XATVTrack", None]:
        return self.by_property("unplayed", unplayed)

    def by_volume_adjustment(self, volume_adjustment: int) -> Union["XATVTrack", None]:
        return self.by_property("volumeAdjustment", volume_adjustment)

    def by_year(self, year: int) -> Union["XATVTrack", None]:
        return self.by_property("year", year)

    def _format_for_filter(self, filter, value1, value2=None):
        if filter in [
            "album_rating_kind",
            "albumRatingKind",
            "media_kind",
            "mediaKind",
            "rating_kind",
            "ratingKind",
        ]:
            value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XATVTrack(XATVItem):
    """A class for managing and interacting with tracks in media apps.

    .. seealso:: :class:`XATVSharedTrack`, :class:`XATVFileTrack`, :class:`XATVRemoteURLTrack`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        if not hasattr(self, "xa_specialized"):
            oldDict = self.__dict__.copy()
            if self.object_class == TVObjectClass.SHARED_TRACK:
                self.__class__ = XATVSharedTrack

            elif self.object_class == TVObjectClass.FILE_TRACK:
                self.__class__ = XATVFileTrack

            elif self.object_class == TVObjectClass.URL_TRACK:
                self.__class__ = XATVURLTrack

            self.xa_specialized = True
            self.__init__(properties)
            self.__dict__.update(oldDict)

    @property
    def album(self) -> str:
        """The name of the track's album."""
        return self.xa_elem.album()

    @album.setter
    def album(self, album: str):
        self.set_property("album", album)

    @property
    def album_rating(self) -> int:
        """The rating of the track's album."""
        return self.xa_elem.albumRating()

    @album_rating.setter
    def album_rating(self, album_rating: int):
        self.set_property("albumRating", album_rating)

    @property
    def album_rating_kind(self) -> XATVApplication.RatingKind:
        """The album's rating kind."""
        return XATVApplication.RatingKind(self.xa_elem.albumRatingKind())

    @property
    def bit_rate(self) -> int:
        """The track's bitrate in kbps."""
        return self.xa_elem.bitRate()

    @property
    def bookmark(self) -> float:
        """The bookmark time of the track in seconds."""
        return self.xa_elem.bookmark()

    @bookmark.setter
    def bookmark(self, bookmark: float):
        self.set_property("bookmark", bookmark)

    @property
    def bookmarkable(self) -> bool:
        """Whether the playback position is kept in memory after stopping the track."""
        return self.xa_elem.bookmarkable()

    @bookmarkable.setter
    def bookmarkable(self, bookmarkable: bool):
        self.set_property("bookmarkable", bookmarkable)

    @property
    def category(self) -> str:
        """The category of the track."""
        return self.xa_elem.category()

    @category.setter
    def category(self, category: str):
        self.set_property("category", category)

    @property
    def comment(self) -> str:
        """User-provided notes on the track."""
        return self.xa_elem.comment()

    @comment.setter
    def comment(self, comment: str):
        self.set_property("comment", comment)

    @property
    def database_id(self) -> int:
        """A unique ID for the track."""
        return self.xa_elem.databaseID()

    @property
    def date_added(self) -> datetime:
        """The date the track was added to the current playlist."""
        return self.xa_elem.dateAdded()

    @property
    def object_description(self) -> str:
        """A string description of the track."""
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property("objectDescription", object_description)

    @property
    def disc_count(self) -> int:
        """The number of discs in the source album."""
        return self.xa_elem.discCount()

    @disc_count.setter
    def disc_count(self, disc_count: int):
        self.set_property("discCount", disc_count)

    @property
    def disc_number(self) -> int:
        """The index of the disc containing the track."""
        return self.xa_elem.discNumber()

    @disc_number.setter
    def disc_number(self, disc_number: int):
        self.set_property("discNumber", disc_number)

    @property
    def downloader_apple_id(self) -> str:
        """The Apple ID of the person who downloaded the track."""
        return self.xa_elem.downloaderAppleID()

    @property
    def downloader_name(self) -> str:
        """The full name of the person who downloaded the track."""
        return self.xa_elem.downloaderName()

    @property
    def duration(self) -> float:
        """Length of the track in seconds."""
        return self.xa_elem.duration()

    @property
    def enabled(self) -> bool:
        """Whether the track is able to be played."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def episode_id(self) -> str:
        """A unique ID for the episode of the track."""
        return self.xa_elem.episodeID()

    @episode_id.setter
    def episode_id(self, episode_id: str):
        self.set_property("episodeId", episode_id)

    @property
    def episode_number(self) -> int:
        """The episode number of the track."""
        return self.xa_elem.episodeNumber()

    @episode_number.setter
    def episode_number(self, episode_number: int):
        self.set_property("episodeNumber", episode_number)

    @property
    def finish(self) -> float:
        """The time in seconds from the start at which the track stops playing."""
        return self.xa_elem.finish()

    @finish.setter
    def finish(self, finish: float):
        self.set_property("finish", finish)

    @property
    def genre(self) -> str:
        """The music/audio genre category of the track."""
        return self.xa_elem.genre()

    @genre.setter
    def genre(self, genre: str):
        self.set_property("genre", genre)

    @property
    def grouping(self) -> str:
        """The current section/chapter/movement of the track."""
        return self.xa_elem.grouping()

    @grouping.setter
    def grouping(self, grouping: str):
        self.set_property("grouping", grouping)

    @property
    def kind(self) -> str:
        """A text description of the track."""
        return self.xa_elem.kind()

    @property
    def long_description(self) -> str:
        """A long description for the track."""
        return self.xa_elem.longDescription()

    @long_description.setter
    def long_description(self, long_description: str):
        self.set_property("longDescription", long_description)

    @property
    def media_kind(self) -> XATVApplication.MediaKind:
        """A description of the track's media type."""
        return XATVApplication.MediaKind(self.xa_elem.mediaKind())

    @media_kind.setter
    def media_kind(self, media_kind: XATVApplication.MediaKind):
        self.set_property("mediaKind", media_kind.value)

    @property
    def modification_date(self) -> datetime:
        """The last modification date of the track's content."""
        return self.xa_elem.modificationDate()

    @property
    def played_count(self) -> int:
        """The number of the times the track has been played."""
        return self.xa_elem.playedCount()

    @played_count.setter
    def played_count(self, played_count: int):
        self.set_property("playedCount", played_count)

    @property
    def played_date(self) -> datetime:
        """The date the track was last played."""
        return self.xa_elem.playedDate()

    @played_date.setter
    def played_date(self, played_date: datetime):
        self.set_property("playedDate", played_date)

    @property
    def purchaser_apple_id(self) -> str:
        """The Apple ID of the person who bought the track."""
        return self.xa_elem.purchaserAppleID()

    @property
    def purchaser_name(self) -> str:
        """The full name of the person who bought the track."""
        return self.xa_elem.purchaserName()

    @property
    def rating(self) -> int:
        """The rating of the track from 0 to 100."""
        return self.xa_elem.rating()

    @rating.setter
    def rating(self, rating: int):
        self.set_property("rating", rating)

    @property
    def rating_kind(self) -> XATVApplication.RatingKind:
        """Whether the rating is user-provided or computed."""
        return XATVApplication.RatingKind(self.xa_elem.ratingKind())

    @property
    def release_date(self) -> datetime:
        """The date the track was released."""
        return self.xa_elem.releaseDate()

    @property
    def sample_rate(self) -> int:
        """The sample rate of the track in Hz."""
        return self.xa_elem.sampleRate()

    @property
    def season_number(self) -> int:
        """The number of the season the track belongs to."""
        return self.xa_elem.seasonNumber()

    @season_number.setter
    def season_number(self, season_number: int):
        self.set_property("seasonNumber", season_number)

    @property
    def skipped_count(self) -> int:
        """The number of times the track has been skipped."""
        return self.xa_elem.skippedCount()

    @skipped_count.setter
    def skipped_count(self, skipped_count: int):
        self.set_property("skippedCount", skipped_count)

    @property
    def skipped_date(self) -> datetime:
        """The date the track was last skipped."""
        return self.xa_elem.skippedDate()

    @skipped_date.setter
    def skipped_date(self, skipped_date: datetime):
        self.set_property("skippedDate", skipped_date)

    @property
    def show(self) -> str:
        """The name of the show the track belongs to."""
        return self.xa_elem.show()

    @show.setter
    def show(self, show: str):
        self.set_property("show", show)

    @property
    def sort_album(self) -> str:
        """The string used for this track when sorting by album."""
        return self.xa_elem.sortAlbum()

    @sort_album.setter
    def sort_album(self, sort_album: str):
        self.set_property("sortAlbum", sort_album)

    @property
    def sort_name(self) -> str:
        """The string used for this track when sorting by name."""
        return self.xa_elem.sortName()

    @sort_name.setter
    def sort_name(self, sort_name: str):
        self.set_property("sortName", sort_name)

    @property
    def sort_show(self) -> str:
        """The string used for this track when sorting by show."""
        return self.xa_elem.sortShow()

    @sort_show.setter
    def sort_show(self, sort_show: str):
        self.set_property("sortShow", sort_show)

    @property
    def size(self) -> int:
        """The size of the track in bytes."""
        return self.xa_elem.size()

    @property
    def start(self) -> float:
        """The start time of the track in seconds."""
        return self.xa_elem.start()

    @start.setter
    def start(self, start: float):
        self.set_property("start", start)

    @property
    def time(self) -> str:
        """HH:MM:SS representation for the duration of the track."""
        return self.xa_elem.time()

    @property
    def track_count(self) -> int:
        """The number of tracks in the track's album."""
        return self.xa_elem.trackCount()

    @track_count.setter
    def track_count(self, track_count: int):
        self.set_property("trackCount", track_count)

    @property
    def track_number(self) -> int:
        """The index of the track within its album."""
        return self.xa_elem.trackNumber()

    @track_number.setter
    def track_number(self, track_number: int):
        self.set_property("trackNumber", track_number)

    @property
    def unplayed(self) -> bool:
        """Whether the track has been played before."""
        return self.xa_elem.unplayed()

    @unplayed.setter
    def unplayed(self, unplayed: bool):
        self.set_property("unplayed", unplayed)

    @property
    def volume_adjustment(self) -> int:
        """Volume adjustment setting for this track from -100 to +100."""
        return self.xa_elem.volumeAdjustment()

    @volume_adjustment.setter
    def volume_adjustment(self, volume_adjustment: int):
        self.set_property("volumeAdjustment", volume_adjustment)

    @property
    def year(self) -> int:
        """The year the track was released."""
        return self.xa_elem.year()

    @year.setter
    def year(self, year: int):
        self.set_property("year", year)

    @property
    def sort_director(self) -> str:
        """The string used for this track when sorting by director."""
        return self.xa_elem.sortDirector()

    @sort_director.setter
    def sort_director(self, sort_director: str):
        self.set_property("sortDirector", sort_director)

    def select(self) -> "XATVItem":
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XATVTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self

    def play(self) -> "XATVItem":
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XATVItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self

    def move(self, location: Union[XATVPlaylist, XATVSource]):
        """Moves the track to the specified location, copying it if appropriate.

        :param location: The playlist or source to move the track to
        :type location: Union[XATVPlaylist, XATVSource]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.moveTo_(location.xa_elem)

    def duplicate(self, location: Union[XATVPlaylist, XATVSource]):
        """Duplicates the track at the specified location.

        :param location: The location to duplicate the track to
        :type location: Union[XATVPlaylist, XATVSource]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.duplicateTo_(location.xa_elem)

    def artworks(self, filter: Union[dict, None] = None) -> "XATVArtworkList":
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XATVArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.artworks(), XATVArtworkList, filter)


class XATVFileTrackList(XATVTrackList):
    """A wrapper around lists of music file tracks that employs fast enumeration techniques.

    All properties of music file tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVFileTrack)

    def location(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("location") or []
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union["XATVFileTrack", None]:
        return self.by_property("location", location.xa_elem)


class XATVFileTrack(XATVTrack):
    """A file track in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def location(self) -> XABase.XAPath:
        """The location of the file represented by the track."""
        return XABase.XAPath(self.xa_elem.location())

    @location.setter
    def location(self, location: Union[XABase.XAPath, str]):
        if isinstance(location, str):
            location = XABase.XAPath(location)
        self.set_property("location", location.xa_elem)


class XATVSharedTrackList(XATVTrackList):
    """A wrapper around lists of music shared tracks that employs fast enumeration techniques.

    All properties of music shared tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVSharedTrack)


class XATVSharedTrack(XATVTrack):
    """A shared track in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XATVURLTrackList(XATVTrackList):
    """A wrapper around lists of music URL tracks that employs fast enumeration techniques.

    All properties of music URL tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVURLTrack)

    def address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("address") or [])

    def by_address(self, address: str) -> Union["XATVURLTrack", None]:
        return self.by_property("address", address)


class XATVURLTrack(XATVTrack):
    """A URL track in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def address(self) -> XABase.XAURL:
        """The URL for the track."""
        return XABase.XAURL(self.xa_elem.address())

    @address.setter
    def address(self, address: Union[XABase.XAURL, str]):
        if isinstance(address, str):
            address = XABase.XAURL(address)
        self.set_property("address", address.xa_elem)


class XATVUserPlaylistList(XATVPlaylistList):
    """A wrapper around lists of music user playlists that employs fast enumeration techniques.

    All properties of music user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVUserPlaylist)

    def shared(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared") or [])

    def smart(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("smart") or [])

    def by_shared(self, shared: bool) -> Union["XATVUserPlaylist", None]:
        return self.by_property("shared", shared)

    def by_smart(self, smart: bool) -> Union["XATVUserPlaylist", None]:
        return self.by_property("smart", smart)


class XATVUserPlaylist(XATVPlaylist):
    """A user-created playlist in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def shared(self) -> bool:
        """Whether the playlist is shared."""
        return self.xa_elem.shared()

    @shared.setter
    def shared(self, shared: bool):
        self.set_property("shared", shared)

    @property
    def smart(self) -> bool:
        """Whether the playlist is a smart playlist."""
        return self.xa_elem.smart()

    def file_tracks(self, filter: Union[dict, None] = None) -> "XATVFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XATVFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.fileTracks(), XATVFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> "XATVURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XATVURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XATVURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> "XATVSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XATVSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.sharedTracks(), XATVSharedTrackList, filter
        )


class XATVFolderPlaylistList(XATVUserPlaylistList):
    """A wrapper around lists of music folder playlists that employs fast enumeration techniques.

    All properties of music folder playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVFolderPlaylist)


class XATVFolderPlaylist(XATVUserPlaylist):
    """A folder playlist in media apps.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)


class XATVWindowList(XATVItemList):
    """A wrapper around lists of windows that employs fast enumeration techniques.

    All properties of windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATVWindow
        super().__init__(properties, filter, obj_class)

    def bounds(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds") or [])

    def closeable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("closeable") or [])

    def collapseable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("collapseable") or [])

    def collapsed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed") or [])

    def full_screen(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullScreen") or [])

    def position(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position") or [])

    def resizable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("resizable") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def zoomable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable") or [])

    def zoomed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed") or [])

    def by_bounds(
        self, bounds: tuple[tuple[int, int], tuple[int, int]]
    ) -> Union["XATVWindow", None]:
        # TODO
        return self.by_property("bounds", bounds)

    def by_closeable(self, closeable: bool) -> Union["XATVWindow", None]:
        return self.by_property("closeable", closeable)

    def by_collapseable(self, collapseable: bool) -> Union["XATVWindow", None]:
        return self.by_property("collapseable", collapseable)

    def by_collapsed(self, collapsed: bool) -> Union["XATVWindow", None]:
        return self.by_property("collapsed", collapsed)

    def by_full_screen(self, full_screen: bool) -> Union["XATVWindow", None]:
        return self.by_property("fullScreen", full_screen)

    def by_position(self, position: tuple[int, int]) -> Union["XATVWindow", None]:
        # TODO
        return self.by_property("position", position)

    def by_resizable(self, resizable: bool) -> Union["XATVWindow", None]:
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union["XATVWindow", None]:
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union["XATVWindow", None]:
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union["XATVWindow", None]:
        return self.by_property("zoomed", zoomed)


class XATVWindow(XABaseScriptable.XASBWindow, XATVItem):
    """A windows of media apps.

    .. seealso:: :class:`XATVBrowserWindow`, :class:`XATVPlaylistWindow`, :class:`XATVVideoWindow`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        obj_class = self.object_class
        if not hasattr(self, "xa_specialized"):
            if obj_class == TVObjectClass.BROWSER_WINDOW:
                self.__class__ = XATVBrowserWindow
            elif obj_class == TVObjectClass.PLAYLIST_WINDOW:
                self.__class__ = XATVPlaylistWindow
            elif obj_class == TVObjectClass.VIDEO_WINDOW:
                self.__class__ = XATVVideoWindow
            self.xa_specialized = True
            self.__init__(properties)

    @property
    def full_screen(self) -> bool:
        """Whether the window is currently full screen."""
        return self.xa_elem.fullScreen()

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.set_property("fullScreen", full_screen)

    @property
    def position(self) -> tuple[int, int]:
        """The upper left position of the window."""
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property("position", position)


class XATVBrowserWindowList(XATVWindowList):
    """A wrapper around lists of music browser windows that employs fast enumeration techniques.

    All properties of music browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVBrowserWindow)

    def selection(self) -> XATVTrackList:
        ls = self.xa_elem.arrayByApplyingSelector_("selection") or []
        return self._new_element(ls, XATVTrackList)

    def view(self) -> XATVPlaylistList:
        ls = self.xa_elem.arrayByApplyingSelector_("view") or []
        return self._new_element(ls, XATVPlaylistList)

    def by_selection(
        self, selection: XATVTrackList
    ) -> Union["XATVPlaylistWindow", None]:
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XATVPlaylist) -> Union["XATVPlaylistWindow", None]:
        return self.by_property("view", view.xa_elem)


class XATVBrowserWindow(XATVWindow):
    """A browser window of media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def selection(self) -> XATVTrackList:
        """The selected tracks."""
        return self._new_element(self.xa_elem.selection(), XATVTrackList)

    @property
    def view(self) -> XATVPlaylist:
        """The playlist currently displayed in the window."""
        return self._new_element(self.xa_elem.view(), XATVPlaylist)


class XATVPlaylistWindowList(XATVWindowList):
    """A wrapper around lists of music playlist windows that employs fast enumeration techniques.

    All properties of music playlist windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVPlaylistWindow)

    def selection(self) -> XATVTrackList:
        ls = self.xa_elem.arrayByApplyingSelector_("selection") or []
        return self._new_element(ls, XATVTrackList)

    def view(self) -> XATVPlaylistList:
        ls = self.xa_elem.arrayByApplyingSelector_("view") or []
        return self._new_element(ls, XATVPlaylistList)

    def by_selection(
        self, selection: XATVTrackList
    ) -> Union["XATVPlaylistWindow", None]:
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XATVPlaylist) -> Union["XATVPlaylistWindow", None]:
        return self.by_property("view", view.xa_elem)


class XATVPlaylistWindow(XATVWindow):
    """A playlist window in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def selection(self) -> XATVTrackList:
        """The selected tracks."""
        return self._new_element(self.xa_elem.selection(), XATVTrackList)

    @property
    def view(self) -> XATVPlaylist:
        """The playlist currently displayed in the window."""
        return self._new_element(self.xa_elem.view(), XATVPlaylist)


class XATVVideoWindowList(XATVWindowList):
    """A wrapper around lists of music video windows that employs fast enumeration techniques.

    All properties of music video windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVVideoWindow)


class XATVVideoWindow(XATVWindow):
    """A video window in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
