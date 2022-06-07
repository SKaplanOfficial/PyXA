import PyXA
app = PyXA.application("Contacts")

contacts = app.contacts()
for contact in contacts:
    contact.show()
# for track in tracks:
#     print(track.title, track.xa_elem.locationType(), track.xa_elem.purchaseDate())



# print(app.tracks({"year": 1997}))
#print(playlists)
# track = app.track({"name": "Ontologiii"})
# playlist = app.first_playlist()
# x = playlist.search("s")

# for y in x:
#     print(y.name)
# app.add_to_playlist(["/Users/steven/Documents/Ontologiii.mov"], playlist)
# app.open_location("https://devstreaming-cdn.apple.com/videos/wwdc/2019/502gzyuhh8p2r8g8/502/hls_vod_mvp.m3u8")
# app.open_location("itmss://tv.apple.com/us/movie/the-sanctity-of-space/umc.cmc.b6dje1348roj7h5n4y4jh8ba")
















# from datetime import date
# import PyXA
# app = PyXA.application("Calendar")

# calendar = app.default_calendar()
# calendar1 = app.calendar(1)
# event = calendar.events_today()[0]

# event.show()
# app.switch_view_to("day")
# app.switch_view_to("week")
# app.switch_view_to("month")
# app.view_calendar_at(date(2022, 6, 5))
# app.view_calendar_at(event.end_date)

# # Getting calendars
# all_calendars = app.calendars()
# calendar = app.default_calendar()
# calendar0 = app.calendar(0)
# calendar1 = app.calendar(1)
# named_calendar = app.calendar({"title": "Calendar"})

# # Getting lists of events
# all_events = calendar.events()
# events_at_location = calendar.events({"location": "1 Main Sreet\\nPortland ME 04101\\nUnited States"})
# named_events = calendar.events({"title": "Learn PyXA"})
# events_between_dates = calendar.events_in_range(datetime.now(), datetime.now() + timedelta(days = 7))
# events_today = calendar.events_today()
# events_this_week = calendar.week_events()

# # Getting specific events
# event0 = calendar.event(0)
# first_event = calendar.first_event()
# last_event = calendar.last_event()
# named_event = calendar.event({"title": "Learn PyXA"})[0]
# event_by_id = calendar.event({"uid": "A54CF13A-36D2-5DE1-9980-BE19C4C102A4"})

# # Get today's event from each calendar
# events = []
# for calendar in all_calendars:
#     events.extend(calendar.events_today())

# from PyXA.XABase import XAList
# test = XAList()
# test.append(2)
# test.append(4)
# print(test.front.add(2))
# print(test.end.add(1))

# # for x in test:
# #     print(x)
# print(test[0])


# XAList.append(1)
# print(XAList)

# from time import sleep
# app = PyXA.application("Calculator")
# print(app.current_value() + 1)
# app.clear_value()
# app.input("3.14159265*2*5*5*5=")
# app.save_tape()
# app.print_tape()
# app.copy_value()
# app.show_basic_calculator()
# app.show_scientific_calculator()
# app.show_programmer_calculator()
# app.toggle_thousands_separators()
# app.toggle_RPN_mode()
# app.show_paper_tape()
# app.show_help()



# import PyXA
# from datetime import datetime, timedelta
# app = PyXA.application("Calendar")
# start_date = datetime.now()
# end_date = datetime.now() + timedelta(hours = 1)
# # app.new_event("Hi", start_date, end_date)
# # print(app.new_calendar("Hi"))
# # app.switch_view_to("year")
# app.view_calendar_at(start_date, "day")



# import PyXA
# app = PyXA.application("Preview")
# app.activate()
# docs = app.documents()
# doc = docs[0]
# # doc.print()
# # # print(docs)
# # app.print("/Users/steven/Documents/eek/Avery.jpg")
# windows = app.windows()
# window = app.front_window()
# # window.print()
# # app.open("/Users/steven/Documents/eek/Avery.jpg")
# # print(window.document)






# import PyXA
# app = PyXA.application("Reminders")
# #PyXA.run_applescript("beep")
# print(PyXA.get_running_applications())

# from datetime import datetime, timedelta
# from time import sleep
# import PyXA
# app = PyXA.application("Calendar")

#print(app.calendars())
#print(app.calendars({"title": "Florida"}))
#print(app.calendar(0))
# print(app.calendar({"title": "Calendar"}))
# print(app.first_calendar())
# print(app.last_calendar())
# print(app.default_calendar())

# cal = app.default_calendar()
# cal2 = app.calendar(1)
# print(cal.events())
# print(cal.events({"title": "Joe"}))
# print(cal.event(0))
# print(cal.event({"title": "Joe"}))
# print(cal.first_event())
# print(cal.last_event().title)
# print(cal.events_today())

