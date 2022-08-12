Tutorial
========

Installation
------------

Before you get started with PyXA, you'll need to install it. The easiest way to do so is through Pip using the following command:

.. code-block:: bash

   python -m pip install mac-pyxa

Alternatively, you can install PyXA on a per-project basis by cloning the GitHub repository in the project's main directory.

Basic Usage
-----------

Let's walk through some examples to introduce you to the ins and outs of PyXA. Create a new folder in a location of your choice and name it `PyXA Examples`. Then, in that folder, create a new file called `basics.py`, then open the file in your favorite code editor. If you have the Visual Studio Code `code` command installed and enabled, the following command accomplishes all of the above in one fell swoop:

.. code-block:: bash

   mkdir "PyXA Examples" && cd "PyXA Examples" && touch basics.py && code basics.py

Now, let's design our first PyXA automation workflow. Suppose we want to write a script that gets the URL of the current Safari tab and prints it (to the Terminal/console). To do this, we first import the PyXA library, then we obtain a reference to the Safari application, a reference to Safari's frontmost window, and finally a reference to the currently displayed tab. From there, we retrieve and print the URL of the tab. The script is thus:

.. code-block:: Python

   import PyXA
   print(PyXA.application("Safari").front_window.current_tab.url)

Save this script to `basics.py`. To test the workflow, open `https://www.google.com` in a new Safari tab, then run `basics.py` in your Terminal. You should see the following:

.. code-block:: bash

   % python basics.py
   https://www.google.com

Try visiting different sites in Safari and re-running the script. As you navigate to different sites, you'll see that the printed URL changes accordingly.

This particular workflow is fairly straightforward, but it is nonetheless useful to compare its syntax to that of AppleScript and JXA. In AppleScript, the same workflow would look like this:

.. code-block:: AppleScript

   tell application "Safari"
      return URL of the current tab of window 1
   end tell

And the equivalent JXA syntax would be:

.. code-block:: JavaScript

   (function() {
      return Application('Safari').windows()[0].currentTab.url()
   })();

As you can see, the syntax of PyXA closely follows the syntax of JXA while remaining true to the standard conventions of Python. Most notably, multi-word names for variables and methods use the Pythonic snake_case format instead of camelCase. For example, as seen above, PyXA uses `current_tab` while JXA uses `currentTab`. Another difference is that PyXA prefers object properties while JXA blurs the line between properties and methods. In PyXA, the properties listed in an application's scripting dictionary are referenced using the dot notation for object properties, and actions on objects are executed via method calls. PyXA also includes properties and methods beyond those described in scripting dictionaries on an application-specific basis.

Like AppleScript and JXA, PyXA's syntax is often flexible, allowing multiple ways to accomplish the same goal. All of the following code samples are valid ways to create the same workflow as above.

.. code-block:: Python

   import PyXA
   print(PyXA.application("Safari").windows()[0].current_tab.url)

.. code-block:: Python

   import PyXA
   print(PyXA.application("Safari").current_document.url)

.. code-block:: Python

   import PyXA
   print(PyXA.application("Safari").documents()[0].url)

The approach you use will depend one your goals for any given workflow as well as the kind(s) of inputs the workflow should be able to handle.

Let's make our workflow more useful by having it save the URL to a new note. To do this, we'll need a reference to the Notes app. We then need to tell the Notes app to create a new note with the URL as the note's content. We can temporarily store the URL in a variable to make our code more readable. The PyXA script for this is as follows:

.. code-block:: Python

   import PyXA
   current_url = PyXA.application("Safari").front_window.current_tab.url
   PyXA.application("Notes").new_note(current_url)

If you run this workflow and go to the Notes app, you'll see that a new note has been created containing the current tab's URL in bold typeface. This is already a more useful automation, but we can improve it by making Notes automatically activate and show the newly created note. To do this, we can simply call the new note object's `show()` method:

.. code-block:: Python

   import PyXA
   current_url = PyXA.application("Safari").front_window.current_tab.url
   PyXA.application("Notes").new_note(current_url).show()

When you run this, the Notes app will open to newly created note containing the current Safari tab's URL. Cool! Let's make another change. Right now, the URL is used as the title for the note, but it would be nice if the title reflected the title of the webpage. Since we need to retrieve multiple properties from the current tab, we should store a reference to it in a variable to keep our script running efficiently. We'll retrieve the `URL` property of the current tab as we did before, and now we'll also retrieve the `name` property. We can then specify the title and content of the new note by passing two arguments to the `new_note()` method. Another improvement we'll make is turning the URL into an actually clickable link by surrounding it with HTML anchor tags. Our script thus becomes:

.. code-block:: Python

   import PyXA
   current_tab = PyXA.application("Safari").front_window.current_tab
   current_url = "<a href=" + current_tab.url + ">" + current_tab.url + "</a>"
   current_name = current_tab.name
   PyXA.application("Notes").new_note(current_name, current_url).show()

With that, our script is complete! You can run the script from your Terminal at any time, but you might want to save the workflow as an executable for greater convenience. The easiest way to do this is to add a `shebang` to the top of the script that instructs the Terminal to run the code using the Python interpreter:

.. code-block:: Python
   
   #!/usr/bin/env python

   import PyXA
   current_tab = PyXA.application("Safari").front_window.current_tab
   current_url = "<a href=" + current_tab.url + ">" + current_tab.url + "</a>"
   current_name = current_tab.name
   PyXA.application("Notes").new_note(current_name, current_url).show()

You then need to remove the .py extension from the script and grant the file execution privileges. Both these actions can be accomplished using the following Terminal command:

.. code-block:: bash

   mv basics.py basics && chmod +x basics

When you double click on the script from within Finder, or when you run `./basics` in the Terminal, the workflow should execute as it did before. If you want, you can `change the icon of the file`_ to give your automation a distinct look. You can then move the file to your desktop, the dock, or anywhere you want.


.. Controlling Application Windows
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Creating Documents
.. ^^^^^^^^^^^^^^^^^^






.. Advanced Usage
.. --------------

Application Modules
===================

First-Party Application Modules
-------------------------------

.. toctree::
   :maxdepth: 1

   apps/index
   apps/automator/index
   apps/calculator/index
   apps/calendar/index
   apps/console/index
   apps/contacts/index
   apps/dictionary/index
   apps/finder/index
   apps/fontbook/index
   apps/keynote/index
   apps/mail/index
   apps/maps/index
   apps/messages/index
   apps/music/index
   apps/notes/index
   apps/pages/index
   apps/photos/index
   apps/preview/index
   apps/quicktimeplayer/index
   apps/reminders/index
   apps/safari/index
   apps/shortcuts/index
   apps/stocks/index
   apps/systempreferences/index
   apps/terminal/index
   apps/textedit/index
   apps/tv/index

Third-Party Application Modules
-------------------------------

.. toctree::
   :maxdepth: 1

   apps/chromium/index

.. _change the icon of the file: https://support.apple.com/en-gb/guide/mac-help/mchlp2313/mac
