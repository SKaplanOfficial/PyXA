""".. versionadded:: 0.0.1

Control the macOS Music application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Union

import AppKit
import ScriptingBridge

from PyXA import XABase
from PyXA import XABaseScriptable
from PyXA.XAProtocols import XACanOpenPath
from PyXA.XAEvents import event_from_str, event_from_type_code


class MusicObjectClass(Enum):
    AIRPLAY_DEVICE = "cAPD"
    APPLICATION = "capp"
    ARTWORK = "cArt"
    AUDIO_CD_PLAYLIST = "cCDP"
    AUDIO_CD_TRACK = "cCDT"
    BROWSER_WINDOW = "cBrW"
    ENCODER = "cEnc"
    EQ_PRESET = "cEQP"
    EQ_WINDOW = "cEQW"
    FILE_TRACK = "cFlT"
    FOLDER_PlAYLIST = "cFoP"
    ITEM = "cobj"
    LIBRARY_PLAYLIST = "cLiP"
    MINIPLAYER_WINDOW = "cMPW"
    PLAYLIST = "cPly"
    PLAYLIST_WINDOW = "cPlW"
    RADIO_TUNER_PLAYLIST = "cRTP"
    SHARED_TRACK = "cShT"
    SOURCE = "cSrc"
    SUBSCRIPTION_PLAYLIST = "cSuP"
    TRACK = "cTrk"
    URL_TRACK = "cURT"
    USER_PLAYLIST = "cUsP"
    VIDEO_WINDOW = "cNPW"
    VISUAL = "cVis"
    WINDOW = "cwin"


class XAMusicApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Music.app.

    .. seealso:: :class:`XAMusicWindow`, class:`XAMusicSource`, :class:`XAMusicPlaylist`, :class:`XAMusicTrack`

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """Types of objects that can be created using the :func:`make` method."""

        PLAYLIST = "playlist"
        USER_PLAYLIST = "user_playlist"
        FOLDER_PLAYLIST = "folder_playlist"
        LIBRARY_PLAYLIST = "library_playlist"
        AUDIO_CD_PLAYLIST = "audio_cd_playlist"
        RADIO_TUNER_PLAYLIST = "radio_tuner_playlist"
        SUBSCRIPTION_PLAYLIST = "subscription_playlist"
        TRACK = "track"
        URL_TRACK = "url_track"
        SHARED_TRACK = "shared_track"
        AUDIO_CD_TRACK = "audio_cd_track"
        FILE_TRACK = "file_track"
        AIRPLAY_DEVICE = "airplay_device"
        ARTWORK = "artwork"
        WINDOW = "window"
        BROWSER_WINDOW = "browser_window"
        ENCODER = "encoder"
        EQ_PRESET = "eq_preset"
        EQ_WINDOW = "eq_window"
        MINIPLAYER_WINDOW = "miniplayer_window"
        PLAYLIST_WINDOW = "playlist_window"
        SOURCE = "source"
        VIDEO_WINDOW = "video_window"
        VISUAL = "visual"

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
        AUDIO_CD = XABase.OSType("kACD")  #: A CD source
        MP3_CD = XABase.OSType("kMCD")  #: An MP3 file source
        RADIO_TUNER = XABase.OSType("kTun")  #: A radio source
        SHARED_LIBRARY = XABase.OSType("kShd")  #: A shared library source
        ITUNES_STORE = XABase.OSType("kITS")  #: The iTunes Store source
        UNKNOWN = XABase.OSType("kUnk")  #: An unknown source

    class SearchFilter(Enum):
        """Filter restrictions on search results."""

        ALBUMS = XABase.OSType("kSrL")  #: Search albums
        ALL = XABase.OSType("kAll")  #: Search all
        ARTISTS = XABase.OSType("kSrR")  #: Search artists
        COMPOSERS = XABase.OSType("kSrC")  #: Search composers
        DISPLAYED = XABase.OSType("kSrV")  #: Search the currently displayed playlist
        NAMES = XABase.OSType("kSrS")  #: Search track names only

    class PlaylistKind(Enum):
        """Types of special playlists."""

        NONE = XABase.OSType("kNon")  #: An unknown playlist kind
        UNKNOWN = 0  #: An unknown playlist kind
        FOLDER = XABase.OSType("kSpF")  #: A folder
        GENIUS = XABase.OSType("kSpG")  #: A smart playlist
        LIBRARY = XABase.OSType("kSpL")  #: The system library playlist
        MUSIC = XABase.OSType("kSpZ")  #: A playlist containing music items
        PURCHASED_MUSIC = XABase.OSType("kSpM")  #: The purchased music playlist
        USER = XABase.OSType("cUsP")  #: A user-created playlist
        USER_LIBRARY = XABase.OSType("cLiP")  #: The user's library

    class MediaKind(Enum):
        """Types of media items."""

        SONG = XABase.OSType("kMdS")  #: A song media item
        MUSIC_VIDEO = XABase.OSType("kVdV")  #: A music video media item
        UNKNOWN = XABase.OSType("kUnk")  #: An unknown media item kind

    class RatingKind(Enum):
        """Types of ratings for media items."""

        USER = XABase.OSType("kRtU")  #: A user-inputted rating
        COMPUTED = XABase.OSType("kRtC")  #: A computer generated rating

    class PrintSetting(Enum):
        """Options to use when printing."""

        STANDARD_ERROR_HANDLING = XABase.OSType(
            "lwst"
        )  #: Standard PostScript error handling
        DETAILED_ERROR_HANDLING = XABase.OSType(
            "lwdt"
        )  #: Print a detailed report of PostScript errors
        TRACK_LISTING = XABase.OSType(
            "kTrk"
        )  #: A basic listing of tracks within a playlist
        ALBUM_LISTING = XABase.OSType(
            "kAlb"
        )  #: A listing of a playlist grouped by album
        CD_INSERT = XABase.OSType(
            "kCDi"
        )  #: A printout of the playlist for jewel case inserts

    class RepeatMode(Enum):
        """Options for how to repeat playback."""

        OFF = XABase.OSType("kRpO")  #: Playback does not repeat
        ONE = XABase.OSType(
            "kRp1"
        )  #: The currently playing media item will be repeated
        ALL = XABase.OSType(
            "kAll"
        )  #: All media items in the current playlist will be repeated

    class ShuffleMode(Enum):
        """Options for how to shuffle playback."""

        SONGS = XABase.OSType("kShS")  #: Shuffle by song
        ALBUMS = XABase.OSType("kShA")  #: Shuffle by album
        GROUPINGS = XABase.OSType("kShG")  #: Shuffle by grouping

    class DeviceKind(Enum):
        """Kinds of devices."""

        COMPUTER = XABase.OSType("kAPC")  #: A computer device
        AIRPORT_EXPRESS = XABase.OSType("kAPX")  #: An airport express device
        APPLE_TV = XABase.OSType("kAPT")  #: An Apple TV device
        AIRPLAY_DEVICE = XABase.OSType("kAPO")  #: An AirPlay-enabled device
        BLUETOOTH_DEVICE = XABase.OSType("kAPB")  #: A BlueTooth-enabled device
        HOMEPOD = XABase.OSType("kAPH")  #: A HomePod device
        UNKNOWN = XABase.OSType("kAPU")  #: An unknown device

    class iCloudStatus(Enum):
        """iCloud statuses of media items."""

        UNKNOWN = XABase.OSType("kUnk")  #: Unknown cloud status
        PURCHASED = XABase.OSType("kPur")  #: A purchased media item
        MATCHED = XABase.OSType("kMat")  #: A matched media item
        UPLOADED = XABase.OSType("kUpl")  #: An unloaded media item
        INELIGIBLE = XABase.OSType("kRej")  #: A media item ineligible for listening
        REMOVED = XABase.OSType("kRem")  #: A removed media item
        ERROR = XABase.OSType("kErr")  #: A media item unavailable due to an error
        DUPLICATE = XABase.OSType("kDup")  #: A duplicate media item
        SUBSCRIPTION = XABase.OSType(
            "kSub"
        )  #: A media item obtained via a subscription to Apple Music
        NO_LONGER_AVAILABLE = XABase.OSType(
            "kRev"
        )  #: A media item unavailable due to expiration
        NOT_UPLOADED = XABase.OSType("kUpP")  #: A non-uploaded media item

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAMusicWindow

    @property
    def current_playlist(self) -> "XAMusicPlaylist":
        """The playlist containing the currently targeted track."""
        return self._new_element(self.xa_scel.currentPlaylist(), XAMusicPlaylist)

    @property
    def current_stream_title(self) -> str:
        """The name of the currently streaming track."""
        return self.xa_scel.currentStreamTitle()

    @property
    def current_stream_url(self) -> str:
        """The URL of the currently streaming track."""
        return self.xa_scel.currentStreamURL()

    @property
    def current_track(self) -> "XAMusicTrack":
        """The currently targeted track."""
        return self._new_element(self.xa_scel.currentTrack(), XAMusicTrack)

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
    def player_state(self) -> "XAMusicApplication.PlayerState":
        """Whether the player is playing, paused, stopped, fast forwarding, or rewinding."""
        return XAMusicApplication.PlayerState(self.xa_scel.playerState())

    @property
    def selection(self) -> "XAMusicItemList":
        """The selected media items."""
        return self._new_element(self.xa_scel.selection().get(), XAMusicTrackList)

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

    @property
    def airplay_enabled(self) -> bool:
        """Whether AirPlay is currently enabled."""
        return self.xa_scel.AirPlayEnabled()

    @property
    def converting(self) -> bool:
        """Whether a track is currently being converted."""
        return self.xa_scel.converting()

    @property
    def current_airplay_devices(self) -> "XAMusicAirPlayDeviceList":
        """The currently selected AirPlay devices."""
        ls = self.xa_scel.currentAirPlayDevices()
        return self._new_element(ls, XAMusicAirPlayDeviceList)

    @current_airplay_devices.setter
    def current_airplay_devices(
        self,
        current_airplay_devices: Union[
            "XAMusicAirPlayDeviceList", list["XAMusicAirPlayDevice"]
        ],
    ):
        if isinstance(current_airplay_devices, list):
            current_airplay_devices = [x.xa_elem for x in current_airplay_devices]
            self.set_property("currentAirplayDevices", current_airplay_devices)
        else:
            self.set_property("currentAirplayDevices", current_airplay_devices.xa_elem)

    @property
    def current_encoder(self) -> "XAMusicEncoder":
        """The currently selected encoder."""
        return self._new_element(self.xa_scel.currentEncoder(), XAMusicEncoder)

    @current_encoder.setter
    def current_encoder(self, current_encoder: "XAMusicEncoder"):
        self.set_property("currentEncoder", current_encoder.xa_elem)

    @property
    def current_eq_preset(self) -> "XAMusicEQPreset":
        """The currently selected equalizer preset."""
        return self._new_element(self.xa_scel.currentEQPreset(), XAMusicEQPreset)

    @current_eq_preset.setter
    def current_eq_preset(self, current_eq_preset: "XAMusicEQPreset"):
        self.set_property("currentEQPreset", current_eq_preset.xa_elem)

    @property
    def current_visual(self) -> "XAMusicVisual":
        """The currently selected visual plug-in."""
        return self._new_element(self.xa_scel.currentVisual(), XAMusicVisual)

    @current_visual.setter
    def current_visual(self, current_visual: "XAMusicVisual"):
        self.set_property("currentVisual", current_visual.xa_elem)

    @property
    def eq_enabled(self) -> bool:
        """Whether the equalizer is enabled."""
        return self.xa_scel.EQEnabled()

    @eq_enabled.setter
    def eq_enabled(self, eq_enabled: bool):
        self.set_property("eqEnabled", eq_enabled)

    @property
    def shuffle_enabled(self) -> bool:
        """Whether songs are played in random order."""
        return self.xa_scel.shuffleEnabled()

    @shuffle_enabled.setter
    def shuffle_enabled(self, shuffle_enabled: bool):
        self.set_property("shuffleEnabled", shuffle_enabled)

    @property
    def shuffle_mode(self) -> "XAMusicApplication.ShuffleMode":
        """The playback shuffle mode."""
        return XAMusicApplication.ShuffleMode(self.xa_scel.shuffleMode())

    @shuffle_mode.setter
    def shuffle_mode(self, shuffle_mode: "XAMusicApplication.ShuffleMode"):
        self.set_property("shuffleMode", shuffle_mode.value)

    @property
    def song_repeat(self) -> "XAMusicApplication.RepeatMode":
        """The playback repeat mode."""
        return XAMusicApplication.RepeatMode(self.xa_scel.songRepeat())

    @song_repeat.setter
    def song_repeat(self, song_repeat: "XAMusicApplication.RepeatMode"):
        self.set_property("songRepeat", song_repeat.value)

    @property
    def visuals_enabled(self) -> bool:
        """Whether visuals are currently displayed."""
        return self.xa_scel.visualsEnabled()

    @visuals_enabled.setter
    def visuals_enabled(self, visuals_enabled: bool):
        self.set_property("visualsEnabled", visuals_enabled)

    @property
    def current_track(self) -> "XAMusicTrack":
        """The currently playing (or paused but not stopped) track."""
        return self._new_element(self.xa_scel.currentTrack(), XAMusicTrack)

    def play(
        self, item: "XAMusicItem" = None, play_once: bool = True
    ) -> "XAMusicApplication":
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XAMusicItem, optional
        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        if item is None:
            self.xa_scel.playOnce_(play_once)
        else:
            self.xa_scel.play_once_(item.xa_elem, play_once)
        return self

    def playpause(self) -> "XAMusicApplication":
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> "XAMusicApplication":
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> "XAMusicApplication":
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> "XAMusicApplication":
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> "XAMusicApplication":
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> "XAMusicApplication":
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> "XAMusicApplication":
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> "XAMusicApplication":
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> "XAMusicApplication":
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> "XAMusicApplication":
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> "XAMusicApplication":
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def add_to_playlist(self, urls: list[Union[str, AppKit.NSURL]], playlist):
        items = []
        for url in urls:
            if isinstance(url, str):
                url = AppKit.NSURL.alloc().initFileURLWithPath_(url)
            items.append(url)
        self.xa_scel.add_to_(items, playlist.xa_elem)

    def airplay_devices(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicAirPlayDeviceList":
        """Returns a list of AirPlay devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned AirPlay devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of devices
        :rtype: XAMusicAirPlayDeviceList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Music")
        >>> print(app.airplay_devices())
        <<class 'PyXA.apps.Music.XAMusicAirPlayDeviceList'>['ExampleUser\\'s MacBook Pro']>

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_scel.AirPlayDevices(), XAMusicAirPlayDeviceList, filter
        )

    def encoders(self, filter: Union[dict, None] = None) -> "XAMusicEncoderList":
        """Returns a list of encoders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned encoders will have, or None
        :type filter: Union[dict, None]
        :return: The list of encoders
        :rtype: XAMusicEncoderList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.encoders(), XAMusicEncoderList, filter)

    def eq_presets(self, filter: Union[dict, None] = None) -> "XAMusicEQPresetList":
        """Returns a list of EQ presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned EQ presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of presets
        :rtype: XAMusicEQPresetList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.EQPresets(), XAMusicEQPresetList, filter)

    def eq_windows(self, filter: Union[dict, None] = None) -> "XAMusicEQWindowList":
        """Returns a list of EQ windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned EQ windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicEQWindowList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.EQWindows(), XAMusicEQWindowList, filter)

    def miniplayer_windows(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicMiniplayerWindowList":
        """Returns a list of miniplayer windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned miniplayer windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicMiniplayWindowList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_scel.miniplayerWindows(), XAMusicMiniplayerWindowList, filter
        )

    def browser_windows(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicBrowserWindowList":
        """Returns a list of browser windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browser windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicBrowserWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.browserWindows(), XAMusicBrowserWindowList, filter
        )

    def playlists(self, filter: Union[dict, None] = None) -> "XAMusicPlaylistList":
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMusicPlaylistList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.playlists(), XAMusicPlaylistList, filter)

    def library_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicLibraryPlaylistList":
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XAMusicLibraryPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.libraryPlaylists(), XAMusicLibraryPlaylistList, filter
        )

    def playlist_windows(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicPlaylistWindowList":
        """Returns a list of playlist windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicPlaylistWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.playlistWindows(), XAMusicPlaylistWindowList, filter
        )

    def sources(self, filter: Union[dict, None] = None) -> "XAMusicSourceList":
        """Returns a list of sources, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sources will have, or None
        :type filter: Union[dict, None]
        :return: The list of sources
        :rtype: XAMusicSourceList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.sources(), XAMusicSourceList, filter)

    def tracks(self, filter: Union[dict, None] = None) -> "XAMusicTrackList":
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMusicTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XAMusicTrackList, filter)

    def file_tracks(self, filter: Union[dict, None] = None) -> "XAMusicFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.fileTracks(), XAMusicFileTrackList, filter
        )

    def url_tracks(self, filter: Union[dict, None] = None) -> "XAMusicURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(self.xa_scel.URLTracks(), XAMusicURLTrackList, filter)

    def shared_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMusicSharedTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.sharedTracks(), XAMusicSharedTrackList, filter
        )

    def video_windows(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicVideoWindowList":
        """Returns a list of video windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XAMusicVideoWindowList

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.videoWindows(), XAMusicVideoWindowList, filter
        )

    def user_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicUserPlaylistList":
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XAMusicUserPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.userPlaylists(), XAMusicUserPlaylistList, filter
        )

    def subscription_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicSubscriptionPlaylistList":
        """Returns a list of subscription playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of subscription playlists
        :rtype: XAMusicSubscriptionPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.subscriptionPlaylists(),
            XAMusicSubscriptionPlaylistList,
            filter,
        )

    def radio_tuner_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicRadioTunerPlaylistList":
        """Returns a list of radio tuner playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio tuner playlists
        :rtype: XAMusicRadioTunerPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.radioTunerPlaylists(), XAMusicRadioTunerPlaylistList, filter
        )

    def audio_cd_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicAudioCDPlaylistList":
        """Returns a list of audio CD playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD playlists
        :rtype: XAMusicAudioCDPlaylistList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.audioCDPlaylists(), XAMusicAudioCDPlaylistList, filter
        )

    def audio_cd_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicAudioCDTrackList":
        """Returns a list of audio CD tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD tracks
        :rtype: XAMusicAudioCDTrackList

        .. versionadded:: 0.2.1
        """
        return self._new_element(
            self.xa_scel.audioCDTracks(), XAMusicAudioCDTrackList, filter
        )

    def visuals(self, filter: Union[dict, None] = None) -> "XAMusicVisualList":
        """Returns a list of visuals, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned visuals will have, or None
        :type filter: Union[dict, None]
        :return: The list of visuals
        :rtype: XAMusicVisualList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.visuals(), XAMusicVisualList, filter)

    def make(
        self,
        specifier: Union[str, "XAMusicApplication.ObjectType"],
        properties: dict,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list. Valid specifiers are: playlist, user playlist, folder playlist, library playlist, audio CD playlist, radio tuner playlist, subscription playlist, track, URL track, shared track, audio CD track, file track, AirPlay device, artwork, window, browser window, EQ window, miniplayer window, playlist window, video window, visual, source, EQ preset, or encoder.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAMusicApplication.ObjectType]
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
        if isinstance(specifier, XAMusicApplication.ObjectType):
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
            return self._new_element(obj, XAMusicPlaylist)
        elif specifier == "user_playlist":
            return self._new_element(obj, XAMusicUserPlaylist)
        elif specifier == "folder_playlist":
            return self._new_element(obj, XAMusicFolderPlaylist)
        elif specifier == "library_playlist":
            return self._new_element(obj, XAMusicLibraryPlaylist)
        elif specifier == "audio_cd_playlist":
            return self._new_element(obj, XAMusicAudioCDPlaylist)
        elif specifier == "radio_tuner_playlist":
            return self._new_element(obj, XAMusicRadioTunerPlaylist)
        elif specifier == "subscription_playlist":
            return self._new_element(obj, XAMusicSubscriptionPlaylist)
        elif specifier == "track":
            return self._new_element(obj, XAMusicTrack)
        elif specifier == "url_track":
            return self._new_element(obj, XAMusicURLTrack)
        elif specifier == "shared_track":
            return self._new_element(obj, XAMusicSharedTrack)
        elif specifier == "audio_cd_track":
            return self._new_element(obj, XAMusicAudioCDTrack)
        elif specifier == "file_track":
            return self._new_element(obj, XAMusicFileTrack)
        elif specifier == "airplay_device":
            return self._new_element(obj, XAMusicAirPlayDevice)
        elif specifier == "artwork":
            return self._new_element(obj, XAMusicArtwork)
        elif specifier == "window":
            return self._new_element(obj, XAMusicWindow)
        elif specifier == "browser_window":
            return self._new_element(obj, XAMusicBrowserWindow)
        elif specifier == "encoder":
            return self._new_element(obj, XAMusicEncoder)
        elif specifier == "eq_preset":
            return self._new_element(obj, XAMusicEQPreset)
        elif specifier == "eq_window":
            return self._new_element(obj, XAMusicEQWindow)
        elif specifier == "miniplayer_window":
            return self._new_element(obj, XAMusicMiniplayerWindow)
        elif specifier == "playlist_window":
            return self._new_element(obj, XAMusicPlaylistWindow)
        elif specifier == "source":
            return self._new_element(obj, XAMusicSource)
        elif specifier == "video_window":
            return self._new_element(obj, XAMusicVideoWindow)
        elif specifier == "visual":
            return self._new_element(obj, XAMusicVisual)


