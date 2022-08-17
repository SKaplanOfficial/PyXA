""".. versionadded:: 0.0.1

Control the macOS Music application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import List, Literal, Tuple, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath

class XAMusicApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XAMusicWindow`, class:`XAMusicSource`, :class:`XAMusicPlaylist`, :class:`XAMusicTrack`

    .. versionadded:: 0.0.1
    """
    class PrintSetting(Enum):
        """Options to use when printing.
        """
        STANDARD_ERROR_HANDLING = XABase.OSType('lwst') #: Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = XABase.OSType('lwdt') #: Print a detailed report of PostScript errors
        TRACK_LISTING           = XABase.OSType('kTrk') #: A basic listing of tracks within a playlist
        ALBUM_LISTING           = XABase.OSType('kAlb') #: A listing of a playlist grouped by album
        CD_INSERT               = XABase.OSType('kCDi') #: A printout of the playlist for jewel case inserts

    class PlayerState(Enum):
        """States of the music player.
        """
        STOPPED         = XABase.OSType('kPSS') #: The player is stopped
        PLAYING         = XABase.OSType('kPSP') #: The player is playing
        PAUSED          = XABase.OSType('kPSp') #: The player is paused
        FAST_FORWARDING = XABase.OSType('kPSF') #: The player is fast forwarding
        REWINDING       = XABase.OSType('kPSR') #: The player is rewinding

    class RepeatMode(Enum):
        """Options for how to repeat playback.
        """
        OFF = XABase.OSType('kRpO') #: Playback does not repeat
        ONE = XABase.OSType('kRp1') #: The currently playing media item will be repeated
        ALL = XABase.OSType('kAll') #: All media items in the current playlist will be repeated

    class ShuffleMode(Enum):
        """Options for how to shuffle playback.
        """
        SONGS       = XABase.OSType('kShS') #: Shuffle by song
        ALBUMS      = XABase.OSType('kShA') #: Shuffle by album
        GROUPINGS   = XABase.OSType('kShG') #: Shuffle by grouping

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

    class DeviceKind(Enum):
        """Kinds of devices.
        """
        COMPUTER            = XABase.OSType('kAPC') #: A computer device
        AIRPORT_EXPRESS     = XABase.OSType('kAPX') #: An airport express device
        APPLE_TV            = XABase.OSType('kAPT') #: An Apple TV device
        AIRPLAY_DEVICE      = XABase.OSType('kAPO') #: An AirPlay-enabled device
        BLUETOOTH_DEVICE    = XABase.OSType('kAPB') #: A BlueTooth-enabled device
        HOMEPOD             = XABase.OSType('kAPH') #: A HomePod device
        UNKNOWN             = XABase.OSType('kAPU') #: An unknown device

    class iCloudStatus(Enum):
        """iCloud statuses of media items.
        """
        UNKNOWN             = XABase.OSType('kUnk') #: Unknown cloud status
        PURCHASED           = XABase.OSType('kPur') #: A purchased media item
        MATCHED             = XABase.OSType('kMat') #: A matched media item
        UPLOADED            = XABase.OSType('kUpl') #: An unloaded media item
        INELIGIBLE          = XABase.OSType('kRej') #: A media item ineligible for listening
        REMOVED             = XABase.OSType('kRem') #: A removed media item
        ERROR               = XABase.OSType('kErr') #: A media item unavailable due to an error
        DUPLICATE           = XABase.OSType('kDup') #: A duplicate media item
        SUBSCRIPTION        = XABase.OSType('kSub') #: A media item obtained via a subscription to Apple Music
        NO_LONGER_AVAILABLE = XABase.OSType('kRev') #: A media item unavailable due to expiration
        NOT_UPLOADED        = XABase.OSType('kUpP') #: A non-uploaded media item

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAMusicWindow

        self.airplay_enabled: bool #: Whether AirPlay is currently ennabled
        self.converting: bool #: Whether a track is currently being converted
        self.current_airplay_devices: XAMusicAirPlayDeviceList #: The currently selected AirPlay devices
        self.current_encoder: XAMusicEncoder #: The currently selected encoder
        self.current_eq_preset: XAMusicEQPreset #: The currently selected equalizer preset
        self.current_playlist: XAMusicPlaylist #: The playlist containing the currently targeted track
        self.current_stream_title: str #: The name of the current streaming track
        self.current_stream_url: str #: The URL of the current streaming 
        self.current_track: XAMusicTrack #: The currently targeted track
        self.current_visual: XAMusicVisual #: The currently selected visual plug-in
        self.eq_enabled: bool #: Whether the equalizer is enabled
        self.fixed_indexing: bool #: Whether the track indices are independent of the order of the current playlist or not
        self.frontmost: bool #: Whether the application is active or not
        self.full_screen: bool #: Whether the app is fullscreen or not
        self.name: str #: The name of the application
        self.mute: bool #: Whether sound output is muted or not
        self.player_position: float #: The time elapsed in the current track
        self.player_state: str #: Whether the player is playing, paused, stopped, fast forwarding, or rewinding
        self.selection: str #: The selected ..............
        self.shuffle_enabled: bool #: Whether songs are played in random order
        self.shuffle_mode: str #: The playback shuffle mode
        self.song_repeat: str #: The playback repeat mode
        self.sound_volume: int #: The sound output volume
        self.version: str #: The version of the application
        self.visuals_enabled: bool #: Whether visuals are currently displayed

    @property
    def airplay_enabled(self) -> bool:
        return self.xa_scel.airplayEnabled()

    @property
    def converting(self) -> bool:
        return self.xa_scel.converting()

    @property
    def current_airplay_devices(self) -> 'XAMusicAirPlayDeviceList':
        ls = self.xa_scel.currentAirPlayDevices()
        return self._new_element(ls, XAMusicAirPlayDeviceList)

    @property
    def current_encoder(self) -> 'XAMusicEncoder':
        return self._new_element(self.xa_scel.currentEncoder(), XAMusicEncoder)

    @property
    def current_eq_preset(self) -> 'XAMusicEQPreset':
        return self._new_element(self.xa_scel.currentEQPreset(), XAMusicEQPreset)

    @property
    def current_playlist(self) -> 'XAMusicPlaylist':
        return self._new_element(self.xa_scel.currentPlaylist(), XAMusicPlaylist)

    @property
    def current_stream_title(self) -> str:
        return self.xa_scel.currentStreamTitle()

    @property
    def current_stream_url(self) -> str:
        return self.xa_scel.currentStreamURL()

    @property
    def current_track(self) -> 'XAMusicTrack':
        return self._new_element(self.xa_scel.currentTrack(), XAMusicTrack)

    @property
    def current_visual(self) -> 'XAMusicVisual':
        return self._new_element(self.xa_scel.currentVisual(), XAMusicVisual)

    @property
    def eq_enabled(self) -> bool:
        return self.xa_scel.eqEnabled()

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
    def player_state(self) -> 'XAMusicApplication.PlayerState':
        return XAMusicApplication.PlayerState(self.xa_scel.playerState())

    @property
    def selection(self) -> 'XAMusicItemList':
        return self._new_element(self.xa_scel.selection().get(), XAMusicTrackList)

    @property
    def shuffle_enabled(self) -> bool:
        return self.xa_scel.shuffleEnabled()

    @property
    def shuffle_mode(self) -> 'XAMusicApplication.ShuffleMode':
        return XAMusicApplication.ShuffleMode(self.xa_scel.shuffleMode())

    @property
    def song_repeat(self) -> 'XAMusicApplication.RepeatMode':
        return XAMusicApplication.RepeatMode(self.xa_scel.songRepeat())

    @property
    def sound_volume(self) -> int:
        return self.xa_scel.soundVolume()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def visuals_enabled(self) -> bool:
        return self.xa_scel.visualsEnabled()

    def play(self, item: 'XAMusicItem' = None) -> 'XAMusicApplication':
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XAMusicItem, optional
        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playOnce_(item)
        return self

    def playpause(self) -> 'XAMusicApplication':
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> 'XAMusicApplication':
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> 'XAMusicApplication':
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> 'XAMusicApplication':
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> 'XAMusicApplication':
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> 'XAMusicApplication':
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> 'XAMusicApplication':
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> 'XAMusicApplication':
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> 'XAMusicApplication':
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> 'XAMusicApplication':
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> 'XAMusicApplication':
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def current_track(self) -> 'XAMusicTrack':
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
        return XAMusicTrack(properties)

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

    def airplay_devices(self, filter: Union[dict, None] = None) -> 'XAMusicAirPlayDeviceList':
        """Returns a list of AirPlay devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned AirPlay devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of devices
        :rtype: XAMusicAirPlayDeviceList

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Music")
        >>> print(app.airplay_devices())
        <<class 'PyXA.apps.Music.XAMusicAirPlayDeviceList'>['ExampleUser\\'s MacBook Pro']>

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.AirPlayDevices(), XAMusicAirPlayDeviceList, filter)

    def browser_windows(self, filter: Union[dict, None] = None) -> 'XAMusicBrowserWindowList':
        """Returns a list of browser windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browser windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicBrowserWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.browserWindows(), XAMusicBrowserWindowList, filter)

    def encoders(self, filter: Union[dict, None] = None) -> 'XAMusicEncoderList':
        """Returns a list of encoders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned encoders will have, or None
        :type filter: Union[dict, None]
        :return: The list of encoders
        :rtype: XAMusicEncoderList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.encoders(), XAMusicEncoderList, filter)

    def eq_presets(self, filter: Union[dict, None] = None) -> 'XAMusicEQPresetList':
        """Returns a list of EQ presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned EQ presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of presets
        :rtype: XAMusicEQPresetList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.EQPresets(), XAMusicEQPresetList, filter)

    def eq_windows(self, filter: Union[dict, None] = None) -> 'XAMusicEQWindowList':
        """Returns a list of EQ windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned EQ windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicEQWindowList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.EQWindows(), XAMusicEQWindowList, filter)

    def miniplayer_windows(self, filter: Union[dict, None] = None) -> 'XAMusicMiniplayerWindowList':
        """Returns a list of miniplayer windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned miniplayer windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicMiniplayWindowList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.miniplayerWindows(), XAMusicMiniplayerWindowList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XAMusicPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMusicPlaylistList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlists(), XAMusicPlaylistList, filter)

    def playlist_windows(self, filter: Union[dict, None] = None) -> 'XAMusicPlaylistWindowList':
        """Returns a list of playlist windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicPlaylistWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlistWindows(), XAMusicPlaylistWindowList, filter)

    def sources(self, filter: Union[dict, None] = None) -> 'XAMusicSourceList':
        """Returns a list of sources, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sources will have, or None
        :type filter: Union[dict, None]
        :return: The list of sources
        :rtype: XAMusicSourceList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.sources(), XAMusicSourceList, filter)

    def tracks(self, filter: Union[dict, None] = None) -> 'XAMusicTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMusicTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XAMusicTrackList, filter)

    def video_windows(self, filter: Union[dict, None] = None) -> 'XAMusicVideoWindowList':
        """Returns a list of video windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicVideoWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.videoWindows(), XAMusicVideoWindowList, filter)

    def visuals(self, filter: Union[dict, None] = None) -> 'XAMusicVisualList':
        """Returns a list of visuals, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned visuals will have, or None
        :type filter: Union[dict, None]
        :return: The list of visuals
        :rtype: XAMusicVisualList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sources(), XAMusicVisualList, filter)




