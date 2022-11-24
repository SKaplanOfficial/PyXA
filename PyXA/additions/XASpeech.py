""".. versionadded:: 0.1.1

A collection of classes for handling speak input and output.
"""

import time
from datetime import datetime, timedelta
from typing import Any, Callable, Union

import AppKit
import AVFoundation
import Speech
from PyObjCTools import AppHelper

from PyXA import XABase


class XACommandDetector():
    """A command-based query detector.

    .. versionadded:: 0.0.9
    """
    def __init__(self, command_function_map: Union[dict[str, Callable[[], Any]], None] = None):
        """Creates a command detector object.

        :param command_function_map: A dictionary mapping command strings to function objects
        :type command_function_map: dict[str, Callable[[], Any]]

        .. versionadded:: 0.0.9
        """
        self.command_function_map = command_function_map or {} #: The dictionary of commands and corresponding functions to run upon detection

    def on_detect(self, command: str, function: Callable[[], Any]):
        """Adds or replaces a command to listen for upon calling :func:`listen`, and associates the given function with that command.

        :param command: The command to listen for
        :type command: str
        :param function: The function to call when the command is heard
        :type function: Callable[[], Any]

        :Example:

        >>> detector = PyXA.XACommandDetector()
        >>> detector.on_detect("go to google", PyXA.XAURL("http://google.com").open)
        >>> detector.listen()

        .. versionadded:: 0.0.9
        """
        self.command_function_map[command] = function

    def listen(self) -> Any:
        """Begins listening for the specified commands.

        :return: The execution return value of the corresponding command function
        :rtype: Any

        :Example:

        >>> import PyXA
        >>> PyXA.speak("What app do you want to open?")
        >>> PyXA.XACommandDetector({
        >>>     "safari": PyXA.Application("Safari").activate,
        >>>     "messages": PyXA.Application("Messages").activate,
        >>>     "shortcuts": PyXA.Application("Shortcuts").activate,
        >>>     "mail": PyXA.Application("Mail").activate,
        >>>     "calendar": PyXA.Application("Calendar").activate,
        >>>     "notes": PyXA.Application("Notes").activate,
        >>>     "music": PyXA.Application("Music").activate,
        >>>     "tv": PyXA.Application("TV").activate,
        >>>     "pages": PyXA.Application("Pages").activate,
        >>>     "numbers": PyXA.Application("Numbers").activate,
        >>>     "keynote": PyXA.Application("Keynote").activate,
        >>> }).listen()

        .. versionadded:: 0.0.9
        """
        command_function_map = self.command_function_map
        return_value = None
        class NSSpeechRecognizerDelegate(AppKit.NSObject):
            def speechRecognizer_didRecognizeCommand_(self, recognizer, cmd):
                return_value = command_function_map[cmd]()
                AppHelper.stopEventLoop()

        recognizer = AppKit.NSSpeechRecognizer.alloc().init()
        recognizer.setCommands_(list(command_function_map.keys()))
        recognizer.setBlocksOtherRecognizers_(True)
        recognizer.setDelegate_(NSSpeechRecognizerDelegate.alloc().init().retain())
        recognizer.startListening()
        AppHelper.runConsoleEventLoop()

        return return_value




