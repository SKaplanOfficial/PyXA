""".. versionadded:: 0.0.8

Control the macOS Numbers application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, List, Tuple, Union
from AppKit import NSURL, NSSet, NSPoint, NSValue, NSMutableArray
from ScriptingBridge import SBElementArray

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import XACloseable

class XANumbersApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Numbers.app.

    .. seealso:: :class:`XANumbersWindow`, :class:`XANumbersDocument`

    .. versionadded:: 0.0.8
    """
    class SaveOption(Enum):
        """Options for what to do when calling a save event.
        """
        SAVE_FILE   = OSType('yes ') #: Save the file. 
        DONT_SAVE   = OSType('no  ') #: Do not save the file. 
        ASK         = OSType('ask ') #: Ask the user whether or not to save the file. 

    class ExportFormat(Enum):
        """Options for what format to export a Numbers project as.
        """
        Numbers                 = OSType('Nuff') #: The Numbers native file format 
        PDF                     = OSType('Npdf') #: PDF format
        MICROSOFT_EXCEL         = OSType('Nexl') #: Excel format
        CSV                     = OSType('Ncsv') #: CSV format
        NUMBERS_09              = OSType('Nnmb') #: Numbers 2009 format

    class PrintSetting(Enum):
        """Options to use when printing documents.
        """
        STANDARD_ERROR_HANDLING = OSType('lwst') #: Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = OSType('lwdt') #: print a detailed report of PostScript errors 

    class ImageQuality(Enum):
        """Options for the quality of exported images.
        """
        GOOD      = OSType('KnP0') #: Good quality 
        BETTER    = OSType('KnP1') #: Better quality 
        BEST      = OSType('KnP2') #: Best quality 

    class Alignment(Enum):
        """Options for the horizontal and vertical alignment of content within table containers.
        """
        BOTTOM                  = OSType('avbt') #: Bottom-align content. 
        CENTER_VERTICAL         = OSType('actr') #: Center-align content. 
        TOP                     = OSType('avtp') #: Top-align content. 
        AUTO                    = OSType('aaut') #: Auto-align based on content type. 
        CENTER_HORIZONTAL       = OSType('actr') #: Center-align content. 
        JUSTIFY                 = OSType('ajst') #: Fully justify (left and right) content. 
        LEFT                    = OSType('alft') #: Left-align content. 
        RIGHT                   = OSType('arit') #: Right-align content. 

    class SortDirection(Enum):
        """Options for the direction of sorting when sorting table cells.
        """
        ASCENDING               = OSType('ascn') #: Sort in increasing value order 
        DESCENDING              = OSType('dscn') #: Sort in decreasing value order 

    class CellFormat(Enum):
        """Options for the format to use when formatting table cells.
        """
        AUTO                    = OSType('faut') #: Automatic format 
        CHECKBOX                = OSType('fcch') #: Checkbox control format (Numbers only) 
        CURRENCY                = OSType('fcur') #: Currency number format 
        DATE_AND_TIME           = OSType('fdtm') #: Date and time format 
        FRACTION                = OSType('ffra') #: Fraction number format 
        DECIMAL_NUMBER          = OSType('nmbr') #: Decimal number format 
        PERCENT                 = OSType('fper') #: Percentage number format 
        POPUP_MENU              = OSType('fcpp') #: Pop-up menu control format (Numbers only) 
        SCIENTIFIC              = OSType('fsci') #: Scientific notation format 
        SLIDER                  = OSType('fcsl') #: Slider control format (Numbers only) 
        STEPPER                 = OSType('fcst') #: Stepper control format (Numbers only) 
        TEXT                    = OSType('ctxt') #: Text format 
        DURATION                = OSType('fdur') #: Duration format 
        RATING                  = OSType('frat') #: Rating format. (Numbers only) 
        NUMERAL_SYSTEM          = OSType('fcns') #: Numeral System 

    class FillOption(Enum):
        """Options for the type of fill to use.
        """
        NO_FILL                 = OSType('fino')   
        COLOR_FILL              = OSType('fico')   
        GRADIENT_FILL           = OSType('figr')   
        ADVANCED_GRADIENT_FILL  = OSType('fiag')   
        IMAGE_FILL              = OSType('fiim')   
        ADVANCED_IMAGE_FILL     = OSType('fiai')   

    class RepetitionMethod(Enum):
        """Options for whether and how a clip will repeat.
        """
        NONE                    = OSType('mvrn')   
        LOOP                    = OSType('mvlp')   
        LOOP_BACK_AND_FORTH     = OSType('mvbf')

    class KeyAction(Enum):
        """Options for key states and interactions.
        """
        COMMAND_DOWN = OSType('Kcmd')
        CONTROL_DOWN = OSType('Kctl')
        OPTION_DOWN  = OSType('Kopt')
        SHIFT_DOWN   = OSType('Ksft')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XANumbersWindow

        self.properties: dict #: All properties of the application
        self.name: str #: The name of the Numbers application
        self.frontmost: bool #: Whether Numbers is the active application
        self.version: str #: The Numbers.app version number
        self.current_document: XANumbersDocument #: The current document of the front window

    @property
    def properties(self) -> dict:
        return self.xa_scel.properties()

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
    def current_document(self) -> 'XANumbersDocument':
        return self.front_window.document

    def print(self, item: Union['XANumbersDocument', XABaseScriptable.XASBWindow], print_properties: dict = None, show_dialog: bool = True) -> 'XANumbersApplication':
        """Prints a document or window.

        :param item: The document or window to print
        :type item: Union[XANumbersDocument, XABaseScriptable.XASBWindow]
        :param print_properties: The settings to pre-populate the print dialog with, defaults to None
        :type print_properties: dict, optional
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: A reference to the PyXA application object
        :rtype: XANumbersApplication

        .. versionadded:: 0.0.8
        """
        if print_properties is None:
            print_properties = {}
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, print_properties, show_dialog)
        return self

    def open(self, path: Union[str, NSURL]) -> 'XANumbersDocument':
            """Opens the file at the given filepath.

            :param target: The path of the file to open.
            :type target: Union[str, NSURL]
            :return: A reference to newly created document object
            :rtype: XANumbersDocument

            .. versionadded:: 0.0.8
            """
            if not isinstance(path, NSURL):
                path = XABase.XAPath(path)
            self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
            return self.documents()[0]

    def set_password(self, document: 'XANumbersDocument', password: str, hint: str, save_in_keychain: bool = True) -> 'XANumbersApplication':
        """Sets the password of an unencrypted document, optionally storing the password in the user's keychain.

        :param document: The document to set the password for
        :type document: XANumbersDocument
        :param password: The password
        :type password: str
        :param hint: A hint for the password
        :type hint: str
        :param save_in_keychain: Whether to save the password in the user's keychain, defaults to True
        :type save_in_keychain: bool, optional
        :return: A reference to the PyXA application object
        :rtype: XANumbersApplication

        .. versionadded:: 0.0.8
        """
        self.xa_scel.setPassword_to_hint_savingInKeychain_(password, document.xa_elem, hint, save_in_keychain)
        return self

    def remove_password(self, document: 'XANumbersDocument', password: str) -> 'XANumbersApplication':
        """Removes the password from a document.

        :param document: The document to remove the password to
        :type document: XANumbersDocument
        :param password: The current password
        :type password: str
        :return: A reference to the PyXA application object
        :rtype: XANumbersApplication

        .. versionadded:: 0.0.8
        """
        self.xa_scel.removePassword_from_(password, document.xa_elem)
        return self

    def new_sheet(self, document: 'XANumbersDocument', properties: dict = None) -> 'XANumbersSheet':
        if properties is None:
            properties = {}
        return self.push("sheet", properties, document.xa_elem.Numbers())

    def documents(self, filter: Union[dict, None] = None) -> 'XANumbersDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: List[XANumbersDocument]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.documents(), XANumbersDocumentList, filter)

    def new_document(self, file_path: str = "./Untitled.key", template: 'XANumbersSheet' = None) -> 'XANumbersDocument':
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        properties = {
            "file": file_path,
        }
        if template is not None:
            properties["documentTemplate"] = template.xa_elem
        return self.push("document", properties, self.xa_scel.documents())

    def templates(self, filter: Union[dict, None] = None) -> 'XANumbersTemplateList':
        """Returns a list of templates, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned templates will have, or None
        :type filter: Union[dict, None]
        :return: The list of templates
        :rtype: XANumbersTemplateList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.templates(), XANumbersTemplateList, filter)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Making a new document

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> new_doc = Numbers.make("document", {"bodyText": "This is a whole new document!"})
        >>> Numbers.documents().push(new_doc)

        :Example 3: Making new elements on a page

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> new_line = Numbers.make("line", {"startPoint": (100, 100), "endPoint": (200, 200)})
        >>> Numbers.documents()[0].Numbers()[0].lines().push(new_line)

        .. versionadded:: 0.0.8
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XANumbersDocument)
        elif specifier == "shape":
            return self._new_element(obj, XANumbersShape)
        elif specifier == "table":
            return self._new_element(obj, XANumbersTable)
        elif specifier == "audioClip":
            return self._new_element(obj, XANumbersAudioClip)
        elif specifier == "chart":
            return self._new_element(obj, XANumbersChart)
        elif specifier == "image":
            return self._new_element(obj, XANumbersImage)
        elif specifier == "sheet":
            return self._new_element(obj, XANumbersSheet)
        # elif specifier == "column":
        #     return self._new_element(obj, XANumbersColumn)
        # elif specifier == "row":
        #     return self._new_element(obj, XANumbersRow)
        elif specifier == "line":
            return self._new_element(obj, XANumbersLine)
        elif specifier == "movie":
            return self._new_element(obj, XANumbersMovie)
        elif specifier == "textItem":
            return self._new_element(obj, XANumbersTextItem)
        elif specifier == "group":
            return self._new_element(obj, XANumbersGroup)
        elif specifier == "iWorkItem":
            return self._new_element(obj, XANumbersiWorkItem)




class XANumbersWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject):
    """A window of Numbers.app.

    .. versionadded:: 0.0.8
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
        self.document: XANumbersDocument #: The document currently displayed in the window

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
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

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
    def document(self) -> 'XANumbersDocument':
        return self._new_element(self.xa_elem.document(), XANumbersDocument)




class XANumbersDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANumbersDocument, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def document_template(self) -> 'XANumbersTemplateList':
        ls = self.xa_elem.arrayByApplyingSelector_("documentTemplate")
        return self._new_element(ls, XANumbersTemplateList)

    def active_sheet(self) -> 'XANumbersSheetList':
        ls = self.xa_elem.arrayByApplyingSelector_("activeSheet")
        return self._new_element(ls, XANumbersSheetList)

    def selection(self) -> 'XANumbersiWorkItemList':
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XANumbersiWorkItemList)

    def password_protected(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> 'XANumbersDocument':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XANumbersDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XANumbersDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XANumbersDocument':
        return self.by_property("file", file)

    def by_id(self, id: str) -> 'XANumbersDocument':
        return self.by_property("id", id)

    def by_document_template(self, document_template: 'XANumbersTemplate') -> 'XANumbersDocument':
        return self.by_property("documentTemplate", document_template.xa_elem)

    def by_active_sheet(self, active_sheet: 'XANumbersSheet') -> 'XANumbersDocument':
        return self.by_property("activeSheet", active_sheet.xa_elem)

    def by_selection(self, selection: 'XANumbersiWorkItemList') -> 'XANumbersDocument':
        return self.by_property("selection", selection.xa_elem)

    def by_password_protected(self, password_protected: bool) -> 'XANumbersDocument':
        return self.by_property("passwordProtected", password_protected)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XANumbersDocument(XABaseScriptable.XASBPrintable, XACloseable):
    """A class for managing and interacting with Numbers documents.

    .. seealso:: :class:`XANumbersApplication`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.file: str #: The location of the document on the disk, if one exists
        self.id: str #: The unique identifier for the document
        self.document_template: XANumbersTemplate #: The template assigned to the document
        self.active_sheet: XANumbersSheet #: The active sheet of the document
        self.selection: XANumbersiWorkItemList #: A list of the currently selected items
        self.password_protected: bool #: Whether the document is password protected

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

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
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def document_template(self) -> 'XANumbersTemplate':
        return self._new_element(self.xa_elem.documentTemplate(), XANumbersTemplate)

    @property
    def active_sheet(self) -> 'XANumbersSheet':
        return self._new_element(self.xa_elem.activeSheet(), XANumbersSheet)

    @property
    def selection(self) -> 'XANumbersiWorkItemList':
        return self._new_element(self.xa_elem.selection(), XANumbersiWorkItemList)

    @property
    def password_protected(self) -> bool:
        return self.xa_elem.passwordProtected()

    def export(self, file_path: Union[str, NSURL] = None, format: XANumbersApplication.ExportFormat = XANumbersApplication.ExportFormat.PDF):
        """Exports the document in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, NSURL], optional
        :param format: The format to export the file in, defaults to XANumbersApplication.ExportFormat.PDF
        :type format: XANumbersApplication.ExportFormat, optional

        .. versionadded:: 0.0.8
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path, format.value, None)

    def new_sheet(self, properties: dict = None) -> 'XANumbersSheet':
        """Creates a new sheet at the end of the document.

        :param properties: The properties to give the new page
        :type properties: dict
        :return: A reference to the newly created sheet object
        :rtype: XANumbersSheet

        .. versionadded:: 0.0.8
        """
        return self.xa_prnt.xa_prnt.new_sheet(self, properties)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XANumbersAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XANumbersAudioClipList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.audioClips(), XANumbersAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XANumbersChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XANumbersChartList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.charts(), XANumbersChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XANumbersGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XANumbersGroupList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.groups(), XANumbersGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XANumbersImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XANumbersImageList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.images(), XANumbersImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XANumbersiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XANumbersiWorkItemList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.iWorkItems(), XANumbersiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XANumbersLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XANumbersLineList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.lines(), XANumbersLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XANumbersMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XANumbersMovieList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.movies(), XANumbersMovieList, filter)

    def sheets(self, filter: Union[dict, None] = None) -> 'XANumbersSheetList':
        """Returns a list of sheets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sheets will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XANumbersSheetList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.sheets(), XANumbersSheetList, filter)

    def sections(self, filter: Union[dict, None] = None) -> 'XANumbersSectionList':
        """Returns a list of sections, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sections will have, or None
        :type filter: Union[dict, None]
        :return: The list of sections
        :rtype: XANumbersSectionList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.sections(), XANumbersSectionList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XANumbersShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XANumbersShapeList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.shapes(), XANumbersShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XANumbersTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XANumbersTableList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.tables(), XANumbersTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XANumbersTextItemList':
        """Returns a list of text items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text items
        :rtype: XANumbersTextItemList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.textItems(), XANumbersTextItemList, filter)




class XANumbersTemplateList(XABase.XAList):
    """A wrapper around lists of templates that employs fast enumeration techniques.

    All properties of templates can be called as methods on the wrapped list, returning a list containing each template's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANumbersTemplate, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XANumbersTemplate':
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XANumbersTemplate':
        return self.by_property("name", name)

    def __repr__(self):
        return f"<{str(type(self))}{self.name}>"

