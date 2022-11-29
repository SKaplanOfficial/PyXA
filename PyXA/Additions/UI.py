""".. versionadded:: 0.1.2

Classes for creating and displaying various UI elements.
"""

from datetime import datetime, timedelta
from enum import Enum
from time import sleep
from typing import Any, Callable, Union

import AppKit
from PyObjCTools import AppHelper

from PyXA import XABase


class XAHUD():
    """A momentary HUD window that displays a message to the user.

    .. versionadded:: 0.1.1
    """

    def __init__(self, message: str, font_size: int = 20, duration: float = 3.0, background_color: Union['XABase.XAColor', None] = None, text_color: Union['XABase.XAColor', None] = None):
        self.message = message #: The HUD's message text
        self.font_size = font_size #: The font size of the HUD's message text
        self.duration: float = duration #: The amount of time to display the HUD for, in seconds
        self.background_color: XABase.XAColor = background_color or XABase.XAColor(0, 0, 0, 0.3) #: The background color of the HUD window
        self.text_color: XABase.XAColor = text_color or XABase.XAColor(1, 1, 1, 1) #: The text color of the HUD's message text

    def display(self):
        """Displays the HUD in the center of the screen.

        .. versionadded:: 0.1.2
        """
        # Adjust text frame bounds according to current font size
        text = AppKit.NSText.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 500, 50))
        text.setString_(self.message)
        text.setDrawsBackground_(False)
        text.setSelectable_(False)
        text.setAlignment_(AppKit.NSTextAlignmentCenter)
        text.setTextColor_(self.text_color.xa_elem)
        font = AppKit.NSFont.systemFontOfSize_(font_size)
        text.setFont_(font)
        text.sizeToFit()

        # Create a HUD panel, add the text as a subview
        panel = AppKit.NSPanel.alloc().initWithContentRect_styleMask_backing_defer_(text.frame(), AppKit.NSWindowStyleMaskFullSizeContentView | AppKit.NSWindowStyleMaskUtilityWindow | AppKit.NSTitledWindowMask | AppKit.NSWindowStyleMaskHUDWindow, AppKit.NSBackingStoreBuffered, False)
        panel.setTitlebarAppearsTransparent_(True)
        panel.contentView().addSubview_(text)
        panel.contentView().setBackgroundColor_(self.background_color.xa_elem)

        # Vertically center the text within the panel frame
        font_size = text.font().boundingRectForFont().size.height
        offset = text.frame().size.height - font_size / 2
        new_text_rect = AppKit.NSInsetRect(text.frame(), 0, offset)
        text.setFrame_(new_text_rect)

        # Center the panel in the display
        panel.center()

        # Display the HUD for the specified duration
        panel.makeKeyAndOrderFront_(panel)
        app = AppKit.NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
        app.activateIgnoringOtherApps_(True)
        AppKit.NSRunLoop.currentRunLoop().runUntilDate_(datetime.now() + timedelta(seconds = self.duration))




class XAAlertStyle(Enum):
    """Options for which alert style an alert should display with.
    """
    INFORMATIONAL   = AppKit.NSAlertStyleInformational
    WARNING         = AppKit.NSAlertStyleWarning
    CRITICAL        = AppKit.NSAlertStyleCritical

