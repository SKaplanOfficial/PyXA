""".. versionadded:: 0.1.0

Control Spotify using JXA-like syntax.
"""
from enum import Enum
from typing import Union

from PyXA import XABase
from PyXA import XABaseScriptable

class XASpotifyApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Spotify.app.

    .. versionadded:: 0.1.0
    """
    class PlayerState(Enum):
        """States of the Spotify track player.
        """
        STOPPED = XABase.OSType('kPSS')
        PLAYING = XABase.OSType('kPSP')
        PAUSED  = XABase.OSType('kPSp')

    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Spotify is the active application
        self.version: str #: The version of Spotify.app
        self.current_track: XASpotifyTrack #: The currently playing track
        self.sound_volume: int #: The sound output volume (0 = minimum, 100 = maximum)
        self.player_state: int #: Is Spotify stopped, paused, or playing?
        self.player_position: float #: The player’s position within the currently playing track in seconds
        self.repeating_enabled: bool #: Whether repeating is enabled in the current playback context
        self.repeating: bool #: Whether repeating is on or off
        self.shuffling_enabled: bool #: Whether shuffling is enabled in the current playback context
        self.shuffling: bool #: Whether shuffling is on or off

    @property
    def current_track(self) -> 'XASpotifyTrack':
        return self._new_element(self.xa_scel.currentTrack(), XASpotifyTrack)

    @property
    def sound_volume(self) -> int:
        return self.xa_scel.soundVolume()

    @sound_volume.setter
    def sound_volume(self, sound_volume: int):
        self.set_property('soundVolume', sound_volume)

    @property
    def player_state(self) -> 'XASpotifyApplication.PlayerState':
        return XASpotifyApplication.PlayerState(self.xa_scel.playerState())

    @property
    def player_position(self) -> float:
        return self.xa_scel.playerPosition()

    @player_position.setter
    def player_position(self, player_position: float):
        self.set_property('playerPosition', player_position)

    @property
    def repeating_enabled(self) -> bool:
        return self.xa_scel.repeatingEnabled()

    @property
    def repeating(self) -> bool:
        return self.xa_scel.repeating()

    @repeating.setter
    def repeating(self, repeating: bool):
        self.set_property('repeating', repeating)

    @property
    def shuffling_enabled(self) -> bool:
        return self.xa_scel.shufflingEnabled()

    @property
    def shuffling(self) -> bool:
        return self.xa_scel.shuffling()

    @shuffling.setter
    def shuffling(self, shuffling: bool):
        self.set_property('shuffling', shuffling)
        
    def search(self, search_string: str = "", track: str = "", start_year: int = -1, end_year: int = -1, genre: str = "", artist: str = "", album: str = "", label: str = "", mood: str = ""):
        """Opens the search tab and searches for content matching given parameters.
        
        .. versionadded:: 0.1.0
        """
        if track != "":
            search_string += f" track:{track}"

        if start_year != -1:
            if end_year == -1:
                search_string += f" year:{start_year}-{start_year}"
            else:
                search_string += f" year:{start_year}-{end_year}"

        if genre != "":
            search_string += f" genre:{genre}"

        if artist != "":
            search_string += f" artist:{artist}"

        if album != "":
            search_string += f" album:{album}"

        if label != "":
            search_string += f" label:{label}"

        if mood != "":
            search_string += f" mood:{mood}"

        XABase.XAURL(f"spotify:search:{search_string}").open()

    def next_track(self):
        """Skips to the next track.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.next_track()


        .. versionadded:: 0.1.0
        """
        self.xa_scel.nextTrack()

    def previous_track(self):
        """Skips to the previous track.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.previous_track()

        .. versionadded:: 0.1.0
        """
        self.xa_scel.previousTrack()

    def playpause(self):
        """Toggles play/pause.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.playpause()

        .. versionadded:: 0.1.0
        """
        self.xa_scel.playpause()

    def pause(self):
        """Pauses playback.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.pause()

        .. versionadded:: 0.1.0
        """
        self.xa_scel.pause()

    def play(self):
        """Resumes playback.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.play()

        .. versionadded:: 0.1.0
        """
        self.xa_scel.play()

    def play_track(self, track_uri: str, context_uri: Union[str, None] = None):
        """Starts playback of a track in the given context.

        :param track_uri: The URI of the track to play
        :type track_uri: str
        :param context_uri: The URI of the context to play in, defaults to None
        :type context_uri: Union[str, None], optional

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Spotify")
        >>> app.play_track("spotify:track:4LRPiXqCikLlN15c3yImP7")

        .. versionadded:: 0.1.0
        """
        self.xa_scel.playTrack_inContext_(track_uri, context_uri)




class XASpotifyTrack(XABase.XAObject):
    """A Spotify track.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.artist: str #: The artist of the track
        self.album: str #: The album of the track
        self.disc_number: int #: The disc number of the track
        self.duration: int #: The length of the track in milliseconds
        self.played_count: int #: The number of times this track has been played
        self.track_number: int #: The index of the track in its album
        self.starred: bool #: Whether the track is starred
        self.popularity: int #: The popularity of this track, 0-100
        self.id: str #: The ID of the track
        self.name: str #: The name of the track
        self.artwork_url: XABase.XAURL #: The URL of the track's album cover
        self.artwork: XABase.XAImage #: The album artwork image
        self.album_artist: str #: The album artist of the track
        self.spotify_url: XABase.XAURL #: The URL of the track

    @property
    def artist(self) -> str:
        return self.xa_elem.artist()

    @property
    def album(self) -> str:
        return self.xa_elem.album()

    @property
    def disc_number(self) -> int:
        return self.xa_elem.discNumber()

    @property
    def duration(self) -> int:
        return self.xa_elem.duration()

    @property
    def played_count(self) -> int:
        return self.xa_elem.playedCount()

    @property
    def track_number(self) -> int:
        return self.xa_elem.trackNumber()

    @property
    def starred(self) -> bool:
        return self.xa_elem.starred()

    @property
    def popularity(self) -> int:
        return self.xa_elem.popularity()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def artwork_url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.artworkUrl())

    @property
    def artwork(self) -> XABase.XAImage:
        return XABase.XAImage(self.artwork_url)

    @property
    def album_artist(self) -> str:
        return self.xa_elem.albumArtist()

    @property
    def spotify_url(self) -> type:
        return XABase.XAURL(self.xa_elem.spotifyUrl())

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"