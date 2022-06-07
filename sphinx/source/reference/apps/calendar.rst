Calendar Module
===============

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
########
PyXA supports nearly all AppleScript/JXA commands for the Calendar application while adding some additional quality-of-life methods that AppleScript is missing. Alarms are not currently supported, but they will be by the time of PyXA's full release. New methods, such as :func:`PyXA.apps.Calendar.XACalendarEvent.add_attachment`, attempt to follow the style of JXA and make use of Apple's `EventKit Framework <https://developer.apple.com/documentation/eventkit>`_.

Tutorials
#########
There are two (planned) tutorials for working with the Calendar application:

- Create a Daily Event Summary Script
- How To: Add a Zoom link to all events with a given tag

Examples
########
The examples below provide an overview of the capabilities of the Calendar module. They do not provide any output. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Tutorials`).

Example 1 - Listing Calendars and Events
****************************************

One of the most common tasks when working with the Calendar application is that of listing events. PyXA offers several ways to obtain such lists, all of which may be useful in different contexts. In order to list events, you must first obtain a reference to one or more calendars, which can be done in a few ways as well. Lines `5-10` show the primary ways of obtain a calendar reference, while lines `12-18` show ways to obtain lists of events from the selected calendar.

A general rule of thumb when using PyXA to list events is that the more specific you can make your query, the better. While listing all events is necessary in some situations, a more specific query will always perform better. Filters, such as `{"title": "Learn PyXA"}`, can be used to decrease the number of queried events and, likewise, decrease the time of the listing operation. Filters can contain multiple parameters to further narrow the selection of events. The Calendar module provides some helper methods to assist in the creation and application of filters. For example, :func:`PyXA.apps.Calendar.XACalendar.events_in_range` can (and should) be used to find events occurring between two dates.

In addition to listing events, you can obtain references to specific events using the methods shown in lines `20-25`. These methods always select the first event that matches their respective filter, if applicable, so there are no performance concerns there. However, there is no guarantee that the list of events will maintain a consistent order. A filter that directly identifies an event using its unique properties is therefore preferred over a general filter that matches with multiple events.

.. code-block:: python
   :linenos:

   from datetime import datetime, timedelta
   import PyXA
   app = PyXA.application("Calendar")

   # Getting calendars
   all_calendars = app.calendars()
   calendar = app.default_calendar()
   calendar0 = app.calendar(0)
   calendar1 = app.calendar(1)
   named_calendar = app.calendar({"title": "Calendar"})

   # Getting lists of events
   all_events = calendar.events()
   events_at_location = calendar.events({"location": "1 Main Street\\nPortland ME 04101\\nUnited States"})
   named_events = calendar.events({"title": "Learn PyXA"})
   events_between_dates = calendar.events_in_range(datetime.now(), datetime.now() + timedelta(days = 7))
   events_today = calendar.events_today()
   events_this_week = calendar.week_events()

   # Getting specific events
   event0 = calendar.event(0)
   first_event = calendar.first_event()
   last_event = calendar.last_event()
   named_event = calendar.events({"title": "Learn PyXA"})[0]
   event_by_id = calendar.event({"uid": "A54CF13A-36D2-5DE1-9980-BE19C4C102A4"})

   # Get today's event from each calendar
   events = []
   for calendar in all_calendars:
      events.extend(calendar.events_today())

Example 2 - Creating Calendars and Events
*****************************************

.. code-block:: python
   :linenos:

   from datetime import datetime, timedelta
   import PyXA
   app = PyXA.application("Calendar")

   # Create a new calendar
   new_calendar = app.new_calendar("PyXA Development")

   # Create new events
   start_date = datetime.now()
   end_date = start_date + timedelta(hours = 1)
   app.new_event("Test 1", start_date, end_date) # Created in default/currently selected calendar
   app.new_event("Test 2", start_date, end_date, new_calendar) # Created in the new calendar
   new_calendar.new_event("Test 3", start_date, end_date) # Same as Test 2

Example 3 - Modifying and Manipulating Events
*********************************************

.. code-block:: python
   :linenos:

   from datetime import date
   import PyXA
   app = PyXA.application("Calendar")

   calendar = app.default_calendar()
   calendar1 = app.calendar(1)
   event = calendar.events_today()[0]

   # Modify event properties
   event.rename("Title changed")

   new_start_date = date(2022, 6, 6)
   new_end_date = date(2022, 6, 7)
   event.set_property("startDate", new_start_date)
   event.set_property("endDate", new_end_date)

   # Execute event actions
   event.duplicate()
   event.copy_to(calendar1)
   event.move_to(calendar1)
   event.delete()

Example 5 - Displaying Events in Calendar.app
*********************************************

.. code-block:: python
   :linenos:

   from datetime import date
   import PyXA
   app = PyXA.application("Calendar")

   calendar = app.default_calendar()
   calendar1 = app.calendar(1)
   event = calendar.events_today()[0]

   event.show()
   app.switch_view_to("day")
   app.switch_view_to("week")
   app.switch_view_to("month")
   app.view_calendar_at(date(2022, 6, 5))
   app.view_calendar_at(event.end_date)

Resources
#########

Calendar Classes and Methods
############################
.. toctree::
   :maxdepth: 1
   :caption: Classes

   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication
   ../api/apps/calendar/XACalendarAttachment/PyXA.apps.Calendar.XACalendarAttachment
   ../api/apps/calendar/XACalendarAttendee/PyXA.apps.Calendar.XACalendarAttendee
   ../api/apps/calendar/XACalendarEvent/PyXA.apps.Calendar.XACalendarEvent
   ../api/apps/calendar/XACalendarWindow/PyXA.apps.Calendar.XACalendarWindow

.. toctree::
   :maxdepth: 1
   :caption: Methods

   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.event
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.events
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.events_in_range
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.events_today
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.first_event
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.last_event
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.new_event
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.push
   ../api/apps/calendar/XACalendar/PyXA.apps.Calendar.XACalendar.week_events
   
.. toctree::
   :maxdepth: 1
   
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.calendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.calendars
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.default_calendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.first_calendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.last_calendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.new_calendar
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.new_event
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.reload_calendars
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.subscribe_to
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.switch_view_to
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarApplication.view_calendar_at

.. toctree::
   :maxdepth: 1
   
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarAttachment.open

.. toctree::
   :maxdepth: 1
   
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.add_attachment
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.attachments
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.attendees
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.copy_to
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.delete
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.duplicate
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.move_to
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.rename
   ../api/apps/calendar/XACalendarApplication/PyXA.apps.Calendar.XACalendarEvent.show

For all classes, methods, and inherited members on one page, see the :ref:`Complete Calendar API`


.. .. automodapi:: PyXA.apps.Calendar
..    :no-main-docstr:
..    :skip: NSMutableArray, NSPredicate, NSURL, SBObject, date, datetime, timedelta