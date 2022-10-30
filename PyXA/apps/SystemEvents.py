""".. versionadded:: 0.1.0

Control the macOS System Events application using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from pprint import pprint
from time import sleep
from typing import Any, Union

import AppKit

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

from ..XAProtocols import XACanPrintPath, XACloseable, XAPrintable, XASelectable
        

class XASystemEventsApplication(XABase.XAEventsApplication, XABaseScriptable.XASBApplication, XACanPrintPath):
    """A class for managing and interacting with System Events.app.

    .. versionadded:: 0.1.0
    """
    class DynamicStyle(Enum):
        """Options for the dynamic style of the desktop background.
        """
        AUTO    = OSType('atmt') #: automatic (if supported, follows light/dark appearance)
        DYNAMIC = OSType('dynm') #: dynamic (if supported, updates desktop picture based on time and/or location)
        LIGHT   = OSType('lite') #: light style
        DARK    = OSType('dark') #: dark style
        UNKNOWN    = OSType('unk\?') #: unknown style

    class DoubleClickBehavior(Enum):
        """Options for double click behaviors.
        """
        MINIMIZE    = OSType('ddmi') #: Minimize
        OFF         = OSType('ddof') #: Off
        ZOOM        = OSType('ddzo') #: Zoom

    class MinimizeEffect(Enum):
        """Options for the effect to use when minimizing applications.
        """
        GENIE   = OSType('geni') #: Genie effect
        SCALE   = OSType('scal') #: Scale effect

    class ScreenLocation(Enum):
        """Locations on the screen.
        """
        BOTTOM = OSType('bott') #: Bottom of screen
        LEFT   = OSType('left') #: Left side of screen
        RIGHT  = OSType('righ') #: Right side of screen

    class ScrollPageBehavior(Enum):
        """Scroll page behaviors.
        """
        JUMP_TO_HERE        = OSType('tohr') #: Jump to here
        JUMP_TO_NEXT_PAGE   = OSType('nxpg') #: Jump to next page

    class FontSmoothingStyle(Enum):
        """Font smoothing styles.
        """
        AUTOMATIC   = OSType('autm')
        LIGHT       = OSType('lite')
        MEDIUM      = OSType('medi')
        STANDARD    = OSType('stnd')
        STRONG      = OSType('strg')

    class Appearance(Enum):
        """Appearance colors.
        """
        BLUE        = OSType('blue')
        GRAPHITE    = OSType('grft')

    class HighlightColor(Enum):
        """Highlight colors.
        """
        BLUE        = OSType('blue')
        GOLD        = OSType('gold')
        GRAPHITE    = OSType('grft')
        GREEN       = OSType('gren')
        ORANGE      = OSType('orng')
        PURPLE      = OSType('prpl')
        RED         = OSType('red ')
        SILVER      = OSType('slvr')

    class MediaInsertionAction(Enum):
        """Actions to perform when media is inserted.
        """
        ASK_WHAT_TO_DO      = OSType('dhas')
        IGNORE              = OSType('dhig')
        OPEN_APPLICATION    = OSType('dhap')
        RUN_A_SCRIPT        = OSType('dhrs')

    class Key(Enum):
        """Keys and key actions.
        """
        COMMAND         = OSType('eCmd')
        CONTROL         = OSType('eCnd')
        OPTION          = OSType('eOpt')
        SHIFT           = OSType('eSft')
        COMMAND_DOWN    = OSType('Kcmd')
        CONTROL_DOWN    = OSType('Kctl')
        OPTION_DOWN     = OSType('Kopt')
        SHIFT_DOWN      = OSType('Ksft')

    class AccessRight(Enum):
        """Access right levels.
        """
        NONE        = OSType('none')
        READ        = OSType('read') #: Read only
        READ_WRITE  = OSType('rdwr') #: Read and write
        WRITE       = OSType('writ') #: Write only

    class PictureRotation(Enum):
        """Desktop image picture rotation settings.
        """
        NEVER = 0
        USING_INTERVAL = 1
        USING_LOGIN = 2
        AFTER_SLEEP = 3

    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the application.
        self.frontmost: bool #: Is this the active application?
        self.version: str #: The version number of the application.
        self.quit_delay: int #: the time in seconds the application will idle before quitting; if set to zero, idle time will not cause the application to quit
        self.script_menu_enabled: bool #: Is the Script menu installed in the menu bar?
        self.current_user: XASystemEventsUser #: the currently logged in user
        self.appearance_preferences: XASystemEventsAppearancePreferencesObject #: a collection of appearance preferences
        self.cd_and_dvd_preferences: XASystemEventsCDAndDVDPreferencesObject #: the preferences for the current user when a CD or DVD is inserted
        self.current_desktop: XASystemEventsDesktop #: the primary desktop
        self.dock_preferences: XASystemEventsDockPreferencesObject #: the preferences for the current user's dock
        self.network_preferences: XASystemEventsNetworkPreferencesObject #: the preferences for the current user's network
        self.current_screen_saver: XASystemEventsScreenSaver #: the currently selected screen saver
        self.screen_saver_preferences: XASystemEventsScreenSaverPreferencesObject #: the preferences common to all screen savers
        self.security_preferences: XASystemEventsSecurityPreferencesObject #: a collection of security preferences
        self.application_support_folder: XABase.XAFolder #: The Application Support folder
        self.applications_folder: XABase.XAFolder #: The user's Applications folder
        self.classic_domain: XABase.XAClassicDomainObject #: the collection of folders belonging to the Classic System
        self.desktop_folder: XABase.XAFolder #: The user's Desktop folder
        self.desktop_pictures_folder: XABase.XAFolder #: The Desktop Pictures folder
        self.documents_folder: XABase.XAFolder #: The user's Documents folder
        self.downloads_folder: XABase.XAFolder #: The user's Downloads folder
        self.favorites_folder: XABase.XAFolder #: The user's Favorites folder
        self.folder_action_scripts_folder: XABase.XAFolder #: The user's Folder Action Scripts folder
        self.fonts_folder: XABase.XAFolder #: The Fonts folder
        self.home_folder: XABase.XAFolder #: The Home folder of the currently logged in user
        self.library_folder: XABase.XAFolder #: The Library folder
        self.local_domain: XABase.XALocalDomainObject #: the collection of folders residing on the Local machine
        self.movies_folder: XABase.XAFolder #: The user's Movies folder
        self.music_folder: XABase.XAFolder #: The user's Music folder
        self.network_domain: XABase.XANetworkDomainObject #: the collection of folders residing on the Network
        self.pictures_folder: XABase.XAFolder #: The user's Pictures folder
        self.preferences_folder: XABase.XAFolder #: The user's Preferences folder
        self.public_folder: XABase.XAFolder #: The user's Public folder
        self.scripting_additions_folder: XABase.XAFolder #: The Scripting Additions folder
        self.scripts_folder: XABase.XAFolder #: The user's Scripts folder
        self.shared_documents_folder: XABase.XAFolder #: The Shared Documents folder
        self.sites_folder: XABase.XAFolder #: The user's Sites folder
        self.speakable_items_folder: XABase.XAFolder #: The Speakable Items folder
        self.startup_disk: XABase.XADisk #: the disk from which Mac OS X was loaded
        self.system_domain: XABase.XASystemDomainObject #: the collection of folders belonging to the System
        self.temporary_items_folder: XABase.XAFolder #: The Temporary Items folder
        self.trash: XABase.XAFolder #: The user's Trash folder
        self.user_domain: XABase.XAUserDomainObject #: the collection of folders belonging to the User
        self.utilities_folder: XABase.XAFolder #: The Utilities folder
        self.workflows_folder: XABase.XAFolder #: The Automator Workflows folder
        self.folder_actions_enabled: bool #: Are Folder Actions currently being processed?
        self.ui_elements_enabled: bool #: Are UI element events currently being processed?
        self.scripting_definition: XASystemEventsScriptingDefinitionObject #: The scripting definition of the System Events application

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def quit_delay(self) -> int:
        return self.xa_scel.quitDelay()

    @quit_delay.setter
    def quit_delay(self, quit_delay: int):
        self.set_property('quitDelay', quit_delay)

    @property
    def script_menu_enabled(self) -> bool:
        return self.xa_scel.scriptMenuEnabled()

    @property
    def current_user(self) -> 'XASystemEventsUser':
        return self._new_element(self.xa_scel.currentUser(), XASystemEventsUser)

    @property
    def appearance_preferences(self) -> 'XASystemEventsAppearancePreferencesObject':
        return self._new_element(self.xa_scel.appearancePreferences(), XASystemEventsAppearancePreferencesObject)

    @appearance_preferences.setter
    def appearance_preferences(self, appearance_preferences: 'XASystemEventsAppearancePreferencesObject'):
        self.set_property('appearancePreferences', appearance_preferences.xa_elem)

    @property
    def cd_and_dvd_preferences(self) -> 'XASystemEventsCDAndDVDPreferencesObject':
        return self._new_element(self.xa_scel.CDAndDVDPreferences(), XASystemEventsCDAndDVDPreferencesObject)

    @cd_and_dvd_preferences.setter
    def cd_and_dvd_preferences(self, cd_and_dvd_preferences: 'XASystemEventsCDAndDVDPreferencesObject'):
        self.set_property('cd_and_dvd_preferences', cd_and_dvd_preferences.xa_elem)

    @property
    def current_desktop(self) -> 'XASystemEventsDesktop':
        return self._new_element(self.xa_scel.currentDesktop(), XASystemEventsDesktop)

    @property
    def dock_preferences(self) -> 'XASystemEventsDockPreferencesObject':
        return self._new_element(self.xa_scel.dockPreferences(), XASystemEventsDockPreferencesObject)

    @dock_preferences.setter
    def dock_preferences(self, dock_preferences: 'XASystemEventsDockPreferencesObject'):
        self.set_property('dock_preferences', dock_preferences.xa_elem)

    @property
    def network_preferences(self) -> 'XASystemEventsNetworkPreferencesObject':
        return self._new_element(self.xa_scel.networkPreferences(), XASystemEventsNetworkPreferencesObject)

    @network_preferences.setter
    def network_preferences(self, network_preferences: 'XASystemEventsNetworkPreferencesObject'):
        self.set_property('network_preferences', network_preferences.xa_elem)

    @property
    def current_screen_saver(self) -> 'XASystemEventsScreenSaver':
        return self._new_element(self.xa_scel.currentScreenSaver(), XASystemEventsScreenSaver)

    @current_screen_saver.setter
    def current_screen_saver(self, current_screen_saver: 'XASystemEventsScreenSaver'):
        self.set_property('currentScreenSaver', current_screen_saver.xa_elem)

    @property
    def screen_saver_preferences(self) -> 'XASystemEventsScreenSaverPreferencesObject':
        return self._new_element(self.xa_scel.screenSaverPreferences(), XASystemEventsScreenSaverPreferencesObject)

    @screen_saver_preferences.setter
    def screen_saver_preferences(self, screen_saver_preferences: 'XASystemEventsScreenSaverPreferencesObject'):
        self.set_property('screenSaverPreferences', screen_saver_preferences.xa_elem)

    @property
    def security_preferences(self) -> 'XASystemEventsSecurityPreferencesObject':
        return self._new_element(self.xa_scel.securityPreferences(), XASystemEventsSecurityPreferencesObject)

    @security_preferences.setter
    def security_preferences(self, security_preferences: 'XASystemEventsSecurityPreferencesObject'):
        self.set_property('securityPreferences', security_preferences.xa_elem)

    @property
    def application_support_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.applicationSupportFolder(), XABase.XAFolder)

    @property
    def applications_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.applicationsFolder(), XABase.XAFolder)

    @property
    def classic_domain(self) -> 'XABase.XAClassicDomainObject':
        return self._new_element(self.xa_scel.ClassicDomain(), XABase.XAClassicDomainObject)

    @property
    def desktop_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.desktopFolder(), XABase.XAFolder)

    @property
    def desktop_pictures_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.desktopPicturesFolder(), XABase.XAFolder)

    @property
    def documents_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.documentsFolder(), XABase.XAFolder)

    @property
    def downloads_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.downloadsFolder(), XABase.XAFolder)

    @property
    def favorites_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.favoritesFolder(), XABase.XAFolder)

    @property
    def folder_action_scripts_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.FolderActionScriptsFolder(), XABase.XAFolder)

    @property
    def fonts_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.fontsFolder(), XABase.XAFolder)

    @property
    def home_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.homeFolder(), XABase.XAFolder)

    @property
    def library_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.libraryFolder(), XABase.XAFolder)

    @property
    def local_domain(self) -> 'XABase.XALocalDomainObject':
        return self._new_element(self.xa_scel.localDomain(), XABase.XALocalDomainObject)

    @property
    def movies_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.moviesFolder(), XABase.XALocalDomainObject)

    @property
    def music_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.musicFolder(), XABase.XAFolder)

    @property
    def network_domain(self) -> 'XABase.XANetworkDomainObject':
        return self._new_element(self.xa_scel.networkDomain(), XABase.XANetworkDomainObject)

    @property
    def pictures_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.picturesFolder(), XABase.XAFolder)

    @property
    def preferences_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.preferencesFolder(), XABase.XAFolder)

    @property
    def public_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.publicFolder(), XABase.XAFolder)

    @property
    def scripting_additions_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.scriptingAdditionsFolder(), XABase.XAFolder)

    @property
    def scripts_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.scriptsFolder(), XABase.XAFolder)

    @property
    def shared_documents_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.sharedDocumentsFolder(), XABase.XAFolder)

    @property
    def sites_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.sitesFolder(), XABase.XAFolder)

    @property
    def speakable_items_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.speakableItemsFolder(), XABase.XAFolder)

    @property
    def startup_disk(self) -> 'XABase.XADisk':
        return self._new_element(self.xa_scel.startupDisk(), XABase.XADisk)

    @property
    def system_domain(self) -> 'XABase.XASystemDomainObject':
        return self._new_element(self.xa_scel.systemDomain(), XABase.XASystemDomainObject)

    @property
    def temporary_items_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.temporaryItemsFolder(), XABase.XAFolder)

    @property
    def trash(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.trash(), XABase.XAFolder)

    @property
    def user_domain(self) -> 'XABase.XAUserDomainObject':
        return self._new_element(self.xa_scel.userDomain(), XABase.XAUserDomainObject)

    @property
    def utilities_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.utilitiesFolder(), XABase.XAFolder)

    @property
    def workflows_folder(self) -> 'XABase.XAFolder':
        return self._new_element(self.xa_scel.workflowsFolder(), XABase.XAFolder)

    @property
    def folder_actions_enabled(self) -> bool:
        return self.xa_scel.folderActionsEnabled()

    @folder_actions_enabled.setter
    def folder_actions_enabled(self, folder_actions_enabled: bool):
        self.set_property('folderActionsEnabled', folder_actions_enabled)

    @property
    def ui_elements_enabled(self) -> bool:
        return self.xa_scel.UIElementsEnabled()

    @property
    def scripting_definition(self) -> 'XASystemEventsScriptingDefinitionObject':
        return self._new_element(self.xa_scel.scriptingDefinition(), XASystemEventsScriptingDefinitionObject)

    def log_out(self):
        """Logs out the current user.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.logOut()

    def restart(self, state_saving_preference: bool = False):
        """Restarts the computer.

        :param state_saving_preference: Whether the user defined state saving preference is followed, defaults to False (always saved)
        :type state_saving_preference: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_scel.restartStateSavingPreference_(state_saving_preference)

    def shut_down(self, state_saving_preference: bool = False):
        """Shuts down the computer.

        :param state_saving_preference: Whether the user defined state saving preference is followed, defaults to False (always saved)
        :type state_saving_preference: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_scel.shutDownStateSavingPreference_(state_saving_preference)

    def sleep(self):
        """Puts the computer to sleep.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.sleep()

    def begin_transaction(self) -> int:
        """Discards the results of a bounded update session with one or more files.

        :return: _description_
        :rtype: int
        """
        return self.xa_scel.beginTransaction()

    def end_transaction(self):
        """Ends the current transaction gracefully.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.endTransaction()

    def abort_transaction(self):
        """Aborts the current transaction.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.abortTransaction()

    def click(self):
        """Clicks on the application.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.click()

    def key_code(self, key_code: Union[int, list[int]], modifier: Union['XASystemEventsApplication.Key', list['XASystemEventsApplication.Key'], None] = None):
        if isinstance(modifier, list):
            modifier = [x.value for x in modifier]
            self.xa_scel.keyCode_using_(key_code, modifier)
        else:
            self.xa_scel.keyCode_using_(key_code, modifier.value if modifier is not None else None)

    def key_stroke(self, key: Union[int, list[int]], modifier: Union['XASystemEventsApplication.Key', list['XASystemEventsApplication.Key'], None] = None):
        def four_char_code(s):
            (ord(s[0]) << 24) + (ord(s[1]) << 16) + (ord(s[2]) << 8) + ord(s[3])

        if isinstance(modifier, list):
            modifier = [x.value for x in modifier]
            self.xa_scel.keystroke_using_(key, modifier)
        else:
            self.xa_scel.keystroke_using_(key, modifier.value if modifier is not None else None)

    def documents(self, filter: dict = None) -> Union['XASystemEventsDocumentList', None]:
        """Returns a list of documents, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XASystemEventsDocumentList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.documents(), XASystemEventsDocumentList, filter)

    def users(self, filter: dict = None) -> Union['XASystemEventsUserList', None]:
        """Returns a list of users, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned users will have, or None
        :type filter: Union[dict, None]
        :return: The list of users
        :rtype: XASystemEventsUserList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.users(), XASystemEventsUserList, filter)

    def desktops(self, filter: dict = None) -> Union['XASystemEventsDesktopList', None]:
        """Returns a list of desktops, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned desktops will have, or None
        :type filter: Union[dict, None]
        :return: The list of desktops
        :rtype: XASystemEventsDesktopList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.desktops(), XASystemEventsDesktopList, filter)

    def login_items(self, filter: dict = None) -> Union['XASystemEventsLoginItemList', None]:
        """Returns a list of login items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned login items will have, or None
        :type filter: Union[dict, None]
        :return: The list of login items
        :rtype: XASystemEventsLoginItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.loginItems(), XASystemEventsLoginItemList, filter)

    def screen_savers(self, filter: dict = None) -> Union['XASystemEventsScreenSaverList', None]:
        """Returns a list of screen savers, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned screen savers will have, or None
        :type filter: Union[dict, None]
        :return: The list of screen savers
        :rtype: XASystemEventsScreenSaverList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.screenSavers(), XASystemEventsScreenSaverList, filter)

    def aliases(self, filter: dict = None) -> Union['XABase.XAAliasList', None]:
        """Returns a list of aliases, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned aliases will have, or None
        :type filter: Union[dict, None]
        :return: The list of aliases
        :rtype: XABase.XAAliasList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.aliases(), XABase.XAAliasList, filter)

    def disks(self, filter: dict = None) -> Union['XABase.XADiskList', None]:
        """Returns a list of disks, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned disks will have, or None
        :type filter: Union[dict, None]
        :return: The list of disks
        :rtype: XABase.XADiskList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.disks(), XABase.XADiskList, filter)

    def disk_items(self, filter: dict = None) -> Union['XABase.XADiskItemList', None]:
        """Returns a list of disk items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned disk items will have, or None
        :type filter: Union[dict, None]
        :return: The list of disk items
        :rtype: XABase.XADiskItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.diskItems(), XABase.XADiskItemList, filter)

    def domains(self, filter: dict = None) -> Union['XABase.XADomainList', None]:
        """Returns a list of domains, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned domains will have, or None
        :type filter: Union[dict, None]
        :return: The list of domains
        :rtype: XABase.XADomainList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.domains(), XABase.XADomainList, filter)

    def files(self, filter: dict = None) -> Union['XABase.XAFileList', None]:
        """Returns a list of files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned files will have, or None
        :type filter: Union[dict, None]
        :return: The list of files
        :rtype: XABase.XAFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.files(), XABase.XAFileList, filter)

    def file_packages(self, filter: dict = None) -> Union['XABase.XAFilePackageList', None]:
        """Returns a list of file packages, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file packages will have, or None
        :type filter: Union[dict, None]
        :return: The list of file packages
        :rtype: XABase.XAFilePackageList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.filePackages(), XABase.XAFilePackageList, filter)

    def folders(self, filter: dict = None) -> Union['XABase.XAFolderList', None]:
        """Returns a list of folders, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XABase.XAFolderList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folders(), XABase.XAFolderList, filter)

    def folder_actions(self, filter: dict = None) -> Union['XABase.XAFolderActionList', None]:
        """Returns a list of folder actions, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folder actions will have, or None
        :type filter: Union[dict, None]
        :return: The list of folder actions
        :rtype: XABase.XAFolderActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folderActions(), XABase.XAFolderActionList, filter)

    def application_processes(self, filter: dict = None) -> Union['XASystemEventsApplicationProcessList', None]:
        """Returns a list of application processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsApplicationProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.applicationProcesses(), XASystemEventsApplicationProcessList, filter)

    def desk_accessory_processes(self, filter: dict = None) -> Union['XASystemEventsDeskAccessoryProcessList', None]:
        """Returns a list of desk accessory processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsDeskAccessoryProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.deskAccessoryProcesses(), XASystemEventsDeskAccessoryProcessList, filter)

    def processes(self, filter: dict = None) -> Union['XASystemEventsProcessList', None]:
        """Returns a list of processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.processes(), XASystemEventsProcessList, filter)

    def ui_elements(self, filter: dict = None) -> Union['XASystemEventsUIElementList', None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned UI elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.uiElements(), XASystemEventsUIElementList, filter)

    def property_list_files(self, filter: dict = None) -> Union['XASystemEventsPropertyListFileList', None]:
        """Returns a list of property list files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list files will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list files
        :rtype: XASystemEventsPropertyListFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.propertyListFiles(), XASystemEventsPropertyListFileList, filter)

    def property_list_items(self, filter: dict = None) -> Union['XASystemEventsPropertyListItemList', None]:
        """Returns a list of property list items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list items will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list items
        :rtype: XASystemEventsPropertyListItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.propertyListItems(), XASystemEventsPropertyListItemList, filter)

    def xml_datas(self, filter: dict = None) -> Union['XASystemEventsXMLDataList', None]:
        """Returns a list of XML datas, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML datas will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML datas
        :rtype: XASystemEventsXMLDataList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.xmlDatas(), XASystemEventsXMLDataList, filter)

    def xml_files(self, filter: dict = None) -> Union['XASystemEventsXMLFileList', None]:
        """Returns a list of XML files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML files will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML files
        :rtype: XASystemEventsXMLFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.xmlFiles(), XASystemEventsXMLFileList, filter)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.1.0
        """
        specifier_map = {
            "login item": "login item"
        }
        specifier = specifier_map.get(specifier) or specifier

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "login item":
            return self._new_element(obj, XASystemEventsLoginItem)
        elif specifier == "file":
            return self._new_element(obj, XABase.XAFile)
        elif specifier == "folder":
            return self._new_element(obj, XABase.XAFolder)




class XASystemEventsDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> 'XABase.XAFileList':
        """Gets the file of each document in the list.

        :return: A list of document files
        :rtype: XABase.XAFileList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return self._new_element(ls, XABase.XAFileList)

    def by_name(self, name: str) -> Union['XASystemEventsDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XASystemEventsDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("modified", modified)

    def by_file(self, file: 'XABase.XAFile') -> Union['XASystemEventsDocument', None]:
        """Retrieves the document whose file matches the given file, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XASystemEventsDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsDocument(XABase.XAObject, XACloseable, XAPrintable):
    """A document of System Events.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: Its name.
        self.modified: bool #: Has it been modified since the last save?
        self.file: XABase.XAFile #: Its location on disk, if it has one.

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> 'XABase.XAFile':
        return self._new_element(self.xa_elem.file(), XABase.XAFile)

    def save(self, path: Union[str, XABase.XAPath, None] = None):
        """Saves the document at the specified file path.

        :param path: The path to save the document at, defaults to None
        :type path: Union[str, XABase.XAPath, None], optional

        .. versionadded:: 0.1.0
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        if path is not None:
            self.xa_elem.saveIn_as_(path.xa_elem, XASystemEventsApplication, XABase.OSType("ctxt"))
    



class XASystemEventsWindow(XABaseScriptable.XASBWindow, XASelectable):
    """A window belonging to a process.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XASystemEventsDocument #: The document whose contents are displayed in the window
        self.accessibility_description: Union[str, None] #: a more complete description of the window and its capabilities
        self.object_description: Union[str, None] #: the accessibility description, if available; otherwise, the role description
        self.enabled: Union[bool, None] #: Is the window enabled? ( Does it accept clicks? )
        self.entire_contents: list[XABase.XAObject] #: A list of every UI element contained in this window and its child UI elements, to the limits of the tree
        self.focused: Union[bool, None] #: Is the focus on this window?
        self.help: Union[str, None] #: an elaborate description of the window and its capabilities
        self.maximum_value: Union[int, float, None] #: the maximum value that the UI element can take on
        self.minimum_value: Union[int, float, None] #: the minimum value that the UI element can take on
        self.name: str #: the name of the window, which identifies it within its container
        self.orientation: Union[str, None] #: the orientation of the window
        self.position: Union[list[Union[int, float]], None] #: the position of the window
        self.role: str #: an encoded description of the window and its capabilities
        self.role_description: str #: a more complete description of the window's role
        self.selected: Union[bool, None] #: Is the window selected?
        self.size: Union[list[Union[int, float]], None] #: the size of the window
        self.subrole: Union[str, None] #: an encoded description of the window and its capabilities
        self.title: str #: the title of the window as it appears on the screen
        self.value: Any #: the current value of the window

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

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
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

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
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

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
    def document(self) -> XASystemEventsDocument:
        return self._new_element(self.xa_elem.document(), XASystemEventsDocument)

    @property
    def accessibility_description(self) -> Union[str, None]:
        return self.xa_elem.accessibilityDescription()

    @property
    def object_description(self) -> Union[str, None]:
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> Union[bool, None]:
        return self.xa_elem.enabled()

    @property
    def entire_contents(self) -> list[XABase.XAObject]:
        return self.xa_elem.entireContents()

    @property
    def focused(self) -> Union[bool, None]:
        return self.xa_elem.focused()

    @focused.setter
    def focused(self, focused: bool):
        self.set_property('focused', focused)

    @property
    def help(self) -> Union[str, None]:
        return self.xa_elem.help()

    @property
    def maximum_value(self) -> Union[int, float, None]:
        return self.xa_elem.maximumValue()

    @property
    def minimum_value(self) -> Union[int, float, None]:
        return self.xa_elem.minimumValue()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def orientation(self) -> Union[str, None]:
        return self.xa_elem.orientation()

    @property
    def position(self) -> Union[list[Union[int, float]], None]:
        return self.xa_elem.position()

    @position.setter
    def position(self, position: list[Union[int, float]]):
        self.set_property('position', position)

    @property
    def role(self) -> str:
        return self.xa_elem.role()

    @property
    def role_description(self) -> str:
        return self.xa_elem.roleDescription()

    @property
    def selected(self) -> Union[bool, None]:
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property('selected', selected)

    @property
    def size(self) -> Union[list[Union[int, float]], None]:
        return self.xa_elem.size()

    @size.setter
    def size(self, size: list[Union[int, float]]):
        self.set_property('size', size)

    @property
    def subrole(self) -> Union[str, None]:
        return self.xa_elem.subrole()

    @property
    def title(self) -> Union[str, None]:
        return self.xa_elem.title()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    def actions(self, filter: dict = None) -> Union['XASystemEventsActionList', None]:
        """Returns a list of action elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of actions
        :rtype: XASystemEventsActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.actions(), XASystemEventsActionList)

    def attributes(self, filter: dict = None) -> Union['XASystemEventsAttributeList', None]:
        """Returns a list of attribute elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of attributes
        :rtype: XASystemEventsAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.attributes(), XASystemEventsAttributeList)

    def browsers(self, filter: dict = None) -> Union['XASystemEventsBrowserList', None]:
        """Returns a list of browser elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XASystemEventsBrowserList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.browsers(), XASystemEventsBrowserList)

    def busy_indicators(self, filter: dict = None) -> Union['XASystemEventsBusyIndicatorList', None]:
        """Returns a list of busy indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of busy indicators
        :rtype: XASystemEventsBusyIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.busyIndicators(), XASystemEventsBusyIndicatorList)

    def buttons(self, filter: dict = None) -> Union['XASystemEventsButtonList', None]:
        """Returns a list of button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of buttons
        :rtype: XASystemEventsButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.buttons(), XASystemEventsCheckboxList)

    def checkboxes(self, filter: dict = None) -> Union['XASystemEventsButtonList', None]:
        """Returns a list of checkbox elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of checkboxes
        :rtype: XASystemEventsCheckboxList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.checkboxes(), XASystemEventsCheckboxList)

    def color_wells(self, filter: dict = None) -> Union['XASystemEventsColorWellList', None]:
        """Returns a list of color well elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of color wells
        :rtype: XASystemEventsColorWellList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.colorWells(), XASystemEventsColorWellList)

    def combo_boxes(self, filter: dict = None) -> Union['XASystemEventsComboBoxList', None]:
        """Returns a list of combo box elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of combo boxes
        :rtype: XASystemEventsComboBoxList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.comboBoxes(), XASystemEventsComboBoxList)

    def drawers(self, filter: dict = None) -> Union['XASystemEventsDrawerList', None]:
        """Returns a list of drawer elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of drawers
        :rtype: XASystemEventsDrawerList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.drawers(), XASystemEventsDrawerList)

    def groups(self, filter: dict = None) -> Union['XASystemEventsGroupList', None]:
        """Returns a list of group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XASystemEventsGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.groups(), XASystemEventsGroupList)

    def grow_areas(self, filter: dict = None) -> Union['XASystemEventsGrowAreaList', None]:
        """Returns a list of grow area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of grow areas
        :rtype: XASystemEventsGrowAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.growAreas(), XASystemEventsGrowAreaList)

    def images(self, filter: dict = None) -> Union['XASystemEventsImageList', None]:
        """Returns a list of image elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XASystemEventsImageList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.images(), XASystemEventsImageList)

    def incrementors(self, filter: dict = None) -> Union['XASystemEventsIncrementorList', None]:
        """Returns a list of incrementor elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of incrementors
        :rtype: XASystemEventsIncrementorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.incrementors(), XASystemEventsIncrementorList)

    def lists(self, filter: dict = None) -> Union['XASystemEventsListList', None]:
        """Returns a list of list elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of lists
        :rtype: XASystemEventsListList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.lists(), XASystemEventsListList)

    def menu_buttons(self, filter: dict = None) -> Union['XASystemEventsMenuButtonList', None]:
        """Returns a list of menu button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu buttons
        :rtype: XASystemEventsMenuButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuButtons(), XASystemEventsMenuButtonList)

    def outlines(self, filter: dict = None) -> Union['XASystemEventsOutlineList', None]:
        """Returns a list of outline elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsOutlineList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.outlines(), XASystemEventsOutlineList)

    def pop_overs(self, filter: dict = None) -> Union['XASystemEventsPopOverList', None]:
        """Returns a list of pop-over elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-overs
        :rtype: XASystemEventsPopOverList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popOvers(), XASystemEventsPopOverList)

    def pop_up_buttons(self, filter: dict = None) -> Union['XASystemEventsPopUpButtonList', None]:
        """Returns a list of pop-up button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-up buttons
        :rtype: XASystemEventsPopUpButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popUpButtons(), XASystemEventsPopUpButtonList)

    def progress_indicators(self, filter: dict = None) -> Union['XASystemEventsProgressIndicatorList', None]:
        """Returns a list of progress indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of progress indicators
        :rtype: XASystemEventsProgressIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.progressIndicators(), XASystemEventsProgressIndicatorList)

    def radio_buttons(self, filter: dict = None) -> Union['XASystemEventsRadioButtonList', None]:
        """Returns a list of radio button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio buttons
        :rtype: XASystemEventsRadioButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.radioButtons(), XASystemEventsRadioButtonList)

    def radio_groups(self, filter: dict = None) -> Union['XASystemEventsRadioGroupList', None]:
        """Returns a list of radio group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio groups
        :rtype: XASystemEventsRadioGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.radioGroups(), XASystemEventsRadioGroupList)

    def relevance_indicators(self, filter: dict = None) -> Union['XASystemEventsRelevanceIndicatorList', None]:
        """Returns a list of relevance indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of relevance indicators
        :rtype: XASystemEventsRelevanceIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.relevanceIndicators(), XASystemEventsRelevanceIndicatorList)

    def scroll_areas(self, filter: dict = None) -> Union['XASystemEventsScrollAreaList', None]:
        """Returns a list of scroll area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll areas
        :rtype: XASystemEventsScrollAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollAreas(), XASystemEventsScrollAreaList)

    def scroll_bars(self, filter: dict = None) -> Union['XASystemEventsScrollBarList', None]:
        """Returns a list of scroll bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll bars
        :rtype: XASystemEventsScrollBarList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollBars(), XASystemEventsScrollBarList)

    def sheets(self, filter: dict = None) -> Union['XASystemEventsSheetList', None]:
        """Returns a list of sheet elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XASystemEventsSheetList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sheets(), XASystemEventsSheetList)

    def sliders(self, filter: dict = None) -> Union['XASystemEventsSliderList', None]:
        """Returns a list of slider elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sliders
        :rtype: XASystemEventsSliderList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sliders(), XASystemEventsSliderList)

    def splitters(self, filter: dict = None) -> Union['XASystemEventsSplitterList', None]:
        """Returns a list of splitter elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitters
        :rtype: XASystemEventsSplitterList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitters(), XASystemEventsSplitterList)

    def splitter_groups(self, filter: dict = None) -> Union['XASystemEventsSplitterGroupList', None]:
        """Returns a list of splitter group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitter groups
        :rtype: XASystemEventsSplitterGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitterGroups(), XASystemEventsSplitterGroupList)

    def static_texts(self, filter: dict = None) -> Union['XASystemEventsStaticTextList', None]:
        """Returns a list of static text elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of static texts
        :rtype: XASystemEventsStaticTextList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.staticTexts(), XASystemEventsStaticTextList)

    def tab_groups(self, filter: dict = None) -> Union['XASystemEventsTabGroupList', None]:
        """Returns a list of tab group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tab groups
        :rtype: XASystemEventsTabGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tabGroups(), XASystemEventsTabGroupList)

    def tables(self, filter: dict = None) -> Union['XASystemEventsTableList', None]:
        """Returns a list of table elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XASystemEventsTableList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tables(), XASystemEventsTableList)

    def text_areas(self, filter: dict = None) -> Union['XASystemEventsTextAreaList', None]:
        """Returns a list of text area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text areas
        :rtype: XASystemEventsTextAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textAreas(), XASystemEventsTextAreaList)

    def text_fields(self, filter: dict = None) -> Union['XASystemEventsTextFieldList', None]:
        """Returns a list of text fields elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text fields
        :rtype: XASystemEventsTextFieldList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textFields(), XASystemEventsTextFieldList)

    def toolbars(self, filter: dict = None) -> Union['XASystemEventsToolbarList', None]:
        """Returns a list of toolbar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsToolbarList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsToolbarList)

    def ui_elements(self, filter: dict = None) -> Union['XASystemEventsUIElementList', None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsUIElementList)

    def click(self, point: Union[tuple[int, int], None] = None):
        """Cause the window.

        :param point: The coordinate location at which to click, defaults to None
        :type point: Union[tuple[int, int], None], optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.clickAt_(point)

    def increment(self):
        """Increments the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.increment()

    def decrement(self):
        """Decrements the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.decrement()

    def confirm(self):
        """Confirms the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.confirm()

    def pick(self):
        """Picks the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.pick()

    def cancel(self):
        """Cancels the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cancel()




