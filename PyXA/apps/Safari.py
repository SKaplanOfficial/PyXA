""".. versionadded:: 0.0.1

Control Safari using JXA-like syntax.
"""

from enum import Enum
from typing import Any, List, Tuple, Union
import threading

from PyXA import XABase
from PyXA import XABaseScriptable

class XASafariApplication(XABaseScriptable.XASBApplication, XABaseScriptable.XASBPrintable, XABaseScriptable.XAHasScriptableElements):
    """A class for interacting with Safari.app.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`, :class:`XABaseScriptable.XASBApplication`, :class:`XABaseScriptable.XASBSaveable`, :class:`XABaseScriptable.XASBPrintable`

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = XABase.OSType('yes ') #: Save the file
        NO  = XABase.OSType('no  ') #: Do not save the file
        ASK = XABase.OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XASafariWindow

        self.frontmost: bool #: Whether Safari is the active application
        self.name: str #: The name of the application
        self.version: str #: The version of Safari.app
        self.current_document: XASafariDocument #: The currently displayed document in the active tab

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def current_document(self) -> 'XASafariDocument':
        return self._new_element(self.xa_scel.documents()[0], XASafariDocument)

    def open(self, url: str = "https://google.com") -> 'XASafariApplication':
        """Opens a URL in new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        :Example 1: Open local and external URLs

        >>> import PyXA
        >>> app = PyXA.application("Safari")
        >>> app.open("https://www.google.com")
        >>> app.open("google.com")
        >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.1
        """
        if url.startswith("/"):
            # URL is a path to file
            self.xa_wksp.openFile_(url)
            return self
        # Otherwise, URL is web address
        elif not url.startswith("http"):
            url = "http://" + url
        url = XABase.xa_url(url)
        self.xa_wksp.openURL_(url)
        return self

    def show_bookmarks(self) -> 'XASafariApplication':
        """Opens Safari's bookmarks page.

        :return: A reference to the Safari application object.
        :rtype: XASafariApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.showBookmarks();
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
        >>> doc = app.current_document
        >>> tab = window.current_tab
        >>> app.add_to_reading_list(doc)
        >>> app.add_to_reading_list(tab)

        .. versionadded:: 0.0.1
        """
        if not isinstance(item, str):
            item = item.xa_elem.URL()
        self.xa_scel.addReadingListItem_andPreviewText_withTitle_(item, None, None)
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
        self.xa_scel.searchTheWebIn_for_(self.xa_scel.windows()[0], term)
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
        >>> tab = app.front_window().current_tab
        >>> app.search_in_tab(tab, "What is PyXA?")

        .. seealso:: :func:`search`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.searchTheWebIn_for_(tab.xa_elem, term)
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
        >>> tab = app.front_window().current_tab
        >>> script = "(function example() { return 1 + 1 })()"
        >>> print(app.do_javascript(script, tab))
        2.0

        .. versionadded:: 0.0.1
        """
        if tab is None:
            tab = self.front_window().current_tab
        return self.xa_scel.doJavaScript_in_(script, tab.xa_elem)

    def email(self, item: Union['XASafariDocument', 'XASafariTab']):
        """Opens a new email draft with the content of a tab or document.

        :param item: The object to email
        :type item: Union[XASafariDocument, XASafariTab]

        .. versionadded:: 0.0.4
        """
        self.xa_scel.emailContentsOf_(item.xa_elem)

    def save(self):
        self.xa_elem.saveIn_as_(None, None)

    def documents(self, filter: dict = None) -> 'XASafariDocumentList':
        """Returns a list of documents matching the given filter.

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XASafariDocumentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.documents(), XASafariDocumentList, filter)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new tab in Safari's front window

        >>> import PyXA
        >>> app = PyXA.application("Safari")
        >>> new_tab = app.make("tab", {"URL": "http://google.com"})
        >>> app.front_window().tabs().push(new_tab)

        :Example 2: Open a page in a new window by making a new document

        >>> import PyXA
        >>> app = PyXA.application("Safari")
        >>> new_doc = app.make("document", {"URL": "http://google.com"})
        >>> app.documents().push(new_doc)

        .. versionadded:: 0.0.4
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XASafariDocument)
        elif specifier == "tab":
            return self._new_element(obj, XASafariTab)




class XASafariWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBCloseable, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for interacting with Safari windows.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XASafariDocument #: The document currently displayed in the window
        self.current_tab: XASafariTab #: The currently selected tab

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
    def miniaturizable(self) -> bool:
        return self.xa_scel.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_scel.miniaturized()

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
    def document(self) -> 'XASafariDocument':
        return self._new_element(self.xa_elem.document(), XASafariDocument)

    @property
    def current_tab(self) -> 'XASafariTab':
        return self._new_element(self.xa_elem.currentTab(), XASafariTab)

    def tabs(self, filter: dict = None) -> 'XASafariTabList':
        """Returns a list of tabs matching the given filter.

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XASafariTabList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.tabs(), XASafariTabList, filter)




