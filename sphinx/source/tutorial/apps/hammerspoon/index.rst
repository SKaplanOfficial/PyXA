Hammerspoon Module Overview
===========================

The Hammerspoon module provides the ability to run Hammerspoon Lua scripts from within PyXA. To do this, simply call the :func:`~PyXA.apps.Hammerspoon.XAHammerspoonApplication.execute_lua_code` method and supply a Lua script as an argument. You can then utilize the value returned by the Lua script in your Python program.

.. code-block:: Python

    import PyXA
    app = PyXA.application("hammerspoon")
    result = app.execute_lua_code("""
        app = hs.appfinder.appFromName("Finder")
        window = app:mainWindow()
        return window:title()
    """)
    print(result)
    # Recents

For all classes, methods, and inherited members of the Hammerspoon module, see the :ref:`Hammerspoon Module Reference`.