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
    "preview": XAPreviewApplication,
    "calculator": XACalculatorApplication,
    "tv": XATVApplication,
    "contacts": XAContactsApplication,
    "shortcuts": XAShortcutsApplication,
    "dictionary": XADictionaryApplication,
}