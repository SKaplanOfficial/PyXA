""".. versionadded:: 0.1.0

A base set of classes for media applications such as Music.app and TV.app.
"""

from datetime import datetime
from enum import Enum
import time
from typing import Literal, Union

import AppKit
from PyXA import XABase
from PyXA import XABaseScriptable
from PyXA.XAProtocols import XACanOpenPath


class XAMediaApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with media apps.

    .. seealso:: :class:`XAMediaWindow`, class:`XAMediaSource`, :class:`XAMediaPlaylist`, :class:`XAMediaTrack`

    .. versionadded:: 0.0.1
    """
    class PlayerState(Enum):
        """States of the music player.
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
        AUDIO_CD        = XABase.OSType('kACD') #: A CD source
        MP3_CD          = XABase.OSType('kMCD') #: An MP3 file source
        RADIO_TUNER     = XABase.OSType('kTun') #: A radio source
        SHARED_LIBRARY  = XABase.OSType('kShd') #: A shared library source
        ITUNES_STORE    = XABase.OSType('kITS') #: The iTunes Store source
        UNKNOWN         = XABase.OSType('kUnk') #: An unknown source

    class SearchFilter(Enum):
        """Filter restrictions on search results.
        """
        ALBUMS      = XABase.OSType('kSrL') #: Search albums
        ALL         = XABase.OSType('kAll') #: Search all
        ARTISTS     = XABase.OSType('kSrR') #: Search artists
        COMPOSERS   = XABase.OSType('kSrC') #: Search composers
        DISPLAYED   = XABase.OSType('kSrV') #: Search the currently displayed playlist
        NAMES       = XABase.OSType('kSrS') #: Search track names only
    
    class PlaylistKind(Enum):
        """Types of special playlists.
        """
        NONE            = XABase.OSType('kNon') #: An unknown playlist kind
        FOLDER          = XABase.OSType('kSpF') #: A folder
        GENIUS          = XABase.OSType('kSpG') #: A smart playlist
        LIBRARY         = XABase.OSType('kSpL') #: The system library playlist
        MUSIC           = XABase.OSType('kSpZ') #: A playlist containing music items
        PURCHASED_MUSIC = XABase.OSType('kSpM') #: The purchased music playlist
        USER            = XABase.OSType('cUsP') #: A user-created playlist
        USER_LIBRARY    = XABase.OSType('cLiP') #: The user's library

    class MediaKind(Enum):
        """Types of media items.
        """
        SONG        = XABase.OSType('kMdS') #: A song media item
        MUSIC_VIDEO = XABase.OSType('kVdV') #: A music video media item
        UNKNOWN     = XABase.OSType('kUnk') #: An unknown media item kind

    class RatingKind(Enum):
        """Types of ratings for media items.
        """
        USER        = XABase.OSType('kRtU') #: A user-inputted rating
        COMPUTED    = XABase.OSType('kRtC') #: A computer generated rating

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAMediaWindow

        self.current_playlist: XAMediaPlaylist #: The playlist containing the currently targeted track
        self.current_stream_title: str #: The name of the current streaming track
        self.current_stream_url: str #: The URL of the current streaming 
        self.current_track: XAMediaTrack #: The currently targeted track
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
    def current_playlist(self) -> 'XAMediaPlaylist':
        return self._new_element(self.xa_scel.currentPlaylist(), XAMediaPlaylist)

    @property
    def current_stream_title(self) -> str:
        return self.xa_scel.currentStreamTitle()

    @property
    def current_stream_url(self) -> str:
        return self.xa_scel.currentStreamURL()

    @property
    def current_track(self) -> 'XAMediaTrack':
        return self._new_element(self.xa_scel.currentTrack(), XAMediaTrack)

    @property
    def fixed_indexing(self) -> bool:
        return self.xa_scel.fixedIndexing()

    @fixed_indexing.setter
    def fixed_indexing(self, fixed_indexing: bool):
        self.set_property('fixedIndexing', fixed_indexing)

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def full_screen(self) -> bool:
        return self.xa_scel.fullScreen()

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.set_property('fullScreen', full_screen)

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def mute(self) -> bool:
        return self.xa_scel.mute()

    @mute.setter
    def mute(self, mute: bool):
        self.set_property('mute', mute)

    @property
    def player_position(self) -> float:
        return self.xa_scel.playerPosition()

    @player_position.setter
    def player_position(self, player_position: float):
        self.set_property('playerPosition', player_position)

    @property
    def player_state(self) -> 'XAMediaApplication.PlayerState':
        return XAMediaApplication.PlayerState(self.xa_scel.playerState())

    @property
    def selection(self) -> 'XAMediaItemList':
        return self._new_element(self.xa_scel.selection().get(), XAMediaTrackList)

    @property
    def sound_volume(self) -> int:
        return self.xa_scel.soundVolume()

    @sound_volume.setter
    def sound_volume(self, sound_volume: int):
        self.set_property('soundVolume', sound_volume)

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def play(self, item: 'XAMediaItem' = None) -> 'XAMediaApplication':
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XAMediaItem, optional
        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playOnce_(item)
        return self

    def playpause(self) -> 'XAMediaApplication':
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> 'XAMediaApplication':
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> 'XAMediaApplication':
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> 'XAMediaApplication':
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> 'XAMediaApplication':
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> 'XAMediaApplication':
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> 'XAMediaApplication':
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> 'XAMediaApplication':
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> 'XAMediaApplication':
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> 'XAMediaApplication':
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XAMediaApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> 'XAMediaApplication':
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XAMediaApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def current_track(self) -> 'XAMediaTrack':
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
        return XAMediaTrack(properties)

    # def convert(self, items):
    #     self.xa_scel.convert_([item.xa_elem for item in items])

    def browser_windows(self, filter: Union[dict, None] = None) -> 'XAMediaBrowserWindowList':
        """Returns a list of browser windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browser windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMediaBrowserWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.browserWindows(), XAMediaBrowserWindowList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XAMediaPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMediaPlaylistList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlists(), XAMediaPlaylistList, filter)

    def playlist_windows(self, filter: Union[dict, None] = None) -> 'XAMediaPlaylistWindowList':
        """Returns a list of playlist windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMediaPlaylistWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlistWindows(), XAMediaPlaylistWindowList, filter)

    def sources(self, filter: Union[dict, None] = None) -> 'XAMediaSourceList':
        """Returns a list of sources, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sources will have, or None
        :type filter: Union[dict, None]
        :return: The list of sources
        :rtype: XAMediaSourceList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.sources(), XAMediaSourceList, filter)

    def tracks(self, filter: Union[dict, None] = None) -> 'XAMediaTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMediaTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XAMediaTrackList, filter)

    def video_windows(self, filter: Union[dict, None] = None) -> 'XAMediaVideoWindowList':
        """Returns a list of video windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMediaVideoWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.videoWindows(), XAMediaVideoWindowList, filter)




