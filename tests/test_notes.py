import PyXA
import unittest
import ScriptingBridge
import AppKit
from datetime import datetime

class TestNotes(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Notes")

    def test_notes_application_type(self):
        self.assertIsInstance(self.app, PyXA.XABaseScriptable.XASBApplication)
        self.assertIsInstance(self.app, PyXA.apps.Notes.XANotesApplication)

    def test_notes_attributes(self):
        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.default_account, PyXA.apps.Notes.XANotesAccount)
        self.assertIsInstance(self.app.name, str)

    def test_notes_lists(self):
        self.assertIsInstance(self.app.documents(), PyXA.apps.Notes.XANotesDocumentList)
        self.assertIsInstance(self.app.documents()[0], PyXA.apps.Notes.XANotesDocument)
        self.assertIsInstance(self.app.documents()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.notes(), PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(self.app.notes()[0], PyXA.apps.Notes.XANote)
        self.assertIsInstance(self.app.notes()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.folders(), PyXA.apps.Notes.XANotesFolderList)
        self.assertIsInstance(self.app.folders()[0], PyXA.apps.Notes.XANotesFolder)
        self.assertIsInstance(self.app.folders()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.accounts(), PyXA.apps.Notes.XANotesAccountList)
        self.assertIsInstance(self.app.accounts()[0], PyXA.apps.Notes.XANotesAccount)
        self.assertIsInstance(self.app.accounts()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.attachments(), PyXA.apps.Notes.XANotesAttachmentList)
        self.assertIsInstance(self.app.attachments()[0], PyXA.apps.Notes.XANoteAttachment)
        self.assertIsInstance(self.app.attachments()[0].xa_elem, ScriptingBridge.SBObject)

    def test_notes_selection(self):
        self.assertIsInstance(self.app.selection, PyXA.apps.Notes.XANoteList)
        self.app.selection = self.app.notes()[0:3]
        self.assertIsInstance(self.app.selection, PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(self.app.selection[0], PyXA.apps.Notes.XANote)
        self.assertIsInstance(self.app.selection[0].xa_elem, ScriptingBridge.SBObject)

    def test_notes_note_list(self):
        notes = self.app.notes()

        self.assertIsInstance(notes.name(), list)
        self.assertIsInstance(notes.name()[0], str)
        self.assertIsInstance(notes.by_name(notes.name()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.id(), list)
        self.assertIsInstance(notes.id()[0], str)
        self.assertIsInstance(notes.by_id(notes.id()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.plaintext(), list)
        self.assertIsInstance(notes.plaintext()[0], str)
        self.assertIsInstance(notes.by_plaintext(notes.plaintext()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.creation_date(), list)
        self.assertIsInstance(notes.creation_date()[0], AppKit.NSDate)
        self.assertIsInstance(notes.by_creation_date(notes.creation_date()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.modification_date(), list)
        self.assertIsInstance(notes.modification_date()[0], AppKit.NSDate)
        self.assertIsInstance(notes.by_modification_date(notes.modification_date()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.password_protected(), list)
        self.assertIsInstance(notes.password_protected()[0], bool)
        self.assertIsInstance(notes.by_password_protected(notes.password_protected()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.shared(), list)
        self.assertIsInstance(notes.shared()[0], bool)
        self.assertIsInstance(notes.by_shared(notes.shared()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.container(), PyXA.apps.Notes.XANotesFolderList)
        self.assertIsInstance(notes.container()[0], PyXA.apps.Notes.XANotesFolder)
        self.assertIsInstance(notes.by_container(notes.container()[0]), PyXA.apps.Notes.XANote)

        self.assertIsInstance(notes.attachments(), PyXA.apps.Notes.XANotesAttachmentList)
        self.assertIsInstance(notes.attachments()[0], PyXA.apps.Notes.XANoteAttachment)

    def test_notes_account_list(self):
        accounts = self.app.accounts()

        self.assertIsInstance(accounts.name(), list)
        self.assertIsInstance(accounts.name()[0], str)
        self.assertIsInstance(accounts.by_name(accounts.name()[0]), PyXA.apps.Notes.XANotesAccount)

        self.assertIsInstance(accounts.upgraded(), list)
        self.assertIsInstance(accounts.upgraded()[0], bool)
        self.assertIsInstance(accounts.by_upgraded(accounts.upgraded()[0]), PyXA.apps.Notes.XANotesAccount)

        self.assertIsInstance(accounts.id(), list)
        self.assertIsInstance(accounts.id()[0], str)
        self.assertIsInstance(accounts.by_id(accounts.id()[0]), PyXA.apps.Notes.XANotesAccount)

        self.assertIsInstance(accounts.default_folder(), PyXA.apps.Notes.XANotesFolderList)
        self.assertIsInstance(accounts.default_folder()[0], PyXA.apps.Notes.XANotesFolder)
        self.assertIsInstance(accounts.by_default_folder(accounts.default_folder()[0]), PyXA.apps.Notes.XANotesAccount)

        self.assertIsInstance(accounts.notes(), PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(accounts.notes()[0], PyXA.apps.Notes.XANote)

        self.assertIsInstance(accounts.folders(), PyXA.apps.Notes.XANotesFolderList)
        self.assertIsInstance(accounts.folders()[0], PyXA.apps.Notes.XANotesFolder)

    def test_notes_folder_list(self):
        folders = self.app.folders()

        self.assertIsInstance(folders.name(), list)
        self.assertIsInstance(folders.name()[0], str)
        self.assertIsInstance(folders.by_name(folders.name()[0]), PyXA.apps.Notes.XANotesFolder)

        self.assertIsInstance(folders.id(), list)
        self.assertIsInstance(folders.id()[0], str)
        self.assertIsInstance(folders.by_id(folders.id()[0]), PyXA.apps.Notes.XANotesFolder)

        self.assertIsInstance(folders.shared(), list)
        self.assertIsInstance(folders.shared()[0], bool)
        self.assertIsInstance(folders.by_shared(folders.shared()[0]), PyXA.apps.Notes.XANotesFolder)

        self.assertIsInstance(folders.container(), PyXA.apps.Notes.XANotesAccountList)
        self.assertIsInstance(folders.container()[0], PyXA.apps.Notes.XANotesAccount)
        self.assertIsInstance(folders.by_container(folders.container()[0]), PyXA.apps.Notes.XANotesFolder)

        self.assertIsInstance(folders.folders(), PyXA.apps.Notes.XANotesFolderList)
        self.assertIsInstance(folders.folders()[0], PyXA.apps.Notes.XANotesFolder)

        self.assertIsInstance(folders.notes(), PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(folders.notes()[0], PyXA.apps.Notes.XANote)
        
    def test_notes_attachment_list(self):
        attachments = self.app.attachments()

        self.assertIsInstance(attachments.name(), list)
        self.assertIsInstance(attachments.name()[0], str)
        self.assertIsInstance(attachments.by_name(attachments.name()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.id(), list)
        self.assertIsInstance(attachments.id()[0], str)
        self.assertIsInstance(attachments.by_id(attachments.id()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.content_identifier(), list)
        self.assertIsInstance(attachments.content_identifier()[0], str)
        self.assertIsInstance(attachments.by_content_identifier(attachments.content_identifier()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.creation_date(), list)
        self.assertIsInstance(attachments.creation_date()[0], AppKit.NSDate)
        self.assertIsInstance(attachments.by_creation_date(attachments.creation_date()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.modification_date(), list)
        self.assertIsInstance(attachments.modification_date()[0], AppKit.NSDate)
        self.assertIsInstance(attachments.by_modification_date(attachments.modification_date()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.url(), list)
        self.assertIsInstance(attachments.url()[0], PyXA.XABase.XAURL)
        self.assertIsInstance(attachments.by_url(attachments.url()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.shared(), list)
        self.assertIsInstance(attachments.shared()[0], bool)
        self.assertIsInstance(attachments.by_shared(attachments.shared()[0]), PyXA.apps.Notes.XANoteAttachment)

        self.assertIsInstance(attachments.container(), PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(attachments.container()[0], PyXA.apps.Notes.XANote)
        self.assertIsInstance(attachments.by_container(attachments.container()[0]), PyXA.apps.Notes.XANoteAttachment)

    def test_notes_note(self):
        note = self.app.notes()[0]

        self.assertIsInstance(note.name, str)
        self.assertIsInstance(note.id, str)
        self.assertIsInstance(note.body, str)
        self.assertIsInstance(note.plaintext, str)
        self.assertIsInstance(note.creation_date, AppKit.NSDate)
        self.assertIsInstance(note.modification_date, AppKit.NSDate)
        self.assertIsInstance(note.password_protected, bool)
        self.assertIsInstance(note.shared, bool)
        self.assertIsInstance(note.container, PyXA.apps.Notes.XANotesFolder)
        self.assertIsInstance(note.attachments(), PyXA.apps.Notes.XANotesAttachmentList)

    def test_notes_account(self):
        account = self.app.accounts()[0]

        self.assertIsInstance(account.name, str)
        self.assertIsInstance(account.upgraded, bool)
        self.assertIsInstance(account.id, str)
        self.assertIsInstance(account.default_folder, PyXA.apps.Notes.XANotesFolder)
        self.assertIsInstance(account.notes(), PyXA.apps.Notes.XANoteList)
        self.assertIsInstance(account.folders(), PyXA.apps.Notes.XANotesFolderList)

    def test_notes_folder(self):
        folder = self.app.folders()[0]

        self.assertIsInstance(folder.name, str)
        self.assertIsInstance(folder.id, str)
        self.assertIsInstance(folder.shared, bool)
        self.assertIsInstance(folder.container, PyXA.apps.Notes.XANotesAccount)
        self.assertIsInstance(folder.notes(), PyXA.apps.Notes.XANoteList)

    def test_notes_attachment(self):
        attachment = self.app.attachments()[0]

        self.assertIsInstance(attachment.name, str)
        self.assertIsInstance(attachment.id, str)
        self.assertIsInstance(attachment.content_identifier, str)
        self.assertIsInstance(attachment.creation_date, AppKit.NSDate)
        self.assertIsInstance(attachment.modification_date, AppKit.NSDate)
        self.assertTrue(isinstance(attachment.url, PyXA.XABase.XAURL) or attachment.url is None)
        self.assertIsInstance(attachment.shared, bool)
        self.assertIsInstance(attachment.container, PyXA.apps.Notes.XANote)