class XAMusicItemList(XABase.XAList):
    """A wrapper around lists of music items that employs fast enumeration techniques.

    All properties of music items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicItem
        super().__init__(properties, obj_class, filter)

    def container(self) -> List[XABase.XAObject]:
        """Gets the container of each music item in the list.

        :return: A list of music item containers
        :rtype: List[XABase.XAObject]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XABase.XAList)

    def id(self) -> List[int]:
        """Gets the ID of each music item in the list.

        :return: A list of music item IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def index(self) -> List[int]:
        """Gets the index of each music item in the list.

        :return: A list of music item indices
        :rtype: List[nt]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def name(self) -> List[str]:
        """Gets the name of each music item in the list.

        :return: A list of music item names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def persistent_id(self) -> List[str]:
        """Gets the persistent ID of each music item in the list.

        :return: A list of music item persistent IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("persistentID"))
    
    def properties(self) -> List[dict]:
        """Gets the properties of each music item in the list.

        :return: A list of music item properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def by_container(self, container: XABase.XAObject) -> Union['XAMusicItem', None]:
        """Retrieves the first music item whose container matches the given container object, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("container", container.xa_elem)

    def by_id(self, id: int) -> Union['XAMusicItem', None]:
        """Retrieves the music item whose ID matches the given ID, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union['XAMusicItem', None]:
        """Retrieves the music item whose index matches the given index, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union['XAMusicItem', None]:
        """Retrieves the music item whose name matches the given name, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_persistent_id(self, persistent_id: str) -> Union['XAMusicItem', None]:
        """Retrieves the music item whose persistent ID matches the given ID, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("persistentID", persistent_id)

    def by_properties(self, properties: dict) -> Union['XAMusicItem', None]:
        """Retrieves the music item whose properties dictionary matches the given dictionary, if one exists.

        :return: The desired music item, if it is found
        :rtype: Union[XAMusicItem, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("properties", properties)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each music item in the list.

        When a list of music items is copied to the clipboard, the name of each item is added to the clipboard.

        :return: A list of track names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMusicItem(XABase.XAObject):
    """A generic class with methods common to the various playable media classes in TV.app.

    .. seealso:: :class:`XAMusicSource`, :class:`XAMusicPlaylist`, :class:`XAMusicTrack`

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

    def download(self) -> 'XAMusicItem':
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XAMusicItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> 'XAMusicItem':
        """Reveals the item in the TV.app window.

        :return: A reference to the TV item object.
        :rtype: XAMusicItem

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



class XAMusicAirPlayDeviceList(XAMusicItemList):
    """A wrapper around lists of AirPlay devices that employs fast enumeration techniques.

    All properties of AirPlay devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAirPlayDevice)

    def active(self) -> List[bool]:
        """Gets the active status of each device in the list.

        :return: A list of AirPlay device active statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("active"))

    def available(self) -> List[bool]:
        """Gets the available status of each device in the list.

        :return: A list of AirPlay device available statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("available"))

    def kind(self) -> List[XAMusicApplication.DeviceKind]:
        """Gets the kind of each device in the list.

        :return: A list of AirPlay device kinds
        :rtype: List[XAMusicApplication.DeviceKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("kind")
        return [XAMusicApplication.DeviceKind(XABase.OSType(x.stringValue())) for x in ls]

    def network_address(self) -> List[str]:
        """Gets the network address of each device in the list.

        :return: A list of AirPlay device MAC addresses
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("networkAddress"))

    def protected(self) -> List[bool]:
        """Gets the protected status of each device in the list.

        :return: A list of AirPlay device protected statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("protected"))

    def selected(self) -> List[bool]:
        """Gets the selected status of each device in the list.

        :return: A list of AirPlay device selected statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("selected"))

    def supports_audio(self) -> List[bool]:
        """Gets the supports audio status of each device in the list.

        :return: A list of AirPlay device supports audio statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("supportsAudio"))

    def supports_audio(self) -> List[bool]:
        """Gets the supports video status of each device in the list.

        :return: A list of AirPlay device supports video statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("supportsVideo"))

    def sound_volume(self) -> List[int]:
        """Gets the sound volume of each device in the list.

        :return: A list of AirPlay device sound volumes
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("soundVolume"))

    def by_active(self, active: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose active status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("active", active)

    def by_available(self, available: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose available status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("available", available)

    def by_kind(self, kind: XAMusicApplication.DeviceKind) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose kind matches the given kind, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("kind", kind.value)

    def by_network_address(self, network_address: str) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the AirPlay device whose MAC address matches the given MAC address, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("networkAddress", network_address)

    def by_protected(self, protected: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose protected status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("protected", protected)

    def by_selected(self, selected: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose selected status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selected", selected)

    def by_supports_audio(self, supports_audio: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose supports audio status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("supportsAudio", supports_audio)

    def by_supports_video(self, supports_video: bool) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose supports video status matches the given boolean value, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("supportsVideo", supports_video)

    def by_sound_volume(self, sound_volume: int) -> Union['XAMusicAirPlayDevice', None]:
        """Retrieves the first AirPlay device whose sound volume matches the given volume, if one exists.

        :return: The desired AirPlay device, if it is found
        :rtype: Union[XAMusicAirPlayDevice, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("soundVolume", sound_volume)

class XAMusicAirPlayDevice(XAMusicItem):
    """An AirPlay device.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties) 
        self.active: bool #: Whether the device is currently being played to
        self.available: bool #: Whether the device is currently available
        self.kind: XAMusicApplication.DeviceKind #: The kind of the device
        self.network_address: str #: The MAC address of the device
        self.protected: bool #: Whether the device is password/passcode protected
        self.selected: bool #: Whether the device is currently selected
        self.supports_audio: bool #: Whether the device supports audio playback
        self.supports_video: bool #: Whether the device supports video playback
        self.sound_volume: int #: The output volume for the device from 0 to 100

    @property
    def active(self) -> bool:
        return self.xa_elem.active()

    @property
    def available(self) -> bool:
        return self.xa_elem.available()

    @property
    def kind(self) -> XAMusicApplication.DeviceKind:
        return XAMusicApplication.DeviceKind(self.xa_elem.kind())

    @property
    def network_address(self) -> str:
        return self.xa_elem.networkAddress()

    @property
    def protected(self) -> bool:
        return self.xa_elem.protected()

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    @property
    def supports_audio(self) -> bool:
        return self.xa_elem.supportsAudio()

    @property
    def supports_video(self) -> bool:
        return self.xa_elem.supportsVideo()

    @property
    def sound_volume(self) -> int:
        return self.xa_elem.soundVolume()




class XAMusicArtworkList(XAMusicItemList):
    """A wrapper around lists of music artworks that employs fast enumeration techniques.

    All properties of music artworks can be called as methods on the wrapped list, returning a list containing each artworks's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicArtwork)

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

    def by_data(self, data: XABase.XAImage) -> Union['XAMusicArtwork', None]:
        """Retrieves the artwork whose data matches the given image, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("data", data.xa_elem)

    def by_object_description(self, object_description: str) -> Union['XAMusicArtwork', None]:
        """Retrieves the artwork whose description matches the given description, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_downloaded(self, downloaded: bool) -> Union['XAMusicArtwork', None]:
        """Retrieves the first artwork whose downloaded status matches the given boolean value, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaded", downloaded)

    def by_format(self, format: int) -> Union['XAMusicArtwork', None]:
        """Retrieves the first artwork whose format matches the format, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("format", format)

    def by_kind(self, kind: int) -> Union['XAMusicArtwork', None]:
        """Retrieves the first artwork whose kind matches the given kind, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_raw_data(self, raw_data: bytes) -> Union['XAMusicArtwork', None]:
        """Retrieves the artwork whose raw data matches the given byte data, if one exists.

        :return: The desired artwork, if it is found
        :rtype: Union[XAMusicArtwork, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rawData", raw_data)

class XAMusicArtwork(XAMusicItem):
    """An artwork in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.data: XABase.XAImage #: The data for the artwork in the form of a picture
        self.object_description: str #: The string description of the artwork
        self.downloaded: bool #: Whether the artwork was downloaded by Music.app
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




class XAMusicEncoderList(XAMusicItemList):
    """A wrapper around lists of encoders that employs fast enumeration techniques.

    All properties of encoders can be called as methods on the wrapped list, returning a list containing each encoders's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEncoder)

    def format(self) -> List[str]:
        """Gets the format of each encoder in the list.

        :return: A list of encoder desformatscriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("format"))

    def by_format(self, format: str) -> Union['XAMusicEncoder', None]:
        """Retrieves the first encoder whose format matches the given format, if one exists.

        :return: The desired encoder, if it is found
        :rtype: Union[XAMusicEncoder, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("format", format)

class XAMusicEncoder(XAMusicItem):
    """An encoder in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.format: str #: The data format created by the encoder

    @property
    def format(self) -> str:
        return self.xa_elem.format()




class XAMusicEQPresetList(XAMusicItemList):
    """A wrapper around lists of equalizer presets that employs fast enumeration techniques.

    All properties of equalizer presets can be called as methods on the wrapped list, returning a list containing each preset's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEQPreset)

    def band1(self) -> List[float]:
        """Gets the band1 of each preset in the list.

        :return: A list of preset band1 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band1"))

    def band2(self) -> List[float]:
        """Gets the band2 of each preset in the list.

        :return: A list of preset band2 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band2"))

    def band3(self) -> List[float]:
        """Gets the band3 of each preset in the list.

        :return: A list of preset band3 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band3"))

    def band4(self) -> List[float]:
        """Gets the band4 of each preset in the list.

        :return: A list of preset band4 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band4"))

    def band5(self) -> List[float]:
        """Gets the band5 of each preset in the list.

        :return: A list of preset band5 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band5"))

    def band6(self) -> List[float]:
        """Gets the band6 of each preset in the list.

        :return: A list of preset band6 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band6"))

    def band7(self) -> List[float]:
        """Gets the band7 of each preset in the list.

        :return: A list of preset band7 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band7"))

    def band8(self) -> List[float]:
        """Gets the band8 of each preset in the list.

        :return: A list of preset band8 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band8"))

    def band9(self) -> List[float]:
        """Gets the band9 of each preset in the list.

        :return: A list of preset band9 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band9"))

    def band10(self) -> List[float]:
        """Gets the band10 of each preset in the list.

        :return: A list of preset band10 levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("band10"))

    def modifiable(self) -> List[float]:
        """Gets the modifiable status of each preset in the list.

        :return: A list of preset modifiable statuses
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modifiable"))

    def preamp(self) -> List[float]:
        """Gets the preamp level of each preset in the list.

        :return: A list of preset preamp levels
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("preamp"))

    def update_tracks(self) -> List[float]:
        """Gets the update track status of each preset in the list.

        :return: A list of preset update track statuses
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("updateTracks"))

    def by_band1(self, band1: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band1 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band1", band1)

    def by_band2(self, band2: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band2 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band2", band2)

    def by_band3(self, band3: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band3 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band3", band3)
    
    def by_band4(self, band4: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band4 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band4", band4)

    def by_band5(self, band5: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band5 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band5", band5)

    def by_band6(self, band6: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band6 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band6", band6)

    def by_band7(self, band7: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band7 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band7", band7)

    def by_band8(self, band8: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band8 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band8", band8)

    def by_band9(self, band9: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band9 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band9", band9)

    def by_band10(self, band10: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose band10 level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("band10", band10)

    def by_modifiable(self, modifiable: bool) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose modifiable status level matches the given boolean value, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("modifiable", modifiable)

    def by_preamp(self, preamp: float) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose preamp level matches the given level, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("preamp", preamp)

    def by_update_tracks(self, update_tracks: bool) -> Union['XAMusicEQPreset', None]:
        """Retrieves the first EQ preset whose update tracks status level matches the given boolean value, if one exists.

        :return: The desired EQ preset, if it is found
        :rtype: Union[XAMusicEQPreset, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("updateTracks", update_tracks)

class XAMusicEQPreset(XAMusicItem):
    """An equalizer preset in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.band1: float #: The 32 Hz band level (-12.0 dB to +12.0 dB)
        self.band2: float #: The 64 Hz band level (-12.0 dB to +12.0 dB)
        self.band3: float #: The 125 HZ band level (-12.0 dB to +12.0 dB)
        self.band4: float #: The 250 Hz band level (-12.0 dB to +12.0 dB)
        self.band5: float #: The 500 Hz band level (-12.0 dB to +12.0 dB)
        self.band6: float #: The 1 kHz band level (-12.0 dB to +12.0 dB)
        self.band7: float #: The 2 kHz band level (-12.0 dB to +12.0 dB)
        self.band8: float #: The 4 kHz band level (-12.0 dB to +12.0 dB)
        self.band9: float #: The 8 kHz band level (-12.0 dB to +12.0 dB)
        self.band10: float #: The 16 kHz band level (-12.0 dB to +12.0 dB)
        self.modifiable: bool #: Whether the preset can be modified
        self.preamp: float #: The equalizer preamp level (-12.0 dB to +12.0 dB)
        self.update_tracks: bool #: Whether tracks using the preset are updated when the preset is renamed or deleted

    @property
    def band1(self) -> float:
        return self.xa_elem.band1()

    @property
    def band2(self) -> float:
        return self.xa_elem.band2()

    @property
    def band3(self) -> float:
        return self.xa_elem.band3()

    @property
    def band4(self) -> float:
        return self.xa_elem.band4()

    @property
    def band5(self) -> float:
        return self.xa_elem.band5()

    @property
    def band6(self) -> float:
        return self.xa_elem.band6()

    @property
    def band7(self) -> float:
        return self.xa_elem.band7()

    @property
    def band8(self) -> float:
        return self.xa_elem.band8()

    @property
    def band9(self) -> float:
        return self.xa_elem.band9()

    @property
    def band10(self) -> float:
        return self.xa_elem.band10()

    @property
    def modifiable(self) -> bool:
        return self.xa_elem.modifiable()

    @property
    def preamp(self) -> float:
        return self.xa_elem.preamp()

    @property
    def update_tracks(self) -> bool:
        return self.xa_elem.updateTracks()




class XAMusicPlaylistList(XAMusicItemList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicPlaylist
        super().__init__(properties, filter, obj_class)

    def object_description(self) -> List[str]:
        """Gets the description of each playlist in the list.

        :return: A list of playlist descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def disliked(self) -> List[bool]:
        """Gets the dislike status of each playlist in the list.

        :return: A list of playlist dislike statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("disliked"))

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

    def loved(self) -> List[bool]:
        """Gets the loved status of each playlist in the list.

        :return: A list of playlist loved statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("loved"))

    def parent(self) -> 'XAMusicPlaylistList':
        """Gets the parent playlist of each playlist in the list.

        :return: A list of playlist parent playlists
        :rtype: XAMusicPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAMusicPlaylistList)

    def size(self) -> List[int]:
        """Gets the size of each playlist in the list.

        :return: A list of playlist sizes
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def special_kind(self) -> List[XAMusicApplication.PlaylistKind]:
        """Gets the special kind of each playlist in the list.

        :return: A list of playlist kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("specialKind")
        return [XAMusicApplication.PlaylistKind(XABase.OSType(x.stringValue())) for x in ls]

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

    def by_object_description(self, object_description: str) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose closeable description matches the given description, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_disliked(self, disliked: bool) -> Union['XAMusicPlaylist', None]:
        """Retrieves the first playlist whose closeable disliked status matches the given boolean value, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("disliked", disliked)

    def by_duration(self, duration: int) -> Union['XAMusicPlaylist', None]:
        """Retrieves the first playlist whose duration matches the given duration, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_name(self, name: str) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose name matches the given name, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_loved(self, loved: bool) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose loved status matches the given boolean value, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("loved", loved)

    def by_parent(self, parent: 'XAMusicPlaylist') -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose parent matches the given playlist, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("parent", parent.xa_elem)

    def by_size(self, size: int) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose size matches the given size, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_special_kind(self, special_kind: XAMusicApplication.PlaylistKind) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose kind matches the given kind, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("specialKind", special_kind.value)

    def by_time(self, time: str) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose time string matches the given string, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_visible(self, visible: bool) -> Union['XAMusicPlaylist', None]:
        """Retrieves the playlist whose visible status matches the given boolean value, if one exists.

        :return: The desired playlist, if it is found
        :rtype: Union[XAMusicPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

class XAMusicPlaylist(XAMusicItem):
    """A playlist in Music.app.

    .. seealso:: :class:`XAMusicLibraryPlaylist`, :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.object_description: str #: The string description of the playlist
        self.disliked: bool #: Whether the playlist is disliked
        self.duration: int #: The total length of all tracks in seconds
        self.name: str #: The name of the playlist
        self.loved: bool #: Whether the playlist is loved
        self.parent: XAMusicPlaylist #: The folder containing the playlist, if any
        self.size: int #: The total size of all tracks in the playlist in bytes
        self.special_kind: XAMusicApplication.PlaylistKind #: The special playlist kind
        self.time: str #: The length of all tracks in the playlist in MM:SS format
        self.visible: bool #: Whether the playlist is visible in the source list

        if not hasattr(self, "xa_specialized"):
            print(self.xa_elem.objectClass())
            if self.special_kind == XAMusicApplication.PlaylistKind.LIBRARY or self.special_kind == XAMusicApplication.PlaylistKind.USER_LIBRARY:
                self.__class__ = XAMusicLibraryPlaylist

            elif self.special_kind == XAMusicApplication.PlaylistKind.FOLDER:
                self.__class__ = XAMusicFolderPlaylist

            elif self.special_kind == XAMusicApplication.PlaylistKind.USER or self.special_kind == XAMusicApplication.PlaylistKind.NONE:
                self.__class__ = XAMusicUserPlaylist

            self.xa_specialized = True
            self.__init__(properties)

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def disliked(self) -> bool:
        return self.xa_elem.disliked()

    @property
    def duration(self) -> int:
        return self.xa_elem.duration()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def loved(self) -> bool:
        return self.xa_elem.loved()

    @property
    def parent(self) -> 'XAMusicPlaylist':
        return self._new_element(self.xa_elem.parent(), XAMusicPlaylist)

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def special_kind(self) -> XAMusicApplication.PlaylistKind:
        return XAMusicApplication.PlaylistKind(self.xa_elem.specialKind())

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
            "all": XAMusicApplication.SearchFilter.ALL,
            "artists": XAMusicApplication.SearchFilter.ARTISTS,
            "albums": XAMusicApplication.SearchFilter.ALBUMS,
            "displayed": XAMusicApplication.SearchFilter.DISPLAYED,
            "tracks": XAMusicApplication.SearchFilter.NAMES,
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
            items.append(XAMusicTrack(properties))
        return items

    def tracks(self, filter: Union[dict, None] = None) -> 'XAMusicTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMusicTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.tracks(), XAMusicTrackList, filter)

    def artworks(self, filter: Union[dict, None] = None) -> 'XAMusicArtworkList':
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMusicArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.artworks(), XAMusicArtworkList, filter)




class XAMusicAudioCDPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of audio CD playlists that employs fast enumeration techniques.

    All properties of audio CD playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAudioCDPlaylist)

    def artist(self) -> List[str]:
        """Gets the artist of each playlist in the list.

        :return: A list of audio CD playlist artists
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("artist"))

    def compilation(self) -> List[bool]:
        """Gets the compilation status of each playlist in the list.

        :return: A list of audio CD playlist compilation status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("compilation"))

    def composer(self) -> List[str]:
        """Gets the composer of each playlist in the list.

        :return: A list of audio CD playlist composers
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("composer"))

    def disc_count(self) -> List[int]:
        """Gets the disc count of each playlist in the list.

        :return: A list of audio CD playlist disc counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discCount"))

    def disc_number(self) -> List[int]:
        """Gets the disc number of each playlist in the list.

        :return: A list of audio CD playlist disc numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("discNumber"))

    def genre(self) -> List[str]:
        """Gets the genre of each playlist in the list.

        :return: A list of audio CD playlist genres
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("genre"))

    def year(self) -> List[int]:
        """Gets the year of each playlist in the list.

        :return: A list of audio CD playlist years
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("year"))

    def by_artist(self, artist: str) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose artist matches the given artist, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("artist", artist)

    def by_compilation(self, compilation: bool) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose compilation status matches the given boolean value, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose composer matches the given composer, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("composer", composer)

    def by_disc_count(self, disc_count: int) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose disc count matches the given disc count, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose disc number matches the given disc number, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discNumber", disc_number)

    def by_genre(self, genre: str) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose genre matches the given genre, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("genre", genre)

    def by_year(self, year: int) -> Union['XAMusicAudioCDPlaylist', None]:
        """Retrieves the first audio CD playlist whose year matches the given year, if one exists.

        :return: The desired audio CD playlist, if it is found
        :rtype: Union[XAMusicAudioCDPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("year", year)

class XAMusicAudioCDPlaylist(XAMusicPlaylist):
    """An audio CD playlist in Music.app.

    .. seealso:: :class:`XAMusicLibraryPlaylist`, :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.artist: str #: The artist of the CD
        self.compilation: bool #: Whether the CD is a compilation album
        self.composer: str #: The composer of the CD
        self.disc_count: int #: The total number of discs in the CD's album
        self.disc_number: int #: The index of the CD disc in the source album
        self.genre: str #: The genre of the CD
        self.year: int #: The year the album was recorded/released

    @property
    def artist(self) -> str:
        return self.xa_elem.artist()

    @property
    def compilation(self) -> bool:
        return self.xa_elem.compilation()

    @property
    def composer(self) -> str:
        return self.xa_elem.composer()

    @property
    def disc_count(self) -> int:
        return self.xa_elem.discCount()

    @property
    def disc_number(self) -> int:
        return self.xa_elem.discNumber()

    @property
    def genre(self) -> str:
        return self.xa_elem.genre()
    
    @property
    def year(self) -> int:
        return self.xa_elem.year()

    def audio_cd_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicAudioCDTrackList':
        """Returns a list of audio CD tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD tracks
        :rtype: XAMusicAudioCDTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.audioCDTracks(), XAMusicAudioCDTrackList, filter)




class XAMusicLibraryPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of library playlists that employs fast enumeration techniques.

    All properties of library playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicLibraryPlaylist)

class XAMusicLibraryPlaylist(XAMusicPlaylist):
    """The library playlist in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), XAMusicFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMusicURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMusicSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sharedTracks(), XAMusicSharedTrackList, filter)




class XAMusicRadioTunerPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of radio tuner playlists that employs fast enumeration techniques.

    All properties of radio tuner playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicRadioTunerPlaylist)

class XAMusicRadioTunerPlaylist(XAMusicPlaylist):
    """A radio playlist in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMusicURLTrackList, filter)




class XAMusicSourceList(XAMusicItemList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSource)

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

    def kind(self) -> List[XAMusicApplication.SourceKind]:
        """Gets the kind of each source in the list.

        :return: A list of source kinds
        :rtype: List[XAMusicApplication.SourceKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("kind")
        return [XAMusicApplication.SourceKind(XABase.OSType(x.stringValue())) for x in ls]

    def by_capacity(self, capacity: int) -> Union['XAMusicSource', None]:
        """Retrieves the source whose capacity matches the given capacity, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMusicSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union['XAMusicSource', None]:
        """Retrieves the source whose free space matches the given value, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMusicSource, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("freeSpace", free_space)

    def by_kind(self, kind: XAMusicApplication.SourceKind) -> Union['XAMusicSource', None]:
        """Retrieves the source whose kind matches the given kind, if one exists.

        :return: The desired source, if it is found
        :rtype: Union[XAMusicSource, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("kind", kind.value)

class XAMusicSource(XAMusicItem):
    """A media source in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.capacity: int #: The total size of the source, if it has a fixed size
        self.free_space: int #: The free space on the source, if it has a fixed size
        self.kind: XAMusicApplication.SourceKind #: The source kind

    @property
    def capacity(self) -> int:
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        return self.xa_elem.freeSpace()

    @property
    def kind(self) -> XAMusicApplication.SourceKind:
        return XAMusicApplication.SourceKind(self.xa_elem.kind())

    def audio_cd_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicAudioCDPlaylistList':
        """Returns a list of audio CD playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD playlists
        :rtype: XAMusicAudioCDPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.audioCDPlaylists(), XAMusicAudioCDPlaylistList, filter)

    def library_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicLibraryPlaylistList':
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned library playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XAMusicLibraryPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.libraryPlaylists(), XAMusicLibraryPlaylistList, filter)

    def playlists(self, filter: Union[dict, None] = None) -> 'XAMusicPlaylistList':
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMusicPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.playlists(), XAMusicPlaylistList, filter)

    def radio_tuner_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicRadioTunerPlaylistList':
        """Returns a list of radio tuner playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned radio tuner playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio tuner playlists
        :rtype: XAMusicRadioTunerPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.radioTunerPlaylists(), XAMusicRadioTunerPlaylistList, filter)

    def subscription_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicSubscriptionPlaylistList':
        """Returns a list of subscription playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned subscription playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of subscription playlists
        :rtype: XAMusicSubscriptionPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.subscriptionPlaylists(), XAMusicSubscriptionPlaylistList, filter)

    def user_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicUserPlaylistList':
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned user playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XAMusicUserPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.userPlaylists(), XAMusicUserPlaylistList, filter)




class XAMusicSubscriptionPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of subscription playlists that employs fast enumeration techniques.

    All properties of subscription playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSubscriptionPlaylist)

class XAMusicSubscriptionPlaylist(XAMusicPlaylist):
    """A subscription playlist from Apple Music in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), XAMusicFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMusicURLTrackList, filter)




