""".. versionadded:: 0.1.0

Control Adobe Acrobat Reader using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Union, Literal

import AppKit

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable, XADeletable, XAShowable

class XAAcrobatReaderApplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """A class for interacting with Adobe Acrobat Reader.app.

    .. versionadded:: 0.1.0
    """
    class ZoomType(Enum):
        """Options for zoom type to use when opening a new document.
        """
        NO_VARY = 0
        FIT_PAGE = 1
        FIT_WIDTH = 2
        FIT_HEIGHT = 3
        FIT_VISIBLE_WIDTH = 4

    class FitType(Enum):
        """Options for fit type.
        """
        LEFT_TOP_ZOOM = XABase.OSType('ftlz')
        FIT_PAGE = XABase.OSType('fpag')
        FIT_WIDTH = XABase.OSType('fwid')
        FIT_HEIGHT = XABase.OSType('fhei')
        FIT_RECT = XABase.OSType('frec')
        FIT_BBOX = XABase.OSType('fbbo')
        FIT_BBWIDTH = XABase.OSType('fbbw')
        FIT_BBHEIGHT = XABase.OSType('fbbh')

    class CursorSetting(Enum):
        """Options for cursor visibility.
        """
        ALWAYS_VISIBLE = XABase.OSType('show')
        ALWAYS_HIDDEN = XABase.OSType('hidn')
        HIDDEN_AFTER_DELAY = XABase.OSType('dlay')

    class ViewMode(Enum):
        """Document view modes.
        """
        NOT_VISIBLE = XABase.OSType('pnvs')
        JUST_PAGES = XABase.OSType('pgs ')
        PAGES_AND_THUMBS = XABase.OSType('pgtb')
        PAGES_AND_BOOKMARKS = XABase.OSType('pgbm')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAAcrobatReaderWindow

        self.active_doc: XAAcrobatReaderDocument #: The active document
        self.active_tool: str #: The type of the currently active tool
        self.anti_alias_text: bool #: Whether to anti-alias text and monochrome images
        self.best_type: str #: The best descriptor type
        self.case_sensitivity: bool #: Whether searches are case sensitive
        self.default_type: str #: The default descriptor type
        self.default_zoom_factor: float #: The default zoom factor at which new documents are displayed
        self.default_zoom_type: XAAcrobatReaderApplication.ZoomType #: The default zoom type when opening a new document. Valid values are “no vary”, “fit page”, “fit width”, “fit height”, and “fit visible width”
        self.download_entire_file: bool #: Whether to download the entire file
        self.frontmost: bool #: Whether Reader is the frontmost application. Value can be set to true only; false not supported
        self.fullscreen_transition: str #: Default fullscreen transition
        self.fullscreen_loop: bool #: Loop after last page in fullscreen mode
        self.fullscreen_click_advances: bool #: Mouse click advances in fullscreen mode
        self.fullscreen_escape: bool #: Escape key exits fullscreen mode
        self.fullscreen_cursor: str #: Cursor visibility in fullscreen mode. Valid values are “always visible”, “always hidden” or “hidden after delay”)
        self.use_fullscreen_timer: bool #: Whether to use a timer to advance pages in fullscreen mode
        self.fullscren_timer_delay: int #: The number of seconds to pause before advancing to next page in fullscreen mode
        self.highlight_color: XABase.XAColor #: Color used to highlight selections
        self.maximum_documents: int #: Maximum number of open documents
        self.name: str #: The application’s name
        self.note_color: XABase.XAColor #: The color of the border around newly created text annotations
        self.open_in_place: bool #: Open cross document links in the same window
        self.page_units: str #: Default page display units. One of Points, Picas, Inches, Millimeters or Centimeters
        self.page_layout: str #: Default page layout preference for a document on open (“Single Page”, “Continuous”, “Continuous - Facing”, “Facing”)
        self.show_splash_at_startup: bool #: Whether the splash screen is shown at startup
        self.skip_warnings: bool #: Whether to skip warning dialogs during program execution
        self.text_note_label: str #: The text that will appear in the “title bar” of all newly created text notes
        self.toolbar_visibility: bool #: Whether the ToolBar is visible
        self.ui_language: str #: Identifies which language Reader's UI is using.  This is a 3 character language code (ENU is English, for instance)
        self.version: str #: The version number of the application
        self.whole_word_searching: bool #: Whether searches are for whole words

    @property
    def active_doc(self) -> 'XAAcrobatReaderDocument':
        return self._new_element(self.xa_scel.activeDoc(), XAAcrobatReaderDocument)

    @active_doc.setter
    def active_doc(self, active_doc: 'XAAcrobatReaderDocument'):
        self.set_property('activeDoc', active_doc.xa_elem)

    @property
    def active_tool(self) -> str:
        return self.xa_scel.activeTool()

    @active_tool.setter
    def active_tool(self, active_tool: str):
        self.set_property('activeTool', active_tool)

    @property
    def anti_alias_text(self) -> bool:
        return self.xa_scel.antiAliasText()

    @anti_alias_text.setter
    def anti_alias_text(self, anti_alias_text: bool):
        self.set_property('antiAliasText', anti_alias_text)

    @property
    def best_type(self) -> str:
        return self.xa_scel.bestType()

    @property
    def case_sensitivity(self) -> bool:
        return self.xa_scel.case_sensitivity()

    @case_sensitivity.setter
    def case_sensitivity(self, case_sensitivity: bool):
        self.set_property('caseSensitivity', case_sensitivity)

    @property
    def default_type(self) -> str:
        return self.xa_scel.default_type()

    @property
    def default_zoom_factor(self) -> float:
        return self.xa_scel.defaultZoomFactor()

    @default_zoom_factor.setter
    def default_zoom_factor(self, default_zoom_factor: float):
        self.set_property('defaultZoomFactor', default_zoom_factor)

    @property
    def default_zoom_type(self) -> 'XAAcrobatReaderApplication.ZoomType':
        return XAAcrobatReaderApplication.ZoomType(self.xa_scel.defaultZoomType())

    @default_zoom_type.setter
    def default_zoom_type(self, default_zoom_type: 'XAAcrobatReaderApplication.ZoomType'):
        self.set_property('defaultZoomType', default_zoom_type.value)

    @property
    def download_entire_file(self) -> bool:
        return self.xa_scel.downloadEntireFile()

    @download_entire_file.setter
    def download_entire_file(self, download_entire_file: bool):
        self.set_property('downloadEntireFile', download_entire_file)

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def fullscreen_transition(self) -> str:
        return self.xa_scel.fullscreenTransition()

    @property
    def fullscreen_loop(self) -> bool:
        return self.xa_scel.fullscreenLoop()

    @property
    def fullscreen_click_advances(self) -> bool:
        return self.xa_scel.fullscreenClickAdvances()

    @fullscreen_click_advances.setter
    def fullscreen_click_advances(self, fullscreen_click_advances: bool):
        self.set_property('fullscreenClickAdvances', fullscreen_click_advances)

    @property
    def fullscreen_escape(self) -> bool:
        return self.xa_scel.fullscreenEscape()

    @fullscreen_escape.setter
    def fullscreen_escape(self, fullscreen_escape: type):
        self.set_property('fullscreen_escape', fullscreen_escape)

    @property
    def fullscreen_cursor(self) -> 'XAAcrobatReaderApplication.CursorSetting':
        return XAAcrobatReaderApplication.CursorSetting(self.xa_scel.fullscreenCursor())

    @fullscreen_cursor.setter
    def fullscreen_cursor(self, fullscreen_cursor: 'XAAcrobatReaderApplication.CursorSetting'):
        self.set_property('fullscreenCursor', fullscreen_cursor.value)

    @property
    def use_fullscreen_timer(self) -> bool:
        return self.xa_elem.useFullscreenTimer()

    @use_fullscreen_timer.setter
    def use_fullscreen_timer(self, use_fullscreen_timer: bool):
        self.set_property('useFullscreenTimer', use_fullscreen_timer)

    @property
    def fullscreen_timer_delay(self) -> int:
        return self.xa_elem.fullscreenTimerDelay()

    @fullscreen_timer_delay.setter
    def fullscreen_timer_delay(self, fullscreen_timer_delay: int):
        self.set_property('fullscreenTimerDelay', fullscreen_timer_delay)

    @property
    def highlight_color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.highlightColor())

    @highlight_color.setter
    def highlight_color(self, highlight_color: XABase.XAColor):
        self.set_property('highlightColor', highlight_color.xa_elem)

    @property
    def maximum_documents(self) -> int:
        return self.xa_elem.maximumDocuments()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def note_color(self) -> XABase.XAColor:
        return self.xa_elem.noteColor()

    @note_color.setter
    def note_color(self, note_color: XABase.XAColor):
        self.set_property('noteColor', note_color.xa_elem)

    @property
    def open_in_place(self) -> bool:
        return self.xa_elem.openInPlace()

    @open_in_place.setter
    def open_in_place(self, open_in_place: bool):
        self.set_property('openInPlace', open_in_place)

    @property
    def page_units(self) -> Literal["Points", "Picas", "Inches", "Millimeters", "Centimeters"]:
        return self.xa_elem.pageUnits()

    @page_units.setter
    def page_units(self, page_units: Literal["Points", "Picas", "Inches", "Millimeters", "Centimeters"]):
        self.set_property('pageUnits', page_units)

    @property
    def page_layout(self) -> Literal["Single Page", "Continuous", "Continuous - Facing", "Facing"]:
        return self.xa_elem.page_layout()

    @page_layout.setter
    def page_layout(self, page_layout: Literal["Single Page", "Continuous", "Continuous - Facing", "Facing"]):
        self.set_property('pageLayout', page_layout)

    @property
    def show_splash_at_startup(self) -> bool:
        return self.xa_elem.showSplashAtStartup()

    @show_splash_at_startup.setter
    def show_splash_at_startup(self, show_splash_at_startup: bool):
        self.set_property('showSplashAtStartup', show_splash_at_startup)

    @property
    def skip_warnings(self) -> bool:
        return self.xa_elem.skipWarnings()

    @skip_warnings.setter
    def skip_warnings(self, skip_warnings: bool):
        self.set_property('skipWarnings', skip_warnings)

    @property
    def text_note_label(self) -> str:
        return self.xa_elem.textNoteLabel()

    @text_note_label.setter
    def text_note_label(self, text_note_label: str):
        self.set_property('textNoteLabel', text_note_label)

    @property
    def toolbar_visibility(self) -> bool:
        return self.xa_elem.toolbarVisibility()

    @toolbar_visibility.setter
    def toolbar_visibility(self, toolbar_visibility: bool):
        self.set_property('toolbarVisibility', toolbar_visibility)

    @property
    def ui_language(self) -> str:
        return self.xa_elem.UILanguage()

    @property
    def version(self) -> str:
        return self.xa_elem.version()

    @property
    def whole_word_searching(self) -> bool:
        return self.xa_elem.wholeWordSearching()

    @whole_word_searching.setter
    def whole_word_searching(self, whole_word_searching: bool):
        self.set_property('wholeWordSearching', whole_word_searching)

    def documents(self, filter: Union[dict, None] = None) -> 'XAAcrobatReaderDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAAcrobatReaderDocumentList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.documents(), XAAcrobatReaderDocumentList, filter)




class XAAcrobatReaderWindow(XABaseScriptable.XASBWindow):
    """A window of Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The title of the window
        self.bounds: tuple[int, int, int, int] #: The bounding rectangle for the window
        self.visible: bool #: Whether the window is visible

    @property
    def name(self) -> str:
        return self.xa_elem.name()

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
    def visible(self) -> bool:
        return self.xa_elem.visible()




class XAAcrobatReaderDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderDocument, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each document in the list.

        :return: A list of document best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def bounds(self) -> list[tuple[int, int, int, int]]:
        """Gets the bounds of each document in the list.

        :return: A list of document bounds
        :rtype: list[tuple[int, int, int, int]]
        
        .. versionadded:: 0.1.0
        """
        bounds = []
        ls = self.xa_elem.arrayByApplyingSelector_("bounds")
        for bound in ls:
            origin = bound.origin
            size = bound.size
            bounds.append((origin.x, origin.y, size.width, size.height))
        return bounds

    def default_type(self) -> list[str]:
        """Gets the default type of each document in the list.

        :return: A list of document default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def file_alias(self) -> list[XABase.XAPath]:
        """Gets the file alias of each document in the list.

        :return: A list of document file aliases
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("fileAlias")
        return [XABase.XAPath(x) for x in ls]

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

    def view_mode(self) -> list[XAAcrobatReaderApplication.ViewMode]:
        """Gets the view mode of each document in the list.

        :return: A list of document view modes
        :rtype: list[XAAcrobatReaderApplication.ViewMode]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("viewMode")
        return [XAAcrobatReaderApplication.ViewMode(x) for x in ls]

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the first document whose best type matches the given type, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_bounds(self, bounds: tuple[int, int, int, int]) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the document whose bounds match the given bounds, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        return self.by_property("name", value)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the first document whose default type matches the given type, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_file_alias(self, file_alias: Union[str, XABase.XAPath]) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the document whose file alias matches the given file, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(file_alias, str):
            file_alias = XABase.XAPath(file_alias)
        return self.by_property("fileAlias", file_alias.xa_elem)

    def by_name(self, name: str) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("modified", modified)

    def by_view_mode(self, view_mode: XAAcrobatReaderApplication.ViewMode) -> Union['XAAcrobatReaderDocument', None]:
        """Retrieves the first document whose view mode matches the given view mode, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAAcrobatReaderDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("viewMode", view_mode.value)

