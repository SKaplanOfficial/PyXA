Shortcuts Module Overview
=========================

.. contents:: Table of Contents
   :depth: 3
   :local:

Most of Shortcuts.app's scripting interface is available via PyXA, however some significant features are currently limited by sandboxing constraints. PyXA is able to interact with existing shortcuts, including run them, but it is currently unable to create new shortcuts or shortcut folders. That said, it is possible to use Shortcuts links to install new shortcuts. It would be feasible to use functional, atomically constructed shortcuts (i.e. each shortcut accomplishes a single task and returns a transformed value) to construct larger sequences of actions, effectively re-instituting an ability to create shortcuts. For now, that is left as an exercise for PyXA users. Future versions of PyXA may utilize the Shortcuts URI scheme, in combination with the Intents framework, to re-implement these features in a more straightforward way.

Shortcuts Tutorials
###################
There are currently no tutorials for the Shortcuts module.

Shortcuts Examples
##################
The examples below provide an overview of the capabilities of the Shortcuts module. They do not provide any output. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Shortcuts Tutorials`).

Example 1 - Run shortcuts and receive their return values
*********************************************************

The example below activates Chromium.app, opens Apple's website in a new tab, waits for the tab to finish loading, then saves the site's resources (e.g. HTML, CSS, JavaScript, and images) to a location on the disk. Note the use of a full URL, beginning with "http", as well as a full file path, beginning with "/". Both a full URL and full file path are necessary in order for this example to operate successfully. 

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Application("Shortcuts Events")

   # Get shortcuts by name
   sqrt = app.shortcuts().by_name("sqrt(x)")
   sin = app.shortcuts().by_name("sin(x)")

   # Run sqrt function, get first entry in output array
   root = sqrt.run(81)[0]
   print(root)

   # Run sin function, get first entry in output array
   sin_root = sin.run(root)[0]
   print(sin_root)

Example 2 - Combine shortcut output with Python
***********************************************

This example highlights how you can intertwine PyXA, Shortcuts, and Python to carry out more complex processes. The example below uses a shortcut to obtain the source HTML of the Google homepage, then uses Python's tempfile module alongside PyXA's :func:`PyXA.Safari.XASafariApplication.open` method to display a local HTML file in the browser.

.. code-block:: python
   :linenos:

   import PyXA
   import tempfile

   # Get the source of webpage, using a shortcut
   app = PyXA.Application("Shortcuts Events")
   s1 = app.shortcuts().by_name("Get HTML")
   source = s1.run("http://google.com")[0]

   # Create a temporary HTML file
   temp = tempfile.NamedTemporaryFile(suffix=".html")
   temp.write(bytes(source, "UTF-8"))

   # Open the HTML file
   PyXA.application("Safari").open(temp.name)
   sleep(0.5)
   temp.close()

Shortcuts Resources
###################
- `Shortcuts for macOS User Guide - Apple Support <https://support.apple.com/guide/shortcuts-mac/welcome/mac>`_

For all classes, methods, and inherited members of the Shortcuts module, see the :ref:`Shortcuts Module Reference`.