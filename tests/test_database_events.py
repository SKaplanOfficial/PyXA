from datetime import datetime, timedelta
from time import sleep

import AppKit
import PyXA
import unittest
import ScriptingBridge

from PyXA.XABase import XAColor, XALocation, XAURL, XAPath
from PyXA.XABaseScriptable import XASBApplication
from PyXA.apps.DatabaseEvents import XADatabaseEventsApplication, XADatabaseEventsDatabaseList, XADatabaseEventsDatabase, XADatabaseEventsRecordList, XADatabaseEventsRecord, XADatabaseEventsFieldList, XADatabaseEventsField

class TestDatabaseEvents(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Database Events")

    def test_database_events_application(self):
        self.assertIsInstance(self.app, XASBApplication)
        self.assertIsInstance(self.app, XADatabaseEventsApplication)

        self.assertIsInstance(self.app.quit_delay, int)
        self.assertIsInstance(self.app.databases(), XADatabaseEventsDatabaseList)
        self.assertIsInstance(self.app.databases()[0], XADatabaseEventsDatabase)
        self.assertIsInstance(self.app.databases()[0].xa_elem, ScriptingBridge.SBObject)

    def test_database_events_database(self):
        dbs = self.app.databases()

        self.assertIsInstance(dbs.location(), list)
        self.assertIsInstance(dbs.location()[0], XAPath)

        self.assertIsInstance(dbs.name(), list)
        self.assertIsInstance(dbs.name()[0], str)

        self.assertIsInstance(dbs.store_type(), list)
        self.assertIsInstance(dbs.store_type()[0], XADatabaseEventsApplication.StoreType)

    def test_database_events_record(self):
        pass

    def test_database_events_field(self):
        pass