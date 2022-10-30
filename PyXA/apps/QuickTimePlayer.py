""".. versionadded:: 0.0.6

Control the macOS QuickTime application using JXA-like syntax.
"""
from typing import Any, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath

class XAQuickTimeApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with QuickTime.app.

    .. seealso:: :class:`XAQuickTimeWindow`, :class:`XAQuickTimeDocument`, :class:`XAQuickTimeAudioRecordingDevice`, :class:`XAQuickTimeVideoRecordingDevice`, :class:`XAQuickTimeAudioCompressionPreset`, :class:`XAQuickTimeMovieCompressionPreset`, :class:`XAQuickTimeScreenCompressionPreset`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAQuickTimeWindow

        self.properties: dict #: Every property of the QuickTime application
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether QuickTime is the frontmost application
        self.version: str #: The version of QuickTime.app
        self.current_document: XAQuickTimeDocument #: The document currently open in the front window of QuickTime

    @property
    def properties(self) -> dict:
        return self.xa_scel.properties()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def current_document(self) -> 'XAQuickTimeDocument':
        return self.front_window.document

    def open(self, path: Union[str, AppKit.NSURL]) -> 'XAQuickTimeDocument':
        """Opens the file at the given filepath.

        :param target: The path of a file to open.
        :type target: Union[str, AppKit.NSURL]
        :return: A reference to the newly opened document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        if not isinstance(path, AppKit.NSURL):
            if "://" not in path:
                path = XABase.XAPath(path)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self._new_element(self.front_window.document, XAQuickTimeDocument)

    def open_url(self, url: Union[str, AppKit.NSURL]) -> 'XAQuickTimeDocument':
        """Opens the file at the given (remote) URL.

        :param target: The path of a file to stream.
        :type target: Union[str, NSURL]
        :return: A reference to the newly opened document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        if not isinstance(url, AppKit.NSURL):
            if "://" not in url:
                url = XABase.XAURL(url)
        self.xa_scel.openURL_(url)

    def new_audio_recording(self) -> 'XAQuickTimeDocument':
        """Starts a new audio recording.

        :return: The newly created audio recording document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_scel.newAudioRecording()

    def new_movie_recording(self) -> 'XAQuickTimeDocument':
        """Starts a new movie recording.

        :return: The newly created movie recording document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_scel.newMovieRecording()

    def new_screen_recording(self) -> 'XAQuickTimeApplication':
        """Starts a new screen recording.

        :return: A reference to the application object.
        :rtype: XAQuickTimeApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.newScreenRecording()
        return self

    def documents(self, filter: Union[dict, None] = None) -> 'XAQuickTimeDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAQuickTimeDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.documents(), XAQuickTimeDocumentList, filter)

    def audio_recording_devices(self, filter: Union[dict, None] = None) -> 'XAQuickTimeAudioRecordingDeviceList':
        """Returns a list of audio recording devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio recording devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio recording devices
        :rtype: XAQuickTimeAudioRecordingDeviceList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.audioRecordingDevices(), XAQuickTimeAudioRecordingDeviceList, filter)

    def video_recording_devices(self, filter: Union[dict, None] = None) -> 'XAQuickTimeVideoRecordingDeviceList':
        """Returns a list of video recording devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video recording devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of video recording devices
        :rtype: XAQuickTimeVideoRecordingDeviceList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.videoRecordingDevices(), XAQuickTimeVideoRecordingDeviceList, filter)

    def audio_compression_presets(self, filter: Union[dict, None] = None) -> 'XAQuickTimeAudioCompressionPresetList':
        """Returns a list of audio compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned p[resets] will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio compression presets
        :rtype: XAQuickTimeAudioCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.audioCompressionPresets(), XAQuickTimeAudioCompressionPresetList, filter)

    def movie_compression_presets(self, filter: Union[dict, None] = None) -> 'XAQuickTimeMovieCompressionPresetList':
        """Returns a list of movie compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of movie compression presets
        :rtype: XAQuickTimeMovieCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.movieCompressionPresets(), XAQuickTimeMovieCompressionPresetList, filter)

    def screen_compression_presets(self, filter: Union[dict, None] = None) -> 'XAQuickTimeScreenCompressionPresetList':
        """Returns a list of screen compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of screen compression presets
        :rtype: XAQuickTimeScreenCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.screenCompressionPresets(), XAQuickTimeScreenCompressionPresetList, filter)



