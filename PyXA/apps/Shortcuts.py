""".. versionadded:: 0.0.2

Control the macOS Shortcuts application using JXA-like syntax.
"""
from typing import Any, List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

class XAShortcutsApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Shortcuts.app.

    .. seealso:: :class:`XATextEditWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def run(self, shortcut: 'XAShortcut', input: Any = None) -> Any:
        """Runs the shortcut with the provided input.

        :param shortcut: The shortcut to run
        :type shortcut: XAShortcut
        :param input: The input to pass to the shortcut, defaults to None
        :type input: Any, optional
        :return: The return value of the last action to execute
        :rtype: Any

        .. versionadded:: 0.0.4
        """
        return shortcut.run(input)

    def folders(self, filter: dict = None) -> 'XAShortcutFolderList':
        """Returns a list of folders matching the given filter.

        :Example 1: Get all folders

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> print(app.folders())
        <<class 'PyXA.apps.Shortcuts.XAShortcutFolderList'>['Starter Shortcuts', 'Window Management', 'Dev Tools', ...]>

        :Example 2: Get the number of shortcuts contained in each folder

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> all_shortcuts = app.folders().shortcuts()
        >>> lengths = [len(ls) for ls in all_shortcuts]
        >>> print(lengths)
        [4, 3, 2, 15, 12, ...]

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutFolderList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.folders(), XAShortcutFolderList, filter)

    def shortcuts(self, filter: dict = None) -> 'XAShortcutList':
        """Returns a list of shortcuts matching the given filter.

        :Example 1: Get all shortcuts

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> print(app.shortcuts())
        <<class 'PyXA.apps.Shortcuts.XAShortcutList'>['Combine Screenshots & Share', 'Travel plans', 'Paywall Bypasser via Facebook', 'Display Notification', 'Text Converter For iMessage', ...]>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.shortcuts(), XAShortcutList, filter)


class XAShortcutFolderList(XABase.XAList):
    """A wrapper around lists of shortcuts folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folders's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAShortcutFolder, filter)

    def id(self) -> List[str]:
        """Gets the ID of each folder in the list.

        :return: A list of folder IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        """Gets the name of each folder in the list.

        :return: A list of folder names
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> Union['XAShortcutFolder', None]:
        """Retrieves the folder whose ID matches the given ID, if one exists.

        :return: The desired folder, if it is found
        :rtype: Union[XAShortcutFolder, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XAShortcutFolder', None]:
        """Retrieves the first folder whose name matches the given name, if one exists.

        :return: The desired folder, if it is found
        :rtype: Union[XAShortcutFolder, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def shortcuts(self, filter: dict = None) -> List['XAShortcutList']:
        """Gets the shortcuts within each folder in the list.

        :return: A list of lists of shortcuts.
        :rtype: List[XAShortcutList]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("shortcuts")
        return [self._new_element(x, XAShortcutList, filter) for x in ls.get()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAShortcutFolder(XABaseScriptable.XASBObject):
    """A class for managing and interacting with folders of shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: A unique identifier for the folder
        self.name: str #: The name string for the folder

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    # Shortcuts
    def shortcuts(self, filter: dict = None) -> 'XAShortcutList':
        """Returns a list of shortcuts matching the given filter.

        :Example 1: Get all shortcuts in a folder

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> folder = app.folders()[0]
        >>> print(folder.shortcuts())
        <<class 'PyXA.apps.Shortcuts.XAShortcutList'>['Text Last Image', 'Shazam shortcut', 'Make QR Code', 'Music Quiz', ...]>

        :Example 2: Get a list of shortcut colors in a folder

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> folder = app.folders()[0]
        >>> print(folder.shortcuts().color())
        [<<class 'PyXA.XABase.XAColor'>r=0.21521323919296265, g=0.7715266942977905, b=0.32515448331832886, a=0.0>, <<class 'PyXA.XABase.XAColor'>r=0.2379034161567688, g=0.3681696951389313, b=0.7627069354057312, a=0.0>, ...]>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shortcuts(), XAShortcutList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"

    def __eq__(self, other: 'XAShortcutFolder'):
        return self.id == other.id


class XAShortcutList(XABase.XAList):
    """A wrapper around lists of shortcuts that employs fast enumeration techniques.

    All properties of shortcuts can be called as methods on the wrapped list, returning a list containing each shortcut's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAShortcut, filter)

    def id(self) -> List[str]:
        """Gets the ID of each shortcut in the list.

        :return: A list of shortcut IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        """Gets the name of each shortcut in the list.

        :return: A list of shortcut names
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def subtitle(self) -> List[str]:
        """Gets the subtitle of each shortcut in the list.

        :return: A list of shortcut subtitles
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("subtitle"))

    def folder(self) -> XAShortcutFolderList:
        """Gets the containing folder of each shortcut in the list.

        :return: A list of shortcut folders containing the shortcuts in the list
        :rtype: XAShortcutFolderList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("id")
        return self._new_element(ls, XAShortcutFolderList)

    def color(self) -> List[XABase.XAColor]:
        """Gets the color of each shortcut in the list.

        :return: A list of colors
        :rtype: List[XABase.XAColor]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("color")
        return [XABase.XAColor(x) for x in ls]

    def icon(self) -> XABase.XAImageList:
        """Gets the icon of each shortcut in the list.

        :return: A list of shortcut icons
        :rtype: XABase.XAImageList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("icon")
        return self._new_element(ls, XABase.XAImageList)

    def accepts_input(self) -> List[bool]:
        """Gets the accept input status of each shortcut in the list.

        :return: A list of accept input statuses
        :rtype: List[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("acceptsInput"))

    def action_count(self) -> List[int]:
        """Gets the action count of each shortcut in the list.

        :return: A list of each shortcut's action count
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("actionCount"))

    def by_id(self, id: str) -> 'XAShortcut':
        """Gets the shortcut whose ID matches the given ID, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAShortcut':
        """Gets the first shortcut whose name matches the given name, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def by_subtitle(self, subtitle: str) -> 'XAShortcut':
        """Gets the first shortcut whose subtitle matches the given subtitle, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("subtitle", subtitle)

    def by_folder(self, folder: XAShortcutFolder) -> 'XAShortcut':
        """Gets the first shortcut whose parent folder matches the given folder, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("folder", folder.xa_elem)

    def by_color(self, color: XABase.XAColor) -> 'XAShortcut':
        """Gets the first shortcut whose color matches the given color, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("color", color.xa_elem)

    def by_icon(self, icon: XABase.XAImage) -> 'XAShortcut':
        """Gets the first shortcut whose icon matches the given icon, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("icon", icon.xa_elem)

    def by_accepts_input(self, accepts_input: bool) -> 'XAShortcut':
        """Gets the first shortcut whose accepts input status matches the given boolean value, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("acceptsInput", accepts_input)

    def by_action_count(self, action_count: int) -> 'XAShortcut':
        """Gets the first shortcut whose action count matches the given number, if one exists.

        :return: The desired shortcut, if it is found
        :rtype: XAShortcut
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("actionCount", action_count)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAShortcut(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the shortcut
        self.name: str #: The name of the shortcut
        self.subtitle: str #: The shortcut's subtitle
        self.folder: XAShortcutFolder #: The folder that contains the shortcut
        self.color: XABase.XAColor #: The color of the short
        self.icon: XABase.XAImage #: The shortcut's icon
        self.accepts_input: bool #: Whether the shortcut accepts input data
        self.action_count: int #: The number of actions in the shortcut

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def subtitle(self) -> str:
        return self.xa_elem.subtitle()

    @property
    def folder(self) -> XAShortcutFolder:
        return self._new_element(self.xa_elem.folder(), XAShortcutFolder)

    @property
    def color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.color())

    @property
    def icon(self) -> XABase.XAImage:
        return XABase.XAImage(self.xa_elem.icon())

    @property
    def accepts_input(self) -> bool:
        return self.xa_elem.acceptsInput()

    @property
    def action_count(self) -> int:
        return self.xa_elem.actionCount()

    def run(self, input: Any = None) -> Any:
        """Runs the shortcut with the provided input.

        :param input: The input to pass to the shortcut, defaults to None
        :type input: Any, optional
        :return: The value returned when the shortcut executes
        :rtype: Any

        :Example 1: Run a shortcut without inputs

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> folder = app.folders().by_name("Dev Tools")
        >>> shortcut = folder.shortcuts().by_name("Show IP Address")
        >>> shortcut.run()

        :Example 2: Run a shortcut with text input

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> shortcut = app.shortcuts().by_name("Show Notification")
        >>> shortcut.run("Testing 1 2 3...")

        :Example 3: Run a shortcut with URL input

        >>> import PyXA
        >>> app = PyXA.application("Shortcuts")
        >>> safari = PyXA.application("Safari")
        >>> document = safari.document(0)
        >>> shortcut = app.shortcuts().by_name("Save URL as PDF")
        >>> shortcut.run(document.url)

        .. versionadded:: 0.0.2
        """
        if isinstance(input, XABase.XAObject):
            input = input.xa_elem
        return self.xa_elem.runWithInput_(input)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"

    def __eq__(self, other: 'XAShortcut'):
        return self.id == other.id