class XAMusicItemList(XABase.XAList):
    """A wrapper around lists of music items that employs fast enumeration techniques.

    All properties of music items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAMusicItem
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

    def by_container(self, container: XABase.XAObject) -> Union["XAMusicItem", None]:
        return self.by_property("container", container.xa_elem)

    def by_id(self, id: int) -> Union["XAMusicItem", None]:
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union["XAMusicItem", None]:
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union["XAMusicItem", None]:
        return self.by_property("name", name)

    def by_persistent_id(self, persistent_id: str) -> Union["XAMusicItem", None]:
        return self.by_property("persistentID", persistent_id)

    def by_properties(self, properties: dict) -> Union["XAMusicItem", None]:
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


class XAMusicItem(XABase.XAObject):
    """A generic class with methods common to the various playable media classes in media apps.

    .. seealso:: :class:`XAMusicSource`, :class:`XAMusicPlaylist`, :class:`XAMusicTrack`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_class(self):
        try:
            return MusicObjectClass(
                XABase.unOSType(self.xa_elem.objectClass().typeCodeValue())
            )
        except AttributeError:
            return MusicObjectClass.ITEM

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

    def download(self) -> "XAMusicItem":
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XAMusicItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> "XAMusicItem":
        """Reveals the item in the media apps window.

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


class XAMusicArtworkList(XAMusicItemList):
    """A wrapper around lists of music artworks that employs fast enumeration techniques.

    All properties of music artworks can be called as methods on the wrapped list, returning a list containing each artworks's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicArtwork)

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

    def by_data(self, data: XABase.XAImage) -> Union["XAMusicArtwork", None]:
        return self.by_property("data", data.xa_elem)

    def by_object_description(
        self, object_description: str
    ) -> Union["XAMusicArtwork", None]:
        return self.by_property("objectDescription", object_description)

    def by_downloaded(self, downloaded: bool) -> Union["XAMusicArtwork", None]:
        return self.by_property("downloaded", downloaded)

    def by_format(self, format: int) -> Union["XAMusicArtwork", None]:
        return self.by_property("format", format)

    def by_kind(self, kind: int) -> Union["XAMusicArtwork", None]:
        return self.by_property("kind", kind)

    def by_raw_data(self, raw_data: bytes) -> Union["XAMusicArtwork", None]:
        return self.by_property("rawData", raw_data)