class XASystemEventsUserList(XABase.XAList):
    """A wrapper around lists of users that employs fast enumeration techniques.

    All properties of users can be called as methods on the wrapped list, returning a list containing each user's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsUser, filter)

    def full_name(self) -> list[str]:
        """Gets the full name of each user in the list.

        :return: A list of user names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fullName"))

    def home_directory(self) -> list[XABase.XAPath]:
        """Gets the home directory path of each user in the list.

        :return: A list of user home directory paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("homeDirectory")
        return [XABase.XAPath(x) for x in ls]

    def name(self) -> list[str]:
        """Gets the short name of each user in the list.

        :return: A list of user names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def picture_path(self) -> list[XABase.XAPath]:
        """Gets the picture path of each user in the list.

        :return: A list of user picture paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("picturePath")
        return [XABase.XAPath(x) for x in ls]

    def by_full_name(self, full_name: str) -> Union['XASystemEventsUser', None]:
        """Retrieves the user whose full name matches the given name, if one exists.

        :return: The desired user, if it is found
        :rtype: Union[XASystemEventsUser, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("fullName", full_name)

    def by_home_directory(self, home_directory: Union[XABase.XAPath, str]) -> Union['XASystemEventsUser', None]:
        """Retrieves the user whose short name matches the given name, if one exists.

        :return: The desired user, if it is found
        :rtype: Union[XASystemEventsUser, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(home_directory, str):
            home_directory = XABase.XAPath(home_directory)
        return self.by_property("homeDirectory", home_directory.xa_elem)

    def by_name(self, name: str) -> Union['XASystemEventsUser', None]:
        """Retrieves the user whose short name matches the given name, if one exists.

        :return: The desired user, if it is found
        :rtype: Union[XASystemEventsUser, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_picture_path(self, picture_path: Union[XABase.XAPath, str]) -> Union['XASystemEventsUser', None]:
        """Retrieves the user whose short name matches the given name, if one exists.

        :return: The desired user, if it is found
        :rtype: Union[XASystemEventsUser, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(picture_path, str):
            picture_path = XABase.XAPath(picture_path)
        return self.by_property("picturePath", picture_path.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.full_name()) + ">"

class XASystemEventsUser(XABase.XAObject):
    """A user of the system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.full_name: str #: user's full name
        self.home_directory: XABase.XAPath #: path to user's home directory
        self.name: str #: user's short name
        self.picture_path: XABase.XAPath #: path to user's picture. Can be set for current user only!

    @property
    def full_name(self) -> str:
        return self.xa_elem.fullName()

    @property
    def home_directory(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.homeDirectory())

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def picture_path(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.picturePath())

    @picture_path.setter
    def picture_path(self, picture_path: Union[XABase.XAPath, str]):
        if isinstance(picture_path, str):
            self.set_property('picturePath', picture_path)
        else:
            self.set_property('picturePath', picture_path.xa_elem)




class XASystemEventsAppearancePreferencesObject(XABase.XAObject):
    """A collection of appearance preferences.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.appearance: XASystemEventsApplication.Appearance #: the overall look of buttons, menus and windows
        self.font_smoothing: bool #: Is font smoothing on?
        self.font_smoothing_style: XASystemEventsApplication.FontSmoothingStyle #: the method used for smoothing fonts
        self.highlight_color: XASystemEventsApplication.HighlightColor #: color used for hightlighting selected text and lists
        self.recent_applications_limit: int #: the number of recent applications to track
        self.recent_documents_limit: int #: the number of recent documents to track
        self.recent_servers_limit: int #: the number of recent servers to track
        self.scroll_bar_action: XASystemEventsApplication.ScrollPageBehavior #: the action performed by clicking the scroll bar
        self.smooth_scrolling: bool #: Is smooth scrolling used?
        self.dark_mode: bool #: use dark menu bar and dock

    @property
    def appearance(self) -> XASystemEventsApplication.Appearance:
        return XASystemEventsApplication.Appearance(self.xa_elem.appearance())

    @appearance.setter
    def appearance(self, appearance: XASystemEventsApplication.Appearance):
        self.set_property('appearance', appearance.value)

    @property
    def font_smoothing(self) -> bool:
        return self.xa_elem.fontSmoothing()

    @font_smoothing.setter
    def font_smoothing(self, font_smoothing: bool):
        self.set_property('fontSmoothing', font_smoothing)

    @property
    def font_smoothing_style(self) -> XASystemEventsApplication.FontSmoothingStyle:
        return XASystemEventsApplication.FontSmoothingStyle(self.xa_elem.fontSmoothingStyle())

    @font_smoothing_style.setter
    def font_smoothing_style(self, font_smoothing_style: XASystemEventsApplication.FontSmoothingStyle):
        self.set_property('fontSmoothingStyle', font_smoothing_style.value)

    @property
    def highlight_color(self) -> XASystemEventsApplication.HighlightColor:
        return XASystemEventsApplication.HighlightColor(self.xa_elem.highlightColor())

    @highlight_color.setter
    def highlight_color(self, highlight_color: XASystemEventsApplication.HighlightColor):
        self.set_property('highlightColor', highlight_color.value)

    @property
    def recent_applications_limit(self) -> int:
        return self.xa_elem.recentApplicationsLimit()

    @recent_applications_limit.setter
    def recent_applications_limit(self, recent_applications_limit: int):
        self.set_property('recentApplicationsLimit', recent_applications_limit)

    @property
    def recent_documents_limit(self) -> int:
        return self.xa_elem.recentDocumentsLimit()

    @recent_documents_limit.setter
    def recent_documents_limit(self, recent_documents_limit: int):
        self.set_property('recentDocumentsLimit', recent_documents_limit)

    @property
    def recent_servers_limit(self) -> int:
        return self.xa_elem.recentServersLimit()

    @recent_servers_limit.setter
    def recent_servers_limit(self, recent_servers_limit: int):
        self.set_property('recentServersLimit', recent_servers_limit)

    @property
    def scroll_bar_action(self) -> XASystemEventsApplication.ScrollPageBehavior:
        return XASystemEventsApplication.ScrollPageBehavior(self.xa_elem.scrollBarAction())

    @scroll_bar_action.setter
    def scroll_bar_action(self, scroll_bar_action: XASystemEventsApplication.ScrollPageBehavior):
        self.set_property('scrollBarAction', scroll_bar_action.value)

    @property
    def smooth_scrolling(self) -> bool:
        return self.xa_elem.smoothScrolling()

    @smooth_scrolling.setter
    def smooth_scrolling(self, smooth_scrolling: bool):
        self.set_property('smoothScrolling', smooth_scrolling)

    @property
    def dark_mode(self) -> bool:
        return self.xa_elem.darkMode()

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self.set_property('darkMode', dark_mode)
    



class XASystemEventsCDAndDVDPreferencesObject(XABase.XAObject):
    """The user's CD and DVD insertion preferences.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.blank_cd: XASystemEventsInsertionPreference #: the blank CD insertion preference
        self.blank_dvd: XASystemEventsInsertionPreference #: the blank DVD insertion preference
        self.blank_bd: XASystemEventsInsertionPreference #: the blank BD insertion preference
        self.music_cd: XASystemEventsInsertionPreference #: the music CD insertion preference
        self.picture_cd: XASystemEventsInsertionPreference #: the picture CD insertion preference
        self.video_dvd: XASystemEventsInsertionPreference #: the video DVD insertion preference
        self.video_bd: XASystemEventsInsertionPreference #: the video BD insertion preference

    @property
    def blank_cd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.blankCD(), XASystemEventsInsertionPreference)

    @property
    def blank_dvd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.blankDVD(), XASystemEventsInsertionPreference)

    @property
    def blank_bd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.blankBD(), XASystemEventsInsertionPreference)

    @property
    def music_cd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.musicCD(), XASystemEventsInsertionPreference)

    @property
    def picture_cd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.pictureCD(), XASystemEventsInsertionPreference)

    @property
    def video_dvd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.videoDVD(), XASystemEventsInsertionPreference)

    @property
    def video_bd(self) -> 'XASystemEventsInsertionPreference':
        return self._new_element(self.xa_elem.videoBD(), XASystemEventsInsertionPreference)
    