class XANumbersTemplate(XABase.XAObject):
    """A class for managing and interacting with Numbers templates.

    .. seealso:: :class:`XANumbersApplication`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the template
        self.name: str #: The localized name of the template

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def __repr__(self):
        return f"<{str(type(self))}{self.name}, id={str(self.id)}>"




class XANumbersSectionList(XABase.XAList):
    """A wrapper around lists of sections that employs fast enumeration techniques.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANumbersSection, filter)

    def body_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyText"))

    def by_body_text(self, body_text: str) -> 'XANumbersSection':
        return self.by_property("bodyText", body_text)

class XANumbersSection(XABase.XAObject):
    """A class for managing and interacting with sections in Numbers.

    .. seealso:: :class:`XANumbersApplication`, :class:`XANumbersiWorkItem`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.body_text: str #: The section body text

    @property
    def body_text(self) -> str:
        return self.xa_elem.bodyText()




class XANumbersContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XANumbersContainer
        super().__init__(properties, obj_class, filter)

class XANumbersContainer(XABase.XAObject):
    """A class for managing and interacting with containers in Numbers.

    .. seealso:: :class:`XANumbersApplication`, :class:`XANumbersiWorkItem`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    def iwork_items(self, filter: Union[dict, None] = None) -> List['XANumbersiWorkItem']:
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: List[XANumbersiWorkItem]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.iWorkItems(), XANumbersiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> List['XANumbersAudioClip']:
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: List[XANumbersAudioClip]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.audioClips(), XANumbersAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> List['XANumbersChart']:
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: List[XANumbersChart]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.charts(), XANumbersChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> List['XANumbersImage']:
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: List[XANumbersImage]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.images(), XANumbersImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> List['XANumbersGroup']:
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: List[XANumbersGroup]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.groups(), XANumbersGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> List['XANumbersLine']:
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: List[XANumbersLine]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.lines(), XANumbersLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> List['XANumbersMovie']:
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: List[XANumbersMovie]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.movies(), XANumbersMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> List['XANumbersShape']:
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: List[XANumbersShape]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.shapes(), XANumbersShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> List['XANumbersTable']:
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: List[XANumbersTable]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.tables(), XANumbersTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> List['XANumbersTextItem']:
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: List[XANumbersTextItem]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.textItems(), XANumbersTextItemList, filter)




