import PyXA
import unittest
import ScriptingBridge
import AppKit
from datetime import datetime

class TestReminders(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Reminders")

    def test_reminders_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.app, PyXA.apps.Reminders.XARemindersApplication)

    def test_reminders_attributes(self):
        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.default_account, PyXA.apps.Reminders.XARemindersAccount)
        self.assertIsInstance(self.app.default_list, PyXA.apps.Reminders.XARemindersList)

    def test_reminders_lists(self):
        self.assertIsInstance(self.app.documents(), PyXA.apps.Reminders.XARemindersDocumentList)
        self.assertIsInstance(self.app.documents()[0], PyXA.apps.Reminders.XARemindersDocument)
        self.assertIsInstance(self.app.documents()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.accounts(), PyXA.apps.Reminders.XARemindersAccountList)
        self.assertIsInstance(self.app.accounts()[0], PyXA.apps.Reminders.XARemindersAccount)
        self.assertIsInstance(self.app.accounts()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.lists(), PyXA.apps.Reminders.XARemindersListList)
        self.assertIsInstance(self.app.lists()[0], PyXA.apps.Reminders.XARemindersList)
        self.assertIsInstance(self.app.lists()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.reminders(), PyXA.apps.Reminders.XARemindersReminderList)
        self.assertIsInstance(self.app.reminders()[0], PyXA.apps.Reminders.XARemindersReminder)
        self.assertIsInstance(self.app.reminders()[0].xa_elem, ScriptingBridge.SBObject)

    # def test_new_list(self):
    #     len_before = len(self.app.lists())
    #     new_list = self.app.new_list("Test")
    #     self.assertEqual(len(self.app.lists()), len_before + 1)
    #     new_list.delete()
    #     self.assertEqual(len(self.app.lists()), len_before)

    # def test_new_reminder(self):
    #     len_before = len(self.app.reminders())
    #     new_reminder = self.app.new_reminder("Test")
    #     self.assertEqual(len(self.app.reminders()), len_before + 1)
    #     new_reminder.delete()
    #     self.assertEqual(len(self.app.reminders()), len_before)

    def test_reminders_accounts(self):
        accounts = self.app.accounts()

        self.assertIsInstance(accounts.properties(), list)
        self.assertIsInstance(accounts.properties()[0], dict)
        self.assertIsInstance(accounts.by_properties(accounts.properties()[0]), PyXA.apps.Reminders.XARemindersAccount)

        self.assertIsInstance(accounts.id(), list)
        self.assertIsInstance(accounts.id()[0], str)
        self.assertIsInstance(accounts.by_id(accounts.id()[0]), PyXA.apps.Reminders.XARemindersAccount)

        self.assertIsInstance(accounts.name(), list)
        self.assertIsInstance(accounts.name()[0], str)
        self.assertIsInstance(accounts.by_name(accounts.name()[0]), PyXA.apps.Reminders.XARemindersAccount)

        account = accounts[0]

        self.assertIsInstance(account.properties, dict)
        self.assertIsInstance(account.id, str)
        self.assertIsInstance(account.name, str)

    def test_reminders_lists_list(self):
        lists = self.app.lists()

        self.assertIsInstance(lists.properties(), list)
        self.assertIsInstance(lists.properties()[0], dict)
        self.assertIsInstance(lists.by_properties(lists.properties()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.id(), list)
        self.assertIsInstance(lists.id()[0], str)
        self.assertIsInstance(lists.by_id(lists.id()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.name(), list)
        self.assertIsInstance(lists.name()[0], str)
        self.assertIsInstance(lists.by_name(lists.name()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.container(), PyXA.apps.Reminders.XARemindersAccountList)
        self.assertIsInstance(lists.container()[0], PyXA.apps.Reminders.XARemindersAccount)
        self.assertIsInstance(lists.by_container(lists.container()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.color(), list)
        self.assertIsInstance(lists.color()[0], str)
        self.assertIsInstance(lists.by_color(lists.color()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.emblem(), list)
        self.assertIsInstance(lists.emblem()[0], str)
        self.assertIsInstance(lists.by_emblem(lists.emblem()[0]), PyXA.apps.Reminders.XARemindersList)

        self.assertIsInstance(lists.reminders(), PyXA.apps.Reminders.XARemindersReminderList)
        self.assertIsInstance(lists.reminders()[0], PyXA.apps.Reminders.XARemindersReminder)

        ls = lists[0]

        self.assertIsInstance(ls.properties, dict)
        self.assertIsInstance(ls.id, str)
        self.assertIsInstance(ls.name, str)
        self.assertIsInstance(ls.container, PyXA.apps.Reminders.XARemindersAccount)
        self.assertIsInstance(ls.color, str)
        self.assertIsInstance(ls.emblem, str)
        self.assertIsInstance(ls.reminders(), PyXA.apps.Reminders.XARemindersReminderList)

    def test_reminders_reminder_list(self):
        reminders = self.app.reminders()

        self.assertIsInstance(reminders.properties(), list)
        self.assertIsInstance(reminders.properties()[0], dict)
        self.assertIsInstance(reminders.by_properties(reminders.properties()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.name(), list)
        self.assertIsInstance(reminders.name()[0], str)
        self.assertIsInstance(reminders.by_name(reminders.name()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.id(), list)
        self.assertIsInstance(reminders.id()[0], str)
        self.assertIsInstance(reminders.by_id(reminders.id()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.container(), PyXA.apps.Reminders.XARemindersListList)
        self.assertIsInstance(reminders.container()[0], PyXA.apps.Reminders.XARemindersList)
        self.assertIsInstance(reminders.by_container(reminders.container()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.creation_date(), list)
        self.assertIsInstance(reminders.creation_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_creation_date(reminders.creation_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.modification_date(), list)
        self.assertIsInstance(reminders.modification_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_modification_date(reminders.modification_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.body(), list)
        self.assertIsInstance(reminders.body()[0], str)
        self.assertIsInstance(reminders.by_body(reminders.body()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.completed(), list)
        self.assertIsInstance(reminders.completed()[0], bool)
        self.assertIsInstance(reminders.by_completed(reminders.completed()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.completion_date(), list)
        self.assertIsInstance(reminders.completion_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_completion_date(reminders.completion_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.due_date(), list)
        self.assertIsInstance(reminders.due_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_due_date(reminders.due_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.allday_due_date(), list)
        self.assertIsInstance(reminders.allday_due_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_allday_due_date(reminders.allday_due_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.remind_me_date(), list)
        self.assertIsInstance(reminders.remind_me_date()[0], AppKit.NSDate)
        self.assertIsInstance(reminders.by_remind_me_date(reminders.remind_me_date()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.priority(), list)
        self.assertIsInstance(reminders.priority()[0], int)
        self.assertIsInstance(reminders.by_priority(reminders.priority()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.flagged(), list)
        self.assertIsInstance(reminders.flagged()[0], bool)
        self.assertIsInstance(reminders.by_flagged(reminders.flagged()[0]), PyXA.apps.Reminders.XARemindersReminder)

        self.assertIsInstance(reminders.alarms(), list)
        self.assertIsInstance(reminders.alarms()[0], PyXA.apps.Reminders.XARemindersAlarmList)

        reminder = reminders[0]

        self.assertIsInstance(reminder.properties, dict)
        self.assertIsInstance(reminder.name, str)
        self.assertIsInstance(reminder.id, str)
        self.assertIsInstance(reminder.container, PyXA.apps.Reminders.XARemindersList)
        self.assertIsInstance(reminder.creation_date, AppKit.NSDate)
        self.assertIsInstance(reminder.modification_date, AppKit.NSDate)
        self.assertIsInstance(reminder.body, str)
        self.assertIsInstance(reminder.completed, bool)
        # self.assertIsInstance(reminder.completion_date, AppKit.NSDate)
        # self.assertIsInstance(reminder.due_date, AppKit.NSDate)
        # self.assertIsInstance(reminder.allday_due_date, AppKit.NSDate)
        # self.assertIsInstance(reminder.remind_me_date, AppKit.NSDate)
        self.assertIsInstance(reminder.priority, int)
        self.assertIsInstance(reminder.flagged, bool)
        self.assertIsInstance(reminder.alarms(), PyXA.apps.Reminders.XARemindersAlarmList)