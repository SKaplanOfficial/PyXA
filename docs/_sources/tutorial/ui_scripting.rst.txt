UI Scripting
============

PyXA supports using System Events to script the UI of otherwise non-scriptable applications. In fact, PyXA uses this functionality to provide scripting features for several applications, including Maps and Stocks.

The process for scripting an application's UI starts with getting its window object, from which you can call various methods, such as :func:`~PyXA.apps.SystemEvents.XASystemEventsWindow.groups` and :func:`~PyXA.apps.SystemEvents.XASystemEventsWindow.toolbars`, to obtain lists of UI elements. These methods provide access to all UI element types listed in the System Events scripting dictionary. Lists of elements obtained in this fashion are instances of :class:`~PyXA.apps.SystemEvents.XASystemEventsUIElementList`, a subclass of :class:`~PyXA.XABase.XAList`. You can use bulk methods on a list of UI elements to retrieve information about the list's contents. For example, you can call :func:`~PyXA.apps.SystemEvents.XASystemEventsUIElementList.object_description` to get the accessibility or role description of all elements in the list. List filtration methods such as :func:`~PyXA.apps.SystemEvents.XASystemEventsUIElementList.by_object_description` allow you to efficiently access elements with particular property values.

Retrieving an element from an :class:`~PyXA.apps.SystemEvents.XASystemEventsUIElementList` object will return a instance of :class:`~PyXA.apps.SystemEvents.XASystemEventsUIElement`. You can then obtain the properties of the UI element via the object's attributes. Upon doing so, the reference to the AppleScript scripting object will be evaluated, causing one or more Apple Events to be sent. This behavior makes it possible to quickly traverse the UI hierarchy without sending unnecessary Apple Events and causing slowdowns.

Once you have a reference to a specific UI element, you can call methods such as :func:`~PyXA.apps.SystemEvents.XASystemEventsButton.click` to carry out actions on that element, or you can obtain a list of actions by calling :func:`~PyXA.apps.SystemEvents.XASystemEventsUIElement.actions`. Call :func:`~PyXA.apps.SystemEvents.XASystemEventsAction.perform` to perform a particular action.

An example of this process is provided below.

.. code-block:: python

    from time import sleep
    import PyXA

    podcasts = PyXA.Application("Podcasts")

    # Get the list of podcast playback controls
    playback_buttons = podcasts.front_window.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[2].groups()[0].groups()[0].buttons()

    # Get buttons by property value
    rewind_button = playback_buttons.by_object_description("Rewind")
    play_button = playback_buttons.by_object_description("Play")
    skip_button = playback_buttons.by_object_description("Skip")

    # Click the buttons
    play_button.click()
    sleep(1)
    skip_button.click()
    sleep(1)
    rewind_button.click()

In this example, we obtain a list of buttons by traversing the UI hierarchy of the Podcasts app to reach the specific group containing the rewind, play, and skip forward buttons at the top of the window. You can use macOS's built-in `Accessibility Inspector` application to help identify the element hierarchy. Once we have the list of buttons, we obtain references to each individual button according to its object description. We then call the :func:`~PyXA.apps.SystemEvents.XASystemEventsButton.click` method of each button to observe its effect.