class XANumbersSheetList(XANumbersContainerList):
    """A wrapper around lists of Numbers sheets that employs fast enumeration techniques.

    All properties of Numbers sheets can be called as methods on the wrapped list, returning a list containing each sheet's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersSheet)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def body_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyText"))

    def by_properties(self, properties: dict) -> 'XANumbersSheet':
        return self.by_property("properties", properties)

    def by_body_text(self, body_text: str) -> 'XANumbersSheet':
        return self.by_property("bodyText", body_text)

class XANumbersSheet(XANumbersContainer):
    """A class for managing and interacting with Numbers in Numbers documents.

    .. seealso:: :class:`XANumbersApplication`, :class:`XANumbersiWorkItem`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the sheet
        self.name: str #: The name of the sheet

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    # def duplicate(self) -> 'XANumbersPage':
    #     """Duplicates the page, mimicking the action of copying and pasting the page manually.

    #     :return: A reference to the PyXA page object that called this command.
    #     :rtype: XANumbersPage

    #     .. versionadded:: 0.0.8
    #     """
    #     new_page = self.xa_prnt.xa_prnt.xa_prnt.xa_prnt.make("page", {})
    #     self.xa_prnt.xa_prnt.Numbers().push(new_page)
    #     for item in self.xa_elem.lines():
    #         print("ya")
    #         item.duplicateTo_withProperties_(new_page.xa_elem.lines()[0].positionAfter(), None)
    #     return self

    # def move_to(self, document):
    #     self.xa_elem.moveTo_(document.xa_elem.Numbers())

    # def delete(self):
    #     """Deletes the page.

    #     .. versionadded:: 0.0.8
    #     """
    #     self.xa_elem.get().delete()

    def add_image(self, file_path: Union[str, NSURL]) -> 'XANumbersImage':
        """Adds the image at the specified path to the slide.

        :param file_path: The path to the image file.
        :type file_path: Union[str, NSURL]
        :return: The newly created image object.
        :rtype: XANumbersImage

        .. versionadded:: 0.0.8
        """
        url = file_path
        if isinstance(url, str):
            url = NSURL.alloc().initFileURLWithPath_(file_path)
        image = self.xa_prnt.xa_prnt.xa_prnt.xa_prnt.make("image", {
            "file": url,
        })
        self.xa_elem.images().addObject_(image.xa_elem)
        image.xa_prnt = self
        return image

    # def add_chart(self, row_names: List[str], column_names: List[str], data: List[List[Any]], type: int = XANumbersApplication.ChartType.LINE_2D.value, group_by: int = XANumbersApplication.ChartGrouping.ROW.value) -> 'XANumbersChart':
    #     """_summary_

    #     _extended_summary_

    #     :param row_names: A list of row names.
    #     :type row_names: List[str]
    #     :param column_names: A list of column names.
    #     :type column_names: List[str]
    #     :param data: A 2d array 
    #     :type data: List[List[Any]]
    #     :param type: The chart type, defaults to _NumbersLegacyChartType.NumbersLegacyChartTypeLine_2d.value
    #     :type type: int, optional
    #     :param group_by: The grouping schema, defaults to _NumbersLegacyChartGrouping.NumbersLegacyChartGroupingChartRow.value
    #     :type group_by: int, optional
    #     :return: A reference to the newly created chart object.
    #     :rtype: XANumbersChart

    #     .. versionadded:: 0.0.8
    #     """
    #     self.xa_prnt.set_property("currentSlide", self.xa_elem)
    #     self.xa_elem.addChartRowNames_columnNames_data_type_groupBy_(row_names, column_names, data, type, group_by)
    #     chart = self.xa_elem.charts()[-1].get()
    #     properties = {
    #         "parent": self,
    #         "appspace": self.xa_apsp,
    #         "workspace": self.xa_wksp,
    #         "element": chart,
    #         "appref": self.xa_aref,
    #         "system_events": self.xa_sevt,
    #     }
    #     return XANumbersChart(properties)




class XANumbersiWorkItemList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XANumbersiWorkItem
        super().__init__(properties, obj_class, filter)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def locked(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def parent(self) -> XANumbersContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XANumbersContainerList)

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def by_height(self, height: int) -> 'XANumbersiWorkItem':
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> 'XANumbersiWorkItem':
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> 'XANumbersiWorkItem':
        return self.by_property("width", width)

    def by_parent(self, parent: XANumbersContainer) -> 'XANumbersiWorkItem':
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: Tuple[int, int]) -> 'XANumbersiWorkItem':
        return self.by_property("position", position)

class XANumbersiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Numbers.

    .. seealso:: :class:`XANumbersApplication`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict
        self.height: int #: The height of the iWork item
        self.locked: bool #: Whether the object is locked
        self.width: int #: The width of the iWork item
        self.parent: XANumbersContainer #: The iWork container that contains the iWork item
        self.position: Tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the iWork item

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @property
    def locked(self) -> bool:
        return self.xa_elem.locked()

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @property
    def parent(self) -> XANumbersContainer:
        return self._new_element(self.xa_elem.parent(), XANumbersContainer)

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.0.8
        """
        self.xa_elem.delete()

    def duplicate(self) -> 'XANumbersiWorkItem':
        """Duplicates the item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XANumbersiWorkItem

        .. versionadded:: 0.0.8
        """
        self.xa_elem.duplicateTo_withProperties_(self.parent.xa_elem.iWorkItems(), None)
        return self

    def resize(self, width: int, height: int) -> 'XANumbersiWorkItem':
        """Sets the width and height of the item.

        :param width: The desired width, in pixels
        :type width: int
        :param height: The desired height, in pixels
        :type height: int
        :return: The iWork item
        :rtype: XANumbersiWorkItem

        .. versionadded:: 0.0.8
        """
        self.set_properties({
            "width": width,
            "height": height,
        })
        return self

    def lock(self) -> 'XANumbersiWorkItem':
        """Locks the properties of the item, preventing changes.

        :return: The iWork item
        :rtype: XANumbersiWorkItem

        .. versionadded:: 0.0.8
        """
        self.set_property("locked", True)
        return self

    def unlock(self) -> 'XANumbersiWorkItem':
        """Unlocks the properties of the item, allowing changes.

        :return: The iWork item
        :rtype: XANumbersiWorkItem

        .. versionadded:: 0.0.8
        """
        self.set_property("locked", False)
        return self

    def set_position(self, x: int, y: int) -> 'XANumbersiWorkItem':
        position = NSValue.valueWithPoint_(NSPoint(x, y))
        self.xa_elem.setValue_forKey_(position, "position")





class XANumbersGroupList(XANumbersContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersGroup)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def parent(self) -> XANumbersContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XANumbersContainerList)

    def by_height(self, height: int) -> 'XANumbersGroup':
        return self.by_property("height", height)

    def by_position(self, position: Tuple[int, int]) -> 'XANumbersGroup':
        return self.by_property("position", position)

    def by_width(self, width: int) -> 'XANumbersGroup':
        return self.by_property("width", width)

    def by_rotation(self, rotation: int) -> 'XANumbersGroup':
        return self.by_property("rotation", rotation)

    def by_parent(self, parent: XANumbersContainer) -> 'XANumbersGroup':
        return self.by_property("parent", parent.xa_elem)

class XANumbersGroup(XANumbersContainer):
    """A class for managing and interacting with iWork item groups in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int #: The height of the group
        self.position: Tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the group
        self.width: int #: The widht of the group
        self.rotation: int #: The rotation of the group, in degrees from 0 to 359
        self.parent: XANumbersContainer #: The container which contains the group

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @property
    def parent(self) -> XANumbersContainer:
        return self._new_element(self.xa_elem.parent(), XANumbersContainer)

    def rotate(self, degrees: int) -> 'XANumbersGroup':
        """Rotates the group by the specified number of degrees.

        :param degrees: The amount to rotate the group, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: XANumbersGroup

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> group = Numbers.current_document.groups()[0]
        >>> group.rotate(45)

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XANumbersImageList(XANumbersiWorkItemList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersImage)

    def object_description(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def file(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def file_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def opacity(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_object_description(self, object_description: str) -> 'XANumbersImage':
        return self.by_property("objectDescription", object_description)

    def by_file(self, file: str) -> 'XANumbersImage':
        return self.by_property("file", file)

    def by_file_name(self, file_name: str) -> 'XANumbersImage':
        return self.by_property("fileName", file_name)

    def by_opacity(self, opacity: int) -> 'XANumbersImage':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XANumbersImage':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XANumbersImage':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XANumbersImage':
        return self.by_property("rotation", rotation)

class XANumbersImage(XANumbersiWorkItem):
    """A class for managing and interacting with images in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.object_description: str #: Text associated with the image, read aloud by VoiceOVer
        self.file: str #: The image file
        self.file_name: str #: The name of the image file
        self.opacity: int #: The opacity of the image, in percent from 0 to 100
        self.reflection_showing: bool #: Whether the image displays a reflection
        self.reflection_value: int #: The percentage of reflection of the image, from 0 to 100
        self.rotation: int #: The rotation of the image, in degrees from 0 to 359

    @property
    def description(self) -> str:
        return self.xa_elem.object_description()

    @property
    def file(self) -> str:
        return self.xa_elem.file()

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName().get()

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    def rotate(self, degrees: int) -> 'XANumbersImage':
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: XANumbersImage

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> page = Numbers.documents()[0].Numbers()[0]
        >>> img = page.add_image("/Users/steven/Documents/idk/idk.001.png")
        >>> img.rotate(30)
        >>> img.rotate(60)  # Rotated 60+30
        >>> img.rotate(90)  # Rotated 90+90
        >>> img.rotate(180) # Rotated 180+180

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, NSURL]) -> 'XANumbersImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, NSURL]
        :return: A reference to the new PyXA image object.
        :rtype: XANumbersImage

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> page = Numbers.documents()[0].Numbers()[0]
        >>> img = page.add_image("/Users/exampleuser/Documents/Images/Test1.png")
        >>> sleep(1)
        >>> img.replace_with("/Users/exampleuser/Documents/Images/Test2.png")

        .. versionadded:: 0.0.8
        """
        self.delete()
        if isinstance(self.xa_prnt.xa_prnt, XANumbersSheet):
            return self.xa_prnt.xa_prnt.add_image(img_path)
        return self.xa_prnt.add_image(img_path)




class XANumbersAudioClipList(XANumbersiWorkItemList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersAudioClip)

    def file_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> List[XANumbersApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XANumbersApplication.RepetitionMethod(x) for x in ls]

    def by_file_name(self, file_name: str) -> 'XANumbersAudioClip':
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> 'XANumbersAudioClip':
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XANumbersApplication.RepetitionMethod) -> 'XANumbersAudioClip':
        return self.by_property("repetitionMethod", repetition_method.value)

class XANumbersAudioClip(XANumbersiWorkItem):
    """A class for managing and interacting with audio clips in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str #: The name of the audio file
        self.clip_volume: int #: The volume setting for the audio clip, from 0 to 100
        self.repetition_method: XANumbersApplication.RepetitionMethod #: Whether or how the audio clip  repeats

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName()

    @property
    def clip_volume(self) -> int:
        return self.xa_elem.clipVolume()

    @property
    def repetition_method(self) -> XANumbersApplication.RepetitionMethod:
        return XANumbersApplication.RepetitionMethod(self.xa_elem.repetitionMethod())




