Fantastical Module Overview
===========================

The Fantastical module provides access to Fantastical's features from within PyXA, making use of both the application's scripting dictionary as well as its URL scheme.

Examples
########

Example 1 - Interacting with Currently Selected Calendar Items
**************************************************************

.. code-block:: python
   :linenos:

    import PyXA
    app = PyXA.application("Fantastical")
    items = app.selected_calendar_items()
    urls = [item.show_url.url for item in items]
    print(urls)
    # ['x-fantastical://show?item=7d627e52-ae3d-39eb-b86b-57b037f92cab&calendarIdentifier=A5E06B53-667F-42EE-A6FD-99609F6711E3&date=2022-02-21%2000:00', 'x-fantastical://show?item=e4bcc8c4-cd34-3c1d-b273-def4ecd47eae&calendarIdentifier=A5E06B53-667F-42EE-A6FD-99609F6711E3&date=2022-02-14%2000:00', ...]

Example 2 - Using Natural Language to Create Events
***************************************************

.. code-block:: python
   :linenos:

    import PyXA
    app = PyXA.application("Fantastical")
    app.parse_sentence("Meeting from 2pm to 3 today")
    app.parse_sentence("Joe's birthday August 26th all day")
    app.parse_sentence("Computer Science Homework due on Tuesday")
    app.parse_sentence("Vacation from August 26 to September 2")
    app.parse_sentence("Meeting at 2pm today alert 20 minutes before")
    app.parse_sentence("Attend Apple Event at 1 Infinite Loop, Cupertino, CA on September 14 at 9am")
    app.parse_sentence("Remind me to clean on Wednesday")

Fantastical Resources
#####################
- `Fantastical Integration With Other Apps Help <https://flexibits.com/fantastical/help/integration-with-other-apps>`_
- `Fantastical Guide - Calendar.com <https://web.archive.org/web/20220822222939/https://www.calendar.com/fantastical/#createe>`_

For all classes, methods, and inherited members of the Fantastical module, see the :ref:`Fantastical Module Reference`.