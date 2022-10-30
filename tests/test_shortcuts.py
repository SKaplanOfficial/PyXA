import PyXA
import time
import unittest

class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Shortcuts")
        self.folders = self.app.folders()
        self.shortcuts = self.app.shortcuts()

    def test_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)

    def test_folders_type(self):
        self.assertIsInstance(self.folders, PyXA.XABase.XAList)

    def test_shortcuts_type(self):
        self.assertIsInstance(self.shortcuts, PyXA.XABase.XAList)

    def test_folder_type(self):
        self.assertIsInstance(self.folders[0], PyXA.apps.Shortcuts.XAShortcutFolder)

    def test_shortcut_type(self):
        self.assertIsInstance(self.shortcuts[0], PyXA.apps.Shortcuts.XAShortcut)

    def test_folders_name(self):
        names = self.folders.name()
        self.assertIsInstance(names, list)
        self.assertIsInstance(names[0], str)

    def test_shortcuts_name(self):
        names = self.shortcuts.name()
        self.assertIsInstance(names, list)
        self.assertIsInstance(names[0], str)

    def test_folder_eq(self):
        folder1 = self.app.folders({"name": "PyXA Test Folder"})[0]
        folder2 = self.folders.by_name("PyXA Test Folder")
        self.assertEqual(folder1, folder2)

    def test_shortcut_eq(self):
        shortcut1 = self.app.shortcuts({"name": "PyXA Test"})[0]
        shortcut2 = self.shortcuts.by_name("PyXA Test")
        self.assertEqual(shortcut1, shortcut2)

    def test_folder_shortcuts(self):
        all_shortcuts = self.folders.shortcuts()
        shortcut = all_shortcuts[0][0]
        self.assertIsInstance(shortcut, PyXA.apps.Shortcuts.XAShortcut)

    def test_shortcuts_quit(self):
        self.app.quit()
        time.sleep(0.5)
        running_apps = PyXA.PyXA.running_applications()
        self.assertNotIn(self.app, running_apps)

if __name__ == '__main__':
    unittest.main()