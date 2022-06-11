<p align="center"><img src="./sphinx/source/_static/assets/PyXALogoTransparent.png" alt="The dark logo for PyXA" height="250px"></p>

# Python for Automation
Python for Automation, or PyXA for short, is a wrapper around Apple's Scripting Bridge framework that enables AppleScript- and JXA-like control over macOS applications from within Python. PyXA delivers intuitive application scripting by mapping existing AppleScript specifiers and commands, defined in sdef files, to per-application Python classes and associated methods. PyXA then expands on the capabilities of AppleScript by interfacing with low-level Objective-C frameworks.

PyXA was created with the goals of:
1. Simplifying the way AppleScript tasks can be accomplished via Python
2. Disambiguating the capabilities of application scripting on macOS by providing easy-to-follow documentation throughout the entire project
3. Introducing new features to macOS application scripting by creating simple, JXA-like methods for complex Objective-C procedures

PyXA is not intended to replace AppleScript; rather, it is meant to provide general convenience in accomplishing AppleScript tasks via Python. PyXA simplifies the process of accomplishing AppleScript tasks from Python, filling the gap where current available frameworks ultimately fall short. AppleScript is still preferable in use cases requiring great speed due to the large number of Apple Events that PyXA sends during its operations. That said, there are plans to improve PyXA's speed in future versions, and there are countless use cases where PyXA's current speed is completely sufficient.

# Feature Overview
- Support for most AppleScript commands in built-in macOS applications (in progress)
- Support for several operations on non-scriptable applications (e.g. `PyXA.application("Maps").front_window().collapse()`)
- Command Chaining similar to JXA (e.g. `PyXA.application("Reminders").list(0).reminders()`)
- Property extraction from scriptable objects, allowing access via attributes (e.g. `note.name`, `tab.URL`, or `track.artist`)
- Automatic translation of clipboard items to PyXA objects
- Support for executing AppleScript scripts via NSAppleScript

# Some Examples
## Example 1: Open a URL in Safari and print the loaded page.
PyXA can also be to control Safari and interact with its content. In this example, we use PyXA to obtain a reference to the Safari application, open a specific URL, then bring up the print dialog for the loaded page. If we wanted, we could pass additional parameters to the print() method to skip the print dialog and immediately print the page without any user interaction. 
```python
import PyXA
from time import sleep
safari = PyXA.application("Safari")
safari.open("https://www.apple.com")
sleep(1)
safari.current_document().print()
```

## Example 2: Print Music track info whenever the track changes.
PyXA can be used to control the Music app as well as extract information from in. In this example, we use PyXA to get a reference to the Music app, begin playback of the next-up song, then repeatedly print out some information about the track whenever the current track changes. The information will be printed regardless of *how* the track changes, so you can test this script by running it and skipping to the next song. 
```python
import PyXA
music = PyXA.application("Music")
music.play()

track_name = ""
while True:
    if music.current_track().name != track_name:
        track_name = music.current_track().name
        print(music.current_track().name)
        print(music.current_track().album)
        print(music.current_track().artist, "\n")
```
When run, this script produces an output similar to the following:
```
Die Hard
Mr. Morale & The Big Steppers
Kendrick Lamar, Blxst & Amanda Reifer 

I Like You (A Happier Song) [feat. Doja Cat]
Twelve Carat Toothache
Post Malone 

WAIT FOR U (feat. Drake & Tems)
I NEVER LIKED YOU
Future

...
```

## Example 3: Create a new note with a list of all events and reminders for the day.
PyXA can also be used for more complex tasks. In this example, we use PyXA to get a summary of upcoming reminders and events for the day. We obtain references to the Notes, Calendars, and Reminders applications, then we iterate through our reminders and events, creating a new line of text to summarize each item due today. We apply some HTML formatting to the note to make it look nice, then we create a new note containing the summarized content.
```python
import PyXA
from datetime import datetime, timedelta
end_date = datetime.now().strftime("%Y-%m-%d")

notes = PyXA.application("Notes")
calendar = PyXA.application("Calendar")
reminders = PyXA.application("Reminders")

note_text = "-- Reminders --"
for reminder in reminders.reminders({"completed": False}):
    if reminder.dueDate is None or end_date in str(reminder.dueDate):
        note_text += "\nReminder: " + reminder.name
        if reminder.body != "" and reminder.body != None:
            note_text += "\n" + reminder.body

note_text += "\n\n-- Events --"
for calendar in calendar.calendars():
    for event in calendar.events():
        if end_date in str(event.endDate):
            note_text += "\nEvent: " + event.summary + ", from " + str(event.startDate) + " to " + str(event.endDate)

notes.new_note(f"<h1>Agenda for {end_date}</h1>", note_text)
```
When run, the above script creates a note in the Notes application similar to the following:

![A note in the Notes app showing a summary of reminders and events for the day](./sphinx/source/_static/assets/Example3_Notes.png)

# Installation
To install the latest version of PyXA on macOS, use the following pip command:
```
python -m pip install mac-pyxa
```

# Documentation
The best way to learn about PyXA is to visit the [Reference](./docs/index.html) section of this repository. From there, you can find tutorials, examples, in-depth class and method documentation, and additional resources.

For further help, consider joining the (PyXA Discord Server](https://discord.gg/Crypg65dxK) and asking your questions there.

# Known Limitations
- Currently, PyXA only supports macOS automation. There is a goal to expand support to other operating systems, but no concrete plan exists at this time.
- PyXA can be quite slow when working with large lists of items (such as the list of Calendar events). There are plans to improve this by better utilizing Objective-C predicates.
- Since PyXA uses hard-coded class and method definitions, instead of deriving them automatically from existing sdef files, support for third-party applications is limited to the applications that contributors deem relevant. This is a sacrifice made in order to have detailed, consistent documentation for all supported applications.

Limitations of specific applications and methods are noted in their respective reference documents.

# Contributing
Contributions are welcome, big or small. Please refer to the [Contributing Guidelines](./docs/about/contributing_guidelines.html) for any contributions larger than a spelling correction. For small fixes such as spelling corrections, no issue needs to be created; you can go right to making a pull request. Other small issues include general grammar fixes, short comment additions, and formatting (whitespace) changes.

# Contact
If you have any questions about PyXA that are not addressed in the documentation, or if you just want to talk, feel free to email [stephen.kaplan@maine.edu](mailto:stephen.kaplan@maine.edu).
