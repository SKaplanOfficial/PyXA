""".. versionadded:: 0.0.1

Control the macOS Music application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Literal, Union

import AppKit
from PyXA import XABase, XABaseScriptable

from . import MediaApplicationBase


class XAMusicApplication(MediaApplicationBase.XAMediaApplication):
    """A class for managing and interacting with Music.app.

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

    @property
    def airplay_enabled(self) -> bool:
        """Whether AirPlay is currently enabled.
        """
        return self.xa_scel.airplayEnabled()

    @property
    def converting(self) -> bool:
        """Whether a track is currently being converted.
        """
        return self.xa_scel.converting()

    @property
    def current_airplay_devices(self) -> 'XAMusicAirPlayDeviceList':
        """The currently selected AirPlay devices.
        """
        ls = self.xa_scel.currentAirPlayDevices()
        return self._new_element(ls, XAMusicAirPlayDeviceList)

    @current_airplay_devices.setter
    def current_airplay_devices(self, current_airplay_devices: Union['XAMusicAirPlayDeviceList', list['XAMusicAirPlayDevice']]):
        if isinstance(current_airplay_devices, list):
            current_airplay_devices = [x.xa_elem for x in current_airplay_devices]
            self.set_property('currentAirplayDevices', current_airplay_devices)
        else:
            self.set_property('currentAirplayDevices', current_airplay_devices.xa_elem)

    @property
    def current_encoder(self) -> 'XAMusicEncoder':
        """The currently selected encoder.
        """
        return self._new_element(self.xa_scel.currentEncoder(), XAMusicEncoder)

    @current_encoder.setter
    def current_encoder(self, current_encoder: 'XAMusicEncoder'):
        self.set_property('currentEncoder', current_encoder.xa_elem)

    @property
    def current_eq_preset(self) -> 'XAMusicEQPreset':
        """The currently selected equalizer preset.
        """
        return self._new_element(self.xa_scel.currentEQPreset(), XAMusicEQPreset)

    @current_eq_preset.setter
    def current_eq_preset(self, current_eq_preset: 'XAMusicEQPreset'):
        self.set_property('currentEQPreset', current_eq_preset.xa_elem)

    @property
    def current_visual(self) -> 'XAMusicVisual':
        """The currently selected visual plug-in.
        """
        return self._new_element(self.xa_scel.currentVisual(), XAMusicVisual)

    @current_visual.setter
    def current_visual(self, current_visual: 'XAMusicVisual'):
        self.set_property('currentVisual', current_visual.xa_elem)

    @property
    def eq_enabled(self) -> bool:
        """Whether the equalizer is enabled.
        """
        return self.xa_scel.eqEnabled()

    @eq_enabled.setter
    def eq_enabled(self, eq_enabled: bool):
        self.set_property('eqEnabled', eq_enabled)

    @property
    def shuffle_enabled(self) -> bool:
        """Whether songs are played in random order.
        """
        return self.xa_scel.shuffleEnabled()

    @shuffle_enabled.setter
    def shuffle_enabled(self, shuffle_enabled: bool):
        self.set_property('shuffleEnabled', shuffle_enabled)

    @property
    def shuffle_mode(self) -> 'XAMusicApplication.ShuffleMode':
        """The playback shuffle mode.
        """
        return XAMusicApplication.ShuffleMode(self.xa_scel.shuffleMode())

    @shuffle_mode.setter
    def shuffle_mode(self, shuffle_mode: 'XAMusicApplication.ShuffleMode'):
        self.set_property('shuffleMode', shuffle_mode.value)

    @property
    def song_repeat(self) -> 'XAMusicApplication.RepeatMode':
        """The playback repeat mode.
        """
        return XAMusicApplication.RepeatMode(self.xa_scel.songRepeat())

    @song_repeat.setter
    def song_repeat(self, song_repeat: 'XAMusicApplication.RepeatMode'):
        self.set_property('songRepeat', song_repeat.value)

    @property
    def visuals_enabled(self) -> bool:
        """Whether visuals are currently displayed.
        """
        return self.xa_scel.visualsEnabled()

    @visuals_enabled.setter
    def visuals_enabled(self, visuals_enabled: bool):
        self.set_property('visualsEnabled', visuals_enabled)

    @property
    def current_track(self) -> 'XAMusicTrack':
        """The currently playing (or paused but not stopped) track.
        """
        return self._new_element(self.xa_scel.currentTrack(), XAMusicTrack)

    # def convert(self, items):
    #     self.xa_scel.convert_([item.xa_elem for item in items])

    def add_to_playlist(self, urls: list[Union[str, AppKit.NSURL]], playlist):
        items = []
        for url in urls:
            if isinstance(url, str):
                url = AppKit.NSURL.alloc().initFileURLWithPath_(url)
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
        >>> app = PyXA.Application("Music")
        >>> print(app.airplay_devices())
        <<class 'PyXA.apps.Music.XAMusicAirPlayDeviceList'>['ExampleUser\\'s MacBook Pro']>

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.AirPlayDevices(), XAMusicAirPlayDeviceList, filter)

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

    def tracks(self, filter: Union[dict, None] = None) -> 'XAMusicTrackList':
        """Returns a list of tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of tracks
        :rtype: XAMusicTrackList

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.tracks(), XAMusicTrackList, filter)

    def visuals(self, filter: Union[dict, None] = None) -> 'XAMusicVisualList':
        """Returns a list of visuals, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned visuals will have, or None
        :type filter: Union[dict, None]
        :return: The list of visuals
        :rtype: XAMusicVisualList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.sources(), XAMusicVisualList, filter)