class XAMediaItemList(XABase.XAList):
    """A wrapper around lists of music items that employs fast enumeration techniques.

    All properties of music items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMediaItem
        super().__init__(properties, obj_class, filter)

    def container(self) -> list[XABase.XAObject]:
        """Gets the container of each music item in the list.

        :return: A list of music item containers
        :rtype: list[XABase.XAObject]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XABase.XAList)

    def id(self) -> list[int]:
        """Gets the ID of each music item in the list.

        :return: A list of music item IDs
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def index(self) -> list[int]:
        """Gets the index of each music item in the list.

        :return: A list of music item indices
        :rtype: list[nt]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def name(self) -> list[str]:
        """Gets the name of each music item in the list.

        :return: A list of music item names
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def persistent_id(self) -> list[str]:
        """Gets the persistent ID of each music item in the list.

        :return: A list of music item persistent IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("persistentID"))
    
    def properties(self) -> list[dict]:
        """Gets the properties of each music item in the list.

        :return: A list of music item properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def by_container(self, container: XABase.XAObject) -> Union['XAMediaItem', None]:
        """Retrieves the first music item whose container matches the given container object, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("container", container.xa_elem)

    def by_id(self, id: int) -> Union['XAMediaItem', None]:
        """Retrieves the music item whose ID matches the given ID, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union['XAMediaItem', None]:
        """Retrieves the music item whose index matches the given index, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union['XAMediaItem', None]:
        """Retrieves the music item whose name matches the given name, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_persistent_id(self, persistent_id: str) -> Union['XAMediaItem', None]:
        """Retrieves the music item whose persistent ID matches the given ID, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("persistentID", persistent_id)

    def by_properties(self, properties: dict) -> Union['XAMediaItem', None]:
        """Retrieves the music item whose properties dictionary matches the given dictionary, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMediaItem, None]
        
        .. versionadded:: 0.0.7
        """
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

class XAMediaItem(XABase.XAObject):
    """A generic class with methods common to the various playable media classes in media apps.

    .. seealso:: :class:`XAMediaSource`, :class:`XAMediaPlaylist`, :class:`XAMediaTrack`

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

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def persistent_id(self) -> str:
        return self.xa_elem.persistentID()

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    def download(self) -> 'XAMediaItem':
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XAMediaItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> 'XAMediaItem':
        """Reveals the item in the media apps window.

        :return: A reference to the TV item object.
        :rtype: XAMediaItem

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




class XAMediaArtworkList(XAMediaItemList):
    """A wrapper around lists of music artworks that employs fast enumeration techniques.

    All properties of music artworks can be called as methods on the wrapped list, returning a list containing each artworks's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaArtwork)

    def data(self) -> list[XABase.XAImage]:
        """Gets the data image of each artwork in the list.

        :return: A list of artwork images
        :rtype: list[XABase.XAImage]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("data")
        return [XABase.XAImage(x) for x in ls]

    def object_description(self) -> list[str]:
        """Gets the description of each artwork in the list.

        :return: A list of artwork descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def downloaded(self) -> list[bool]:
        """Gets the download status of each artwork in the list.

        :return: A list of artwork download statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaded"))

    def format(self) -> list[int]:
        """Gets the format of each artwork in the list.

        :return: A list of artwork formats
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("format"))

    def kind(self) -> list[int]:
        """Gets the kind of each artwork in the list.

        :return: A list of artwork kinds
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def raw_data(self) -> list[bytes]:
        """Gets the raw data of each artwork in the list.

        :return: A list of artwork raw data
        :rtype: list[bytes]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rawData"))

    def by_data(self, data: XABase.XAImage) -> Union['XAMediaArtwork', None]:
        """Retrieves the artwork whose data matches the given image, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("data", data.xa_elem)

    def by_object_description(self, object_description: str) -> Union['XAMediaArtwork', None]:
        """Retrieves the artwork whose description matches the given description, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_downloaded(self, downloaded: bool) -> Union['XAMediaArtwork', None]:
        """Retrieves the first artwork whose downloaded status matches the given boolean value, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaded", downloaded)

    def by_format(self, format: int) -> Union['XAMediaArtwork', None]:
        """Retrieves the first artwork whose format matches the format, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("format", format)

    def by_kind(self, kind: int) -> Union['XAMediaArtwork', None]:
        """Retrieves the first artwork whose kind matches the given kind, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_raw_data(self, raw_data: bytes) -> Union['XAMediaArtwork', None]:
        """Retrieves the artwork whose raw data matches the given byte data, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMediaArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rawData", raw_data)

class XAMediaArtwork(XAMediaItem):
    """An artwork in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.data: XABase.XAImage #: The data for the artwork in the form of a picture
        self.object_description: str #: The string description of the artwork
        self.downloaded: bool #: Whether the artwork was downloaded by media apps
        self.format: int #: The data format for the artwork
        self.kind: int #: The kind/purpose of the artwork
        self.raw_data: bytes #: The data for the artwork in original format

    @property
    def data(self) -> XABase.XAImage:
        return XABase.XAImage(self.xa_elem.data())

    @data.setter
    def data(self, data: XABase.XAImage):
        self.set_property('data', data.xa_elem)

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property('objectDescription', object_description)

    @property
    def downloaded(self) -> bool:
        return self.xa_elem.downloaded()

    @property
    def format(self) -> int:
        return self.xa_elem.format()

    @property
    def kind(self) -> int:
        return self.xa_elem.kind()

    @kind.setter
    def kind(self, kind: int):
        self.set_property('kind', kind)

    @property
    def raw_data(self) -> bytes:
        return self.xa_elem.rawData()

    @raw_data.setter
    def raw_data(self, raw_data: str):
        self.set_property('rawData', raw_data)




