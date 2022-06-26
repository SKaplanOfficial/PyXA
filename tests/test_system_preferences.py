import unittest
import PyXA

class TestSystemPreferences(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.application("System Preferences")
        self.panes = self.app.panes()

    def test_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)

    def test_panes_type(self):
        self.assertIsInstance(self.panes, PyXA.XABase.XAList)

    def test_pane_type(self):
        self.assertIsInstance(self.panes[0], PyXA.apps.SystemPreferences.XAPreferencePane)

    def test_panes_name(self):
        names = self.panes.name()
        self.assertIsInstance(names, list)
        self.assertIsInstance(names[0], str)

    def test_pane_eq(self):
        pane1 = self.app.panes({"name": "Battery"})[0]
        pane2 = self.panes.by_name("Battery")
        self.assertEqual(pane1, pane2)

    def test_anchors_type(self):
        pane = self.panes[0]
        self.assertIsInstance(pane.anchors(), PyXA.XABase.XAList)

    def test_anchor_type(self):
        pane = self.panes[0]
        anchor = pane.anchors()[0]
        self.assertIsInstance(anchor, PyXA.apps.SystemPreferences.XAPreferenceAnchor)

    def test_anchors_name(self):
        pane = self.panes[0]
        names = pane.anchors().name()
        self.assertIsInstance(names, list)
        self.assertIsInstance(names[0], str)


if __name__ == '__main__':
    unittest.main()