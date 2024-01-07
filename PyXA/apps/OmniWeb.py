""".. versionadded:: 0.3.0

Control OmniWeb using JXA-like syntax.
"""

from enum import Enum
from typing import Union, Any
from datetime import datetime
import threading

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import (
    XACanOpenPath,
    XACanPrintPath,
    XAClipboardCodable,
    XACloseable,
    XADeletable,
    XAPrintable,
)
from ..XAErrors import UnconstructableClassError
from ..XAEvents import event_from_str


class XAOmniWebApplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """A class for managing and interacting with OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    class ObjectType(Enum):
        """Types of objects that can be created using :func:`XAOmniWebApplication.make`."""
        Document = "document"
        Window = "window"
        Workspace = "workspace"
        Browser = "browser"
        Tab = "tab"
        Bookmark = "bookmark"
        BookmarksDocument = "bookmarks_document"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAOmniWebWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether OmniWeb is the frontmost application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of OmniWeb.app."""
        return self.xa_scel.version()

    @property
    def active_workspace(self) -> "XAOmniWebWorkspace":
        """The currently active workspace."""
        return self._new_element(self.xa_scel.activeWorkspace(), XAOmniWebWorkspace)

    @active_workspace.setter
    def active_workspace(self, active_workspace: "XAOmniWebWorkspace"):
        self.set_property("activeWorkspace", active_workspace.xa_elem)

    @property
    def favorites(self) -> "XAOmniWebBookmark":
        """The bookmark item whose contents are displayed in the Favorites bar."""
        return self._new_element(self.xa_scel.favorites(), XAOmniWebBookmark)

    @property
    def full_version(self) -> str:
        """The complete version string for this instance of OmniWeb."""
        return self.xa_scel.fullVersion()

    @property
    def personal_bookmarks(self) -> "XAOmniWebBookmarksDocument":
        """The default bookmarks document."""
        return self._new_element(
            self.xa_scel.personalBookmarks(), XAOmniWebBookmarksDocument
        )

    def documents(self, filter: dict = None) -> Union["XAOmniWebDocumentList", None]:
        """Returns a list of documents, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAOmniWebDocumentList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.documents())
        <<class 'PyXA.apps.Bike.XABikeDocumentList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(
            self.xa_scel.documents(), XAOmniWebDocumentList, filter
        )

    def workspaces(self, filter: dict = None) -> Union["XAOmniWebWorkspaceList", None]:
        """Returns a list of workspaces, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned workspaces will have, or None
        :type filter: Union[dict, None]
        :return: The list of workspaces
        :rtype: XAOmniWebWorkspaceList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.workspaces())
        <<class 'PyXA.apps.Bike.XABikeWorkspaceList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(
            self.xa_scel.workspaces(), XAOmniWebWorkspaceList, filter
        )

    def browsers(self, filter: dict = None) -> Union["XAOmniWebBrowserList", None]:
        """Returns a list of browsers, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browsers will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XAOmniWebBrowserList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.browsers())
        <<class 'PyXA.apps.Bike.XABikeBrowserList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_scel.browsers(), XAOmniWebBrowserList, filter)

    def bookmarks_documents(
        self, filter: dict = None
    ) -> Union["XAOmniWebBookmarksDocumentList", None]:
        """Returns a list of bookmarks documents, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned bookmarks documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of bookmarks documents
        :rtype: XAOmniWebBookmarksDocumentList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.bookmarks_documents())
        <<class 'PyXA.apps.Bike.XABikeBookmarksDocumentList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(
            self.xa_scel.bookmarksDocuments(), XAOmniWebBookmarksDocumentList, filter
        )
    
    def open(self, target: Union[XABase.XAURL, XABase.XAPath, str]) -> None:
        """Opens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to open.
        :type target: Union[XABase.XAURL, XABase.XAPath, str]

        :Example 1: Open files from file paths

        >>> import PyXA
        >>> app = PyXA.Application("VLC")
        >>> app.open("/Users/exampleUser/Downloads/Example.avi")
        >>> 
        >>> path = PyXA.XAPath("/Users/exampleUser/Documents/Example.m4v")
        >>> app.open(path)

        :Example 2: Open URLs

        >>> import PyXA
        >>> app = PyXA.Application("VLC")
        >>> app.open("https://upload.wikimedia.org/wikipedia/commons/transcoded/0/0f/Baby_pelican.ogg/Baby_pelican.ogg.mp3")
        >>> 
        >>> url = PyXA.XAURL("https://www.youtube.com/watch?v=e9B3E_DnnWw")
        >>> app.open(url)

        .. versionadded:: 0.0.8
        """
        if isinstance(target, str):
            if target.startswith("/"):
                target = XABase.XAPath(target)
            else:
                target = XABase.XAURL(target)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([target.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)

    # def print(self, item: Union[str, 'XAOmniWebDocument'], properties: dict = None, show_dialog: bool = True):
    #     """Prints or opens the print dialog for the document.

    #     :param properties: The print properties to pre-set for the print, defaults to None
    #     :type properties: dict, optional
    #     :param show_dialog: Whether to display the print dialog, defaults to True
    #     :type show_dialog: bool, optional

    #     .. versionadded:: 0.0.5
    #     """
    #     if properties is None:
    #         properties = {}

    #     if isinstance(item, XABase.XAObject):
    #         item = item.xa_elem

    #     print_thread = threading.Thread(target=self.xa_scel.print_printDialog_withProperties_, args=(item, show_dialog, properties), name="Print Document")
    #     print_thread.start()
    
    def list_windows(self) -> list[int]:
        """Returns a list of the numeric IDs of all open browser windows.

        :return: The list of IDs
        :rtype: list[int]

        .. versionadded:: 0.3.0
        """
        return list(self.xa_scel.ListWindows())
    
    def get_window_info(self) -> dict:
        """Returns a dictionary containing information about the frontmost window.

        :return: The window's information
        :rtype: dict

        .. versionadded:: 0.3.0
        """
        return list(self.xa_scel.GetWindowInfo())

    def make(self, specifier: Union[str, 'XAOmniWebApplication.ObjectType'], properties: Union[dict, None] = None, data: Any = None) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAOmniWebApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Add new rows to the current document

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> front_doc_rows = app.front_window.document.rows()
        >>>
        >>> row1 = app.make("row", {"name": "This is a new row!"})
        >>> row2 = app.make("row", {"name": "This is another new row!"})
        >>> row3 = app.make("row", {"name": "This is a third new row!"})
        >>>
        >>> front_doc_rows.push(row1) # Add to the end of the document
        >>> front_doc_rows.insert(row2, 0) # Insert at the beginning of the document
        >>> front_doc_rows.insert(row3, 5) # Insert at the middle of the document

        .. versionadded:: 0.3.0
        """
        if isinstance(specifier, XAOmniWebApplication.ObjectType):
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
            return self._new_element(obj, XAOmniWebWindow)
        elif specifier == "document":
            return self._new_element(obj, XAOmniWebDocument)
        elif specifier == "tab":
            return self._new_element(obj, XAOmniWebTab)
        elif specifier == "bookmark":
            return self._new_element(obj, XAOmniWebBookmark)
        elif specifier == "bookmarks_document":
            return self._new_element(obj, XAOmniWebBookmarksDocument)
        elif specifier == "browser":
            return self._new_element(obj, XAOmniWebBrowser)
        elif specifier == "workspace":
            return self._new_element(obj, XAOmniWebWorkspace)



class XAOmniWebWindow(XABaseScriptable.XASBWindow):
    """A window of OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XAOmniWebDocument":
        """The document whose contents are currently displayed in the window."""
        return self._new_element(self.xa_elem.document(), XAOmniWebDocument)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"



class XAOmniWebDocumentList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebDocument, filter)

    def name(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("name") or []
        return self._new_element(ls, XABase.XATextList)

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def by_name(self, name: Union[str, XABase.XAText]) -> Union["XAOmniWebDocument", None]:
        if isinstance(name, XABase.XAText):
            name = name.text
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XAOmniWebDocument", None]:
        return self.by_property("modified", modified)

    def by_path(
        self, path: Union[str, XABase.XAPath]
    ) -> Union["XAOmniWebDocument", None]:
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAOmniWebDocument(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A document of OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> XABase.XAText:
        """The name of the document."""
        return self._new_element(self.xa_elem.name(), XABase.XAText)
    
    @name.setter
    def name(self, name: Union[str, XABase.XAText]):
        if isinstance(name, XABase.XAText):
            name = name.text
        self.set_property("name", name)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since it was last saved."""
        return self.xa_elem.modified()

    @property
    def path(self) -> XABase.XAPath:
        """The location of the document on disk, if it has one."""
        return XABase.XAPath(self.xa_elem.path())

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAOmniWebWorkspaceList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb workspaces that employs fast enumeration techniques.

    All properties of workspaces can be called as methods on the wrapped list, returning a list containing each workspace's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebWorkspace, filter)

    def autosaves(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("autosaves") or [])

    def name(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("name") or []
        return self._new_element(ls, XABase.XATextList)

    def by_autosaves(self, autosaves: bool) -> Union["XAOmniWebWorkspace", None]:
        return self.by_property("autosaves", autosaves)

    def by_name(self, name: Union[str, XABase.XAText]) -> Union["XAOmniWebWorkspace", None]:
        if isinstance(name, XABase.XAText):
            name = name.text
        return self.by_property("name", name)

    def browsers(self) -> "XAOmniWebBrowserList":
        """Returns a list of all browsers contained by the workspaces in the list.

        :return: The list of browsers
        :rtype: XAOmniWebBrowserList

        .. versionadded:: 0.3.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("browsers")]
        return self._new_element(ls, XAOmniWebBrowserList)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAOmniWebWorkspace(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A workspace in OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def autosaves(self) -> bool:
        """Whether the workspace saves its browser windows automatically."""
        return self.xa_elem.autosaves()

    @autosaves.setter
    def autosaves(self, autosaves: bool):
        self.set_property("autosaves", autosaves)

    @property
    def name(self) -> XABase.XAText:
        """The name of the workspace."""
        return self._new_element(self.xa_elem.name(), XABase.XAText)

    @name.setter
    def name(self, name: Union[str, XABase.XAText]):
        if isinstance(name, XABase.XAText):
            name = name.text
        self.set_property("name", name)

    def browsers(self, filter: dict = None) -> Union["XAOmniWebBrowserList", None]:
        """Returns a list of browsers, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned browsers will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XAOmniWebBrowserList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.browsers())
        <<class 'PyXA.apps.Bike.XABikeBrowserList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.browsers(), XAOmniWebBrowserList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAOmniWebBrowserList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb browsers that employs fast enumeration techniques.

    All properties of browsers can be called as methods on the wrapped list, returning a list containing each browser's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebBrowser, filter)

    def active_tab(self) -> "XAOmniWebTabList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("activeTab") or [], XAOmniWebTabList
        )

    def address(self) -> XABase.XAURLList:
        ls = self.xa_elem.arrayByApplyingSelector_("address") or []
        return self._new_element(ls, XABase.XAURLList)

    def has_favorites(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hasFavorites") or [])

    def has_tabs(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hasTabs") or [])

    def has_toolbar(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hasToolbar") or [])

    def is_busy(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isBusy") or [])

    def shows_address(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("showsAddress") or [])

    def by_active_tab(
        self, active_tab: "XAOmniWebTab"
    ) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("activeTab", active_tab.xa_elem)

    def by_address(
        self, address: Union[str, XABase.XAURL]
    ) -> Union["XAOmniWebBrowser", None]:
        if isinstance(address, XABase.XAURL):
            address = address.url
        return self.by_property("address", address)

    def by_has_favorites(self, has_favorites: bool) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("hasFavorites", has_favorites)

    def by_has_tabs(self, has_tabs: bool) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("hasTabs", has_tabs)

    def by_has_toolbar(self, has_toolbar: bool) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("hasToolbar", has_toolbar)

    def by_is_busy(self, is_busy: bool) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("isBusy", is_busy)

    def by_shows_address(self, shows_address: bool) -> Union["XAOmniWebBrowser", None]:
        return self.by_property("showsAddress", shows_address)

    def tabs(self) -> "XAOmniWebTabList":
        """Returns a list of all tabs contained by the browsers in the list.

        :return: The list of tabs
        :rtype: XAOmniWebTabList

        .. versionadded:: 0.3.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("tabs")]
        return self._new_element(ls, XAOmniWebTabList)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.address()) + ">"