class XAAlert():
    """A class for creating and interacting with an alert dialog window.

    .. versionadded:: 0.0.5
    """
    def __init__(self, title: str = "Alert!", message: str = "", style: XAAlertStyle = XAAlertStyle.INFORMATIONAL, buttons = ["Ok", "Cancel"], icon: Union['XABase.XAImage', None] = None):
        """Initializes an alert object.

        :param title: The title text of the alert
        :type title: str
        :param message: The detail message text of the alert, defaults to ""
        :type message: str, optional
        :param style: The style of the alert (i.e. informational, warning, or critical), deprecated as of PyXA 0.1.2
        :type style: XAAlertStyle, optional
        :param buttons: A list specifying the buttons available for the user to click
        :type buttons: list[str]
        :param icon: The icon displayed in the alert window
        :type icon: XABase.XAImage
        """
        self.title: str = title #: The title text of the alert
        self.message: str = message #: The detail message text of the alert
        self.style: XAAlertStyle = style
        """The style of the alert.

        .. deprecated:: 0.1.2
        
           To customize the icon, set the :attr:`icon` attribute instead.
        """

        self.buttons: list[str] = buttons #: A list specifying the buttons available for the user to click
        self.icon = icon #: The icon displayed in the alert window
        self.__return_value = None

    def __display(self):
        # Actual logic for displaying the alert, run on main thread via display()
        alert = AppKit.NSAlert.alloc().init()
        alert.setInformativeText_(self.title)
        alert.setMessageText_(self.message)

        if self.icon is not None:
            alert.setIcon_(self.icon.xa_elem)

        for button in self.buttons:
            alert.addButtonWithTitle_(button)
        self.__return_value = alert.runModal()

    def display(self) -> int:
        """Displays the alert.

        :return: A number representing the button that the user selected, if any
        :rtype: int

        .. versionadded:: 0.0.5
        """
        loop_mode = AppKit.NSRunLoop.mainRunLoop().currentMode()
        if loop_mode is None:
            # Not in run loop; run normally (must be done on main thread)
            self.__display()
        else:
            # In run loop; force run on main thread
            AppHelper.callAfter(self.__display)

        # Wait for user to click some button
        while self.__return_value is None:
            sleep(0.01)
        return self.__return_value




class XANotification():
    """A class for managing and interacting with notifications.

    .. versionadded:: 0.0.9
    """
    def __init__(self, text: str, title: Union[str, None] = None, subtitle: Union[str, None] = None, image: Union['XABase.XAImage', None] = None, sound_name: Union[str, None] = None, primary_button_title: Union[str, None] = None, show_reply_button: bool = False, click_action: Union[Callable[[], None], None] = None, primary_action: Union[Callable[[], None], None] = None, reply_action: Union[Callable[[], None], None] = None, timeout: float = -1):
        """Initializes a notification object.

        :param text: The main text of the notification
        :type text: str
        :param title: The title of the notification, defaults to None
        :type title: Union[str, None], optional
        :param subtitle: The subtitle of the notification, defaults to None
        :type subtitle: Union[str, None], optional
        :param image: The content image of the notification, defaults to None
        :type image: Union[XABase.XAImage, None], optional
        :param sound_name: The sound to play when the notification is displayed, defaults to None
        :type sound_name: Union[str, None], optional
        :param primary_button_title: The name of the primary action button, defaults to None
        :type primary_button_title: str, optional
        :param click_action: The method to run when the user clicks the notification
        :type click_action: Union[Callable[[XANotification], None], None], optional
        :param primary_action: The method to run when the user clicks the primary action button, defaults to None
        :type primary_action: Union[Callable[[XANotification], None], None], optional
        :param reply_action: The method to run when the user replies to the notification, defaults to None
        :type reply_action: Union[Callable[[XANotification, str], None], None], optional
        :param timeout: The number of seconds to wait for the user to act on the notification, or -1 to wait infinitely, defaults to -1
        :type timeout: float

        .. versionadded:: 0.0.9
        """
        self.text: str = text #: The main text of the notification
        self.title: str = title #: The title of the notification
        self.subtitle: str = subtitle #: The subtitle of the notification
        self.image: XABase.XAImage = image #: The content image of the notification
        self.sound_name = sound_name #: The sound to play when the notification is displayed
        self.primary_button_title: str = primary_button_title #: The name of the primary action button
        self.click_action: Union[Callable[[XANotification], None], None] = click_action or (lambda x: None) #: The method to run when the user clicks the notification
        self.primary_action: Union[Callable[[XANotification], None], None] = primary_action or (lambda x: None) #: The method to run when the user clicks the primary action button
        self.reply_action: Union[Callable[[XANotification, str], None], None] = reply_action #: The method to run when the user replies to the notification. Overrides the primary action and replaces the primary action button with a "Reply" button.
        self.timeout: float = timeout #: The number of seconds to wait for the user to act on the notification, or -1 to wait infinitely

    def display(self):
        """Displays the notification.

        .. versionadded:: 0.0.9
        """
        nc = AppKit.NSUserNotificationCenter.defaultUserNotificationCenter()
        parent = self

        class NotificationCenterDelegate(AppKit.NSObject):
            def userNotificationCenter_didActivateNotification_(self, nc, notification):
                activation_type = notification.activationType()
                if activation_type == 1:
                    parent.click_action(parent)
                elif activation_type == 2:
                    parent.primary_action(parent)
                elif activation_type == 3:
                    parent.reply_action(parent, notification.response().string())

                nc.removeDeliveredNotification_(notification)

        nc.setDelegate_(NotificationCenterDelegate.alloc().init().retain())
        notification = AppKit.NSUserNotification.alloc().init()

        if isinstance(self.title, str):
            notification.setTitle_(self.title)

        if isinstance(self.subtitle, str):
            notification.setSubtitle_(self.subtitle)

        notification.setInformativeText_(self.text)

        if isinstance(self.image, XABase.XAImage):
            notification.setContentImage_(self.image.xa_elem)
        
        if isinstance(self.sound_name, str):
            notification.setSoundName_(self.sound_name)

        if isinstance(self.primary_button_title, str):
            notification.setActionButtonTitle_(self.primary_button_title)
            self.__dismiss = False
        else:
            notification.setHasActionButton_(False)

        if callable(self.reply_action):
            notification.setHasReplyButton_(True)
            self.__dismiss = False

        notification.setDeliveryDate_(datetime.now())
        nc.scheduleNotification_(notification)

        # Wait for notification to be delivered
        while notification not in nc.deliveredNotifications():
            sleep(0.01)

        # Wait for user to do some action on the notification
        while notification in nc.deliveredNotifications():
            AppKit.NSRunLoop.mainRunLoop().runUntilDate_(datetime.now() + timedelta(seconds=0.01))




