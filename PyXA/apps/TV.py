""".. versionadded:: 0.0.2

Control the macOS TV application using JXA-like syntax.
"""

from typing import List, Literal, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

_STOPPED = 1800426323
_PLAYING = 1800426320
_PAUSED = 1800426352
_FAST_FORWARDING = 1800426310
_REWINDING = 1800426322
_KIND_LIBRARY = 1800169826
_KIND_SHARED_LIBRARY = 1800628324
_KIND_ITUNES_STORE = 1799967827
_KIND_UNKNOWN = 1800760939
_SEARCH_ALBUMS = 1800630860
_SEARCH_ALL = 1799449708
_SEARCH_ARTISTS = 1800630866
_SEARCH_DISPLAYED = 1800630870
_SEARCH_TRACK_NAMES = 1800630867
_SPECIAL_KIND_NONE = 1800302446
_SPECIAL_KIND_FOLDER = 1800630342
_SPECIAL_KIND_LIBRARY = 1800630348
_SPECIAL_KIND_MOVIE = 1800630345
_SPECIAL_KIND_TV_SHOW = 1800630356
_HOME_VIDEO_TRACK = 1800823880
_MOVIE_TRACK = 1800823885
_TV_SHOW_TRACK = 1800823892
_UNKNOWN_TRACK = 1800760939
_USER_RATING = 1800565845
_COMPUTED_RATING = 1800565827


class XATVApplication(XABaseScriptable.XASBApplication, XABaseScriptable.XAHasScriptableElements, XABase.XACanOpenPath):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.current_stream_title = self.xa_scel.currentStreamTitle() #: The name of the current streaming track
        self.current_stream_url = self.xa_scel.currentStreamURL() #: The URL of the current streaming track
        self.fixed_indexing = self.xa_scel.fixedIndexing() #: Whether the track indices are independent of the order of the current playlist or not
        self.frontmost = self.xa_scel.frontmost() #: Whether the application is active or not
        self.fullscreen = self.xa_scel.fullScreen() #: Whether the app is fullscreen or not
        self.name = self.xa_scel.name() #: The name of the application
        self.mute = self.xa_scel.mute() #: Whether sound output is muted or not
        self.player_position = self.xa_scel.playerPosition() #: The time elapsed in the current track
        self.player_state = self.xa_scel.playerState() #: Whether the player is playing, paused, stopped, fast forwarding, or rewinding
        self.sound_volume = self.xa_scel.soundVolume() #: The sound output volume
        self.version = self.xa_scel.version() #: The version of the application

    def play(self, item: 'XATVItem' = None) -> 'XATVApplication':
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: XATVItem, optional
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`playpause`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.playOnce_(item)
        return self

    def playpause(self) -> 'XATVApplication':
        """Toggles the playing/paused state of the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.playpause()
        return self

    def pause(self) -> 'XATVApplication':
        """Pauses the current track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`stop`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.pause()
        return self

    def stop(self) -> 'XATVApplication':
        """Stops playback of the current track. Subsequent playback will start from the beginning of the track.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`play`, :func:`playpause`, :func:`pause`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.stop()
        return self

    def next_track(self) -> 'XATVApplication':
        """Advances to the next track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`back_track`, :func:`previous_track`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.nextTrack()
        return self

    def back_track(self) -> 'XATVApplication':
        """Restarts the current track or returns to the previous track if playback is currently at the start.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`previous_track`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.backTrack()
        return self

    def previous_track(self) -> 'XATVApplication':
        """Returns to the previous track in the current playlist.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`next_track`, :func:`back_track`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.previousTrack()
        return self

    def fast_forward(self) -> 'XATVApplication':
        """Repeated skip forward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`rewind`, :func:`resume`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.fastForward()
        return self

    def rewind(self) -> 'XATVApplication':
        """Repeatedly skip backward in the track until resume() is called.

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`resume`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.rewind()
        return self

    def resume(self) -> 'XATVApplication':
        """Returns to normal playback after calls to fast_forward() or rewind().

        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. seealso:: :func:`fast_forward`, :func:`rewind`

        .. versionadded:: 0.0.2
        """
        self.xa_scel.resume()
        return self

    def open_location(self, video_url: str) -> 'XATVApplication':
        """Opens and plays an video stream URL or iTunes Store URL.

        :param audio_url: The URL of an audio stream (e.g. a web address to an MP3 file) or an item in the iTunes Store.
        :type audio_url: str
        :return: _description_
        :rtype: XATVApplication

        .. versionadded:: 0.0.2
        """
        self.xa_scel.openLocation_(video_url)
        return self

    def set_volume(self, new_volume: float) -> 'XATVApplication':
        """Sets the volume of playback.

        :param new_volume: The desired volume of playback.
        :type new_volume: float
        :return: A reference to the TV application object.
        :rtype: XATVApplication

        .. versionadded:: 0.0.2
        """
        self.set_property("soundVolume", new_volume)
        return self

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

    # Tracks
    def tracks(self, filter: dict = None) -> List['XATVTrack']:
        """Returns a list of tracks matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("tracks", filter, XATVTrack)

    def track(self, filter: Union[int, dict]) -> 'XATVTrack':
        """Returns the first track that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("tracks", filter, XATVTrack)

    def first_track(self) -> 'XATVTrack':
        """Returns the track at the first index of the tracks array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("tracks", XATVTrack)

    def last_track(self) -> 'XATVTrack':
        """Returns the track at the last (-1) index of the tracks array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("tracks", XATVTrack)

    def current_track(self) -> 'XATVTrack':
        """Returns the currently playing (or paused but not stopped) track.

        .. versionadded:: 0.0.2
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

    # Playlists
    def playlists(self, filter: dict = None) -> List['XATVPlaylist']:
        """Returns a list of playlists matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("playlists", filter, XATVPlaylist)

    def playlist(self, filter: Union[int, dict]) -> 'XATVPlaylist':
        """Returns the first playlist that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("playlists", filter, XATVPlaylist)

    def first_playlist(self) -> 'XATVPlaylist':
        """Returns the playlist at the first index of the playlists array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("playlists", XATVPlaylist)

    def last_playlist(self) -> 'XATVPlaylist':
        """Returns the playlist at the last (-1) index of the playlists array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("playlists", XATVPlaylist)


class XATVItem(XABaseScriptable.XASBObject):
    """A generic class with methods common to the various playable media classes in TV.app.

    .. seealso:: :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.index = self.xa_elem.index()
        self.name = self.xa_elem.name()
        self.persistent_id = self.xa_elem.persistentID()
        self.properties = self.xa_elem.properties()

    def download(self) -> 'XATVItem':
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. versionadded:: 0.0.2
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> 'XATVItem':
        """Reveals the item in the TV.app window.

        :return: A reference to the TV item object.
        :rtype: XATVItem

        .. seealso:: :func:`select`
        
        .. versionadded:: 0.0.2
        """
        self.xa_elem.reveal()
        return self


