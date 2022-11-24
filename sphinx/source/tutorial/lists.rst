Working With Lists
==================

PyXA uses the :class:`~PyXA.XABase.XAList` class to enable batch operations and provide fast enumeration over scriptable objects. This wrapper class behaves like a regular list in many situations; for example, when working with an :class:`~PyXA.XABase.XAList` object, you can use indices, slices, and iterators as you would normally. To avoid sending numerous Apple Events and causing excessive delays, :class:`~PyXA.XABase.XAList` objects lazily evaluate their members -- that is, they don't retrieve their member objects until you request an object at a specific index. At that point, they send a single Apple Event, obtain a reference to the desired scriptable object, and wrap it in a PyXA-compatible class.

This approach allows you to quickly access large lists of scriptable objects such as all notes, songs, or photos. As evidence: the list-fetching portion of script below takes only 64 milliseconds to complete on my machine despite me having well over 2000 notes, 2000 songs, and 8000 photos. 

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    music_app = PyXA.Application("Music")
    notes_app = PyXA.Application("Notes")
    photos_app = PyXA.Application("Photos")
    
    time_1 = datetime.now()
    tracks = music_app.tracks()
    notes = notes_app.notes()
    photos = photos_app.media_items()
    time_2 = datetime.now()
    
    print(time_2 - time_1)
    # 0:00:00.063908

In addition to speed, `XALists` provide batch operation capabilities. When working with a list of PyXA objects, all properties of those objects can be accessed via method calls on the list wrapper class. For example, you can retrieve the plaintext of every note, the name of every Music track, or the filename of every photo by just calling the appropriate method on the associated list object. The example below illustrates the latter.

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    photos_app = PyXA.Application("Photos")
    
    time_1 = datetime.now()
    photos = photos_app.media_items()
    print(photos.filename())
    time_2 = datetime.now()
    
    print(time_2 - time_1)
    # ['IMG_0497.PNG', 'IMG_4341.JPG', 'IMG_2482.JPG', 'IMG_0488.JPG', ...]
    # 0:00:00.691846

As you can see, this operation is also very speedy, even for large photo collections. Using multithreaded enumeration, PyXA sends many Apple Events requesting the filename property for each photo. Since each Apple Event involves a retrieving a single unicode property, without requiring any recursive queries, the entire operation can be done in well under a second. Note that the photo objects still have yet to be fully evaluated at this point.

Forcing Evaluation
------------------

To force evaluation of an object, request it by index or by using the :func:`~PyXA.XABase.XAList.first` or :func:`~PyXA.XABase.XAList.last` methods, or by a specialized :func:`~PyXA.XABase.XAList.by_property` method (such as :func:`PyXA.apps.PhotosApp.XAPhotosMediaItemList.by_filename()`). The code below showcases each of these approaches:

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    photos_app = PyXA.Application("Photos")
    
    time_1 = datetime.now()
    photos = photos_app.media_items()
    
    photo_1 = photos[0]
    photo_2 = photos[-1]
    photo_3 = photos.at(0)
    photo_4 = photos.at(-1)
    photo_5 = photos.first
    photo_6 = photos.last
    photo_7 = photos.by_filename("IMG_0497.PNG")
    time_2 = datetime.now()
    
    print(time_2 - time_1)
    # 0:00:01.201319

This script takes a bit longer than the previous ones due to the many requests for scriptable object references. Still, the overall process remains far faster than if we didn't do lazy evaluation at all.

For comparison, if we force evaluation on each object in a list by iterating over the list, we find that getting a property value for each object takes a significant amount of time. The script below uses the iterative approach to get the name of each note, and it took almost half a minute on my machine. Attempting this form of batch operation on 8000+ photos would take an even longer time.

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    notes_app = PyXA.Application("Notes")
    
    time_1 = datetime.now()
    notes = notes_app.notes()
    names = []
    for note in notes:
        names.append(note.name)
    time_2 = datetime.now()
    
    print(names)
    print(time_2 - time_1)
    # ['Note 1', 'Note 2', ...]
    # 0:00:33.767063

Filters
-------

