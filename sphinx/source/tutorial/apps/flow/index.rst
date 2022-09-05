Flow Module Overview
====================

The Flow module allows you to programmatically control Flow's timer sessions from within your Python scripts.

Flow Examples
#############

Example 1 - Run session only while a specific app is open
*********************************************************

One possible use case of the Flow module is automatically starting Flow sessions based on the context of the system. For example, you might want to start a Flow session when you first open Notes, then only allow the session counter to continue as long as you're using the Notes app (in other words, if you get distracted and wander over to YouTube, the session pauses until you get back on track). The code below shows how to use PyXA to implement this use case.

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

Based on this code, you can create scripts for managing context-based Flow sessions informed by many metrics--or as few as you need.

Flow Resources
##############
- `Flow API/Scripts <https://flowapp.info/docs/#docs-api>`_