class XAMusicTrackList(XAMusicItemList):
    """A wrapper around lists of music tracks that employs fast enumeration techniques.

    All properties of music tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicTrack
        super().__init__(properties, filter, obj_class)

    def album(self) -> List[str]:
        """Gets the album name of each track in the list.

        :return: A list of track album names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("album"))

    def album_artist(self) -> List[str]:
        """Gets the album artist of each track in the list.

        :return: A list of track album artists
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumArtist"))

    def album_disliked(self) -> List[bool]:
        """Gets the album disliked status of each track in the list.

        :return: A list of track album disliked statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumDisliked"))

    def album_loved(self) -> List[bool]:
        """Gets the album loved status of each track in the list.

        :return: A list of track album loved statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumLoved"))

    def album_rating(self) -> List[int]:
        """Gets the album rating of each track in the list.

        :return: A list of track album ratings
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("albumRating"))

    def album_rating_kind(self) -> List[XAMusicApplication.RatingKind]:
        """Gets the album rating kind of each track in the list.

        :return: A list of track album rating kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("albumRatingKind")
        return [XAMusicApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

    def artist(self) -> List[str]:
        """Gets the artist of each track in the list.

        :return: A list of track artists
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("artist"))

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

    def bpm(self) -> List[int]:
        """Gets the BPM of each track in the list.

        :return: A list of track BPMs
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bpm"))

    def category(self) -> List[str]:
        """Gets the category of each track in the list.

        :return: A list of track categories
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("category"))

    def cloud_status(self) -> List[XAMusicApplication.iCloudStatus]:
        """Gets the cloud status of each track in the list.

        :return: A list of track cloud statuses
        :rtype: List[XAMusicApplication.iCloudStatus]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cloudStatus")
        return [XAMusicApplication.iCloudStatus(XABase.OSType(x.stringValue())) for x in ls]

    def comment(self) -> List[str]:
        """Gets the comment of each track in the list.

        :return: A list of track comments
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def compilation(self) -> List[bool]:
        """Gets the compilation status of each track in the list.

        :return: A list of track compilation statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("compilation"))

    def composes(self) -> List[str]:
        """Gets the composer of each track in the list.

        :return: A list of track composers
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("composer"))

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

    def disliked(self) -> List[bool]:
        """Gets the disliked status of each track in the list.

        :return: A list of track disliked statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("disliked"))

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

    def eq(self) -> List[str]:
        """Gets the name of the EQ preset of each track in the list.

        :return: A list of track EQ presets
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("EQ"))

    def finish(self) -> List[float]:
        """Gets the stop time of each track in the list.

        :return: A list of track stop times
        :rtype: List[float]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("finish"))

    def gapless(self) -> List[bool]:
        """Gets the gapless status of each track in the list.

        :return: A list of track gapless statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("gapless"))

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

    def loved(self) -> List[bool]:
        """Gets the loved status of each track in the list.

        :return: A list of track loved statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("loved"))

    def lyrics(self) -> List[str]:
        """Gets the lyrics of each track in the list.

        :return: A list of track lyrics
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("lyrics"))

    def media_kind(self) -> List[XAMusicApplication.MediaKind]:
        """Gets the media kind of each track in the list.

        :return: A list of track media kinds
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("mediaKind")
        return [XAMusicApplication.MediaKind(XABase.OSType(x.stringValue())) for x in ls]

    def modification_date(self) -> List[datetime]:
        """Gets the modification date of each track in the list.

        :return: A list of track modification dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def movement(self) -> List[str]:
        """Gets the movement of each track in the list.

        :return: A list of track movements
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("movement"))

    def movement_count(self) -> List[int]:
        """Gets the movement count of each track in the list.

        :return: A list of track movement counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("movementCount"))

    def movement_number(self) -> List[int]:
        """Gets the movement number of each track in the list.

        :return: A list of track movement numbers
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("movementNumber"))

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

    def rating_kind(self) -> List[XAMusicApplication.RatingKind]:
        """Gets the rating kind of each track in the list.

        :return: A list of track rating kinds
        :rtype: List[XAMusicApplication.RatingKind]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("ratingKind")
        return [XAMusicApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls]

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

    def shufflable(self) -> List[bool]:
        """Gets the shufflable status of each track in the list.

        :return: A list of track shuffle statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shufflable"))

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

    def sort_artist(self) -> List[str]:
        """Gets the artist sort string of each track in the list.

        :return: A list of track artist sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortArtist"))

    def sort_album_artist(self) -> List[str]:
        """Gets the album artist sort string of each track in the list.

        :return: A list of track album artist sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortAlbumArtist"))

    def sort_name(self) -> List[str]:
        """Gets the name sort string of each track in the list.

        :return: A list of track name sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortName"))

    def sort_composer(self) -> List[str]:
        """Gets the composer sort string of each track in the list.

        :return: A list of track composer sort strings
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortComposer"))

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

    def work(self) -> List[str]:
        """Gets the work of each track in the list.

        :return: A list of track works
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("work"))

    def year(self) -> List[int]:
        """Gets the year of each track in the list.

        :return: A list of track years
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("year"))

    def by_album(self, album: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album matches the given album, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("album", album)

    def by_album_artist(self, album_artist: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album artist matches the given artist, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumArtist", album_artist)

    def by_album_disliked(self, album_disliked: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album disliked status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumDisliked", album_disliked)

    def by_album_loved(self, album_loved: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album loved status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumLoved", album_loved)

    def by_album_rating(self, album_rating: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("albumRating", album_rating)

    def by_album_rating_kind(self, album_rating_kind: XAMusicApplication.RatingKind) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album rating kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("albumRatingKind", album_rating_kind.value)

    def by_artist(self, artist: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose artist matches the given artist, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("artist", artist)

    def by_bit_rate(self, bit_rate: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose bit rate matches the given bit rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bitRate", bit_rate)

    def by_bookmark(self, bookmark: float) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose bookmark matches the given bookmark, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmark", bookmark)

    def by_bookmarkable(self, bookmarkable: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose bookmarkable status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bookmarkable", bookmarkable)

    def by_bpm(self, bpm: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose BPM matches the given BPM, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("bpm", bpm)

    def by_category(self, category: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose category matches the given category, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("category", category)

    def by_cloud_status(self, cloud_status: XAMusicApplication.iCloudStatus) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose cloud status matches the given status, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("cloudStatus", cloud_status.value)

    def by_comment(self, comment: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose comment matches the given comment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("comment", comment)

    def by_compilation(self, compilation: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose compilation status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose composer matches the given composer, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("composer", composer)

    def by_database_id(self, database_id: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose database ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("databaseID", database_id)

    def by_date_added(self, date_added: datetime) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose date added matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("dateAdded", date_added)

    def by_object_description(self, object_description: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose description matches the given description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("objectDescription", object_description)

    def by_disc_count(self, disc_count: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose disc count matches the given disc count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose disc number matches the given disc number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("discNumber", disc_number)

    def by_disliked(self, disliked: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose disliked status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("disliked", disliked)

    def by_downloader_apple_id(self, downloader_apple_id: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose downloader Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderAppleID", downloader_apple_id)

    def by_downloader_name(self, downloader_name: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose downloader name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("downloaderName", downloader_name)

    def by_duration(self, duration: float) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose duration matches the given duration, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("duration", duration)

    def by_enabled(self, enabled: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose enabled status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("enabled", enabled)

    def by_episode_id(self, episode_id: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose episode ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeID", episode_id)

    def by_episode_number(self, episode_number: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose episode number matches the given episode number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("episodeNumber", episode_number)

    def by_eq(self, eq: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose EQ preset matches the given EQ preset name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("EQ", eq)

    def by_finish(self, finish: float) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose stop time matches the given stop time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("finish", finish)

    def by_gapless(self, gapless: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose gapless status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("gapless", gapless)

    def by_genre(self, genre: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose genre matches the given genre, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("genre", genre)

    def by_grouping(self, grouping: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose grouping matches the given grouping, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("grouping", grouping)

    def by_kind(self, kind: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose kind matches the given kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("kind", kind)

    def by_long_description(self, long_description: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose long description matches the given long description, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("longDescription", long_description)

    def by_loved(self, loved: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose loved status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("loved", loved)

    def by_lyrics(self, lyrics: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose lyrics match the given lyrics, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("lyrics", lyrics)

    def by_media_kind(self, media_kind: XAMusicApplication.MediaKind) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose media kind matches the given media kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("mediaKind", media_kind.value)

    def by_modification_date(self, modification_date: datetime) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose modification date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("modificationDate", modification_date)

    def by_movement(self, movement: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose movement matches the given movement, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("movement", movement)

    def by_movement_count(self, movement_count: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose movement count matches the given movement count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("movementCount", movement_count)

    def by_movement_number(self, movement_number: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose movement number matches the given movement number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("movementNumber", movement_number)

    def by_played_count(self, played_count: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose played count matches the given played count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedCount", played_count)

    def by_played_date(self, played_date: datetime) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose last played date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("playedDate", played_date)

    def by_purchaser_apple_id(self, purchaser_apple_id: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose purchaser Apple ID matches the given ID, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserAppleID", purchaser_apple_id)

    def by_purchaser_name(self, purchaser_name: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose purchaser name matches the given name, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("purchaserName", purchaser_name)

    def by_rating(self, rating: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose rating matches the given rating, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("rating", rating)

    def by_rating_kind(self, rating_kind: XAMusicApplication.RatingKind) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose rating kind matches the given rating kind, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("ratingKind", rating_kind.value)

    def by_release_date(self, release_date: datetime) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose release date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("releaseDate", release_date)

    def by_sample_rate(self, sample_rate: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose sample rate matches the given rate, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sampleRate", sample_rate)

    def by_season_number(self, season_number: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose season number matches the given season number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("seasonNumber", season_number)

    def by_shufflable(self, shufflable: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose shufflable status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("shufflable", shufflable)

    def by_skipped_count(self, skipped_count: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose skipped count matches the given skipped count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedCount", skipped_count)

    def by_skipped_date(self, skipped_date: datetime) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose last skipped date matches the given date, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("skippedDate", skipped_date)

    def by_show(self, show: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose show matches the given show, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("show", show)

    def by_sort_album(self, sort_album: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortAlbum", sort_album)

    def by_sort_artist(self, sort_artist: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose artist sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortArtist", sort_artist)

    def by_sort_album_artist(self, sort_album_artist: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose album artist sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortAlbumArtist", sort_album_artist)

    def by_sort_name(self, sort_name: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose name sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortName", sort_name)

    def by_sort_composer(self, sort_composer: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose composer sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortComposer", sort_composer)

    def by_sort_show(self, sort_show: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose show sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortShow", sort_show)

    def by_size(self, size: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose size matches the given size, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("size", size)

    def by_start(self, start: float) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose start time matches the given start time, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("start", start)

    def by_time(self, time: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose time string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("time", time)

    def by_track_count(self, track_count: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose track count matches the given track count, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackCount", track_count)

    def by_track_number(self, track_number: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose track number matches the given track number, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("trackNumber", track_number)

    def by_unplayed(self, unplayed: bool) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose unplayed status matches the given boolean value, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("unplayed", unplayed)

    def by_volume_adjustment(self, volume_adjustment: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose volume adjustment matches the given volume adjustment, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("volumeAdjustment", volume_adjustment)

    def by_work(self, work: str) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose work matches the given work, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("work", work)

    def by_year(self, year: int) -> Union['XAMusicTrack', None]:
        """Retrieves the first track whose year matches the given year, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XAMusicTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("year", year)

