import math
import os
from pathlib import Path
from random import random
from time import sleep
from typing import Any, List, Union

from AppKit import (
    NSWorkspace,
    NSApplication,
    NSSound,
    NSPasteboard,
    NSArray,
    NSPasteboardTypeString,
    NSAppleScript,
    NSRunningApplication,
    NSMutableArray
)
from Foundation import NSURL, NSBundle

import threading

from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, kCGWindowListOptionIncludingWindow, kCGWindowListExcludeDesktopElements, kCGWindowListOptionOnScreenAboveWindow, kCGWindowListOptionOnScreenBelowWindow, kCGWindowListOptionAll

from .XABase import (
    XAApplication,
    XASound,
    timeout,
)

from .XAErrors import ApplicationNotFoundError

from .apps import application_classes

appspace = NSApplication.sharedApplication()
workspace = NSWorkspace.sharedWorkspace()
apps = []

def _get_path_to_app(app_identifier: str) -> str:
    app_path = app_identifier
    if not app_identifier.endswith(".app"):
            app_identifier += ".app"

    if not app_path.startswith("/"):
        app_path = "/System/Applications/" + app_identifier
        if not os.path.exists(app_path):
            app_path = "/System/Applications/Utilities/" + app_identifier
        if not os.path.exists(app_path):
            app_path = str(Path.home()) + "/" + app_identifier
        if not os.path.exists(app_path):
            app_path = "/Applications/" + app_identifier
        if not os.path.exists(app_path):
            app_path = "/System/Library/CoreServices/" + app_identifier
        if not os.path.exists(app_path):
            app_path = "/System/Library/CoreServices/Applications" + app_identifier

    if os.path.exists(app_path):
        return app_path

    raise ApplicationNotFoundError(app_identifier)

def get_running_applications() -> List[XAApplication]:
    """Gets PyXA references to all currently running applications whose app bundles are stored in typical application directories.

    :return: A list of PyXA application objects.
    :rtype: List[XAApplication]
    
    .. versionadded:: 0.0.1
    """

    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    layers = [window["kCGWindowLayer"] for window in windows]
    names = [window["kCGWindowOwnerName"] for window in windows]

    def append_app(name, apps):
        try:
            apps.append(application(name.lower()))
        except ApplicationNotFoundError as e:
            pass
            #print("Couldn't create a reference to " + e.name)
    
    threads = []
    for index, name in enumerate(names):
        if layers[index] == 0:
            app_thread = threading.Thread(target=append_app, args=(name.lower(), apps), name="Append App", daemon=False)
            threads.append(app_thread)
            app_thread.start()
    
    wait = True
    while wait != False:
        wait = False
        for thread in threads:
            if thread.is_alive():
                wait = True

    return apps

def current_application() -> XAApplication:
    """Retrieves a PyXA representation of the frontmost application.

    :return: A PyXA application object referencing the current application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """
    app = workspace.frontmostApplication()
    app_identifier = app.localizedName().lower()
    return application(app_identifier)

def launch_application(app_identifier: str) -> XAApplication:
    """Launches and activates an application, or activates an already running application, and returns its PyXA application object representation.

    :param app_identifier: The name of the application to launch or activate.
    :type app_identifier: str
    :return: A PyXA application object referencing the target application.
    :rtype: XAApplication

    .. seealso:: :func:`application`

    .. versionadded:: 0.0.1
    """
    app_identifier = app_identifier.lower()
    app = application(app_identifier)
    app.activate()
    return app

def application(app_identifier: str) -> XAApplication:
    """Retrieves a PyXA application object representation of the target application without launching or activating the application.

    :param app_identifier: The name of the application to get an object of.
    :type app_identifier: str
    :return: A PyXA application object referencing the target application.
    :rtype: XAApplication

    .. seealso:: :func:`launch_application`

    .. versionadded:: 0.0.1
    """

    app_object = None
    def _launch_completion_handler(app, _error):
        nonlocal app_object
        app_object = app

    bundle = None
    app_path = _get_path_to_app(app_identifier)
    bundle = NSBundle.alloc().initWithPath_(app_path)
    url = workspace.URLForApplicationWithBundleIdentifier_(bundle.bundleIdentifier())
    workspace.openApplicationAtURL_configuration_completionHandler_(url, None, _launch_completion_handler)
    while app_object is None:
        sleep(0.1)

    properties = {
        "parent": None,
        "appspace": appspace,
        "workspace": workspace,
        "element": app_object,
        "appref": app_object,
    }
    if app_identifier.lower() in application_classes:
        app = application_classes[app_identifier.lower()](properties)
    else:
        app = XAApplication(properties)
    apps.append(app)
    return app