class XAMusicArtwork(XAMusicItem):
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


class XAMusicAirPlayDeviceList(XAMusicItemList):
    """A wrapper around lists of AirPlay devices that employs fast enumeration techniques.

    All properties of AirPlay devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. seealso:: :class:`XAMusicAirPlayDevice`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAirPlayDevice)

    def active(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("active") or [])

    def available(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("available") or [])

    def kind(self) -> list[XAMusicApplication.DeviceKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("kind") or []
        return [
            XAMusicApplication.DeviceKind(XABase.OSType(x.stringValue())) for x in ls
        ]

    def network_address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("networkAddress") or [])

    def protected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("protected") or [])

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def supports_audio(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsAudio") or [])

    def supports_video(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsVideo") or [])

    def sound_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("soundVolume") or [])

    def by_active(self, active: bool) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("active", active)

    def by_available(self, available: bool) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("available", available)

    def by_kind(
        self, kind: XAMusicApplication.DeviceKind
    ) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("kind", event_from_str(XABase.unOSType(kind.value)))

    def by_network_address(
        self, network_address: str
    ) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("networkAddress", network_address)

    def by_protected(self, protected: bool) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("protected", protected)

    def by_selected(self, selected: bool) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("selected", selected)

    def by_supports_audio(
        self, supports_audio: bool
    ) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("supportsAudio", supports_audio)

    def by_supports_video(
        self, supports_video: bool
    ) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("supportsVideo", supports_video)

    def by_sound_volume(self, sound_volume: int) -> Union["XAMusicAirPlayDevice", None]:
        return self.by_property("soundVolume", sound_volume)

    def _format_for_filter(self, filter, value1, value2=None):
        if filter == "kind":
            if isinstance(value1, XAMusicApplication.DeviceKind):
                value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XAMusicAirPlayDevice(XAMusicItem):
    """An AirPlay device.

    .. seealso:: :class:`XAMusicAirPlayDeviceList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def active(self) -> bool:
        """Whether the device is currently being played to."""
        return self.xa_elem.active()

    @property
    def available(self) -> bool:
        """Whether the device is currently available."""
        return self.xa_elem.available()

    @property
    def kind(self) -> XAMusicApplication.DeviceKind:
        """The kind of the device."""
        return XAMusicApplication.DeviceKind(self.xa_elem.kind())

    @property
    def network_address(self) -> str:
        """The MAC address of the device."""
        return self.xa_elem.networkAddress()

    @property
    def protected(self) -> bool:
        """Whether the device is password/passcode protected."""
        return self.xa_elem.protected()

    @property
    def selected(self) -> bool:
        """Whether the device is currently selected."""
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property("selected", selected)

    @property
    def supports_audio(self) -> bool:
        """Whether the device supports audio playback."""
        return self.xa_elem.supportsAudio()

    @property
    def supports_video(self) -> bool:
        """Whether the device supports video playback."""
        return self.xa_elem.supportsVideo()

    @property
    def sound_volume(self) -> int:
        """The output volume for the device from 0 to 100."""
        return self.xa_elem.soundVolume()

    @sound_volume.setter
    def sound_volume(self, sound_volume: int):
        self.set_property("soundVolume", sound_volume)


class XAMusicEncoderList(XAMusicItemList):
    """A wrapper around lists of encoders that employs fast enumeration techniques.

    All properties of encoders can be called as methods on the wrapped list, returning a list containing each encoders's value for the property.

    .. seealso:: :class:`XAMusicEncoder`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEncoder)

    def format(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("format") or [])

    def by_format(self, format: str) -> Union["XAMusicEncoder", None]:
        return self.by_property("format", format)


class XAMusicEncoder(XAMusicItem):
    """An encoder in Music.app.

    .. seealso:: :class:`XAMusicEncoderList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def format(self) -> str:
        """The data format created by the encoder."""
        return self.xa_elem.format()


