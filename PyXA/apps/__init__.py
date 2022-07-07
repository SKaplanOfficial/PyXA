from .Finder import XAFinderApplication
from .Safari import XASafariApplication
from .Music import XAMusicApplication
from .Notes import XANotesApplication
from .Reminders import XARemindersApplication, XAReminder
from .Calendar import XACalendarApplication
from .TextEdit import XATextEditApplication
from .Terminal import XATerminalApplication
from .Messages import XAMessagesApplication
from .Pages import XAPagesApplication
from .SystemEvents import XASystemEventsApplication
from .Preview import XAPreviewApplication
from .Calculator import XACalculatorApplication
from .TV import XATVApplication
from .Contacts import XAContactsApplication
from .Shortcuts import XAShortcutsApplication
from .Dictionary import XADictionaryApplication
from .PhotosApp import XAPhotosApplication
from .SystemPreferences import XASystemPreferencesApplication
from .Keynote import XAKeynoteApplication
from .Chromium import XAChromiumApplication
from .Mail import XAMailApplication
from .Automator import XAAutomatorApplication
from .Console import XAConsoleApplication

application_classes = {
    ### First Party Scriptable Apps
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
    "preview": XAPreviewApplication,
    "tv": XATVApplication,
    "contacts": XAContactsApplication,
    "shortcuts": XAShortcutsApplication,
    "shortcuts events": XAShortcutsApplication,
    "photos": XAPhotosApplication,
    "system preferences": XASystemPreferencesApplication,
    "keynote": XAKeynoteApplication,
    "mail": XAMailApplication,
    "automator": XAAutomatorApplication,
    "console": XAConsoleApplication,

    ### First Party Non-scriptable Apps
    "calculator": XACalculatorApplication,
    "dictionary": XADictionaryApplication,

    ### Third Party Scriptable Apps
    # Chromium
    "chromium": XAChromiumApplication,
    "brave browser": XAChromiumApplication,
    "microsoft edge": XAChromiumApplication,
    "google chrome": XAChromiumApplication,
    "opera": XAChromiumApplication,
    "vivaldi": XAChromiumApplication,
    "blisk": XAChromiumApplication,
    "iridium": XAChromiumApplication,
}