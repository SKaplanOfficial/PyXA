""".. versionadded:: 0.0.2

Control the macOS Keynote application using JXA-like syntax.
"""
from enum import Enum
from time import sleep
from typing import Any, List, Tuple, Union
from AppKit import NSURL, NSPoint, NSValue

from PyXA import XABase, XAEvents
import ApplicationServices

from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XAKeynoteApplication(XABaseScriptable.XASBApplication, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement, XABase.XACanOpenPath):
    """A class for managing and interacting with Keynote.app.

    .. seealso:: :class:`XAKeynoteWindow`, :class:`XAKeynoteDocument`

    .. versionadded:: 0.0.2
    """
    class SaveOption(Enum):
        """Options for what to do when calling a save event.
        """
        SAVE_FILE   = OSType('yes ') #: Save the file. 
        DONT_SAVE   = OSType('no  ') #: Do not save the file. 
        ASK         = OSType('ask ') #: Ask the user whether or not to save the file. 

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
        NONE  = OSType('tnil') 
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
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, {"copies": 2}, True)
        return self

    def documents(self, filter: Union[dict, None] = None) -> 'XAKeynoteDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: List[XAKeynoteDocument]

        :Example 1: List the name of every open Keynote document

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
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
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        properties = {
            "file": file_path,
        }
        if theme is not None:
            properties["documentTheme"] = theme.xa_elem
        return self.push("document", properties, self.xa_scel.documents())

    def new_slide(self, document: 'XAKeynoteDocument', properties: dict):
        return self.push("slide", properties, document.xa_elem.slides())

    def themes(self, filter: Union[dict, None] = None) -> List['XAKeynoteTheme']:
        """Returns a list of themes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned themes will have, or None
        :type filter: Union[dict, None]
        :return: The list of themes
        :rtype: List[XAKeynoteTheme]

        :Example 1: List the name of each theme

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
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
        # elif specifier == "column":
        #     return self._new_element(obj, XAKeynoteColumn)
        # elif specifier == "row":
        #     return self._new_element(obj, XAKeynoteRow)
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




class XAKeynoteWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Keynote.app.

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
        self.document: XAKeynoteDocument #: The document currently displayed in the window

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def id(self) -> int:
        return self.xa_scel.id()

    @property
    def index(self) -> int:
        return self.xa_scel.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_scel.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_scel.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_scel.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_scel.miniaturized()

    @property
    def resizable(self) -> bool:
        return self.xa_scel.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_scel.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_scel.zoomed()

    @property
    def document(self) -> 'XAKeynoteDocument':
        return self._new_element(self.xa_scel.document(), XAKeynoteDocument)




class XAKeynoteDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteDocument, filter)

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

    def slide_numbers_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("slideNumbersShowing"))

    def document_theme(self) -> 'XAKeynoteThemeList':
        ls = self.xa_elem.arrayByApplyingSelector_("documentTheme")
        return self._new_element(ls, XAKeynoteThemeList)

    def auto_loop(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoLoop"))

    def auto_play(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoPlay"))

    def auto_restart(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("autoRestart"))

    def maximum_idle_duration(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximumIdleDuration"))

    def current_slide(self) -> 'XAKeynoteSlideList':
        ls = self.xa_elem.arrayByApplyingSelector_("currentSlide")
        return self._new_element(ls, XAKeynoteSlideList)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def selection(self) -> 'XAKeynoteiWorkItemList':
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAKeynoteiWorkItemList)

    def password_protected(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> 'XAKeynoteDocument':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAKeynoteDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XAKeynoteDocument':
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> 'XAKeynoteDocument':
        return self.by_property("file", file)

    def by_id(self, id: str) -> 'XAKeynoteDocument':
        return self.by_property("id", id)

    def by_slide_numbers_showing(self, slide_numbers_showing: bool) -> 'XAKeynoteDocument':
        return self.by_property("slideNumbersShowing", slide_numbers_showing)

    def by_document_theme(self, document_theme: 'XAKeynoteTheme') -> 'XAKeynoteDocument':
        return self.by_property("documentTheme", document_theme.xa_elem)

    def by_auto_loop(self, auto_loop: bool) -> 'XAKeynoteDocument':
        return self.by_property("autoLoop", auto_loop)

    def by_auto_play(self, auto_play: bool) -> 'XAKeynoteDocument':
        return self.by_property("autoPlay", auto_play)

    def by_auto_restart(self, auto_restart: bool) -> 'XAKeynoteDocument':
        return self.by_property("autoRestart", auto_restart)

    def by_maximum_idle_duration(self, maximum_idle_duration: int) -> 'XAKeynoteDocument':
        return self.by_property("maxmimumIdleDuration", maximum_idle_duration)

    def by_current_slide(self, current_slide: 'XAKeynoteSlide') -> 'XAKeynoteDocument':
        return self.by_property("currentSlide", current_slide.xa_elem)

    def by_height(self, height: int) -> 'XAKeynoteDocument':
        return self.by_property("height", height)

    def by_width(self, width: int) -> 'XAKeynoteDocument':
        return self.by_property("width", width)

    def by_selection(self, selection: 'XAKeynoteiWorkItemList') -> 'XAKeynoteDocument':
        return self.by_property("selection", selection.xa_elem)

    def by_password_protected(self, password_protected: bool) -> 'XAKeynoteDocument':
        return self.by_property("passwordProtected", password_protected)

class XAKeynoteDocument(XABase.XAHasElements, XABaseScriptable.XASBPrintable, XABaseScriptable.XASBCloseable, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.name: str #: The name of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.file: str #: The location of the document on the disk, if one exists
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
    def slide_numbers_showing(self) -> bool:
        return self.xa_elem.slideNumbersShowing()

    @property
    def document_theme(self) -> 'XAKeynoteTheme':
        return self._new_element(self.xa_elem.documentTheme(), XAKeynoteTheme)

    @property
    def auto_loop(self) -> bool:
        return self.xa_elem.autoLoop()

    @property
    def auto_play(self) -> bool:
        return self.xa_elem.autoPlay()

    @property
    def auto_restart(self) -> bool:
        return self.xa_elem.autoRestart()

    @property
    def maximum_idle_duration(self) -> int:
        return self.xa_elem.maximumIdleDuration()

    @property
    def current_slide(self) -> 'XAKeynoteSlide':
        return self._new_element(self.xa_elem.currentSlide(), XAKeynoteSlide)

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @property
    def selection(self) -> 'XAKeynoteiWorkItemList':
        return self._new_element(self.xa_elem.selection(), XAKeynoteiWorkItemList)

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

    def export(self, file_path: Union[str, NSURL] = None, format: XAKeynoteApplication.ExportFormat = XAKeynoteApplication.ExportFormat.PDF):
        """Exports the slideshow in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, NSURL], optional
        :param format: The format to export the file in, defaults to XAKeynoteApplication.ExportFormat.PDF
        :type format: XAKeynoteApplication.ExportFormat, optional

        .. versionadded:: 0.0.3
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = NSURL.alloc().initFileURLWithPath_(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path, format.value, None)

    def make_image_slides(self, files: List[Union[str, NSURL]], set_titles: bool = False, slide_layout: 'XAKeynoteSlideLayout' = None) -> 'XAKeynoteDocument':
        """Creates slides out of image files.

        Creates a new slide for each image file path in the files list, if the image can be found.

        :param files: A list of paths to image files
        :type files: List[Union[str, NSURL]]
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
                file = NSURL.alloc().initFileURLWithPath_(file)
            urls.append(file)
        self.xa_elem.makeImageSlidesFiles_setTitles_slideLayout_(urls, set_titles, slide_layout)
        return self

    def slides(self, filter: Union[dict, None] = None) -> List['XAKeynoteSlide']:
        """Returns a list of slides, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned slides will have, or None
        :type filter: Union[dict, None]
        :return: The list of slides
        :rtype: List[XAKeynoteSlide]

        :Example 1: List all slides

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.panes())

        :Example 2: List slides after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.panes({"name": "Accessibility"}))

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

    # Slide Layouts
    def slide_layouts(self, filter: Union[dict, None] = None) -> List['XAKeynoteSlideLayout']:
        """Returns a list of slide_layouts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned slide_layouts will have, or None
        :type filter: Union[dict, None]
        :return: The list of slide_layouts
        :rtype: List[XAKeynoteSlideLayout]

        :Example 1: List all slide_layouts

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.panes())

        :Example 2: List slide_layouts after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.slideLayouts(), XAKeynoteSlideLayoutList, filter)




class XAKeynoteThemeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteTheme, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XAKeynoteTheme':
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAKeynoteTheme':
        return self.by_property("name", name)

class XAKeynoteTheme(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Keynote themes.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier for the theme
        self.name: str #: The name of the theme

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
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteContainer, filter)

class XAKeynoteContainer(XABase.XAHasElements):
    """A class for managing and interacting with containers in Keynote.

    .. seealso:: :class:`XAKeynoteApplication`, :class:`XAKeynoteiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def iwork_items(self, filter: Union[dict, None] = None) -> List['XAKeynoteiWorkItem']:
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: List[XAKeynoteiWorkItem]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAKeynoteiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> List['XAKeynoteAudioClip']:
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: List[XAKeynoteAudioClip]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), XAKeynoteAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> List['XAKeynoteChart']:
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: List[XAKeynoteChart]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), XAKeynoteChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> List['XAKeynoteImage']:
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: List[XAKeynoteImage]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), XAKeynoteImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> List['XAKeynoteGroup']:
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: List[XAKeynoteGroup]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), XAKeynoteGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> List['XAKeynoteLine']:
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: List[XAKeynoteLine]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), XAKeynoteLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> List['XAKeynoteMovie']:
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: List[XAKeynoteMovie]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), XAKeynoteMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> List['XAKeynoteShape']:
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: List[XAKeynoteShape]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), XAKeynoteShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> List['XAKeynoteTable']:
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: List[XAKeynoteTable]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), XAKeynoteTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> List['XAKeynoteTextItem']:
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: List[XAKeynoteTextItem]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), XAKeynoteTextItemList, filter)




class XAKeynoteSlideList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteSlide, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def body_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("bodyShowing"))

    def skipped(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("skipped"))

    def slide_number(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("slideNumber"))

    def title_showing(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("titleShowing"))

    def transition_properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("transitionProperties"))

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
        ls = self.xa_elem.arrayByApplyingSelector_("bodyShowing")
        return self._new_element(ls, XABase.XATextList)

    def by_properties(self, properties: dict) -> 'XAKeynoteSlide':
        return self.by_property("properties", properties)

    def by_body_showing(self, body_showing: bool) -> 'XAKeynoteSlide':
        return self.by_property("bodyShowing", body_showing)

    def by_skipped(self, skipped: bool) -> 'XAKeynoteSlide':
        return self.by_property("skipped", skipped)

    def by_slide_number(self, slide_number: int) -> 'XAKeynoteSlide':
        return self.by_property("slideNumber", slide_number)

    def by_title_showing(self, title_showing: bool) -> 'XAKeynoteSlide':
        return self.by_property("titleShowing", title_showing)

    def by_transition_properties(self, transition_properties: dict) -> 'XAKeynoteSlide':
        return self.by_property("transitionProperties", transition_properties)

    def by_base_layout(self, base_layout: 'XAKeynoteSlideLayout') -> 'XAKeynoteSlide':
        return self.by_property("baseLayout", base_layout.xa_elem)

    def by_default_body_item(self, default_body_item: 'XAKeynoteShape') -> 'XAKeynoteSlide':
        return self.by_property("defaultBodyItem", default_body_item)

    def by_default_text_item(self, default_text_item: 'XAKeynoteShape') -> 'XAKeynoteSlide':
        return self.by_property("defaultTextItem", default_text_item.xa_elem)

    def by_presenter_notes(self, presenter_notes: XABase.XAText) -> 'XAKeynoteSlide':
        return self.by_property("presenterNotes", presenter_notes.xa_elem)

class XAKeynoteSlide(XAKeynoteContainer):
    """A class for managing and interacting with TextEdit documents.

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
        return self.xa_elem.properties()

    @property
    def body_showing(self) -> bool:
        return self.xa_elem.bodyShowing()

    @property
    def skipped(self) -> bool:
        return self.xa_elem.shipped()

    @property
    def slide_number(self) -> int:
        return self.xa_elem.slideNumber()

    @property
    def title_showing(self) -> bool:
        return self.xa_elem.titleShowing()

    @property
    def transition_properties(self) -> dict:
        return self.xa_elem.transitionProperties()

    @property
    def base_layout(self) -> 'XAKeynoteSlideLayout':
        return self._new_element(self.xa_elem.baseLayout(), XAKeynoteSlideLayout)

    @property
    def default_body_item(self) -> 'XAKeynoteShape':
        return self._new_element(self.xa_elem.defaultBodyItem(), XAKeynoteShape)

    @property
    def default_title_item(self) -> 'XAKeynoteShape':
        return self._new_element(self.xa_elem.defaultTitleItem(), XAKeynoteShape)

    @property
    def presenter_notes(self) -> XABase.XAText:
        return self._new_element(self.xa_elem.presenterNotes(), XABase.XAText)

    def duplicate(self) -> 'XAKeynoteSlide':
        """Duplicates the slide, mimicking the action of copying and pasting the slide manually.

        :return: A reference to the PyXA slide object that called this command.
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        self.xa_elem.duplicateTo_withProperties_(self.xa_elem.positionAfter(), None)
        return self

    def delete(self):
        """Deletes the slide.

        .. versionadded:: 0.0.2
        """
        self.xa_elem.delete()

    def add_image(self, file_path: Union[str, NSURL]) -> 'XAKeynoteImage':
        """Adds the image at the specified path to the slide.

        :param file_path: The path to the image file.
        :type file_path: Union[str, NSURL]
        :return: The newly created image object.
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        url = file_path
        if isinstance(url, str):
            url = NSURL.alloc().initFileURLWithPath_(file_path)
        image = self.xa_prnt.xa_prnt.construct("image", {
            "file": url,
        })
        self.xa_elem.images().addObject_(image)
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": image,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XAKeynoteImage(properties)

    def add_chart(self, row_names: List[str], column_names: List[str], data: List[List[Any]], type: int = XAKeynoteApplication.ChartType.LINE_2D.value, group_by: int = XAKeynoteApplication.ChartGrouping.ROW.value) -> 'XAKeynoteChart':
        """_summary_

        _extended_summary_

        :param row_names: A list of row names.
        :type row_names: List[str]
        :param column_names: A list of column names.
        :type column_names: List[str]
        :param data: A 2d array 
        :type data: List[List[Any]]
        :param type: The chart type, defaults to _KeynoteLegacyChartType.KeynoteLegacyChartTypeLine_2d.value
        :type type: int, optional
        :param group_by: The grouping schema, defaults to _KeynoteLegacyChartGrouping.KeynoteLegacyChartGroupingChartRow.value
        :type group_by: int, optional
        :return: A reference to the newly created chart object.
        :rtype: XAKeynoteChart

        .. versionadded:: 0.0.2
        """
        self.xa_prnt.set_property("currentSlide", self.xa_elem)
        self.xa_elem.addChartRowNames_columnNames_data_type_groupBy_(row_names, column_names, data, type, group_by)
        chart = self.xa_elem.charts()[-1].get()
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": chart,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XAKeynoteChart(properties)




class XAKeynoteSlideLayoutList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteTheme, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_name(self, name: str) -> 'XAKeynoteTheme':
        return self.by_property("name", name)

class XAKeynoteSlideLayout(XAKeynoteSlide):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteSlide`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name #: The name of the slide layout

    @property
    def name(self) -> str:
        return self.xa_elem.name()