class XAMusicAirPlayDeviceList(MediaApplicationBase.XAMediaItemList):
    """A wrapper around lists of AirPlay devices that employs fast enumeration techniques.

    All properties of AirPlay devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

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
        return [XAMusicApplication.DeviceKind(XABase.OSType(x.stringValue())) for x in ls]

    def network_address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("networkAddress") or [])

    def protected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("protected") or [])

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def supports_audio(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsAudio") or [])

    def supports_audio(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsVideo") or [])

    def sound_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("soundVolume") or [])

    def by_active(self, active: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("active", active)

    def by_available(self, available: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("available", available)

    def by_kind(self, kind: XAMusicApplication.DeviceKind) -> Union['XAMusicAirPlayDevice', None]:
        # TODO
        return self.by_property("kind", kind.value)

    def by_network_address(self, network_address: str) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("networkAddress", network_address)

    def by_protected(self, protected: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("protected", protected)

    def by_selected(self, selected: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("selected", selected)

    def by_supports_audio(self, supports_audio: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("supportsAudio", supports_audio)

    def by_supports_video(self, supports_video: bool) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("supportsVideo", supports_video)

    def by_sound_volume(self, sound_volume: int) -> Union['XAMusicAirPlayDevice', None]:
        return self.by_property("soundVolume", sound_volume)

class XAMusicAirPlayDevice(MediaApplicationBase.XAMediaItem):
    """An AirPlay device.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties) 

    @property
    def active(self) -> bool:
        """Whether the device is currently being played to.
        """
        return self.xa_elem.active()

    @property
    def available(self) -> bool:
        """Whether the device is currently available.
        """
        return self.xa_elem.available()

    @property
    def kind(self) -> XAMusicApplication.DeviceKind:
        """The kind of the device.
        """
        return XAMusicApplication.DeviceKind(self.xa_elem.kind())

    @property
    def network_address(self) -> str:
        """The MAC address of the device.
        """
        return self.xa_elem.networkAddress()

    @property
    def protected(self) -> bool:
        """Whether the device is password/passcode protected.
        """
        return self.xa_elem.protected()

    @property
    def selected(self) -> bool:
        """Whether the device is currently selected.
        """
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property('selected', selected)

    @property
    def supports_audio(self) -> bool:
        """Whether the device supports audio playback.
        """
        return self.xa_elem.supportsAudio()

    @property
    def supports_video(self) -> bool:
        """Whether the device supports video playback.
        """
        return self.xa_elem.supportsVideo()

    @property
    def sound_volume(self) -> int:
        """The output volume for the device from 0 to 100.
        """
        return self.xa_elem.soundVolume()

    @sound_volume.setter
    def sound_volume(self, sound_volume: int):
        self.set_property('soundVolume', sound_volume)




