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

    @property
    def active_doc(self) -> 'XAAcrobatReaderDocument':
        """The active document.
        """
        return self._new_element(self.xa_scel.activeDoc(), XAAcrobatReaderDocument)

    @active_doc.setter
    def active_doc(self, active_doc: 'XAAcrobatReaderDocument'):
        self.set_property('activeDoc', active_doc.xa_elem)

    @property
    def active_tool(self) -> str:
        """The type of the currently active tool.
        """
        return self.xa_scel.activeTool()

    @active_tool.setter
    def active_tool(self, active_tool: str):
        self.set_property('activeTool', active_tool)

    @property
    def anti_alias_text(self) -> bool:
        """Whether to anti-alias text and monochrome images.
        """
        return self.xa_scel.antiAliasText()

    @anti_alias_text.setter
    def anti_alias_text(self, anti_alias_text: bool):
        self.set_property('antiAliasText', anti_alias_text)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_scel.bestType()

    @property
    def case_sensitivity(self) -> bool:
        """Whether searches are case sensitive.
        """
        return self.xa_scel.case_sensitivity()

    @case_sensitivity.setter
    def case_sensitivity(self, case_sensitivity: bool):
        self.set_property('caseSensitivity', case_sensitivity)

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_scel.default_type()

    @property
    def default_zoom_factor(self) -> float:
        """The default zoom factor at which new documents are displayed.
        """
        return self.xa_scel.defaultZoomFactor()

    @default_zoom_factor.setter
    def default_zoom_factor(self, default_zoom_factor: float):
        self.set_property('defaultZoomFactor', default_zoom_factor)

    @property
    def default_zoom_type(self) -> 'XAAcrobatReaderApplication.ZoomType':
        """The default zoom type when opening a new document. Valid values are “no vary”, “fit page”, “fit width”, “fit height”, and “fit visible width”.
        """
        return XAAcrobatReaderApplication.ZoomType(self.xa_scel.defaultZoomType())

    @default_zoom_type.setter
    def default_zoom_type(self, default_zoom_type: 'XAAcrobatReaderApplication.ZoomType'):
        self.set_property('defaultZoomType', default_zoom_type.value)

    @property
    def download_entire_file(self) -> bool:
        """Whether to download the entire file.
        """
        return self.xa_scel.downloadEntireFile()

    @download_entire_file.setter
    def download_entire_file(self, download_entire_file: bool):
        self.set_property('downloadEntireFile', download_entire_file)

    @property
    def frontmost(self) -> bool:
        """Whether Reader is the frontmost application. Value can be set to true only; false not supported.
        """
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def fullscreen_transition(self) -> str:
        """Default fullscreen transition.
        """
        return self.xa_scel.fullscreenTransition()

    @property
    def fullscreen_loop(self) -> bool:
        """Loop after last page in fullscreen mode.
        """
        return self.xa_scel.fullscreenLoop()

    @property
    def fullscreen_click_advances(self) -> bool:
        """Mouse click advances in fullscreen mode.
        """
        return self.xa_scel.fullscreenClickAdvances()

    @fullscreen_click_advances.setter
    def fullscreen_click_advances(self, fullscreen_click_advances: bool):
        self.set_property('fullscreenClickAdvances', fullscreen_click_advances)

    @property
    def fullscreen_escape(self) -> bool:
        """Escape key exits fullscreen mode.
        """
        return self.xa_scel.fullscreenEscape()

    @fullscreen_escape.setter
    def fullscreen_escape(self, fullscreen_escape: type):
        self.set_property('fullscreen_escape', fullscreen_escape)

    @property
    def fullscreen_cursor(self) -> 'XAAcrobatReaderApplication.CursorSetting':
        """Cursor visibility in fullscreen mode. Valid values are “always visible”, “always hidden” or “hidden after delay”).
        """
        return XAAcrobatReaderApplication.CursorSetting(self.xa_scel.fullscreenCursor())

    @fullscreen_cursor.setter
    def fullscreen_cursor(self, fullscreen_cursor: 'XAAcrobatReaderApplication.CursorSetting'):
        self.set_property('fullscreenCursor', fullscreen_cursor.value)

    @property
    def use_fullscreen_timer(self) -> bool:
        """Whether to use a timer to advance pages in fullscreen mode.
        """
        return self.xa_elem.useFullscreenTimer()

    @use_fullscreen_timer.setter
    def use_fullscreen_timer(self, use_fullscreen_timer: bool):
        self.set_property('useFullscreenTimer', use_fullscreen_timer)

    @property
    def fullscreen_timer_delay(self) -> int:
        """The number of seconds to pause before advancing to next page in fullscreen mode.
        """
        return self.xa_elem.fullscreenTimerDelay()

    @fullscreen_timer_delay.setter
    def fullscreen_timer_delay(self, fullscreen_timer_delay: int):
        self.set_property('fullscreenTimerDelay', fullscreen_timer_delay)

    @property
    def highlight_color(self) -> XABase.XAColor:
        """Color used to highlight selections.
        """
        return XABase.XAColor(self.xa_elem.highlightColor())

    @highlight_color.setter
    def highlight_color(self, highlight_color: XABase.XAColor):
        self.set_property('highlightColor', highlight_color.xa_elem)

    @property
    def maximum_documents(self) -> int:
        """Maximum number of open documents.
        """
        return self.xa_elem.maximumDocuments()

    @property
    def name(self) -> str:
        """The application's name.
        """
        return self.xa_elem.name()

    @property
    def note_color(self) -> XABase.XAColor:
        """The color of the border around newly created text annotations.
        """
        return self.xa_elem.noteColor()

    @note_color.setter
    def note_color(self, note_color: XABase.XAColor):
        self.set_property('noteColor', note_color.xa_elem)

    @property
    def open_in_place(self) -> bool:
        """Whether to open cross document links in the same window.
        """
        return self.xa_elem.openInPlace()

    @open_in_place.setter
    def open_in_place(self, open_in_place: bool):
        self.set_property('openInPlace', open_in_place)

    @property
    def page_units(self) -> Literal["Points", "Picas", "Inches", "Millimeters", "Centimeters"]:
        """Default page display units. One of Points, Picas, Inches, Millimeters or Centimeters.
        """
        return self.xa_elem.pageUnits()

    @page_units.setter
    def page_units(self, page_units: Literal["Points", "Picas", "Inches", "Millimeters", "Centimeters"]):
        self.set_property('pageUnits', page_units)

    @property
    def page_layout(self) -> Literal["Single Page", "Continuous", "Continuous - Facing", "Facing"]:
        """Default page layout preference for a document on open (“Single Page”, “Continuous”, “Continuous - Facing”, “Facing”).
        """
        return self.xa_elem.page_layout()

    @page_layout.setter
    def page_layout(self, page_layout: Literal["Single Page", "Continuous", "Continuous - Facing", "Facing"]):
        self.set_property('pageLayout', page_layout)

    @property
    def show_splash_at_startup(self) -> bool:
        """Whether the splash screen is shown at startup.
        """
        return self.xa_elem.showSplashAtStartup()

    @show_splash_at_startup.setter
    def show_splash_at_startup(self, show_splash_at_startup: bool):
        self.set_property('showSplashAtStartup', show_splash_at_startup)

    @property
    def skip_warnings(self) -> bool:
        """Whether to skip warning dialogs during program execution.
        """
        return self.xa_elem.skipWarnings()

    @skip_warnings.setter
    def skip_warnings(self, skip_warnings: bool):
        self.set_property('skipWarnings', skip_warnings)

    @property
    def text_note_label(self) -> str:
        """The text that will appear in the “title bar” of all newly created text notes.
        """
        return self.xa_elem.textNoteLabel()

    @text_note_label.setter
    def text_note_label(self, text_note_label: str):
        self.set_property('textNoteLabel', text_note_label)

    @property
    def toolbar_visibility(self) -> bool:
        """Whether the ToolBar is visible.
        """
        return self.xa_elem.toolbarVisibility()

    @toolbar_visibility.setter
    def toolbar_visibility(self, toolbar_visibility: bool):
        self.set_property('toolbarVisibility', toolbar_visibility)

    @property
    def ui_language(self) -> str:
        """Identifies which language Reader's UI is using.  This is a 3 character language code (ENU is English, for instance).
        """
        return self.xa_elem.UILanguage()

    @property
    def version(self) -> str:
        """The version number of the application.
        """
        return self.xa_elem.version()

    @property
    def whole_word_searching(self) -> bool:
        """Whether searches are for whole words.
        """
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




class XAAcrobatReaderDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderDocument, filter)

    def best_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def bounds(self) -> list[tuple[int, int, int, int]]:
        bounds = []
        ls = self.xa_elem.arrayByApplyingSelector_("bounds") or []
        for bound in ls:
            origin = bound.origin
            size = bound.size
            bounds.append((origin.x, origin.y, size.width, size.height))
        return bounds

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def file_alias(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileAlias") or []
        return [XABase.XAPath(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def view_mode(self) -> list[XAAcrobatReaderApplication.ViewMode]:
        ls = self.xa_elem.arrayByApplyingSelector_("viewMode") or []
        return [XAAcrobatReaderApplication.ViewMode(x) for x in ls]

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderDocument', None]:
        return self.by_property("bestType", best_type)

    def by_bounds(self, bounds: tuple[int, int, int, int]) -> Union['XAAcrobatReaderDocument', None]:
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        return self.by_property("name", value)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderDocument', None]:
        return self.by_property("defaultType", default_type)

    def by_file_alias(self, file_alias: Union[str, XABase.XAPath]) -> Union['XAAcrobatReaderDocument', None]:
        if isinstance(file_alias, str):
            file_alias = XABase.XAPath(file_alias)
        return self.by_property("fileAlias", file_alias.xa_elem)

    def by_name(self, name: str) -> Union['XAAcrobatReaderDocument', None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAAcrobatReaderDocument', None]:
        return self.by_property("modified", modified)

    def by_view_mode(self, view_mode: XAAcrobatReaderApplication.ViewMode) -> Union['XAAcrobatReaderDocument', None]:
        return self.by_property("viewMode", view_mode.value)

class XAAcrobatReaderDocument(XABase.XAObject):
    """A document of Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """The boundary rectangle for the document's window, in screen coordinates (left, top, right, bottom). Note that (0,0) is in the upper left.
        """
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
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def file_alias(self) -> XABase.XAPath:
        """An alias to the file where the doc will be saved to if no other name is supplied. This is usually the same file as where it the document was read in from.
        """
        return XABase.XAPath(self.xa_elem.fileAlias())

    @property
    def name(self) -> str:
        """The document's name (as shown in the window's titlebar).
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified enough to warrant saving.
        """
        return self.xa_elem.modified()

    @property
    def view_mode(self) -> XAAcrobatReaderApplication.ViewMode:
        """The view mode of the document.
        """
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

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def name(self) -> str:
        """The document's name (as shown in the window's titlebar).
        """
        return self.xa_elem.name()

    @property
    def page_number(self) -> int:
        """The number of the current displayed page.
        """
        return self.xa_elem.pageNumber()

    @page_number.setter
    def page_number(self, page_number: int):
        self.set_property('pageNumber', page_number)

    @property
    def zoom_factor(self) -> float:
        """The current zoom factor.
        """
        return self.xa_elem.zoomFactor()

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor: float):
        self.set_property('zoomFactor', zoom_factor)

    @property
    def zoom_type(self) -> XAAcrobatReaderApplication.ZoomType:
        """The zooming and content fitting algorithm current employed.
        """
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
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def art_box(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("artBox") or [])

    def bleed_box(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bleedBox") or [])

    def crop_box(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("cropBox") or [])

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def label_text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("labelText") or [])

    def media_box(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("mediaBox") or [])

    def page_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("pageNumber") or [])

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation") or [])

    def trim_box(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("trimBox") or [])

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("bestType", best_type)

    def by_art_box(self, art_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("artBox", art_box)

    def by_bleed_box(self, bleed_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("bleedBox", bleed_box)

    def by_crop_box(self, crop_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("cropBox", crop_box)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("defaultType", default_type)

    def by_label_text(self, label_text: str) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("labelText", label_text)

    def by_media_box(self, media_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("mediaBox", media_box)

    def by_page_number(self, page_number: int) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("pageNumber", page_number)

    def by_rotation(self, rotation: int) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("rotation", rotation)

    def by_trim_box(self, trim_box: list[float]) -> Union['XAAcrobatReaderPDFPage', None]:
        return self.by_property("trimBox", trim_box)

class XAAcrobatReaderPDFPage(XAAcrobatReaderWindow):
    """A document page in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()
        
    @property
    def art_box(self) -> list[float]:
        """The art box rectangle for the page, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.artBox()

    @art_box.setter
    def art_box(self, art_box: list[float]):
        self.set_property('artBox', art_box)

    @property
    def bleed_box(self) -> list[float]:
        """The bleed box rectangle for the page, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.bleedBox()

    @bleed_box.setter
    def bleed_box(self, bleed_box: list[float]):
        self.set_property('bleedBox', bleed_box)

    @property
    def crop_box(self) -> list[float]:
        """The crop rectangle for the page, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.cropBox()

    @crop_box.setter
    def crop_box(self, crop_box: list[float]):
        self.set_property('cropBox', crop_box)

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def label_text(self) -> str:
        """The label (or custom page number) used to describe the page.
        """
        return self.xa_elem.labelText()

    @property
    def media_box(self) -> list[float]:
        """The media bounds rectangle for the page, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.mediaBox()

    @media_box.setter
    def media_box(self, media_box: list[float]):
        self.set_property('mediaBox', media_box)

    @property
    def page_number(self) -> int:
        """The page’s number.
        """
        return self.xa_elem.pageNumber()

    @property
    def rotation(self) -> int:
        """The rotation angle of the page (0, 90, 180, 270).
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def trim_box(self) -> list[float]:
        """The trim box rectangle for the page, in PDF space (left, top, right, bottom).
        """
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
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def destination_page_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("destinationPageNumber") or [])

    def destination_rectangle(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("destinationRectangle") or [])

    def fit_type(self) -> list[XAAcrobatReaderApplication.FitType]:
        ls = self.xa_elem.arrayByApplyingSelector_("fitType") or []
        return [XAAcrobatReaderApplication.FitType(x) for x in ls]

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def zoom_factor(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomFactor") or [])

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("defaultType", default_type)

    def by_destination_page_number(self, destination_page_number: int) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("destinationPageNumber", destination_page_number)

    def by_destination_rectangle(self, destination_rectangle: list[float]) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("destinationRectangle", destination_rectangle)

    def by_fit_type(self, fit_type: XAAcrobatReaderApplication.FitType) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("fitType", fit_type.value)

    def by_index(self, index: int) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("name", name)

    def by_zoom_factor(self, zoom_factor: float) -> Union['XAAcrobatReaderBookmark', None]:
        return self.by_property("zoomFactor", zoom_factor)

class XAAcrobatReaderBookmark(XABase.XAObject):
    """A bookmark of a document in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def destination_page_number(self) -> int:
        """The number of the page the PDF Window goes to when the bookmark is performed.
        """
        return self.xa_elem.destinationPageNumber()

    @destination_page_number.setter
    def destination_page_number(self, destination_page_number: int):
        self.set_property('destinationPageNumber', destination_page_number)

    @property
    def destination_rectangle(self) -> list[float]:
        """The boundary rectangle for the view of the destination, in PDF space (left, top, right, bottom). [Set this only after setting the fit type property].
        """
        return self.xa_elem.destinationRectangle()

    @destination_rectangle.setter
    def destination_rectangle(self, destination_rectangle: list[float]):
        self.set_property('destinationRectangle', destination_rectangle)

    @property
    def fit_type(self) -> XAAcrobatReaderApplication.FitType:
        """Controls how the destination rectangle is fitted to the window when the bookmark is executed.
        """
        return XAAcrobatReaderApplication.FitType(self.xa_elem.fitType())

    @fit_type.setter
    def fit_type(self, fit_type: XAAcrobatReaderApplication.FitType):
        self.set_property('fitType', fit_type.value)

    @property
    def index(self) -> int:
        """The bookmark's index within the Document.
        """
        return self.xa_elem.index()

    @property
    def name(self) -> str:
        """The bookmark's title.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def zoom_factor(self) -> float:
        """If fit type is “Left Top Zoom”, then this specifies the zoom factor, otherwise, this property is ignored. Setting this property automatically sets the fit type to “Left Top Zoom”.
        """
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
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def bounds(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds") or [])

    def color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("color") or []
        return [XABase.XAColor(x) for x in ls]

    def contents(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("contents") or [])

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def destination_page_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("destinationPageNumber") or [])

    def destination_rectangle(self) -> list[list[float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("destinationRectangle") or [])

    def fit_type(self) -> list[XAAcrobatReaderApplication.FitType]:
        ls = self.xa_elem.arrayByApplyingSelector_("fitType") or []
        # TODO
        return [XAAcrobatReaderApplication.FitType(x) for x in ls]

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def open_state(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("openState") or [])

    def subtype(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subtype") or [])

    def zoom_factor(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomFactor") or [])

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("bestType", best_type)

    def by_bounds(self, bounds: list[float]) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("bounds", bounds)

    def by_color(self, color: XABase.XAColor) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("color", color.xa_elem)

    def by_contents(self, contents: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("contents", contents)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("defaultType", default_type)

    def by_destination_page_number(self, destination_page_number: int) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("destinationPageNumber", destination_page_number)

    def by_destination_rectangle(self, destination_rectangle: list[float]) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("destinationRectangle", destination_rectangle)

    def by_fit_type(self, fit_type: XAAcrobatReaderApplication.FitType) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("fitType", fit_type.value)

    def by_name(self, name: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("name", name)

    def by_index(self, index: int) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("index", index)

    def by_modification_date(self, modification_date: datetime) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("modificationDate", modification_date)

    def by_name(self, name: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("name", name)

    def by_open_state(self, open_state: bool) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("openState", open_state)

    def by_subtype(self, subtype: str) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("subtype", subtype)

    def by_zoom_factor(self, zoom_factor: float) -> Union['XAAcrobatReaderAnnotation', None]:
        return self.by_property("zoomFactor", zoom_factor)

class XAAcrobatReaderAnnotation(XABase.XAObject):
    """An annotation in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def bounds(self) -> list[float]:
        """The boundary rectangle for the annotation, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.bounds()

    @bounds.setter
    def bounds(self, bounds: list[float]):
        self.set_property('bounds', bounds)

    @property
    def color(self) -> XABase.XAColor:
        """The color of the border around the annotation.
        """
        return XABase.XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: XABase.XAColor):
        self.set_property('color', color.xa_elem)

    @property
    def contents(self) -> str:
        """Text subtype only: The textual contents of the annotation.
        """
        return self.xa_elem.contents()

    @contents.setter
    def contents(self, contents: str):
        self.set_property('contents', contents)

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def destination_page_number(self) -> int:
        """Link subtype only: The number of the page the PDF Window goes to when the link annotation is performed.
        """
        return self.xa_elem.destinationPageNumber()

    @destination_page_number.setter
    def destination_page_number(self, destination_page_number: int):
        self.set_property('destinationPageNumber', destination_page_number)

    @property
    def destination_rectangle(self) -> list[float]:
        """Link subtype only: The boundary rectangle for the view of the destination, in PDF space (left, top, right, bottom).
        """
        return self.xa_elem.destinationRectangle()

    @destination_rectangle.setter
    def destination_rectangle(self, destination_rectangle: list[float]):
        self.set_property('destinationRectangle', destination_rectangle)

    @property
    def fit_type(self) -> XAAcrobatReaderApplication.FitType:
        """Link subtype only: Controls how the destination rectangle is fitted to the window when the annotation is performed.
        """
        return XAAcrobatReaderApplication.FitType(self.xa_elem.fitType())

    @fit_type.setter
    def fit_type(self, fit_type: XAAcrobatReaderApplication.FitType):
        self.set_property('fitType', fit_type.value)

    @property
    def index(self) -> int:
        """The annotation’s index within a Page object.
        """
        return self.xa_elem.index()

    @property
    def modification_date(self) -> datetime:
        """The date and time the annotation was last modified.
        """
        return self.xa_elem.modificationDate()

    @modification_date.setter
    def modification_date(self, modification_date: datetime):
        self.set_property('modificationDate', modification_date)

    @property
    def name(self) -> str:
        """Text subtypes only: The annotation's label.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def open_state(self) -> bool:
        """ext subtype only: Whether the annotation is open.
        """
        return self.xa_elem.openState()

    @open_state.setter
    def open_state(self, open_state: bool):
        self.set_property('openState', open_state)

    @property
    def subtype(self) -> str:
        """The subtype of the annotation.
        """
        return self.xa_elem.subtype()

    @property
    def zoom_factor(self) -> float:
        """Link subtype only: If fit type is “Left Top Zoom”, then this specifies the zoom factor, otherwise, this property is ignored. Setting this property automatically sets the fit type to “Left Top Zoom”.
        """
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
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderMenu', None]:
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderMenu', None]:
        return self.by_property("defaultType", default_type)

    def by_name(self, name: str) -> Union['XAAcrobatReaderMenu', None]:
        return self.by_property("name", name)
    
    def by_title(self, title: str) -> Union['XAAcrobatReaderMenu', None]:
        return self.by_property("title", title)

class XAAcrobatReaderMenu(XABase.XAObject):
    """An menu of Adobe Reader. Includes some menus that don't show in the UI.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def name(self) -> str:
        """The menu’s name (a language-independent name that uniquely identifies the menu).
        """
        return self.xa_elem.name()

    @property
    def title(self) -> str:
        """The menu’s title (as shown in the menu itself). This title will be in the application’s UI language.
        """
        return self.xa_elem.title()




class XAAcrobatReaderMenuItemList(XABase.XAList):
    """A wrapper around lists of menu items that employs fast enumeration techniques.

    All properties of menu items can be called as methods on the wrapped list, returning a list containing each menu item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAcrobatReaderMenuItem, filter)

    def best_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bestType") or [])

    def default_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultType") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def marked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("marked") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def has_submenu(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hasSubmenu") or [])

    def by_best_type(self, best_type: str) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("bestType", best_type)

    def by_default_type(self, default_type: str) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("defaultType", default_type)

    def by_enabled(self, enabled: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("enabled", enabled)

    def by_marked(self, marked: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("marked", marked)

    def by_name(self, name: str) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("name", name)

    def by_title(self, title: str) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("title", title)

    def by_has_submenu(self, has_submenu: bool) -> Union['XAAcrobatReaderMenuItem', None]:
        return self.by_property("hasSubmenu", has_submenu)

class XAAcrobatReaderMenuItem(XABase.XAObject):
    """An item of a menu in Adobe Reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def best_type(self) -> str:
        """The best descriptor type.
        """
        return self.xa_elem.bestType()

    @property
    def default_type(self) -> str:
        """The default descriptor type.
        """
        return self.xa_elem.defaultType()

    @property
    def enabled(self) -> bool:
        """Whether the menu item is enabled.
        """
        return self.xa_elem.enabled()

    @property
    def marked(self) -> bool:
        """Whether the menu item is checked.
        """
        return self.xa_elem.marked()

    @property
    def name(self) -> str:
        """The menu item's name (a language-independent name that uniquely identifies the menu item).
        """
        return self.xa_elem.name()

    @property
    def title(self) -> str:
        """The menu item’s title (as shown in the menu item itself). This title will be in the application’s UI language.
        """
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property('title', title)

    @property
    def has_submenu(self) -> bool:
        """Whether the menu item has a hierarchical sub-menu.
        """
        return self.xa_elem.hasSubmenu()