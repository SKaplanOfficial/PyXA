""".. versionadded:: 0.0.2

Control the macOS TV application using JXA-like syntax.
"""

from datetime import datetime
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
_BROWSER_WINDOW = b'cBrW'
_VIDEO_WINDOW = b'niwc'
_PLAYLIST_WINDOW = b'WlPc'
_LIBRARY_PLAYLIST = b'PiLc'
_USER_PLAYLIST = b'PsUc'
_SHARED_TRACK = b'ThSc'
_FILE_TRACK = b'TlFc'
_URL_TRACK = b'TRUc'


class _XATVHasSharedTracks(XABase.XAObject):
    """A convenience class for media items that have shared tracks.

    .. versionadded:: 0.0.2
    """
    def shared_tracks(self, filter: dict = None) -> List['XATVSharedTrack']:
        """Returns a list of shared tracks matching the filter.

        :param filter: A dictionary of property names and desired values that shared tracks in the resulting list will have.
        :type filter: dict
        :return: The list of shared track objects.
        :rtype: List[XATVSharedTrack]

        :Example: Listing all shared tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.shared_tracks())
        [<PyXA.apps.TV.XATVSharedTrack object at 0x105d972e0>, <PyXA.apps.TV.XATVSharedTrack object at 0x105d56b80>, ...]

        .. note::

           Querying for all or many tracks can take significant time and should be avoided when possible. Apply filters or use more specific methods such as :func:`shared_track` to reduce the number of queried tracks.

        :Example: Listing filtered shared tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.shared_tracks({"genre": "Sci-Fi & Fantasy"}))
        [<PyXA.apps.TV.XATVSharedTrack object at 0x10484cd90>, <PyXA.apps.TV.XATVSharedTrack object at 0x10755ebe0>]

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_elements("sharedTracks", filter, XATVSharedTrack)
        return self.elements("sharedTracks", filter, XATVSharedTrack)

    def shared_track(self, filter: Union[int, dict]) -> 'XATVSharedTrack':
        """Returns the first shared track that matches the filter.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_element_with_properties("sharedTracks", filter, XATVSharedTrack)
        return self.element_with_properties("sharedTracks", filter, XATVSharedTrack)

    def first_shared_track(self) -> 'XATVSharedTrack':
        """Returns the shared track at the first index of the shared tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.first_scriptable_element("sharedTracks", XATVSharedTrack)
        return self.first_element("sharedTracks", XATVSharedTrack)

    def last_shared_track(self) -> 'XATVSharedTrack':
        """Returns the shared track at the last (-1) index of the shared tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.last_scriptable_element("sharedTracks", XATVSharedTrack)
        return self.last_element("sharedTracks", XATVSharedTrack)


class _XATVHasFileTracks(XABase.XAObject):
    """A convenience class for media items that have file tracks.

    .. versionadded:: 0.0.2
    """
    def file_tracks(self, filter: dict = None) -> List['XATVFileTrack']:
        """Returns a list of file tracks matching the filter.

        :param filter: A dictionary of property names and desired values that file tracks in the resulting list will have.
        :type filter: dict
        :return: The list of file track objects.
        :rtype: List[XATVFileTrack]

        :Example: Listing all file tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.file_tracks())
        [<PyXA.apps.TV.XATVFileTrack object at 0x105ce4310>, <PyXA.apps.TV.XATVFileTrack object at 0x106dc4220>, ...]

        .. note::

           Querying for all or many tracks can take significant time and should be avoided when possible. Apply filters or use more specific methods such as :func:`file_track` to reduce the number of queried tracks.

        :Example: Listing filtered file tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.file_tracks({"unplayed": True}))
        [<PyXA.apps.TV.XATVFileTrack object at 0x1054e0d90>]

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_elements("fileTracks", filter, XATVFileTrack)
        return self.elements("fileTracks", filter, XATVFileTrack)

    def file_track(self, filter: Union[int, dict]) -> 'XATVFileTrack':
        """Returns the first file track that matches the filter.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_element_with_properties("fileTracks", filter, XATVFileTrack)
        return self.element_with_properties("fileTracks", filter, XATVFileTrack)

    def first_file_track(self) -> 'XATVFileTrack':
        """Returns the file track at the first index of the file tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.first_scriptable_element("fileTracks", XATVFileTrack)
        return self.first_element("fileTracks", XATVFileTrack)

    def last_file_track(self) -> 'XATVFileTrack':
        """Returns the file track at the last (-1) index of the file tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.last_scriptable_element("fileTracks", XATVFileTrack)
        return self.last_element("fileTracks", XATVFileTrack)