class XAOmniWebBrowser(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A browser in OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def active_tab(self) -> "XAOmniWebTab":
        """The tab currently being displayed in the browser."""
        return self._new_element(self.xa_elem.activeTab(), XAOmniWebTab)

    @active_tab.setter
    def active_tab(self, active_tab: "XAOmniWebTab"):
        self.set_property("activeTab", active_tab.xa_elem)

    @property
    def address(self) -> XABase.XAURL:
        """The URL currently being displayed in the browser."""
        return XABase.XAURL(self.xa_elem.address())

    @address.setter
    def address(self, address: Union[str, XABase.XAURL]):
        if isinstance(address, XABase.XAURL):
            address = address.url
        self.set_property("address", address)

    @property
    def has_favorites(self) -> bool:
        """Whether the browser window displays the favorites shelf."""
        return self.xa_elem.hasFavorites()

    @has_favorites.setter
    def has_favorites(self, has_favorites: bool):
        self.set_property("hasFavorites", has_favorites)

    @property
    def has_tabs(self) -> bool:
        """Whether the browser window displays the tabs drawer."""
        return self.xa_elem.hasTabs()

    @has_tabs.setter
    def has_tabs(self, has_tabs: bool):
        self.set_property("hasTabs", has_tabs)

    @property
    def has_toolbar(self) -> bool:
        """Whether the browser window displays the toolbar."""
        return self.xa_elem.hasToolbar()

    @has_toolbar.setter
    def has_toolbar(self, has_toolbar: bool):
        self.set_property("hasToolbar", has_toolbar)

    @property
    def is_busy(self) -> bool:
        """Whether the browser is currently loading a page."""
        return self.xa_elem.isBusy()

    @property
    def shows_address(self) -> bool:
        """Whether the browser window displays the address (URL) field."""
        return self.xa_elem.showsAddress()

    @shows_address.setter
    def shows_address(self, shows_address: bool):
        self.set_property("showsAddress", shows_address)

    def tabs(self, filter: dict = None) -> Union["XAOmniWebTabList", None]:
        """Returns a list of tabs, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tabs will have, or None
        :type filter: Union[dict, None]
        :return: The list of tabs
        :rtype: XAOmniWebTabList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.tabs())
        <<class 'PyXA.apps.Bike.XABikeTabList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.tabs(), XAOmniWebTabList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.address) + ">"



class XAOmniWebTabList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebTab, filter)

    def address(self) -> XABase.XAURLList:
        ls = self.xa_elem.arrayByApplyingSelector_("address") or []
        return self._new_element(ls, XABase.XAURLList)

    def is_busy(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isBusy") or [])

    def source(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("source") or []
        return self._new_element(ls, XABase.XATextList)

    def title(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("title") or []
        return self._new_element(ls, XABase.XATextList)

    def by_address(
        self, address: Union[str, XABase.XAURL]
    ) -> Union["XAOmniWebTab", None]:
        if isinstance(address, XABase.XAURL):
            address = address.url
        return self.by_property("address", address)

    def by_is_busy(self, is_busy: bool) -> Union["XAOmniWebTab", None]:
        return self.by_property("isBusy", is_busy)

    def by_source(self, source: Union[str, XABase.XAText]) -> Union["XAOmniWebTab", None]:
        if isinstance(source, XABase.XAText):
            source = source.text
        return self.by_property("source", source)

    def by_title(self, title: Union[str, XABase.XAText]) -> Union["XAOmniWebTab", None]:
        if isinstance(title, XABase.XAText):
            title = title.text
        return self.by_property("title", title)

    def delete(self) -> None:
        """Closes all tabs in the list.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.makeObjectsPerformSelector_("delete")

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"


class XAOmniWebTab(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A tab in OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def address(self) -> XABase.XAURL:
        """The URL currently being displayed in the tab."""
        return XABase.XAURL(self.xa_elem.address())

    @address.setter
    def address(self, address: Union[str, XABase.XAURL]):
        if isinstance(address, XABase.XAURL):
            address = address.url
        self.set_property("address", address)

    @property
    def is_busy(self) -> bool:
        """Whether the tab is currently loading a page."""
        return self.xa_elem.isBusy()

    @property
    def source(self) -> XABase.XAText:
        """The source code of the page currently being displayed in the tab."""
        return self._new_element(self.xa_elem.source(), XABase.XAText)

    @property
    def title(self) -> XABase.XAText:
        """The title of the page currently being displayed in the tab."""
        return self._new_element(self.xa_elem.title(), XABase.XAText)

    def delete(self) -> None:
        """Closes the tab.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"



class XAOmniWebBookmarksDocumentList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb bookmarks documents that employs fast enumeration techniques.

    All properties of bookmarks documents can be called as methods on the wrapped list, returning a list containing each bookmarks document's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebBookmarksDocument, filter)

    def address(self) -> XABase.XAURLList:
        ls = self.xa_elem.arrayByApplyingSelector_("address") or []
        return self._new_element(ls, XABase.XAURLList)

    def is_read_only(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isReadOnly") or [])

    def by_address(self, address: Union[str, XABase.XAURL]) -> Union["XAOmniWebBookmarksDocument", None]:
        if isinstance(address, XABase.XAURL):
            address = address.url
        return self.by_property("address", address)

    def by_is_read_only(self, is_read_only: bool) -> Union["XAOmniWebBookmarksDocument", None]:
        return self.by_property("isReadOnly", is_read_only)
    
    def bookmarks(self) -> 'XAOmniWebBookmarkList':
        """Returns a list of all bookmarks contained by the bookmarks documents in the list.

        :return: The list of bookmarks
        :rtype: XAOmniWebBookmarkList

        .. versionadded:: 0.3.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("bookmarks")]
        return self._new_element(ls, XAOmniWebBookmarkList)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.address()) + ">"
    
