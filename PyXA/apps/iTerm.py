""".. versionadded:: 0.1.0

Control iTerm using JXA-like syntax.
"""

from typing import Union

import AppKit
from PyXA import XABaseScriptable, XABase
from PyXA.XAProtocols import XACloseable, XADeletable, XAPrintable, XASelectable

class XAiTermApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with iTerm.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAiTermWindow

        self.current_window: XAiTermWindow #: The frontmost window
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether iTerm is the active application
        self.version: str #: The version of iTerm.app

    @property
    def current_window(self) -> 'XAiTermWindow':
        return self._new_element(self.xa_scel.current_window(), XAiTermWindow)

    @current_window.setter
    def current_window(self, current_window: 'XAiTermWindow'):
        self.set_property('currentWindow', current_window.xa_elem)

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def create_window(self, profile: Union[str, None] = None, command: Union[str, None] = None) -> 'XAiTermWindow':
        """Creates a new window with the given profile, executing the specified command upon the window's creation.

        :param profile: The profile to initialize the window with, defaults to None (default profile)
        :type profile: Union[str, None], optional
        :param command: The command to execute, defaults to None
        :type command: Union[str, None], optional
        :return: The newly created window object
        :rtype: XAiTermWindow

        .. versionadded:: 0.1.0
        """
        if profile is None:
            window = self.xa_scel.createWindowWithDefaultProfileCommand_(command)
        else:
            window = self.xa_scel.createWindowWithProfile_command_(profile, command)
        return self._new_element(window, XAiTermWindow)

    def create_hotkey_window(self, profile: Union[str, None] = None) -> 'XAiTermHotkeyWindow':
        """Creates a new hotkey window with the given profile.

        :param profile: The profile to initialize the window with, defaults to None
        :type profile: Union[str, None], optional
        :return: The newly created hotkey window object
        :rtype: XAiTermHotkeyWindow

        .. versionadded:: 0.1.0
        """
        window = self.xa_scel.createHotkeyWindowWithProfile_(profile)
        return self._new_element(window, XAiTermHotkeyWindow)

    def request_cookie_and_key(self, app: str) -> str:
        """Requests a Python API cookie for the specified application.

        :param app: The app to retrieve an API cookie for
        :type app: str
        :return: The API cookie
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.requestCookieAndKeyForAppNamed_(app)

    def launch_api_script(self, script_name: str, arguments: Union[list[str], None] = None):
        """Launches an API script by name, providing it with the given arguments.

        :param script_name: The name of the script to launch
        :type script_name: str
        :param arguments: The arguments to pass to the script, defaults to None
        :type arguments: Union[list[str], None], optional

        .. versionadded:: 0.1.0
        """
        if arguments is None:
            arguments = []
        self.xa_scel.launchAPIScriptNamed_arguments_(script_name, arguments)

    def invoke_api_expression(self, expression: str):
        """Invokes an expression, such as a registered function.

        :param expression: The expression to invoke
        :type expression: str

        .. versionadded:: 0.1.0
        """
        self.xa_scel.invokeAPIExpression_(expression)




class XAiTermWindow(XABaseScriptable.XASBWindow, XABase.XAObject, XASelectable, XACloseable):
    """A window of iTerm.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: int #: The unique identifier of the session
        self.alternate_identifier: str #: The alternate unique identifier of the session
        self.name: str #: The full title of the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.frontmost: bool #: Whether the window is currently the frontmost Terminal window
        self.current_tab: XAiTermTab #: The currently selected tab
        self.current_session: XAiTermSession #: The current session in a window
        self.is_hotkey_window: bool #: Whether the window is a hotkey window
        self.hotkey_window_profile: str #: If the window is a hotkey window, this gives the name of the profile that created the window
        self.position: tuple[int, int] #: The position os the window, relative to the upper left corner of the screen

        if self.is_hotkey_window:
            self.__class__ = XAiTermHotkeyWindow

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def alternate_identifier(self) -> str:
        return self.xa_elem.alternateIdentifier()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return (origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: tuple[int, int, int, int]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property("miniaturized", miniaturized)

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def frontmost(self) -> bool:
        return self.xa_elem.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def current_tab(self) -> 'XAiTermTab':
        return self._new_element(self.xa_elem.currentTab(), XAiTermTab)

    @current_tab.setter
    def current_tab(self, current_tab: 'XAiTermTab'):
        self.set_property('currentTab', current_tab.xa_elem)

    @property
    def current_session(self) -> 'XAiTermSession':
        return self._new_element(self.xa_elem.currentSession(), XAiTermSession)

    @current_session.setter
    def current_session(self, current_session: 'XAiTermSession'):
        self.set_property('currentSession', current_session.xa_elem)

    @property
    def is_hotkey_window(self) -> bool:
        return self.xa_elem.isHotkeyWindow()

    @is_hotkey_window.setter
    def is_hotkey_window(self, is_hotkey_window: bool):
        self.set_property('isHotkeyWindow', is_hotkey_window)

    @property
    def hotkey_window_profile(self) -> str:
        return self.xa_elem.hotkeyWindowProfile()

    @hotkey_window_profile.setter
    def hotkey_window_profile(self, hotkey_window_profile: str):
        self.set_property('hotkeyWindowProfile', hotkey_window_profile)

    @property
    def position(self) -> tuple[int, int]:
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    def create_tab(self, profile: Union[str, None] = None, command: Union[str, None] = None):
        """Creates a new tab with the given profile, executing the specified command upon the tab's creation.

        :param profile: The name of the profile to assign to the tab, if any, defaults to None (default profile)
        :type profile: Union[str, None], optional
        :param command: The command to run in the tab, if any, defaults to None
        :type command: Union[str, None], optional
        """
        if profile is None:
            self.xa_elem.createTabWithDefaultProfileCommand_(command)
        else:
            self.xa_elem.createTabWithProfile_command_(profile, command)

    def close(self):
        """Closes the window.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.close()




class XAiTermHotkeyWindow(XAiTermWindow):
    """A hotkey window of iTerm.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def reveal_hotkey_window(self):
        """Reveals the hotkey window.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.revealHotkeyWindow()

    def hide_hotkey_window(self):
        """Hides the hotkey window.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.hideHotkeyWindow()

    def toggle_hotkey_window(self):
        """Toggles the hotkey window.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.toggleHotkeyWindow()




class XAiTermTab(XABase.XAObject, XACloseable, XASelectable):
    """A tab of iTerm.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.current_session: XAiTermSession #: The current session in a tab
        self.index: int #: Index of tab in parent tab view control

    @property
    def current_session(self) -> 'XAiTermSession':
        return self._new_element(self.xa_elem.currentSession(), XAiTermSession)

    @current_session.setter
    def current_session(self, current_session: 'XAiTermSession'):
        self.set_property('currentSession', current_session.xa_elem)

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property('index', index)

    def close(self):
        """Closes the tab.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.close()

    def move_to(self, window: XAiTermWindow):
        self.xa_elem.moveTo_(window.xa_elem)




class XAiTermSession(XABase.XAObject, XACloseable, XASelectable):
    """A session of iTerm.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: The unique identifier of the session
        self.is_processing: bool #: Whether the session is currently processing
        self.is_at_shell_prompt: bool #: Whether the terminal is at the shell prompt
        self.columns: int #: The number of columns in the terminal window
        self.rows: int #: The number of rows in the terminal window
        self.tty: str #: The current TTY
        self.contents: str #: The currently visible contents of the session.
        self.text: str #: The currently visible contents of the session.
        self.color_preset: str #: The color preset of the session
        self.background_color: XABase.XAColor
        self.bold_color: XABase.XAColor
        self.cursor_color: XABase.XAColor
        self.cursor_text_color: XABase.XAColor
        self.foreground_color: XABase.XAColor
        self.selected_text_color: XABase.XAColor
        self.selection_color: XABase.XAColor
        self.ansi_black_color: XABase.XAColor
        self.ansi_red_color: XABase.XAColor
        self.ansi_green_color: XABase.XAColor
        self.ansi_yellow_color: XABase.XAColor
        self.ansi_blue_color: XABase.XAColor
        self.ansi_magenta_color: XABase.XAColor
        self.ansi_cyan_color: XABase.XAColor
        self.ansi_white_color: XABase.XAColor
        self.ansi_bright_black_color: XABase.XAColor
        self.ansi_bright_red_color: XABase.XAColor
        self.ansi_bright_green_color: XABase.XAColor
        self.ansi_bright_yellow_color: XABase.XAColor
        self.ansi_bright_blue_color: XABase.XAColor
        self.ansi_bright_magenta_color: XABase.XAColor
        self.ansi_bright_cyan_color: XABase.XAColor
        self.ansi_bright_white_color: XABase.XAColor
        self.underline_color: XABase.XAColor
        self.use_underline_color: bool #: Whether to use a dedicated color for underlining
        self.background_image: str #: The path of the background image file
        self.name: str #: The name of the session
        self.transparency: float #: The transparency of the session window
        self.unique_id: str #: The unique identifier of the session
        self.profile_name: str #: The session's profile name
        self.answerback_string: str #: ENQ Answerback string

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def is_processing(self) -> bool:
        return self.xa_elem.isProcessing()

    @is_processing.setter
    def is_processing(self, is_processing: bool):
        self.set_property('isProcessing', is_processing)

    @property
    def is_at_shell_prompt(self) -> bool:
        return self.xa_elem.isAtShellPrompt()

    @is_at_shell_prompt.setter
    def is_at_shell_prompt(self, is_at_shell_prompt: bool):
        self.set_property('isAtShellPrompt', is_at_shell_prompt)

    @property
    def columns(self) -> int:
        return self.xa_elem.columns()

    @columns.setter
    def columns(self, columns: int):
        self.set_property('columns', columns)

    @property
    def rows(self) -> int:
        return self.xa_elem.rows()

    @rows.setter
    def rows(self, rows: int):
        self.set_property('rows', rows)

    @property
    def tty(self) -> str:
        return self.xa_elem.tty()

    @property
    def contents(self) -> str:
        return self.xa_elem.contents()

    @contents.setter
    def contents(self, contents: str):
        self.set_property('contents', contents)

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    @property
    def color_preset(self) -> str:
        return self.xa_elem.colorPreset()

    @color_preset.setter
    def color_preset(self, color_preset: str):
        self.set_property('colorPreset', color_preset)

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property('backgroundColor', background_color.xa_elem)

    @property
    def bold_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.boldColor())

    @bold_color.setter
    def bold_color(self, bold_color: XABase.XAColor):
        self.set_property('boldColor', bold_color.xa_elem)

    @property
    def cursor_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.cursorColor())

    @cursor_color.setter
    def cursor_color(self, cursor_color: XABase.XAColor):
        self.set_property('cursorColor', cursor_color.xa_elem)

    @property
    def cursor_text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.cursorTextColor())

    @cursor_text_color.setter
    def cursor_text_color(self, cursor_text_color: XABase.XAColor):
        self.set_property('cursorTextColor', cursor_text_color.xa_elem)

    @property
    def foreground_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.foregroundColor())

    @foreground_color.setter
    def foreground_color(self, foreground_color: XABase.XAColor):
        self.set_property('foregroundColor', foreground_color.xa_elem)

    @property
    def selected_text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.selectedTextColor())

    @selected_text_color.setter
    def selected_text_color(self, selected_text_color: XABase.XAColor):
        self.set_property('selectedTextColor', selected_text_color.xa_elem)

    @property
    def selection_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.selectionColor())

    @selection_color.setter
    def selection_color(self, selection_color: XABase.XAColor):
        self.set_property('selectionColor', selection_color.xa_elem)

    @property
    def ansi_black_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBlackColor())

    @ansi_black_color.setter
    def ansi_black_color(self, ansi_black_color: XABase.XAColor):
        self.set_property('ANSIBlackColor', ansi_black_color.xa_elem)

    @property
    def ansi_red_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIRedColor())

    @ansi_red_color.setter
    def ansi_black_color(self, ansi_red_color: XABase.XAColor):
        self.set_property('ANSIRedColor', ansi_red_color.xa_elem)

    @property
    def ansi_green_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIGreenColor())

    @ansi_green_color.setter
    def ansi_green_color(self, ansi_green_color: XABase.XAColor):
        self.set_property('ANSIGreenColor', ansi_green_color.xa_elem)

    @property
    def ansi_yellow_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIYellowColor())

    @ansi_yellow_color.setter
    def ansi_yellow_color(self, ansi_yellow_color: XABase.XAColor):
        self.set_property('ANSIYellowColor', ansi_yellow_color.xa_elem)

    @property
    def ansi_blue_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBlueColor())

    @ansi_blue_color.setter
    def ansi_blue_color(self, ansi_blue_color: XABase.XAColor):
        self.set_property('ANSIBlueColor', ansi_blue_color.xa_elem)

    @property
    def ansi_magenta_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIMagentaColor())

    @ansi_magenta_color.setter
    def ansi_magenta_color(self, ansi_magenta_color: XABase.XAColor):
        self.set_property('ANSIMagentaColor', ansi_magenta_color.xa_elem)

    @property
    def ansi_cyan_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSICyanColor())

    @ansi_cyan_color.setter
    def ansi_cyan_color(self, ansi_cyan_color: XABase.XAColor):
        self.set_property('ANSICyanColor', ansi_cyan_color.xa_elem)

    @property
    def ansi_white_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIWhiteColor())

    @ansi_white_color.setter
    def ansi_white_color(self, ansi_white_color: XABase.XAColor):
        self.set_property('ANSIWhiteColor', ansi_white_color.xa_elem)

    @property
    def ansi_bright_black_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightBlackColor())

    @ansi_bright_black_color.setter
    def ansi_bright_black_color(self, ansi_bright_black_color: XABase.XAColor):
        self.set_property('ANSIBrightBlackColor', ansi_bright_black_color.xa_elem)

    @property
    def ansi_bright_red_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightRedColor())

    @ansi_bright_red_color.setter
    def ansi_bright_red_color(self, ansi_bright_red_color: XABase.XAColor):
        self.set_property('ANSIBrightRedColor', ansi_bright_red_color.xa_elem)

    @property
    def ansi_bright_green_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightGreenColor())

    @ansi_bright_green_color.setter
    def ansi_bright_green_color(self, ansi_bright_green_color: XABase.XAColor):
        self.set_property('ANSIBrightGreenColor', ansi_bright_green_color.xa_elem)

    @property
    def ansi_bright_yellow_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightYellowColor())

    @ansi_bright_yellow_color.setter
    def ansi_bright_yellow_color(self, ansi_bright_yellow_color: XABase.XAColor):
        self.set_property('ANSIBrightYellowColor', ansi_bright_yellow_color.xa_elem)

    @property
    def ansi_bright_blue_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightBlueColor())

    @ansi_bright_blue_color.setter
    def ansi_bright_blue_color(self, ansi_bright_blue_color: XABase.XAColor):
        self.set_property('ANSIBrightBlueColor', ansi_bright_blue_color.xa_elem)

    @property
    def ansi_bright_magenta_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightMagentaColor())

    @ansi_bright_magenta_color.setter
    def ansi_bright_magenta_color(self, ansi_bright_magenta_color: XABase.XAColor):
        self.set_property('ANSIBrightMagentaColor', ansi_bright_magenta_color.xa_elem)

    @property
    def ansi_bright_cyan_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightCyanColor())

    @ansi_bright_cyan_color.setter
    def ansi_bright_cyan_color(self, ansi_bright_cyan_color: XABase.XAColor):
        self.set_property('ANSIBrightCyanColor', ansi_bright_cyan_color.xa_elem)

    @property
    def ansi_bright_white_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.ANSIBrightWhiteColor())

    @ansi_bright_white_color.setter
    def ansi_bright_white_color(self, ansi_bright_white_color: XABase.XAColor):
        self.set_property('ANSIBrightWhiteColor', ansi_bright_white_color.xa_elem)

    @property
    def underline_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.underlineColor())

    @underline_color.setter
    def underline_color(self, underline_color: XABase.XAColor):
        self.set_property('underlineColor', underline_color.xa_elem)

    @property
    def use_underline_color(self) -> bool:
        return self.xa_elem.useUnderlineColor()

    @use_underline_color.setter
    def use_underline_color(self, use_underline_color: bool):
        self.set_property('useUnderlineColor', use_underline_color)

    @property
    def background_image(self) -> str:
        return self.xa_elem.backgroundImage()

    @background_image.setter
    def background_image(self, background_image: str):
        self.set_property('backgroundImage', background_image)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def transparency(self) -> float:
        return self.xa_elem.transparency()

    @transparency.setter
    def transparency(self, transparency: float):
        self.set_property('transparency', transparency)

    @property
    def unique_id(self) -> str:
        return self.xa_elem.uniqueID()

    @property
    def profile_name(self) -> str:
        return self.xa_elem.profileName()

    @property
    def answerback_string(self) -> str:
        return self.xa_elem.answerbackString()

    @answerback_string.setter
    def answerback_string(self, answerback_string: str):
        self.set_property('answerbackString', answerback_string)

    def split_vertically(self, profile: Union[str, None] = None, command: Union[str, None] = None):
        """Splits the session vertically, instantiating a new session with the specified profile.

        :param profile: The profile to instantiate the new session with, defaults to None (current profile)
        :type profile: Union[str, None], optional
        :param command: The command to run in the newly created session upon its creation, defaults to None
        :type command: Union[str, None], optional

        .. versionadded:: 0.1.0
        """
        if profile is None:
            self.xa_elem.splitVerticallyWithSameProfileCommand_(command)
        else:
            self.xa_elem.splitVerticallyWithProfile_command_(profile, command)

    def split_vertically_with_default_profile(self, command: Union[str, None]):
        """Splits the session vertically, instantiating a new session with the default profile.

        :param command: The command to run in the newly created session upon its creation, defaults to None
        :type command: Union[str, None]

        .. versionadded:: 0.1.0
        """
        self.xa_elem.splitVerticallyWithDefaultProfileCommand_(command)

    def split_horizontally(self, profile: Union[str, None] = None, command: Union[str, None] = None):
        """Splits the session horizontally, instantiating a new session with the specified profile.

        :param profile: The profile to instantiate the new session with, defaults to None (current profile)
        :type profile: Union[str, None], optional
        :param command: The command to run in the newly created session upon its creation, defaults to None
        :type command: Union[str, None], optional

        .. versionadded:: 0.1.0
        """
        if profile is None:
            self.xa_elem.splitHorizontallyWithSameProfileCommand_(command)
        else:
            self.xa_elem.splitHorizontallyWithProfile_command_(profile, command)

    def split_horizontally_with_default_profile(self, command: Union[str, None] = None):
        """Splits the session horizontally, instantiating a new session with the default profile.

        :param command: The command to run in the newly created session upon its creation, defaults to None
        :type command: Union[str, None]

        .. versionadded:: 0.1.0
        """
        self.xa_elem.splitHorizontallyWithDefaultProfileCommand_(command)

    def variable(self, variable_name: str) -> str:
        """Returns the value of a session variable with the given name.

        :param variable_name: The name of the variable to retrieve the value on
        :type variable_name: str
        :return: The value of the variable
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.variableNamed_(variable_name)

    def set_variable(self, variable_name: str, value: str) -> str:
        """Sets the value of a session variable.

        :param variable_name: The name of the variable to set
        :type variable_name: str
        :param value: The value to give the variable
        :type value: str
        :return: The new value of the variable
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.setVariableNamed_to_(variable_name, value)

    def write(self, text: Union[str, None] = None, file: Union[XABase.XAPath, str, None] = None, add_newline: bool = True):
        """Writes a string or file contents to the session.

        :param text: The text to input into the session, defaults to None
        :type text: Union[str, None], optional
        :param file: The file whose contents to input into the session, defaults to None
        :type file: Union[XABase.XAPath, str, None], optional
        :param add_newline: Whether to add a new line after inputting the specified content, defaults to True
        :type add_newline: bool, optional

        .. versionadded:: 0.1.0
        """
        if isinstance(file, str):
            file = XABase.XAPath(str)

        if file is None:
            self.xa_elem.writeContentsOfFile_text_newline_(None, text, add_newline)
        else:
            self.xa_elem.writeContentsOfFile_text_newline_(file.xa_elem, text, add_newline)

    def close(self):
        """Closes the session.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.close()