class XASafariGeneric(XABaseScriptable.XASBCloseable, XABase.XAHasElements):
    """A generic class containing methods relevant to Safari tabs and documents.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`, :class:`XABaseScriptable.XASBCloseable`

    .. versionadded:: 0.0.1
    """
    def search(self, term: str) -> 'XASafariGeneric':
        """Searches for the specified term in the current tab or document.

        :param term: The term to search.
        :type term: str
        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.xa_elem.searchTheWebIn_for_(self.xa_elem, term)
        return self

    def add_to_reading_list(self) -> 'XASafariGeneric':
        """Adds the URL of a tab or document to the reading list.

        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.xa_elem.addReadingListItem_andPreviewText_withTitle_(self.xa_elem.URL(), None, None)
        return self

    def do_javascript(self, script: str) -> Any:
        """Runs JavaScript in a tab or document.

        :return: The value returned from the script after it completes execution.
        :rtype: Any

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.doJavaScript_in_(script, self.xa_elem)

    def email(self):
        """Opens a new email draft with the content of a tab or document.

        :param item: The object to email
        :type item: Union[XASafariDocument, XASafariTab]

        .. versionadded:: 0.0.4
        """
        self.xa_elem.emailContentsOf_(self.xa_elem)

    def reload(self):
        """Reloads the tab or document.

        .. versionadded:: 0.0.4
        """
        self.set_property("URL", self.url)




class XASafariDocumentList(XABase.XAList):
    """A wrapper around lists of Safari documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASafariDocument, filter)

    def name(self) -> List[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of modified status booleans
        :rtype: List[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[str]:
        """Gets the file path of each document in the list.

        :return: A list of file paths
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def source(self) -> List[str]:
        """Gets the source HTML of each document in the list.

        :return: A list of document source HTML
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("source"))

    def url(self) -> List[str]:
        """Gets the file URL of each document in the list.

        :return: A list of document URLs
        :rtype: List[str]
        
        .. versionadded:: 0.0.
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def text(self) -> List[str]:
        """Gets the visible text of each document in the list.

        :return: A list of document text
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("text"))

    def by_name(self, name: str) -> 'XASafariDocument':
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XASafariDocument':
        """Retrieves the tab whose modified status matches the given boolean value, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XASafariDocument':
        """Retrieves the tab whose file matches the given file path, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("file", file)

    def by_source(self, source: str) -> 'XASafariDocument':
        """Retrieves the tab whose source HTML matches the given HTML, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("source", source)

    def by_url(self, url: str) -> 'XASafariDocument':
        """Retrieves the tab whose URL matches the given URL, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("URL", url)
    
    def by_text(self, text: str) -> 'XASafariDocument':
        """Retrieves the tab whose visible text matches the given text, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("text", text)

    def reload(self) -> 'XASafariDocumentList':
        """Reloads all documents in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList
        
        .. versionadded:: 0.0.4
        """
        for document in self.xa_elem:
            document.setValue_forKey_(document.URL(), "URL")
        return self

    def add_to_reading_list(self) -> 'XASafariDocumentList':
        """Adds the URL of all documents in the list to the reading list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList
        
        .. versionadded:: 0.0.5
        """
        for document in self:
            document.add_to_reading_list()
        return self

    def email(self) -> 'XASafariDocumentList':
        """Opens a new email draft with embedded links to the URL of each document in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList
        
        .. versionadded:: 0.0.5
        """
        for document in self:
            document.email()
        return self

    def do_javascript(self, script: str) -> 'XASafariDocumentList':
        """Runs a given JavaScript script in each document in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList
        
        .. versionadded:: 0.0.5
        """
        for document in self:
            document.do_javascript(script)
        return self

    def search(self, term: str) -> 'XASafariDocumentList':
        """Searches for the given term in each document in the list, using the default search engine.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList
        
        .. versionadded:: 0.0.5
        """
        for document in self:
            document.search(term)
        return self

    def close(self):
        """Closes each tab in the list.

        .. versionadded:: 0.0.5
        """
        length = len(self)
        for _index in range(length):
            self[0].close()

class XASafariDocument(XASafariGeneric, XABaseScriptable.XASBPrintable):
    """A class for interacting with Safari documents.

    .. seealso:: :class:`XASafariGeneric`, :class:`XABaseScriptable.XASBPrintable`, :class:`XABaseScriptable.XASBSaveable`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.file: str #: The location of the document on the disk, if there is one
        self.source: str #: The HTML source of the web page currently loaded in the document
        self.url: str #: The current URL of the document
        self.text: str #: The text of the web page currently loaded in the document

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        return self.xa_elem.file()

    @property
    def source(self) -> str:
        return self.xa_elem.source()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    def print(self, properties: dict = None, show_dialog: bool = True):
        """Prints or opens the print dialog for the document.

        :param properties: The print properties to pre-set for the print, defaults to None
        :type properties: dict, optional
        :param show_dialog: Whether to display the print dialog, defaults to True
        :type show_dialog: bool, optional

        .. versionadded:: 0.0.5
        """
        if properties is None:
            properties = {}

        print_thread = threading.Thread(target=self.xa_elem.printWithProperties_printDialog_, args=(properties, show_dialog), name="Print Document")
        print_thread.start()


