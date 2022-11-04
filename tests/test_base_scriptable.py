import AppKit
import PyXA
import time
import unittest

class TestMessages(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Messages")
        self.app.activate()

        start = time.time()
        success = False
        while time.time() - start < 5:
            if self.app.frontmost:
                success = True
                break
            time.sleep(0.1)

        if not success:
            raise TimeoutError

    def test_scriptable_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)

    def test_scriptable_types(self):
        self.assertIsInstance(self.app.windows(), PyXA.XABaseScriptable.XASBWindowList)

        self.assertIsInstance(self.app.windows()[0], PyXA.apps.Messages.XAMessagesWindow)

    def test_scriptable_windowlist_attributes_and_methods(self):
        windows = self.app.windows()
        win = windows[0]

        # XASBWindowList methods & content
        self.assertIsInstance(windows.name(), list)
        self.assertIsInstance(windows.id(), list)
        self.assertIsInstance(windows.index(), list)
        self.assertIsInstance(windows.bounds(), list)
        self.assertIsInstance(windows.closeable(), list)
        self.assertIsInstance(windows.resizable(), list)
        self.assertIsInstance(windows.visible(), list)
        self.assertIsInstance(windows.zoomable(), list)
        self.assertIsInstance(windows.zoomed(), list)

        self.assertEqual(windows.by_name(windows.name()[0]), win)
        self.assertEqual(windows.by_id(windows.id()[0]), win)
        self.assertEqual(windows.by_index(windows.index()[0]), win)
        self.assertEqual(windows.by_bounds(windows.bounds()[0]), win)
        self.assertEqual(windows.by_closeable(windows.closeable()[0]), win)
        self.assertEqual(windows.by_resizable(windows.resizable()[0]), win)
        self.assertEqual(windows.by_visible(windows.visible()[0]), win)
        self.assertEqual(windows.by_zoomable(windows.zoomable()[0]), win)
        self.assertEqual(windows.by_zoomed(windows.zoomed()[0]), win)

        windows.collapse()
        self.assertEqual(all([win.miniaturized for win in windows]), True)

        windows.uncollapse()
        self.assertEqual(any([win.miniaturized for win in windows]), False)

    def test_scriptable_window_attributes_and_methods(self):
        windows = self.app.windows()
        win = windows[0]
        win2 = self.app.front_window
        win3 = windows.by_name(win.name)

        self.assertEqual(win, win2)
        self.assertEqual(win, win3)

        self.assertIsInstance(win.name, str)
        self.assertIsInstance(win.id, int)
        self.assertIsInstance(win.index, int)
        self.assertIsInstance(win.bounds, tuple)
        self.assertIsInstance(win.closeable, bool)
        self.assertIsInstance(win.resizable, bool)
        self.assertIsInstance(win.visible, bool)
        self.assertIsInstance(win.zoomable, bool)
        self.assertIsInstance(win.zoomed, bool)

        win.collapse()
        if hasattr(win, "miniaturized"):
            self.assertEqual(win.miniaturized, True)
        elif hasattr(win, "minimized"):
            self.assertEqual(win.minimized, True)
        elif hasattr(win, "collapsed"):
            self.assertEqual(win.collapsed, True)

        win.uncollapse()
        if hasattr(win, "miniaturized"):
            self.assertEqual(win.miniaturized, False)
        elif hasattr(win, "minimized"):
            self.assertEqual(win.minimized, False)
        elif hasattr(win, "collapsed"):
            self.assertEqual(win.collapsed, False)

        win.bounds = (100, 100, 1024, 768)
        self.assertEqual(win.bounds, (100, 100, 1024, 768))

        win.visible = False
        self.assertEqual(win.visible, False)

        win.visible = True
        self.assertEqual(win.visible, True)

        win.zoomed = True
        self.assertEqual(win.zoomed, True)

        win.zoomed = False
        self.assertEqual(win.zoomed, False)

if __name__ == '__main__':
    unittest.main()