class _XATVHasURLTracks(XABase.XAObject):
    """A convenience class for media items that have URL tracks.

    .. versionadded:: 0.0.2
    """
    def url_tracks(self, filter: dict = None) -> List['XATVRemoteURLTrack']:
        """Returns a list of URL tracks matching the filter.

        :param filter: A dictionary of property names and desired values that URL tracks in the resulting list will have.
        :type filter: dict
        :return: The list of URL track objects.
        :rtype: List[XATVRemoteURLTrack]

        :Example: Listing all URL track

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.url_tracks())
        [<PyXA.apps.TV.XATVRemoteURLTrack object at 0x1074532e0>, <PyXA.apps.TV.XATVRemoteURLTrack object at 0x107412a30>, ...]

        .. note::

           Querying for all or many tracks can take significant time and should be avoided when possible. Apply filters or use more specific methods such as :func:`url_track` to reduce the number of queried tracks.

        :Example: Listing filtered URL tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.url_tracks({"enabled": False}))
        []

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_elements("URLTracks", filter, XATVRemoteURLTrack)
        return self.elements("URLTracks", filter, XATVRemoteURLTrack)

    def url_track(self, filter: Union[int, dict]) -> 'XATVRemoteURLTrack':
        """Returns the first URL track that matches the filter.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_element_with_properties("urlTracks", filter, XATVRemoteURLTrack)
        return self.element_with_properties("urlTracks", filter, XATVRemoteURLTrack)

    def first_url_track(self) -> 'XATVRemoteURLTrack':
        """Returns the URL track at the first index of the URL tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.first_scriptable_element("urlTracks", XATVRemoteURLTrack)
        return self.first_element("urlTracks", XATVRemoteURLTrack)

    def last_url_track(self) -> 'XATVRemoteURLTrack':
        """Returns the URL track at the last (-1) index of the URL tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.last_scriptable_element("urlTracks", XATVRemoteURLTrack)
        return self.last_element("urlTracks", XATVRemoteURLTrack)


