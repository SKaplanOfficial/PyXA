""".. versionadded:: 0.0.3

Control Brave using JXA-like syntax.
"""

from typing import List, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray
from numpy import isin

from PyXA import XABase
from PyXA import XABaseScriptable

class XABraveApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Brave.app.

    .. seealso:: :class:`XABraveWindow`, :class:`XABraveDocument`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XABraveWindow

        self.frontmost: bool = self.xa_scel.frontmost() #: Whether Brave is the active application
        self.name: str = self.xa_scel.name() #: The name of the Brave application
        self.version: str = self.xa_scel.version() #: The currently installed version of Brave
        self.__bookmarks_bar = None #: The bookmarks bar bookmark folder
        self.__other_bookmarks = None #: The other bookmarks bookmark folder

    @property
    def bookmarks_bar(self) -> 'XABraveBookmarkFolder':
        if self.__bookmarks_bar is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_scel.bookmarksBar(),
                "scriptable_element": self.xa_scel.bookmarksBar(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__bookmarks_bar = XABraveBookmarkFolder(properties)
        return self.__bookmarks_bar

    @property
    def other_bookmarks(self) -> 'XABraveBookmarkFolder':
        if self.__other_bookmarks is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_scel.otherBookmarks(),
                "scriptable_element": self.xa_scel.otherBookmarks(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__other_bookmarks = XABraveBookmarkFolder(properties)
        return self.__other_bookmarks

    def open(self, url: Union[str, NSURL] = "https://google.com") -> 'XABraveApplication':
        """Opens a URL in a new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Safari application object.
        :rtype: XABraveApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Brave")
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

class XABraveWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Keynote.app.

    .. seealso:: :class:`XABraveApplication`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.given_name: str = self.xa_scel.givenName() #: The given name of the window
        self.mode: str = self.xa_scel.mode() #: The window privacy mode, i.e. "normal" or "incognito"
        self.active_tab_index: int = self.xa_scel.activeTabIndex() #: The index of the active tab
        self.minimizable: bool = self.xa_scel.minimizable() #: Whether the window has a minimize button
        self.minimized: bool = self.xa_scel.minimized() #: Whether the window is currently minimized
        self.__active_tab = None #: The currently selected tab
        
    @property
    def active_tab(self) -> 'XABraveTab':
        if self.__active_tab is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_scel.activeTab(),
                "scriptable_element": self.xa_scel.activeTab(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__active_tab = XABraveTab(properties)
        return self.__active_tab

class XABraveTab(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAFirefoxWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int = self.xa_scel.id() #: The unique identifier for the tab
        self.title: str = self.xa_scel.title() #: The title of the tab; generally the title of the page contained by the tab
        self.url: str = self.xa_scel.URL() #: The URL of the page contained by the tab
        self.loading: bool = self.xa_scel.loading() #: Whether the tab is currently loading

    def select_all(self) -> 'XABraveTab':
        """Selects all selectable content in the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.selectAll()
        return self

    def copy_selection(self) -> 'XABraveTab':
        """Copies the selected text of the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.copySelection()
        return self

    def cut_selection(self) -> 'XABraveTab':
        """Cuts the selected text of the tab, if possible.

        If cutting is not possible, the text will only be copied.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.cutSelection()
        return self

    def paste_selection(self) -> 'XABraveTab':
        """Pastes text from the clipboard.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.pasteSelection()
        return self

    def reload(self) -> 'XABraveTab':
        """Reloads the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.reload()
        return self

    def stop(self) -> 'XABraveTab':
        """Stops loading of the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.stop()
        return self

    def close(self):
        """Closes the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.close()

    def save(self, file_path: Union[str, NSURL], save_assets: bool = True) -> 'XABraveTab':
        """Saves the tab's content to a local HTML archive.

        :param file_path: The path to save the HTML document at
        :type file_path: Union[str, NSURL]
        :param save_assets: Whether to save assets such as CSS, JavaScript, fonts, and image files, defaults to True
        :type save_assets: bool, optional
        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        if save_assets:
            self.xa_scel.saveIn_as_(file_path, None)
        else:
            self.xa_scel.saveIn_as_(file_path, "only html")
        return self

    def go_back(self) -> 'XABraveTab':
        """Goes back to the previous page. Mimics clicking the back button in the browser window.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.goBack()
        return self

    def go_forward(self) -> 'XABraveTab':
        """Goes forward to the next page. Mimics clicking the forward button in the browser window.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.goForward()
        return self

    def undo(self) -> 'XABraveTab':
        """Undoes the last change.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.undo()
        return self

    def redo(self) -> 'XABraveTab':
        """Redoes the last undone change.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.redo()
        return self

    def view_source(self) -> 'XABraveTab':
        """Opens the source of the page currently open in the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.viewSource()
        return self

    def execute(self, script: str) -> 'XABraveTab':
        """Executes JavaScript in the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        return self.xa_scel.executeJavascript_(script)

    def print(self) -> 'XABraveTab':
        """Opens the print dialog for the tab.

        :return: A reference to the tab object
        :rtype: XABraveTab

        .. versionadded:: 0.0.3
        """
        self.xa_scel.print()
        return self

class XABraveBookmarkFolder(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAFirefoxWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int = self.xa_scel.id() #: The unique identifier for the folder
        self.title: str = self.xa_scel.title() #: The title of the folder
        self.index: int = self.xa_scel.index() #: The index of the folder with respect to its parent bookmark folder

class XABraveBookmarkItem(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAFirefoxWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int = self.xa_scel.id() #: The unique identifier for the bookmark
        self.title: str = self.xa_scel.title() #: The title of the bookmark; the title of the page referred to by the bookmark by default
        self.url: str = self.xa_scel.URL() #: The URL referred to by the bookmark
        self.index: int = self.xa_scel.index() #: The index of the bookmark with respect to its parent bookmark folder