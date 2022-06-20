""".. versionadded:: 0.0.2

Control the macOS Shortcuts application using JXA-like syntax.
"""
from typing import Any, List, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

class XAShortcutsApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Podcasts.app.

    .. seealso:: :class:`XATextEditWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def run(self, shortcut: 'XAShortcut', input: Any = None) -> Any:
        return shortcut.run(input)

    # Folders
    def folders(self, filter: dict = None) -> List['XAShortcutFolder']:
        """Returns a list of folders matching the given filter.

        .. versionadded:: 0.0.2
        """
        return super().scriptable_elements("folders", filter, XAShortcutFolder)

    def folder(self, filter: Union[int, dict]) -> 'XAShortcutFolder':
        """Returns the first folder that matches the given filter.

        .. versionadded:: 0.0.2
        """
        return super().scriptable_element_with_properties("folders", filter, XAShortcutFolder)

    def first_folder(self) -> 'XAShortcutFolder':
        """Returns the folder at the first index of the folders array.

        .. versionadded:: 0.0.2
        """
        return super().first_scriptable_element("folders", XAShortcutFolder)

    def last_folder(self) -> 'XAShortcutFolder':
        """Returns the folder at the last (-1) index of the folders array.

        .. versionadded:: 0.0.2
        """
        return super().last_scriptable_element("folders", XAShortcutFolder)

    # Shortcuts
    def shortcuts(self, filter: dict = None) -> List['XAShortcut']:
        """Returns a list of shortcuts matching the given filter.

        .. versionadded:: 0.0.2
        """
        return super().scriptable_elements("shortcuts", filter, XAShortcut)

    def shortcut(self, filter: Union[int, dict]) -> 'XAShortcut':
        """Returns the first shortcut that matches the given filter.

        .. versionadded:: 0.0.2
        """
        return super().scriptable_element_with_properties("shortcuts", filter, XAShortcut)

    def first_shortcut(self) -> 'XAShortcut':
        """Returns the shortcut at the first index of the shortcuts array.

        .. versionadded:: 0.0.2
        """
        return super().first_scriptable_element("shortcuts", XAShortcut)

    def last_shortcut(self) -> 'XAShortcut':
        """Returns the shortcut at the last (-1) index of the shortcuts array.

        .. versionadded:: 0.0.2
        """
        return super().last_scriptable_element("shortcuts", XAShortcut)


class XAShortcutFolder(XABaseScriptable.XASBObject, XABase.XAHasAttachments):
    """A class for managing and interacting with folders of shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.xa_elem.id() #: A unique identifier for the folder
        self.name = self.xa_elem.name() #: The name string for the folder
        self.xa_scel = self.xa_prnt.xa_scel

    # Shortcuts
    def shortcuts(self, filter: dict = None) -> List['XAShortcut']:
        """Returns a list of shortcuts matching the given filter.

        .. versionadded:: 0.0.2
        """
        return super().elements("shortcuts", filter, XAShortcut)

    def shortcut(self, filter: Union[int, dict]) -> 'XAShortcut':
        """Returns the first shortcut that matches the given filter.

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("shortcuts", filter, XAShortcut)

    def first_shortcut(self) -> 'XAShortcut':
        """Returns the shortcut at the first index of the shortcuts array.

        .. versionadded:: 0.0.2
        """
        return super().first_element("shortcuts", XAShortcut)

    def last_shortcut(self) -> 'XAShortcut':
        """Returns the shortcut at the last (-1) index of the shortcuts array.

        .. versionadded:: 0.0.2
        """
        return super().last_element("shortcuts", XAShortcut)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"


class XAShortcut(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.xa_elem.id()
        self.name = self.xa_elem.name()
        self.subtitle = self.xa_elem.subtitle()
        self.folder = self.xa_elem.folder()
        self.color = XABase.XAColor().copy_color(self.xa_elem.color())
        self.icon = XABase.XAImage().copy_image(self.xa_elem.icon())
        self.accepts_input = self.xa_elem.acceptsInput()
        self.action_count = self.xa_elem.actionCount()

    def run(self, input: Any = None) -> Any:
        """Runs the shortcut with the provided input.

        :param input: The input to pass to the shortcut, defaults to None
        :type input: Any, optional
        :return: The value returned when the shortcut executes
        :rtype: Any

        .. versionadded:: 0.0.2
        """
        return self.xa_elem.runWithInput_(input)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"