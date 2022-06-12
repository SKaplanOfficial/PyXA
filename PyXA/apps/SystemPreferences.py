""".. versionadded:: 0.0.2

Control the macOS System Preferences application using JXA-like syntax.
"""
from typing import List, Union

from PyXA import XABase
from PyXA import XABaseScriptable

class XASystemPreferencesApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Podcasts.app.

     .. seealso:: :class:`XAPreferencePane`, :class:`XAPreferenceAnchor`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.show_all = self.xa_scel.showAll() #: Whether the system preferences is in show all view
        self.__current_pane = None #: The currently selected preference pane
        self.__preferences_window = None #: The main preferences window

    def panes(self, properties: Union[dict, None] = None) -> List['XAPreferencePane']:
        """Returns a list of preference panes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned preference panes will have, or None
        :type filter: Union[dict, None]
        :return: The list of preference panes
        :rtype: List[XAPreferencePane]

        :Example 1: List all preference panes

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes())
        [<<class 'PyXA.apps.SystemPreferences.XAPreferencePane'>Accessibility, id=com.apple.preference.universalaccess>, <<class 'PyXA.apps.SystemPreferences.XAPreferencePane'>Apple ID, id=com.apple.preferences.AppleIDPrefPane>, ...]

        :Example 2: List preference panes after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))
        [<<class 'PyXA.apps.SystemPreferences.XAPreferencePane'>Accessibility, id=com.apple.preference.universalaccess>]

        .. versionadded:: 0.0.2
        """
        return super().scriptable_elements("panes", properties, XAPreferencePane)

    def pane(self, properties: Union[int, dict]) -> List['XAPreferencePane']:
        """Returns the first preference pane matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned preference pane will have
        :type filter: Union[int, dict]
        :return: The preference pane
        :rtype: XAPreferencePane

        :Example 1: Get a preference pane by index

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.pane(0))
        <<class 'PyXA.apps.SystemPreferences.XAPreferencePane'>Accessibility, id=com.apple.preference.universalaccess>

        :Example 2: Get a preference pane by using a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))
        <<class 'PyXA.apps.SystemPreferences.XAPreferencePane'>Accessibility, id=com.apple.preference.universalaccess>

        .. versionadded:: 0.0.2
        """
        return super().scriptable_element_with_properties("panes", properties, XAPreferencePane)

    def first_pane(self) -> 'XAPreferencePane':
        """Returns the preference pane at the zero index of the panes array.

        :return: The first preference pane
        :rtype: XAPreferencePane

        .. versionadded:: 0.0.2
        """
        return super().first_scriptable_element("panes", XAPreferencePane)

    def last_pane(self) -> 'XAPreferencePane':
        """Returns the preference pane at the last (-1) index of the panes array.

        :return: The last preference pane
        :rtype: XAPreferencePane

        .. versionadded:: 0.0.2
        """
        return super().last_scriptable_element("panes", XAPreferencePane)


class XAPreferencePane(XABase.XAHasElements, XABase.XARevealable):
    """A class for managing and interacting with preference panes in System Preferences.

    .. seealso:: :class:`XAPreferenceAnchor`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str = self.xa_elem.id() #: A unique identifier for the preference pane independent of locale
        self.localized_name: str = self.xa_elem.localizedName() #: The locale-dependant name of the preference pane
        self.name: str = self.xa_elem.name() #: The name of the preference pane as it appears in the title bar

    def authorize(self):
        self.xa_scel.authorize()

    def anchors(self, properties: Union[dict, None] = None) -> List['XAPreferenceAnchor']:
        """Returns a list of anchors, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned anchors will have, or None
        :type filter: Union[dict, None]
        :return: The list of anchors
        :rtype: List[XAPreferenceAnchor]

        :Example 1: Listing all anchors
        
        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.pane(0)
        >>> print(pane.anchors())
        [<<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchor'>Accessibility_Shortcut>, <<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchor'>Seeing_Cursor>, ...]

        :Example 2: List anchors after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.pane(0)
        >>> print(pane.anchors({"name": "Keyboard"}))
        [<<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchor'>Keyboard>]

        .. versionadded:: 0.0.2
        """
        return super().elements("anchors", properties, XAPreferenceAnchor)

    def anchor(self, properties: Union[int, dict]) -> List['XAPreferenceAnchor']:
        """Returns the first anchor matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned anchor will have
        :type filter: Union[int, dict]
        :return: The anchor
        :rtype: XAPreferenceAnchor

        :Example 1: Get an anchor by index

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.pane(0)
        >>> print(pane.anchor(0))
        <<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchor'>Accessibility_Shortcut>

        :Example 2: Get an anchor by applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> pane = app.pane(0)
        >>> print(pane.anchor({"name": "Full_Keyboard_Access"}))
        <<class 'PyXA.apps.SystemPreferences.XAPreferenceAnchor'>Full_Keyboard_Access>

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("anchors", properties, XAPreferenceAnchor)

    def first_anchor(self) -> 'XAPreferenceAnchor':
        """Returns the anchor at the zero index of the anchors array.

        :return: The first anchor
        :rtype: XAPreferenceAnchor

        .. versionadded:: 0.0.2
        """
        return super().first_element("anchors", XAPreferenceAnchor)

    def last_anchor(self) -> 'XAPreferenceAnchor':
        """Returns the anchor at the last (-1) index of the anchors array.

        :return: The last anchor
        :rtype: XAPreferenceAnchor

        .. versionadded:: 0.0.2
        """
        return super().last_element("anchors", XAPreferenceAnchor)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"


class XAPreferenceAnchor(XABase.XARevealable):
    """A class for managing and interacting with anchors in System Preferences.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name = self.xa_elem.name() #: The name of the anchor

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"