class XAMusicEncoderList(MediaApplicationBase.XAMediaItemList):
    """A wrapper around lists of encoders that employs fast enumeration techniques.

    All properties of encoders can be called as methods on the wrapped list, returning a list containing each encoders's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicEncoder)

    def format(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("format") or [])

    def by_format(self, format: str) -> Union['XAMusicEncoder', None]:
        return self.by_property("format", format)

class XAMusicEncoder(MediaApplicationBase.XAMediaItem):
    """An encoder in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def format(self) -> str:
        """The data format created by the encoder.
        """
        return self.xa_elem.format()




class XAMusicEQPresetList(MediaApplicationBase.XAMediaItemList):
    """A wrapper around lists of equalizer presets that employs fast enumeration techniques.

    All properties of equalizer presets can be called as methods on the wrapped list, returning a list containing each preset's value for the property.

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

    def modifiable(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("modifiable") or [])

    def preamp(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("preamp") or [])

    def update_tracks(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("updateTracks") or [])

    def by_band1(self, band1: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band1", band1)

    def by_band2(self, band2: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band2", band2)

    def by_band3(self, band3: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band3", band3)
    
    def by_band4(self, band4: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band4", band4)

    def by_band5(self, band5: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band5", band5)

    def by_band6(self, band6: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band6", band6)

    def by_band7(self, band7: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band7", band7)

    def by_band8(self, band8: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band8", band8)

    def by_band9(self, band9: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band9", band9)

    def by_band10(self, band10: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("band10", band10)

    def by_modifiable(self, modifiable: bool) -> Union['XAMusicEQPreset', None]:
        return self.by_property("modifiable", modifiable)

    def by_preamp(self, preamp: float) -> Union['XAMusicEQPreset', None]:
        return self.by_property("preamp", preamp)

    def by_update_tracks(self, update_tracks: bool) -> Union['XAMusicEQPreset', None]:
        return self.by_property("updateTracks", update_tracks)

class XAMusicEQPreset(MediaApplicationBase.XAMediaItem):
    """An equalizer preset in Music.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def band1(self) -> float:
        """The 32 Hz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band1()

    @band1.setter
    def band1(self, band1: float):
        self.set_property('band1', band1)

    @property
    def band2(self) -> float:
        """The 64 Hz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band2()

    @band2.setter
    def band2(self, band2: float):
        self.set_property('band2', band2)

    @property
    def band3(self) -> float:
        """The 125 HZ band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band3()

    @band3.setter
    def band3(self, band3: float):
        self.set_property('band3', band3)

    @property
    def band4(self) -> float:
        """The 250 Hz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band4()

    @band4.setter
    def band4(self, band4: float):
        self.set_property('band4', band4)

    @property
    def band5(self) -> float:
        """The 500 Hz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band5()

    @band5.setter
    def band5(self, band5: float):
        self.set_property('band5', band5)

    @property
    def band6(self) -> float:
        """The 1 kHz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band6()

    @band6.setter
    def band6(self, band6: float):
        self.set_property('band6', band6)

    @property
    def band7(self) -> float:
        """The 2 kHz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band7()

    @band7.setter
    def band7(self, band7: float):
        self.set_property('band7', band7)

    @property
    def band8(self) -> float:
        """The 4 kHz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band8()

    @band8.setter
    def band8(self, band8: float):
        self.set_property('band8', band8)

    @property
    def band9(self) -> float:
        """The 8 kHz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band9()

    @band9.setter
    def band9(self, band9: float):
        self.set_property('band9', band9)

    @property
    def band10(self) -> float:
        """The 16 kHz band level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.band10()

    @band10.setter
    def band10(self, band10: float):
        self.set_property('band10', band10)

    @property
    def modifiable(self) -> bool:
        """Whether the preset can be modified.
        """
        return self.xa_elem.modifiable()

    @property
    def preamp(self) -> float:
        """The equalizer preamp level (-12.0 dB to +12.0 dB).
        """
        return self.xa_elem.preamp()

    @preamp.setter
    def preamp(self, preamp: float):
        self.set_property('preamp', preamp)

    @property
    def update_tracks(self) -> bool:
        """Whether tracks using the preset are updated when the preset is renamed or deleted.
        """
        return self.xa_elem.updateTracks()

    @update_tracks.setter
    def update_tracks(self, update_tracks: bool):
        self.set_property('updateTracks', update_tracks)




