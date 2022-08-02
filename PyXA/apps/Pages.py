""".. versionadded:: 0.0.6

Control the macOS Pages application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, List, Tuple, Union
from AppKit import NSURL, NSSet, NSPoint, NSValue, NSMutableArray
from ScriptingBridge import SBElementArray

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XAPagesApplication(XABaseScriptable.XASBApplication, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with Pages.app.

    .. seealso:: :class:`XAPagesWindow`, :class:`XAPagesDocument`

    .. versionadded:: 0.0.6
    """
    class SaveOption(Enum):
        """Options for what to do when calling a save event.
        """
        SAVE_FILE   = OSType('yes ') #: Save the file. 
        DONT_SAVE   = OSType('no  ') #: Do not save the file. 
        ASK         = OSType('ask ') #: Ask the user whether or not to save the file. 

    class ExportFormat(Enum):
        """Options for what format to export a Pages project as.
        """
        Pages                   = OSType('Pgff') # The Pages native file format 
        EPUB                    = OSType('Pepu') # EPUB format
        PLAINTEXT               = OSType('Ptxf') # Plaintext format
        PDF                     = OSType('Ppdf') # PDF format
        MICROSOFT_WORD          = OSType('Pwrd') # MS Word format
        RTF                     = OSType('Prtf') # RTF format
        PAGES_09                = OSType('PPag') # Pages 09 format

    class PrintSetting(Enum):
        """Options to use when printing slides.
        """
        STANDARD_ERROR_HANDLING = OSType('lwst') # Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = OSType('lwdt') # print a detailed report of PostScript errors 

    class ImageQuality(Enum):
        """Options for the quality of exported images.
        """
        GOOD      = OSType('PgP0') # Good quality 
        BETTER    = OSType('PgP1') # Better quality 
        BEST      = OSType('PgP2') # Best quality 

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
        self.xa_wcls = XAPagesWindow

        self.properties: dict #: All properties of the application
        self.name: str #: The name of the Pages application
        self.frontmost: bool #: Whether Pages is the active application
        self.version: str #: The Pages version number
        self.current_document: XAPagesDocument #: The current document of the front window

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
    def current_document(self) -> 'XAPagesDocument':
        return self.front_window().document

    def print(self, item: Union['XAPagesDocument', XABaseScriptable.XASBWindow], print_properties: dict = None, show_dialog: bool = True) -> 'XAPagesApplication':
        """Prints a document or window.

        :param item: The document or window to print
        :type item: Union[XAPagesDocument, XABaseScriptable.XASBWindow]
        :param print_properties: The settings to pre-populate the print dialog with, defaults to None
        :type print_properties: dict, optional
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: A reference to the PyXA application object
        :rtype: XAPagesApplication

        .. versionadded:: 0.0.6
        """
        if print_properties is None:
            print_properties = {}
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, print_properties, show_dialog)
        return self

    def open(self, path: Union[str, NSURL]) -> 'XAPagesDocument':
            """Opens the file at the given filepath.

            :param target: The path of the file to open.
            :type target: Union[str, NSURL]
            :return: A reference to newly created document object
            :rtype: XAPagesDocument

            .. versionadded:: 0.0.6
            """
            if not isinstance(path, NSURL):
                path = XABase.XAPath(path)
            self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
            return self.documents()[0]

    def set_password(self, document: 'XAPagesDocument', password: str, hint: str, save_in_keychain: bool = True) -> 'XAPagesApplication':
        """Sets the password of an unencrypted document, optionally storing the password in the user's keychain.

        :param document: The document to set the password for
        :type document: XAPagesDocument
        :param password: The password
        :type password: str
        :param hint: A hint for the password
        :type hint: str
        :param save_in_keychain: Whether to save the password in the user's keychain, defaults to True
        :type save_in_keychain: bool, optional
        :return: A reference to the PyXA application object
        :rtype: XAPagesApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.setPassword_to_hint_savingInKeychain_(password, document.xa_elem, hint, save_in_keychain)
        return self

    def remove_password(self, document: 'XAPagesDocument', password: str) -> 'XAPagesApplication':
        """Removes the password from a document.

        :param document: The document to remove the password to
        :type document: XAPagesDocument
        :param password: The current password
        :type password: str
        :return: A reference to the PyXA application object
        :rtype: XAPagesApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.removePassword_from_(password, document.xa_elem)
        return self

    def new_page(self, document: 'XAPagesDocument', properties: dict = None) -> 'XAPagesPage':
        if properties is None:
            properties = {}
        return self.push("page", properties, document.xa_elem.pages())

    def documents(self, filter: Union[dict, None] = None) -> 'XAPagesDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: List[XAPagesDocument]

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XAPagesDocumentList, filter)

    def new_document(self, file_path: str = "./Untitled.key", template: 'XAPagesPage' = None) -> 'XAPagesDocument':
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        properties = {
            "file": file_path,
        }
        if template is not None:
            properties["documentTemplate"] = template.xa_elem
        return self.push("document", properties, self.xa_scel.documents())

    def templates(self, filter: Union[dict, None] = None) -> 'XAPagesTemplateList':
        """Returns a list of templates, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned templates will have, or None
        :type filter: Union[dict, None]
        :return: The list of templates
        :rtype: XAPagesTemplateList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.templates(), XAPagesTemplateList, filter)

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
        >>> pages = PyXA.application("Pages")
        >>> new_doc = pages.make("document", {"bodyText": "This is a whole new document!"})
        >>> pages.documents().push(new_doc)

        :Example 3: Making new elements on a page

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> new_line = pages.make("line", {"startPoint": (100, 100), "endPoint": (200, 200)})
        >>> pages.documents()[0].pages()[0].lines().push(new_line)

        .. versionadded:: 0.0.5
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XAPagesDocument)
        elif specifier == "shape":
            return self._new_element(obj, XAPagesShape)
        elif specifier == "table":
            return self._new_element(obj, XAPagesTable)
        elif specifier == "audioClip":
            return self._new_element(obj, XAPagesAudioClip)
        elif specifier == "chart":
            return self._new_element(obj, XAPagesChart)
        elif specifier == "image":
            return self._new_element(obj, XAPagesImage)
        elif specifier == "page":
            return self._new_element(obj, XAPagesPage)
        # elif specifier == "column":
        #     return self._new_element(obj, XAPagesColumn)
        # elif specifier == "row":
        #     return self._new_element(obj, XAPagesRow)
        elif specifier == "line":
            return self._new_element(obj, XAPagesLine)
        elif specifier == "movie":
            return self._new_element(obj, XAPagesMovie)
        elif specifier == "textItem":
            return self._new_element(obj, XAPagesTextItem)
        elif specifier == "group":
            return self._new_element(obj, XAPagesGroup)
        elif specifier == "iWorkItem":
            return self._new_element(obj, XAPagesiWorkItem)




class XAPagesWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Pages.app.

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
        self.document: XAPagesDocument #: The document currently displayed in the window

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
    def document(self) -> 'XAPagesDocument':
        return self._new_element(self.xa_elem.document(), XAPagesDocument)




class XAPagesDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesDocument, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def document_template(self) -> 'XAPagesTemplateList':
        ls = self.xa_elem.arrayByApplyingSelector_("documentTemplate")
        return self._new_element(ls, XAPagesTemplateList)

    def body_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyText"))

    def document_body(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("documentBody"))

    def facing_pages(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("facingPages"))

    def current_page(self) -> 'XAPagesPageList':
        ls = self.xa_elem.arrayByApplyingSelector_("currentPage")
        return self._new_element(ls, XAPagesPageList)

    def selection(self) -> 'XAPagesiWorkItemList':
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAPagesiWorkItemList)

    def password_protected(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> 'XAPagesDocument':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAPagesDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAPagesDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XAPagesDocument':
        return self.by_property("file", file)

    def by_id(self, id: str) -> 'XAPagesDocument':
        return self.by_property("id", id)

    def by_document_template(self, document_template: 'XAPagesTemplate') -> 'XAPagesDocument':
        return self.by_property("documentTemplate", document_template.xa_elem)

    def by_body_text(self, body_text: str) -> 'XAPagesDocument':
        return self.by_property("bodyText", body_text)

    def by_document_body(self, document_body: bool) -> 'XAPagesDocument':
        return self.by_property("documentBody", document_body)

    def by_facing_pages(self, facing_pages: bool) -> 'XAPagesDocument':
        return self.by_property("facingPages", facing_pages)

    def by_current_page(self, current_page: 'XAPagesPage') -> 'XAPagesDocument':
        return self.by_property("currentPage", current_page.xa_elem)

    def by_selection(self, selection: 'XAPagesiWorkItemList') -> 'XAPagesDocument':
        return self.by_property("selection", selection.xa_elem)

    def by_password_protected(self, password_protected: bool) -> 'XAPagesDocument':
        return self.by_property("passwordProtected", password_protected)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPagesDocument(XABase.XAHasElements, XABaseScriptable.XASBPrintable, XABaseScriptable.XASBCloseable, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with Pages documents.

    .. seealso:: :class:`XAPagesApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.file: str #: The location of the document on the disk, if one exists
        self.id: str #: The unique identifier for the document
        self.document_template: XAPagesTemplate #: The template assigned to the document
        self.body_text: str #: The document body text
        self.document_body: bool #: Whether the document has body text
        self.facing_pages: bool #: Whether the document has facing pages
        self.current_page: XAPagesPage #: The current page of the document
        self.selection: XAPagesiWorkItemList #: A list of the currently selected items
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
    def document_template(self) -> 'XAPagesTemplate':
        return self._new_element(self.xa_elem.documentTemplate(), XAPagesTemplate)

    @property
    def body_text(self) -> str:
        return self.xa_elem.bodyText()

    @property
    def document_body(self) -> bool:
        return self.xa_elem.documentBody()

    @property
    def facing_pages(self) -> str:
        return self.xa_elem.facingPages()

    @property
    def current_page(self) -> 'XAPagesPage':
        return self._new_element(self.xa_elem.currentPage(), XAPagesPage)

    @property
    def selection(self) -> 'XAPagesiWorkItemList':
        return self._new_element(self.xa_elem.selection(), XAPagesiWorkItemList)

    @property
    def password_protected(self) -> bool:
        return self.xa_elem.passwordProtected()

    def export(self, file_path: Union[str, NSURL] = None, format: XAPagesApplication.ExportFormat = XAPagesApplication.ExportFormat.PDF):
        """Exports the document in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, NSURL], optional
        :param format: The format to export the file in, defaults to XAPagesApplication.ExportFormat.PDF
        :type format: XAPagesApplication.ExportFormat, optional

        .. versionadded:: 0.0.3
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path, format.value, None)

    def new_page(self, properties: dict = None) -> 'XAPagesPage':
        """Creates a new page at the end of the document.

        :param properties: The properties to give the new page
        :type properties: dict
        :return: A reference to the newly created page object
        :rtype: XAPagesPage

        .. versionadded:: 0.0.6
        """
        return self.xa_prnt.xa_prnt.new_page(self, properties)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.audioClips(), XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.charts(), XAPagesChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.groups(), XAPagesGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XAPagesImageList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.images(), XAPagesImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAPagesiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.lines(), XAPagesLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.movies(), XAPagesMovieList, filter)

    def pages(self, filter: Union[dict, None] = None) -> 'XAPagesPageList':
        """Returns a list of pages, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned pages will have, or None
        :type filter: Union[dict, None]
        :return: The list of pages
        :rtype: XAPagesPageList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.pages(), XAPagesPageList, filter)

    def sections(self, filter: Union[dict, None] = None) -> 'XAPagesSectionList':
        """Returns a list of sections, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sections will have, or None
        :type filter: Union[dict, None]
        :return: The list of sections
        :rtype: XAPagesSectionList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.sections(), XAPagesSectionList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.shapes(), XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.tables(), XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns a list of text items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.textItems(), XAPagesTextItemList, filter)

    def placeholder_texts(self, filter: Union[dict, None] = None) -> 'XAPagesPlaceholderTextList':
        """Returns a list of placeholder texts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned placeholder texts will have, or None
        :type filter: Union[dict, None]
        :return: The list of placeholder texts
        :rtype: XAPagesPlaceholderTextList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.placeholderTexts(), XAPagesPlaceholderTextList, filter)




class XAPagesTemplateList(XABase.XAList):
    """A wrapper around lists of templates that employs fast enumeration techniques.

    All properties of templates can be called as methods on the wrapped list, returning a list containing each template's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesTemplate, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XAPagesTemplate':
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAPagesTemplate':
        return self.by_property("name", name)

    def __repr__(self):
        return f"<{str(type(self))}{self.name}>"