class XAMusicEQPresetList(XAMusicItemList):
    """A wrapper around lists of equalizer presets that employs fast enumeration techniques.

    All properties of equalizer presets can be called as methods on the wrapped list, returning a list containing each preset's value for the property.

    .. seealso:: :class:`XAMusicEQPreset`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEQPreset)

    def band1(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band1") or [])

    def band2(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band2") or [])

    def band3(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band3") or [])

    def band4(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band4") or [])

    def band5(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band5") or [])

    def band6(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band6") or [])

    def band7(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band7") or [])

    def band8(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band8") or [])

    def band9(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band9") or [])

    def band10(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("band10") or [])

    def modifiable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modifiable") or [])

    def preamp(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("preamp") or [])

    def update_tracks(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("updateTracks") or [])

    def by_band1(self, band1: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band1", band1)

    def by_band2(self, band2: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band2", band2)

    def by_band3(self, band3: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band3", band3)

    def by_band4(self, band4: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band4", band4)

    def by_band5(self, band5: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band5", band5)

    def by_band6(self, band6: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band6", band6)

    def by_band7(self, band7: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band7", band7)

    def by_band8(self, band8: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band8", band8)

    def by_band9(self, band9: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band9", band9)

    def by_band10(self, band10: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("band10", band10)

    def by_modifiable(self, modifiable: bool) -> Union["XAMusicEQPreset", None]:
        return self.by_property("modifiable", modifiable)

    def by_preamp(self, preamp: float) -> Union["XAMusicEQPreset", None]:
        return self.by_property("preamp", preamp)

    def by_update_tracks(self, update_tracks: bool) -> Union["XAMusicEQPreset", None]:
        return self.by_property("updateTracks", update_tracks)


class XAMusicEQPreset(XAMusicItem):
    """An equalizer preset in Music.app.

    .. seealso:: :class:`XAMusicEQPresetList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def band1(self) -> float:
        """The 32 Hz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band1()

    @band1.setter
    def band1(self, band1: float):
        self.set_property("band1", band1)

    @property
    def band2(self) -> float:
        """The 64 Hz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band2()

    @band2.setter
    def band2(self, band2: float):
        self.set_property("band2", band2)

    @property
    def band3(self) -> float:
        """The 125 HZ band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band3()

    @band3.setter
    def band3(self, band3: float):
        self.set_property("band3", band3)

    @property
    def band4(self) -> float:
        """The 250 Hz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band4()

    @band4.setter
    def band4(self, band4: float):
        self.set_property("band4", band4)

    @property
    def band5(self) -> float:
        """The 500 Hz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band5()

    @band5.setter
    def band5(self, band5: float):
        self.set_property("band5", band5)

    @property
    def band6(self) -> float:
        """The 1 kHz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band6()

    @band6.setter
    def band6(self, band6: float):
        self.set_property("band6", band6)

    @property
    def band7(self) -> float:
        """The 2 kHz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band7()

    @band7.setter
    def band7(self, band7: float):
        self.set_property("band7", band7)

    @property
    def band8(self) -> float:
        """The 4 kHz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band8()

    @band8.setter
    def band8(self, band8: float):
        self.set_property("band8", band8)

    @property
    def band9(self) -> float:
        """The 8 kHz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band9()

    @band9.setter
    def band9(self, band9: float):
        self.set_property("band9", band9)

    @property
    def band10(self) -> float:
        """The 16 kHz band level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.band10()

    @band10.setter
    def band10(self, band10: float):
        self.set_property("band10", band10)

    @property
    def modifiable(self) -> bool:
        """Whether the preset can be modified."""
        return self.xa_elem.modifiable()

    @property
    def preamp(self) -> float:
        """The equalizer preamp level (-12.0 dB to +12.0 dB)."""
        return self.xa_elem.preamp()

    @preamp.setter
    def preamp(self, preamp: float):
        self.set_property("preamp", preamp)

    @property
    def update_tracks(self) -> bool:
        """Whether tracks using the preset are updated when the preset is renamed or deleted."""
        return self.xa_elem.updateTracks()

    @update_tracks.setter
    def update_tracks(self, update_tracks: bool):
        self.set_property("updateTracks", update_tracks)


class XAMusicPlaylistList(XAMusicItemList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. seealso:: :class:`XAMusicPlaylist`

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAMusicPlaylist
        super().__init__(properties, filter, obj_class)

    def disliked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("disliked") or [])

    def loved(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loved") or [])

    def by_disliked(self, disliked: bool) -> Union["XAMusicPlaylist", None]:
        return self.by_property("disliked", disliked)

    def by_loved(self, loved: bool) -> Union["XAMusicPlaylist", None]:
        return self.by_property("loved", loved)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def duration(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("duration") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def parent(self) -> "XAMusicPlaylistList":
        ls = self.xa_elem.arrayByApplyingSelector_("parent") or []
        return self._new_element(ls, XAMusicPlaylistList)

    def size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def special_kind(self) -> list[XAMusicApplication.PlaylistKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("specialKind") or []
        return [
            XAMusicApplication.PlaylistKind(XABase.OSType(x.stringValue())) for x in ls
        ]

    def time(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("time") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def by_object_description(
        self, object_description: str
    ) -> Union["XAMusicPlaylist", None]:
        return self.by_property("objectDescription", object_description)

    def by_duration(self, duration: int) -> Union["XAMusicPlaylist", None]:
        return self.by_property("duration", duration)

    def by_name(self, name: str) -> Union["XAMusicPlaylist", None]:
        return self.by_property("name", name)

    def by_parent(self, parent: "XAMusicPlaylist") -> Union["XAMusicPlaylist", None]:
        return self.by_property("parent", parent.xa_elem)

    def by_size(self, size: int) -> Union["XAMusicPlaylist", None]:
        return self.by_property("size", size)

    def by_special_kind(
        self, special_kind: XAMusicApplication.PlaylistKind
    ) -> Union["XAMusicPlaylist", None]:
        return self.by_property(
            "specialKind", event_from_str(XABase.unOSType(special_kind.value))
        )

    def by_time(self, time: str) -> Union["XAMusicPlaylist", None]:
        return self.by_property("time", time)

    def by_visible(self, visible: bool) -> Union["XAMusicPlaylist", None]:
        return self.by_property("visible", visible)

    def push(
        self, *elements: list["XAMusicPlaylist"]
    ) -> Union["XAMusicPlaylist", list["XAMusicPlaylist"], None]:
        old_list = [x.id for x in self]
        super().push(*elements)
        new_list = [x.id for x in self if not x.id in old_list]
        if len(new_list) == 1:
            return self.by_id(new_list[0])
        return [self.by_id(id) for id in new_list]

    def _format_for_filter(self, filter, value1, value2=None):
        if filter == "special_kind" or filter == "specialKind":
            if isinstance(value1, XAMusicApplication.PlaylistKind):
                value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XAMusicPlaylist(XAMusicItem):
    """A playlist in Music.app.

    .. seealso:: :class:`XAMusicPlaylistList`, :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        if isinstance(self.xa_elem, ScriptingBridge.SBProxyByCode):
            return

        object_class = self.object_class
        if not hasattr(self, "xa_specialized"):
            if (
                object_class == MusicObjectClass.LIBRARY_PLAYLIST
                or self.special_kind == XAMusicApplication.PlaylistKind.LIBRARY
                or self.special_kind == XAMusicApplication.PlaylistKind.USER_LIBRARY
            ):
                self.__class__ = XAMusicLibraryPlaylist

            elif object_class == MusicObjectClass.FOLDER_PlAYLIST:
                self.__class__ = XAMusicFolderPlaylist

            elif object_class == MusicObjectClass.USER_PLAYLIST:
                self.__class__ = XAMusicUserPlaylist

            elif object_class == MusicObjectClass.SUBSCRIPTION_PLAYLIST:
                self.__class__ = XAMusicSubscriptionPlaylist

            elif object_class == MusicObjectClass.RADIO_TUNER_PLAYLIST:
                self.__class__ = XAMusicRadioTunerPlaylist

            elif object_class == MusicObjectClass.AUDIO_CD_PLAYLIST:
                self.__class__ = XAMusicAudioCDPlaylist

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
    def parent(self) -> "XAMusicPlaylist":
        """The folder containing the playlist, if any."""
        return self._new_element(self.xa_elem.parent(), XAMusicPlaylist)

    @property
    def size(self) -> int:
        """The total size of all tracks in the playlist in bytes."""
        return self.xa_elem.size()

    @property
    def special_kind(self) -> XAMusicApplication.PlaylistKind:
        """The special playlist kind."""
        return XAMusicApplication.PlaylistKind(self.xa_elem.specialKind())

    @property
    def time(self) -> str:
        """The length of all tracks in the playlist in MM:SS format."""
        return self.xa_elem.time()

    @property
    def visible(self) -> bool:
        """Whether the playlist is visible in the source list."""
        return self.xa_elem.visible()

    @property
    def disliked(self) -> bool:
        """Whether the playlist is disliked."""
        return self.xa_elem.disliked()

    @disliked.setter
    def disliked(self, disliked: bool):
        self.set_property("disliked", disliked)

    @property
    def loved(self) -> bool:
        """Whether the playlist is loved."""
        return self.xa_elem.loved()

    @loved.setter
    def loved(self, loved: bool):
        self.set_property("loved", loved)

    def search(
        self,
        query: str,
        type: Literal["all", "artists", "albums", "displayed", "tracks"] = "displayed",
    ):
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
                "element": result,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            items.append(XAMusicTrack(properties))
        return items

    def move(self, location: Union["XAMusicSource", "XAMusicFolderPlaylist"]):
        """Moves the playlist to the specified source or folder playlist.

        :param location: The source or folder playlist to move this playlist to
        :type location: Union[XAMusicSource, XAMusicPlaylist]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.moveTo_(location.xa_elem)

    def duplicate(
        self, location: Union["XAMusicSource", "XAMusicFolderPlaylist", None] = None
    ):
        """Duplicates the playlist to the specified source or folder playlist.

        :param location: The source or folder playlist to duplicate this playlist to, or None to duplicate into the parent of this playlist, defaults to None
        :type location: Union[XAMusicSource, XAMusicFolderPlaylist, None], optional

        .. versionadded:: 0.2.2
        """
        if location is None:
            location = self.xa_prnt
        self.xa_elem.duplicateTo_(location.xa_elem)

    def play(self):
        """Starts playback of the playlist, beginning with the first track in the list.

        .. versionadded:: 0.2.1
        """
        self.xa_elem.playOnce_(True)

    def add_tracks(self, *tracks: Union["XAMusicTrackList", list["XAMusicTrack"]]):
        """Add one or more tracks to this playlist.

        :param tracks: The list of tracks to add to this playlist
        :type tracks: Union[XAMusicTrackList, list[XAMusicTrack]]

        .. versionadded:: 0.2.2
        """
        if len(tracks) == 1 and isinstance(tracks[0], XAMusicTrackList):
            tracks = tracks[0].xa_elem
        elif len(tracks) == 1 and isinstance(tracks[0], list):
            tracks = [x.xa_elem for x in tracks[0]]
        else:
            tracks = [x.xa_elem for x in tracks]

        for track in tracks:
            track.duplicateTo_(self.xa_elem)

    def tracks(self, filter: Union[dict, None] = None) -> "XAMusicTrackList":
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMusicTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.tracks(), XAMusicTrackList, filter)

    def artworks(self, filter: Union[dict, None] = None) -> "XAMusicArtworkList":
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMusicArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.artworks(), XAMusicArtworkList, filter)


class XAMusicLibraryPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of library playlists that employs fast enumeration techniques.

    All properties of library playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicLibraryPlaylist)


class XAMusicLibraryPlaylist(XAMusicPlaylist):
    """The library playlist in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> "XAMusicFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.fileTracks(), XAMusicFileTrackList, filter
        )

    def url_tracks(self, filter: Union[dict, None] = None) -> "XAMusicURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XAMusicURLTrackList, filter)

    def shared_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMusicSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.sharedTracks(), XAMusicSharedTrackList, filter
        )


class XAMusicAudioCDPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of audio CD playlists that employs fast enumeration techniques.

    All properties of audio CD playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. seealso:: :class:`XAMusicAudioCDPlaylist`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAudioCDPlaylist)

    def artist(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("artist") or [])

    def compilation(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("compilation") or [])

    def composer(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("composer") or [])

    def disc_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("discCount") or [])

    def disc_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("discNumber") or [])

    def genre(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("genre") or [])

    def year(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("year") or [])

    def by_artist(self, artist: str) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("artist", artist)

    def by_compilation(
        self, compilation: bool
    ) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("composer", composer)

    def by_disc_count(self, disc_count: int) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("discNumber", disc_number)

    def by_genre(self, genre: str) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("genre", genre)

    def by_year(self, year: int) -> Union["XAMusicAudioCDPlaylist", None]:
        return self.by_property("year", year)


class XAMusicAudioCDPlaylist(XAMusicPlaylist):
    """An audio CD playlist in Music.app.

    .. seealso:: :class:`XAMusicAudioCDPlaylistList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def artist(self) -> str:
        """The artist of the CD."""
        return self.xa_elem.artist()

    @artist.setter
    def artist(self, artist: str):
        self.set_property("artist", artist)

    @property
    def compilation(self) -> bool:
        """Whether the CD is a compilation album."""
        return self.xa_elem.compilation()

    @compilation.setter
    def compilation(self, compilation: bool):
        self.set_property("compilation", compilation)

    @property
    def composer(self) -> str:
        """The composer of the CD."""
        return self.xa_elem.composer()

    @composer.setter
    def composer(self, composer: str):
        self.set_property("composer", composer)

    @property
    def disc_count(self) -> int:
        """The total number of discs in the CD's album."""
        return self.xa_elem.discCount()

    @disc_count.setter
    def disc_count(self, disc_count: int):
        self.set_property("discCount", disc_count)

    @property
    def disc_number(self) -> int:
        """The index of the CD disc in the source album."""
        return self.xa_elem.discNumber()

    @disc_number.setter
    def disc_number(self, disc_number: int):
        self.set_property("discNumber", disc_number)

    @property
    def genre(self) -> str:
        """The genre of the CD."""
        return self.xa_elem.genre()

    @genre.setter
    def genre(self, genre: str):
        self.set_property("genre", genre)

    @property
    def year(self) -> int:
        """The year the album was recorded/released."""
        return self.xa_elem.year()

    @year.setter
    def year(self, year: int):
        self.set_property("year", year)

    def audio_cd_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicAudioCDTrackList":
        """Returns a list of audio CD tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD tracks
        :rtype: XAMusicAudioCDTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.audioCDTracks(), XAMusicAudioCDTrackList, filter
        )


class XAMusicRadioTunerPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of radio tuner playlists that employs fast enumeration techniques.

    All properties of radio tuner playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. seealso:: :class:`XAMusicRadioTunerPlaylist`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicRadioTunerPlaylist)


class XAMusicRadioTunerPlaylist(XAMusicPlaylist):
    """A radio playlist in Music.app.

    .. seealso:: :class:`XAMusicRadioTunerPlaylistList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    def url_tracks(self, filter: Union[dict, None] = None) -> "XAMusicURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XAMusicURLTrackList, filter)


class XAMusicSourceList(XAMusicItemList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. seealso:: :class:`XAMusicSource`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSource)

    def capacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity") or [])

    def free_space(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace") or [])

    def kind(self) -> list[XAMusicApplication.SourceKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("kind") or []
        return [
            XAMusicApplication.SourceKind(XABase.OSType(x.stringValue())) for x in ls
        ]

    def by_capacity(self, capacity: int) -> Union["XAMusicSource", None]:
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union["XAMusicSource", None]:
        return self.by_property("freeSpace", free_space)

    def by_kind(
        self, kind: XAMusicApplication.SourceKind
    ) -> Union["XAMusicSource", None]:
        return self.by_property("kind", event_from_str(XABase.unOSType(kind.value)))

    def _format_for_filter(self, filter, value1, value2=None):
        if filter == "kind":
            if isinstance(value1, XAMusicApplication.SourceKind):
                value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XAMusicSource(XAMusicItem):
    """A media source in Music.app.

    .. seealso:: :class:`XAMusicSourceList`

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
    def kind(self) -> XAMusicApplication.SourceKind:
        """The source kind."""
        return XAMusicApplication.SourceKind(self.xa_elem.kind())

    def library_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicLibraryPlaylistList":
        """Returns a list of library playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned library playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of library playlists
        :rtype: XAMusicLibraryPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.libraryPlaylists(), XAMusicLibraryPlaylistList, filter
        )

    def playlists(self, filter: Union[dict, None] = None) -> "XAMusicPlaylistList":
        """Returns a list of playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlists
        :rtype: XAMusicPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.playlists(), XAMusicPlaylistList, filter)

    def user_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicUserPlaylistList":
        """Returns a list of user playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned user playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of user playlists
        :rtype: XAMusicUserPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.userPlaylists(), XAMusicUserPlaylistList, filter
        )

    def audio_cd_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicAudioCDPlaylistList":
        """Returns a list of audio CD playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD playlists
        :rtype: XAMusicAudioCDPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.audioCDPlaylists(), XAMusicAudioCDPlaylistList, filter
        )

    def radio_tuner_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicRadioTunerPlaylistList":
        """Returns a list of radio tuner playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned radio tuner playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio tuner playlists
        :rtype: XAMusicRadioTunerPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.radioTunerPlaylists(), XAMusicRadioTunerPlaylistList, filter
        )

    def subscription_playlists(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicSubscriptionPlaylistList":
        """Returns a list of subscription playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned subscription playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of subscription playlists
        :rtype: XAMusicSubscriptionPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.subscriptionPlaylists(),
            XAMusicSubscriptionPlaylistList,
            filter,
        )


class XAMusicSubscriptionPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of subscription playlists that employs fast enumeration techniques.

    All properties of subscription playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. seealso:: :class:`XAMusicSubscriptionPlaylist`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSubscriptionPlaylist)


class XAMusicSubscriptionPlaylist(XAMusicPlaylist):
    """A subscription playlist from Apple Music in Music.app.

    .. seealso:: :class:`XAMusicSubscriptionPlaylistList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)

    def file_tracks(self, filter: Union[dict, None] = None) -> "XAMusicFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.fileTracks(), XAMusicFileTrackList, filter
        )

    def url_tracks(self, filter: Union[dict, None] = None) -> "XAMusicURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XAMusicURLTrackList, filter)