class XASystemEventsInsertionPreference(XABase.XAObject):
    """A specific insertion preference.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.custom_application: Union[str, None] #: application to launch or activate on the insertion of media
        self.custom_script: Union[str, None] #: AppleScript to launch or activate on the insertion of media
        self.insertion_action: XASystemEventsApplication.MediaInsertionAction #: action to perform on media insertion

    @property
    def custom_application(self) -> Union[str, None]:
        return self.xa_elem.customApplication()

    @custom_application.setter
    def custom_application(self, custom_application: Union[str, None]):
        self.set_property('customApplication', custom_application)

    @property
    def custom_script(self) -> Union[str, None]:
        return self.xa_elem.customScript()

    @custom_script.setter
    def custom_script(self, custom_script: Union[str, None]):
        self.set_property('customScript', custom_script)

    @property
    def insertion_action(self) -> XASystemEventsApplication.MediaInsertionAction:
        return XASystemEventsApplication.MediaInsertionAction(self.xa_elem.insertionAction())

    @insertion_action.setter
    def insertion_action(self, insertion_action: XASystemEventsApplication.MediaInsertionAction):
        self.set_property('insertionAction', insertion_action.value)




class XASystemEventsDesktopList(XABase.XAList):
    """A wrapper around lists of desktops that employs fast enumeration techniques.

    All properties of desktops can be called as methods on the wrapped list, returning a list containing each desktop's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsUser, filter)

    def name(self) -> list[str]:
        """Gets the name of each desktop in the list.

        :return: A list of desktop names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[int]:
        """Gets the ID of each desktop in the list.

        :return: A list of desktop IDs
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def change_interval(self) -> list[float]:
        """Gets the change interval of each desktop in the list.

        :return: A list of desktop picture change intervals
        :rtype: list[float]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("changeInterval"))

    def display_name(self) -> list[str]:
        """Gets the display name of each desktop in the list.

        :return: A list of desktop display names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayName"))

    def picture(self) -> list[XABase.XAPath]:
        """Gets the picture path of each desktop in the list.

        :return: A list of desktop picture paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("picture")
        return [XABase.XAPath(x) for x in ls]

    def picture_rotation(self) -> list[XASystemEventsApplication.PictureRotation]:
        """Gets the picture rotation setting of each desktop in the list.

        :return: A list of desktop picture rotation settings
        :rtype: list[XASystemEventsApplication.PictureRotation]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("pictureRotation")
        return [XASystemEventsApplication.PictureRotation(x) for x in ls]

    def pictures_folder(self) -> list[XABase.XAPath]:
        """Gets the pictures folder of each desktop in the list.

        :return: A list of desktop pictures folders
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("picturesFolder")
        return [XABase.XAPath(x) for x in ls]

    def random_folder(self) -> list[bool]:
        """Gets the random order setting of each desktop in the list.

        :return: A list of desktop random order settings
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("randomOrder"))

    def translucent_menu_bar(self) -> list[bool]:
        """Gets the translucent menu bar setting of each desktop in the list.

        :return: A list of desktop translucent menu bar settings
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("translucentMenuBar"))

    def dynamic_style(self) -> list[XASystemEventsApplication.DynamicStyle]:
        """Gets the dynamic style of each desktop in the list.

        :return: A list of desktop dynamic styles
        :rtype: list[XASystemEventsApplication.DynamicStyle]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("dynamicStyle")
        return [XASystemEventsApplication.DynamicStyle(x) for x in ls]

    def by_name(self, name: str) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the desktop whose name matches the given name, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: int) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the desktop whose ID matches the given ID, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_change_interval(self, change_interval: float) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose change interval matches the given change interval, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("changeInterval", change_interval)

    def by_display_name(self, display_name: str) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose display name matches the given name, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("displayName", display_name)

    def by_picture(self, picture: Union[XABase.XAPath, str]) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose picture path matches the given path, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(picture, str):
            picture = XABase.XAPath(picture)
        return self.by_property("picture", picture.xa_elem)

    def by_picture_rotation(self, picture_rotation: XASystemEventsApplication.PictureRotation) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose picture rotation setting matches the given picture rotation setting, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("pictureRotation", picture_rotation.value)

    def by_pictures_folder(self, pictures_folder: Union[XABase.XAPath, str]) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose pictures folder path matches the given path, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(pictures_folder, str):
            pictures_folder = XABase.XAPath(pictures_folder)
        return self.by_property("picturesFolder", pictures_folder.xa_elem)

    def by_random_order(self, random_order: bool) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose random order setting matches the given boolean value, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("randomOrder", random_order)

    def by_translucent_menu_bar(self, translucent_menu_bar: bool) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the first desktop whose translucent menu bar setting matches the given boolean value, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("translucentMenuBar", translucent_menu_bar)

    def by_dynamic_style(self, dynamic_style: XASystemEventsApplication.DynamicStyle) -> Union['XASystemEventsDesktop', None]:
        """Retrieves the desktop whose dynamic style matches the given dynamic style, if one exists.

        :return: The desired desktop, if it is found
        :rtype: Union[XASystemEventsDesktop, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("dynamicStyle", dynamic_style.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsDesktop(XABase.XAObject):
    """Desktop picture settings for desktops belonging to the user.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: name of the desktop
        self.id: int #: unique identifier of the desktop
        self.change_interval: float #: number of seconds to wait between changing the desktop picture
        self.display_name: str #: name of display on which this desktop appears
        self.picture: XABase.XAPath #: path to file used as desktop picture
        self.picture_rotation: XASystemEventsApplication.PictureRotation #: never, using interval, using login, after sleep
        self.pictures_folder: XABase.XAPath #: path to folder containing pictures for changing desktop background
        self.random_order: bool #: turn on for random ordering of changing desktop pictures
        self.translucent_menu_bar: bool #: indicates whether the menu bar is translucent
        self.dynamic_style: XASystemEventsApplication.DynamicStyle #: desktop picture dynamic style

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def change_interval(self) -> float:
        return self.xa_elem.changeInterval()

    @change_interval.setter
    def change_interval(self, change_interval: float):
        self.set_property('changeInterval', change_interval)

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def picture(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.picture().get())

    @picture.setter
    def picture(self, picture: Union[XABase.XAPath, str]):
        if isinstance(picture, str):
            picture = XABase.XAPath(picture)
        self.set_property('picture', picture.xa_elem)

    @property
    def picture_rotation(self) -> XASystemEventsApplication.PictureRotation:
        return XASystemEventsApplication.PictureRotation(self.xa_elem.pictureRotation())

    @picture_rotation.setter
    def picture_rotation(self, picture_rotation: XASystemEventsApplication.PictureRotation):
        self.set_property('pictureRotation', picture_rotation.value)

    @property
    def pictures_folder(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.picturesFolder())

    @pictures_folder.setter
    def pictures_folder(self, pictures_folder: Union[XABase.XAPath, str]):
        if isinstance(pictures_folder, str):
            pictures_folder = XABase.XAPath(pictures_folder)
        self.set_property('picturesFolder', pictures_folder.xa_elem)

    @property
    def random_order(self) -> bool:
        return self.xa_elem.randomOrder()

    @random_order.setter
    def random_order(self, random_order: bool):
        self.set_property('randomOrder', random_order)

    @property
    def translucent_menu_bar(self) -> bool:
        return self.xa_elem.translucentMenuBar()

    @translucent_menu_bar.setter
    def transluscent_menu_bar(self, transluscent_menu_bar: bool):
        self.set_property('transluscent_menu_bar', transluscent_menu_bar)

    @property
    def dynamic_style(self) -> XASystemEventsApplication.DynamicStyle:
        # TODO - check
        return XASystemEventsApplication.DynamicStyle(XABase.OSType(self.xa_elem.dynamicStyle().stringValue()))

    @dynamic_style.setter
    def dynamic_style(self, dynamic_style: XASystemEventsApplication.DynamicStyle):
        self.set_property('dynamicStyle', dynamic_style.value)
    