class XAMediaPlaylistList(XAMediaItemList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMediaPlaylist
        super().__init__(properties, filter, obj_class)

    def object_description(self) -> list[str]:
        """Gets the description of each playlist in the list.

        :return: A list of playlist descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def duration(self) -> list[int]:
        """Gets the duration of each playlist in the list.

        :return: A list of playlist durations
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duration"))

    def name(self) -> list[str]:
        """Gets the name of each playlist in the list.

        :return: A list of playlist names
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def parent(self) -> 'XAMediaPlaylistList':
        """Gets the parent playlist of each playlist in the list.

        :return: A list of playlist parent playlists
        :rtype: XAMediaPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAMediaPlaylistList)

    def size(self) -> list[int]:
        """Gets the size of each playlist in the list.

        :return: A list of playlist sizes
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def special_kind(self) -> list[XAMediaApplication.PlaylistKind]:
        """Gets the special kind of each playlist in the list.

        :return: A list of playlist kinds
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("specialKind")
        return [XAMediaApplication.PlaylistKind(XABase.OSType(x.stringValue())) for x in ls]

    def time(self) -> list[str]:
        """Gets the time, in HH:MM:SS format, of each playlist in the list.

        :return: A list of playlist times
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("time"))

    def visible(self) -> list[bool]:
        """Gets the visible status of each playlist in the list.

        :return: A list of playlist visible statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def by_object_description(self, object_description: str) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose closeable description matches the given description, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_duration(self, duration: int) -> Union['XAMediaPlaylist', None]:
        """Retrieves the first playlist whose duration matches the given duration, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_name(self, name: str) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose name matches the given name, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_parent(self, parent: 'XAMediaPlaylist') -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose parent matches the given playlist, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("parent", parent.xa_elem)

    def by_size(self, size: int) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose size matches the given size, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_special_kind(self, special_kind: XAMediaApplication.PlaylistKind) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose kind matches the given kind, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("specialKind", special_kind.value)

    def by_time(self, time: str) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose time string matches the given string, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_visible(self, visible: bool) -> Union['XAMediaPlaylist', None]:
        """Retrieves the playlist whose visible status matches the given boolean value, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMediaPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

class XAMediaPlaylist(XAMediaItem):
    """A playlist in media apps.

    .. seealso:: :class:`XAMediaLibraryPlaylist`, :class:`XAMediaUserPlaylist`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.object_description: str #: The string description of the playlist
        self.disliked: bool #: Whether the playlist is disliked
        self.duration: int #: The total length of all tracks in seconds
        self.name: str #: The name of the playlist
        self.loved: bool #: Whether the playlist is loved
        self.parent: XAMediaPlaylist #: The folder containing the playlist, if any
        self.size: int #: The total size of all tracks in the playlist in bytes
        self.special_kind: XAMediaApplication.PlaylistKind #: The special playlist kind
        self.time: str #: The length of all tracks in the playlist in MM:SS format
        self.visible: bool #: Whether the playlist is visible in the source list

        if not hasattr(self, "xa_specialized"):
            print(self.xa_elem.objectClass())
            if self.special_kind == XAMediaApplication.PlaylistKind.LIBRARY or self.special_kind == XAMediaApplication.PlaylistKind.USER_LIBRARY:
                self.__class__ = XAMediaLibraryPlaylist

            elif self.special_kind == XAMediaApplication.PlaylistKind.FOLDER:
                self.__class__ = XAMediaFolderPlaylist

            elif self.special_kind == XAMediaApplication.PlaylistKind.USER or self.special_kind == XAMediaApplication.PlaylistKind.NONE:
                self.__class__ = XAMediaUserPlaylist

            self.xa_specialized = True
            self.__init__(properties)

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property('objectDescription', object_description)

    @property
    def duration(self) -> int:
        return self.xa_elem.duration()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def parent(self) -> 'XAMediaPlaylist':
        return self._new_element(self.xa_elem.parent(), XAMediaPlaylist)

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def special_kind(self) -> XAMediaApplication.PlaylistKind:
        return XAMediaApplication.PlaylistKind(self.xa_elem.specialKind())

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
            "all": XAMediaApplication.SearchFilter.ALL,
            "artists": XAMediaApplication.SearchFilter.ARTISTS,
            "albums": XAMediaApplication.SearchFilter.ALBUMS,
            "displayed": XAMediaApplication.SearchFilter.DISPLAYED,
            "tracks": XAMediaApplication.SearchFilter.NAMES,
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
            items.append(XAMediaTrack(properties))
        return items

    def tracks(self, filter: Union[dict, None] = None) -> 'XAMediaTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMediaTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.tracks(), XAMediaTrackList, filter)

    def artworks(self, filter: Union[dict, None] = None) -> 'XAMediaArtworkList':
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMediaArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.artworks(), XAMediaArtworkList, filter)



class XAMediaLibraryPlaylistList(XAMediaPlaylistList):
    """A wrapper around lists of library playlists that employs fast enumeration techniques.

    All properties of library playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaLibraryPlaylist)

class XAMediaLibraryPlaylist(XAMediaPlaylist):
    """The library playlist in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMediaFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), XAMediaFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMediaURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMediaURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMediaSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sharedTracks(), XAMediaSharedTrackList, filter)




class XAMediaSourceList(XAMediaItemList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMediaSource
        super().__init__(properties, filter, obj_class)

    def capacity(self) -> list[int]:
        """Gets the capacity of each source in the list.

        :return: A list of source capacity amounts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("capacity"))

    def free_space(self) -> list[int]:
        """Gets the free space of each source in the list.

        :return: A list of source free space amounts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace"))

    def kind(self) -> list[XAMediaApplication.SourceKind]:
        """Gets the kind of each source in the list.

        :return: A list of source kinds
        :rtype: list[XAMediaApplication.SourceKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("kind")
        return [XAMediaApplication.SourceKind(XABase.OSType(x.stringValue())) for x in ls]

    def by_capacity(self, capacity: int) -> Union['XAMediaSource', None]:
        """Retrieves the source whose capacity matches the given capacity, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMediaSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union['XAMediaSource', None]:
        """Retrieves the source whose free space matches the given value, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMediaSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("freeSpace", free_space)

    def by_kind(self, kind: XAMediaApplication.SourceKind) -> Union['XAMediaSource', None]:
        """Retrieves the source whose kind matches the given kind, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMediaSource, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("kind", kind.value)

class XAMediaSource(XAMediaItem):
    """A media source in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.capacity: int #: The total size of the source, if it has a fixed size
        self.free_space: int #: The free space on the source, if it has a fixed size
        self.kind: XAMediaApplication.SourceKind #: The source kind

    @property
    def capacity(self) -> int:
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        return self.xa_elem.freeSpace()

    @property
    def kind(self) -> XAMediaApplication.SourceKind:
        return XAMediaApplication.SourceKind(self.xa_elem.kind())

    def library_playlists(self, filter: Union[dict, None] = None) -> 'XAMediaLibraryPlaylistList':
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned library playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XAMediaLibraryPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.libraryPlaylists(), XAMediaLibraryPlaylistList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XAMediaPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMediaPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.playlists(), XAMediaPlaylistList, filter)

    def user_playlists(self, filter: Union[dict, None] = None) -> 'XAMediaUserPlaylistList':
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned user playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XAMediaUserPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.userPlaylists(), XAMediaUserPlaylistList, filter)




