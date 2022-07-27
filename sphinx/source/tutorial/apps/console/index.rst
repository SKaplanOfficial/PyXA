Console Module Overview
=======================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA has fully supports all scripting features of Console.app, but there is minimal support (from Apple) in the first place in that regard. Future versions of PyXA might explore expanding the feature offering through UI scripting, utilization of Objective-C frameworks, and other means.

Console Tutorials
#################
There are currently no tutorials for the Console module.

Examples
########
.. The examples below provide an overview of the capabilities of the Chromium module. They do not provide any output. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Chromium Tutorials`).

Example 1 - Coming Soon
****************************************

An example will be added soon.

.. .. code-block:: python
..    :linenos:

..    import PyXA
..    from time import sleep

..    # Open URL in new tab
..    app = PyXA.application("Chromium")
..    app.activate()
..    app.open("http://apple.com")

..    # Wait for tab to finish loading
..    tab = app.front_window().tabs().last()
..    while tab.loading:
..       sleep(0.1)

..    # Save the tab's content
..    tab.save("/Users/exampleuser/Downloads/apple-site")

Console Resources
#################
- `Console User Guide - Apple Support <https://support.apple.com/guide/console/welcome/mac>`_

Console Classes and Methods
###########################

Classes
*******
   
.. autosummary:: PyXA.apps.Console
   :nosignatures:

   ~PyXA.apps.Console.XAConsoleApplication

XAConsoleApplication Methods
****************************
   
.. autosummary:: PyXA.apps.Console.XAConsoleApplication
   :nosignatures:

   ~PyXA.apps.Console.XAConsoleApplication.select_device

For all classes, methods, and inherited members on one page, see the :ref:`Console Module Reference`