""".. versionadded:: 0.0.3

Control Google Chrome using JXA-like syntax.
"""

from typing import Any, List, Tuple, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

class XAGoogleChromeApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with GoogleChrome.app.

    .. seealso:: :class:`XAGoogleChromeWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAGoogleChromeWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether GoogleChrome is the active application
        self.version: str #: The version of GoogleChrome
        self.bookmarks_bar: XAGoogleChromeBookmarkFolder #: The bookmarks bar bookmark folder
        self.other_bookmarks: XAGoogleChromeBookmarkFolder #: The other bookmarks bookmark folder

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
    def bookmarks_bar(self) -> 'XAGoogleChromeBookmarkFolder':
        return self._new_element(self.xa_scel.bookmarksBar(), XAGoogleChromeBookmarkFolder)

    @property
    def other_bookmarks(self) -> 'XAGoogleChromeBookmarkFolder':
        return self._new_element(self.xa_scel.otherBookmarks(), XAGoogleChromeBookmarkFolder)

    def open(self, url: Union[str, NSURL] = "https://google.com") -> 'XAGoogleChromeApplication':
        """Opens a URL in a new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the GoogleChrome application object.
        :rtype: XAGoogleChromeApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("GoogleChrome")
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

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAGoogleChromeBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAGoogleChromeBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.bookmarkFolders(), XAGoogleChromeBookmarkFolderList, filter)

class XAGoogleChromeWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with GoogleChrome windows.

    .. seealso:: :class:`XAGoogleChromeApplication`, :class:`XAGoogleChromeTab`

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
        self.active_tab: XAGoogleChromeTab #: The currently selected tab

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
    def active_tab(self) -> 'XAGoogleChromeTab':
        return self._new_element(self.xa_scel.activeTab(), XAGoogleChromeTab)

    def tabs(self, filter: Union[dict, None] = None) -> 'XAGoogleChromeTabList':
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter tabs by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of tabs
        :rtype: XAGoogleChromeTabList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.tabs(), XAGoogleChromeTabList, filter)


class XAGoogleChromeTabList(XABase.XAList):
    """A wrapper around a list of tabs.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAGoogleChromeTab, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def loading(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loading"))

    def by_id(self, id: int) -> 'XAGoogleChromeTab':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAGoogleChromeTab':
        return self.by_property("title", title)

    def by_url(self, url: str) -> 'XAGoogleChromeTab':
        return self.by_property("url", url)

    def by_loading(self, loading: bool) -> 'XAGoogleChromeTab':
        return self.by_property("loading", loading)

class XAGoogleChromeTab(XABaseScriptable.XASBObject):
    """A class for managing and interacting with GoogleChrome tabs.

    .. seealso:: :class:`XAGoogleChromeWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = None
        self.title = None
        self.url = None
        self.loading = None

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

    def undo(self) -> 'XAGoogleChromeTab':
        self.xa_elem.undo()
        return self

    def redo(self) -> 'XAGoogleChromeTab':
        self.xa_elem.redo()
        return self

    def cut_selection(self) -> 'XAGoogleChromeTab':
        self.xa_elem.cutSelection()
        return self

    def copy_selection(self) -> 'XAGoogleChromeTab':
        self.xa_elem.copySelection()
        return self

    def paste_selection(self) -> 'XAGoogleChromeTab':
        self.xa_elem.pasteSelection()
        return self

    def select_all(self) -> 'XAGoogleChromeTab':
        self.xa_elem.selectAll()
        return self

    def go_back(self) -> 'XAGoogleChromeTab':
        self.xa_elem.goBack()
        return self

    def go_forward(self) -> 'XAGoogleChromeTab':
        self.xa_elem.goForward()
        return self

    def reload(self) -> 'XAGoogleChromeTab':
        self.xa_elem.reload()
        return self

    def stop(self) -> 'XAGoogleChromeTab':
        self.xa_elem.stop()
        return self

    def print(self) -> 'XAGoogleChromeTab':
        self.xa_elem.print()
        return self

    def view_source(self) -> 'XAGoogleChromeTab':
        self.xa_elem.viewSource()
        return self

    def save(self, file_path: Union[str, NSURL], save_assets: bool = True) -> 'XAGoogleChromeTab':
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        if save_assets:
            self.xa_elem.saveIn_as_(file_path, "complete html")
        else:
            self.xa_elem.saveIn_as_(file_path, "only html")
        return self

    def close(self) -> 'XAGoogleChromeTab':
        self.xa_elem.close()
        return self

    def execute(self, script: str) -> Any:
        return self.xa_elem.executeJavascript_(script)


class XAGoogleChromeBookmarkFolderList(XABase.XAList):
    """A wrapper around a list of bookmark folders.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAGoogleChromeBookmarkFolder, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> 'XAGoogleChromeBookmarkFolder':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAGoogleChromeBookmarkFolder':
        return self.by_property("title", title)

    def by_index(self, index: int) -> 'XAGoogleChromeBookmarkFolder':
        return self.by_property("index", index)

class XAGoogleChromeBookmarkFolder(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmark folders in GoogleChrome.app.

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

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAGoogleChromeBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAGoogleChromeBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkFolders(), XAGoogleChromeBookmarkFolderList, filter)

    def bookmark_items(self, filter: Union[dict, None] = None) -> 'XAGoogleChromeBookmarkItemList':
        """Returns a list of bookmark items, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter items by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark items
        :rtype: XAGoogleChromeBookmarkItemList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkItems(), XAGoogleChromeBookmarkItemList, filter)


class XAGoogleChromeBookmarkItemList(XABase.XAList):
    """A wrapper around a list of bookmark items.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAGoogleChromeBookmarkItem, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> 'XAGoogleChromeBookmarkItem':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAGoogleChromeBookmarkItem':
        return self.by_property("title", title)

    def by_url(self, url: str) -> 'XAGoogleChromeBookmarkItem':
        return self.by_property("URL", url)

    def by_index(self, index: int) -> 'XAGoogleChromeBookmarkItem':
        return self.by_property("index", index)

class XAGoogleChromeBookmarkItem(XABaseScriptable.XASBObject):
    """A class for managing and interacting with bookmarks in GoogleChrome.app.

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