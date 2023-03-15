Running AppleScripts
====================

PyXA has a dedicated :class:`~PyXA.XABase.AppleScript` class which supports several useful features for working with AppleScript scripts. This allows you to run any AppleScript you desire, thereby opening up the entirety of AppleScript's capabilities to Python.


Creating and Running AppleScript Code
-------------------------------------

The easiest way to run AppleScript code on-the-fly is to instantiate an :class:`~PyXA.XABase.AppleScript` object with the text of the script as an argument. You can run the script using the :func:`~PyXA.XABase.AppleScript.run` method, as seen in the code below. The script won't run until you tell it to, allowing you to modify the script after instantiation but before execution.

.. code-block:: Python

    import PyXA
    PyXA.AppleScript("tell application \"Safari\" to activate").run()

Note that if your script includes quoted text, you need to properly escape the quotation marks if using the above format. You can also use triple quotes to preserve the string's formatting, which allows you to use unescaped quotes and has the added benefit of preserving line breaks. As seen in the example below, this provides an easy way to create and run multiline AppleScripts.

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript("""tell application "Pages"
       set the miniaturized of window 1 to true
   end tell
   """)
   script.run()

You can also modify :class:`~PyXA.XABase.AppleScript` objects after instantiation using the :func:`~PyXA.XABase.AppleScript.add`, :func:`~PyXA.XABase.AppleScript.insert`, and :func:`~PyXA.XABase.AppleScript.pop` methods. These provide the ability to dynamically add and remove lines from the script. You can then use Python's control blocks (such as if/elif/else) to create powerful combinations of Python and AppleScript that utilize the capabilities of both languages. The script below shows a basic implementation of this. The code creates an :class:`PyXA.apps.Notes.XANotesApplication` application object to interact with the Notes app and sets up and empty :class:`~PyXA.XABase.AppleScript` object. We then use combinations of the :func:`~PyXA.XABase.AppleScript.add`, :func:`~PyXA.XABase.AppleScript.insert`, and :func:`~PyXA.XABase.AppleScript.pop` methods to construct an AppleScript script. Note how we dynamically construct the AppleScript code based on whether a note with a specific name exists, which we check from within Python. While this particular script is not very useful, you could use this capability to generate lengthy AppleScripts that are specialized to a user's system, for example. 

.. code-block:: Python

   import PyXA
   app = PyXA.Application("Notes")
   script = PyXA.AppleScript()
   script.add("tell application \"Notes\"")
   script.add("end tell")
   script.add("error")
   script.pop()
   
   if "PyXA Ideas" in app.notes().name():
      script.insert(1, "set note1 to the note \"PyXA Ideas\"")
      script.add("show note1")
   else:
      script.add("error \"Could not find the note!\"")
   
   script.run()
   print(script)
   # <<class 'PyXA.XABase.AppleScript'>['tell application "Notes"', 'set note1 to the note "PyXA Ideas"', 'show note1', 'end tell']>


Reading Execution Results
-------------------------

The script contained within an :class:`~PyXA.XABase.AppleScript` object will execute upon calling the :func:`~PyXA.XABase.AppleScript.run` method, returning a dictionary containing the execution return value of the script. This allows you to further intertwine Python logic with AppleScript. The returned dictionary is structured as follows:

.. code-block::

   {
      'string': 'Example.txt',
      'int': 0,
      'bool': True,
      'float': 0.0,
      'date': None,
      'file_url': file:///Users/exampleUser/Documents/Example.txt,
      'type_code': 6881357,
      'data': {length = 108, bytes = 0x4d006900 6e006500 63007200 61006600 ... 54007500 62006500 },
      'event': <NSAppleEventDescriptor: 'utxt'("Example.txt")>
   }