class XASystemEventsDockPreferencesObject(XABase.XAObject):
    """The current user's dock preferences.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.animate: bool #: is the animation of opening applications on or off?
        self.autohide: bool #: is autohiding the dock on or off?
        self.dock_size: float #: size/height of the items (between 0.0 (minimum) and 1.0 (maximum))
        self.autohide_menu_bar: bool #: is autohiding the menu bar on or off?
        self.double_click_behavior: XASystemEventsApplication.DoubleClickBehavior #: behaviour when double clicking window a title bar
        self.magnification: bool #: is magnification on or off?
        self.magnification_size: float #: maximum magnification size when magnification is on (between 0.0 (minimum) and 1.0 (maximum))
        self.minimize_effect: XASystemEventsApplication.MinimizeEffect #: minimization effect
        self.minimize_into_application: bool #: minimize window into its application?
        self.screen_edge: XASystemEventsApplication.ScreenLocation #: location on screen
        self.show_indicators: bool #: show indicators for open applications?
        self.show_recents: bool #: show recent applications?

    @property
    def animate(self) -> bool:
        return self.xa_elem.animate()

    @animate.setter
    def animate(self, animate: bool):
        self.set_property('animate', animate)

    @property
    def autohide(self) -> bool:
        return self.xa_elem.autohide()

    @autohide.setter
    def autohide(self, autohide: bool):
        self.set_property('autohide', autohide)

    @property
    def dock_size(self) -> float:
        return self.xa_elem.dockSize()

    @dock_size.setter
    def dock_size(self, dock_size: float):
        self.set_property('dockSize', dock_size)

    @property
    def autohide_menu_bar(self) -> bool:
        return self.xa_elem.autohideMenuBar()

    @autohide_menu_bar.setter
    def autohide_menu_bar(self, autohide_menu_bar: bool):
        self.set_property('autohideMenuBar', autohide_menu_bar)

    @property
    def double_click_behavior(self) -> XASystemEventsApplication.DoubleClickBehavior:
        # TODO - check
        return XASystemEventsApplication.DoubleClickBehavior(XABase.OSType(self.xa_elem.doubleClickBehavior().stringValue()))

    @double_click_behavior.setter
    def double_click_behavior(self, double_click_behavior: XASystemEventsApplication.DoubleClickBehavior):
        self.set_property('double_click_behavior', double_click_behavior.value)

    @property
    def magnification(self) -> bool:
        return self.xa_elem.magnification()

    @magnification.setter
    def magnification(self, magnification: bool):
        self.set_property('magnification', magnification)

    @property
    def magnification_size(self) -> float:
        return self.xa_elem.magnificationSize()

    @magnification_size.setter
    def magnification_size(self, magnification_size: float):
        self.set_property('magnificationSize', magnification_size)

    @property
    def minimize_effect(self) -> XASystemEventsApplication.MinimizeEffect:
        # TODO - check
        return XASystemEventsApplication.MinimizeEffect(XABase.OSType(self.xa_elem.minimizeEffect().stringValue()))

    @minimize_effect.setter
    def minimize_effect(self, minimize_effect: XASystemEventsApplication.MinimizeEffect):
        self.set_property('minimizeEffect', minimize_effect.value)

    @property
    def minimize_into_application(self) -> bool:
        return self.xa_elem.minimizeIntoApplication()

    @minimize_into_application.setter
    def minimize_into_application(self, minimize_into_application: bool):
        self.set_property('minimizeIntoApplication', minimize_into_application)

    @property
    def screen_edge(self) -> XASystemEventsApplication.ScreenLocation:
        # TODO - check
        return XASystemEventsApplication.ScreenLocation(XABase.OSType(self.xa_elem.screenEdge().stringValue()))

    @screen_edge.setter
    def screen_edge(self, screen_edge: XASystemEventsApplication.ScreenLocation):
        self.set_property('screenEdge', screen_edge.value)

    @property
    def show_indicators(self) -> bool:
        return self.xa_elem.showIndicators()

    @show_indicators.setter
    def show_indicators(self, show_indicators: bool):
        self.set_property('showIndicators', show_indicators)

    @property
    def show_recents(self) -> bool:
        return self.xa_elem.showRecents()

    @show_recents.setter
    def show_recents(self, show_recents: bool):
        self.set_property('showRecents', show_recents)




class XASystemEventsLoginItemList(XABase.XAList):
    """A wrapper around lists of login items that employs fast enumeration techniques.

    All properties of property login items can be called as methods on the wrapped list, returning a list containing each login item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsLoginItem, filter)

    def hidden(self) -> list[bool]:
        """Gets the hidden status of each item in the list.

        :return: A list of property list hidden statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("contents"))

    def kind(self) -> list[str]:
        """Gets the kind of each item in the list.

        :return: A list of property list kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def name(self) -> list[str]:
        """Gets the name of each item in the list.

        :return: A list of property list names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each item in the list.

        :return: A list of property list paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XABase.XAPath(x) for x in ls]
        
    def by_hidden(self, hidden: bool) -> Union['XASystemEventsLoginItem', None]:
        """Retrieves the first login item whose hidden status matches the given boolean value, if one exists.

        :return: The desired login item, if it is found
        :rtype: Union[XASystemEventsLoginItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union['XASystemEventsLoginItem', None]:
        """Retrieves the first login item whose kind matches the given kind, if one exists.

        :return: The desired login item, if it is found
        :rtype: Union[XASystemEventsLoginItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union['XASystemEventsLoginItem', None]:
        """Retrieves the first login item whose name matches the given name, if one exists.

        :return: The desired login item, if it is found
        :rtype: Union[XASystemEventsLoginItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_path(self, path: Union[XABase.XAPath, str]) -> Union['XASystemEventsLoginItem', None]:
        """Retrieves the first login item whose path matches the given path, if one exists.

        :return: The desired login item, if it is found
        :rtype: Union[XASystemEventsLoginItem, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsLoginItem(XABase.XAObject):
    """An item to be launched or opened at login.add()
    
    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.hidden: bool #: Is the Login Item hidden when launched?
        self.kind: str #: the file type of the Login Item
        self.name: str #: the name of the Login Item
        self.path: str #: the file system path to the Login Item

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    @hidden.setter
    def hidden(self, hidden: bool):
        self.set_property('hidden', hidden)

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    def delete(self):
        """Deletes the login item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.delete()




class XASystemEventsConfigurationList(XABase.XAList):
    """A wrapper around lists of configurations that employs fast enumeration techniques.

    All properties of configurations can be called as methods on the wrapped list, returning a list containing each configuration's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsConfiguration, filter)

    def account_name(self) -> list[str]:
        """Gets the account name of each configuration in the list.

        :return: A list of configuration account names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("accountName") or [])

    def connected(self) -> list[bool]:
        """Gets the connected status of each configuration in the list.

        :return: A list of configuration connected status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("connected") or [])

    def id(self) -> list[str]:
        """Gets the ID of each configuration in the list.

        :return: A list of configuration IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        """Gets the name of each configuration in the list.

        :return: A list of configuration names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_account_name(self, account_name: str) -> Union['XASystemEventsConfiguration', None]:
        """Retrieves the first configuration whose account name matches the given name, if one exists.

        :return: The desired configuration, if it is found
        :rtype: Union[XASystemEventsConfiguration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("accountName", account_name)

    def by_connected(self, connected: bool) -> Union['XASystemEventsConfiguration', None]:
        """Retrieves the first configuration whose name matches the given name, if one exists.

        :return: The desired configuration, if it is found
        :rtype: Union[XASystemEventsConfiguration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("connected", connected)

    def by_id(self, id: str) -> Union['XASystemEventsConfiguration', None]:
        """Retrieves the configuration whose ID matches the given ID, if one exists.

        :return: The desired configuration, if it is found
        :rtype: Union[XASystemEventsConfiguration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XASystemEventsConfiguration', None]:
        """Retrieves the configuration whose name matches the given name, if one exists.

        :return: The desired configuration, if it is found
        :rtype: Union[XASystemEventsConfiguration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsConfiguration(XABase.XAObject):
    """A collection of settings for configuring a connection.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.account_name: str #: the name used to authenticate
        self.connected: bool #: Is the configuration connected?
        self.id: str #: the unique identifier for the configuration
        self.name: str #: the name of the configuration

    @property
    def account_name(self) -> str:
        return self.xa_elem.accountName()

    @account_name.setter
    def account_name(self, account_name: str):
        self.set_property('accountName', account_name)

    @property
    def connected(self) -> bool:
        return self.xa_elem.connected()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def connect(self) -> 'XASystemEventsConfiguration':
        """Connects the configuration.

        :return: The configuration object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.connect(), XASystemEventsConfiguration)

    def disconnect(self) -> 'XASystemEventsConfiguration':
        """Disconnects the configuration.

        :return: The configuration object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.disconnect(), XASystemEventsConfiguration)




class XASystemEventsInterfaceList(XABase.XAList):
    """A wrapper around lists of network interfaces that employs fast enumeration techniques.

    All properties of interfaces can be called as methods on the wrapped list, returning a list containing each interfaces's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsInterface, filter)

    def automatic(self) -> list[bool]:
        """Gets the automatic status of each interface in the list.

        :return: A list of interface automatic status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("automatic") or [])

    def duplex(self) -> list[str]:
        """Gets the duplex setting of each interface in the list.

        :return: A list of interface duplex settings
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("duplex") or [])

    def id(self) -> list[str]:
        """Gets the ID of each interface in the list.

        :return: A list of interface IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def kind(self) -> list[str]:
        """Gets the kind of each interface in the list.

        :return: A list of interface kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def mac_address(self) -> list[str]:
        """Gets the MAC address of each interface in the list.

        :return: A list of interface MAC addresses
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("macAddress") or [])

    def mtu(self) -> list[str]:
        """Gets the packet size of each interface in the list.

        :return: A list of interface packet sizes
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("mtu") or [])

    def name(self) -> list[str]:
        """Gets the name of each interface in the list.

        :return: A list of interface names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def speed(self) -> list[int]:
        """Gets the speed of each interface in the list.

        :return: A list of interface speeds
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("speed") or [])

    def by_automatic(self, automatic: bool) -> Union['XASystemEventsInterface', None]:
        """Retrieves the first interface whose automatic status matches the given boolean value, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("automatic", automatic)

    def by_duplex(self, duplex: str) -> Union['XASystemEventsInterface', None]:
        """Retrieves the first interface whose duplex setting matches the given duplex setting, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("duplex", duplex)

    def by_id(self, id: str) -> Union['XASystemEventsInterface', None]:
        """Retrieves the interface whose ID matches the given ID, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_kind(self, kind: str) -> Union['XASystemEventsInterface', None]:
        """Retrieves the first interface whose kind matches the given kind, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_mac_address(self, mac_address: str) -> Union['XASystemEventsInterface', None]:
        """Retrieves the interface whose MAC address matches the given MAC address, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("macAddress", mac_address)

    def by_mtu(self, mtu: int) -> Union['XASystemEventsInterface', None]:
        """Retrieves the first interface whose packet size matches the given size, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("mtu", mtu)

    def by_name(self, name: str) -> Union['XASystemEventsInterface', None]:
        """Retrieves the interface whose name matches the given name, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_speed(self, speed: int) -> Union['XASystemEventsInterface', None]:
        """Retrieves the first interface whose speed matches the given speed, if one exists.

        :return: The desired interface, if it is found
        :rtype: Union[XASystemEventsInterface, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("speed", speed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsInterface(XABase.XAObject):
    """A collection of settings for a network interface.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.automatic: bool #: configure the interface speed, duplex, and mtu automatically?
        self.duplex: str #: the duplex setting half | full | full with flow control
        self.id: str #: the unique identifier for the interface
        self.kind: str #: the type of interface
        self.mac_address: str #: the MAC address for the interface
        self.mtu: int #: the packet size
        self.name: str #: the name of the interface
        self.speed: int #: ethernet speed 10 | 100 | 1000

    @property
    def automatic(self) -> bool:
        return self.xa_elem.automatic()

    @automatic.setter
    def automatic(self, automatic: bool):
        self.set_property('automatic', automatic)

    @property
    def duplex(self) -> str:
        return self.xa_elem.duplex()

    @duplex.setter
    def duplex(self, duplex: str):
        self.set_property('duplex', duplex)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def mac_address(self) -> str:
        return self.xa_elem.MACAddress()

    @property
    def mtu(self) -> int:
        return self.xa_elem.mtu()

    @mtu.setter
    def mtu(self, mtu: int):
        self.set_property('mtu', mtu)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def speed(self) -> int:
        return self.xa_elem.speed()

    @speed.setter
    def speed(self, speed: int):
        self.set_property('speed', speed)




class XASystemEventsLocationList(XABase.XAList):
    """A wrapper around lists of service locations that employs fast enumeration techniques.

    All properties of locations can be called as methods on the wrapped list, returning a list containing each location's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsLocation, filter)

    def id(self) -> list[str]:
        """Gets the ID of each location in the list.

        :return: A list of location IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        """Gets the name of each location in the list.

        :return: A list of location names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_id(self, id: str) -> Union['XASystemEventsLocation', None]:
        """Retrieves the location whose ID matches the given ID, if one exists.

        :return: The desired location, if it is found
        :rtype: Union[XASystemEventsLocation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)
    
    def by_name(self, name: str) -> Union['XASystemEventsLocation', None]:
        """Retrieves the location whose name matches the given name, if one exists.

        :return: The desired location, if it is found
        :rtype: Union[XASystemEventsLocation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsLocation(XABase.XAObject):
    """A set of services.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.id: str #: The unique identifier for the location
        self.name: str #: The name of the location

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)
    



class XASystemEventsNetworkPreferencesObject(XABase.XAObject):
    """The preferences for the current user's network.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.current_location: XASystemEventsLocation #: The current location

    @property
    def current_location(self) -> XASystemEventsLocation:
        return self._new_element(self.xa_elem.currentLocation(), XASystemEventsLocation)

    @current_location.setter
    def current_location(self, current_location: XASystemEventsLocation):
        self.set_property('currentLocation', current_location.xa_elem)

    def interfaces(self, filter: dict = None) -> Union['XASystemEventsInterfaceList', None]:
        """Returns a list of interfaces, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned interfaces will have, or None
        :type filter: Union[dict, None]
        :return: The list of interfaces
        :rtype: XASystemEventsInterfaceList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.interfaces(), XASystemEventsInterfaceList, filter)

    def locations(self, filter: dict = None) -> Union['XASystemEventsLocationList', None]:
        """Returns a list of locations, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned locations will have, or None
        :type filter: Union[dict, None]
        :return: The list of locations
        :rtype: XASystemEventsLocationList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.locations(), XASystemEventsLocationList, filter)

    def services(self, filter: dict = None) -> Union['XASystemEventsServiceList', None]:
        """Returns a list of services, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned services will have, or None
        :type filter: Union[dict, None]
        :return: The list of services
        :rtype: XASystemEventsServiceList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.services(), XASystemEventsServiceList, filter)
    



class XASystemEventsServiceList(XABase.XAList):
    """A wrapper around lists of services that employs fast enumeration techniques.

    All properties of services can be called as methods on the wrapped list, returning a list containing each service's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsService, filter)

    def active(self) -> list[bool]:
        """Gets the active status of each service in the list.

        :return: A list of service active booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("active") or [])

    def current_configuration(self) -> XASystemEventsConfigurationList:
        """Gets the current configuration of each service in the list.

        :return: A list of service configurations
        :rtype: XASystemEventsConfigurationList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentConfiguration") or []
        return self._new_element(ls, XASystemEventsConfigurationList)

    def id(self) -> list[str]:
        """Gets the ID of each service in the list.

        :return: A list of service IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def interface(self) -> XASystemEventsInterfaceList:
        """Gets the interface of each service in the list.

        :return: A list of service interfaces
        :rtype: XASystemEventsInterfaceList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("interface") or []
        return self._new_element(ls, XASystemEventsInterfaceList)

    def kind(self) -> list[str]:
        """Gets the kind of each service in the list.

        :return: A list of service kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def name(self) -> list[str]:
        """Gets the name of each service in the list.

        :return: A list of service names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_active(self, active: bool) -> Union['XASystemEventsService', None]:
        """Retrieves the first service whose active status matches the given boolean value, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("active", active)

    def by_current_configuration(self, current_configuration: XASystemEventsConfiguration) -> Union['XASystemEventsService', None]:
        """Retrieves the first service whose current configuration matches the given configuration, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("currentConfiguration", current_configuration.xa_elem)

    def by_id(self, id: str) -> Union['XASystemEventsService', None]:
        """Retrieves the service whose ID matches the given ID, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_interface(self, interface: XASystemEventsInterface) -> Union['XASystemEventsService', None]:
        """Retrieves the service whose interface matches the given interface, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("interface", interface.xa_elem)

    def by_kind(self, kind: str) -> Union['XASystemEventsService', None]:
        """Retrieves the service whose kind matches the given kind, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union['XASystemEventsService', None]:
        """Retrieves the service whose name matches the given name, if one exists.

        :return: The desired service, if it is found
        :rtype: Union[XASystemEventsService, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsService(XABase.XAObject):
    """A collection of settings for a network service.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.active: bool #: Is the service active?
        self.current_configuration: XASystemEventsConfiguration #: The currently selected configuration
        self.id: str #: The unique identifier for the service
        self.interface: XASystemEventsInterface #: The interface the service is built on
        self.kind: int #: The type of service
        self.name: str #: The name of the service

    @property
    def active(self) -> bool:
        return self.xa_elem.active()

    @property
    def current_configuration(self) -> XASystemEventsConfiguration:
        return self._new_element(self.xa_elem.currentConfiguration(), XASystemEventsConfiguration)

    @current_configuration.setter
    def current_configuration(self, current_configuration: XASystemEventsConfiguration):
        self.set_property('currentConfiguration', current_configuration.xa_elem)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def interface(self) -> XASystemEventsInterface:
        return self._new_element(self.xa_elem.interface(), XASystemEventsInterface)

    @interface.setter
    def interface(self, interface: XASystemEventsInterface):
        self.set_property('interface', interface.xa_elem)

    @property
    def kind(self) -> int:
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    def connect(self) -> XASystemEventsConfiguration:
        """Connects the service.

        :return: The service object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.connect()

    def disconnect(self) -> XASystemEventsConfiguration:
        """Disconnects the service.

        :return: The service object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.disconnect()




class XASystemEventsScreenSaverList(XABase.XAList):
    """A wrapper around lists of screen savers that employs fast enumeration techniques.

    All properties of screen savers can be called as methods on the wrapped list, returning a list containing each screen saver's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScreenSaver, filter)

    def displayed_name(self) -> list[str]:
        """Gets the displayed name of each screen saver in the list.

        :return: A list of screen saver displayed names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def name(self) -> list[str]:
        """Gets the name of each screen saver in the list.

        :return: A list of screen saver names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each screen saver in the list.

        :return: A list of screen saver paths
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def picture_display_style(self) -> list[str]:
        """Gets the picture display style of each screen saver in the list.

        :return: A list of screen saver picture display styles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("pictureDisplayStyle") or [])

    def by_displayed_name(self, displayed_name: str) -> Union['XASystemEventsScreenSaver', None]:
        """Retrieves the screen saver whose displayed name matches the given name, if one exists.

        :return: The desired screen saver, if it is found
        :rtype: Union[XASystemEventsScreenSaver, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("displayedName", displayed_name)

    def by_name(self, name: str) -> Union['XASystemEventsScreenSaver', None]:
        """Retrieves the screen saver whose name matches the given name, if one exists.

        :return: The desired screen saver, if it is found
        :rtype: Union[XASystemEventsScreenSaver, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_path(self, path: Union[XABase.XAPath, str]) -> Union['XASystemEventsScreenSaver', None]:
        """Retrieves the screen saver whose name matches the given name, if one exists.

        :return: The desired screen saver, if it is found
        :rtype: Union[XASystemEventsScreenSaver, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        return self.by_property("path", path.xa_elem)

    def by_picture_display_style(self, picture_display_style: str) -> Union['XASystemEventsScreenSaver', None]:
        """Retrieves the first screen saver whose picture display style matches the given style, if one exists.

        :return: The desired screen saver, if it is found
        :rtype: Union[XASystemEventsScreenSaver, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("pictureDisplayStyle", picture_display_style)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScreenSaver(XABase.XAObject):
    """An installed screen saver.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.displayed_name: str #: name of the screen saver module as displayed to the user
        self.name: str #: name of the screen saver module to be displayed
        self.path: XABase.XAAlias #: path to the screen saver module
        self.picture_display_style: str #: effect to use when displaying picture-based screen savers (slideshow, collage, or mosaic)

    @property
    def displayedName(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> 'XABase.XAAlias':
        return self._new_element(self.xa_elem.path(), XABase.XAAlias)

    @property
    def picture_display_style(self) -> str:
        return self.xa_elem.pictureDisplayStyle()

    @picture_display_style.setter
    def picture_display_style(self, picture_display_style: str):
        self.set_property('pictureDisplayStyle', picture_display_style)

    def start(self):
        """Starts the screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.start()

    def stop(self):
        """Stops the screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stop()




class XASystemEventsScreenSaverPreferencesObject(XABase.XAObject):
    """Screen saver settings.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.delay_interval: int #: number of seconds of idle time before the screen saver starts; zero for never
        self.main_screen_only: bool #: should the screen saver be shown only on the main screen?
        self.running: bool #: is the screen saver running?
        self.show_clock: bool #: should a clock appear over the screen saver?

    @property
    def delay_interval(self) -> int:
        return self.xa_elem.delayInterval()

    @delay_interval.setter
    def delay_interval(self, delay_interval: int):
        self.set_property('delayInterval', delay_interval)

    @property
    def main_screen_only(self) -> bool:
        return self.xa_elem.mainScreenOnly()

    @main_screen_only.setter
    def main_screen_only(self, main_screen_only: bool):
        self.set_property('mainScreenOnly', main_screen_only)

    @property
    def running(self) -> bool:
        return self.xa_elem.running()

    @property
    def show_clock(self) -> bool:
        return self.xa_elem.showClock()

    @show_clock.setter
    def show_clock(self, show_clock: bool):
        self.set_property('showClock', show_clock)

    def start(self):
        """Starts the current screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.start()

    def stop(self):
        """Stops the current screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stop()




class XASystemEventsSecurityPreferencesObject(XABase.XAObject):
    """A collection of security preferences.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.automatic_login: bool #: Is automatic login allowed?
        self.log_out_when_inactive: bool #: Will the computer log out when inactive?
        self.log_out_when_inactive_interval: int #: The interval of inactivity after which the computer will log out
        self.require_password_to_unlock: bool #: Is a password required to unlock secure preferences?
        self.require_password_to_wake: bool #: Is a password required to wake the computer from sleep or screen saver?
        self.secure_virtual_memory: bool #: Is secure virtual memory being used?

    @property
    def automatic_login(self) -> bool:
        return self.xa_elem.automaticLogin()

    @automatic_login.setter
    def automatic_login(self, automatic_login: bool):
        self.set_property('automaticLogin', automatic_login)

    @property
    def log_out_when_inactive(self) -> bool:
        return self.xa_elem.logOutWhenInactive()

    @log_out_when_inactive.setter
    def log_out_when_inactive(self, log_out_when_inactive: bool):
        self.set_property('logOutWhenInactive', log_out_when_inactive)

    @property
    def log_out_when_inactive_interval(self) -> int:
        return self.xa_elem.logOutWhenInactiveInterval()

    @log_out_when_inactive_interval.setter
    def log_out_when_inactive_interval(self, log_out_when_inactive_interval: int):
        self.set_property('logOutWhenInactiveInterval', log_out_when_inactive_interval)

    @property
    def require_password_to_unlock(self) -> bool:
        return self.xa_elem.requirePasswordToUnlock()

    @require_password_to_unlock.setter
    def require_password_to_unlock(self, require_password_to_unlock: bool):
        self.set_property('requirePasswordToUnlock', require_password_to_unlock)

    @property
    def require_password_to_wake(self) -> bool:
        return self.xa_elem.requirePasswordToWake()

    @require_password_to_wake.setter
    def require_password_to_wake(self, require_password_to_wake: bool):
        self.set_property('requirePasswordToWake', require_password_to_wake)

    @property
    def secure_virtual_memory(self) -> bool:
        return self.xa_elem.secureVirtualMemory()

    @secure_virtual_memory.setter
    def secure_virtual_memory(self, secure_virtual_memory: bool):
        self.set_property('secureVirtualMemory', secure_virtual_memory)




class XASystemEventsFolderActionList(XABase.XAList):
    """A wrapper around lists of folder actions that employs fast enumeration techniques.

    All properties of folder actions can be called as methods on the wrapped list, returning a list containing each actions's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XABase.XAFolderAction, filter)

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each folder action in the list.

        :return: A list of folder action enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def name(self) -> list[str]:
        """Gets the name of each folder action in the list.

        :return: A list of folder action names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each folder action in the list.

        :return: A list of folder action paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def volume(self) -> list[str]:
        """Gets the volume of each folder action in the list.

        :return: A list of folder action volumes
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("volume") or [])

    def by_enabled(self, enabled: bool) -> Union['XABase.XAFolderAction', None]:
        """Retrieves the first folder action whose enabled status matches the given boolean value, if one exists.

        :return: The desired folder action, if it is found
        :rtype: Union[XABase.XAFolderAction, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enabled", enabled)

    def by_name(self, name: str) -> Union['XABase.XAFolderAction', None]:
        """Retrieves the folder action whose name matches the given name, if one exists.

        :return: The desired folder action, if it is found
        :rtype: Union[XABase.XAFolderAction, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_path(self, path: Union[XABase.XAPath, str]) -> Union['XABase.XAFolderAction', None]:
        """Retrieves the folder action whose path matches the given path, if one exists.

        :return: The desired folder action, if it is found
        :rtype: Union[XABase.XAFolderAction, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_volume(self, volume: str) -> Union['XABase.XAFolderAction', None]:
        """Retrieves the first folder action whose volume matches the given volume, if one exists.

        :return: The desired folder action, if it is found
        :rtype: Union[XABase.XAFolderAction, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("volume", volume)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsFolderAction(XABase.XAObject):
    """An action attached to a folder in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.enabled: bool #: Is the folder action enabled?
        self.name: str #: the name of the folder action, which is also the name of the folder
        self.path: str #: the path to the folder to which the folder action applies
        self.volume: str #: the volume on which the folder to which the folder action applies resides

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def volume(self) -> str:
        return self.xa_elem.volume()

    def enable(self):
        """Enables the folder action.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.enable()

    def scripts(self, filter: dict = None) -> Union['XASystemEventsScriptList', None]:
        """Returns a list of scripts, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripts will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripts
        :rtype: XASystemEventsScriptList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scripts(), XASystemEventsScriptList)




class XASystemEventsScriptList(XABase.XAList):
    """A wrapper around lists of scripts that employs fast enumeration techniques.

    All properties of scripts can be called as methods on the wrapped list, returning a list containing each script's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScript, filter)

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each script in the list.

        :return: A list of script enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def name(self) -> list[str]:
        """Gets the name of each script in the list.

        :return: A list of script names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each script in the list.

        :return: A list of script paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def posix_path(self) -> list[str]:
        """Gets the POSIX path of each script in the list.

        :return: A list of script POSIX paths
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("posixPath") or [])

    def by_enabled(self, enabled: bool) -> Union['XASystemEventsScript', None]:
        """Retrieves the first script whose enabled status matches the given boolean value, if one exists.

        :return: The desired script, if it is found
        :rtype: Union[XASystemEventsScript, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enabled", enabled)

    def by_name(self, name: str) -> Union['XASystemEventsScript', None]:
        """Retrieves the script whose name matches the given name, if one exists.

        :return: The desired script, if it is found
        :rtype: Union[XASystemEventsScript, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_path(self, path: Union[XABase.XAPath, str]) -> Union['XASystemEventsScript', None]:
        """Retrieves the script whose path matches the given path, if one exists.

        :return: The desired script, if it is found
        :rtype: Union[XASystemEventsScript, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_posix_path(self, posix_path: str) -> Union['XASystemEventsScript', None]:
        """Retrieves the script whose POSIX path matches the given POSIX path, if one exists.

        :return: The desired script, if it is found
        :rtype: Union[XASystemEventsScript, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("posixPath", posix_path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScript(XABase.XAObject):
    """A script invoked by a folder action.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.enabled: bool #: Is the script enabled?
        self.name: str #: the name of the script
        self.path: str #: the file system path of the disk
        self.posix_path: str #: the POSIX file system path of the disk

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property('enabled', enabled)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def posix_path(self) -> str:
        return self.xa_elem.POSIXPath()
    



class XASystemEventsActionList(XABase.XAList):
    """A wrapper around lists of actions that employs fast enumeration techniques.

    All properties of actions can be called as methods on the wrapped list, returning a list containing each action's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsAction, filter)

    def object_description(self) -> list[str]:
        """Gets the description of each action in the list.

        :return: A list of action descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def name(self) -> list[str]:
        """Gets the name of each action in the list.

        :return: A list of action names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_object_description(self, object_description: str) -> Union['XASystemEventsAction', None]:
        """Retrieves the action whose description matches the given description, if one exists.

        :return: The desired action, if it is found
        :rtype: Union[XASystemEventsAction, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_name(self, name: str) -> Union['XASystemEventsAction', None]:
        """Retrieves the action whose name matches the given name, if one exists.

        :return: The desired action, if it is found
        :rtype: Union[XASystemEventsAction, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsAction(XABase.XAObject):
    """An action that can be performed on the UI element.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.object_description: str #: what the action does
        self.name: str #: the name of the action

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def perform(self):
        """Performs the action.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.perform()
    



class XASystemEventsAttributeList(XABase.XAList):
    """A wrapper around lists of attributes that employs fast enumeration techniques.

    All properties of attributes can be called as methods on the wrapped list, returning a list containing each attribute's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsAttribute, filter)

    def name(self) -> list[str]:
        """Gets the name of each attribute in the list.

        :return: A list of attribute names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def settable(self) -> list[bool]:
        """Gets the settable status of each attribute in the list.

        :return: A list of attribute settable status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("settable") or [])

    def value(self) -> Any:
        """Gets the value of each attribute in the list.

        :return: A list of attribute values
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_name(self, name: str) -> Union['XASystemEventsAttribute', None]:
        """Retrieves the attribute whose name matches the given name, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XASystemEventsAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_settable(self, settable: bool) -> Union['XASystemEventsAttribute', None]:
        """Retrieves the first attribute whose settable status matches the given boolean value, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XASystemEventsAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("settable", settable)

    def by_value(self, value: Any) -> Union['XASystemEventsAttribute', None]:
        """Retrieves the attribute whose value matches the given value, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XASystemEventsAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsAttribute(XABase.XAObject):
    """A named data value associated with the UI element.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: the name of the attribute
        self.settable: bool #: Can the attribute be set?
        self.value: Any #: the current value of the attribute

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def settable(self) -> bool:
        return self.xa_elem.settable()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property('value', value)
    



class XASystemEventsUIElementList(XABase.XAList):
    """A wrapper around lists of UI elements that employs fast enumeration techniques.

    All properties of UI elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XASystemEventsUIElement
        super().__init__(properties, obj_class, filter)

    def accessibility_description(self) -> list[str]:
        """Gets the accessibility description of each UI element in the list.

        :return: A list of UI element accessibility descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("accessibilityDescription") or [])

    def object_description(self) -> list[str]:
        """Gets the object description of each UI element in the list.

        :return: A list of UI element object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each UI element in the list.

        :return: A list of UI element enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def entire_contents(self) -> 'XASystemEventsUIElementList':
        """Gets the entire contents of each UI element in the list.

        :return: A list of UI element contents
        :rtype: XASystemEventsUIElementList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents") or []
        return self._new_element(ls, XASystemEventsUIElementList)

    def focused(self) -> list[bool]:
        """Gets the focused status of each UI element in the list.

        :return: A list of UI element focused status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("focused") or [])

    def help(self) -> list[str]:
        """Gets the help text of each UI element in the list.

        :return: A list of UI element help texts
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("help") or [])

    def maximum_value(self) -> list[Union[int, float]]:
        """Gets the maximum value of each UI element in the list.

        :return: A list of UI element maximum values
        :rtype: list[Union[int, float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("maximumValue") or [])

    def minimum_value(self) -> list[Union[int, float]]:
        """Gets the minimum value of each UI element in the list.

        :return: A list of UI element minimum values
        :rtype: list[Union[int, float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("minimumValue") or [])

    def name(self) -> list[str]:
        """Gets the name of each UI element in the list.

        :return: A list of UI element names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def orientation(self) -> list[str]:
        """Gets the orientation of each UI element in the list.

        :return: A list of UI element orientations
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("orientation") or [])

    def position(self) -> list[tuple[int, int]]:
        """Gets the position of each UI element in the list.

        :return: A list of UI element positions
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("position") or [])

    def role(self) -> list[str]:
        """Gets the role of each UI element in the list.

        :return: A list of UI element roles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("role") or [])

    def role_description(self) -> list[str]:
        """Gets the role description of each UI element in the list.

        :return: A list of UI element role descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("roleDescription") or [])

    def selected(self) -> list[bool]:
        """Gets the selected status of each UI element in the list.

        :return: A list of UI element selected status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def size(self) -> list[tuple[int, int]]:
        """Gets the size of each UI element in the list.

        :return: A list of UI element sizes
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def subrole(self) -> list[str]:
        """Gets the subrole of each UI element in the list.

        :return: A list of UI element subroles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("subrole") or [])

    def title(self) -> list[str]:
        """Gets the title of each UI element in the list.

        :return: A list of UI element titles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def value(self) -> list[Any]:
        """Gets the value of each UI element in the list.

        :return: A list of UI element values
        :rtype: list[Any]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_accessibility_description(self, accessibility_description: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose accessibility description matches the given description, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("accessibilityDescription", accessibility_description)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose object description matches the given description, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_enabled(self, enabled: bool) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose enabled status matches the given boolean value, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enabled", enabled)

    def by_entire_contents(self, entire_contents: 'XASystemEventsUIElementList') -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose entire contnets matches the given list of contents, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("entireContents", entire_contents.xa_elem)

    def by_focused(self, focused: bool) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose focused status matches the given boolean values, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("focused", focused)

    def by_help(self, help: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose help text matches the given help text, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("help", help)

    def by_maximum_value(self, maximum_value: Union[int, float]) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose maximum value matches the given value, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("maximumValue", maximum_value)

    def by_minimum_value(self, minimum_value: Union[int, float]) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose minimum value matches the given value, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("minimumValue", minimum_value)

    def by_name(self, name: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose name matches the given name, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_orientation(self, orientation: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose orientation matches the given orientation, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("orientation", orientation)

    def by_position(self, position: tuple[int, int]) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose position matches the given position, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("position", position)

    def by_role(self, role: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose role matches the given role, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("role", role)

    def by_role_description(self, role_description: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose role description matches the given description, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("roleDescription", role_description)

    def by_selected(self, selected: bool) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose selected status matches the given boolean value, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("selected", selected)

    def by_size(self, size: tuple[int, int]) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose size matches the given size, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("size", size)

    def by_subrole(self, subrole: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose subrole matches the given subrole, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("subrole", subrole)

    def by_title(self, title: str) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose title matches the given title, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("title", title)

    def by_value(self, value: Any) -> Union['XASystemEventsUIElement', None]:
        """Retrieves the UI element whose value matches the given value, if one exists.

        :return: The desired UI element, if it is found
        :rtype: Union[XASystemEventsUIElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsUIElement(XABase.XAObject, XASelectable):
    """A piece of the user interface of a process.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.accessibility_description: Union[str, None] #: a more complete description of the UI element and its capabilities
        self.object_description: Union[str, None] #: the accessibility description, if available; otherwise, the role description
        self.enabled: Union[bool, None] #: Is the UI element enabled? ( Does it accept clicks? )
        self.entire_contents: XABase.XAList #: a list of every UI element contained in this UI element and its child UI elements, to the limits of the tree
        self.focused: Union[bool, None] #: Is the focus on this UI element?
        self.help: Union[str, None] #: an elaborate description of the UI element and its capabilities
        self.maximum_value: Union[int, float, None] #: the maximum value that the UI element can take on
        self.minimum_value: Union[int, float, None] #: the minimum value that the UI element can take on
        self.name: str #: the name of the UI Element, which identifies it within its container
        self.orientation: Union[str, None] #: the orientation of the UI element
        self.position: Union[list[Union[int, float]], None] #: the position of the UI element
        self.role: str #: an encoded description of the UI element and its capabilities
        self.role_description: str #: a more complete description of the UI element's role
        self.selected: Union[bool, None] #: Is the UI element selected?
        self.size: Union[list[Union[int, float]], None] #: the size of the UI element
        self.subrole: Union[str, None] #: an encoded description of the UI element and its capabilities
        self.title: str #: the title of the UI element as it appears on the screen
        self.value: Any #: the current value of the UI element

    @property
    def accessibility_description(self) -> Union[str, None]:
        return self.xa_elem.accessibilityDescription()

    @property
    def object_description(self) -> Union[str, None]:
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> Union[bool, None]:
        return self.xa_elem.enabled()

    @property
    def entire_contents(self) -> XABase.XAList:
        return self._new_element(self.xa_elem.entireContents(), XABase.XAList)

    @property
    def focused(self) -> Union[bool, None]:
        return self.xa_elem.focused()

    @focused.setter
    def focused(self, focused: bool):
        self.set_property('focused', focused)

    @property
    def help(self) -> Union[str, None]:
        return self.xa_elem.help()

    @property
    def maximum_value(self) -> Union[int, float, None]:
        return self.xa_elem.maximumValue()

    @property
    def minimum_value(self) -> Union[int, float, None]:
        return self.xa_elem.minimumValue()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def orientation(self) -> Union[str, None]:
        return self.xa_elem.orientation()

    @property
    def position(self) -> Union[list[Union[int, float]], None]:
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    @property
    def role(self) -> str:
        return self.xa_elem.role()

    @property
    def role_description(self) -> str:
        return self.xa_elem.roleDescription()

    @property
    def selected(self) -> Union[bool, None]:
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property('selected', selected)

    @property
    def size(self) -> Union[list[Union[int, float]], None]:
        return self.xa_elem.size()

    @size.setter
    def size(self, size: list[Union[int, float]]):
        self.set_property('size', size)

    @property
    def subrole(self) -> Union[str, None]:
        return self.xa_elem.subrole()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property('value', value)

    def click(self, point: Union[tuple[int, int], None] = None):
        """Cause the target process to behave as if the UI element were clicked.

        :param point: The coordinate location at which to click, defaults to None
        :type point: Union[tuple[int, int], None], optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.clickAt_(point)

    def increment(self):
        """Increments the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.increment()

    def decrement(self):
        """Decrements the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.decrement()

    def confirm(self):
        """Confirms the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.confirm()

    def pick(self):
        """Picks the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.pick()

    def cancel(self):
        """Cancels the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cancel()

    def actions(self, filter: dict = None) -> Union['XASystemEventsActionList', None]:
        """Returns a list of action elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of actions
        :rtype: XASystemEventsActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.actions(), XASystemEventsActionList)

    def attributes(self, filter: dict = None) -> Union['XASystemEventsAttributeList', None]:
        """Returns a list of attribute elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of attributes
        :rtype: XASystemEventsAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.attributes(), XASystemEventsAttributeList)

    def browsers(self, filter: dict = None) -> Union['XASystemEventsBrowserList', None]:
        """Returns a list of browser elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XASystemEventsBrowserList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.browsers(), XASystemEventsBrowserList)

    def busy_indicators(self, filter: dict = None) -> Union['XASystemEventsBusyIndicatorList', None]:
        """Returns a list of busy indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of busy indicators
        :rtype: XASystemEventsBusyIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.busyIndicators(), XASystemEventsBusyIndicatorList)

    def buttons(self, filter: dict = None) -> Union['XASystemEventsButtonList', None]:
        """Returns a list of button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of buttons
        :rtype: XASystemEventsButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.buttons(), XASystemEventsCheckboxList)

    def checkboxes(self, filter: dict = None) -> Union['XASystemEventsButtonList', None]:
        """Returns a list of checkbox elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of checkboxes
        :rtype: XASystemEventsCheckboxList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.checkboxes(), XASystemEventsCheckboxList)

    def color_wells(self, filter: dict = None) -> Union['XASystemEventsColorWellList', None]:
        """Returns a list of color well elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of color wells
        :rtype: XASystemEventsColorWellList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.colorWells(), XASystemEventsColorWellList)

    def columns(self, filter: dict = None) -> Union['XASystemEventsColumnList', None]:
        """Returns a list of table column elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XASystemEventsColumnList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.columns(), XASystemEventsColumnList)

    def combo_boxes(self, filter: dict = None) -> Union['XASystemEventsComboBoxList', None]:
        """Returns a list of combo box elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of combo boxes
        :rtype: XASystemEventsComboBoxList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.comboBoxes(), XASystemEventsComboBoxList)

    def drawers(self, filter: dict = None) -> Union['XASystemEventsDrawerList', None]:
        """Returns a list of drawer elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of drawers
        :rtype: XASystemEventsDrawerList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.drawers(), XASystemEventsDrawerList)

    def groups(self, filter: dict = None) -> Union['XASystemEventsGroupList', None]:
        """Returns a list of group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XASystemEventsGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.groups(), XASystemEventsGroupList)

    def grow_areas(self, filter: dict = None) -> Union['XASystemEventsGrowAreaList', None]:
        """Returns a list of grow area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of grow areas
        :rtype: XASystemEventsGrowAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.growAreas(), XASystemEventsGrowAreaList)

    def images(self, filter: dict = None) -> Union['XASystemEventsImageList', None]:
        """Returns a list of image elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XASystemEventsImageList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.images(), XASystemEventsImageList)

    def incrementors(self, filter: dict = None) -> Union['XASystemEventsIncrementorList', None]:
        """Returns a list of incrementor elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of incrementors
        :rtype: XASystemEventsIncrementorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.incrementors(), XASystemEventsIncrementorList)

    def lists(self, filter: dict = None) -> Union['XASystemEventsListList', None]:
        """Returns a list of list elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of lists
        :rtype: XASystemEventsListList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.lists(), XASystemEventsListList)

    def menus(self, filter: dict = None) -> Union['XASystemEventsMenuList', None]:
        """Returns a list of menu elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menus
        :rtype: XASystemEventsMenuList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menus(), XASystemEventsMenuList)

    def menu_bars(self, filter: dict = None) -> Union['XASystemEventsMenuBarList', None]:
        """Returns a list of menu bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu bars
        :rtype: XASystemEventsMenuBarList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuBars(), XASystemEventsMenuBarList)

    def menu_bar_items(self, filter: dict = None) -> Union['XASystemEventsMenuBarItemList', None]:
        """Returns a list of menu bar item elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu bar items
        :rtype: XASystemEventsMenuBarItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuBarItems(), XASystemEventsMenuBarItemList)

    def menu_buttons(self, filter: dict = None) -> Union['XASystemEventsMenuButtonList', None]:
        """Returns a list of menu button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu buttons
        :rtype: XASystemEventsMenuButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuButtons(), XASystemEventsMenuButtonList)

    def menu_items(self, filter: dict = None) -> Union['XASystemEventsMenuItemList', None]:
        """Returns a list of menu item elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu items
        :rtype: XASystemEventsMenuItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuItems(), XASystemEventsMenuItemList)

    def outlines(self, filter: dict = None) -> Union['XASystemEventsOutlineList', None]:
        """Returns a list of outline elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsOutlineList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.outlines(), XASystemEventsOutlineList)

    def pop_overs(self, filter: dict = None) -> Union['XASystemEventsPopOverList', None]:
        """Returns a list of pop-over elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-overs
        :rtype: XASystemEventsPopOverList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popOvers(), XASystemEventsPopOverList)

    def pop_up_buttons(self, filter: dict = None) -> Union['XASystemEventsPopUpButtonList', None]:
        """Returns a list of pop-up button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-up buttons
        :rtype: XASystemEventsPopUpButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popUpButtons(), XASystemEventsPopUpButtonList)

    def progress_indicators(self, filter: dict = None) -> Union['XASystemEventsProgressIndicatorList', None]:
        """Returns a list of progress indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of progress indicators
        :rtype: XASystemEventsProgressIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.progressIndicators(), XASystemEventsProgressIndicatorList)

    def radio_buttons(self, filter: dict = None) -> Union['XASystemEventsRadioButtonList', None]:
        """Returns a list of radio button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio buttons
        :rtype: XASystemEventsRadioButtonList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.radioButtons(), XASystemEventsRadioButtonList)

    def radio_groups(self, filter: dict = None) -> Union['XASystemEventsRadioGroupList', None]:
        """Returns a list of radio group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio groups
        :rtype: XASystemEventsRadioGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.radioGroups(), XASystemEventsRadioGroupList)

    def relevance_indicators(self, filter: dict = None) -> Union['XASystemEventsRelevanceIndicatorList', None]:
        """Returns a list of relevance indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of relevance indicators
        :rtype: XASystemEventsRelevanceIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.relevanceIndicators(), XASystemEventsRelevanceIndicatorList)

    def rows(self, filter: dict = None) -> Union['XASystemEventsRowList', None]:
        """Returns a list of table row elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XASystemEventsRowList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.rows(), XASystemEventsRowList)

    def scroll_areas(self, filter: dict = None) -> Union['XASystemEventsScrollAreaList', None]:
        """Returns a list of scroll area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll areas
        :rtype: XASystemEventsScrollAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollAreas(), XASystemEventsScrollAreaList)

    def scroll_bars(self, filter: dict = None) -> Union['XASystemEventsScrollBarList', None]:
        """Returns a list of scroll bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll bars
        :rtype: XASystemEventsScrollBarList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollBars(), XASystemEventsScrollBarList)

    def sheets(self, filter: dict = None) -> Union['XASystemEventsSheetList', None]:
        """Returns a list of sheet elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XASystemEventsSheetList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sheets(), XASystemEventsSheetList)

    def sliders(self, filter: dict = None) -> Union['XASystemEventsSliderList', None]:
        """Returns a list of slider elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sliders
        :rtype: XASystemEventsSliderList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sliders(), XASystemEventsSliderList)

    def splitters(self, filter: dict = None) -> Union['XASystemEventsSplitterList', None]:
        """Returns a list of splitter elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitters
        :rtype: XASystemEventsSplitterList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitters(), XASystemEventsSplitterList)

    def splitter_groups(self, filter: dict = None) -> Union['XASystemEventsSplitterGroupList', None]:
        """Returns a list of splitter group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitter groups
        :rtype: XASystemEventsSplitterGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitterGroups(), XASystemEventsSplitterGroupList)

    def static_texts(self, filter: dict = None) -> Union['XASystemEventsStaticTextList', None]:
        """Returns a list of static text elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of static texts
        :rtype: XASystemEventsStaticTextList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.staticTexts(), XASystemEventsStaticTextList)

    def tab_groups(self, filter: dict = None) -> Union['XASystemEventsTabGroupList', None]:
        """Returns a list of tab group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tab groups
        :rtype: XASystemEventsTabGroupList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tabGroups(), XASystemEventsTabGroupList)

    def tables(self, filter: dict = None) -> Union['XASystemEventsTableList', None]:
        """Returns a list of table elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XASystemEventsTableList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tables(), XASystemEventsTableList)

    def text_areas(self, filter: dict = None) -> Union['XASystemEventsTextAreaList', None]:
        """Returns a list of text area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text areas
        :rtype: XASystemEventsTextAreaList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textAreas(), XASystemEventsTextAreaList)

    def text_fields(self, filter: dict = None) -> Union['XASystemEventsTextFieldList', None]:
        """Returns a list of text fields elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text fields
        :rtype: XASystemEventsTextFieldList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textFields(), XASystemEventsTextFieldList)

    def toolbars(self, filter: dict = None) -> Union['XASystemEventsToolbarList', None]:
        """Returns a list of toolbar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsToolbarList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsToolbarList)

    def ui_elements(self, filter: dict = None) -> Union['XASystemEventsUIElementList', None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsUIElementList)

    def value_indicators(self, filter: dict = None) -> Union['XASystemEventsValueIndicatorList', None]:
        """Returns a list of value indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of value indicators
        :rtype: XASystemEventsValueIndicatorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.valueIndicators(), XASystemEventsValueIndicatorList)

    def windows(self, filter: dict = None) -> Union['XASystemEventsToolbarList', None]:
        """Returns a list of window elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XASystemEventsToolbarList

        .. versionadded:: 0.1.0
        """
        self.xa_wcls = XASystemEventsWindow
        return self._new_element(self.xa_elem.windows(), XABaseScriptable.XASBWindowList)
    