class XAMusicPlaylistList(MediaApplicationBase.XAMediaPlaylistList):
    """A wrapper around lists of playlists that employs fast enumeration techniques.

    All properties of playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicPlaylist
        super().__init__(properties, filter, obj_class)

    def disliked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("disliked") or [])

    def loved(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loved") or [])

    def by_disliked(self, disliked: bool) -> Union['XAMusicPlaylist', None]:
        return self.by_property("disliked", disliked)

    def by_loved(self, loved: bool) -> Union['XAMusicPlaylist', None]:
        return self.by_property("loved", loved)

class XAMusicPlaylist(MediaApplicationBase.XAMediaPlaylist):
    """A playlist in Music.app.

    .. seealso:: :class:`XAMusicLibraryPlaylist`, :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        if not hasattr(self, "xa_specialized"):
            if self.special_kind == XAMusicApplication.PlaylistKind.USER or self.special_kind == XAMusicApplication.PlaylistKind.NONE:
                self.__class__ = XAMusicUserPlaylist

            self.xa_specialized = True
            self.__init__(properties)

    @property
    def disliked(self) -> bool:
        """Whether the playlist is disliked.
        """
        return self.xa_elem.disliked()

    @disliked.setter
    def disliked(self, disliked: bool):
        self.set_property('disliked', disliked)

    @property
    def loved(self) -> bool:
        """Whether the playlist is loved.
        """
        return self.xa_elem.loved()

    @loved.setter
    def loved(self, loved: bool):
        self.set_property('loved', loved)

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




class XAMusicAudioCDPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of audio CD playlists that employs fast enumeration techniques.

    All properties of audio CD playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

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

    def by_artist(self, artist: str) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("artist", artist)

    def by_compilation(self, compilation: bool) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("composer", composer)

    def by_disc_count(self, disc_count: int) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("discCount", disc_count)

    def by_disc_number(self, disc_number: int) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("discNumber", disc_number)

    def by_genre(self, genre: str) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("genre", genre)

    def by_year(self, year: int) -> Union['XAMusicAudioCDPlaylist', None]:
        return self.by_property("year", year)

class XAMusicAudioCDPlaylist(XAMusicPlaylist):
    """An audio CD playlist in Music.app.

    .. seealso:: :class:`XAMusicLibraryPlaylist`, :class:`XAMusicUserPlaylist`

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def artist(self) -> str:
        """The artist of the CD.
        """
        return self.xa_elem.artist()

    @artist.setter
    def artist(self, artist: str):
        self.set_property('artist', artist)

    @property
    def compilation(self) -> bool:
        """Whether the CD is a compilation album.
        """
        return self.xa_elem.compilation()

    @compilation.setter
    def compilation(self, compilation: bool):
        self.set_property('compilation', compilation)

    @property
    def composer(self) -> str:
        """The composer of the CD.
        """
        return self.xa_elem.composer()

    @composer.setter
    def composer(self, composer: str):
        self.set_property('composer', composer)

    @property
    def disc_count(self) -> int:
        """The total number of discs in the CD's album.
        """
        return self.xa_elem.discCount()

    @disc_count.setter
    def disc_count(self, disc_count: int):
        self.set_property('discCount', disc_count)

    @property
    def disc_number(self) -> int:
        """The index of the CD disc in the source album.
        """
        return self.xa_elem.discNumber()

    @disc_number.setter
    def disc_number(self, disc_number: int):
        self.set_property('discNumber', disc_number)

    @property
    def genre(self) -> str:
        """The genre of the CD.
        """
        return self.xa_elem.genre()

    @genre.setter
    def genre(self, genre: str):
        self.set_property('genre', genre)
    
    @property
    def year(self) -> int:
        """The year the album was recorded/released.
        """
        return self.xa_elem.year()

    @year.setter
    def year(self, year: int):
        self.set_property('year', year)

    def audio_cd_tracks(self, filter: Union[dict, None] = None) -> 'XAMusicAudioCDTrackList':
        """Returns a list of audio CD tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD tracks
        :rtype: XAMusicAudioCDTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.audioCDTracks(), XAMusicAudioCDTrackList, filter)




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

    def url_tracks(self, filter: Union[dict, None] = None) -> 'MediaApplicationBase.XAMediaURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: MediaApplicationBase.XAMediaURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), MediaApplicationBase.XAMediaURLTrackList, filter)