Filter methods can be used to narrow down the list of objects, thereby making iteration more feasible. The script below uses a filter to narrow the list of all tracks down to just the tracks whose artist is Adele.

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    music_app = PyXA.Application("Music")
    
    time_1 = datetime.now()
    tracks = music_app.tracks().filter("artist", "==", "Adele")
    time_2 = datetime.now()
    
    print(tracks.name())
    print(time_2 - time_1)
    # ['Hello', 'Chasing Pavements', 'Skyfall', ...]
    # 0:00:00.076569

PyXA provides several convenience methods for retrieving lists matching simple filters. These methods include :func:`~PyXA.XABase.XAList.equalling`, :func:`~PyXA.XABase.XAList.not_equalling`, :func:`~PyXA.XABase.XAList.containing`, :func:`~PyXA.XABase.XAList.beginning_with`, :func:`~PyXA.XABase.XAList.ending_width`, :func:`~PyXA.XABase.XAList.greater_than`, :func:`~PyXA.XABase.XAList.less_than`, and :func:`~PyXA.XABase.XAList.between`. Each of these methods returns an :class:`~PyXA.XABase.XAList` object containing the items matching the corresponding filter. The code below shows how many of the methods can be used.

.. code-block:: Python

    import PyXA
    notes = PyXA.Application("Notes")
    print(app.notes().containing("body", "Hello").name())
    print(app.notes().containing("title", "Hello").name())
    # ['Note 1', 'Example Note', 'Another Note']
    # ['Hello, world!']

    print(notes.notes().greater_than("creationDate", date(2022, 8, 30)).name())
    print(notes.notes().not_equalling("shared", True).name())
    # ["Aug. 31st Note"]
    # ["Note 1", "Note 2", "Note 3", ...]

    music = PyXA.Application("Music")
    print(music.tracks().between("playedCount", 10, 20))
    print(music.tracks().not_containing("name", "a"))
    # <<class 'PyXA.apps.Music.XAMusicTrackList'>['Irresistible', 'Absent Minded (Piano Version)', "Say You Won't Let Go", ...]>
    # <<class 'PyXA.apps.Music.XAMusicTrackList'>['Hello', 'Rolling in the Deep', ...]>

    photos = PyXA.Application("Photos")
    print(photos.media_items().equalling("favorite", True))
    print(photos.media_items().beginning_with("name", "P"))
    # <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItemList'>['CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001', ...]>
    # <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItemList'>['0BA38221-C569-4ACF-A3BD-967CB87EB7EB/L0/001']>

You can also use :func:`~PyXA.XABase.XAList.by_property` to retrieve a single object from the list based on its property values. :func:`~PyXA.XABase.XAList.containing` will match the first object whose property value contains a given value, while :func:`~PyXA.XABase.XAList.by_property` will match the first object whose property value exactly matches the given value. The example below shows these methods at work.

.. code-block:: Python

    import PyXA
    from datetime import datetime
    
    music_app = PyXA.Application("Music")
    
    time_1 = datetime.now()
    tracks = music_app.tracks()
    track_1 = tracks.containing("name", "yfal")
    track_2 = tracks.by_property("genre", "pop")
    name_1 = track_1.name
    name_2 = track_2.name
    time_2 = datetime.now()
    
    print(name_1)
    print(name_2)
    print(time_2 - time_1)
    # Skyfall
    # Take On Me
    # 0:00:00.144339

Bulk Actions
------------

In addition to improving the efficiency of automation workflows aiming to get values from numerous scriptable objects, `~PyXA.XABase.XAList` objects are a quick and convenient way to execute actions on many objects at a time. The available actions vary by object type. The script below uses this strategy to implement a rudimentary dark mode for Safari by setting the background of all tabs to black and their body text to white.

.. code-block:: Python

    import PyXA
    safari_app = PyXA.Application("Safari")
    tabs = safari_app.front_window.tabs()
    tabs.do_javascript("document.body.style.backgroundColor = 'black'; document.body.style.textColor = 'white';")


Adding New Elements
-------------------

The :func:`~PyXA.XABase.XAList.push` method allows you to add new elements to a scriptable object list, thereby creating a scriptable object. This can be used to create new notes, new tabs, new playlists, and so on.

.. code-block:: Python

    import PyXA
    safari_app = PyXA.Application("Safari")
    new_doc = safari_app.make("tab", {"URL": "http://www.google.com"})
    safari_app.front_window.tabs().push(new_doc)