class XAMusicTrackList(XAMusicItemList):
    """A wrapper around lists of music tracks that employs fast enumeration techniques.

    All properties of music tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. seealso:: :class:`XAMusicTrack`

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAMusicTrack
        super().__init__(properties, filter, obj_class)

    def album_artist(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("albumArtist") or [])

    def album_disliked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("albumDisliked") or [])

    def album_loved(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("albumLoved") or [])

    def artist(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("artist") or [])

    def bpm(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("bpm") or [])

    def cloud_status(self) -> list[XAMusicApplication.iCloudStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("cloudStatus") or []
        return [
            XAMusicApplication.iCloudStatus(XABase.OSType(x.stringValue())) for x in ls
        ]

    def compilation(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("compilation") or [])

    def composer(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("composer") or [])

    def disliked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("disliked") or [])

    def eq(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("EQ") or [])

    def gapless(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("gapless") or [])

    def loved(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loved") or [])

    def lyrics(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("lyrics") or [])

    def movement(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("movement") or [])

    def movement_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("movementCount") or [])

    def movement_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("movementNumber") or [])

    def shufflable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shufflable") or [])

    def sort_artist(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortArtist") or [])

    def sort_album_artist(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortAlbumArtist") or [])

    def sort_composer(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortComposer") or [])

    def work(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("work") or [])

    def album(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("album") or [])

    def album_rating(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("albumRating") or [])

    def album_rating_kind(self) -> list[XAMusicApplication.RatingKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("albumRatingKind") or []
        return [
            XAMusicApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls
        ]

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

    def media_kind(self) -> list[XAMusicApplication.MediaKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("mediaKind") or []
        return [
            XAMusicApplication.MediaKind(XABase.OSType(x.stringValue())) for x in ls
        ]

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

    def rating_kind(self) -> list[XAMusicApplication.RatingKind]:
        ls = self.xa_elem.arrayByApplyingSelector_("ratingKind") or []
        return [
            XAMusicApplication.RatingKind(XABase.OSType(x.stringValue())) for x in ls
        ]

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

    def by_album(self, album: str) -> Union["XAMusicTrack", None]:
        return self.by_property("album", album)

    def by_album_rating(self, album_rating: int) -> Union["XAMusicTrack", None]:
        return self.by_property("albumRating", album_rating)

    def by_album_rating_kind(
        self, album_rating_kind: XAMusicApplication.RatingKind
    ) -> Union["XAMusicTrack", None]:
        return self.by_property(
            "albumRatingKind", event_from_str(XABase.unOSType(album_rating_kind.value))
        )

    def by_bit_rate(self, bit_rate: int) -> Union["XAMusicTrack", None]:
        return self.by_property("bitRate", bit_rate)

    def by_bookmark(self, bookmark: float) -> Union["XAMusicTrack", None]:
        return self.by_property("bookmark", bookmark)

    def by_bookmarkable(self, bookmarkable: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("bookmarkable", bookmarkable)

    def by_category(self, category: str) -> Union["XAMusicTrack", None]:
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> Union["XAMusicTrack", None]:
        return self.by_property("comment", comment)

    def by_database_id(self, database_id: int) -> Union["XAMusicTrack", None]:
        return self.by_property("databaseID", database_id)

    def by_date_added(self, date_added: datetime) -> Union["XAMusicTrack", None]:
        return self.by_property("dateAdded", date_added)

    def by_object_description(
        self, object_description: str
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("objectDescription", object_description)

    def by_disc_count(self, disc_count: int) -> Union["XAMusicTrack", None]:
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union["XAMusicTrack", None]:
        return self.by_property("discNumber", disc_number)

    def by_downloader_apple_id(
        self, downloader_apple_id: str
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("downloaderAppleID", downloader_apple_id)

    def by_downloader_name(self, downloader_name: str) -> Union["XAMusicTrack", None]:
        return self.by_property("downloaderName", downloader_name)

    def by_duration(self, duration: float) -> Union["XAMusicTrack", None]:
        return self.by_property("duration", duration)

    def by_enabled(self, enabled: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("enabled", enabled)

    def by_episode_id(self, episode_id: str) -> Union["XAMusicTrack", None]:
        return self.by_property("episodeID", episode_id)

    def by_episode_number(self, episode_number: int) -> Union["XAMusicTrack", None]:
        return self.by_property("episodeNumber", episode_number)

    def by_finish(self, finish: float) -> Union["XAMusicTrack", None]:
        return self.by_property("finish", finish)

    def by_genre(self, genre: str) -> Union["XAMusicTrack", None]:
        return self.by_property("genre", genre)

    def by_grouping(self, grouping: str) -> Union["XAMusicTrack", None]:
        return self.by_property("grouping", grouping)

    def by_kind(self, kind: str) -> Union["XAMusicTrack", None]:
        return self.by_property("kind", kind)

    def by_long_description(self, long_description: str) -> Union["XAMusicTrack", None]:
        return self.by_property("longDescription", long_description)

    def by_media_kind(
        self, media_kind: XAMusicApplication.MediaKind
    ) -> Union["XAMusicTrack", None]:
        return self.by_property(
            "mediaKind", event_from_str(XABase.unOSType(media_kind.value))
        )

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("modificationDate", modification_date)

    def by_played_count(self, played_count: int) -> Union["XAMusicTrack", None]:
        return self.by_property("playedCount", played_count)

    def by_played_date(self, played_date: datetime) -> Union["XAMusicTrack", None]:
        return self.by_property("playedDate", played_date)

    def by_purchaser_apple_id(
        self, purchaser_apple_id: str
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("purchaserAppleID", purchaser_apple_id)

    def by_purchaser_name(self, purchaser_name: str) -> Union["XAMusicTrack", None]:
        return self.by_property("purchaserName", purchaser_name)

    def by_rating(self, rating: int) -> Union["XAMusicTrack", None]:
        return self.by_property("rating", rating)

    def by_rating_kind(
        self, rating_kind: XAMusicApplication.RatingKind
    ) -> Union["XAMusicTrack", None]:
        return self.by_property(
            "ratingKind", event_from_str(XABase.unOSType(rating_kind.value))
        )

    def by_release_date(self, release_date: datetime) -> Union["XAMusicTrack", None]:
        return self.by_property("releaseDate", release_date)

    def by_sample_rate(self, sample_rate: int) -> Union["XAMusicTrack", None]:
        return self.by_property("sampleRate", sample_rate)

    def by_season_number(self, season_number: int) -> Union["XAMusicTrack", None]:
        return self.by_property("seasonNumber", season_number)

    def by_skipped_count(self, skipped_count: int) -> Union["XAMusicTrack", None]:
        return self.by_property("skippedCount", skipped_count)

    def by_skipped_date(self, skipped_date: datetime) -> Union["XAMusicTrack", None]:
        return self.by_property("skippedDate", skipped_date)

    def by_show(self, show: str) -> Union["XAMusicTrack", None]:
        return self.by_property("show", show)

    def by_sort_album(self, sort_album: str) -> Union["XAMusicTrack", None]:
        return self.by_property("sortAlbum", sort_album)

    def by_sort_name(self, sort_name: str) -> Union["XAMusicTrack", None]:
        return self.by_property("sortName", sort_name)

    def by_sort_show(self, sort_show: str) -> Union["XAMusicTrack", None]:
        return self.by_property("sortShow", sort_show)

    def by_size(self, size: int) -> Union["XAMusicTrack", None]:
        return self.by_property("size", size)

    def by_start(self, start: float) -> Union["XAMusicTrack", None]:
        return self.by_property("start", start)

    def by_time(self, time: str) -> Union["XAMusicTrack", None]:
        return self.by_property("time", time)

    def by_track_count(self, track_count: int) -> Union["XAMusicTrack", None]:
        return self.by_property("trackCount", track_count)

    def by_track_number(self, track_number: int) -> Union["XAMusicTrack", None]:
        return self.by_property("trackNumber", track_number)

    def by_unplayed(self, unplayed: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("unplayed", unplayed)

    def by_volume_adjustment(
        self, volume_adjustment: int
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("volumeAdjustment", volume_adjustment)

    def by_year(self, year: int) -> Union["XAMusicTrack", None]:
        return self.by_property("year", year)

    def by_album_artist(self, album_artist: str) -> Union["XAMusicTrack", None]:
        return self.by_property("albumArtist", album_artist)

    def by_album_disliked(self, album_disliked: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("albumDisliked", album_disliked)

    def by_album_loved(self, album_loved: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("albumLoved", album_loved)

    def by_artist(self, artist: str) -> Union["XAMusicTrack", None]:
        return self.by_property("artist", artist)

    def by_bpm(self, bpm: int) -> Union["XAMusicTrack", None]:
        return self.by_property("bpm", bpm)

    def by_cloud_status(
        self, cloud_status: XAMusicApplication.iCloudStatus
    ) -> Union["XAMusicTrack", None]:
        return self.by_property(
            "cloudStatus", event_from_str(XABase.unOSType(cloud_status.value))
        )

    def by_compilation(self, compilation: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union["XAMusicTrack", None]:
        return self.by_property("composer", composer)

    def by_disliked(self, disliked: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("disliked", disliked)

    def by_eq(self, eq: str) -> Union["XAMusicTrack", None]:
        return self.by_property("EQ", eq)

    def by_gapless(self, gapless: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("gapless", gapless)

    def by_loved(self, loved: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("loved", loved)

    def by_lyrics(self, lyrics: str) -> Union["XAMusicTrack", None]:
        return self.by_property("lyrics", lyrics)

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("modificationDate", modification_date)

    def by_movement(self, movement: str) -> Union["XAMusicTrack", None]:
        return self.by_property("movement", movement)

    def by_movement_count(self, movement_count: int) -> Union["XAMusicTrack", None]:
        return self.by_property("movementCount", movement_count)

    def by_movement_number(self, movement_number: int) -> Union["XAMusicTrack", None]:
        return self.by_property("movementNumber", movement_number)

    def by_shufflable(self, shufflable: bool) -> Union["XAMusicTrack", None]:
        return self.by_property("shufflable", shufflable)

    def by_sort_artist(self, sort_artist: str) -> Union["XAMusicTrack", None]:
        return self.by_property("sortArtist", sort_artist)

    def by_sort_album_artist(
        self, sort_album_artist: str
    ) -> Union["XAMusicTrack", None]:
        return self.by_property("sortAlbumArtist", sort_album_artist)

    def by_sort_composer(self, sort_composer: str) -> Union["XAMusicTrack", None]:
        return self.by_property("sortComposer", sort_composer)

    def by_work(self, work: str) -> Union["XAMusicTrack", None]:
        return self.by_property("work", work)

    def _format_for_filter(self, filter, value1, value2=None):
        if filter in [
            "cloud_status",
            "cloudStatus",
            "album_rating_kind",
            "albumRatingKind",
            "media_kind",
            "mediaKind",
            "rating_kind",
            "ratingKind",
        ]:
            value1 = event_from_str(XABase.unOSType(value1.value))
        return super()._format_for_filter(filter, value1, value2)


class XAMusicTrack(XAMusicItem):
    """A class for managing and interacting with tracks in Music.app.

    .. seealso:: :class:`XAMusicTrackList`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        if not hasattr(self, "xa_specialized"):
            oldDict = self.__dict__.copy()
            if self.object_class == MusicObjectClass.SHARED_TRACK:
                self.__class__ = XAMusicSharedTrack

            elif self.object_class == MusicObjectClass.FILE_TRACK:
                self.__class__ = XAMusicFileTrack

            elif self.object_class == MusicObjectClass.URL_TRACK:
                self.__class__ = XAMusicURLTrack

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
    def album_rating_kind(self) -> XAMusicApplication.RatingKind:
        """The album's rating kind."""
        return XAMusicApplication.RatingKind(self.xa_elem.albumRatingKind())

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
    def media_kind(self) -> XAMusicApplication.MediaKind:
        """A description of the track's media type."""
        return XAMusicApplication.MediaKind(self.xa_elem.mediaKind())

    @media_kind.setter
    def media_kind(self, media_kind: XAMusicApplication.MediaKind):
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
    def rating_kind(self) -> XAMusicApplication.RatingKind:
        """Whether the rating is user-provided or computed."""
        return XAMusicApplication.RatingKind(self.xa_elem.ratingKind())

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
    def album_artist(self) -> str:
        """The album artist of the track."""
        return self.xa_elem.albumArtist()

    @album_artist.setter
    def album_artist(self, album_artist: str):
        self.set_property("albumArtist", album_artist)

    @property
    def album_disliked(self) -> bool:
        """Whether the album for the track is disliked."""
        return self.xa_elem.albumDisliked()

    @album_disliked.setter
    def album_disliked(self, album_disliked: bool):
        self.set_property("albumDisliked", album_disliked)

    @property
    def album_loved(self) -> bool:
        """Whether the album for the track is loved."""
        return self.xa_elem.albumLoved()

    @album_loved.setter
    def album_loved(self, album_loved: bool):
        self.set_property("albumLoved", album_loved)

    @property
    def artist(self) -> str:
        """The artist/source of the track."""
        return self.xa_elem.artist()

    @artist.setter
    def artist(self, artist: str):
        self.set_property("artist", artist)

    @property
    def bpm(self) -> int:
        """The tempo of the track in beats per minute."""
        return self.xa_elem.bpm()

    @bpm.setter
    def bpm(self, bpm: int):
        self.set_property("bpm", bpm)

    @property
    def cloud_status(self) -> XAMusicApplication.iCloudStatus:
        """The iCloud status of the track."""
        return XAMusicApplication.iCloudStatus(self.xa_elem.cloudStatus())

    @property
    def compilation(self) -> bool:
        """Whether the track is from a compilation album."""
        return self.xa_elem.compilation()

    @compilation.setter
    def compilation(self, compilation: bool):
        self.set_property("compilation", compilation)

    @property
    def composer(self) -> str:
        """The composer of the track."""
        return self.xa_elem.composer()

    @composer.setter
    def composer(self, composer: str):
        self.set_property("composer", composer)

    @property
    def disliked(self) -> bool:
        """Whether the track is disliked."""
        return self.xa_elem.disliked()

    @disliked.setter
    def disliked(self, disliked: bool):
        self.set_property("disliked", disliked)

    @property
    def eq(self) -> str:
        """The name of the EQ preset of the track."""
        return self.xa_elem.EQ()

    @eq.setter
    def eq(self, eq: str):
        self.set_property("EQ", eq)

    @property
    def gapless(self) -> bool:
        """Whether the track is a from a gapless album."""
        return self.xa_elem.gapless()

    @gapless.setter
    def gapless(self, gapless: bool):
        self.set_property("gapless", gapless)

    @property
    def loved(self) -> bool:
        """Whether the track is loved."""
        return self.xa_elem.loved()

    @loved.setter
    def loved(self, loved: bool):
        self.set_property("loved", loved)

    @property
    def lyrics(self) -> str:
        """The lyrics of the track."""
        return self.xa_elem.lyrics()

    @lyrics.setter
    def lyrics(self, lyrics: str):
        self.set_property("lyrics", lyrics)

    @property
    def movement(self) -> str:
        """The movement name of the track."""
        return self.xa_elem.movement()

    @movement.setter
    def movement(self, movement: str):
        self.set_property("movement", movement)

    @property
    def movement_count(self) -> int:
        """The total number of movements in the work."""
        return self.xa_elem.movementCount()

    @movement_count.setter
    def movement_count(self, movement_count: int):
        self.set_property("movementCount", movement_count)

    @property
    def movement_number(self) -> int:
        """The index of the movement in the work."""
        return self.xa_elem.movementNumber()

    @movement_number.setter
    def movement_number(self, movement_number: int):
        self.set_property("movementNumber", movement_number)

    @property
    def shufflable(self) -> bool:
        """Whether the track is included when shuffling."""
        return self.xa_elem.shufflable()

    @shufflable.setter
    def shufflable(self, shufflable: bool):
        self.set_property("shufflable", shufflable)

    @property
    def sort_artist(self) -> str:
        """The string used for this track when sorting by artist."""
        return self.xa_elem.sortArtist()

    @sort_artist.setter
    def sort_artist(self, sort_artist: str):
        self.set_property("sortArtist", sort_artist)

    @property
    def sort_album_artist(self) -> str:
        """The string used for this track when sorting by album artist."""
        return self.xa_elem.sortAlbumArtist()

    @sort_album_artist.setter
    def sort_album_artist(self, sort_album_artist: str):
        self.set_property("sortAlbumArtist", sort_album_artist)

    @property
    def sort_composer(self) -> str:
        """The string used for this track when sorting by composer."""
        return self.xa_elem.sortComposer()

    @sort_composer.setter
    def sort_composer(self, sort_composer: str):
        self.set_property("sortComposer", sort_composer)

    @property
    def work(self) -> str:
        """The work name of the track."""
        return self.xa_elem.work()

    @work.setter
    def work(self, work: str):
        self.set_property("work", work)

    def move(self, location: Union[XAMusicPlaylist, XAMusicSource]):
        """Moves the track to the specified location, copying it if appropriate.

        :param location: The playlist or source to move the track to
        :type location: Union[XAMusicPlaylist, XAMusicSource]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.moveTo_(location.xa_elem)

    def duplicate(self, location: Union[XAMusicPlaylist, XAMusicSource]):
        """Duplicates the track at the specified location.

        :param location: The location to duplicate the track to
        :type location: Union[XAMusicPlaylist, XAMusicSource]

        .. versionadded:: 0.2.2
        """
        self.xa_elem.duplicateTo_(location.xa_elem)

    def select(self) -> "XAMusicItem":
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XAMusicTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self

    def play(self) -> "XAMusicItem":
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XAMusicItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self

    def artworks(self, filter: Union[dict, None] = None) -> "XAMusicArtworkList":
        """Returns a list of artworks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned artworks will have, or None
        :type filter: Union[dict, None]
        :return: The list of artworks
        :rtype: XAMusicArtworkList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.artworks(), XAMusicArtworkList, filter)