class XANumbersShapeList(XANumbersiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersShape)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def background_fill_type(self) -> List[XANumbersApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XANumbersApplication.FillOption(x) for x in ls]

    def object_text(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("clipVolume")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_properties(self, properties: dict) -> 'XANumbersShape':
        return self.by_property("properties", properties)

    def by_background_fill_type(self, background_fill_type: XANumbersApplication.FillOption) -> 'XANumbersShape':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_object_text(self, object_text: XABase.XAText) -> 'XANumbersShape':
        return self.by_property("objectText", object_text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XANumbersShape':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XANumbersShape':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XANumbersShape':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XANumbersShape':
        return self.by_property("rotation", rotation)

class XANumbersShape(XANumbersiWorkItem):
    """A class for managing and interacting with shapes in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the shape
        self.background_fill_type: XANumbersApplication.FillOption #: The background, if any, for the shape
        self.object_text: str #: The text contained within the shape
        self.opacity: int #: The percent opacity of the object
        self.reflection_showing: bool #: Whether the iWork item displays a reflection
        self.reflection_value: int #: The percentage of relfection that the iWork item displays, from 0 to 100
        self.rotation: int #: The rotation of the iWork item, in degrees, from 0 to 359

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def background_fill_type(self) -> XANumbersApplication.FillOption:
        return XANumbersApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def object_text(self) -> str:
        return self.xa_elem.objectText()

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    def rotate(self, degrees: int) -> 'XANumbersShape':
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: XANumbersShape

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = NSValue.valueWithPoint_(NSPoint(value[0], value[1]))
        super().set_property(property_name, value)




class XANumbersChartList(XANumbersiWorkItemList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersChart)

class XANumbersChart(XANumbersiWorkItem):
    """A class for managing and interacting with charts in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)




class XANumbersLineList(XANumbersiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersLine)

    def end_point(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("end_point"))

    def reflection_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def start_point(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("start_point"))

    def by_end_point(self, end_point: Tuple[int, int]) -> 'XANumbersLine':
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XANumbersLine':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XANumbersLine':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XANumbersLine':
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: Tuple[int, int]) -> 'XANumbersLine':
        return self.by_property("startPoint", start_point)

