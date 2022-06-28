""".. versionadded:: 0.0.3

Control Chromium using JXA-like syntax.
"""

from typing import Any, List, Tuple, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

class XAChromiumApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Chromium.app.

    .. seealso:: :class:`XAChromiumWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAChromiumWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Chromium is the active application
        self.version: str #: The version of Chromium
        self.bookmarks_bar: XAChromiumBookmarkFolder #: The bookmarks bar bookmark folder
        self.other_bookmarks: XAChromiumBookmarkFolder #: The other bookmarks bookmark folder

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
    def bookmarks_bar(self) -> 'XAChromiumBookmarkFolder':
        return self._new_element(self.xa_scel.bookmarksBar(), XAChromiumBookmarkFolder)

    @property
    def other_bookmarks(self) -> 'XAChromiumBookmarkFolder':
        return self._new_element(self.xa_scel.otherBookmarks(), XAChromiumBookmarkFolder)

    def open(self, url: Union[str, NSURL] = "https://google.com") -> 'XAChromiumApplication':
        """Opens a URL in a new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Chromium application object.
        :rtype: XAChromiumApplication

        :Example 1: Open a local or external URL

           >>> import PyXA
           >>> app = PyXA.application("Chromium")
           >>> app.open("https://www.google.com")
           >>> app.open("google.com")
           >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.3
        """
        if isinstance(url, str):
            if url.startswith("/"):
                # URL is a path to file
                self.xa_wksp.openFile_application_(url, self.xa_scel)
                return self
            # Otherwise, URL is web address
            elif not url.startswith("http"):
                url = "http://" + url
            url = XABase.xa_url(url)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAChromiumBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.bookmarkFolders(), XAChromiumBookmarkFolderList, filter)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.4
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "tab":
            return self._new_element(obj, XAChromiumTab)

    
class XAChromiumWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Chromium windows.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumTab`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.given_name: str #: The given name of the window
        self.name: str #: The full title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.minimizable: bool #: Whether the window can be minimized
        self.minimized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.mode: str #: The mode of the window, either "normal" or "incognito"
        self.active_tab_index: int #: The index of the active tab
        self.active_tab: XAChromiumTab #: The currently selected tab

    @property
    def given_name(self) -> str:
        return self.xa_scel.givenName()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def id(self) -> int:
        return self.xa_scel.id()

    @property
    def index(self) -> int:
        return self.xa_scel.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_scel.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_scel.closeable()

    @property
    def minimizable(self) -> bool:
        return self.xa_scel.minimizable()

    @property
    def minimized(self) -> bool:
        return self.xa_scel.minimized()

    @property
    def resizable(self) -> bool:
        return self.xa_scel.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_scel.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_scel.zoomed()

    @property
    def mode(self) -> str:
        return self.xa_scel.mode()

    @property
    def active_tab_index(self) -> int:
        return self.xa_scel.activeTabIndex() 

    @property
    def active_tab(self) -> 'XAChromiumTab':
        return self._new_element(self.xa_scel.activeTab(), XAChromiumTab)

    def tabs(self, filter: Union[dict, None] = None) -> 'XAChromiumTabList':
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter tabs by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of tabs
        :rtype: XAChromiumTabList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.tabs(), XAChromiumTabList, filter)