class XAPagesTemplate(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Pages templates.

    .. seealso:: :class:`XAPagesApplication`

    .. versionadded:: 0.0.6
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




class XAPagesSectionList(XABase.XAList):
    """A wrapper around lists of sections that employs fast enumeration techniques.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesSection, filter)

    def body_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyText"))

    def by_body_text(self, body_text: str) -> 'XAPagesSection':
        return self.by_property("bodyText", body_text)

class XAPagesSection(XABase.XAHasElements):
    """A class for managing and interacting with sections in Pages.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.body_text: str #: The section body text

    @property
    def body_text(self) -> str:
        return self.xa_elem.bodyText()




class XAPagesContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesContainer, filter)

class XAPagesContainer(XABase.XAHasElements):
    """A class for managing and interacting with containers in Pages.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def iwork_items(self, filter: Union[dict, None] = None) -> List['XAPagesiWorkItem']:
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: List[XAPagesiWorkItem]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAPagesiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> List['XAPagesAudioClip']:
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: List[XAPagesAudioClip]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> List['XAPagesChart']:
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: List[XAPagesChart]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), XAPagesChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> List['XAPagesImage']:
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: List[XAPagesImage]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), XAPagesImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> List['XAPagesGroup']:
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: List[XAPagesGroup]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), XAPagesGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> List['XAPagesLine']:
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: List[XAPagesLine]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), XAPagesLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> List['XAPagesMovie']:
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: List[XAPagesMovie]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), XAPagesMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> List['XAPagesShape']:
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: List[XAPagesShape]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> List['XAPagesTable']:
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: List[XAPagesTable]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> List['XAPagesTextItem']:
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: List[XAPagesTextItem]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), XAPagesTextItemList, filter)




class XAPagesPageList(XABase.XAList):
    """A wrapper around lists of pages that employs fast enumeration techniques.

    All properties of pages can be called as methods on the wrapped list, returning a list containing each page's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesPage, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def body_text(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyText"))

    def by_properties(self, properties: dict) -> 'XAPagesPage':
        return self.by_property("properties", properties)

    def by_body_text(self, body_text: str) -> 'XAPagesPage':
        return self.by_property("bodyText", body_text)