class XAMusicSourceList(MediaApplicationBase.XAMediaSourceList):
    """A wrapper around lists of sources that employs fast enumeration techniques.

    All properties of sources can be called as methods on the wrapped list, returning a list containing each source's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicSource)

class XAMusicSource(MediaApplicationBase.XAMediaSource):
    """A media source in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def audio_cd_playlists(self, filter: Union[dict, None] = None) -> 'XAMusicAudioCDPlaylistList':
        """Returns a list of audio CD playlists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio CD playlists will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio CD playlists
        :rtype: XAMusicAudioCDPlaylistList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.audioCDPlaylists(), XAMusicAudioCDPlaylistList, filter)

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

    def file_tracks(self, filter: Union[dict, None] = None) -> 'MediaApplicationBase.XAMediaFileTrackList':
        """Returns a list of file tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of file tracks
        :rtype: MediaApplicationBase.XAMediaFileTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.fileTracks(), MediaApplicationBase.XAMediaFileTrackList, filter)

    def url_tracks(self, filter: Union[dict, None] = None) -> 'MediaApplicationBase.XAMediaURLTrackList':
        """Returns a list of URL tracks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URL tracks will have, or None
        :type filter: Union[dict, None]
        :return: The list of URL tracks
        :rtype: MediaApplicationBase.XAMediaURLTrackList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.URLTracks(), MediaApplicationBase.XAMediaURLTrackList, filter)




class XAMusicTrackList(MediaApplicationBase.XAMediaTrackList):
    """A wrapper around lists of music tracks that employs fast enumeration techniques.

    All properties of music tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
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
        return [XAMusicApplication.iCloudStatus(XABase.OSType(x.stringValue())) for x in ls]

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

    def by_album_artist(self, album_artist: str) -> Union['XAMusicTrack', None]:
        return self.by_property("albumArtist", album_artist)

    def by_album_disliked(self, album_disliked: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("albumDisliked", album_disliked)

    def by_album_loved(self, album_loved: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("albumLoved", album_loved)

    def by_artist(self, artist: str) -> Union['XAMusicTrack', None]:
        return self.by_property("artist", artist)

    def by_bpm(self, bpm: int) -> Union['XAMusicTrack', None]:
        return self.by_property("bpm", bpm)

    def by_cloud_status(self, cloud_status: XAMusicApplication.iCloudStatus) -> Union['XAMusicTrack', None]:
        # TODO
        return self.by_property("cloudStatus", cloud_status.value)

    def by_compilation(self, compilation: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("compilation", compilation)

    def by_composer(self, composer: str) -> Union['XAMusicTrack', None]:
        return self.by_property("composer", composer)

    def by_disliked(self, disliked: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("disliked", disliked)

    def by_eq(self, eq: str) -> Union['XAMusicTrack', None]:
        return self.by_property("EQ", eq)

    def by_gapless(self, gapless: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("gapless", gapless)

    def by_loved(self, loved: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("loved", loved)

    def by_lyrics(self, lyrics: str) -> Union['XAMusicTrack', None]:
        return self.by_property("lyrics", lyrics)

    def by_modification_date(self, modification_date: datetime) -> Union['XAMusicTrack', None]:
        return self.by_property("modificationDate", modification_date)

    def by_movement(self, movement: str) -> Union['XAMusicTrack', None]:
        return self.by_property("movement", movement)

    def by_movement_count(self, movement_count: int) -> Union['XAMusicTrack', None]:
        return self.by_property("movementCount", movement_count)

    def by_movement_number(self, movement_number: int) -> Union['XAMusicTrack', None]:
        return self.by_property("movementNumber", movement_number)

    def by_shufflable(self, shufflable: bool) -> Union['XAMusicTrack', None]:
        return self.by_property("shufflable", shufflable)

    def by_sort_artist(self, sort_artist: str) -> Union['XAMusicTrack', None]:
        return self.by_property("sortArtist", sort_artist)

    def by_sort_album_artist(self, sort_album_artist: str) -> Union['XAMusicTrack', None]:
        return self.by_property("sortAlbumArtist", sort_album_artist)

    def by_sort_composer(self, sort_composer: str) -> Union['XAMusicTrack', None]:
        return self.by_property("sortComposer", sort_composer)

    def by_work(self, work: str) -> Union['XAMusicTrack', None]:
        return self.by_property("work", work)

class XAMusicTrack(MediaApplicationBase.XAMediaTrack):
    """A class for managing and interacting with tracks in Music.app.

    .. seealso:: :class:`XAMusicSharedTrack`, :class:`MediaApplicationBase.XAMediaFileTrack`, :class:`XAMusicRemoteURLTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        # print("Track type", self.objectClass.data())
        # if self.objectClass.data() == _SHARED_TRACK:
        #     self.__class__ = XAMusicSharedTrack
        #     self.__init__()
        # elif self.objectClass.data() == _FILE_TRACK:
        #     self.__class__ = MediaApplicationBase.XAMediaFileTrack
        #     self.__init__()
        # elif self.objectClass.data() == _URL_TRACK:
        #     self.__class__ = MediaApplicationBase.XAMediaURLTrack
        #     self.__init__()

    @property
    def album_artist(self) -> str:
        """The album artist of the track.
        """
        return self.xa_elem.albumArtist()

    @album_artist.setter
    def album_artist(self, album_artist: str):
        self.set_property('albumArtist', album_artist)

    @property
    def album_disliked(self) -> bool:
        """Whether the album for the track is disliked.
        """
        return self.xa_elem.albumDisliked()

    @album_disliked.setter
    def album_disliked(self, album_disliked: bool):
        self.set_property('albumDisliked', album_disliked)

    @property
    def album_loved(self) -> bool:
        """Whether the album for the track is loved.
        """
        return self.xa_elem.albumLoved()

    @album_loved.setter
    def album_loved(self, album_loved: bool):
        self.set_property('albumLoved', album_loved)

    @property
    def artist(self) -> str:
        """The artist/source of the track.
        """
        return self.xa_elem.artist()

    @artist.setter
    def artist(self, artist: str):
        self.set_property('artist', artist)

    @property
    def bpm(self) -> int:
        """The tempo of the track in beats per minute.
        """
        return self.xa_elem.bpm()

    @bpm.setter
    def bpm(self, bpm: int):
        self.set_property('bpm', bpm)

    @property
    def cloud_status(self) -> XAMusicApplication.iCloudStatus:
        """The iCloud status of the track.
        """
        return XAMusicApplication.iCloudStatus(self.xa_elem.cloudStatus())

    @property
    def compilation(self) -> bool:
        """Whether the track is from a compilation album.
        """
        return self.xa_elem.compilation()

    @compilation.setter
    def compilation(self, compilation: bool):
        self.set_property('compilation', compilation)

    @property
    def composer(self) -> str:
        """The composer of the track.
        """
        return self.xa_elem.composer()

    @composer.setter
    def composer(self, composer: str):
        self.set_property('composer', composer)

    @property
    def disliked(self) -> bool:
        """Whether the track is disliked.
        """
        return self.xa_elem.disliked()

    @disliked.setter
    def disliked(self, disliked: bool):
        self.set_property('disliked', disliked)

    @property
    def eq(self) -> str:
        """The name of the EQ preset of the track.
        """
        return self.xa_elem.EQ()

    @eq.setter
    def eq(self, eq: str):
        self.set_property('EQ', eq)

    @property
    def gapless(self) -> bool:
        """Whether the track is a from a gapless album.
        """
        return self.xa_elem.gapless()

    @gapless.setter
    def gapless(self, gapless: bool):
        self.set_property('gapless', gapless)

    @property
    def loved(self) -> bool:
        """Whether the track is loved.
        """
        return self.xa_elem.loved()

    @loved.setter
    def loved(self, loved: bool):
        self.set_property('loved', loved)

    @property
    def lyrics(self) -> str:
        """The lyrics of the track.
        """
        return self.xa_elem.lyrics()

    @lyrics.setter
    def lyrics(self, lyrics: str):
        self.set_property('lyrics', lyrics)

    @property
    def movement(self) -> str:
        """The movement name of the track.
        """
        return self.xa_elem.movement()

    @movement.setter
    def movement(self, movement: str):
        self.set_property('movement', movement)

    @property
    def movement_count(self) -> int:
        """The total number of movements in the work.
        """
        return self.xa_elem.movementCount()

    @movement_count.setter
    def movement_count(self, movement_count: int):
        self.set_property('movementCount', movement_count)

    @property
    def movement_number(self) -> int:
        """The index of the movement in the work.
        """
        return self.xa_elem.movementNumber()

    @movement_number.setter
    def movement_number(self, movement_number: int):
        self.set_property('movementNumber', movement_number)

    @property
    def shufflable(self) -> bool:
        """Whether the track is included when shuffling.
        """
        return self.xa_elem.shufflable()

    @shufflable.setter
    def shufflable(self, shufflable: bool):
        self.set_property('shufflable', shufflable)

    @property
    def sort_artist(self) -> str:
        """The string used for this track when sorting by artist.
        """
        return self.xa_elem.sortArtist()

    @sort_artist.setter
    def sort_artist(self, sort_artist: str):
        self.set_property('sortArtist', sort_artist)

    @property
    def sort_album_artist(self) -> str:
        """The string used for this track when sorting by album artist.
        """
        return self.xa_elem.sortAlbumArtist()

    @sort_album_artist.setter
    def sort_album_artist(self, sort_album_artist: str):
        self.set_property('sortAlbumArtist', sort_album_artist)

    @property
    def sort_composer(self) -> str:
        """The string used for this track when sorting by composer.
        """
        return self.xa_elem.sortComposer()

    @sort_composer.setter
    def sort_composer(self, sort_composer: str):
        self.set_property('sortComposer', sort_composer)

    @property
    def work(self) -> str:
        """The work name of the track.
        """
        return self.xa_elem.work()

    @work.setter
    def work(self, work: str):
        self.set_property('work', work)



class XAMusicAudioCDTrackList(XAMusicTrackList):
    """A wrapper around lists of music audio CD tracks that employs fast enumeration techniques.

    All properties of music audio CD tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicAudioCDTrack)

    def location(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("location") or []
        return [XABase.XAURL(x) for x in ls]

    def by_location(self, location: XABase.XAURL) -> Union['XAMusicAudioCDTrack', None]:
        return self.by_property("location", location.xa_elem)

class XAMusicAudioCDTrack(XAMusicTrack):
    """An audio CD track in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def location(self) -> XABase.XAPath:
        """The location of the file represented by the track.
        """
        return XABase.XAPath(self.xa_elem.location())

    @location.setter
    def location(self, location: XABase.XAPath):
        self.set_property('location', location.xa_elem)



class XAMusicUserPlaylistList(XAMusicPlaylistList):
    """A wrapper around lists of music user playlists that employs fast enumeration techniques.

    All properties of music user playlists can be called as methods on the wrapped list, returning a list containing each playlist's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAMusicUserPlaylist)

    def genius(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("genius") or [])

    def by_genius(self, genius: bool) -> Union['XAMusicUserPlaylist', None]:
        return self.by_property("genius", genius)

class XAMusicUserPlaylist(XAMusicPlaylist):
    """A user-created playlist in Music.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def genius(self) -> bool:
        """Whether the playlist is a genius playlist.
        """
        return self.xa_elem.genius()




class XAMusicVisualList(MediaApplicationBase.XAMediaItemList):
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



class XAMusicWindowList(MediaApplicationBase.XAMediaWindowList):
    """A wrapper around lists of music windows that employs fast enumeration techniques.

    All properties of music windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAMusicWindow
        super().__init__(properties, filter, obj_class)

class XAMusicWindow(MediaApplicationBase.XAMediaWindow, XABaseScriptable.XASBWindow):
    """A windows of Music.app.

    .. seealso:: :class:`XAMusicBrowserWindow`, :class:`XAMusicPlaylistWindow`, :class:`XAMusicVideoWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        obj_class = self.xa_elem.objectClass().data()
        if not hasattr(self, "xa_specialized"):
            if obj_class == b'WrBc':
                self.__class__ = MediaApplicationBase.XAMediaBrowserWindow
            elif obj_class == b'WlPc':
                self.__class__ = MediaApplicationBase.XAMediaPlaylistWindow
            elif obj_class == b'niwc':
                self.__class__ = MediaApplicationBase.XAMediaVideoWindow
            elif obj_class == b'WPMc':
                self.__class__ = XAMusicMiniplayerWindow
            elif obj_class == b'WQEc':
                self.__class__ = XAMusicEQWindow
            self.xa_specialized = True
            self.__init__(properties)




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