class XASystemEventsBrowserList(XASystemEventsUIElementList):
    """A wrapper around lists of browser elements that employs fast enumeration techniques.

    All properties of browser elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsBrowser)

class XASystemEventsBrowser(XASystemEventsUIElement):
    """A browser belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsBusyIndicatorList(XASystemEventsUIElementList):
    """A wrapper around lists of busy indicator elements that employs fast enumeration techniques.

    All properties of busy indicator elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsBusyIndicator)

class XASystemEventsBusyIndicator(XASystemEventsUIElement):
    """A busy indicator belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsButtonList(XASystemEventsUIElementList):
    """A wrapper around lists of button elements that employs fast enumeration techniques.

    All properties of button elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsButton)

class XASystemEventsButton(XASystemEventsUIElement):
    """A button belonging to a window or scroll bar.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsCheckboxList(XASystemEventsUIElementList):
    """A wrapper around lists of checkbox elements that employs fast enumeration techniques.

    All properties of checkbox elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsCheckbox)

class XASystemEventsCheckbox(XASystemEventsUIElement):
    """A checkbox belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsColorWellList(XASystemEventsUIElementList):
    """A wrapper around lists of color well elements that employs fast enumeration techniques.

    All properties of color well elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsColorWell)

class XASystemEventsColorWell(XASystemEventsUIElement):
    """A color well belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsColumnList(XASystemEventsUIElementList):
    """A wrapper around lists of table column elements that employs fast enumeration techniques.

    All properties of table column elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsColumn)

class XASystemEventsColumn(XASystemEventsUIElement):
    """A column belonging to a table.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsComboBoxList(XASystemEventsUIElementList):
    """A wrapper around lists of combo box elements that employs fast enumeration techniques.

    All properties of combo box elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsComboBox)

class XASystemEventsComboBox(XASystemEventsUIElement):
    """A combo box belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsDrawerList(XASystemEventsUIElementList):
    """A wrapper around lists of drawer elements that employs fast enumeration techniques.

    All properties of drawer elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsDrawer)

class XASystemEventsDrawer(XASystemEventsUIElement):
    """A drawer that may be extended from a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsGroupList(XASystemEventsUIElementList):
    """A wrapper around lists of group elements that employs fast enumeration techniques.

    All properties of group elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsGroup)

class XASystemEventsGroup(XASystemEventsUIElement):
    """A group belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsGrowAreaList(XASystemEventsUIElementList):
    """A wrapper around lists of grow area elements that employs fast enumeration techniques.

    All properties of grow area elements can be called as methods on the wrapped list, returning a list containing each button's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsGrowArea)

class XASystemEventsGrowArea(XASystemEventsUIElement):
    """A grow area belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsImageList(XASystemEventsUIElementList):
    """A wrapper around lists of image elements that employs fast enumeration techniques.

    All properties of image elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsImage)

class XASystemEventsImage(XASystemEventsUIElement):
    """An image belonging to a static text field.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsIncrementorList(XASystemEventsUIElementList):
    """A wrapper around lists of incrementor elements that employs fast enumeration techniques.

    All properties of incrementor elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsIncrementor)

class XASystemEventsIncrementor(XASystemEventsUIElement):
    """A incrementor belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsListList(XASystemEventsUIElementList):
    """A wrapper around lists of list UI elements that employs fast enumeration techniques.

    All properties of list elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsList)

class XASystemEventsList(XASystemEventsUIElement):
    """A list belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsMenuList(XASystemEventsUIElementList):
    """A wrapper around lists of menu elements that employs fast enumeration techniques.

    All properties of menu elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsMenu)

class XASystemEventsMenu(XASystemEventsUIElement):
    """A menu belonging to a menu bar item.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsMenuBarList(XASystemEventsUIElementList):
    """A wrapper around lists of menu bar elements that employs fast enumeration techniques.

    All properties of menu bar elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsMenuBar)

class XASystemEventsMenuBar(XASystemEventsUIElement):
    """A menu bar belonging to a process.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsMenuBarItemList(XASystemEventsUIElementList):
    """A wrapper around lists of menu bar item elements that employs fast enumeration techniques.

    All properties of menu bar item elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsMenuBarItem)

class XASystemEventsMenuBarItem(XASystemEventsUIElement):
    """A menu bar item belonging to a menu bar.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsMenuButtonList(XASystemEventsUIElementList):
    """A wrapper around lists of menu button elements that employs fast enumeration techniques.

    All properties of menu button elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsMenuButton)

class XASystemEventsMenuButton(XASystemEventsUIElement):
    """A menu button belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsMenuItemList(XASystemEventsUIElementList):
    """A wrapper around lists of menu item elements that employs fast enumeration techniques.

    All properties of menu item elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsMenuItem)

class XASystemEventsMenuItem(XASystemEventsUIElement):
    """A menu item belonging to a menu.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsOutlineList(XASystemEventsUIElementList):
    """A wrapper around lists of outline elements that employs fast enumeration techniques.

    All properties of outline elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsOutline)

class XASystemEventsOutline(XASystemEventsUIElement):
    """An outline belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsPopOverList(XASystemEventsUIElementList):
    """A wrapper around lists of popover elements that employs fast enumeration techniques.

    All properties of outline popover can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsPopOver)

class XASystemEventsPopOver(XASystemEventsUIElement):
    """A pop over belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsPopUpButtonList(XASystemEventsUIElementList):
    """A wrapper around lists of popup button elements that employs fast enumeration techniques.

    All properties of popup button elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsPopUpButton)

class XASystemEventsPopUpButton(XASystemEventsUIElement):
    """A pop up button belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsProcessList(XASystemEventsUIElementList):
    """A wrapper around lists of processes that employs fast enumeration techniques.

    All properties of processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XASystemEventsProcess
        super().__init__(properties, filter, obj_class)

    def accepts_high_level_events(self) -> list[bool]:
        """Gets the accepts high level events status of each process in the list.

        :return: A list of process accepts high level events status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("acceptsHighLevelEvents") or [])

    def accepts_remote_events(self) -> list[bool]:
        """Gets the accepts remote events status of each process in the list.

        :return: A list of process accepts remote events status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("acceptsRemoteEvents") or [])

    def architecture(self) -> list[str]:
        """Gets the architecture of each process in the list.

        :return: A list of process architectures
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("architecture") or [])

    def background_only(self) -> list[bool]:
        """Gets the background only status of each process in the list.

        :return: A list of process background only status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("backgroundOnly") or [])

    def bundle_identifier(self) -> list[str]:
        """Gets the bundle identifier of each process in the list.

        :return: A list of process bundle identifiers
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bundleIdentifier") or [])

    def classic(self) -> list[bool]:
        """Gets the classic status of each process in the list.

        :return: A list of process classic status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("class") or [])

    def creator_type(self) -> list[str]:
        """Gets the creator type of each process in the list.

        :return: A list of process creator types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def displayed_name(self) -> list[str]:
        """Gets the displayed name of each process in the list.

        :return: A list of process displayed names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def file(self) -> XABase.XAFileList:
        """Gets the file of each process in the list.

        :return: A list of process files
        :rtype: XABase.XAFileList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return self._new_element(ls, XABase.XAFileList)

    def file_type(self) -> list[str]:
        """Gets the file type of each process in the list.

        :return: A list of process file types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def has_scripting_terminology(self) -> list[bool]:
        """Gets the has scripting terminology status of each process in the list.

        :return: A list of process has scripting terminology status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hasScriptingTerminology") or [])

    def id(self) -> list[int]:
        """Gets the ID of each process in the list.

        :return: A list of process IDs
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        """Gets the name of each process in the list.

        :return: A list of process names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def partition_space_used(self) -> list[int]:
        """Gets the partition spaced used of each process in the list.

        :return: A list of process partition spaces used
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("partitionSpaceUsed") or [])

    def short_name(self) -> list[str]:
        """Gets the short name of each process in the list.

        :return: A list of process short names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shortName") or [])

    def total_partition_size(self) -> list[int]:
        """Gets the total partition size of each process in the list.

        :return: A list of process total partition sizes
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("totalPartitionSize") or [])

    def unix_id(self) -> list[int]:
        """Gets the Unix PID of each process in the list.

        :return: A list of process Unix PIDs
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("unixId") or [])

    def visible(self) -> list[bool]:
        """Gets the visible status of each process in the list.

        :return: A list of process visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def by_accepts_high_level_events(self, accepts_high_level_events: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose accepts high level events status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("acceptsHighLevelEvents", accepts_high_level_events)

    def by_accepts_remote_events(self, accepts_remote_events: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose accepts remote events status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("acceptsRemoteEvents", accepts_remote_events)

    def by_architecture(self, architecture: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose architecture matches the given architecture, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("architecture", architecture)

    def by_background_only(self, background_only: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose background only status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("backgroundOnly", background_only)

    def by_bundle_identifier(self, bundle_identifier: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose bundle identifier matches the given bundle identifier, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bundleIdentifier", bundle_identifier)

    def by_classic(self, classic: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose classic status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("classic", classic)

    def by_creator_type(self, creator_type: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose creator type matches the given creator type, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("creatorType", creator_type)

    def by_file(self, file: XABase.XAFile) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose file matches the given file, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("file", file.xa_elem)

    def by_file_type(self, file_type: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose file type matches the given file type, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", file_type)

    def by_frontmost(self, frontmost: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose frontmost status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("frontmost", frontmost)

    def by_has_scripting_terminology(self, has_scripting_terminology: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose has scripting terminology status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hasScriptingTerminology", has_scripting_terminology)

    def by_id(self, id: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose ID matches the given ID, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose name matches the given name, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_partition_space_used(self, partition_space_used: int) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose partition space used matches the given amount, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("partitionSpaceUsed", partition_space_used)

    def by_short_name(self, short_name: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose short name matches the given short name, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("shortName", short_name)

    def by_total_partition_size(self, total_partition_size: int) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose total partition size matches the given amount, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("totalPartitionSize", total_partition_size)

    def by_unix_id(self, unix_id: str) -> Union['XASystemEventsProcess', None]:
        """Retrieves the process whose UNIX PID matches the given ID, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("unixId", unix_id)

    def by_visible(self, visible: bool) -> Union['XASystemEventsProcess', None]:
        """Retrieves the first process whose visible status matches the given boolean value, if one exists.

        :return: The desired process, if it is found
        :rtype: Union[XASystemEventsProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("visible", visible)

class XASystemEventsProcess(XASystemEventsUIElement):
    """A process running on this computer.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.accepts_high_level_events: bool #: Is the process high-level event aware (accepts open application, open document, print document, and quit)?
        self.accepts_remote_events: bool #: Does the process accept remote events?
        self.architecture: str #: the architecture in which the process is running
        self.background_only: bool #: Does the process run exclusively in the background?
        self.bundle_identifier: str #: the bundle identifier of the process' application file
        self.classic: bool #: Is the process running in the Classic environment?
        self.creator_type: str #: the OSType of the creator of the process (the signature)
        self.displayed_name: str #: the name of the file from which the process was launched, as displayed in the User Interface
        self.file: XABase.XAFile #: the file from which the process was launched
        self.file_type: str #: the OSType of the file type of the process
        self.frontmost: bool #: Is the process the frontmost process
        self.has_scripting_terminology: bool #: Does the process have a scripting terminology, i.e., can it be scripted?
        self.id: int #: The unique identifier of the process
        self.name: str #: the name of the process
        self.partition_space_used: int #: the number of bytes currently used in the process' partition
        self.short_name: Union[str, None] #: the short name of the file from which the process was launched
        self.total_partition_size: int #: the size of the partition with which the process was launched
        self.unix_id: int #: The Unix process identifier of a process running in the native environment, or -1 for a process running in the Classic environment
        self.visible: bool #: Is the process' layer visible?

    @property
    def accepts_high_level_events(self) -> bool:
        return self.xa_elem.acceptsHighLevelEvents()

    @property
    def accepts_remote_events(self) -> bool:
        return self.xa_elem.acceptsRemoteEvents()

    @property
    def architecture(self) -> str:
        return self.xa_elem.architecture()

    @property
    def background_only(self) -> bool:
        return self.xa_elem.backgroundOnly()

    @property
    def bundle_identifier(self) -> str:
        return self.xa_elem.bundleIdentifier()

    @property
    def classic(self) -> bool:
        return self.xa_elem.Classic()

    @property
    def creator_type(self) -> str:
        return self.xa_elem.creatorType()

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def file(self) -> XABase.XAFile:
        return self._new_element(self.xa_elem.file(), XABase.XAFile)

    @property
    def file_type(self) -> str:
        return self.xa_elem.fileType()

    @property
    def frontmost(self) -> bool:
        return self.xa_elem.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def has_scripting_terminology(self) -> bool:
        return self.xa_elem.hasScriptingTerminology()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def partition_space_used(self) -> int:
        return self.xa_elem.partitionSpaceUsed()

    @property
    def short_name(self) -> Union[str, None]:
        return self.xa_elem.shortName()

    @property
    def total_partition_size(self) -> int:
        return self.xa_elem.totalPartitionSize()

    @property
    def unix_id(self) -> int:
        return self.xa_elem.unixId()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property('visible', visible)




