import PyXA
import unittest
import ScriptingBridge

class TestFinder(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Finder")

    def test_finder_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.app, PyXA.apps.Finder.XAFinderApplication)

    def test_finder_application_attributes(self):
        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.visible, bool)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.product_version, str)
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.selection, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(self.app.insertion_location, PyXA.apps.Finder.XAFinderFolder)
        self.assertIsInstance(self.app.startup_disk, PyXA.apps.Finder.XAFinderDisk)
        self.assertIsInstance(self.app.desktop, PyXA.apps.Finder.XAFinderDesktop)
        self.assertIsInstance(self.app.home, PyXA.apps.Finder.XAFinderFolder)
        self.assertIsInstance(self.app.trash, PyXA.apps.Finder.XAFinderTrash)
        self.assertIsInstance(self.app.computer_container, PyXA.apps.Finder.XAFinderComputer)
        self.assertIsInstance(self.app.desktop_picture, PyXA.apps.Finder.XAFinderFile)
        self.assertIsInstance(self.app.finder_preferences, PyXA.apps.Finder.XAFinderPreferences)

    def test_finder_lists(self):
        items = self.app.items()
        containers = self.app.containers()
        disks = self.app.disks()
        folders = self.app.folders()
        files = self.app.files()
        alias_files = self.app.alias_files()
        app_files = self.app.application_files()
        doc_files = self.app.document_files()
        inet_loc_files = self.app.internet_location_files()
        clippings = self.app.clippings()
        packages = self.app.packages()
        windows = self.app.windows()
        finder_windows = self.app.finder_windows()
        clipping_windows = self.app.clipping_windows()

        self.assertIsInstance(items, PyXA.XABase.XAList)
        self.assertIsInstance(containers, PyXA.XABase.XAList)
        self.assertIsInstance(disks, PyXA.XABase.XAList)
        self.assertIsInstance(folders, PyXA.XABase.XAList)
        self.assertIsInstance(files, PyXA.XABase.XAList)
        self.assertIsInstance(alias_files, PyXA.XABase.XAList)
        self.assertIsInstance(app_files, PyXA.XABase.XAList)
        self.assertIsInstance(doc_files, PyXA.XABase.XAList)
        self.assertIsInstance(inet_loc_files, PyXA.XABase.XAList)
        self.assertIsInstance(clippings, PyXA.XABase.XAList)
        self.assertIsInstance(packages, PyXA.XABase.XAList)
        self.assertIsInstance(windows, PyXA.XABase.XAList)
        self.assertIsInstance(finder_windows, PyXA.XABase.XAList)
        self.assertIsInstance(clipping_windows, PyXA.XABase.XAList)

        self.assertIsInstance(items, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(items[0], PyXA.apps.Finder.XAFinderItem)
        self.assertIsInstance(items[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(containers, PyXA.apps.Finder.XAFinderContainerList)
        self.assertIsInstance(containers, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(containers[0], PyXA.apps.Finder.XAFinderContainer)
        self.assertIsInstance(containers[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(disks, PyXA.apps.Finder.XAFinderDiskList)
        self.assertIsInstance(disks, PyXA.apps.Finder.XAFinderContainerList)
        self.assertIsInstance(disks, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(disks[0], PyXA.apps.Finder.XAFinderDisk)
        self.assertIsInstance(disks[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(folders, PyXA.apps.Finder.XAFinderFolderList)
        self.assertIsInstance(folders, PyXA.apps.Finder.XAFinderContainerList)
        self.assertIsInstance(folders, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(folders[0], PyXA.apps.Finder.XAFinderFolder)
        self.assertIsInstance(folders[0].xa_elem, ScriptingBridge.SBObject)
        
        self.assertIsInstance(files, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(files, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(files[0], PyXA.apps.Finder.XAFinderFile)
        self.assertIsInstance(files[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(alias_files, PyXA.apps.Finder.XAFinderAliasFileList)
        self.assertIsInstance(alias_files, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(alias_files, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(alias_files[0], PyXA.apps.Finder.XAFinderAliasFile)
        self.assertIsInstance(alias_files[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(app_files, PyXA.apps.Finder.XAFinderApplicationFileList)
        self.assertIsInstance(app_files, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(app_files, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(app_files[0], PyXA.apps.Finder.XAFinderApplicationFile)
        self.assertIsInstance(app_files[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(doc_files, PyXA.apps.Finder.XAFinderDocumentFileList)
        self.assertIsInstance(doc_files, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(doc_files, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(doc_files[0], PyXA.apps.Finder.XAFinderDocumentFile)
        self.assertIsInstance(doc_files[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(inet_loc_files, PyXA.apps.Finder.XAFinderInternetLocationFileList)
        self.assertIsInstance(inet_loc_files, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(inet_loc_files, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(inet_loc_files[0], PyXA.apps.Finder.XAFinderInternetLocationFile)
        self.assertIsInstance(inet_loc_files[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(clippings, PyXA.apps.Finder.XAFinderClippingList)
        self.assertIsInstance(clippings, PyXA.apps.Finder.XAFinderFileList)
        self.assertIsInstance(clippings, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(clippings[0], PyXA.apps.Finder.XAFinderClipping)
        self.assertIsInstance(clippings[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(packages, PyXA.apps.Finder.XAFinderPackageList)
        self.assertIsInstance(packages, PyXA.apps.Finder.XAFinderItemList)
        self.assertIsInstance(packages[0], PyXA.apps.Finder.XAFinderPackage)
        self.assertIsInstance(packages[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(windows, PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(windows[0], PyXA.apps.Finder.XAFinderWindow)
        self.assertIsInstance(windows[0], PyXA.XABaseScriptable.XASBWindow)
        self.assertIsInstance(windows[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(finder_windows, PyXA.apps.Finder.XAFinderFinderWindowList)
        self.assertIsInstance(finder_windows, PyXA.apps.Finder.XAFinderWindowList)
        self.assertIsInstance(finder_windows, PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(finder_windows[0], PyXA.apps.Finder.XAFinderFinderWindow)
        self.assertIsInstance(finder_windows[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(clipping_windows, PyXA.apps.Finder.XAFinderClippingWindowList)
        self.assertIsInstance(clipping_windows, PyXA.apps.Finder.XAFinderWindowList)
        self.assertIsInstance(clipping_windows, PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(clipping_windows[0], PyXA.apps.Finder.XAFinderClippingWindow)
        self.assertIsInstance(clipping_windows[0].xa_elem, ScriptingBridge.SBObject)

    def test_finder_selection(self):
        self.app.selection = self.app.files()[0]
        self.assertEqual(len(self.app.selection), 1)

        pre_selection = self.app.selection

        self.app.selection = self.app.files()[0:10]

        self.assertNotEqual(len(self.app.selection), 1)
        print(pre_selection)
        print(self.app.selection)
        self.assertEqual(pre_selection == self.app.selection, False)

        file = self.app.files()[0]
        file.reveal()
        self.assertEqual(len(self.app.selection), 1)
        self.assertIn(file.url, self.app.selection.url())

if __name__ == '__main__':
    unittest.main()