class XAKeynoteiWorkItemList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteiWorkItem, filter)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def locked(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def parent(self) -> XAKeynoteContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAKeynoteContainerList)

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def by_height(self, height: int) -> 'XAKeynoteiWorkItem':
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> 'XAKeynoteiWorkItem':
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> 'XAKeynoteiWorkItem':
        return self.by_property("width", width)

    def by_parent(self, parent: XAKeynoteContainer) -> 'XAKeynoteiWorkItem':
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: Tuple[int, int]) -> 'XAKeynoteiWorkItem':
        return self.by_property("position", position)

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
        self.position: Tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the iWork item

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
    def parent(self) -> XAKeynoteContainer:
        return self._new_element(self.xa_elem.parent(), XAKeynoteContainer)

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

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
        self.xa_elem.duplicateTo_withProperties_(self.xa_prnt.xa_elem.iWorkItems(), None)
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
        position = NSValue.valueWithPoint_(NSPoint(x, y))
        self.xa_elem.setValue_forKey_(position, "position")





class XAKeynoteGroupList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteGroup, filter)

    def height(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def rotation(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def parent(self) -> XAKeynoteContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAKeynoteContainerList)

    def by_height(self, height: int) -> 'XAKeynoteGroup':
        return self.by_property("height", height)

    def by_position(self, position: Tuple[int, int]) -> 'XAKeynoteGroup':
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
        self.position: Tuple[int, int] #: The horizontal and vertical coordinates of the top left point of the group
        self.width: int #: The widht of the group
        self.rotation: int #: The rotation of the group, in degrees from 0 to 359
        self.parent: XAKeynoteContainer #: The container which contains the group

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
    def parent(self) -> XAKeynoteContainer:
        return self._new_element(self.xa_elem.parent(), XAKeynoteContainer)




class XAKeynoteImageList(XABase.XAList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteImage, filter)

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

    def by_object_description(self, object_description: str) -> 'XAKeynoteImage':
        return self.by_property("objectDescription", object_description)

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

class XAKeynoteImage(XAKeynoteiWorkItem):
    """A class for managing and interacting with images in Keynote.

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
        return self.xa_elem.fileName()

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

    def rotate(self, degrees: int) -> 'XAKeynoteImage':
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, NSURL]) -> 'XAKeynoteImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, NSURL]
        :return: A reference to the new PyXA image object.
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        self.delete()
        return self.xa_prnt.add_image(img_path)




class XAKeynoteAudioClipList(XABase.XAList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteAudioClip, filter)

    def file_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> List[XAKeynoteApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAKeynoteApplication.RepetitionMethod(x) for x in ls]

    def by_file_name(self, file_name: str) -> 'XAKeynoteAudioClip':
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> 'XAKeynoteAudioClip':
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XAKeynoteApplication.RepetitionMethod) -> 'XAKeynoteAudioClip':
        return self.by_property("repetitionMethod", repetition_method.value)

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
        return self.xa_elem.fileName()

    @property
    def clip_volume(self) -> int:
        return self.xa_elem.clipVolume()

    @property
    def repetition_method(self) -> XAKeynoteApplication.RepetitionMethod:
        return XAKeynoteApplication.RepetitionMethod(self.xa_elem.repetitionMethod())




class XAKeynoteShapeList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteShape, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def background_fill_type(self) -> List[XAKeynoteApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAKeynoteApplication.FillOption(x) for x in ls]

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

    def by_properties(self, properties: dict) -> 'XAKeynoteShape':
        return self.by_property("properties", properties)

    def by_background_fill_type(self, background_fill_type: XAKeynoteApplication.FillOption) -> 'XAKeynoteShape':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_object_text(self, object_text: XABase.XAText) -> 'XAKeynoteShape':
        return self.by_property("objectText", object_text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XAKeynoteShape':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteShape':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteShape':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteShape':
        return self.by_property("rotation", rotation)

class XAKeynoteShape(XAKeynoteiWorkItem):
    """A class for managing and interacting with shapes in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the shape
        self.background_fill_type: XAKeynoteApplication.FillOption #: The background, if any, for the shape
        self.object_text: str #: The text contained within the shape
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

    def rotate(self, degrees: int) -> 'XAKeynoteShape':
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: XAKeynoteShape

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




class XAKeynoteChartList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteChart, filter)

