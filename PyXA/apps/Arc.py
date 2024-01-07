from typing import Any, Callable, Union
from enum import Enum

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

from ..XAProtocols import XACanOpenPath


class XAArcApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """The application's top-level scripting object.

    .. versionadded:: 0.3.0
    """

    class ObjectType(Enum):
        """The object types available for creation in Arc.

        .. versionadded:: 0.3.0
        """

        WINDOW = "window"
        TAB = "tab"
        SPACE = "space"

    class WindowMode(Enum):
        """Window modes for Arc windows.

        .. versionadded:: 0.3.0
        """

        NORMAL = "normal"
        INCOGNITO = "incognito"

    class TabLocation(Enum):
        """Tab locations for Arc tabs.

        .. versionadded:: 0.3.0
        """

        TOPAPP = "topApp"
        PINNED = "pinned"
        UNPINNED = "unpinned"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAArcWindow

    @property
    def name(self) -> "str":
        """The name of the application.

        .. versionadded:: 0.3.0
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> "bool":
        """Is this the frontmost (active) application?

        .. versionadded:: 0.3.0
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> "str":
        """The version of the application.

        .. versionadded:: 0.3.0
        """
        return self.xa_scel.version()

    def windows(self, filter: Union[dict, None] = None) -> "XAArcWindow":
        """Returns a list of windows, as PyXA objects, matching the given filter.

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_scel.windows(), XAArcWindowList, filter)

    def make(
        self,
        specifier: Union[str, "XAArcApplication.ObjectType"],
        properties: Union[dict, None] = None,
        data: Any = None,
    ) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAArcApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.3.0
        """
        if isinstance(specifier, XAArcApplication.ObjectType):
            specifier = specifier.value

        if data is None:
            camelized_properties = {}

            if properties is None:
                properties = {}

            for key, value in properties.items():
                if key == "url":
                    key = "URL"

                camelized_properties[XABase.camelize(key)] = value

            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithProperties_(camelized_properties)
            )
        else:
            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithData_(data)
            )

        if specifier == "window":
            return self._new_element(obj, XAArcWindow)
        elif specifier == "tab":
            return self._new_element(obj, XAArcTab)
        elif specifier == "space":
            return self._new_element(obj, XAArcSpace)


