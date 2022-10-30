""".. versionadded:: 0.0.9

Control OmniOutliner using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from typing import Union
import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable, XACloseable, XADeletable, XAPrintable

class XAOmniOutlinerApplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """A class for managing and interacting with OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    class DisplayType(Enum):
        """Note display types.
        """
        INLINE      = XABase.OSType('Ond1') #: Inline display type
        OUT_OF_LINE = XABase.OSType('Ond2') #: Out of line display type

    class SortOrder(Enum):
        """Sort order directions.
        """
        ASCENDING   = XABase.OSType('OOs1') #: Ascending sort order
        DESCENDING  = XABase.OSType('OOs2') #: Descending sort order
        NONE        = XABase.OSType('OOno') #: No sort direction

    class CheckboxState(Enum):
        """Checkbox states.
        """
        CHECKED         = XABase.OSType('OOS2') #: Checkbox checked
        UNCHECKED       = XABase.OSType('OOS0') #: Checkbox unchecked
        NONE            = XABase.OSType('OOno') #: No checkbox state
        INDETERMINATE   = XABase.OSType('OOS1') #: Indeterminate checkbox state

    class ColumnType(Enum):
        """Column types.
        """
        STYLED_TEXT     = XABase.OSType('Oct0')
        CHECKBOX        = XABase.OSType('Oct1')
        DATETIME        = XABase.OSType('Oct2')
        DURATION        = XABase.OSType('Oct3')
        POPUP           = XABase.OSType('Oct4')
        NUMERIC         = XABase.OSType('Oct5')

    class ColumnSummaryType(Enum):
        """Column summary types.
        """
        NONE        = XABase.OSType('OOno')
        HIDDEN      = XABase.OSType('Osm1')
        CALCULATED  = XABase.OSType('Osm2')
        TOTAL       = XABase.OSType('Osm3')
        MAXIMUM     = XABase.OSType('Osm4')
        MINIMUM     = XABase.OSType('Osm5')
        AVERAGE     = XABase.OSType('Osm6')

    class Alignment(Enum):
        """Text alignment types.
        """
        CENTER      = XABase.OSType('OTa1')
        JUSTIFIED   = XABase.OSType('OTa3')
        LEFT        = XABase.OSType('OTa0')
        NATURAL     = XABase.OSType('OTa4')
        RIGHT       = XABase.OSType('OTa2')

    class FormatStyle(Enum):
        """Format styles.
        """
        SHORT   = XABase.OSType('OOFS')
        MEDIUM  = XABase.OSType('OOFM')
        LONG    = XABase.OSType('OOFL')
        FULL    = XABase.OSType('OOFF')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAOmniOutlinerWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether OmniOutliner is the active application
        self.version: str #: The version of OmniOutliner.app
        self.build_number: str #: The build number of the application, for example 63.1 or 63. Major and minor versions are separated by a dot, so 63.10 comes after 63.1
        self.imported_files_should_store_compressed: bool #: Controls whether OmniOutliner will default imported files to being stored in a compressed format
        self.prompt_on_file_format_upgrade: bool #: Controls whether OmniOutliner will prompt the user when updating a older file format to a newer one

    @property
    def name(self) -> str:
        return self.xa_scel.name

    @property
    def version(self) -> str:
        return self.xa_scel.version

    @property
    def build_number(self) -> str:
        return self.xa_scel.buildNumber()

    @property
    def imported_files_should_store_compressed(self) -> bool:
        return self.xa_scel.importedFilesShouldStoreCompressed()

    @imported_files_should_store_compressed.setter
    def imported_files_should_store_compressed(self, imported_files_should_store_compressed: bool):
        self.set_property("importedFilesShouldStoreCompressed", imported_files_should_store_compressed)

    @property
    def prompt_on_file_format_upgrade(self) -> bool:
        return self.xa_scel.promptOnFileFormatUpgrade()

    @prompt_on_file_format_upgrade.setter
    def prompt_on_file_format_upgrade(self, prompt_on_file_format_upgrade: bool):
        self.set_property("promptOnFileFormatUpgrade", prompt_on_file_format_upgrade)

    def documents(self, filter: dict = None) -> 'XAOmniOutlinerDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.documents(), XAOmniOutlinerDocumentList, filter)

    def preferences(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerPreferenceList':
        """Returns a list of preferences, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.preferences(), XAOmniOutlinerPreferenceList, filter)

    def document_types(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerDocumentTypeList':
        """Returns a list of document types, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.documentTypes(), XAOmniOutlinerDocumentTypeList, filter)

    def readable_document_types(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerReadableDocumentTypeList':
        """Returns a list of readable document types, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.readableDocumentTypes(), XAOmniOutlinerReadableDocumentTypeList, filter)

    def writable_document_types(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerWritableDocumentTypeList':
        """Returns a list of writable document types, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.writableDocumentTypes(), XAOmniOutlinerWritableDocumentTypeList, filter)

    def xsl_transforms(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerXslTransformList':
        """Returns a list of XSL transforms, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.xslTransforms(), XAOmniOutlinerXslTransformList, filter)

    def test(self):
        self.xa_scel.collapseall_()




class XAOmniOutlinerWindow(XABaseScriptable.XASBWindow):
    """A window of OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The title of window
        self.id: int #: The unique identifier of the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window in the form of (top-left-x, top-left-y, width, height)
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window has a minimize button
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window has a zoom button
        self.zoomed: bool #: Whether the window is currently zoomed
        self.document: XAOmniOutlinerDocument #: The document whose contents are currently displayed in the window

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
        self.set_property("miniaturized", miniaturized)

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

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def document(self) -> 'XAOmniOutlinerDocument':
        return self._new_element(self.xa_elem.document(), XAOmniOutlinerDocument)

    @document.setter
    def document(self, document: 'XAOmniOutlinerDocument'):
        self.set_property("document", document.xa_elem)




class XAOmniOutlinerRichTextList(XABase.XATextList):
    """A wrapper around lists of rich texts that employs fast enumeration techniques.

    All properties of rich texts can be called as methods on the wrapped list, returning a list containing each texts's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerRichText)

class XAOmniOutlinerRichText(XABase.XAText, XADeletable):
    """A row object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.style: XAOmniOutlinerStyle #: The style of the text
        self.baseline_offset: float #: Number of pixels shifted above or below the normal baseline
        self.underlined: bool #: Is the first character underlined?
        self.superscript: int #: The superscript level of the text
        self.alignment: XAOmniOutlinerApplication.Alignment #: Alignment of the text

    @property
    def style(self) -> 'XAOmniOutlinerStyle':
        return self._new_element(self.xa_elem.style(), XAOmniOutlinerStyle)

    @style.setter
    def style(self, style: 'XAOmniOutlinerStyle'):
        self.set_property("style", style.xa_elem)

    @property
    def baseline_offset(self) -> float:
        return self.xa_elem.baselineOffset()

    @baseline_offset.setter
    def baseline_offset(self, baseline_offset: float):
        self.set_property("baselineOffset", baseline_offset)

    @property
    def underlined(self) -> bool:
        return self.xa_elem.underlined()

    @underlined.setter
    def underlined(self, underlined: bool):
        self.set_property("underlined", underlined)

    @property
    def superscript(self) -> int:
        return self.xa_elem.superscript()

    @superscript.setter
    def superscript(self, superscript: int):
        self.set_property("superscript", superscript)

    @property
    def alignment(self) -> XAOmniOutlinerApplication.Alignment:
        return XAOmniOutlinerApplication.Alignment(self.xa_elem.alignment())

    @alignment.setter
    def alignment(self, alignment: XAOmniOutlinerApplication.Alignment):
        self.set_property("alignment", alignment.value)

    def bold(self):
        """Bolds the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.bold()

    def italicize(self):
        """Italicizes the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.italicize()

    def unbold(self):
        """Unbolds the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.unbold()

    def underline(self):
        """Underlines the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.underline()

    def unitalicize(self):
        """Unitalicizes the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.unitalicize()

    def ununderline(self):
        """Ununderlines the text.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.ununderline()

    def replace(self, replacement: str, regex_to_find: Union[str, None] = None, string_to_find: Union[str, None] = None):
        """Replaces the text.

        :param replacement: The replacement strng
        :type replacement: str
        :param regex_to_find: Regular expression to find and replace, defaults to None
        :type regex_to_find: Union[str, None], optional
        :param string_to_find: String to find and replace, defaults to None
        :type string_to_find: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.replaceMatchingRegularExpression_replacement_string_(regex_to_find, replacement, string_to_find)

    def file_attachments(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerFileAttachmentList':
        """Returns a list of file attachments, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.fileAttachments(), XAOmniOutlinerFileAttachmentList, filter)




class XAOmniOutlinerFileAttachmentList(XABase.XATextList):
    """A wrapper around lists of file attachments that employs fast enumeration techniques.

    All properties of file attachments can be called as methods on the wrapped list, returning a list containing attachments texts's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerFileAttachment)

class XAOmniOutlinerFileAttachment(XABase.XAText):
    """A file attachment object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.file_name: str #: The path to the file for the attachment, if the attachment resides outside the document
        self.embdedded: bool #: If true, the attached file will reside inside the document on the next save

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName()

    @property
    def embdedded(self) -> bool:
        return self.xa_elem.embedded()