class XAQuickTimeWindow(XABaseScriptable.XASBWindow):
    """A QuickTime window.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier for the window
        self.bounds: tuple[int, int, int, int] #: The boundary rectangle for the window
        self.name: str #: The name of the window
        self.index: int #: The index of the window in the front-to-back order of Finder windows
        self.closeable: bool #: Whether the window has a close button
        self.resizable: bool #: Whether the window can be resized
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.visible: bool #: Whether the window is currently visible
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.properties: dict #: Every property of a QuickTime window
        self.document: XAQuickTimeDocument #: The document currently displayed in the front window of QuickTime

    @property
    def id(self) -> int:
        return self.xa_elem.id()

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
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property("miniaturized", miniaturized)

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def document(self) -> 'XAQuickTimeDocument':
        return self._new_element(self.xa_elem.document(), XAQuickTimeDocument)

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], tuple):
                # Value is a rectangle boundary
                x = value[0][0]
                y = value[0][1]
                w = value[1][0]
                h = value[1][1]
                value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        super().set_property(property_name, value)




class XAQuickTimeDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeDocument, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each document in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def audio_volume(self) -> list[float]:
        """Gets the audio volume of each document in the list.

        :return: The list of audio volumes
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("audioVolume"))

    def current_time(self) -> list[float]:
        """Gets the current time of each document in the list.

        :return: The list of current times
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("currentTime"))

    def data_rate(self) -> list[int]:
        """Gets the data rate of each document in the list.

        :return: The list of data rates
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dataRate"))

    def data_size(self) -> list[int]:
        """Gets the data size of each document in the list.

        :return: The list of data sizes
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dataSize"))

    def duration(self) -> list[float]:
        """Gets the duration of each document in the list.

        :return: The list of durations
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duration"))

    def looping(self) -> list[bool]:
        """Gets the looping status of each document in the list.

        :return: The list of looping status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("looping"))

    def muted(self) -> list[bool]:
        """Gets the muted status of each document in the list.

        :return: The list of muted status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("muted"))

    def natural_dimensions(self) -> list[tuple[int, int]]:
        """Gets the natural dimensions of each document in the list.

        :return: The list of document dimensions
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("naturalDimensions"))

    def playing(self) -> list[bool]:
        """Gets the playing status of each document in the list.

        :return: The list of playing status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("playing"))

    def rate(self) -> list[float]:
        """Gets the rate of each document in the list.

        :return: The list of rates
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rate"))

    def presenting(self) -> list[bool]:
        """Gets the presenting status of each document in the list.

        :return: The list of presenting status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("presenting"))

    def current_microphone(self) -> 'XAQuickTimeAudioRecordingDeviceList':
        """Gets the audio recording device of each document in the list.

        :return: The list of audio recording devices
        :rtype: XAQuickTimeAudioRecordingDeviceList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentMicrophone")
        return self._new_element(ls, XAQuickTimeAudioRecordingDeviceList)

    def current_camera(self) -> 'XAQuickTimeVideoRecordingDeviceList':
        """Gets the video recording device of each document in the list.

        :return: The list of video recording devices
        :rtype: XAQuickTimeVideoRecordingDeviceList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentCamera")
        return self._new_element(ls, XAQuickTimeVideoRecordingDeviceList)

    def current_audio_compression(self) -> 'XAQuickTimeAudioCompressionPresetList':
        """Gets the audio compression preset device of each document in the list.

        :return: The list of audio compression presets
        :rtype: XAQuickTimeVideoRecordingDeviceList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentAudioCompression")
        return self._new_element(ls, XAQuickTimeAudioCompressionPresetList)

    def current_movie_compression(self) -> 'XAQuickTimeMovieCompressionPresetList':
        """Gets the movie compression preset device of each document in the list.

        :return: The list of movie compression presets
        :rtype: XAQuickTimeMovieCompressionPresetList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentMovieCompression")
        return self._new_element(ls, XAQuickTimeMovieCompressionPresetList)

    def current_screen_compression(self) -> 'XAQuickTimeScreenCompressionPresetList':
        """Gets the screen compression preset device of each document in the list.

        :return: The list of screen compression presets
        :rtype: XAQuickTimeScreenCompressionPresetList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentScreenCompression")
        return self._new_element(ls, XAQuickTimeScreenCompressionPresetList)

    def by_properties(self, properties: dict) -> 'XAQuickTimeDocument':
        """Retrieves the document whose properties matches the given properties, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_audio_volume(self, audio_volume: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose audio volume matches the given volume, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("audioVolume", audio_volume)

    def by_current_time(self, current_time: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current time matches the given time, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentTime", current_time)

    def by_data_rate(self, data_rate: int) -> 'XAQuickTimeDocument':
        """Retrieves the document whose data rate matches the given rate, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("dataRate", data_rate)

    def by_data_size(self, data_size: int) -> 'XAQuickTimeDocument':
        """Retrieves the document whose data size matches the given size, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("dataSize", data_size)

    def by_duration(self, duration: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose duration matches the given duration, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("duration", duration)

    def by_looping(self, looping: bool) -> 'XAQuickTimeDocument':
        """Retrieves the document whose looping status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("looping", looping)

    def by_muted(self, muted: bool) -> 'XAQuickTimeDocument':
        """Retrieves the document whose muted status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("muted", muted)

    def by_natural_dimensions(self, natural_dimensions: tuple[int, int]) -> 'XAQuickTimeDocument':
        """Retrieves the document whose natural dimensions match the given dimensions, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("naturalDimensions", natural_dimensions)

    def by_playing(self, playing: bool) -> 'XAQuickTimeDocument':
        """Retrieves the document whose playing status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("playing", playing)

    def by_rate(self, rate: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose rate matches the given rate, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("rate", rate)

    def by_presenting(self, presenting: bool) -> 'XAQuickTimeDocument':
        """Retrieves the document whose presenting status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("presenting", presenting)

    def by_current_microphone(self, current_microphone: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current microphone matches the given microphone, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentMicrophone", current_microphone.xa_elem)

    def by_current_camera(self, current_camera: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current camera matches the given camera, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentCamera", current_camera.xa_elem)

    def by_current_audio_compression(self, current_audio_compression: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current audio compression present matches the given preset, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentAudioCompression", current_audio_compression.xa_elem)

    def by_current_movie_compression(self, current_movie_compression: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current movie compression present matches the given preset, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentMovieCompression", current_movie_compression.xa_elem)

    def by_current_screen_compression(self, current_screen_compression: float) -> 'XAQuickTimeDocument':
        """Retrieves the document whose current screen compression present matches the given preset, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAQuickTimeDocument, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("currentScreenCompression", current_screen_compression.xa_elem)

class XAQuickTimeDocument(XABase.XAObject):
    """A class for managing and interacting with documents in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.audio_volume: float #: The volume of the movie from 0 to 1 (0 to 100%)
        self.current_time: float #: The current time of the movie in seconds
        self.data_rate: int #: The data rate of the movie in bytes per second
        self.data_size: int #: The data size of the movie in bytes
        self.duration: float #: The duration of the movie in seconds
        self.looping: bool #: Whether the movie plays in a loop
        self.muted: bool #: Whether the movie is muted
        self.natural_dimensions: tuple[int, int] #: The national dimensions of the movie
        self.playing: bool #: Whether the movie is currently playing
        self.rate: float #: The current rate of the movie
        self.presenting: bool #: Whether the movie is presented in full screen
        self.current_microphone: XAQuickTimeAudioRecordingDevice #: The currently previewing audio device
        self.current_camera: XAQuickTimeVideoRecordingDevice #: The currently previewing video device
        self.current_audio_compression: XAQuickTimeAudioCompressionPreset #: The current audio compression preset
        self.current_movie_compression: XAQuickTimeMovieCompressionPreset #: The current movie compression preset
        self.current_screen_compression: XAQuickTimeScreenCompressionPreset #: The current screen compression preset

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def audio_volume(self) -> float:
        return self.xa_elem.audioVolume()

    @audio_volume.setter
    def audio_volume(self, audio_volume: float):
        self.set_property("audioVolume", audio_volume)

    @property
    def current_time(self) -> float:
        return self.xa_elem.currentTime()

    @current_time.setter
    def current_time(self, current_time: float):
        self.set_property("currentTime", current_time)

    @property
    def data_rate(self) -> int:
        return self.xa_elem.dataRate()

    @property
    def data_size(self) -> int:
        return self.xa_elem.dataSize()

    @property
    def duration(self) -> float:
        return self.xa_elem.duration()

    @property
    def looping(self) -> bool:
        return self.xa_elem.looping()

    @looping.setter
    def looping(self, looping: bool):
        self.set_property("looping", looping)

    @property
    def muted(self) -> bool:
        return self.xa_elem.muted()

    @muted.setter
    def muted(self, muted: bool):
        self.set_property("muted", muted)

    @property
    def natural_dimensions(self) -> tuple[int, int]:
        return self.xa_elem.naturalDimensions()

    @property
    def playing(self) -> bool:
        return self.xa_elem.playing()

    @property
    def rate(self) -> float:
        return self.xa_elem.rate()

    @rate.setter
    def rate(self, rate: float):
        self.set_property("rate", rate)

    @property
    def presenting(self) -> bool:
        return self.xa_elem.presenting()

    @presenting.setter
    def presenting(self, presenting: bool):
        self.set_property("presenting", presenting)

    @property
    def current_microphone(self) -> 'XAQuickTimeAudioRecordingDevice':
        return self._new_element(self.xa_elem.currentMicrophone(), XAQuickTimeAudioRecordingDevice)

    @current_microphone.setter
    def current_microphone(self, current_microphone: 'XAQuickTimeAudioRecordingDevice'):
        self.set_property("currentMicrophone", current_microphone.xa_elem)

    @property
    def current_camera(self) -> 'XAQuickTimeVideoRecordingDevice':
        return self._new_element(self.xa_elem.currentCamera(), XAQuickTimeVideoRecordingDevice)

    @current_camera.setter
    def current_camera(self, current_camera: 'XAQuickTimeVideoRecordingDevice'):
        self.set_property("currentCamera", current_camera.xa_elem)

    @property
    def current_audio_compression(self) -> 'XAQuickTimeAudioCompressionPreset':
        return self._new_element(self.xa_elem.currentAudioCompression(), XAQuickTimeAudioCompressionPreset)

    @current_audio_compression.setter
    def current_audio_compression(self, current_audio_compression: 'XAQuickTimeAudioCompressionPreset'):
        self.set_property("currentAudioCompression", current_audio_compression.xa_elem)

    @property
    def current_movie_compression(self) -> 'XAQuickTimeMovieCompressionPreset':
        return self._new_element(self.xa_elem.currentMovieCompression(), XAQuickTimeMovieCompressionPreset)

    @current_movie_compression.setter
    def current_movie_compression(self, current_movie_compression: 'XAQuickTimeMovieCompressionPreset'):
        self.set_property("currentMovieCompression", current_movie_compression.xa_elem)

    @property
    def current_screen_compression(self) -> 'XAQuickTimeScreenCompressionPreset':
        return self._new_element(self.xa_elem.currentScreenCompression(), XAQuickTimeScreenCompressionPreset)

    @current_screen_compression.setter
    def current_screen_compression(self, current_screen_compression: 'XAQuickTimeScreenCompressionPreset'):
        self.set_property("currentScreenCompression", current_screen_compression.xa_elem)

    def play(self) -> 'XAQuickTimeDocument':
        self.xa_elem.play()
        return self

    def start(self) -> 'XAQuickTimeDocument':
        self.xa_elem.start()
        return self

    def pause(self) -> 'XAQuickTimeDocument':
        self.xa_elem.pause()
        return self

    def resume(self) -> 'XAQuickTimeDocument':
        self.xa_elem.resume()
        return self

    def stop(self) -> 'XAQuickTimeDocument':
        self.xa_elem.stop()
        return self

    def step_backward(self, num_steps: int) -> 'XAQuickTimeDocument':
        self.xa_elem.stepBackwardBy_(num_steps)
        return self

    def step_forward(self, num_steps: int) -> 'XAQuickTimeDocument':
        self.xa_elem.stepForwardBy_(num_steps)
        return self

    def trim(self, start_time: float, end_time: float) -> 'XAQuickTimeDocument':
        self.xa_elem.trimFrom_to_(start_time, end_time)
        return self

    def present(self) -> 'XAQuickTimeDocument':
        self.xa_elem.present()
        return self




class XAQuickTimeAudioRecordingDeviceList(XABase.XAList):
    """A wrapper around lists of audio recording devices that employs fast enumeration techniques.

    All properties of audio recording devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeAudioRecordingDevice, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each device in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each device in the list.

        :return: The list of names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each device in the list.

        :return: The list of IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ID"))

class XAQuickTimeAudioRecordingDevice(XABase.XAObject):
    """A class for managing and interacting with microphones in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the device
        self.name: str #: The name of the device
        self.id: str #: The unique identifier for the device

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()




class XAQuickTimeVideoRecordingDeviceList(XABase.XAList):
    """A wrapper around lists of video recording devices that employs fast enumeration techniques.

    All properties of video recording devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeVideoRecordingDevice, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each device in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each device in the list.

        :return: The list of names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each device in the list.

        :return: The list of IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ID"))

class XAQuickTimeVideoRecordingDevice(XABase.XAObject):
    """A class for managing and interacting with cameras in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the device
        self.name: str #: The name of the device
        self.id: str #: The unique identifier for the device

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()
    
    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()




class XAQuickTimeAudioCompressionPresetList(XABase.XAList):
    """A wrapper around lists of audio compression presets that employs fast enumeration techniques.

    All properties of audio compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeAudioCompressionPreset, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each preset in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each preset in the list.

        :return: The list of names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each preset in the list.

        :return: The list of IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ID"))

class XAQuickTimeAudioCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with audio compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the preset
        self.name: str #: The name of the preset
        self.id: str #: The unique identifier for the preset

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()
    
    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()




class XAQuickTimeMovieCompressionPresetList(XABase.XAList):
    """A wrapper around lists of movie compression presets that employs fast enumeration techniques.

    All properties of movie compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeMovieCompressionPreset, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each preset in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each preset in the list.

        :return: The list of names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each preset in the list.

        :return: The list of IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ID"))

class XAQuickTimeMovieCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with movie compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the preset
        self.name: str #: The name of the preset
        self.id: str #: The unique identifier for the preset

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()
    
    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()




class XAQuickTimeScreenCompressionPresetList(XABase.XAList):
    """A wrapper around lists of screen compression presets that employs fast enumeration techniques.

    All properties of screen compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeScreenCompressionPreset, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each preset in the list.

        :return: The list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each preset in the list.

        :return: The list of names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each preset in the list.

        :return: The list of IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ID"))

class XAQuickTimeScreenCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with screen compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the preset
        self.name: str #: The name of the preset
        self.id: str #: The unique identifier for the preset

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()
    
    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()