class XAMusicTrack(XAMusicItem):
    """A class for managing and interacting with tracks in TV.app.

    .. seealso:: :class:`XAMusicSharedTrack`, :class:`XAMusicFileTrack`, :class:`XAMusicRemoteURLTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.album: str #: The name of the album the track's album
        self.album_artist: str #: The album artist of the track
        self.album_disliked: bool #: Whether the album for the track is disliked
        self.album_loved: bool #: Whether the album for the track is loved
        self.album_rating: int #: The rating of the track's album
        self.album_rating_kind: str #: The album's rating kind
        self.artist: str #: The artist/source of the track
        self.bit_rate: int #: The track's bitrate in kbps
        self.bookmark: float #: The bookmark time of the track in seconds
        self.bookmarkable: bool #: Whether the playback position is kept in memory after stopping the track
        self.bpm: int #: The tempo of the track in beats per minute
        self.category: str #: The category of the track
        self.cloud_status: XAMusicApplication.iCloudStatus # The iCloud status of the track
        self.comment: str #: User-provided notes on the track
        self.compilation: bool #: Whether the track is from a compilation album
        self.composer: str #: The composer of the track
        self.database_id: int #: A unique ID for the track
        self.date_added: datetime #: The date the track was added to the current playlist
        self.object_description: str #: A string description of the track
        self.disc_count: int #: The number of discs in the source album
        self.disc_number: int #: The index of the disc containing the track
        self.disliked: bool #: Whether the track is disliked
        self.downloader_apple_id: str #: The Apple ID of the person who downloaded the track
        self.downloader_name: str #: The full name of the person who downloaded the track
        self.duration: float #: Length of the track in seconds
        self.enabled: bool #: Whether the track is able to be played
        self.episode_id: str #: A unique ID for the episode of the track
        self.episode_number: int #: The episode number of the track
        self.eq: str #: The name of the EQ preset of the track
        self.finish: float #: The time in seconds from the start at which the track stops playing.
        self.gapless: bool #: Whether the track is a from a gapless album
        self.genre: str #: The music/audio genre category of the track.
        self.grouping: str #: The current section/chapter/movement of the track
        self.kind: str #: A text description of the track
        self.long_description: str #: A long description for the track
        self.loved: bool #: Whether the track is loved
        self.lyrics: str #: The lyrics of the track
        self.media_kind: XAMusicApplication.MediaKind #: A description of the track's media type
        self.modification_date: datetime #: The last modification date of the track's content
        self.movement: str #: The movement name of the track
        self.movement_count: int #: The total number of movements in the work
        self.movement_number: int #: The index of the movement in the work
        self.played_count: int #: The number of the times the track has been played
        self.played_date: datetime #: The date the track was last played
        self.purchaser_apple_id: str #: The Apple ID of the person who bought the track
        self.purchaser_name: str #: The full name of the person who bought the track
        self.rating: int #: The rating of the track from 0 to 100
        self.rating_kind: XAMusicApplication.RatingKind #: Whether the rating is user-provided or computed
        self.release_date: datetime #: The date the track was released
        self.sample_rate: int #: The sample rate of the track in Hz
        self.season_number: int #: The number of the season the track belongs to
        self.shufflable: bool #: Whether the track is included when shuffling
        self.skipped_count: int #: The number of times the track has been skipped
        self.skipped_date: datetime #: The date the track was last skipped
        self.show: str #: The name of the show the track belongs to
        self.sort_album: str #: The string used for this track when sorting by album
        self.sort_artist: str #: The string used for this track when sorting by artist
        self.sort_album_artist: str #: The string used for this track when sorting by album artist
        self.sort_name: str #: The string used for this track when sorting by name
        self.sort_composer: str #: The string used for this track when sorting by composer
        self.sort_show: str #: The string used for this track when sorting by show
        self.size: int #: The size of the track in bytes
        self.start: float #: The start time of the track in seconds
        self.time: str #: HH:MM:SS representation for the duration of the track
        self.track_count: int #: The number of tracks in the track's album
        self.track_number: int #: The index of the track within its album
        self.unplayed: bool #: Whether the track has been played before
        self.volume_adjustment: int #: Volume adjustment setting for this track from -100 to +100
        self.work: str #: The work name of the track
        self.year: int #: The year the track was released

        # print("Track type", self.objectClass.data())
        # if self.objectClass.data() == _SHARED_TRACK:
        #     self.__class__ = XAMusicSharedTrack
        #     self.__init__()
        # elif self.objectClass.data() == _FILE_TRACK:
        #     self.__class__ = XAMusicFileTrack
        #     self.__init__()
        # elif self.objectClass.data() == _URL_TRACK:
        #     self.__class__ = XAMusicURLTrack
        #     self.__init__()

    @property
    def album(self) -> str:
        return self.xa_elem.album()

    @property
    def album_artist(self) -> str:
        return self.xa_elem.albumArtist()

    @property
    def album_disliked(self) -> bool:
        return self.xa_elem.albumDisliked()

    @property
    def album_loved(self) -> bool:
        return self.xa_elem.albumLoved()

    @property
    def album_rating(self) -> int:
        return self.xa_elem.albumRating()

    @property
    def album_rating_kind(self) -> XAMusicApplication.RatingKind:
        return XAMusicApplication.RatingKind(self.xa_elem.albumRatingKind())

    @property
    def artist(self) -> str:
        return self.xa_elem.artist()

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
    def bpm(self) -> int:
        return self.xa_elem.bpm()

    @property
    def category(self) -> str:
        return self.xa_elem.category()

    @property
    def cloud_status(self) -> XAMusicApplication.iCloudStatus:
        return XAMusicApplication.iCloudStatus(self.xa_elem.cloudStatus())

    @property
    def comment(self) -> str:
        return self.xa_elem.comment()

    @property
    def compilation(self) -> bool:
        return self.xa_elem.compilation()

    @property
    def composer(self) -> str:
        return self.xa_elem.composer()

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
    def disc_count(self) -> int:
        return self.xa_elem.discCount()

    @property
    def disc_number(self) -> int:
        return self.xa_elem.discNumber()

    @property
    def disliked(self) -> bool:
        return self.xa_elem.disliked()

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
    def eq(self) -> str:
        return self.xa_elem.EQ()

    @property
    def finish(self) -> float:
        return self.xa_elem.finish()

    @property
    def gapless(self) -> bool:
        return self.xa_elem.gapless()

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
    def loved(self) -> bool:
        return self.xa_elem.loved()

    @property
    def lyrics(self) -> str:
        return self.xa_elem.lyrics()

    @property
    def media_kind(self) -> XAMusicApplication.MediaKind:
        return XAMusicApplication.MediaKind(self.xa_elem.mediaKind())

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def movement(self) -> str:
        return self.xa_elem.movement()

    @property
    def movement_count(self) -> int:
        return self.xa_elem.movementCount()

    @property
    def movement_number(self) -> int:
        return self.xa_elem.movementNumber()

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
    def rating_kind(self) -> XAMusicApplication.RatingKind:
        return XAMusicApplication.RatingKind(self.xa_elem.ratingKind())

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
    def shufflable(self) -> bool:
        return self.xa_elem.shufflable()

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
    def sort_artist(self) -> str:
        return self.xa_elem.sortArtist()

    @property
    def sort_album_artist(self) -> str:
        return self.xa_elem.sortAlbumArtist()

    @property
    def sort_name(self) -> str:
        return self.xa_elem.sortName()

    @property
    def sort_composer(self) -> str:
        return self.xa_elem.sortComposer()

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
    def work(self) -> str:
        return self.xa_elem.work()

    @property
    def year(self) -> int:
        return self.xa_elem.year()

    def select(self) -> 'XAMusicItem':
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XAMusicTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self

    def play(self) -> 'XAMusicItem':
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XAMusicItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self

    def artworks(self, filter: Union[dict, None] = None) -> 'XAMusicArtworkList':
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMusicArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.artworks(), XAMusicArtworkList, filter)



class XAMusicAudioCDTrackList(XAMusicTrackList):
    """A wrapper around lists of music audio CD tracks that employs fast enumeration techniques.

    All properties of music audio CD tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAudioCDTrack)

    def location(self) -> List[XABase.XAURL]:
        """Gets the location of each track in the list.

        :return: A list of track locations
        :rtype: List[XABase.XAURL]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union['XAMusicAudioCDTrack', None]:
        """Retrieves the audio CD track whose location matches the given location, if one exists.

        :return: The desired audio CD track, if it is found
        :rtype: Union[MusicAudioCDTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("location", location.xa_elem)

class XAMusicAudioCDTrack(XAMusicTrack):
    """An audio CD track in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.location: XABase.XAURL #: The location of the file represented by the track

    @property
    def location(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.location())




class XAMusicFileTrackList(XAMusicTrackList):
    """A wrapper around lists of music file tracks that employs fast enumeration techniques.

    All properties of music file tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicFileTrack)

    def location(self) -> List[XABase.XAURL]:
        """Gets the location of each track in the list.

        :return: A list of track locations
        :rtype: List[XABase.XAURL]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union['XAMusicFileTrack', None]:
        """Retrieves the file track whose location matches the given location, if one exists.

        :return: The desired file track, if it is found
        :rtype: Union[XAMusicFileTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("location", location.xa_elem)

class XAMusicFileTrack(XAMusicTrack):
    """A file track in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.location: XABase.XAURL #: The location of the file represented by the track

    @property
    def location(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.location())




class XAMusicSharedTrackList(XAMusicTrackList):
    """A wrapper around lists of music shared tracks that employs fast enumeration techniques.

    All properties of music shared tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSharedTrack)

