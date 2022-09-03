Flow Module Overview
====================

The Fantastical module provides access to Fantastical's features from within PyXA, making use of both the application's scripting dictionary as well as its URL scheme.

Flow Examples
#############

Example 1 - Run session only while a specific app is open
*********************************************************

.. code-block:: python

    import PyXA
    from time import sleep

    flow = PyXA.Application("Flow")
    in_session = False

    while True:
        apps = PyXA.running_applications().localized_name()
        if "Notes" in apps and not in_session:
            flow.start()
            in_session = True
        elif "Notes" not in apps:
            flow.stop()
            in_session = False
        sleep(1)