class XAKeynoteChart(XAKeynoteiWorkItem):
    """A class for managing and interacting with charts in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAKeynoteLineList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteLine, filter)

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

    def by_end_point(self, end_point: Tuple[int, int]) -> 'XAKeynoteLine':
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAKeynoteLine':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAKeynoteLine':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAKeynoteLine':
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: Tuple[int, int]) -> 'XAKeynoteLine':
        return self.by_property("startPoint", start_point)

class XAKeynoteLine(XAKeynoteiWorkItem):
    """A class for managing and interacting with lines in Keynote.

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




class XAKeynoteMovieList(XABase.XAList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteMovie, filter)

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

    def reflection_value(self) -> List[XAKeynoteApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAKeynoteApplication.RepetitionMethod(x) for x in ls]

    def rotation(self) -> List[int]:
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
    def repetition_method(self) -> XAKeynoteApplication.RepetitionMethod:
        return XAKeynoteApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @property
    def rotation(self) -> int:
        return self.xa_elem.rotation()




class XAKeynoteTextItemList(XABase.XAList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteTextItem, filter)

    def background_fill_type(self) -> List[XAKeynoteApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAKeynoteApplication.FillOption(x) for x in ls]

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

    def by_background_fill_type(self, background_fill_type: XAKeynoteApplication.FillOption) -> 'XAKeynoteTextItem':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_text(self, text: XABase.XAText) -> 'XAKeynoteTextItem':
        return self.by_property("text", text.xa_elem)

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