# event = cal.events_today()[0]
# print(event.title)
# event.rename("Test")
# event.delete()
# event.duplicate()
# event.move_to(cal2)
# print(cal.title)
# print(cal2.title)
# event.add_attachment("/Users/steven/Documents/eek/eek.txt")
# print(event.attachments())
# event.attendees()

# event = cal.events()[0]
# event.duplicate()
# cal = app.default_calendar()

# start_date = datetime.now()
# end_date = datetime.now() + timedelta(hours = 1)
# new_event = app.new_event("Learn about PyXA", start_date, end_date)

# cal2 = app.calendar(3) # Florida
# new_event.move_to(cal2)


















# app = PyXA.application("Messages")
# files = app.file_transfers()
#PyXA.open_file(files[0].filePath)
#PyXA.open_url("http://youtube.com")
# for file in files:
#     PyXA.open_file(file.filePath)


# import PyXA
# app = PyXA.application("Notes")
# app.open("/Users/steven/Desktop/sdefs/Notes.h") # Import to Notes
# print(app.first_folder().first_note().last_attachment().contents)

# Script to create a new note with a list of all events and reminders for the day.
# import PyXA
# from datetime import datetime, timedelta
# start_date = datetime.now()
# end_date = datetime.now().strftime("%Y-%m-%d")
# end_date_1 = datetime.now() + timedelta(days = 1)

# notes = PyXA.application("Notes")
# calendar = PyXA.application("Calendar")
# reminders = PyXA.application("Reminders")

# note_text = "-- Reminders --"
# for reminder in reminders.reminders({"completed": False}):
#     if reminder.dueDate is None or end_date in str(reminder.dueDate):
#         note_text += "\nReminder: " + reminder.name
#         if reminder.body != "" and reminder.body != None:
#             note_text += "\n" + reminder.body

# print("---")
# note_text += "\n\n-- Events --"
# for calendar in calendar.calendars():
#     for event in calendar.events():
#         if end_date in str(event.endDate):
#             note_text += "\nEvent: " + event.summary + ", from " + str(event.startDate) + " to " + str(event.endDate)

# notes.new_note(f"<h1>Agenda for {end_date}</h1>", note_text)


# Script to open a URL in Safari and print the loaded page.
# import PyXA
# from time import sleep
# safari = PyXA.application("Safari")
# safari.open("https://www.apple.com")
# sleep(1)
# safari.current_document().print()

# Script to print current track information whenever the track changes
# import PyXA
# music = PyXA.application("Music")
# music.play()

# track_name = ""
# while True:
#     if music.current_track().name != track_name:
#         track_name = music.current_track().name
#         print(music.current_track().name)
#         print(music.current_track().album)
#         print(music.current_track().artist, "\n")

#app = PyXA.application("TextEdit")
# doc = app.documents()[0]
#app.new_document("Hi.txt")
# app.new_document("Hi.txt", "This is some text")
#app.new_document("Hi.txt", "This is some text", "/Users/steven/Documents/wow.txt")
# print(doc.paragraphs())
#print(doc.words())
#print(doc.characters())
#print(doc.attribute_runs())
#print(doc.attachments())
# print(doc.text)
#doc.set_text("hi")
#doc.prepend("1.")
#doc.append("----")
# print(doc.text)
#doc.print()
# app.activate()
# app.open("/Users/steven/Desktop/sdefs/Notes.h")
#app.print("/Users/steven/Documents/GitHub/PyXA/Experiment.py")
# windows = app.windows()
# print(windows)
# window = app.front_window()
# doc = window.document
# print(doc)



# app = PyXA.application("Terminal")
#print(app.settings_sets())
#print(app.windows())
#print(app.front_window().element_properties)
#print(app.default_settings())
#print(app.startup_settings())
# window = app.front_window()
# window.print()
# app.open("/Users/steven/Documents/test")
#tab = app.current_tab()
#app.do_script("say hi", tab)
#print(tab.current_settings())










#app = PyXA.application("Reminders")
#print(app.last_list())
#print(app.reminders({"name": "Created in fancy"}))
#new_list = app.new_list("Neo Listo")
#reminder = app.new_reminder("Neo remindero")

#app.open("/Users/steven/Documents/eek/test.textClipping")






















