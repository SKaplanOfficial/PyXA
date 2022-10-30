""".. versionadded:: 0.1.0

Control Bike using JXA-like syntax.
"""

from enum import Enum
from typing import Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable, XACloseable, XADeletable, XAPrintable
from ..XAErrors import UnconstructableClassError

class XABikeApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Bike.app.

    .. versionadded:: 0.1.0
    """
    class FileFormat(Enum):
        BIKE        = XABase.OSType("BKff")
        OPML        = XABase.OSType("OPml")
        PLAINTEXT   = XABase.OSType("PTfm")

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XABikeWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Bike is the frontmost application
        self.version: str #: The version of Bike.app
        self.font_size: Union[int, float] #: Bike font size preference
        self.background_color: XABase.XAColor #: Bike background color preference
        self.foreground_color: XABase.XAColor #: Bike foreground color preference

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
    def font_size(self) -> Union[int, float]:
        return self.xa_scel.fontSize()

    @font_size.setter
    def font_size(self, font_size: Union[int, float]):
        self.set_property('fontSize', font_size)

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_scel.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property('backgroundColor', background_color.xa_elem)

    @property
    def foreground_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_scel.foregroundColor())

    @foreground_color.setter
    def foreground_color(self, foreground_color: XABase.XAColor):
        self.set_property('foregroundColor', foreground_color.xa_elem)

    def documents(self, filter: dict = None) -> Union['XABikeDocumentList', None]:
        """Returns a list of documents, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XABikeDocumentList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> print(app.documents())
        <<class 'PyXA.apps.Bike.XABikeDocumentList'>['Untitled', 'PyXA Notes.bike']>

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.documents(), XABikeDocumentList, filter)

    def make(self, specifier: str, properties: Union[dict, None] = None) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
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

        .. versionadded:: 0.1,0
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "window":
            raise UnconstructableClassError("Windows cannot be created for Bike.app.")
        elif specifier == "document":
            return self._new_element(obj, XABikeDocument)
        elif specifier == "row":
            return self._new_element(obj, XABikeRow)
        elif specifier == "attribute":
            return self._new_element(obj, XABikeAttribute)




