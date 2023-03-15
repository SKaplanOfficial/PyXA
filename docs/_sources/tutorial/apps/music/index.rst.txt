Music Module Overview
=====================

.. contents:: Table of Contents
   :depth: 3
   :local:

The entirety of Music's scripting interface is available via PyXA.

Music Tutorials
###############
There are currently no tutorials for the Music module.

Music Examples
##############
The examples below provide an overview of the capabilities of the Music module.

Example 1 - Playback Control
****************************

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Application("Music")

   # Play/Pause/Stop/Resume
   app.play()
   app.pause()
   app.stop()
   app.playpause()

   # Fast-forward/Rewind
   app.fast_forward()
   app.rewind()
   app.resume()

Example 2 - Add Current Track to a Playlist
*******************************************

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Music()

   # Gather info about current track
   title = app.current_track.name
   artist = app.current_track.artist
   album = app.current_track.album

   # Save track to library
   library = app.sources().by_name("Library")
   app.current_track.duplicate(library)

   # Get the saved track object
   saved_track = app.tracks().filter("name", "==", title).filter("artist", "==", artist).by_album(album)

   # Add track to playlist
   playlist = app.playlists().by_name("test")
   saved_track.move(playlist)

Example 3 - Make a Playlist of Tracks in a Given Genre
******************************************************

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Music()

   # Get a list of all soundtrack tracks
   soundtracks = app.tracks().filter("genre", "==", "Soundtrack")

   # Create a new playlist
   prototype = app.make("playlist", {"name": "Soundtracks"})
   new_playlist = app.playlists().push(prototype)

   # Add soundtracks to the new playlist
   new_playlist.add_tracks(soundtracks)

For all classes, methods, and inherited members of the Music module, see the :ref:`Music Module Reference` and :ref:`Media Application Reference`.