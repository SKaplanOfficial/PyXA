""".. versionadded:: 0.1.2

Classes for creating and displaying various UI elements.
"""

from datetime import datetime, timedelta
from enum import Enum
from time import sleep
from typing import Any, Callable, Union, Literal

import AppKit
from PyObjCTools import AppHelper

from PyXA import XABase


class XASwitch():
    """A switch UI element. Wrapper around AppKit.NSSwitch functionality.

    .. versionadded:: 0.1.2
    """
    def __init__(self, action: Union[Callable[['XASwitch', int, Any], None], None] = None, args: Union[list[Any], None] = None):
        """Initializes a switch object.

        :param action: The method to run when the switch's state changes, defaults to None
        :type action: Union[Callable[[XASwitch, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional

        .. versionadded:: 0.1.2
        """
        self.action = action #: The method to run when the switch's state changes
        self.args = args or [] #: The arguments to pass to the action method upon execution
        switch = AppKit.NSSwitch.alloc().init()
        switch.setFrame_(AppKit.NSMakeRect(0, 0, 100, 32))
        switch.setAction_("run:action:")
        switch.setTarget_(self)
        self.xa_elem = switch

    @property
    def state(self) -> bool:
        """The current state of the switch.
        """
        return self.xa_elem.state() == AppKit.NSControlStateValueOn

    @state.setter
    def state(self, state: bool):
        if state:
            self.xa_elem.setState_(AppKit.NSControlStateValueOn)
        else:
            self.xa_elem.setState_(AppKit.NSControlStateValueOff)

    def run_action_(self, slider, _):
        """Runs the action method attached to the switch.

        :param switch: The NSSwitch object associated with this object
        :type switch: AppKit.NSSwitch

        .. versionadded:: 0.1.2
        """
        button = AppKit.NSApplication.sharedApplication().currentEvent().buttonNumber()
        if callable(self.action):
            self.action(self, button, *self.args)
    
    def toggle(self):
        """Toggles the switch on or off.

        .. versionadded:: 0.1.2
        """
        if self.xa_elem.state() == AppKit.NSControlStateValueOn:
            self.xa_elem.setState_(AppKit.NSControlStateValueOff)
        else:
            self.xa_elem.setState_(AppKit.NSControlStateValueOn)




class XASlider():
    """A slider UI element. Wrapper around AppKit.NSSlider functionality.

    .. versionadded:: 0.1.2
    """
    def __init__(self, action: Union[Callable[['XASlider', int, Any], None], None] = None, args: Union[list[Any], None] = None, value: float = 50.0, min_value: float = 0, max_value: float = 100):
        """Initializes a new slider object.

        :param action: The method to call when the value of the slider changes, defaults to None
        :type action: Union[Callable[[XASlider, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param value: The starting value of the slider, defaults to 50.0
        :type value: float, optional
        :param min_value: The minimum value of the slider, defaults to 0
        :type min_value: float, optional
        :param max_value: The maximum value of the slider, defaults to 100
        :type max_value: float, optional

        .. versionadded:: 0.1.2
        """
        self.action = action #: The method to run when the value of the slider changes
        self.args = args or [] #: The arguments to pass to the action method upon execution
        slider = AppKit.NSSlider.sliderWithTarget_action_(None, 'action:')
        slider.setMinValue_(min_value)
        slider.setMaxValue_(max_value)
        slider.setDoubleValue_(value)
        slider.setFrameSize_(AppKit.NSMakeSize(100, 25))
        slider.setAction_("run:action:")
        slider.setTarget_(self)
        self.xa_elem = slider

    @property
    def value(self) -> float:
        """The current value of the slider.
        """
        return self.xa_elem.doubleValue()

    @value.setter
    def value(self, value: float):
        self.xa_elem.setDoubleValue_(value)

    @property
    def min_value(self) -> float:
        """The minimum value that the slider can be set to.
        """
        return self.xa_elem.minValue()

    @min_value.setter
    def min_value(self, min_value: float):
        self.xa_elem.setMinValue_(min_value)

    @property
    def max_value(self) -> float:
        """The maximum value that the slider can be set to.
        """
        return self.xa_elem.maxValue()

    @max_value.setter
    def max_value(self, max_value: float):
        self.xa_elem.setMaxValue_(max_value)

    def run_action_(self, slider, _):
        """Runs the action method associated with the slider.

        .. versionadded:: 0.1.2
        """
        button = AppKit.NSApplication.sharedApplication().currentEvent().buttonNumber()
        if callable(self.action):
            self.action(self, button, *self.args)




