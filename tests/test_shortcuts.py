import unittest
import PyXA

class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.application("Shortcuts")
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
        folder1 = self.app.folders({"name": "Test"})[0]
        folder2 = self.folders.by_name("Test")
        self.assertEqual(folder1, folder2)

    def test_shortcut_eq(self):
        shortcut1 = self.app.shortcuts({"name": "Test"})[0]
        shortcut2 = self.shortcuts.by_name("Test")
        self.assertEqual(shortcut1, shortcut2)

    def test_folder_shortcuts(self):
        all_shortcuts = self.folders.shortcuts()
        shortcut = all_shortcuts[0][0]
        self.assertIsInstance(shortcut, PyXA.apps.Shortcuts.XAShortcut)

if __name__ == '__main__':
    unittest.main()