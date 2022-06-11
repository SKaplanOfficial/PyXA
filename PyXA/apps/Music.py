""".. versionadded:: 0.0.1

Control the macOS Music application using JXA-like syntax.
"""

from typing import List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

_KIND_TRACK_LISTING = 1800696427
_KIND_ALBUM_LISTING = 1799449698
_KIND_CD_INSERT = 1799570537
_STOPPED = 1800426323
_PLAYING = 1800426320
_PAUSED = 1800426352
_FAST_FORWARDING = 1800426310
_REWINDING = 1800426322
_REPEAT_OFF = 1800564815
_REPEAT_ONE = 1800564785
_REPEAT_ALL = 1799449708
_SHUFFLE_MODE_SONGS = 1800628307
_SHUFFLE_MODE_ALBUMS = 1800628289
_SHUFFLE_MODE_GROUPINGS = 1800628295
_SOURCE_LIBRARY = 1800169826
_SOURCE_AUDIO_CD = 1799439172
_SOURCE_MP3 = 1800225604
_SOURCE_RADIO = 1800697198
_SOURCE_SHARED_LIBRARY = 1800628324
_SOURCE_STORE = 1799967827
_SOURCE_UNKNOWN = 1800760939
_SEARCH_ALL = 1799449708
_SEARCH_ALBUMS = 1800630860
_SEARCH_ARTISTS = 1800630866
_SEARCH_COMPOSERS = 1800630851
_SEARCH_DISPLAYED = 1800630870
_SEARCH_TRACK_NAMES = 1800630867
_KIND_NONE = 1800302446
_KIND_FOLDER = 1800630342
_KIND_GENIUS = 1800630343
_KIND_LIBRARY = 1800630348
_KIND_MUSIC = 1800630362
_KIND_PURCHASED = 1800630349
_KIND_SONG = 1800234067
_KIND_VIDEO = 1800823894
_KIND_UNKNOWN = 1800760939
_USER_RATING = 1800565845
_COMPUTED_RATING = 1800565827
_DEVICE_COMPUTER = 1799442499
_DEVICE_AIRPORT_EXPRESS = 1799442520
_DEVICE_APPLETV = 1799442516
_DEVICE_AIRPLAY = 1799442511
_DEVICE_BLUETOOTH = 1799442498
_DEVICE_HOMEPOD = 1799442504
_DEVICE_UNKNOWN = 1799442517
_STATUS_UNKNOWN = 1800760939
_STATUS_PURCHASED = 1799442520
_STATUS_MATCHED = 1800233332
_STATUS_UPLOADED = 1800761452
_STATUS_INELIGIBLE = 1800562026
_STATUS_REMOVED = 1800562029
_STATUS_ERROR = 1799713394
_STATUS_DUPLICATE = 1799648624
_STATUS_SUBSCRIPTION = 1800631650
_STATUS_UNAVAILABLE = 1800562038
_STATUS_NOT_UPLOADED = 1800761424

class XAMusicApplication(XABaseScriptable.XASBApplication, XABaseScriptable.XAHasScriptableElements, XABase.XACanOpenPath):
    """A class for managing and interacting with Music.app.

    .. seealso:: :class:`XAMediaPlaylist`, :class:`XAMediaTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def play(self, item: 'XAMediaItem' = None) -> 'XAMusicApplication':
        """Plays the specified music item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: XAMediaItem, optional
        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playOnce_(item)
        return self

    def playpause(self) -> 'XAMusicApplication':
        """Toggles the playing/paused state of the current track.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> 'XAMusicApplication':
        """Pauses the current track.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> 'XAMusicApplication':
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> 'XAMusicApplication':
        """Advances to the next track in the current playlist.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> 'XAMusicApplication':
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> 'XAMusicApplication':
        """Returns to the previous track in the current playlist.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> 'XAMusicApplication':
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> 'XAMusicApplication':
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> 'XAMusicApplication':
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.resume()
        return self

    def open_location(self, audio_url: str) -> 'XAMusicApplication':
        """Opens and plays an audio stream URL or iTunes URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.openLocation_(audio_url)
        return self

    def set_volume(self, new_volume: float) -> 'XAMusicApplication':
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the Music application object.
        :rtype: XAMusicApplication

        .. versionadded:: 0.0.1
        """
        self.set_property("soundVolume", new_volume)
        return self

    def repeat_off(self):
        self.set_property("songRepeat", _REPEAT_OFF)
        return self

    def repeat_one(self):
        self.set_property("songRepeat", _REPEAT_ONE)
        return self

    def repeat_all(self):
        self.set_property("songRepeat", _REPEAT_ALL)
        return self

    # Tracks
    def tracks(self, filter: dict = None) -> List['XAMediaTrack']:
        """Returns a list of tracks matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("tracks", filter, XAMediaTrack)

    def track(self, filter: Union[int, dict]) -> 'XAMediaTrack':
        """Returns the first track that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("tracks", filter, XAMediaTrack)

    def first_track(self) -> 'XAMediaTrack':
        """Returns the track at the first index of the tracks array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("tracks", XAMediaTrack)

    def last_track(self) -> 'XAMediaTrack':
        """Returns the track at the last (-1) index of the tracks array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("tracks", XAMediaTrack)

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

    # Playlists
    def playlists(self, filter: dict = None) -> List['XAMediaPlaylist']:
        """Returns a list of playlists matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("playlists", filter, XAMediaPlaylist)

    def playlist(self, filter: Union[int, dict]) -> 'XAMediaPlaylist':
        """Returns the first playlist that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("playlists", filter, XAMediaPlaylist)

    def first_playlist(self) -> 'XAMediaPlaylist':
        """Returns the playlist at the first index of the playlists array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("playlists", XAMediaPlaylist)

    def last_playlist(self) -> 'XAMediaPlaylist':
        """Returns the playlist at the last (-1) index of the playlists array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("playlists", XAMediaPlaylist)


class XAMediaItem(XABaseScriptable.XASBObject):
    """A generic class with methods common to the various playable media classes in Music.app.

    .. seealso:: :class:`XAMediaPlaylist`, :class:`XAMediaTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def download(self) -> 'XAMediaItem':
        """Downloads the item into the local library.

        :return: A reference to the media item object.
        :rtype: XAMediaItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> 'XAMediaItem':
        """Reveals the item in the Music.app window.

        :return: A reference to the media item object.
        :rtype: XAMediaItem

        .. seealso:: :func:`select`
        
        .. versionadded:: 0.0.1
        """
        self.xa_elem.reveal()
        return self

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
        :rtype: XAMediaItem

        .. versionadded:: 0.0.1
        """
        self.xa_elem.playOnce_(True)
        return self


class XAMediaPlaylist(XAMediaItem, XABase.XAHasElements):
    """A class for managing and interacting with playlists in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def tracks(self, filter: dict = None) -> List['XAMediaTrack']:
        """Returns a list of tracks matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.elements("tracks", filter, XAMediaTrack)

    def track(self, filter: Union[int, dict]) -> 'XAMediaTrack':
        """Returns the first track that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("tracks", filter, XAMediaTrack)

    def first_track(self) -> 'XAMediaTrack':
        """Returns the track at the first index of the tracks array.

        .. versionadded:: 0.0.1
        """
        return self.first_element("tracks", XAMediaTrack)

    def last_track(self) -> 'XAMediaTrack':
        """Returns the track at the last (-1) index of the tracks array.

        .. versionadded:: 0.0.1
        """
        return self.last_element("tracks", XAMediaTrack)


class XAMediaTrack(XAMediaItem):
    """A class for managing and interacting with tracks in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)