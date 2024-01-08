""".. versionadded:: 0.1.0

Control Bike using JXA-like syntax.
"""

from enum import Enum
from typing import Union, Any

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import (
    XACanOpenPath,
    XAClipboardCodable,
    XACloseable,
    XADeletable,
    XAPrintable,
)
from ..XAErrors import UnconstructableClassError
from ..XAEvents import event_from_str


class XABikeApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Bike.app.

    .. versionadded:: 0.1.0
    """

    class ObjectType(Enum):
        """Types of objects that can be created with :func:`XABikeApplication.make`."""
        WINDOW = "window"
        DOCUMENT = "document"
        ROW = "row"
        ATTRIBUTE = "attribute"

    class FileFormat(Enum):
        BIKE = XABase.OSType("BKff")
        OPML = XABase.OSType("OPml")
        PLAINTEXT = XABase.OSType("PTfm")

    class EditMode(Enum):
        TEXT = XABase.OSType("Btmd")
        OUTLINE = XABase.OSType("Bomd")

    class RowType(Enum):
        BODY = XABase.OSType("Brtb")
        HEADING = XABase.OSType("Brth")
        QUOTE = XABase.OSType("Brtq")
        CODE = XABase.OSType("Brtc")
        NOTE = XABase.OSType("Brtn")
        UNORDERED = XABase.OSType("Brtu")
        ORDERED = XABase.OSType("Brto")
        TASK = XABase.OSType("Brtt")
        HORIZONTAL_RULE = XABase.OSType("Brtr")

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XABikeWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Bike is the frontmost application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of Bike.app."""
        return self.xa_scel.version()

    @property
    def font_size(self) -> Union[int, float]:
        """Bike font size preference."""
        return self.xa_scel.fontSize()

    @font_size.setter
    def font_size(self, font_size: Union[int, float]):
        self.set_property("fontSize", font_size)

    @property
    def background_color(self) -> XABase.XAColor:
        """Bike background color preference."""
        return XABase.XAColor(self.xa_scel.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property("backgroundColor", background_color._nscolor)

    @property
    def foreground_color(self) -> XABase.XAColor:
        """Bike foreground color preference."""
        return XABase.XAColor(self.xa_scel.foregroundColor())

    @foreground_color.setter
    def foreground_color(self, foreground_color: XABase.XAColor):
        self.set_property("foregroundColor", foreground_color._nscolor)

    def documents(self, filter: dict = None) -> Union["XABikeDocumentList", None]:
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

    def make(
        self,
        specifier: Union[str, "XABikeApplication.ObjectType"],
        properties: Union[dict, None] = None,
        data: Any = None,
    ) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XABikeApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to initialize the object with
        :type data: Any
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

        .. versionadded:: 0.1.0
        """
        if isinstance(specifier, XABikeApplication.ObjectType):
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
            raise UnconstructableClassError("Windows cannot be created for Bike.app.")
        elif specifier == "document":
            return self._new_element(obj, XABikeDocument)
        elif specifier == "row":
            return self._new_element(obj, XABikeRow)
        elif specifier == "attribute":
            return self._new_element(obj, XABikeAttribute)


class XABikeWindow(XABaseScriptable.XASBWindow, XAPrintable):
    """A window of Bike.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XABikeDocument":
        """The document whose contents are currently displayed in the window."""
        return self._new_element(self.xa_elem.document(), XABikeDocument)

    def print(
        self, print_properties: Union[dict, None] = None, show_dialog: bool = True
    ) -> "XABikeDocument":
        return super().print(print_properties, show_dialog, new_thread=False)

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
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("url") or []
        return [XABase.XAURL(x) for x in ls]

    def root_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("rootRow") or []
        return self._new_element(ls, XABikeRowList)

    def entireContents(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents") or []
        ls = [row for contents in ls for row in contents]
        return self._new_element(ls, XABikeRowList)

    def focused_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("focusedRow") or []
        return self._new_element(ls, XABikeRowList)

    def hoisted_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("hoistedRow") or []
        return self._new_element(ls, XABikeRowList)

    def edit_mode(self) -> list[XABikeApplication.EditMode]:
        ls = self.xa_elem.arrayByApplyingSelector_("editMode") or []
        return [XABikeApplication.EditMode(XABase.OSType(x.stringValue())) for x in ls]

    def selected_text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("selectedText") or [])

    def selection_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRow") or []
        return self._new_element(ls, XABikeRowList)

    def selection_rows(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRows") or []
        ls = [row for contents in ls for row in contents]
        return self._new_element(ls, XABikeRowList)

    def by_name(self, name: str) -> Union["XABikeDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XABikeDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: Union[str, XABase.XAPath]) -> Union["XABikeDocument", None]:
        if isinstance(file, XABase.XAPath):
            file = file.path
        return self.by_property("file", file)

    def by_id(self, id: str) -> Union["XABikeDocument", None]:
        return self.by_property("id", id)

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union["XABikeDocument", None]:
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("url", url)

    def by_root_row(self, root_row: "XABikeRow") -> Union["XABikeDocument", None]:
        return self.by_property("rootRow", root_row.xa_elem)

    def by_entire_contents(
        self, entire_contents: Union["XABikeRowList", list["XABikeRow"]]
    ) -> Union["XABikeDocument", None]:
        if isinstance(entire_contents, list):
            entire_contents = [x.xa_elem for x in entire_contents]
            return self.by_property("entireContents", entire_contents)
        else:
            return self.by_property("entireContents", entire_contents.xa_elem)

    def by_focused_row(self, focused_row: "XABikeRow") -> Union["XABikeDocument", None]:
        return self.by_property("focusedRow", focused_row.xa_elem)

    def by_hoisted_row(self, hoisted_row: "XABikeRow") -> Union["XABikeDocument", None]:
        return self.by_property("hoistedRow", hoisted_row.xa_elem)

    def by_edit_mode(
        self, edit_mode: XABikeApplication.EditMode
    ) -> Union["XABikeDocument", None]:
        return self.by_property(
            "editMode", event_from_str(XABase.unOSType(edit_mode.value))
        )

    def by_selected_text(self, selected_text: str) -> Union["XABikeDocument", None]:
        return self.by_property("selectedText", selected_text)

    def by_selection_row(
        self, selection_row: "XABikeRow"
    ) -> Union["XABikeDocument", None]:
        return self.by_property("selectionRow", selection_row.xa_elem)

    def by_selection_rows(
        self, selection_rows: Union["XABikeRowList", list["XABikeRow"]]
    ) -> Union["XABikeDocument", None]:
        if isinstance(selection_rows, list):
            selection_rows = [x.xa_elem for x in selection_rows]
            return self.by_property("selectionRows", selection_rows)
        else:
            return self.by_property("selectionRows", selection_rows.xa_elem)

    def close(self, save: "XACloseable.SaveOption" = None):
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


class XABikeDocument(XABase.XAObject, XACloseable, XAPrintable, XADeletable):
    """A document of Bike.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the document."""
        return self.xa_elem.name()

    @property
    def modified(self) -> str:
        """Whether the document has been modified since it was last saved."""
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        """The location of the document on disk, if it has one."""
        return XABase.XAPath(self.xa_elem.file())

    @property
    def id(self) -> str:
        """The unique and persistent identifier for the document."""
        return self.xa_elem.id()

    @property
    def url(self) -> XABase.XAURL:
        """The Bike URL link for the document."""
        return XABase.XAURL(self.xa_elem.url())

    @property
    def root_row(self) -> "XABikeRow":
        """The top 'root' row of the document, not visible in the outline editor."""
        return self._new_element(self.xa_elem.rootRow(), XABikeRow)

    @property
    def entire_contents(self) -> "XABikeRowList":
        """All rows in the document."""
        return self._new_element(self.xa_elem.entireContents(), XABikeRowList)

    @property
    def focused_row(self) -> "XABikeRow":
        """The currently focused row."""
        return self._new_element(self.xa_elem.focusedRow(), XABikeRow)

    @focused_row.setter
    def focused_row(self, focused_row: "XABikeRow"):
        self.set_property("focusedRow", focused_row.xa_elem)

    @property
    def hoisted_row(self) -> "XABikeRow":
        """The currently hoisted row."""
        return self._new_element(self.xa_elem.hoisted_row(), XABikeRow)

    @hoisted_row.setter
    def hoisted_row(self, hoisted_row: "XABikeRow"):
        self.set_property("hoistedRow", hoisted_row.xa_elem)

    @property
    def edit_mode(self) -> XABikeApplication.EditMode:
        """The document's edit mode."""
        return XABikeApplication.EditMode(self.xa_elem.editMode())

    @edit_mode.setter
    def edit_mode(self, edit_mode: XABikeApplication.EditMode):
        self.set_property("editMode", edit_mode.value)

    @property
    def selected_text(self) -> str:
        """The currently selected text."""
        return self.xa_elem.selectedText()

    @property
    def selection_row(self) -> "XABikeRow":
        """The row intersecting the selected text head."""
        return self._new_element(self.xa_elem.selectionRow(), XABikeRow)

    @property
    def selection_rows(self) -> "XABikeRowList":
        """All rows intersecting the selected text."""
        return self._new_element(self.xa_elem.selectionRows(), XABikeRowList)

    def print(
        self, print_properties: Union[dict, None] = None, show_dialog: bool = True
    ) -> "XABikeDocument":
        return super().print(print_properties, show_dialog, new_thread=False)

    def query(self, outline_path: str) -> Union["XABikeRowList", int, str, bool]:
        """Queries the document for the given outline path.

        :param outline_path: The outline path to query for
        :type outline_path: str
        :return: The queried row(s), numbers, booleans, or texts
        :rtype: Union['XABikeRowList', int, str, bool]

        .. versionadded:: 0.3.0
        """
        result = self.xa_elem.queryOutlinePath_(outline_path)
        if isinstance(result, float) or isinstance(result, int):
            return result
        elif isinstance(result, str):
            return result
        elif isinstance(result, bool):
            return result
        else:
            return self._new_element(result, XABikeRowList)

    def save(
        self,
        path: Union[str, XABase.XAPath, None] = None,
        format: XABikeApplication.FileFormat = XABikeApplication.FileFormat.BIKE,
    ):
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

    def import_rows(
        self,
        text: Union[str, XABase.XAText],
        format: XABikeApplication.FileFormat = XABikeApplication.FileFormat.PLAINTEXT,
        parent: Union["XABikeRow", None] = None,
    ) -> "XABikeRowList":
        """Imports rows into the document.

        :param text: The text to import
        :type text: Union[str, XABase.XAText]
        :param format: The texts format, defaults to XABikeApplication.FileFormat.PLAINTEXT
        :type format: XABikeApplication.FileFormat, optional
        :param parent: The location to insert the new row(s), or None to import at the end of the document, defaults to None
        :type parent: Union['XABikeRow', None], optional
        :return: The imported row(s)
        :rtype: XABikeRowList

        .. versionadded:: 0.2.1
        """
        if isinstance(text, XABase.XAText):
            text = text.xa_elem

        if parent is None:
            parent = self

        new_rows = self.xa_elem.importFrom_as_to_(
            text, format.value, parent.xa_elem.rows()[-1].positionAfter()
        )
        return self._new_element(new_rows, XABikeRowList)

    def export(
        self,
        rows: Union[list["XABikeRow"], "XABikeRowList", None] = None,
        format: XABikeApplication.FileFormat = XABikeApplication.FileFormat.PLAINTEXT,
        all: bool = True,
    ) -> str:
        """Exports rows from the document.

        :param rows: The rows to export, or None to export the entire document, defaults to None
        :type rows: Union[list['XABikeRow'], 'XABikeRowList', None], optional
        :param format: The file fort to export rows as, defaults to XABikeApplication.FileFormat.PLAINTEXT
        :type format: XABikeApplication.FileFormat, optional
        :param all: Export all contained rows (true) or only the given rows (false), defaults to True
        :type all: bool, optional
        :return: The formatted text of the exported rows
        :rtype: str

        .. versionadded:: 0.2.1
        """
        if isinstance(rows, XABikeRowList):
            rows = rows.xa_elem
        elif isinstance(rows, list):
            rows = [x.xa_elem for x in rows]
        return self.xa_elem.exportFrom_as_all_(rows, format.value, all)

    def rows(self, filter: dict = None) -> Union["XABikeRowList", None]:
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
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def type(self) -> list[XABikeApplication.RowType]:
        ls = self.xa_elem.arrayByApplyingSelector_("type") or []
        return [XABikeApplication.RowType(XABase.OSType(x.stringValue())) for x in ls]

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("url") or []
        return [XABase.XAURL(x) for x in ls]

    def level(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("level") or [])

    def contains_rows(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("containsRows") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def container(self) -> list[Union[XABikeDocument, "XABikeRow"]]:
        return [x.container for x in self]

    def container_document(self) -> XABikeDocument:
        ls = self.xa_elem.arrayByApplyingSelector_("containerDocument") or []
        return self._new_element(ls, XABikeDocumentList)

    def container_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("containerRow") or []
        return self._new_element(ls, XABikeRowList)

    def prev_sibling_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("prevSiblingRow") or []
        return self._new_element(ls, XABikeRowList)

    def next_sibling_row(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("nextSiblingRow") or []
        return self._new_element(ls, XABikeRowList)

    def entire_contents(self) -> "XABikeRowList":
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents") or []
        ls = [item for contents in ls for item in contents]
        return self._new_element(ls, XABikeRowList)

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def expanded(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("expanded") or [])

    def collapsed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed") or [])

    def by_id(self, id: str) -> Union["XABikeRow", None]:
        return self.by_property("id", id)

    def by_type(self, type: XABikeApplication.RowType) -> Union["XABikeRow", None]:
        return self.by_property("type", event_from_str(XABase.unOSType(type.value)))

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union["XABikeRow", None]:
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("url", url)

    def by_level(self, level: int) -> Union["XABikeRow", None]:
        return self.by_property("level", level)

    def by_contains_rows(self, contains_rows: bool) -> Union["XABikeRow", None]:
        return self.by_property("containsRows", contains_rows)

    def by_name(self, name: str) -> Union["XABikeRow", None]:
        return self.by_property("name", name)

    def by_container(
        self, container: Union[XABikeDocument, "XABikeRow"]
    ) -> Union["XABikeRow", None]:
        return self.by_property("container", container.xa_elem)

    def by_container_row(self, container_row: "XABikeRow") -> Union["XABikeRow", None]:
        return self.by_property("containerRow", container_row.xa_elem)

    def by_prev_sibling_row(
        self, prev_sibling_row: "XABikeRow"
    ) -> Union["XABikeRow", None]:
        return self.by_property("prevSiblingRow", prev_sibling_row.xa_elem)

    def by_next_sibling_row(
        self, next_sibling_row: "XABikeRow"
    ) -> Union["XABikeRow", None]:
        return self.by_property("nextSiblingRow", next_sibling_row.xa_elem)

    def by_container_document(
        self, container_document: XABikeDocument
    ) -> Union["XABikeRow", None]:
        return self.by_property("containerDocument", container_document.xa_elem)

    def by_entire_contents(
        self, entire_contents: Union["XABikeRowList", list["XABikeRow"]]
    ) -> Union["XABikeRow", None]:
        if isinstance(entire_contents, list):
            entire_contents = [x.xa_elem for x in entire_contents]
            return self.by_property("entireContents", entire_contents)
        else:
            return self.by_property("entireContents", entire_contents.xa_elem)

    def by_visible(self, visible: bool) -> Union["XABikeRow", None]:
        return self.by_property("visible", visible)

    def by_selected(self, selected: bool) -> Union["XABikeRow", None]:
        return self.by_property("selected", selected)

    def by_expanded(self, expanded: bool) -> Union["XABikeRow", None]:
        return self.by_property("expanded", expanded)

    def by_collapsed(self, collapsed: bool) -> Union["XABikeRow", None]:
        return self.by_property("collapsed", collapsed)

    def rows(self) -> "XABikeRowList":
        """Returns a list of all rows contained by the rows in the list.

        :return: The list of rows
        :rtype: XABikeRowList

        .. versionadded:: 0.3.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("rows") or []
        ls = [row for row in ls]
        return self._new_element(ls, XABikeRowList)

    def attributes(self) -> "XABikeAttributeList":
        """Returns a list of all attributes contained by the rows in the list.

        :return: The list of attributes
        :rtype: XABikeAttributeList

        .. versionadded:: 0.3.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("attributes") or []
        ls = [attribute for attribute in ls]
        return self._new_element(ls, XABikeAttributeList)

    def delete(self) -> None:
        """Deletes all rows in the list.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.makeObjectsPerformSelector_("delete")

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

    @property
    def id(self) -> str:
        """The unique and persistent identifier for the row."""
        return self.xa_elem.id()

    @property
    def type(self) -> XABikeApplication.RowType:
        """The type of the row."""
        return XABikeApplication.RowType(self.xa_elem.type())

    @type.setter
    def type(self, type: XABikeApplication.RowType):
        self.set_property("type", type.value)

    @property
    def url(self) -> XABase.XAURL:
        """The Bike URL for the row combining the document ID with the item ID."""
        return XABase.XAURL(self.xa_elem.url())

    @property
    def level(self) -> int:
        """The indentation level for the row in the outline."""
        return self.xa_elem.level()

    @property
    def text_content(self) -> type:
        content = self.xa_elem.textContent()
        if type(content) == str:
            return content
        return content.get()

    @text_content.setter
    def text_content(self, text_content: Union[str, XABase.XAText]):
        if isinstance(text_content, XABase.XAText):
            text_content = text_content.xa_elem
        self.set_property("textContent", text_content)

    @property
    def contains_rows(self) -> bool:
        """True if the row contains other rows."""
        return self.xa_elem.containsRows()

    @property
    def name(self) -> str:
        """The plain text content of the row."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def container(self) -> Union["XABikeRow", XABikeDocument]:
        """The container of the row."""
        container = self.xa_elem.container()
        if hasattr(container, "level"):
            return self._new_element(container, XABikeRow)
        else:
            return self._new_element(container, XABikeDocument)

    @property
    def container_row(self) -> Union["XABikeRow", None]:
        """The row that directly contains this row."""
        row = self.xa_elem.containerRow()
        if row is not None:
            return self._new_element(row, XABikeRow)

    @property
    def prev_sibling_row(self) -> "XABikeRow":
        """The previous row with the same container row as this row."""
        return self._new_element(self.xa_elem.prevSiblingRow(), XABikeRow)

    @property
    def next_sibling_row(self) -> type:
        """The next row with the same container as this row."""
        return self._new_element(self.xa_elem.nextSiblingRow(), XABikeRow)

    @property
    def container_document(self) -> XABikeDocument:
        """The document that contains this row."""
        return self._new_element(self.xa_elem.containerDocument(), XABikeDocument)

    @property
    def entire_contents(self) -> XABikeRowList:
        """The list of all rows contained by this row."""
        return self._new_element(self.xa_elem.entire_contents(), XABikeRowList)

    @property
    def visible(self) -> bool:
        """True if this row is visible in the window (may require scrolling)."""
        return self.xa_elem.visible()

    @property
    def selected(self) -> bool:
        """True if this row is selected in the window."""
        return self.xa_elem.selected()

    @property
    def expanded(self) -> bool:
        """True if this row is expanded in the window."""
        return self.xa_elem.expanded()

    @property
    def collapsed(self) -> bool:
        """True if this row is collapsed in the window."""
        return self.xa_elem.collapsed()

    def delete(self) -> None:
        """Deletes the row.

        .. versionadded:: 0.3.0
        """
        self.xa_elem.delete()

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

    def move_to(self, location: "XABikeRow"):
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

    def duplicate(
        self,
        location: Union[XABikeDocument, "XABikeRow", None] = None,
        properties: Union[dict, None] = None,
    ):
        """Duplicates the row either in-place or at a specified location.

        :param location: The document or row to create a duplicate of this row in, defaults to None (duplicate in-place)
        :type location: Union[XABikeDocument, XABikeRow, None], optional
        :param properties: Properties to set in the new copy right away, defaults to None (no properties changed)
        :type properties: Union[dict, None], options
        """
        if properties is None:
            properties = {}

        if location is None:
            self.xa_elem.duplicateTo_withProperties_(
                self.xa_elem.positionAfter(), properties
            )
        else:
            self.xa_elem.duplicateTo_withProperties_(
                location.xa_elem.rows().lastObject().positionAfter(), properties
            )

    def rows(self, filter: dict = None) -> Union["XABikeRowList", None]:
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

    def attributes(self, filter: dict = None) -> Union["XABikeAttributeList", None]:
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
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def container_row(self) -> XABikeRowList:
        ls = self.xa_elem.arrayByApplyingSelector_("containerRow") or []
        return self._new_element(ls, XABikeRowList)

    def by_name(self, name: str) -> Union["XABikeAttribute", None]:
        return self.by_property("name", name)

    def by_value(self, value: str) -> Union["XABikeAttribute", None]:
        return self.by_property("value", value)

    def by_container_row(
        self, container_row: XABikeRow
    ) -> Union["XABikeAttribute", None]:
        return self.by_property("containerRow", container_row.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XABikeAttribute(XABase.XAObject):
    """An attribute in a row.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the attribute."""
        return self.xa_elem.name()

    @property
    def value(self) -> str:
        """The value of the attribute."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: str):
        self.set_property("value", value)

    @property
    def container_row(self) -> XABikeRow:
        """The row that contains this attribute."""
        return self._new_element(self.xa_elem.containerRow(), XABikeRow)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