class XASystemEventsApplicationProcessList(XASystemEventsProcessList):
    """A wrapper around lists of application processes that employs fast enumeration techniques.

    All properties of application processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsApplicationProcess)

    def application_file(self) -> XABase.XAFileList:
        """Gets the application file of each application process in the list.

        :return: A list of application process files
        :rtype: XABase.XAFileList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("applicationFile") or []
        return self._new_element(ls, XABase.XAFileList)

    def by_application_file(self, application_file: XABase.XAFile) -> Union['XASystemEventsApplicationProcess', None]:
        """Retrieves the application process whose file matches the given file, if one exists.

        :return: The desired application process, if it is found
        :rtype: Union[XASystemEventsApplicationProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("applicationFile", application_file.xa_elem)

class XASystemEventsApplicationProcess(XASystemEventsProcess):
    """A process launched from an application file.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.application_file: XABase.XAFile #: a reference to the application file from which this process was launched

    @property
    def application_file(self) -> XABase.XAFile:
        return self._new_element(self.xa_elem.applicationFile(), XABase.XAFile)




class XASystemEventsDeskAccessoryProcessList(XASystemEventsProcessList):
    """A wrapper around lists of desk accessory processes that employs fast enumeration techniques.

    All properties of desk accessory processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsDeskAccessoryProcess)

    def desk_accessory_file(self) -> XABase.XAFileList:
        """Gets the desk accessory file of each desk accessory process in the list.

        :return: A list of desk accessory process files
        :rtype: XABase.XAFileList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("deskAccessoryFile") or []
        return self._new_element(ls, XABase.XAFileList)

    def by_desk_accessory_file(self, desk_accessory_file: XABase.XAFile) -> Union['XASystemEventsDeskAccessoryProcess', None]:
        """Retrieves the desk accessory process whose file matches the given file, if one exists.

        :return: The desired desk accessory process, if it is found
        :rtype: Union[XASystemEventsDeskAccessoryProcess, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("deskAccessoryFile", desk_accessory_file.xa_elem)

class XASystemEventsDeskAccessoryProcess(XASystemEventsProcess):
    """A process launched from an desk accessory file.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.desk_accessory_file: XABase.XAAlias #: A reference to the desk accessory file from which this process was launched

    @property
    def desk_accessory_file(self) -> XABase.XAAlias:
        return self._new_element(self.xa_elem.deskAccessoryFile(), XABase.XAAlias)




