""".. versionadded:: 0.0.1

Control the macOS Terminal application using JXA-like syntax.
"""

from typing import List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

_YES = 2036691744
_NO = 1852776480
_ASK = 1634954016
_STANDARD_ERRORS = 1819767668
_DETAILED_ERRORS = 1819763828

class XATerminalApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with Messages.app

    .. seealso:: :class:`XATerminalWindow`, :class:`XATerminalTab`, :class:`XATerminalSettingsSet`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATerminalWindow

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
            window_tab = self.front_window()
        self.xa_scel.doScript_in_(script, window_tab.xa_elem)
        return self

    # Tabs
    def current_tab(self) -> 'XATerminalTab':
        """Returns the selected tab of the frontmost Terminal window.

        :return: A PyXA reference to the current tab.
        :rtype: XATerminalTab

        .. versionadded:: 0.0.1
        """
        return self.front_window().selected_tab()

    # Settings Sets
    def default_settings(self) -> 'XATerminalSettingsSet':
        """Gets a reference to the settings set used for new windows.

        :return: The default settings set.
        :rtype: XATerminalSettingsSet

        .. seealso:: :func:`startup_settings`

        .. versionadded:: 0.0.1
        """
        settings_set_obj = self.xa_scel.defaultSettings()
        return self._new_element(settings_set_obj, XATerminalSettingsSet)

    def startup_settings(self) -> 'XATerminalSettingsSet':
        """Gets a reference to the settings set used for the window created upon opening the Terminal application.

        :return: The startup settings set.
        :rtype: XATerminalSettingsSet

        .. seealso:: :func:`default_settings`

        .. versionadded:: 0.0.1
        """
        settings_set_obj = self.xa_scel.startupSettings()
        return self._new_element(settings_set_obj, XATerminalSettingsSet)

    def settings_sets(self, filter: dict = None) -> List['XATerminalSettingsSet']:
        """Returns a list of settings sets matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("settingsSets", filter, XATerminalSettingsSet)

    def settings_set(self, filter: Union[int, dict]) -> 'XATerminalSettingsSet':
        """Returns the first settings set that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("settingsSets", filter, XATerminalSettingsSet)

    def first_settings_set(self) -> 'XATerminalSettingsSet':
        """Returns the settings set at the first index of the settings sets array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("settingsSets", XATerminalSettingsSet)

    def last_settings_set(self) -> 'XATerminalSettingsSet':
        """Returns the settings set at the last (-1) index of the settings sets array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("settingsSets", XATerminalSettingsSet)

class XATerminalWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    # Tabs
    def selected_tab(self) -> 'XATerminalTab':
        """Gets a reference to the window's currently selected tab.

        :return: The selected tab.
        :rtype: XATerminalTab

        .. versionadded:: 0.0.1
        """
        tab_obj = self.xa_elem.selectedTab()
        return self._new_element(tab_obj, XATerminalTab)

    def tabs(self, filter: dict = None) -> List['XATerminalTab']:
        """Returns a list of tabs matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.elements("tabs", filter, XATerminalTab)

    def tab(self, filter: Union[int, dict]) -> 'XATerminalTab':
        """Returns the first tab that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("tabs", filter, XATerminalTab)

    def first_tab(self) -> 'XATerminalTab':
        """Returns the tab at the first index of the tabs array.

        .. versionadded:: 0.0.1
        """
        return self.first_element("tabs", XATerminalTab)

    def last_tab(self) -> 'XATerminalTab':
        """Returns the tab at the last (-1) index of the tabs array.

        .. versionadded:: 0.0.1
        """
        return self.last_element("tabs", XATerminalTab)

class XATerminalTab(XABaseScriptable.XASBObject):
    """A class for managing and interacting with tabs in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def current_settings(self) -> 'XATerminalSettingsSet':
        """Gets a reference to the settings set currently in use by the tab.

        :return: The tab's settings set.
        :rtype: XATerminalSettingsSet

        .. versionadded:: 0.0.1
        """
        settings_set_obj = self.xa_elem.currentSettings()
        return self._new_element(settings_set_obj, XATerminalSettingsSet)

class XATerminalSettingsSet(XABaseScriptable.XASBObject):
    """A class for managing and interacting with settings sets in Terminal.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)