class XASegmentedControl():
    """A segmented control UI element. Wrapper around AppKit.NSSegmentedControl functionality.

    .. versionadded:: 0.1.2
    """
    def __init__(self, segments: Union[list[str], list[XABase.XAImage]], action: Union[Callable[['XASlider', int, Any], None], None] = None, args: Union[list[Any], None] = None, multiselect: bool = False):
        """Initializes a new slider object.

        :param segments: The labels or images to display as available options
        :type segments: Union[list[str], list[XABase.XAImage]]
        :param action: The method to call when the value of the slider changes, defaults to None
        :type action: Union[Callable[[XASlider, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param multiselect: Controls whether one or multiple options can be selected, defaults to False
        :type multiselect: bool, optional

        .. versionadded:: 0.1.2
        """
        if not isinstance(segments, list):
            raise TypeError("Must provided a list of segment names (strings) or images (of the XABase.XAImage class).")

        all_strings = all([isinstance(segment, str) for segment in segments])
        all_images = all(isinstance(segment, XABase.XAImage) for segment in segments)
        if not all_strings and not all_images:
            raise TypeError("Segments must be either *all* strings or *all* images.")

        self.__segments = segments
        self.__state = [False for _ in segments]

        if multiselect:
            multiselect = AppKit.NSSegmentSwitchTrackingSelectAny
        else:
            multiselect = AppKit.NSSegmentSwitchTrackingSelectOne

        if all_strings:
            control = AppKit.NSSegmentedControl.segmentedControlWithLabels_trackingMode_target_action_(segments, multiselect, self, 'run:action:')
        else:
            images = [image.xa_elem for image in segments]
            control = AppKit.NSSegmentedControl.segmentedControlWithImages_trackingMode_target_action_(images, multiselect, self, 'run:action:')

        self.__multiselect = multiselect
        self.action = action #: The method to run when the value of the slider changes
        self.args = args or [] #: The arguments to pass to the action method upon execution
        self.xa_elem = control

    @property
    def selection(self) -> Union[list[str], list[XABase.XAImage]]:
        """The list of currently selected segments.

        .. versionadded:: 0.1.2
        """
        selected_segments = []
        for index, segment in enumerate(self.__segments):
            if self.__state[index] is True:
                selected_segments.append(segment)

        return selected_segments

    @selection.setter
    def selection(self, selection: Union[list[str], list[XABase.XAImage]]):
        self.xa_elem.setSelectedSegment_(-1)
        for new_segment in selection:
            for index, segment in enumerate(self.__segments):
                if new_segment == segment:
                    self.xa_elem.setSelected_forSegment_(True, index)

    def run_action_(self, slider, _):
        """Runs the action method associated with the segmented control.

        .. versionadded:: 0.1.2
        """
        index = self.xa_elem.selectedSegment()
        if not self.__multiselect:
            self.__state = [False for _ in self.__state]
        self.__state[index] = not self.__state[index]

        button = AppKit.NSApplication.sharedApplication().currentEvent().buttonNumber()
        if callable(self.action):
            self.action(self, button, *self.args)




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

        :Example:

        >>> import PyXA
        >>> menubar = PyXA.XAMenuBar()
        >>> menu_icon = PyXA.XAImage.symbol("sparkles")
        >>> menu = menubar.new_menu(icon=menu_icon)
        >>> 
        >>> button_item = menu.new_item("Click me", action=lambda item, button: print(item.text))
        >>> url_item = menu.new_url_item("www.github.com")
        >>> image_item = menu.new_image_item("/Users/steven/Desktop/Screenshot 2022-12-06 at 21.40.37.png", tooltip="An image")
        >>> switch_item = menu.new_switch_item(label="Toggle", action=lambda switch, button: print(switch.state))
        >>> segmented_control_item = menu.new_segmented_control_item(["A", "B", "C"], multiselect=True, action=lambda control, button: print(control.selection))
        >>> segmented_control_item = menu.new_segmented_control_item(["1", "2", "3"], action=lambda control, button: print(control.selection))
        >>> slider_item = menu.new_slider_item(action=lambda slider, button: print(slider.value))
        >>> menu.new_separator()
        >>> 
        >>> menubar.display()

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
                if app.currentEvent().type() == AppKit.NSEventTypeMouseMoved:
                    button = -1

                for menu_key, menu in detector.menus.items():
                    subitems = get_all_subitems(menu)
                    for subitem in subitems:
                        if subitem.xa_elem == menu_item:
                            subitem._run_action(button)
                            break

                    # popover = AppKit.NSPopover.alloc().init()
                    # popover.setContentSize_((100, 200))
                    # # popover.setBehavior_(AppKit.NSPopoverBehaviorTransient)
                    # view_controller = AppKit.NSViewController.alloc().init()
                    # view_controller.setView_(AppKit.NSView.alloc().init())
                    # popover.setContentViewController_(view_controller)
                    # popover.showRelativeToRect_ofView_preferredEdge_(menu._status_item.button().bounds(), menu._status_item.button(), AppKit.NSRectEdgeMinY)

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

    def new_menu(self, content: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath, None] = None, icon: Union[XABase.XAImage, None] = None, tooltip: Union[str, None] = None, icon_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenu':
        """Adds a new menu to be displayed in the system menu bar.

        :param content: The content of the menu (the string or icon shown in the menubar), defaults to None
        :type content: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath, None], optional
        :param icon: The icon for the menu, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param tooltip: The tooltip to display on hovering over the menu, defaults to None
        :type tooltip: Union[str, None], optional
        :param icon_dimensions: The width and height of the image, in pixels, defaults to (30, 30)
        :type icon_dimensions: tuple[int, int], optional
        :param action: The method, if any, to associate with the menu (the method called when the menu is opened), defaults to None
        :type action: Callable[[XAMenuBarMenu, None], None], optional
        :param id: A unique identifier for the menu, or None to use the title, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the menu in the list of menus, defaults to -1
        :type index: int, optional
        :param label: The label for the menu item, defaults to None
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
        content = content or ""
        id = id or content
        while id in self.menus:
            id += "_"

        self.menus[id] = XAMenuBarMenu(content, icon, tooltip, icon_dimensions, action, id, index)
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
            menu = self.menus[menu]
            item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
            menu.xa_elem.addItem_(item)
            menu.xa_elem.setDelegate_(self.__delegate)

            for item in menu.xa_elem.itemArray():
                view = item.view()
                if view is None:
                    continue

                menu_width = max(menu.xa_elem.size().width, 100)
                view_height = view.frame().size.height
                view.setFrameSize_((menu_width, view_height))

                if isinstance(view, AppKit.NSImageView):
                    view.image().setSize_(AppKit.NSMakeSize(menu_width * 0.9, view_height * 0.95))

                for subview in view.subviews():
                    if isinstance(subview, AppKit.NSSwitch):
                        subview_height = subview.frame().size.height
                        subview.sizeToFit()
                        subview.setFrame_(AppKit.NSMakeRect(menu_width * 0.95 - subview.frame().size.width, 0, subview.frame().size.width, subview_height))

                    elif not isinstance(subview, AppKit.NSText):
                        subview_y = subview.frame().origin.y
                        subview_height = subview.frame().size.height
                        subview.setFrame_(AppKit.NSMakeRect((menu_width - menu_width * 0.9) / 2, subview_y, menu_width * 0.9, subview_height))

        try:
            if len(self.menus) > 0:
                AppHelper.installMachInterrupt()
                AppHelper.runEventLoop()
        except Exception as e:
            print(e)




class XAMenuBarMenu():
    def __init__(self, content: Union[str, int, float, XABase.XAObject], icon: Union[XABase.XAImage, None] = None, tooltip: Union[str, None] = None, icon_dimensions: tuple[int, int] = (30, 30), action: Callable[['XAMenuBarMenu', None], None] = None, id: Union[str, None] = None, index: int = -1):
        """Initializes a new menu to be displayed in the system menu bar.

        :param content: The content of the menu (the string or icon shown in the menubar)
        :type content: str
        :param icon: The icon associated with the menu
        :type icon: XABase.XAImage
        :param tooltip: The tooltip to display on hovering over the menu, defaults to None
        :type tooltip: Union[str, None], optional
        :param icon_dimensions: The width and height of the image, in pixels, defaults to (30, 30)
        :type icon_dimensions: int, optional
        :param action: The method, if any, to associate with the menu (the method called when the menu is opened), defaults to None
        :type action: Callable[[XAMenuBarMenu, None], None], optional
        :param id: A unique identifier for the menu, or None to use the title, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the menu in the list of menus, defaults to -1
        :type index: int, optional

        .. versionadded:: 0.1.1
        """
        self.__content = content
        self.__icon = icon
        self.__icon_dimensions = icon_dimensions
        self.__tooltip = tooltip
        self.action = action #: The method to call when the menu is opened
        self.id = id or str(content) #: The unique identifier for the menu
        self.items = {} #: The menu items, keyed by their IDs
        self.index = index
    
        # Create a new status bar item
        self.__status_bar = AppKit.NSStatusBar.systemStatusBar()
        self._status_item = self.__status_bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength).retain()
       
        # Add an image to the status bar item, if necessary
        if icon is not None:
            self.icon = icon

        self.content = content

        # Add a tooltip to the status bar item, if necessary
        if isinstance(tooltip, str):
            self.tooltip = tooltip

        # Create a new menu and associate it to the status bar item
        # Disable auto-enabling items so that users have the option to disable them
        self.xa_elem = AppKit.NSMenu.alloc().init()
        self.xa_elem.setAutoenablesItems_(False)
        self._status_item.setMenu_(self.xa_elem)

    @property
    def content(self) -> str:
        """The content of the menu.
        """
        return self.__content

    @content.setter
    def content(self, content: str):
        self.__content = content
        if isinstance(content, str):
            self._status_item.setTitle_(content)
        elif isinstance(content, XABase.XAImage):
            self.__icon = content
            img = content.xa_elem.copy()
            img.setScalesWhenResized_(True)
            img.setSize_(self.__icon_dimensions)
            self._status_item.button().setImage_(img)

    @property
    def icon(self) -> 'XABase.XAImage':
        """The image associated with the menu.
        """
        return self.__icon

    @icon.setter
    def icon(self, icon: 'XABase.XAImage'):
        self.__icon = icon
        img = icon.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_(self.__icon_dimensions)
        self._status_item.button().setImage_(img)

    @property
    def icon_dimensions(self) -> tuple[int, int]:
        """The width and height of the menu's image, in pixels.
        """
        return self.__icon_dimensions

    @icon_dimensions.setter
    def icon_dimensions(self, icon_dimensions: tuple[int, int]):
        self.__icon_dimensions = icon_dimensions
        size = AppKit.NSSizeFromCGSize(icon_dimensions)
        self._status_item.button().image().setSize_(size)

    @property
    def tooltip(self) -> str:
        """The tooltip that appears when hovering over the menu.
        """
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, tooltip: str):
        self.__tooltip = tooltip
        self._status_item.setToolTip_(tooltip)

    def new_item(self, content: Union[str, None] = None, icon: Union['XABase.XAImage', None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, icon_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1, label: Union[str, None] = None, tooltip: Union[str, None] = None, multiselect: bool = False) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and adds it to this menu at the current insertion point.

        :param content: The title text of the item, defaults to None
        :type content: Union[str, None], optional
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param action: The method to call when the item is clicked, defaults to None
        :type action: Union[Callable[[], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param icon_dimensions: The width and height of the image, in pixels, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the item in the list of menu items, defaults to -1
        :type index: int, optional
        :param label: The label to the left of the item's content
        :type label: Union[str, None], optional
        :param tooltip: The tooltip text for the menu item, defaults to None
        :type tooltip: Union[str, None], optional
        :param multiselect: Whether multiple options in a segmented control item can be selected at once, defaults to False
        :type multiselect: bool, optional
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
        >>> m2.new_item("Item 1", lambda _: print("Action 3"), image=img3, icon_dimensions=(50, 50))
        >>> 
        >>> menu_bar.display()

        .. versionadded:: 0.1.1
        """
        # If no ID provided, use the title, then make it unique
        content = content or ""

        id = id or str(content)
        while id in self.items:
            id += "_"

        if index == -1:
            index = self.xa_elem.numberOfItems()

        if content == "separator":
            self.items[id] =  XASeparatorMenuItem(self)
        elif content == "slider":
            self.items[id] =  XASliderMenuItem(self, tooltip, action, args)
        elif content == "switch":
            self.items[id] =  XASwitchMenuItem(self, label, tooltip, action, args)
        elif isinstance(content, list):
            self.items[id] =  XASegmentedControlMenuItem(self, content, tooltip, action, args, multiselect)
        elif isinstance(content, XABase.XAImage):
            self.items[id] = XAImageMenuItem(self, content, tooltip)
        elif isinstance(content, XABase.XAURL) or isinstance(content, XABase.XAPath):
            self.items[id] = XAURLMenuItem(self, content, label, icon, icon_dimensions, tooltip, action, args)
        elif isinstance(content, str) or isinstance(content, int) or isinstance(content, float) or isinstance(content, bool):
            self.items[id] = XATextMenuItem(self, str(content), icon, icon_dimensions, tooltip, action, args)
        else:
            self.items[id] = XAMenuBarMenuItem(self, content, icon, action, args, icon_dimensions, id, index, label, tooltip)

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

    def new_url_item(self, url: Union[str, XABase.XAURL, XABase.XAPath], label: Union[str, None] = None, icon: Union[XABase.XAImage, None] = None, icon_dimensions: tuple[int, int] = (20, 20), tooltip: Union[str, None] = None, action: Union[Callable[['XAURLMenuItem'], None], None] = None, args: Union[list[Any], None] = None, index: int = -1) -> 'XAURLMenuItem':
        """Creates a new URL menu item at the specified index or the current insertion point.

        :param url: The URL or file path that the item will link to
        :type url: Union[str, XABase.XAURL, XABase.XAPath]
        :param label: The label for the item, or None to use the full URL as the label
        :type label: Union[str, None]
        :param icon: The icon to display to the left of the label, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param icon_dimensions: The dimensions of the icon, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param tooltip: The tooltip text to display when the cursor hovers over this item, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the user clicks this item, or None to open the URL using standard methods, defaults to None
        :type action: Union[Callable[[XAURLMenuItem], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created URL menu item
        :rtype: XAURLMenuItem

        .. versionadded:: 0.1.2
        """
        # Convert string URL to XAURL
        if isinstance(url, str):
            url = XABase.XAURL(url)
        return self.new_item(url, icon, action, args, icon_dimensions, None, index, label, tooltip)

    def new_image_item(self, image: Union[str, XABase.XAImage], tooltip: Union[str, None] = None, index: int = -1) -> 'XAImageMenuItem':
        """Creates a new image menu item at the specified index or the current insertion point.

        :param image: An image object or the path to an image file to display in the menu
        :type image: Union[str, XABase.XAImage]
        :param tooltip: The tooltip text to display when the cursor hovers over the image, defaults to None
        :type tooltip: Union[str, None], optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created image menu item
        :rtype: XAImageMenuItem

        .. versionadded:: 0.1.2
        """
        # Convert image path to XAImage
        if isinstance(image, str):
            image = XABase.XAImage(image)
        return self.new_item(image, tooltip=tooltip, index=index)

    def new_segmented_control_item(self, segments: Union[list[str], list[XABase.XAImage]], tooltip: Union[str, None] = None, action: Union[Callable[[XASlider], None], None] = None, args: Union[list[Any], None] = None, multiselect: bool = False, index: int = -1) -> 'XASegmentedControlMenuItem':
        """Creates a new segmented control menu item at the specified index or the current insertion point.

        :param segments: The strings or images to display as button options
        :type segments: Union[list[str], list[XABase.XAImage]]
        :param tooltip: The tooltip to display when the cursor hovers over the segmented control, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the user changes the state of the segmented control (when the user activates/deactivates a button), defaults to None
        :type action: Union[Callable[[XASlider], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param multiselect: Whether multiple options can be selected at a time, defaults to False
        :type multiselect: bool optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created segmented control menu item
        :rtype: XASegmentedControlMenuItem

        .. versionadded:: 0.1.2
        """
        return self.new_item(segments, tooltip=tooltip, action=action, args=args, multiselect=multiselect, index=index)

    def new_switch_item(self, label: Union[str, None] = None, tooltip: Union[str, None] = None, action: Union[Callable[[XASlider], None], None] = None, args: Union[list[Any], None] = None, index: int = -1) -> 'XASwitchMenuItem':
        """Creates a new switch menu item at the specified index or the current insertion point.

        :param label: The label text to display left of the switch, defaults to None
        :type label: Union[str, None], optional
        :param tooltip: The tooltip text to display when the cursor hovers over the switch, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the user changes the switch's state, defaults to None
        :type action: Union[Callable[[XASlider], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created switch menu item
        :rtype: XASwitchMenuItem

        .. versionadded:: 0.1.2
        """
        return self.new_item("switch", label=label, tooltip=tooltip, action=action, args=args, index=index)

    def new_slider_item(self, tooltip: Union[str, None] = None, action: Union[Callable[[XASlider], None], None] = None, args: Union[list[Any], None] = None, index: int = -1) -> 'XASliderMenuItem':
        """Creates a new slider menu item at the specified index or the current insertion point.

        :param tooltip: The tooltip text to display when the cursor hovers over the item, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the user changes the slider's value, defaults to None
        :type action: Union[Callable[[XASlider], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created slider menu item
        :rtype: XASliderMenuItem

        .. versionadded:: 0.1.2
        """
        return self.new_item("slider", tooltip=tooltip, action=action, args=args, index=index)

    def new_separator(self, id: Union[str, None] = None, index: int = -1) -> 'XAMenuBarMenuItem':
        """Adds a separator to the menu at the current insertion point.

        :param id: A unique identifier for the separator, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the separator in the list of menu items, defaults to -1
        :type index: int, optional
        :return: The newly created separator menu item object
        :rtype: XAMenuBarMenuItem

        .. versionadded:: 0.1.1
        """
        return self.new_item("separator", index=index)

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