class XAKeynoteTableList(XABase.XAList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteTable, filter)

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

    def cell_range(self) -> 'XAKeynoteRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XAKeynoteRangeList)

    def selection_range(self) -> 'XAKeynoteRangeList':
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XAKeynoteRangeList)

    def by_name(self, name: str) -> 'XAKeynoteTable':
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> 'XAKeynoteTable':
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> 'XAKeynoteTable':
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> 'XAKeynoteTable':
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> 'XAKeynoteTable':
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> 'XAKeynoteTable':
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XAKeynoteRange') -> 'XAKeynoteTable':
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XAKeynoteRange') -> 'XAKeynoteTable':
        return self.by_property("selectionRange", selection_range.xa_elem)

class XAKeynoteTable(XAKeynoteiWorkItem, XABase.XAHasElements):
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
    def cell_range(self) -> 'XAKeynoteRange':
        return self._new_element(self.xa_elem.cellRange(), XAKeynoteRange)

    @property
    def selection_range(self) -> 'XAKeynoteRange':
        return self._new_element(self.xa_elem.selectionRange(), XAKeynoteRange)

    # TODO
    def sort(self, columns: List['XAKeynoteColumn'], rows: List['XAKeynoteRow'], direction: XAKeynoteApplication.SortDirection = XAKeynoteApplication.SortDirection.ASCENDING) -> 'XAKeynoteTable':
        column_objs = [column.xa_elem for column in columns]
        row_objs = [row.xa_elem for row in rows]
        self.xa_elem.sortBy_direction_inRows_(column_objs[0], direction.value, row_objs)
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XAKeynoteCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAKeynoteCell]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAKeynoteCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XAKeynoteColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAKeynoteColumn]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAKeynoteColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XAKeynoteRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAKeynoteRow]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAKeynoteRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> List['XAKeynoteRange']:
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: List[XAKeynoteRange]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.ranges(), XAKeynoteRangeList, filter)




class XAKeynoteRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteRange, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def font_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def format(self) -> List[XAKeynoteApplication.CellFormat]:
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAKeynoteApplication.CellFormat(x) for x in ls]

    def alignment(self) -> List[XAKeynoteApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XAKeynoteApplication.Alignment(x) for x in ls]

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

    def vertical_alignment(self) -> List[XAKeynoteApplication.Alignment]:
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XAKeynoteApplication.Alignment(x) for x in ls]

    def by_properties(self, properties: dict) -> 'XAKeynoteRange':
        return self.by_property("properties", properties)

    def by_font_name(self, font_name: str) -> 'XAKeynoteRange':
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> 'XAKeynoteRange':
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XAKeynoteApplication.CellFormat) -> 'XAKeynoteRange':
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XAKeynoteApplication.Alignment) -> 'XAKeynoteRange':
        return self.by_property("alignment", alignment.value)

    def by_name(self, name: str) -> 'XAKeynoteRange':
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> 'XAKeynoteRange':
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> 'XAKeynoteRange':
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> 'XAKeynoteRange':
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XAKeynoteApplication.Alignment) -> 'XAKeynoteRange':
        return self.by_property("verticalAlignment", vertical_alignment.value)

class XAKeynoteRange(XABase.XAHasElements):
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
        return self.xa_elem.dict()

    @property
    def font_name(self) -> str:
        return self.xa_elem.fontName()

    @property
    def font_size(self) -> int:
        return self.xa_elem.fontSize()

    @property
    def format(self) -> XAKeynoteApplication.CellFormat:
        return XAKeynoteApplication.CellFormat(self.xa_elem.format())

    @property
    def alignment(self) -> XAKeynoteApplication.Alignment:
        return XAKeynoteApplication.Alignment(self.xa_elem.alighment())

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
    def vertical_alignment(self) -> XAKeynoteApplication.Alignment:
        return XAKeynoteApplication.Alignment(self.xa_elem.verticalAlignment())

    def clear(self) -> 'XAKeynoteRange':
        """Clears the content of every cell in the range.

        :Example 1: Clear all cells in a table

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.clear()

        :Example 2: Clear all cells whose value is 3

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> cells = app.document(0).slide(0).table(0).cells()
        >>> for cell in cells:
        >>>     if cell.value == 3:
        >>>         cell.clear()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.clear()
        return self

    def merge(self) -> 'XAKeynoteRange':
        """Merges all cells in the range.

        :Example 1: Merge all cells in the first row of a table

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> table = app.document(0).slide(0).table(0)
        >>> row = table.row(0)
        >>> row.merge()

        :Example 2: Merge all cells in the first column of a table

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> table = app.document(0).slide(0).table(0)
        >>> col = table.column(0)
        >>> col.merge()

        .. note::

           If you merge an entire row, then merge an entire column, all cells in the table will be merged. The same is true if the row and column operations are flipped.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.merge()
        return self

    def unmerge(self) -> 'XAKeynoteRange':
        """Unmerges all cells in the range.

        :Example 1: Unmerge all merged cells

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> range = app.document(0).slide(0).table(0).cell_range
        >>> range.unmerge()

        .. versionadded:: 0.0.3
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> List['XAKeynoteCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAKeynoteCell]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.cells(), XAKeynoteCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> List['XAKeynoteColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAKeynoteColumn]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.columns(), XAKeynoteColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> List['XAKeynoteRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAKeynoteRow]

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.rows(), XAKeynoteRowList, filter)




class XAKeynoteRowList(XABase.XAList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteRow, filter)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_address(self, address: float) -> 'XAKeynoteRow':
        return self.by_property("address", address)

    def by_width(self, width: int) -> 'XAKeynoteRow':
        return self.by_property("width", width)

class XAKeynoteRow(XAKeynoteRange):
    """A class for managing and interacting with table rows in Keynote.

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