class XAMusicFileTrackList(XAMusicTrackList):
    """A wrapper around lists of music file tracks that employs fast enumeration techniques.

    All properties of music file tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicFileTrack)

    def location(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("location") or []
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union["XAMusicFileTrack", None]:
        return self.by_property("location", location.xa_elem)


class XAMusicFileTrack(XAMusicTrack):
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


class XAMusicSharedTrackList(XAMusicTrackList):
    """A wrapper around lists of music shared tracks that employs fast enumeration techniques.

    All properties of music shared tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSharedTrack)


class XAMusicSharedTrack(XAMusicTrack):
    """A shared track in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAMusicAudioCDTrackList(XAMusicTrackList):
    """A wrapper around lists of music audio CD tracks that employs fast enumeration techniques.

    All properties of music audio CD tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. seealso:: :class:`XAMusicAudioCDTrack`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAudioCDTrack)

    def location(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("location") or []
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union["XAMusicAudioCDTrack", None]:
        return self.by_property("location", location.xa_elem)


class XAMusicAudioCDTrack(XAMusicTrack):
    """An audio CD track in Music.app.

    .. seealso:: :class:`XAMusicAudioCDTrackList`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def location(self) -> XABase.XAPath:
        """The location of the file represented by the track."""
        return XABase.XAPath(self.xa_elem.location())

    @location.setter
    def location(self, location: XABase.XAPath):
        self.set_property("location", location.xa_elem)


class XAMusicURLTrackList(XAMusicTrackList):
    """A wrapper around lists of music URL tracks that employs fast enumeration techniques.

    All properties of music URL tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicURLTrack)

    def address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("address") or [])

    def by_address(self, address: str) -> Union["XAMusicURLTrack", None]:
        return self.by_property("address", address)


