# PyXA Changelog

## [PyXA 0.3.0] - 2023-04-13

**Additions**

- Added _XACamera_.
- Added _XAMicrophone_.
- Added _XAScreen_.
- Added _XADatetimeBlock_ type representing dates with a duration attached.
- Added _XAList.map()_.
- Added _XAText.extract_urls()_. Returns a list of _XAURL_ objects.
- Added _XAText.extract_dates()_. Returns a list of _XADatetimeBlock_ objects.
- Added _XAText.extract_addresses()_. Returns a list of _XALocation_ objects.
- Added _XAText.extract_phone_numbers()_. Returns a list of _XAText_ objects.
- Script Editor:
  - Added _XAScriptEditorApplication.make()_.
- Shortcuts:
  - Added _XAShortcutsApplication.make()_.
- Bike Outliner:
  - Added _XABikeApplication.RowType_ enum.
  - Added _XABikeApplication.query()_.
  - Added _XABikeRowList.type()_. Returns a list of _XABikeApplication.RowType_.
  - Added _XABikeRowList.by_type()_. Returns a _XABikeRowList_.
  - Added _XABikeRowList.delete()_.
  - Added _XABikeRowList.rows()_.
  - Added _XABikeRowList.attributes()_.
  - Added _XABikeRow.type()_. Returns a _XABikeApplication.RowType_.
  - Added _XABikeRow.delete()_.
- Added _XAErrors.AppleScriptError_ for handling AppleScript compilation and runtime errors.
- New Applications:
  - Added support for Arc.
  - Added greater support for various Chromium browsers.
  - Added support for OmniWeb.
  - Added support for Path Finder.

**Changes**

- AppleScript:
  - AppleScript.load()
  - _AppleScript.run()_ now accepts one argument, _args_, providing a list of arguments to pass to the script.
  - _AppleScript.run()_ now raises the error returned by the script, if any.
- Maps:
  - _XAMapsApplication.sidebar_showing_ can now be set to True/False.
  - _XAMapsApplication.search()_ now accepts both str and _XAText_ as input.
  - _XAMapsApplication.directions_to()_ now accepts both str and _XAText_ as input.
  - _XAMapsTabList_ and _XAMapsTab_ now print elegantly.
  - _XAMapsTabList_ is now a subclass of _XASystemEventsUIElementList_.
  - _XAMapsTab_ is now a subclass of _XASystemEventsUIElement_.

**Bug Fixes**