class _XATVHasTracks(_XATVHasSharedTracks, _XATVHasFileTracks, _XATVHasURLTracks):
    """A convenience class for media items that have tracks.

    .. versionadded:: 0.0.2
    """
    def tracks(self, filter: dict = None) -> List['XATVTrack']:
        """Returns a list of tracks matching the filter.

        :param filter: A dictionary of property names and desired values that tracks in the resulting list will have.
        :type filter: dict
        :return: The list of track objects.
        :rtype: List[XATVTrack]

        :Example: Listing all track

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.tracks())
        [<PyXA.apps.TV.XATVSharedTrack object at 0x10451b2e0>, <PyXA.apps.TV.XATVSharedTrack object at 0x1043bab80>, ...]

        .. note::

           Querying for all or many tracks can take significant time and should be avoided when possible. Apply filters or use more specific methods such as :func:`track` to reduce the number of queried tracks.

        :Example: Listing filtered tracks

        >>> import PyXA
        >>> app = PyXA.application("TV")
        >>> print(app.tracks({"year": 1997}))
        [<PyXA.apps.TV.XATVSharedTrack object at 0x1055c4d90>, <PyXA.apps.TV.XATVFileTrack object at 0x1079d0d00>]

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_elements("tracks", filter, XATVTrack)
        return self.elements("tracks", filter, XATVTrack)

    def track(self, filter: Union[int, dict]) -> 'XATVTrack':
        """Returns the first track that matches the filter.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.scriptable_element_with_properties("tracks", filter, XATVTrack)
        return self.element_with_properties("tracks", filter, XATVTrack)

    def first_track(self) -> 'XATVTrack':
        """Returns the track at the first index of the tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.first_scriptable_element("tracks", XATVTrack)
        return self.first_element("tracks", XATVTrack)

    def last_track(self) -> 'XATVTrack':
        """Returns the track at the last (-1) index of the tracks array.

        .. versionadded:: 0.0.2
        """
        if self.xa_scel is not None:
            return self.last_scriptable_element("tracks", XATVTrack)
        return self.last_element("tracks", XATVTrack)


class XATVApplication(XABaseScriptable.XASBApplication, XABaseScriptable.XAHasScriptableElements, XABase.XACanOpenPath, _XATVHasTracks):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XATVWindow`, class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATVWindow

        self.current_stream_title = self.xa_scel.currentStreamTitle() #: The name of the current streaming track
        self.current_stream_url = self.xa_scel.currentStreamURL() #: The URL of the current streaming track
        self.fixed_indexing = self.xa_scel.fixedIndexing() #: Whether the track indices are independent of the order of the current playlist or not
        self.frontmost #: Whether the application is active or not
        self.fullscreen = self.xa_scel.fullScreen() #: Whether the app is fullscreen or not
        self.name = self.xa_scel.name() #: The name of the application
        self.mute = self.xa_scel.mute() #: Whether sound output is muted or not
        self.player_position = self.xa_scel.playerPosition() #: The time elapsed in the current track
        self.player_state = self.xa_scel.playerState() #: Whether the player is playing, paused, stopped, fast forwarding, or rewinding
        self.sound_volume = self.xa_scel.soundVolume() #: The sound output volume
        self.version = self.xa_scel.version() #: The version of the application

    def play(self, item: '_XATVItem' = None) -> 'XATVApplication':
        """Plays the specified TV item (e.g. track, playlist, etc.). If no item is provided, this plays the current track from its current player position.

        :param item: The track, playlist, or video to play, defaults to None
        :type item: _XATVItem, optional
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

    # Browser Windows
    def browser_windows(self, filter: dict = None) -> List['XATVBrowserWindow']:
        """Returns a list of browser windows matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("browserWindows", filter, XATVBrowserWindow)

    def browser_window(self, filter: Union[int, dict]) -> 'XATVBrowserWindow':
        """Returns the first browser window that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("browserWindows", filter, XATVBrowserWindow)

    def first_browser_window(self) -> 'XATVBrowserWindow':
        """Returns the window at the first index of the browser windows array.

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("browserWindows", XATVBrowserWindow)

    def last_browser_window(self) -> 'XATVBrowserWindow':
        """Returns the window at the last (-1) index of the browser windows array.

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("browserWindows", XATVBrowserWindow)

    # Playlist Windows
    def playlist_windows(self, filter: dict = None) -> List['XATVPlaylistWindow']:
        """Returns a list of playlist windows matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("playlistWindows", filter, XATVPlaylistWindow)

    def playlist_window(self, filter: Union[int, dict]) -> 'XATVPlaylistWindow':
        """Returns the first playlist window that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("playlistWindows", filter, XATVPlaylistWindow)

    def first_playlist_window(self) -> 'XATVPlaylistWindow':
        """Returns the window at the first index of the playlist windows array.

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("playlistWindows", XATVPlaylistWindow)

    def last_playlist_window(self) -> 'XATVPlaylistWindow':
        """Returns the window at the last (-1) index of the playlist windows array.

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("playlistWindows", XATVPlaylistWindow)

    # Video Windows
    def video_windows(self, filter: dict = None) -> List['XATVVideoWindow']:
        """Returns a list of video windows matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("videoWindows", filter, XATVVideoWindow)

    def video_window(self, filter: Union[int, dict]) -> 'XATVVideoWindow':
        """Returns the first video window that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("videoWindows", filter, XATVVideoWindow)

    def first_video_window(self) -> 'XATVVideoWindow':
        """Returns the window at the first index of the video windows array.

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("videoWindows", XATVVideoWindow)

    def last_video_window(self) -> 'XATVVideoWindow':
        """Returns the window at the last (-1) index of the video windows array.

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("videoWindows", XATVVideoWindow)

    # Sources
    def sources(self, filter: dict = None) -> List['XATVSource']:
        """Returns a list of sources matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("sources", filter, XATVSource)

    def source(self, filter: Union[int, dict]) -> 'XATVSource':
        """Returns the first source that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("sources", filter, XATVSource)

    def first_source(self) -> 'XATVSource':
        """Returns the source at the first index of the sources array.

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("sources", XATVSource)

    def last_source(self) -> 'XATVSource':
        """Returns the source at the last (-1) index of the sources array.

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("sources", XATVSource)

    # Playlists
    def playlists(self, filter: dict = None) -> List['XATVPlaylist']:
        """Returns a list of playlists matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_elements("playlists", filter, XATVPlaylist)

    def playlist(self, filter: Union[int, dict]) -> 'XATVPlaylist':
        """Returns the first playlist that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.scriptable_element_with_properties("playlists", filter, XATVPlaylist)

    def first_playlist(self) -> 'XATVPlaylist':
        """Returns the playlist at the first index of the playlists array.

        .. versionadded:: 0.0.2
        """
        return self.first_scriptable_element("playlists", XATVPlaylist)

    def last_playlist(self) -> 'XATVPlaylist':
        """Returns the playlist at the last (-1) index of the playlists array.

        .. versionadded:: 0.0.2
        """
        return self.last_scriptable_element("playlists", XATVPlaylist)


