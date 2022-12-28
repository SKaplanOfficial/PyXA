import PyXA
import unittest
import ScriptingBridge

from PyXA.apps.Terminal import XATerminalApplication, XATerminalWindow, XATerminalTabList, XATerminalTab, XATerminalSettingsSetList, XATerminalSettingsSet

class TestTerminal(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Terminal")

    def test_terminal_application(self):
        self.assertIsInstance(self.app, XATerminalApplication)
        self.assertIsInstance(self.app.xa_scel, ScriptingBridge.SBApplication)

        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.version, str)

        self.assertIsInstance(self.app.default_settings, XATerminalSettingsSet)
        self.assertIsInstance(self.app.default_settings.xa_elem.get(), ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.startup_settings, XATerminalSettingsSet)
        self.assertIsInstance(self.app.startup_settings.xa_elem.get(), ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.current_tab, XATerminalTab)
        self.assertIsInstance(self.app.current_tab.xa_elem.get(), ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.settings_sets(), XATerminalSettingsSetList)
        self.assertIsInstance(self.app.settings_sets().xa_elem, ScriptingBridge.SBElementArray)

    def test_terminal_window(self):
        windows = self.app.windows()
        window_1 = windows[0]
        front_window = self.app.front_window

        self.assertIsInstance(windows, PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(window_1, XATerminalWindow)
        self.assertIsInstance(front_window, XATerminalWindow)
        self.assertIsInstance(window_1, PyXA.XABaseScriptable.XASBWindow)
        self.assertIsInstance(front_window, PyXA.XABaseScriptable.XASBWindow)

        self.assertIsInstance(front_window.frontmost, bool)
        self.assertIsInstance(front_window.selected_tab, XATerminalTab)
        self.assertIsInstance(front_window.selected_tab.xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(front_window.position, tuple)
        self.assertIsInstance(front_window.tabs(), XATerminalTabList)
        self.assertIsInstance(front_window.tabs().xa_elem, ScriptingBridge.SBElementArray)

    def test_terminal_tab(self):
        tabs = self.app.front_window.tabs()
        
        self.assertIsInstance(tabs.number_of_rows(), list)
        self.assertIsInstance(tabs.number_of_rows()[0], int)
        self.assertIsInstance(tabs.by_number_of_rows(tabs.number_of_rows()[0]), XATerminalTab)

        self.assertIsInstance(tabs.number_of_columns(), list)
        self.assertIsInstance(tabs.number_of_columns()[0], int)
        self.assertIsInstance(tabs.by_number_of_columns(tabs.number_of_columns()[0]), XATerminalTab)

        self.assertIsInstance(tabs.contents(), list)
        self.assertIsInstance(tabs.contents()[0], str)
        self.assertIsInstance(tabs.by_contents(tabs.contents()[0]), XATerminalTab)

        self.assertIsInstance(tabs.history(), list)
        self.assertIsInstance(tabs.history()[0], str)
        self.assertIsInstance(tabs.by_history(tabs.history()[0]), XATerminalTab)

        self.assertIsInstance(tabs.busy(), list)
        self.assertIsInstance(tabs.busy()[0], bool)
        self.assertIsInstance(tabs.by_busy(tabs.busy()[0]), XATerminalTab)

        self.assertIsInstance(tabs.processes(), list)
        self.assertIsInstance(tabs.processes()[0], list)
        self.assertIsInstance(tabs.by_processes(tabs.processes()[0]), XATerminalTab)

        self.assertIsInstance(tabs.selected(), list)
        self.assertIsInstance(tabs.selected()[0], bool)
        self.assertIsInstance(tabs.by_selected(tabs.selected()[0]), XATerminalTab)

        self.assertIsInstance(tabs.title_displays_custom_title(), list)
        self.assertIsInstance(tabs.title_displays_custom_title()[0], bool)
        self.assertIsInstance(tabs.by_title_displays_custom_title(tabs.title_displays_custom_title()[0]), XATerminalTab)

        self.assertIsInstance(tabs.custom_title(), list)
        self.assertIsInstance(tabs.custom_title()[0], str)
        self.assertIsInstance(tabs.by_custom_title(tabs.custom_title()[0]), XATerminalTab)

        self.assertIsInstance(tabs.tty(), list)
        self.assertIsInstance(tabs.tty()[0], str)
        self.assertIsInstance(tabs.by_tty(tabs.tty()[0]), XATerminalTab)

        self.assertIsInstance(tabs.current_settings(), XATerminalSettingsSetList)
        self.assertIsInstance(tabs.current_settings()[0], XATerminalSettingsSet)
        self.assertIsInstance(tabs.by_current_settings(tabs.current_settings()[0]), XATerminalTab)

        tab = tabs[0]

        self.assertIsInstance(tab.number_of_rows, int)
        self.assertIsInstance(tab.number_of_columns, int)
        self.assertIsInstance(tab.contents, str)
        self.assertIsInstance(tab.history, str)
        self.assertIsInstance(tab.busy, bool)
        self.assertIsInstance(tab.processes, list)
        self.assertIsInstance(tab.processes[0], str)
        self.assertIsInstance(tab.title_displays_custom_title, bool)
        self.assertIsInstance(tab.custom_title, str)
        self.assertIsInstance(tab.tty, str)
        self.assertIsInstance(tab.current_settings, XATerminalSettingsSet)

    def test_terminal_settings_set(self):
        settings_sets = self.app.settings_sets()

        self.assertIsInstance(settings_sets.id(), list)
        self.assertIsInstance(settings_sets.id()[0], int)
        self.assertIsInstance(settings_sets.by_id(settings_sets.id()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.name(), list)
        self.assertIsInstance(settings_sets.name()[0], str)
        self.assertIsInstance(settings_sets.by_name(settings_sets.name()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.number_of_rows(), list)
        self.assertIsInstance(settings_sets.number_of_rows()[0], int)
        self.assertIsInstance(settings_sets.by_number_of_rows(settings_sets.number_of_rows()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.number_of_columns(), list)
        self.assertIsInstance(settings_sets.number_of_columns()[0], int)
        self.assertIsInstance(settings_sets.by_number_of_columns(settings_sets.number_of_columns()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.cursor_color(), list)
        self.assertIsInstance(settings_sets.cursor_color()[0], PyXA.XABase.XAColor)
        self.assertIsInstance(settings_sets.by_cursor_color(settings_sets.cursor_color()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.background_color(), list)
        self.assertIsInstance(settings_sets.background_color()[0], PyXA.XABase.XAColor)
        self.assertIsInstance(settings_sets.by_background_color(settings_sets.background_color()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.normal_text_color(), list)
        self.assertIsInstance(settings_sets.normal_text_color()[0], PyXA.XABase.XAColor)
        self.assertIsInstance(settings_sets.by_normal_text_color(settings_sets.normal_text_color()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.bold_text_color(), list)
        self.assertIsInstance(settings_sets.bold_text_color()[0], PyXA.XABase.XAColor)
        self.assertIsInstance(settings_sets.by_bold_text_color(settings_sets.bold_text_color()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.font_name(), list)
        self.assertIsInstance(settings_sets.font_name()[0], str)
        self.assertIsInstance(settings_sets.by_font_name(settings_sets.font_name()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.font_size(), list)
        self.assertIsInstance(settings_sets.font_size()[0], int)
        self.assertIsInstance(settings_sets.by_font_size(settings_sets.font_size()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.font_antialiasing(), list)
        self.assertIsInstance(settings_sets.font_antialiasing()[0], bool)
        self.assertIsInstance(settings_sets.by_font_antialiasing(settings_sets.font_antialiasing()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.clean_commands(), list)
        self.assertIsInstance(settings_sets.clean_commands()[0], list)
        self.assertIsInstance(settings_sets.by_clean_commands(settings_sets.clean_commands()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.title_displays_device_name(), list)
        self.assertIsInstance(settings_sets.title_displays_device_name()[0], bool)
        self.assertIsInstance(settings_sets.by_title_displays_device_name(settings_sets.title_displays_device_name()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.title_displays_shell_path(), list)
        self.assertIsInstance(settings_sets.title_displays_shell_path()[0], bool)
        self.assertIsInstance(settings_sets.by_title_displays_shell_path(settings_sets.title_displays_shell_path()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.title_displays_window_size(), list)
        self.assertIsInstance(settings_sets.title_displays_window_size()[0], bool)
        self.assertIsInstance(settings_sets.by_title_displays_window_size(settings_sets.title_displays_window_size()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.title_displays_settings_name(), list)
        self.assertIsInstance(settings_sets.title_displays_settings_name()[0], bool)
        self.assertIsInstance(settings_sets.by_title_displays_settings_name(settings_sets.title_displays_settings_name()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.title_displays_custom_title(), list)
        self.assertIsInstance(settings_sets.title_displays_custom_title()[0], bool)
        self.assertIsInstance(settings_sets.by_title_displays_custom_title(settings_sets.title_displays_custom_title()[0]), XATerminalSettingsSet)

        self.assertIsInstance(settings_sets.custom_title(), list)
        self.assertIsInstance(settings_sets.custom_title()[0], str)
        self.assertIsInstance(settings_sets.by_custom_title(settings_sets.custom_title()[0]), XATerminalSettingsSet)

        settings_set = settings_sets[0]

        self.assertIsInstance(settings_set.id, int)
        self.assertIsInstance(settings_set.name, str)
        self.assertIsInstance(settings_set.number_of_rows, int)
        self.assertIsInstance(settings_set.number_of_columns, int)
        self.assertIsInstance(settings_set.cursor_color, PyXA.XABase.XAColor)
        self.assertIsInstance(settings_set.background_color, PyXA.XABase.XAColor)
        self.assertIsInstance(settings_set.normal_text_color, PyXA.XABase.XAColor)
        self.assertIsInstance(settings_set.bold_text_color, PyXA.XABase.XAColor)
        self.assertIsInstance(settings_set.font_name, str)
        self.assertIsInstance(settings_set.font_size, int)
        self.assertIsInstance(settings_set.font_antialiasing, bool)
        self.assertIsInstance(settings_set.clean_commands, list)
        self.assertIsInstance(settings_set.clean_commands[0], str)
        self.assertIsInstance(settings_set.title_displays_device_name, bool)
        self.assertIsInstance(settings_set.title_displays_shell_path, bool)
        self.assertIsInstance(settings_set.title_displays_window_size, bool)
        self.assertIsInstance(settings_set.title_displays_settings_name, bool)
        self.assertIsInstance(settings_set.title_displays_custom_title, bool)
        self.assertIsInstance(settings_set.custom_title, str)