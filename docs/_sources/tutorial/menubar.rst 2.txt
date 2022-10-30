Add Items to the Menu Bar
=========================

The Basics
##########

PyXA provides a straightforward way to add interactive items to the top menu bar of your Mac. Using the :class:`~PyXA.XABase.XAMenuBar` class, you can add new menus, attach items and actions to them, and customize them in just a few lines of code. For example, the four line code below creates a new menu titled "Hello" and places it on the right side of the menu bar, to the left of any existing items.

.. code-block:: Python

    import PyXA
    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_menu("Hello!")
    menu_bar.display()

We haven't added any interactivity yet, but PyXA already handles the task of adding a "Quit" option to the menu. Helpful! When you run this code, you should see something along these lines (though your icons may be in a different order):

.. image:: ../_static/assets/HelloMenu.png

Note that, unlike many other PyXA features, your menu bar script will stay running until you specific tell it to quit. This allows you to create create customizations to your menu bar that persist throughout your work session. If you set the script to run on startup, you can create a persistent modification to the menu bar in this way.

The script above creates menu button that currently doesn't do anything. To add interactivity, use the :func:`~PyXA.XABase.XAMenuBar.add_item` method to associate a menu item with some method. Continuing our example, let's add a menu item that, when clicked, prints "Hi" to the Terminal. This change can be made by adding a single line, as seen below:

.. code-block:: Python

    import PyXA
    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_menu("Hello!")
    menu_bar.add_item(menu="Hello!", item_name="Print Hi", method=lambda : print("Hi"))
    menu_bar.display()

The :func:`~PyXA.XABase.XAMenuBar.add_item` method associates a method to a menu item with a given name, then attaches that menu item to the menu with the specified title. If no menu exists with the specified title, then a new menu is automatically created, and the item is added to it. The above code, when run, produces the following menu:

.. image:: ../_static/assets/PrintHi.png

The code above uses a lambda function to specify our method; this is a convenient way to write the code concisely, but you can also pass in a normal function name to achieve the same effect. The code above can also be expressed as:

.. code-block:: Python

    import PyXA

    def print_hi():
        print("Hi")

    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_menu("Hello!")
    menu_bar.add_item(menu="Hello!", item_name="Print Hi", method=print_hi)
    menu_bar.display()

.. image:: ../_static/assets/PrintHiImage.png

You can easily add additional menus and menu items, further extending the functionality of your menu bar. A few examples are provided below.

Example 1 - Application Launcher
********************************

.. code-block:: Python

    import PyXA
    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_item(menu="Apps", item_name="Safari", method=lambda : PyXA.application("Safari").activate())
    menu_bar.add_item("Apps", "Messages", lambda : PyXA.application("Messages").activate())
    menu_bar.add_item("Apps", "Notes", lambda : PyXA.application("Notes").activate())
    menu_bar.add_item("Apps", "Shortcuts", lambda : PyXA.application("Shortcuts").activate())
    menu_bar.add_item("Apps", "Discord", lambda : PyXA.application("Discord").activate())
    menu_bar.add_item("Apps", "GitHub Desktop", lambda : PyXA.application("GitHub Desktop").activate())
    menu_bar.add_item("Apps", "Visual Studio Code", lambda : PyXA.application("Visual Studio Code").activate())
    menu_bar.display()

Example 2 - Emoji Bookmarks
***************************

.. code-block:: Python

    import PyXA
    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_item("🌦", "Weather.gov", lambda : PyXA.XAURL("https://www.weather.gov").open())
    menu_bar.add_item("🌦", "Weather.com", lambda : PyXA.XAURL("https://weather.com/weather/today").open())
    menu_bar.add_item("🌦", "Accuweather.com", lambda : PyXA.XAURL("https://www.accuweather.com").open())

    menu_bar.add_item("📖", "Develop in Swift", lambda : PyXA.XAURL("https://books.apple.com/us/book/develop-in-swift-fundamentals/id1511184145").open())
    menu_bar.add_item("📖", "NYTime", lambda : PyXA.XAURL("https://www.nytimes.com").open())
    menu_bar.add_item("📖", "New York Public Library", lambda : PyXA.XAURL("https://www.nypl.org").open())

    menu_bar.add_item("🦊", "Random Fox Image", lambda : PyXA.XAURL("https://randomfox.ca").open())
    menu_bar.add_item("🦊", "Random Duck Image", lambda : PyXA.XAURL("https://generatorfun.com/random-duck-image").open())
    menu_bar.add_item("🦊", "Random Cat Image", lambda : PyXA.XAURL("https://genrandom.com/cats/").open())
    menu_bar.display()

