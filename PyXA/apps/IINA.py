""".. versionadded:: 0.2.2

Control IINA+ (https://github.com/CarterLi/iina) using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from PyXA.XAProtocols import XACanOpenPath, XACloseable
from PyXA.XAEvents import event_from_str


class IINAObjectClass(Enum):
    APPLICATION = "capp"
    WINDOW = "cwin"
    PLAYER = "cPla"
    TRACK = "cTra"
    VIDEO_TRACK = "cTrV"
    AUDIO_TRACK = "cTrA"
    SUBTITLE_TRACK = "cTrS"
    PLAYLIST_ITEM = "cPLI"


class XAIINAApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with IINA.app.

    .. versionadded:: 0.2.2
    """

    class PlayerState(Enum):
        """States of a player."""

        PLAYING = XABase.OSType("kPSP")  #: Playback is playing
        PAUSED = XABase.OSType("kPSp")  #: Playback is paused
        SEEKING = XABase.OSType("kPSS")  #: The player is seeking

    class TrackType(Enum):
        """States of a player."""

        VIDEO = XABase.OSType("kTTV")  #: Video track
        AUDIO = XABase.OSType("kTTA")  #: Audio track
        SUBTITLE = XABase.OSType("kTTS")  #: Subtitle track

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Is IINA the active application?"""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of the application."""
        return self.xa_scel.version()

    def play(self):
        """Begin or resume playback.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.play()

    def pause(self):
        """Pause playback.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.pause()

    def playpause(self):
        """Toggle the playing/paused state of the player.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.playpause()

    def next_item(self):
        """Advance to the next playlist item.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.nextItem()

    def previous_item(self):
        """Return to the previous playlist item.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.previousItem()

    def next_frame(self):
        """Advance to the next frame.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.nextFrame()

    def previous_frame(self):
        """Return to the previous frame.

        .. versionadded:: 0.2.2
        """
        self.xa_scel.previousFrame()

    def players(self, filter: Union[dict, None] = None) -> "XAIINAPlayerList":
        """Returns a list of players, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned players will have, or None
        :type filter: Union[dict, None]
        :return: The list of players
        :rtype: XAIINAPlayerList

        .. versionadded:: 0.2.2
        """
        return self._new_element(self.xa_scel.players(), XAIINAPlayerList, filter)


