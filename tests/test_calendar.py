from datetime import datetime, timedelta
from time import sleep

import AppKit
import PyXA
import unittest
import ScriptingBridge

from PyXA.XABase import XAColor, XALocation, XAURL, XAPath
from PyXA.XABaseScriptable import XASBApplication
from PyXA.apps.Calendar import XACalendarApplication, XACalendarCalendar, XACalendarDocumentList, XACalendarDocument, XACalendarCalendarList, XACalendarEventList, XACalendarEvent, XACalendarAttendeeList, XACalendarAttachmentList, XACalendarAttachment

class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Calendar")

    def test_calendar_application_type(self):
        self.assertIsInstance(self.app, XASBApplication)
        self.assertIsInstance(self.app, XACalendarApplication)

    def test_calendar_application_attributes(self):
        self.assertIsInstance(self.app.properties, dict)
        self.assertIsInstance(self.app.name, str)
        self.assertIsInstance(self.app.frontmost, bool)
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.default_calendar, XACalendarCalendar)

    def test_calendar_application_lists(self):
        self.assertIsInstance(self.app.documents(), XACalendarDocumentList)
        self.assertIsInstance(self.app.documents()[0], XACalendarDocument)
        self.assertIsInstance(self.app.documents()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.calendars(), XACalendarCalendarList)
        self.assertIsInstance(self.app.calendars()[0], XACalendarCalendar)
        self.assertIsInstance(self.app.calendars()[0].xa_elem, ScriptingBridge.SBObject)

    def test_calendar_application_methods(self):
        num_cals_before = len(self.app.calendars())
        new_calendar = self.app.new_calendar("Test")
        self.assertNotEqual(num_cals_before, len(self.app.calendars()))
        new_calendar.delete()
        self.assertEqual(num_cals_before, len(self.app.calendars()))

        num_events_before = len(self.app.default_calendar.events())
        new_event = self.app.new_event("Test", datetime.now(), datetime.now() + timedelta(hours=1))
        self.assertNotEqual(num_events_before, len(self.app.default_calendar.events()))
        new_event.delete()
        self.assertEqual(num_events_before, len(self.app.default_calendar.events()))

    def test_calendar_calendars(self):
        calendars = self.app.calendars()

        self.assertIsInstance(calendars.properties(), list)
        self.assertIsInstance(calendars.properties()[0], dict)
        self.assertIsInstance(calendars.by_properties(calendars.properties()[0]), XACalendarCalendar)

        self.assertIsInstance(calendars.name(), list)
        self.assertIsInstance(calendars.name()[0], str)
        self.assertIsInstance(calendars.by_name(calendars.name()[0]), XACalendarCalendar)

        self.assertIsInstance(calendars.color(), list)
        self.assertIsInstance(calendars.color()[0], XAColor)
        self.assertIsInstance(calendars.by_color(calendars.color()[0]), XACalendarCalendar)

        self.assertIsInstance(calendars.writable(), list)
        self.assertIsInstance(calendars.writable()[0], bool)
        self.assertIsInstance(calendars.by_writable(calendars.writable()[0]), XACalendarCalendar)

        self.assertIsInstance(calendars.description(), list)
        self.assertIsInstance(calendars.description()[0], str)
        self.assertIsInstance(calendars.by_description(calendars.description()[0]), XACalendarCalendar)

        self.assertIsInstance(calendars.events(), XACalendarEventList)
        self.assertIsInstance(calendars.events()[0], XACalendarEvent)

        calendar = calendars[0]

        self.assertIsInstance(calendar.properties, dict)
        self.assertIsInstance(calendar.name, str)
        self.assertIsInstance(calendar.color, XAColor)
        self.assertIsInstance(calendar.writable, bool)
        self.assertIsInstance(calendar.description, str)

    def test_calendar_events(self):
        events = self.app.default_calendar.events()

        self.assertIsInstance(events, XACalendarEventList)
        self.assertIsInstance(events[0], XACalendarEvent)

        props = events.properties()
        self.assertIsInstance(props, list)
        self.assertIsInstance(props[0], dict)
        self.assertIsInstance(events.by_properties(next(props)), XACalendarEvent)

        self.assertIsInstance(events.description(), list)
        self.assertIsInstance(events.description()[0], str)
        self.assertIsInstance(events.by_description(events.description()[0]), XACalendarEvent)

        self.assertIsInstance(events.start_date(), list)
        self.assertIsInstance(events.start_date()[0], AppKit.NSDate)
        self.assertIsInstance(events.by_start_date(events.start_date()[0]), XACalendarEvent)

        self.assertIsInstance(events.end_date(), list)
        self.assertIsInstance(events.end_date()[0], AppKit.NSDate)
        self.assertIsInstance(events.by_end_date(events.end_date()[0]), XACalendarEvent)

        self.assertIsInstance(events.allday_event(), list)
        self.assertIsInstance(events.allday_event()[0], bool)
        self.assertIsInstance(events.by_allday_event(events.allday_event()[0]), XACalendarEvent)

        self.assertIsInstance(events.recurrence(), list)
        self.assertIsInstance(events.recurrence()[0], str)
        self.assertIsInstance(events.by_recurrence(events.recurrence()[0]), XACalendarEvent)

        self.assertIsInstance(events.sequence(), list)
        self.assertIsInstance(events.sequence()[0], int)
        self.assertIsInstance(events.by_sequence(events.sequence()[0]), XACalendarEvent)

        self.assertIsInstance(events.stamp_date(), list)
        self.assertIsInstance(events.stamp_date()[0], AppKit.NSDate)
        self.assertIsInstance(events.by_stamp_date(events.stamp_date()[0]), XACalendarEvent)

        self.assertIsInstance(events.excluded_dates(), list)
        self.assertIsInstance(events.excluded_dates()[0], list)
        self.assertIsInstance(events.by_excluded_dates(events.excluded_dates()[0]), XACalendarEvent)

        self.assertIsInstance(events.status(), list)
        self.assertIsInstance(events.status()[0], XACalendarApplication.EventStatus)
        self.assertIsInstance(events.by_status(events.status()[0]), XACalendarEvent)

        self.assertIsInstance(events.summary(), list)
        self.assertIsInstance(events.summary()[0], str)
        self.assertIsInstance(events.by_summary(events.summary()[0]), XACalendarEvent)

        self.assertIsInstance(events.location(), list)
        self.assertIsInstance(events.location()[0], str)
        self.assertIsInstance(events.by_location(events.location()[0]), XACalendarEvent)

        self.assertIsInstance(events.uid(), list)
        self.assertIsInstance(events.uid()[0], str)
        self.assertIsInstance(events.by_uid(events.uid()[0]), XACalendarEvent)

        self.assertIsInstance(events.url(), list)
        self.assertIsInstance(events.url()[0], XAURL)
        self.assertIsInstance(events.by_url(events.url()[0]), XACalendarEvent)

        event = events[0]
        self.assertIsInstance(event, XACalendarEvent)

        self.assertIsInstance(event.properties, dict)
        self.assertIsInstance(event.description, str)
        self.assertIsInstance(event.start_date, AppKit.NSDate)
        self.assertIsInstance(event.end_date, AppKit.NSDate)
        self.assertIsInstance(event.allday_event, bool)
        self.assertIsInstance(event.recurrence, str)
        self.assertIsInstance(event.sequence, int)
        self.assertIsInstance(event.stamp_date, AppKit.NSDate)
        self.assertIsInstance(event.excluded_dates, list)
        self.assertIsInstance(event.status, XACalendarApplication.EventStatus)
        self.assertIsInstance(event.summary, str)
        self.assertIsInstance(event.location, str)
        self.assertIsInstance(event.uid, str)
        self.assertTrue(event.url == None or isinstance(event.url, XAURL))

    def test_calendar_event_methods(self):
        calendar1 = self.app.calendars().by_name("Calendar")
        calendar2 = self.app.calendars().by_name("Test")

        num_events_before1 = len(calendar1.events())
        event = calendar1.events()[-1]
        new_event1 = event.duplicate()
        self.assertNotEqual(num_events_before1, len(calendar1.events()))

        num_events_before2 = len(calendar2.events())
        new_event2 = new_event1.duplicate_to(calendar2)
        self.assertNotEqual(num_events_before2, len(calendar2.events()))
        new_event2.delete()
        self.assertEqual(num_events_before2, len(calendar2.events()))

        new_event3 = new_event1.move_to(calendar2)
        self.assertEqual(num_events_before1, len(calendar1.events()))
        self.assertNotEqual(num_events_before2, len(calendar2.events()))
        new_event4 = new_event3.move_to(calendar1)
        self.assertNotEqual(num_events_before1, len(calendar1.events()))
        self.assertEqual(num_events_before2, len(calendar2.events()))

        new_event4.delete()
        self.assertEqual(num_events_before1, len(calendar1.events()))

        self.assertIsInstance(event.attendees(), XACalendarAttendeeList)

        attachments = event.attachments()
        self.assertIsInstance(attachments, XACalendarAttachmentList)
        self.assertIsInstance(attachments[0], XACalendarAttachment)

    def test_calendar_attachments(self):
        attachments = self.app.calendars().by_name("Calendar").events()[-1].attachments()

        types = attachments.type()
        file_names = attachments.file_name()
        files = attachments.file()
        urls = attachments.url()
        uuids = attachments.uuid()

        self.assertIsInstance(types, list)
        self.assertIsInstance(types[0], str)
        self.assertIsInstance(attachments.by_type(types[0]), XACalendarAttachment)

        self.assertIsInstance(file_names, list)
        self.assertIsInstance(file_names[0], str)
        self.assertIsInstance(attachments.by_file_name(file_names[0]), XACalendarAttachment)

        self.assertIsInstance(files, list)
        self.assertIsInstance(files[0], XAPath)
        self.assertIsInstance(attachments.by_file(files[0]), XACalendarAttachment)

        self.assertIsInstance(urls, list)
        self.assertIsInstance(urls[0], XAURL)
        self.assertIsInstance(attachments.by_url(urls[0]), XACalendarAttachment)

        self.assertIsInstance(uuids, list)
        self.assertIsInstance(uuids[0], str)
        self.assertIsInstance(attachments.by_uuid(uuids[0]), XACalendarAttachment)

        attachment = attachments[0]
        self.assertIsInstance(attachment, XACalendarAttachment)

        self.assertIsInstance(attachment.type, str)
        self.assertIsInstance(attachment.file_name, str)
        self.assertIsInstance(attachment.file, XAPath)
        self.assertIsInstance(attachment.url, XAURL)
        self.assertIsInstance(attachment.uuid, str)