class XAMusicURLTrack(XAMusicTrack):
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


class XAMusicUserPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of music user playlists that employs fast enumeration techniques.

    All properties of music user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. seealso:: :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicUserPlaylist)

    def genius(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("genius") or [])

    def shared(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared") or [])

    def smart(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("smart") or [])

    def by_shared(self, shared: bool) -> Union["XAMusicUserPlaylist", None]:
        return self.by_property("shared", shared)

    def by_smart(self, smart: bool) -> Union["XAMusicUserPlaylist", None]:
        return self.by_property("smart", smart)

    def by_genius(self, genius: bool) -> Union["XAMusicUserPlaylist", None]:
        return self.by_property("genius", genius)


class XAMusicUserPlaylist(XAMusicPlaylist):
    """A user-created playlist in Music.app.

    .. seealso:: :class:`XAMusicUserPlaylistList`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def genius(self) -> bool:
        """Whether the playlist is a genius playlist."""
        return self.xa_elem.genius()

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

    def file_tracks(self, filter: Union[dict, None] = None) -> "XAMusicFileTrackList":
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: XAMusicFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.fileTracks(), XAMusicFileTrackList, filter
        )

    def url_tracks(self, filter: Union[dict, None] = None) -> "XAMusicURLTrackList":
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: XAMusicURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.URLTracks(), XAMusicURLTrackList, filter)

    def shared_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAMusicSharedTrackList":
        """Returns a list of shared tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shared tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of shared tracks
        :rtype: XAMusicSharedTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_elem.sharedTracks(), XAMusicSharedTrackList, filter
        )


