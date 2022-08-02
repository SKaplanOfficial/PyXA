""".. versionadded:: 0.0.6

Control the macOS Maps application using JXA-like syntax.
"""

from typing import List, Literal, Union
from AppKit import NSPredicate

from PyXA import XABase
from PyXA import XABaseScriptable

class XAMapsApplication(XABase.XAApplication):
    """A class for managing and interacting with Maps.app.

    .. seealso:: :class:`XAMapsSidebarLocation`, :class:`XAMapsDirection`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.sidebar_showing: bool #: Whether the sidebar is currently showing

    @property
    def sidebar_showing(self) -> bool:
        sidebar = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[1]
        return sidebar.get() is not None

    # TODO: This
    # def set_view(self, view: Literal[""])

    def toggle_sidebar(self):
        """Toggles the sidebar.

        .. versionadded:: 0.0.6
        """
        self.front_window().toolbars()[0].buttons()[0].actions().by_name("AXPress").perform()

    def search(self, query: str, latitude: Union[float, None] = None, longitude: Union[float, None] = None, exact: bool = True):
        """Searches Maps for the given query, centered at the (optional) specified location.

        :param query: The term to search for
        :type query: str
        :param latitude: The latitude of the location to center the search at, defaults to None
        :type latitude: Union[float, None], optional
        :param longitude: The longitude of the location to center the search at, defaults to None
        :type longitude: Union[float, None], optional
        :param exact: Whether search results must be centered on the specified location versus allowing further away results, defaults to True
        :type exact: bool, optional

        .. versionadded:: 0.0.6
        """
        url = "maps://?q=" + query
        if latitude is not None and longitude is not None:
            if exact is True:
                url += f"&sll={latitude},{longitude}"
            else:
                url += f"&near={latitude},{longitude}"
        XABase.XAURL(url).open()

    def zoom_in(self) -> 'XAMapsApplication':
        """Zoom in on the currently centered location of the map.

        .. versionadded:: 0.0.6
        """
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = locations = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[5].buttons()[2].actions().filteredArrayUsingPredicate_(predicate)[0]
        press_action.perform()

    def zoom_out(self) -> 'XAMapsApplication':
        """Zoom out on the currently centered location of the map.

        .. versionadded:: 0.0.6
        """
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = locations = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[5].buttons()[1].actions().filteredArrayUsingPredicate_(predicate)[0]
        press_action.perform()

    def orient_north(self) -> 'XAMapsApplication':
        """Orients the map with North facing upward.

        .. versionadded:: 0.0.6
        """
        self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[5].buttons()[0].actions()[0].perform()

    def show_address(self, address: str):
        """Centers the map at the specified address.

        :param address: The address to display
        :type address: str

        .. versionadded:: 0.0.6
        """
        XABase.XAURL("maps://?address=" + address).open()

    def show_coordinate(self, latitude: float, longitude: float):
        """Centers the map at the specified coordinate.

        :param latitude: The latitude of the coordinate to display
        :type latitude: float
        :param longitude: The longitude of the coordinate to display
        :type longitude: float

        .. versionadded:: 0.0.6
        """
        url = f"maps://?ll={latitude},{longitude}"
        XABase.XAURL(url).open()

    def drop_pin(self, latitude: float, longitude: float, name: Union[str, None] = None):
        """Drops at pin at the specified coordinate.

        :param latitude: The latitude of the coordinate at which to drop a pin
        :type latitude: float
        :param longitude: The longitude of the coordinate at which to drop a pin
        :type longitude: float
        :param name: The name of the pin, defaults to None
        :type name: Union[str, None], optional

        .. versionadded:: 0.0.6
        """
        if name is None:
            name = "New Pin"
        url = f"maps://?q={name}&ll={latitude},{longitude}"
        XABase.XAURL(url).open()

    def directions_to(self, destination_address: str, source_address: Union[str, None] = None, transport_type: Union[Literal["d", "driving", "w", "walking", "p", "pt", "r", "public transit", "transit"], None] = None): # Eventually return XAMapsDirections object?
        """Queries for directions to the destination address, optionally starting from a source address.

        If no source address is provided, the current location is used.

        :param destination_address: The address to retrieve directions to
        :type destination_address: str
        :param source_address: The address to start the directions from, defaults to None
        :type source_address: Union[str, None], optional
        :param transport_type: The type of directions to retrieve, defaults to None
        :type transport_type: Union[Literal["d", "driving", "w", "walking", "p", "pt", "r", "public transit", "transit"], None], optional

        .. versionadded:: 0.0.6
        """
        url = "maps://?daddr=" + destination_address.replace(" ", "%20")
        if source_address is not None:
            url += "&saddr=" + source_address
        if transport_type is not None:
            if transport_type == "driving" or transport_type == "d":
                url += "&dirflg=d"
            elif transport_type == "walking" or transport_type == "w":
                url += "&dirflg=w"
            elif transport_type in ["public transit", "transit", "p", "pt", "r"]:
                url += "&dirflg=r"
        XABase.XAURL(url).open()

    def new_tab(self):
        """Opens a new tab.

        .. versionadded:: 0.0.6
        """
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = self.front_window().xa_elem.tabGroups()[0].buttons()[0].actions().filteredArrayUsingPredicate_(predicate)[0]
        press_action.perform()

    def tabs(self) -> 'XAMapsTabList':
        """Gets a list of tabs.

        :return: The list of tabs
        :rtype: XAMapsTabList

        .. versionadded:: 0.0.6
        """
        tabs = self.front_window().xa_elem.tabGroups()[0].radioButtons()
        return self._new_element(tabs, XAMapsTabList)

    def sidebar_locations(self) -> 'XAMapsSidebarLocationList':
        """Gets a list of sidebar locations.

        :return: The list of locations
        :rtype: XAMapsSidebarLocationList

        .. versionadded:: 0.0.6
        """
        if not self.sidebar_showing:
            self.toggle_sidebar()

        locations = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].UIElements()

        predicate = NSPredicate.predicateWithFormat_("role == %@", "AXGenericElement")
        locations = locations.filteredArrayUsingPredicate_(predicate)

        return self._new_element(locations, XAMapsSidebarLocationList)




class XAMapsTabList(XABase.XAList):
    """A wrapper around a list of locations.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMapsTab, filter)

    # def name(self) -> List[str]:
    #     ls = self.xa_elem.arrayByApplyingSelector_("objectDescription")
    #     return [x.split(",")[0] for x in ls]

    # def __repr__(self):
    #     return "<" + str(type(self)) + str(self.name()) + ">"

