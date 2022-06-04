""".. versionadded:: 0.0.1

Control Safari using JXA-like syntax.
"""

from typing import Any, List, Union

import XABase
import XABaseScriptable

class XASafariApplication(XABaseScriptable.XASBApplication, XABaseScriptable.XASBSaveable, XABaseScriptable.XASBPrintable, XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with Safari.app.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`, :class:`XABaseScriptable.XASBApplication`, :class:`XABaseScriptable.XASBSaveable`, :class:`XABaseScriptable.XASBPrintable`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.properties["window_class"] = XASafariWindow

    def open(self, url: str = "https://google.com") -> 'XASafariApplication':
        """Opens a URL in new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> app.open("https://www.google.com")
           >>> app.open("google.com")
           >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.1
        """
        if url.startswith("/"):
            # URL is a path to file
            self.properties["workspace"].openFile_(url)
            return self
        # Otherwise, URL is web address
        elif not url.startswith("http"):
            url = "http://" + url
        url = XABase.xa_url(url)
        self.properties["workspace"].openURL_(url)
        return self

    def show_bookmarks(self) -> 'XASafariApplication':
        """Opens Safari's bookmarks page.

        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        .. versionadded:: 0.0.1
        """
        self.properties["sb_element"].showBookmarks();
        return self

    def add_to_reading_list(self, item: Union[str, 'XASafariTab', 'XASafariDocument']) -> 'XASafariApplication':
        """Adds a URL to the reading list.

        :param item: A URL string or a Safari tab or document containing the URL to add to the reading list.
        :type item: Union[str, XASafariTab, XASafariDocument]
        :return: A reference to the Safari application object.
        :rtype: XASafariTab

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> window = app.front_window()
           >>> doc = app.current_document()
           >>> tab = window.current_tab()
           >>> app.add_to_reading_list(doc)
           >>> app.add_to_reading_list(tab)

        .. versionadded:: 0.0.1
        """
        if not isinstance(item, str):
            item = item.properties["element"].URL()
        self.properties["sb_element"].addReadingListItem_andPreviewText_withTitle_(item, None, None)
        return self

    def search(self, term: str) -> 'XASafariApplication':
        """Searches the specified string in a new tab of the frontmost Safari window. Uses the default search engine.

        :param term: The string to search.
        :type term: str
        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> app.search("What is PyXA?")

        .. seealso:: :func:`search_in_tab`

        .. versionadded:: 0.0.1
        """
        self.properties["sb_element"].searchTheWebIn_for_(self.properties["sb_element"].windows()[0], term)
        return self

    def search_in_tab(self, tab: 'XASafariTab', term: str) -> 'XASafariApplication':
        """Searches the given search string in the specified tab. Uses the default search engine.

        :param tab: The tab to conduct the web search in.
        :type tab: XASafariTab
        :param term: The string to search.
        :type term: str
        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> tab = app.front_window().current_tab()
           >>> app.search_in_tab(tab, "What is PyXA?")

        .. seealso:: :func:`search`

        .. versionadded:: 0.0.1
        """
        self.properties["sb_element"].searchTheWebIn_for_(tab.properties["element"], term)
        return self

    def do_javascript(self, script: str, tab: 'XASafariTab' = None) -> Any:
        """Runs JavaScript in the specified tab. If no tab is specified, the script is run in the current tab of the frontmost Safari window.

        :param script: The script to run.
        :type script: str
        :param tab: The tab to execute the JavaScript script in, defaults to None
        :type tab: XASafariTab
        :return: The value returned from the script after it completes execution.
        :rtype: Any

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> tab = app.front_window().current_tab()
           >>> script = "(function example() { return 1 + 1 })()"
           >>> print(app.do_javascript(script, tab))
           2.0

        .. versionadded:: 0.0.1
        """
        if tab is None:
            tab = self.front_window().current_tab()
        return self.properties["sb_element"].doJavaScript_in_(script, tab.properties["element"])

    def documents(self, filter: dict = None) -> List['XASafariDocument']:
        """Returns a list of documents matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_elements("documents", filter, XASafariDocument)

    def document(self, filter: Union[int, dict]) -> 'XASafariDocument':
        """Returns the first document that matches the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().scriptable_element("documents", filter, XASafariDocument)

    def first_document(self) -> 'XASafariDocument':
        """Returns the document at the first index of the documents array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_scriptable_element("documents", XASafariDocument)

    def last_document(self) -> 'XASafariDocument':
        """Returns the document at the last (-1) index of the documents array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_scriptable_element("documents", XASafariDocument)

    def current_document(self) -> 'XASafariDocument':
        """Returns the document open in the frontmost Safari window's current tab.

        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.properties["appspace"],
            "workspace": self.properties["workspace"],
            "element": self.properties["sb_element"].documents()[0],
            "appref": self.properties["appref"],
            "system_events": self.properties["system_events"],
        }
        return XASafariDocument(properties)


class XASafariWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBSaveable, XABaseScriptable.XASBCloseable, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for interacting with Safari windows.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def tabs(self, filter: dict = None) -> List['XASafariTab']:
        """Returns a list of tabs matching the given filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return super().elements("tabs", filter, XASafariTab)

    def tab(self, filter: Union[int, dict]) -> 'XASafariTab':
        """Returns the first tab that matches the given filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return super().element("tabs", filter, XASafariTab)

    def first_tab(self) -> 'XASafariTab':
        """Returns the tab at the first index of the window's tabs array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().first_element("tabs", XASafariTab)

    def last_tab(self) -> 'XASafariTab':
        """Returns the tab at the last (-1) index of the window's tabs array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return super().last_element("tabs", XASafariTab)

    def current_tab(self) -> 'XASafariTab':
        """Returns the window's currently focused tab.

        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.properties["appspace"],
            "workspace": self.properties["workspace"],
            "element": self.properties["element"].currentTab(),
            "appref": self.properties["appref"],
            "system_events": self.properties["system_events"],
        }
        return XASafariTab(properties)


class XASafariGeneric(XABaseScriptable.XASBCloseable, XABase.XAHasElements):
    """A generic class containing methods relevant to Safari tabs and documents.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`, :class:`XABaseScriptable.XASBCloseable`

    .. versionadded:: 0.0.1
    """
    def search(self, term: str) -> 'XASafariGeneric':
        """Searches for the specified term in a tab or document.

        :param term: The term to search.
        :type term: str
        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.properties["element"].searchTheWebIn_for_(self.properties["element"], term)
        return self

    def email(self) -> 'XASafariGeneric':
        """Opens a new email draft with the content of a tab or document.

        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.properties["element"].emailContentsOf_(self.properties["element"])
        return self

    def add_to_reading_list(self) -> 'XASafariGeneric':
        """Adds the URL of a tab or document to the reading list.

        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.properties["element"].addReadingListItem_andPreviewText_withTitle_(self.properties["element"].URL(), None, None)
        return self

    def do_javascript(self, script: str) -> Any:
        """Runs JavaScript in a tab or document.

        :return: The value returned from the script after it completes execution.
        :rtype: Any

        .. versionadded:: 0.0.1
        """
        return self.properties["element"].doJavaScript_in_(script, self.properties["element"])


class XASafariDocument(XASafariGeneric, XABaseScriptable.XASBPrintable, XABaseScriptable.XASBSaveable):
    """A class for interacting with Safari documents.

    .. seealso:: :class:`XASafariGeneric`, :class:`XABaseScriptable.XASBPrintable`, :class:`XABaseScriptable.XASBSaveable`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XASafariTab(XASafariGeneric):
    """A class for interacting with Safari tabs.

    .. seealso:: :class:`XASafariGeneric`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def move_to(self, window: 'XASafariWindow') -> 'XASafariTab':
        """Moves the tab to the specified window. After, the tab will exist in only one location.

        :param window: The window to move the tab to.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariGeneric

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> tab = app.front_window().current_tab()
           >>> window2 = app.window(1)
           >>> tab.move_to(window2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.1
        """
        self.properties["element"].moveTo_(window.properties["element"])
        self.close()
        return self

    def duplicate_to(self, window: 'XASafariWindow') -> 'XASafariTab':
        """Duplicates the tab in the specified window. The tab will then exist in two locations.

        :param window: The window to duplicate the tab in.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariGeneric

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Safari")
           >>> tab = app.front_window().current_tab()
           >>> window2 = app.window(1)
           >>> tab.duplicate_to(window2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.1
        """
        self.properties["element"].moveTo_(window.properties["element"])
        return self