class XAArcWindowList(XABaseScriptable.XASBWindowList):
    """A wrapper around lists of windows that employs fast enumeration techniques.

    All properties of windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAArcWindow)

    def id(self) -> list["str"]:
        """The unique identifier of the window.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list["str"]:
        """The full title of the window.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def index(self) -> list["int"]:
        """The index of the window, ordered front to back.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def closeable(self) -> list["bool"]:
        """Whether the window has a close box.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("closeable"))

    def minimizable(self) -> list["bool"]:
        """Whether the window can be minimized.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("minimizable"))

    def minimized(self) -> list["bool"]:
        """Whether the window is currently minimized.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("minimized"))

    def resizable(self) -> list["bool"]:
        """Whether the window can be resized.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("resizable"))

    def visible(self) -> list["bool"]:
        """Whether the window is currently visible.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def zoomable(self) -> list["bool"]:
        """Whether the window can be zoomed.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable"))

    def zoomed(self) -> list[bool]:
        """Whether the window is currently zoomed.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed"))

    def active_tab(self) -> list["XAArcTab"]:
        """Returns the currently selected tab

        .. versionadded:: 0.3.0
        """
        ls = [x.activeTab() for x in self.xa_elem]
        return self._new_element(ls, XAArcTabList)

    def active_space(self) -> list["XAArcSpace"]:
        """Returns the currently active space

        .. versionadded:: 0.3.0
        """
        ls = [x.activeSpace() for x in self.xa_elem]
        return self._new_element(ls, XAArcSpaceList)

    def incognito(self) -> list["bool"]:
        """Whether the window is an incognito window.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("incognito"))

    def mode(self) -> list["XAArcApplication.WindowMode"]:
        """Represents the mode of the window which can be 'normal' or 'incognito', can be set only once during creation of the window.

        .. versionadded:: 0.3.0
        """
        ls = list(self.xa_elem.arrayByApplyingSelector_("mode"))
        return [XAArcApplication.WindowMode(mode) for mode in ls]

    def by_id(self, id: str) -> "XAArcWindow":
        """Retrieves the An application's window whose id matches the given id.

        .. versionadded:: 0.3.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> "XAArcWindow":
        """Retrieves the An application's window whose name matches the given name.

        .. versionadded:: 0.3.0
        """
        return self.by_property("name", name)

    def by_index(self, index: int) -> "XAArcWindow":
        """Retrieves the An application's window whose index matches the given index.

        .. versionadded:: 0.3.0
        """
        return self.by_property("index", index)

    def by_closeable(self, closeable: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose closeable matches the given closeable.

        .. versionadded:: 0.3.0
        """
        return self.by_property("closeable", closeable)

    def by_minimizable(self, minimizable: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose minimizable matches the given minimizable.

        .. versionadded:: 0.3.0
        """
        return self.by_property("minimizable", minimizable)

    def by_minimized(self, minimized: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose minimized matches the given minimized.

        .. versionadded:: 0.3.0
        """
        return self.by_property("minimized", minimized)

    def by_resizable(self, resizable: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose resizable matches the given resizable.

        .. versionadded:: 0.3.0
        """
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose visible matches the given visible.

        .. versionadded:: 0.3.0
        """
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose zoomable matches the given zoomable.

        .. versionadded:: 0.3.0
        """
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose zoomed matches the given zoomed.

        .. versionadded:: 0.3.0
        """
        return self.by_property("zoomed", zoomed)

    def by_active_tab(self, active_tab: "XAArcTab") -> "XAArcWindow":
        """Retrieves the An application's window whose active_tab matches the given active_tab.

        .. versionadded:: 0.3.0
        """
        for window in self:
            if window.active_tab.id == active_tab.id:
                return window

    def by_active_space(self, active_space: "XAArcSpace") -> "XAArcWindow":
        """Retrieves the An application's window whose active_space matches the given active_space.

        .. versionadded:: 0.3.0
        """
        for window in self:
            if window.active_space.id == active_space.id:
                return window

    def by_incognito(self, incognito: bool) -> "XAArcWindow":
        """Retrieves the An application's window whose incognito matches the given incognito.

        .. versionadded:: 0.3.0
        """
        return self.by_property("incognito", incognito)

    def by_mode(self, mode: "XAArcApplication.WindowMode") -> "XAArcWindow":
        """Retrieves the An application's window whose mode matches the given mode.

        .. versionadded:: 0.3.0
        """
        return self.by_property("mode", mode.value)


class XAArcWindow(XABaseScriptable.XASBWindow):
    """An application's window.

    .. versionadded:: 0.3.0
    """

    @property
    def id(self) -> "str":
        """The unique identifier of the window.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.id()

    @property
    def name(self) -> "str":
        """The full title of the window.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.name()

    @property
    def index(self) -> "int":
        """The index of the window, ordered front to back.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.index()

    @property
    def closeable(self) -> "bool":
        """Whether the window has a close box.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.closeable()

    @property
    def minimizable(self) -> "bool":
        """Whether the window can be minimized.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.minimizable()

    @property
    def minimized(self) -> "bool":
        """Whether the window is currently minimized.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.minimized()

    @property
    def resizable(self) -> "bool":
        """Whether the window can be resized.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.resizable()

    @property
    def visible(self) -> "bool":
        """Whether the window is currently visible.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> "bool":
        """Whether the window can be zoomed.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> "bool":
        """Whether the window is currently zoomed.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.zoomed()

    @property
    def active_tab(self) -> "XAArcTab":
        """Returns the currently selected tab

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.activeTab(), XAArcTab)

    @property
    def active_space(self) -> "XAArcSpace":
        """Returns the currently active space

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.activeSpace(), XAArcSpace)

    @property
    def incognito(self) -> "bool":
        """Whether the window is an incognito window.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.incognito()

    @property
    def mode(self) -> "str":
        """Represents the mode of the window which can be 'normal' or 'incognito', can be set only once during creation of the window.

        .. versionadded:: 0.3.0
        """
        mode = self.xa_elem.mode()
        return XAArcApplication.WindowMode(mode)

    def tabs(self, filter: Union[dict, None] = None) -> "XAArcTab":
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.tabs(), XAArcTabList, filter)

    def spaces(self, filter: Union[dict, None] = None) -> "XAArcSpace":
        """Returns a list of spaces, as PyXA objects, matching the given filter.

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.spaces(), XAArcSpaceList, filter)

    def close(self):
        """Close the window.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.close()


class XAArcTabList(XABase.XAList):
    """A wrapper around lists of tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAArcTab, filter)

    def id(self) -> list["str"]:
        """The unique identifier of the tab.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> list["str"]:
        """The full title of the tab.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def url(self) -> list["XABase.XAURLList"]:
        """The url of the tab.

        .. versionadded:: 0.3.0
        """
        ls = list(self.xa_elem.arrayByApplyingSelector_("URL"))
        return self._new_element(ls, XABase.XAURLList)

    def loading(self) -> list["bool"]:
        """Is loading?

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("loading"))

    def location(self) -> list["XAArcApplication.TabLocation"]:
        """Represents the location of the tab in the sidebar. Can be 'topApp', 'pinned', or 'unpinned'.

        .. versionadded:: 0.3.0
        """
        ls = list(self.xa_elem.arrayByApplyingSelector_("location"))
        return [XAArcApplication.TabLocation(location) for location in ls]

    def by_id(self, id: str) -> "XAArcTab":
        """Retrieves the A window's tabwhose id matches the given id.

        .. versionadded:: 0.3.0
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> "XAArcTab":
        """Retrieves the A window's tabwhose title matches the given title.

        .. versionadded:: 0.3.0
        """
        return self.by_property("title", title)

    def by_url(self, url: Union["str", "XABase.XAURL"]) -> "XAArcTab":
        """Retrieves the A window's tabwhose url matches the given url.

        .. versionadded:: 0.3.0
        """
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("URL", url)

    def by_loading(self, loading: bool) -> "XAArcTab":
        """Retrieves the A window's tabwhose loading matches the given loading.

        .. versionadded:: 0.3.0
        """
        return self.by_property("loading", loading)

    def by_location(self, location: "XAArcApplication.TabLocation") -> "XAArcTab":
        """Retrieves the A window's tabwhose location matches the given location.

        .. versionadded:: 0.3.0
        """
        return self.by_property("location", location.value)

    def __repr__(self):
        return f"<{self.__class__}{self.title()}>"