class XAMusicSharedTrack(XAMusicTrack):
    """A shared track in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMusicURLTrackList(XAMusicTrackList):
    """A wrapper around lists of music URL tracks that employs fast enumeration techniques.

    All properties of music URL tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicURLTrack)

    def address(self) -> List[str]:
        """Gets the address of each track in the list.

        :return: A list of track addresses
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def by_address(self, address: str) -> Union['XAMusicURLTrack', None]:
        """Retrieves the URL track whose address matches the given address, if one exists.

        :return: The desired URL track, if it is found
        :rtype: Union[XAMusicURLTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("address", address)

class XAMusicURLTrack(XAMusicTrack):
    """A URL track in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: str #: The URL for the track

    @property
    def address(self) -> str:
        return self.xa_elem.address()




class XAMusicUserPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of music user playlists that employs fast enumeration techniques.

    All properties of music user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicUserPlaylist)

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

    def genius(self) -> List[bool]:
        """Gets the genius status of each user playlist in the list.

        :return: A list of playlist genius status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("genius"))

    def by_shared(self, shared: bool) -> Union['XAMusicUserPlaylist', None]:
        """Retrieves the user playlist whose shared status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XAMusicUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("shared", shared)

    def by_smart(self, smart: bool) -> Union['XAMusicUserPlaylist', None]:
        """Retrieves the user playlist whose smart status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XAMusicUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("smart", smart)

    def by_genius(self, genius: bool) -> Union['XAMusicUserPlaylist', None]:
        """Retrieves the user playlist whose genius status matches the given value, if one exists.

        :return: The desired user playlist, if it is found
        :rtype: Union[XAMusicUserPlaylist, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("genius", genius)

class XAMusicUserPlaylist(XAMusicPlaylist):
    """A user-created playlist in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.shared: bool #: Whether the playlist is shared
        self.smart: bool #: Whether the playlist is a smart playlist
        self.genius: bool #: Whether the playlist is a genius playlist

    @property
    def shared(self) -> bool:
        return self.xa_elem.shared()

    @property
    def smart(self) -> bool:
        return self.xa_elem.smart()

    @property
    def genius(self) -> bool:
        return self.xa_elem.genius()

    def file_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), XAMusicFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMusicURLTrackList, filter)

    def shared_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicSharedTrackList':
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMusicSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sharedTracks(), XAMusicSharedTrackList, filter)