- Fixed _AppleScript.load()_ removing excess characters from scripts, causing e.g. lists not to work.
- Fixed error when creating new note in Notes using _XANotesApplication.new_note()_. (Resolve #13)
- Fixed _XAAudio.beep()_ failing due to too many arguments.

---

## [PyXA 0.2.2] - 2023-03-15

**Additions**

- Added _XAObject.exists()_.
- Added “exists” filter support.
- Added “not exists” filter support.
  - Alternate forms: “!exists”, “nonexistent”
- iWork Improvements:
  - Added _XAKeynoteSlide.move()_.
  - Added _XAKeynoteSlide.duplicate()_.
- Music improvements:
  - Added _XAMusicApplication.make()_.
  - Added _XAMusicTrack.move()_.
  - Added _XAMusicTrack.duplicate()_.
  - Added _XAMusicPlaylist.move()_.
  - Added _XAMusicPlaylist.duplicate()_.
  - Added _XAMusicPlaylist.add_tracks()_.
- TV improvements:
  - Added _XATVApplication.make()_.
  - Added _XATVTrack.move()_.
  - Added _XATVTrack.duplicate()_.
  - Added _XATVPlaylist.move()_.
  - Added _XATVPlaylist.duplicate()_.
  - Added _XATVPlaylist.add_tracks()_.
- Added support for IINA+

**Changes**

- Reverted use of shared base classes for media applications.
  - Removed _MediaApplicationBase_.
  - This should have no impact on most code, unless it references specific class types. Otherwise, the methods and attributes available for media application classes are the same.
- _XAMusicApplication.current_track_ is now a property instead of a method.

**Bug Fixes**

- Fixed Music objects not correctly specializing to Music-specific classes. (#10)
- Fixed TV objects not correctly specializing to TV-specific classes.
- Fixed _XANotesApplication.new_note()_ failing due to not getting string form of XAText object.
- Fixed _XAMusicSourceList.by_kind()_ and _XATVSourceList.by_kind()_ always returning None.
- Fixed _XAMusicSourceList.filter()_ and _XATVSourceList.filter()_ not transforming “kind” value into proper event format.
- Fixed _XAMusicTrackList.by_cloud_status()_ always returning None.
- Fixed _XAMusicTrackList.by_rating_kind()_ and _XATVTrackList.by_rating_kind()_ always returning None.
- Fixed _XAMusicTrackList.by_media_kind()_ and _XATVTrackList.by_media_kind()_ always returning None.
- Fixed _XAMusicTrackList.by_album_rating_kind()_ and _XATVTrackList.by_album_rating_kind()_ always returning None.
- Fixed _XAMusicTrackList.filter()_ and _XATVTrackList.filter()_ not transforming event values into proper event format.
- Fixed _XASystemEventsDesktop.dynamic_style_, _XASystemEventsDockPreferencesObject.double_click_behavior_, _XASystemEventsDockPreferencesObject.minimize_effect_, _XASystemEventsDockPreferencesObject.screen_edge_ yielding an error due to improper conversion from event format.

---

## [PyXA 0.2.1] - 2023-03-04

**Additions**

- Added _XADiskItem.move_to(folder)_ and _XADiskItemList.move_to(folder)_.
- Improvements to Bike support:
  - Added _XABikeDocumentList.edit_mode()_.
  - Added _XABikeDocument.edit_mode_.
  - Added _XABikeDocument.import_rows()_.
  - Added _XABikeDocument.export()_.
  - Added _XABikeRowList.container_document()_.
  - Added _XABikeRow.duplicate()_.
- Improvements to Media apps (Music/TV):
  - Added _XAMediaApplication.library_playlists()_.
  - Added _XAMediaApplication.file_tracks()_.
  - Added _XAMediaApplication.url_tracks()_.
  - Added _XAMediaApplication.shared_tracks()_.
  - Added _XAMediaPlaylist.play()_.
  - Added _XAMusicAirPlayDeviceList.supports_video()_.
  - Added _XAMusicApplication.user_playlists()_.
  - Added _XAMusicApplication.subscription_playlists()_. (#8)
  - Added _XAMusicApplication.radio_tuner_playlists()_.
  - Added _XAMusicApplication.audio_cd_playlists()_.
- Improvements to Mail support:
  - Added _XAMailAccountList.mailboxes()_.
  - Added _XAMailboxList.messages()_.

**Bug Fixes/Changes**

- Fixed missing dependencies: ApplicationServices, CoreText
- Fixed _XASBWindow_ object not correctly linking to the UI element subsystem of System Events. Scriptable and non-scriptable applications should now behave the same (previously only non-scriptable applications could directly access their UI elements). (#8)
- Fixed _XAFolder.aliases()_, _XAFolder.disk_items()_, _XAFolder.files()_, _XAFolder.file_packages()_, and _XAFolder.folders()_ always returning None.
- Fixed _XAFilePackage.aliases()_, _XAFilePackage.disk_items()_, _XAFilePackage.files()_, _XAFilePackage.file_packages()_, and _XAFilePackage.folders()_ always returning None.
- Fixed _XADisk.aliases()_, _XADisk.disk_items()_, _XADisk.files()_, _XADisk.file_packages()_, and _XADisk.folders()_ always returning None.
- Fixed _XAAlias.aliases()_, _XAAlias.disk_items()_, _XAAlias.files()_, _XAAlias.file_packages()_, and _XAAlias.folders()_ always returning None.
- Fixed _XAClassicDomainObject.folders()_ always returning None.
- Fixed _XADomain.folders()_ always returning None.
- Fixed _XAMusicApplication.airplay_enabled_ yielding an error due to invalid property name.
- Fixed _XAMusicApplication.eq_enabled_ yielding an error due to invalid property name.
- Fixed _XAMusicApplication.play(item)_ resuming playback instead of playing the specified item. (#8)
- Fixed _XAMusicAirPlayDeviceList.by_kind()_ always returning None.
- Fixed _XAProtocols.XAPrintable_ running in the main thread instead of separately.

---

## [PyXA 0.2.0] - 2023-01-18

**Additions**

- Added support for Python 3.10 (Removed ‘Self’ type annotations)
- Added support for Database Events
- New Notes app functionality
  - _Notes.XANotesFolder.folders()_ - Gets the subfolders of a folder.
  - _Notes.XANotesFolderList.folders()_ - Gets the subfolders of each folder in a list.
- Added _Additions.UI.XAHeaderMenuItem_ and _Additions.UI.XAMenuBarMenu.new_header()_ for adding non-clickable section headers to menus.

**Bug Fixes/Changes**

- Upgraded to PyObjC 9.x (Current version is 9.0.1). Resolves #3.
- Getting the ID of a Notes.app object now always returns a string.
- Fixed _Terminal.XATerminalSettingsSetList.by_cursor_color()_, _Terminal.XATerminalSettingsSetList.by_background_color()_, _Terminal.XATerminalSettingsSetList.by_normal_text_color()_, and _Terminal.XATerminalSettingsSetList.by_bold_text_color()_ always returning None.

**Deprecations**

- _XABase.XAObject.set_properties()_ — Use set_property() instead. This change is being made to reduce unnecessary redundancy within the codebase.
- _XABase.XAImageList_ — Use XAImage method with iteration instead. This change is being made to reduce unnecessary redundancy within the codebase.

**Removals**

- Removes _XAObject.has_element()_ — Deprecated in v0.0.9. If necessary, perform this check manually instead.
- Removed _XAObject.has_element_properties() — Deprecated in v0.0.8. All elements now have a properties dictionary, even if it is empty.
- Removed _XAObject.set_element() — Deprecated in v0.0.9.
- Removed ability to pass a _data_ parameter when initializing an _XAImage_ — Deprecated in v0.1.0. Pass data as the _image_reference_ parameter instead.
- Removed _XASBWindow.toggle_zoom()_ — Deprecated in v0.1.0.2. Set the _zoomed_ attribute instead.
- Removed _Calendar.XACalendarCalendar.week_events()_ — Deprecated in v0.1.2. Use _events_in_range()_ instead.
- Removed _Finder.XAFinderApplication.recycle_items()_ — Deprecated in v0.1.2. Use _recycle_item()_ instead.
- Removed _Finder.XAFinderApplication.delete_items()_ — Deprecated in v0.1.2. Use _delete_item()_ instead.
- Removed _Finder.XAFinderApplication.duplicate_items()_ — Deprecated in v0.1.2. Use _duplicate_item()_ instead.
- Removed _Additions.UI.XAAlertStyle_ and _Additions.UI.XAAlert.style_ — Deprecated in v0.1.2. Customize the icon by setting the alert’s _icon_ attribute instead.
- _Removed Additions.UI.XAMenuBar.add_menu()_ — Deprecated in v0.1.1. Use _new_menu()_ instead.
- Removed _XAMediaWindow.collapseable_ and _XAMediaWindow.collapsed_ attributes — Deprecated in v0.1.1. Use the _miniaturizable_ and _miniaturized_ attributes instead.
- Removed _XAiWorkImage.rotate()_ and _XAiWorkShape.rotate()_ — Deprecated in v0.1.1. Set the _rotation_ attribute instead.
- Removed _Additions.UI.XAMenuBar.add_item()_ — Deprecated in v0.1.1. Use _Additions.UI.XAMenuBarMenu.new_item()_ instead.
- Removed _Additions.UI.XAMenuBar.set_item()_ — Deprecated in v0.1.1. Set the _image_ attribute of menus and menu items instead.
- Removed _Additions.UI.XAMenuBar.set_item()_ — Deprecated in v0.1.1. Set the _title_ attribute of menus and menu items instead.
- Removed _Additions.UI.XAMenuBar.add_separator()_ — Deprecated in v0.1.2. Use _Additions.UI.XAMenuBarMenu.new_separator()_ instead.
- Removed _Additions.UI.XAMenuBarMenuItem.new_subitem()_ — Deprecated in v0.1.2. Use _new_item()_ instead.
- Removed _Additions.UI.XAMenuBarMenuItem.remove_subitem()_ — Deprecated in v0.1.2. Use _remove_item()_ instead.
- Removed various XASystemEvents UI classes, now condensed to a single UI element class — this better represents the scripting dictionary for System Events. Unless scripts reference these classes directly, there will be no observable impact of this change.
- Removed numpy dependency.

---

## [PyXA 0.1.2] - 2022-12-14

**Additions**

- Added ability to instantiate application objects by calling their title-case name (with whitespace removed) on the PyXA module, e.g. _PyXA.Calendar()_ and _PyXA.Safari()_
- Added _Additions.UI.XAHUD_ — A class for displaying momentary messages to the user via a HUD window in the center of their screen.
- Added _SystemEvents.XASystemEventsProcessList.by_displayed_name(str)_
- Added bulk methods to _XASoundList_.
- Added by_property methods to _XAApplicationList_.
- Added _XABase.XAURLList._
- Added _XAList.index(element)_, which functions the same as the index method of standard list objects.
- Added ability to quit menu bar apps from the terminal with control+C

**Bug Fixes/Changes**

- _XAMenuBar_ now automatically hides the dock icon of the application.
- _XANotesAttachment.url_ now return an XAURL instance.
- Fixed bulk getter methods on _XAList_ objects sometimes attempting to operate on empty lists and causing a TypeError. Bulk getter methods should now always return a list, even if empty.
- Fixed _XAFinderContainerList.entire_contents_ not returning anything. Now returns an instance of _XAFinderItemList_.
- Fixed _XAFinderListViewOptions.colums()_ returning instance of _XAFinderColumn_ instead of _XAFinderColumnList_.
- Fixed _XAFinderContainerList.container_window()_ failing to return a list of windows due to inaccessible object property.
- _XANoteList.by_creation_date()_, _XANoteList.by_modification_date()_,  _XANotesAttachmentList.by_creation_date()_, and _XANotesAttachmentList.by_modification_date()_ always returning None.
- Fixed _XANoteList.by_container()_ failing due to AttributeError.
- Fixed _XANotesAccountList.by_default_folder()_ failing due to AttributeError.
- Fixed _XANotesFolderList.by_container()_ failing due to AttributeError.
- Fixed _XANotesAttachmentList.by_container()_ failing due to AttributeError.
- Fixed _Reminders.XARemindersReminderList.container_ returning creation dates instead of containers (Now returns list of Reminders lists).
- Fixed setting _XAVLCDocument.path_ not working due to infinite recursion.
- Fixed _XARemindersApplication.new_list()_ failing due to trying to access ID property of proxy element.
- Fixed _XARemindersApplication.new_reminder()_ failing due to trying to set an unknown property key.
- Fixed _XARemindersAccountList.by_properties()_, _XARemindersListList.by_properties()_, and _XARemindersReminderList.by_properties()_ failing due to accessing unknown property key.
- Fixed _XARemindersListList.by_container()_ and XARemindersReminderList.by_container() always returning None.
- Fixed _XACalendarCalendarList.properties()_ returning a list of None elements.
- Fixed _XACalendarCalendarList.by_properties()_ failing due to AttributeError.
- Fixed _XACalendarCalendarList.description()_ returning a list of None elements.
- Fixed _XACalendarCalendarList.by_description()_ failing due to slight differences in memory locations.
- Fixed _XACalendarEventList.properties()_ returning a list of None elements.
- Fixed _XACalendarEventList.by_properties()_ failing due to AttributeError.
- Fixed _XACalendarEventList.by_description()_ always returning None.
- Fixed _XACalendarEvent.properties_ always returning None.
- Fixed _XACalendarEventList.duplicate()_, XACalendarEventList.duplicate_to(), and _XACalendarEventList.move_to()_ not saving events.
- Fixed _XACalendarAttachmentList.uuid()_ having a typo in its declaration.

**Deprecations**

- Importing various classes from the core PyXA module is now deprecated in favor of submodule imports
  - These classes are still available via PyXA.[class_name] for now, but importing them from their respective submodule will be necessary in the future. This is to minimize memory usage and load time when importing PyXA.
- _XAFinderApplication.delete_items()_ — Use _delete_item()_ instead.
- _XAFinderApplication.duplicate_items()_ — Use _duplicate_item()_ instead.
- _XAFinderApplication.recycle_items()_ — Use _recycle_item()_ instead.
- _XACalendarCalendar.week_events()_ — Use _events_in_range()_ instead.

**Removals**

- Removed logging using the Python logging module as it was causing issues with PyXA scripts bundled as Mac apps via py2app. NSLog is (minimally) used instead.
- _XACalendarCalendarList.calendar_identifier()_, _XACalendarCalendarList.by_calendar_identifier()_, and _XACalendarCalendar.calendar_identifier_; these methods/attributes have never worked correctly and cannot currently be fixed.

---

## [PyXA 0.1.1] - 2022-11-23

**Additions**

- Added various property setters that were missing previously.
- Added setter for the ‘properties’ property of many objects.
  - Setting this will update multiple properties at once.
  - Updates only the properties specified in the provided dictionary.
- Added _XAApplication.launch()_
- Added bulk attribute methods to _XABaseScriptable.XASBWindowList_
- Added _XABaseScriptable.XASBWindowList.uncollapse()_
- Added _XAList.extend(ls)_; functions the same as Python’s list.extend() method.
- Added _XAImage.symbol(name)_ for initializing images of system symbols (any symbol in the SF Symbols collection).
- Added _XAColor.hex_value_ for getting the HEX representation of a color.
- Added _XACalendarEventList.end_date()_.

**Changes**

- Reworked XAMenuBar structure and functionality; now follows OOP more closely.
  - Added _XAMenuBarMenu_, _XAMenuBarMenuItem_ classes
  - Added _XAMenuBar.new_menu_, _XAMenuBarMenu.new_item_, _XAMenuBarMenuItem.new_subitem_, _XAMenuBar.remove_menu_, _XAMenuBarMenu.remove_item_, _XAMenuBarMenuItem.remove_subitem_ methods
  - Kept previous functionality for the time being, but will remove it in the near future.
- Reduced XAObject instantiation time by moving property documentation into the property’s associated method(s), thus avoiding slow downs caused by on-init requests for property values. This provides a slight performance boost to many classes.
- Improved performance of XALists by reducing calls to PyObjC’s nsarray__len__() method.
- Improved performance of the Calendar and Reminders modules by utilizing lazy loading for translating between ScriptingBridge and EventKit objects.
- Improved performance of calling _PyXA.running_applications().windows()_ about 25% by better utilizing list comprehension.
- _XAApplication.activate()_ now launches the application if it is not already running, then activates it.
- Fixed _XABaseScriptable.XASBWindowList.collapse()_ not reliably collapsing every window in the list (fixed by adding success check and delay).
- Fixed _XAScriptEditorApplication.classes()_ not working due to misspelling.
- Fixed _XASystemEventsApplication.key_code()_ and _XASystemEventsApplication.key_stroke()_ not working; now uses CGEventCreateKeyboardEvent.
- Fixed setting _XAFinderApplication.selection_ to an XAFinderItemList object doing nothing.
- Adjusted the str and repr format of various classes, generally with the aim to balance execution time and utility.
  - Beyond a certain length, for example, many XALists will simply report their length instead of attempting to get information about each element
- Restructured XABase.py and PyXA.additions, moving some classes into addition modules. This is primarily to reduce the complexity of XABase.py, which is currently a headache to work with. There should be no impact on end-user scripts. The new structure (as of now) is as follows:
  - PyXA.additions
    - XALearn.py
      - XALSM
    - XASpeech.py
      - XASpeech
      - XASpeechRecognizer
      - XACommandDetector
    - XAUtils.py
      - SDEFParser
      - XAMenuBar
    - XAWeb.py
      - RSSFeed

**Deprecations**

- PyXA.PyXA.py
  - All classes and methods have been integrated into XABase.py. Use those instead.
- _XABase.XAMenuBar.add_menu()_ — Use the new_menu() method instead.
- _XABase.XAMenuBar.addItem()_ — Use the new_item() method of the XAMenuBarMenu class instead.
- _XABase.XAMenuBar.set_image()_ — Set the image attribute of XAMenuBarMenu and XAMenuBarMenuItem objects directly instead.
- _XABase.XAMenuBar.set_text()_ — Set the title attribute XAMenuBarMenu and XAMenuBarMenuItem objects directly instead.
- _QuickTimePlayer.XAQuickTimeWindow.set_property_ — Set the desired attribute directly instead.
- _MediaApplication.XAMediaWindow.collapseable_ — Use MediaApplication.XAMediaWindow.miniaturizable instead.
- _MediaApplication.XAMediaWindow.collapsed_ — Use MediaApplication.XAMediaWindow.miniaturized instead.
- _Finder.XAFinderApplication.directory(path)_ — Use the XAFinderApplication.folders() method with a filter instead.

**Images**
<img width="504" alt="An image of a menu bar app for copying colors in various representations created with the new XAMenuBar structure." src="https://user-images.githubusercontent.com/7865925/203693101-5ad833e9-f897-4080-97c2-d611e5bc8afe.png">

---

## [PyXA 0.1.0] - 2022-10-30

Note: This version of PyXA requires Python 3.11.

**Additions**

- _XALSM_ — A class for convenient text classification using latent semantic mapping
  - Added save() method for saving LSM models to the disk.
  - Added load() method for loading LSM models from the disk.
  - Added add_category() method for easily adding new categories to the mapping.
  - Added add_data() method for adding categories and training data.
  - Added add_text() method for adding training data.
  - Added categorize_query() method for mapping a string to a category using the built model.
- _XABase.XAApplicationPicker_ — A class for having users selected an application from a menu
  - Works similarly to XAFolderPicker and XAFilePicker.
- _XABase.XATextDocumentList_ — General class for text documents that provides several bulk functions
  - Has the same methods and attributes as the DocumentList class previously found in the TextEdit module
- _XABase.XAVideo_ — Initial support for working with videos in PyXA
  - Added reverse() method for reversing videos (this takes some time)
  - Added save() method for saving modified videos to the disk
  - Added show_in_quicktime() method for opening videos in QuickTime
- New features for _XABase.XAImage_ and _XABase.XAImageList_:
  - Added additional non-mutable information attributes has_alpha_channel, is_opaque, and color_space_name.
  - Added ability to control image properties using mutable attributes for gamma, vibrance, tint, temperature, white_point, highlight, and shadow.
  - Added an open() method to open one or more images from files or URLs.
  - Added a save() method to save images to the disk.
  - Added several filter methods for easy image adjustments, e.g. gaussian_blur(), pixellate(), invert(), and bloom(), among others.
  - Added auto_enhance() method to automatically apply suggested image enhancements, e.g. correct red-eye.
  - Added several distortion methods such as bump(), pinch(), and twirl().
  - Added several transformation methods such as flip_horizontally(), rotate(), crop(), scale(), and pad().
  - Added composition methods such as overlay_image(), overlay_text(), stitch_horizontally(), and additive_composition().
  - Added extract_text() and image_from_text() to read text from images and turn text into images, respectively.
  - All of these methods are implemented in both XAImage and XAImageList, with the latter offering some performance benefits
- New features for _XABase.XAColor_:
  - Added several class methods, such as white(), black(), and orange(), for instantiating common XAColor objects.
  - Added make_swatch() method for making a solid color image of a specified size
  - Added clipboard-codability
- New features for _XABase.XAList_:
  - Added additional filtering methods such as equalling(), not_equalling(), not_containing(), beginning_with(), ending_with(), greater_than(), less_than(), and between()
  - Added count() method for counting elements of XALists that pass a key function
  - Added support for checking membership in XALists using the “in” keyword
- New methods for _XABase.XASound_:
  - Added trim() method for adjusting the length of sounds via PyXA
  - Added save() method for saving modified sounds to the disk
  - Added information attributes such as num_sample_frames, sample_rate, and duration
- New features fro _XABase.XAText_:
  - Added working sentences() method to get a list of sentences in a text document.
  - Added methods for tagging tokens by sentiment, lemma, language, and part of speech
- _PyXA Additions_ — Modules that utilize other packages alongside PyXA and PyObjC features to provide useful automation features.
  - Additions.XAWeb — A module for internet-related PyXA additions.
    - RSS Features
      - Additions.XAWeb.RSSReader — A class for fetching items from RSS feeds
      - Additions.XAWeb.RSSItem, Additions.XAWeb.RSSItemList — Classes for interacting with fetched RSS items, e.g. to view metadata, access the contained content, or extract URLs from link tags
      - Additions.XAWeb.RSSItemContent, Additions.XAWeb.RSSItemContentList — Classes for interacting with the content of RSS items, e.g to retrieve all images and links within in their full-featured PyXA representation
- Pythonic properties and setters for every class
- Added local debug logging
- _Support for New Applications_
  - Adobe Acrobat Reader
  - Amphetamine
  - Bike
  - CardHop
  - Flow
  - Image Events
  - iTerm
  - RStudio
  - Spotify
  - System Events

**Changes**

- _XABase.XAList_
  - Now correctly responds to negative indexing.
  - Filtering now works with (more) non-string values.
  - Push() now correctly returns either the added element(s) or None — before, it would return a location reference that could end up incorrectly pointing to another element.
- _XABase.XAURL_ / _XABase.XAPath_
  - Now tries to prepend necessary schemes if no valid is present when the object is initialized.
- _XABase.XAColor_
  - red(), green(), and blue() methods now create instances of pure red, pure green, and pure blue colors, respectively. The red_value, green_value, and blue_value attributes now take on the previous functionality of these methods. Other value-getting methods have been transitioned to attributes as well.
- In general, modules have been tweaked to support more data types when calling methods, where appropriate.
- Many behind-the-scenes changes have been made to support faster execution.
- Documentation throughout several modules has been significantly improved, especially for the iWork suite.

**Deprecations**

- _PyXA.application()_ — Use the PyXA.Application class instead.
- _XABase.XATextDocument.set_text()_ — Directly set the XABase.XATextDocument.text attribute instead
- Providing NSData as the data parameter when initializing an XABase.XAList object — Pass the NSData as the image_reference parameter instead.
- _XAiWorkItem.rotate()_, in all forms — Set the rotate attribute instead.

**Removals**

- _XABase.XAImage.name_ — Removed due to lack of use case
- _TextEdit.XATextEditDocument.copy()_ — Deprecated in 0.0.8, now fully removed

**Direction for Next Release**

- Performance improvements
- Code reorganization
- Full macOS Ventura Support
- Integrate Finder classes with System Events classes

---

## [PyXA 0.0.9] - 2022-08-25

**Additions**

- XASpotlight class — ability to search for files on the disk using Spotlight
  - Returns a list of XAURL objects
  - Supports searching by string, date, date range, and combinations of those
  - Supports searching by custom predicate
  - _XASpotlight.run()_ — Runs the search
  - _XASpotlight.show_in_finder()_ — Shows the search in Finder (but might not display the exact same results)
- XANotification — ability to display notifications, currently supported by osascript
  - _XANotification.display()_ — Displays the notification
- XACommandDetector — ability to listen for specific spoken commands and react accordingly
  - _XACommandDetector.on_detect()_ — Adds or replaces a command to listen for and associates it with a specified function
  - _XACommandDetector.listen()_ — Begins listening for all specified commands
- XASpeechRecognizer — ability to listen for spoken queries matching some condition and react accordingly
  - _XASpeechRecognizer.on_detect()_ — Adds a rule that executes some method when a query meets the conditions of the rule
  - _XASpeechRecognizer.listen()_ — Begins listening for a query, continues until a rule returns True
- XASpeech — ability to speak text with customizable voices, volume, and speaking rate
  - _XASpeech.speak()_ — Speaks the specified text or outputs the spoken audio to an AIFF file
  - _XASpeech.voice()_ — Lists available voice names
- XAMenuBar — ability to create menus on the system menu/status bar + ability to add items to those menus that execute specified functions when clicked
  - Supports images
  - Supports runtime changes to menu display parameters (text, image)
  - Automatically adds “Quit” item to menus
  - _XAMenuBar.add_menu()_ — Adds a new menu
  - _XAMenuBar.add_item()_ — Adds a new item to a menu
  - _XAMenuBar.set_image()_ — Sets the image displayed for a menu or menu item
  - _XAMenuBar.set_text()_ — Sets the text displayed for a menu or menu item
  - _XAMenuBar.display()_ — Displays the menu bar, keeping it displayed until the program is quit
  - Examples:
    - <img width="606" alt="JWSTMenuBar" src="https://user-images.githubusercontent.com/7865925/186786102-cbdc3f5c-d48f-4d2c-b962-c4974bca03ae.png">
    - <img width="256" alt="CPUMonitor" src="https://user-images.githubusercontent.com/7865925/186786134-607435a9-457b-460d-bba6-54c7d6945121.png">
- New methods for AppleScript class
  - _AppleScript.insert()_ — Inserts a string, list of strings, or script object as a line entry in the current script
  - _AppleScript.pop()_ — Removes and returns the line at the specified index of the script
  - _AppleScript.load()_ — Loads an AppleScript .scpt file as a runnable AppleScript object
  - _AppleScript.save()_ — Saves the current script to the specified file path
  - _AppleScript.extract_result_data()_ — Attempts to extract string data from an execution result dictionary
- New features for XALocation class
  - _XALocation.current_location_ property — Holds the user’s current location object
- PyXA.scriptable_applications variable — Holds a list of the currently supported applications
- Setters for properties on many classes
- Support for new applications
  - Fantastical
  - OmniOutliner
  - Script Editor
- Documentation for many more classes and methods

**Changes**

- All new classes going forward will utilize @property and @x.setter decorators; existing classes will be updated over the course of the next few updates.
- Several methods have been converted to attributes of the parent class
  - _XATerminalApplication.current_tab()_
  - _XATerminalWindow.selected_tab()_
  - _XATerminalTab.current_settings()_
- XAColor can now be instantiated using _PyXA.XAColor()_
- Various small bug fixes

**Deprecations**

- _XAObject.has_element()_ — Perform this check manually instead.
- _XAObject.set_element()_ — Set the element attribute directly instead.

**Removals**

- _PyXA.open_url()_ — Deprecated in v0.0.5, now completely replaced by XAURL class
- _PyXA.get_clipboard()_, _PyXA.get_clipboard_strings()_, _PyXA.set_clipboard()_ — Deprecated in v0.0.5, now completely replaced by XAClipboard class
- _PyXA.run_application()_ — Deprecated in v0.0.5, now completely replaced by AppleScript class

---

## [PyXA 0.0.8] - 2022-08-18

**Additions**

- _XAProtocols.py_ — Contains definitions for high-level classes that can be subclassed to indicate availability of functionality to other aspects of PyXA. For example, XAClipboard utilizes the get_clipboard_representation() method of classes subclassed from XAClipboardCodable.
  - Current protocols:
    - XAShowable
    - XASelectable
    - XADeletable
    - XAPrintable
    - XACloseable
    - XAClipboardCodable
    - XACanOpenPath
    - XACanPrintPath
- Expanded functionality for _XABase.XAClipboard_ via _XAProtocols.XAClipboardCodable protocol_
        - All Python literals can be set as the content of the clipboard
        - Many PyXA objects can be set as the content of the clipboard
- New properties and methods for _XABase.XAURL_
  - base_url — The base/host portion of the URL, e.g. `www.google.com`
  - parameters — The parameter portion of the URL, e.g. `?query=“Hi”`
  - scheme — The scheme portion of the URL, e.g. `http://`/
  - fragment — The fragment portion of the URL, e.g. `#example`
  - html — The HTML code for the webpage at the URL
  - title — The title of the webpage at the URL
  - extract_text() -> List[str] — Gets the visible text of the webpage at the URL
  - extract_images() -> List[XAImage] — Gets all images on the webpage at the URL
- _XABase.XAImage.show_in_preview()_ — Shows the TIFF representation of the image in Preview
- User input classes — Currently use NSAppleScript to create the views that users are accustomed to. Might use custom-created windows and views in the future.
  - _XABase.XADialog_
  - _XABase.XAMenu_
  - _XABase.XAFilePicker_
  - _XABase.XAFolderPicker_
  - _XABase.XAFileNameDialog_
- Support for several new applications
  - Numbers
  - Alfred
  - Drafts
  - Hammerspoon
  - VLC

**Changes**

- Several methods that actually represent properties have been corrected to be object properties.
  - XAApplication.front_window, XAScriptableApplication.front_window
  - XAMusicApplication.current_track
  - XASafariApplication.current_document
- Added SaveOption and PrintErrorHandling enums to XABaseScriptable.XASBApplication

**Deprecations**

- Using property dictionaries to filter XALists is now deprecated functionality. Use the _XABase.XAList.filter()_ method instead.
- _XABase.XAList.containing()_ — Use the _XABase.XAList.filter()_ method instead.
- _XABase.XAObject.has_element_properties()_ — all elements now have a properties dictionary, even if it is empty.
- _XABase.XAClipboard.set_contents()_ — Directly set the _XABase.XAClipboard.contents_ property instead.
- _TextEdit.XATextEditDocument.copy()_ - Use the _XABase.XAClipboard_ class instead.

**Removals**

- _XABase.XAHasElements_, _XABaseScriptable.XAHasScriptableElements_, and all associated methods — Functionalities completely replaced by XAList. No impact to existing scripts.
- _XABase.XAAcceptsPushedElements_ — Functionality replaced by XAList. No impact to existing scripts.
- _XABase.XACanConstructElement_ — Functionality replaced by per-application make() methods. No impact to existing scripts.
- _XABase.XAShowable_, _XABase.XACanOpenPath_, _XABase.XASelectable_, _XABase.XADeletable_, _XABase.CanPrintPath_, _XABase.XACloseable_ — Moved to XAProtocols. No impact to existing scripts.
- _XABase.xa_url()_ — Deprecated in v0.0.5. Now completely replaced by XAURL.
- _XABase.xa_path()_ — Deprecated in v0.0.5. Now completely replaced by XAPath.

**Full Changelog**: <https://github.com/SKaplanOfficial/PyXA/compare/v0.0.7...v0.0.8>

---

## [PyXA 0.0.7] - 2022-08-12

This pre-release version expands fast enumeration over list objects to the Music, TV, Contacts, and Terminal apps, improves documentation throughout the project, and adds an introductory tutorial.

**Full Changelog**: <https://github.com/SKaplanOfficial/PyXA/compare/v0.0.6...v0.0.7>

---

## [PyXA 0.0.6] - 2022-08-02

This pre-release version includes performance improvements, support for several new applications (Maps, Font Book, Pages, Stocks, QuickTime Player), expanded support for UI scripting, and updates throughout other areas to improve PyXA's overall utility and stability.

**Full Changelog**: <https://github.com/SKaplanOfficial/PyXA/compare/v0.0.5...v0.0.6>

---

## [PyXA 0.0.5] - 2022-07-14

This is the first pre-release version of PyXA [available on PyPi.org](https://pypi.org/project/mac-pyxa/) and installable via `pip install mac-pyxa`.

Features:

- Support for Automator, Calculator, Calendar, Console, Contacts, Dictionary, Finder, Keynote, Mail, Messages, Music, Notes, Photos, Preview, Reminders, Safari, Shortcuts, System Preferences, Terminal, TextEdit, and TV applications
- Support for native alert dialogs and color pickers via XAAlert and XAColorPicker, respectively
- Additional classes for interacting with the system clipboard (XAClipboard), URLs (XAURL), paths (XAPath), images (XAImage), colors (XAColor), locations (XALocation)
- Fast enumeration over lists of scriptable objects via the XAList class
- Support for executing AppleScript script strings via the AppleScript class