class XAMenuBarMenuItem(XAMenuBarMenu):
    def __init__(self, parent: XAMenuBarMenu, content: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath], icon: Union['XABase.XAImage', None] = None, action: Union[Callable[['XAMenuBarMenuItem', Any], None], None] = None, args: Union[list[Any], None] = None, tooltip: Union[str, None] = None):
        """Initializes an item of a menu.

        :param parent: The menu which owns this menu item
        :type parent: XAMenuBarMenu
        :param content: The content of the item
        :type content: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath]
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param action: The method to associate with the item (the method called when the item is clicked), defaults to None
        :type action: Callable[[XAMenuBarMenuItem], None]
        :param args: The arguments to call the method with, defaults to None
        :type args: Union[list[Any], None], optional
        :param tooltip: The tooltip text for the menu item, defaults to None
        :type tooltip: Union[str, None], optional

        .. versionadded:: 0.1.1
        """
        self.parent = parent #: The parent menu or menu item of this item
        self.args = args or [] #: The arguments to pass to the action method upon execution
        self.action = None #: The method to call when this menu item is clicked

        self.items = {}

        if isinstance(self.xa_elem, AppKit.NSView):
            # Menu item with subviews has been initialized by subclass
            new_elem = AppKit.NSMenuItem.alloc().init()
            new_elem.setView_(self.xa_elem)
            self.xa_elem = new_elem

        if tooltip is not None:
            self.xa_elem.setToolTip_(tooltip)

        if self.action is None:
            self.action = action

    @property
    def tooltip(self) -> str:
        """The tooltip text displayed when the cursor hovers over the menu item.
        """
        return self.xa_elem.toolTip()

    @tooltip.setter
    def tooltip(self, tooltip: str):
        self.xa_elem.setToolTip_(tooltip)

    def _run_action(self, button: int):
        """Runs the action associated with this menu item.

        .. versionadded:: 0.1.1
        """
        if callable(self.action):
            self.action(self, button, *self.args)

    def new_item(self, content: Union[str, None] = None, icon: Union['XABase.XAImage', None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, icon_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1, label: Union[str, None] = None, tooltip: Union[str, None] = None, multiselect: bool = False) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and places it in a submenu of this item.

        This will create a new submenu as needed, or will append to the existing submenu if one is already available on this item.

        :param content: The title text of the item, defaults to None
        :type content: Union[str, None], optional
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param action: The method to call when the item is clicked, defaults to None
        :type action: Union[Callable[[], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param icon_dimensions: The width and height of the image, in pixels, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the item in the list of menu items, defaults to -1
        :type index: int, optional
        :param label: The label to the left of the item's content
        :type label: Union[str, None], optional
        :param tooltip: The tooltip text for the menu item, defaults to None
        :type tooltip: Union[str, None], optional
        :param multiselect: Controls whether one or multiple options can be selected in a segmented control menu item, defaults to False
        :type multiselect: bool, optional
        :return: The newly created menu item object
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

        .. versionadded:: 0.1.2
        """
        # If no ID provided, use the title, then make it unique
        content = content or ""
        id = id or str(content)
        while id in self.items:
            id += "_"

        # Create a new submenu, if necessary
        submenu = self.xa_elem.submenu()
        if submenu is None:
            submenu = AppKit.NSMenu.alloc().init()

        if index == -1:
            index = submenu.numberOfItems()

        subitem = None
        if content == "separator":
            subitem =  XASeparatorMenuItem(self)
        elif content == "slider":
            subitem =  XASliderMenuItem(self, tooltip, action, args)
        elif content == "switch":
            subitem =  XASwitchMenuItem(self, label, tooltip, action, args)
        elif isinstance(content, list):
            subitem =  XASegmentedControlMenuItem(self, content, tooltip, action, args, multiselect)
        elif isinstance(content, XABase.XAImage):
            subitem = XAImageMenuItem(self, content, tooltip)
        elif isinstance(content, XABase.XAURL) or isinstance(content, XABase.XAPath):
            subitem = XAURLMenuItem(self, content, label, icon, icon_dimensions, tooltip, action, args)
        elif isinstance(content, str) or isinstance(content, int) or isinstance(content, float) or isinstance(content, bool):
            subitem = XATextMenuItem(self, str(content), icon, icon_dimensions, tooltip, action, args)
        else:
            subitem = XAMenuBarMenuItem(self, content, icon, action, args, icon_dimensions, id, index, label, tooltip)

        submenu.insertItem_atIndex_(subitem.xa_elem, index)
        self.xa_elem.menu().setSubmenu_forItem_(submenu, self.xa_elem)
        self.items[id] = subitem
        return self.items[id]

    def new_subitem(self, content: Union[str, None] = None, icon: Union['XABase.XAImage', None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, icon_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1, label: Union[str, None] = None, tooltip: Union[str, None] = None, multiselect: bool = False) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and places it in a submenu of this item.

        .. deprecated:: 0.1.2
        
           Use :func:`new_item` instead.

        .. versionadded:: 0.1.2
        """
        return self.new_item(content, icon, action, args, icon_dimensions, id, index, label, tooltip, multiselect)

    def remove_item(self, id: str):
        """Removes a subitem from this item's submenu.

        :param id: The ID of the subitem to remove
        :type id: str

        .. deprecated:: 0.1.2
        
           Use :func:`remove_item` instead.

        .. versionadded:: 0.1.1
        """
        item = self.items.pop(id)
        self.xa_elem.submenu().removeItem_(item.xa_elem)

    def remove_subitem(self, id: str):
        """Removes a subitem from this item's submenu.

        :param id: The ID of the subitem to remove
        :type id: str

        .. deprecated:: 0.1.2
        
           Use :func:`remove_item` instead.

        .. versionadded:: 0.1.1
        """
        item = self.items.pop(id)
        self.xa_elem.submenu().removeItem_(item.xa_elem)

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.1.2
        """
        if isinstance(self.parent, XAMenuBarMenu):
            self.parent.xa_elem.removeItem_(self.xa_elem)
        else:
            self.parent.xa_elem.submenu().removeItem_(self.xa_elem)




class XASliderMenuItem(XAMenuBarMenuItem):
    """A menu item containing a slider.

    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, tooltip: Union[str, None] = None, action: Union[Callable[['XASlider', Any], None], None] = None, args: Union[list[Any], None] = None, value: float = 50, min_value: float = 0, max_value: float = 100):
        """Initializes a new slider menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param tooltip: The tooltip text for this item, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the slider's value changes, defaults to None
        :type action: Union[Callable[[XASlider, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param value: The starting value of the slider, defaults to 50
        :type value: float, optional
        :param min_value: The minimum value of the slider, defaults to 0
        :type min_value: float, optional
        :param max_value: The maximum value of the slider, defaults to 100
        :type max_value: float, optional

        .. versionadded:: 0.1.2
        """
        slider_view = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 100, 30))
        self.slider = XASlider(action, args, value, min_value, max_value)
        slider_view.addSubview_(self.slider.xa_elem)
        self.xa_elem = slider_view
        super().__init__(parent, None)

    @property
    def value(self) -> float:
        return self.slider.value

    @value.setter
    def value(self, value: float):
        self.slider.value = value