class XAMediaTrackList(XAMediaItemList):
    """A wrapper around lists of music tracks that employs fast enumeration techniques.

    All properties of music tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMediaTrack
        super().__init__(properties, filter, obj_class)

    def album(self) -> list[str]:
        """Gets the album name of each track in the list.

        :return: A list of track album names
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("album"))

    def album_rating(self) -> list[int]:
        """Gets the album rating of each track in the list.

        :return: A list of track album ratings
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumRating"))

    def album_rating_kind(self) -> list[XAMediaApplication.RatingKind]:
        """Gets the album rating kind of each track in the list.

        :return: A list of track album rating kinds
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("albumRatingKind")
        return [XAMediaApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def bit_rate(self) -> list[int]:
        """Gets the bit rate of each track in the list.

        :return: A list of track bit rates
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bitRate"))

    def bookmark(self) -> list[float]:
        """Gets the bookmark time of each track in the list.

        :return: A list of track bookmark times
        :rtype: list[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bookmark"))

    def bookmarkable(self) -> list[bool]:
        """Gets the bookmarkable status of each track in the list.

        :return: A list of track bookmarkable statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bookmarkable"))

    def category(self) -> list[str]:
        """Gets the category of each track in the list.

        :return: A list of track categories
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("category"))

    def comment(self) -> list[str]:
        """Gets the comment of each track in the list.

        :return: A list of track comments
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def database_id(self) -> list[int]:
        """Gets the database ID of each track in the list.

        :return: A list of track database IDs
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("databaseID"))

    def date_added(self) -> list[datetime]:
        """Gets the date added of each track in the list.

        :return: A list of track dates added
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dateAdded"))

    def object_description(self) -> list[str]:
        """Gets the description of each track in the list.

        :return: A list of track descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def disc_count(self) -> list[int]:
        """Gets the disc count of each track in the list.

        :return: A list of track disc counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discCount"))

    def disc_number(self) -> list[int]:
        """Gets the disc number of each track in the list.

        :return: A list of track disc numbers
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discNumber"))

    def downloader_apple_id(self) -> list[str]:
        """Gets the downloader Apple ID of each track in the list.

        :return: A list of track downloader Apple IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderAppleID"))

    def downloader_name(self) -> list[str]:
        """Gets the downloader name of each track in the list.

        :return: A list of track downloader names
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("downloaderName"))

    def duration(self) -> list[float]:
        """Gets the duration of each track in the list.

        :return: A list of track durations
        :rtype: list[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duration"))

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each track in the list.

        :return: A list of track enabled statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def episode_id(self) -> list[str]:
        """Gets the episode ID of each track in the list.

        :return: A list of track episode IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("episodeID"))

    def episode_number(self) -> list[int]:
        """Gets the episode number of each track in the list.

        :return: A list of track episode numbers
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("episodeNumber"))

    def finish(self) -> list[float]:
        """Gets the stop time of each track in the list.

        :return: A list of track stop times
        :rtype: list[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("finish"))

    def genre(self) -> list[str]:
        """Gets the genre of each track in the list.

        :return: A list of track genres
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("genre"))

    def grouping(self) -> list[str]:
        """Gets the grouping of each track in the list.

        :return: A list of track groupings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("grouping"))

    def kind(self) -> list[str]:
        """Gets the kind of each track in the list.

        :return: A list of track kinds
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def long_description(self) -> list[str]:
        """Gets the long description of each track in the list.

        :return: A list of track long descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("longDescription"))

    def media_kind(self) -> list[XAMediaApplication.MediaKind]:
        """Gets the media kind of each track in the list.

        :return: A list of track media kinds
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("mediaKind")
        return [XAMediaApplication.MediaKind(XABase.OSType(x.stringValue())) for x in ls]

    def modification_date(self) -> list[datetime]:
        """Gets the modification date of each track in the list.

        :return: A list of track modification dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def played_count(self) -> list[int]:
        """Gets the played count of each track in the list.

        :return: A list of track played counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("playedCount"))

    def played_date(self) -> list[datetime]:
        """Gets the played date of each track in the list.

        :return: A list of track played dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("playedDate"))

    def purchaser_apple_id(self) -> list[str]:
        """Gets the purchaser Apple ID of each track in the list.

        :return: A list of track purchaser Apple IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserAppleID"))

    def purchaser_name(self) -> list[str]:
        """Gets the purchaser name of each track in the list.

        :return: A list of track purchaser names
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("purchaserName"))

    def rating(self) -> list[int]:
        """Gets the rating of each track in the list.

        :return: A list of track ratings
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rating"))

    def rating_kind(self) -> list[XAMediaApplication.RatingKind]:
        """Gets the rating kind of each track in the list.

        :return: A list of track rating kinds
        :rtype: list[XAMediaApplication.RatingKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("ratingKind")
        return [XAMediaApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def release_date(self) -> list[datetime]:
        """Gets the release date of each track in the list.

        :return: A list of track release dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("releaseDate"))

    def sample_rate(self) -> list[int]:
        """Gets the sample rate of each track in the list.

        :return: A list of track sample rates
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sampleRate"))

    def season_number(self) -> list[int]:
        """Gets the season number of each track in the list.

        :return: A list of track season numbers
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("seasonNumber"))

    def skipped_count(self) -> list[int]:
        """Gets the skipped count of each track in the list.

        :return: A list of track skipped count
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("skippedCount"))

    def skipped_date(self) -> list[datetime]:
        """Gets the skipped date of each track in the list.

        :return: A list of track skipped dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("skippedDate"))

    def show(self) -> list[str]:
        """Gets the show of each track in the list.

        :return: A list of track shows
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("show"))

    def sort_album(self) -> list[str]:
        """Gets the album sort string of each track in the list.

        :return: A list of track album sort strings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortAlbum"))

    def sort_name(self) -> list[str]:
        """Gets the name sort string of each track in the list.

        :return: A list of track name sort strings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortName"))

    def sort_show(self) -> list[str]:
        """Gets the show sort strings of each track in the list.

        :return: A list of track show sort strings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortShow"))

    def size(self) -> list[int]:
        """Gets the size of each track in the list.

        :return: A list of track sizes
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def start(self) -> list[float]:
        """Gets the start time of each track in the list.

        :return: A list of track start times
        :rtype: list[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("start"))

    def time(self) -> list[str]:
        """Gets the time string of each track in the list.

        :return: A list of track time strings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("time"))

    def track_count(self) -> list[int]:
        """Gets the track count of each track in the list.

        :return: A list of track counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("trackCount"))

    def track_number(self) -> list[int]:
        """Gets the track number of each track in the list.

        :return: A list of track numbers
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("trackNumber"))

    def unplayed(self) -> list[bool]:
        """Gets the unplayed status of each track in the list.

        :return: A list of track unplayed statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("unplayed"))

    def volume_adjustment(self) -> list[int]:
        """Gets the volume adjustment of each track in the list.

        :return: A list of track volume adjustments
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("volumeAdjustment"))

    def year(self) -> list[int]:
        """Gets the year of each track in the list.

        :return: A list of track years
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("year"))

    def by_album(self, album: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose album matches the given album, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("album", album)

    def by_album_rating(self, album_rating: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose album rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumRating", album_rating)

    def by_album_rating_kind(self, album_rating_kind: XAMediaApplication.RatingKind) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose album rating kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("albumRatingKind", album_rating_kind.value)

    def by_bit_rate(self, bit_rate: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose bit rate matches the given bit rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bitRate", bit_rate)

    def by_bookmark(self, bookmark: float) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose bookmark matches the given bookmark, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmark", bookmark)

    def by_bookmarkable(self, bookmarkable: bool) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose bookmarkable status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmarkable", bookmarkable)

    def by_category(self, category: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose category matches the given category, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose comment matches the given comment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("comment", comment)

    def by_database_id(self, database_id: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose database ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("databaseID", database_id)

    def by_date_added(self, date_added: datetime) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose date added matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("dateAdded", date_added)

    def by_object_description(self, object_description: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose description matches the given description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_disc_count(self, disc_count: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose disc count matches the given disc count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose disc number matches the given disc number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discNumber", disc_number)

    def by_downloader_apple_id(self, downloader_apple_id: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose downloader Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderAppleID", downloader_apple_id)

    def by_downloader_name(self, downloader_name: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose downloader name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderName", downloader_name)

    def by_duration(self, duration: float) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose duration matches the given duration, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_enabled(self, enabled: bool) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose enabled status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("enabled", enabled)

    def by_episode_id(self, episode_id: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose episode ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeID", episode_id)

    def by_episode_number(self, episode_number: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose episode number matches the given episode number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeNumber", episode_number)

    def by_finish(self, finish: float) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose stop time matches the given stop time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("finish", finish)

    def by_genre(self, genre: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose genre matches the given genre, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("genre", genre)

    def by_grouping(self, grouping: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose grouping matches the given grouping, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("grouping", grouping)

    def by_kind(self, kind: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_long_description(self, long_description: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose long description matches the given long description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("longDescription", long_description)

    def by_media_kind(self, media_kind: XAMediaApplication.MediaKind) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose media kind matches the given media kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("mediaKind", media_kind.value)

    def by_modification_date(self, modification_date: datetime) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose modification date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("modificationDate", modification_date)

    def by_played_count(self, played_count: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose played count matches the given played count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedCount", played_count)

    def by_played_date(self, played_date: datetime) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose last played date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedDate", played_date)

    def by_purchaser_apple_id(self, purchaser_apple_id: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose purchaser Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserAppleID", purchaser_apple_id)

    def by_purchaser_name(self, purchaser_name: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose purchaser name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserName", purchaser_name)

    def by_rating(self, rating: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rating", rating)

    def by_rating_kind(self, rating_kind: XAMediaApplication.RatingKind) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose rating kind matches the given rating kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("ratingKind", rating_kind.value)

    def by_release_date(self, release_date: datetime) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose release date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("releaseDate", release_date)

    def by_sample_rate(self, sample_rate: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose sample rate matches the given rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sampleRate", sample_rate)

    def by_season_number(self, season_number: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose season number matches the given season number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("seasonNumber", season_number)

    def by_skipped_count(self, skipped_count: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose skipped count matches the given skipped count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedCount", skipped_count)

    def by_skipped_date(self, skipped_date: datetime) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose last skipped date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedDate", skipped_date)

    def by_show(self, show: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose show matches the given show, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("show", show)

    def by_sort_album(self, sort_album: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose album sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortAlbum", sort_album)

    def by_sort_name(self, sort_name: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose name sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortName", sort_name)

    def by_sort_show(self, sort_show: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose show sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortShow", sort_show)

    def by_size(self, size: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose size matches the given size, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_start(self, start: float) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose start time matches the given start time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("start", start)

    def by_time(self, time: str) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose time string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_track_count(self, track_count: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose track count matches the given track count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackCount", track_count)

    def by_track_number(self, track_number: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose track number matches the given track number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackNumber", track_number)

    def by_unplayed(self, unplayed: bool) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose unplayed status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("unplayed", unplayed)

    def by_volume_adjustment(self, volume_adjustment: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose volume adjustment matches the given volume adjustment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("volumeAdjustment", volume_adjustment)

    def by_year(self, year: int) -> Union['XAMediaTrack', None]:
        """Retrieves the first track whose year matches the given year, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMediaTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("year", year)