class XAPagesPage(XAPagesContainer):
    """A class for managing and interacting with pages in Pages documents.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the slide
        self.body_text: str #: The page body text

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def body_text(self) -> str:
        return self.xa_elem.bodyText()

    # def duplicate(self) -> 'XAPagesPage':
    #     """Duplicates the page, mimicking the action of copying and pasting the page manually.

    #     :return: A reference to the PyXA page object that called this command.
    #     :rtype: XAPagesPage

    #     .. versionadded:: 0.0.6
    #     """
    #     new_page = self.xa_prnt.xa_prnt.xa_prnt.xa_prnt.make("page", {})
    #     self.xa_prnt.xa_prnt.pages().push(new_page)
    #     for item in self.xa_elem.lines():
    #         print("ya")
    #         item.duplicateTo_withProperties_(new_page.xa_elem.lines()[0].positionAfter(), None)
    #     return self

    # def move_to(self, document):
    #     self.xa_elem.moveTo_(document.xa_elem.pages())

    # def delete(self):
    #     """Deletes the page.

    #     .. versionadded:: 0.0.6
    #     """
    #     self.xa_elem.get().delete()

    def add_image(self, file_path: Union[str, NSURL]) -> 'XAPagesImage':
        """Adds the image at the specified path to the slide.

        :param file_path: The path to the image file.
        :type file_path: Union[str, NSURL]
        :return: The newly created image object.
        :rtype: XAPagesImage

        .. versionadded:: 0.0.6
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

    # def add_chart(self, row_names: List[str], column_names: List[str], data: List[List[Any]], type: int = XAPagesApplication.ChartType.LINE_2D.value, group_by: int = XAPagesApplication.ChartGrouping.ROW.value) -> 'XAPagesChart':
    #     """_summary_

    #     _extended_summary_

    #     :param row_names: A list of row names.
    #     :type row_names: List[str]
    #     :param column_names: A list of column names.
    #     :type column_names: List[str]
    #     :param data: A 2d array 
    #     :type data: List[List[Any]]
    #     :param type: The chart type, defaults to _PagesLegacyChartType.PagesLegacyChartTypeLine_2d.value
    #     :type type: int, optional
    #     :param group_by: The grouping schema, defaults to _PagesLegacyChartGrouping.PagesLegacyChartGroupingChartRow.value
    #     :type group_by: int, optional
    #     :return: A reference to the newly created chart object.
    #     :rtype: XAPagesChart

    #     .. versionadded:: 0.0.2
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
    #     return XAPagesChart(properties)




