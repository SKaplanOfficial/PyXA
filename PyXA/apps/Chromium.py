""".. versionadded:: 0.0.3

Control Chromium using JXA-like syntax.
"""

from typing import Any, List, Tuple, Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

class XAChromiumApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Chromium.app.

    .. seealso:: :class:`XAChromiumWindow`, :class:`XAChromiumBookmarkFolder`, :class:`XAChromiumBookmarkItem`, :class:`XAChromiumTab`

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

    def open(self, url: Union[str, XABase.XAURL] = "https://google.com") -> 'XAChromiumApplication':
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
            url = XABase.XAURL(url)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
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

    def new_window(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumWindow':
        """Opens a new window at the specified URL.


        :param url: The URL to open in a new window, or None to open the window at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created window object
        :rtype: XAChromiumWindow

        .. seealso:: :func:`new_tab`, :func:`make`

        .. versionadded:: 0.0.5
        """
        new_window = self.make("window")
        self.windows().push(new_window)

        if isinstance(url, str):
            if url.startswith("/"):
                # URL is a path to file
                self.xa_wksp.openFile_application_(url, self.xa_scel)
                return self
            # Otherwise, URL is web address
            elif not url.startswith("http"):
                url = "http://" + url
            url = XABase.XAURL(url)
        new_window.active_tab.set_property("URL", url.xa_elem)
        return new_window

    def new_tab(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumTab':
        """Opens a new tab at the specified URL.

        :param url: The URL to open in a new tab, or None to open the tab at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created tab object
        :rtype: XAChromiumTab

        .. seealso:: :func:`new_window`, :func:`make`

        .. versionadded:: 0.0.5
        """
        new_tab = None
        if url is None:
            new_tab = self.make("tab")
        else:
            new_tab = self.make("tab", {"URL": url})
        self.front_window().tabs().push(new_tab)
        return new_tab

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. seealso:: :func:`new_window`, :func:`new_tab`

        .. versionadded:: 0.0.4
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "tab":
            return self._new_element(obj, XAChromiumTab)
        elif specifier == "window":
            return self._new_element(obj, XAChromiumWindow)




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
        return self.xa_elem.givenName()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def minimizable(self) -> bool:
        return self.xa_elem.minimizable()

    @property
    def minimized(self) -> bool:
        return self.xa_elem.minimized()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @property
    def mode(self) -> str:
        return self.xa_elem.mode()

    @property
    def active_tab_index(self) -> int:
        return self.xa_elem.activeTabIndex() 

    @property
    def active_tab(self) -> 'XAChromiumTab':
        return self._new_element(self.xa_elem.activeTab(), XAChromiumTab)

    def new_tab(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumTab':
        """Opens a new tab at the specified URL.

        :param url: The URL to open in a new tab, or None to open the tab at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created tab object
        :rtype: XAChromiumTab

        .. versionadded:: 0.0.5
        """
        new_tab = None
        if url is None:
            new_tab = self.xa_prnt.xa_prnt.make("tab")
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", {"URL": url})
        self.tabs().push(new_tab)
        return new_tab

    def tabs(self, filter: Union[dict, None] = None) -> 'XAChromiumTabList':
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter tabs by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of tabs
        :rtype: XAChromiumTabList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.tabs(), XAChromiumTabList, filter)




class XAChromiumTabList(XABase.XAList):
    """A wrapper around a list of tabs.

    .. seealso:: :class:`XAChromiumTab`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumTab, filter)

    def id(self) -> List[int]:
        """Gets the ID of each tab in the list.

        :return: A list of tab IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        """Gets the title of each tab in the list.

        :return: A list of tab titles
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        """Gets the URL of each tab in the list.

        :return: A list of tab URLS
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def loading(self) -> List[bool]:
        """Gets the loading state of each tab in the list.

        :return: A list of loading states; a list of booleans.
        :rtype: List[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("loading"))

    def by_id(self, id: int) -> Union['XAChromiumTab', None]:
        """Retrieves the tab whose ID matches the given ID, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XAChromiumTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumTab', None]:
        """Retrieves the first tab whose title matches the given title, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XAChromiumTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("title", title)

    def by_url(self, url: str) -> Union['XAChromiumTab', None]:
        """Retrieves the first tab whose URL matches the given URL, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XAChromiumTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("url", url)

    def by_loading(self, loading: bool) -> Union['XAChromiumTab', None]:
        """Retrieves the first tab whose loading state matches the given boolean value, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XAChromiumTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("loading", loading)

class XAChromiumTab(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Chromium tabs.

    .. seealso:: :class:`XAChromiumWindow`, :class:`XAChromiumTabList`, :class:`XAChromiumWindow`

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
        """Undoes the last action done on the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.undo()
        return self

    def redo(self) -> 'XAChromiumTab':
        """Redoes the last action done on the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.redo()
        return self

    def cut_selection(self) -> 'XAChromiumTab':
        """Attempts to cut the selected content and copy it to the clipboard. If the content cannot be deleted, then it is only copied to the clipboard.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.cutSelection()
        return self

    def copy_selection(self) -> 'XAChromiumTab':
        """Copies the selected element to the clipboard.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.copySelection()
        return self

    def paste_selection(self) -> 'XAChromiumTab':
        """Attempts to paste the clipboard into the selected element.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.pasteSelection()
        return self

    def select_all(self) -> 'XAChromiumTab':
        """Selects all text content within the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.selectAll()
        return self

    def go_back(self) -> 'XAChromiumTab':
        """Goes to the previous URL in the tab's history.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.goBack()
        return self

    def go_forward(self) -> 'XAChromiumTab':
        """Goes to the next URL in the tab's history, or does nothing if the current document is the most recent URL.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.goForward()
        return self

    def reload(self) -> 'XAChromiumTab':
        """Reloads the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.reload()
        return self

    def stop(self) -> 'XAChromiumTab':
        """Forces the tab to stop loading.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.stop()
        return self

    def print(self) -> 'XAChromiumTab':
        """Opens the print dialog for the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.print()
        return self

    def view_source(self) -> 'XAChromiumTab':
        """Opens the source HTML of the tab's document in a separate tab.
        
        .. versionadded:: 0.0.4
        """
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
        """Closes the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.close()
        return self

    def execute(self, script: str) -> Any:
        """Executes JavaScript in the tab.
        
        .. versionadded:: 0.0.4
        """
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

    .. seealso:: :class:`XAChromiumBookmarkFolder`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkFolder, filter)

    def id(self) -> List[int]:
        """Gets the ID of each bookmark folder in the list.

        :return: A list of bookmark folder IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        """Gets the title of each bookmark folder in the list.

        :return: A list of bookmark folder titles
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def index(self) -> List[int]:
        """Gets the index of each bookmark folder in the list.

        :return: A list of indexes
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> Union['XAChromiumBookmarkFolder', None]:
        """Retrieves the bookmark folder whose ID matches the given ID, if one exists.

        :return: The desired bookmark folder, if it is found
        :rtype: Union[XAChromiumBookmarkFolder, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumBookmarkFolder', None]:
        """Retrieves the first bookmark folder whose title matches the given title, if one exists.

        :return: The desired bookmark folder, if it is found
        :rtype: Union[XAChromiumBookmarkFolder, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("title", title)

    def by_index(self, index: int) -> Union['XAChromiumBookmarkFolder', None]:
        """Retrieves the bookmark folder whose index matches the given index, if one exists.

        :return: The desired bookmark folder, if it is found
        :rtype: Union[XAChromiumBookmarkFolder, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("index", index)

class XAChromiumBookmarkFolder(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmark folders in Chromium.app.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumBookmarkFolderList`

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

    .. seealso:: :class:`XAChromiumBookmarkItem`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkItem, filter)

    def id(self) -> List[int]:
        """Gets the ID of each item in the list.

        :return: A list of bookmark item IDs
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        """Gets the title of each item in the list.

        :return: A list of bookmark item titles
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        """Gets the url of each item in the list.

        :return: A list of bookmark item URLs
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def index(self) -> List[int]:
        """Gets the index of each item in the list.

        :return: A list of indexes
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> Union['XAChromiumBookmarkItem', None]:
        """Retrieves the bookmark item whose ID matches the given ID, if one exists.

        :return: The desired bookmark item, if it is found
        :rtype: Union[XAChromiumBookmarkItem, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumBookmarkItem', None]:
        """Retrieves the first bookmark item whose title matches the given title, if one exists.

        :return: The desired bookmark item, if it is found
        :rtype: Union[XAChromiumBookmarkItem, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("title", title)

    def by_url(self, url: str) -> Union['XAChromiumBookmarkItem', None]:
        """Retrieves the first bookmark item whose URL matches the given URL, if one exists.

        :return: The desired bookmark item, if it is found
        :rtype: Union[XAChromiumBookmarkItem, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("URL", url)

    def by_index(self, index: int) -> Union['XAChromiumBookmarkItem', None]:
        """Retrieves the bookmark item whose index matches the given index, if one exists.

        :return: The desired bookmark item, if it is found
        :rtype: Union[XAChromiumBookmarkItem, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("index", index)

class XAChromiumBookmarkItem(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmarks in Chromium.app.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumBookmarkItemList`

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