This structure provides a convenient way to access the information contained in an execution return value, especially when that data has a well-defined type (such as a string, integer, boolean, float, or date). When the return value is a single string, for example, you can access it by getting the "string" key of the result dictionary, as shown in the example below:

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript("""tell application "Safari" to get the name of window 1""")
   result = script.run()
   print(result["string"])
   # Running AppleScripts — PyXA 0.0.9 documentation

When dealing with other forms of data, such as a list of Safari tab names or the list of IDs of all chats in Messages, you can use the :func:`~PyXA.XABase.AppleScript.parse_result_data` function to extract the text and numbers from the raw Apple Event data. This function takes the results dictionary, isolated the NSAppleEventDescriptor, loops through each sub-descriptor, gets the string value of the descriptor or creates a tuple of the sub-descriptor's values, then returns a list containing the value or tuple associated with each entry. The first code snippet below shows how to get the names of all Safari tabs, the second shows how to list the ID property of all chats in Messages, and the third shows how to create PyXA objects from the returned data.

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript("""tell application "Safari"
      set tabNames to {}
      repeat with t in tabs of window 1
         set end of tabNames to (name of t)
      end repeat
      return tabNames
   end tell
   """)
   result = script.run()
   print(PyXA.AppleScript.parse_result_data(result))
   # ['Google', 'Bing', 'Apple']

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript("""tell application "Messages"
      get chats
   end tell
   """)
   result = script.run()
   print(PyXA.AppleScript.parse_result_data(result))
   # [('ID', 'iMessage;-;+11234567890'), ('ID', 'iMessage;-;+11234567891'), ...]

.. code-block:: Python

   import PyXA
   app = PyXA.Application("Messages")
   script = PyXA.AppleScript("""tell application "Messages"
      get chats
   end tell
   """)
   result = script.run()
   entries = PyXA.AppleScript.parse_result_data(result)
   chats = [app.chats().by_id(entry[1]) for entry in entries]
   print(chats)
   # [<<class 'PyXA.apps.Messages.XAMessagesChat'><<class 'PyXA.apps.Messages.XAMessagesParticipantList'>['Example Person']>>, ...]

The example above are not particularly useful, as PyXA already provides faster and more straightforward ways to accomplish these tasks. For example, the third example, re-written in PyXA code, is:

.. code-block:: Python

   import PyXA
   app = PyXA.Application("Messages")
   print([x for x in app.chats()])

Still, the ability to convert between AppleScript return values and PyXA object types may be useful in some situations.


Loading External Scripts
------------------------
PyXA provides a way to load existing AppleScript .scpt files using the :func:`~PyXA.XABase.AppleScript.load` method. Once loaded, the script can be treated like any other :class:`~PyXA.XABase.AppleScript` object.

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
   print(script.run())

You can even modify the script in the same ways as before:

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
   script.add(3, "set note1 to the note \"PyXA Ideas\"")
   script.insert(4, "show note1")
   print(script.run())

This allows you to run your existing AppleScripts from Python. In combination with the ability to read execution results (see `Reading Execution Results`), the ability to load scripts makes PyXA a powerful yet convenient way to interface between Python and AppleScript, without losing access to your existing library of AppleScript automations.


Saving Scripts
--------------
Once you've created and/or modified a script, you can save it to a .scpt file using the :func:`~PyXA.XABase.AppleScript.save` method. If the script was initially loaded from a file, you can call :func:`~PyXA.XABase.AppleScript.save` without any arguments -- the script will be saved to the existing .scpt file. You can also provide a file path as an argument to instruct PyXA to save the script to a particular destination. Note that the script is compiled before it is saved, so specifying a path to anything other than a .scpt file will result in an unreadable document.

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript.load("/Users/steven/Downloads/Example.scpt")
   script.insert(2, "delay 2")
   script.insert(3, "set the miniaturized of window 1 to true")
   script.save()

.. code-block:: Python

   import PyXA
   script = PyXA.AppleScript("""
      tell application "Safari"
         activate
      end tell
   """)
   >>> script.save("/Users/exampleUser/Downloads/Example.scpt")