class XASegmentedControlMenuItem(XAMenuBarMenuItem):
    """A menu item containing a segmented control.

    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, segments: Union[list[str], list[XABase.XAImage]], tooltip: Union[str, None] = None, action: Union[Callable[['XASlider', Any], None], None] = None, args: Union[list[Any], None] = None, multiselect: bool = False):
        """Initializes a new segmented control menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param segments: The strings or images to display as button options
        :type segments: Union[list[str], list[XABase.XAImage]]
        :param tooltip: The tooltip text for this item, defaults to None
        :type tooltip: Union[str, None], optional
        :param action: The method to call when the slider's value changes, defaults to None
        :type action: Union[Callable[[XASlider, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param multiselect: Whether multiple options can be selected at once, defaults to False
        :type multiselect: bool, optional

        .. versionadded:: 0.1.2
        """
        self.xa_elem = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 100, 25))
        self.segmented_control = XASegmentedControl(segments, action, args, multiselect)
        self.xa_elem.addSubview_(self.segmented_control.xa_elem)
        super().__init__(parent, None)




class XAImageMenuItem(XAMenuBarMenuItem):
    """A menu item containing an image.
    
    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, image: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath], tooltip: Union[str, None] = None):
        """Initializes an image menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param image: The image to display in the menu
        :type image: Union[str, int, float, XABase.XAImage, XABase.XAURL, XABase.XAPath]

        .. versionadded:: 0.1.2
        """
        self.xa_elem = AppKit.NSImageView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 200, image.size[1] * 200/image.size[0]))
        rounded_img = AppKit.NSImage.alloc().initWithSize_(image.xa_elem.size())
        rounded_img.setScalesWhenResized_(True)
        rounded_img.lockFocus()

        ctx = AppKit.NSGraphicsContext.currentContext()
        ctx.setImageInterpolation_(AppKit.NSImageInterpolationHigh)

        image_frame = AppKit.NSMakeRect(0, 0, *image.xa_elem.size())
        clip_path = AppKit.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(image_frame, 50, 50)
        clip_path.setWindingRule_(AppKit.NSWindingRuleEvenOdd)
        clip_path.addClip()

        image.xa_elem.drawAtPoint_fromRect_operation_fraction_(AppKit.NSZeroPoint, image_frame, AppKit.NSCompositingOperationSourceOver, 1)
        rounded_img.unlockFocus()

        self.xa_elem.setImage_(rounded_img)
        super().__init__(parent, image)