class XASystemEventsProgressIndicatorList(XASystemEventsUIElementList):
    """A wrapper around lists of progress indicator elements that employs fast enumeration techniques.

    All properties of progress indicator elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsProgressIndicator)

class XASystemEventsProgressIndicator(XASystemEventsUIElement):
    """A progress indicator belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsRadioButtonList(XASystemEventsUIElementList):
    """A wrapper around lists of radio button elements that employs fast enumeration techniques.

    All properties of radio button elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsRadioButton)

class XASystemEventsRadioButton(XASystemEventsUIElement):
    """A radio button belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsRadioGroupList(XASystemEventsUIElementList):
    """A wrapper around lists of radio button group elements that employs fast enumeration techniques.

    All properties of radio button group elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsRadioGroup)

class XASystemEventsRadioGroup(XASystemEventsUIElement):
    """A radio button group belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsRelevanceIndicatorList(XASystemEventsUIElementList):
    """A wrapper around lists of relevance indicator elements that employs fast enumeration techniques.

    All properties of relevance indicator elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsRelevanceIndicator)

class XASystemEventsRelevanceIndicator(XASystemEventsUIElement):
    """A relevance indicator belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsRowList(XASystemEventsUIElementList):
    """A wrapper around lists of table row elements that employs fast enumeration techniques.

    All properties of table row elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsRow)

class XASystemEventsRow(XASystemEventsUIElement):
    """A row belonging to a table.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsScrollAreaList(XASystemEventsUIElementList):
    """A wrapper around lists of scroll area elements that employs fast enumeration techniques.

    All properties of scroll area elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsScrollArea)

class XASystemEventsScrollArea(XASystemEventsUIElement):
    """A scroll area belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsScrollBarList(XASystemEventsUIElementList):
    """A wrapper around lists of scroll bar elements that employs fast enumeration techniques.

    All properties of scroll bar elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsScrollBar)

class XASystemEventsScrollBar(XASystemEventsUIElement):
    """A scroll bar belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsSheetList(XASystemEventsUIElementList):
    """A wrapper around lists of sheet elements that employs fast enumeration techniques.

    All properties of sheet elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsSheet)

class XASystemEventsSheet(XASystemEventsUIElement):
    """A sheet displayed over a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsSliderList(XASystemEventsUIElementList):
    """A wrapper around lists of slider elements that employs fast enumeration techniques.

    All properties of slider elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsSlider)

class XASystemEventsSlider(XASystemEventsUIElement):
    """A slider belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsSplitterList(XASystemEventsUIElementList):
    """A wrapper around lists of splitter elements that employs fast enumeration techniques.

    All properties of splitter elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsSplitter)

class XASystemEventsSplitter(XASystemEventsUIElement):
    """A splitter belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsSplitterGroupList(XASystemEventsUIElementList):
    """A wrapper around lists of splitter group elements that employs fast enumeration techniques.

    All properties of splitter group elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsSplitterGroup)

class XASystemEventsSplitterGroup(XASystemEventsUIElement):
    """A splitter group belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsStaticTextList(XASystemEventsUIElementList):
    """A wrapper around lists of static text elements that employs fast enumeration techniques.

    All properties of static text elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsStaticText)

class XASystemEventsStaticText(XASystemEventsUIElement):
    """A static text field belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsTabGroupList(XASystemEventsUIElementList):
    """A wrapper around lists of tab group elements that employs fast enumeration techniques.

    All properties of tab group elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsTabGroup)

class XASystemEventsTabGroup(XASystemEventsUIElement):
    """A tab group belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsTableList(XASystemEventsUIElementList):
    """A wrapper around lists of table elements that employs fast enumeration techniques.

    All properties of table elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsTable)

class XASystemEventsTable(XASystemEventsUIElement):
    """A table belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsTextAreaList(XASystemEventsUIElementList):
    """A wrapper around lists of text area elements that employs fast enumeration techniques.

    All properties of text area elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsTextArea)

class XASystemEventsTextArea(XASystemEventsUIElement):
    """A text area belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsTextFieldList(XASystemEventsUIElementList):
    """A wrapper around lists of text field elements that employs fast enumeration techniques.

    All properties of text field elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsTextField)

class XASystemEventsTextField(XASystemEventsUIElement):
    """A text field belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsToolbarList(XASystemEventsUIElementList):
    """A wrapper around lists of toolbar elements that employs fast enumeration techniques.

    All properties of toolbar elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsToolbar)

class XASystemEventsToolbar(XASystemEventsUIElement):
    """A toolbar belonging to a window.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsValueIndicatorList(XASystemEventsUIElementList):
    """A wrapper around lists of value indicator elements that employs fast enumeration techniques.

    All properties of value indicator elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsValueIndicator)

class XASystemEventsValueIndicator(XASystemEventsUIElement):
    """A value indicator ( thumb or slider ) belonging to a scroll bar.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsPropertyListFileList(XABase.XAList):
    """A wrapper around lists of property list files that employs fast enumeration techniques.

    All properties of property list files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsPropertyListFile, filter)

    def contents(self) -> 'XASystemEventsPropertyListItemList':
        """Gets the items of each file in the list.

        :return: A list of property list items
        :rtype: XASystemEventsPropertyListItemList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("contents")
        return self._new_element(ls, XASystemEventsPropertyListItemList)

    def by_content(self, contents: 'XASystemEventsPropertyListItemList') -> Union['XASystemEventsPropertyListFile', None]:
        """Retrieves the property list ite whose contents matches the given contents, if one exists.

        :return: The desired property list item, if it is found
        :rtype: Union[XASystemEventsPropertyListFile, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents()) + ">"

class XASystemEventsPropertyListFile(XABase.XAObject):
    """A file containing data in Property List format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.contents: XASystemEventsPropertyListItem #: the contents of the property list file; elements and properties of the property list item may be accessed as if they were elements and properties of the property list file

    @property
    def contents(self) -> 'XASystemEventsPropertyListItem':
        return self._new_element(self.xa_elem.contents(), XASystemEventsPropertyListItem)

    @contents.setter
    def contents(self, contents: 'XASystemEventsPropertyListItem'):
        self.set_property('contents', contents.xa_elem)




class XASystemEventsPropertyListItemList(XABase.XAList):
    """A wrapper around lists of property list items that employs fast enumeration techniques.

    All properties of property list items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsPropertyListItem, filter)

    def kind(self) -> list[str]:
        """Gets the kind of each property list item in the list.

        :return: A list of property list item kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        # TODO
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def name(self) -> list[str]:
        """Gets the name of each property list item in the list.

        :return: A list of property list item names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def text(self) -> list[str]:
        """Gets the text of each property list item in the list.

        :return: A list of property list item texts
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("text"))

    def value(self) -> list[Union[int, bool, datetime, 'XASystemEventsList', dict, str, bytes]]:
        """Gets the value of each property list item in the list.

        :return: A list of property list item values
        :rtype: list[Union[int, bool, datetime, XASystemEventsList, dict, str, XASystemEventsData]]
        
        .. versionadded:: 0.1.0
        """
        # TODO: SPECIALIZE TYPE
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def by_kind(self, kind: str) -> Union['XASystemEventsPropertyListItem', None]:
        """Retrieves the property list ite whose kind matches the given kind, if one exists.

        :return: The desired property list item, if it is found
        :rtype: Union[XASystemEventsPropertyListItem, None]
        
        .. versionadded:: 0.1.0
        """
        # TODO
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union['XASystemEventsPropertyListItem', None]:
        """Retrieves the property list ite whose name matches the given name, if one exists.

        :return: The desired property list item, if it is found
        :rtype: Union[XASystemEventsPropertyListItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_text(self, text: str) -> Union['XASystemEventsPropertyListItem', None]:
        """Retrieves the property list ite whose text matches the given text, if one exists.

        :return: The desired property list item, if it is found
        :rtype: Union[XASystemEventsPropertyListItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("text", text)

    def by_value(self, value: Any) -> Union['XASystemEventsPropertyListItem', None]:
        """Retrieves the property list ite whose value matches the given value, if one exists.

        :return: The desired property list item, if it is found
        :rtype: Union[XASystemEventsPropertyListItem, None]
        
        .. versionadded:: 0.1.0
        """
        # TODO
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsPropertyListItem(XABase.XAObject):
    """A unit of data in Property List format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        # TODO - type of kind?
        self.kind: str #: the kind of data stored in the property list item: boolean/data/date/list/number/record/string
        self.name: str #: the name of the property list item (if any)
        self.text: str #: the text representation of the property list data
        self.value: Any #: the value of the property list item

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        self.set_property('text', text)

    # TODO: Specialize to exact type
    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property('value', value)

    def property_list_items(self, filter: dict = None) -> Union['XASystemEventsPropertyListItemList', None]:
        """Returns a list of property list items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list items will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list items
        :rtype: XASystemEventsPropertyListItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.propertyListItems(), XASystemEventsPropertyListItemList)




class XASystemEventsXMLAttributeList(XABase.XAList):
    """A wrapper around lists of XML attributes that employs fast enumeration techniques.

    All properties of XML attributes can be called as methods on the wrapped list, returning a list containing each attribute's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLAttribute, filter)

    def name(self) -> list[str]:
        """Gets the name of each XML attribute in the list.

        :return: A list of XML attribute names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        """Gets the value of each XML attribute in the list.

        :return: A list of XML attribute values
        :rtype: list[Any]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_name(self, name: str) -> Union['XASystemEventsXMLAttribute', None]:
        """Retrieves the XML attribute whose name matches the given name, if one exists.

        :return: The desired XML attribute, if it is found
        :rtype: Union[XASystemEventsXMLAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union['XASystemEventsXMLAttribute', None]:
        """Retrieves the first XML attribute whose value matches the given value, if one exists.

        :return: The desired XML attribute, if it is found
        :rtype: Union[XASystemEventsXMLAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsXMLAttribute(XABase.XAObject):
    """A named value associated with a unit of data in XML format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: the name of the XML attribute
        self.value: Any #: the value of the XML attribute

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property('value', value)
    



class XASystemEventsXMLDataList(XABase.XAList):
    """A wrapper around lists of XML data that employs fast enumeration techniques.

    All properties of XML datas can be called as methods on the wrapped list, returning a list containing each XML data's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLData, filter)

    def id(self) -> list[str]:
        """Gets the ID of each XML data in the list.

        :return: A list of XML data IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        """Gets the name of each XML data in the list.

        :return: A list of XML data names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def text(self) -> list[str]:
        """Gets the text of each XML data in the list.

        :return: A list of XML data texts
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("text") or [])

    def by_id(self, id: str) -> Union['XASystemEventsXMLData', None]:
        """Retrieves the XML data whose ID matches the given ID, if one exists.

        :return: The desired XML data, if it is found
        :rtype: Union[XASystemEventsXMLData, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XASystemEventsXMLData', None]:
        """Retrieves the XML data whose name matches the given name, if one exists.

        :return: The desired XML data, if it is found
        :rtype: Union[XASystemEventsXMLData, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_text(self, text: str) -> Union['XASystemEventsXMLData', None]:
        """Retrieves the first XML data whose text matches the given text, if one exists.

        :return: The desired XML data, if it is found
        :rtype: Union[XASystemEventsXMLData, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("text", text)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsXMLData(XABase.XAObject):
    """Data in XML format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.id: str #: the unique identifier of the XML data
        self.name: str #: the name of the XML data
        self.text: str #: the text representation of the XML data

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        self.set_property('text', text)

    def xml_elements(self, filter: dict = None) -> Union['XASystemEventsXMLElementList', None]:
        """Returns a list of XML elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML elements
        :rtype: XASystemEventsXMLElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.xmlElements(), XASystemEventsXMLElementList)
    



class XASystemEventsXMLElementList(XABase.XAList):
    """A wrapper around lists of XML elements that employs fast enumeration techniques.

    All properties of XML elements can be called as methods on the wrapped list, returning a list containing each elements's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLElement, filter)

    def id(self) -> list[str]:
        """Gets the ID of each XML element in the list.

        :return: A list of XML element IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        """Gets the name of each XML element in the list.

        :return: A list of XML element names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        """Gets the value of each XML element in the list.

        :return: A list of XML element values
        :rtype: list[Any]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_id(self, id: str) -> Union['XASystemEventsXMLElement', None]:
        """Retrieves the XML element whose ID matches the given ID, if one exists.

        :return: The desired XML element, if it is found
        :rtype: Union[XASystemEventsXMLElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XASystemEventsXMLElement', None]:
        """Retrieves the XML element whose name matches the given name, if one exists.

        :return: The desired XML element, if it is found
        :rtype: Union[XASystemEventsXMLElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union['XASystemEventsXMLElement', None]:
        """Retrieves the first XML element whose value matches the given value, if one exists.

        :return: The desired XML element, if it is found
        :rtype: Union[XASystemEventsXMLElement, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsXMLElement(XABase.XAObject):
    """A unit of data in XML format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.id: str #: the unique identifier of the XML element
        self.name: str #: the name of the XML element
        self.value: Any #: the value of the XML element

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property('value', value)

    def xml_attributes(self, filter: dict = None) -> Union['XASystemEventsXMLAttributeList', None]:
        """Returns a list of XML attributes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML attributes will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML attributes
        :rtype: XASystemEventsXMLAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.xmlAttributes(), XASystemEventsXMLAttributeList)

    def xml_elements(self, filter: dict = None) -> Union['XASystemEventsXMLElementList', None]:
        """Returns a list of XML elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML elements
        :rtype: XASystemEventsXMLElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.xmlElements(), XASystemEventsXMLElementList)
    



class XASystemEventsXMLFileList(XABase.XAFileList):
    """A wrapper around lists of XML files that employs fast enumeration techniques.

    All properties of XML files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsXMLFile)

    def contents(self) -> XASystemEventsXMLDataList:
        """Gets the contents of each XML file in the list.

        :return: A list of XML files contents
        :rtype: XASystemEventsXMLDataList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XASystemEventsXMLDataList)

    def by_contents(self, contents: XASystemEventsXMLData) -> Union['XASystemEventsXMLFile', None]:
        """Retrieves the XML file whose contents match the given contents, if one exists.

        :return: The desired XML file, if it is found
        :rtype: Union[XASystemEventsXMLFile, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("contents", contents.xa_elem)

class XASystemEventsXMLFile(XABase.XAObject):
    """A file containing data in XML format.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.contents: XASystemEventsXMLData #: the contents of the XML file; elements and properties of the XML data may be accessed as if they were elements and properties of the XML file

    @property
    def contents(self) -> XASystemEventsXMLData:
        return self._new_element(self.xa_elem.contents(), XASystemEventsXMLData)

    @contents.setter
    def contents(self, contents: XASystemEventsXMLData):
        self.set_property('contents', contents.xa_elem)




class XASystemEventsPrintSettings(XABase.XAObject):
    """Settings for printing.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.copies: int #: the number of copies of a document to be printed
        self.collating: bool #: Should printed copies be collated?
        self.starting_page: int #: the first page of the document to be printed
        self.ending_page: int #: the last page of the document to be printed
        self.pages_across: int #: number of logical pages laid across a physical page
        self.pages_down: int #: number of logical pages laid out down a physical page
        self.requested_print_time: datetime #: the time at which the desktop printer should print the document
        self.error_handling: XASystemEventsApplication.PrintErrorHandling #: how errors are handled
        self.fax_number: str #: for fax number
        self.target_printer: str #: for target printer

    @property
    def copies(self) -> int:
        return self.xa_elem.copies()

    @copies.setter
    def copies(self, copies: int):
        self.set_property('copies', copies)

    @property
    def collating(self) -> bool:
        return self.xa_elem.collating()

    @collating.setter
    def collating(self, collating: bool):
        self.set_property('collating', collating)

    @property
    def starting_page(self) -> int:
        return self.xa_elem.startingPage()

    @starting_page.setter
    def starting_page(self, starting_page: int):
        self.set_property('startingPage', starting_page)

    @property
    def ending_page(self) -> int:
        return self.xa_elem.endingPage()

    @ending_page.setter
    def ending_page(self, ending_page: int):
        self.set_property('endingPage', ending_page)

    @property
    def pages_across(self) -> int:
        return self.xa_elem.pagesAcross()

    @pages_across.setter
    def pages_across(self, pages_across: int):
        self.set_property('pagesAcross', pages_across)

    @property
    def pages_down(self) -> int:
        return self.xa_elem.pagesDown()

    @pages_down.setter
    def pages_down(self, pages_down: int):
        self.set_property('pagesDown', pages_down)

    @property
    def requested_print_time(self) -> datetime:
        return self.xa_elem.requestedPrintTime()

    @requested_print_time.setter
    def requested_print_time(self, requested_print_time: datetime):
        self.set_property('requestedPrintTime', requested_print_time)

    @property
    def error_handling(self) -> XASystemEventsApplication.PrintErrorHandling:
        return XASystemEventsApplication.PrintErrorHandling(self.xa_elem.errorHandling())

    @error_handling.setter
    def error_handling(self, error_handling: XASystemEventsApplication.PrintErrorHandling):
        self.set_property('error_handling', error_handling.value)

    @property
    def fax_number(self) -> str:
        return self.xa_elem.faxNumber()

    @fax_number.setter
    def fax_number(self, fax_number: str):
        self.set_property('faxNumber', fax_number)

    @property
    def target_printer(self) -> str:
        return self.xa_elem.targetPrinter()

    @target_printer.setter
    def target_printer(self, target_printer: str):
        self.set_property('targetPrinter', target_printer)
    



class XASystemEventsScriptingClassList(XABase.XAList):
    """A wrapper around lists of scripting classes that employs fast enumeration techniques.

    All properties of scripting classes can be called as methods on the wrapped list, returning a list containing each class' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingClass, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting class in the list.

        :return: A list of scripting class names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting class in the list.

        :return: A list of scripting class IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting class in the list.

        :return: A list of scripting class object description
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[bool]:
        """Gets the hidden status of each scripting class in the list.

        :return: A list of scripting class hidden status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def plural_name(self) -> list[str]:
        """Gets the plural name of each scripting class in the list.

        :return: A list of scripting class plural names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("pluralName") or [])

    def suite_name(self) -> list[str]:
        """Gets the suite name of each scripting class in the list.

        :return: A list of scripting class suite names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("suiteName") or [])

    def superclass(self) -> 'XASystemEventsScriptingClassList':
        """Gets the superclass of each scripting class in the list.

        :return: A list of scripting class superclasses
        :rtype: XASystemEventsScriptingClassList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("superclass") or []
        return self._new_element(ls, XASystemEventsScriptingClassList)

    def by_name(self, name: str) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the scripting class whose name matches the given name, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the scripting class whose ID matches the given ID, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the scripting class whose object description matches the given description, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the first scripting class whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def by_plural_name(self, plural_name: str) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the scripting class whose plural name matches the given plural name, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("pluralName", plural_name)

    def by_suite_name(self, suite_name: str) -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the first scripting class whose suite name matches the given suite name, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("suiteName", suite_name)

    def by_superclass(self, superclass: 'XASystemEventsScriptingClass') -> Union['XASystemEventsScriptingClass', None]:
        """Retrieves the first scripting class whose superclass matches the given class, if one exists.

        :return: The desired scripting class, if it is found
        :rtype: Union[XASystemEventsScriptingClass, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("superclass", superclass.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingClass(XABase.XAObject):
    """A class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the class
        self.id: str #: The unique identifier of the class
        self.object_description: str #: The description of the class
        self.hidden: bool #: Is the class hidden?
        self.plural_name: str #: The plural name of the class
        self.suite_name: str #: The name of the suite to which this class belongs
        self.superclass: XASystemEventsScriptingClass #: The class from which this class inherits

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    @property
    def plural_name(self) -> str:
        return self.xa_elem.pluralName()

    @property
    def suite_name(self) -> str:
        return self.xa_elem.suiteName()

    @property
    def superclass(self) -> 'XASystemEventsScriptingClass':
        return self._new_element(self.xa_elem.superclass(), XASystemEventsScriptingClass)

    def scripting_elements(self, filter: dict = None) -> Union['XASystemEventsScriptingElementList', None]:
        """Returns a list of scripting elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting elements
        :rtype: XASystemEventsScriptingElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingElements(), XASystemEventsScriptingElementList)

    def scripting_properties(self, filter: dict = None) -> Union['XASystemEventsScriptingPropertyList', None]:
        """Returns a list of scripting properties, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting properties will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting properties
        :rtype: XASystemEventsScriptingPropertyList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingProperties(), XASystemEventsScriptingPropertyList)
    



class XASystemEventsScriptingCommandList(XABase.XAList):
    """A wrapper around lists of scripting commands that employs fast enumeration techniques.

    All properties of scripting commands can be called as methods on the wrapped list, returning a list containing each command's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingCommand, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting command in the list.

        :return: A list of scripting command names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting command in the list.

        :return: A list of scripting command IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting command in the list.

        :return: A list of scripting command object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def direct_parameter(self) -> 'XASystemEventsScriptingParameterList':
        """Gets the direct parameters of each scripting command in the list.

        :return: A list of scripting command parameters
        :rtype: XASystemEventsScriptingParameterList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("directParameter") or []
        return self._new_element(ls, XASystemEventsScriptingParameterList)

    def hidden(self) -> list[str]:
        """Gets the hidden status of each scripting command in the list.

        :return: A list of scripting command hidden status booleans
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def scripting_result(self) -> 'XASystemEventsScriptingResultObjectList':
        """Gets the scripting result object of each scripting command in the list.

        :return: A list of scripting command scripting result objects
        :rtype: XASystemEventsScriptingResultObjectList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("scriptingResult") or []
        return self._new_element(ls, XASystemEventsScriptingResultObjectList)

    def suite_name(self) -> list[str]:
        """Gets the suite name of each scripting command in the list.

        :return: A list of scripting command suite names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("suiteName") or [])

    def by_name(self, name: str) -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the scripting command whose name matches the given name, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the scripting command whose ID matches the given ID, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the scripting command whose object description matches the given description, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_direct_parameter(self, direct_parameter: 'XASystemEventsScriptingParameter') -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the first scripting command whose direct parameter matches the given parameter, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("directParameter", direct_parameter.xa_elem)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the first scripting command whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def by_scripting_result(self, scripting_result: 'XASystemEventsScriptingResultObject') -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the first scripting command whose scripting result matches the given result object, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("scriptingResult", scripting_result.xa_elem)

    def by_suite_name(self, suite_name: str) -> Union['XASystemEventsScriptingCommand', None]:
        """Retrieves the first scripting command whose suite name matches the given suite name, if one exists.

        :return: The desired scripting command, if it is found
        :rtype: Union[XASystemEventsScriptingCommand, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("suiteName", suite_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingCommand(XABase.XAObject):
    """A command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the command
        self.id: str #: The unique identifier of the command
        self.object_description: str #: The description of the command
        self.direct_parameter: XASystemEventsScriptingParameter #: The direct parameter of the command
        self.hidden: bool #: Is the command hidden?
        self.scripting_result: XASystemEventsScriptingResultObject #: The object or data returned by this command
        self.suite_name: str #: The name of the suite to which this command belongs

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def direct_parameter(self) -> 'XASystemEventsScriptingParameter':
        return self._new_element(self.xa_elem.directParameter(), XASystemEventsScriptingParameter)

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    @property
    def scripting_result(self) -> 'XASystemEventsScriptingResultObject':
        return self._new_element(self.xa_elem.scriptingResult(), XASystemEventsScriptingResultObject)

    @property
    def suite_name(self) -> str:
        return self.xa_elem.suiteName()

    def scripting_parameters(self, filter: dict = None) -> Union['XASystemEventsScriptingParameterList', None]:
        """Returns a list of scripting parameters, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting parameters will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting parameters
        :rtype: XASystemEventsScriptingParameterList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingParameters(), XASystemEventsScriptingParameterList)
    



class XASystemEventsScriptingDefinitionObject(XABase.XAObject):
    """The scripting definition of the System Events application.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def scripting_suites(self, filter: dict = None) -> Union['XASystemEventsScriptingSuiteList', None]:
        """Returns a list of scripting suites, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting suites will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting suites
        :rtype: XASystemEventsScriptingSuiteList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingSuites(), XASystemEventsScriptingSuiteList, filter)
    



class XASystemEventsScriptingElementList(XABase.XAList):
    """A wrapper around lists of scripting elements that employs fast enumeration techniques.

    All properties of scripting elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsScriptingElement)