class XAOmniOutlinerDocumentList(XABase.XAList):
    """A wrapper around lists of OmniOutliner documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerDocument, filter)

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def alternate_color(self) -> list[XABase.XAColor]:
        """Gets the alternate row color of each document in the list.

        :return: A list of document alternate row colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("alternateColor")
        return [XABase.XAColor(x) for x in ls]

    def background_color(self) -> list[XABase.XAColor]:
        """Gets the background color of each document in the list.

        :return: A list of document background colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor")
        return [XABase.XAColor(x) for x in ls]

    def canredo(self) -> list[bool]:
        """Gets the redo status of each document in the list.

        :return: A list of redo status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("canredo") or [])

    def canundo(self) -> list[bool]:
        """Gets the undo status of each document in the list.

        :return: A list of undo status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("canundo") or [])

    def children_are_sections(self) -> list[bool]:
        """Gets the children are sections status of each document in the list.

        :return: A list of child are sections status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("childrenAreSections") or [])

    def column_title_style(self) -> 'XAOmniOutlinerStyleList':
        """Gets the column title style of each document in the list.

        :return: A list of column title styles
        :rtype: XAOmniOutlinerStyleList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("columnTitleStyle")
        return self._new_element(ls, XAOmniOutlinerStyleList)

    def editable(self) -> list[bool]:
        """Gets the editable status of each document in the list.

        :return: A list of editable status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("editable") or [])

    def folded_editing_enabled(self) -> list[bool]:
        """Gets the folded editing enabled status of each document in the list.

        :return: A list of folded editing enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("foldedEditingEnabled") or [])

    def has_subtopics(self) -> list[bool]:
        """Gets the has subtopics of each document in the list.

        :return: A list of has subtopics status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hasSubtopics") or [])

    def horizontal_grid_color(self) -> list[XABase.XAColor]:
        """Gets the horizontal grid color of each document in the list.

        :return: A list of horizontal grid colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("horizontalGridColor")
        return [XABase.XAColor(x) for x in ls]

    def id(self) -> list[str]:
        """Gets the ID of each document in the list.

        :return: A list of document IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def note_column(self) -> 'XAOmniOutlinerColumnList':
        """Gets the note column of each document in the list.

        :return: A list of document note columns
        :rtype: XAOmniOutlinerColumnList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("noteColumn")
        return self._new_element(ls, XAOmniOutlinerColumnList)

    def note_display(self) -> list[XAOmniOutlinerApplication.DisplayType]:
        """Gets the note display type of each document in the list.

        :return: A list of document note display types
        :rtype: list[XAOmniOutlinerApplication.DisplayType]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("noteDisplay")
        return [XAOmniOutlinerApplication.DisplayType(XABase.OSType(x.stringValue())) for x in ls]

    def save_identifier(self) -> list[str]:
        """Gets the save identifier of each document in the list.

        :return: A list of document save identifiers
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("saveIdentifier") or [])

    def save_identifier_enabled(self) -> list[bool]:
        """Gets the save identifier enabled status of each document in the list.

        :return: A list of saved identifier enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("saveIdentifierEnabled") or [])

    def sorting_postponed(self) -> list[bool]:
        """Gets the sorting postponed status of each document in the list.

        :return: A list of sort postponed status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortingPostponed") or [])

    def status_sort_order(self) -> list[XAOmniOutlinerApplication.SortOrder]:
        """Gets the status sort order direction of each document in the list.

        :return: A list of status sort order directions
        :rtype: list[XAOmniOutlinerApplication.SortOrder]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("statusSortOrder")
        return [XAOmniOutlinerApplication.SortOrder(XABase.OSType(x.stringValue())) for x in ls]

    def status_visible(self) -> list[bool]:
        """Gets the status visible status of each document in the list.

        :return: A list of status visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("statusVisible") or [])

    def store_compressed(self) -> list[bool]:
        """Gets the store compressed status of each document in the list.

        :return: A list of store compressed status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("storeCompressed") or [])

    def style(self) -> 'XAOmniOutlinerStyleList':
        """Gets the style of each document in the list.

        :return: A list of document styles
        :rtype: XAOmniOutlinerStyleList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("style")
        return self._new_element(ls, XAOmniOutlinerStyleList)

    def title(self) -> list[str]:
        """Gets the title of each document in the list.

        :return: A list of document titles
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def topic_column(self) -> 'XAOmniOutlinerColumnList':
        """Gets the topic column of each document in the list.

        :return: A list of document topic columns
        :rtype: XAOmniOutlinerColumnList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("topicColumn")
        return self._new_element(ls, XAOmniOutlinerColumnList)

    def undo_enabled(self) -> list[bool]:
        """Gets the undo enabled status of each document in the list.

        :return: A list of document undo enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("undoEnabled") or [])

    def verticalGridColor(self) -> list[XABase.XAColor]:
        """Gets the vertical grid color of each document in the list.

        :return: A list of vertical grid colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("verticalGridColor")
        return [XABase.XAColor(x) for x in ls]

    def visible(self) -> list[bool]:
        """Gets the visible status of each document in the list.

        :return: A list of document visible status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def writes_wrapper(self) -> list[bool]:
        """Gets the writes wrapper of each document in the list.

        :return: A list of document writes wrapper status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("writesWrapper") or [])

    def topiccolumnid(self) -> list[str]:
        """Gets the topic column ID of each document in the list.

        :return: A list of document topic column IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("topiccolumnid") or [])

    def notecolumnid(self) -> list[str]:
        """Gets the note column ID of each document in the list.

        :return: A list of document note column IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("notecolumnid") or [])

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAOmniOutlinerDocument(XABase.XAObject, XACloseable, XAPrintable):
    """A document in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since it was last saved
        self.file: XABase.XAPath #: The location of the file on disk, if it has one
        self.alternate_color: XABase.XAColor #: The background color of every other row
        self.background_color: XABase.XAColor #: The background color of the document
        self.canredo: bool #: Whether the document can redo the most recently undone command
        self.canundo: bool #: Whether the document can undo the most recent command
        self.children_are_sections: bool #: This is always true for documents. This is here to make it easier to deal with mixed lists of rows and documents
        self.column_title_style: XAOmniOutlinerStyle #: The style of column titles
        self.editable: bool #: This lets you know whether the document is editable. For example, the release notes document is not editable, so your script may want to avoid trying to edit it
        self.folded_editing_enabled: bool #: Whether folded editing of item and inline note text is enabled
        self.has_subtopics: bool #: Whether the document has any subtopics
        self.horizontal_grid_color: XABase.XAColor #: The color of hairline dividers between rows
        self.id: str #: An identifier unique to the document
        self.note_column: XAOmniOutlinerColumn #: The column of the document that contains the notes for the rows
        self.note_display: XAOmniOutlinerApplication.DisplayType #: Whether notes are displayed inline
        self.save_identifier: str #: A string that changes each time the document is saved. If the save identifier is disabled, then this returns 'missing value'
        self.save_identifier_enabled: bool #: Controls whether a save identifier will be emitted in the archived document each time the document is saved. This is useful for external tools that need to quickly determine whether the document has changed without relying on the file modification time
        self.sorting_postponed: bool #: Whether sorting is currently postponed for the document
        self.status_sort_order: XAOmniOutlinerApplication.SortOrder #: The sort order used for the status checkbox in the topic column
        self.status_visible: bool #: Whether the status checkbox is visible in the outline column
        self.stored_compressed: bool #: Whether xml should be compressed when saved
        self.style: XAOmniOutlinerStyle #: The default style for the document
        self.title: str #: This is the title of the document
        self.topic_column: XAOmniOutlinerColumn #: The column of the document that displays the hierarchy of rows
        self.undo_enabled: bool #: Controls whether undo is currently enabled in the document. This should be used very carefully. If it is set to 'false', all previously registered undo events will be removed and any further modifications to the document will not record undo operations
        self.vertical_grid_color: XABase.XAColor #: The color hairline dividers between columns
        self.visible: bool #: Whether the interface for the document is visible. Note that miniaturized counts as visible. Mostly this isn't useful to third parties right now
        self.writes_wrapper: bool #: If set to true, this indicates that the document will write itself as a file wrapper (folder)
        self.topiccolumnid: str #: The topic column id for newly created documents
        self.notecolumnid: str #: The note column id for newly created documents

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.file())

    @property
    def alternate_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.alternateColor())

    @alternate_color.setter
    def alternate_color(self, alternate_color: XABase.XAColor):
        self.set_property("alternateColor", alternate_color.xa_elem)

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.alternateColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property("backgroundColor", background_color.xa_elem)

    @property
    def canredo(self) -> bool:
        return self.xa_elem.canredo()

    @property
    def canundo(self) -> bool:
        return self.xa_elem.canundo()

    @property
    def children_are_sections(self) -> bool:
        return self.xa_elem.childrenAreSections()

    @property
    def column_title_style(self) -> 'XAOmniOutlinerStyle':
        return self._new_element(self.xa_elem.columnTitleStyle(), XAOmniOutlinerStyle)

    @column_title_style.setter
    def column_title_style(self, column_title_style: 'XAOmniOutlinerStyle'):
        self.set_property("columnTitleStyle", column_title_style.xa_elem)

    @property
    def editable(self) -> bool:
        return self.xa_elem.editable()

    @property
    def folded_editing_enabled(self) -> bool:
        return self.xa_elem.foldedEditingEnabled()

    @folded_editing_enabled.setter
    def folded_editing_enabled(self, folded_editing_enabled: bool):
        self.set_property("foldedEditingEnabled", folded_editing_enabled)

    @property
    def has_subtopics(self) -> bool:
        return self.xa_elem.hasSubtopics()

    @property
    def horizontal_grid_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.horizontalGridColor())

    @horizontal_grid_color.setter
    def horizontal_grid_color(self, horizontal_grid_color: XABase.XAColor):
        self.set_property("horizontalGridColor", horizontal_grid_color.xa_elem)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def note_column(self) -> 'XAOmniOutlinerColumn':
        return self._new_element(self.xa_elem.noteColumn(), XAOmniOutlinerColumn)

    @property
    def note_display(self) -> XAOmniOutlinerApplication.DisplayType:
        return XAOmniOutlinerApplication.DisplayType(self.xa_elem.noteDisplay())

    @note_display.setter
    def note_display(self, note_display: XAOmniOutlinerApplication.DisplayType):
        self.set_property("noteDisplay", note_display.value)
    
    @property
    def save_identifier(self) -> str:
        return self.xa_elem.saveIdentifier()

    @property
    def save_identifier_enabled(self) -> bool:
        return self.xa_elem.saveIdentifierEnabled()

    @save_identifier_enabled.setter
    def save_identifier_enabled(self, save_identifier_enabled: bool):
        self.set_property("saveIdentifierEnabled", save_identifier_enabled)

    @property
    def sorting_postponed(self) -> bool:
        return self.xa_elem.sortingPostponed()

    @sorting_postponed.setter
    def sorting_postponed(self, sorting_postponed: bool):
        self.set_property("sortingPostponed", sorting_postponed)

    @property
    def status_sort_order(self) -> XAOmniOutlinerApplication.SortOrder:
        return XAOmniOutlinerApplication.SortOrder(self.xa_elem.statusSortOrder())

    @status_sort_order.setter
    def status_sort_order(self, status_sort_order: XAOmniOutlinerApplication.SortOrder):
        self.set_property("statusSortOrder", status_sort_order.value)

    @property
    def status_visible(self) -> bool:
        return self.xa_elem.statusVisible()

    @status_visible.setter
    def status_visible(self, status_visible: bool):
        self.set_property("statusVisible", status_visible)

    @property
    def store_compressed(self) -> bool:
        return self.xa_elem.storeCompressed()

    @store_compressed.setter
    def store_compressed(self, store_compressed: bool):
        self.set_property("storeCompressed", store_compressed)

    @property
    def style(self) -> 'XAOmniOutlinerStyle':
        return self._new_element(self.xa_elem.style(), XAOmniOutlinerStyle)

    @style.setter
    def style(self, style: 'XAOmniOutlinerStyle'):
        self.set_property("style", style.xa_elem)

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property("title", title)

    @property
    def topic_column(self) -> 'XAOmniOutlinerColumn':
        return self._new_element(self.xa_elem.topicColumn(), XAOmniOutlinerColumn)

    @property
    def undo_enabled(self) -> bool:
        return self.xa_elem.undoEnabled()

    @undo_enabled.setter
    def undo_enabled(self, undo_enabled: bool):
        self.set_property("undoEnabled", undo_enabled)

    @property
    def vertical_grid_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.verticalGridColor())

    @vertical_grid_color.setter
    def vertical_grid_color(self, vertical_grid_color: XABase.XAColor):
        self.set_property("verticalGridColor", vertical_grid_color.xa_elem)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def writes_wrapper(self) -> bool:
        return self.xa_elem.writesWrapper()

    @writes_wrapper.setter
    def writes_wrapper(self, writes_wrapper: bool):
        self.set_property("writesWrapper", writes_wrapper)

    @property
    def topiccolumnid(self) -> str:
        return self.xa_elem.topiccolumnid()

    @topiccolumnid.setter
    def topiccolumnid(self, topiccolumnid: str):
        self.set_property("topiccolumnid", topiccolumnid)

    @property
    def notescolumnid(self) -> str:
        return self.xa_elem.notescolumndid()

    @notescolumnid.setter
    def notescolumnid(self, notescolumnid: str):
        self.set_property("notescolumnid", notescolumnid)

    def undo(self):
        """Undoes the most recent change.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.undo()

    def redo(self):
        """Redoes the most recent undo operation.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.redo()

    def select(self, items: Union[XABase.XAObject, list[XABase.XAObject], None] = None, extend: bool = False):
        """Selects one or more objects.

        :param items: An object or list of objects to select
        :type items: Union[XABase.XAObject, list[XABase.XAObject], None]
        :param extend: Whether the selection is replaced or extended, defaults to False
        :type extend: bool, optional

        .. versionadded:: 0.0.9
        """
        if items is None:
            # Select this document
            self.xa_elem.selectExtending_(extend)
        elif isinstance(items, XABase.XAObject):
            # Select one object (can be an XAList)
            self.xa_elem.select_extending_(items.xa_elem, extend)
        elif isinstance(items, list):
            # Select a list of items
            items = [x.xa_elem for x in items]
            self.xa_elem.select_extending_(items, extend)

    def add(self, items: Union[XABase.XAObject, list[XABase.XAObject]]):
        """Adds objects to the document.

        :param items: The object(s) to add
        :type items: Union[XABase.XAObject, list[XABase.XAObject]]

        .. versionadded:: 0.0.9
        """
        if isinstance(items, list):
            items = [x.xa_elem for x in items]
        self.xa_elem.add_to_(items, self.xa_elem)

    def add_to(self, destination: XABase.XAObject):
        """Adds the document to a location.

        :param destination: The container to which to add the document 
        :type destination: XABase.XAObject

        .. versionadded:: 0.0.9
        """
        self.xa_elem.addTo_(destination.xa_elem)

    def remove(self, items: Union[XABase.XAObject, list[XABase.XAObject]]):
        """Remove objects from the document.

        :param items: The object(s) to remove
        :type items: Union[XABase.XAObject, list[XABase.XAObject]]

        .. versionadded:: 0.0.9
        """
        if isinstance(items, list):
            items = [x.xa_elem for x in items]
        self.xa_elem.remove_from_(items, self.xa_elem)

    def remove_from(self, container: XABase.XAObject):
        """Adds the document to a location.

        :param container: The container from which to remove the document 
        :type container: XABase.XAObject

        .. versionadded:: 0.0.9
        """
        self.xa_elem.removeFrom_(container.xa_elem)

    def expand_all(self, items: Union['XAOmniOutlinerDocument', 'XAOmniOutlinerRow', XAOmniOutlinerDocumentList, 'XAOmniOutlinerRowList', list['XAOmniOutlinerDocument'], list['XAOmniOutlinerRow'], None] = None):
        """Expand the entire outline of an object.

        .. versionadded:: 0.0.9
        """
        if items is None:
            # Expand the entire document
            self.xa_elem.expandAll()
        elif isinstance(items, list):
            # Expand a list of items
            items = [x.xa_elem for x in items]
            self.xa_elem.expandAll_(items)
        else:
            # Expand an XAList of items
            self.xa_elem.expandAll_(items.xa_elem)

    def collapse_all(self, items: Union['XAOmniOutlinerDocument', 'XAOmniOutlinerRow', XAOmniOutlinerDocumentList, 'XAOmniOutlinerRowList', list['XAOmniOutlinerDocument'], list['XAOmniOutlinerRow'], None] = None):
        """Collapse the entire outline of an object.

        .. versionadded:: 0.0.9
        """
        if items is None:
            # Collapse the entire document
            self.xa_elem.collapseAll()
        elif isinstance(items, list):
            # Collapse a list of items
            items = [x.xa_elem for x in items]
            self.xa_elem.collapseAll_(items)
        else:
            # Collapse an XAObject, which can be an XAList
            self.xa_elem.collapseAll_(items.xa_elem)

    def group(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Increase the outline level of a list of rows by creating a new parent row for them and moving under that new row.

        :param rows: The rows to group, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Group the entire document
            self.xa_elem.group()
        elif isinstance(rows, list):
            # Group a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.group_(rows)
        else:
            # Group an XAObject, which can be an XAList
            self.xa_elem.group_(rows.xa_elem)

    def ungroup(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Decrease the outline level of all children of a row, moving them left one step.

        :param rows: The rows to ungroup, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Ungroup the entire document
            self.xa_elem.ungroup()
        elif isinstance(rows, list):
            # Ungroup a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.ungroup_(rows)
        else:
            # Ungroup an XAObject, which can be an XAList
            self.xa_elem.ungroup_(rows.xa_elem)

    def hoist(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Hide all rows in the outline, except for the descendants of the row passed to this command.

        :param rows: The rows to hoist, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Hoist the entire document
            self.xa_elem.hoist()
        elif isinstance(rows, list):
            # Hoist a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.hoist_(rows)
        else:
            # Hoist an XAObject, which can be an XAList
            self.xa_elem.hoist_(rows.xa_elem)

    def unhoist(self, documents: Union['XAOmniOutlinerDocument', XAOmniOutlinerDocumentList, list['XAOmniOutlinerDocument'], None] = None, unhoist_all: bool = False):
        """Show rows hidden in the last hoist operation on a document.

        :param documents: The documents to unhoist, defaults to None
        :type documents: Union[XAOmniOutlinerDocument, XAOmniOutlinerDocumentList, list[XAOmniOutlinerDocument], None], optional
        :param unhoist_all: Reverse just the last Hoist operation on the outline, or show items hidden by all previous Hoist operations, defaults to False
        :type unhoist_all: bool, optional

        .. versionadded:: 0.0.9
        """
        if documents is None:
            # Unhoist the current document
            self.xa_elem.unhoistUnhoistingAll_(unhoist_all)
        elif isinstance(documents, list):
            # Unhoist a list of documents
            documents = [x.xa_elem for x in documents]
            self.xa_elem.unhoist_unhoistingAll_(documents, unhoist_all)
        else:
            # Unhoist an XAObject, which can be an XAList
            self.xa_elem.unhoist_unhoistingAll_(documents, unhoist_all)

    def pbcopy(self, items: list[XABase.XAObject], type: Union[str, list[str], None] = None, clipboard_name: Union[str, None] = None):
        """Copies one or more nodes to the clipboard.

        :param items: The list of items to copy to the clipboard
        :type items: list[XABase.XAObject]
        :param type: The list of type identifier to use when copying the trees. If omitted, all writable clipboard types are used, defaults to None
        :type type: Union[str, list[str], None], optional
        :param clipboard_name: The name of the clipboard to copy to, defaults to None
        :type clipboard_name: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.pbcopyItems_as_to_(items, type, clipboard_name)

    def pbpaste(self, location: XABase.XAObject, clipboard_name: Union[str, None] = None):
        """Pastes nodes from the clipboard.

        :param location: The location at which to paste the nodes
        :type location: XABase.XAObject
        :param clipboard_name: The name of the clipboard to paste from, defaults to None
        :type clipboard_name: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.pbpasteAt_from_(location, clipboard_name)

    def export(self, file: Union[str, XABase.XAPath], type: Union[str, None] = None):
        """Exports the document to the specified location and file type. Unlike the "save" command, this will never set the name of the document or change its modified flag.

        :param file: Where to place the exported document
        :type file: Union[str, XABase.XAPath]
        :param type: The name of a writable file type to use when writing the document. Defaults to the appropriate type for the path extension on the export destination, defaults to None
        :type type: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        if isinstance(file, str):
            file = XABase.XAPath(file)
        self.xa_elem.exportTo_as_(file.xa_elem, type)

    def selected_columns(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerSelectedColumnList':
        """Returns a list of selected columns, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.selectedColumns(), XAOmniOutlinerSelectedColumnList, filter)

    def sections(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerSectionList':
        """Returns a list of sections, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.sections(), XAOmniOutlinerSectionList, filter)

    def selected_rows(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerSelectedRowList':
        """Returns a list of selected rows, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.selectedRows(), XAOmniOutlinerSelectedRowList, filter)

    def children(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerChildList':
        """Returns a list of children, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.children(), XAOmniOutlinerChildList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.columns(), XAOmniOutlinerColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.rows(), XAOmniOutlinerRowList, filter)

    def leaves(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerLeafList':
        """Returns a list of leaves, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.leaves(), XAOmniOutlinerLeafList, filter)

    def level_styles(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerLevelStyleList':
        """Returns a list of level styles, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.levelStyles(), XAOmniOutlinerLevelStyleList, filter)

    def named_styles(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerNamedStyleList':
        """Returns a list of named styles, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.namedStyles(), XAOmniOutlinerNamedStyleList, filter)




class XAOmniOutlinerDocumentTypeList(XABase.XAList):
    """A wrapper around lists of document types that employs fast enumeration techniques.

    All properties of document types can be called as methods on the wrapped list, returning a list containing each types's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAOmniOutlinerDocumentType
        super().__init__(properties, obj_class, filter)

class XAOmniOutlinerDocumentType(XABase.XAObject):
    """A document type in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.uti: str #: The Uniform Type Identifier for this document type
        self.display_name: str #: A user-presentable display name for this document type
        self.file_extensions: list[str] #: File extensions for this document type

    @property
    def uti(self) -> str:
        return self.xa_elem.uti()

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def file_extensions(self) -> list[str]:
        return self.xa_elem.fileExtensions()




class XAOmniOutlinerReadableDocumentTypeList(XAOmniOutlinerDocumentTypeList):
    """A wrapper around lists of readable document types that employs fast enumeration techniques.

    All properties of document types can be called as methods on the wrapped list, returning a list containing each types's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerReadableDocumentType)

class XAOmniOutlinerReadableDocumentType(XAOmniOutlinerDocumentType):
    """A readable document type in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerWritableDocumentTypeList(XAOmniOutlinerDocumentTypeList):
    """A wrapper around lists of writable document types that employs fast enumeration techniques.

    All properties of document types can be called as methods on the wrapped list, returning a list containing each types's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerReadableDocumentType)

class XAOmniOutlinerWritableDocumentType(XAOmniOutlinerDocumentType):
    """A writable document type in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerEnumerationList(XABase.XAList):
    """A wrapper around lists of enumerations that employs fast enumeration techniques.

    All properties of enumerations can be called as methods on the wrapped list, returning a list containing each enumeration's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerEnumeration, filter)

class XAOmniOutlinerEnumeration(XABase.XAObject):
    """An enumeration in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: An identifier for the enumeration that is unique within the column
        self.index: int #: The index of the enumeration member int he column
        self.name: str #: The name of the enumeration

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def index(self) -> str:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    def move_to(self, destination: 'XAOmniOutlinerColumn'):
        """Moves the enumeration to a new column.

        :param destination: The column to move the enumeration to
        :type destination: XAOmniOutlinerColumn

        .. versionadded:: 0.0.9
        """
        self.xa_elem.moveTo_(destination.xa_elem)




class XAOmniOutlinerColumnList(XABase.XAList):
    """A wrapper around lists of OmniOutliner columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAOmniOutlinerColumn
        super().__init__(properties, obj_class, filter)

class XAOmniOutlinerColumn(XABase.XAObject):
    """A column in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.alignment: XAOmniOutlinerApplication.Alignment #: Default alignment for cells of the column
        self.background_color: XABase.XAColor #: The background color of the column
        self.column_style: XAOmniOutlinerStyle #: The style of the column. This is used as the default style for values in the column (but is overriden by any style attributes defined on rows)
        self.document: XAOmniOutlinerDocument #: The document containing the column
        self.column_format: XAOmniOutlinerColumFormat #: All aspects of the column's format
        self.format_string: str #: The format string for formatted columns. Depends on the type of the column
        self.id: str #: An identifier for the column that is unique within the document
        self.index: int #: The index of the column in the document. This includes hidden columns
        self.name: str #: The name of the column. This is currently the same as the title, but in the future the title may be styled while the name will always be a plain string
        self.sort_order: XAOmniOutlinerApplication.SortOrder #: The sort order of the column
        self.summary_type: XAOmniOutlinerApplication.ColumnSummaryType #: This is the summary type of the column
        self.title: str #: The title of the column
        self.column_type: XAOmniOutlinerApplication.ColumnType #: This is the type of the column
        self.width: int #: The width of the column in pixels
        self.visible: bool #: Whether the column is visible or not

    @property
    def alignment(self) -> XAOmniOutlinerApplication.Alignment:
        return XAOmniOutlinerApplication.Alignment(self.xa_elem.alignment())

    @alignment.setter
    def alignment(self, alignment: XAOmniOutlinerApplication.Alignment):
        self.set_property("alignment", alignment.value)

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property("backgroundColor", background_color.xa_elem)

    @property
    def column_style(self) -> 'XAOmniOutlinerStyle':
        return self._new_element(self.xa_elem.columnStyle(), XAOmniOutlinerStyle)

    @column_style.setter
    def column_style(self, column_style: 'XAOmniOutlinerStyle'):
        self.set_property("columnStyle", column_style.xa_elem)

    @property
    def document(self) -> XAOmniOutlinerDocument:
        return self._new_element(self.xa_elem.document(), XAOmniOutlinerDocument)

    @document.setter
    def document(self, document: XAOmniOutlinerDocument):
        self.set_property("document", document.xa_elem)

    @property
    def column_format(self) -> 'XAOmniOutlinerColumFormat':
        return self._new_element(self.xa_elem.columnFormat(), XAOmniOutlinerColumFormat)

    @column_format.setter
    def column_format(self, column_format: 'XAOmniOutlinerColumFormat'):
        self.set_property("columnFormat", column_format.xa_elem)

    @property
    def format_string(self) -> str:
        return self.xa_elem.formatString()

    @format_string.setter
    def format_string(self, format_string: str):
        self.set_property("formatString", format_string)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def sort_order(self) -> XAOmniOutlinerApplication.SortOrder:
        return XAOmniOutlinerApplication.SortOrder(self.xa_elem.sortOrder())

    @sort_order.setter
    def sort_order(self, sort_order: XAOmniOutlinerApplication.SortOrder):
        self.set_property("sortOrder", sort_order.value)

    @property
    def summary_type(self) -> XAOmniOutlinerApplication.ColumnSummaryType:
        return XAOmniOutlinerApplication.SortOrder(self.xa_elem.summaryType())

    @summary_type.setter
    def summary_type(self, summary_type: XAOmniOutlinerApplication.ColumnSummaryType):
        self.set_property("summaryType", summary_type.value)

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property("title", title)
    
    @property
    def column_type(self) -> XAOmniOutlinerApplication.ColumnType:
        return XAOmniOutlinerApplication.ColumnType(self.xa_elem.columnType())

    @column_type.setter
    def column_type(self, column_type: XAOmniOutlinerApplication.ColumnType):
        self.set_property("columnType", column_type.value)

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property("width", width)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    def move_to(self, destination: XAOmniOutlinerDocument):
        """Moves the column to the specified document.

        :param destination: The document to move the column to
        :type destination: XAOmniOutlinerDocument

        .. versionadded:: 0.0.9
        """
        self.xa_elem.moveTo_(destination.xa_elem)

    def enumerations(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerEnumerationList':
        """Returns a list of enumerations, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.enumerations(), XAOmniOutlinerEnumerationList, filter)




class XAOmniOutlinerSelectedColumnList(XAOmniOutlinerColumnList):
    """A wrapper around lists of selected columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerSelectedColumn)

class XAOmniOutlinerSelectedColumn(XABase.XAObject):
    """A style object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerColumFormat(XABase.XAObject):
    """A column format in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.format: str #: The ICU format string
        self.id: str #: The identifier for built-in formats
        self.calendar: str #: The calendar to use for date formats
        self.locale: str #: The locale identifier (such as "en_US" or "ja_JP") for formats
        self.timezone: str #: The time zone to use for date formats
        self.date_style: XAOmniOutlinerApplication.FormatStyle #: The style of date format to use, based off the user's preference
        self.time_style: XAOmniOutlinerApplication.FormatStyle #: The style of date format to use, based off the user's preference
        self.currency: str #: The ISO currency identifier (such as "USD" or "JPY") for columns with a currency format. Must be used with an id of "currency

    @property
    def format(self) -> str:
        return self.xa_elem.format()

    @format.setter
    def format(self, format: str):
        self.set_property("format", format)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def calendar(self) -> str:
        return self.xa_elem.calendar()

    @calendar.setter
    def calendar(self, calendar: str):
        self.set_property("calendar", calendar)

    @property
    def locale(self) -> str:
        return self.xa_elem.locale()

    @locale.setter
    def locale(self, locale: str):
        self.set_property("locale", locale)

    @property
    def timezone(self) -> str:
        return self.xa_elem.timezone()

    @timezone.setter
    def timezone(self, timezone: str):
        self.set_property("timezone", timezone)

    @property
    def date_style(self) -> XAOmniOutlinerApplication.FormatStyle:
        return XAOmniOutlinerApplication.FormatStyle(self.xa_elem.dateStyle())

    @date_style.setter
    def date_style(self, date_style: XAOmniOutlinerApplication.FormatStyle):
        self.set_property("dateStyle", date_style.value)    

    @property
    def time_style(self) -> XAOmniOutlinerApplication.FormatStyle:
        return XAOmniOutlinerApplication.FormatStyle(self.xa_elem.timeStyle())

    @time_style.setter
    def time_style(self, time_style: XAOmniOutlinerApplication.FormatStyle):
        self.set_property("timeStyle", time_style.value)

    @property
    def currency(self):
        return self.xa_elem.currency()

    @currency.setter
    def currency(self, currency: str):
        self.set_property("currency", currency)




class XAOmniOutlinerRowList(XABase.XAList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAOmniOutlinerRow
        super().__init__(properties, obj_class, filter)

class XAOmniOutlinerRow(XABase.XAObject):
    """A row object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.children_are_sections: bool #: Whether the row's children are treated as separate sections
        self.document: XAOmniOutlinerDocument #: The document containing the row
        self.expanded: bool #: Whether the row's subtopics are visible
        self.has_subtopics: bool #: Whether the row has any subtopics
        self.id: str #: An identifier for the row that is unique within the document
        self.name: str #: The name of the row (just a plain string version of the topic)
        self.index: int #: The index of the row among its siblings
        self.level: int #: How 'deep' this item is. Top-level rows are level 1, subtopics of those rows are level 2, and so on
        self.note: XAOmniOutlinerRichText #: Contents of the note column
        self.note_cell: XAOmniOutlinerCell #: The cell for the note column in the row
        self.note_expanded: bool #: Whether inline note is currently displayed
        self.parent: XAOmniOutlinerRow #: The row that contains this row
        self.selected: bool #: This is true if the row is selected. Note that attempts to set this while the row is not visible (collapsed parent, hoisted root isn't an ancestor, etc.) will silently do nothing
        self.state: XAOmniOutlinerApplication.CheckboxState #: The state of the check box for this row
        self.style: XAOmniOutlinerStyle #: The style of the row
        self.topic: XAOmniOutlinerRichText #: Contents of the outline column
        self.topic_cell: XAOmniOutlinerCell #: The cell for the topic column in the row
        self.visible: bool #: Whether this row is in the outline view. It must be a descendent of the current root item taking hoisting into account, with no collapsed ancestors below the current root. Hoisted rows are visible in the outline and so are considered visible
    
    @property
    def children_are_sections(self) -> bool:
        return self.xa_elem.childrenAreSections()

    @children_are_sections.setter
    def children_are_sections(self, children_are_sections: bool):
        self.set_property("childrenAreSections", children_are_sections)

    @property
    def document(self) -> XAOmniOutlinerDocument:
        return self._new_element(self.xa_elem.document(), XAOmniOutlinerDocument)

    @property
    def expanded(self) -> bool:
        return self.xa_elem.expanded()

    @expanded.setter
    def expanded(self, expanded: bool):
        self.set_property("expanded", expanded)

    @property
    def has_subtopics(self) -> bool:
        return self.xa_elem.hasSubtopics()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def level(self) -> int:
        return self.xa_elem.level()

    @property
    def note(self) -> XAOmniOutlinerRichText:
        return self._new_element(self.xa_elem.note(), XAOmniOutlinerRichText)

    @note.setter
    def note(self, note: XAOmniOutlinerRichText):
        self.set_property("note", note.xa_elem)

    @property
    def note_cell(self) -> 'XAOmniOutlinerCell':
        return self._new_element(self.xa_elem.noteCell(), XAOmniOutlinerCell)

    @note_cell.setter
    def note_cell(self, note_cell: 'XAOmniOutlinerCell'):
        self.set_property("noteCell", note_cell.xa_elem)

    @property
    def note_expanded(self) -> bool:
        return self.xa_elem.noteExpanded()

    @note_expanded.setter
    def note_expanded(self, note_expanded: bool):
        self.set_property("noteExpanded", note_expanded)

    @property
    def parent(self) -> 'XAOmniOutlinerRow':
        return self._new_element(self.xa_elem.parent(), XAOmniOutlinerRow)

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property("selected", selected)

    @property
    def state(self) -> XAOmniOutlinerApplication.CheckboxState:
        return XAOmniOutlinerApplication.CheckboxState(self.xa_elem.state())

    @state.setter
    def state(self, state: XAOmniOutlinerApplication.CheckboxState):
        self.set_property("state", state.value)

    @property
    def style(self) -> 'XAOmniOutlinerStyle':
        return self._new_element(self.xa_elem.style(), XAOmniOutlinerStyle)

    @style.setter
    def style(self, style: 'XAOmniOutlinerStyle'):
        self.set_property("style", style.xa_elem)

    @property
    def topic(self) -> XAOmniOutlinerRichText:
        return self._new_element(self.xa_elem.topic(), XAOmniOutlinerRichText)

    @topic.setter
    def topic(self, topic: XAOmniOutlinerRichText):
        self.set_property("topic", topic.xa_elem)

    @property
    def topic_cell(self) -> 'XAOmniOutlinerCell':
        return self._new_element(self.xa_elem.topicCell(), XAOmniOutlinerCell)

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    def expand_all(self, items: Union['XAOmniOutlinerRow', list['XAOmniOutlinerRow'], XAOmniOutlinerRowList, None] = None):
        """Expands a row or list of rows.

        :param items: The row(s) to expand, defaults to None
        :type items: Union[XAOmniOutlinerRow, list[XAOmniOutlinerRow], XAOmniOutlinerRowList, None], optional

        .. versionadded:: 0.0.9
        """
        if items is None:
            # Expand all items in the row
            self.xa_elem.expandAll()
        elif isinstance(items, list):
            # Expand a list of rows
            items = [x.xa_elem for x in items]
        self.xa_elem.expandAll_(items)

    def collapse_all(self, items: Union['XAOmniOutlinerRow', list['XAOmniOutlinerRow'], XAOmniOutlinerRowList, None] = None):
        """Collapses a row or list of rows.

        :param items: The row(s) to collapse, defaults to None
        :type items: Union[XAOmniOutlinerRow, list[XAOmniOutlinerRow], XAOmniOutlinerRowList, None], optional

        .. versionadded:: 0.0.9
        """
        if items is None:
            # Collapse all items in the row
            self.xa_elem.collapseAll()
        elif isinstance(items, list):
            # Collapse a list of rows
            items = [x.xa_elem for x in items]
        self.xa_elem.collapseAll_(items)

    def indent(self):
        """Indents the row.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.indent()

    def outdent(self):
        """Outdents the row.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.outdent()

    def add(self, items: Union[XABase.XAObject, list[XABase.XAObject]]):
        """Adds objects to the row.

        :param items: The object(s) to add
        :type items: Union[XABase.XAObject, list[XABase.XAObject]]

        .. versionadded:: 0.0.9
        """
        if isinstance(items, list):
            items = [x.xa_elem for x in items]
        self.xa_elem.add_to_(items, self.xa_elem)

    def add_to(self, destination: XABase.XAObject):
        """Adds the row to a location.

        :param destination: The container to which to add the row 
        :type destination: XABase.XAObject

        .. versionadded:: 0.0.9
        """
        self.xa_elem.addTo_(destination.xa_elem)

    def remove(self, items: Union[XABase.XAObject, list[XABase.XAObject]]):
        """Remove objects from the row.

        :param items: The object(s) to remove
        :type items: Union[XABase.XAObject, list[XABase.XAObject]]

        .. versionadded:: 0.0.9
        """
        if isinstance(items, list):
            items = [x.xa_elem for x in items]
        self.xa_elem.remove_from_(items, self.xa_elem)

    def remove_from(self, container: XABase.XAObject):
        """Removes the row from a location.

        :param container: The container from which to remove the row 
        :type container: XABase.XAObject

        .. versionadded:: 0.0.9
        """
        self.xa_elem.removeFrom_(container.xa_elem)

    def group(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Increase the outline level of a list of rows by creating a new parent row for them and moving under that new row.

        :param rows: The rows to group, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Group the entire row
            self.xa_elem.group()
        elif isinstance(rows, list):
            # Group a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.group_(rows)
        else:
            # Group an XAObject, which can be an XAList
            self.xa_elem.group_(rows.xa_elem)

    def ungroup(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Decrease the outline level of all children of a row, moving them left one step.

        :param rows: The rows to ungroup, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Ungroup the entire row
            self.xa_elem.ungroup()
        elif isinstance(rows, list):
            # Ungroup a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.ungroup_(rows)
        else:
            # Ungroup an XAObject, which can be an XAList
            self.xa_elem.ungroup_(rows.xa_elem)

    def hoist(self, rows: Union['XAOmniOutlinerRow', 'XAOmniOutlinerRowList', list['XAOmniOutlinerRow'], None] = None):
        """Hide all rows in the outline, except for the descendants of the row passed to this command.

        :param rows: The rows to hoist, defaults to None
        :type rows: Union[XAOmniOutlinerRow, XAOmniOutlinerRowList, list[XAOmniOutlinerRow], None], optional

        .. versionadded:: 0.0.9
        """
        if rows is None:
            # Hoist the entire row
            self.xa_elem.hoist()
        elif isinstance(rows, list):
            # Hoist a list of rows
            rows = [x.xa_elem for x in rows]
            self.xa_elem.hoist_(rows)
        else:
            # Hoist an XAObject, which can be an XAList
            self.xa_elem.hoist_(rows.xa_elem)

    def pbcopy(self, items: list[XABase.XAObject], type: Union[str, list[str], None] = None, clipboard_name: Union[str, None] = None):
        """Copies one or more nodes to the clipboard.

        :param items: The list of items to copy to the clipboard
        :type items: list[XABase.XAObject]
        :param type: The list of type identifier to use when copying the trees. If omitted, all writable clipboard types are used, defaults to None
        :type type: Union[str, list[str], None], optional
        :param clipboard_name: The name of the clipboard to copy to, defaults to None
        :type clipboard_name: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.pbcopyItems_as_to_(items, type, clipboard_name)

    def pbpaste(self, location: XABase.XAObject, clipboard_name: Union[str, None] = None):
        """Pastes nodes from the clipboard.

        :param location: The location at which to paste the nodes
        :type location: XABase.XAObject
        :param clipboard_name: The name of the clipboard to paste from, defaults to None
        :type clipboard_name: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.pbpasteAt_from_(location, clipboard_name)

    def import_file(self, file: Union[str, XABase.XAPath]):
        """Imports a file, as rows, to a specified location. Returns the list of imported rows.

        :param file: The file to import
        :type file: Union[str, XABase.XAPath]

        .. versionadded:: 0.0.9
        """
        if isinstance(file, str):
            file = XABase.XAPath(file)
        self.xa_elem.import_to_(file.xa_elem, self.xa_elem)

    def ancestors(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerAncestorList':
        """Returns a list of ancestors, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.ancestors(), XAOmniOutlinerAncestorList, filter)

    def cells(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.cells(), XAOmniOutlinerCellList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.rows(), XAOmniOutlinerRowList, filter)

    def children(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerChildList':
        """Returns a list of children, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.children(), XAOmniOutlinerChildList, filter)

    def conduit_setting_domains(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerConduitSettingDomainList':
        """Returns a list of conduit setting domains, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.conduitSettingDomains(), XAOmniOutlinerConduitSettingDomainList, filter)

    def following_siblings(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerFollowingSiblingList':
        """Returns a list of following siblings, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.followingSiblings(), XAOmniOutlinerFollowingSiblingList, filter)

    def leaves(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerLeafList':
        """Returns a list of leaves, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.leaves(), XAOmniOutlinerLeafList, filter)

    def paragraphs(self, filter: Union[dict, None] = None) -> 'XABase.XAParagraphList':
        """Returns a list of paragraphs, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.paragraphs(), XABase.XAParagraphList, filter)

    def rowpath(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerPathComponentList':
        """Returns a row path, or list of path components as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.rowpath(), XAOmniOutlinerPathComponentList, filter)

    def preceding_siblings(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerPrecedingSiblingList':
        """Returns a list of preceding siblings, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.precedingSiblings(), XAOmniOutlinerPrecedingSiblingList, filter)

    def sections(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerSectionList':
        """Returns a list of sections, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.sections(), XAOmniOutlinerSectionList, filter)

    def selected_rows(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerSelectedRowList':
        """Returns a list of selected rows, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.selectedRows(), XAOmniOutlinerSelectedRowList, filter)




class XAOmniOutlinerChildList(XAOmniOutlinerRowList):
    """A wrapper around lists of child rows that employs fast enumeration techniques.

    All properties of child rows can be called as methods on the wrapped list, returning a list containing each child row's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerChild)

class XAOmniOutlinerChild(XAOmniOutlinerRow):
    """For a document, the top level rows. For a row, the rows one level below this one.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerAncestorList(XAOmniOutlinerRowList):
    """A wrapper around lists of ancestor rows that employs fast enumeration techniques.

    All properties of ancestor rows can be called as methods on the wrapped list, returning a list containing each ancestor row's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerAncestor)

class XAOmniOutlinerAncestor(XAOmniOutlinerRow):
    """The rows that this row is contained by, from the top level on down.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerSectionList(XAOmniOutlinerRowList):
    """A wrapper around lists of sections that employs fast enumeration techniques.

    All properties of sections can be called as methods on the wrapped list, returning a list containing each section's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerSection)

class XAOmniOutlinerSection(XAOmniOutlinerRow):
    """The sections underneath the document or row. Note that a row is not a section of itself, so if you access this on a single row, an empty list will be returned.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerSelectedRowList(XAOmniOutlinerRowList):
    """A wrapper around lists of selected rows that employs fast enumeration techniques.

    All properties of selected rows can be called as methods on the wrapped list, returning a list containing each selected row's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerSelectedRow)

class XAOmniOutlinerSelectedRow(XAOmniOutlinerRow):
    """The sections underneath the document or row. Note that a row is not a section of itself, so if you access this on a single row, an empty list will be returned.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerLeafList(XAOmniOutlinerRowList):
    """A wrapper around lists of leaf rows that employs fast enumeration techniques.

    All properties of leaf rows can be called as methods on the wrapped list, returning a list containing each leaf row's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerLeaf)

class XAOmniOutlinerLeaf(XAOmniOutlinerRow):
    """The leaf rows underneath a document or row. Note that a row is not its own leaf, so if you access this on a single row with no children, that row will not be returned (use the command 'bottom rows' for that).

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerFollowingSiblingList(XAOmniOutlinerRowList):
    """A wrapper around lists of following siblings that employs fast enumeration techniques.

    All properties of following siblings can be called as methods on the wrapped list, returning a list containing each siblings's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerFollowingSibling)

class XAOmniOutlinerFollowingSibling(XAOmniOutlinerRow):
    """The row which follows this row.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerPrecedingSiblingList(XAOmniOutlinerRowList):
    """A wrapper around lists of preceding siblings that employs fast enumeration techniques.

    All properties of preceding siblings can be called as methods on the wrapped list, returning a list containing each siblings's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerPrecedingSibling)

class XAOmniOutlinerPrecedingSibling(XAOmniOutlinerRow):
    """The row which precedes this row.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)





class XAOmniOutlinerPathComponentList(XAOmniOutlinerRowList):
    """A wrapper around lists of path components that employs fast enumeration techniques.

    All properties of path components can be called as methods on the wrapped list, returning a list containing each path component's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerPathComponent)

class XAOmniOutlinerPathComponent(XAOmniOutlinerRow):
    """A list of rows up to and including the given row.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerCellList(XABase.XAList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerCell, filter)

class XAOmniOutlinerCell(XABase.XAObject):
    """A cell object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.column: XAOmniOutlinerColumn #: Column that this cell is in
        self.state: XAOmniOutlinerApplication.CheckboxState #:  State of the cell. This is only valid on checkbox columns
        self.id: str #: The unique identifier of the cell within the containing row. This identifier is the same as the identifier of the cell's column
        self.text: XAOmniOutlinerRichText #: Text of the cell. This is only valid on text columns
        self.value: Union[str, datetime, int, float, 'XAOmniOutlinerEnumeration', XAOmniOutlinerApplication.CheckboxState] #: Contents of the cell, whatever the type
        self.row: XAOmniOutlinerRow #: Row that this cell is in
        self.name: str #: The name of the cell. This is the same as the name of the cell's column

    @property
    def column(self) -> XAOmniOutlinerColumn:
        return self._new_element(self.xa_elem.column(), XAOmniOutlinerColumn)

    @column.setter
    def column(self, column: XAOmniOutlinerColumn):
        self.set_property("column", column.xa_elem)

    @property
    def state(self) -> XAOmniOutlinerApplication.CheckboxState:
        return XAOmniOutlinerApplication.CheckboxState(self.xa_elem.state())

    @state.setter
    def state(self, state: XAOmniOutlinerApplication.CheckboxState):
        self.set_property("state", state.value)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def text(self) -> XAOmniOutlinerRichText:
        return self._new_element(self.xa_elem.text(), XAOmniOutlinerRichText)
    
    @text.setter
    def text(self, text: XAOmniOutlinerRichText):
        self.set_property("text", text.xa_elem)

    @property
    def value(self) -> Union[str, datetime, int, float, 'XAOmniOutlinerEnumeration', XAOmniOutlinerApplication.CheckboxState]:
        # TODO
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Union[str, datetime, int, float, 'XAOmniOutlinerEnumeration', XAOmniOutlinerApplication.CheckboxState]):
        # TODO
        self.set_property("value", value)

    @property
    def row(self) -> XAOmniOutlinerRow:
        self._new_element(self.xa_elem.row(), XAOmniOutlinerRow)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def replace(self, replacement: str, regex_to_find: Union[str, None] = None, string_to_find: Union[str, None] = None):
        """Replaces the contents of the cell.

        :param replacement: The replacement string
        :type replacement: str
        :param regex_to_find: The regular expression to find and replace, defaults to None
        :type regex_to_find: Union[str, None], optional
        :param string_to_find: The string to find and replace, defaults to None
        :type string_to_find: Union[str, None], optional

        .. versionadded:: 0.0.9
        """
        self.xa_elem.replaceMatchingRegularExpression_replacement_string_(regex_to_find, replacement, string_to_find)




class XAOmniOutlinerStyleList(XABase.XAList):
    """A wrapper around lists of OmniOutliner styles that employs fast enumeration techniques.

    All properties of styles can be called as methods on the wrapped list, returning a list containing each style's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAOmniOutlinerStyle
        super().__init__(properties, obj_class, filter)

class XAOmniOutlinerStyle(XABase.XAObject):
    """A style object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.container: XABase.XAObject #: The object owning the style
        self.font: str #: The name of the font of the style

    @property
    def container(self) -> XABase.XAObject:
        container = self.xa_elem.container()
        if hasattr(container, "alternateColor"):
            return self._new_element(container, XAOmniOutlinerDocument)
        # TODO -- other types!

    @property
    def font(self) -> str:
        return self.xa_elem.font()

    @font.setter
    def font(self, font: str):
        self.set_property("font", font)

    def named_styles(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerNamedStyleList':
        """Returns a list of named styles, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.namedStyles(), XAOmniOutlinerNamedStyleList, filter)

    def attributes(self, filter: Union[dict, None] = None) -> 'XAOmniOutlinerAttributeList':
        """Returns a list of attributes, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.attributes(), XAOmniOutlinerAttributeList, filter)




class XAOmniOutlinerLevelStyleList(XAOmniOutlinerStyleList):
    """A wrapper around lists of level styles that employs fast enumeration techniques.

    All properties of level styles can be called as methods on the wrapped list, returning a list containing each style's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerLevelStyle)

class XAOmniOutlinerLevelStyle(XABase.XAObject):
    """A level style object in a document.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerNamedStyleList(XAOmniOutlinerStyleList):
    """A wrapper around lists of named styles that employs fast enumeration techniques.

    All properties of named styles can be called as methods on the wrapped list, returning a list containing each styles's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAOmniOutlinerNamedStyleList)

class XAOmniOutlinerNamedStyle(XAOmniOutlinerStyle):
    """A named style object.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: An identifier for the named style that is unique within its document. Currently this identifier is not persistent between two different sessions of editing the document
        self.name: str #: The name of the style. Must be unique within the containing document

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)




