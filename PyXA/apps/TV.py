""".. versionadded:: 0.0.1

Control the macOS TV application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import List, Literal, Tuple, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath

class XATVApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XATVWindow`, class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.1
    """
    class PlayerState(Enum):
        """States of the TV player.
        """
        STOPPED         = XABase.OSType('kPSS') #: The player is stopped
        PLAYING         = XABase.OSType('kPSP') #: The player is playing
        PAUSED          = XABase.OSType('kPSp') #: The player is paused
        FAST_FORWARDING = XABase.OSType('kPSF') #: The player is fast forwarding
        REWINDING       = XABase.OSType('kPSR') #: The player is rewinding

    class SourceKind(Enum):
        """Types of sources for media items.
        """
        LIBRARY         = XABase.OSType('kLib') #: A library source
        SHARED_LIBRARY  = XABase.OSType('kShd') #: A shared library source
        ITUNES_STORE    = XABase.OSType('kITS') #: The iTunes Store source
        UNKNOWN         = XABase.OSType('kUnk') #: An unknown source

    class SearchFilter(Enum):
        """Filter restrictions on search results.
        """
        ALBUMS      = XABase.OSType('kSrL') #: Search albums
        ALL         = XABase.OSType('kAll') #: Search all
        ARTISTS     = XABase.OSType('kSrR') #: Search artists
        DISPLAYED   = XABase.OSType('kSrV') #: Search the currently displayed playlist
        NAMES       = XABase.OSType('kSrS') #: Search track names only
    
    class PlaylistKind(Enum):
        """Types of special playlists.
        """
        NONE            = XABase.OSType('kNon') #: An unknown playlist kind
        FOLDER          = XABase.OSType('kSpF') #: A folder
        LIBRARY         = XABase.OSType('kSpL') #: The system library playlist
        MOVIES          = XABase.OSType('kSpI') #: A playlist containing movies
        TV              = XABase.OSType('kSpT') #: A playlist containing TV shows
        USER            = XABase.OSType('cUsP') #: A user-created playlist
        USER_LIBRARY    = XABase.OSType('cLiP') #: The user's library

    class MediaKind(Enum):
        """Types of media items.
        """
        HOME_VIDEO  = XABase.OSType('kVdH') #: A home video track
        MOVIE       = XABase.OSType('kVdM') #: A movie track
        TV_SHOW     = XABase.OSType('kVdT') #: A TV show track
        UNKNOWN     = XABase.OSType('kUnk') #: An unknown media item kind

    class RatingKind(Enum):
        """Types of ratings for media items.
        """
        USER        = XABase.OSType('kRtU') #: A user-inputted rating
        COMPUTED    = XABase.OSType('kRtC') #: A computer generated rating

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATVWindow

        self.current_playlist: XATVPlaylist #: The playlist containing the currently targeted track
        self.current_stream_title: str #: The name of the current streaming track
        self.current_stream_url: str #: The URL of the current streaming 
        self.current_track: XATVTrack #: The currently targeted track
        self.fixed_indexing: bool #: Whether the track indices are independent of the order of the current playlist or not
        self.frontmost: bool #: Whether the application is active or not
        self.full_screen: bool #: Whether the app is fullscreen or not
        self.name: str #: The name of the application
        self.mute: bool #: Whether sound output is muted or not
        self.player_position: float #: The time elapsed in the current track
        self.player_state: str #: Whether the player is playing, paused, stopped, fast forwarding, or rewinding
        self.selection: str #: The selected ..............
        self.sound_volume: int #: The sound output volume
        self.version: str #: The version of the application

    @property
    def current_playlist(self) -> 'XATVPlaylist':
        return self._new_element(self.xa_scel.currentPlaylist(), XATVPlaylist)

    @property
    def current_stream_title(self) -> str:
        return self.xa_scel.currentStreamTitle()

    @property
    def current_stream_url(self) -> str:
        return self.xa_scel.currentStreamURL()

    @property
    def current_track(self) -> 'XATVTrack':
        return self._new_element(self.xa_scel.currentTrack(), XATVTrack)

    @property
    def fixed_indexing(self) -> bool:
        return self.xa_scel.fixedIndexing()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def full_screen(self) -> bool:
        return self.xa_scel.fullScreen()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def mute(self) -> bool:
        return self.xa_scel.mute()

    @property
    def player_position(self) -> float:
        return self.xa_scel.playerPosition()

    @property
    def player_state(self) -> 'XATVApplication.PlayerState':
        return XATVApplication.PlayerState(self.xa_scel.playerState())

    @property
    def selection(self) -> 'XATVItemList':
        return self._new_element(self.xa_scel.selection().get(), XATVTrackList)

    @property
    def sound_volume(self) -> int:
        return self.xa_scel.soundVolume()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def play(self, item: 'XATVItem' = None) -> 'XATVApplication':
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XATVItem, optional
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playOnce_(item)
        return self

    def playpause(self) -> 'XATVApplication':
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> 'XATVApplication':
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> 'XATVApplication':
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> 'XATVApplication':
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> 'XATVApplication':
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> 'XATVApplication':
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> 'XATVApplication':
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> 'XATVApplication':
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> 'XATVApplication':
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> 'XATVApplication':
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XATVApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> 'XATVApplication':
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def current_track(self) -> 'XATVTrack':
        """Returns the currently playing (or paused but not stopped) track.

        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": self.xa_scel.currentTrack(),
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XATVTrack(properties)

    # def convert(self, items):
    #     self.xa_scel.convert_([item.xa_elem for item in items])

    def add_to_playlist(self, urls: List[Union[str, NSURL]], playlist):
        items = []
        for url in urls:
            if isinstance(url, str):
                url = NSURL.alloc().initFileURLWithPath_(url)
            items.append(url)
        print(items)
        self.xa_scel.add_to_(items, playlist.xa_elem)

    def browser_windows(self, filter: Union[dict, None] = None) -> 'XATVBrowserWindowList':
        """Returns a list of browser windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browser windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVBrowserWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.browserWindows(), XATVBrowserWindowList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XATVPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XATVPlaylistList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlists(), XATVPlaylistList, filter)

    def playlist_windows(self, filter: Union[dict, None] = None) -> 'XATVPlaylistWindowList':
        """Returns a list of playlist windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVPlaylistWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlistWindows(), XATVPlaylistWindowList, filter)

    def sources(self, filter: Union[dict, None] = None) -> 'XATVSourceList':
        """Returns a list of sources, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sources will have, or None
        :type filter: Union[dict, None]
        :return: The list of sources
        :rtype: XATVSourceList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.sources(), XATVSourceList, filter)

    def tracks(self, filter: Union[dict, None] = None) -> 'XATVTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XATVTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XATVTrackList, filter)

    def video_windows(self, filter: Union[dict, None] = None) -> 'XATVVideoWindowList':
        """Returns a list of video windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XATVVideoWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.videoWindows(), XATVVideoWindowList, filter)




class XATVItemList(XABase.XAList):
    """A wrapper around lists of TV items that employs fast enumeration techniques.

    All properties of TV items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATVItem
        super().__init__(properties, obj_class, filter)

    def container(self) -> List[XABase.XAObject]:
        """Gets the container of each TV item in the list.

        :return: A list of TV item containers
        :rtype: List[XABase.XAObject]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XABase.XAList)

    def id(self) -> List[int]:
        """Gets the ID of each TV item in the list.

        :return: A list of TV item IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def index(self) -> List[int]:
        """Gets the index of each TV item in the list.

        :return: A list of TV item indices
        :rtype: List[nt]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def name(self) -> List[str]:
        """Gets the name of each TV item in the list.

        :return: A list of TV item names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def persistent_id(self) -> List[str]:
        """Gets the persistent ID of each TV item in the list.

        :return: A list of TV item persistent IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("persistentID"))
    
    def properties(self) -> List[dict]:
        """Gets the properties of each TV item in the list.

        :return: A list of TV item properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def by_container(self, container: XABase.XAObject) -> Union['XATVItem', None]:
        """Retrieves the first TV item whose container matches the given container object, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("container", container.xa_elem)

    def by_id(self, id: int) -> Union['XATVItem', None]:
        """Retrieves the TV item whose ID matches the given ID, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union['XATVItem', None]:
        """Retrieves the TV item whose index matches the given index, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union['XATVItem', None]:
        """Retrieves the TV item whose name matches the given name, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_persistent_id(self, persistent_id: str) -> Union['XATVItem', None]:
        """Retrieves the TV item whose persistent ID matches the given ID, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("persistentID", persistent_id)

    def by_properties(self, properties: dict) -> Union['XATVItem', None]:
        """Retrieves the TV item whose properties dictionary matches the given dictionary, if one exists.

        :return: The desired TV item, if it is found
        :rtype: Union[XATVItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("properties", properties)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XATVItem(XABase.XAObject):
    """A generic class with methods common to the various playable media classes in TV.app.

    .. seealso:: :class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.container: XABase.XAObject #: The container of the item
        self.id: int #: The ID of the item
        self.index: int #: The index of the item in the internal application order
        self.name: str #: The name of the item
        self.persistent_id: str #: The constant unique identifier for the item
        self.properties: dict #: Every property of the item

    @property
    def container(self) -> XABase.XAObject:
        return self._new_element(self.xa_elem.container(), XABase.XAObject)

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def persistent_id(self) -> str:
        return self.xa_elem.persistentID()

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    def download(self) -> 'XATVItem':
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> 'XATVItem':
        """Reveals the item in the TV.app window.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. seealso:: :func:`select`
        
        .. versionadded:: 0.0.1
        """
        self.xa_elem.reveal()
        return self




class XATVArtworkList(XATVItemList):
    """A wrapper around lists of TV artworks that employs fast enumeration techniques.

    All properties of TV artworks can be called as methods on the wrapped list, returning a list containing each artworks's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVArtwork)

    def data(self) -> List[XABase.XAImage]:
        """Gets the data image of each artwork in the list.

        :return: A list of artwork images
        :rtype: List[XABase.XAImage]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("data")
        return [XABase.XAImage(x) for x in ls]

    def object_description(self) -> List[str]:
        """Gets the description of each artwork in the list.

        :return: A list of artwork descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def downloaded(self) -> List[bool]:
        """Gets the download status of each artwork in the list.

        :return: A list of artwork download statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaded"))

    def format(self) -> List[int]:
        """Gets the format of each artwork in the list.

        :return: A list of artwork formats
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("format"))

    def kind(self) -> List[int]:
        """Gets the kind of each artwork in the list.

        :return: A list of artwork kinds
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def raw_data(self) -> List[bytes]:
        """Gets the raw data of each artwork in the list.

        :return: A list of artwork raw data
        :rtype: List[bytes]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rawData"))

    def by_data(self, data: XABase.XAImage) -> Union['XATVArtwork', None]:
        """Retrieves the artwork whose data matches the given image, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("data", data.xa_elem)

    def by_object_description(self, object_description: str) -> Union['XATVArtwork', None]:
        """Retrieves the artwork whose description matches the given description, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_downloaded(self, downloaded: bool) -> Union['XATVArtwork', None]:
        """Retrieves the first artwork whose downloaded status matches the given boolean value, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaded", downloaded)

    def by_format(self, format: int) -> Union['XATVArtwork', None]:
        """Retrieves the first artwork whose format matches the format, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("format", format)

    def by_kind(self, kind: int) -> Union['XATVArtwork', None]:
        """Retrieves the first artwork whose kind matches the given kind, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_raw_data(self, raw_data: bytes) -> Union['XATVArtwork', None]:
        """Retrieves the artwork whose raw data matches the given byte data, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XATVArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rawData", raw_data)