class XAMediaTrack(XAMediaItem):
    """A class for managing and interacting with tracks in media apps.

    .. seealso:: :class:`XAMediaSharedTrack`, :class:`XAMediaFileTrack`, :class:`XAMediaRemoteURLTrack`

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
        self.disc_count: int #: The number of discs in the source album
        self.disc_number: int #: The index of the disc containing the track
        self.downloader_apple_id: str #: The Apple ID of the person who downloaded the track
        self.downloader_name: str #: The full name of the person who downloaded the track
        self.duration: float #: Length of the track in seconds
        self.enabled: bool #: Whether the track is able to be played
        self.episode_id: str #: A unique ID for the episode of the track
        self.episode_number: int #: The episode number of the track
        self.finish: float #: The time in seconds from the start at which the track stops playing.
        self.genre: str #: The music/audio genre category of the track.
        self.grouping: str #: The current section/chapter/movement of the track
        self.kind: str #: A text description of the track
        self.long_description: str #: A long description for the track
        self.media_kind: XAMediaApplication.MediaKind #: A description of the track's media type
        self.modification_date: datetime #: The last modification date of the track's content
        self.played_count: int #: The number of the times the track has been played
        self.played_date: datetime #: The date the track was last played
        self.purchaser_apple_id: str #: The Apple ID of the person who bought the track
        self.purchaser_name: str #: The full name of the person who bought the track
        self.rating: int #: The rating of the track from 0 to 100
        self.rating_kind: XAMediaApplication.RatingKind #: Whether the rating is user-provided or computed
        self.release_date: datetime #: The date the track was released
        self.sample_rate: int #: The sample rate of the track in Hz
        self.season_number: int #: The number of the season the track belongs to
        self.skipped_count: int #: The number of times the track has been skipped
        self.skipped_date: datetime #: The date the track was last skipped
        self.show: str #: The name of the show the track belongs to
        self.sort_album: str #: The string used for this track when sorting by album
        self.sort_name: str #: The string used for this track when sorting by name
        self.sort_show: str #: The string used for this track when sorting by show
        self.size: int #: The size of the track in bytes
        self.start: float #: The start time of the track in seconds
        self.time: str #: HH:MM:SS representation for the duration of the track
        self.track_count: int #: The number of tracks in the track's album
        self.track_number: int #: The index of the track within its album
        self.unplayed: bool #: Whether the track has been played before
        self.volume_adjustment: int #: Volume adjustment setting for this track from -100 to +100
        self.work: str #: The work name of the track

        # print("Track type", self.objectClass.data())
        # if self.objectClass.data() == _SHARED_TRACK:
        #     self.__class__ = XAMediaSharedTrack
        #     self.__init__()
        # elif self.objectClass.data() == _FILE_TRACK:
        #     self.__class__ = XAMediaFileTrack
        #     self.__init__()
        # elif self.objectClass.data() == _URL_TRACK:
        #     self.__class__ = XAMediaURLTrack
        #     self.__init__()

    @property
    def album(self) -> str:
        return self.xa_elem.album()

    @album.setter
    def album(self, album: str):
        self.set_property('album', album)

    @property
    def album_rating(self) -> int:
        return self.xa_elem.albumRating()

    @album_rating.setter
    def album_rating(self, album_rating: int):
        self.set_property('albumRating', album_rating)

    @property
    def album_rating_kind(self) -> XAMediaApplication.RatingKind:
        return XAMediaApplication.RatingKind(self.xa_elem.albumRatingKind())

    @property
    def bit_rate(self) -> int:
        return self.xa_elem.bitRate()

    @property
    def bookmark(self) -> float:
        return self.xa_elem.bookmark()

    @bookmark.setter
    def bookmark(self, bookmark: float):
        self.set_property('bookmark', bookmark)

    @property
    def bookmarkable(self) -> bool:
        return self.xa_elem.bookmarkable()

    @bookmarkable.setter
    def bookmarkable(self, bookmarkable: bool):
        self.set_property('bookmarkable', bookmarkable)

    @property
    def category(self) -> str:
        return self.xa_elem.category()

    @category.setter
    def category(self, category: str):
        self.set_property('category', category)

    @property
    def comment(self) -> str:
        return self.xa_elem.comment()

    @comment.setter
    def comment(self, comment: str):
        self.set_property('comment', comment)

    @property
    def database_id(self) -> int:
        return self.xa_elem.databaseID()

    @property
    def date_added(self) -> datetime:
        return self.xa_elem.dateAdded()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property('objectDescription', object_description)

    @property
    def disc_count(self) -> int:
        return self.xa_elem.discCount()

    @disc_count.setter
    def disc_count(self, disc_count: int):
        self.set_property('discCount', disc_count)

    @property
    def disc_number(self) -> int:
        return self.xa_elem.discNumber()

    @disc_number.setter
    def disc_number(self, disc_number: int):
        self.set_property('discNumber', disc_number)

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

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def episode_id(self) -> str:
        return self.xa_elem.episodeID()

    @episode_id.setter
    def episode_id(self, episode_id: str):
        self.set_property('episodeId', episode_id)

    @property
    def episode_number(self) -> int:
        return self.xa_elem.episodeNumber()

    @episode_number.setter
    def episode_number(self, episode_number: int):
        self.set_property('episodeNumber', episode_number)

    @property
    def finish(self) -> float:
        return self.xa_elem.finish()

    @finish.setter
    def finish(self, finish: float):
        self.set_property('finish', finish)

    @property
    def genre(self) -> str:
        return self.xa_elem.genre()

    @genre.setter
    def genre(self, genre: str):
        self.set_property('genre', genre)

    @property
    def grouping(self) -> str:
        return self.xa_elem.grouping()

    @grouping.setter
    def grouping(self, grouping: str):
        self.set_property('grouping', grouping)

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def long_description(self) -> str:
        return self.xa_elem.longDescription()

    @long_description.setter
    def long_description(self, long_description: str):
        self.set_property('longDescription', long_description)

    @property
    def media_kind(self) -> XAMediaApplication.MediaKind:
        return XAMediaApplication.MediaKind(self.xa_elem.mediaKind())

    @media_kind.setter
    def media_kind(self, media_kind: XAMediaApplication.MediaKind):
        self.set_property('mediaKind', media_kind.value)

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def played_count(self) -> int:
        return self.xa_elem.playedCount()

    @played_count.setter
    def played_count(self, played_count: int):
        self.set_property('playedCount', played_count)

    @property
    def played_date(self) -> datetime:
        return self.xa_elem.playedDate()

    @played_date.setter
    def played_date(self, played_date: datetime):
        self.set_property('playedDate', played_date)

    @property
    def purchaser_apple_id(self) -> str:
        return self.xa_elem.purchaserAppleID()

    @property
    def purchaser_name(self) -> str:
        return self.xa_elem.purchaserName()

    @property
    def rating(self) -> int:
        return self.xa_elem.rating()

    @rating.setter
    def rating(self, rating: int):
        self.set_property('rating', rating)

    @property
    def rating_kind(self) -> XAMediaApplication.RatingKind:
        return XAMediaApplication.RatingKind(self.xa_elem.ratingKind())

    @property
    def release_date(self) -> datetime:
        return self.xa_elem.releaseDate()

    @property
    def sample_rate(self) -> int:
        return self.xa_elem.sampleRate()

    @property
    def season_number(self) -> int:
        return self.xa_elem.seasonNumber()

    @season_number.setter
    def season_number(self, season_number: int):
        self.set_property('seasonNumber', season_number)

    @property
    def skipped_count(self) -> int:
        return self.xa_elem.skippedCount()

    @skipped_count.setter
    def skipped_count(self, skipped_count: int):
        self.set_property('skippedCount', skipped_count)

    @property
    def skipped_date(self) -> datetime:
        return self.xa_elem.skippedDate()

    @skipped_date.setter
    def skipped_date(self, skipped_date: datetime):
        self.set_property('skippedDate', skipped_date)

    @property
    def show(self) -> str:
        return self.xa_elem.show()

    @show.setter
    def show(self, show: str):
        self.set_property('show', show)

    @property
    def sort_album(self) -> str:
        return self.xa_elem.sortAlbum()

    @sort_album.setter
    def sort_album(self, sort_album: str):
        self.set_property('sortAlbum', sort_album)

    @property
    def sort_name(self) -> str:
        return self.xa_elem.sortName()

    @sort_name.setter
    def sort_name(self, sort_name: str):
        self.set_property('sortName', sort_name)

    @property
    def sort_show(self) -> str:
        return self.xa_elem.sortShow()

    @sort_show.setter
    def sort_show(self, sort_show: str):
        self.set_property('sortShow', sort_show)

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def start(self) -> float:
        return self.xa_elem.start()

    @start.setter
    def start(self, start: float):
        self.set_property('start', start)

    @property
    def time(self) -> str:
        return self.xa_elem.time()

    @property
    def track_count(self) -> int:
        return self.xa_elem.trackCount()

    @track_count.setter
    def track_count(self, track_count: int):
        self.set_property('trackCount', track_count)

    @property
    def track_number(self) -> int:
        return self.xa_elem.trackNumber()

    @track_number.setter
    def track_number(self, track_number: int):
        self.set_property('trackNumber', track_number)

    @property
    def unplayed(self) -> bool:
        return self.xa_elem.unplayed()

    @unplayed.setter
    def unplayed(self, unplayed: bool):
        self.set_property('unplayed', unplayed)

    @property
    def volume_adjustment(self) -> int:
        return self.xa_elem.volumeAdjustment()

    @volume_adjustment.setter
    def volume_adjustment(self, volume_adjustment: int):
        self.set_property('volumeAdjustment', volume_adjustment)

    @property
    def year(self) -> int:
        return self.xa_elem.year()

    @year.setter
    def year(self, year: int):
        self.set_property('year', year)

    def select(self) -> 'XAMediaItem':
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XAMediaTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self

    def play(self) -> 'XAMediaItem':
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XAMediaItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self

    def artworks(self, filter: Union[dict, None] = None) -> 'XAMediaArtworkList':
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMediaArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.artworks(), XAMediaArtworkList, filter)




class XAMediaFileTrackList(XAMediaTrackList):
    """A wrapper around lists of music file tracks that employs fast enumeration techniques.

    All properties of music file tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaFileTrack)

    def location(self) -> list[XABase.XAURL]:
        """Gets the location of each track in the list.

        :return: A list of track locations
        :rtype: list[XABase.XAURL]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union['XAMediaFileTrack', None]:
        """Retrieves the file track whose location matches the given location, if one exists.

        :return: The desired file track, if it is found
        :rtype: Union[XAMediaFileTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("location", location.xa_elem)

class XAMediaFileTrack(XAMediaTrack):
    """A file track in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.location: XABase.XAURL #: The location of the file represented by the track

    @property
    def location(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.location())

    @location.setter
    def location(self, location: Union[XABase.XAPath, str]):
        if isinstance(location, str):
            location = XABase.XAPath(location)
        self.set_property('location', location.xa_elem)




class XAMediaSharedTrackList(XAMediaTrackList):
    """A wrapper around lists of music shared tracks that employs fast enumeration techniques.

    All properties of music shared tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaSharedTrack)

