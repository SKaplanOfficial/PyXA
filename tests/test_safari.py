import AppKit
import PyXA
import time
import unittest

class TestSafari(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Safari")

        self.windows = self.app.windows()
        self.docs = self.app.documents()
        self.tabs = self.app.front_window.tabs()

    def test_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)

    def test_safari_list_types(self):
        self.assertIsInstance(self.windows, PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(self.docs, PyXA.apps.Safari.XASafariDocumentList)
        self.assertIsInstance(self.tabs, PyXA.apps.Safari.XASafariTabList)

    def test_safari_object_types(self):
        self.assertIsInstance(self.windows[0], PyXA.apps.Safari.XASafariWindow)
        self.assertIsInstance(self.docs[0], PyXA.apps.Safari.XASafariGeneric)
        self.assertIsInstance(self.docs[0], PyXA.apps.Safari.XASafariDocument)
        self.assertIsInstance(self.tabs[0], PyXA.apps.Safari.XASafariGeneric)
        self.assertIsInstance(self.tabs[0], PyXA.apps.Safari.XASafariTab)

    def text_safari_doc_list_attribute_methods(self):
        l1 = self.docs.name()
        l2 = self.docs.modified()
        l3 = self.docs.source()
        l4 = self.docs.text()

        self.assertEqual(all(isinstance(x, list) for x in [l1, l2, l3, l4]), list)

        d1 = self.docs.by_name(l1[0])
        d2 = self.docs.by_modified(l2[0])
        d3 = self.docs.by_source(l3[0])
        d4 = self.docs.by_text(l4[0])

        self.assertEqual(all(isinstance(x, PyXA.apps.Safari.XASafariDocument) for x in [d1, d2, d3, d4]), list)

        self.assertIsInstance(l1[0], str)
        self.assertIsInstance(l2[0], bool)
        self.assertIsInstance(l3[0], str)
        self.assertIsInstance(l4[0], PyXA.XABase.XAText)

    def test_safari_doc_attribute_methods(self):
        doc = self.docs[0]
        a1 = doc.name
        a2 = doc.modified
        a3 = doc.source
        a4 = doc.text

        self.assertIsInstance(a1, str)
        self.assertIsInstance(a2, bool)
        self.assertIsInstance(a3, str)
        self.assertIsInstance(a4, PyXA.XABase.XAText)

    def test_safari_tab_list_attribute_methods(self):
        l1 = self.tabs.source()
        l2 = self.tabs.url()
        l3 = self.tabs.index()
        l4 = self.tabs.text()
        l5 = self.tabs.visible()
        l6 = self.tabs.name()

        self.assertEqual(all(isinstance(x, list) for x in [l1, l2, l3, l4, l5, l6]), True)

        d1 = self.tabs.by_source(l1[0])
        d2 = self.tabs.by_url(l2[0])
        d3 = self.tabs.by_index(l3[0])
        d4 = self.tabs.by_text(l4[0])
        d5 = self.tabs.by_visible(l5[0])
        d6 = self.tabs.by_name(l6[0])

        self.assertEqual(all(isinstance(x, PyXA.apps.Safari.XASafariTab) for x in [d1, d2, d3, d4, d5, d6]), True)

        self.assertIsInstance(l1[0], str)
        self.assertIsInstance(l2[0], PyXA.XABase.XAURL)
        self.assertIsInstance(l3[0], int)
        self.assertIsInstance(l4[0], PyXA.XABase.XAText)
        self.assertIsInstance(l5[0], bool)
        self.assertIsInstance(l6[0], str)

    def test_safari_tab_attribute_methods(self):
        tab = self.tabs[0]
        a1 = tab.source
        a2 = tab.url
        a3 = tab.index
        a4 = tab.text
        a5 = tab.visible
        a6 = tab.name

        self.assertIsInstance(a1, str)
        self.assertIsInstance(a2, PyXA.XABase.XAURL)
        self.assertIsInstance(a3, int)
        self.assertIsInstance(a4, PyXA.XABase.XAText)
        self.assertIsInstance(a5, bool)
        self.assertIsInstance(a6, str)

    def test_safari_clipboard_reps(self):
        c1 = self.app.front_window.get_clipboard_representation()
        c2 = self.app.documents().get_clipboard_representation()
        c3 = self.app.current_document.get_clipboard_representation()
        c4 = self.app.front_window.tabs().get_clipboard_representation()
        c5 = self.app.current_tab.get_clipboard_representation()

        self.assertIsInstance(c1, str)

        self.assertIsInstance(c2, list)
        self.assertIsInstance(c2[0], AppKit.NSURL)
        self.assertIsInstance(c3, AppKit.NSURL)

        self.assertIsInstance(c4, list)
        self.assertIsInstance(c4[0], AppKit.NSURL)
        self.assertIsInstance(c5, AppKit.NSURL)


if __name__ == '__main__':
    unittest.main()