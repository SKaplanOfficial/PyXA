Terminal Module Overview
========================

The Terminal module enables control over Terminal.app from within Python, including the ability to run Terminal script and receive the execution return value.

Terminal Examples
#################

Example 1 - Using Terminal methods and attributes
*************************************************

This example showcases many of the methods and attributes available for use in the Terminal module.

.. code-block:: python

    import PyXA
    app = PyXA.application("Terminal")

    # Get information about the current tab
    tab = app.current_tab
    print(tab.custom_title)
    print(tab.processes)
    print(tab.number_of_rows, tab.number_of_columns)
    # Terminal
    # (
    #     login,
    #     "-zsh",
    #     python
    # )
    # 24 80

    # Set tab properties
    tab.custom_title = "Testing 1 2 3"
    tab.number_of_rows = 50
    tab.title_displays_custom_title = True

    # Run scripts and utilize return values
    value = app.do_script("ls", return_result=True)
    print("Number of items:", len(value["stdout"].split("\n")) - 1)

    value = app.do_script("ping www.google.com -c 1", return_result=True)
    if "1 packets received" in value["stdout"]:
        print("Online!")
    else:
        print("Offline!")

    # Modify settings
    settings = tab.current_settings
    settings.background_color = PyXA.XAColor(255, 0, 0)
    settings.font_size = 10

Terminal Resources
##################
- `Terminal User Guide - Apple Support <https://support.apple.com/guide/terminal/welcome/mac>`_

For all classes, methods, and inherited members of the Terminal module, see the :ref:`Terminal Module Reference`.