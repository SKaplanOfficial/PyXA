VLC Module Overview
===================

VLC Examples
############

Example 1 - Working with VLC methods and attributes
***************************************************

This example provides a general overview of the functionalities supported by the VLC module. Additional examples can be found in the code reference for this module.

.. code-block:: python
   :linenos:
   
    import PyXA
    app = PyXA.application("VLC")

    # Open or get (without opening) files and URLs
    app.open("/Users/exampleUser/ExampleFile.m4v")
    app.open("https://upload.wikimedia.org/wikipedia/commons/transcoded/e/e1/Black_Hole_Merger_Simulation_GW170104.webm/Black_Hole_Merger_Simulation_GW170104.webm.1080p.vp9.webm")
    app.get_url("https://upload.wikimedia.org/wikipedia/commons/transcoded/e/e1/Black_Hole_Merger_Simulation_GW170104.webm/Black_Hole_Merger_Simulation_GW170104.webm.1080p.vp9.webm")

    # Control playback
    app.stop()
    app.play()
    app.previous()
    app.next()
    app.step_forward()
    app.step_backward()
    app.current_time = app.current_time + 5

    # Control volume
    app.volume_up()
    app.volume_down()
    app.mute()
    app.audio_volume = 256

    # Control the VLC window
    app.fullscreen()
    app.fullscreen_mode = False
    app.front_window.bounds = (0, 0, 500, 500)
    app.zoomed = True

    # Utilize information about playback
    file = app.path_of_current_item
    file.show_in_finder()

    if app.audio_volume > 256:
        app.audio_volume = 256


VLC Resources
#############
- `TextEdit User Guide - Apple Support <https://support.apple.com/guide/textedit/welcome/mac>`_

For all classes, methods, and inherited members of the VLC module, see the :ref:`VLC Module Reference`.