class XAChromiumTabList(XABase.XAList):
    """A wrapper around a list of tabs.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumTab, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def loading(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loading"))

    def by_id(self, id: int) -> 'XAChromiumTab':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAChromiumTab':
        return self.by_property("title", title)

    def by_url(self, url: str) -> 'XAChromiumTab':
        return self.by_property("url", url)

    def by_loading(self, loading: bool) -> 'XAChromiumTab':
        return self.by_property("loading", loading)

class XAChromiumTab(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Chromium tabs.

    .. seealso:: :class:`XAChromiumWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int
        self.title: str
        self.url: str
        self.loading: bool

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def loading(self) -> bool:
        return self.xa_elem.loading()

    def undo(self) -> 'XAChromiumTab':
        self.xa_elem.undo()
        return self

    def redo(self) -> 'XAChromiumTab':
        self.xa_elem.redo()
        return self

    def cut_selection(self) -> 'XAChromiumTab':
        self.xa_elem.cutSelection()
        return self

    def copy_selection(self) -> 'XAChromiumTab':
        self.xa_elem.copySelection()
        return self

    def paste_selection(self) -> 'XAChromiumTab':
        self.xa_elem.pasteSelection()
        return self

    def select_all(self) -> 'XAChromiumTab':
        self.xa_elem.selectAll()
        return self

    def go_back(self) -> 'XAChromiumTab':
        self.xa_elem.goBack()
        return self

    def go_forward(self) -> 'XAChromiumTab':
        self.xa_elem.goForward()
        return self

    def reload(self) -> 'XAChromiumTab':
        self.xa_elem.reload()
        return self

    def stop(self) -> 'XAChromiumTab':
        self.xa_elem.stop()
        return self

    def print(self) -> 'XAChromiumTab':
        self.xa_elem.print()
        return self

    def view_source(self) -> 'XAChromiumTab':
        self.xa_elem.viewSource()
        return self

    def save(self, file_path: Union[str, NSURL], save_assets: bool = True) -> 'XAChromiumTab':
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        if save_assets:
            self.xa_elem.saveIn_as_(file_path, "complete html")
        else:
            self.xa_elem.saveIn_as_(file_path, "only html")
        return self

    def close(self) -> 'XAChromiumTab':
        self.xa_elem.close()
        return self

    def execute(self, script: str) -> Any:
        return self.xa_elem.executeJavascript_(script)

    def move_to(self, window: 'XAChromiumWindow') -> 'XAChromiumWindow':
        """Moves the tab to the specified window. After, the tab will exist in only one location.

        :param window: The window to move the tab to.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariGeneric

        :Example 1: Move the current tab to the second window

        >>> import PyXA
        >>> app = PyXA.application("Chromium")
        >>> tab = app.front_window().active_tab
        >>> window2 = app.window(1)
        >>> tab.move_to(window2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.1
        """
        current = self.xa_elem.get()
        properties = {"URL": self.url}
        if isinstance(self.xa_prnt, XABase.XAList):
            new_tab = self.xa_prnt.xa_prnt.xa_prnt.make("tab", properties)
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", properties)
        window.tabs().push(new_tab)
        current.close()
        return self

    def duplicate_to(self, window: 'XAChromiumWindow') -> 'XAChromiumWindow':
        """Duplicates the tab in the specified window. The tab will then exist in two locations.

        :param window: The window to duplicate the tab in.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariTab

        :Example 1: Duplicate the current tab in the second window

        >>> import PyXA
        >>> app = PyXA.application("Chromium")
        >>> tab = app.front_window().active_tab
        >>> window2 = app.window(1)
        >>> tab.duplicate_to(window2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.1
        """
        properties = {"URL": self.url}

        new_tab = None
        print(self.xa_prnt)
        if isinstance(self.xa_prnt, XABase.XAList):
            new_tab = self.xa_prnt.xa_prnt.xa_prnt.make("tab", properties)
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", properties)
        window.tabs().push(new_tab)
        return self


class XAChromiumBookmarkFolderList(XABase.XAList):
    """A wrapper around a list of bookmark folders.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkFolder, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> 'XAChromiumBookmarkFolder':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAChromiumBookmarkFolder':
        return self.by_property("title", title)

    def by_index(self, index: int) -> 'XAChromiumBookmarkFolder':
        return self.by_property("index", index)

class XAChromiumBookmarkFolder(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmark folders in Chromium.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier for the bookmark folder
        self.title: str #: The name of the bookmark folder
        self.index: int #: The index of the bookmark folder with respect to its parent folder

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAChromiumBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkFolders(), XAChromiumBookmarkFolderList, filter)

    def bookmark_items(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkItemList':
        """Returns a list of bookmark items, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter items by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark items
        :rtype: XAChromiumBookmarkItemList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkItems(), XAChromiumBookmarkItemList, filter)

    def delete(self):
        """Permanently deletes the bookmark folder.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()


class XAChromiumBookmarkItemList(XABase.XAList):
    """A wrapper around a list of bookmark items.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkItem, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> 'XAChromiumBookmarkItem':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAChromiumBookmarkItem':
        return self.by_property("title", title)

    def by_url(self, url: str) -> 'XAChromiumBookmarkItem':
        return self.by_property("URL", url)

    def by_index(self, index: int) -> 'XAChromiumBookmarkItem':
        return self.by_property("index", index)

class XAChromiumBookmarkItem(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmarks in Chromium.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier for the bookmark item
        self.title: str #: The title of the bookmark item
        self.url: str #: The URL of the bookmark
        self.index: int #: The index of the item with respect to its parent folder

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    def delete(self):
        """Permanently deletes the bookmark.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()