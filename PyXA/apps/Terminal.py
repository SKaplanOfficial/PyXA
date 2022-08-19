""".. versionadded:: 0.0.1

Control the macOS Terminal application using JXA-like syntax.
"""

from enum import Enum
from typing import List, Tuple, Union

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable

class XATerminalApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Messages.app

    .. seealso:: :class:`XATerminalWindow`, :class:`XATerminalTab`, :class:`XATerminalSettingsSet`

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for what to do when calling a save event.
        """
        SAVE_FILE   = XABase.OSType('yes ') #: Save the file. 
        DONT_SAVE   = XABase.OSType('no  ') #: Do not save the file. 
        ASK         = XABase.OSType('ask ') #: Ask the user whether or not to save the file. 

    class PrintSetting(Enum):
        """Options to use when printing contacts.
        """
        STANDARD_ERROR_HANDLING = XABase.OSType('lwst') #: Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = XABase.OSType('lwdt') #: print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATerminalWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Terminal is the active application
        self.version: str #: The version of Terminal.app
        self.default_settings: XATerminalSettingsSet #: The settings set used for new windows
        self.startup_settings: XATerminalSettingsSet #: The settings set used for the window created on application startup

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
    def default_settings(self) -> 'XATerminalSettingsSet':
        return self._new_element(self.xa_scel.defaultSettings(), XATerminalSettingsSet)

    @property
    def startup_settings(self) -> 'XATerminalSettingsSet':
        return self._new_element(self.xa_scel.startupSettings(), XATerminalSettingsSet)

    def do_script(self, script: str, window_tab: Union['XATerminalWindow', 'XATerminalTab'] = None) -> 'XATerminalApplication':
        """Executes a Terminal script in the specified window or tab.

        If no window or tab is provided, the script will run in a new tab of the frontmost window.

        :param script: The script to execute.
        :type script: str
        :param window_tab: The window or tab to execute the script in, defaults to None
        :type window_tab: Union[XATerminalWindow, XATerminalTab], optional
        :return: A reference to the Terminal application object.
        :rtype: XATerminalApplication

        .. versionadded:: 0.0.1
        """
        if window_tab is None:
            window_tab = self.front_window
        self.xa_scel.doScript_in_(script, window_tab.xa_elem)
        return self

    def current_tab(self) -> 'XATerminalTab':
        """Returns the selected tab of the frontmost Terminal window.

        :return: A PyXA reference to the current tab.
        :rtype: XATerminalTab

        .. versionadded:: 0.0.1
        """
        return self.front_window.selected_tab()

    def settings_sets(self, filter: dict = None) -> Union['XATerminalSettingsSetList', None]:
        """Returns a list of settings sets, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned settings sets will have, or None
        :type filter: Union[dict, None]
        :return: The list of settings sets
        :rtype: XATerminalSettingsSetList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.settingsSets(), XATerminalSettingsSetList, filter)




class XATerminalWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject):
    """A class for managing and interacting with windows in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.frontmost: bool #: Whether the window is currently the frontmost Terminal window
        self.selected_tab: XATerminalTab #: The Terminal tab currently displayed in the window
        self.position: Tuple[int, int] #: The position of the top-left corner of the window

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @property
    def frontmost(self) -> bool:
        return self.xa_elem.frontmost()

    @property
    def selected_tab(self) -> 'XATerminalTab':
        return self._new_element(self.xa_elem.selectedTab(), XATerminalTab)

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    def selected_tab(self) -> 'XATerminalTab':
        """Gets a reference to the window's currently selected tab.

        :return: The selected tab.
        :rtype: XATerminalTab

        .. versionadded:: 0.0.1
        """
        tab_obj = self.xa_elem.selectedTab()
        return self._new_element(tab_obj, XATerminalTab)

    def tabs(self, filter: dict = None) -> Union['XATerminalTabList', None]:
        """Returns a list of tabs, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tabs will have, or None
        :type filter: Union[dict, None]
        :return: The list of tabs
        :rtype: XATerminalTabList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.tabs(), XATerminalTabList, filter)




