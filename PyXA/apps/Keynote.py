""".. versionadded:: 0.0.2

Control the macOS Keynote application using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from pprint import pprint
from time import sleep
from typing import Any, Union, Self

import AppKit, ScriptingBridge
import logging

from PyXA import XABase
from PyXA import XAEvents
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACloseable

logger = logging.getLogger("keynote")

class XAKeynoteApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Keynote.app.

    .. seealso:: :class:`XAKeynoteWindow`, :class:`XAKeynoteDocument`

    .. versionadded:: 0.0.2
    """
    class ExportFormat(Enum):
        """Options for what format to export a Keynote project as.
        """
        KEYNOTE                 = OSType('Knff') # The Keynote native file format 
        HTML                    = OSType('Khtm') # HTML 
        QUICKTIME_MOVIE         = OSType('Kmov') # QuickTime movie 
        PDF                     = OSType('Kpdf') # PDF 
        SLIDE_IMAGES            = OSType('Kimg') # image 
        MICROSOFT_POWERPOINT    = OSType('Kppt') # Microsoft PowerPoint 
        KEYNOTE_09              = OSType('Kkey') # Keynote 09 
        JPEG                    = OSType('Kifj') # JPEG 
        PNG                     = OSType('Kifp') # PNG 
        TIFF                    = OSType('Kift') # TIFF 
        f360p                   = OSType('Kmf3') # 360p 
        f540p                   = OSType('Kmf5') # 540p 
        f720p                   = OSType('Kmf7') # 720p 
        f1080p                  = OSType('Kmf8') # 1080p 
        f2160p                  = OSType('Kmf4') # DCI 4K (4096x2160) 
        NativeSize              = OSType('KmfN') # Exported movie will have the same dimensions as the document, up to 4096x2160 

    class Codec(Enum):
        """Options for which video codec to use.
        """
        H264                    = OSType('Kmc1') # H.264 
        APPLE_PRO_RES_422       = OSType('Kmc2') # Apple ProRes 422 
        APPLE_PRO_RES_4444      = OSType('Kmc3') # Apple ProRes 4444 
        APPLE_PRO_RES_422LT     = OSType('Kmc4') # Apple ProRes 422LT 
        APPLE_PRO_RES_422HQ     = OSType('Kmc5') # Apple ProRes 422HQ 
        APPLE_PRO_RES_422Proxy  = OSType('Kmc6') # Apple ProRes 422Proxy 
        HEVC                    = OSType('Kmc7') # HEVC 

    class Framerate(Enum):
        """Options for which framerate to use when exporting a Keynote project as a video.
        """
        FPS_12     = OSType('Kfr1') # 12 FPS 
        FPS_2398   = OSType('Kfr2') # 23.98 FPS 
        FPS_24     = OSType('Kfr3') # 24 FPS 
        FPS_25     = OSType('Kfr4') # 25 FPS 
        FPS_2997   = OSType('Kfr5') # 29.97 FPS 
        FPS_30     = OSType('Kfr6') # 30 FPS 
        FPS_50     = OSType('Kfr7') # 50 FPS 
        FPS_5994   = OSType('Kfr8') # 59.94 FPS 
        FPS_60     = OSType('Kfr9') # 60 FPS 

    class PrintSetting(Enum):
        """Options to use when printing slides.
        """
        STANDARD_ERROR_HANDLING = OSType('lwst') # Standard PostScript error handling 
        DETAILED_ERROR_HANDLING = OSType('lwdt') # print a detailed report of PostScript errors 
        INDIVIDUAL_SLIDES       = OSType('Kpwi') # individual slides 
        SLIDE_WITH_NOTES        = OSType('Kpwn') # slides with notes 
        HANDOUTS                = OSType('Kpwh') # handouts 

    class ImageQuality(Enum):
        """Options for the quality of exported images.
        """
        GOOD      = OSType('KnP0') # good quality 
        BETTER    = OSType('KnP1') # better quality 
        BEST      = OSType('KnP2') # best quality 

    class Transition(Enum):
        """The available options for transitions to assign to slides.
        """
        NONE                = OSType('tnil') 
        MAGIC_MOVE          = OSType('tmjv')   
        SHIMMER             = OSType('tshm')  
        SPARKLE             = OSType('tspk')   
        SWING               = OSType('tswg')   
        OBJECT_CUBE         = OSType('tocb')   
        OBJECT_FLIP         = OSType('tofp')   
        OBJECT_POP          = OSType('topp')   
        OBJECT_PUSH         = OSType('toph')   
        OBJECT_REVOLVE      = OSType('torv')   
        OBJECT_ZOOM         = OSType('tozm')   
        PERSPECTIVE         = OSType('tprs')   
        CLOTHESLINE         = OSType('tclo')   
        CONFETTI            = OSType('tcft')   
        DISSOLVE            = OSType('tdis')   
        DROP                = OSType('tdrp')   
        DROPLET             = OSType('tdpl')   
        FADE_THROUGH_COLOR  = OSType('tftc')   
        GRID                = OSType('tgrd')   
        IRIS                = OSType('tirs')   
        MOVE_IN             = OSType('tmvi')   
        PUSH                = OSType('tpsh')   
        REVEAL              = OSType('trvl')   
        SWITCH              = OSType('tswi')   
        WIPE                = OSType('twpe')   
        BLINDS              = OSType('tbld')   
        COLOR_PANES         = OSType('tcpl')   
        CUBE                = OSType('tcub')   
        DOORWAY             = OSType('tdwy')   
        FALL                = OSType('tfal')   
        FLIP                = OSType('tfip')   
        FLOP                = OSType('tfop')   
        MOSAIC              = OSType('tmsc')   
        PAGE_FLIP           = OSType('tpfl')   
        PIVOT               = OSType('tpvt')   
        REFLECTION          = OSType('trfl')   
        REVOLVING_DOOR      = OSType('trev')   
        SCALE               = OSType('tscl')   
        SWAP                = OSType('tswp')   
        SWOOSH              = OSType('tsws')   
        TWIRL               = OSType('ttwl')   
        TWIST               = OSType('ttwi')   
        FADE_AND_MOVE       = OSType('tfad')   

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

    class ChartType(Enum):
        """Options for available chart types.
        """
        PIE_2D                      = OSType('pie2') #: Two-dimensional pie chart 
        VERTICAL_BAR_2D             = OSType('vbr2') #: Two-dimensional vertical bar chart 
        STACKED_VERTICAL_BAR_2D     = OSType('svb2') #: Two-dimensional stacked vertical bar chart 
        HORIZONTAL_BAR_2D           = OSType('hbr2') #: Two-dimensional horizontal bar chart 
        STACKED_HORIZONTAL_BAR_2D   = OSType('shb2') #: Two-dimensional stacked horizontal bar chart 
        PIE_3D                      = OSType('pie3') #: Three-dimensional pie chart. 
        VERTICAL_BAR_3D             = OSType('vbr3') #: Three-dimensional vertical bar chart 
        STACKED_VERTICAL_BAR_3D     = OSType('svb3') #: Three-dimensional stacked bar chart 
        HORIZONTAL_BAR_3D           = OSType('hbr3') #: Three-dimensional horizontal bar chart 
        STACKED_HORIZONTAL_BAR_3D   = OSType('shb3') #: Three-dimensional stacked horizontal bar chart 
        AREA_2D                     = OSType('are2') #: Two-dimensional area chart. 
        STACKED_AREA_2D             = OSType('sar2') #: Two-dimensional stacked area chart 
        LINE_2D                     = OSType('lin2') #: Two-dimensional line chart. 
        LINE_3D                     = OSType('lin3') #: Three-dimensional line chart 
        AREA_3D                     = OSType('are3') #: Three-dimensional area chart 
        STACKED_AREA_3D             = OSType('sar3') #: Three-dimensional stacked area chart 
        SCATTERPLOT_2D              = OSType('scp2') #: Two-dimensional scatterplot chart 

    class ChartGrouping(Enum):
        """Options for how data is grouped within a chart.
        """
        ROW      = OSType('KCgr') # group by row
        COLUMN   = OSType('KCgc') # group by column

    class KeyAction(Enum):
        """Options for key states and interactions.
        """
        COMMAND_DOWN = OSType('Kcmd')
        CONTROL_DOWN = OSType('Kctl')
        OPTION_DOWN  = OSType('Kopt')
        SHIFT_DOWN   = OSType('Ksft')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAKeynoteWindow

        self.properties: dict #: All properties of the Keynote application
        self.name: str #: The name of the Keynote application
        self.frontmost: bool #: Whether Keynote is the active application
        self.version: str #: The Keynote version number

        logger.debug("Initialized XAKeynoteApplication")

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_scel.properties()
        return {
            "slide_switcher_visible": raw_dict["slideSwitcherVisible"] == 1,
            "frontmost": self.frontmost,
            "playing": self.playing,
            "version": self.version,
            "name": self.name,
        }

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
    def playing(self) -> bool:
        return self.xa_scel.playing()

    @property
    def slide_switcher_visible(self) -> bool:
        return self.xa_scel.slideSwitcherVisible()

    def show_next(self) -> 'XAKeynoteApplication':
        """Advance one slide or animation build.
        """
        self.xa_scel.showNext()
        return self

    def show_previous(self) -> 'XAKeynoteApplication':
        """Go back one slide or animation build.
        """
        self.xa_scel.showPrevious()
        return self

    def print(self, item: Union['XAKeynoteDocument', XABaseScriptable.XASBWindow]) -> 'XAKeynoteApplication':
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, {}, True)
        return self

    def documents(self, filter: Union[dict, None] = None) -> 'XAKeynoteDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAKeynoteDocumentList

        :Example 1: List the name of every open Keynote document

        >>> import PyXA
        >>> app = PyXA.Application("Keynote")
        >>> docs = app.documents()
        >>> for doc in docs:
        >>>     print(doc.name)
        Example1.key
        Example2.key

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.documents(), XAKeynoteDocumentList, filter)

    def new_document(self, file_path: str = "./Untitled.key", theme: 'XAKeynoteTheme' = None) -> 'XAKeynoteDocument':
        if isinstance(file_path, str):
            file_path = AppKit.NSURL.alloc().initFileURLWithPath_(file_path)
        properties = {
            "file": file_path,
        }
        if theme is not None:
            properties["documentTheme"] = theme.xa_elem
        return self.push("document", properties, self.xa_scel.documents())

    def new_slide(self, document: 'XAKeynoteDocument', properties: dict):
        return self.push("slide", properties, document.xa_elem.slides())

    def themes(self, filter: Union[dict, None] = None) -> 'XAKeynoteThemeList':
        """Returns a list of themes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned themes will have, or None
        :type filter: Union[dict, None]
        :return: The list of themes
        :rtype: XAKeynoteThemeList

        :Example 1: List the name of each theme

        >>> import PyXA
        >>> app = PyXA.Application("Keynote")
        >>> themes = app.themes()
        >>> print(themes.name())
        ['Basic White', 'Basic Black', 'Classic White', 'White', 'Black', 'Basic Color', 'Color Gradient Light', 'Color Gradient', 'Gradient', 'Showroom', 'Modern Portfolio', 'Slate', 'Photo Essay', 'Bold Color', 'Showcase', 'Briefing', 'Academy', 'Modern Type', 'Exhibition', 'Feature Story', 'Look Book', 'Classic', 'Editorial', 'Cream Paper', 'Industrial', 'Blueprint', 'Graph Paper', 'Chalkboard', 'Photo Portfolio', 'Leather Book', 'Artisan', 'Improv', 'Drafting', 'Kyoto', 'Brushed Canvas', 'Craft', 'Parchment', 'Renaissance', 'Moroccan', 'Hard Cover', 'Linen Book', 'Vintage', 'Typeset', 'Harmony', 'Formal']

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.themes(), XAKeynoteThemeList, filter)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.5
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XAKeynoteDocument)
        elif specifier == "shape":
            return self._new_element(obj, XAKeynoteShape)
        elif specifier == "table":
            return self._new_element(obj, XAKeynoteTable)
        elif specifier == "audioClip":
            return self._new_element(obj, XAKeynoteAudioClip)
        elif specifier == "chart":
            return self._new_element(obj, XAKeynoteChart)
        elif specifier == "image":
            return self._new_element(obj, XAKeynoteImage)
        elif specifier == "slide":
            return self._new_element(obj, XAKeynoteSlide)
        elif specifier == "line":
            return self._new_element(obj, XAKeynoteLine)
        elif specifier == "movie":
            return self._new_element(obj, XAKeynoteMovie)
        elif specifier == "textItem":
            return self._new_element(obj, XAKeynoteTextItem)
        elif specifier == "group":
            return self._new_element(obj, XAKeynoteGroup)
        elif specifier == "slide":
            return self._new_element(obj, XAKeynoteSlide)
        elif specifier == "iWorkItem":
            return self._new_element(obj, XAKeynoteiWorkItem)
        elif specifier == "TransitionSettings":
            return self._new_element(obj, XAKeynoteTransitionSettings)




class XAKeynoteWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject):
    """A class for managing and interacting with windows in Keynote.app.

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
        self.document: XAKeynoteDocument #: The document currently displayed in the window

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
    def document(self) -> 'XAKeynoteDocument':
        return self._new_element(self.xa_elem.document(), XAKeynoteDocument)




class XAKeynoteDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteDocument, filter)
        logger.debug("Got list of documents")

    def properties(self) -> list[dict]:
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, document in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "name": document.name(),
                "modified": document.modified(),
                "file": XABase.XAPath(document.file()),
                "id": document.id(),
                "slide_numbers_showing": document.slideNumbersShowing(),
                "document_theme": self._new_element(document.documentTheme(), XAKeynoteTheme),
                "auto_loop": document.autoLoop(),
                "auto_play": document.autoPlay(),
                "auto_restart": document.autoRestart(),
                "maximum_idle_duration": document.maximumIdleDuration(),
                "current_slide": self._new_element(document.currentSlide(), XAKeynoteSlide),
                "height": document.height(),
                "width": document.width(),
                "selection": [self._new_element(x, XAKeynoteiWorkItem) for x in document.selection()],
                "password_protected": document.passwordProtected(),
            }
        return pyxa_dicts

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def slide_numbers_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("slideNumbersShowing"))

    def document_theme(self) -> 'XAKeynoteThemeList':
        ls = self.xa_elem.arrayByApplyingSelector_("documentTheme")
        return self._new_element(ls, XAKeynoteThemeList)

    def auto_loop(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoLoop"))

    def auto_play(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoPlay"))

    def auto_restart(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoRestart"))

    def maximum_idle_duration(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximumIdleDuration"))

    def current_slide(self) -> 'XAKeynoteSlideList':
        ls = self.xa_elem.arrayByApplyingSelector_("currentSlide")
        return self._new_element(ls, XAKeynoteSlideList)

    def height(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def selection(self) -> 'XAKeynoteiWorkItemList':
        ls = [x for y in self.xa_elem.arrayByApplyingSelector_("selection") for x in y]
        return self._new_element(ls, XAKeynoteiWorkItemList)

    def password_protected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> Union['XAKeynoteDocument', None]:
        raw_dict = {}

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        if "file" in properties:
            if isinstance(properties["file"], str):
                raw_dict["file"] = properties["file"]
            else:
                raw_dict["file"] = properties["file"].xa_elem

        if "slide_numbers_showing" in properties:
            raw_dict["slideNumbersShowing"] = properties["slide_numbers_showing"]

        if "document_theme" in properties:
            raw_dict["documentTheme"] = properties["document_theme"].xa_elem

        if "auto_loop" in properties:
            raw_dict["autoLoop"] = properties["auto_loop"]

        if "auto_play" in properties:
            raw_dict["autoPlay"] = properties["auto_play"]

        if "auto_restart" in properties:
            raw_dict["autoRestart"] = properties["auto_restart"]

        if "maximum_idle_duration" in properties:
            raw_dict["maximumIdleDuration"] = properties["maximum_idle_duration"]

        if "height" in properties:
            raw_dict["height"] = properties["height"]

        if "width" in properties:
            raw_dict["width"] = properties["width"]

        for document in self.xa_elem:
            if all(raw_dict[x] == document.properties()[x] for x in raw_dict):
                return self._new_element(document, XAKeynoteDocument)

    def by_name(self, name: str) -> Union['XAKeynoteDocument', None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("modified", modified)

    def by_file(self, file: Union[XABase.XAPath, str]) -> Union['XAKeynoteDocument', None]:
        if isinstance(file, XABase.XAPath):
            file = file.path
        return self.by_property("file", file)

    def by_id(self, id: str) -> Union['XAKeynoteDocument', None]:
        return self.by_property("id", id)

    def by_slide_numbers_showing(self, slide_numbers_showing: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("slideNumbersShowing", slide_numbers_showing)

    def by_document_theme(self, document_theme: 'XAKeynoteTheme') -> Union['XAKeynoteDocument', None]:
        return self.by_property("documentTheme", document_theme.xa_elem)

    def by_auto_loop(self, auto_loop: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("autoLoop", auto_loop)

    def by_auto_play(self, auto_play: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("autoPlay", auto_play)

    def by_auto_restart(self, auto_restart: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("autoRestart", auto_restart)

    def by_maximum_idle_duration(self, maximum_idle_duration: int) -> Union['XAKeynoteDocument', None]:
        return self.by_property("maxmimumIdleDuration", maximum_idle_duration)

    def by_current_slide(self, current_slide: 'XAKeynoteSlide') -> Union['XAKeynoteDocument', None]:
        return self.by_property("currentSlide", current_slide.xa_elem)

    def by_height(self, height: int) -> Union['XAKeynoteDocument', None]:
        return self.by_property("height", height)

    def by_width(self, width: int) -> Union['XAKeynoteDocument', None]:
        return self.by_property("width", width)

    def by_selection(self, selection: 'XAKeynoteiWorkItemList') -> Union['XAKeynoteDocument', None]:
        return self.by_property("selection", selection.xa_elem)

    def by_password_protected(self, password_protected: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("passwordProtected", password_protected)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XAKeynoteDocument(XABaseScriptable.XASBPrintable, XACloseable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.file: XABase.XAPath #: The location of the document on the disk, if one exists
        self.id: str #: The unique identifier for the document
        self.slide_numbers_showing: bool #: Whether slide numbers are displayed
        self.document_theme: XAKeynoteTheme #: The theme assigned to the document
        self.auto_loop: bool #: Whether the slideshow should play repeatedly
        self.auto_play: bool #: Whether the slideshow should automatically play when opening the file
        self.auto_restart: bool #: Whether the slideshow should restart if its inactive for the maximum idle duration
        self.maximum_idle_duration: int #: The duration before which the slideshow restarts due to inactivity
        self.current_slide: XAKeynoteSlide #: The currently selected slide, or the slide that would display is the presentation was started

        self.height: int #: The height of the document in points; standard is 768; wide slide height is 1080
        self.width: int #: The width of the document in points; standard is 1080; wide slide width is 1920
        self.selection: XAKeynoteiWorkItemList #: A list of the currently selected items
        self.password_protected: bool #: Whether the document is password protected

    @property
    def properties(self) -> dict:
        pyxa_dict = {
            "name": self.xa_elem.name(),
            "modified": self.xa_elem.modified(),
            "file": XABase.XAPath(self.xa_elem.file()),
            "id": self.xa_elem.id(),
            "slide_numbers_showing": self.xa_elem.slideNumbersShowing(),
            "document_theme": self._new_element(self.xa_elem.documentTheme(), XAKeynoteTheme),
            "auto_loop": self.xa_elem.autoLoop(),
            "auto_play": self.xa_elem.autoPlay(),
            "auto_restart": self.xa_elem.autoRestart(),
            "maximum_idle_duration": self.xa_elem.maximumIdleDuration(),
            "current_slide": self._new_element(self.xa_elem.currentSlide(), XAKeynoteSlide),
            "height": self.xa_elem.height(),
            "width": self.xa_elem.width(),
            "selection": self._new_element(self.xa_elem.selection(), XAKeynoteiWorkItemList),
            "password_protected": self.xa_elem.passwordProtected(),
        }
        return pyxa_dict

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
    def slide_numbers_showing(self) -> bool:
        return self.xa_elem.slideNumbersShowing()

    @slide_numbers_showing.setter
    def slide_numbers_showing(self, slide_numbers_showing: bool):
        self.set_property('slideNumbersShowing', slide_numbers_showing)

    @property
    def document_theme(self) -> 'XAKeynoteTheme':
        return self._new_element(self.xa_elem.documentTheme(), XAKeynoteTheme)

    @document_theme.setter
    def document_theme(self, document_theme: 'XAKeynoteTheme'):
        self.set_property('documentTheme', document_theme.xa_elem)

    @property
    def auto_loop(self) -> bool:
        return self.xa_elem.autoLoop()

    @auto_loop.setter
    def auto_loop(self, auto_loop: bool):
        self.set_property('autoLoop', auto_loop)

    @property
    def auto_play(self) -> bool:
        return self.xa_elem.autoPlay()

    @auto_play.setter
    def auto_play(self, auto_play: bool):
        self.set_property('autoPlay', auto_play)

    @property
    def auto_restart(self) -> bool:
        return self.xa_elem.autoRestart()

    @auto_restart.setter
    def auto_restart(self, auto_restart: bool):
        self.set_property('autoRestart', auto_restart)

    @property
    def maximum_idle_duration(self) -> int:
        return self.xa_elem.maximumIdleDuration()

    @maximum_idle_duration.setter
    def maximum_idle_duration(self, maximum_idle_duration: int):
        self.set_property('maximumIdleDuration', maximum_idle_duration)

    @property
    def current_slide(self) -> 'XAKeynoteSlide':
        return self._new_element(self.xa_elem.currentSlide(), XAKeynoteSlide)

    @current_slide.setter
    def current_slide(self, current_slide: 'XAKeynoteSlide'):
        self.set_property('currentSlide', current_slide.xa_elem)

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def selection(self) -> 'XAKeynoteiWorkItemList':
        return self._new_element(self.xa_elem.selection(), XAKeynoteiWorkItemList)

    @selection.setter
    def selection(self, selection: Union['XAKeynoteiWorkItemList', list['XAKeynoteiWorkItem']]):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property('selection', selection)
        else:
            self.set_property('selection', selection.xa_elem)

    @property
    def password_protected(self) -> bool:
        return self.xa_elem.passwordProtected()

    def start_from(self, slide: 'XAKeynoteSlide') -> 'XAKeynoteSlide':
        """Starts the slideshow from the specified slide.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.startFrom_(slide.xa_elem)
        return self

    def stop(self):
        """Stops the currently playing slideshow.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.stop()

    def show_slide_switcher(self):
        """Shows the slide switch within the active slideshow interface.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSlideSwitcher()

    def hide_slide_switcher(self):
        """Hides the slide switcher.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.hideSlideSwitcher()

    def move_slide_switcher_forward(self):
        """Advances the slide switcher one slide forward.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.moveSlideSwitcherForward()

    def move_slide_switcher_backward(self):
        """Goes back one slide in the slide switcher.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.moveSlideSwitcherBackward()

    def cancel_slide_switcher(self):
        """Dismisses the slide switcher.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.cancelSlideSwitcher()

    def accept_slide_switcher(self):
        """Advances the slideshow to the selected slide of the slide switcher.
        
        .. versionadded:: 0.0.3
        """
        self.xa_elem.acceptSlideSwitcher()

    def save(self):
        """Saves the Keynote file.
        
        .. versionadded:: 0.0.3
        """
        export_format = XAKeynoteApplication.ExportFormat.KEYNOTE.value
        self.xa_elem.saveIn_as_(self.file, export_format)

    def export(self, file_path: Union[str, XABase.XAPath] = None, format: XAKeynoteApplication.ExportFormat = XAKeynoteApplication.ExportFormat.PDF):
        """Exports the slideshow in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, XABase.XAPath], optional
        :param format: The format to export the file in, defaults to XAKeynoteApplication.ExportFormat.PDF
        :type format: XAKeynoteApplication.ExportFormat, optional

        .. versionadded:: 0.0.3
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path.xa_elem, format.value, None)

    def make_image_slides(self, files: list[Union[str, XABase.XAPath]], set_titles: bool = False, slide_layout: 'XAKeynoteSlideLayout' = None) -> 'XAKeynoteDocument':
        """Creates slides out of image files.

        Creates a new slide for each image file path in the files list, if the image can be found.

        :param files: A list of paths to image files
        :type files: list[Union[str, XABase.XAPath]]
        :param set_titles: Whether to set the slide titles to the image file name, defaults to False
        :type set_titles: bool, optional
        :param slide_layout: The base slide layout to use for the new slides, defaults to None
        :type slide_layout: XAKeynoteSlideLayout, optional
        :return: A reference back to this PyXA object.
        :rtype: XAKeynoteDocument

        .. versionadded:: 0.0.3
        """
        urls = []
        for file in files:
            if isinstance(file, str):
                file = XABase.XAPath(file)
            urls.append(file.xa_elem)
        self.xa_elem.makeImageSlidesFiles_setTitles_slideLayout_(urls, set_titles, slide_layout)
        return self

    def slides(self, filter: Union[dict, None] = None) -> 'XAKeynoteSlideList':
        """Returns a list of slides, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned slides will have, or None
        :type filter: Union[dict, None]
        :return: The list of slides
        :rtype: XAKeynoteSlideList

        :Example 1: List all slides

        >>> import PyXA
        >>> app = PyXA.Application("Keynotes")
        >>> print(app.slides())

        :Example 2: List slides after applying a filter

        >>> import PyXA
        >>> app = PyXA.Application("Keynotes")
        >>> print(app.slides().greater_than("slideNumber", 5))

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.slides(), XAKeynoteSlideList, filter)

    def new_slide(self, properties: dict) -> 'XAKeynoteSlide':
        """Creates a new slide at the end of the presentation.

        :param properties: The properties to give the new slide
        :type properties: dict
        :return: A reference to the newly created slide
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        return self.xa_prnt.xa_prnt.new_slide(self, properties)

    def slide_layouts(self, filter: Union[dict, None] = None) -> 'XAKeynoteSlideLayoutList':
        """Returns a list of slide layouts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned slide layouts will have, or None
        :type filter: Union[dict, None]
        :return: The list of slide layouts
        :rtype: XAKeynoteSlideLayoutList

        :Example: List all slide layouts

        >>> import PyXA
        >>> app = PyXA.Application("Keynotes")
        >>> print(app.slide_layouts())

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.slideLayouts(), XAKeynoteSlideLayoutList, filter)

    def __repr__(self):
        return f"<{str(type(self))}{self.name}>"




class XAKeynoteThemeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteTheme, filter)
        logger.debug("Got list of themes")

    def properties(self) -> list[str]:
        # TODO
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, theme in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "id": theme.id(),
                "name": theme.name()
            }
        return pyxa_dicts

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_properties(self, properties: dict) -> Union['XAKeynoteTheme', None]:
        for theme in self.xa_elem:
            if all(properties[x] == theme.properties()[x] for x in properties):
                return self._new_element(theme, XAKeynoteTheme)

    def by_id(self, id: str) -> Union['XAKeynoteTheme', None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XAKeynoteTheme', None]:
        return self.by_property("name", name)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XAKeynoteTheme(XABase.XAObject):
    """A class for managing and interacting with Keynote themes.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the theme
        self.id: str #: The unique identifier for the theme
        self.name: str #: The name of the theme

    @property
    def properties(self) -> dict:
        return {
            "id": self.xa_elem.id(),
            "name": self.xa_elem.name()
        }

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def __repr__(self):
        return f"<{str(type(self))}{self.name}, id={str(self.id)}>"




class XAKeynoteContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAKeynoteContainer
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of containers")

        # Specialize to XAKeynoteGroupList or XAKeynoteSlideList object
        if self.__class__ == XAKeynoteContainerList:
            if all([x.parent().get() == None for x in self.xa_elem]):
                new_self = self._new_element(self.xa_elem, XAKeynoteSlideList)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAKeynoteContainerList to XAKeynoteSlideList")

            elif all([x.parent().get() != None for x in self.xa_elem]):
                new_self = self._new_element(self.xa_elem, XAKeynoteGroupList)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAKeynoteContainerList to XAKeynoteGroupList")

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self.xa_elem)) + ">"

class XAKeynoteContainer(XABase.XAObject):
    """A class for managing and interacting with containers in Keynote.

    .. seealso:: :class:`XAKeynoteApplication`, :class:`XAKeynoteiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

        # Specialize to XAKeynoteGroup or XAKeynoteSlide object
        if self.__class__ == XAKeynoteContainer:
            if self.xa_elem.baseLayout().get() is not None:
                new_self = self._new_element(self.xa_elem, XAKeynoteSlide)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAKeynoteContainer to XAKeynoteSlide")

            elif self.xa_elem.parent().get() is not None:
                new_self = self._new_element(self.xa_elem, XAKeynoteGroup)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
                logger.debug("Specialized XAKeynoteContainer to XAKeynoteGroup")

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAKeynoteiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XAKeynoteiWorkItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAKeynoteiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAKeynoteAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XAKeynoteAudioClipList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), XAKeynoteAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAKeynoteChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XAKeynoteChartList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), XAKeynoteChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAKeynoteImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XAKeynoteImageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), XAKeynoteImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAKeynoteGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAKeynoteGroupList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), XAKeynoteGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAKeynoteLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XAKeynoteLineList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), XAKeynoteLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XAKeynoteMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XAKeynoteMovieList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), XAKeynoteMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAKeynoteShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XAKeynoteShapeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), XAKeynoteShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAKeynoteTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XAKeynoteTableList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), XAKeynoteTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAKeynoteTextItemList':
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: XAKeynoteTextItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), XAKeynoteTextItemList, filter)




class XAKeynoteSlideList(XAKeynoteContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteSlide)
        logger.debug("Got list of slides")

    def properties(self) -> list[dict]:
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "default_title_item": self._new_element(raw_dict["defaultTitleItem"], XAKeynoteShape),
                "slide_number": raw_dict["slideNumber"],
                "default_body_item": self._new_element(raw_dict["defaultBodyItem"], XAKeynoteShape),
                "skipped": raw_dict["skipped"] == 1,
                "body_showing": raw_dict["bodyShowing"] == 1,
                "presenter_notes": self._new_element(raw_dict["presenterNotes"], XABase.XAText),
                "title_showing": raw_dict["titleShowing"] == 1,
                "transition_properties": XAKeynoteTransitionSettings({
                    "automatic_transition": raw_dict["transitionProperties"]["automaticTransition"] == 1,
                    "transition_delay": raw_dict["transitionProperties"]["transitionDelay"],
                    "transtion_duration": raw_dict["transitionProperties"]["transitionDuration"],
                    "transition_effect": XAKeynoteApplication.Transition(XABase.OSType(raw_dict["transitionProperties"]["transitionEffect"].stringValue()))
                }, self._new_element(self.xa_elem[index], XAKeynoteSlide)),
                "base_layout": self._new_element(raw_dict["baseLayout"], XAKeynoteSlideLayout)
            }
        return pyxa_dicts

    def body_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyShowing"))

    def skipped(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("skipped"))

    def slide_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("slideNumber"))

    def title_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("titleShowing"))

    def transition_properties(self) -> list[dict]:
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("transitionProperties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = XAKeynoteTransitionSettings({
                "automatic_transition": raw_dict["automaticTransition"] == 1,
                "transition_delay": raw_dict["transitionDelay"],
                "transtion_duration": raw_dict["transitionDuration"],
                "transition_effect": XAKeynoteApplication.Transition(XABase.OSType(raw_dict["transitionEffect"].stringValue()))
            }, self._new_element(self.xa_elem[index], XAKeynoteSlide))
        return pyxa_dicts

    def base_layout(self) -> 'XAKeynoteSlideLayoutList':
        ls = self.xa_elem.arrayByApplyingSelector_("baseLayout")
        return self._new_element(ls, XAKeynoteSlideLayoutList)

    def default_body_item(self) -> 'XAKeynoteShapeList':
        ls = self.xa_elem.arrayByApplyingSelector_("defaultBodyItem")
        return self._new_element(ls, XAKeynoteShapeList)

    def default_title_item(self) -> 'XAKeynoteShapeList':
        ls = self.xa_elem.arrayByApplyingSelector_("defaultTitleItem")
        return self._new_element(ls, XAKeynoteShapeList)

    def presenter_notes(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("presenterNotes")
        return self._new_element(ls, XABase.XATextList)

    def by_properties(self, properties: dict) -> 'XAKeynoteSlide':
        raw_dict = {}

        if "default_title_item" in properties:
            raw_dict["defaultTitleItem"] = properties["default_title_item"].xa_elem

        if "slide_number" in properties:
            raw_dict["slideNumber"] = properties["slide_number"]
        
        if "default_body_item" in properties:
            raw_dict["defaultBodyItem"] = properties["default_body_item"].xa_elem

        if "skipped" in properties:
            raw_dict["skipped"] = properties["skipped"]

        if "body_showing" in properties:
            raw_dict["bodyShowing"] = properties["body_showing"]

        if "presenter_notes" in properties:
            if isinstance(properties["presenter_notes"], str):
                raw_dict["presenterNotes"] = properties["presenter_notes"]
            else:
                raw_dict["presenterNotes"] = properties["presenter_notes"].xa_elem

        if "title_showing" in properties:
            raw_dict["titleShowing"] = properties["title_showing"]

        if "transition_properties" in properties:
            raw_dict["transitionProperties"] = {}
            if isinstance(properties["transition_properties"], XAKeynoteTransitionSettings):
                properties["transition_properties"] = properties["transition_properties"]._pyxa_dict

            if "automatic_transition" in properties["transition_properties"]:
                raw_dict["transitionProperties"]["automaticTransition"] = properties["transition_properties"]["automatic_transition"]

            if "transition_delay" in properties["transition_properties"]:
                raw_dict["transitionProperties"]["transitionDelay"] = properties["transition_properties"]["transition_delay"]
                
            if "transtion_duration" in properties["transition_properties"]:
                raw_dict["transitionProperties"]["transitionDuration"] = properties["transition_properties"]["transtion_duration"]
                
            if "transition_effect" in properties["transition_properties"]:
                raw_dict["transitionProperties"]["transitionEffect"] = XAEvents.event_from_type_code(properties["transition_properties"]["transition_effect"].value)

        if "base_layout" in properties:
            raw_dict["baseLayout"] = properties["base_layout"].xa_elem

        for slide in self.xa_elem:
            if all(raw_dict[x] == slide.properties()[x] for x in raw_dict):
                return self._new_element(slide, XAKeynoteSlide)

    def by_body_showing(self, body_showing: bool) -> 'XAKeynoteSlide':
        return self.by_property("bodyShowing", body_showing)

    def by_skipped(self, skipped: bool) -> 'XAKeynoteSlide':
        return self.by_property("skipped", skipped)

    def by_slide_number(self, slide_number: int) -> 'XAKeynoteSlide':
        return self.by_property("slideNumber", slide_number)

    def by_title_showing(self, title_showing: bool) -> 'XAKeynoteSlide':
        return self.by_property("titleShowing", title_showing)

    def by_transition_properties(self, transition_properties: Union['XAKeynoteTransitionSettings', dict]) -> 'XAKeynoteSlide':
        properties = {}
        if isinstance(transition_properties, XAKeynoteTransitionSettings):
            transition_properties = transition_properties._pyxa_dict

        if "automatic_transition" in transition_properties:
            properties["automaticTransition"] = transition_properties["automatic_transition"]

        if "transition_delay" in transition_properties:
            properties["transitionDelay"] = transition_properties["transition_delay"]
            
        if "transtion_duration" in transition_properties:
            properties["transitionDuration"] = transition_properties["transtion_duration"]
            
        if "transition_effect" in transition_properties:
            properties["transitionEffect"] = XAEvents.event_from_type_code(transition_properties["transition_effect"].value)

        return self.by_property("transitionProperties", properties)

    def by_base_layout(self, base_layout: 'XAKeynoteSlideLayout') -> 'XAKeynoteSlide':
        return self.by_property("baseLayout", base_layout.xa_elem)

    def by_default_body_item(self, default_body_item: 'XAKeynoteShape') -> 'XAKeynoteSlide':
        return self.by_property("defaultBodyItem", default_body_item.xa_elem)

    def by_default_text_item(self, default_text_item: 'XAKeynoteShape') -> 'XAKeynoteSlide':
        return self.by_property("defaultTextItem", default_text_item.xa_elem)

    def by_presenter_notes(self, presenter_notes: Union[str, XABase.XAText]) -> 'XAKeynoteSlide':
        if isinstance(presenter_notes, str):
            self.by_property('presenterNotes', presenter_notes)
        else:
            self.by_property('presenterNotes', presenter_notes.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self.xa_elem)) + ">"

class XAKeynoteSlide(XAKeynoteContainer):
    """A class for managing and interacting with Keynote slides.

    .. seealso:: :class:`XAKeynoteApplication`, :class:`XAKeynoteiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the slide
        self.body_showing: bool #: Whether the default body text is displayed
        self.skipped: bool #: Whether the slide is skipped
        self.slide_number: int #: The index of the slide in the document
        self.title_showing: bool #: Whether the default slide title is displayed
        self.transition_properties: dict #: The transition settings applied to the slide
        self.base_layout: XAKeynoteSlideLayout #: The slide layout this slide is based on
        self.default_body_item: XAKeynoteShape #: The default body container of the slide
        self.default_title_item: XAKeynoteShape #: The default title container of the slide
        self.presenter_notes: XABase.XAText #: The presenter notes for the slide

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "default_title_item": self._new_element(raw_dict["defaultTitleItem"], XAKeynoteShape),
            "slide_number": raw_dict["slideNumber"],
            "default_body_item": self._new_element(raw_dict["defaultBodyItem"], XAKeynoteShape),
            "skipped": raw_dict["skipped"] == 1,
            "body_showing": raw_dict["bodyShowing"] == 1,
            "presenter_notes": self._new_element(raw_dict["presenterNotes"], XABase.XAText),
            "title_showing": raw_dict["titleShowing"] == 1,
            "transition_properties": XAKeynoteTransitionSettings({
                "automatic_transition": raw_dict["transitionProperties"]["automaticTransition"] == 1,
                "transition_delay": raw_dict["transitionProperties"]["transitionDelay"],
                "transition_duration": raw_dict["transitionProperties"]["transitionDuration"],
                "transition_effect": XAKeynoteApplication.Transition(XABase.OSType(raw_dict["transitionProperties"]["transitionEffect"].stringValue()))
            }, self),
            "base_layout": self._new_element(raw_dict["baseLayout"], XAKeynoteSlideLayout)
        }
        return pyxa_dict

    @property
    def body_showing(self) -> bool:
        return self.xa_elem.bodyShowing()

    @body_showing.setter
    def body_showing(self, body_showing: bool):
        self.set_property('bodyShowing', body_showing)

    @property
    def skipped(self) -> bool:
        return self.xa_elem.skipped()

    @skipped.setter
    def skipped(self, skipped: bool):
        self.set_property('skipped', skipped)

    @property
    def slide_number(self) -> int:
        return self.xa_elem.slideNumber()

    @property
    def title_showing(self) -> bool:
        return self.xa_elem.titleShowing()

    @title_showing.setter
    def title_showing(self, title_showing: bool):
        self.set_property('titleShowing', title_showing)

    @property
    def transition_properties(self) -> dict:
        raw_dict = self.xa_elem.transitionProperties()
        pyxa_dict = {
            "automatic_transition": raw_dict["automaticTransition"] == 1,
            "transition_delay": raw_dict["transitionDelay"],
            "transition_duration": raw_dict["transitionDuration"],
            "transition_effect": XAKeynoteApplication.Transition(XABase.OSType(raw_dict["transitionEffect"].stringValue()))
        }
        return XAKeynoteTransitionSettings(pyxa_dict, self)

    @transition_properties.setter
    def transition_properties(self, transition_properties: Union['XAKeynoteTransitionSettings', dict]):
        properties = {}
        if isinstance(transition_properties, XAKeynoteTransitionSettings):
            transition_properties = transition_properties._pyxa_dict

        if "automatic_transition" in transition_properties:
            properties["automaticTransition"] = transition_properties["automatic_transition"]

        if "transition_delay" in transition_properties:
            properties["transitionDelay"] = transition_properties["transition_delay"]
            
        if "transtion_duration" in transition_properties:
            properties["transitionDuration"] = transition_properties["transtion_duration"]
            
        if "transition_effect" in transition_properties:
            properties["transitionEffect"] = XAEvents.event_from_type_code(transition_properties["transition_effect"].value)
        
        self.set_property('transitionProperties', properties)

    @property
    def base_layout(self) -> 'XAKeynoteSlideLayout':
        return self._new_element(self.xa_elem.baseLayout(), XAKeynoteSlideLayout)

    @base_layout.setter
    def base_layout(self, base_layout: 'XAKeynoteSlideLayout'):
        self.set_property('baseLayout', base_layout.xa_elem)

    @property
    def default_body_item(self) -> 'XAKeynoteShape':
        return self._new_element(self.xa_elem.defaultBodyItem(), XAKeynoteShape)

    @property
    def default_title_item(self) -> 'XAKeynoteShape':
        return self._new_element(self.xa_elem.defaultTitleItem(), XAKeynoteShape)

    @property
    def presenter_notes(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.presenterNotes(), XABase.XAText)

    @presenter_notes.setter
    def presenter_notes(self, presenter_notes: Union[XABase.XAText, str]):
        if isinstance(presenter_notes, str):
            self.set_property('presenterNotes', presenter_notes)
        else:
            self.set_property('presenterNotes', presenter_notes.xa_elem)

    def duplicate(self) -> 'XAKeynoteSlide':
        """Duplicates the slide, mimicking the action of copying and pasting the slide manually.

        :return: A reference to newly created (duplicate) slide object.
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        new_slide = None
        if isinstance(self.xa_prnt, XAKeynoteSlideList):
            # Parent is an XAList object -- we can natively use positionAfter()
            self.xa_elem.duplicateTo_withProperties_(self.xa_elem.positionAfter(), None)
            new_slide = self._new_element(self.xa_prnt.xa_prnt.xa_elem.slides()[-1], XAKeynoteSlide)
        else:
            # Parent is an XADocument object -- we have to get an NSArray instance
            slide = self.xa_prnt.xa_elem.slides()[self.slide_number - 1]
            slide.duplicateTo_withProperties_(slide.positionAfter(), None)
            new_slide = self._new_element(self.xa_prnt.xa_elem.slides()[-1], XAKeynoteSlide)
        return new_slide

    def delete(self):
        """Deletes the slide.

        .. versionadded:: 0.0.2
        """
        self.xa_elem.delete()

    def add_image(self, file_path: Union[str, XABase.XAPath, XABase.XAURL]) -> 'XAKeynoteImage':
        """Adds the image at the specified path to the slide.

        :param file_path: The path to the image file.
        :type file_path: Union[str, XABase.XAPath, XABase.XAURL]
        :return: The newly created image object.
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        url = file_path
        if isinstance(url, str):
            if "://" in url:
                url = XABase.XAURL(url)
            else:
                url = XABase.XAPath(url)

        image = None

        parent = self.xa_prnt.xa_prnt
        max_backtracks = 6 # this -> slidelist -> document -> document list -> window -> window list -> application
        num_backtracks = 0
        while not hasattr(parent, "make") and num_backtracks < max_backtracks:
            parent = parent.xa_prnt
            num_backtracks += 1

        image = parent.make("image", { "file": url.xa_elem })
        return self.images().push(image)

    def add_chart(self, row_names: list[str], column_names: list[str], data: list[list[Any]], type: int = XAKeynoteApplication.ChartType.LINE_2D.value, group_by: int = XAKeynoteApplication.ChartGrouping.ROW.value) -> 'XAKeynoteChart':
        """_summary_

        _extended_summary_

        :param row_names: A list of row names.
        :type row_names: list[str]
        :param column_names: A list of column names.
        :type column_names: list[str]
        :param data: A 2d array 
        :type data: list[list[Any]]
        :param type: The chart type, defaults to _KeynoteLegacyChartType.KeynoteLegacyChartTypeLine_2d.value
        :type type: int, optional
        :param group_by: The grouping schema, defaults to _KeynoteLegacyChartGrouping.KeynoteLegacyChartGroupingChartRow.value
        :type group_by: int, optional
        :return: A reference to the newly created chart object.
        :rtype: XAKeynoteChart

        .. versionadded:: 0.0.2
        """
        parent = self.xa_prnt
        max_backtracks = 2 # this -> slidelist -> document
        num_backtracks = 0
        while not isinstance(parent, XAKeynoteDocument) and num_backtracks < max_backtracks:
            parent = parent.xa_prnt
            num_backtracks += 1

        self.xa_prnt.set_property("currentSlide", self.xa_elem)
        self.xa_elem.addChartRowNames_columnNames_data_type_groupBy_(row_names, column_names, data, type, group_by)
        chart = self.xa_elem.charts()[-1].get()
        return self._new_element(chart, XAKeynoteChart)

    def __repr__(self):
        return "<" + str(type(self)) + "slide number: " + str(self.slide_number) + ">"




class XAKeynoteSlideLayoutList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteSlideLayout, filter)
        logger.debug("Got list of slide layouts")

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_name(self, name: str) -> 'XAKeynoteSlideLayout':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAKeynoteSlideLayout(XAKeynoteSlide):
    """A class for managing and interacting with Keynote slide layouts.

    .. seealso:: :class:`XAKeynoteSlide`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name #: The name of the slide layout

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAKeynoteiWorkItemList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAKeynoteiWorkItem
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of iWork items")

    def height(self) -> list[int]:
        return [x.height() for x in self.xa_elem]

    def locked(self) -> list[bool]:
        return [x.locked() for x in self.xa_elem]

    def width(self) -> list[int]:
        return [x.width() for x in self.xa_elem]

    def parent(self) -> XAKeynoteContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAKeynoteContainerList)

    def position(self) -> list[tuple[int, int]]:
        return [tuple(x.position()) for x in self.xa_elem]

    def by_height(self, height: int) -> 'XAKeynoteiWorkItem':
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> 'XAKeynoteiWorkItem':
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> 'XAKeynoteiWorkItem':
        return self.by_property("width", width)

    def by_parent(self, parent: XAKeynoteContainer) -> 'XAKeynoteiWorkItem':
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: tuple[int, int]) -> 'XAKeynoteiWorkItem':
        return self.by_property("position", position)

    def __repr__(self):
        return "<" + str(type(self)) + "positions: " + str(self.position()) + ">"

class XAKeynoteiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Keynote.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int #: The height of the iWork item
        self.locked: bool #: Whether the object is locked
        self.width: int #: The width of the iWork item
        self.parent: XAKeynoteContainer #: The iWork container that contains the iWork item
        self.position: tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the iWork item

        if self.__class__ == XAKeynoteiWorkItem:
            description = self.xa_elem.get().description()

            # Specialize to some iWork Item type
            new_self = None
            if ": defaultTitleItem" in description or ": defaultBodyItem" in description or ": <class 'sshp'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteShape)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteShape")
            elif ": <class 'imag'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteImage)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteImage")
            elif ": <class 'igrp'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteGroup)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteGroup")
            elif ": <class 'shtx'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteTextItem)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteTextItem")
            elif ": <class 'NmTb'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteTable)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteTable")
            elif ": <class 'iWln'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteLine)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteLine")
            elif ": <class 'shmv'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteMovie)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteMovie")
            elif ": <class 'shau'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteAudioClip)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteAudioClip")
            elif ": <class 'shct'>" in description:
                new_self = self._new_element(self.xa_elem, XAKeynoteChart)
                logger.debug("Specialized XAKeynoteiWorkItem to XAKeynoteChart")

            if new_self is not None:
                new_self.xa_prnt = self.xa_prnt
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
            else:
                print(description)

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
    def parent(self) -> XAKeynoteContainer:
        return self._new_element(self.xa_elem.parent(), XAKeynoteContainer)

    @property
    def position(self) -> tuple[int, int]:
        return tuple(self.xa_elem.position())

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.0.2
        """
        self.xa_elem.delete()

    def duplicate(self) -> 'XAKeynoteiWorkItem':
        """Duplicates the item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        if isinstance(self.xa_prnt, XAKeynoteiWorkItemList):
            self.xa_elem.duplicateTo_withProperties_(self.xa_elem.positionAfter(), {})
        else:
            self.xa_elem.duplicateTo_withProperties_(self.xa_prnt.xa_elem.iWorkItems(), {})
        return self

    def resize(self, width: int, height: int) -> 'XAKeynoteiWorkItem':
        """Sets the width and height of the item.

        :param width: The desired width, in pixels
        :type width: int
        :param height: The desired height, in pixels
        :type height: int
        :return: The iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        self.set_properties({
            "width": width,
            "height": height,
        })
        return self

    def lock(self) -> 'XAKeynoteiWorkItem':
        """Locks the properties of the item, preventing changes.

        :return: The iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        self.set_property("locked", True)
        return self

    def unlock(self) -> 'XAKeynoteiWorkItem':
        """Unlocks the properties of the item, allowing changes.

        :return: The iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        self.set_property("locked", False)
        return self

    def set_position(self, x: int, y: int) -> 'XAKeynoteiWorkItem':
        position = AppKit.NSValue.valueWithPoint_(AppKit.NSPoint(x, y))
        self.xa_elem.setValue_forKey_(position, "position")

    def __repr__(self):
        return "<" + str(type(self)) + "position: " + str(self.position) + ">"





class XAKeynoteGroupList(XAKeynoteContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteGroup)
        logger.debug("Got list of groups")

    def height(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def position(self) -> list[tuple[int, int]]:
        ls = self.xa_elem.arrayByApplyingSelector_("position")
        return [tuple(point.pointValue()) for point in ls]

    def width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def parent(self) -> XAKeynoteContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAKeynoteContainerList)

    def by_height(self, height: int) -> 'XAKeynoteGroup':
        return self.by_property("height", height)

    def by_position(self, position: tuple[int, int]) -> 'XAKeynoteGroup':
        return self.by_property("position", position)

    def by_width(self, width: int) -> 'XAKeynoteGroup':
        return self.by_property("width", width)

    def by_rotation(self, rotation: int) -> 'XAKeynoteGroup':
        return self.by_property("rotation", rotation)

    def by_parent(self, parent: XAKeynoteContainer) -> 'XAKeynoteGroup':
        return self.by_property("parent", parent.xa_elem)

class XAKeynoteGroup(XAKeynoteContainer):
    """A class for managing and interacting with iWork item groups in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int #: The height of the group
        self.position: tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the group
        self.width: int #: The widht of the group
        self.rotation: int #: The rotation of the group, in degrees from 0 to 359
        self.parent: XAKeynoteContainer #: The container which contains the group

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def position(self) -> tuple[int, int]:
        return self.xa_elem.position()

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
    def parent(self) -> XAKeynoteContainer:
        return self._new_element(self.xa_elem.parent(), XAKeynoteContainer)




class XAKeynoteImageList(XAKeynoteiWorkItemList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteImage)
        logger.debug("Got list of images")

    def description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def file(self) -> list[str]:
        return [x.file() for x in self.xa_elem]

    def file_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def opacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_description(self, description: str) -> 'XAKeynoteImage':
        return self.by_property("objectDescription", description)

    def by_file(self, file: str) -> 'XAKeynoteImage':
        return self.by_property("file", file)

    def by_file_name(self, file_name: str) -> 'XAKeynoteImage':
        return self.by_property("fileName", file_name)

    def by_opacity(self, opacity: int) -> 'XAKeynoteImage':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteImage':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteImage':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteImage':
        return self.by_property("rotation", rotation)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XAKeynoteImage(XAKeynoteiWorkItem):
    """A class for managing and interacting with images in Keynote.

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
        self.set_property('description', description)

    @property
    def file(self) -> str:
        return self.xa_elem.file()

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
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> 'XAKeynoteImage':
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: XAKeynoteImage

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.2
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, XABase.XAPath, XABase.XAURL]) -> 'XAKeynoteImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, XABase.XAPath, XABase.XAURL]
        :return: A reference to the new PyXA image object.
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        self.delete()
        if isinstance(img_path, str):
            if "://" in img_path:
                img_path = XABase.XAURL(img_path)
            else:
                img_path = XABase.XAPath(img_path)

        parent = self.xa_prnt
        while not isinstance(parent, XAKeynoteSlide):
            parent = parent.xa_prnt

        return parent.add_image(img_path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAKeynoteAudioClipList(XAKeynoteiWorkItemList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteAudioClip)
        logger.debug("Got list of audio clips")

    def file_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> list[XAKeynoteApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAKeynoteApplication.RepetitionMethod(XABase.OSType(x.stringValue())) for x in ls]

    def by_file_name(self, file_name: str) -> 'XAKeynoteAudioClip':
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> 'XAKeynoteAudioClip':
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XAKeynoteApplication.RepetitionMethod) -> 'XAKeynoteAudioClip':
        for audio_clip in self.xa_elem:
            if audio_clip.repetitionMethod() == repetition_method.value:
                return self._new_element(audio_clip, XAKeynoteAudioClip)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XAKeynoteAudioClip(XAKeynoteiWorkItem):
    """A class for managing and interacting with audio clips in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str #: The name of the audio file
        self.clip_volume: int #: The volume setting for the audio clip, from 0 to 100
        self.repetition_method: XAKeynoteApplication.RepetitionMethod #: Whether or how the audio clip  repeats

    @property
    def file_name(self) -> str:
        return self.xa_elem.fileName().get()

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
    def repetition_method(self) -> XAKeynoteApplication.RepetitionMethod:
        return XAKeynoteApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAKeynoteApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAKeynoteShapeList(XAKeynoteiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteShape)
        logger.debug("Got list of shapes")

    def properties(self) -> list[dict]:
        return [{
            "reflection_showing": shape.reflectionShowing(),
            "rotation": shape.rotation(),
            "position": tuple(shape.position()),
            "parent": self._new_element(shape.parent(), XAKeynoteContainer),
            "width": shape.width(),
            "opacity": shape.opacity(),
            "locked": shape.locked(),
            "height": shape.height(),
            "background_fill_type": XAKeynoteApplication.FillOption(shape.backgroundFillType()),
            "reflection_value": shape.reflectionValue(),
            "object_text": shape.objectText().get()
        } for shape in self.xa_elem]

    def background_fill_type(self) -> list[XAKeynoteApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundFillType")
        return [XAKeynoteApplication.FillOption(XABase.OSType(x.stringValue())) for x in ls]

    def object_text(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("objectText")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_properties(self, properties: dict) -> Union['XAKeynoteShape', None]:
        raw_dict = {}

        if "reflection_show" in properties:
            raw_dict["reflectionShowing"] = properties["reflection_showing"]

        if "rotation" in properties:
            raw_dict["rotation"] = properties["rotation"]

        if "position" in properties:
            raw_dict["position"] = properties["position"]

        if "parent" in properties:
            raw_dict["parent"] = properties["parent"].xa_elem

        if "width" in properties:
            raw_dict["width"] = properties["width"]

        if "opacity" in properties:
            raw_dict["opacity"] = properties["opacity"]

        if "locked" in properties:
            raw_dict["locked"] = properties["lockedv"]

        if "height" in properties:
            raw_dict["height"] = properties["height"]

        if "background_fill_type" in properties:
            raw_dict["backgroundFillType"] = properties["background_fill_type"]

        if "reflection_value" in properties:
            raw_dict["reflectionValue"] = properties["reflection_value"]

        if "object_text" in properties:
            raw_dict["objectText"] = properties["object_text"]

        for shape in self.xa_elem:
            if all([raw_dict[x] == shape.properties()[x] for x in raw_dict]):
                return self._new_element(shape, XAKeynoteShape)

    def by_background_fill_type(self, background_fill_type: XAKeynoteApplication.FillOption) -> Union['XAKeynoteShape', None]:
        for shape in self.xa_elem:
            if shape.backgroundFillType() == background_fill_type.value:
                return self._new_element(shape, XAKeynoteShape)

    def by_object_text(self, object_text: Union[str, XABase.XAText]) -> Union['XAKeynoteShape', None]:
        if isinstance(object_text, str):
            return self.by_property('objectText', object_text)
        else:
            return self.by_property('objectText', object_text.xa_elem)

    def by_opacity(self, opacity: int) -> Union['XAKeynoteShape', None]:
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAKeynoteShape', None]:
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAKeynoteShape', None]:
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAKeynoteShape', None]:
        return self.by_property("rotation", rotation)

class XAKeynoteShape(XAKeynoteiWorkItem):
    """A class for managing and interacting with shapes in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the shape
        self.background_fill_type: XAKeynoteApplication.FillOption #: The background, if any, for the shape
        self.object_text: XABase.XAText #: The text contained within the shape
        self.opacity: int #: The percent opacity of the object
        self.reflection_showing: bool #: Whether the iWork item displays a reflection
        self.reflection_value: int #: The percentage of relfection that the iWork item displays, from 0 to 100
        self.rotation: int #: The rotation of the iWork item, in degrees, from 0 to 359

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def background_fill_type(self) -> XAKeynoteApplication.FillOption:
        return XAKeynoteApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def object_text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.objectText(), XABase.XAText)

    @object_text.setter
    def object_text(self, object_text: Union[str, XABase.XAText]):
        if isinstance(object_text, str):
            self.set_property('objectText', object_text)
        else:
            self.set_property('objectText', object_text.xa_elem)

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

    def rotate(self, degrees: int) -> 'XAKeynoteShape':
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: XAKeynoteShape

        .. deprecated:: 0.1.0

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.0.2
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = AppKit.NSValue.valueWithPoint_(AppKit.NSPoint(value[0], value[1]))
        super().set_property(property_name, value)




class XAKeynoteChartList(XAKeynoteiWorkItemList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteChart)
        logger.debug("Got list of charts")

class XAKeynoteChart(XAKeynoteiWorkItem):
    """A class for managing and interacting with charts in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAKeynoteLineList(XAKeynoteiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteLine)
        logger.debug("Got list of lines")

    def end_point(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("end_point"))

    def reflection_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def start_point(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("start_point"))

    def by_end_point(self, end_point: tuple[int, int]) -> 'XAKeynoteLine':
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteLine':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteLine':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteLine':
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: tuple[int, int]) -> 'XAKeynoteLine':
        return self.by_property("startPoint", start_point)

class XAKeynoteLine(XAKeynoteiWorkItem):
    """A class for managing and interacting with lines in Keynote.

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
        return self.xa_elem.endPoint()

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
        return self.xa_elem.startPoint()

    @start_point.setter
    def start_point(self, start_point: tuple[int, int]):
        self.set_property('startPoint', start_point)




class XAKeynoteMovieList(XAKeynoteiWorkItemList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteMovie)
        logger.debug("Got list of movies")

    def file_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def movie_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("movieVolume"))

    def opacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def reflection_value(self) -> list[XAKeynoteApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAKeynoteApplication.RepetitionMethod(x) for x in ls]

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_file_name(self, file_name: str) -> 'XAKeynoteMovie':
        return self.by_property("fileName", file_name)

    def by_movie_volume(self, movie_volume: int) -> 'XAKeynoteMovie':
        return self.by_property("movieVolume", movie_volume)

    def by_opacity(self, opacity: int) -> 'XAKeynoteMovie':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteMovie':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteMovie':
        return self.by_property("reflectionValue", reflection_value)

    def by_repetition_method(self, repetition_method: XAKeynoteApplication.RepetitionMethod) -> 'XAKeynoteMovie':
        return self.by_property("repetitionMethod", repetition_method.value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteMovie':
        return self.by_property("rotation", rotation)

class XAKeynoteMovie(XAKeynoteiWorkItem):
    """A class for managing and interacting with movie containers in Keynote.

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
        self.set_property('reflection_value', reflection_value)

    @property
    def repetition_method(self) -> XAKeynoteApplication.RepetitionMethod:
        return XAKeynoteApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAKeynoteApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)




class XAKeynoteTextItemList(XAKeynoteiWorkItemList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteTextItem)
        logger.debug("Got list of text items")

    def background_fill_type(self) -> list[XAKeynoteApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAKeynoteApplication.FillOption(x) for x in ls]

    def text(self) -> XABase.XATextList:
        ls = self.xa_elem.arrayByApplyingSelector_("text")
        return self._new_element(ls, XABase.XATextList)

    def opacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("opacity"))

    def reflection_showing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionShowing"))

    def reflection_value(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("reflectionValue"))

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_background_fill_type(self, background_fill_type: XAKeynoteApplication.FillOption) -> 'XAKeynoteTextItem':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_text(self, text: Union[str, XABase.XAText]) -> 'XAKeynoteTextItem':
        if isinstance(text, str):
            self.by_property('text', text)
        else:
            self.by_property('text', text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XAKeynoteTextItem':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteTextItem':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteTextItem':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteTextItem':
        return self.by_property("rotation", rotation)

class XAKeynoteTextItem(XAKeynoteiWorkItem):
    """A class for managing and interacting with text items in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: XAKeynoteApplication.FillOption #: The background of the text item
        self.text: XABase.XAText #: The text contained within the text item
        self.opacity: int #: The opacity of the text item
        self.reflection_showing: bool #: Whether the text item displays a reflection
        self.reflection_value: int #: The percentage of reflection of the text item, from 0 to 100
        self.rotation: int #: The rotation of the text item, in degrees from 0 to 359

    @property
    def background_fill_type(self) -> XAKeynoteApplication.FillOption:
        return XAKeynoteApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def text(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.text(), XABase.XAText)

    @text.setter
    def text(self, text: Union[str, XABase.XAText]):
        if isinstance(text, str):
            self.set_property('text', text)
        else:
            self.set_property('text', text.xa_elem)

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




class XAKeynoteTableList(XAKeynoteiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteTable)

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

    def cell_range(self) -> 'XAKeynoteRangeList':
        """Gets the total cell range of each table in the list.

        :return: A list of table cell ranges
        :rtype: XAKeynoteRangeList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XAKeynoteRangeList)

    def selection_range(self) -> 'XAKeynoteRangeList':
        """Gets the selected cell range of each table in the list.

        :return: A list of selected table cell ranges
        :rtype: XAKeynoteRangeList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XAKeynoteRangeList)

    def by_name(self, name: str) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose name matches the given name, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose header row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose header column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose footer row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XAKeynoteRange') -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose cell range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XAKeynoteRange') -> Union['XAKeynoteTable', None]:
        """Retrieves the first table whose selection range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAKeynoteTable, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("selectionRange", selection_range.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAKeynoteTable(XAKeynoteiWorkItem):
    """A class for managing and interacting with tables in Keynote.

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
        self.cell_range: XAKeynoteRange #: The range of all cells in the table
        self.selection_range: XAKeynoteRange #: The currently selected cells
    
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
    def cell_range(self) -> 'XAKeynoteRange':
        return self._new_element(self.xa_elem.cellRange(), XAKeynoteRange)

    @property
    def selection_range(self) -> 'XAKeynoteRange':
        return self._new_element(self.xa_elem.selectionRange(), XAKeynoteRange)

    @selection_range.setter
    def selection_range(self, selection_range: 'XAKeynoteRange'):
        self.set_property('selectionRange', selection_range.xa_elem)

    def sort(self, by_column: 'XAKeynoteColumn', in_rows: Union[list['XAKeynoteRow'], 'XAKeynoteRowList', None] = None, direction: XAKeynoteApplication.SortDirection = XAKeynoteApplication.SortDirection.ASCENDING) -> Self:
        """Sorts the table according to the specified column, in the specified sorting direction.

        :param by_column: The column to sort by
        :type by_column: XAKeynoteColumn
        :param in_rows: The rows to sort, or None to sort the whole table, defaults to None
        :type in_rows: Union[list[XAKeynoteRow], XAKeynoteRowList, None], optional
        :param direction: The direction to sort in, defaults to XAKeynoteApplication.SortDirection.ASCENDING
        :type direction: XAKeynoteApplication.SortDirection, optional
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

    def cells(self, filter: Union[dict, None] = None) -> 'XAKeynoteCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAKeynoteCellList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAKeynoteCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAKeynoteColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAKeynoteColumnList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAKeynoteColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAKeynoteRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAKeynoteRowList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAKeynoteRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> 'XAKeynoteRangeList':
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: XAKeynoteRangeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.ranges(), XAKeynoteRangeList, filter)

    def __repr__(self):
        try:
            return "<" + str(type(self)) + str(self.name) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAKeynoteRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAKeynoteRange
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
                "format": XAKeynoteApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
                "vertical_alignment": XAKeynoteApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
                "font_name": raw_dict["fontName"],
                "alignment": XAKeynoteApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
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

    def format(self) -> list[XAKeynoteApplication.CellFormat]:
        """Gets the cell format of each range in the list.

        :return: A list of range cell formats
        :rtype: list[XAKeynoteApplication.CellFormat]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAKeynoteApplication.CellFormat(x) for x in ls]

    def alignment(self) -> list[XAKeynoteApplication.Alignment]:
        """Gets the alignment setting of each range in the list.

        :return: A list of range alignment settings
        :rtype: list[XAKeynoteApplication.Alignment]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XAKeynoteApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

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

    def vertical_alignment(self) -> list[XAKeynoteApplication.Alignment]:
        """Gets the vertical alignment setting of each range in the list.

        :return: A list of range vertical alignment settings
        :rtype: list[XAKeynoteApplication.Alignment]
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XAKeynoteApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
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
                return self._new_element(page_range, XAKeynoteRange)

    def by_font_name(self, font_name: str) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose font name matches the given font name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose font size matches the given font size, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XAKeynoteApplication.CellFormat) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose cell format matches the given format, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XAKeynoteApplication.Alignment) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        for page_range in self.xa_elem:
            if page_range.alignment() == alignment.value:
                return self._new_element(page_range, XAKeynoteRange)

    def by_name(self, name: str) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose name matches the given name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose text color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose text wrap setting matches the given boolean value, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose background color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XAKeynoteApplication.Alignment) -> Union['XAKeynoteRange', None]:
        """Retrieves the first range whose vertical alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAKeynoteRange, None]
        
        .. versionadded:: 0.0.5
        """
        for page_range in self.xa_elem:
            if page_range.verticalAlignment() == vertical_alignment.value:
                return self._new_element(page_range, XAKeynoteRange)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAKeynoteRange(XABase.XAObject):
    """A class for managing and interacting with ranges of table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the range
        self.font_name: str #: The font of the range's cells
        self.font_size: float #: The font size of the range's cells
        self.format: XAKeynoteApplication.CellFormat #: The format of the range's cells
        self.alignment: XAKeynoteApplication.Alignment #: The horizontall alignment of content within the range's cells
        self.name: str #: The range's coordinates
        self.text_color: XABase.XAColor #: The text color of the range's cells
        self.text_wrap: bool #: Whether text within the range's cell sshould wrap
        self.background_color: XABase.XAColor #: The background color of the range's cells
        self.vertical_alignment: XAKeynoteApplication.Alignment #: The vertical alignment of content in the range's cells

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        return {
            "background_color": XABase.XAColor(raw_dict["backgroundColor"]),
            "font_size": raw_dict["fontSize"],
            "name": raw_dict["name"],
            "format": XAKeynoteApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
            "vertical_alignment": XAKeynoteApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
            "font_name": raw_dict["fontName"],
            "alignment": XAKeynoteApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
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
    def format(self) -> XAKeynoteApplication.CellFormat:
        return XAKeynoteApplication.CellFormat(self.xa_elem.format())

    @format.setter
    def format(self, format: XAKeynoteApplication.CellFormat):
        self.set_property('format', format.value)

    @property
    def alignment(self) -> XAKeynoteApplication.Alignment:
        return XAKeynoteApplication.Alignment(self.xa_elem.alignment())

    @alignment.setter
    def alignment(self, alignment: XAKeynoteApplication.Alignment):
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
    def vertical_alignment(self) -> XAKeynoteApplication.Alignment:
        return XAKeynoteApplication.Alignment(self.xa_elem.verticalAlignment())

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment: XAKeynoteApplication.Alignment):
        self.set_property('verticalAlignment', vertical_alignment.value)

    def clear(self) -> Self:
        """Clears the content of every cell in the range.

        :return: The range object
        :rtype: Self

        :Example 1: Clear all cells in a table

        >>> import PyXA
        >>> app = PyXA.Application("Keynote")
        >>> range = app.documents()[0].slides()[0].tables()[0].cell_range
        >>> range.clear()

        :Example 2: Clear all cells whose value is 3

        >>> import PyXA
        >>> app = PyXA.Application("Keynote")
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
        >>> app = PyXA.Application("Keynote")
        >>> table = app.documents()[0].slides()[0].tables()[0]
        >>> row = table.rows()[0]
        >>> row.merge()

        :Example 2: Merge all cells in the first column of a table

        >>> import PyXA
        >>> app = PyXA.Application("Keynote")
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
        >>> app = PyXA.Application("Keynote")
        >>> range = app.documents()[0].slides()[0].tables()[0].cell_range
        >>> range.unmerge()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> 'XAKeynoteCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAKeynoteCellList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAKeynoteCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAKeynoteColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAKeynoteColumnList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAKeynoteColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAKeynoteRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAKeynoteRowList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAKeynoteRowList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAKeynoteRowList(XAKeynoteRangeList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteRow)
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

    def by_properties(self, properties: dict) -> Union['XAKeynoteRow', None]:
        """Retrieves the first row whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAKeynoteRow, None]
        
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
                return self._new_element(page_range, XAKeynoteRow)

    def by_address(self, address: float) -> Union['XAKeynoteRow', None]:
        """Retrieves the first row whose address matches the given address, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAKeynoteRow, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("address", address)

    def by_height(self, height: int) -> Union['XAKeynoteRow', None]:
        """Retrieves the first row whose height matches the given height, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAKeynoteRow, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("height", height)

class XAKeynoteRow(XAKeynoteRange):
    """A class for managing and interacting with table rows in Keynote.

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




class XAKeynoteColumnList(XAKeynoteRangeList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteColumn)
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

    def by_properties(self, properties: dict) -> Union['XAKeynoteColumn', None]:
        """Retrieves the first column whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAKeynoteColumn, None]
        
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
                return self._new_element(page_range, XAKeynoteColumn)

    def by_address(self, address: float) -> Union['XAKeynoteColumn', None]:
        """Retrieves the first column whose address matches the given address, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAKeynoteColumn, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("address", address)

    def by_width(self, width: int) -> Union['XAKeynoteColumn', None]:
        """Retrieves the first column whose width matches the given width, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAKeynoteColumn, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("width", width)

class XAKeynoteColumn(XAKeynoteRange):
    """A class for managing and interacting with table columns in Keynote.

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




class XAKeynoteCellList(XAKeynoteRangeList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteCell)
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
            properties["column"] = self._new_element(raw_dict["column"], XAKeynoteColumn)
            properties["row"] = self._new_element(raw_dict["row"], XAKeynoteRow)
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

    def column(self) -> XAKeynoteColumnList:
        """Gets the column of each cell in the list.

        :return: A list of cell columns
        :rtype: XAKeynoteColumnList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XAKeynoteColumnList)

    def row(self) -> XAKeynoteRowList:
        """Gets the row of each cell in the list.

        :return: A list of cell rows
        :rtype: XAKeynoteRowList
        
        .. versionadded:: 0.0.5
        """
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XAKeynoteRowList)

    def by_properties(self, properties: dict) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
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
                return self._new_element(page_range, XAKeynoteCell)

    def by_formatted_value(self, formatted_value: str) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose formatted value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose formula matches the given formula, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("value", value)

    def by_column(self, column: XAKeynoteColumn) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose column matches the given column, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XAKeynoteRow) -> Union['XAKeynoteCell', None]:
        """Retrieves the first cell whose row matches the given row, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAKeynoteCell, None]
        
        .. versionadded:: 0.0.5
        """
        return self.by_property("row", row.xa_elem)

class XAKeynoteCell(XAKeynoteRange):
    """A class for managing and interacting with table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.formatted_value: str #: The formatted form of the value stored in the cell
        self.formula: str #: The formula in the cell as text
        self.value: Any #: The value stored in the cell
        self.column: XAKeynoteColumn #: The cell's column
        self.row: XAKeynoteRow #: The cell's row

    @property
    def properties(self) -> dict:
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["formatted_value"] = raw_dict["formattedValue"]
        properties["formula"] = raw_dict["formula"]
        properties["value"] = raw_dict["value"]
        properties["column"] = self._new_element(raw_dict["column"], XAKeynoteColumn)
        properties["row"] = self._new_element(raw_dict["row"], XAKeynoteRow)
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
    def column(self) -> XAKeynoteColumn:
        return self._new_element(self.xa_elem.column(), XAKeynoteColumn)

    @property
    def row(self) -> XAKeynoteRow:
        return self._new_element(self.xa_elem.row(), XAKeynoteRow)




class XAKeynoteTransitionSettings(XABase.XAObject):
    """Properties common to all transtions.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, parent: XABase.XAObject = None):
        self.__automatic_transition: bool = properties["automatic_transition"]
        self.__transition_delay: float = properties["transition_delay"]
        self.__transition_duration: float = properties["transition_duration"]
        self.__transition_effect: XAKeynoteApplication.Transition = properties["transition_effect"]
        self.__parent = parent

    @property
    def _pyxa_dict(self):
        return {
            "automatic_transition": self.__automatic_transition,
            "transition_telay": self.__transition_delay,
            "transition_duration": self.__transition_duration,
            "transition_effect": self.__transition_effect
        }

    @property
    def automatic_transition(self) -> bool:
        return self.__automatic_transition

    @automatic_transition.setter
    def automatic_transition(self, automatic_transition: bool):
        self.__automatic_transition = automatic_transition
        if self.__parent is not None:
            self.__parent.transition_properties = self._pyxa_dict

    @property
    def transition_delay(self) -> float:
        return self.__transition_delay

    @transition_delay.setter
    def automatic_transition(self, transition_delay: float):
        self.__transition_delay = transition_delay
        if self.__parent is not None:
            self.__parent.transition_properties = self._pyxa_dict

    @property
    def transition_duration(self) -> float:
        return self.__transition_duration

    @transition_duration.setter
    def automatic_transition(self, transition_duration: float):
        self.__transition_duration = transition_duration
        if self.__parent is not None:
            self.__parent.transition_properties = self._pyxa_dict

    @property
    def transition_effect(self) -> XAKeynoteApplication.Transition:
        return self.__transition_effect

    @transition_effect.setter
    def transition_effect(self, transition_effect: XAKeynoteApplication.Transition):
        self.__transition_effect = transition_effect
        if self.__parent is not None:
            self.__parent.transition_properties = self._pyxa_dict

    def __repr__(self):
        return "<" + str(type(self)) + str(self._pyxa_dict) + ">"