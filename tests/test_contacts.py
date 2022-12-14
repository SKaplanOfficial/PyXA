import PyXA
import unittest
import AppKit
import ScriptingBridge

class TestContacts(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Contacts")

    def test_iwork_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.app, PyXA.apps.Contacts.XAContactsApplication)

    def test_contacts_attrs_and_methods(self):
        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.my_card, PyXA.apps.Contacts.XAContactsPerson)
        self.assertIsInstance(self.app.unsaved, bool)
        self.assertIsInstance(self.app.selection, PyXA.apps.Contacts.XAContactsPersonList)
        self.assertIsInstance(self.app.default_country_code, str)

        self.assertIsInstance(self.app.my_card.xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.selection.xa_elem, AppKit.NSArray)

    def test_contacts_lists(self):
        groups = self.app.groups()
        people = self.app.people()

        self.assertIsInstance(groups, PyXA.apps.Contacts.XAContactsGroupList)
        self.assertIsInstance(groups[0], PyXA.apps.Contacts.XAContactsGroup)
        self.assertIsInstance(groups[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(groups.name(), list)
        if len(groups.name()) > 0:
            self.assertIsInstance(groups.name()[0], str)

        self.assertIsInstance(people, PyXA.apps.Contacts.XAContactsPersonList)
        self.assertIsInstance(people[0], PyXA.apps.Contacts.XAContactsPerson)
        self.assertIsInstance(people[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(people.name(), list)
        if len(people.name()) > 0:
            self.assertIsInstance(people.name()[0], str)



if __name__ == '__main__':
    unittest.main()