class XAOmniWebBookmarksDocument(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A bookmarks document in OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def address(self) -> XABase.XAURL:
        """The URL at which these bookmarks are stored."""
        return XABase.XAURL(self.xa_elem.address())

    @property
    def is_read_only(self) -> bool:
        """Whether the bookmarks document is read-only."""
        return self.xa_elem.isReadOnly()
    
    def bookmarks(self, filter: dict = None) -> Union["XAOmniWebBookmarkList", None]:
        """Returns a list of bookmarks, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned bookmarks will have, or None
        :type filter: Union[dict, None]
        :return: The list of bookmarks
        :rtype: XAOmniWebBookmarkList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.bookmarks())
        <<class 'PyXA.apps.Bike.XABikeBookmarkList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.bookmarks(), XAOmniWebBookmarkList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.address) + ">"



class XAOmniWebBookmarkList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of OmniWeb bookmarks that employs fast enumeration techniques.

    All properties of bookmarks can be called as methods on the wrapped list, returning a list containing each bookmark's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniWebBookmark, filter)

    def address(self) -> XABase.XAURLList:
        ls = self.xa_elem.arrayByApplyingSelector_("address") or []
        return self._new_element(ls, XABase.XAURLList)

    def check_interval(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("checkInterval") or [])

    def is_new(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isNew") or [])

    def is_reachable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isReachable") or [])

    def last_checked_date(self) -> list[datetime]:
        return self.xa_elem.arrayByApplyingSelector_("lastCheckedDate") or []

    def name(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("name") or []
        return self._new_element(ls, XABase.XATextList)

    def note(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("note") or []
        return self._new_element(ls, XABase.XATextList)
    
    def by_address(self, address: Union[str, XABase.XAURL]) -> Union["XAOmniWebBookmark", None]:
        if isinstance(address, XABase.XAURL):
            address = address.url
        return self.by_property("address", address)
    
    def by_check_interval(self, check_interval: int) -> Union["XAOmniWebBookmark", None]:
        return self.by_property("checkInterval", check_interval)
    
    def by_is_new(self, is_new: bool) -> Union["XAOmniWebBookmark", None]:
        return self.by_property("isNew", is_new)
    
    def by_is_reachable(self, is_reachable: bool) -> Union["XAOmniWebBookmark", None]:
        return self.by_property("isReachable", is_reachable)
    
    def by_last_checked_date(self, last_checked_date: datetime) -> Union["XAOmniWebBookmark", None]:
        return self.by_property("lastCheckedDate", last_checked_date)

    def by_name(self, name: Union[str, XABase.XAText]) -> Union["XAOmniWebBookmark", None]:
        if isinstance(name, XABase.XAText):
            name = name.xa_elem
        return self.by_property("name", name)
    
    def by_note(self, note: Union[str, XABase.XAText]) -> Union["XAOmniWebBookmark", None]:
        if isinstance(note, XABase.XAText):
            note = note.text
        return self.by_property("note", note)
    
    def bookmarks(self) -> 'XAOmniWebBookmarkList':
        """Returns a list of all bookmarks contained by the bookmarks documents in the list.

        :return: The list of bookmarks
        :rtype: XAOmniWebBookmarkList

        .. versionadded:: 0.3.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bookmarks") or []
        return self._new_element(ls, XAOmniWebBookmarkList)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAOmniWebBookmark(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A bookmark in OmniWeb.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def address(self) -> XABase.XAURL:
        """The URL of the bookmark."""
        return XABase.XAURL(self.xa_elem.address())

    @address.setter
    def address(self, address: Union[str, XABase.XAURL]):
        if isinstance(address, XABase.XAURL):
            address = address.url
        self.set_property("address", address)

    @property
    def check_interval(self) -> int:
        """The number of seconds between checks for updates to the bookmark."""
        return self.xa_elem.checkInterval()

    @check_interval.setter
    def check_interval(self, check_interval: int):
        self.set_property("checkInterval", check_interval)

    @property
    def is_new(self) -> bool:
        """Whether the bookmark has been added since the last time it was checked for updates."""
        return self.xa_elem.isNew()

    @is_new.setter
    def is_new(self, is_new: bool):
        self.set_property("isNew", is_new)

    @property
    def is_reachable(self) -> bool:
        """Whether this page could be retrieved last time it was checked."""
        return self.xa_elem.isReachable()

    @is_reachable.setter
    def is_reachable(self, is_reachable: bool):
        self.set_property("isReachable", is_reachable)

    @property
    def last_checked_date(self) -> datetime:
        """The date and time the bookmark was last checked for updates."""
        return self.xa_elem.lastCheckedDate()

    @property
    def name(self) -> XABase.XAText:
        """The label text of the bookmark item."""
        return self._new_element(self.xa_elem.name(), XABase.XAText)

    @name.setter
    def name(self, name: Union[str, XABase.XAText]):
        if isinstance(name, XABase.XAText):
            name = name.text
        self.set_property("name", name)

    @property
    def note(self) -> XABase.XAText:
        """The annotation text of the bookmark item."""
        return self._new_element(self.xa_elem.note(), XABase.XAText)

    @note.setter
    def note(self, note: Union[str, XABase.XAText]):
        if isinstance(note, XABase.XAText):
            note = note.text
        self.set_property("note", note)

    def bookmarks(self, filter: dict = None) -> Union["XAOmniWebBookmarkList", None]:
        """Returns a list of bookmarks, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned bookmarks will have, or None
        :type filter: Union[dict, None]
        :return: The list of bookmarks
        :rtype: XAOmniWebBookmarkList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.bookmarks())
        <<class 'PyXA.apps.Bike.XABikeBookmarkList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.3.0
        """
        return self._new_element(self.xa_elem.bookmarks(), XAOmniWebBookmarkList, filter)
    
    def check_for_updates(self, including_children = False) -> None:
        """Checks the bookmark for updates of its resources.

        :param including_children: Whether to check all of the bookmark's children for updates as well, defaults to False
        :type including_children: bool, optional

        .. versionadded:: 0.3.0
        """
        self.xa_elem.checkForUpdatesIncludingChildren_(including_children)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