class XANumbersLine(XANumbersiWorkItem):
    """A class for managing and interacting with lines in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.end_point: Tuple[int, int] #: A list of two numbers indicating the horizontal and vertical position of the line ending point
        self.reflection_showing: bool #: Whether the line displays a reflection
        self.reflection_value: int #: The reflection of reflection of the line, from 0 to 100
        self.rotation: int #: The rotation of the line, in degrees from 0 to 359
        self.start_point: Tuple[int, int] #: A list of two numbers indicating the horizontal and vertical position of the line starting point

    @property
    def end_point(self) -> Tuple[int, int]:
        return self.xa_elem.endPoint()

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @property
    def start_point(self) -> Tuple[int, int]:
        return self.xa_elem.startPoint()

    def rotate(self, degrees: int) -> 'XANumbersLine':
        """Rotates the line by the specified number of degrees.

        :param degrees: The amount to rotate the line, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: XANumbersLine

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> line = Numbers.current_document.lines()[0]
        >>> line.rotate(45)

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XANumbersMovieList(XANumbersiWorkItemList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersMovie)

    def file_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def movie_volume(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("movieVolume"))

    def opacity(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def reflection_value(self) -> List[XANumbersApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XANumbersApplication.RepetitionMethod(x) for x in ls]

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_file_name(self, file_name: str) -> 'XANumbersMovie':
        return self.by_property("fileName", file_name)

    def by_movie_volume(self, movie_volume: int) -> 'XANumbersMovie':
        return self.by_property("movieVolume", movie_volume)

    def by_opacity(self, opacity: int) -> 'XANumbersMovie':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XANumbersMovie':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XANumbersMovie':
        return self.by_property("reflectionValue", reflection_value)

    def by_repetition_method(self, repetition_method: XANumbersApplication.RepetitionMethod) -> 'XANumbersMovie':
        return self.by_property("repetitionMethod", repetition_method.value)

    def by_rotation(self, rotation: int) -> 'XANumbersMovie':
        return self.by_property("rotation", rotation)

class XANumbersMovie(XANumbersiWorkItem):
    """A class for managing and interacting with movie containers in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str #: The name of the movie file
        self.movie_volume: int #: The volume setting for the movie, from 0 to 100
        self.opacity: int #: The percent opacity of the object
        self.reflection_showing: bool #: Whether the movie displays a reflection
        self.reflection_value: int #: The percentage of reflection of the movie, from 0 to 100
        self.repetition_method: int #: If or how the movie repeat
        self.rotation: int #: The toation of the item, in degrees from 0 to 359

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName()

    @property
    def movie_volume(self) -> int:
        return self.xa_elem.moveVolume()

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @property
    def repetition_method(self) -> XANumbersApplication.RepetitionMethod:
        return XANumbersApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    def rotate(self, degrees: int) -> 'XANumbersMovie':
        """Rotates the movie by the specified number of degrees.

        :param degrees: The amount to rotate the movie, in degrees, from -359 to 359
        :type degrees: int
        :return: The movie object.
        :rtype: XANumbersMovie

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> movie = Numbers.current_document.movies()[0]
        >>> movie.rotate(45)

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XANumbersTextItemList(XANumbersiWorkItemList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersTextItem)

    def background_fill_type(self) -> List[XANumbersApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XANumbersApplication.FillOption(x) for x in ls]

    def text(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("text")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_background_fill_type(self, background_fill_type: XANumbersApplication.FillOption) -> 'XANumbersTextItem':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_text(self, text: XABase.XAText) -> 'XANumbersTextItem':
        return self.by_property("text", text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XANumbersTextItem':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XANumbersTextItem':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XANumbersTextItem':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XANumbersTextItem':
        return self.by_property("rotation", rotation)

class XANumbersTextItem(XANumbersiWorkItem):
    """A class for managing and interacting with text items in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: XANumbersApplication.FillOption #: The background of the text item
        self.text: XABase.XAText #: The text contained within the text item
        self.opacity: int #: The opacity of the text item
        self.reflection_showing: bool #: Whether the text item displays a reflection
        self.reflection_value: int #: The percentage of reflection of the text item, from 0 to 100
        self.rotation: int #: The rotation of the text item, in degrees from 0 to 359

    @property
    def background_fill_type(self) -> XANumbersApplication.FillOption:
        return XANumbersApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.text())

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    def rotate(self, degrees: int) -> 'XANumbersTextItem':
        """Rotates the text item by the specified number of degrees.

        :param degrees: The amount to rotate the text item, in degrees, from -359 to 359
        :type degrees: int
        :return: The text item object.
        :rtype: XANumbersTextItem

        :Example:

        >>> import PyXA
        >>> Numbers = PyXA.application("Numbers")
        >>> text = Numbers.current_document.text_items()[0]
        >>> text.rotate(45)

        .. versionadded:: 0.0.8
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XANumbersTableList(XANumbersiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersTable)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def row_count(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rowCount"))

    def column_count(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("columnCount"))

    def header_row_count(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("headerRowCount"))

    def header_column_count(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("headerColumnCount"))

    def footer_row_count(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("footerRowCount"))

    def cell_range(self) -> 'XANumbersRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XANumbersRangeList)

    def selection_range(self) -> 'XANumbersRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XANumbersRangeList)

    def by_name(self, name: str) -> 'XANumbersTable':
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> 'XANumbersTable':
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> 'XANumbersTable':
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> 'XANumbersTable':
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> 'XANumbersTable':
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> 'XANumbersTable':
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XANumbersRange') -> 'XANumbersTable':
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XANumbersRange') -> 'XANumbersTable':
        return self.by_property("selectionRange", selection_range.xa_elem)

class XANumbersTable(XANumbersiWorkItem):
    """A class for managing and interacting with tables in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the table
        self.row_count: int #: The number of rows in the table
        self.column_count: int #: The number of columns in the table
        self.header_row_count: int #: The number of header rows in the table
        self.header_column_count: int #: The number of header columns in the table
        self.footer_row_count: int #: The number of footer rows in the table
        self.cell_range: XANumbersRange #: The range of all cells in the table
        self.selection_range: XANumbersRange #: The currently selected cells
        self.filtered: bool #: Whether the table is currently filtered
        self.header_rows_frozen: bool #: Whether the header rows are frozen
        self.header_columns_frozen: bool #: Whether the header columns are frozen
    
    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def row_count(self) -> int:
        return self.xa_elem.rowCount()

    @property
    def column_count(self) -> int:
        return self.xa_elem.columnCount()

    @property
    def header_row_count(self) -> int:
        return self.xa_elem.headerRowCount()

    @property
    def header_column_count(self) -> int:
        return self.xa_elem.headerColumnCount()

    @property
    def footer_row_count(self) -> int:
        return self.xa_elem.footerRowCount()

    @property
    def cell_range(self) -> 'XANumbersRange':
        return self._new_element(self.xa_elem.cellRange(), XANumbersRange)

    @property
    def selection_range(self) -> 'XANumbersRange':
        return self._new_element(self.xa_elem.selectionRange(), XANumbersRange)

    @property
    def filtered(self) -> bool:
        return self.xa_elem.filtered()

    @property
    def header_rows_frozen(self) -> bool:
        return self.xa_elem.headerRowsFrozen()

    @property
    def header_columns_frozen(self) -> bool:
        return self.xa_elem.headerColumnsFrozen()

    # TODO
    def sort(self, columns: List['XANumbersColumn'], rows: List['XANumbersRow'], direction: XANumbersApplication.SortDirection = XANumbersApplication.SortDirection.ASCENDING) -> 'XANumbersTable':
        column_objs = [column.xa_elem for column in columns]
        row_objs = [row.xa_elem for row in rows]
        self.xa_elem.sortBy_direction_inRows_(column_objs[0], direction.value, row_objs)
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XANumbersCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XANumbersCell]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.cells(), XANumbersCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XANumbersColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XANumbersColumn]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.columns(), XANumbersColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XANumbersRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XANumbersRow]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.rows(), XANumbersRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> List['XANumbersRange']:
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: List[XANumbersRange]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.ranges(), XANumbersRangeList, filter)




class XANumbersRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XANumbersRange
        super().__init__(properties, obj_class, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def font_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def format(self) -> List[XANumbersApplication.CellFormat]:
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XANumbersApplication.CellFormat(x) for x in ls]

    def alignment(self) -> List[XANumbersApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XANumbersApplication.Alignment(x) for x in ls]

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def text_color(self) -> List[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("textColor")
        return [self._new_element(x, XABase.XAColor) for x in ls]

    def text_wrap(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("textWrap"))

    def background_color(self) -> List[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor")
        return [self._new_element(x, XABase.XAColor) for x in ls]

    def vertical_alignment(self) -> List[XANumbersApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XANumbersApplication.Alignment(x) for x in ls]

    def by_properties(self, properties: dict) -> 'XANumbersRange':
        return self.by_property("properties", properties)

    def by_font_name(self, font_name: str) -> 'XANumbersRange':
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> 'XANumbersRange':
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XANumbersApplication.CellFormat) -> 'XANumbersRange':
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XANumbersApplication.Alignment) -> 'XANumbersRange':
        return self.by_property("alignment", alignment.value)

    def by_name(self, name: str) -> 'XANumbersRange':
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> 'XANumbersRange':
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> 'XANumbersRange':
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> 'XANumbersRange':
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XANumbersApplication.Alignment) -> 'XANumbersRange':
        return self.by_property("verticalAlignment", vertical_alignment.value)

class XANumbersRange(XABase.XAObject):
    """A class for managing and interacting with ranges of table cells in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the range
        self.font_name: str #: The font of the range's cells
        self.font_size: float #: The font size of the range's cells
        self.format: XANumbersApplication.CellFormat #: The format of the range's cells
        self.alignment: XANumbersApplication.Alignment #: The horizontall alignment of content within the range's cells
        self.name: str #: The range's coordinates
        self.text_color: XABase.XAColor #: The text color of the range's cells
        self.text_wrap: bool #: Whether text within the range's cell sshould wrap
        self.background_color: XABase.XAColor #: The background color of the range's cells
        self.vertical_alignment: XANumbersApplication.Alignment #: The vertical alignment of content in the range's cells

    @property
    def properties(self) -> dict:
        return self.xa_elem.dict()

    @property
    def font_name(self) -> str:
        return self.xa_elem.fontName()

    @property
    def font_size(self) -> int:
        return self.xa_elem.fontSize()

    @property
    def format(self) -> XANumbersApplication.CellFormat:
        return XANumbersApplication.CellFormat(self.xa_elem.format())

    @property
    def alignment(self) -> XANumbersApplication.Alignment:
        return XANumbersApplication.Alignment(self.xa_elem.alighment())

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.textColor())

    @property
    def text_wrap(self) -> bool:
        return self.xa_elem.textWrap()

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @property
    def vertical_alignment(self) -> XANumbersApplication.Alignment:
        return XANumbersApplication.Alignment(self.xa_elem.verticalAlignment())

    def clear(self) -> 'XANumbersRange':
        """Clears the content of every cell in the range.

        :Example 1: Clear all cells in a table

        >>> import PyXA
        >>> app = PyXA.application("Numbers")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.clear()

        :Example 2: Clear all cells whose value is 3

        >>> import PyXA
        >>> app = PyXA.application("Numbers")
        >>> cells = app.document(0).slide(0).table(0).cells()
        >>> for cell in cells:
        >>>     if cell.value == 3:
        >>>         cell.clear()

        .. versionadded:: 0.0.8
        """
        self.xa_elem.clear()
        return self

    def merge(self) -> 'XANumbersRange':
        """Merges all cells in the range.

        :Example 1: Merge all cells in the first row of a table

        >>> import PyXA
        >>> app = PyXA.application("Numbers")
        >>> table = app.document(0).slide(0).table(0)
        >>> row = table.row(0)
        >>> row.merge()

        :Example 2: Merge all cells in the first column of a table

        >>> import PyXA
        >>> app = PyXA.application("Numbers")
        >>> table = app.document(0).slide(0).table(0)
        >>> col = table.column(0)
        >>> col.merge()

        .. note::

           If you merge an entire row, then merge an entire column, all cells in the table will be merged. The same is true if the row and column operations are flipped.

        .. versionadded:: 0.0.8
        """
        self.xa_elem.merge()
        return self

    def unmerge(self) -> 'XANumbersRange':
        """Unmerges all cells in the range.

        :Example 1: Unmerge all merged cells

        >>> import PyXA
        >>> app = PyXA.application("Numbers")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.unmerge()

        .. versionadded:: 0.0.8
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XANumbersCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XANumbersCell]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.cells(), XANumbersCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XANumbersColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XANumbersColumn]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.columns(), XANumbersColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XANumbersRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XANumbersRow]

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_elem.rows(), XANumbersRowList, filter)




class XANumbersRowList(XANumbersRangeList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersRow)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def by_address(self, address: float) -> 'XANumbersRow':
        return self.by_property("address", address)

    def by_height(self, height: int) -> 'XANumbersRow':
        return self.by_property("height", height)

class XANumbersRow(XANumbersRange):
    """A class for managing and interacting with table rows in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int #: The index of the row in the table
        self.height: float #: The height of the row in pixels

    @property
    def address(self) -> int:
        return self.xa_elem.address()

    @property
    def height(self) -> float:
        return self.xa_elem.height()




class XANumbersColumnList(XANumbersRangeList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersColumn)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_address(self, address: float) -> 'XANumbersColumn':
        return self.by_property("address", address)

    def by_width(self, width: int) -> 'XANumbersColumn':
        return self.by_property("width", width)

class XANumbersColumn(XANumbersRange):
    """A class for managing and interacting with table columns in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int #: The index of the column in the tabel
        self.width: float #: The width of the column in pixels

    @property
    def address(self) -> int:
        return self.xa_elem.address()

    @property
    def width(self) -> float:
        return self.xa_elem.width()




class XANumbersCellList(XANumbersRangeList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersCell)

    def formatted_value(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formattedValue"))

    def formula(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formula"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def column(self) -> XANumbersColumnList:
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XANumbersColumnList)

    def row(self) -> XANumbersRowList:
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XANumbersRowList)

    def by_formatted_value(self, formatted_value: str) -> 'XANumbersCell':
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> 'XANumbersCell':
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> 'XANumbersCell':
        return self.by_property("value", value)

    def by_column(self, column: XANumbersColumn) -> 'XANumbersCell':
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XANumbersRow) -> 'XANumbersCell':
        return self.by_property("row", row.xa_elem)

class XANumbersCell(XANumbersRange):
    """A class for managing and interacting with table cells in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.formatted_value: str #: The formatted form of the value stored in the cell
        self.formula: str #: The formula in the cell as text
        self.value: Any #: The value stored in the cell
        self.column: XANumbersColumn #: The cell's column
        self.row: XANumbersRow #: The cell's row

    @property
    def formatted_value(self) -> str:
        return self.xa_elem.formattedValue()

    @property
    def formula(self) -> str:
        return self.xa_elem.formula()

    @property
    def value(self) -> str:
        return self.xa_elem.value().get()

    @property
    def column(self) -> XANumbersColumn:
        return self._new_element(self.xa_elem.column(), XANumbersColumn)

    @property
    def row(self) -> XANumbersRow:
        return self._new_element(self.xa_elem.row(), XANumbersRow)