class XASystemEventsScriptingElement(XASystemEventsScriptingClass):
    """An element within a class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        



class XASystemEventsScriptingEnumerationList(XABase.XAList):
    """A wrapper around lists of scripting enumerations that employs fast enumeration techniques.

    All properties of scripting enumerations can be called as methods on the wrapped list, returning a list containing each enumerations's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingEnumeration, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting enumeration in the list.

        :return: A list of scripting enumeration names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting enumeration in the list.

        :return: A list of scripting enumeration IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def hidden(self) -> list[str]:
        """Gets the hidden status of each scripting enumeration in the list.

        :return: A list of scripting enumeration hidden status booleans
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def by_name(self, name: str) -> Union['XASystemEventsScriptingEnumeration', None]:
        """Retrieves the scripting enumeration whose name matches the given name, if one exists.

        :return: The desired scripting enumeration, if it is found
        :rtype: Union[XASystemEventsScriptingEnumeration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingEnumeration', None]:
        """Retrieves the scripting enumeration whose ID matches the given ID, if one exists.

        :return: The desired scripting enumeration, if it is found
        :rtype: Union[XASystemEventsScriptingEnumeration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingEnumeration', None]:
        """Retrieves the first scripting enumeration whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting enumeration, if it is found
        :rtype: Union[XASystemEventsScriptingEnumeration, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingEnumeration(XABase.XAObject):
    """An enumeration within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the enumeration
        self.id: str #: The unique identifier of the enumeration
        self.hidden: bool #: Is the enumeration hidden?

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    def scripting_enumerators(self, filter: dict = None) -> Union['XASystemEventsScriptingEnumeratorList', None]:
        """Returns a list of scripting enumerators, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting enumerators will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting enumerators
        :rtype: XASystemEventsScriptingEnumeratorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingEnumerators(), XASystemEventsScriptingEnumeratorList)




class XASystemEventsScriptingEnumeratorList(XABase.XAList):
    """A wrapper around lists of scripting enumerators that employs fast enumeration techniques.

    All properties of scripting enumerators can be called as methods on the wrapped list, returning a list containing each enumerator's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingEnumerator, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting enumerator in the list.

        :return: A list of scripting enumerator names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting enumerator in the list.

        :return: A list of scripting enumerator IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting enumerator in the list.

        :return: A list of scripting enumerator object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[str]:
        """Gets the hidden status of each scripting enumerator in the list.

        :return: A list of scripting enumerator hidden status booleans
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def by_name(self, name: str) -> Union['XASystemEventsScriptingEnumerator', None]:
        """Retrieves the scripting enumerator whose name matches the given name, if one exists.

        :return: The desired scripting enumerator, if it is found
        :rtype: Union[XASystemEventsScriptingEnumerator, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingEnumerator', None]:
        """Retrieves the scripting enumerator whose ID matches the given ID, if one exists.

        :return: The desired scripting enumerator, if it is found
        :rtype: Union[XASystemEventsScriptingEnumerator, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingEnumerator', None]:
        """Retrieves the scripting enumerator whose object description matches the given description, if one exists.

        :return: The desired scripting enumerator, if it is found
        :rtype: Union[XASystemEventsScriptingEnumerator, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingEnumerator', None]:
        """Retrieves the first scripting enumerator whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting enumerator, if it is found
        :rtype: Union[XASystemEventsScriptingEnumerator, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingEnumerator(XABase.XAObject):
    """An enumerator within an enumeration within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the enumerator
        self.id: str #: The unique identifier of the enumerator
        self.object_description: str #: The description of the enumerator
        self.hidden: bool #: Is the enumerator hidden?

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()




class XASystemEventsScriptingParameterList(XABase.XAList):
    """A wrapper around lists of scripting parameters that employs fast enumeration techniques.

    All properties of scripting parameters can be called as methods on the wrapped list, returning a list containing each parameter's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingParameter, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting parameter in the list.

        :return: A list of scripting parameter names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting parameter in the list.

        :return: A list of scripting parameter IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting parameter in the list.

        :return: A list of scripting parameter object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[bool]:
        """Gets the hidden status of each scripting parameter in the list.

        :return: A list of scripting parameter hidden status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def kind(self) -> list[str]:
        """Gets the kind of each scripting parameter in the list.

        :return: A list of scripting parameter kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def optional(self) -> list[bool]:
        """Gets the optional status of each scripting parameter in the list.

        :return: A list of scripting parameter optional status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("optional") or [])

    def by_name(self, name: str) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the scripting parameter whose name matches the given name, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the scripting parameter whose ID matches the given ID, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the scripting parameter whose object description matches the given description, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the first scripting parameter whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the first scripting parameter whose kind matches the given kind, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_optional(self, optional: bool) -> Union['XASystemEventsScriptingParameter', None]:
        """Retrieves the first scripting parameter whose optional status matches the given boolean value, if one exists.

        :return: The desired scripting parameter, if it is found
        :rtype: Union[XASystemEventsScriptingParameter, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("optional", optional)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingParameter(XABase.XAObject):
    """A parameter within a command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the parameter
        self.id: str #: The unique identifier of the parameter
        self.object_description: str #: The description of the parameter
        self.hidden: bool #: Is the parameter hidden?
        self.kind: str #: The kind of object or data specified by this parameter
        self.optional: bool #: Is the parameter optional?

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def optional(self) -> bool:
        return self.xa_elem.optional()




class XASystemEventsScriptingPropertyList(XABase.XAList):
    """A wrapper around lists of scripting properties that employs fast enumeration techniques.

    All properties of scripting properties can be called as methods on the wrapped list, returning a list containing each scripting property's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingProperty, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting property in the list.

        :return: A list of scripting property names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        """Gets the ID of each scripting property in the list.

        :return: A list of scripting property IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def access(self) -> list[XASystemEventsApplication.AccessRight]:
        """Gets the access type of each scripting property in the list.

        :return: A list of scripting property access types
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("access") or []
        return [XASystemEventsApplication.AccessRight(x) for x in ls]

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting property in the list.

        :return: A list of scripting property object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enumerated(self) -> list[bool]:
        """Gets the enumerated status of each scripting property in the list.

        :return: A list of scripting property enumerated status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enumerated") or [])

    def hidden(self) -> list[str]:
        """Gets the hidden status of each scripting property in the list.

        :return: A list of scripting property hidden status booleans
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def kind(self) -> list[str]:
        """Gets the kind of each scripting property in the list.

        :return: A list of scripting property kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def listed(self) -> list[bool]:
        """Gets the listed status of each scripting property in the list.

        :return: A list of scripting property listed status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("listed") or [])

    def by_name(self, name: str) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the scripting property whose name matches the given name, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the scripting property whose ID matches the given ID, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_access(self, access: XASystemEventsApplication.AccessRight) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the first scripting property whose access type matches the given access type, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("access", access.value)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the scripting property whose object description matches the given description, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_enumerated(self, enumerated: bool) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the first scripting property whose enumerated status matches the given boolean value, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enumerated", enumerated)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the first scripting property whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the first scripting property whose kind matches the given kind, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_listed(self, listed: bool) -> Union['XASystemEventsScriptingProperty', None]:
        """Retrieves the first scripting property whose listed status matches the given boolean value, if one exists.

        :return: The desired scripting property, if it is found
        :rtype: Union[XASystemEventsScriptingProperty, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("listed", listed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingProperty(XABase.XAObject):
    """A property within a class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the property
        self.id: str #: The unique identifier of the property
        self.access: XASystemEventsApplication.AccessRight #: The type of access to this property
        self.object_description: str #: The description of the property
        self.enumerated: bool #: Is the property's value an enumerator?
        self.hidden: bool #: Is the property hidden?
        self.kind: str #: The kind of object or data returned by this property
        self.listed: bool #: Is the property's value a list?

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def access(self) -> XASystemEventsApplication.AccessRight:
        return XASystemEventsApplication.AccessRight(self.xa_elem.access())

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def enumerated(self) -> bool:
        return self.xa_elem.enumerated()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def listed(self) -> bool:
        return self.xa_elem.listed()




class XASystemEventsScriptingResultObjectList(XABase.XAList):
    """A wrapper around lists of scripting result objects that employs fast enumeration techniques.

    All properties of scripting result objects can be called as methods on the wrapped list, returning a list containing each result's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingResultObject, filter)

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting result object in the list.

        :return: A list of scripting result object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enumerated(self) -> list[bool]:
        """Gets the enumerated status of each scripting result object in the list.

        :return: A list of scripting result object enumerated status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enumerated") or [])

    def kind(self) -> list[str]:
        """Gets the kind of each scripting result object in the list.

        :return: A list of scripting result object kinds
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def listed(self) -> list[bool]:
        """Gets the listed status of each scripting result object in the list.

        :return: A list of scripting result object listed status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("listed") or [])

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingResultObject', None]:
        """Retrieves the scripting result object whose object description matches the given description, if one exists.

        :return: The desired scripting result object, if it is found
        :rtype: Union[XASystemEventsScriptingResultObject, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_enumerated(self, enumerated: bool) -> Union['XASystemEventsScriptingResultObject', None]:
        """Retrieves the first scripting result object whose enumerated status matches the given boolean value, if one exists.

        :return: The desired scripting result object, if it is found
        :rtype: Union[XASystemEventsScriptingResultObject, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enumerated", enumerated)

    def by_kind(self, kind: str) -> Union['XASystemEventsScriptingResultObject', None]:
        """Retrieves the first scripting result object whose kind matches the given kind, if one exists.

        :return: The desired scripting result object, if it is found
        :rtype: Union[XASystemEventsScriptingResultObject, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_listed(self, listed: bool) -> Union['XASystemEventsScriptingResultObject', None]:
        """Retrieves the first scripting result object whose listed status matches the given boolean value, if one exists.

        :return: The desired scripting result object, if it is found
        :rtype: Union[XASystemEventsScriptingResultObject, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("listed", listed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.kind()) + ">"

class XASystemEventsScriptingResultObject(XABase.XAObject):
    """The result of a command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.object_description: str #: The description of the property
        self.enumerated: bool #: Is the scripting result's value an enumerator?
        self.kind: str #: The kind of object or data returned by this property
        self.listed: bool #: Is the scripting result's value a list?

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def enumerated(self) -> bool:
        return self.xa_elem.enumerated()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def listed(self) -> bool:
        return self.xa_elem.listed()
    



class XASystemEventsScriptingSuiteList(XABase.XAList):
    """A wrapper around lists of scripting suites that employs fast enumeration techniques.

    All properties of scripting suites can be called as methods on the wrapped list, returning a list containing each suite's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingSuite, filter)

    def name(self) -> list[str]:
        """Gets the name of each scripting suite in the list.

        :return: A list of scripting suite names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> list[str]:
        """Gets the ID of each scripting suite in the list.

        :return: A list of scripting suite IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def object_description(self) -> list[str]:
        """Gets the object description of each scripting suite in the list.

        :return: A list of scripting suite object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def hidden(self) -> list[bool]:
        """Gets the hidden status of each scripting suite in the list.

        :return: A list of scripting suite hidden statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hidden"))

    def by_name(self, name: str) -> Union['XASystemEventsScriptingSuite', None]:
        """Retrieves the scripting suite whose name matches the given name, if one exists.

        :return: The desired scripting suite, if it is found
        :rtype: Union[XASystemEventsScriptingSuite, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union['XASystemEventsScriptingSuite', None]:
        """Retrieves the scripting suite whose ID matches the given ID, if one exists.

        :return: The desired scripting suite, if it is found
        :rtype: Union[XASystemEventsScriptingSuite, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_object_description(self, object_description: str) -> Union['XASystemEventsScriptingSuite', None]:
        """Retrieves the scripting suite whose object description matches the given description, if one exists.

        :return: The desired scripting suite, if it is found
        :rtype: Union[XASystemEventsScriptingSuite, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union['XASystemEventsScriptingSuite', None]:
        """Retrieves the first scripting suite whose hidden status matches the given boolean value, if one exists.

        :return: The desired scripting suite, if it is found
        :rtype: Union[XASystemEventsScriptingSuite, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASystemEventsScriptingSuite(XABase.XAObject):
    """A suite within a scripting definition.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The name of the suite
        self.id: str #: The unique identifier of the suite
        self.object_description: str #: The description of the suite
        self.hidden: bool #: Is the suite hidden?

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        return self.xa_elem.hidden()

    def scripting_commands(self, filter: dict = None) -> Union['XASystemEventsScriptingCommandList', None]:
        """Returns a list of scripting commands, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting commands will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting commands
        :rtype: XASystemEventsScriptingCommandList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingCommands(), XASystemEventsScriptingCommandList)

    def scripting_classes(self, filter: dict = None) -> Union['XASystemEventsScriptingClassList', None]:
        """Returns a list of scripting classes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting classes will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting classes
        :rtype: XASystemEventsScriptingClassList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingClasses(), XASystemEventsScriptingClassList)

    def scripting_enumerations(self, filter: dict = None) -> Union['XASystemEventsScriptingEnumerationList', None]:
        """Returns a list of scripting enumerations, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting enumerations will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting enumerations
        :rtype: XASystemEventsScriptingEnumerationList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingEnumerations(), XASystemEventsScriptingEnumerationList)