class XATVArtwork(XATVItem):
    """An artwork in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.data: XABase.XAImage #: The data for the artwork in the form of a picture
        self.object_description: str #: The string description of the artwork
        self.downloaded: bool #: Whether the artwork was downloaded by TV.app
        self.format: int #: The data format for the artwork
        self.kind: int #: The kind/purpose of the artwork
        self.raw_data: bytes #: The data for the artwork in original format

    @property
    def data(self) -> XABase.XAImage:
        return XABase.XAImage(self.xa_elem.data())

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def downloaded(self) -> bool:
        return self.xa_elem.downloaded()

    @property
    def format(self) -> int:
        return self.xa_elem.format()

    @property
    def kind(self) -> int:
        return self.xa_elem.kind()

    @property
    def raw_data(self) -> bytes:
        return self.xa_elem.rawData()




class XATVPlaylistList(XATVItemList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATVPlaylist
        super().__init__(properties, filter, obj_class)

    def object_description(self) -> List[str]:
        """Gets the description of each playlist in the list.

        :return: A list of playlist descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def duration(self) -> List[int]:
        """Gets the duration of each playlist in the list.

        :return: A list of playlist durations
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duration"))

    def name(self) -> List[str]:
        """Gets the name of each playlist in the list.

        :return: A list of playlist names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def parent(self) -> 'XATVPlaylistList':
        """Gets the parent playlist of each playlist in the list.

        :return: A list of playlist parent playlists
        :rtype: XATVPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XATVPlaylistList)

    def size(self) -> List[int]:
        """Gets the size of each playlist in the list.

        :return: A list of playlist sizes
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def special_kind(self) -> List[XATVApplication.PlaylistKind]:
        """Gets the special kind of each playlist in the list.

        :return: A list of playlist kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("specialKind")
        return [XATVApplication.PlaylistKind(XABase.OSType(x.stringValue())) for x in ls]

    def time(self) -> List[str]:
        """Gets the time, in HH:MM:SS format, of each playlist in the list.

        :return: A list of playlist times
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("time"))

    def visible(self) -> List[bool]:
        """Gets the visible status of each playlist in the list.

        :return: A list of playlist visible statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def by_object_description(self, object_description: str) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose closeable description matches the given description, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_duration(self, duration: int) -> Union['XATVPlaylist', None]:
        """Retrieves the first playlist whose duration matches the given duration, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_name(self, name: str) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose name matches the given name, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_parent(self, parent: 'XATVPlaylist') -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose parent matches the given playlist, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("parent", parent.xa_elem)

    def by_size(self, size: int) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose size matches the given size, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_special_kind(self, special_kind: XATVApplication.PlaylistKind) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose kind matches the given kind, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("specialKind", special_kind.value)

    def by_time(self, time: str) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose time string matches the given string, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_visible(self, visible: bool) -> Union['XATVPlaylist', None]:
        """Retrieves the playlist whose visible status matches the given boolean value, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XATVPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

class XATVPlaylist(XATVItem):
    """A playlist in TV.app.

    .. seealso:: :class:`XATVLibraryPlaylist`, :class:`XATVUserPlaylist`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.object_description: str #: The string description of the playlist
        self.duration: int #: The total length of all tracks in seconds
        self.name: str #: The name of the playlist
        self.parent: XATVPlaylist #: The folder containing the playlist, if any
        self.size: int #: The total size of all tracks in the playlist in bytes
        self.special_kind: XATVApplication.PlaylistKind #: The special playlist kind
        self.time: str #: The length of all tracks in the playlist in MM:SS format
        self.visible: bool #: Whether the playlist is visible in the source list

        if not hasattr(self, "xa_specialized"):
            print(self.xa_elem.objectClass())
            if self.special_kind == XATVApplication.PlaylistKind.LIBRARY or self.special_kind == XATVApplication.PlaylistKind.USER_LIBRARY:
                self.__class__ = XATVLibraryPlaylist

            elif self.special_kind == XATVApplication.PlaylistKind.FOLDER:
                self.__class__ = XATVFolderPlaylist

            elif self.special_kind == XATVApplication.PlaylistKind.USER or self.special_kind == XATVApplication.PlaylistKind.NONE:
                self.__class__ = XATVUserPlaylist

            self.xa_specialized = True
            self.__init__(properties)

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def duration(self) -> int:
        return self.xa_elem.duration()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def parent(self) -> 'XATVPlaylist':
        return self._new_element(self.xa_elem.parent(), XATVPlaylist)

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def special_kind(self) -> XATVApplication.PlaylistKind:
        return XATVApplication.PlaylistKind(self.xa_elem.specialKind())

    @property
    def time(self) -> str:
        return self.xa_elem.time()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    def move_to(self, parent_playlist):
        self.xa_elem.moveTo_(parent_playlist.xa_elem)

    def search(self, query: str, type: Literal["all", "artists", "albums", "displayed", "tracks"] = "displayed"):
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
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": result,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            items.append(XATVTrack(properties))
        return items

    def tracks(self, filter: Union[dict, None] = None) -> 'XATVTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XATVTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.tracks(), XATVTrackList, filter)

    def artworks(self, filter: Union[dict, None] = None) -> 'XATVArtworkList':
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
    """The library playlist in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XATVFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XATVFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.fileTracks(), XATVFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XATVURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XATVURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XATVURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XATVSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XATVSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.sharedTracks(), XATVSharedTrackList, filter)




class XATVSourceList(XATVItemList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVSource)

    def capacity(self) -> List[int]:
        """Gets the capacity of each source in the list.

        :return: A list of source capacity amounts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("capacity"))

    def free_space(self) -> List[int]:
        """Gets the free space of each source in the list.

        :return: A list of source free space amounts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace"))

    def kind(self) -> List[XATVApplication.SourceKind]:
        """Gets the kind of each source in the list.

        :return: A list of source kinds
        :rtype: List[XATVApplication.SourceKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("kind")
        return [XATVApplication.SourceKind(XABase.OSType(x.stringValue())) for x in ls]

    def by_capacity(self, capacity: int) -> Union['XATVSource', None]:
        """Retrieves the source whose capacity matches the given capacity, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XATVSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union['XATVSource', None]:
        """Retrieves the source whose free space matches the given value, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XATVSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("freeSpace", free_space)

    def by_kind(self, kind: XATVApplication.SourceKind) -> Union['XATVSource', None]:
        """Retrieves the source whose kind matches the given kind, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XATVSource, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("kind", kind.value)

class XATVSource(XATVItem):
    """A media source in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.capacity: int #: The total size of the source, if it has a fixed size
        self.free_space: int #: The free space on the source, if it has a fixed size
        self.kind: XATVApplication.SourceKind #: The source kind

    @property
    def capacity(self) -> int:
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        return self.xa_elem.freeSpace()

    @property
    def kind(self) -> XATVApplication.SourceKind:
        return XATVApplication.SourceKind(self.xa_elem.kind())

    def library_playlists(self, filter: Union[dict, None] = None) -> 'XATVLibraryPlaylistList':
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned library playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XATVLibraryPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.libraryPlaylists(), XATVLibraryPlaylistList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XATVPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XATVPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.playlists(), XATVPlaylistList, filter)

    def user_playlists(self, filter: Union[dict, None] = None) -> 'XATVUserPlaylistList':
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned user playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XATVUserPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.userPlaylists(), XATVUserPlaylistList, filter)