class XATVPlaylist(XATVItem, XABase.XAHasElements):
    """A class for managing and interacting with playlists in TV.app.

    .. seealso:: :class:`XATVItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.description = self.xa_elem.objectDescription()
        self.duration = self.xa_elem.duration()
        self.name = self.xa_elem.name()
        self.size = self.xa_elem.size()
        self.kind = self.xa_elem.specialKind()
        self.time = self.xa_elem.time()
        self.visible =  self.xa_elem.visible()

    def move_to(self, parent_playlist):
        self.xa_elem.moveTo_(parent_playlist.xa_elem)

    def search(self, query: str, type: Literal["all", "artists", "albums", "displayed", "tracks"] = "displayed"):
        search_ids = {
            "all": _SEARCH_ALL,
            "artists": _SEARCH_ARTISTS,
            "albums": _SEARCH_ALBUMS,
            "displayed": _SEARCH_DISPLAYED,
            "tracks": _SEARCH_TRACK_NAMES,
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


    # Tracks
    def tracks(self, filter: dict = None) -> List['XATVTrack']:
        """Returns a list of tracks matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.2
        """
        return self.elements("tracks", filter, XATVTrack)

    def track(self, filter: Union[int, dict]) -> 'XATVTrack':
        """Returns the first track that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.2
        """
        return self.element_with_properties("tracks", filter, XATVTrack)

    def first_track(self) -> 'XATVTrack':
        """Returns the track at the first index of the tracks array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.2
        """
        return self.first_element("tracks", XATVTrack)

    def last_track(self) -> 'XATVTrack':
        """Returns the track at the last (-1) index of the tracks array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.2
        """
        return self.last_element("tracks", XATVTrack)


class XATVTrack(XATVItem):
    """A class for managing and interacting with tracks in TV.app.

    .. seealso:: :class:`XATVItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def select(self) -> 'XATVItem':
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XATVTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.2
        """
        self.xa_elem.select()
        return self

    def play(self) -> 'XATVItem':
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: XATVItem

        .. versionadded:: 0.0.2
        """
        self.xa_elem.playOnce_(True)
        return self

    # Artworks
    def artworks(self, filter: dict = None) -> List['XATVTrackArtwork']:
        """Returns a list of artworks matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.2
        """
        return self.elements("artworks", filter, XATVTrackArtwork)

    def artwork(self, filter: Union[int, dict]) -> 'XATVTrackArtwork':
        """Returns the first artwork that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.2
        """
        return self.element_with_properties("artworks", filter, XATVTrackArtwork)

    def first_artwork(self) -> 'XATVTrackArtwork':
        """Returns the artwork at the first index of the artworks array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.2
        """
        return self.first_element("artworks", XATVTrackArtwork)

    def last_artworks(self) -> 'XATVTrackArtwork':
        """Returns the artwork at the last (-1) index of the artworks array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.2
        """
        return self.last_element("artworks", XATVTrackArtwork)

class XATVTrackArtwork(XATVItem):
    """A class for managing and interacting with artworks in TV.app.

    .. seealso:: :class:`XATVItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.description = self.xa_elem.objectDescription()
        self.downloaded = self.xa_elem.downloaded()
        self.format = self.xa_elem.format()
        self.kind = self.xa_elem.kind()
        self.raw_data = self.xa_elem.rawData()
        self.data = self.xa_elem.data()