Example 3 - Application Controller
**********************************

.. code-block:: Python

    import PyXA

    def minimize_all():
        apps = PyXA.running_applications()
        for app in apps:
            app.windows().collapse()

    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_item("⚙️", "Minimize all windows", minimize_all)
    menu_bar.add_item("⚙️", "Hide all applications", lambda : PyXA.running_applications().hide())
    menu_bar.add_item("⚙️", "Quite all applications", lambda : PyXA.running_applications().terminate())
    menu_bar.display()


Customization
#############

You can customize your menu bar items by adding images to them, as well as by adjusting the width and height of the images. Additional customization options might be added in the future.

To display an image on the menu bar, create an :class:`~PyXA.XABase.XAImage` object and set it as the image argument when calling :func:`~PyXA.XABase.XAMenuBar.add_menu`. The example below shows this in action -- and it even draws the image from an online source (though you could just as easily use a local source instead). When calling :func:`~PyXA.XABase.XAMenuBar.add_menu`, you can also specify the `img_width` and `img_height` arguments to customize the size of the image.

.. code-block:: Python

    import PyXA
    img = PyXA.XAImage("https://www.nasa.gov/sites/default/files/thumbnails/image/main_image_star-forming_region_carina_nircam_final-5mb.jpg")
    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_menu("Menu 1", image=img, img_width=100)
    menu_bar.display()

.. image:: ../_static/assets/JWSTMenuBar.png

You can update the image during runtime using the :func:`~PyXA.XABase.XAMenuBar.set_image` method, which takes as parameters the menu name, the image object, and an optional width and height. The code below displays a random fox image in the menu bar and allows users to click a "Random Fox" menu item to retrieve a new image.

.. code-block:: Python

    import PyXA
    import requests

    menu_bar = PyXA.XAMenuBar()

    def random_fox_link() -> str:
        response = requests.get("https://randomfox.ca/floof/")
        json_data = response.json()
        return json_data["image"]

    def update_image():
        img = PyXA.XAImage(random_fox_link())
        menu_bar.set_image("Menu 1", img)

    img = PyXA.XAImage(random_fox_link())
    menu_bar.add_menu("Menu 1", image=img, img_width=80, img_height = 80)
    menu_bar.add_item("Menu 1", "Random Fox", update_image)
    menu_bar.display()

You can also add images to menu items in a similar manner. When calling :func:`PyXA.XABase.XAMenuBar`, provide an `image` argument alongside optional `img_width` and `img_height` arguments. The example below creates three menu items, each with an image attached. While the width and height for a menu in the menu bar is limited to the available space, there is no such restriction for items within menus -- you can set the image to be as large or as small as you want.

.. code-block:: Python

    import PyXA
    import requests

    icon1 = PyXA.XAImage("/Users/exampleUser/Documents/icon1.jpg")
    icon2 = PyXA.XAImage("/Users/exampleUser/Documents/icon2.jpg")
    icon3 = PyXA.XAImage("/Users/exampleUser/Documents/icon3.jpg")

    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_item("Menu 1", "Item 1", image=icon1)
    menu_bar.add_item("Menu 1", "Item 2", image=icon2, img_width=300)
    menu_bar.add_item("Menu 1", "Item 3", image=icon3, img_height=500)
    menu_bar.display()

.. image:: ../_static/assets/MenuItemImages.png

Another way to customize your menus is by modifying the text that they display. By default, menus and menu items will display the name that they are given upon creation, but you can modify the displayed text using the :func:`~PyXA.XABase.XAMenuBar.set_text` method. With this method, similar to when setting images, you identify a menu or menu item by referencing its name, then you provide a new text string for the item to display. The example below uses this feature to create a near-live CPU monitor in the menu bar:

.. code-block:: Python

    import PyXA
    import psutil
    import threading
    from time import sleep

    menu_bar = PyXA.XAMenuBar()
    menu_bar.add_menu("CPU")

    def update_display():
        while True:
            message = "CPU Usage: " + str(psutil.cpu_percent(4)) + "%"
            menu_bar.set_text("CPU", message)
            sleep(0.05)

    cpu_monitor = threading.Thread(target=update_display)
    cpu_monitor.start()
    menu_bar.display()

.. image:: ../_static/assets/CPUMonitor.png