def open_url(path: Union[str, NSURL]) -> None:
    """Opens the document at the given URL in its default application.

    :param path: The path of the item to open. This can be a file path, folder path, web address, or application URL.
    :type path: Union[str, NSURL]

    .. versionadded:: 0.0.2
    """
    url = path
    if isinstance(path, str):
        url = NSURL.alloc().initWithString_(path)
    if url.path().startswith("/"):
        url = NSURL.alloc().initFileURLWithPath_(url.path())
    workspace.openURL_(url)

def sound(sound_file: Union[str, NSURL]) -> XASound:
    """Creates a new XASound object.

    :param sound_file: The sound file to associate with the XASound object
    :type sound_file: Union[str, NSURL]
    :return: A reference to the new XASound object.
    :rtype: XASound

    .. seealso:: :func:`play_sound`

    .. versionadded:: 0.0.1
    """
    return XASound(sound_file)

def play_sound(sound_file: Union[str, NSURL]) -> None:
    """Immediately plays a sound from the specified file.

    :param sound_file: The path to the file to play.
    :type sound_file: Union[str, NSURL]

    .. seealso:: :func:`sound`

    .. versionadded:: 0.0.1
    """
    if isinstance(sound_file, str):
        if "/" in sound_file:
            sound_file = NSURL.alloc().initWithString_(sound_file)
        else:
            sound_file = NSURL.alloc().initWithString_("/System/Library/Sounds/" + sound_file + ".aiff")
    sound = NSSound.alloc()
    sound.initWithContentsOfURL_byReference_(sound_file, True)
    sound.play()
    sleep(sound.duration())

def get_clipboard() -> List[bytes]:
    """Returns the byte representation of all items on the clipboard.

    :return: A list of items currently on the clipboard in their byte representation.
    :rtype: List[bytes]

    .. seealso:: :func:`get_clipboard_strings`, :func:`set_clipboard`

    .. versionadded:: 0.0.1
    """
    items = []
    pb = NSPasteboard.generalPasteboard()
    for item in pb.pasteboardItems():
        for item_type in item.types():
            items.append(item.dataForType_(item_type))
    return items

def get_clipboard_strings() -> List[str]:
    """Returns the string representation all items on the clipboard that can be represented as strings.

    :return: A list of items currently on the clipboard in their string representation.
    :rtype: List[str]

    .. seealso:: :func:`get_clipboard`, :func:`set_clipboard`

    .. versionadded:: 0.0.1
    """
    items = []
    pb = NSPasteboard.generalPasteboard()
    for item in pb.pasteboardItems():
        if NSPasteboardTypeString in item.types():
            decoded_item = item.dataForType_(NSPasteboardTypeString).decode()
            if "\r" in decoded_item:
                items.extend(decoded_item.split("\r"))
            elif "\n" in decoded_item:
                items.extend(decoded_item.split("\n"))
            else:
                items.append(decoded_item)
    return items

def set_clipboard(content: Any) -> None:
    """Sets the clipboard to the specified content.

    :param content: The item or object to set the clipboard to. Can be a list of items.
    :type content: Any

    .. seealso:: :func:`get_clipboard`, :func:`get_clipboard_strings`

    .. versionadded:: 0.0.1
    """
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    pb.writeObjects_(NSArray.arrayWithObject_(content))

def run_applescript(source: Union[str, NSURL]) -> Any:
    """Runs AppleScript and returns its result.

    :param source: Either AppleScript code as text or the path to a .scpt file.
    :type source: Union[str, NSURL]
    :return: The value returned from the script upon completing execution.
    :rtype: Any

    .. versionadded:: 0.0.1
    """
    script = None
    if source.startswith("/"):
        source = NSURL.fileURLWithPath_(source)
        script = NSAppleScript.initWithContentsOfURL_error_(source, None)
    elif isinstance(source, NSURL):
        script = NSAppleScript.initWithContentsOfURL_error_(source, None)
    else:
        script = NSAppleScript.alloc().initWithSource_(source)
    return script.executeAndReturnError_(None)