class XASwitchMenuItem(XAMenuBarMenuItem):
    """A menu item containing a labelled switch.

    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, label: Union[str, None] = None, tooltip: Union[str, None] = None, action: Union[Callable[['XASwitch', int, Any], None], None] = None, args: Union[list[Any], None] = None):
        """Initializes a new switch menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param label: The label displayed to the left of the switch, defaults to None
        :type label: Union[str, None], optional
        :param action: The method to call when the switch changes state, defaults to None
        :type action: Union[Callable[[XASwitch, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional

        .. versionadded:: 0.1.2
        """
        self.xa_elem = AppKit.NSView.alloc().initWithFrame_(AppKit.NSMakeRect(0, 0, 100, 30))
        if label is not None:
            self.__text = AppKit.NSText.alloc().initWithFrame_(AppKit.NSMakeRect(9, -7, 151, 32))
            self.__text.setString_(label)
            self.__text.setDrawsBackground_(False)

            font = AppKit.NSFont.menuBarFontOfSize_(0)
            self.__text.setFont_(font)
            self.xa_elem.addSubview_(self.__text)

        self.switch = XASwitch(action, args)
        self.xa_elem.addSubview_(self.switch.xa_elem)

        self.xa_elem.setWantsLayer_(True)
        self.xa_elem.setCanDrawSubviewsIntoLayer_(True)
        self.xa_elem.layer().setBackgroundColor_(XABase.XAColor(1, 0, 0).xa_elem)
        super().__init__(parent, None)

    @property
    def label(self) -> str:
        """The label for this switch menu item.
        """
        return self.__text.string()

    @label.setter
    def label(self, label: str):
        self.__text.setString_(label)




class XASeparatorMenuItem(XAMenuBarMenuItem):
    """A menu item containing a separator.
    
    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu):
        """Initializes a separator menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu

        .. versionadded:: 0.1.2
        """
        self.xa_elem = AppKit.NSMenuItem.separatorItem()
        super().__init__(parent, None)




class XATextMenuItem(XAMenuBarMenuItem):
    """A menu item containing text.
    
    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, text: str, icon: Union['XABase.XAImage', None] = None, icon_dimensions: tuple[int, int] = (20, 20), tooltip: Union[str, None] = None, action: Union[Callable[['XAURLMenuItem', int, Any], None], None] = None, args: Union[list[Any], None] = None):
        """Initializes a text menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param text: The text string to display
        :type text: str
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param icon_dimensions: The width and height of the icon, in pixels, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param action: The method to call when the user clicks the menu item, defaults to None
        :type action: Union[Callable[[XAURLMenuItem, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional

        .. versionadded:: 0.1.2
        """
        self.__text = text
        self.xa_elem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(text, 'action:', '')

        if isinstance(icon, XABase.XAImage):
            img = icon.xa_elem.copy()
            img.setScalesWhenResized_(True)
            img.setSize_(icon_dimensions)
            self.xa_elem.setImage_(img)

        super().__init__(parent, None, action=action, args=args)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
        self.xa_elem.setTitle_(text)

    @property
    def icon(self) -> 'XABase.XAImage':
        """The image associated with the menu item.
        """
        img_obj = self.xa_elem.image()
        if img_obj is None:
            return None
        return self.__icon

    @icon.setter
    def icon(self, icon: 'XABase.XAImage'):
        self.__icon = icon
        img = icon.xa_elem.copy()
        img.setScalesWhenResized_(True)
        img.setSize_(self.__icon_dimensions)
        self.xa_elem.setImage_(img)

    @property
    def icon_dimensions(self) -> tuple[int, int]:
        """The width and height of the menu item's image, in pixels.
        """
        return self.__icon_dimensions

    @icon_dimensions.setter
    def icon_dimensions(self, icon_dimensions: tuple[int, int]):
        self.__icon_dimensions = icon_dimensions
        size = AppKit.NSSizeFromCGSize(icon_dimensions)
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

    def new_subitem(self, content: Union[str, None] = None, icon: Union['XABase.XAImage', None] = None, action: Union[Callable[[], None], None] = None, args: Union[list[Any], None] = None, icon_dimensions: tuple[int, int] = (20, 20), id: Union[str, None] = None, index: int = -1, label: Union[str, None] = None, tooltip: Union[str, None] = None) -> 'XAMenuBarMenuItem':
        """Creates a new menu item and places it in a submenu of this item.

        This will create a new submenu as needed, or will append to the existing submenu if one is already available on this item.

        :param content: The title text of the item, defaults to None
        :type content: Union[str, None], optional
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param action: The method to call when the item is clicked, defaults to None
        :type action: Union[Callable[[], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional
        :param icon_dimensions: The width and height of the image, in pixels, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param id: A unique identifier for the item, defaults to None
        :type id: Union[str, None], optional
        :param index: The position to insert the item in the list of menu items, defaults to -1
        :type index: int, optional
        :param label: The label to the left of the item's content
        :type label: Union[str, None], optional
        :param tooltip: The tooltip text for the menu item, defaults to None
        :type tooltip: Union[str, None], optional
        :return: The newly created menu item object
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
        content = content or ""
        id = id or str(content)
        while id in self.items:
            id += "_"

        # Create a new submenu, if necessary
        submenu = self.xa_elem.submenu()
        if submenu is None:
            submenu = AppKit.NSMenu.alloc().init()

        if index == -1:
            index = submenu.numberOfItems()

        subitem = None
        if content == "separator":
            subitem =  XASeparatorMenuItem(self)
        elif content == "slider":
            subitem =  XASliderMenuItem(self, action, tooltip, args)
        elif content == "switch":
            subitem =  XASwitchMenuItem(self, label, tooltip, action, args)
        elif isinstance(content, XABase.XAImage):
            subitem = XAImageMenuItem(self, content, tooltip)
        elif isinstance(content, XABase.XAURL) or isinstance(content, XABase.XAPath):
            subitem = XAURLMenuItem(self, content, label, icon, icon_dimensions, tooltip, action, args)
        elif isinstance(content, str) or isinstance(content, int) or isinstance(content, float) or isinstance(content, bool):
            subitem = XATextMenuItem(self, str(content), icon, icon_dimensions, tooltip, action, args)
        else:
            subitem = XAMenuBarMenuItem(self, content, icon, action, args, icon_dimensions, id, index, label, tooltip)

        submenu.insertItem_atIndex_(subitem.xa_elem, index)
        self.xa_elem.menu().setSubmenu_forItem_(submenu, self.xa_elem)
        self.items[id] = subitem
        return self.items[id]

    def remove_subitem(self, id: str):
        """Removes a subitem from this item's submenu.

        :param id: The ID of the subitem to remove
        :type id: str

        .. versionadded:: 0.1.1
        """
        item = self.items.pop(id)
        self.xa_elem.submenu().removeItem_(item.xa_elem)



class XAURLMenuItem(XATextMenuItem):
    """A menu item containing a URL or path.
    
    .. versionadded:: 0.1.2
    """
    def __init__(self, parent: XAMenuBarMenu, url: Union[XABase.XAURL, XABase.XAPath], label: Union[str, None] = None, icon: Union['XABase.XAImage', None] = None, icon_dimensions: tuple[int, int] = (20, 20), tooltip: Union[str, None] = None, action: Union[Callable[['XAURLMenuItem', int, Any], None], None] = None, args: Union[list[Any], None] = None):
        """Initializes a URL menu item.

        :param parent: The menu containing this item
        :type parent: XAMenuBarMenu
        :param url: The URL or path to display
        :type url: Union[XABase.XAURL, XABase.XAPath]
        :param label: The text displayed for the item, or None to use the raw URL/path, defaults to None
        :type label: Union[str, None], optional
        :param icon: The image for the item, defaults to None
        :type icon: Union[XABase.XAImage, None], optional
        :param icon_dimensions: The width and height of the icon, in pixels, defaults to (20, 20)
        :type icon_dimensions: tuple[int, int], optional
        :param action: The method to call when the user clicks the menu item, defaults to None
        :type action: Union[Callable[[XAURLMenuItem, int, Any], None], None], optional
        :param args: The arguments to pass to the action method upon execution, defaults to None
        :type args: Union[list[Any], None], optional

        .. versionadded:: 0.1.2
        """
        self.__location = url
        self.xa_elem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(label or str(url.xa_elem), 'action:', '')
        if action is None:
            action = lambda item, button, *args: url.open() if button != -1 else None
        super().__init__(parent, label or str(url.xa_elem), icon=icon, icon_dimensions=icon_dimensions, tooltip=tooltip, action=action, args=args)

    @property
    def location(self) -> Union[XABase.XAURL, XABase.XAPath]:
        """The URL or path that the menu item refers to."""
        return self.__location

    @location.setter
    def location(self, location: Union[XABase.XAURL, XABase.XAPath]):
        self.__location = location
        self.xa_elem.setTitle_(self.label or str(location.xa_elem))

    @property
    def label(self) -> str:
        return self.xa_elem.title()

    @label.setter
    def label(self, label: Union[str, None]):
        self.xa_elem.setTitle_(label or str(self.content.xa_elem))