class XAMenuBar():
    def __init__(self):
        """Creates a new menu bar object for interacting with the system menu bar.

        .. versionadded:: 0.0.9
        """
        self.menus = {} #: The menus to be displayed in the status bar, keyed by ID

        app = AppKit.NSApplication.sharedApplication()
        detector = self

        def get_all_subitems(menu):
            items = []
            for item_key, item in menu.items.items():
                items.append(item)
                items.extend(get_all_subitems(item))
            return items

        class MyApplicationAppDelegate(AppKit.NSObject):
            def menu_willHighlightItem_(self, menu, item):
                if hasattr(item, "submenu") and item.submenu() is not None:
                    self.action_(item)

            def menuWillOpen_(self, selected_menu):
                button = app.currentEvent().buttonNumber()
                for menu_key, menu in detector.menus.items():
                    if menu.xa_elem == selected_menu:
                        menu._run_action(button)

            def action_(self, menu_item):
                button = app.currentEvent().buttonNumber()
                for menu_key, menu in detector.menus.items():
                    subitems = get_all_subitems(menu)
                    for subitem in subitems:
                        if subitem.xa_elem == menu_item:
                            subitem._run_action(button)
                            break

        self.__delegate = MyApplicationAppDelegate.alloc().init().retain()
        app.setDelegate_(self.__delegate)
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

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

    def new_menu(self, title: Union[str, None] = None, image: Union['XABase.XAImage', None] = None, tooltip: Union[str, None] = None, image_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenu':
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
        :param index: The position to insert the menu in the list of menus, defaults to -1
        :type index: int, optional
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

        self.menus[id] = XAMenuBarMenu(title, image, tooltip, image_dimensions, action, id, index)
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
    def __init__(self, title: str, image: Union['XABase.XAImage', None] = None, tooltip: Union[str, None] = None, image_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None, index: int = -1):
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
        :param index: The position to insert the menu in the list of menus, defaults to -1
        :type index: int, optional

        .. versionadded:: 0.1.1
        """
        self.__title = title
        self.__image = image
        self.__tooltip = tooltip
        self.__image_dimensions = image_dimensions
        self.action = action #: The method to call when the menu is opened
        self.id = id or title #: The unique identifier for the menu
        self.items = {} #: The menu items, keyed by their IDs
        self.index = index 
    
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

    def new_item(self, title: Union[str, None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenuItem':
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
        :param index: The position to insert the item in the list of menu items, defaults to -1
        :type index: int, optional
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

        if index == -1:
            index = self.xa_elem.numberOfItems()
        self.items[id] = XAMenuBarMenuItem(self, title, action, args, image, image_dimensions, id, index)
        self.xa_elem.insertItem_atIndex_(self.items[id].xa_elem, index)
        return self.items[id]

    def add_separator(self, id: Union[str, None] = None) -> 'XAMenuBarMenuItem':
        """Adds a separator to the menu at the current insertion point.

        :param id: A unique identifier for the separator, defaults to None
        :type id: Union[str, None], optional
        :return: The newly created separator menu item object
        :rtype: XAMenuBarMenuItem

        .. deprecated:: 0.1.2
        
           Use :func:`new_separator` instead.

        .. versionadded:: 0.1.1
        """
        id = id or "separator"
        while id in self.items:
            id += "_"

        self.items[id] = XAMenuBarMenuItem(self, id)
        self.xa_elem.addItem_(self.items[id].xa_elem)
        return self.items[id]

    def new_separator(self, id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenuItem':
        """Adds a separator to the menu at the current insertion point.

        :param id: A unique identifier for the separator, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the separator in the list of menus, defaults to -1
        :type index: int, optional
        :return: The newly created separator menu item object
        :rtype: XAMenuBarMenuItem

        .. versionadded:: 0.1.1
        """
        id = id or "separator"
        while id in self.items:
            id += "_"

        if index == -1:
            index = self.xa_elem.numberOfItems()
        self.items[id] = XAMenuBarMenuItem(self, id)
        self.xa_elem.insertItem_atIndex_(self.items[id].xa_elem, index)
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

    def delete(self):
        """Deletes the menu.

        .. versionadded:: 0.1.2
        """
        self.__status_bar.removeStatusItem_(self._status_item)


class XAMenuBarMenuItem():
    def __init__(self, parent: XAMenuBarMenu, title: str, action: Union[Callable[['XAMenuBarMenuItem', Any], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1):
        """Initializes an item of a menu.

        :param parent: The menu which owns this menu item
        :type parent: XAMenuBarMenu
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
        :param index: The position to insert the item in the list of menu items, defaults to -1
        :type index: int, optional

        .. versionadded:: 0.1.1
        """
        self.__parent = parent
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

    def new_subitem(self, title: Union[str, None] = None, action: Union[Callable[['XAMenuBarMenuItem', Any], None], None] = None, args: Union[list[Any], None] = None, image: Union['XABase.XAImage', None] = None, image_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenuItem':
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
        :param index: The position to insert the subitem in the list of subitems, defaults to -1
        :type index: int, optional
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
        if index == -1:
            index = submenu.numberOfItems()
        item = XAMenuBarMenuItem(self, title, action, args, image, image_dimensions, id)
        submenu.insertItem_atIndex_(item.xa_elem, index)

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

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.1.2
        """
        if isinstance(self.__parent, XAMenuBarMenu):
            self.__parent.xa_elem.removeItem_(self.xa_elem)
        else:
            self.__parent.xa_elem.submenu().removeItem_(self.xa_elem)