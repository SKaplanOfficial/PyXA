import importlib
import sys
from types import ModuleType

import PyXA.Additions
import PyXA.XABase

from .PyXA import (
    application,
)

from .XABase import (
    # Base Types
    XAText,
    XAURL,
    XAPath,
    XAColor,
    XASound,
    XAImage,
    XAVideo,
    XALocation,
    Application,

    # Utilities
    AppleScript,
    XAPredicate,
    
    # System Features
    XAClipboard,
    XASpotlight,

    # Alerts, Dialogs, Menus, and Notifications
    XAFilePicker, XAFolderPicker, XAApplicationPicker,
    XADialog, XAFileNameDialog,
    XAColorPicker, XAColorPickerStyle,
    XAMenu,

    # Constants
    VERSION, application_classes,

    # XAFinderExtension,

    # Methods
    current_application, running_applications,
)

old_module = sys.modules["PyXA"]

# Adds apps as methods on PyXA module, e.g. PyXA.Calendar() --> XACalendarApplication instance
for index, app_name in enumerate(application_classes):
    wrapper_name = app_name.title().replace(" ", "")
    setattr(old_module, wrapper_name, lambda local_app_name=app_name: Application(local_app_name))

# JIT imports
module_map = {
    "XACommandDetector": ".Additions.Speech",
    "XASpeech": ".Additions.Speech",
    "XASpeechRecognizer": ".Additions.Speech",

    "XALSM": ".Additions.Learn",

    "SDEFParser": ".Additions.Utils",

    "XAMenuBar": ".Additions.UI",
    "XAAlertStyle": ".Additions.UI",
    "XAAlert": ".Additions.UI",
    "XANotification": ".Additions.UI",
    "XAHUD": ".Additions.UI",

    "RSSFeed": ".Additions.Web",
}

class module(ModuleType):
    def __getattr__(self, attr):
        if attr in old_module.__dict__:
            return getattr(old_module, attr)

        if attr in module_map:
            module = importlib.import_module(module_map[attr], "PyXA")
            return getattr(module, attr)

sys.modules["PyXA"] = module("PyXA")