class XAMusicFolderPlaylistList(XAMusicUserPlaylistList):
    """A wrapper around lists of music folder playlists that employs fast enumeration techniques.

    All properties of music folder playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicFolderPlaylist)


class XAMusicFolderPlaylist(XAMusicUserPlaylist):
    """A folder playlist in media apps.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAMusicVisualList(XAMusicItemList):
    """A wrapper around lists of music visuals that employs fast enumeration techniques.

    All properties of music visuals can be called as methods on the wrapped list, returning a list containing each visual's value for the property.

    .. seealso:: :class:`XAMusicVisual`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicVisual)


class XAMusicVisual(XAMusicPlaylist):
    """A music visual in Music.app.

    .. seealso:: :class:`XAMusicVisualList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAMusicWindowList(XAMusicItemList):
    """A wrapper around lists of music windows that employs fast enumeration techniques.

    All properties of music windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. seealso:: :class:`XAMusicWindow`

    .. versionadded:: 0.0.7
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAMusicWindow
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
    ) -> Union["XAMusicWindow", None]:
        # TODO
        return self.by_property("bounds", bounds)

    def by_closeable(self, closeable: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("closeable", closeable)

    def by_collapseable(self, collapseable: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("collapseable", collapseable)

    def by_collapsed(self, collapsed: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("collapsed", collapsed)

    def by_full_screen(self, full_screen: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("fullScreen", full_screen)

    def by_position(self, position: tuple[int, int]) -> Union["XAMusicWindow", None]:
        # TODO
        return self.by_property("position", position)

    def by_resizable(self, resizable: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union["XAMusicWindow", None]:
        return self.by_property("zoomed", zoomed)


class XAMusicWindow(XABaseScriptable.XASBWindow, XAMusicItem):
    """A window of Music.app.

    .. seealso:: :class:`XAMusicWindowList`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

        obj_class = self.object_class
        if not hasattr(self, "xa_specialized"):
            new_self = None
            if obj_class == MusicObjectClass.BROWSER_WINDOW:
                new_self = self._new_element(self.xa_elem, XAMusicBrowserWindow)
            elif obj_class == MusicObjectClass.PLAYLIST_WINDOW:
                new_self = self._new_element(self.xa_elem, XAMusicPlaylistWindow)
            elif obj_class == MusicObjectClass.VIDEO_WINDOW:
                new_self = self._new_element(self.xa_elem, XAMusicVideoWindow)
            elif obj_class == MusicObjectClass.MINIPLAYER_WINDOW:
                new_self = self._new_element(self.xa_elem, XAMusicMiniplayerWindow)
            elif obj_class == MusicObjectClass.EQ_WINDOW:
                new_self = self._new_element(self.xa_elem, XAMusicEQWindow)

            if new_self is not None:
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)

            self.xa_specialized = True

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


class XAMusicBrowserWindowList(XAMusicWindowList):
    """A wrapper around lists of music browser windows that employs fast enumeration techniques.

    All properties of music browser windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicBrowserWindow)

    def selection(self) -> XAMusicTrackList:
        ls = self.xa_elem.arrayByApplyingSelector_("selection") or []
        return self._new_element(ls, XAMusicTrackList)

    def view(self) -> XAMusicPlaylistList:
        ls = self.xa_elem.arrayByApplyingSelector_("view") or []
        return self._new_element(ls, XAMusicPlaylistList)

    def by_selection(
        self, selection: XAMusicTrackList
    ) -> Union["XAMusicPlaylistWindow", None]:
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMusicPlaylist) -> Union["XAMusicPlaylistWindow", None]:
        return self.by_property("view", view.xa_elem)


class XAMusicBrowserWindow(XAMusicWindow):
    """A browser window of media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def selection(self) -> XAMusicTrackList:
        """The selected tracks."""
        return self._new_element(self.xa_elem.selection(), XAMusicTrackList)

    @property
    def view(self) -> XAMusicPlaylist:
        """The playlist currently displayed in the window."""
        return self._new_element(self.xa_elem.view(), XAMusicPlaylist)


class XAMusicPlaylistWindowList(XAMusicWindowList):
    """A wrapper around lists of music playlist windows that employs fast enumeration techniques.

    All properties of music playlist windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicPlaylistWindow)

    def selection(self) -> XAMusicTrackList:
        ls = self.xa_elem.arrayByApplyingSelector_("selection") or []
        return self._new_element(ls, XAMusicTrackList)

    def view(self) -> XAMusicPlaylistList:
        ls = self.xa_elem.arrayByApplyingSelector_("view") or []
        return self._new_element(ls, XAMusicPlaylistList)

    def by_selection(
        self, selection: XAMusicTrackList
    ) -> Union["XAMusicPlaylistWindow", None]:
        return self.by_property("selection", selection.xa_elem)

    def by_view(self, view: XAMusicPlaylist) -> Union["XAMusicPlaylistWindow", None]:
        return self.by_property("view", view.xa_elem)


class XAMusicPlaylistWindow(XAMusicWindow):
    """A playlist window in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def selection(self) -> XAMusicTrackList:
        """The selected tracks."""
        return self._new_element(self.xa_elem.selection(), XAMusicTrackList)

    @property
    def view(self) -> XAMusicPlaylist:
        """The playlist currently displayed in the window."""
        return self._new_element(self.xa_elem.view(), XAMusicPlaylist)


class XAMusicVideoWindowList(XAMusicWindowList):
    """A wrapper around lists of music video windows that employs fast enumeration techniques.

    All properties of music video windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicVideoWindow)


class XAMusicVideoWindow(XAMusicWindow):
    """A video window in media apps.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAMusicEQWindowList(XAMusicWindowList):
    """A wrapper around lists of music equalizer windows that employs fast enumeration techniques.

    All properties of music equalizer windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. seealso:: :class:`XAMusicEQWindow`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEQWindow)


class XAMusicEQWindow(XAMusicWindow):
    """An equalizer window in Music.app.

    .. seealso:: :class:`XAMusicEQWindowList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAMusicMiniplayerWindowList(XAMusicWindowList):
    """A wrapper around lists of music miniplayer windows that employs fast enumeration techniques.

    All properties of music minipplayer windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. seealso:: :class:`XAMusicMiniplayerWindow`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicMiniplayerWindow)


class XAMusicMiniplayerWindow(XAMusicWindow):
    """A miniplayer window in Music.app.

    .. seealso:: :class:`XAMusicMiniplayerWindowList`

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties):
        super().__init__(properties)