class XAMediaSharedTrack(XAMediaTrack):
    """A shared track in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMediaURLTrackList(XAMediaTrackList):
    """A wrapper around lists of music URL tracks that employs fast enumeration techniques.

    All properties of music URL tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaURLTrack)

    def address(self) -> list[str]:
        """Gets the address of each track in the list.

        :return: A list of track addresses
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def by_address(self, address: str) -> Union['XAMediaURLTrack', None]:
        """Retrieves the URL track whose address matches the given address, if one exists.

        :return: The desired URL track, if it is found
        :rtype: Union[XAMediaURLTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("address", address)

class XAMediaURLTrack(XAMediaTrack):
    """A URL track in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: str #: The URL for the track

    @property
    def address(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.address())

    @address.setter
    def address(self, address: Union[XABase.XAURL, str]):
        if isinstance(address, str):
            address = XABase.XAURL(address)
        self.set_property('address', address.xa_elem)




class XAMediaUserPlaylistList(XAMediaPlaylistList):
    """A wrapper around lists of music user playlists that employs fast enumeration techniques.

    All properties of music user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaUserPlaylist)

    def shared(self) -> list[bool]:
        """Gets the shared status of each user playlist in the list.

        :return: A list of playlist shared status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shared"))

    def smart(self) -> list[bool]:
        """Gets the smart status of each user playlist in the list.

        :return: A list of playlist smart status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("smart"))

    def by_shared(self, shared: bool) -> Union['XAMediaUserPlaylist', None]:
        """Retrieves the user playlist whose shared status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XAMediaUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("shared", shared)

    def by_smart(self, smart: bool) -> Union['XAMediaUserPlaylist', None]:
        """Retrieves the user playlist whose smart status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XAMediaUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("smart", smart)