class XAPagesiWorkItemList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesiWorkItem, filter)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def locked(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def parent(self) -> XAPagesContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAPagesContainerList)

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def by_height(self, height: int) -> 'XAPagesiWorkItem':
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> 'XAPagesiWorkItem':
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> 'XAPagesiWorkItem':
        return self.by_property("width", width)

    def by_parent(self, parent: XAPagesContainer) -> 'XAPagesiWorkItem':
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: Tuple[int, int]) -> 'XAPagesiWorkItem':
        return self.by_property("position", position)

class XAPagesiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Pages.

    .. seealso:: :class:`XAPagesApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict
        self.height: int #: The height of the iWork item
        self.locked: bool #: Whether the object is locked
        self.width: int #: The width of the iWork item
        self.parent: XAPagesContainer #: The iWork container that contains the iWork item
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
    def parent(self) -> XAPagesContainer:
        return self._new_element(self.xa_elem.parent(), XAPagesContainer)

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.delete()

    def duplicate(self) -> 'XAPagesiWorkItem':
        """Duplicates the item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAPagesiWorkItem

        .. versionadded:: 0.0.2
        """
        self.xa_elem.duplicateTo_withProperties_(self.parent.xa_elem.iWorkItems(), None)
        return self

    def resize(self, width: int, height: int) -> 'XAPagesiWorkItem':
        """Sets the width and height of the item.

        :param width: The desired width, in pixels
        :type width: int
        :param height: The desired height, in pixels
        :type height: int
        :return: The iWork item
        :rtype: XAPagesiWorkItem

        .. versionadded:: 0.0.6
        """
        self.set_properties({
            "width": width,
            "height": height,
        })
        return self

    def lock(self) -> 'XAPagesiWorkItem':
        """Locks the properties of the item, preventing changes.

        :return: The iWork item
        :rtype: XAPagesiWorkItem

        .. versionadded:: 0.0.6
        """
        self.set_property("locked", True)
        return self

    def unlock(self) -> 'XAPagesiWorkItem':
        """Unlocks the properties of the item, allowing changes.

        :return: The iWork item
        :rtype: XAPagesiWorkItem

        .. versionadded:: 0.0.6
        """
        self.set_property("locked", False)
        return self

    def set_position(self, x: int, y: int) -> 'XAPagesiWorkItem':
        position = NSValue.valueWithPoint_(NSPoint(x, y))
        self.xa_elem.setValue_forKey_(position, "position")





class XAPagesGroupList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesGroup, filter)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def parent(self) -> XAPagesContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAPagesContainerList)

    def by_height(self, height: int) -> 'XAPagesGroup':
        return self.by_property("height", height)

    def by_position(self, position: Tuple[int, int]) -> 'XAPagesGroup':
        return self.by_property("position", position)

    def by_width(self, width: int) -> 'XAPagesGroup':
        return self.by_property("width", width)

    def by_rotation(self, rotation: int) -> 'XAPagesGroup':
        return self.by_property("rotation", rotation)

    def by_parent(self, parent: XAPagesContainer) -> 'XAPagesGroup':
        return self.by_property("parent", parent.xa_elem)

class XAPagesGroup(XAPagesContainer):
    """A class for managing and interacting with iWork item groups in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int #: The height of the group
        self.position: Tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the group
        self.width: int #: The widht of the group
        self.rotation: int #: The rotation of the group, in degrees from 0 to 359
        self.parent: XAPagesContainer #: The container which contains the group

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
    def parent(self) -> XAPagesContainer:
        return self._new_element(self.xa_elem.parent(), XAPagesContainer)

    def rotate(self, degrees: int) -> 'XAPagesGroup':
        """Rotates the group by the specified number of degrees.

        :param degrees: The amount to rotate the group, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: XAPagesGroup

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> group = pages.current_document.groups()[0]
        >>> group.rotate(45)

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesImageList(XABase.XAList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesImage, filter)

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

    def by_object_description(self, object_description: str) -> 'XAPagesImage':
        return self.by_property("objectDescription", object_description)

    def by_file(self, file: str) -> 'XAPagesImage':
        return self.by_property("file", file)

    def by_file_name(self, file_name: str) -> 'XAPagesImage':
        return self.by_property("fileName", file_name)

    def by_opacity(self, opacity: int) -> 'XAPagesImage':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAPagesImage':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAPagesImage':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAPagesImage':
        return self.by_property("rotation", rotation)

class XAPagesImage(XAPagesiWorkItem):
    """A class for managing and interacting with images in Pages.

    .. versionadded:: 0.0.2
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

    def rotate(self, degrees: int) -> 'XAPagesImage':
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: XAPagesImage

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> page = pages.documents()[0].pages()[0]
        >>> img = page.add_image("/Users/steven/Documents/idk/idk.001.png")
        >>> img.rotate(30)
        >>> img.rotate(60)  # Rotated 60+30
        >>> img.rotate(90)  # Rotated 90+90
        >>> img.rotate(180) # Rotated 180+180

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, NSURL]) -> 'XAPagesImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, NSURL]
        :return: A reference to the new PyXA image object.
        :rtype: XAPagesImage

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> page = pages.documents()[0].pages()[0]
        >>> img = page.add_image("/Users/exampleuser/Documents/Images/Test1.png")
        >>> sleep(1)
        >>> img.replace_with("/Users/exampleuser/Documents/Images/Test2.png")

        .. versionadded:: 0.0.6
        """
        self.delete()
        if isinstance(self.xa_prnt.xa_prnt, XAPagesPage):
            return self.xa_prnt.xa_prnt.add_image(img_path)
        return self.xa_prnt.add_image(img_path)




class XAPagesAudioClipList(XABase.XAList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesAudioClip, filter)

    def file_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> List[XAPagesApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAPagesApplication.RepetitionMethod(x) for x in ls]

    def by_file_name(self, file_name: str) -> 'XAPagesAudioClip':
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> 'XAPagesAudioClip':
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod) -> 'XAPagesAudioClip':
        return self.by_property("repetitionMethod", repetition_method.value)

class XAPagesAudioClip(XAPagesiWorkItem):
    """A class for managing and interacting with audio clips in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str #: The name of the audio file
        self.clip_volume: int #: The volume setting for the audio clip, from 0 to 100
        self.repetition_method: XAPagesApplication.RepetitionMethod #: Whether or how the audio clip  repeats

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName()

    @property
    def clip_volume(self) -> int:
        return self.xa_elem.clipVolume()

    @property
    def repetition_method(self) -> XAPagesApplication.RepetitionMethod:
        return XAPagesApplication.RepetitionMethod(self.xa_elem.repetitionMethod())




class XAPagesShapeList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesShape, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def background_fill_type(self) -> List[XAPagesApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAPagesApplication.FillOption(x) for x in ls]

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

    def by_properties(self, properties: dict) -> 'XAPagesShape':
        return self.by_property("properties", properties)

    def by_background_fill_type(self, background_fill_type: XAPagesApplication.FillOption) -> 'XAPagesShape':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_object_text(self, object_text: XABase.XAText) -> 'XAPagesShape':
        return self.by_property("objectText", object_text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XAPagesShape':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAPagesShape':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAPagesShape':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAPagesShape':
        return self.by_property("rotation", rotation)

class XAPagesShape(XAPagesiWorkItem):
    """A class for managing and interacting with shapes in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the shape
        self.background_fill_type: XAPagesApplication.FillOption #: The background, if any, for the shape
        self.object_text: str #: The text contained within the shape
        self.opacity: int #: The percent opacity of the object
        self.reflection_showing: bool #: Whether the iWork item displays a reflection
        self.reflection_value: int #: The percentage of relfection that the iWork item displays, from 0 to 100
        self.rotation: int #: The rotation of the iWork item, in degrees, from 0 to 359

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def background_fill_type(self) -> XAPagesApplication.FillOption:
        return XAPagesApplication.FillOption(self.xa_elem.backgroundFillType())

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

    def rotate(self, degrees: int) -> 'XAPagesShape':
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: XAPagesShape

        .. versionadded:: 0.0.2
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = NSValue.valueWithPoint_(NSPoint(value[0], value[1]))
        super().set_property(property_name, value)




class XAPagesChartList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesChart, filter)

class XAPagesChart(XAPagesiWorkItem):
    """A class for managing and interacting with charts in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAPagesLineList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesLine, filter)

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

    def by_end_point(self, end_point: Tuple[int, int]) -> 'XAPagesLine':
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAPagesLine':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAPagesLine':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAPagesLine':
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: Tuple[int, int]) -> 'XAPagesLine':
        return self.by_property("startPoint", start_point)

class XAPagesLine(XAPagesiWorkItem):
    """A class for managing and interacting with lines in Pages.

    .. versionadded:: 0.0.2
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

    def rotate(self, degrees: int) -> 'XAPagesLine':
        """Rotates the line by the specified number of degrees.

        :param degrees: The amount to rotate the line, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: XAPagesLine

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> line = pages.current_document.lines()[0]
        >>> line.rotate(45)

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesMovieList(XABase.XAList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesMovie, filter)

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

    def reflection_value(self) -> List[XAPagesApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAPagesApplication.RepetitionMethod(x) for x in ls]

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_file_name(self, file_name: str) -> 'XAPagesMovie':
        return self.by_property("fileName", file_name)

    def by_movie_volume(self, movie_volume: int) -> 'XAPagesMovie':
        return self.by_property("movieVolume", movie_volume)

    def by_opacity(self, opacity: int) -> 'XAPagesMovie':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAPagesMovie':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAPagesMovie':
        return self.by_property("reflectionValue", reflection_value)

    def by_repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod) -> 'XAPagesMovie':
        return self.by_property("repetitionMethod", repetition_method.value)

    def by_rotation(self, rotation: int) -> 'XAPagesMovie':
        return self.by_property("rotation", rotation)

class XAPagesMovie(XAPagesiWorkItem):
    """A class for managing and interacting with movie containers in Pages.

    .. versionadded:: 0.0.2
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
    def repetition_method(self) -> XAPagesApplication.RepetitionMethod:
        return XAPagesApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    def rotate(self, degrees: int) -> 'XAPagesMovie':
        """Rotates the movie by the specified number of degrees.

        :param degrees: The amount to rotate the movie, in degrees, from -359 to 359
        :type degrees: int
        :return: The movie object.
        :rtype: XAPagesMovie

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> movie = pages.current_document.movies()[0]
        >>> movie.rotate(45)

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesTextItemList(XABase.XAList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesTextItem, filter)

    def background_fill_type(self) -> List[XAPagesApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAPagesApplication.FillOption(x) for x in ls]

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

    def by_background_fill_type(self, background_fill_type: XAPagesApplication.FillOption) -> 'XAPagesTextItem':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_text(self, text: XABase.XAText) -> 'XAPagesTextItem':
        return self.by_property("text", text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XAPagesTextItem':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAPagesTextItem':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAPagesTextItem':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAPagesTextItem':
        return self.by_property("rotation", rotation)

class XAPagesTextItem(XAPagesiWorkItem):
    """A class for managing and interacting with text items in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: XAPagesApplication.FillOption #: The background of the text item
        self.text: XABase.XAText #: The text contained within the text item
        self.opacity: int #: The opacity of the text item
        self.reflection_showing: bool #: Whether the text item displays a reflection
        self.reflection_value: int #: The percentage of reflection of the text item, from 0 to 100
        self.rotation: int #: The rotation of the text item, in degrees from 0 to 359

    @property
    def background_fill_type(self) -> XAPagesApplication.FillOption:
        return XAPagesApplication.FillOption(self.xa_elem.backgroundFillType())

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

    def rotate(self, degrees: int) -> 'XAPagesTextItem':
        """Rotates the text item by the specified number of degrees.

        :param degrees: The amount to rotate the text item, in degrees, from -359 to 359
        :type degrees: int
        :return: The text item object.
        :rtype: XAPagesTextItem

        :Example:

        >>> import PyXA
        >>> pages = PyXA.application("Pages")
        >>> text = pages.current_document.text_items()[0]
        >>> text.rotate(45)

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesPlaceholderTextList(XABase.XATextList):
    """A wrapper around lists of placeholder texts that employs fast enumeration techniques.

    All properties of placeholder texts can be called as methods on the wrapped list, returning a list containing each text's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesTextItem, filter)

    def background_fill_type(self) -> List[XAPagesApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAPagesApplication.FillOption(x) for x in ls]

class XAPagesPlaceholderText(XABase.XAText):
    """A class for managing and interacting with placeholder texts in Pages.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.tag: str #: The placeholder text's script tag

    @property
    def tag(self) -> str:
        return self.xa_elem.tag()





class XAPagesTableList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesTable, filter)

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

    def cell_range(self) -> 'XAPagesRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XAPagesRangeList)

    def selection_range(self) -> 'XAPagesRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XAPagesRangeList)

    def by_name(self, name: str) -> 'XAPagesTable':
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> 'XAPagesTable':
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> 'XAPagesTable':
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> 'XAPagesTable':
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> 'XAPagesTable':
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> 'XAPagesTable':
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XAPagesRange') -> 'XAPagesTable':
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XAPagesRange') -> 'XAPagesTable':
        return self.by_property("selectionRange", selection_range.xa_elem)

class XAPagesTable(XAPagesiWorkItem):
    """A class for managing and interacting with tables in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the table
        self.row_count: int #: The number of rows in the table
        self.column_count: int #: The number of columns in the table
        self.header_row_count: int #: The number of header rows in the table
        self.header_column_count: int #: The number of header columns in the table
        self.footer_row_count: int #: The number of footer rows in the table
        self.cell_range: XAPagesRange #: The range of all cells in the table
        self.selection_range: XAPagesRange #: The currently selected cells
    
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
    def cell_range(self) -> 'XAPagesRange':
        return self._new_element(self.xa_elem.cellRange(), XAPagesRange)

    @property
    def selection_range(self) -> 'XAPagesRange':
        return self._new_element(self.xa_elem.selectionRange(), XAPagesRange)

    # TODO
    def sort(self, columns: List['XAPagesColumn'], rows: List['XAPagesRow'], direction: XAPagesApplication.SortDirection = XAPagesApplication.SortDirection.ASCENDING) -> 'XAPagesTable':
        column_objs = [column.xa_elem for column in columns]
        row_objs = [row.xa_elem for row in rows]
        self.xa_elem.sortBy_direction_inRows_(column_objs[0], direction.value, row_objs)
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XAPagesCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAPagesCell]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAPagesCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XAPagesColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAPagesColumn]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAPagesColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XAPagesRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAPagesRow]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAPagesRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> List['XAPagesRange']:
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: List[XAPagesRange]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.ranges(), XAPagesRangeList, filter)




class XAPagesRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesRange, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def font_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def format(self) -> List[XAPagesApplication.CellFormat]:
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAPagesApplication.CellFormat(x) for x in ls]

    def alignment(self) -> List[XAPagesApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XAPagesApplication.Alignment(x) for x in ls]

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

    def vertical_alignment(self) -> List[XAPagesApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XAPagesApplication.Alignment(x) for x in ls]

    def by_properties(self, properties: dict) -> 'XAPagesRange':
        return self.by_property("properties", properties)

    def by_font_name(self, font_name: str) -> 'XAPagesRange':
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> 'XAPagesRange':
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XAPagesApplication.CellFormat) -> 'XAPagesRange':
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XAPagesApplication.Alignment) -> 'XAPagesRange':
        return self.by_property("alignment", alignment.value)

    def by_name(self, name: str) -> 'XAPagesRange':
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> 'XAPagesRange':
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> 'XAPagesRange':
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> 'XAPagesRange':
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XAPagesApplication.Alignment) -> 'XAPagesRange':
        return self.by_property("verticalAlignment", vertical_alignment.value)

class XAPagesRange(XABase.XAHasElements):
    """A class for managing and interacting with ranges of table cells in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the range
        self.font_name: str #: The font of the range's cells
        self.font_size: float #: The font size of the range's cells
        self.format: XAPagesApplication.CellFormat #: The format of the range's cells
        self.alignment: XAPagesApplication.Alignment #: The horizontall alignment of content within the range's cells
        self.name: str #: The range's coordinates
        self.text_color: XABase.XAColor #: The text color of the range's cells
        self.text_wrap: bool #: Whether text within the range's cell sshould wrap
        self.background_color: XABase.XAColor #: The background color of the range's cells
        self.vertical_alignment: XAPagesApplication.Alignment #: The vertical alignment of content in the range's cells

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
    def format(self) -> XAPagesApplication.CellFormat:
        return XAPagesApplication.CellFormat(self.xa_elem.format())

    @property
    def alignment(self) -> XAPagesApplication.Alignment:
        return XAPagesApplication.Alignment(self.xa_elem.alighment())

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
    def vertical_alignment(self) -> XAPagesApplication.Alignment:
        return XAPagesApplication.Alignment(self.xa_elem.verticalAlignment())

    def clear(self) -> 'XAPagesRange':
        """Clears the content of every cell in the range.

        :Example 1: Clear all cells in a table

        >>> import PyXA
        >>> app = PyXA.application("Pages")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.clear()

        :Example 2: Clear all cells whose value is 3

        >>> import PyXA
        >>> app = PyXA.application("Pages")
        >>> cells = app.document(0).slide(0).table(0).cells()
        >>> for cell in cells:
        >>>     if cell.value == 3:
        >>>         cell.clear()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.clear()
        return self

    def merge(self) -> 'XAPagesRange':
        """Merges all cells in the range.

        :Example 1: Merge all cells in the first row of a table

        >>> import PyXA
        >>> app = PyXA.application("Pages")
        >>> table = app.document(0).slide(0).table(0)
        >>> row = table.row(0)
        >>> row.merge()

        :Example 2: Merge all cells in the first column of a table

        >>> import PyXA
        >>> app = PyXA.application("Pages")
        >>> table = app.document(0).slide(0).table(0)
        >>> col = table.column(0)
        >>> col.merge()

        .. note::

           If you merge an entire row, then merge an entire column, all cells in the table will be merged. The same is true if the row and column operations are flipped.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.merge()
        return self

    def unmerge(self) -> 'XAPagesRange':
        """Unmerges all cells in the range.

        :Example 1: Unmerge all merged cells

        >>> import PyXA
        >>> app = PyXA.application("Pages")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.unmerge()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XAPagesCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAPagesCell]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAPagesCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XAPagesColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAPagesColumn]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAPagesColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XAPagesRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAPagesRow]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAPagesRowList, filter)




class XAPagesRowList(XABase.XAList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesRow, filter)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_address(self, address: float) -> 'XAPagesRow':
        return self.by_property("address", address)

    def by_width(self, width: int) -> 'XAPagesRow':
        return self.by_property("width", width)

class XAPagesRow(XAPagesRange):
    """A class for managing and interacting with table rows in Pages.

    .. versionadded:: 0.0.2
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




class XAPagesColumnList(XABase.XAList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesColumn, filter)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_address(self, address: float) -> 'XAPagesColumn':
        return self.by_property("address", address)

    def by_width(self, width: int) -> 'XAPagesColumn':
        return self.by_property("width", width)

class XAPagesColumn(XAPagesRange):
    """A class for managing and interacting with table columns in Pages.

    .. versionadded:: 0.0.2
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




class XAPagesCellList(XABase.XAList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesCell, filter)

    def formatted_value(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formattedValue"))

    def formula(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formula"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def column(self) -> XAPagesColumnList:
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XAPagesColumnList)

    def row(self) -> XAPagesRowList:
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XAPagesRowList)

    def by_formatted_value(self, formatted_value: str) -> 'XAPagesCell':
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> 'XAPagesCell':
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> 'XAPagesCell':
        return self.by_property("value", value)

    def by_column(self, column: XAPagesColumn) -> 'XAPagesCell':
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XAPagesRow) -> 'XAPagesCell':
        return self.by_property("row", row.xa_elem)

class XAPagesCell(XAPagesRange):
    """A class for managing and interacting with table cells in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.formatted_value: str #: The formatted form of the value stored in the cell
        self.formula: str #: The formula in the cell as text
        self.value: Any #: The value stored in the cell
        self.column: XAPagesColumn #: The cell's column
        self.row: XAPagesRow #: The cell's row

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
    def column(self) -> XAPagesColumn:
        return self._new_element(self.xa_elem.column(), XAPagesColumn)

    @property
    def row(self) -> XAPagesRow:
        return self._new_element(self.xa_elem.row(), XAPagesRow)