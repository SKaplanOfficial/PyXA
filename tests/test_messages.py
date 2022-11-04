import PyXA
import time
import unittest

from datetime import datetime, date
from pprint import pprint

import AppKit

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

    def test_messages_application_type(self):
        self.assertIsInstance(self.app, PyXA.apps.Messages.XAMessagesApplication)

    def test_messages_list_types(self):
        self.assertIsInstance(self.app.documents(), PyXA.apps.Messages.XAMessagesDocumentList)
        self.assertIsInstance(self.app.chats(), PyXA.apps.Messages.XAMessagesChatList)
        self.assertIsInstance(self.app.participants(), PyXA.apps.Messages.XAMessagesParticipantList)
        self.assertIsInstance(self.app.accounts(), PyXA.apps.Messages.XAMessagesAccountList)
        self.assertIsInstance(self.app.file_transfers(), PyXA.apps.Messages.XAMessagesFileTransferList)

    def test_messages_object_types(self):
        self.assertIsInstance(self.app.windows()[0], PyXA.apps.Messages.XAMessagesWindow)
        self.assertIsInstance(self.app.documents()[0], PyXA.apps.Messages.XAMessagesDocument)
        self.assertIsInstance(self.app.chats()[0], PyXA.apps.Messages.XAMessagesChat)
        self.assertIsInstance(self.app.participants()[0], PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(self.app.accounts()[0], PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(self.app.file_transfers()[0], PyXA.apps.Messages.XAMessagesFileTransfer)

    def test_messages_window_attributes_and_methods(self):
        win = self.app.front_window
        self.assertIsInstance(win.miniaturizable, bool)
        self.assertIsInstance(win.miniaturized, bool)
        self.assertIsInstance(win.document, PyXA.apps.Messages.XAMessagesDocument)

    def test_messages_chats(self):
        chats = self.app.chats()

        self.assertIsInstance(chats.id(), list)
        self.assertIsInstance(chats.name(), list)
        self.assertIsInstance(chats.account(), PyXA.apps.Messages.XAMessagesAccountList)
        self.assertIsInstance(chats.participants(), list)

        self.assertIsInstance(chats.id()[0], str)
        self.assertIsInstance(chats.name()[0], str)
        self.assertIsInstance(chats.account()[0], PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(chats.participants()[0], PyXA.apps.Messages.XAMessagesParticipantList)

        self.assertIsInstance(chats.by_id(chats.id()[0]), PyXA.apps.Messages.XAMessagesChat)
        self.assertIsInstance(chats.by_name(chats.name()[0]), PyXA.apps.Messages.XAMessagesChat)
        self.assertIsInstance(chats.by_account(chats.account()[0]), PyXA.apps.Messages.XAMessagesChat)
        self.assertIsInstance(chats.by_participants(chats.participants()[0]), PyXA.apps.Messages.XAMessagesChat)

        chat = chats[0]
        self.assertIsInstance(chat.id, str)
        self.assertIsInstance(chat.name, str)
        self.assertIsInstance(chat.account, PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(chat.participants(), PyXA.apps.Messages.XAMessagesParticipantList)

    def test_messages_file_transfers(self):
        file_transfers = self.app.file_transfers()

        self.assertIsInstance(file_transfers.id(), list)
        self.assertIsInstance(file_transfers.name(), list)
        self.assertIsInstance(file_transfers.file_path(), list)
        self.assertIsInstance(file_transfers.direction(), list)
        self.assertIsInstance(file_transfers.account(), PyXA.apps.Messages.XAMessagesAccountList)
        self.assertIsInstance(file_transfers.participant(), PyXA.apps.Messages.XAMessagesParticipantList)
        self.assertIsInstance(file_transfers.file_size(), list)
        self.assertIsInstance(file_transfers.file_progress(), list)
        self.assertIsInstance(file_transfers.transfer_status(), list)
        self.assertIsInstance(file_transfers.started(), list)

        self.assertIsInstance(file_transfers.id()[0], str)
        self.assertIsInstance(file_transfers.name()[0], str)
        self.assertIsInstance(file_transfers.file_path()[0], PyXA.XABase.XAPath)
        self.assertIsInstance(file_transfers.direction()[0], PyXA.apps.Messages.XAMessagesApplication.MessageDirection)
        self.assertIsInstance(file_transfers.account()[0], PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(file_transfers.participant()[0], PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(file_transfers.file_size()[0], int)
        self.assertIsInstance(file_transfers.file_progress()[0], int)
        self.assertIsInstance(file_transfers.transfer_status()[0], PyXA.apps.Messages.XAMessagesApplication.TransferStatus)
        self.assertIsInstance(file_transfers.started()[0], AppKit.NSDate)

        self.assertIsInstance(file_transfers.by_id(file_transfers.id()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_name(file_transfers.name()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_file_path(file_transfers.file_path()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_direction(file_transfers.direction()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        #self.assertIsInstance(file_transfers.by_account(file_transfers.account()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        #self.assertIsInstance(file_transfers.by_participant(file_transfers.participant()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_file_size(file_transfers.file_size()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_file_progress(file_transfers.file_progress()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_transfer_status(file_transfers.transfer_status()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)
        self.assertIsInstance(file_transfers.by_started(file_transfers.started()[0]), PyXA.apps.Messages.XAMessagesFileTransfer)

        file_transfer = file_transfers[0]
        self.assertIsInstance(file_transfer.id, str)
        self.assertIsInstance(file_transfer.name, str)
        self.assertIsInstance(file_transfer.direction, PyXA.apps.Messages.XAMessagesApplication.MessageDirection)
        self.assertIsInstance(file_transfer.account, PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(file_transfer.participant, PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(file_transfer.file_size, int)
        self.assertIsInstance(file_transfer.file_progress, int)
        self.assertIsInstance(file_transfer.transfer_status, PyXA.apps.Messages.XAMessagesApplication.TransferStatus)
        self.assertIsInstance(file_transfer.started, AppKit.NSDate)

    def test_messages_participants(self):
        participants = self.app.participants()

        self.assertIsInstance(participants.id(), list)
        self.assertIsInstance(participants.account(), PyXA.apps.Messages.XAMessagesAccountList)
        self.assertIsInstance(participants.name(), list)
        self.assertIsInstance(participants.handle(), list)
        self.assertIsInstance(participants.first_name(), list)
        self.assertIsInstance(participants.last_name(), list)
        self.assertIsInstance(participants.full_name(), list)

        self.assertIsInstance(participants.id()[0], str)
        self.assertIsInstance(participants.account()[0], PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(participants.name()[0], str)
        self.assertIsInstance(participants.handle()[0], str)
        self.assertIsInstance(participants.first_name()[0], str)
        self.assertIsInstance(participants.last_name()[0], str)
        self.assertIsInstance(participants.full_name()[0], str)

        self.assertIsInstance(participants.by_id(participants.id()[0]), PyXA.apps.Messages.XAMessagesParticipant)

        self.assertIsInstance(participants.by_account(participants.account()[0]), PyXA.apps.Messages.XAMessagesParticipant)

        self.assertIsInstance(participants.by_name(participants.name()[0]), PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(participants.by_handle(participants.handle()[0]), PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(participants.by_first_name(participants.first_name()[0]), PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(participants.by_last_name(participants.last_name()[0]), PyXA.apps.Messages.XAMessagesParticipant)
        self.assertIsInstance(participants.by_full_name(participants.full_name()[0]), PyXA.apps.Messages.XAMessagesParticipant)

        participant = participants[0]
        self.assertIsInstance(participant.id, str)
        self.assertIsInstance(participant.account, PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(participant.name, str)
        self.assertIsInstance(participant.handle, str)
        self.assertIsInstance(participant.first_name, str)
        self.assertIsInstance(participant.last_name, str)
        self.assertIsInstance(participant.full_name, str)

    def test_messages_accounts(self):
        accounts = self.app.accounts()

        self.assertIsInstance(accounts.id(), list)
        self.assertIsInstance(accounts.object_description(), list)
        self.assertIsInstance(accounts.enabled(), list)
        self.assertIsInstance(accounts.connection_status(), list)
        self.assertIsInstance(accounts.service_type(), list)

        self.assertIsInstance(accounts.id()[0], str)
        self.assertIsInstance(accounts.object_description()[0], str)
        self.assertIsInstance(accounts.enabled()[0], bool)
        self.assertIsInstance(accounts.connection_status()[0], PyXA.apps.Messages.XAMessagesApplication.ConnectionStatus)
        self.assertIsInstance(accounts.service_type()[0], PyXA.apps.Messages.XAMessagesApplication.ServiceType)

        self.assertIsInstance(accounts.by_id(accounts.id()[0]), PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(accounts.by_object_description(accounts.object_description()[0]), PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(accounts.by_enabled(accounts.enabled()[0]), PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(accounts.by_connection_status(accounts.connection_status()[0]), PyXA.apps.Messages.XAMessagesAccount)
        self.assertIsInstance(accounts.by_service_type(accounts.service_type()[0]), PyXA.apps.Messages.XAMessagesAccount)

        account = accounts[0]
        self.assertIsInstance(account.id, str)
        self.assertIsInstance(account.object_description, str)
        self.assertIsInstance(account.enabled, bool)
        self.assertIsInstance(account.connection_status, PyXA.apps.Messages.XAMessagesApplication.ConnectionStatus)
        self.assertIsInstance(account.service_type, PyXA.apps.Messages.XAMessagesApplication.ServiceType)

if __name__ == '__main__':
    unittest.main()