class XAAcrobatReaderDocument(XABase.XAObject):
    """A document of Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.bounds: tuple[int, int, int, int] #: The boundary rectangle for the document's window, in screen coordinates (left, top, right, bottom). Note that (0,0) is in the upper left.
        self.default_type: str #: The default descriptor type
        self.file_alias: str #: An alias to the file where the doc will be saved to if no other name is supplied. This is usually the same file as where it the document was read in from
        self.name: str #: The document’s name (as shown in the window’s titlebar)
        self.modified: bool #: Whether the document has been modified enough to warrant saving
        self.view_mode: XAAcrobatReaderApplication.ViewMode #: The view mode of the document

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

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
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def file_alias(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.fileAlias())

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def view_mode(self) -> XAAcrobatReaderApplication.ViewMode:
        return XAAcrobatReaderApplication.ViewMode(self.xa_elem.viewMode())

    @view_mode.setter
    def view_mode(self, view_mode: XAAcrobatReaderApplication.ViewMode):
        self.set_property('viewMode', view_mode.value)

    def bookmarks(self, filter: Union[dict, None] = None) -> 'XAAcrobatReaderBookmarkList':
        """Returns a list of bookmarks, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned bookmarks will have, or None
        :type filter: Union[dict, None]
        :return: The list of bookmarks
        :rtype: XAAcrobatReaderBookmarkList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.bookmarks(), XAAcrobatReaderBookmarkList, filter)