#app = PyXA.application("Finder")
# print(app.settings_sets())
#app.empty_trash()
#app.select_item("/Users/steven/Documents/eek.txt")
#app.select_items(["/Users/steven/Documents/eek.txt", "/Users/steven/Documents/Toni.jpg", "/Users/steven/Downloads/Test.ics"])
#app.search("hi")
#app.recycle_item("/Users/steven/Documents/eek.txt")
#app.delete_item("/Users/steven/Documents/eek.txt")
#app.duplicate_item("/Users/steven/Documents/test")
#app.duplicate_items(["/Users/steven/Documents/test"])
#folders = app.folders()
# for folder in folders:
#     print(folder.name)
#print(app.home_directory().URL)
#print(app.temp_directory().URL)
# print(app.documents_directory().URL)
# print(app.applications_directory().URL)
# print(app.public_directory().URL)
# print(app.pictures_directory().URL)
# print(app.movies_directory().URL)
# print(app.music_directory().URL)
# print(app.downloads_directory().URL)
# print(app.directory("/Users/steven/Documents/test").URL)
#directory = app.music_directory()
# directory.reveal()
#directory.select()
#directory.delete()
# directory = app.directory("/Users/steven/Documents/eek")
#print(directory.size())
# directory.copy()
# selected = app.selection()
# file = selected[0]
# print(file.exists())
#file.print()
# print(file.size)

#directory.move_to("/Users/steven/Documents/test")
#print(app.selection())
#print(app.insertion_location().URL)


#directory.properties["element"].delete()























# app = PyXA.application("Calendar")
# # window = app.front_window()
# # cal = app.first_calendar()
# # #print(cal)
# # #app.new_calendar("Test")
# cal3 = app.calendar(3)
# start_date = datetime.now()
# end_date = start_date + timedelta(hours = 50)
# # #new_event = app.new_event("Learn about PyXA", start_date, end_date)
# # #new_event = cal.new_event("Learn about PyXA", start_date, end_date)
# # # event = app.construct("event", {"summary": "A new event!", "startDate": start_date, "endDate": end_date})
# # # print(event)
# # # cal.push(event)
# # # new_event = app.construct("event", {"summary": "Learn about PyXA", "startDate": start_date, "endDate": end_date})
# # # print(cal.push(new_event))
# # # cal.new_event("Test", start_date, end_date)
# new_event = app.new_event("Learn about PyXA", start_date, end_date)
# # # print(new_event)
# #print(app.first_calendar().events())
# # print(app.default_calendar().first_event().properties["element"].properties())
# #app.default_calendar().event({"summary": "COS 140"}).show()
# # new_cal = app.new_calendar("Test")
# # time.sleep(10)
# # new_cal.delete()
# #new_event.delete()
# #app.open("/Users/steven/Downloads/Test.ics")
# #app.subscribe_to("https://calendar.google.com/calendar/ical/nett.moodle%40gmail.com/private-e2019fa078137a257fb211782ae631a5/basic.ics")
# # #app.reload_calendars()
# # #app.view_calendar_at(datetime.now() + timedelta(days = 100))
# # app.switch_view_to("month")
# time.sleep(3)



# app = PyXA.application("Safari")
# tab = app.front_window().current_tab()
# window2 = app.window(1)
#tab.move_to(window2)
#tab.duplicate_to(window2)

#app = PyXA.application("Safari")
#app.open("/Users/steven/Documents/GitHub/py-jxa/PyXA/reference/build/html/bugs.html")
#app.open("youtube.com")
# tab = app.front_window().current_tab()
# app.search_in_tab(tab, "What is PyXA?")
# window = app.front_window()
# doc = app.current_document()
# tab = window.current_tab()
# app.add_to_reading_list(doc)
# app.add_to_reading_list(tab)
# app.do_javascript("(function myMain2() { return '5' })()")







# app = PyXA.application("Notes")
#app.new_note("hi")
#app.new_folder("hi")
# print(app.note({"name": "Joe"}))








#app = PyXA.application("Music")
#print(app.current_track().unplayed)
#app.open("/Users/steven/Downloads/Music/Audio/starsabove.mp3")
# print(app.properties["sb_element"].properties())
#app.set_volume(50)
#app.set_fullscreen()
#app.open_location("itmss://music.apple.com/us/station/afrobeats-101/ra.1626113290")
#app.open_location("https://ia800700.us.archive.org/0/items/DamroschOrchestra/DamroschOrchestra-ToreadorSong.mp3")

#app.set_clipboard("test")
#print(app.get_clipboard())

#app.play()
#app.pause()
#app.stop()
#app.playpause()
#app.next_track()
#app.back_track()
#app.previous_track()
#app.fast_forward()
#app.rewind()
#app.resume()

#current = app.current_track()
#current.select()
#current.reveal()
#current.select()
#current.play()

# first = app.track({"name": track.properties["element"].name()})
#named_track = app.track({"name": "21 Guns"})
#print(current.properties["element"].properties())
#print(named_track.kind)
#print(named_track.properties["element"].properties())
#named_track.play()
#named_track.open() <-- Not working currently

