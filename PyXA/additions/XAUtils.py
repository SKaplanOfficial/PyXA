""".. versionadded:: 0.1.1

A collection of classes for interacting with macOS features in various ways.
"""

import AppKit
import xml.etree.ElementTree as ET
from typing import Union, Callable, Any
from PyObjCTools import AppHelper
from PyXA import XABase

class SDEFParser():
    def __init__(self, sdef_file: Union['XABase.XAPath', str]):
        if isinstance(sdef_file, str):
            sdef_file = XABase.XAPath(sdef_file)
        self.file = sdef_file #: The full path to the SDEF file to parse

        self.app_name = ""
        self.scripting_suites = []

    def parse(self):
        app_name = self.file.path.split("/")[-1][:-5].title()
        xa_prefix = "XA" + app_name

        tree = ET.parse(self.file.path)

        suites = []

        scripting_suites = tree.findall("suite")
        for suite in scripting_suites:
            classes = []
            commands = {}

            ### Class Extensions
            class_extensions = suite.findall("class-extension")
            for extension in class_extensions:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + extension.attrib.get("extends", "").title()
                class_comment = extension.attrib.get("description", "")

                ## Class Extension Properties
                class_properties = extension.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Extension Elements
                class_elements = extension.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Extension Responds-To Commands
                class_responds_to_commands = extension.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })

            ### Classes
            scripting_classes = suite.findall("class")
            for scripting_class in scripting_classes:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + scripting_class.attrib.get("name", "").title()
                class_comment = scripting_class.attrib.get("description", "")

                ## Class Properties
                class_properties = scripting_class.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Elements
                class_elements = scripting_class.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Responds-To Commands
                class_responds_to_commands = scripting_class.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })


            ### Commands
            script_commands = suite.findall("command")
            for command in script_commands:
                command_name = command.attrib.get("name", "").lower().replace(" ", "_")
                command_comment = command.attrib.get("description", "")

                parameters = []
                direct_param = command.find("direct-parameter")
                if direct_param is not None:
                    direct_parameter_type = direct_param.attrib.get("type", "")
                    if direct_parameter_type == "specifier":
                        direct_parameter_type = "XABase.XAObject"

                    direct_parameter_comment = direct_param.attrib.get("description")

                    parameters.append({
                        "name": "direct_param",
                        "type": direct_parameter_type,
                        "comment": direct_parameter_comment
                    })

                if not "_" in command_name and len(parameters) > 0:
                    command_name += "_"

                command_parameters = command.findall("parameter")
                for parameter in command_parameters:
                    parameter_type = parameter.attrib.get("type", "")
                    if parameter_type == "specifier":
                        parameter_type = "XAObject"

                    parameter_name = parameter.attrib.get("name", "").lower().replace(" ", "_")
                    parameter_comment = parameter.attrib.get("description", "")

                    parameters.append({
                        "name": parameter_name,
                        "type": parameter_type,
                        "comment": parameter_comment,
                    })

                commands[command_name] = {
                    "name": command_name,
                    "comment": command_comment,
                    "parameters": parameters
                }

            suites.append({
                "classes": classes,
                "commands": commands
            })

        self.scripting_suites = suites
        return suites

    def export(self, output_file: Union['XABase.XAPath', str]):
        if isinstance(output_file, XABase.XAPath):
            output_file = output_file.path

        lines = []

        lines.append("from typing import Any, Callable, Union")
        lines.append("\nfrom PyXA import XABase")
        lines.append("from PyXA.XABase import OSType")
        lines.append("from PyXA import XABaseScriptable")

        for suite in self.scripting_suites:
            for scripting_class in suite["classes"]:
                lines.append("\n\n")
                lines.append("class " + scripting_class["name"].replace(" ", "") + "List:")
                lines.append("\t\"\"\"A wrapper around lists of " + scripting_class["name"].lower() + "s that employs fast enumeration techniques.")
                lines.append("\n\tAll properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.")
                lines.append("\n\t.. versionadded:: " + XABase.VERSION)
                lines.append("\t\"\"\"")

                lines.append("\tdef __init__(self, properties: dict, filter: Union[dict, None] = None):")
                lines.append("\t\tsuper().__init__(properties, " + scripting_class["name"].replace(" ", "") + ", filter)")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef " + property["name"] + "(self) -> list['" + property["type"].replace(" ", "") + "']:")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn list(self.xa_elem.arrayByApplyingSelector_(\"" + property["name"] + "\"))")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef by_" + property["name"] + "(self, " + property["name"] + ") -> '" + scripting_class["name"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Retrieves the " + scripting_class["comment"] + "whose " + property["name"] + " matches the given " + property["name"] + ".\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.by_property(\"" + property["name"] + "\", " + property["name"] + ")")


                lines.append("")
                lines.append("class " + scripting_class["name"].replace(" ", "") + ":")
                lines.append("\t\"\"\"" + scripting_class["comment"] + "\n\n\t.. versionadded:: " + XABase.VERSION + "\n\t\"\"\"")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\t@property")
                    lines.append("\tdef " + property["name"] + "(self) -> '" + property["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.xa_elem." + property["name"] + "()")

                for element in scripting_class["elements"]:
                    lines.append("")
                    lines.append("\tdef " + element["name"].replace(" ", "") + "(self, filter: Union[dict, None] = None) -> '" + element["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Returns a list of " + element["name"] + ", as PyXA objects, matching the given filter.")
                    lines.append("\n\t\t.. versionadded:: " + XABase.VERSION)
                    lines.append("\t\t\"\"\"")
                    lines.append("\t\tself._new_element(self.xa_elem." + element["name"] + "(), " + element["type"].replace(" ", "") + "List, filter)")

                for command in scripting_class["responds-to"]:
                    if command in suite["commands"]:
                        lines.append("")
                        command_str = "\tdef " + suite["commands"][command]["name"] + "(self, "

                        for parameter in suite["commands"][command]["parameters"]:
                            command_str += parameter["name"] + ": '" + parameter["type"] + "', "

                        command_str = command_str[:-2] + "):"
                        lines.append(command_str)

                        lines.append("\t\t\"\"\"" + suite["commands"][command]["comment"])
                        lines.append("\n\t\t.. versionadded:: " + XABase.VERSION)
                        lines.append("\t\t\"\"\"")

                        cmd_call_str = "self.xa_elem." + suite["commands"][command]["name"] + "("

                        if len(suite["commands"][command]["parameters"]) > 0:
                            for parameter in suite["commands"][command]["parameters"]:
                                cmd_call_str += parameter["name"] + ", "
                            
                            cmd_call_str = cmd_call_str[:-2] + ")"
                        else:
                            cmd_call_str += ")"

                        lines.append("\t\t" + cmd_call_str)

        data = "\n".join(lines)
        with open(output_file, "w") as f:
            f.write(data)



class XAMenuBar():
    def __init__(self):
        """Creates a new menu bar object for interacting with the system menu bar.

        .. versionadded:: 0.0.9
        """
        self.menus = {} #: The menus to be displayed in the status bar, keyed by ID

        app = AppKit.NSApplication.sharedApplication()
        detector = self

        class MyApplicationAppDelegate(AppKit.NSObject):
            def menuWillOpen_(self, selected_menu):
                button = app.currentEvent().buttonNumber()
                for menu_key, menu in detector.menus.items():
                    if menu.xa_elem == selected_menu:
                        menu._run_action(button)

            def statusBarButtonClicked_(self, sender):
                print("hi", sender)

            def action_(self, menu_item):
                button = app.currentEvent().buttonNumber()
                for menu_key, menu in detector.menus.items():
                    for item_key, item in menu.items.items():
                        if item.xa_elem == menu_item:
                                item._run_action(button)

                        else:
                            for subitem_key, subitem in item.items.items():
                                if subitem.xa_elem == menu_item:
                                    subitem._run_action(button)

        self.__delegate = MyApplicationAppDelegate.alloc().init().retain()
        app.setDelegate_(self.__delegate)

    def add_menu(self, title: str, image: Union['XABase.XAImage', None] = None, tool_tip: Union[str, None] = None, img_width: int = 30, img_height: int = 30):
        """Adds a new menu to be displayed in the system menu bar.

        :param title: The name of the menu
        :type title: str
        :param image: The image to display for the menu, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param tool_tip: The tooltip to display on hovering over the menu, defaults to None
        :type tool_tip: Union[str, None], optional
        :param img_width: The width of the image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> img = PyXA.XAImage("/Users/steven/Downloads/Blackness.jpg")
        >>> menu_bar.add_menu("Menu 1", image=img, img_width=100, img_height=100)
        >>> menu_bar.display()

        .. deprecated:: 0.1.1
        
           Use :func:`new_menu` instead.

        .. versionadded:: 0.0.9
        """
        self.new_menu(title, image, tool_tip, (img_width, img_height))

    def new_menu(self, title: Union[str, None] = None, image: Union['XABase.XAImage', None] = None, tooltip: Union[str, None] = None, image_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None) -> 'XAMenuBarMenu':
        """Adds a new menu to be displayed in the system menu bar.

        :param title: The title text of the menu, defaults to None
        :type title: Union[str, None], optional
        :param image: The image to display for the menu, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param tooltip: The tooltip to display on hovering over the menu, defaults to None
        :type tooltip: Union[str, None], optional
        :param image_dimensions: The width and height of the image, in pixels, defaults to (30, 30)
        :type image_dimensions: tuple[int, int], optional
        :param action: The method, if any, to associate with the menu (the method called when the menu is opened), defaults to None
        :type action: Callable[[XAMenuBarMenu, None], None], optional
        :param id: A unique identifier for the menu, or None to use the title, defaults to None
        :type id: Union[str, None], optional
        :return: The newly created menu object
        :rtype: XAMenuBarMenu

        :Example:

        >>> import random
        >>> import threading
        >>> import time
        >>> 
        >>> emojis = ["😀", "😍", "🙂", "😎", "🤩", "🤯", "😭", "😱", "😴", "🤒", "😈", "🤠"]
        >>> 
        >>> menu_bar = PyXA.XAMenuBar()
        >>> emoji_bar = menu_bar.new_menu()
        >>> 
        >>> def update_display():
        >>>     while True:
        >>>         new_emoji = random.choice(emojis)
        >>>         emoji_bar.title = new_emoji
        >>>         time.sleep(0.25)
        >>> 
        >>> threading.Thread(target=update_display).start()
        >>> menu_bar.display()

        .. versionadded:: 0.1.1
        """
        title = title or ""
        id = id or title
        while id in self.menus:
            id += "_"

        self.menus[id] = XAMenuBarMenu(title, image, tooltip, image_dimensions, action, id)
        return self.menus[id]
        
    def add_item(self, menu: str, item_name: str, action: Union[Callable[[], None], None] = None, image: Union['XABase.XAImage', None] = None, img_width: int = 20, img_height: int = 20):
        """Adds an item to a menu, creating the menu if necessary.

        :param menu: The name of the menu to add an item to, or the name of the menu to create
        :type menu: str
        :param item_name: The name of the item
        :type item_name: str
        :param action: The method to associate with the item (the method called when the item is clicked)
        :type action: Callable[[], None]
        :param image: The image for the item, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param img_width: The width of image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> 
        >>> menu_bar.add_menu("Menu 1")
        >>> menu_bar.add_item(menu="Menu 1", item_name="Item 1", method=lambda : print("Action 1"))
        >>> menu_bar.add_item(menu="Menu 1", item_name="Item 2", method=lambda : print("Action 2"))
        >>> 
        >>> menu_bar.add_item(menu="Menu 2", item_name="Item 1", method=lambda : print("Action 1"))
        >>> img = PyXA.XAImage("/Users/exampleUser/Downloads/example.jpg")
        >>> menu_bar.add_item("Menu 2", "Item 1", lambda : print("Action 1"), image=img, img_width=100)
        >>> menu_bar.display()

        .. deprecated:: 0.1.1
        
           Use :func:`XAMenuBarMenu.new_item` instead.

        .. versionadded:: 0.0.9
        """
        if menu not in self.menus:
            self.add_menu(menu)
            
        menu = self.menus[menu]
        menu.new_item(item_name, action, [], image, (img_width, img_height))

    def set_image(self, item_name: str, image: 'XABase.XAImage', img_width: int = 30, img_height: int = 30):
        """Sets the image displayed for a menu or menu item.

        :param item_name: The name of the item to update
        :type item_name: str
        :param image: The image to display
        :type image: XAImage
        :param img_width: The width of the image, in pixels, defaults to 30
        :type img_width: int, optional
        :param img_height: The height of the image, in pixels, defaults to 30
        :type img_height: int, optional

        :Example: Set Image on State Change

        >>> import PyXA
        >>> current_state = True # On
        >>> img_on = PyXA.XAImage("/Users/exampleUser/Documents/on.jpg")
        >>> img_off = PyXA.XAImage("/Users/exampleUser/Documents/off.jpg")
        >>> menu_bar = PyXA.XAMenuBar()
        >>> menu_bar.add_menu("Status", image=img_on)
        >>> 
        >>> def update_state():
        >>>     global current_state
        >>>     if current_state is True:
        >>>         # ... (Actions for turning off)
        >>>         menu_bar.set_text("Turn off", "Turn on")
        >>>         menu_bar.set_image("Status", img_off)
        >>>         current_state = False
        >>>     else:
        >>>         # ... (Actions for turning on)
        >>>         menu_bar.set_text("Turn off", "Turn off")
        >>>         menu_bar.set_image("Status", img_on)
        >>>         current_state = True

        menu_bar.add_item("Status", "Turn off", update_state)
        menu_bar.display()

        .. deprecated:: 0.1.1
        
           Set the :attr:`XAMenuBarMenu.image` and :attr:`XAMenuBarMenuItem.image` attributes directly instead.

        .. versionadded:: 0.0.9
        """
        img = image.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_((img_width, img_height))

        for menu_key, menu in self.menus.items():
            if menu_key == item_name:
                menu._status_item.button().setImage_(img)

            else:
                for item_key, item in menu.items.items():
                    if item_key == item_name:
                        item.xa_elem.setImage_(img)

       

    def set_text(self, item_name: str, text: str):
        """Sets the text displayed for a menu or menu item.

        :param item_name: The name of the item to update
        :type item_name: str
        :param text: The new text to display
        :type text: str

        .. deprecated:: 0.1.1
        
           Set the :attr:`XAMenuBarMenu.title` and :attr:`XAMenuBarMenuItem.title` attributes directly instead.

        .. versionadded:: 0.0.9
        """
        for menu_key, menu in self.menus.items():
            if menu_key == item_name:
                menu._status_item.button().setTitle_(item_name)

            else:
                for item_key, item in menu.items.items():
                    if item_key == item_name:
                        item.xa_elem.setTitle_(item_name)

    def remove_menu(self, id):
        """Removes a menu from the status bar.

        :param id: The ID of the menu to remove
        :type id: str

        .. versionadded:: 0.1.1
        """
        menu = self.menus.pop(id)
        status_bar = AppKit.NSStatusBar.systemStatusBar()
        status_bar.removeStatusItem_(menu._status_item)

    def display(self):
        """Displays the custom menus on the menu bar.

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> menu_bar.new_menu("🔥", tooltip="Fire")
        >>> menu_bar.new_menu("💧", tooltip="Water")
        >>> menu_bar.display()

        .. versionadded:: 0.0.9
        """
        for menu in self.menus:
            # Add a 'Quit' item to the bottom of each menu
            item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
            self.menus[menu].xa_elem.addItem_(item)

            self.menus[menu].xa_elem.setDelegate_(self.__delegate)

        try:
            if len(self.menus) > 0:
                AppHelper.runEventLoop(installInterrupt=True)
        except Exception as e:
            print(e)

    

class XAMenuBarMenu():
    def __init__(self, title: str, image: Union['XABase.XAImage', None] = None, tooltip: Union[str, None] = None, image_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None):
        """Initializes a new menu to be displayed in the system menu bar.

        :param title: The name of the menu
        :type title: str
        :param image: The image to display for the menu, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param tooltip: The tooltip to display on hovering over the menu, defaults to None
        :type tooltip: Union[str, None], optional
        :param image_dimensions: The width and height of the image, in pixels, defaults to (30, 30)
        :type image_dimensions: int, optional
        :param action: The method, if any, to associate with the menu (the method called when the menu is opened), defaults to None
        :type action: Callable[[XAMenuBarMenu, None], None], optional
        :param id: A unique identifier for the menu, or None to use the title, defaults to None
        :type id: Union[str, None], optional

        .. versionadded:: 0.1.1
        """
        self.__title = title
        self.__image = image
        self.__tooltip = tooltip
        self.__image_dimensions = image_dimensions
        self.action = action #: The method to call when the menu is opened
        self.id = id or title #: The unique identifier for the menu
        self.items = {} #: The menu items, keyed by their IDs
    
        # Create a new status bar item
        self.__status_bar = AppKit.NSStatusBar.systemStatusBar()
        self._status_item = self.__status_bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength).retain()
        self._status_item.setTitle_(title)
       
        # Add an image to the status bar item, if necessary
        if isinstance(image, XABase.XAImage):
            img = image.xa_elem.copy()
            img.setScalesWhenResized_(True)
            img.setSize_(image_dimensions)
            self._status_item.button().setImage_(img)

        # Add a tooltip to the status bar item, if necessary
        if isinstance(tooltip, str):
            self._status_item.setToolTip_(tooltip)

        # Create a new menu and associate it to the status bar item
        # Disable auto-enabling items so that users have the option to disable them
        self.xa_elem = AppKit.NSMenu.alloc().init()
        self.xa_elem.setAutoenablesItems_(False)
        self._status_item.setMenu_(self.xa_elem)

    @property
    def title(self) -> str:
        """The title text of the menu.
        """
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title
        self._status_item.setTitle_(title)

    @property
    def image(self) -> 'XABase.XAImage':
        """The image associated with the menu.
        """
        img_obj = self._status_item.button().image()
        if img_obj is None:
            return None
        return self.__image

    @image.setter
    def image(self, image: 'XABase.XAImage'):
        self.__image = image
        img = image.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_(self.__image_dimensions)
        self._status_item.button().setImage_(img)

    @property
    def image_dimensions(self) -> tuple[int, int]:
        """The width and height of the menu's image, in pixels.
        """
        return self.__image_dimensions

    @image_dimensions.setter
    def image_dimensions(self, image_dimensions: tuple[int, int]):
        self.__image_dimensions = image_dimensions
        size = AppKit.NSSizeFromCGSize(image_dimensions)
        self._status_item.button().image().setSize_(size)

    @property
    def tooltip(self) -> int:
        """The tooltip that appears when hovering over the menu.
        """
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, tooltip: int):
        self.__tooltip = tooltip
        self._status_item.setToolTip_(tooltip)

    def new_item(self, title: Union[str, None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and adds it to this menu at the current insertion point.

        :param title: The title text of the item, defaults to None
        :type title: Union[str, None], optional
        :param action: The method to call when the item is clicked, defaults to None
        :type action: Union[Callable[[], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param image: The image for the item, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param image_dimensions: The width and height of the image, in pixels, defaults to (20, 20)
        :type image_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, defaults to None
        :type id: Union[str, None], optional
        :return: The newly created menu item object
        :rtype: XAMenuBarMenuItem

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> 
        >>> img1 = PyXA.XAColor.red().make_swatch(10, 10)
        >>> img2 = PyXA.XAImage("https://avatars.githubusercontent.com/u/7865925?v=4")
        >>> img3 = PyXA.XAImage.symbol("flame.circle")
        >>> 
        >>> m1 = menu_bar.new_menu("Menu 1")
        >>> m1.new_item("Item 1", lambda _: print("Action 1"), [], img1, (100, 100))
        >>> m1.new_item("Item 2", lambda _: print("Action 2"), [], img2, (100, 100))
        >>> 
        >>> m2 = menu_bar.new_menu("Menu 2")
        >>> m2.new_item("Item 1", lambda _: print("Action 3"), image=img3, image_dimensions=(50, 50))
        >>> 
        >>> menu_bar.display()

        .. versionadded:: 0.1.1
        """
        # If no ID provided, use the title, then make it unique
        title = title or ""
        id = id or title
        while id in self.items:
            id += "_"

        self.items[id] = XAMenuBarMenuItem(title, action, args, image, image_dimensions, id)
        self.xa_elem.addItem_(self.items[id].xa_elem)
        return self.items[id]

    def add_separator(self, id: Union[str, None] = None) -> 'XAMenuBarMenuItem':
        """Adds a separator to the menu at the current insertion point.

        :param id: A unique identifier for the separator, defaults to None
        :type id: Union[str, None], optional
        :return: The newly created separator menu item object
        :rtype: XAMenuBarMenuItem

        .. versionadded:: 0.1.1
        """
        id = id or "separator"
        while id in self.items:
            id += "_"

        self.items[id] = XAMenuBarMenuItem(id)
        self.xa_elem.addItem_(self.items[id].xa_elem)
        return self.items[id]

    def _run_action(self, button: int):
        """Runs the action associated with this menu.

        .. versionadded:: 0.1.1
        """
        if callable(self.action):
            self.action(self, button)

    def remove_item(self, id):
        """Removes an item from this menu.

        :param id: The ID of the item to remove
        :type id: str

        .. versionadded:: 0.1.1
        """
        item = self.items.pop(id)
        self.xa_elem.removeItem_(item.xa_elem)


class XAMenuBarMenuItem():
    def __init__(self, title: str, action: Union[Callable[['XAMenuBarMenuItem', Any], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None):
        """Initializes an item of a menu.

        :param title: The name of the item
        :type title: str
        :param action: The method to associate with the item (the method called when the item is clicked), defaults to None
        :type action: Callable[[XAMenuBarMenuItem], None]
        :param args: The arguments to call the method with, defaults to None
        :type args: Union[list[Any], None], optional
        :param image: The image for the item, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param image_dimensions: The width and height of image, in pixels, defaults to (20, 20)
        :type image_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, or None to use the title, defaults to None
        :type id: Union[str, None], optional

        .. versionadded:: 0.1.1
        """
        self.__title = title
        self.action = action #: The method to call when this menu item is clicked
        self.args = args or [] #: The arguments to pass to the action method upon execution
        self.__image = image
        self.__image_dimensions = image_dimensions
        self.__indent = 0
        self.__enabled = True
        self.id = id or title #: The unique identifier of the item

        self.items = {}

        if self.id.startswith("separator"):
            self.xa_elem = AppKit.NSMenuItem.separatorItem()
        else:
            self.xa_elem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, 'action:', '')
            
            if isinstance(image, XABase.XAImage):
                img = image.xa_elem.copy()
                img.setScalesWhenResized_(True)
                img.setSize_(image_dimensions)
                self.xa_elem.setImage_(img)

    @property
    def title(self) -> str:
        """The title text of the menu item.
        """
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title
        self.xa_elem.setTitle_(title)

    @property
    def image(self) -> 'XABase.XAImage':
        """The image associated with the menu item.
        """
        img_obj = self.xa_elem.image()
        if img_obj is None:
            return None
        return self.__image

    @image.setter
    def image(self, image: 'XABase.XAImage'):
        self.__image = image
        img = image.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_(self.__image_dimensions)
        self.xa_elem.setImage_(img)

    @property
    def image_dimensions(self) -> tuple[int, int]:
        """The width and height of the menu item's image, in pixels.
        """
        return self.__image_dimensions

    @image_dimensions.setter
    def image_dimensions(self, image_dimensions: tuple[int, int]):
        self.__image_dimensions = image_dimensions
        size = AppKit.NSSizeFromCGSize(image_dimensions)
        self.xa_elem.image().setSize_(size)

    @property
    def indent(self) -> int:
        """The level of indentation of the menu item, from 0 to 15.
        """
        return self.__indent

    @indent.setter
    def indent(self, indent: int):
        self.__indent = indent
        self.xa_elem.setIndentationLevel_(indent)

    @property
    def enabled(self) -> int:
        """Whether the menu item is enabled (vs. appearing grayed out).
        """
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self.__enabled = enabled
        self.xa_elem.setEnabled_(enabled)

    def _run_action(self, button: int):
        """Runs the action associated with this menu item.

        .. versionadded:: 0.1.1
        """
        if callable(self.action):
            self.action(self, button, *self.args)

    def new_subitem(self, title: Union[str, None] = None, action: Union[Callable[['XAMenuBarMenuItem', Any], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and places it in a submenu of this item.

        This will create a new submenu as needed, or will append to the existing submenu if one is already available on this item.

        :param title: The title text of the item, defaults to None
        :type title: Union[str, None], optional
        :param action: The method called when the item is clicked, defaults to None
        :type action: Union[Callable[[XAMenuBarMenuItem, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param image: The image for the item, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param image_dimensions: The width and height of the image, in pixels, defaults to (20, 20)
        :type image_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, or None to use the title, defaults to None
        :type id: Union[str, None], optional
        :return: The newly created menu item
        :rtype: XAMenuBarMenuItem

        :Example:

        >>> import PyXA
        >>> menu_bar = PyXA.XAMenuBar()
        >>> m1 = menu_bar.new_menu("Menu 1")
        >>> i1 = m1.new_item("Item 1")
        >>> i2 = i1.new_subitem("Item 1.1")
        >>> i3 = i2.new_subitem("Item 1.1.1")
        >>> i4 = i3.new_subitem("Item 1.1.1.1")
        >>> menu_bar.display()

        .. versionadded:: 0.1.1
        """
        # If no ID provided, use the title, then make it unique
        title = title or ""
        id = id or title
        while id in self.items:
            id += "_"

        # Create a new submenu, if necessary
        submenu = self.xa_elem.submenu()
        if submenu is None:
            submenu = AppKit.NSMenu.alloc().init()

        # Create a subitem and add it to the submenu
        item = XAMenuBarMenuItem(title, action, args, image, image_dimensions, id)
        submenu.addItem_(item.xa_elem)

        # Associate the submenu to this item
        self.xa_elem.menu().setSubmenu_forItem_(submenu, self.xa_elem)
        self.items[id] = item
        return self.items[id]

    def remove_subitem(self, id: str):
        """Removes a subitem from this item's submenu.

        :param id: The ID of the subitem to remove
        :type id: str

        .. versionadded:: 0.1.1
        """
        item = self.items.pop(id)
        self.xa_elem.submenu().removeItem_(item.xa_elem)