class XABikeWindow(XABaseScriptable.XASBWindow):
    """A window of Bike.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)
        
        self.name: str #: The title of the window
        self.id: int #: The unique identifier of the window
        self.index: int #: The index of the window, ordered front to back
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window has a minimize button
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window has a zoom button
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XABikeDocument #: The document whose contents are currently displayed in the window

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property('index', index)

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return (origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: tuple[int, int, int, int]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property('miniaturized', miniaturized)

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property('visible', visible)

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property('zoomed', zoomed)

    @property
    def document(self) -> 'XABikeDocument':
        return self._new_element(self.xa_elem.document(), XABikeDocument)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"




class XABikeDocumentList(XABase.XAList, XACanOpenPath, XAClipboardCodable):
    """A wrapper around lists of Bike documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XABikeDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of document file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> list[str]:
        """Gets the ID of each document in the list.

        :return: A list of document IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))
    
    def url(self) -> list[XABase.XAURL]:
        """Gets the URL of each document in the list.

        :return: A list of document urls
        :rtype: list[XABase.XAURL]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("url")
        return [XABase.XAURL(x) for x in ls]

    def root_row(self) -> 'XABikeRowList':
        """Gets the root row of each document in the list.

        :return: A list of document root rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("rootRow")
        return self._new_element(ls, XABikeRowList)

    def entireContents(self) -> 'XABikeRowList':
        """Gets the entire contents of each document in the list.

        :return: A list of document rows
        :rtype: XABikeRowLists
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents")
        ls = [row for contents in ls for row in contents]
        return self._new_element(ls, XABikeRowList)

    def focused_row(self) -> 'XABikeRowList':
        """Gets the focused row of each document in the list.

        :return: A list of document focused rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("focusedRow")
        return self._new_element(ls, XABikeRowList)

    def hoisted_row(self) -> 'XABikeRowList':
        """Gets the hoisted row of each document in the list.

        :return: A list of document hoisted rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("hoistedRow")
        return self._new_element(ls, XABikeRowList)

    def selected_text(self) -> list[str]:
        """Gets the selected text of each document in the list.

        :return: A list of document selected texts
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("selectedText"))

    def selection_row(self) -> 'XABikeRowList':
        """Gets the selection row of each document in the list.

        :return: A list of document selection rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRow")
        return self._new_element(ls, XABikeRowList)

    def selection_rows(self) -> 'XABikeRowList':
        """Gets the selection rows of each document in the list.

        :return: A list of document selection rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRows")
        ls = [row for contents in ls for row in contents]
        return self._new_element(ls, XABikeRowList)

    def by_name(self, name: str) -> Union['XABikeDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XABikeDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("modified", modified)

    def by_file(self, file: Union[str, XABase.XAPath]) -> Union['XABikeDocument', None]:
        """Retrieves the document whose file path matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(file, XABase.XAPath):
            file = file.path
        return self.by_property("file", file)

    def by_id(self, id: str) -> Union['XABikeDocument', None]:
        """Retrieves the document whose ID matches the given ID, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union['XABikeDocument', None]:
        """Retrieves the document whose URL matches the given URL, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("url", url)

    def by_root_row(self, root_row: 'XABikeRow') -> Union['XABikeDocument', None]:
        """Retrieves the document whose root row matches the given row, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("rootRow", root_row.xa_elem)

    def by_entire_contents(self, entire_contents: Union['XABikeRowList', list['XABikeRow']]) -> Union['XABikeDocument', None]:
        """Retrieves the document whose entire contents matches the given list of rows, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(entire_contents, list):
            entire_contents = [x.xa_elem for x in entire_contents]
            return self.by_property("entireContents", entire_contents)
        else:
            return self.by_property("entireContents", entire_contents.xa_elem)

    def by_focused_row(self, focused_row: 'XABikeRow') -> Union['XABikeDocument', None]:
        """Retrieves the document whose focused row matches the given row, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("focusedRow", focused_row.xa_elem)

    def by_hoisted_row(self, hoisted_row: 'XABikeRow') -> Union['XABikeDocument', None]:
        """Retrieves the document whose hoisted row matches the given row, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hoistedRow", hoisted_row.xa_elem)

    def by_selected_text(self, selected_text: str) -> Union['XABikeDocument', None]:
        """Retrieves the document whose selected text matches the given text, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("selectedText", selected_text)

    def by_selection_row(self, selection_row: 'XABikeRow') -> Union['XABikeDocument', None]:
        """Retrieves the document whose selection row matches the given row, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("selectionRow", selection_row.xa_elem)

    def by_selection_rows(self, selection_rows: Union['XABikeRowList', list['XABikeRow']]) -> Union['XABikeDocument', None]:
        """Retrieves the document whose selection rows match the given list of rows, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XABikeDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(selection_rows, list):
            selection_rows = [x.xa_elem for x in selection_rows]
            return self.by_property("selectionRows", selection_rows)
        else:
            return self.by_property("selectionRows", selection_rows.xa_elem)

    def close(self, save: 'XACloseable.SaveOption' = None):
        """Closes every document in the list. Leaves the last document open if it is the only document open in the application.
        
        :param save: Whether to save the documents before closing, defaults to YES
        :type save: XACloseable.SaveOption, optional

        .. versionadded:: 0.1.0
        """
        if save is None:
            save = 1852776480
        else:
            save = save.value

        for document in self.xa_elem:
            document.closeSaving_savingIn_(save, None)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XABikeDocument(XABase.XAObject, XACloseable):
    """A document of Bike.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since it was last saved
        self.file: XABase.XAPath #: The location of the document on disk, if it has one
        self.id: str #: The unique and persistent identifier for the document
        self.url: XABase.XAURL #: The Bike URL link for the document
        self.root_row: XABikeRow #: The top 'root' row of the document, not visible in the outline editor
        self.entire_contents: XABikeRowList #: All rows in the document
        self.focused_row: XABikeRow #: The currently focused row
        self.hoisted_row: XABikeRow #: The currently hoisted row
        self.selected_text: str #: The currently selected text
        self.selection_row: XABikeRow #: The row intersecting the selected text head
        self.selection_rows: XABikeRowList #: All rows intersecting the selected text

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> str:
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.file())

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.url())

    @property
    def root_row(self) -> 'XABikeRow':
        return self._new_element(self.xa_elem.rootRow(), XABikeRow)

    @property
    def entire_contents(self) -> 'XABikeRowList':
        return self._new_element(self.xa_elem.entireContents(), XABikeRowList)

    @property
    def focused_row(self) -> 'XABikeRow':
        return self._new_element(self.xa_elem.focusedRow(), XABikeRow)

    @focused_row.setter
    def focused_row(self, focused_row: 'XABikeRow'):
        self.set_property('focusedRow', focused_row.xa_elem)

    @property
    def hoisted_row(self) -> 'XABikeRow':
        return self._new_element(self.xa_elem.hoisted_row(), XABikeRow)

    @hoisted_row.setter
    def hoisted_row(self, hoisted_row: 'XABikeRow'):
        self.set_property('hoistedRow', hoisted_row.xa_elem)

    @property
    def selected_text(self) -> str:
        return self.xa_elem.selectedText()

    @property
    def selection_row(self) -> 'XABikeRow':
        return self._new_element(self.xa_elem.selectionRow(), XABikeRow)

    @property
    def selection_rows(self) -> 'XABikeRowList':
        return self._new_element(self.xa_elem.selectionRows(), XABikeRowList)

    def save(self, path: Union[str, XABase.XAPath, None] = None, format: XABikeApplication.FileFormat = XABikeApplication.FileFormat.BIKE):
        """Saves the document to the specified location, or at its existing location.

        :param path: The location to save the document in, defaults to None
        :type path: Union[str, XABase.XAPath, None], optional
        :param format: The format to save the document as, defaults to XABikeApplication.FileFormat.BIKE
        :type format: XABikeApplication.FileFormat, optional

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> doc = app.documents()[0]
        >>> doc.save("/Users/exampleUser/Documents/Notes.opml", app.FileFormat.OPML)

        .. versionadded:: 0.1.0
        """
        if path is None:
            path = self.xa_elem.file()
        elif isinstance(path, str):
            path = XABase.XAPath(path).xa_elem
        self.xa_elem.saveIn_as_(path, format.value)

    def rows(self, filter: dict = None) -> Union['XABikeRowList', None]:
        """Returns a list of rows, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XABikeRowList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> doc = app.front_window.document
        >>> print(doc.rows())
        <<class 'PyXA.apps.Bike.XABikeRowList'>['Row 1', 'Row 2', 'Row 2.1']>

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.rows(), XABikeRowList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XABikeRowList(XABase.XAList):
    """A wrapper around a list of rows.

    All properties of row objects can be accessed via methods on the list, returning a list of each row's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XABikeRow, filter)

    def id(self) -> list[str]:
        """Gets the ID of each row in the list.

        :return: A list of row IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def url(self) -> list[XABase.XAURL]:
        """Gets the URL of each row in the list.

        :return: A list of row URLs
        :rtype: list[XABase.XAURL]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("url")
        return [XABase.XAURL(x) for x in ls]

    def level(self) -> list[int]:
        """Gets the level of each row in the list.

        :return: A list of row levels
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("level"))

    def contains_rows(self) -> list[bool]:
        """Gets the contains rows status of each row in the list.

        :return: A list of row contains rows status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("containsRows"))

    def name(self) -> list[str]:
        """Gets the name of each row in the list.

        :return: A list of row names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def container(self) -> list[Union[XABikeDocument, 'XABikeRow']]:
        """Gets the container of each row in the list.

        :return: A list of row containers
        :rtype: list[Union[XABikeDocument, 'XABikeRow']]
        
        .. versionadded:: 0.1.0
        """
        return [x.container for x in self]

    def container_row(self) -> 'XABikeRowList':
        """Gets the container row of each row in the list.

        :return: A list of row container rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("containerRow")
        return self._new_element(ls, XABikeRowList)

    def prev_sibling_row(self) -> 'XABikeRowList':
        """Gets the previous sibling row of each row in the list.

        :return: A list of row previous sibling rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("prevSiblingRow")
        return self._new_element(ls, XABikeRowList)

    def next_sibling_row(self) -> 'XABikeRowList':
        """Gets the next sibling row of each row in the list.

        :return: A list of row next sibling rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("nextSiblingRow")
        return self._new_element(ls, XABikeRowList)

    def entire_contents(self) -> 'XABikeRowList':
        """Gets the all contained rows of each row in the list.

        :return: A list of contained rows
        :rtype: XABikeRowList
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents")
        ls = [item for contents in ls for item in contents]
        return self._new_element(ls, XABikeRowList)

    def visible(self) -> list[bool]:
        """Gets the visible status of each row in the list.

        :return: A list of row visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def selected(self) -> list[bool]:
        """Gets the selected status of each row in the list.

        :return: A list of row selected status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("selected"))

    def expanded(self) -> list[bool]:
        """Gets the expanded status of each row in the list.

        :return: A list of row expanded status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("expanded"))

    def collapsed(self) -> list[bool]:
        """Gets the collapsed status of each row in the list.

        :return: A list of row collapsed status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed"))

    def by_id(self, id: str) -> Union['XABikeRow', None]:
        """Retrieves the row whose ID matches the given ID, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union['XABikeRow', None]:
        """Retrieves the row whose URL matches the given URL, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("url", url)

    def by_level(self, level: int) -> Union['XABikeRow', None]:
        """Retrieves the first row whose level matches the given level, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("level", level)

    def by_contains_rows(self, contains_rows: bool) -> Union['XABikeRow', None]:
        """Retrieves the first row whose contains rows status matches the given boolean value, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("containsRows", contains_rows)

    def by_name(self, name: str) -> Union['XABikeRow', None]:
        """Retrieves the row whose name matches the given name, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_container(self, container: Union[XABikeDocument, 'XABikeRow']) -> Union['XABikeRow', None]:
        """Retrieves the first row whose container matches the given container, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("container", container.xa_elem)

    def by_container_row(self, container_row: 'XABikeRow') -> Union['XABikeRow', None]:
        """Retrieves the first row whose container row matches the given row, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("containerRow", container_row.xa_elem)

    def by_prev_sibling_row(self, prev_sibling_row: 'XABikeRow') -> Union['XABikeRow', None]:
        """Retrieves the row whose previous sibling row matches the given row, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("prevSiblingRow", prev_sibling_row.xa_elem)

    def by_next_sibling_row(self, next_sibling_row: 'XABikeRow') -> Union['XABikeRow', None]:
        """Retrieves the row whose next sibling row matches the given row, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("nextSiblingRow", next_sibling_row.xa_elem)

    def by_container_document(self, container_document: XABikeDocument) -> Union['XABikeRow', None]:
        """Retrieves the first row whose container document matches the given document, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("containerDocument", container_document.xa_elem)

    def by_entire_contents(self, entire_contents: Union['XABikeRowList', list['XABikeRow']]) -> Union['XABikeRow', None]:
        """Retrieves the row whose entire contents matches the given list of rows, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(entire_contents, list):
            entire_contents = [x.xa_elem for x in entire_contents]
            return self.by_property("entireContents", entire_contents)
        else:
            return self.by_property("entireContents", entire_contents.xa_elem)

    def by_visible(self, visible: bool) -> Union['XABikeRow', None]:
        """Retrieves the first row whose visible status matches the given boolean value, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("visible", visible)

    def by_selected(self, selected: bool) -> Union['XABikeRow', None]:
        """Retrieves the first row whose selected status matches the given boolean value, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("selected", selected)

    def by_expanded(self, expanded: bool) -> Union['XABikeRow', None]:
        """Retrieves the first row whose expanded status matches the given boolean value, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("expanded", expanded)

    def by_collapsed(self, collapsed: bool) -> Union['XABikeRow', None]:
        """Retrieves the first row whose collapsed status matches the given boolean value, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XABikeRow, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("collapsed", collapsed)

    def collapse(self, all: bool = False):
        """Collapses all rows in the list, optionally collapsing all of the children as well.

        :param all: Whether to collapse all child rows, defaults to False
        :type all: bool, optional

        .. versionadded:: 0.1.0
        """
        for row in self.xa_elem:
            row.collapse_all_([row], all)

    def expand(self, all: bool = False):
        """Expands all rows in the list, optionally expanding all of the children as well.

        :param all: Whether to expand all child rows, defaults to False
        :type all: bool, optional

        .. versionadded:: 0.1.0
        """
        for row in self.xa_elem:
            row.expand_all_(row, all)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XABikeRow(XABase.XAObject, XADeletable):
    """A row in an outline.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: The unique and persistent identifier for the row
        self.url: XABase.XAURL #: The Bike URL for the row combining the document ID with the item ID
        self.level: int #: The indentation level for the row in the outline
        self.contains_rows: bool #: True if the row contains other rows
        self.name: str #: The plain text content of the row
        self.container: Union[XABikeRow, XABikeDocument] #: Container of the row
        self.container_row: XABikeRow #: The row that directly contains this row
        self.prev_sibling_row: XABikeRow #: The previous row with the same container row as this row
        self.next_sibling_row: XABikeRow #: The next row with the same container as this row
        self.container_document: XABikeDocument #: The document that contains this row
        self.entire_contents: XABikeRowList #: The list of all rows contained by this row
        self.visible: bool #: True if this row is visible in the window (may require scrolling)
        self.selected: bool #: True if this row is selected in the window
        self.expanded: bool #: True if this row is expanded in the window
        self.collapsed: bool #: True if this row is collapsed in the window

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def url(self) -> XABase.XAURL:
        return XABase.XAURL(self.xa_elem.url())

    @property
    def level(self) -> int:
        return self.xa_elem.level()

    @property
    def contains_rows(self) -> bool:
        return self.xa_elem.containsRows()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def container(self) -> Union['XABikeRow', XABikeDocument]:
        container = self.xa_elem.container()
        if hasattr(container, "level"):
            return self._new_element(container, XABikeRow)
        else:
            return self._new_element(container, XABikeDocument)

    @property
    def container_row(self) -> Union['XABikeRow', None]:
        row = self.xa_elem.containerRow()
        if row is not None:
            return self._new_element(row, XABikeRow)

    @property
    def prev_sibling_row(self) -> 'XABikeRow':
        return self._new_element(self.xa_elem.prevSiblingRow(), XABikeRow)

    @property
    def next_sibling_row(self) -> type:
        return self._new_element(self.xa_elem.nextSiblingRow(), XABikeRow)

    @property
    def container_document(self) -> XABikeDocument:
        return self._new_element(self.xa_elem.containerDocument(), XABikeDocument)

    @property
    def entire_contents(self) -> XABikeRowList:
        return self._new_element(self.xa_elem.entire_contents(), XABikeRowList)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    @property
    def expanded(self) -> bool:
        return self.xa_elem.expanded()

    @property
    def collapsed(self) -> bool:
        return self.xa_elem.collapsed()

    def collapse(self, all: bool = False):
        """Collapses the row and optionally all rows it contains.

        :param recursive: Whether to also collapse all rows contained by this row, defaults to False
        :type recursive: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.collapseAll_(all)

    def expand(self, all: bool = False):
        """Expanded the row and optionally all rows it contains.

        :param recursive: Whether to also expand all rows contained by this row, defaults to False
        :type recursive: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.expandAll_(all)

    def move_to(self, location: 'XABikeRow'):
        """Makes the row a child of the specified row.

        :param location: The row to move this row to.
        :type location: XABikeRow

        :Example:
    
        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> doc = app.documents()[0]
        >>> row1 = doc.rows()[0]
        >>> row2 = doc.rows()[5]
        >>> row1.move_to(row2)

        .. versionadded:: 0.1.0
        """
        self.xa_elem.moveTo_(location.xa_elem)

    # def duplicate(self, location: Union[XABikeDocument, 'XABikeRow', None] = None, properties: Union[dict, None] = None):
    #     """Duplicates the row either in-place or at a specified location.

    #     :param location: The document or row to create a duplicate of this row in, defaults to None (duplicate in-place)
    #     :type location: Union[XABikeDocument, XABikeRow, None], optional
    #     :param properties: Properties to set in the new copy right away, defaults to None (no properties changed)
    #     :type properties: Union[dict, None], options
    #     """
    #     if properties is None:
    #         properties = {}

    #     if location is None:
    #         self.xa_elem.duplicateTo_withProperties_(self.xa_elem.containerDocument(), properties)
    #     else:
    #         self.xa_elem.duplicateTo_withProperties_(location.xa_elem, properties)

    def rows(self, filter: dict = None) -> Union['XABikeRowList', None]:
        """Returns a list of rows, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XABikeRowList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Bike")
        >>> doc = app.front_window.document
        >>> row = doc.rows()[4]
        >>> print(row.rows())
        <<class 'PyXA.apps.Bike.XABikeRowList'>['Watch intro movie', 'Glance through features list', 'https://www.hogbaysoftware.com/bike']>

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.rows(), XABikeRowList, filter)

    def attributes(self, filter: dict = None) -> Union['XABikeAttributeList', None]:
        """Returns a list of attributes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned attributes will have, or None
        :type filter: Union[dict, None]
        :return: The list of attributes
        :rtype: XABikeAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.attributes(), XABikeAttributeList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"