#playlist = app.last_playlist()
#app.repeat_one()
#app.repeat_off()
#app.repeat_all()
# print(playlist.properties["element"].name())
# playlist.reveal()
#playlist.play()

































# app = PyXA.new_application("com.apple.MobileSMS")
# app.activate()
# app.print()

#app = PyXA.application("Safari")
# #app.show_bookmarks()
#window = app.front_window()
# #window.close()
# #window.print()
#doc = app.first_document()
# # doc.print()
# # doc.close()
# # doc.save() # <-- Not working currently
# #doc.do_javascript("alert('hi');")
# # doc.search("ayo")
# tab = window.current_tab()
# # app.search(tab, "Hi")
# #app.do_javascript("alert('hi');", tab)
# #tab.close()
# #tab.do_javascript("alert('hi');")
# #tab.search("wow")
# window2 = app.window(1)
# tab2 = window2.current_tab()
# #doc.move_to(window2) # <-- Not working currently
# #doc.duplicate_to(tab2) # <-- Not working currently
# #tab.email()
# #doc.email()
# #tab.add_to_reading_list()
# #doc.add_to_reading_list()
# #app.search("hi")
# #app.search_in_tab(tab, "hi")




# app = PyXA.application("Notes")
# folder = app.first_folder()
# note = folder.new_note("Pyxa Notes", "Yay")
# print(note.properties)

# se = PyXA.application("System Events")
# sound = PyXA.sound("Bottle")

# maps = se.processes_with_properties({"name": "Maps"})[0]
# window = maps.windows()[0]
# window.activate()

# toolbar = window.toolbars()[0]
# sidebar_btn = toolbar.buttons_with_properties({"objectDescription": "Toggle Sidebar"})[0]
# sidebar_btn.press()

# location_btn = toolbar.buttons_with_properties({"objectDescription": "Location"})[0]
# location_btn.press()



# safari = PyXA.application("Safari")
# window = safari.elements_with_properties("windows", {"miniaturized": False}, XASBWindow)[0]
# print(window.buttons())

# se = PyXA.application("System Events")
# maps = se.processes_with_properties({"name": "Maps"})[0]
# window = maps.windows()[0]
# window.activate()

# toolbar = window.toolbars()[0]
# sidebar_btn = toolbar.buttons_with_properties({"objectDescription": "Toggle Sidebar"})[0]
# sidebar_btn.press()

# location_btn = toolbar.buttons_with_properties({"objectDescription": "Location"})[0]
# location_btn.press()



# window.entire_contents()
# window.all("buttons")[0].click()
# time.sleep(10)
# window.all("buttons")[0].click()

# window = messages.first_window()
# action = window.first_action()
# action.perform()

# buttons = window.buttons()
# minimize_btn = buttons[2]
# minimize_btn.click()


# pages = PyXA.application("Pages")
# document = pages.first_document()
# print(document.first_shape().properties)

# document.new_shape()
#document.new_page()

# while True:
#     te.front_window().collapse()
#     te.front_window().uncollapse()
#te.new_document("hello.txt")
#te.documents()[0].append("hello")

#print(PyXA.get_running_applications())
# safari = PyXA.launch_application("Mail")
# print(safari.properties)
#print(safari.front_window().properties)

# calendar = PyXA.application("Calendar")
# print(calendar.first_calendar())
# start = datetime.now()
# end = start + timedelta(minutes=30)
# calendar.new_event("Test event", start, end)

# messages = PyXA.application("Messages")
# messages.send("Test", "ET")

### EXAMPLE 1 - Ways to make a new note
# notes = PyXA.application("Notes")
# notes.new_note("1st Note", "Made via new_note() method.")
# notes.push("note", {"name": "2nd Note", "body": "Made via top-level push() method."}, notes.element.notes())
# notes.folders()[0].push("note", {"body": "<b>3rd Note</b><br />Made via folder-level push() method."})



# reminders = PyXA.launch_application("Reminders")
# reminders.make()

# windows = PyXA.launch_application("Music").windows()
# test = windows[0]
# test.fullScreen();

# music = PyXA.application("Music")
# music.activate()
# music.set_volume(20)


# finder = PyXA.application("Finder")
# finder.launch()
# print(finder.directory("/Users/steven/Documents/test"))

# safari = PyXA.application("Safari")
# safari.launch()
# safari.custom_window(800, 500, "http://google.com")
#safari.open("http://google.com")

# test = XA.launch_application("Music").windows()
# print(test)

#test = PyXA.application("Finder").activate().processIdentifier()
#print(test)

# finder = PyXA.application("Finder")
# finder.launch()
# windows, windowList = finder.windows()
# print(windowList)
# print(windows)