class XAAcrobatReaderPDFWindow(XAAcrobatReaderWindow):
    """A PDF window in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.default_type: str #: The default descriptor type
        self.name: str #: The document's name (as shown in the window's titlebar)
        self.page_number: int #: The number of the current displayed page
        self.zoom_factor: float #: The current zoom factor
        self.zoom_type: XAAcrobatReaderApplication.ZoomType #: The zooming and content fitting algorithm current employed

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def page_number(self) -> int:
        return self.xa_elem.pageNumber()

    @page_number.setter
    def page_number(self, page_number: int):
        self.set_property('pageNumber', page_number)

    @property
    def zoom_factor(self) -> float:
        return self.xa_elem.zoomFactor()

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor: float):
        self.set_property('zoomFactor', zoom_factor)

    @property
    def zoom_type(self) -> XAAcrobatReaderApplication.ZoomType:
        return self.xa_elem.zoomType()

    @zoom_type.setter
    def zoom_type(self, zoom_type: XAAcrobatReaderApplication.ZoomType):
        self.set_property('zoomType', zoom_type.value)




class XAAcrobatReaderPDFPageList(XABase.XAList):
    """A wrapper around lists of PDF pages that employs fast enumeration techniques.

    All properties of PDF pages can be called as methods on the wrapped list, returning a list containing each PDF page's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderPDFPage, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each PDF page in the list.

        :return: A list of PDF page best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def art_box(self) -> list[list[float]]:
        """Gets the art box of each PDF page in the list.

        :return: A list of PDF page art boxes
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("artBox"))

    def bleed_box(self) -> list[list[float]]:
        """Gets the bleed box of each PDF page in the list.

        :return: A list of PDF page bleed boxes
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bleedBox"))

    def crop_box(self) -> list[list[float]]:
        """Gets the crop box of each PDF page in the list.

        :return: A list of PDF page crop boxes
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("cropBox"))

    def default_type(self) -> list[str]:
        """Gets the default type of each PDF page in the list.

        :return: A list of PDF page default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def label_text(self) -> list[str]:
        """Gets the label text of each PDF page in the list.

        :return: A list of PDF page label texts
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("labelText"))

    def media_box(self) -> list[list[float]]:
        """Gets the media box of each PDF page in the list.

        :return: A list of PDF page media boxes
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("mediaBox"))

    def page_number(self) -> list[int]:
        """Gets the page number of each PDF page in the list.

        :return: A list of PDF page page numbers
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("pageNumber"))

    def rotation(self) -> list[int]:
        """Gets the rotation of each PDF page in the list.

        :return: A list of PDF page rotation amounts
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def trim_box(self) -> list[list[float]]:
        """Gets the trim box of each PDF page in the list.

        :return: A list of PDF page trim boxes
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("trimBox"))

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose best type matches the given type, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_art_box(self, art_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose art box matches the given rectangle, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("artBox", art_box)

    def by_bleed_box(self, bleed_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose blled box matches the given rectangle, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bleedBox", bleed_box)

    def by_crop_box(self, crop_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose crop box matches the given rectangle, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("cropBox", crop_box)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose default type matches the given type, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_label_text(self, label_text: str) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose page label text matches the given text, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("labelText", label_text)

    def by_media_box(self, media_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose media box matches the given rectangle, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("mediaBox", media_box)

    def by_page_number(self, page_number: int) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose page number matches the given number, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("pageNumber", page_number)

    def by_rotation(self, rotation: int) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose page rotation matches the given rotation, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("rotation", rotation)

    def by_trim_box(self, trim_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        """Retrieves the first PDF page whose trim box matches the given rectangle, if one exists.

        :return: The desired PDF page, if it is found
        :rtype: Union[XAAcrobatReaderPDFPage, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("trimBox", trim_box)

class XAAcrobatReaderPDFPage(XAAcrobatReaderWindow):
    """A document page in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.art_box: list[float] #: The art box rectangle for the page, in PDF space (left, top, right, bottom)
        self.bleed_box: list[float] #: The bleed box rectangle for the page, in PDF space (left, top, right, bottom)
        self.crop_box: list[float] #: The crop rectangle for the page, in PDF space (left, top, right, bottom)
        self.default_type: str #: The default descriptor type
        self.label_text: str #: The label (or custom page number) used to describe the page
        self.media_box: list[float] #: The media bounds rectangle for the page, in PDF space (left, top, right, bottom)
        self.page_number: int #: The page’s number.
        self.rotation: int #: The rotation angle of the page (0, 90, 180, 270)
        self.trim_box: list[float] #: The trim box rectangle for the page, in PDF space (left, top, right, bottom)

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()
        
    @property
    def art_box(self) -> list[float]:
        return self.xa_elem.artBox()

    @art_box.setter
    def art_box(self, art_box: list[float]):
        self.set_property('artBox', art_box)

    @property
    def bleed_box(self) -> list[float]:
        return self.xa_elem.bleedBox()

    @bleed_box.setter
    def bleed_box(self, bleed_box: list[float]):
        self.set_property('bleedBox', bleed_box)

    @property
    def crop_box(self) -> list[float]:
        return self.xa_elem.cropBox()

    @crop_box.setter
    def crop_box(self, crop_box: list[float]):
        self.set_property('cropBox', crop_box)

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def label_text(self) -> str:
        return self.xa_elem.labelText()

    @property
    def media_box(self) -> list[float]:
        return self.xa_elem.mediaBox()

    @media_box.setter
    def media_box(self, media_box: list[float]):
        self.set_property('mediaBox', media_box)

    @property
    def page_number(self) -> int:
        return self.xa_elem.pageNumber()

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def trim_box(self) -> list[float]:
        return self.xa_elem.trimBox()

    @trim_box.setter
    def trim_box(self, trim_box: list[float]):
        self.set_property('trimBox', trim_box)




class XAAcrobatReaderBookmarkList(XABase.XAList):
    """A wrapper around lists of bookmarks that employs fast enumeration techniques.

    All properties of bookmarks can be called as methods on the wrapped list, returning a list containing each bookmark's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderBookmark, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each bookmark in the list.

        :return: A list of bookmark best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def default_type(self) -> list[str]:
        """Gets the default type of each bookmark in the list.

        :return: A list of bookmark default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def destination_page_number(self) -> list[int]:
        """Gets the destination page number of each bookmark in the list.

        :return: A list of bookmark destination page numbers
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("destinationPageNumber"))

    def destination_rectangle(self) -> list[list[float]]:
        """Gets the destination rectangle of each bookmark in the list.

        :return: A list of bookmark destination rectangles
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("destinationRectangle"))

    def fit_type(self) -> list[XAAcrobatReaderApplication.FitType]:
        """Gets the fit type of each bookmark in the list.

        :return: A list of bookmark fit types
        :rtype: list[XAAcrobatReaderApplication.FitType]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("fitType")
        return [XAAcrobatReaderApplication.FitType(x) for x in ls]

    def index(self) -> list[int]:
        """Gets the index of each bookmark in the list.

        :return: A list of bookmark indices
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def name(self) -> list[str]:
        """Gets the name of each bookmark in the list.

        :return: A list of bookmark names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def zoom_factor(self) -> list[float]:
        """Gets the zoom factor of each bookmark in the list.

        :return: A list of bookmark zoom factors
        :rtype: list[float]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomFactor"))

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the first bookmark whose best type matches the given type, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the first bookmark whose default type matches the given type, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_destination_page_number(self, destination_page_number: int) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the bookmark whose destination page number matches the given number, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("destinationPageNumber", destination_page_number)

    def by_destination_rectangle(self, destination_rectangle: list[float]) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the bookmark whose destination rectangle matches the given rectangle, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("destinationRectangle", destination_rectangle)

    def by_fit_type(self, fit_type: XAAcrobatReaderApplication.FitType) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the first bookmark whose fit type matches the given fit type, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("fitType", fit_type.value)

    def by_index(self, index: int) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the bookmark whose index matches the given index, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the bookmark whose name matches the given name, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_zoom_factor(self, zoom_factor: float) -> Union['XAAcrobatReaderBookmark', None]:
        """Retrieves the first bookmark whose zoom factor matches the given zoom factor, if one exists.

        :return: The desired bookmark, if it is found
        :rtype: Union[XAAcrobatReaderBookmark, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("zoomFactor", zoom_factor)

class XAAcrobatReaderBookmark(XABase.XAObject):
    """A bookmark of a document in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.default_type: str #: The default descriptor type
        self.destination_page_number: int #: The number of the page the PDF Window goes to when the bookmark is performed
        self.destination_rectangle: list[float] #: The boundary rectangle for the view of the destination, in PDF space (left, top, right, bottom). [Set this only after setting the fit type property]
        self.fit_type: XAAcrobatReaderApplication.FitType #: Controls how the destination rectangle is fitted to the window when the bookmark is executed
        self.index: int #: The bookmark’s index within the Document
        self.name: str #: The bookmark’s title
        self.zoom_factor: float #: If fit type is “Left Top Zoom”, then this specifies the zoom factor, otherwise, this property is ignored. Setting this property automatically sets the fit type to “Left Top Zoom”

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def destination_page_number(self) -> int:
        return self.xa_elem.destinationPageNumber()

    @destination_page_number.setter
    def destination_page_number(self, destination_page_number: int):
        self.set_property('destinationPageNumber', destination_page_number)

    @property
    def destination_rectangle(self) -> list[float]:
        return self.xa_elem.destinationRectangle()

    @destination_rectangle.setter
    def destination_rectangle(self, destination_rectangle: list[float]):
        self.set_property('destinationRectangle', destination_rectangle)

    @property
    def fit_type(self) -> XAAcrobatReaderApplication.FitType:
        return XAAcrobatReaderApplication.FitType(self.xa_elem.fitType())

    @fit_type.setter
    def fit_type(self, fit_type: XAAcrobatReaderApplication.FitType):
        self.set_property('fitType', fit_type.value)

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def zoom_factor(self) -> float:
        return self.xa_elem.zoomFactor()

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor: float):
        self.set_property('zoomFactor', zoom_factor)




class XAAcrobatReaderAnnotationList(XABase.XAList):
    """A wrapper around lists of annotations that employs fast enumeration techniques.

    All properties of annotations can be called as methods on the wrapped list, returning a list containing each annotation's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderAnnotation, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each annotation in the list.

        :return: A list of annotation best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def bounds(self) -> list[list[float]]:
        """Gets the bounds of each annotation in the list.

        :return: A list of annotation bounds
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def color(self) -> list[XABase.XAColor]:
        """Gets the color of each annotation in the list.

        :return: A list of annotation colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("color")
        return [XABase.XAColor(x) for x in ls]

    def contents(self) -> list[str]:
        """Gets the contents of each annotation in the list.

        :return: A list of annotation contents
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("contents"))

    def default_type(self) -> list[str]:
        """Gets the default type of each annotation in the list.

        :return: A list of annotation default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def destination_page_number(self) -> list[int]:
        """Gets the destination page number of each annotation in the list.

        :return: A list of annotation destination page numbers
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("destinationPageNumber"))

    def destination_rectangle(self) -> list[list[float]]:
        """Gets the destination rectangle of each annotation in the list.

        :return: A list of annotation destination rectangles
        :rtype: list[list[float]]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("destinationRectangle"))

    def fit_type(self) -> list[XAAcrobatReaderApplication.FitType]:
        """Gets the fit type of each annotation in the list.

        :return: A list of annotation fit types
        :rtype: list[XAAcrobatReaderApplication.FitType]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("fitType")
        # TODO
        return [XAAcrobatReaderApplication.FitType(x) for x in ls]

    def index(self) -> list[int]:
        """Gets the index of each annotation in the list.

        :return: A list of annotation indices
        :rtype: list[int]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def modification_date(self) -> list[datetime]:
        """Gets the modification date of each annotation in the list.

        :return: A list of annotation modification dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def name(self) -> list[str]:
        """Gets the name of each annotation in the list.

        :return: A list of annotation names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def open_state(self) -> list[bool]:
        """Gets the open status of each annotation in the list.

        :return: A list of annotation open status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("openState"))

    def subtype(self) -> list[str]:
        """Gets the subtype of each annotation in the list.

        :return: A list of annotation subtypes
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("subtype"))

    def zoom_factor(self) -> list[float]:
        """Gets the zoom factor of each annotation in the list.

        :return: A list of annotation zoom factors
        :rtype: list[float]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zoomFactor"))

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose best type matches the given type, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_bounds(self, bounds: list[float]) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose bounds match the given bounds, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bounds", bounds)

    def by_color(self, color: XABase.XAColor) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose color matches the given color, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("color", color.xa_elem)

    def by_contents(self, contents: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose contents matches the given contents, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("contents", contents)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose default type matches the given type, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_destination_page_number(self, destination_page_number: int) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose destination page number matches the given number, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("destinationPageNumber", destination_page_number)

    def by_destination_rectangle(self, destination_rectangle: list[float]) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose destination rectangle matches the given rectangle, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("destinationRectangle", destination_rectangle)

    def by_fit_type(self, fit_type: XAAcrobatReaderApplication.FitType) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose fit type matches the given fit type, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("fitType", fit_type.value)

    def by_name(self, name: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose name matches the given name, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_index(self, index: int) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose index matches the given index, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("index", index)

    def by_modification_date(self, modification_date: datetime) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose modification date matches the given name, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("modificationDate", modification_date)

    def by_name(self, name: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose name matches the given name, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_open_state(self, open_state: bool) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose open state matches the given boolean value, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("openState", open_state)

    def by_subtype(self, subtype: str) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose subtype matches the given subtype, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("subtype", subtype)

    def by_zoom_factor(self, zoom_factor: float) -> Union['XAAcrobatReaderAnnotation', None]:
        """Retrieves the first annotation whose zoom factor matches the given zoom factor, if one exists.

        :return: The desired annotation, if it is found
        :rtype: Union[XAAcrobatReaderAnnotation, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("zoomFactor", zoomFactor)

class XAAcrobatReaderAnnotation(XABase.XAObject):
    """An annotation in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.bounds: list[float] #: The boundary rectangle for the annotation, in PDF space (left, top, right, bottom)
        self.color: XABase.XAColor #: The color of the border around the annotation
        self.contents: str #: Text subtype only: The textual contents of the annotation
        self.default_type: str #: The default descriptor type
        self.destination_page_number: int #: Link subtype only: The number of the page the PDF Window goes to when the link annotation is performed
        self.destination_rectangle: list[float] #: Link subtype only: The boundary rectangle for the view of the destination, in PDF space (left, top, right, bottom)
        self.fit_type: XAAcrobatReaderApplication.FitType #: Link subtype only: Controls how the destination rectangle is fitted to the window when the annotation is performed
        self.index: int #: The annotation’s index within a Page object
        self.modification_date: datetime #: The date and time the annotation was last modified
        self.name: str #: Text subtypes only: The annotation’s label
        self.open_state: bool #: ext subtype only: Whether the annotation is open
        self.subtype: str #: The subtype of the annotation
        self.zoom_factor: float #: Link subtype only: If fit type is “Left Top Zoom”, then this specifies the zoom factor, otherwise, this property is ignored. Setting this property automatically sets the fit type to “Left Top Zoom”

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

    @property
    def bounds(self) -> list[float]:
        return self.xa_elem.bounds()

    @bounds.setter
    def bounds(self, bounds: list[float]):
        self.set_property('bounds', bounds)

    @property
    def color(self) -> XABase.XAColor:
        return XABase.XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: XABase.XAColor):
        self.set_property('color', color.xa_elem)

    @property
    def contents(self) -> str:
        return self.xa_elem.contents()

    @contents.setter
    def contents(self, contents: str):
        self.set_property('contents', contents)

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def destination_page_number(self) -> int:
        return self.xa_elem.destinationPageNumber()

    @destination_page_number.setter
    def destination_page_number(self, destination_page_number: int):
        self.set_property('destinationPageNumber', destination_page_number)

    @property
    def destination_rectangle(self) -> list[float]:
        return self.xa_elem.destinationRectangle()

    @destination_rectangle.setter
    def destination_rectangle(self, destination_rectangle: list[float]):
        self.set_property('destinationRectangle', destination_rectangle)

    @property
    def fit_type(self) -> XAAcrobatReaderApplication.FitType:
        return XAAcrobatReaderApplication.FitType(self.xa_elem.fitType())

    @fit_type.setter
    def fit_type(self, fit_type: XAAcrobatReaderApplication.FitType):
        self.set_property('fitType', fit_type.value)

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @modification_date.setter
    def modification_date(self, modification_date: datetime):
        self.set_property('modificationDate', modification_date)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def open_state(self) -> bool:
        return self.xa_elem.openState()

    @open_state.setter
    def open_state(self, open_state: bool):
        self.set_property('openState', open_state)

    @property
    def subtype(self) -> str:
        return self.xa_elem.subtype()

    @property
    def zoom_factor(self) -> float:
        return self.xa_elem.zoomFactor()

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor: float):
        self.set_property('zoomFactor', zoom_factor)




class XAAcrobatReaderMenuList(XABase.XAList):
    """A wrapper around lists of menus that employs fast enumeration techniques.

    All properties of menus can be called as methods on the wrapped list, returning a list containing each menu's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderMenu, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each menu in the list.

        :return: A list of menu best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def default_type(self) -> list[str]:
        """Gets the default type of each menu in the list.

        :return: A list of menu default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def name(self) -> list[str]:
        """Gets the name of each menu in the list.

        :return: A list of menu names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def title(self) -> list[str]:
        """Gets the title of each menu in the list.

        :return: A list of menu titles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderMenu', None]:
        """Retrieves the first menu whose best type matches the given type, if one exists.

        :return: The desired menu, if it is found
        :rtype: Union[XAAcrobatReaderMenu, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderMenu', None]:
        """Retrieves the first menu whose default type matches the given type, if one exists.

        :return: The desired menu, if it is found
        :rtype: Union[XAAcrobatReaderMenu, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_name(self, name: str) -> Union['XAAcrobatReaderMenu', None]:
        """Retrieves the first menu whose name matches the given name, if one exists.

        :return: The desired menu, if it is found
        :rtype: Union[XAAcrobatReaderMenu, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)
    
    def by_title(self, title: str) -> Union['XAAcrobatReaderMenu', None]:
        """Retrieves the first menu whose title matches the given title, if one exists.

        :return: The desired menu, if it is found
        :rtype: Union[XAAcrobatReaderMenu, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("title", title)

class XAAcrobatReaderMenu(XABase.XAObject):
    """An menu of Adobe Reader. Includes some menus that don't show in the UI.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.default_type: str #: The default descriptor type.
        self.name: str #: The menu’s name (a language-independent name that uniquely identifies the menu)
        self.title: str #: The menu’s title (as shown in the menu itself). This title will be in the application’s UI language

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def title(self) -> str:
        return self.xa_elem.title()




class XAAcrobatReaderMenuItemList(XABase.XAList):
    """A wrapper around lists of menu items that employs fast enumeration techniques.

    All properties of menu items can be called as methods on the wrapped list, returning a list containing each menu item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderMenuItem, filter)

    def best_type(self) -> list[str]:
        """Gets the best type of each menu item in the list.

        :return: A list of menu item best types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("bestType"))

    def default_type(self) -> list[str]:
        """Gets the default type of each menu item in the list.

        :return: A list of menu item default types
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType"))

    def enabled(self) -> list[bool]:
        """Gets the enabled status of each menu item in the list.

        :return: A list of menu item enabled status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def marked(self) -> list[bool]:
        """Gets the marked status of each menu item in the list.

        :return: A list of menu item marked status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("marked"))

    def name(self) -> list[str]:
        """Gets the name of each menu item in the list.

        :return: A list of menu item names
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def title(self) -> list[str]:
        """Gets the title of each menu item in the list.

        :return: A list of menu item titles
        :rtype: list[str]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def has_submenu(self) -> list[bool]:
        """Gets the has submenu status of each menu item in the list.

        :return: A list of menu item has submenu status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("hasSubmenu"))

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose best type matches the given type, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose default type matches the given type, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultType", default_type)

    def by_enabled(self, enabled: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose enabled status matches the given boolean value, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("enabled", enabled)

    def by_marked(self, marked: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose marked status matches the given boolean value, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("marked", marked)

    def by_name(self, name: str) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose name matches the given name, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_title(self, title: str) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose title matches the given title, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("title", title)

    def by_has_submenu(self, has_submenu: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        """Retrieves the first menu item whose has submenu status matches the given boolean value, if one exists.

        :return: The desired menu item, if it is found
        :rtype: Union[XAAcrobatReaderMenuItem, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("hasSubmenu", has_submenu)

class XAAcrobatReaderMenuItem(XABase.XAObject):
    """An item of a menu in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.best_type: str #: The best descriptor type
        self.default_type: str #: The default descriptor type.
        self.enabled: bool #: Whether the menu item is enabled
        self.marked: bool #: Whether the menu item is checked
        self.name: str #: The menu item's name (a language-independent name that uniquely identifies the menu item)
        self.title: str #: The menu item’s title (as shown in the menu item itself). This title will be in the application’s UI language
        self.has_submenu: bool #: Whether the menu item has a hierarchical sub-menu

    @property
    def best_type(self) -> str:
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        return self.xa_elem.defaultType()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def marked(self) -> bool:
        return self.xa_elem.marked()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def title(self) -> str:
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property('title', title)

    @property
    def has_submenu(self) -> bool:
        return self.xa_elem.hasSubmenu()