class XATerminalTabList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Terminal tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XATerminalTab, filter)

    def number_of_rows(self) -> List[int]:
        """Gets the number of rows of each tab in the list.

        :return: A list of tab row counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfRows"))

    def number_of_columns(self) -> List[int]:
        """Gets the number of columns of each tab in the list.

        :return: A list of tab column counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfColumns"))

    def contents(self) -> List[str]:
        """Gets the contents of each tab in the list.

        :return: A list of tab contents
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("contents"))

    def history(self) -> List[str]:
        """Gets the history f each tab in the list.

        :return: A list of tab histories
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("history"))

    def busy(self) -> List[bool]:
        """Gets the busy status of each tab in the list.

        :return: A list of tab busy statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("busy"))

    def processes(self) -> List[List[str]]:
        """Gets the processes of each tab in the list.

        :return: A list of tab process lists
        :rtype: List[List[str]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("processes"))

    def selected(self) -> List[bool]:
        """Gets the selected status of each tab in the list.

        :return: A list of tab selected statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("selected"))

    def title_displays_custom_title(self) -> List[bool]:
        """Gets the custom title status of each tab in the list.

        :return: A list of tab custom title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysCustomTitle"))

    def custom_title(self) -> List[str]:
        """Gets the custom title of each tab in the list.

        :return: A list of tab custom titles
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("customTitle"))

    def tty(self) -> List[str]:
        """Gets the TTY name of each tab in the list.

        :return: A list of tab TTY names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("tty"))

    def current_settings(self) -> 'XATerminalSettingsSetList':
        """Gets the current settings of each tab in the list.

        :return: A list of tab current settings set objects
        :rtype: XATerminalSettingsSetList
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentSettings")
        return self._new_element(ls, XATerminalSettingsSetList)

    def by_number_of_rows(self, number_of_rows: int) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose number of rows matches the given number, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("numberOfRows", number_of_rows)

    def by_number_of_columns(self, number_of_columns: int) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose number of columns matches the given number, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("numberOfColumns", number_of_columns)

    def by_contents(self, contents: str) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose contents matches the given string, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("contents", contents)

    def by_history(self, history: str) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose history matches the given string, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("history", history)

    def by_busy(self, busy: bool) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose busy status matches the given boolean value, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("busy", busy)

    def by_processes(self, processes: List[str]) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose list of processes matches the given list, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("processes", processes)

    def by_selected(self, selected: bool) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose selected status matches the given boolean value, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("selected", selected)

    def by_title_displays_custom_title(self, title_displays_custom_title: bool) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose custom title status matches the given boolean value, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysCustomTitle", title_displays_custom_title)

    def by_custom_title(self, custom_title: str) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose custom title matches the given title, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("customTitle", custom_title)

    def by_tty(self, tty: str) -> Union['XATerminalTab', None]:
        """Retrieves the tab whose TTY name matches the given TTY name, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("tty", tty)

    def by_current_settings(self, current_settings: 'XATerminalSettingsSet') -> Union['XATerminalTab', None]:
        """Retrieves the tab whose current settings matches the given settings set object, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XATerminalTab, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("currentSettings", current_settings.xa_elem)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each tab in the list.

        When the clipboard content is set to a list of Terminal tabs, each tab's custom title and history are added to the clipboard.

        :return: The list of each tab's custom title and history
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        items = []
        titles = self.custom_title()
        histories = self.history()
        for index, title in enumerate(titles):
            items.append(title)
            items.append(histories[index])
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.custom_title()) + ">"

class XATerminalTab(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with tabs in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.number_of_rows: int #: The number of rows displayed in the tab
        self.number_of_columns: int #: The number of columns displayed in the tab
        self.contents: str #: The currently visible contents of the tab
        self.history: str #: The contents of the entire scrolling buffer of the tab
        self.busy: bool #: Whether the tab is currently busy running a process
        self.processes: List[str] #: The processes currently running in the tab
        self.selected: bool #: Whether the tab is currently selected
        self.title_displays_custom_title: bool #: Whether the tab's title contains a custom title
        self.custom_title: str #: The tab's custom title
        self.tty: str #: The tab's TTY device
        self.current_settings: XATerminalSettingsSet #: The set of settings which control the tab's behavior and appearance

    @property
    def number_of_rows(self) -> int:
        return self.xa_elem.numberOfRows()

    @property
    def number_of_columns(self) -> int:
        return self.xa_elem.numberOfColumns()

    @property
    def contents(self) -> str:
        return self.xa_elem.contents()

    @property
    def history(self) -> str:
        return self.xa_elem.history()

    @property
    def busy(self) -> bool:
        return self.xa_elem.busy()

    @property
    def processes(self) -> List[str]:
        return self.xa_elem.processes()

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    @property
    def title_displays_custom_title(self) -> bool:
        return self.xa_elem.titleDisplaysCustomTitle()

    @property
    def custom_title(self) -> str:
        return self.xa_elem.customTitle()

    @property
    def tty(self) -> str:
        return self.xa_elem.tty()

    @property
    def current_settings(self) -> 'XATerminalSettingsSet':
        return self._new_element(self.xa_elem.currentSettings(), XATerminalSettingsSet)

    def current_settings(self) -> 'XATerminalSettingsSet':
        """Gets a reference to the settings set currently in use by the tab.

        :return: The tab's settings set.
        :rtype: XATerminalSettingsSet

        .. versionadded:: 0.0.1
        """
        settings_set_obj = self.xa_elem.currentSettings()
        return self._new_element(settings_set_obj, XATerminalSettingsSet)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of the tab.

        When the clipboard content is set to a Terminal tab, the tab's custom title and its history are added to the clipboard.

        :return: The tab's custom title and history
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return [self.custom_title, self.history]

    def __repr__(self):
        return "<" + str(type(self)) + self.custom_title + ">"




class XATerminalSettingsSetList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Terminal settings sets that employs fast enumeration techniques.

    All properties of settings sets can be called as methods on the wrapped list, returning a list containing each settings set's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XATerminalSettingsSet, filter)

    def id(self) -> List[int]:
        """Gets the ID of each settings set in the list.

        :return: A list of settings set IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        """Gets the name of each settings set in the list.

        :return: A list of settings set names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def number_of_rows(self) -> List[int]:
        """Gets the number of rows of each settings set in the list.

        :return: A list of settings set row counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfRows"))

    def number_of_columns(self) -> List[int]:
        """Gets the number of columns of each settings set in the list.

        :return: A list of settings set column counts
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfColumns"))

    def cursor_color(self) -> List[XABase.XAColor]:
        """Gets the cursor color of each settings set in the list.

        :return: A list of settings set cursor colors
        :rtype: List[XABase.XAColor]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cursorColor")
        return [XABase.XAColor(x) for x in ls]

    def background_color(self) -> List[XABase.XAColor]:
        """Gets the background color of each settings set in the list.

        :return: A list of settings set background colors
        :rtype: List[XABase.XAColor]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor")
        return [XABase.XAColor(x) for x in ls]

    def normal_text_color(self) -> List[XABase.XAColor]:
        """Gets the normal text color of each settings set in the list.

        :return: A list of settings set normal text colors
        :rtype: List[XABase.XAColor]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("normalTextColor")
        return [XABase.XAColor(x) for x in ls]

    def bold_text_color(self) -> List[XABase.XAColor]:
        """Gets the bold text color of each settings set in the list.

        :return: A list of settings set bold text colors
        :rtype: List[XABase.XAColor]
        
        .. versionadded:: 0.0.7
        """
        ls = self.xa_elem.arrayByApplyingSelector_("boldTextColor")
        return [XABase.XAColor(x) for x in ls]

    def font_name(self) -> List[str]:
        """Gets the font name of each settings set in the list.

        :return: A list of settings set font names
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> List[int]:
        """Gets the font size of each settings set in the list.

        :return: A list of settings set font sizes
        :rtype: List[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def font_antialiasing(self) -> List[bool]:
        """Gets the font antialiasing status of each settings set in the list.

        :return: A list of settings set font antialiasing statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontAntialiasing"))

    def clean_commands(self) -> List[List[str]]:
        """Gets the clean commands of each settings set in the list.

        :return: A list of settings set clean commands
        :rtype: List[List[str]]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("cleanCommands"))

    def title_displays_device_name(self) -> List[bool]:
        """Gets the device name in title status of each settings set in the list.

        :return: A list of settings set device name in title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysDeviceName"))

    def title_displays_shell_path(self) -> List[bool]:
        """Gets the shell path in title status of each settings set in the list.

        :return: A list of settings set shell path in title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysShellPath"))

    def title_displays_window_size(self) -> List[bool]:
        """Gets the window size in title status of each settings set in the list.

        :return: A list of settings set window size in title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysWindowSize"))

    def title_displays_settings_name(self) -> List[bool]:
        """Gets the settings name in title status of each settings set in the list.

        :return: A list of settings set settings name in title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysSettingsName"))

    def title_displays_custom_title(self) -> List[bool]:
        """Gets the custom title in title status of each settings set in the list.

        :return: A list of settings set custom title in title statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("titleDisplaysCustomTitle"))

    def custom_title(self) -> List[str]:
        """Gets the custom title of each settings set in the list.

        :return: A list of settings set custom titles
        :rtype: List[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("customTitle"))

    def by_id(self, id: int) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the settings set whose ID matches the given ID, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the settings set whose name matches the given name, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("name", name)

    def by_number_of_rows(self, number_of_rows: int) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose number of rows matches the given number, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("numberOfRows", number_of_rows)

    def by_number_of_columns(self, number_of_columns: int) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose number of columns matches the given number, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("numberOfColumns", number_of_columns)

    def by_cursor_color(self, cursor_color: XABase.XAColor) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose cursor color matches the given color, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("cursorColor", cursor_color.xa_elem)

    def by_background_color(self, background_color: XABase.XAColor) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose background color matches the given color, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_normal_text_color(self, normal_text_color: XABase.XAColor) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose normal text color matches the given color, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("normalTextColor", normal_text_color.xa_elem)

    def by_bold_text_color(self, bold_text_color: XABase.XAColor) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose bold text color matches the given color, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("boldTextColor", bold_text_color.xa_elem)

    def by_font_name(self, font_name: str) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose font name matches the given font name, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: int) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose font size matches the given font size, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fontSize", font_size)

    def by_font_antialiasing(self, font_antialiasing: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose font antialiasing status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("fontAntialiasing", font_antialiasing)

    def by_clean_commands(self, clean_commands: List[str]) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose list of clean commands matches the given list, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("cleanCommands", clean_commands)

    def by_title_displays_device_name(self, title_displays_device_name: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose device name in title status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysDeviceName", title_displays_device_name)

    def by_title_displays_shell_path(self, title_displays_shell_path: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose shell path in title status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysShellPath", title_displays_shell_path)

    def by_title_displays_windows_size(self, title_displays_windows_size: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose window size in title status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysWindowSize", title_displays_windows_size)

    def by_title_displays_settings_name(self, title_displays_settings_name: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose settings name in title status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysSettingsName", title_displays_settings_name)
    
    def by_title_displays_custom_title(self, title_displays_custom_title: bool) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the first settings set whose custom title in title status matches the given boolean value, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("titleDisplaysCustomTitle", title_displays_custom_title)

    def by_custom_title(self, custom_title: str) -> Union['XATerminalSettingsSet', None]:
        """Retrieves the settings set whose custom title matches the given title, if one exists.

        :return: The desired settings set, if it is found
        :rtype: Union[XATerminalSettingsSet, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("customTitle", custom_title)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each settings set in the list.

        When the clipboard content is set to a list of settings sets, each setting set's name is added to the clipboard.

        :return: The list of setting set names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XATerminalSettingsSet(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with settings sets in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier of the settings set
        self.name: str #: The name of the settings set
        self.number_of_rows: int #: The number of rows displayed in the tab
        self.number_of_columns: int #: The number of columns displayed in the tab
        self.cursor_color: XABase.XAColor #: The cursor color for the tab
        self.background_color: XABase.XAColor #: The background color for the tab
        self.normal_text_color: XABase.XAColor #: The normal text color for the tab
        self.bold_text_color: XABase.XAColor #: The bold text color for the tab
        self.font_name: str #: The name of the font used to display the tab's contents
        self.font_size: int #: The size of the font used to display the tab's contents
        self.font_antialiasing: bool #: Whether the font used to display the tab's contents is antialiased
        self.clean_commands: List[str] #: The processes which will be ignored when checking whether a tab can be closed without showing a prompt
        self.title_displays_device_name: bool #: Whether the title contains the device name
        self.title_displays_shell_path: bool #: Whether the title contains the shell path
        self.title_displays_window_size: bool #: Whether the title contains the tab's size, in rows and columns
        self.title_displays_settings_name: bool #: Whether the title contains the settings set name
        self.title_displays_custom_title: bool #: Whether the title contains a custom title
        self.custom_title: str #: The tab's custom title

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def number_of_rows(self) -> int:
        return self.xa_elem.numberOfRows()

    @property
    def number_of_columns(self) -> int:
        return self.xa_elem.numberOfColumns()

    @property
    def cursor_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.cursorColor())

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @property
    def normal_text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.normalTextColor())

    @property
    def bold_text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.boldTextColor())

    @property
    def font_name(self) -> str:
        return self.xa_elem.fontName()

    @property
    def font_size(self) -> int:
        return self.xa_elem.fontSize()

    @property
    def font_antialiasing(self) -> bool:
        return self.xa_elem.fontAntialiasing()

    @property
    def clean_commands(self) -> List[str]:
        return self.xa_elem.cleanCommands()

    @property
    def title_displays_device_name(self) -> bool:
        return self.xa_elem.titleDisplaysDeviceName()

    @property
    def title_displays_shell_path(self) -> bool:
        return self.xa_elem.titleDisplaysShellPath()

    @property
    def title_displays_window_size(self) -> bool:
        return self.xa_elem.titleDisplaysWindowSize()

    @property
    def title_displays_settings_name(self) -> bool:
        return self.xa_elem.titleDisplaysSettingsName()

    @property
    def title_displays_custom_title(self) -> bool:
        return self.xa_elem.titleDisplaysCustomTitle()

    @property
    def custom_title(self) -> str:
        return self.xa_elem.customTitle()

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the settings set.

        When the clipboard content is set to a settings set, the setting set's name is added to the clipboard.

        :return: The setting set's name
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"