class XABikeAttributeList(XABase.XAList):
    """A wrapper around a list of attributes.

    All properties of attribute objects can be accessed via methods on the list, returning a list of each attribute's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XABikeAttribute, filter)

    def name(self) -> list[str]:
        """Gets the name of each attribute in the list.

        :return: A list of attribute names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def value(self) -> list[str]:
        """Gets the value of each attribute in the list.

        :return: A list of attribute values
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def container_row(self) -> XABikeRowList:
        """Gets the container row of each attribute in the list.

        :return: A list of attribute container rows
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("containerRow")
        return self._new_element(ls, XABikeRowList)

    def by_name(self, name: str) -> Union['XABikeAttribute', None]:
        """Retrieves the attribute whose name matches the given name, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XABikeAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_value(self, value: str) -> Union['XABikeAttribute', None]:
        """Retrieves the first attribute whose value matches the given value, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XABikeAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("value", value)

    def by_container_row(self, container_row: XABikeRow) -> Union['XABikeAttribute', None]:
        """Retrieves the first attribute whose container row matches the given row, if one exists.

        :return: The desired attribute, if it is found
        :rtype: Union[XABikeAttribute, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("containerRow", container_row.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XABikeAttribute(XABase.XAObject):
    """An attribute in a row.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the attribute
        self.value: str #: The value of the attribute
        self.container_row: XABikeRow #: The row that contains this attribute

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def value(self) -> str:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: str):
        self.set_property('value', value)

    @property
    def container_row(self) -> XABikeRow:
        return self._new_element(self.xa_elem.containerRow(), XABikeRow)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"