class XASpeechRecognizer():
    """A rule-based query detector.

    .. versionadded:: 0.0.9
    """
    def __init__(self, finish_conditions: Union[None, dict[Callable[[str], bool], Callable[[str], bool]]] = None):
        """Creates a speech recognizer object.

        By default, with no other rules specified, the Speech Recognizer will timeout after 10 seconds once :func:`listen` is called.

        :param finish_conditions: A dictionary of rules and associated methods to call when a rule evaluates to true, defaults to None
        :type finish_conditions: Union[None, dict[Callable[[str], bool], Callable[[str], bool]]], optional

        .. versionadded:: 0.0.9
        """
        default_conditions = {
            lambda x: self.time_elapsed > timedelta(seconds = 10): lambda x: self.spoken_query,
        }
        self.finish_conditions: Callable[[str], bool] = finish_conditions or default_conditions #: A dictionary of rules and associated methods to call when a rule evaluates to true
        self.spoken_query: str = "" #: The recognized spoken input
        self.start_time: datetime #: The time that the Speech Recognizer begins listening
        self.time_elapsed: timedelta #: The amount of time passed since the start time

    def __prepare(self):
        # Request microphone access if we don't already have it
        Speech.SFSpeechRecognizer.requestAuthorization_(None)

        # Set up audio session
        self.audio_session = AVFoundation.AVAudioSession.sharedInstance()
        self.audio_session.setCategory_mode_options_error_(AVFoundation.AVAudioSessionCategoryRecord, AVFoundation.AVAudioSessionModeMeasurement, AVFoundation.AVAudioSessionCategoryOptionDuckOthers, None)
        self.audio_session.setActive_withOptions_error_(True, AVFoundation.AVAudioSessionSetActiveOptionNotifyOthersOnDeactivation, None)

        # Set up recognition request
        self.recognizer = Speech.SFSpeechRecognizer.alloc().init()
        self.recognition_request = Speech.SFSpeechAudioBufferRecognitionRequest.alloc().init()
        self.recognition_request.setShouldReportPartialResults_(True)

        # Set up audio engine
        self.audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self.input_node = self.audio_engine.inputNode()
        recording_format = self.input_node.outputFormatForBus_(0)
        self.input_node.installTapOnBus_bufferSize_format_block_(0, 1024, recording_format,
            lambda buffer, _when: self.recognition_request.appendAudioPCMBuffer_(buffer))
        self.audio_engine.prepare()
        self.audio_engine.startAndReturnError_(None)

    def on_detect(self, rule: Callable[[str], bool], method: Callable[[str], bool]):
        """Sets the given rule to call the specified method if a spoken query passes the rule.

        :param rule: A function that takes the spoken query as a parameter and returns a boolean value depending on whether the query passes a desired rule
        :type rule: Callable[[str], bool]
        :param method: A function that takes the spoken query as a parameter and acts on it
        :type method: Callable[[str], bool]

        .. versionadded:: 0.0.9
        """
        self.finish_conditions[rule] = method

    def listen(self) -> Any:
        """Begins listening for a query until a rule returns True.

        :return: The value returned by the method invoked upon matching some rule
        :rtype: Any

        .. versionadded:: 0.0.9
        """
        self.start_time = datetime.now()
        self.time_elapsed = None
        self.__prepare()

        old_self = self
        def detect_speech(transcription, error):
            if error is not None:
                print("Failed to detect speech. Error: ", error)
            else:
                old_self.spoken_query = transcription.bestTranscription().formattedString()
                print(old_self.spoken_query)

        recognition_task = self.recognizer.recognitionTaskWithRequest_resultHandler_(self.recognition_request, detect_speech)
        while self.spoken_query == "" or not any(x(self.spoken_query) for x in self.finish_conditions):
            self.time_elapsed = datetime.now() - self.start_time
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = 0.5))

        self.audio_engine.stop()
        for rule, method in self.finish_conditions.items():
            if rule(self.spoken_query):
                return method(self.spoken_query)




class XASpeech():
    def __init__(self, message: str = "", voice: Union[str, None] = None, volume: float = 0.5, rate: int = 200):
        self.message: str = message #: The message to speak
        self.voice: Union[str, None] = voice #: The voice that the message is spoken in
        self.volume: float = volume #: The speaking volume
        self.rate: int = rate #: The speaking rate

    def voices(self) -> list[str]:
        """Gets the list of voice names available on the system.

        :return: The list of voice names
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> speaker = PyXA.XASpeech()
        >>> print(speaker.voices())
        ['Agnes', 'Alex', 'Alice', 'Allison',

        .. versionadded:: 0.0.9
        """
        ls = AppKit.NSSpeechSynthesizer.availableVoices()
        return [x.replace("com.apple.speech.synthesis.voice.", "").replace(".premium", "").title() for x in ls]
    
    def speak(self, path: Union[str, XABase.XAPath, None] = None):
        """Speaks the provided message using the desired voice, volume, and speaking rate. 

        :param path: The path to a .AIFF file to output sound to, defaults to None
        :type path: Union[str, XAPath, None], optional

        :Example 1: Speak a message aloud

        >>> import PyXA
        >>> PyXA.XASpeech("This is a test").speak()

        :Example 2: Output spoken message to an AIFF file

        >>> import PyXA
        >>> speaker = PyXA.XASpeech("Hello, world!")
        >>> speaker.speak("/Users/steven/Downloads/Hello.AIFF")

        :Example 3: Control the voice, volume, and speaking rate

        >>> import PyXA
        >>> speaker = PyXA.XASpeech(
        >>>     message = "Hello, world!",
        >>>     voice = "Alex",
        >>>     volume = 1,
        >>>     rate = 500
        >>> )
        >>> speaker.speak()

        .. versionadded:: 0.0.9
        """
        # Get the selected voice by name
        voice = None
        for v in AppKit.NSSpeechSynthesizer.availableVoices():
            if self.voice.lower() in v.lower():
                voice = v

        # Set up speech synthesis object
        synthesizer = AppKit.NSSpeechSynthesizer.alloc().initWithVoice_(voice)
        synthesizer.setVolume_(self.volume)
        synthesizer.setRate_(self.rate)

        # Start speaking
        if path is None:
            synthesizer.startSpeakingString_(self.message)
        else:
            if isinstance(path, str):
                path = XABase.XAPath(path)
            synthesizer.startSpeakingString_toURL_(self.message, path.xa_elem)

        # Wait for speech to complete
        while synthesizer.isSpeaking():
            time.sleep(0.01)