class XATVWindow(XABaseScriptable.XASBWindow, XABase.XAHasElements):
    """A class for managing and interacting with windows in TV.app.

    .. seealso:: :class:`XATVBrowserWindow`, :class:`XATVPlaylistWindow`, :class:`XATVVideoWindow`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        obj_class = self.xa_elem.objectClass().data()
        if obj_class == _BROWSER_WINDOW:
            self.__class__ = XATVBrowserWindow
            self.__init__()
        elif obj_class == _PLAYLIST_WINDOW:
            self.__class__ = XATVPlaylistWindow
            self.__init__()
        elif obj_class == _VIDEO_WINDOW:
            self.__class__ = XATVVideoWindow
            self.__init__()


class XATVBrowserWindow(XATVWindow):
    """A class for managing and interacting with browser windows in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)

class XATVPlaylistWindow(XATVWindow):
    """A class for managing and interacting with playlist windows in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVVideoWindow(XATVWindow):
    """A class for managing and interacting with video windows in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)

class _XATVItem(XABaseScriptable.XASBObject):
    """A generic class with methods common to the various playable media classes in TV.app.

    .. seealso:: :class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.xa_elem.id()
        self.index = self.xa_elem.index()
        self.name = self.xa_elem.name()
        self.persistent_id = self.xa_elem.persistentID()
        self.properties = self.xa_elem.properties()

    def download(self) -> '_XATVItem':
        """Downloads the item into the local library.

        :return: A reference to the TV item object.
        :rtype: _XATVItem

        .. versionadded:: 0.0.2
        """
        self.xa_elem.download()
        return self

    def reveal(self) -> '_XATVItem':
        """Reveals the item in the TV.app window.

        :return: A reference to the TV item object.
        :rtype: _XATVItem

        .. seealso:: :func:`select`
        
        .. versionadded:: 0.0.2
        """
        self.xa_elem.reveal()
        return self

class XATVSource(_XATVItem, XABase.XAHasElements):
    """A class for managing and interacting with media sources in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.capacity = self.xa_elem.capacity()
        self.free_space = self.xa_elem.freeSpace()
        self.kind = self.xa_elem.kind()