class XAIINAPlayerList(XABase.XAList):
    """A wrapper around lists of players that employs fast enumeration techniques.

    All properties of players can be called as methods on the wrapped list, returning a list containing each player's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINAPlayer, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def state(self) -> list[XAIINAApplication.PlayerState]:
        ls = self.xa_elem.arrayByApplyingSelector_("state") or []
        return [
            XAIINAApplication.PlayerState(XABase.OSType(x.stringValue())) for x in ls
        ]

    def playback_speed(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("playbackSpeed") or [])

    def file_loop(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileLoop") or [])

    def audio_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("audioVolume") or [])

    def muted(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("muted") or [])

    def position(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("position") or [])

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAPath(x) for x in ls]

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("sampleRate") or []
        return [XABase.XAURL(x) for x in ls]

    def music_mode(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("musicMode") or [])

    def fullscreen(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullscreen") or [])

    def window(self) -> XABaseScriptable.XASBWindowList:
        ls = self.xa_elem.arrayByApplyingSelector_("window") or []
        return self._new_element(ls, XABaseScriptable.XASBWindowList)

    def current_video_track(self) -> "XAIINAVideoTrackList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentVideoTrack") or []
        return self._new_element(ls, XAIINAVideoTrackList)

    def current_audio_track(self) -> "XAIINAAudioTrackList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentAudioTrack") or []
        return self._new_element(ls, XAIINAAudioTrackList)

    def current_subtitle_track(self) -> "XAIINASubtitleTrackList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentSubtitleTrack") or []
        return self._new_element(ls, XAIINASubtitleTrackList)

    def second_subtitle_track(self) -> "XAIINASubtitleTrackList":
        ls = self.xa_elem.arrayByApplyingSelector_("secondSubtitleTrack") or []
        return self._new_element(ls, XAIINASubtitleTrackList)

    def aspect_ratio(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("aspectRatio") or [])

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation") or [])

    def mirrored(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("mirrored") or [])

    def flipped(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("flipped") or [])

    def pip(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("pip") or [])

    def current_playlist_item(self) -> "XAIINAPlaylistItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentPlaylistItem") or []
        return self._new_element(ls, XAIINAPlaylistItemList)

    def by_id(self, id: str) -> Union["XAIINAPlayer", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XAIINAPlayer", None]:
        return self.by_property("name", name)

    def by_state(
        self, state: XAIINAApplication.PlayerState
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("state", event_from_str(XABase.unOSType(state.value)))

    def by_playback_speed(self, playback_speed: float) -> Union["XAIINAPlayer", None]:
        return self.by_property("playbackSpeed", playback_speed)

    def by_file_loop(self, file_loop: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("fileLoop", file_loop)

    def by_audio_volume(self, audio_volume: int) -> Union["XAIINAPlayer", None]:
        return self.by_property("audioVolume", audio_volume)

    def by_muted(self, muted: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("muted", muted)

    def by_position(self, position: float) -> Union["XAIINAPlayer", None]:
        return self.by_property("position", position)

    def by_file(self, file: Union[XABase.XAPath, str]) -> Union["XAIINAPlayer", None]:
        if isinstance(file, str):
            file = XABase.XAPath(file)
        return self.by_property("file", file.xa_elem)

    def by_url(self, url: Union[XABase.XAURL, str]) -> Union["XAIINAPlayer", None]:
        if isinstance(url, str):
            url = XABase.XAURL(url)
        return self.by_property("URL", url.xa_elem)

    def by_music_mode(self, music_mode: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("musicMode", music_mode)

    def by_fullscreen(self, fullscreen: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("fullscreen", fullscreen)

    def by_window(
        self, window: XABaseScriptable.XASBWindow
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("window", window.xa_elem)

    def by_aspect_ratio(self, aspect_ratio: str) -> Union["XAIINAPlayer", None]:
        return self.by_property("aspectRatio", aspect_ratio)

    def by_rotation(self, rotation: int) -> Union["XAIINAPlayer", None]:
        return self.by_property("rotation", rotation)

    def by_mirrored(self, mirrored: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("mirrored", mirrored)

    def by_flipped(self, flipped: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("flipped", flipped)

    def by_pip(self, pip: bool) -> Union["XAIINAPlayer", None]:
        return self.by_property("pip", pip)

    def by_current_video_track(
        self, current_video_track: "XAIINAVideoTrack"
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("currentVideoTrack", current_video_track)

    def by_current_audio_track(
        self, current_audio_track: "XAIINAAudioTrack"
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("currentAudioTrack", current_audio_track)

    def by_current_subtitle_track(
        self, current_subtitle_track: "XAIINASubtitleTrack"
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("currentSubtitleTrack", current_subtitle_track)

    def by_second_subtitle_track(
        self, second_subtitle_track: "XAIINASubtitleTrack"
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("secondSubtitleTrack", second_subtitle_track)

    def by_current_playlist_item(
        self, current_playlist_item: "XAIINAPlaylistItem"
    ) -> Union["XAIINAPlayer", None]:
        return self.by_property("currentPlaylistItem", current_playlist_item)


class XAIINAPlayer(XABase.XAObject, XACloseable):
    """A player in IINA.app.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique ID of the player."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the player."""
        return self.xa_elem.name()

    @property
    def state(self) -> XAIINAApplication.PlayerState:
        """The playback state."""
        return XAIINAApplication.PlayerState(self.xa_elem.state())

    @property
    def playback_speed(self) -> float:
        """The playback speed."""
        return self.xa_elem.playbackSpeed()

    @playback_speed.setter
    def playback_speed(self, playback_speed: float):
        self.set_property("playbackSpeed", playback_speed)

    @property
    def file_loop(self) -> bool:
        """The file loop setting (whether the file should loop continuously)."""
        return self.xa_elem.fileLoop()

    @file_loop.setter
    def file_loop(self, file_loop: bool):
        self.set_property("fileLoop", file_loop)

    @property
    def audio_volume(self) -> int:
        """The audio output volume (0 = minimum, 150 = maximum, 100 = normal)."""
        return self.xa_elem.audioVolume()

    @audio_volume.setter
    def audio_volume(self, audio_volume: int):
        self.set_property("audioVolume", audio_volume)

    @property
    def muted(self) -> bool:
        """Has the audio output been muted?"""
        return self.xa_elem.muted()

    @muted.setter
    def muted(self, muted: bool):
        self.set_property("muted", muted)

    @property
    def position(self) -> float:
        """The playback position in seconds."""
        return self.xa_elem.position()

    @position.setter
    def position(self, position: float):
        self.set_property("position", position)

    @property
    def file(self) -> XABase.XAPath:
        """The currently playing file."""
        return XABase.XAPath(self.xa_elem.file())

    @property
    def url(self) -> XABase.XAURL:
        """The currently playing URL."""
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def music_mode(self) -> bool:
        """Is the playing in music mode?"""
        return self.xa_elem.musicMode()

    @music_mode.setter
    def music_mode(self, music_mode: bool):
        self.set_property("musicMode", music_mode)

    @property
    def fullscreen(self) -> bool:
        """Is the player in fullscreen?"""
        return self.xa_elem.fullscreen()

    @fullscreen.setter
    def fullscreen(self, fullscreen: bool):
        self.set_property("fullscreen", fullscreen)

    @property
    def window(self) -> XABaseScriptable.XASBWindow:
        """The player's currently visible window."""
        return self._new_element(self.xa_elem.window(), XABaseScriptable.XASBWindow)

    @property
    def aspect_ratio(self) -> str:
        """The current aspect ratio."""
        return self.xa_elem.aspectRatio()

    @aspect_ratio.setter
    def aspect_ratio(self, aspect_ratio: str):
        self.set_property("aspectRatio", aspect_ratio)

    @property
    def rotation(self) -> int:
        """The current video rotation in degrees."""
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property("rotation", rotation)

    @property
    def mirrored(self) -> bool:
        """Whether the video is mirrored (horizontally)."""
        return self.xa_elem.mirrored()

    @mirrored.setter
    def mirrored(self, mirrored: bool):
        self.set_property("mirrored", mirrored)

    @property
    def flipped(self) -> bool:
        """Whether the video is flipped (vertically)."""
        return self.xa_elem.flipped()

    @flipped.setter
    def flipped(self, flipped: bool):
        self.set_property("flipped", flipped)

    @property
    def pip(self) -> bool:
        """Is the player in picture-in-picture mode? (macOS 10.12+)"""
        return self.xa_elem.pip()

    @pip.setter
    def pip(self, pip: bool):
        self.set_property("pip", pip)

    @property
    def current_video_track(self) -> "XAIINAVideoTrack":
        """The index of the current video track."""
        return self._new_element(self.xa_elem.currentVideoTrack(), XAIINAVideoTrack)

    @current_video_track.setter
    def current_video_track(self, current_video_track: "XAIINAVideoTrack"):
        self.set_property("currentVideoTrack", current_video_track.xa_elem)

    @property
    def current_audio_track(self) -> "XAIINAAudioTrack":
        """The index of the current audio track."""
        return self._new_element(self.xa_elem.currentAudioTrack(), XAIINAAudioTrack)

    @current_audio_track.setter
    def current_audio_track(self, current_audio_track: "XAIINAAudioTrack"):
        self.set_property("currentAudiotrack", current_audio_track.xa_elem)

    @property
    def current_subtitle_track(self) -> "XAIINASubtitleTrack":
        """The index of the current subtitle track."""
        return self._new_element(
            self.xa_elem.currentSubtitleTrack(), XAIINASubtitleTrack
        )

    @current_subtitle_track.setter
    def current_subtitle_track(self, current_subtitle_track: "XAIINASubtitleTrack"):
        self.set_property("currentSubtitleTrack", current_subtitle_track.xa_elem)

    @property
    def second_subtitle_track(self) -> "XAIINASubtitleTrack":
        """The index of the second subtitle track."""
        return self._new_element(
            self.xa_elem.secondSubtitleTrack(), XAIINASubtitleTrack
        )

    @second_subtitle_track.setter
    def second_subtitle_track(self, second_subtitle_track: "XAIINASubtitleTrack"):
        self.set_property("secondSubtitleTrack", second_subtitle_track.xa_elem)

    @property
    def current_playlist_item(self) -> "XAIINAPlaylistItem":
        """The current playlist item."""
        return self._new_element(self.xa_elem.currentPlaylistItem(), XAIINAPlaylistItem)

    @current_playlist_item.setter
    def current_playlist_item(self, current_playlist_item: "XAIINAPlaylistItem"):
        self.set_property("currentPlaylistItem", current_playlist_item.xa_elem)

    def tracks(self, filter: Union[dict, None] = None) -> "XAIINATrackList":
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAIINATrackList

        .. versionadded:: 0.2.2
        """
        return self._new_element(self.xa_elem.tracks(), XAIINATrackList, filter)

    def video_tracks(self, filter: Union[dict, None] = None) -> "XAIINAVideoTrackList":
        """Returns a list of video tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of video tracks
        :rtype: XAIINAVideoTrackList

        .. versionadded:: 0.2.2
        """
        return self._new_element(
            self.xa_elem.videoTracks(), XAIINAVideoTrackList, filter
        )

    def audio_tracks(self, filter: Union[dict, None] = None) -> "XAIINAAudioTrackList":
        """Returns a list of audio tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio tracks
        :rtype: XAIINAAudioTrackList

        .. versionadded:: 0.2.2
        """
        return self._new_element(
            self.xa_elem.audioTracks(), XAIINAAudioTrackList, filter
        )

    def subtitle_tracks(
        self, filter: Union[dict, None] = None
    ) -> "XAIINASubtitleTrackList":
        """Returns a list of subtitle tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned subtitle tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of subtitle tracks
        :rtype: XAIINASubtitleTrackList

        .. versionadded:: 0.2.2
        """
        return self._new_element(
            self.xa_elem.subtitleTracks(), XAIINASubtitleTrackList, filter
        )

    def playlist_items(
        self, filter: Union[dict, None] = None
    ) -> "XAIINAPlaylistItemList":
        """Returns a list of playlist items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned playlist items will have, or None
        :type filter: Union[dict, None]
        :return: The list of playlist items
        :rtype: XAIINAPlaylistItemList

        .. versionadded:: 0.2.2
        """
        return self._new_element(
            self.xa_elem.playlistItems(), XAIINAPlaylistItemList, filter
        )

    def play(self):
        """Begin or resume playback.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.play()

    def pause(self):
        """Pause playback.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.pause()

    def playpause(self):
        """Toggle the playing/paused state of the player.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.playpause()

    def next_item(self):
        """Advance to the next playlist item.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.nextItem()

    def previous_item(self):
        """Return to the previous playlist item.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.previousItem()

    def next_frame(self):
        """Advance to the next frame.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.nextFrame()

    def previous_frame(self):
        """Return to the previous frame.

        .. versionadded:: 0.2.2
        """
        self.xa_elem.previousFrame()


class XAIINATrackList(XABase.XAList):
    """A wrapper around lists of tracks that employs fast enumeration techniques.

    All properties of tracks can be called as methods on the wrapped list, returning a list containing each tracks's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINATrack, filter)

    def type(self) -> list[XAIINAApplication.TrackType]:
        ls = self.xa_elem.arrayByApplyingSelector_("type") or []
        return [XAIINAApplication.TrackType(XABase.OSType(x.stringValue())) for x in ls]

    def codec(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("codec") or [])

    def language(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("language") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def info_string(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("infoString") or [])

    def default(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("default") or [])

    def by_type(self, type: XAIINAApplication.TrackType) -> Union["XAIINATrack", None]:
        return self.by_property("type", event_from_str(XABase.unOSType(type.value)))

    def by_codec(self, codec: str) -> Union["XAIINATrack", None]:
        return self.by_property("codec", codec)

    def by_language(self, language: str) -> Union["XAIINATrack", None]:
        return self.by_property("language", language)

    def by_name(self, name: str) -> Union["XAIINATrack", None]:
        return self.by_property("name", name)

    def by_info_string(self, info_string: str) -> Union["XAIINATrack", None]:
        return self.by_property("infoString", info_string)

    def by_default(self, default: bool) -> Union["XAIINATrack", None]:
        return self.by_property("default", default)


class XAIINATrack(XABase.XAObject):
    """A media track.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def type(self) -> XAIINAApplication.TrackType:
        """The type of the track, either audio, video, or subtitle."""
        return XAIINAApplication.TrackType(self.xa_elem.type())

    @property
    def codec(self) -> str:
        """The audio/video codec of the track."""
        return self.xa_elem.codec()

    @property
    def language(self) -> str:
        """The language of the track."""
        return self.xa_elem.language()

    @property
    def name(self) -> str:
        """The name of the track."""
        return self.xa_elem.name()

    @property
    def info_string(self) -> str:
        """A text description of the track."""
        return self.xa_elem.infoString()

    @property
    def default(self) -> bool:
        """Whether this is the default track."""
        return self.xa_elem.default()


class XAIINAVideoTrackList(XABase.XAList):
    """A wrapper around lists of video tracks that employs fast enumeration techniques.

    All properties of video tracks can be called as methods on the wrapped list, returning a list containing each tracks's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINAVideoTrack, filter)

    def fps(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("fps") or [])

    def width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width") or [])

    def height(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height") or [])

    def by_fps(self, fps: float) -> Union["XAIINAVideoTrack", None]:
        return self.by_property("fps", fps)

    def by_width(self, width: int) -> Union["XAIINAVideoTrack", None]:
        return self.by_property("width", width)

    def by_height(self, height: int) -> Union["XAIINAVideoTrack", None]:
        return self.by_property("height", height)


class XAIINAVideoTrack(XABase.XAObject):
    """A video media track.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def fps(self) -> float:
        """The frames per second of the video."""
        return self.xa_elem.fps()

    @property
    def width(self) -> int:
        """The width of the video in pixels."""
        return self.xa_elem.width()

    @property
    def height(self) -> int:
        """The height of the video in pixels."""
        return self.xa_elem.height()


class XAIINAAudioTrackList(XABase.XAList):
    """A wrapper around lists of audio tracks that employs fast enumeration techniques.

    All properties of audio tracks can be called as methods on the wrapped list, returning a list containing each tracks's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINAAudioTrack, filter)

    def sample_rate(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("sampleRate") or [])

    def channel_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("channelCount") or [])

    def by_sample_rate(self, sample_rate: int) -> Union["XAIINAAudioTrack", None]:
        return self.by_property("sampleRate", sample_rate)

    def by_channel_count(self, channel_count: int) -> Union["XAIINAAudioTrack", None]:
        return self.by_property("channelCount", channel_count)


class XAIINAAudioTrack(XABase.XAObject):
    """An audio media track.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def sample_rate(self) -> int:
        """The sample rate of the audio track."""
        return self.xa_elem.sampleRate()

    @property
    def channel_count(self) -> int:
        """The number of audio channels in the track."""
        return self.xa_elem.channelCount()


class XAIINASubtitleTrackList(XABase.XAList):
    """A wrapper around lists of subtitle tracks that employs fast enumeration techniques.

    All properties of subtitle tracks can be called as methods on the wrapped list, returning a list containing each tracks's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINASubtitleTrack, filter)


class XAIINASubtitleTrack(XABase.XAObject):
    """A subtitle media track.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAIINAPlaylistItemList(XABase.XAList):
    """A wrapper around lists of playlist items that employs fast enumeration techniques.

    All properties of playlist items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAIINAPlaylistItem, filter)

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAPath(x) for x in ls]

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def current(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("current") or [])

    def currently_playing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentlyPlaying") or [])

    def network(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("network") or [])

    def by_file(
        self, file: Union[XABase.XAPath, str]
    ) -> Union["XAIINAPlaylistItem", None]:
        if isinstance(file, str):
            file = XABase.XAPath(file)
        return self.by_property("file", file.xa_elem)

    def by_url(
        self, url: Union[XABase.XAURL, str]
    ) -> Union["XAIINAPlaylistItem", None]:
        if isinstance(url, str):
            url = XABase.XAURL(url)
        return self.by_property("URL", url.xa_elem)

    def by_name(self, name: str) -> Union["XAIINAPlaylistItem", None]:
        return self.by_property("name", name)

    def by_current(self, current: bool) -> Union["XAIINAPlaylistItem", None]:
        return self.by_property("current", current)

    def by_currently_playing(
        self, currently_playing: bool
    ) -> Union["XAIINAPlaylistItem", None]:
        return self.by_property("currentlyPlaying", currently_playing)

    def by_network(self, network: bool) -> Union["XAIINAPlaylistItem", None]:
        return self.by_property("network", network)


class XAIINAPlaylistItem(XABase.XAObject):
    """An item in a playlist.

    .. versionadded:: 0.2.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def file(self) -> XABase.XAPath:
        """The file path of the item on the disk."""
        return XABase.XAPath(self.xa_elem.file())

    @property
    def url(self) -> XABase.XAURL:
        """The URL of the item."""
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def name(self) -> str:
        """The name of the item."""
        return self.xa_elem.name()

    @property
    def current(self) -> bool:
        """Whether the item is the currently selected item."""
        return self.xa_elem.current()

    @property
    def currently_playing(self) -> bool:
        """Whether the item is currently playng."""
        return self.xa_elem.currentlyPlaying()

    @property
    def network(self) -> bool:
        """Whether the item is an internet location item."""
        return self.xa_elem.network()