class XAOmniOutlinerAttributeList(XABase.XAList):
    """A wrapper around lists of attributes that employs fast enumeration techniques.

    All properties of attributes can be called as methods on the wrapped list, returning a list containing each attribute's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerAttribute, filter)

class XAOmniOutlinerAttribute(XABase.XAObject):
    """An attribute of a style.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the attribute
        self.style: XAOmniOutlinerStyle #: The style to which the attribute refers
        self.has_local_value: bool #: If true, the containing style defines a local value for this attribute
        self.defining_style: XAOmniOutlinerStyle #: The style responsible for the effective value in this attributes's style. This processes the local values, inherited styles and cascade chain
        self.value: Union[XAOmniOutlinerGenericColor, XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, XAOmniOutlinerPoint, None] #: The value of the attribute in its style
        self.default_value: Union[XAOmniOutlinerGenericColor, XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, XAOmniOutlinerPoint, None] #: The default value of the attribute in its style

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def style(self) -> XAOmniOutlinerStyle:
        return self._new_element(self.xa_elem.style(), XAOmniOutlinerStyle)

    @style.setter
    def style(self, style: XAOmniOutlinerStyle):
        self.set_property("style", style.xa_elem)

    @property
    def has_local_value(self) -> bool:
        return self.xa_elem.hasLocalValue()

    @property
    def defining_style(self) -> XAOmniOutlinerStyle:
        return self._new_element(self.xa_elem.definingStyle(), XAOmniOutlinerStyle)

    @property
    def value(self) -> Union['XAOmniOutlinerGenericColor', XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, 'XAOmniOutlinerPoint', None]:
        # TODO
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Union['XAOmniOutlinerGenericColor', XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, 'XAOmniOutlinerPoint', None]):
        self.set_property("value", value)

    @property
    def default_value(self) -> Union['XAOmniOutlinerGenericColor', XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, 'XAOmniOutlinerPoint', None]:
        return self.xa_elem.defaultValue()

    @default_value.setter
    def default_value(self, default_value: Union['XAOmniOutlinerGenericColor', XABase.XAColor, str, XABase.XAURL, float, list[float], int, bool, 'XAOmniOutlinerPoint', None]):
        self.set_property("defaultValue", default_value)

    def clear(self):
        """Clears a locally set value for a style attribute.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.clear()




class XAOmniOutlinerPoint(XABase.XAObject):
    """A point value.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.x: float #: The x coordinate of the point
        self.y: float #: The y coordinate of the point

    @property
    def x(self) -> float:
        return self.xa_elem.x()

    @x.setter
    def x(self, x: float):
        self.set_property("x", x)

    @property
    def y(self) -> float:
        return self.xa_elem.y()

    @x.setter
    def y(self, y: float):
        self.set_property("y", y)