class XAArcTab(XABase.XAObject):
    """A window's tab.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> "str":
        """The unique identifier of the tab.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.id()

    @property
    def title(self) -> "str":
        """The full title of the tab.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.title()

    @property
    def url(self) -> "str":
        """The url of the tab.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.URL()

    @property
    def loading(self) -> "bool":
        """Is loading?

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.loading()

    @property
    def location(self) -> "XAArcApplication.TabLocation":
        """Represents the location of the tab in the sidebar. Can be 'topApp', 'pinned', or 'unpinned'.

        .. versionadded:: 0.3.0
        """
        loc = self.xa_elem.location()
        return XAArcApplication.TabLocation(loc)

    def go_back(self):
        """Go Back (If Possible).

        .. versionadded:: 0.3.0
        """
        self.xa_elem.goBack()

    def go_forward(self):
        """Go Forward (If Possible).

        .. versionadded:: 0.3.0
        """
        self.xa_elem.goForward()

    def execute_javascript(self, script: str) -> "Any":
        """Execute JavaScript in the context of the tab.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.executeJavascript_(script)

    def reload(self):
        """Reload the tab.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.reload()

    def stop(self):
        """Stop loading the tab.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.stop()

    def select(self):
        """Select the tab.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.select()

    def close(self):
        """Close the tab.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.close()

    def __repr__(self):
        return f"<{self.__class__}{self.title}>"


class XAArcSpaceList(XABase.XAList):
    """A wrapper around lists of spaces that employs fast enumeration techniques.

    All properties of spaces can be called as methods on the wrapped list, returning a list containing each space's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAArcSpace, filter)

    def id(self) -> list["str"]:
        """The unique identifier of the space.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> list["str"]:
        """The full title of the space.

        .. versionadded:: 0.3.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def by_id(self, id: str) -> "XAArcSpace":
        """Retrieves the A spacewhose id matches the given id.

        .. versionadded:: 0.3.0
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> "XAArcSpace":
        """Retrieves the A spacewhose title matches the given title.

        .. versionadded:: 0.3.0
        """
        return self.by_property("title", title)

    def __repr__(self):
        return f"<{self.__class__}{self.title()}>"


class XAArcSpace(XABase.XAObject):
    """A space.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> "str":
        """The unique identifier of the space.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.id()

    @property
    def title(self) -> "str":
        """The full title of the space.

        .. versionadded:: 0.3.0
        """
        return self.xa_elem.title()

    def tabs(self, filter: Union[dict, None] = None) -> "XAArcTab":
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.tabs(), XAArcTabList, filter)

    def focus(self):
        """Focus the space.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.focus()

    def __repr__(self):
        return f"<{self.__class__}{self.title}>"