class XAMusicFolderPlaylistList(XAMusicUserPlaylistList):
    """A wrapper around lists of music folder playlists that employs fast enumeration techniques.

    All properties of music folder playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicFolderPlaylist)

class XAMusicFolderPlaylist(XAMusicUserPlaylist):
    """A folder playlist in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMusicVisualList(XAMusicItemList):
    """A wrapper around lists of music visuals that employs fast enumeration techniques.

    All properties of music visuals can be called as methods on the wrapped list, returning a list containing each visual's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicVisual)

class XAMusicVisual(XAMusicPlaylist):
    """A music visual in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMusicWindowList(XAMusicItemList):
    """A wrapper around lists of music browser windows that employs fast enumeration techniques.

    All properties of music browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicWindow
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

    def by_bounds(self, bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> Union['XAMusicWindow', None]:
        """Retrieves the window whose bounds matches the given bounds, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("bounds", bounds)

    def by_closeable(self, closeable: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose closeable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("closeable", closeable)

    def by_collapseable(self, collapseable: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose collapseable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapseable", collapseable)

    def by_collapsed(self, collapsed: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose collapsed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("collapsed", collapsed)

    def by_full_screen(self, full_screen: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose full screen status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fullScreen", full_screen)

    def by_position(self, position: Tuple[int, int]) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose position matches the given position, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        # TODO
        return self.by_property("position", position)

    def by_resizable(self, resizable: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose resizable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose visible status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose zoomable status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union['XAMusicWindow', None]:
        """Retrieves the first window whose zoomed status matches the given boolean value, if one exists.

        :return: The desired window, if it is found
        :rtype: Union[XAMusicWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("zoomed", zoomed)

class XAMusicWindow(XABaseScriptable.XASBWindow, XAMusicItem):
    """A windows of Music.app.

    .. seealso:: :class:`XAMusicBrowserWindow`, :class:`XAMusicPlaylistWindow`, :class:`XAMusicVideoWindow`

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
                self.__class__ = XAMusicBrowserWindow
            elif obj_class == b'WlPc':
                self.__class__ = XAMusicPlaylistWindow
            elif obj_class == b'niwc':
                self.__class__ = XAMusicVideoWindow
            elif obj_class == b'WPMc':
                self.__class__ = XAMusicMiniplayerWindow
            elif obj_class == b'WQEc':
                self.__class__ = XAMusicEQWindow
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




class XAMusicBrowserWindowList(XAMusicWindowList):
    """A wrapper around lists of music browser windows that employs fast enumeration techniques.

    All properties of music browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicBrowserWindow)

    def selection(self) -> XAMusicTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XAMusicTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAMusicTrackList)

    def view(self) -> XAMusicPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XAMusicPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XAMusicPlaylistList)

    def by_selection(self, selection: XAMusicTrackList) -> Union['XAMusicPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMusicPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMusicPlaylist) -> Union['XAMusicPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMusicPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XAMusicBrowserWindow(XAMusicWindow):
    """A browser window of Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XAMusicTrackList #: The selected tracks
        self.view: XAMusicPlaylist #: The playlist currently displayed in the window




class XAMusicEQWindowList(XAMusicWindowList):
    """A wrapper around lists of music equalizer windows that employs fast enumeration techniques.

    All properties of music equalizer windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEQWindow)

class XAMusicEQWindow(XAMusicWindow):
    """An equalizer window in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMusicMiniplayerWindowList(XAMusicWindowList):
    """A wrapper around lists of music miniplayer windows that employs fast enumeration techniques.

    All properties of music minipplayer windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicMiniplayerWindow)

class XAMusicMiniplayerWindow(XAMusicWindow):
    """A miniplayer window in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAMusicPlaylistWindowList(XAMusicWindowList):
    """A wrapper around lists of music playlist windows that employs fast enumeration techniques.

    All properties of music playlist windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicPlaylistWindow)

    def selection(self) -> XAMusicTrackList:
        """Gets the selection of each window in the list.

        :return: A list of selected tracks
        :rtype: XAMusicTrackList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAMusicTrackList)

    def view(self) -> XAMusicPlaylistList:
        """Gets the current playlist view of each user window in the list.

        :return: A list of currently viewed playlists
        :rtype: XAMusicPlaylistList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("view")
        return self._new_element(ls, XAMusicPlaylistList)

    def by_selection(self, selection: XAMusicTrackList) -> Union['XAMusicPlaylistWindow', None]:
        """Retrieves the playlist window whose selection matches the given list of tracks, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMusicPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMusicPlaylist) -> Union['XAMusicPlaylistWindow', None]:
        """Retrieves the playlist window whose view matches the given view, if one exists.

        :return: The desired playlist window, if it is found
        :rtype: Union[XAMusicPlaylistWindow, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("view", view.xa_elem)

class XAMusicPlaylistWindow(XAMusicWindow):
    """A playlist window in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.selection: XAMusicTrackList #: The selected tracks
        self.view: XAMusicPlaylist #: The playlist currently displayed in the window




class XAMusicVideoWindowList(XAMusicWindowList):
    """A wrapper around lists of music video windows that employs fast enumeration techniques.

    All properties of music video windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicVideoWindow)

class XAMusicVideoWindow(XAMusicWindow):
    """A video window in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