class XAOmniOutlinerPNGData(XABase.XAObject):
    """A PNG data object.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerTIFFData(XABase.XAObject):
    """A TIFF data object.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerArchiveData(XABase.XAObject):
    """A archive data object.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAOmniOutlinerGenericColor(XABase.XAObject):
    """A generic color value.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.r: float #: If the color is in a RGB color space, this is the calibrated floating point red component, from zero to one
        self.g: float #: If the color is in a RGB color space, this is the calibrated floating point green component, from zero to one
        self.b: float #: If the color is in a RGB color space, this is the calibrated floating point blue component, from zero to one
        self.w: float #: If the color is in a White color space, this is the calibrated floating point white component, from zero to one, with zero being totally black and one being totally white
        self.c: float #: If the color is in a CMYK color space, this is the device-specific floating point cyan component, from zero to one. There is currently no support for calibrated CYMK color spaces
        self.y: float #: If the color is in a CMYK color space, this is the device-specific floating point yellow component, from zero to one. There is currently no support for calibrated CYMK color spaces
        self.m: float #: If the color is in a CMYK color space, this is the device-specific floating point magenta component, from zero to one. There is currently no support for calibrated CYMK color spaces
        self.k: float #: If the color is in a CMYK color space, this is the device-specific floating point black component, from zero to one. There is currently no support for calibrated CYMK color spaces
        self.h: float #: If the color is in a HSV color space, this is the calibrated floating point hue component, from zero to one
        self.s: float #: If the color is in a HSV color space, this is the calibrated floating point saturation component, from zero to one
        self.v: float #: If the color is in a HSV color space, this is the calibrated floating point value component, from zero to on
        self.a: float #: The opacity or alpha of the color as a floating point number from zero to one with zero being totally transparent and one being totally opaque
        self.catalog: str #: If the color is in a catalog color space, this is the name of the catalog
        self.name: str #: If the color is in a catalog color space, this is the name of color with in the catalog
        self.png: XAOmniOutlinerPNGData #: If the color is in a pattern color space, this is PNG data for the image representing the pattern
        self.tiff: XAOmniOutlinerTIFFData #: If the color is in a pattern color space, this is TIFF data for the image representing the pattern
        self.archive: XAOmniOutlinerArchiveData #: If the color cannot be represented in any other format, a binary archive is placed in this property

    @property
    def r(self) -> float:
        return self.xa_elem.r()

    @r.setter
    def r(self, r: float):
        self.set_property("r", r)

    @property
    def g(self) -> float:
        return self.xa_elem.g()

    @g.setter
    def g(self, g: float):
        self.set_property("g", g)

    @property
    def b(self) -> float:
        return self.xa_elem.b()

    @b.setter
    def b(self, b: float):
        self.set_property("b", b)

    @property
    def w(self) -> float:
        return self.xa_elem.w()

    @w.setter
    def w(self, w: float):
        self.set_property("w", w)

    @property
    def c(self) -> float:
        return self.xa_elem.c()

    @c.setter
    def c(self, c: float):
        self.set_property("c", c)

    @property
    def y(self) -> float:
        return self.xa_elem.y()

    @y.setter
    def y(self, y: float):
        self.set_property("y", y)

    @property
    def m(self) -> float:
        return self.xa_elem.m()

    @m.setter
    def m(self, m: float):
        self.set_property("m", m)

    @property
    def k(self) -> float:
        return self.xa_elem.k()

    @k.setter
    def k(self, k: float):
        self.set_property("k", k)

    @property
    def h(self) -> float:
        return self.xa_elem.h()

    @h.setter
    def h(self, h: float):
        self.set_property("h", h)

    @property
    def s(self) -> float:
        return self.xa_elem.s()

    @s.setter
    def s(self, s: float):
        self.set_property("s", s)

    @property
    def v(self) -> float:
        return self.xa_elem.v()

    @v.setter
    def v(self, v: float):
        self.set_property("v", v)

    @property
    def catalog(self) -> str:
        return self.xa_elem.catalog()

    @catalog.setter
    def catalog(self, catalog: str):
        self.set_property("catalog", catalog)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def png(self) -> XAOmniOutlinerPNGData:
        return self._new_element(self.xa_elem.png(), XAOmniOutlinerPNGData)

    @png.setter
    def png(self, png: XAOmniOutlinerPNGData):
        self.set_property("png", png.xa_elem)

    @property
    def tiff(self) -> XAOmniOutlinerTIFFData:
        return self._new_element(self.xa_elem.tiff(), XAOmniOutlinerTIFFData)

    @tiff.setter
    def tiff(self, tiff: XAOmniOutlinerTIFFData):
        self.set_property("tiff", tiff.xa_elem)

    @property
    def archive(self) -> XAOmniOutlinerArchiveData:
        return self._new_element(self.xa_elem.archive(), XAOmniOutlinerArchiveData)

    @archive.setter
    def archive(self, archive: XAOmniOutlinerArchiveData):
        self.set_property("archive", archive.xa_elem)




