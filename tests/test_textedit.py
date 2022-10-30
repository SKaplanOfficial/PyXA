import AppKit
import PyXA
import time
import os
import unittest

class TestTextEdit(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("TextEdit")

    def test_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)

    def test_textedit_app_attributes(self):
        self.app.activate()
        timeout = 0
        while timeout < 10:
            time.sleep(0.1)
            if self.app.frontmost:
                break
            timeout += 1
            if timeout == 10:
                self.fail("TextEdit did not become active")

        self.assertEqual(self.app.name, "TextEdit")
        self.assertEqual(self.app.version, "1.17")

    def test_textedit_make_documents(self):
        new_doc = self.app.make("document", {"text": "This is a test!"})
        doc1 = self.app.documents().push(new_doc)

        doc2 = self.app.new_document("Example.txt", "Hello, world!")

        self.assertIsInstance(doc1, PyXA.apps.TextEdit.XATextEditDocument)
        self.assertIsInstance(doc2, PyXA.apps.TextEdit.XATextEditDocument)
        self.assertIsInstance(doc1.text, PyXA.XABase.XAText)
        self.assertIsInstance(doc2.text, PyXA.XABase.XAText)
        self.assertEqual(str(doc1.text), "Hello, world!")
        self.assertEqual(str(doc2.text), "This is a test!")

        doc1.append("1 2 3")
        doc2.prepend("a b c")

        self.assertEqual(str(doc1.text), "Hello, world!1 2 3")
        self.assertEqual(str(doc2.text), "a b cThis is a test!")

    def test_textedit_window_methods(self):
        self.app.front_window.miniaturized = True
        self.assertEqual(self.app.front_window.miniaturized, True)

        time.sleep(0.5)
        self.app.front_window.miniaturized = False
        self.assertEqual(self.app.front_window.miniaturized, False)

    def test_textedit_list_types(self):
        self.assertIsInstance(self.app.windows(), PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(self.app.documents(), PyXA.apps.TextEdit.XATextEditDocumentList)

    def test_textedit_object_types(self):
        self.assertIsInstance(self.app.windows()[0], PyXA.apps.TextEdit.XATextEditWindow)
        self.assertIsInstance(self.app.documents()[0], PyXA.apps.TextEdit.XATextEditDocument)
        self.assertIsInstance(self.app.front_window, PyXA.apps.TextEdit.XATextEditWindow)
        self.assertIsInstance(self.app.front_window.document, PyXA.apps.TextEdit.XATextEditDocument)

    def test_textedit_doc_list_attribute_methods(self):
        docs = self.app.documents()
        l1 = docs.properties()
        l2 = docs.path()
        l3 = docs.name()
        l4 = docs.modified()

        self.assertEqual(all(isinstance(x, list) for x in [l1, l2, l3, l4]), True)

        d1 = docs.by_properties(l1[0])
        d2 = docs.by_path(l2[0])
        d3 = docs.by_name(l3[0])
        d4 = docs.by_modified(l4[0])

        self.assertEqual(all(isinstance(x, PyXA.apps.TextEdit.XATextEditDocument) for x in [d1, d2, d3, d4]), True)

        self.assertIsInstance(l1[0], dict)
        self.assertIsInstance(l2[0], PyXA.XABase.XAPath)
        self.assertIsInstance(l3[0], str)
        self.assertIsInstance(l4[0], bool)

if __name__ == '__main__':
    unittest.main()