class XASafariTabList(XABase.XAList):
    """A wrapper around lists of tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASafariTab, filter)

    def source(self) -> List[str]:
        """Gets the source HTML of each tab in the list.

        :return: A list of source HTML
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("source"))

    def url(self) -> List[str]:
        """Gets the current URL of each tab in the list.

        :return: A list of web URLs
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def index(self) -> List[int]:
        """Gets the index of each tab in the list.

        :return: A list of indices
        :rtype: List[int]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def text(self) -> List[str]:
        """Gets the visible text of each tab in the list.

        :return: A list of visible text
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("text"))

    def visible(self) -> List[bool]:
        """Gets the visible status of each tab in the list.

        :return: A list of visible status booleans
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def name(self) -> List[str]:
        """Gets the name of each tab in the list.

        :return: A list of tab names
        :rtype: List[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_source(self, source: str) -> Union['XASafariTab', None]:
        """Retrieves the tab whose source HTML matches the given HTML, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("source", source)

    def by_url(self, url: str) -> Union['XASafariTab', None]:
        """Retrieves the tab whose URL matches the given URL, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("URL", url)

    def by_index(self, index: int) -> Union['XASafariTab', None]:
        """Retrieves the tab whose index matches the given index, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("index", index)

    def by_text(self, text: str) -> Union['XASafariTab', None]:
        """Retrieves the tab whose visible text matches the given text, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("text", text)

    def by_visible(self, visible: bool) -> Union['XASafariTab', None]:
        """Retrieves the tab whose visible status matches the given boolean, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("visible", visible)

    def by_name(self, name: str) -> Union['XASafariTab', None]:
        """Retrieves the tab whose name matches the given name, if one exists.

        :return: The desired tab, if it is found
        :rtype: Union[XASafariTab, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def reload(self) -> 'XASafariTabList':
        """Reloads all tabs in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList
        
        .. versionadded:: 0.0.4
        """
        for tab in self.xa_elem:
            tab.setValue_forKey_(tab.URL(), "URL")
        return self

    def add_to_reading_list(self) -> 'XASafariTabList':
        """Adds the URL of all tabs in the list to the reading list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList
        
        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.add_to_reading_list()
        return self

    def email(self) -> 'XASafariTabList':
        """Opens a new email draft with embedded links to the URL of each tab in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList
        
        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.email()
        return self

    def do_javascript(self, script: str) -> 'XASafariTabList':
        """Runs a given JavaScript script in each tab in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList
        
        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.do_javascript(script)
        return self

    def search(self, term: str) -> 'XASafariTabList':
        """Searches for the given term in each tab in the list, using the default search engine.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList
        
        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.search(term)
        return self

    def move_to(self, window: XASafariWindow) -> 'XASafariTabList':
        """Moves all tabs in the list to the specified window.

        :param window: The window to move tabs to
        :type window: XASafariWindow
        :return: The tab list object
        :rtype: XASafariTabList

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.5
        """
        for tab in self.xa_elem:
            tab.moveTo_(window.xa_elem)
            tab.close()
        return self

    def duplicate_to(self, window: XASafariWindow) -> 'XASafariTabList':
        """Duplicate all tabs in the list in the specified window.

        :param window: The window to duplicate tabs in
        :type window: XASafariWindow
        :return: The tab list object
        :rtype: XASafariTabList

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.5
        """
        for tab in self.xa_elem:
            tab.moveTo_(window.xa_elem)
        return self

    def close(self):
        """Closes each tab in the list.

        .. versionadded:: 0.0.5
        """
        length = len(self)
        for _index in range(length):
            self[0].close()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XASafariTab(XASafariGeneric):
    """A class for interacting with Safari tabs.

    .. seealso:: :class:`XASafariGeneric`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.source: str #: The HTML source of the web page currently loaded in the tab
        self.url: str #: The current URL of the tab
        self.index: int #: The index of the tab, ordered left to right
        self.text: str #: The text of the web page currently loaded in the tab
        self.visible: bool #: Whether the tab is currently visible
        self.name: str #: The title of the tab

    @property
    def source(self) -> str:
        return self.xa_elem.source()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def move_to(self, window: 'XASafariWindow') -> 'XASafariTab':
        """Moves the tab to the specified window. After, the tab will exist in only one location.

        :param window: The window to move the tab to.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariGeneric

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Safari")
        >>> tab = app.front_window().current_tab
        >>> window2 = app.window(1)
        >>> tab.move_to(window2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.moveTo_(window.xa_elem)
        self.close()
        return self

    def duplicate_to(self, window: 'XASafariWindow') -> 'XASafariTab':
        """Duplicates the tab in the specified window. The tab will then exist in two locations.

        :param window: The window to duplicate the tab in.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Safari")
        >>> tab = app.front_window().current_tab
        >>> window2 = app.window(1)
        >>> tab.duplicate_to(window2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.moveTo_(window.xa_elem)
        return self