class XAOmniOutlinerPreferenceList(XABase.XAList):
    """A wrapper around lists of preferences that employs fast enumeration techniques.

    All properties of preferences can be called as methods on the wrapped list, returning a list containing each preference's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerPreference, filter)

class XAOmniOutlinerPreference(XABase.XAObject):
    """A row object in OmniOutliner.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: The identifier of the preference
        self.value: Union[str, float, int, bool, None] #: The current value of the preference
        self.default_value: Union[str, float, int, bool, None] #: The default value of the preference

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def value(self) -> Union[str, float, int, bool, None]:
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Union[str, float, int, bool, None]):
        self.set_property("value", value)

    @property
    def default_value(self) -> Union[str, float, int, bool, None]:
        return self.xa_elem.defaultValue()

    @default_value.setter
    def default_value(self, default_value: Union[str, float, int, bool, None]):
        self.set_property("defaultValue", default_value)




class XAOmniOutlinerConduitSettingDomainList(XABase.XAList):
    """A wrapper around lists of conduit setting domains that employs fast enumeration techniques.

    All properties of conduit setting domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerConduitSettingDomain, filter)

class XAOmniOutlinerConduitSettingDomain(XABase.XAObject):
    """A group of custom settings from one external source. Note that conduit setting domains should only be referenced by 'id'. The first time one is referenced it will be created. Any other type of access (by index, every, etc.) will produce an error.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.id: str #: The unique identifier of the domain. These should typically be in the reverse-DNS style of bundle identifiers ("com.mycompany.myproduct")
        self.settings: list[Union[str, None]] #: Values must be strings or 'missing value' (removes value). To set a single entry, concatenate the current value with the changes and then re-set it. Concatenating an empty and non-empty record crashes AppleScript, so 'missing value' will be returned
        self.external_id: str #: Identifies the conduit externally to OmniOutliner. This might be a record identifier in an external database. This will not get copied when duplicating the row, or if a 'save as' or 'save to' operation is performed instead of a normal 'save'
        self.container: XABase.XAObject #: The row or document containing this group of conduit settings

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def settings(self) -> list[Union[str, None]]:
        return self.xa_elem.settings()

    @settings.setter
    def settings(self, settings: list[Union[str, None]]):
        self.set_property("settings", settings)

    @property
    def external_id(self) -> str:
        return self.xa_elem.externalId()

    @property
    def container(self) -> XABase.XAObject:
        # TODO
        return self.xa_elem.container()