class XATVTrackList(XATVItemList):
    """A wrapper around lists of TV tracks that employs fast enumeration techniques.

    All properties of TV tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATVTrack
        super().__init__(properties, filter, obj_class)

    def album(self) -> List[str]:
        """Gets the album name of each track in the list.

        :return: A list of track album names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("album"))

    def album_rating(self) -> List[int]:
        """Gets the album rating of each track in the list.

        :return: A list of track album ratings
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumRating"))

    def album_rating_kind(self) -> List[XATVApplication.RatingKind]:
        """Gets the album rating kind of each track in the list.

        :return: A list of track album rating kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("albumRatingKind")
        return [XATVApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def bit_rate(self) -> List[int]:
        """Gets the bit rate of each track in the list.

        :return: A list of track bit rates
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bitRate"))

    def bookmark(self) -> List[float]:
        """Gets the bookmark time of each track in the list.

        :return: A list of track bookmark times
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bookmark"))

    def bookmarkable(self) -> List[bool]:
        """Gets the bookmarkable status of each track in the list.

        :return: A list of track bookmarkable statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bookmarkable"))

    def category(self) -> List[str]:
        """Gets the category of each track in the list.

        :return: A list of track categories
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("category"))

    def comment(self) -> List[str]:
        """Gets the comment of each track in the list.

        :return: A list of track comments
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def database_id(self) -> List[int]:
        """Gets the database ID of each track in the list.

        :return: A list of track database IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("databaseID"))

    def date_added(self) -> List[datetime]:
        """Gets the date added of each track in the list.

        :return: A list of track dates added
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dateAdded"))

    def object_description(self) -> List[str]:
        """Gets the description of each track in the list.

        :return: A list of track descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def director(self) -> List[str]:
        """Gets the director of each track in the list.

        :return: A list of track directors
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("director"))

    def disc_count(self) -> List[int]:
        """Gets the disc count of each track in the list.

        :return: A list of track disc counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discCount"))

    def disc_number(self) -> List[int]:
        """Gets the disc number of each track in the list.

        :return: A list of track disc numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discNumber"))

    def downloader_apple_id(self) -> List[str]:
        """Gets the downloader Apple ID of each track in the list.

        :return: A list of track downloader Apple IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderAppleID"))

    def downloader_name(self) -> List[str]:
        """Gets the downloader name of each track in the list.

        :return: A list of track downloader names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderName"))

    def duration(self) -> List[float]:
        """Gets the duration of each track in the list.

        :return: A list of track durations
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duration"))

    def enabled(self) -> List[bool]:
        """Gets the enabled status of each track in the list.

        :return: A list of track enabled statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def episode_id(self) -> List[str]:
        """Gets the episode ID of each track in the list.

        :return: A list of track episode IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("episodeID"))

    def episode_number(self) -> List[int]:
        """Gets the episode number of each track in the list.

        :return: A list of track episode numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("episodeNumber"))

    def finish(self) -> List[float]:
        """Gets the stop time of each track in the list.

        :return: A list of track stop times
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("finish"))

    def genre(self) -> List[str]:
        """Gets the genre of each track in the list.

        :return: A list of track genres
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("genre"))

    def grouping(self) -> List[str]:
        """Gets the grouping of each track in the list.

        :return: A list of track groupings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("grouping"))

    def kind(self) -> List[str]:
        """Gets the kind of each track in the list.

        :return: A list of track kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def long_description(self) -> List[str]:
        """Gets the long description of each track in the list.

        :return: A list of track long descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("longDescription"))

    def media_kind(self) -> List[XATVApplication.MediaKind]:
        """Gets the media kind of each track in the list.

        :return: A list of track media kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("mediaKind")
        return [XATVApplication.MediaKind(XABase.OSType(x.stringValue())) for x in ls]

    def modification_date(self) -> List[datetime]:
        """Gets the modification date of each track in the list.

        :return: A list of track modification dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def played_count(self) -> List[int]:
        """Gets the played count of each track in the list.

        :return: A list of track played counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("playedCount"))

    def played_date(self) -> List[datetime]:
        """Gets the played date of each track in the list.

        :return: A list of track played dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("playedDate"))

    def purchaser_apple_id(self) -> List[str]:
        """Gets the purchaser Apple ID of each track in the list.

        :return: A list of track purchaser Apple IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserAppleID"))

    def purchaser_name(self) -> List[str]:
        """Gets the purchaser name of each track in the list.

        :return: A list of track purchaser names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserName"))

    def rating(self) -> List[int]:
        """Gets the rating of each track in the list.

        :return: A list of track ratings
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rating"))

    def rating_kind(self) -> List[XATVApplication.RatingKind]:
        """Gets the rating kind of each track in the list.

        :return: A list of track rating kinds
        :rtype: List[XATVApplication.RatingKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("ratingKind")
        return [XATVApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def release_date(self) -> List[datetime]:
        """Gets the release date of each track in the list.

        :return: A list of track release dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("releaseDate"))

    def sample_rate(self) -> List[int]:
        """Gets the sample rate of each track in the list.

        :return: A list of track sample rates
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sampleRate"))

    def season_number(self) -> List[int]:
        """Gets the season number of each track in the list.

        :return: A list of track season numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("seasonNumber"))

    def skipped_count(self) -> List[int]:
        """Gets the skipped count of each track in the list.

        :return: A list of track skipped count
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("skippedCount"))

    def skipped_date(self) -> List[datetime]:
        """Gets the skipped date of each track in the list.

        :return: A list of track skipped dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("skippedDate"))

    def show(self) -> List[str]:
        """Gets the show of each track in the list.

        :return: A list of track shows
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("show"))

    def sort_album(self) -> List[str]:
        """Gets the album sort string of each track in the list.

        :return: A list of track album sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortAlbum"))

    def sort_director(self) -> List[str]:
        """Gets the director sort string of each track in the list.

        :return: A list of track director sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortDirector"))

    def sort_name(self) -> List[str]:
        """Gets the name sort string of each track in the list.

        :return: A list of track name sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortName"))

    def sort_show(self) -> List[str]:
        """Gets the show sort strings of each track in the list.

        :return: A list of track show sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortShow"))

    def size(self) -> List[int]:
        """Gets the size of each track in the list.

        :return: A list of track sizes
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def start(self) -> List[float]:
        """Gets the start time of each track in the list.

        :return: A list of track start times
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("start"))

    def time(self) -> List[str]:
        """Gets the time string of each track in the list.

        :return: A list of track time strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("time"))

    def track_count(self) -> List[int]:
        """Gets the track count of each track in the list.

        :return: A list of track counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("trackCount"))

    def track_number(self) -> List[int]:
        """Gets the track number of each track in the list.

        :return: A list of track numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("trackNumber"))

    def unplayed(self) -> List[bool]:
        """Gets the unplayed status of each track in the list.

        :return: A list of track unplayed statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("unplayed"))

    def volume_adjustment(self) -> List[int]:
        """Gets the volume adjustment of each track in the list.

        :return: A list of track volume adjustments
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("volumeAdjustment"))

    def year(self) -> List[int]:
        """Gets the year of each track in the list.

        :return: A list of track years
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("year"))

    def by_album(self, album: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose album matches the given album, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("album", album)

    def by_album_rating(self, album_rating: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose album rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumRating", album_rating)

    def by_album_rating_kind(self, album_rating_kind: XATVApplication.RatingKind) -> Union['XATVTrack', None]:
        """Retrieves the first track whose album rating kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("albumRatingKind", album_rating_kind.value)

    def by_bit_rate(self, bit_rate: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose bit rate matches the given bit rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bitRate", bit_rate)

    def by_bookmark(self, bookmark: float) -> Union['XATVTrack', None]:
        """Retrieves the first track whose bookmark matches the given bookmark, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmark", bookmark)

    def by_bookmarkable(self, bookmarkable: bool) -> Union['XATVTrack', None]:
        """Retrieves the first track whose bookmarkable status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmarkable", bookmarkable)

    def by_category(self, category: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose category matches the given category, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose comment matches the given comment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("comment", comment)

    def by_database_id(self, database_id: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose database ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("databaseID", database_id)

    def by_date_added(self, date_added: datetime) -> Union['XATVTrack', None]:
        """Retrieves the first track whose date added matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("dateAdded", date_added)

    def by_object_description(self, object_description: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose description matches the given description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_director(self, director: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose director matches the given director, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("director", director)

    def by_disc_count(self, disc_count: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose disc count matches the given disc count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose disc number matches the given disc number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discNumber", disc_number)

    def by_downloader_apple_id(self, downloader_apple_id: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose downloader Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderAppleID", downloader_apple_id)

    def by_downloader_name(self, downloader_name: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose downloader name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderName", downloader_name)

    def by_duration(self, duration: float) -> Union['XATVTrack', None]:
        """Retrieves the first track whose duration matches the given duration, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_enabled(self, enabled: bool) -> Union['XATVTrack', None]:
        """Retrieves the first track whose enabled status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("enabled", enabled)

    def by_episode_id(self, episode_id: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose episode ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeID", episode_id)

    def by_episode_number(self, episode_number: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose episode number matches the given episode number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeNumber", episode_number)

    def by_finish(self, finish: float) -> Union['XATVTrack', None]:
        """Retrieves the first track whose stop time matches the given stop time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("finish", finish)

    def by_genre(self, genre: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose genre matches the given genre, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("genre", genre)

    def by_grouping(self, grouping: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose grouping matches the given grouping, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("grouping", grouping)

    def by_kind(self, kind: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_long_description(self, long_description: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose long description matches the given long description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("longDescription", long_description)

    def by_media_kind(self, media_kind: XATVApplication.MediaKind) -> Union['XATVTrack', None]:
        """Retrieves the first track whose media kind matches the given media kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("mediaKind", media_kind.value)

    def by_modification_date(self, modification_date: datetime) -> Union['XATVTrack', None]:
        """Retrieves the first track whose modification date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("modificationDate", modification_date)

    def by_played_count(self, played_count: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose played count matches the given played count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedCount", played_count)

    def by_played_date(self, played_date: datetime) -> Union['XATVTrack', None]:
        """Retrieves the first track whose last played date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedDate", played_date)

    def by_purchaser_apple_id(self, purchaser_apple_id: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose purchaser Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserAppleID", purchaser_apple_id)

    def by_purchaser_name(self, purchaser_name: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose purchaser name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserName", purchaser_name)

    def by_rating(self, rating: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rating", rating)

    def by_rating_kind(self, rating_kind: XATVApplication.RatingKind) -> Union['XATVTrack', None]:
        """Retrieves the first track whose rating kind matches the given rating kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("ratingKind", rating_kind.value)

    def by_release_date(self, release_date: datetime) -> Union['XATVTrack', None]:
        """Retrieves the first track whose release date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("releaseDate", release_date)

    def by_sample_rate(self, sample_rate: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose sample rate matches the given rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sampleRate", sample_rate)

    def by_season_number(self, season_number: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose season number matches the given season number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("seasonNumber", season_number)

    def by_skipped_count(self, skipped_count: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose skipped count matches the given skipped count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedCount", skipped_count)

    def by_skipped_date(self, skipped_date: datetime) -> Union['XATVTrack', None]:
        """Retrieves the first track whose last skipped date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedDate", skipped_date)

    def by_show(self, show: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose show matches the given show, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("show", show)

    def by_sort_album(self, sort_album: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose album sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortAlbum", sort_album)

    def by_sort_director(self, sort_director: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose director sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortDirector", sort_director)

    def by_sort_name(self, sort_name: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose name sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortName", sort_name)

    def by_sort_show(self, sort_show: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose show sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortShow", sort_show)

    def by_size(self, size: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose size matches the given size, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_start(self, start: float) -> Union['XATVTrack', None]:
        """Retrieves the first track whose start time matches the given start time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("start", start)

    def by_time(self, time: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose time string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_track_count(self, track_count: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose track count matches the given track count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackCount", track_count)

    def by_track_number(self, track_number: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose track number matches the given track number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackNumber", track_number)

    def by_unplayed(self, unplayed: bool) -> Union['XATVTrack', None]:
        """Retrieves the first track whose unplayed status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("unplayed", unplayed)

    def by_volume_adjustment(self, volume_adjustment: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose volume adjustment matches the given volume adjustment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("volumeAdjustment", volume_adjustment)

    def by_year(self, year: int) -> Union['XATVTrack', None]:
        """Retrieves the first track whose year matches the given year, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("year", year)

class XATVTrack(XATVItem):
    """A class for managing and interacting with tracks in TV.app.

    .. seealso:: :class:`XATVSharedTrack`, :class:`XATVFileTrack`, :class:`XATVRemoteURLTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.album: str #: The name of the album the track's album
        self.album_rating: int #: The rating of the track's album
        self.album_rating_kind: str #: The album's rating kind
        self.bit_rate: int #: The track's bitrate in kbps
        self.bookmark: float #: The bookmark time of the track in seconds
        self.bookmarkable: bool #: Whether the playback position is kept in memory after stopping the track
        self.category: str #: The category of the track
        self.comment: str #: User-provided notes on the track
        self.database_id: int #: A unique ID for the track
        self.date_added: datetime #: The date the track was added to the current playlist
        self.object_description: str #: A string description of the track
        self.director: str #: The director of the track
        self.disc_count: int #: The number of discs in the source album
        self.disc_number: int #: The index of the disc containing the track
        self.downloader_apple_id: str #: The Apple ID of the person who downloaded the track
        self.downloader_name: str #: The full name of the person who downloaded the track
        self.duration: float #: Length of the track in seconds
        self.enabled: bool #: Whether the track is able to be played
        self.episode_id: str #: A unique ID for the episode of the track
        self.episode_number: int #: The episode number of the track
        self.finish: float #: The time in seconds from the start at which the track stops playing.
        self.genre: str #: The TV/audio genre category of the track.
        self.grouping: str #: The current section/chapter/movement of the track
        self.kind: str #: A text description of the track
        self.long_description: str #: A long description for the track
        self.media_kind: XATVApplication.MediaKind #: A description of the track's media type
        self.modification_date: datetime #: The last modification date of the track's content
        self.played_count: int #: The number of the times the track has been played
        self.played_date: datetime #: The date the track was last played
        self.purchaser_apple_id: str #: The Apple ID of the person who bought the track
        self.purchaser_name: str #: The full name of the person who bought the track
        self.rating: int #: The rating of the track from 0 to 100
        self.rating_kind: XATVApplication.RatingKind #: Whether the rating is user-provided or computed
        self.release_date: datetime #: The date the track was released
        self.sample_rate: int #: The sample rate of the track in Hz
        self.season_number: int #: The number of the season the track belongs to
        self.skipped_count: int #: The number of times the track has been skipped
        self.skipped_date: datetime #: The date the track was last skipped
        self.show: str #: The name of the show the track belongs to
        self.sort_album: str #: The string used for this track when sorting by album
        self.sort_director: str #: The string used for this track when sorting by director
        self.sort_name: str #: The string used for this track when sorting by name
        self.sort_show: str #: The string used for this track when sorting by show
        self.size: int #: The size of the track in bytes
        self.start: float #: The start time of the track in seconds
        self.time: str #: HH:MM:SS representation for the duration of the track
        self.track_count: int #: The number of tracks in the track's album
        self.track_number: int #: The index of the track within its album
        self.unplayed: bool #: Whether the track has been played before
        self.volume_adjustment: int #: Volume adjustment setting for this track from -100 to +100
        self.year: int #: The year the track was released

        # print("Track type", self.objectClass.data())
        # if self.objectClass.data() == _SHARED_TRACK:
        #     self.__class__ = XATVSharedTrack
        #     self.__init__()
        # elif self.objectClass.data() == _FILE_TRACK:
        #     self.__class__ = XATVFileTrack
        #     self.__init__()
        # elif self.objectClass.data() == _URL_TRACK:
        #     self.__class__ = XATVURLTrack
        #     self.__init__()

    @property
    def album(self) -> str:
        return self.xa_elem.album()

    @property
    def album_rating(self) -> int:
        return self.xa_elem.albumRating()

    @property
    def album_rating_kind(self) -> XATVApplication.RatingKind:
        return XATVApplication.RatingKind(self.xa_elem.albumRatingKind())

    @property
    def bit_rate(self) -> int:
        return self.xa_elem.bitRate()

    @property
    def bookmark(self) -> float:
        return self.xa_elem.bookmark()

    @property
    def bookmarkable(self) -> bool:
        return self.xa_elem.bookmarkable()

    @property
    def category(self) -> str:
        return self.xa_elem.category()

    @property
    def comment(self) -> str:
        return self.xa_elem.comment()

    @property
    def database_id(self) -> int:
        return self.xa_elem.databaseID()

    @property
    def date_added(self) -> datetime:
        return self.xa_elem.dateAdded()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def director(self) -> str:
        return self.xa_elem.director()

    @property
    def disc_count(self) -> int:
        return self.xa_elem.discCount()

    @property
    def disc_number(self) -> int:
        return self.xa_elem.discNumber()

    @property
    def downloader_apple_id(self) -> str:
        return self.xa_elem.downloaderAppleID()

    @property
    def downloader_name(self) -> str:
        return self.xa_elem.downloaderName()

    @property
    def duration(self) -> float:
        return self.xa_elem.duration()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def episode_id(self) -> str:
        return self.xa_elem.episodeID()

    @property
    def episode_number(self) -> int:
        return self.xa_elem.episodeNumber()

    @property
    def finish(self) -> float:
        return self.xa_elem.finish()

    @property
    def genre(self) -> str:
        return self.xa_elem.genre()

    @property
    def grouping(self) -> str:
        return self.xa_elem.grouping()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def long_description(self) -> str:
        return self.xa_elem.longDescription()

    @property
    def media_kind(self) -> XATVApplication.MediaKind:
        return XATVApplication.MediaKind(self.xa_elem.mediaKind())

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def played_count(self) -> int:
        return self.xa_elem.playedCount()

    @property
    def played_date(self) -> datetime:
        return self.xa_elem.playedDate()

    @property
    def purchaser_apple_id(self) -> str:
        return self.xa_elem.purchaserAppleID()

    @property
    def purchaser_name(self) -> str:
        return self.xa_elem.purchaserName()

    @property
    def rating(self) -> int:
        return self.xa_elem.rating()

    @property
    def rating_kind(self) -> XATVApplication.RatingKind:
        return XATVApplication.RatingKind(self.xa_elem.ratingKind())

    @property
    def release_date(self) -> datetime:
        return self.xa_elem.releaseDate()

    @property
    def sample_rate(self) -> int:
        return self.xa_elem.sampleRate()

    @property
    def season_number(self) -> int:
        return self.xa_elem.seasonNumber()

    @property
    def skipped_count(self) -> int:
        return self.xa_elem.skippedCount()

    @property
    def skipped_date(self) -> datetime:
        return self.xa_elem.skippedDate()

    @property
    def show(self) -> str:
        return self.xa_elem.show()

    @property
    def sort_album(self) -> str:
        return self.xa_elem.sortAlbum()

    @property
    def sort_director(self) -> str:
        return self.xa_elem.sortDirector()

    @property
    def sort_name(self) -> str:
        return self.xa_elem.sortName()

    @property
    def sort_show(self) -> str:
        return self.xa_elem.sortShow()

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def start(self) -> float:
        return self.xa_elem.start()

    @property
    def time(self) -> str:
        return self.xa_elem.time()

    @property
    def track_count(self) -> int:
        return self.xa_elem.trackCount()

    @property
    def track_number(self) -> int:
        return self.xa_elem.trackNumber()

    @property
    def unplayed(self) -> bool:
        return self.xa_elem.unplayed()

    @property
    def volume_adjustment(self) -> int:
        return self.xa_elem.volumeAdjustment()

    @property
    def year(self) -> int:
        return self.xa_elem.year()

    def select(self) -> 'XATVItem':
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XATVTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self

    def play(self) -> 'XATVItem':
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XATVItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self

    def artworks(self, filter: Union[dict, None] = None) -> 'XATVArtworkList':
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XATVArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.artworks(), XATVArtworkList, filter)




class XATVFileTrackList(XATVTrackList):
    """A wrapper around lists of TV file tracks that employs fast enumeration techniques.

    All properties of TV file tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVFileTrack)

    def location(self) -> List[XABase.XAURL]:
        """Gets the location of each track in the list.

        :return: A list of track locations
        :rtype: List[XABase.XAURL]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union['XATVFileTrack', None]:
        """Retrieves the file track whose location matches the given location, if one exists.

        :return: The desired file track, if it is found
        :rtype: Union[XATVFileTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("location", location.xa_elem)

class XATVFileTrack(XATVTrack):
    """A file track in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.location: XABase.XAURL #: The location of the file represented by the track

    @property
    def location(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.location())




class XATVSharedTrackList(XATVTrackList):
    """A wrapper around lists of TV shared tracks that employs fast enumeration techniques.

    All properties of TV shared tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVSharedTrack)

class XATVSharedTrack(XATVTrack):
    """A shared track in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XATVURLTrackList(XATVTrackList):
    """A wrapper around lists of TV URL tracks that employs fast enumeration techniques.

    All properties of TV URL tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVURLTrack)

    def address(self) -> List[str]:
        """Gets the address of each track in the list.

        :return: A list of track addresses
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def by_address(self, address: str) -> Union['XATVURLTrack', None]:
        """Retrieves the URL track whose address matches the given address, if one exists.

        :return: The desired URL track, if it is found
        :rtype: Union[XATVURLTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("address", address)

class XATVURLTrack(XATVTrack):
    """A URL track in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: str #: The URL for the track

    @property
    def address(self) -> str:
        return self.xa_elem.address()




class XATVUserPlaylistList(XATVPlaylistList):
    """A wrapper around lists of TV user playlists that employs fast enumeration techniques.

    All properties of TV user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVUserPlaylist)

    def shared(self) -> List[bool]:
        """Gets the shared status of each user playlist in the list.

        :return: A list of playlist shared status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def smart(self) -> List[bool]:
        """Gets the smart status of each user playlist in the list.

        :return: A list of playlist smart status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("smart"))

    def by_shared(self, shared: bool) -> Union['XATVUserPlaylist', None]:
        """Retrieves the user playlist whose shared status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XATVUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("shared", shared)

    def by_smart(self, smart: bool) -> Union['XATVUserPlaylist', None]:
        """Retrieves the user playlist whose smart status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XATVUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("smart", smart)

class XATVUserPlaylist(XATVPlaylist):
    """A user-created playlist in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.shared: bool #: Whether the playlist is shared
        self.smart: bool #: Whether the playlist is a smart playlist

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @property
    def smart(self) -> bool:
        return self.xa_elem.smart()

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XATVFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XATVFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.fileTracks(), XATVFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XATVURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XATVURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XATVURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XATVSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XATVSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.sharedTracks(), XATVSharedTrackList, filter)




class XATVFolderPlaylistList(XATVUserPlaylistList):
    """A wrapper around lists of TV folder playlists that employs fast enumeration techniques.

    All properties of TV folder playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVFolderPlaylist)

class XATVFolderPlaylist(XATVUserPlaylist):
    """A folder playlist in TV.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XATVWindowList(XATVItemList):
    """A wrapper around lists of TV browser windows that employs fast enumeration techniques.

    All properties of TV browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATVWindow
        super().__init__(properties, filter, obj_class)

    def bounds(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Gets the bounds of each window in the list.

        :return: A list of window bounds
        :rtype: List[Tuple[Tuple[int, int], Tuple[int, int]]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def closeable(self) -> List[bool]:
        """Gets the closeable status of each window in the list.

        :return: A list of window closeable statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("closeable"))

    def collapseable(self) -> List[bool]:
        """Gets the collapseable status of each window in the list.

        :return: A list of window collapseable statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("collapseable"))

    def collapsed(self) -> List[bool]:
        """Gets the collapsed status of each window in the list.

        :return: A list of window collapsed statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed"))

    def full_screen(self) -> List[bool]:
        """Gets the full screen status of each window in the list.

        :return: A list of window full screen statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fullScreen"))

    def position(self) -> List[Tuple[int, int]]:
        """Gets the position of each window in the list.

        :return: A list of window positions
        :rtype: List[Tuple[int, int]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def resizable(self) -> List[bool]:
        """Gets the resizable status of each window in the list.

        :return: A list of window resizable statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("resizable"))

    def visible(self) -> List[bool]:
        """Gets the visible status of each window in the list.

        :return: A list of window visible statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def zoomable(self) -> List[bool]:
        """Gets the zoomable status of each window in the list.

        :return: A list of window zoomable statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable"))

    def zoomed(self) -> List[bool]:
        """Gets the zoomed status of each window in the list.

        :return: A list of window zoomed statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed"))

    def by_bounds(self, bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> Union['XATVWindow', None]:
        """Retrieves the window whose bounds matches the given bounds, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("bounds", bounds)

    def by_closeable(self, closeable: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose closeable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("closeable", closeable)

    def by_collapseable(self, collapseable: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose collapseable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapseable", collapseable)

    def by_collapsed(self, collapsed: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose collapsed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapsed", collapsed)

    def by_full_screen(self, full_screen: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose full screen status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fullScreen", full_screen)

    def by_position(self, position: Tuple[int, int]) -> Union['XATVWindow', None]:
        """Retrieves the first window whose position matches the given position, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("position", position)

    def by_resizable(self, resizable: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose resizable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose visible status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose zoomable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union['XATVWindow', None]:
        """Retrieves the first window whose zoomed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XATVWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomed", zoomed)

class XATVWindow(XABaseScriptable.XASBWindow, XATVItem):
    """A windows of TV.app.

    .. seealso:: :class:`XATVBrowserWindow`, :class:`XATVPlaylistWindow`, :class:`XATVVideoWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle for the window
        self.closeable: bool #: Whether the window has a close button
        self.collapseable: bool #: Whether the window can be minimized
        self.collapsed: bool #: Whether the window is currently minimized
        self.full_screen: bool #: Whether the window is currently full screen
        self.position: Tuple[int, int] #: The upper left position of the window
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed

        obj_class = self.xa_elem.objectClass().data()
        if not hasattr(self, "xa_specialized"):
            if obj_class == b'WrBc':
                self.__class__ = XATVBrowserWindow
            elif obj_class == b'WlPc':
                self.__class__ = XATVPlaylistWindow
            elif obj_class == b'niwc':
                self.__class__ = XATVVideoWindow
            self.xa_specialized = True
            self.__init__(properties)

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def collapseable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def collapsed(self) -> bool:
        return self.xa_elem.miniaturized()

    @property
    def full_screen(self) -> bool:
        return self.xa_elem.fullScreen()

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

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




class XATVBrowserWindowList(XATVWindowList):
    """A wrapper around lists of TV browser windows that employs fast enumeration techniques.

    All properties of TV browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVBrowserWindow)

    def selection(self) -> XATVTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XATVTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XATVTrackList)

    def view(self) -> XATVPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XATVPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XATVPlaylistList)

    def by_selection(self, selection: XATVTrackList) -> Union['XATVPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XATVPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XATVPlaylist) -> Union['XATVPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XATVPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XATVBrowserWindow(XATVWindow):
    """A browser window of TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XATVTrackList #: The selected tracks
        self.view: XATVPlaylist #: The playlist currently displayed in the window




class XATVPlaylistWindowList(XATVWindowList):
    """A wrapper around lists of TV playlist windows that employs fast enumeration techniques.

    All properties of TV playlist windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVPlaylistWindow)

    def selection(self) -> XATVTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XATVTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XATVTrackList)

    def view(self) -> XATVPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XATVPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XATVPlaylistList)

    def by_selection(self, selection: XATVTrackList) -> Union['XATVPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XATVPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XATVPlaylist) -> Union['XATVPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XATVPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XATVPlaylistWindow(XATVWindow):
    """A playlist window in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XATVTrackList #: The selected tracks
        self.view: XATVPlaylist #: The playlist currently displayed in the window




class XATVVideoWindowList(XATVWindowList):
    """A wrapper around lists of TV video windows that employs fast enumeration techniques.

    All properties of TV video windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATVVideoWindow)

class XATVVideoWindow(XATVWindow):
    """A video window in TV.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