class XAMediaUserPlaylist(XAMediaPlaylist):
    """A user-created playlist in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.shared: bool #: Whether the playlist is shared
        self.smart: bool #: Whether the playlist is a smart playlist

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @shared.setter
    def shared(self, shared: bool):
        self.set_property('shared', shared)

    @property
    def smart(self) -> bool:
        return self.xa_elem.smart()

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMediaFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), XAMediaFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMediaURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMediaURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XAMediaSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMediaSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sharedTracks(), XAMediaSharedTrackList, filter)




class XAMediaFolderPlaylistList(XAMediaUserPlaylistList):
    """A wrapper around lists of music folder playlists that employs fast enumeration techniques.

    All properties of music folder playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaFolderPlaylist)

class XAMediaFolderPlaylist(XAMediaUserPlaylist):
    """A folder playlist in media apps.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMediaWindowList(XAMediaItemList):
    """A wrapper around lists of windows that employs fast enumeration techniques.

    All properties of windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMediaWindow
        super().__init__(properties, filter, obj_class)

    def bounds(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Gets the bounds of each window in the list.

        :return: A list of window bounds
        :rtype: list[tuple[tuple[int, int], tuple[int, int]]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def closeable(self) -> list[bool]:
        """Gets the closeable status of each window in the list.

        :return: A list of window closeable statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("closeable"))

    def collapseable(self) -> list[bool]:
        """Gets the collapseable status of each window in the list.

        :return: A list of window collapseable statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("collapseable"))

    def collapsed(self) -> list[bool]:
        """Gets the collapsed status of each window in the list.

        :return: A list of window collapsed statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed"))

    def full_screen(self) -> list[bool]:
        """Gets the full screen status of each window in the list.

        :return: A list of window full screen statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fullScreen"))

    def position(self) -> list[tuple[int, int]]:
        """Gets the position of each window in the list.

        :return: A list of window positions
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def resizable(self) -> list[bool]:
        """Gets the resizable status of each window in the list.

        :return: A list of window resizable statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("resizable"))

    def visible(self) -> list[bool]:
        """Gets the visible status of each window in the list.

        :return: A list of window visible statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def zoomable(self) -> list[bool]:
        """Gets the zoomable status of each window in the list.

        :return: A list of window zoomable statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable"))

    def zoomed(self) -> list[bool]:
        """Gets the zoomed status of each window in the list.

        :return: A list of window zoomed statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed"))

    def by_bounds(self, bounds: tuple[tuple[int, int], tuple[int, int]]) -> Union['XAMediaWindow', None]:
        """Retrieves the window whose bounds matches the given bounds, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("bounds", bounds)

    def by_closeable(self, closeable: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose closeable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("closeable", closeable)

    def by_collapseable(self, collapseable: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose collapseable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapseable", collapseable)

    def by_collapsed(self, collapsed: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose collapsed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapsed", collapsed)

    def by_full_screen(self, full_screen: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose full screen status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fullScreen", full_screen)

    def by_position(self, position: tuple[int, int]) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose position matches the given position, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("position", position)

    def by_resizable(self, resizable: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose resizable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose visible status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose zoomable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union['XAMediaWindow', None]:
        """Retrieves the first window whose zoomed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMediaWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomed", zoomed)

class XAMediaWindow(XABase.XAWindow, XAMediaItem):
    """A windows of media apps.

    .. seealso:: :class:`XAMediaBrowserWindow`, :class:`XAMediaPlaylistWindow`, :class:`XAMediaVideoWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle for the window
        self.closeable: bool #: Whether the window has a close button
        self.collapseable: bool #: Whether the window can be minimized
        self.collapsed: bool #: Whether the window is currently minimized
        self.full_screen: bool #: Whether the window is currently full screen
        self.position: tuple[int, int] #: The upper left position of the window
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
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
    def collapseable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def collapsed(self) -> bool:
        return self.xa_elem.miniaturized()

    @collapsed.setter
    def collapsed(self, collapsed: bool):
        self.set_property('collapsed', collapsed)

    @property
    def full_screen(self) -> bool:
        return self.xa_elem.fullScreen()

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.set_property('fullScreen', full_screen)

    @property
    def position(self) -> tuple[int, int]:
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property('visible', visible)

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property('zoomed', zoomed)




class XAMediaBrowserWindowList(XAMediaWindowList):
    """A wrapper around lists of music browser windows that employs fast enumeration techniques.

    All properties of music browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaBrowserWindow)

    def selection(self) -> XAMediaTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XAMediaTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAMediaTrackList)

    def view(self) -> XAMediaPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XAMediaPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XAMediaPlaylistList)

    def by_selection(self, selection: XAMediaTrackList) -> Union['XAMediaPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMediaPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMediaPlaylist) -> Union['XAMediaPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMediaPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XAMediaBrowserWindow(XAMediaWindow):
    """A browser window of media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XAMediaTrackList #: The selected tracks
        self.view: XAMediaPlaylist #: The playlist currently displayed in the window

    @property
    def selection(self) -> XAMediaTrackList:
        return self._new_element(self.xa_elem.selection(), XAMediaTrackList)

    @property
    def view(self) -> XAMediaPlaylist:
        return self._new_element(self.xa_elem.view(), XAMediaPlaylist)



class XAMediaPlaylistWindowList(XAMediaWindowList):
    """A wrapper around lists of music playlist windows that employs fast enumeration techniques.

    All properties of music playlist windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaPlaylistWindow)

    def selection(self) -> XAMediaTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XAMediaTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAMediaTrackList)

    def view(self) -> XAMediaPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XAMediaPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XAMediaPlaylistList)

    def by_selection(self, selection: XAMediaTrackList) -> Union['XAMediaPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMediaPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMediaPlaylist) -> Union['XAMediaPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMediaPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XAMediaPlaylistWindow(XAMediaWindow):
    """A playlist window in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XAMediaTrackList #: The selected tracks
        self.view: XAMediaPlaylist #: The playlist currently displayed in the window

    @property
    def selection(self) -> XAMediaTrackList:
        return self._new_element(self.xa_elem.selection(), XAMediaTrackList)

    @property
    def view(self) -> XAMediaPlaylist:
        return self._new_element(self.xa_elem.view(), XAMediaPlaylist)




class XAMediaVideoWindowList(XAMediaWindowList):
    """A wrapper around lists of music video windows that employs fast enumeration techniques.

    All properties of music video windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMediaVideoWindow)

class XAMediaVideoWindow(XAMediaWindow):
    """A video window in media apps.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
