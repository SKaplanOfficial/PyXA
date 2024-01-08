Device Interaction
==================

PyXA offers a _Devices_ addition that provides a simple interface to your device's hardware such as its camera, microphone, and screen.

Device Classes
--------------

The following device classes are available:

- :class:`~PyXA.Additions.Devices.XACamera` - for capturing photos and videos
- :class:`~PyXA.Additions.Devices.XAMicrophone` - for recording audio
- :class:`~PyXA.Additions.Devices.XAScreen` - for capturing screenshots and screen recordings

An overview of each class is provided below.

Camera
---------------------------

The :class:`~PyXA.Additions.Devices.XACamera` class provides two methods: one to capture photos (:func:`~PyXA.Additions.Devices.XACamera.capture`) and another to record videos (:func:`~PyXA.Additions.Devices.XACamera.record`). Both methods return an instance of the corresponding PyXA class—either :class:`~PyXA.XABase.XAImage` or :class:`~PyXA.XABase.XAVideo`—that can be used alongside other areas of PyXA.

For example, to capture a photo and save it to the desktop, you could use the following code:

.. code-block:: python

  import PyXA
  import os

  cam = PyXA.XACamera()
  img = cam.capture()
  homedir = os.path.expanduser("~")
  img.save(f"{homedir}/Desktop/test.png")

You can combine this with other PyXA features to create powerful automations. For example, you could use the :class:`~PyXA.Additions.Speech.XASpeech` class to speak any text detected in the image:

.. code-block:: python

  import PyXA

  cam = PyXA.XACamera()
  img = cam.capture()
  img_text = img.extract_text()

  PyXA.XASpeech(img_text).speak()

Microphone
----------

The :class:`~PyXA.Additions.Devices.XAMicrophone` class provides a single method, :func:`~PyXA.Additions.Devices.XAMicrophone.record`, that records audio from the device's microphone and returns an instance of the :class:`~PyXA.XABase.XAAudio` class.

For example, to record 5 seconds of audio and play it back, you could use the following code:

.. code-block:: python

  import PyXA
  import os

  mic = PyXA.XAMicrophone()
  homedir = os.path.expanduser("~")
  recording = mic.record(f"{homedir}/Downloads/test.wav", 5)
  recording.play()

Screen
------

PyXA's :class:`~PyXA.Additions.Devices.XAScreen` class provides methods for capturing screenshots and screen recordings. Each method returns either a :class:`~PyXA.XABase.XAImage` or :class:`~PyXA.XABase.XAVideo` object. The available methods are:

- :func:`~PyXA.Additions.Devices.XAScreen.capture` - captures a screenshot
- :func:`~PyXA.Additions.Devices.XAScreen.capture_rect` - captures a screenshot of a specific area of the screen
- :func:`~PyXA.Additions.Devices.XAScreen.capture_window` - captures a screenshot of a specific window
- :func:`~PyXA.Additions.Devices.XAScreen.record` - records a screen recording