class XATVPlaylist(_XATVItem, XABase.XAHasElements, _XATVHasTracks):
    """A class for managing and interacting with playlists in TV.app.

    .. seealso:: :class:`XATVLibraryPlaylist`, :class:`XATVUserPlaylist`

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

        if self.objectClass.data() == _LIBRARY_PLAYLIST:
            self.__class__ = XATVLibraryPlaylist
            self.__init__()
        elif self.objectClass.data() == _USER_PLAYLIST:
            self.__class__ = XATVUserPlaylist
            self.__init__()

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


class XATVLibraryPlaylist(XATVPlaylist):
    """A class for managing and interacting with the library playlist in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVUserPlaylist(XATVPlaylist):
    """A class for managing and interacting with user playlists in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVTrack(_XATVItem):
    """A class for managing and interacting with tracks in TV.app.

    .. seealso:: :class:`XATVSharedTrack`, :class:`XATVFileTrack`, :class:`XATVRemoteURLTrack`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.album: str = self.xa_elem.album() #: The name of the album the track's album
        self.album_rating: int = self.xa_elem.albumRating() #: The rating of the track's album
        self.album_rating_kind: str = self.xa_elem.albumRatingKind() #: The album's rating kind
        self.bit_rate: int = self.xa_elem.bitRate() #: The track's bitrate in kbps
        self.bookmark: float = self.xa_elem.bookmark() #: The bookmark time of the track in seconds
        self.bookmarkable: bool = self.xa_elem.bookmarkable() #: Whether the playback position is kept in memory after stopping the track
        self.category: str = self.xa_elem.category() #: The category of the track
        self.comment: str = self.xa_elem.comment() #: User-provided notes on the track
        self.database_id: int = self.xa_elem.databaseID() #: A unique ID for the track
        self.date_added: datetime = self.xa_elem.dateAdded() #: The date the track was added to the current playlist
        self.description: str = self.xa_elem.objectDescription() #: A description of the track
        self.director: str = self.xa_elem.director() #: The artist of the track
        self.disc_count: int = self.xa_elem.discCount() #: The number of discs in the source album
        self.disc_number: int = self.xa_elem.discNumber() #: The index of the disc containing the track
        self.downloader_apple_id: str = self.xa_elem.downloaderAppleID() #: The Apple ID of the person who downloaded the track
        self.downloader_name: str = self.xa_elem.downloaderName() #: The full name of the person who downloaded the track
        self.duration: float = self.xa_elem.duration() #: Length of the track in seconds
        self.enabled: bool = self.xa_elem.enabled() #: Whether the track is able to be played
        self.episode_id: str = self.xa_elem.episodeID() #: A unique ID for the episode of the track
        self.episode_number: int = self.xa_elem.episodeNumber() #: The episode number of the track
        self.finish: float = self.xa_elem.finish() #: The time in seconds from the start at which the track stops playing. Same as duration.
        self.genre: str = self.xa_elem.genre() #: The genre category of the track.
        self.grouping: str = self.xa_elem.grouping() #: The current section/chapter/movement of the track
        self.kind: str = self.xa_elem.kind() #: A description of the track's purchase type
        self.long_description: str = self.xa_elem.longDescription() #: A long description for the track
        self.media_kind: str = self.xa_elem.mediaKind() #: A description of the track's media type
        self.modification_date: datetime = self.xa_elem.modificationDate() #: The last modification date of the track's content
        self.played_count: int = self.xa_elem.playedCount() #: The number of the times the track has been played
        self.played_date: datetime = self.xa_elem.playedDate() #: The date the track was last played
        self.purchaser_apple_id: str = self.xa_elem.purchaserAppleID() #: The Apple ID of the person who bought the track
        self.purchaser_name: str = self.xa_elem.purchaserName() #: The full name of the person who bought the track
        self.rating: int = self.xa_elem.rating() #: The rating of the track from 0 to 100
        self.rating_kind: str = self.xa_elem.ratingKind() #: Whether the rating is user-provided or computed
        self.release_date: datetime = self.xa_elem.releaseDate() #: The date the track was released
        self.sample_rate: int = self.xa_elem.sampleRate() #: The sample rate of the track in Hz
        self.season_number: int = self.xa_elem.seasonNumber() #: The number of the season the track belongs to
        self.skipped_count: int = self.xa_elem.skippedCount() #: The number of times the track has been skipped
        self.skipped_date: datetime = self.xa_elem.skippedDate() #: The date the track was last skipped
        self.show: str = self.xa_elem.show() #: The show the track belongs to
        self.sort_album: str = self.xa_elem.sortAlbum() #: The string used for this track when sorting by album
        self.sort_director: str = self.xa_elem.sortDirector() #: The string used for this track when sorting by director
        self.sort_name: str = self.xa_elem.sortName() #: The string used for this track when sorting by name
        self.sort_show: str = self.xa_elem.sortShow() #: The string used for this track when sorting by show
        self.size: int = self.xa_elem.size() #: The size of the track in bytes
        self.start: float = self.xa_elem.start() #: The start time of the track (0)
        self.time: str = self.xa_elem.time() #: HH:MM:SS representation for the duration of the track
        self.track_count: int = self.xa_elem.trackCount() #: The number of tracks in the track's album
        self.track_number: int = self.xa_elem.trackNumber() #: The index of the track within its album
        self.unplayed: bool = self.xa_elem.unplayed() #: Whether the track has been played before
        self.volume_adjustment: int = self.xa_elem.volumeAdjustment() #: Volume adjustment setting for this track from -100 to +100
        self.year: int = self.xa_elem.year() #: The year the track was released

        if self.objectClass.data() == _SHARED_TRACK:
            self.__class__ = XATVSharedTrack
            self.__init__()
        elif self.objectClass.data() == _FILE_TRACK:
            self.__class__ = XATVFileTrack
            self.__init__()
        elif self.objectClass.data() == _URL_TRACK:
            self.__class__ = XATVRemoteURLTrack
            self.__init__()

    def select(self) -> '_XATVItem':
        """Selects the item.

        :return: A reference to the media item object.
        :rtype: XATVTrack

        .. seealso:: :func:`reveal`

        .. versionadded:: 0.0.2
        """
        self.xa_elem.select()
        return self

    def play(self) -> '_XATVItem':
        """Plays the item.

        :return: A reference to the media item object.
        :rtype: _XATVItem

        .. versionadded:: 0.0.2
        """
        self.xa_elem.playOnce_(True)
        return self

    # Artworks
    def artworks(self, filter: dict = None) -> List['XATVTrackArtwork']:
        """Returns a list of artworks matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.elements("artworks", filter, XATVTrackArtwork)

    def artwork(self, filter: Union[int, dict]) -> 'XATVTrackArtwork':
        """Returns the first artwork that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.element_with_properties("artworks", filter, XATVTrackArtwork)

    def first_artwork(self) -> 'XATVTrackArtwork':
        """Returns the artwork at the first index of the artworks array.

        .. versionadded:: 0.0.2
        """
        return self.first_element("artworks", XATVTrackArtwork)

    def last_artworks(self) -> 'XATVTrackArtwork':
        """Returns the artwork at the last (-1) index of the artworks array.

        .. versionadded:: 0.0.2
        """
        return self.last_element("artworks", XATVTrackArtwork)


class XATVSharedTrack(XATVTrack):
    """A class for managing and interacting with shared tracks in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVFileTrack(XATVTrack):
    """A class for managing and interacting with file tracks in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVRemoteURLTrack(XATVTrack):
    """A class for managing and interacting with URL tracks in TV.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties = None):
        if properties is not None:
            super().__init__(properties)


class XATVTrackArtwork(_XATVItem):
    """A class for managing and interacting with artworks in TV.app.

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