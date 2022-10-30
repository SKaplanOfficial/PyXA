""".. versionadded:: 0.0.6

Control the macOS Pages application using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from time import sleep
from typing import Any, Union, Self

import AppKit, ScriptingBridge
import logging
from ScriptingBridge import SBElementArray

from PyXA import XABase, XAEvents
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACloseable

logger = logging.getLogger("pages")

class XAPagesApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Pages.app.

    .. seealso:: :class:`XAPagesWindow`, :class:`XAPagesDocument`

    .. versionadded:: 0.0.6
    """
    class ExportFormat(Enum):
        """Options for what format to export a Pages project as.
        """
        Pages                   = OSType('Pgff') #: The Pages native file format 
        EPUB                    = OSType('Pepu') #: EPUB format
        PLAINTEXT               = OSType('Ptxf') #: Plaintext format
        PDF                     = OSType('Ppdf') #: PDF format
        MICROSOFT_WORD          = OSType('Pwrd') #: MS Word format
        RTF                     = OSType('Prtf') #: RTF format
        PAGES_09                = OSType('PPag') #: Pages 09 format

    class ImageQuality(Enum):
        """Options for the quality of exported images.
        """
        GOOD      = OSType('PgP0') #: Good quality 
        BETTER    = OSType('PgP1') #: Better quality 
        BEST      = OSType('PgP2') #: Best quality 

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
        return dict(self.xa_scel.properties())

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
        return self.front_window.document

    def print(self, item: Union['XAPagesDocument', XABaseScriptable.XASBWindow], print_properties: dict = None, show_dialog: bool = True) -> Self:
        """Prints a document or window.

        :param item: The document or window to print
        :type item: Union[XAPagesDocument, XABaseScriptable.XASBWindow]
        :param print_properties: The settings to pre-populate the print dialog with, defaults to None
        :type print_properties: dict, optional
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: A reference to the PyXA application object
        :rtype: Self

        .. versionadded:: 0.0.6
        """
        if print_properties is None:
            print_properties = {}
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, print_properties, show_dialog)
        return self

    def open(self, path: Union[str, XABase.XAPath]) -> 'XAPagesDocument':
            """Opens the file at the given filepath.

            :param target: The path of the file to open.
            :type target: Union[str, XABase.XAPath]
            :return: A reference to newly created document object
            :rtype: XAPagesDocument

            .. versionadded:: 0.0.6
            """
            if isinstance(path, str):
                path = XABase.XAPath(path)
            self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
            sleep(0.1)
            return self.documents()[0]

    def set_password(self, document: 'XAPagesDocument', password: str, hint: str, save_in_keychain: bool = True) -> Self:
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
        :rtype: Self

        .. versionadded:: 0.0.6
        """
        self.xa_scel.setPassword_to_hint_savingInKeychain_(password, document.xa_elem, hint, save_in_keychain)
        return self

    def remove_password(self, document: 'XAPagesDocument', password: str) -> Self:
        """Removes the password from a document.

        :param document: The document to remove the password to
        :type document: XAPagesDocument
        :param password: The current password
        :type password: str
        :return: A reference to the PyXA application object
        :rtype: Self

        .. versionadded:: 0.0.6
        """
        self.xa_scel.removePassword_from_(password, document.xa_elem)
        return self

    def documents(self, filter: Union[dict, None] = None) -> 'XAPagesDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAPagesDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XAPagesDocumentList, filter)

    def new_document(self, file_path: str = "./Untitled.key", template: 'XAPagesPage' = None) -> 'XAPagesDocument':
        """Creates a new document with the specified properties.

        :param file_path: The path to create the document at, defaults to "./Untitled.key"
        :type file_path: str, optional
        :param template: The template to initialize the document from, defaults to None
        :type template: XAPagesPage, optional
        :return: The newly created document object
        :rtype: XAPagesDocument

        .. versionadded:: 0.0.6
        """
        if isinstance(file_path, str):
            file_path = AppKit.NSURL.alloc().initFileURLWithPath_(file_path)
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
        >>> pages = PyXA.Application("Pages")
        >>> new_doc = pages.make("document", {"bodyText": "This is a whole new document!"})
        >>> pages.documents().push(new_doc)

        :Example 3: Making new elements on a page

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
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




class XAPagesWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject):
    """A class for managing and interacting with windows in Pages.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle of the window
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
    def document(self) -> 'XAPagesDocument':
        return self._new_element(self.xa_elem.document(), XAPagesDocument)




class XAPagesDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesDocument, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, doc in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "id": raw_dicts[index]["id"],
                "current_page": self._new_element(raw_dicts[index]["currentPage"], XAPagesDocument),
                "file": XABase.XAPath(raw_dicts[index]["file"]),
                "modified": raw_dicts[index]["modified"],
                "document_body": raw_dicts[index]["documentBody"],
                "document_template": self._new_element(raw_dicts[index]["documentTemplate"], XAPagesTemplate),
                "body_text": raw_dicts[index]["bodyText"],
                "facing_pages": raw_dicts[index]["facingPages"],
                "selection": self._new_element(raw_dicts[index]["selection"], XAPagesiWorkItemList),
                "name": raw_dicts[index]["name"],
                "password_protected": raw_dicts[index]["passwordProtected"]
            }
        return pyxa_dicts

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status booleans 
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[XABase.XAPath]:
        """Gets the file URL of each document in the list.

        :return: A list of document file URLs
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> list[str]:
        """Gets the ID of each document in the list.

        :return: A list of document IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def document_template(self) -> 'XAPagesTemplateList':
        """Gets the document template of each document in the list.

        :return: A list of document templates
        :rtype: XAPagesTemplateList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("documentTemplate")
        return self._new_element(ls, XAPagesTemplateList)

    def body_text(self) -> XABase.XATextList:
        """Gets the body text of each document in the list.

        :return: A list of document body texts
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bodyText")
        return self._new_element(ls, XABase.XATextList)

    def document_body(self) -> list[bool]:
        """Gets the document body status of each document in the list.

        :return: A list of document body status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("documentBody"))

    def facing_pages(self) -> list[bool]:
        """Gets the facing pages of each document in the list.

        :return: A list of document facing pages status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("facingPages"))

    def current_page(self) -> 'XAPagesPageList':
        """Gets the current page of each document in the list.

        :return: A list of document current pages
        :rtype: XAPagesPageList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("currentPage")
        return self._new_element(ls, XAPagesPageList)

    def selection(self) -> 'XAPagesiWorkItemList':
        """Gets the selection of each document in the list.

        :return: A list of selected items in each document of the list
        :rtype: XAPagesiWorkItemList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        ls = [x for t in ls for x in t]
        return self._new_element(ls, XAPagesiWorkItemList)

    def password_protected(self) -> list[bool]:
        """Gets the password protected status of each document in the list.

        :return: A list of document password protect status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "id" in properties:
            raw_dict["id"] = properties["id"]

        if "current_page" in properties:
            raw_dict["currentPage"] = properties["current_page"].xa_elem

        if "file" in properties:
            if isinstance(properties["file"], str):
                raw_dict["file"] = properties["file"]
            else:
                raw_dict["file"] = properties["file"].xa_elem

        if "modified" in properties:
            raw_dict["modified"] = properties["modified"]

        if "document_body" in properties:
            raw_dict["documentBody"] = properties["document_body"]

        if "document_template" in properties:
            raw_dict["documentTemplate"] = properties["document_template".xa_elem]

        if "body_text" in properties:
            raw_dict["bodyText"] = properties["body_text"]

        if "facing_pages" in properties:
            raw_dict["facingPages"] = properties["facing_pages"]

        if "selection" in properties:
            selection = properties["selection"]
            if isinstance(selection, list):
                selection = [x.xa_elem for x in selection]
            raw_dict["selection"] = selection

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "password_protected" in properties:
            raw_dict["passwordProtected"] = properties["password_protected"]

        for document in self.xa_elem:
            if all(raw_dict[x] == document.properties()[x] for x in raw_dict):
                return self._new_element(document, XAPagesDocument)

    def by_name(self, name: str) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("modified", modified)

    def by_file(self, file: Union[str, XABase.XAPath]) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose file matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        if isinstance(file, XABase.XAPath):
            file = file.url
        return self.by_property("file", file)

    def by_id(self, id: str) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose ID matches the given ID, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("id", id)

    def by_document_template(self, document_template: 'XAPagesTemplate') -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose document template matches the given template, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("documentTemplate", document_template.xa_elem)

    def by_body_text(self, body_text: Union[str, XABase.XAText]) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose body text matches the given text, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        if isinstance(body_text, str):
            self.by_property('bodyText', body_text)
        else:
            self.by_property('bodyText', body_text.xa_elem)

    def by_document_body(self, document_body: bool) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose document body status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("documentBody", document_body)

    def by_facing_pages(self, facing_pages: bool) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose facing pages status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("facingPages", facing_pages)

    def by_current_page(self, current_page: 'XAPagesPage') -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose current page matches the given page, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("currentPage", current_page.xa_elem)

    def by_selection(self, selection: Union['XAPagesiWorkItemList', list['XAPagesiWorkItem']]) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose selection matches the given list, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        for doc in self.xa_elem:
            if doc.selection() == selection.xa_elem:
                return doc

    def by_password_protected(self, password_protected: bool) -> Union['XAPagesDocument', None]:
        """Retrieves the first document whose password protected status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPagesDocument, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("passwordProtected", password_protected)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns the audio clips of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("audioClips")]
        return self._new_element(ls, XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns the charts of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("charts")]
        return self._new_element(ls, XAPagesChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns the groups of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("groups")]
        return self._new_element(ls, XAPagesGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns the images of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's images
        :rtype: XAPagesImageList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("images")]
        return self._new_element(ls, XAPagesImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns the iWork items of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("iWorkItems")]
        return self._new_element(ls, XAPagesiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns the lines of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("lines")]
        return self._new_element(ls, XAPagesLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns the movies of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("movies")]
        return self._new_element(ls, XAPagesMovieList, filter)

    def pages(self, filter: Union[dict, None] = None) -> 'XAPagesPageList':
        """Returns the pages of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned pages will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's pages
        :rtype: XAPagesPageList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("pages")]
        return self._new_element(ls, XAPagesPageList, filter)

    def sections(self, filter: Union[dict, None] = None) -> 'XAPagesSectionList':
        """Returns the sections of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned sections will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's sections
        :rtype: XAPagesSectionList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("sections")]
        return self._new_element(ls, XAPagesSectionList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns the shapes of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("shapes")]
        return self._new_element(ls, XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns the tables of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("tables")]
        return self._new_element(ls, XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns the text items of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's text items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("textItems")]
        return self._new_element(ls, XAPagesTableList, filter)

    def placeholder_texts(self, filter: Union[dict, None] = None) -> 'XAPagesPlaceholderTextList':
        """Returns the placeholder texts of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned placeholder texts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's placeholder texts
        :rtype: XAPagesPlaceholderTextList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("placeholderTexts")]
        return self._new_element(ls, XAPagesTableList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPagesDocument(XABaseScriptable.XASBPrintable, XACloseable):
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
        self.body_text: XABase.XAText #: The document body text
        self.document_body: bool #: Whether the document has body text
        self.facing_pages: bool #: Whether the document has facing pages
        self.current_page: XAPagesPage #: The current page of the document
        self.selection: XAPagesiWorkItemList #: A list of the currently selected items
        self.password_protected: bool #: Whether the document is password protected

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
                "id": raw_dict["id"],
                "current_page": self._new_element(raw_dict["currentPage"], XAPagesDocument),
                "file": XABase.XAPath(raw_dict["file"]),
                "modified": raw_dict["modified"],
                "document_body": raw_dict["documentBody"],
                "document_template": self._new_element(raw_dict["documentTemplate"], XAPagesTemplate),
                "body_text": raw_dict["bodyText"],
                "facing_pages": raw_dict["facingPages"],
                "selection": self._new_element(raw_dict["selection"], XAPagesiWorkItemList),
                "name": raw_dict["name"],
                "password_protected": raw_dict["passwordProtected"]
        }
        return pyxa_dict

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        file = self.xa_elem.file()
        if file is not None:
            return XABase.XAPath(file)

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def document_template(self) -> 'XAPagesTemplate':
        return self._new_element(self.xa_elem.documentTemplate(), XAPagesTemplate)

    @property
    def body_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.bodyText(), XABase.XAText)

    @body_text.setter
    def body_text(self, body_text: Union[XABase.XAText, str]):
        if isinstance(body_text, str):
            self.set_property('bodyText', body_text)
        else:
            self.set_property('bodyText', str(body_text))

    @property
    def document_body(self) -> bool:
        return self.xa_elem.documentBody()

    @property
    def facing_pages(self) -> bool:
        return self.xa_elem.facingPages()

    @facing_pages.setter
    def facing_pages(self, facing_pages: bool):
        self.set_property('facingPages', facing_pages)

    @property
    def current_page(self) -> 'XAPagesPage':
        return self._new_element(self.xa_elem.currentPage(), XAPagesPage)

    @property
    def selection(self) -> 'XAPagesiWorkItemList':
        return self._new_element(self.xa_elem.selection(), XAPagesiWorkItemList)

    @selection.setter
    def selection(self, selection: Union['XAPagesiWorkItemList', 'XAPagesiWorkItem']):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property('selection', selection)
        else:
            self.set_property('selection', selection.xa_elem)

    @property
    def password_protected(self) -> bool:
        return self.xa_elem.passwordProtected()

    def export(self, file_path: Union[str, AppKit.NSURL] = None, format: XAPagesApplication.ExportFormat = XAPagesApplication.ExportFormat.PDF):
        """Exports the document in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, AppKit.NSURL], optional
        :param format: The format to export the file in, defaults to XAPagesApplication.ExportFormat.PDF
        :type format: XAPagesApplication.ExportFormat, optional

        .. versionadded:: 0.0.3
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = AppKit.NSURL.alloc().initFileURLWithPath_(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path, format.value, None)

    def new_page(self, text: Union[str, XABase.XAText]) -> 'XAPagesPage':
        """Creates a new page at the end of the document.

        :param text: The text to initialize the new page with
        :type text: Union[str, XABase.XAText]
        :return: A reference to the newly created page object
        :rtype: XAPagesPage

        .. versionadded:: 0.0.6
        """
        parent = self.xa_prnt
        while not hasattr(parent, "make"):
            parent = parent.xa_prnt
            
        new_page = parent.make("page", {})
        page = self.pages().push(new_page)
        page.body_text = text
        return page

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

    def __repr__(self):
        try:
            return "<" + str(type(self)) + str(self.name) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPagesTemplateList(XABase.XAList):
    """A wrapper around lists of templates that employs fast enumeration techniques.

    All properties of templates can be called as methods on the wrapped list, returning a list containing each template's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesTemplate, filter)

    def id(self) -> list[str]:
        """Gets the ID of each template in the list.

        :return: A list of template IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        """Gets the name of each template in the list.

        :return: A list of template names
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> Union['XAPagesTemplate', None]:
        """Retrieves the first template whose ID matches the given ID, if one exists.

        :return: The desired template, if it is found
        :rtype: Union[XAPagesTemplate, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XAPagesTemplate', None]:
        """Retrieves the first template whose name matches the given name, if one exists.

        :return: The desired template, if it is found
        :rtype: Union[XAPagesTemplate, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XAPagesTemplate(XABase.XAObject):
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
        try:
            return f"<{str(type(self))}{self.name}, id={str(self.id)}>"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPagesSectionList(XABase.XAList):
    """A wrapper around lists of sections that employs fast enumeration techniques.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPagesSection, filter)

    def body_text(self) -> XABase.XATextList:
        """Gets the body text of each section in the list.

        :return: A list of section body texts
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bodyText")
        return self._new_element(ls, XABase.XATextList)

    def by_body_text(self, body_text: Union[str, XABase.XAText]) -> Union['XAPagesSection', None]:
        """Retrieves the first section whose body text matches the given text, if one exists.

        :return: The desired section, if it is found
        :rtype: Union[XAPagesSection, None]
        
        .. versionadded:: 0.0.6
        """
        if isinstance(body_text, str):
            self.by_property('bodyText', body_text)
        else:
            self.by_property('bodyText', str(body_text))

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns the audio clips of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("audioClips")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns the charts of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("charts")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns the groups of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("groups")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns the images of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's images
        :rtype: XAPagesImageList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("images")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns the iWork items of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("iWorkItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns the lines of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("lines")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns the movies of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("movies")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns the shapes of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("shapes")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns the tables of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("tables")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesTableList, filter)

    def pages(self, filter: Union[dict, None] = None) -> 'XAPagesPageList':
        """Returns the pages of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned pages will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's pages
        :rtype: XAPagesPageList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("pages")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesPageList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns the text items of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's text items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesTableList, filter)

    def __repr__(self):
        return f"<{str(type(self))}length:{len(self.xa_elem)}>"

class XAPagesSection(XABase.XAObject):
    """A class for managing and interacting with sections in Pages.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.body_text: XABase.XAText #: The section body text

    @property
    def body_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.bodyText(), XABase.XAText)

    @body_text.setter
    def body_text(self, body_text: Union[XABase.XAText, str]):
        if isinstance(body_text, str):
            self.set_property('bodyText', body_text)
        else:
            self.set_property('bodyText', str(body_text))

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAPagesiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), XAPagesChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XAPagesImageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), XAPagesImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), XAPagesGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), XAPagesLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), XAPagesMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), XAPagesShapeList, filter)

    def pages(self, filter: Union[dict, None] = None) -> 'XAPagesPageList':
        """Returns a list of pages, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned pages will have, or None
        :type filter: Union[dict, None]
        :return: The list of pages
        :rtype: XAPagesPageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.pages(), XAPagesPageList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), XAPagesTextItemList, filter)




class XAPagesContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAPagesContainer
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of containers")

        # Specialize to XAPagesGroupList or XAPagesPageList 
        if self.__class__ == XAPagesContainerList:
            if all([x.parent().get() == None for x in self.xa_elem]):
                new_self = self._new_element(self.xa_elem, XAPagesPageList)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAPagesContainerList to XAPagesPageList")

            elif all([x.parent().get() != None for x in self.xa_elem]):
                new_self = self._new_element(self.xa_elem, XAPagesGroupList)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAPagesContainerList to XAPagesGroupList")

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns the audio clips of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("audioClips")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns the charts of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("charts")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns the groups of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("groups")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns the images of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's images
        :rtype: XAPagesImageList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("images")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns the iWork items of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("iWorkItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns the lines of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("lines")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns the movies of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("movies")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns the shapes of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("shapes")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns the tables of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("tables")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns the text items of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's text items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesTableList, filter)
    
    def __repr__(self):
        return "<" + str(type(self)) + "length:" + str(len(self.xa_elem)) + ">"

class XAPagesContainer(XABase.XAObject):
    """A class for managing and interacting with containers in Pages.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

        # Specialize to XAPagesGroup or XAPagesPage object
        if self.__class__ == XAPagesContainer:
            if self.xa_elem.baseLayout().get() is not None:
                new_self = self._new_element(self.xa_elem, XAPagesPage)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAPagesContainer to XAPagesPage")

            elif self.xa_elem.parent().get() is not None:
                new_self = self._new_element(self.xa_elem, XAPagesGroup)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAPagesContainer to XAPagesGroup")

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAPagesiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XAPagesiWorkItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAPagesiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAPagesAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XAPagesAudioClipList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), XAPagesAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAPagesChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XAPagesChartList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), XAPagesChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAPagesImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XAPagesImageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), XAPagesImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAPagesGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAPagesGroupList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), XAPagesGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAPagesLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XAPagesLineList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), XAPagesLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XAPagesMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XAPagesMovieList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), XAPagesMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAPagesShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XAPagesShapeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), XAPagesShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAPagesTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XAPagesTableList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), XAPagesTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAPagesTextItemList':
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: XAPagesTextItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), XAPagesTextItemList, filter)




class XAPagesPageList(XAPagesContainerList):
    """A wrapper around lists of pages that employs fast enumeration techniques.

    All properties of pages can be called as methods on the wrapped list, returning a list containing each page's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesPage)

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each page in the list.

        :return: A list of page properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "body_text": self._new_element(raw_dict["bodyText"], XABase.XAText)
            }
        return pyxa_dicts

    def body_text(self) -> XABase.XATextList:
        """Gets the body text of each page in the list.

        :return: A list of page body texts
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bodyText")
        return self._new_element(ls, XABase.XATextList)

    def by_properties(self, properties: dict) -> Union['XAPagesPage', None]:
        """Retrieves the first page whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired page, if it is found
        :rtype: Union[XAPagesPage, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "body_text" in properties:
            raw_dict["bodyText"] = str(properties["body_text"])

        for page in self.xa_elem:
            if all([raw_dict[x] == page.properties()[x] for x in raw_dict]):
                return self._new_element(page, XAPagesPage)

    def by_body_text(self, body_text: Union[str, XABase.XAText]) -> Union['XAPagesPage', None]:
        """Retrieves the first page whose body text matches the given text, if one exists.

        :return: The desired page, if it is found
        :rtype: Union[XAPagesPage, None]
        
        .. versionadded:: 0.0.6
        """
        if isinstance(body_text, str):
            self.by_property('bodyText', body_text)
        else:
            self.by_property('bodyText', body_text.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + "length:" + str(len(self.xa_elem)) + ">"

class XAPagesPage(XAPagesContainer):
    """A class for managing and interacting with pages in Pages documents.

    .. seealso:: :class:`XAPagesApplication`, :class:`XAPagesiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the slide
        self.body_text: XABase.XAText #: The page body text

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "body_text": self._new_element(raw_dict["bodyText"], XABase.XAText)
        }
        return pyxa_dict

    @property
    def body_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.bodyText(), XABase.XAText)

    @body_text.setter
    def body_text(self, body_text: Union[XABase.XAText, str]):
        if isinstance(body_text, str):
            self.set_property('bodyText', body_text)
        else:
            self.set_property('bodyText', str(body_text))

    # def duplicate(self) -> 'XAPagesPage':
    #     """Duplicates the page, mimicking the action of copying and pasting the page manually.

    #     :return: A reference to the PyXA page object that called this command.
    #     :rtype: XAPagesPage

    #     .. versionadded:: 0.0.6
    #     """
    #     parent = self.xa_prnt
    #     while not hasattr(parent, "new_page"):
    #         parent = parent.xa_prnt

    #     new_page = parent.new_page(self.body_text)

    #     parent = self.xa_prnt
    #     while not hasattr(parent, "make"):
    #         parent = parent.xa_prnt
        
    #     for item in self.xa_elem.lines():
    #         properties = item.properties()
    #         # properties.pop("id")
    #         properties["parent"] = new_page.xa_elem

    #         print(properties)

    #         new_line = parent.make("line", properties)
    #         print(new_line.xa_elem)
    #         print(new_page.lines().push(new_line))
    #     return self

    # def move_to(self, document):
    #     self.xa_elem.moveTo_(document.xa_elem.pages())

    # def delete(self):
    #     """Deletes the page.

    #     .. versionadded:: 0.0.6
    #     """
    #     self.xa_elem.get().delete()

    def add_image(self, file_path: Union[str, XABase.XAPath, XABase.XAImage]) -> 'XAPagesImage':
        """Adds the image at the specified path to the page.

        :param file_path: The path to the image file
        :type file_path: Union[str, XABase.XAPath, XABase.XAImage]
        :return: The newly created image object
        :rtype: XAPagesImage

        .. versionadded:: 0.0.6
        """
        url = file_path
        if isinstance(url, str):
            url = XABase.XAPath(url).url
        elif isinstance(url, XABase.XAImage):
            url = XABase.XAPath(url.file).xa_elem
        elif isinstance(url, XABase.XAPath):
            url = url.url

        parent = self.xa_prnt
        while not hasattr(parent, "make"):
            parent = parent.xa_prnt

        image = self.images().push(parent.make("image", { "file": url }))
        image.xa_prnt = self
        return image

    # def add_chart(self, row_names: list[str], column_names: list[str], data: list[list[Any]], type: int = XAPagesApplication.ChartType.LINE_2D.value, group_by: int = XAPagesApplication.ChartGrouping.ROW.value) -> 'XAPagesChart':
    #     """_summary_

    #     _extended_summary_

    #     :param row_names: A list of row names.
    #     :type row_names: list[str]
    #     :param column_names: A list of column names.
    #     :type column_names: list[str]
    #     :param data: A 2d array 
    #     :type data: list[list[Any]]
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
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAPagesiWorkItem
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of iWork items")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each iWork item in the list.

        :return: A list of iWork item properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, item in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "parent": self._new_element(item.parent(), XAPagesiWorkItem),
                "locked": item.locked(),
                "height": item.height(),
                "position": tuple(item.position()),
                "width": item.width(),
            }
        return pyxa_dicts

    def height(self) -> list[int]:
        """Gets the height of each iWork item in the list.

        :return: A list of iWork item heights
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def locked(self) -> list[bool]:
        """Gets the locked status of each iWork item in the list.

        :return: A list of iWork item locked status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def width(self) -> list[int]:
        """Gets the width of each iWork item in the list.

        :return: A list of iWork item width
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def parent(self) -> XAPagesContainerList:
        """Gets the parent of each iWork item in the list.

        :return: A list of iWork item containers
        :rtype: XAPagesContainerList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAPagesContainerList)

    def position(self) -> list[tuple[int, int]]:
        """Gets the position of each iWork item in the list.

        :return: A list of iWork item position
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("position")
        return [tuple(x.pointValue()) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose properties dictionary matches the given properties, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        raw_dict = {}

        if "parent" in properties:
            raw_dict["parent"] = properties["parent"].xa_elem

        if "locked" in properties:
            raw_dict["locked"] = properties["locked"]

        if "height" in properties:
            raw_dict["height"] = properties["height"]

        if "position" in properties:
            raw_dict["position"] = properties["position"]

        if "width" in properties:
            raw_dict["width"] = properties["width"]

        for item in self.xa_elem:
            item_properties = item.properties()
            if all(item_properties[x] == raw_dict[x] for x in raw_dict):
                return self._new_element(item, XAPagesiWorkItem)

    def by_height(self, height: int) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose height matches the given height, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose locked status matches the given boolean value, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose width matches the given width, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("width", width)

    def by_parent(self, parent: XAPagesContainer) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose parent matches the given object, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: tuple[int, int]) -> Union['XAPagesiWorkItem', None]:
        """Retrieves the first iWork item whose position matches the given position, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAPagesiWorkItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("position", position)

    def __repr__(self):
        return "<" + str(type(self)) + "length:" + str(len(self.xa_elem)) + ">"

class XAPagesiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Pages.

    .. seealso:: :class:`XAPagesApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the item
        self.height: int #: The height of the iWork item
        self.locked: bool #: Whether the object is locked
        self.width: int #: The width of the iWork item
        self.parent: XAPagesContainer #: The iWork container that contains the iWork item
        self.position: tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the iWork item

    @property
    def properties(self) -> dict:
        return {
            "parent": self._new_element(self.xa_elem.parent(), XAPagesiWorkItem),
            "locked": self.xa_elem.locked(),
            "height": self.xa_elem.height(),
            "position": tuple(self.xa_elem.position()),
            "width": self.xa_elem.width(),
        }

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def locked(self) -> bool:
        return self.xa_elem.locked()

    @locked.setter
    def locked(self, locked: bool):
        self.set_property('locked', locked)

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def parent(self) -> XAPagesContainer:
        return self._new_element(self.xa_elem.parent(), XAPagesContainer)

    @property
    def position(self) -> tuple[int, int]:
        return tuple(self.xa_elem.position())

    @position.setter
    def position(self, position: tuple[int, int]):
        position = AppKit.NSValue.valueWithPoint_(AppKit.NSPoint(position[0], position[1]))
        self.set_property('position', position)

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.delete()

    def duplicate(self) -> Self:
        """Duplicates the item.

        :return: A reference to the PyXA object that called this method.
        :rtype: Self

        .. versionadded:: 0.0.2
        """
        self.xa_elem.duplicateTo_withProperties_(self.parent.xa_elem.iWorkItems(), None)
        return self

    def resize(self, width: int, height: int) -> Self:
        """Sets the width and height of the item.

        :param width: The desired width, in pixels
        :type width: int
        :param height: The desired height, in pixels
        :type height: int
        :return: The iWork item
        :rtype: Self

        .. versionadded:: 0.0.6
        """
        self.set_properties({
            "width": width,
            "height": height,
        })
        return self

    def lock(self) -> Self:
        """Locks the properties of the item, preventing changes.

        :return: The iWork item
        :rtype: XAPagesiWorkItem

        .. versionadded:: 0.0.6
        """
        self.set_property("locked", True)
        return self

    def unlock(self) -> Self:
        """Unlocks the properties of the item, allowing changes.

        :return: The iWork item
        :rtype: Self

        .. versionadded:: 0.0.6
        """
        self.set_property("locked", False)
        return self

    def __repr__(self):
        try:
            return "<" + str(type(self)) +  "position: " + str(self.position) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPagesGroupList(XAPagesContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesGroup)
        logger.debug("Got list of groups")

    def height(self) -> list[int]:
        """Gets the height of each group in the list.

        :return: A list of group heights
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def position(self) -> list[tuple[int, int]]:
        """Gets the position of each group in the list.

        :return: A list of group positions
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.6
        """
        return [tuple(x.position()) for x in self.xa_elem]

    def width(self) -> list[int]:
        """Gets the width of each group in the list.

        :return: A list of group widths
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each group in the list.

        :return: A list of group rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def parent(self) -> XAPagesContainerList:
        """Gets the parent of each group in the list.

        :return: A list of group containers
        :rtype: XAPagesContainerList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAPagesContainerList)

    def by_height(self, height: int) -> Union['XAPagesGroup', None]:
        """Retrieves the first group whose height matches the given height, if one exists.

        :return: The desired group, if it is found
        :rtype: Union[XAPagesGroup, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("height", height)

    def by_position(self, position: tuple[int, int]) -> Union['XAPagesGroup', None]:
        """Retrieves the first group whose position matches the given position, if one exists.

        :return: The desired group, if it is found
        :rtype: Union[XAPagesGroup, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("position", position)

    def by_width(self, width: int) -> Union['XAPagesGroup', None]:
        """Retrieves the first group whose width matches the given width, if one exists.

        :return: The desired group, if it is found
        :rtype: Union[XAPagesGroup, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("width", width)

    def by_rotation(self, rotation: int) -> Union['XAPagesGroup', None]:
        """Retrieves the first group whose rotation matches the given rotation, if one exists.

        :return: The desired group, if it is found
        :rtype: Union[XAPagesGroup, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

    def by_parent(self, parent: XAPagesContainer) -> Union['XAPagesGroup', None]:
        """Retrieves the first group whose parent matches the given object, if one exists.

        :return: The desired group, if it is found
        :rtype: Union[XAPagesGroup, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("parent", parent.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.position()) + ">"

class XAPagesGroup(XAPagesContainer):
    """A class for managing and interacting with iWork item groups in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int #: The height of the group
        self.position: tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the group
        self.width: int #: The widht of the group
        self.rotation: int #: The rotation of the group, in degrees from 0 to 359
        self.parent: XAPagesContainer #: The container which contains the group

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def position(self) -> tuple[int, int]:
        return tuple(self.xa_elem.position())

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def parent(self) -> XAPagesContainer:
        return self._new_element(self.xa_elem.parent(), XAPagesContainer)

    def rotate(self, degrees: int) -> Self:
        """Rotates the group by the specified number of degrees.

        :param degrees: The amount to rotate the group, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
        >>> group = pages.current_document.groups()[0]
        >>> group.rotate(45)

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesImageList(XAPagesiWorkItemList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesImage)
        logger.debug("Got list of images")

    def description(self) -> list[str]:
        """Gets the description of each image in the list.

        :return: A list of image descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def file(self) -> list[XABase.XAPath]:
        """Gets the file path of each image in the list.

        :return: A list of image file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def file_name(self) -> list[str]:
        """Gets the file name of each image in the list.

        :return: A list of image file names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def opacity(self) -> list[int]:
        """Gets the opacity of each image in the list.

        :return: A list of image opacities
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        """Gets the reflection showing status of each image in the list.

        :return: A list of image reflection showing status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        """Gets the reflection value of each image in the list.

        :return: A list of image reflection values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each image in the list.

        :return: A list of image rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_description(self, description: str) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose description matches the given description, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("objectDescription", description)

    def by_file(self, file: Union[str, XABase.XAPath]) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose file path matches the given file, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        if isinstance(file, XABase.XAPath):
            file = file.url
        return self.by_property("file", file)

    def by_file_name(self, file_name: str) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose file name matches the given file name, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fileName", file_name)

    def by_opacity(self, opacity: int) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose opacity matches the given opacity, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose reflection showing status matches the given boolean value, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose reflection value matches the given value, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAPagesImage', None]:
        """Retrieves the first image whose rotation matches the given rotation, if one exists.

        :return: The desired image, if it is found
        :rtype: Union[XAPagesImage, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XAPagesImage(XAPagesiWorkItem):
    """A class for managing and interacting with images in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.description: str #: Text associated with the image, read aloud by VoiceOVer
        self.file: str #: The image file
        self.file_name: str #: The name of the image file
        self.opacity: int #: The opacity of the image, in percent from 0 to 100
        self.reflection_showing: bool #: Whether the image displays a reflection
        self.reflection_value: int #: The percentage of reflection of the image, from 0 to 100
        self.rotation: int #: The rotation of the image, in degrees from 0 to 359

    @property
    def description(self) -> str:
        return self.xa_elem.object_description()

    @description.setter
    def description(self, description: str):
        self.set_property('objectDescription', description)

    @property
    def file(self) -> str:
        file = self.xa_elem.file()
        if file is not None:
            return XABase.XAPath(file)

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName().get()

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflection_value', reflection_value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> Self:
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
        >>> page = pages.documents()[0].pages()[0]
        >>> img = page.add_image("/Users/steven/Documents/idk/idk.001.png")
        >>> img.rotate(30)
        >>> img.rotate(60)  # Rotated 60+30
        >>> img.rotate(90)  # Rotated 90+90
        >>> img.rotate(180) # Rotated 180+180

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, AppKit.NSURL]) -> 'XAPagesImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, AppKit.NSURL]
        :return: A reference to the new PyXA image object.
        :rtype: XAPagesImage

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
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

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAPagesAudioClipList(XAPagesiWorkItemList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesAudioClip)
        logger.debug("Got list of audio clips")

    def file_name(self) -> list[str]:
        """Gets the file name of each audio clip in the list.

        :return: A list of audio clip file names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> list[int]:
        """Gets the volume of each audio clip in the list.

        :return: A list of audio clip volumes
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> list[XAPagesApplication.RepetitionMethod]:
        """Gets the repetition method of each audio clip in the list.

        :return: A list of audio clip repetition methods
        :rtype: list[XAPagesApplication.RepetitionMethod]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAPagesApplication.RepetitionMethod(XABase.OSType(x.stringValue())) for x in ls]

    def by_file_name(self, file_name: str) -> Union['XAPagesAudioClip', None]:
        """Retrieves the first audio clip whose file name matches the given file name, if one exists.

        :return: The desired audio clip, if it is found
        :rtype: Union[XAPagesAudioClip, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> Union['XAPagesAudioClip', None]:
        """Retrieves the first audio clip whose volume matches the given volume, if one exists.

        :return: The desired audio clip, if it is found
        :rtype: Union[XAPagesAudioClip, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod) -> Union['XAPagesAudioClip', None]:
        """Retrieves the first audio clip whose repetition method matches the given repetition method, if one exists.

        :return: The desired audio clip, if it is found
        :rtype: Union[XAPagesAudioClip, None]
        
        .. versionadded:: 0.0.5
        """
        for clip in self.xa_elem:
            if clip.repetitionMethod() == repetition_method.value:
                return self._new_element(clip, XAPagesAudioClip)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

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

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def clip_volume(self) -> int:
        return self.xa_elem.clipVolume()

    @clip_volume.setter
    def clip_volume(self, clip_volume: int):
        self.set_property('clipVolume', clip_volume)

    @property
    def repetition_method(self) -> XAPagesApplication.RepetitionMethod:
        return XAPagesApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAPagesShapeList(XAPagesiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesShape)
        logger.debug("Got list of shapes")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each shape in the list.

        :return: A list of shape properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, theme in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "background_fill_type": XAPagesApplication.FillOption(XABase.OSType(raw_dicts[index]["backgroundFillType"].stringValue())),
                "object_text": raw_dicts[index]["objectText"],
                "opacity": raw_dicts[index]["opacity"],
                "reflection_showing": raw_dicts[index]["reflectionShowing"],
                "reflection_value": raw_dicts[index]["reflectionValue"],
                "rotation": raw_dicts[index]["rotation"]
            }
        return pyxa_dicts

    def background_fill_type(self) -> list[XAPagesApplication.FillOption]:
        """Gets the background fill type of each shape in the list.

        :return: A list of shape background file types
        :rtype: list[XAPagesApplication.FillOption]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundFillType")
        return [XAPagesApplication.FillOption(XABase.OSType(x.stringValue())) for x in ls]

    def object_text(self) -> XABase.XATextList:
        """Gets the text of each shape in the list.

        :return: A list of shape object texts
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("objectText")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> list[int]:
        """Gets the opacity of each shape in the list.

        :return: A list of shape opacities
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        """Gets the reflection showing status of each shape in the list.

        :return: A list of shape reflection showing status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        """Gets the reflection value of each shape in the list.

        :return: A list of shape reflection values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each shape in the list.

        :return: A list of shape rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_properties(self, properties: dict) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose properties dictionary matches the given properties, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        raw_dict = {}

        if "background_fill_type" in properties:
            raw_dict["backgroundFillType"] = properties["backgroundFillType"].value

        if "object_text" in properties:
            raw_dict["objectText"] = properties["object_text"]

        if "reflection_showing" in properties:
            raw_dict["reflectionShowing"] = properties["reflection_showing"]

        if "reflection_value" in properties:
            raw_dict["reflectionValue"] = properties["reflection_value"]

        for shape in self.xa_elem:
            shape_properties = shape.properties()
            if all(shape_properties[x] == raw_dict[x] for x in raw_dict):
                return self._new_element(shape, XAPagesShape)

    def by_background_fill_type(self, background_fill_type: XAPagesApplication.FillOption) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose background fill type matches the given fill type, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_object_text(self, object_text: XABase.XAText) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose text matches the given text, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("objectText", str(object_text))

    def by_opacity(self, opacity: int) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose opacity matches the given opacity, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose reflection showing status matches the given boolean value, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose reflection value matches the given value, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAPagesShape', None]:
        """Retrieves the first shape whose rotation matches the given rotation, if one exists.

        :return: The desired shape, if it is found
        :rtype: Union[XAPagesShape, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

class XAPagesShape(XAPagesiWorkItem):
    """A class for managing and interacting with shapes in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the shape
        self.background_fill_type: XAPagesApplication.FillOption #: The background, if any, for the shape
        self.object_text: XABase.XAText #: The text contained within the shape
        self.opacity: int #: The percent opacity of the object
        self.reflection_showing: bool #: Whether the iWork item displays a reflection
        self.reflection_value: int #: The percentage of relfection that the iWork item displays, from 0 to 100
        self.rotation: int #: The rotation of the iWork item, in degrees, from 0 to 359

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "background_fill_type": XAPagesApplication.FillOption(XABase.OSType(raw_dict["backgroundFillType"].stringValue())),
            "object_text": raw_dict["objectText"],
            "opacity": raw_dict["opacity"],
            "reflection_showing": raw_dict["reflectionShowing"],
            "reflection_value": raw_dict["reflectionValue"],
            "rotation": raw_dict["rotation"]
        }
        return pyxa_dict

    @property
    def background_fill_type(self) -> XAPagesApplication.FillOption:
        return XAPagesApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def object_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.objectText(), XABase.XAText)

    @object_text.setter
    def object_text(self, object_text: str):
        self.set_property('objectText', str(object_text))

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflection_value', reflection_value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> Self:
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: Self

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.2
        """
        self.set_property("rotation", self.rotation + degrees)
        return self




class XAPagesChartList(XAPagesiWorkItemList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesChart)
        logger.debug("Got list of charts")

class XAPagesChart(XAPagesiWorkItem):
    """A class for managing and interacting with charts in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAPagesLineList(XAPagesiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesLine)
        logger.debug("Got list of lines")

    def end_point(self) -> list[tuple[int, int]]:
        """Gets the end point of each line in the list.

        :return: A list of line end points
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("end_point")
        return [tuple(x) for x in ls]

    def reflection_showing(self) -> list[bool]:
        """Gets the reflection showing status of each line in the list.

        :return: A list of line reflection showing status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        """Gets the reflection value of each line in the list.

        :return: A list of line reflection values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each line in the list.

        :return: A list of line rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def start_point(self) -> list[tuple[int, int]]:
        """Gets the start point of each line in the list.

        :return: A list of line start points
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("start_point")
        return [tuple(x) for x in ls]

    def by_end_point(self, end_point: tuple[int, int]) -> Union['XAPagesLine', None]:
        """Retrieves the first line whose end point matches the given point, if one exists.

        :return: The desired line, if it is found
        :rtype: Union[XAPagesLine, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAPagesLine', None]:
        """Retrieves the first line whose reflection showing status matches the given boolean value, if one exists.

        :return: The desired line, if it is found
        :rtype: Union[XAPagesLine, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAPagesLine', None]:
        """Retrieves the first line whose reflection value matches the given value, if one exists.

        :return: The desired line, if it is found
        :rtype: Union[XAPagesLine, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAPagesLine', None]:
        """Retrieves the first line whose rotation matches the given rotation, if one exists.

        :return: The desired line, if it is found
        :rtype: Union[XAPagesLine, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: tuple[int, int]) -> Union['XAPagesLine', None]:
        """Retrieves the first line whose start point matches the given point, if one exists.

        :return: The desired line, if it is found
        :rtype: Union[XAPagesLine, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("startPoint", start_point)

class XAPagesLine(XAPagesiWorkItem):
    """A class for managing and interacting with lines in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.end_point: tuple[int, int] #: A list of two numbers indicating the horizontal and vertical position of the line ending point
        self.reflection_showing: bool #: Whether the line displays a reflection
        self.reflection_value: int #: The reflection of reflection of the line, from 0 to 100
        self.rotation: int #: The rotation of the line, in degrees from 0 to 359
        self.start_point: tuple[int, int] #: A list of two numbers indicating the horizontal and vertical position of the line starting point

    @property
    def end_point(self) -> tuple[int, int]:
        return tuple(self.xa_elem.endPoint())

    @end_point.setter
    def end_point(self, end_point: tuple[int, int]):
        self.set_property('endPoint', end_point)

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def start_point(self) -> tuple[int, int]:
        return tuple(self.xa_elem.startPoint())

    @start_point.setter
    def start_point(self, start_point: tuple[int, int]):
        self.set_property('startPoint', start_point)

    def rotate(self, degrees: int) -> Self:
        """Rotates the line by the specified number of degrees.

        :param degrees: The amount to rotate the line, in degrees, from -359 to 359
        :type degrees: int
        :return: The group object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
        >>> line = pages.current_document.lines()[0]
        >>> line.rotate(45)

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def __repr__(self):
        try:
            return "<" + str(type(self)) + "start:" + str(self.start_point) + ", end:" + str(self.end_point) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPagesMovieList(XAPagesiWorkItemList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesMovie)

    def file_name(self) -> list[str]:
        """Gets the file name of each movie in the list.

        :return: A list of movie file names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def movie_volume(self) -> list[int]:
        """Gets the volume of each movie in the list.

        :return: A list of movie volumes
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("movieVolume"))

    def opacity(self) -> list[int]:
        """Gets the opacity of each movie in the list.

        :return: A list of movie opacities
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        """Gets the reflection showing status of each movie in the list.

        :return: A list of movie reflection showing status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        """Gets the reflection value of each movie in the list.

        :return: A list of movie reflection values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def repetition_method(self) -> list[XAPagesApplication.RepetitionMethod]:
        """Gets the repetition method of each movie in the list.

        :return: A list of movie repetition methods
        :rtype: list[XAPagesApplication.RepetitionMethod]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAPagesApplication.RepetitionMethod(XABase.OSType(x.stringValue())) for x in ls]

    def rotation(self) -> list[int]:
        """Gets the rotation of each movie in the list.

        :return: A list of movie rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_file_name(self, file_name: str) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose file name matches the given file name, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fileName", file_name)

    def by_movie_volume(self, movie_volume: int) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose volume matches the given volume, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("movieVolume", movie_volume)

    def by_opacity(self, opacity: int) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose opacity matches the given opacity, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose reflection showing status matches the given boolean value, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose reflection value matches the given value, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionValue", reflection_value)

    def by_repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose repetition method matches the given repetition method, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("repetitionMethod", repetition_method.value)

    def by_rotation(self, rotation: int) -> Union['XAPagesMovie', None]:
        """Retrieves the first movie whose rotation matches the given rotation, if one exists.

        :return: The desired movie, if it is found
        :rtype: Union[XAPagesMovie, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

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
        return self.xa_elem.fileName().get()

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def movie_volume(self) -> int:
        return self.xa_elem.moveVolume()

    @movie_volume.setter
    def movie_volume(self, movie_volume: int):
        self.set_property('movieVolume', movie_volume)

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def repetition_method(self) -> XAPagesApplication.RepetitionMethod:
        return XAPagesApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAPagesApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> Self:
        """Rotates the movie by the specified number of degrees.

        :param degrees: The amount to rotate the movie, in degrees, from -359 to 359
        :type degrees: int
        :return: The movie object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
        >>> movie = pages.current_document.movies()[0]
        >>> movie.rotate(45)

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.6
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAPagesTextItemList(XAPagesiWorkItemList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesTextItem)

    def background_fill_type(self) -> list[XAPagesApplication.FillOption]:
        """Gets the background fill type of each text item in the list.

        :return: A list of text item background fill types
        :rtype: list[XAPagesApplication.FillOption]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundFillType")
        return [XAPagesApplication.FillOption(XABase.OSType(x.stringValue())) for x in ls]

    def object_text(self) -> XABase.XATextList:
        """Gets the text of each text item in the list.

        :return: A list of text item object textx
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("objectText")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> list[int]:
        """Gets the opacity of each text item in the list.

        :return: A list of text item opacities
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        """Gets the reflection showing status of each text item in the list.

        :return: A list of text item reflection showing status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        """Gets the reflection value of each text item in the list.

        :return: A list of text item reflection values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each text item in the list.

        :return: A list of text item rotation values
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_background_fill_type(self, background_fill_type: XAPagesApplication.FillOption) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose background fill type matches the given fill type, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_object_text(self, object_text: XABase.XAText) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose object text matches the given text, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        self.by_property('objectText', str(object_text))

    def by_opacity(self, opacity: int) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose opacity matches the given opacity, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose reflection showing status matches the given boolean value, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose reflection value matches the given value, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAPagesTextItem', None]:
        """Retrieves the first text item whose rotation matches the given rotation, if one exists.

        :return: The desired text item, if it is found
        :rtype: Union[XAPagesTextItem, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rotation", rotation)

class XAPagesTextItem(XAPagesiWorkItem):
    """A class for managing and interacting with text items in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: XAPagesApplication.FillOption #: The background of the text item
        self.object_text: XABase.XAText #: The text contained within the text item
        self.opacity: int #: The opacity of the text item
        self.reflection_showing: bool #: Whether the text item displays a reflection
        self.reflection_value: int #: The percentage of reflection of the text item, from 0 to 100
        self.rotation: int #: The rotation of the text item, in degrees from 0 to 359

    @property
    def background_fill_type(self) -> XAPagesApplication.FillOption:
        return XAPagesApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def object_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.objectText(), XABase.XAText)

    @object_text.setter
    def object_text(self, object_text: Union[XABase.XAText, str]):
        self.set_property('objectText', str(object_text))

    @property
    def opacity(self) -> int:
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> Self:
        """Rotates the text item by the specified number of degrees.

        :param degrees: The amount to rotate the text item, in degrees, from -359 to 359
        :type degrees: int
        :return: The text item object.
        :rtype: Self

        :Example:

        >>> import PyXA
        >>> pages = PyXA.Application("Pages")
        >>> text = pages.current_document.text_items()[0]
        >>> text.rotate(45)

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

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
        super().__init__(properties, filter, XAPagesTextItem)

    def tag(self) -> list[str]:
        """Gets the script tag of each placeholder text in the list.

        :return: The list of tags
        :rtype: list[str]

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("tag"))

    def by_tag(self, tag: str) -> Union['XAPagesPlaceholderText', None]:
        """Retrieves the placeholder text whose script tag matches the given tag.

        :return: The matching placeholder text, if one is found
        :rtype: Union[XAPagesPlaceholderText, None]

        .. versionadded:: 0.1.0
        """
        return self.by_property("tag", tag)

class XAPagesPlaceholderText(XABase.XAText):
    """A placeholder text in Pages.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.tag: str #: The placeholder text's script tag

    @property
    def tag(self) -> str:
        return self.xa_elem.tag()

    @tag.setter
    def tag(self, tag: str):
        self.set_property('tag', tag)




class XAPagesTableList(XAPagesiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesTable)

    def name(self) -> list[str]:
        """Gets the name of each table in the list.

        :return: A list of table names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def row_count(self) -> list[int]:
        """Gets the row count of each table in the list.

        :return: A list of table row counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rowCount"))

    def column_count(self) -> list[int]:
        """Gets the column count of each table in the list.

        :return: A list of table column counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("columnCount"))

    def header_row_count(self) -> list[int]:
        """Gets the header row count of each table in the list.

        :return: A list of table header row counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("headerRowCount"))

    def header_column_count(self) -> list[int]:
        """Gets the header column count of each table in the list.

        :return: A list of table header column counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("headerColumnCount"))

    def footer_row_count(self) -> list[int]:
        """Gets the footer row count of each table in the list.

        :return: A list of table footer row counts
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("footerRowCount"))

    def cell_range(self) -> 'XAPagesRangeList':
        """Gets the total cell range of each table in the list.

        :return: A list of table cell ranges
        :rtype: XAPagesRangeList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XAPagesRangeList)

    def selection_range(self) -> 'XAPagesRangeList':
        """Gets the selected cell range of each table in the list.

        :return: A list of selected table cell ranges
        :rtype: XAPagesRangeList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XAPagesRangeList)

    def by_name(self, name: str) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose name matches the given name, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose header row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose header column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> Union['XAPagesTable', None]:
        """Retrieves the first table whose footer row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XAPagesRange') -> Union['XAPagesTable', None]:
        """Retrieves the first table whose cell range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XAPagesRange') -> Union['XAPagesTable', None]:
        """Retrieves the first table whose selection range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAPagesTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("selectionRange", selection_range.xa_elem)

    def cells(self, filter: Union[dict, None] = None) -> 'XAPagesCellList':
        """Returns the cells of each table in the list.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of every table's cells
        :rtype: XAPagesCellList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cells")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesCellList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAPagesRowList':
        """Returns the rows of each table in the list.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of every table's rows
        :rtype: XAPagesRowList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("rows")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesRowList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAPagesColumnList':
        """Returns the columns of each table in the list.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of every table's columns
        :rtype: XAPagesColumnList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("columns")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesColumnList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> 'XAPagesRangeList':
        """Returns the ranges of each table in the list.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of every table's ranges
        :rtype: XAPagesRangeList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("ranges")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesRangeList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

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

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def row_count(self) -> int:
        return self.xa_elem.rowCount()

    @row_count.setter
    def row_count(self, row_count: int):
        self.set_property('rowCount', row_count)

    @property
    def column_count(self) -> int:
        return self.xa_elem.columnCount()

    @column_count.setter
    def column_count(self, column_count: int):
        self.set_property('columnCount', column_count)

    @property
    def header_row_count(self) -> int:
        return self.xa_elem.headerRowCount()

    @header_row_count.setter
    def header_row_count(self, header_row_count: int):
        self.set_property('headerRowCount', header_row_count)

    @property
    def header_column_count(self) -> int:
        return self.xa_elem.headerColumnCount()

    @header_column_count.setter
    def header_column_count(self, header_column_count: int):
        self.set_property('headerColumnCount', header_column_count)

    @property
    def footer_row_count(self) -> int:
        return self.xa_elem.footerRowCount()

    @footer_row_count.setter
    def footer_row_count(self, footer_row_count: int):
        self.set_property('footerRowCount', footer_row_count)

    @property
    def cell_range(self) -> 'XAPagesRange':
        return self._new_element(self.xa_elem.cellRange(), XAPagesRange)

    @property
    def selection_range(self) -> 'XAPagesRange':
        return self._new_element(self.xa_elem.selectionRange(), XAPagesRange)

    @selection_range.setter
    def selection_range(self, selection_range: 'XAPagesRange'):
        self.set_property('selectionRange', selection_range.xa_elem)

    def sort(self, by_column: 'XAPagesColumn', in_rows: Union[list['XAPagesRow'], 'XAPagesRowList', None] = None, direction: XAPagesApplication.SortDirection = XAPagesApplication.SortDirection.ASCENDING) -> Self:
        """Sorts the table according to the specified column, in the specified sorting direction.

        :param by_column: The column to sort by
        :type by_column: XAPagesColumn
        :param in_rows: The rows to sort, or None to sort the whole table, defaults to None
        :type in_rows: Union[list[XAPagesRow], XAPagesRowList, None], optional
        :param direction: The direction to sort in, defaults to XAPagesApplication.SortDirection.ASCENDING
        :type direction: XAPagesApplication.SortDirection, optional
        :return: The table object
        :rtype: Self

        .. versionadded:: 0.1.0
        """
        if isinstance(in_rows, list):
            in_rows = [row.xa_elem for row in in_rows]
        elif isinstance(in_rows, XABase.XAList):
            in_rows = in_rows.xa_elem

        self.xa_elem.sortBy_direction_inRows_(by_column.xa_elem, direction.value, in_rows)
        return self

    def cells(self, filter: Union[dict, None] = None) -> 'XAPagesCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAPagesCellList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAPagesCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAPagesColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAPagesColumnList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAPagesColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAPagesRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAPagesRowList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAPagesRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> 'XAPagesRangeList':
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: XAPagesRangeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.ranges(), XAPagesRangeList, filter)

    def __repr__(self):
        try:
            return "<" + str(type(self)) + str(self.name) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAPagesRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAPagesRange
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each range in the list.

        :return: A list of range properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.5
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "background_color": XABase.XAColor(raw_dict["backgroundColor"]) if raw_dict["backgroundColor"] is not None else None,
                "font_size": raw_dict["fontSize"],
                "name": raw_dict["name"],
                "format": XAPagesApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
                "vertical_alignment": XAPagesApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
                "font_name": raw_dict["fontName"],
                "alignment": XAPagesApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
                "text_wrap": raw_dict["textWrap"],
                "text_color": XABase.XAColor(raw_dict["textColor"]),
            }
        return pyxa_dicts

    def font_name(self) -> list[str]:
        """Gets the font name of each range in the list.

        :return: A list of range font names
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> list[float]:
        """Gets the font size of each range in the list.

        :return: A list of range font sizes
        :rtype: list[float]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def format(self) -> list[XAPagesApplication.CellFormat]:
        """Gets the cell format of each range in the list.

        :return: A list of range cell formats
        :rtype: list[XAPagesApplication.CellFormat]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAPagesApplication.CellFormat(x) for x in ls]

    def alignment(self) -> list[XAPagesApplication.Alignment]:
        """Gets the alignment setting of each range in the list.

        :return: A list of range alignment settings
        :rtype: list[XAPagesApplication.Alignment]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XAPagesApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def text_color(self) -> list[XABase.XAColor]:
        """Gets the text color of each range in the list.

        :return: A list of range text colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textColor")
        return [XABase.XAColor(x) for x in ls]

    def text_wrap(self) -> list[bool]:
        """Gets the text wrap setting of each range in the list.

        :return: A list of range text wrap settings
        :rtype: list[bool]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("textWrap"))

    def background_color(self) -> list[XABase.XAColor]:
        """Gets the background color of each range in the list.

        :return: A list of range background colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor")
        return [XABase.XAColor(x) for x in ls]

    def vertical_alignment(self) -> list[XAPagesApplication.Alignment]:
        """Gets the vertical alignment setting of each range in the list.

        :return: A list of range vertical alignment settings
        :rtype: list[XAPagesApplication.Alignment]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XAPagesApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "background_color" in properties:
            raw_dict["backgroundColor"] = properties["background_color"].xa_elem

        if "font_size" in properties:
            raw_dict["fontSize"] = properties["font_size"]

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "format" in properties:
            raw_dict["format"] = properties["format"].value

        if "vertical_alignment" in properties:
            raw_dict["verticalAlignment"] = XAEvents.event_from_type_code(properties["vertical_alignment"].value)

        if "font_name" in properties:
            raw_dict["fontName"] = properties["font_name"]

        if "alignment" in properties:
            raw_dict["alignment"] = XAEvents.event_from_type_code(properties["alignment"].value)

        if "text_wrap" in properties:
            raw_dict["textWrap"] = properties["text_wrap"]

        if "text_color" in properties:
            raw_dict["textColor"] = properties["text_color"].xa_elem

        for page_range in self.xa_elem:
            if all([raw_dict[x] == page_range.properties()[x] for x in raw_dict]):
                return self._new_element(page_range, XAPagesRange)

    def by_font_name(self, font_name: str) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose font name matches the given font name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose font size matches the given font size, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XAPagesApplication.CellFormat) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose cell format matches the given format, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XAPagesApplication.Alignment) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        for page_range in self.xa_elem:
            if page_range.alignment() == alignment.value:
                return self._new_element(page_range, XAPagesRange)

    def by_name(self, name: str) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose name matches the given name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose text color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose text wrap setting matches the given boolean value, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose background color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XAPagesApplication.Alignment) -> Union['XAPagesRange', None]:
        """Retrieves the first range whose vertical alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAPagesRange, None]
        
        .. versionadded:: 0.0.5
        """
        for page_range in self.xa_elem:
            if page_range.verticalAlignment() == vertical_alignment.value:
                return self._new_element(page_range, XAPagesRange)

    def cells(self, filter: Union[dict, None] = None) -> 'XAPagesCellList':
        """Returns the cells of each range in the list.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of every ranges's cells
        :rtype: XAPagesCellList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cells")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesCellList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAPagesRowList':
        """Returns the rows of each range in the list.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of every ranges's rows
        :rtype: XAPagesRowList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("rows")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesRowList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAPagesColumnList':
        """Returns the columns of each range in the list.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of every ranges's columns
        :rtype: XAPagesColumnList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("columns")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAPagesColumnList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPagesRange(XABase.XAObject):
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
        raw_dict = self.xa_elem.properties()
        return {
            "background_color": XABase.XAColor(raw_dict["backgroundColor"]),
            "font_size": raw_dict["fontSize"],
            "name": raw_dict["name"],
            "format": XAPagesApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
            "vertical_alignment": XAPagesApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
            "font_name": raw_dict["fontName"],
            "alignment": XAPagesApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
            "text_wrap": raw_dict["textWrap"],
            "text_color": XABase.XAColor(raw_dict["textColor"])
        }

    @property
    def font_name(self) -> str:
        return self.xa_elem.fontName()

    @font_name.setter
    def font_name(self, font_name: str):
        self.set_property('fontName', font_name)

    @property
    def font_size(self) -> float:
        return self.xa_elem.fontSize()

    @font_size.setter
    def font_size(self, font_size: float):
        self.set_property('fontSize', font_size)

    @property
    def format(self) -> XAPagesApplication.CellFormat:
        return XAPagesApplication.CellFormat(self.xa_elem.format())

    @format.setter
    def format(self, format: XAPagesApplication.CellFormat):
        self.set_property('format', format.value)

    @property
    def alignment(self) -> XAPagesApplication.Alignment:
        return XAPagesApplication.Alignment(self.xa_elem.alignment())

    @alignment.setter
    def alignment(self, alignment: XAPagesApplication.Alignment):
        self.set_property('alignment', alignment.value)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def text_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.textColor())

    @text_color.setter
    def text_color(self, text_color: XABase.XAColor):
        self.set_property('textColor', text_color.xa_elem)

    @property
    def text_wrap(self) -> bool:
        return self.xa_elem.textWrap()

    @text_wrap.setter
    def text_wrap(self, text_wrap: bool):
        self.set_property('textWrap', text_wrap)

    @property
    def background_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property('backgroundColor', background_color.xa_elem)

    @property
    def vertical_alignment(self) -> XAPagesApplication.Alignment:
        return XAPagesApplication.Alignment(self.xa_elem.verticalAlignment())

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment: XAPagesApplication.Alignment):
        self.set_property('verticalAlignment', vertical_alignment.value)

    def clear(self) -> Self:
        """Clears the content of every cell in the range.

        :return: The range object
        :rtype: Self

        :Example 1: Clear all cells in a table

        >>> import PyXA
        >>> app = PyXA.Application("Pages")
        >>> range = app.documents()[0].slides()[0].tables()[0].cell_range
        >>> range.clear()

        :Example 2: Clear all cells whose value is 3

        >>> import PyXA
        >>> app = PyXA.Application("Pages")
        >>> cells = app.documents()[0].slides()[0].tables()[0].cells()
        >>> for cell in cells:
        >>>     if cell.value == 3:
        >>>         cell.clear()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.clear()
        return self

    def merge(self) -> Self:
        """Merges all cells in the range.

        :return: The range object
        :rtype: Self

        :Example 1: Merge all cells in the first row of a table

        >>> import PyXA
        >>> app = PyXA.Application("Pages")
        >>> table = app.documents()[0].slides()[0].tables()[0]
        >>> row = table.rows()[0]
        >>> row.merge()

        :Example 2: Merge all cells in the first column of a table

        >>> import PyXA
        >>> app = PyXA.Application("Pages")
        >>> table = app.documents()[0].slides()[0].tables()[0]
        >>> col = table.columns()[0]
        >>> col.merge()

        .. note::

           If you merge an entire row, then merge an entire column, all cells in the table will be merged. The same is true if the row and column operations are flipped.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.merge()
        return self

    def unmerge(self) -> Self:
        """Unmerges all cells in the range.

        :return: The range object
        :rtype: Self

        :Example 1: Unmerge all merged cells

        >>> import PyXA
        >>> app = PyXA.Application("Pages")
        >>> range = app.documents()[0].slides()[0].tables()[0].cell_range
        >>> range.unmerge()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> 'XAPagesCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAPagesCellList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAPagesCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAPagesColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAPagesColumnList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAPagesColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAPagesRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAPagesRowList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAPagesRowList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAPagesRowList(XAPagesRangeList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesRow)
        logger.debug("Got list of table rows")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each row in the list.

        :return: A list of row properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = super().properties()
        for index, raw_dict in enumerate(raw_dicts):
            properties = pyxa_dicts[index]
            properties["address"] = raw_dict["address"]
            properties["height"] = raw_dict["height"]
        return pyxa_dicts

    def address(self) -> list[float]:
        """Gets the address of each row in the list.

        :return: A list of row addresses
        :rtype: list[float]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def height(self) -> list[int]:
        """Gets the height of each row in the list.

        :return: A list of row heights
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def by_properties(self, properties: dict) -> Union['XAPagesRow', None]:
        """Retrieves the first row whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAPagesRow, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "background_color" in properties:
            raw_dict["backgroundColor"] = properties["background_color"].xa_elem

        if "font_size" in properties:
            raw_dict["fontSize"] = properties["font_size"]

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "format" in properties:
            raw_dict["format"] = properties["format"].value

        if "vertical_alignment" in properties:
            raw_dict["verticalAlignment"] = XAEvents.event_from_type_code(properties["vertical_alignment"].value)

        if "font_name" in properties:
            raw_dict["fontName"] = properties["font_name"]

        if "alignment" in properties:
            raw_dict["alignment"] = XAEvents.event_from_type_code(properties["alignment"].value)

        if "text_wrap" in properties:
            raw_dict["textWrap"] = properties["text_wrap"]

        if "text_color" in properties:
            raw_dict["textColor"] = properties["text_color"].xa_elem

        if "address" in properties:
            raw_dict["address"] = properties["address"]

        if "height" in properties:
            raw_dict["height"] = properties["height"]

        for page_range in self.xa_elem:
            if all([raw_dict[x] == page_range.properties()[x] for x in raw_dict]):
                return self._new_element(page_range, XAPagesRow)

    def by_address(self, address: float) -> Union['XAPagesRow', None]:
        """Retrieves the first row whose address matches the given address, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAPagesRow, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("address", address)

    def by_height(self, height: int) -> Union['XAPagesRow', None]:
        """Retrieves the first row whose height matches the given height, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAPagesRow, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("height", height)

class XAPagesRow(XAPagesRange):
    """A class for managing and interacting with table rows in Pages.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int #: The index of the row in the table
        self.height: float #: The height of the row in pixels

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["address"] = raw_dict["address"]
        properties["height"] = raw_dict["height"]
        return properties

    @property
    def address(self) -> int:
        return self.xa_elem.address()

    @property
    def height(self) -> float:
        return self.xa_elem.height()

    @height.setter
    def height(self, height: float):
        self.set_property('height', height)




class XAPagesColumnList(XAPagesRangeList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesColumn)
        logger.debug("Got list of table columns")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each column in the list.

        :return: A list of column properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = super().properties()
        for index, raw_dict in enumerate(raw_dicts):
            properties = pyxa_dicts[index]
            properties["address"] = raw_dict["address"]
            properties["width"] = raw_dict["width"]
        return pyxa_dicts

    def address(self) -> list[float]:
        """Gets the address of each column in the list.

        :return: A list of column addresses
        :rtype: list[float]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> list[int]:
        """Gets the width of each column in the list.

        :return: A list of column widths
        :rtype: list[int]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_properties(self, properties: dict) -> Union['XAPagesColumn', None]:
        """Retrieves the first column whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAPagesColumn, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "background_color" in properties:
            raw_dict["backgroundColor"] = properties["background_color"].xa_elem

        if "font_size" in properties:
            raw_dict["fontSize"] = properties["font_size"]

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "format" in properties:
            raw_dict["format"] = properties["format"].value

        if "vertical_alignment" in properties:
            raw_dict["verticalAlignment"] = XAEvents.event_from_type_code(properties["vertical_alignment"].value)

        if "font_name" in properties:
            raw_dict["fontName"] = properties["font_name"]

        if "alignment" in properties:
            raw_dict["alignment"] = XAEvents.event_from_type_code(properties["alignment"].value)

        if "text_wrap" in properties:
            raw_dict["textWrap"] = properties["text_wrap"]

        if "text_color" in properties:
            raw_dict["textColor"] = properties["text_color"].xa_elem

        if "address" in properties:
            raw_dict["address"] = properties["address"]

        if "width" in properties:
            raw_dict["width"] = properties["width"]

        for page_range in self.xa_elem:
            if all([raw_dict[x] == page_range.properties()[x] for x in raw_dict]):
                return self._new_element(page_range, XAPagesColumn)

    def by_address(self, address: float) -> Union['XAPagesColumn', None]:
        """Retrieves the first column whose address matches the given address, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAPagesColumn, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("address", address)

    def by_width(self, width: int) -> Union['XAPagesColumn', None]:
        """Retrieves the first column whose width matches the given width, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAPagesColumn, None]
        
        .. versionadded:: 0.0.5
        """
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
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["address"] = raw_dict["address"]
        properties["width"] = raw_dict["width"]
        return properties

    @property
    def address(self) -> int:
        return self.xa_elem.address()

    @property
    def width(self) -> float:
        return self.xa_elem.width()

    @width.setter
    def width(self, width: float):
        self.set_property('width', width)




class XAPagesCellList(XAPagesRangeList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesCell)
        logger.debug("Got list of table cells")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each cell in the list.

        :return: A list of cell properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = super().properties()
        for index, raw_dict in enumerate(raw_dicts):
            properties = pyxa_dicts[index]
            properties["formatted_value"] = raw_dict["formattedValue"]
            properties["formula"] = raw_dict["formula"]
            properties["value"] = raw_dict["value"]
            properties["column"] = self._new_element(raw_dict["column"], XAPagesColumn)
            properties["row"] = self._new_element(raw_dict["row"], XAPagesRow)
        return pyxa_dicts

    def formatted_value(self) -> list[str]:
        """Gets the formatted value of each cell in the list.

        :return: A list of cell formatted values
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("formattedValue"))

    def formula(self) -> list[str]:
        """Gets the formula of each cell in the list.

        :return: A list of cell formulae
        :rtype: list[str]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("formula"))

    def value(self) -> list[Any]:
        """Gets the value of each cell in the list.

        :return: A list of cell values
        :rtype: list[Any]
        
        .. versionadded:: 0.0.5
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def column(self) -> XAPagesColumnList:
        """Gets the column of each cell in the list.

        :return: A list of cell columns
        :rtype: XAPagesColumnList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XAPagesColumnList)

    def row(self) -> XAPagesRowList:
        """Gets the row of each cell in the list.

        :return: A list of cell rows
        :rtype: XAPagesRowList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XAPagesRowList)

    def by_properties(self, properties: dict) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "background_color" in properties:
            raw_dict["backgroundColor"] = properties["background_color"].xa_elem

        if "font_size" in properties:
            raw_dict["fontSize"] = properties["font_size"]

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "format" in properties:
            raw_dict["format"] = properties["format"].value

        if "vertical_alignment" in properties:
            raw_dict["verticalAlignment"] = XAEvents.event_from_type_code(properties["vertical_alignment"].value)

        if "font_name" in properties:
            raw_dict["fontName"] = properties["font_name"]

        if "alignment" in properties:
            raw_dict["alignment"] = XAEvents.event_from_type_code(properties["alignment"].value)

        if "text_wrap" in properties:
            raw_dict["textWrap"] = properties["text_wrap"]

        if "text_color" in properties:
            raw_dict["textColor"] = properties["text_color"].xa_elem

        if "formatted_value" in properties:
            raw_dict["formattedValue"] = properties["formatted_value"]

        if "formula" in properties:
            raw_dict["formula"] = properties["formula"]

        if "value" in properties:
            raw_dict["value"] = properties["value"]

        if "column" in properties:
            raw_dict["column"] = properties["column"].xa_elem

        if "row" in properties:
            raw_dict["row"] = properties["row"].xa_elem

        for page_range in self.xa_elem:
            if all([raw_dict[x] == page_range.properties()[x] for x in raw_dict]):
                return self._new_element(page_range, XAPagesCell)

    def by_formatted_value(self, formatted_value: str) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose formatted value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose formula matches the given formula, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("value", value)

    def by_column(self, column: XAPagesColumn) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose column matches the given column, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XAPagesRow) -> Union['XAPagesCell', None]:
        """Retrieves the first cell whose row matches the given row, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAPagesCell, None]
        
        .. versionadded:: 0.0.5
        """
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
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["formatted_value"] = raw_dict["formattedValue"]
        properties["formula"] = raw_dict["formula"]
        properties["value"] = raw_dict["value"]
        properties["column"] = self._new_element(raw_dict["column"], XAPagesColumn)
        properties["row"] = self._new_element(raw_dict["row"], XAPagesRow)
        return properties

    @property
    def formatted_value(self) -> str:
        return self.xa_elem.formattedValue()

    @property
    def formula(self) -> str:
        return self.xa_elem.formula()

    @property
    def value(self) -> Union[int, float, datetime, str, bool, None]:
        return self.xa_elem.value().get()

    @value.setter
    def value(self, value: Union[int, float, datetime, str, bool, None]):
        self.set_property('value', value)

    @property
    def column(self) -> XAPagesColumn:
        return self._new_element(self.xa_elem.column(), XAPagesColumn)

    @property
    def row(self) -> XAPagesRow:
        return self._new_element(self.xa_elem.row(), XAPagesRow)