class XAMapsTab(XABase.XAObject):
    """A class for interacting with sidebar locations in Maps.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.properties: dict #: All properties of the tab
        self.title: str #: The name of the tab
        self.selected: bool #: Whether the tab is the currently selected tab

        print(self.xa_elem.properties())

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def selected(self) -> bool:
        return self.xa_elem.value == 1

    def close(self):
        self.xa_elem.buttons()[0].actions()[0].perform()



class XAMapsSidebarLocationList(XABase.XAList):
    """A wrapper around a list of sidebar locations.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMapsSidebarLocation, filter)

    def name(self) -> List[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("objectDescription")
        return [x.split(",")[0] for x in ls]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAMapsSidebarLocation(XABase.XAObject):
    """A class for interacting with sidebar locations in Maps.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.selected: bool #: Whether the location element is currently selected
        self.description: str #: The description of the location element
        self.name: str #: The name of the location

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    @property
    def description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def name(self) -> str:
        return self.description.split(",")[0]

    def show_directions_to(self):
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = locations = self.xa_elem.actions().filteredArrayUsingPredicate_(predicate)[0]
        press_action.perform()




class XAMapsDirectionsList(XABase.XAList):
    """A wrapper around a list of directions.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMapsDirections, filter)

class XAMapsDirections(XABase.XAObject):
    """A class for interacting with directions in Maps.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.source_address: str #: The starting address of the directions
        self.destination_address: str #: The ending address of the directions
        self.duration: float #: The duration of the currently selected route from the source address to the destination address
        self.has_tolls: bool #: Whether the currently selected route has tolls
        self.has_weather_warnings: bool #: Whether there are weather warnings along the currently selected route