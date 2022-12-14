Getting User Input
==================
PyXA provides several ways to get user input via dialogs, menus, and other familiar means. You can still use Python's :func:`input` method to get keyboard input, and you can use Python's built-in support for commandline arguments to get input in that way as well. Additional input methods (such as detecting keystrokes and/or mouseclicks in other applications) will be added in a future version of PyXA, but other packages exist that already offer such functionality.

Alerts
------

.. code-block:: Python

    import PyXA
    response = PyXA.XAAlert(
        title = "Alert!",
        message = "",
        style = PyXA.XAAlertStyle.INFORMATIONAL,
        buttons = ["Ok", "Cancel"]
    ).display()
    print(response)
    # 1000


Dialogs
-------

.. code-block:: Python

    import PyXA
    response = PyXA.XADialog(
        text = "This is a dialog",
        title = "Notice",
        buttons = ["Ok", "Cool", "Thanks"],
        icon = "caution",
    ).display()
    print(response)
    # Cool

.. code-block:: Python

    import PyXA
    response = PyXA.XADialog(
        text = "What is your name?",
        title = "What is your name?",
        buttons = ["Continue"],
        default_button = "Continue",
        icon = "note",
        default_answer = ""
    ).display()
    print("Your name is", response[1])
    # Your name is Steven

.. code-block:: Python

    import PyXA
    response = PyXA.XADialog(
        text = "Enter the secret",
        title = "Super Secret",
        buttons = ["Continue"],
        default_button = "Continue",
        icon = "note",
        default_answer = "",
        hidden_answer = True
    ).display()
    print("The secret message was", response[1])
    # The secret message was 42



Menus
-----

.. code-block:: Python

    import PyXA
    response = PyXA.XAMenu(
        menu_items = ['Option 1', 'Option 2', 'Option 3'],
        title = "Select Item",
        prompt = "Select an item",
        default_items = ['Option 2'],
        ok_button_name = "Okay",
        cancel_button_name = "Cancel",
        multiple_selections_allowed = False,
        empty_selection_allowed = False
    ).display()
    print(response)
    # Option 2


File and Folder Pickers
-----------------------

.. code-block:: Python

    import PyXA
    response = PyXA.XAFilePicker(
        prompt = "Choose File",
        types = ["png"],
        default_location = "/",
        show_invisibles = False,
        multiple_selections_allowed = False,
        show_package_contents = False
    ).display()
    print(response)
    # <<class 'PyXA.XABase.XAPath'>file:///Users/ExampleUser/Desktop/Example.png>

.. code-block:: Python

    import PyXA
    response = PyXA.XAFolderPicker(
        prompt = "Choose Folder",
        default_location = "/",
        show_invisibles = False,
        multiple_selections_allowed = True,
        show_package_contents = False
    ).display()
    print(response)
    # [<<class 'PyXA.XABase.XAPath'>file:///Applications/>, <<class 'PyXA.XABase.XAPath'>file:///Library/>]


File Name Dialogs
-----------------

.. code-block:: Python

    import PyXA
    response = PyXA.XAFileNameDialog(
        prompt = "Choose Folder",
        default_name = "New File",
        default_location = "/Users/Shared",
    ).display()
    print(response)
    # <<class 'PyXA.XABase.XAPath'>file:///Users/Shared/New%20File>


Color Pickers
-------------

.. code-block:: Python

    import PyXA
    response = PyXA.XAColorPicker(
        style = PyXA.XAColorPickerStyle.CRAYONS
    ).display()
    print(response)
    # <<class 'PyXA.XABase.XAColor'>r=1.0, g=0.8323456645, b=0.4732058644, a=1.0>


Command Detectors
-----------------

.. code-block:: Python

    import PyXA

    def open_google():
        PyXA.XAURL("https://google.com").open()

    detector = PyXA.XACommandDetector()
    detector.on_detect("go to Google", open_google)
    detector.on_detect("go to Bing", lambda : PyXA.XAURL("https://bing.com").open())
    detector.listen()


If you want to detect an exact command and display the standard macOS Voice Control interface, use a :class:`PyXA.XABase.XACommandDetector` object. If you want to detect whether a user's spoken input passes a certain rule, or if you want the command detection to occur without displaying an graphical interface, use :class:`PyXA.XABase.XASpeechRecognizer`.

Speech Recognizers
------------------

.. code-block:: Python

    import PyXA
    listener = PyXA.XASpeechRecognizer()
    result = listener.listen()
    if result == "Hi":
        PyXA.speak("Hey!")

.. code-block:: Python

    import PyXA
    import re

    listener = PyXA.XASpeechRecognizer({
        lambda s: s.lower() == "open google": lambda _: PyXA.XAURL("https://google.com").open(),
    })
    regex = re.compile(r'^(Open|Go to|Site|Jump to|Show me) (b|B)ing')
    listener.on_detect(lambda s: regex.match(s) != None, lambda _: PyXA.XAURL("https://bing.com").open())
    result = listener.listen()

.. code-block:: Python

    import PyXA

    def detect_website_query(query: str) -> bool:
        """Detects queries of the form "Go to [website name]".

        :param query: The query to assess
        :type query: str
        :return: True if the query matches the form "Go to [website name]" for any of the supported websites
        :rtype: bool
        """
        site_names = ["google", "bing", "duckduckgo", "yahoo"]
        return query.startswith("Go to ") and any([query.lower().endswith(x) for x in site_names])

    def go_to_website(query: str) -> PyXA.XAURL:
        """Opens a website specified in a query of the form "Go to [website name]".

        :param query: The query to respond to
        :type query: str
        :return: The url as a PyXA XAURL object
        :rtype: PyXA.XAURL
        """
        site = query[6:]
        url = PyXA.XAURL("https://" + site + ".com")
        url.open()
        return url

    listener = PyXA.XASpeechRecognizer({
        detect_website_query: go_to_website,
    })

    result = listener.listen()
    print(result)
    # <<class 'PyXA.XABase.XAURL'>https://Bing.com>