""".. versionadded:: 0.0.2

Control the macOS System Preferences application using JXA-like syntax.
"""

from typing import List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

class XASystemPreferencesApplication(XABaseScriptable.XASBApplication):
    """A class for interacting with System Preferences.app.

    .. seealso:: :class:`XAPreferencePane`, :class:`XAPreferenceAnchor`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether System Preferences is the active application
        self.version: str #: The version of System Preferences.app
        self.show_all: bool #: Whether the system preferences is in show all view
        self.current_pane: XAPreferencePane #: The currently selected preference pane
        self.preferences_window: XABaseScriptable.XASBWindow #: The main preferences window

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def show_all(self) -> bool:
        return self.xa_scel.showAll()

    @property
    def current_pane(self) -> 'XAPreferencePane':
        return self._new_element(self.xa_scel.currentPane(), XAPreferencePane)

    @property
    def preferences_window(self) -> XABaseScriptable.XASBWindow:
        return self._new_element(self.xa_scel.preferencesWindow(), XABaseScriptable.XASBWindow)

    def panes(self, filter: Union[dict, None] = None) -> 'XAPreferencePaneList':
        """Returns a list of preference panes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned preference panes will have, or None
        :type filter: Union[dict, None]
        :return: The list of preference panes
        :rtype: List[XAPreferencePane]

        :Example 1: List all preference panes

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes())
        <<class 'PyXA.apps.SystemPreferences.XAPreferencePaneList'>['Accessibility', 'Apple ID', 'Battery', ...]>

        :Example 2: List preference panes after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Battery"}))
        <<class 'PyXA.apps.SystemPreferences.XAPreferencePaneList'>['Battery']>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAPreferencePaneList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.panes(), XAPreferencePaneList, filter)


class XAPreferencePaneList(XABase.XAList):
    """A wrapper around lists of preference panes that employs fast enumeration techniques.

    All properties of panes can be called as methods on the wrapped list, returning a list containing each pane's value for the property.

    :Example 1: List the name of each preference pane

    >>> import PyXA
    >>> app = PyXA.application("System Preferences")
    >>> print(app.panes().name())
    ['Accessibility', 'Apple ID', 'Battery', 'Bluetooth', ...]

    :Example 2: Get a preference pane by name (two ways)

    >>> import PyXA
    >>> app = PyXA.application("System Preferences")
    >>> pane1 = app.panes().by_name("Battery")
    >>> pane2 = app.panes({"name": "Battery"})[0]
    >>> print(pane1 == pane2)
    True

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPreferencePane, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def localized_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("localizedName"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XAPreferencePane':
        return self.by_property("id", id)

    def by_localized_name(self, localized_name: str) -> 'XAPreferencePane':
        return self.by_property("localizedName", localized_name)

    def by_name(self, name: str) -> 'XAPreferencePane':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPreferencePane(XABase.XAHasElements):
    """A class for managing and interacting with preference panes in System Preferences.

    .. seealso:: :class:`XAPreferenceAnchor`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: A unique identifier for the preference pane independent of locale
        self.localized_name: str #: The locale-dependant name of the preference pane
        self.name: str #: The name of the preference pane as it appears in the title bar

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def localized_name(self) -> str:
        return self.xa_elem.localizedName()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def anchors(self, filter: Union[dict, None] = None) -> 'XAPreferenceAnchorList':
        """Returns a list of anchors, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned anchors will have, or None
        :type filter: Union[dict, None]
        :return: The list of anchors
        :rtype: List[XAPreferenceAnchor]

        :Example 1: Listing all anchors
        
        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.panes()[0]
        >>> print(pane.anchors())
        <<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchorList'>['Accessibility_Shortcut', 'Seeing_Cursor', ...]>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAPreferenceAnchorList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.anchors(), XAPreferenceAnchorList, filter)

    def reveal(self) -> 'XAPreferencePane':
        """Reveals the preference pane in the System Preferences window.

        :return: A reference to the pane object.
        :rtype: XAPreferencePane

        :Example 1: Reveal the `Displays` preference pane

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> app.activate()
        >>> app.panes().by_name("Displays").reveal()

        .. versionadded:: 0.0.4
        """
        self.xa_elem.reveal()
        return self

    def authorize(self) -> 'XAPreferencePane':
        """Prompts for authorization for the preference pane.

        :return: A reference to the pane object.
        :rtype: XAPreferencePane

        :Example 1: Prompt for authorization for the `Date & Time` pane

        >>> import PyXA
        >>> from time import sleep
        >>> app = PyXA.application("System Preferences")
        >>> app.activate()
        >>> pane = app.panes().by_name("Date & Time")
        >>> pane.reveal()
        >>> sleep(0.5) # Wait for animation to finish
        >>> pane.authorize()

        .. versionadded:: 0.0.2
        """
        self.xa_elem.authorize()
        return self

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"

    def __eq__(self, other: 'XAPreferencePane'):
        return self.id == other.id


class XAPreferenceAnchorList(XABase.XAList):
    """A wrapper around lists of preference anchors that employs fast enumeration techniques.

    All properties of anchors can be called as methods on the wrapped list, returning a list containing each anchor's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPreferenceAnchor, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_name(self, name: str) -> 'XAPreferenceAnchor':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPreferenceAnchor(XABaseScriptable.XASBObject):
    """A class for managing and interacting with anchors in System Preferences.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the anchor

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def reveal(self) -> 'XAPreferenceAnchor':
        """Reveals the anchor in the System Preferences window.

        :return: A reference to the anchor object.
        :rtype: XAPreferenceAnchor

        :Example 1: Reveal the `Siri` anchor in the `Accessibility` pane

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.panes().by_name("Accessibility")
        >>> anchor = pane.anchors().by_name("Siri")
        >>> anchor.reveal()

        .. versionadded:: 0.0.4
        """
        self.xa_elem.reveal()
        return self

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"

    def __eq__(self, other: 'XAPreferenceAnchor'):
        return self.name == other.name
