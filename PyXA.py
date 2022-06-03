import os
from typing import List, Union
import ScriptingBridge
from PyObjCTools import AppHelper
from AppKit import (
    NSWorkspace,
    NSObject,
    NSWorkspaceWillLaunchApplicationNotification,
    NSWorkspaceDidTerminateApplicationNotification,
    NSWorkspaceDidActivateApplicationNotification,
    NSWorkspaceDidWakeNotification,
    NSApplication,
    NSTimer,
    NSApp,
    NSSound,
)
from Foundation import NSURL, NSString, NSBundle

from enum import Enum
from time import sleep
from pprint import pprint
import threading


from XABase import (
    XAApplication,
    XASound,
    XAText,
)

from pathlib import Path

from XAErrors import ApplicationNotFoundError

from Experiment import AutomationWrapper

from apps.Finder import XAFinderApplication
from apps.Safari import XASafariApplication

from apps.Music import XAMusicApplication

from apps.Notes import XANotesApplication
from apps.Reminders import XARemindersApplication
from apps.Calendar import XACalendarApplication

from apps.TextEdit import XATextEditApplication
from apps.Terminal import XATerminalApplication

from apps.Messages import XAMessagesApplication

from apps.Pages import XAPagesApplication

from apps.SystemEvents import XASystemEventsApplication

application_classes = {
    "finder": XAFinderApplication,
    "safari": XASafariApplication,
    "music": XAMusicApplication,
    "reminders": XARemindersApplication,
    "notes": XANotesApplication,
    "messages": XAMessagesApplication,
    "calendar": XACalendarApplication,
    "textedit": XATextEditApplication,
    "pages": XAPagesApplication,
    "system events": XASystemEventsApplication,
    "systemevents": XASystemEventsApplication,
    "terminal": XATerminalApplication,
}

appspace = NSApplication.sharedApplication()
workspace = NSWorkspace.sharedWorkspace()

# _notification_center = workspace2.notificationCenter()

# class NotificationState(Enum):
#     """Levels of running states for processes.
#     """
#     APP_LAUNCHED = 0    # Process is awaiting start.
#     APP_TERMINATED = 1  # Process is in progress.
#     APP_ACTIVATED = 2   # Process is paused, but can be continued.
#     SCREEN_AWAKENED = 3 # Process is paused and cannot continue until conditions are met.

# class NotificationHandler(NSObject):
#     _notification_state = None

#     def handleApplicationLaunchNotification_(self, aNotification):
#         NotificationHandler._notification_state = NotificationState.APP_LAUNCHED
#         print(NotificationHandler._notification_state)

#     def handleApplicationTerminateNotification_(self, aNotification):
#         NotificationHandler._notification_state = NotificationState.APP_TERMINATED

#     def handleApplicationActivateNotification_(self, aNotification):
#         NotificationHandler._notification_state = NotificationState.APP_ACTIVATED

#     def handleWakeNotification_(self, aNotification):
#         NotificationHandler._notification_state = NotificationState.SCREEN_AWAKENED

# notificationHandler1 = NotificationHandler.new()
# _notification_center.addObserver_selector_name_object_(
#     notificationHandler1,
#     "handleApplicationLaunchNotification:",
#     NSWorkspaceWillLaunchApplicationNotification,
#     None,
# )

# notificationHandler2 = NotificationHandler.new()
# _notification_center.addObserver_selector_name_object_(
#     notificationHandler2,
#     "handleApplicationTerminateNotification:",
#     NSWorkspaceDidTerminateApplicationNotification,
#     None,
# )

# notificationHandler3 = NotificationHandler.new()
# _notification_center.addObserver_selector_name_object_(
#     notificationHandler3,
#     "handleApplicationActivateNotification:",
#     NSWorkspaceDidActivateApplicationNotification,
#     None,
# )

# notificationHandler4 = NotificationHandler.new()
# _notification_center.addObserver_selector_name_object_(
#     notificationHandler4,
#     "handleWakeNotification:",
#     NSWorkspaceDidWakeNotification,
#     None,
# )

# class QuitClass(NSObject):
#     def quitMainLoop_(self, aTimer):
#         # Just stop the main loop.
#         print("Quitting main loop.")
#         AppHelper.stopEventLoop()

# def get_notification_state() -> NotificationState:
#     delegate = NSApplication().alloc().init()
#     NSApp().setDelegate_(delegate)
#     quitInst = QuitClass.alloc().init()
#     NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(10.0, quitInst, 'quitMainLoop:', None, False)
#     AppHelper.runConsoleEventLoop(installInterrupt = True)
#     return NotificationHandler._notification_state

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
    apps = []
    for app in workspace.runningApplications():
        if not app.isHidden():
            apps.append(application(app.bundleIdentifier()))
    return apps

def current_application() -> XAApplication:
    """Retrieves a PyXA representation of the frontmost application.

    :return: _description_
    :rtype: XAApplication
    """
    app = workspace.frontmostApplication()
    app_identifier = app.localizedName().lower()

    if application_classes[app.localizedName()] in application_classes:
        SB = ScriptingBridge.SBApplication.alloc()
        app_SB = SB.initWithBundleIdentifier_(app.bundleIdentifier())

        if app_SB is None:
            return application_classes[app_identifier](app, appspace, workspace, app)
        else:
            return application_classes[app_identifier](app, appspace, workspace, app_SB)
    return XAApplication(app)

def launch_application(app_identifier: str) -> XAApplication:
    """Launches and activates an application, or activates an already running application, and returns its PyXA application object representation.

    :param app_identifier: The name of the application to launch or activate.
    :type app_identifier: str
    :return: _description_
    :rtype: XAApplication
    """
    app_identifier = app_identifier.lower()
    app = application(app_identifier)
    app.activate()
    return app

def application(app_identifier: str) -> XAApplication:
    """Retrieves a PyXA application object representation of the target application without launching or activating the application.

    :param app_identifier: The name of the application to get an object of.
    :type app_identifier: str
    :return: An XAApplication object with an `element` attribute holding a reference to the actual application object.
    :rtype: XAApplication
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
        sleep(0.2)

    properties = {
        "parent": None,
        "appspace": appspace,
        "workspace": workspace,
        "element": app_object,
        "appref": app_object,
    }
    if app_identifier.lower() in application_classes:
        return application_classes[app_identifier.lower()](properties)
    return XAApplication(properties)

def sound(sound_file: Union[str, NSURL]) -> XASound:
    return XASound(sound_file)

def play_sound(sound_file: Union[str, NSURL]):
    if isinstance(sound_file, str):
        if "/" in sound_file:
            sound_file = NSURL.alloc().initWithString_(sound_file)
        else:
            sound_file = NSURL.alloc().initWithString_("/System/Library/Sounds/" + sound_file + ".aiff")
    sound = NSSound.alloc()
    sound.initWithContentsOfURL_byReference_(sound_file, True)
    sound.play()
    sleep(sound.duration())