class XAOmniOutlinerXslTransformList(XABase.XAList):
    """A wrapper around lists of XSL transforms that employs fast enumeration techniques.

    All properties of XSL transforms can be called as methods on the wrapped list, returning a list containing each transforms's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAOmniOutlinerXslTransform, filter)

class XAOmniOutlinerXslTransform(XABase.XAObject):
    """This class represents an available XSL transformation that may be applied when loading or saving documents.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.directory_extension: str #: The prefered file extension for file-system representations of wrapped file documents handled by this plugin
        self.directory_index_file_name: str #: When writing a document with attachments, this specifies the name of the index file written inside the directory containing the transformed XML
        self.write_attachments: bool #: When writing a document with attachments, this specifies whether the attachments will be written to the output location
        self.display_name: str #: The human readable name for the transform
        self.file_extension: str #: The preferred file extension for file-system representations of flat file documents handled by this plugin
        self.id: str #: A unique identifier for the transform to be used as the 'as' parameter of the 'save' command
        self.is_export: bool #: Returns true if the source format is a native format for OmniOutliner
        self.is_import: bool #: Returns true if the result format is a native format for OmniOutliner
        self.parameter_names: str #: Names of all XSL parameters set on this transform
        self.result_format: str #: A description of the data type produced by this transform. For XML data types, this is the DTD public identifier
        self.source_format: str #: A description of the data type consumed by this transform. For XML data types, this is the DTD public identifier
        self.stylesheet: str #: The XSL source for the transform

    @property
    def directory_extension(self) -> str:
        return self.xa_elem.directoryExtension()

    @directory_extension.setter
    def directory_extension(self, directory_extension: str):
        self.set_property("directoryExtension", directory_extension)

    @property
    def directory_index_file_name(self) -> str:
        return self.xa_elem.directoryIndexFileName()

    @directory_index_file_name.setter
    def directory_index_file_name(self, directory_index_file_name: str):
        self.set_property("directoryIndexFileName", directory_index_file_name)

    @property
    def write_attachments(self) -> bool:
        return self.xa_elem.writeAttachments()

    @write_attachments.setter
    def write_attachments(self, write_attachments: bool):
        self.set_property("writeAttachments", write_attachments)

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @display_name.setter
    def display_name(self, display_name: str):
        self.set_property("displayName", display_name)

    @property
    def file_extension(self) -> str:
        return self.xa_elem.fileExtension()

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self.set_rpoperty("fileExtension", file_extension)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def is_export(self) -> bool:
        return self.xa_elem.isExport()

    @property
    def is_import(self) -> bool:
        return self.xa_elem.isImport()

    @property
    def parameter_names(self) -> str:
        return self.xa_elem.parameterNames()

    @property
    def result_format(self) -> str:
        return self.xa_elem.resultFormat()

    @result_format.setter
    def result_format(self, result_format: str):
        self.set_rpoperty("resultFormat", result_format)

    @property
    def source_format(self) -> str:
        return self.xa_elem.sourceFormat()

    @source_format.setter
    def source_format(self, source_format: str):
        self.set_property("sourceFormat", source_format)

    @property
    def stylesheet(self) -> str:
        return self.xa_elem.stylesheet()

    @stylesheet.setter
    def stylesheet(self, stylesheet: str):
        self.set_property("stylesheet", stylesheet)

    def get_parameter(self, parameter_name: str) -> str:
        """Gets the XPath expression currently set for a XSL parameter

        :param parameter_name: The name of the parameter
        :type parameter_name: str
        :return: The XPath expression currently set for the parameter
        :rtype: str

        .. versionadded:: 0.0.9
        """
        return self.xa_elem.getParameterNamed_(parameter_name)

    def set_parameter(self, parameter_name: str, value: str):
        """Sets the XPath expression for a parameter. Note that to set a string constant you must quote the string. For example "foo" means "element foo" but "'foo'" means "constant string 'foo'".

        :param parameter_name: The name of the parameter
        :type parameter_name: str
        :param value: The value of the parameter
        :type value: str

        .. versionadded:: 0.0.9
        """
        self.xa_elem.setParameterTo_named_(value, parameter_name)