class XAKeynoteColumnList(XABase.XAList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteColumn, filter)

    def address(self) -> List[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_address(self, address: float) -> 'XAKeynoteColumn':
        return self.by_property("address", address)

    def by_width(self, width: int) -> 'XAKeynoteColumn':
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
    def address(self) -> int:
        return self.xa_elem.address()

    @property
    def width(self) -> float:
        return self.xa_elem.width()




class XAKeynoteCellList(XABase.XAList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAKeynoteCell, filter)

    def formatted_value(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formattedValue"))

    def formula(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formula"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def column(self) -> XAKeynoteColumnList:
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XAKeynoteColumnList)

    def row(self) -> XAKeynoteRowList:
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XAKeynoteRowList)

    def by_formatted_value(self, formatted_value: str) -> 'XAKeynoteCell':
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> 'XAKeynoteCell':
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> 'XAKeynoteCell':
        return self.by_property("value", value)

    def by_column(self, column: XAKeynoteColumn) -> 'XAKeynoteCell':
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XAKeynoteRow) -> 'XAKeynoteCell':
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
    def formatted_value(self) -> str:
        return self.xa_elem.formattedValue()

    @property
    def formula(self) -> str:
        return self.xa_elem.formula()

    @property
    def value(self) -> str:
        return self.xa_elem.value().get()

    @property
    def column(self) -> XAKeynoteColumn:
        return self._new_element(self.xa_elem.column(), XAKeynoteColumn)

    @property
    def row(self) -> XAKeynoteRow:
        return self._new_element(self.xa_elem.row(), XAKeynoteRow)