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
    VERSION,

    # XAFinderExtension,

    # Methods
    current_application, running_applications,
)

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

old_module = sys.modules["PyXA"] 

class module(ModuleType):
    def __getattr__(self, attr):
        if attr in old_module.__dict__:
            return getattr(old_module, attr)

        if attr in module_map:
            module = importlib.import_module(module_map[attr], "PyXA")
            return getattr(module, attr)

sys.modules["PyXA"] = module("PyXA")