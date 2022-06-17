""".. versionadded:: 0.0.2

Control the macOS Keynote application using JXA-like syntax.
"""
from cgitb import text
from enum import Enum
from time import sleep
from typing import Any, List, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray, NSData, NSMutableString, NSASCIIStringEncoding, NSPasteboard
import AppleScriptObjC

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
import ctypes

from PyXA import XAEvents

class _KeynoteSaveOptions(Enum):
	KeynoteSaveOptionsYes   = OSType('yes ') # Save the file. 
	KeynoteSaveOptionsNo    = OSType('no  ') # Do not save the file. 
	KeynoteSaveOptionsAsk   = OSType('ask ') # Ask the user whether or not to save the file. 

class _KeynotePrintingErrorHandling(Enum):
	KeynotePrintingErrorHandlingStandard = OSType('lwst') # Standard PostScript error handling 
	KeynotePrintingErrorHandlingDetailed = OSType('lwdt') # print a detailed report of PostScript errors 

class _KeynoteSaveableFileFormat(Enum):
	KeynoteSaveableFileFormatKeynote = OSType('Knff') # The Keynote native file format 

class _KeynoteExportFormat(Enum):
	KeynoteExportFormatHTML                 = OSType('Khtm') # HTML 
	KeynoteExportFormatQuickTimeMovie       = OSType('Kmov') # QuickTime movie 
	KeynoteExportFormatPDF                  = OSType('Kpdf') # PDF 
	KeynoteExportFormatSlideImages          = OSType('Kimg') # image 
	KeynoteExportFormatMicrosoftPowerPoint  = OSType('Kppt') # Microsoft PowerPoint 
	KeynoteExportFormatKeynote09            = OSType('Kkey') # Keynote 09 

class _KeynoteImageExportFormats(Enum):
	KeynoteImageExportFormatsJPEG   = OSType('Kifj') # JPEG 
	KeynoteImageExportFormatsPNG    = OSType('Kifp') # PNG 
	KeynoteImageExportFormatsTIFF   = OSType('Kift') # TIFF 

class _KeynoteMovieExportFormats(Enum):
	KeynoteMovieExportFormatsFormat360p     = OSType('Kmf3') # 360p 
	KeynoteMovieExportFormatsFormat540p     = OSType('Kmf5') # 540p 
	KeynoteMovieExportFormatsFormat720p     = OSType('Kmf7') # 720p 
	KeynoteMovieExportFormatsFormat1080p    = OSType('Kmf8') # 1080p 
	KeynoteMovieExportFormatsFormat2160p    = OSType('Kmf4') # DCI 4K (4096x2160) 
	KeynoteMovieExportFormatsNativeSize     = OSType('KmfN') # Exported movie will have the same dimensions as the document, up to 4096x2160 

class _KeynoteMovieCodecs(Enum):
	KeynoteMovieCodecsH264                  = OSType('Kmc1') # H.264 
	KeynoteMovieCodecsAppleProRes422        = OSType('Kmc2') # Apple ProRes 422 
	KeynoteMovieCodecsAppleProRes4444       = OSType('Kmc3') # Apple ProRes 4444 
	KeynoteMovieCodecsAppleProRes422LT      = OSType('Kmc4') # Apple ProRes 422LT 
	KeynoteMovieCodecsAppleProRes422HQ      = OSType('Kmc5') # Apple ProRes 422HQ 
	KeynoteMovieCodecsAppleProRes422Proxy   = OSType('Kmc6') # Apple ProRes 422Proxy 
	KeynoteMovieCodecsHEVC                  = OSType('Kmc7') # HEVC 

class _KeynoteMovieFramerates(Enum):
	KeynoteMovieFrameratesFPS12     = OSType('Kfr1') # 12 FPS 
	KeynoteMovieFrameratesFPS2398   = OSType('Kfr2') # 23.98 FPS 
	KeynoteMovieFrameratesFPS24     = OSType('Kfr3') # 24 FPS 
	KeynoteMovieFrameratesFPS25     = OSType('Kfr4') # 25 FPS 
	KeynoteMovieFrameratesFPS2997   = OSType('Kfr5') # 29.97 FPS 
	KeynoteMovieFrameratesFPS30     = OSType('Kfr6') # 30 FPS 
	KeynoteMovieFrameratesFPS50     = OSType('Kfr7') # 50 FPS 
	KeynoteMovieFrameratesFPS5994   = OSType('Kfr8') # 59.94 FPS 
	KeynoteMovieFrameratesFPS60     = OSType('Kfr9') # 60 FPS 

class _KeynotePrintWhat(Enum):
	KeynotePrintWhatIndividualSlides    = OSType('Kpwi') # individual slides 
	KeynotePrintWhatSlideWithNotes      = OSType('Kpwn') # slides with notes 
	KeynotePrintWhatHandouts            = OSType('Kpwh') # handouts 

class _KeynotePDFImageQuality(Enum):
	KeynotePDFImageQualityGood      = OSType('KnP0') # good quality 
	KeynotePDFImageQualityBetter    = OSType('KnP1') # better quality 
	KeynotePDFImageQualityBest      = OSType('KnP2') # best quality 

class _KeynoteTransitionEffects(Enum):
	KeynoteTransitionEffectsNoTransitionEffect  = OSType('tnil') 
	KeynoteTransitionEffectsMagicMove           = OSType('tmjv')   
	KeynoteTransitionEffectsShimmer             = OSType('tshm')  
	KeynoteTransitionEffectsSparkle             = OSType('tspk')   
	KeynoteTransitionEffectsSwing               = OSType('tswg')   
	KeynoteTransitionEffectsObjectCube          = OSType('tocb')   
	KeynoteTransitionEffectsObjectFlip          = OSType('tofp')   
	KeynoteTransitionEffectsObjectPop           = OSType('topp')   
	KeynoteTransitionEffectsObjectPush          = OSType('toph')   
	KeynoteTransitionEffectsObjectRevolve       = OSType('torv')   
	KeynoteTransitionEffectsObjectZoom          = OSType('tozm')   
	KeynoteTransitionEffectsPerspective         = OSType('tprs')   
	KeynoteTransitionEffectsClothesline         = OSType('tclo')   
	KeynoteTransitionEffectsConfetti            = OSType('tcft')   
	KeynoteTransitionEffectsDissolve            = OSType('tdis')   
	KeynoteTransitionEffectsDrop                = OSType('tdrp')   
	KeynoteTransitionEffectsDroplet             = OSType('tdpl')   
	KeynoteTransitionEffectsFadeThroughColor    = OSType('tftc')   
	KeynoteTransitionEffectsGrid                = OSType('tgrd')   
	KeynoteTransitionEffectsIris                = OSType('tirs')   
	KeynoteTransitionEffectsMoveIn              = OSType('tmvi')   
	KeynoteTransitionEffectsPush                = OSType('tpsh')   
	KeynoteTransitionEffectsReveal              = OSType('trvl')   
	KeynoteTransitionEffectsSwitch              = OSType('tswi')   
	KeynoteTransitionEffectsWipe                = OSType('twpe')   
	KeynoteTransitionEffectsBlinds              = OSType('tbld')   
	KeynoteTransitionEffectsColorPlanes         = OSType('tcpl')   
	KeynoteTransitionEffectsCube                = OSType('tcub')   
	KeynoteTransitionEffectsDoorway             = OSType('tdwy')   
	KeynoteTransitionEffectsFall                = OSType('tfal')   
	KeynoteTransitionEffectsFlip                = OSType('tfip')   
	KeynoteTransitionEffectsFlop                = OSType('tfop')   
	KeynoteTransitionEffectsMosaic              = OSType('tmsc')   
	KeynoteTransitionEffectsPageFlip            = OSType('tpfl')   
	KeynoteTransitionEffectsPivot               = OSType('tpvt')   
	KeynoteTransitionEffectsReflection          = OSType('trfl')   
	KeynoteTransitionEffectsRevolvingDoor       = OSType('trev')   
	KeynoteTransitionEffectsScale               = OSType('tscl')   
	KeynoteTransitionEffectsSwap                = OSType('tswp')   
	KeynoteTransitionEffectsSwoosh              = OSType('tsws')   
	KeynoteTransitionEffectsTwirl               = OSType('ttwl')   
	KeynoteTransitionEffectsTwist               = OSType('ttwi')   
	KeynoteTransitionEffectsFadeAndMove         = OSType('tfad')   

class _KeynoteTAVT(Enum):
	KeynoteTAVTBottom   = OSType('avbt') # Right-align content. 
	KeynoteTAVTCenter   = OSType('actr') # Center-align content. 
	KeynoteTAVTTop      = OSType('avtp') # Top-align content. 

class _KeynoteTAHT(Enum):
	KeynoteTAHTAutoAlign    = OSType('aaut') # Auto-align based on content type. 
	KeynoteTAHTCenter       = OSType('actr') # Center-align content. 
	KeynoteTAHTJustify      = OSType('ajst') # Fully justify (left and right) content. 
	KeynoteTAHTLeft         = OSType('alft') # Left-align content. 
	KeynoteTAHTRight        = OSType('arit') # Right-align content. 

class _KeynoteNMSD(Enum):
	KeynoteNMSDAscending    = OSType('ascn') # Sort in increasing value order 
	KeynoteNMSDDescending   = OSType('dscn') # Sort in decreasing value order 

class _KeynoteNMCT(Enum):
	KeynoteNMCTAutomatic        = OSType('faut') # Automatic format 
	KeynoteNMCTCheckbox         = OSType('fcch') # Checkbox control format (Numbers only) 
	KeynoteNMCTCurrency         = OSType('fcur') # Currency number format 
	KeynoteNMCTDateAndTime      = OSType('fdtm') # Date and time format 
	KeynoteNMCTFraction         = OSType('ffra') # Fraction number format 
	KeynoteNMCTNumber           = OSType('nmbr') # Decimal number format 
	KeynoteNMCTPercent          = OSType('fper') # Percentage number format 
	KeynoteNMCTPopUpMenu        = OSType('fcpp') # Pop-up menu control format (Numbers only) 
	KeynoteNMCTScientific       = OSType('fsci') # Scientific notation format 
	KeynoteNMCTSlider           = OSType('fcsl') # Slider control format (Numbers only) 
	KeynoteNMCTStepper          = OSType('fcst') # Stepper control format (Numbers only) 
	KeynoteNMCTText             = OSType('ctxt') # Text format 
	KeynoteNMCTDuration         = OSType('fdur') # Duration format 
	KeynoteNMCTRating           = OSType('frat') # Rating format. (Numbers only) 
	KeynoteNMCTNumeralSystem    = OSType('fcns') # Numeral System 

class _KeynoteItemFillOptions(Enum):
	KeynoteItemFillOptionsNoFill                = OSType('fino')   
	KeynoteItemFillOptionsColorFill             = OSType('fico')   
	KeynoteItemFillOptionsGradientFill          = OSType('figr')   
	KeynoteItemFillOptionsAdvancedGradientFill  = OSType('fiag')   
	KeynoteItemFillOptionsImageFill             = OSType('fiim')   
	KeynoteItemFillOptionsAdvancedImageFill     = OSType('fiai')   

class _KeynotePlaybackRepetitionMethod(Enum):
	KeynotePlaybackRepetitionMethodNone             = OSType('mvrn')   
	KeynotePlaybackRepetitionMethodLoop             = OSType('mvlp')   
	KeynotePlaybackRepetitionMethodLoopBackAndForth = OSType('mvbf')   

# Visual style of chart
class _KeynoteLegacyChartType(Enum):
	KeynoteLegacyChartTypePie_2d                    = OSType('pie2') # two-dimensional pie chart 
	KeynoteLegacyChartTypeVertical_bar_2d           = OSType('vbr2') # two-dimensional vertical bar chart 
	KeynoteLegacyChartTypeStacked_vertical_bar_2d   = OSType('svb2') # two-dimensional stacked vertical bar chart 
	KeynoteLegacyChartTypeHorizontal_bar_2d         = OSType('hbr2') # two-dimensional horizontal bar chart 
	KeynoteLegacyChartTypeStacked_horizontal_bar_2d = OSType('shb2') # two-dimensional stacked horizontal bar chart 
	KeynoteLegacyChartTypePie_3d                    = OSType('pie3') # three-dimensional pie chart. 
	KeynoteLegacyChartTypeVertical_bar_3d           = OSType('vbr3') # three-dimensional vertical bar chart 
	KeynoteLegacyChartTypeStacked_vertical_bar_3d   = OSType('svb3') # three-dimensional stacked bar chart 
	KeynoteLegacyChartTypeHorizontal_bar_3d         = OSType('hbr3') # three-dimensional horizontal bar chart 
	KeynoteLegacyChartTypeStacked_horizontal_bar_3d = OSType('shb3') # three-dimensional stacked horizontal bar chart 
	KeynoteLegacyChartTypeArea_2d                   = OSType('are2') # two-dimensional area chart. 
	KeynoteLegacyChartTypeStacked_area_2d           = OSType('sar2') # two-dimensional stacked area chart 
	KeynoteLegacyChartTypeLine_2d                   = OSType('lin2') # two-dimensional line chart. 
	KeynoteLegacyChartTypeLine_3d                   = OSType('lin3') # three-dimensional line chart 
	KeynoteLegacyChartTypeArea_3d                   = OSType('are3') # three-dimensional area chart 
	KeynoteLegacyChartTypeStacked_area_3d           = OSType('sar3') # three-dimensional stacked area chart 
	KeynoteLegacyChartTypeScatterplot_2d            = OSType('scp2') # two-dimensional scatterplot chart 

class _KeynoteLegacyChartGrouping(Enum):
	KeynoteLegacyChartGroupingChartRow      = OSType('KCgr') # group by row
	KeynoteLegacyChartGroupingChartColumn   = OSType('KCgc') # group by column

class _KeyActions(Enum):
    SystemEventsEMdsCommandDown = 'Kcmd' # command down
    SystemEventsEMdsControlDown = 'Kctl' # control down
    SystemEventsEMdsOptionDown  = 'Kopt' # option down
    SystemEventsEMdsShiftDown   = 'Ksft' # shift down

class XAKeynoteApplication(XABaseScriptable.XASBApplication, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with Podcasts.app.

     .. seealso:: :class:`XAKeynoteWindow`, :class:`XAKeynoteDocument`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties = self.xa_scel.properties()
        self.name = self.properties["name"] #: The name of the Keynote application
        self.frontmost = self.properties["frontmost"] #: Whether Keynote is the active application
        self.version = self.properties["version"] #: The Keynote version number

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

    # Documents
    def documents(self, properties: Union[dict, None] = None) -> List['XAKeynoteDocument']:
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: List[XAKeynoteDocument]

        :Example 1: List all documents

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes())

        :Example 2: List documents after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return super().scriptable_elements("documents", properties, XAKeynoteDocument)

    def document(self, properties: Union[int, dict]) -> 'XAKeynoteDocument':
        """Returns the first document matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned document will have
        :type filter: Union[int, dict]
        :return: The document
        :rtype: XAKeynoteDocument

        :Example 1: Get a document by index

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.pane(0))

        :Example 2: Get a document by using a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return super().scriptable_element_with_properties("documents", properties, XAKeynoteDocument)

    def first_document(self) -> 'XAKeynoteDocument':
        """Returns the document at the zero index of the documents array.

        :return: The first document
        :rtype: XAKeynoteDocument

        .. versionadded:: 0.0.2
        """
        return super().first_scriptable_element("documents", XAKeynoteDocument)

    def last_document(self) -> 'XAKeynoteDocument':
        """Returns the document at the last (-1) index of the documents array.

        :return: The last document
        :rtype: XAKeynoteDocument

        .. versionadded:: 0.0.2
        """
        return super().last_scriptable_element("documents", XAKeynoteDocument)

    def new_slide(self, document: 'XAKeynoteDocument', properties: dict):
        return self.push("slide", properties, document.xa_elem.slides())

class XAKeynoteDocument(XABase.XAHasElements, XABaseScriptable.XASBPrintable, XABaseScriptable.XASBCloseable, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict = self.xa_elem.properties()
        self.name: str = self.properties["name"]
        self.modified: bool = self.properties["modified"]
        self.file: str = self.properties["file"]
        self.id: str = self.properties["id"]
        self.slide_numbers_showing: bool = self.properties["slideNumbersShowing"]
        self.auto_loop: bool = self.properties["autoLoop"]
        self.auto_play: bool = self.properties["autoPlay"]
        self.auto_restart: bool = self.properties["autoRestart"]
        self.maximum_idle_duration: int = self.properties["maximumIdleDuration"]
        self.height: int = self.properties["height"]
        self.width: int = self.properties["width"]
        self.password_protected: bool = self.properties["passwordProtected"]
        self.__document_theme: 'XAKeynoteTheme' = None
        self.__current_slide: 'XAKeynoteSlide' = None
        self.__selection: List['XAKeynoteiWorkItem'] = None

    def start_from(self, slide: 'XAKeynoteSlide') -> 'XAKeynoteSlide':
        self.xa_elem.startFrom_(slide.xa_elem)
        return self

    def stop(self):
        self.xa_elem.stop()

    def show_slide_switcher(self):
        self.xa_elem.showSlideSwitcher()

    def hide_slide_switcher(self):
        self.xa_elem.hideSlideSwitcher()

    def move_slide_switcher_forward(self):
        self.xa_elem.moveSlideSwitcherForward()

    def move_slide_switcher_backward(self):
        self.xa_elem.moveSlideSwitcherBackward()

    def cancel_slide_switcher(self):
        self.xa_elem.cancelSlideSwitcher()

    def accept_slide_switcher(self):
        self.xa_elem.acceptSlideSwitcher()

    def save(self, file_path: str = None, file_type: str = None):
        file_path = "/Users/steven/Downloads/Test.key"
        export_format = _KeynoteSaveableFileFormat.KeynoteSaveableFileFormatKeynote.value
        url = NSURL.alloc().initFileURLWithPath_(file_path)
        # self.xa_elem.exportTo_as_withProperties_(url, export_format, None)
        self.xa_elem.saveIn_as_(url, export_format)

    def export(self, file_path: str = None, file_type: str = None):
        file_path = "/Users/steven/Downloads/wowwwwww.pdf"
        export_format = _KeynoteExportFormat.KeynoteExportFormatPDF.value
        url = NSURL.alloc().initFileURLWithPath_(file_path)
        self.xa_elem.exportTo_as_withProperties_(url, export_format, None)

    # def save(self, file_path: str = None):
    #     # file_path = "/Users/steven/Documents/eek/wow"
    #     url = self.file
    #     if file_path is not None:
    #         url = NSURL.alloc().initFileURLWithPath_(file_path)
    #     self.xa_elem.saveIn_as_(url, _KeynoteSaveableFileFormat.KeynoteSaveableFileFormatKeynote.value)

    # Slides
    def slides(self, properties: Union[dict, None] = None) -> List['XAKeynoteSlide']:
        """Returns a list of slides, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned slides will have, or None
        :type filter: Union[dict, None]
        :return: The list of slides
        :rtype: List[XAKeynoteSlide]

        :Example 1: List all slides

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes())

        :Example 2: List slides after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return super().elements("slides", properties, XAKeynoteSlide)

    def slide(self, properties: Union[int, dict]) -> 'XAKeynoteSlide':
        """Returns the first slide matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned slide will have
        :type filter: Union[int, dict]
        :return: The slide
        :rtype: XAKeynoteSlide

        :Example 1: Get a slide by index

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.pane(0))

        :Example 2: Get a slide by using a filter

        >>> import PyXA
        >>> app = PyXA.application("System Preferences")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("slides", properties, XAKeynoteSlide)

    def first_slide(self) -> 'XAKeynoteSlide':
        """Returns the slide at the zero index of the slides array.

        :return: The first slide
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        return super().first_element("slides", XAKeynoteSlide)

    def last_slide(self) -> 'XAKeynoteSlide':
        """Returns the slide at the last (-1) index of the slides array.

        :return: The last slide
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        return super().last_element("slides", XAKeynoteSlide)

    def new_slide(self, properties: dict) -> 'XAKeynoteSlide':
        """Creates a new slide at the end of the presentation.

        :param properties: The properties to give the new slide
        :type properties: dict
        :return: A reference to the newly created slide
        :rtype: XAKeynoteSlide

        .. versionadded:: 0.0.2
        """
        return self.xa_prnt.new_slide(self, properties)


class XAKeynoteTheme(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Keynote themes.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteContainer(XABase.XAHasElements):
    """A class for managing and interacting with containers in Keynote.

    .. seealso:: :class:`XAKeynoteApplication`, :class:`XAKeynoteiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    # iWork Items
    def iwork_items(self, properties: Union[dict, None] = None) -> List['XAKeynoteiWorkItem']:
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: List[XAKeynoteiWorkItem]

        .. versionadded:: 0.0.2
        """
        return super().elements("iWorkItems", properties, XAKeynoteiWorkItem)

    def iwork_item(self, properties: Union[int, dict]) -> 'XAKeynoteiWorkItem':
        """Returns the first iWork item matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned iWork item will have
        :type filter: Union[int, dict]
        :return: The iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("iWorkItems", properties, XAKeynoteiWorkItem)

    def first_iwork_item(self) -> 'XAKeynoteiWorkItem':
        """Returns the iWork item at the zero index of the iWork items array.

        :return: The first iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        return super().first_element("iWorkItems", XAKeynoteiWorkItem)

    def last_iwork_item(self) -> 'XAKeynoteiWorkItem':
        """Returns the iWork item at the last (-1) index of the iWork items array.

        :return: The last iWork item
        :rtype: XAKeynoteiWorkItem

        .. versionadded:: 0.0.2
        """
        return super().last_element("iWorkItems", XAKeynoteiWorkItem)

    # AudioClips
    def audio_clips(self, properties: Union[dict, None] = None) -> List['XAKeynoteAudioClip']:
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: List[XAKeynoteAudioClip]

        .. versionadded:: 0.0.2
        """
        return super().elements("audioClips", properties, XAKeynoteAudioClip)

    def audio_clip(self, properties: Union[int, dict]) -> 'XAKeynoteAudioClip':
        """Returns the first image matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned audio clip will have
        :type filter: Union[int, dict]
        :return: The audio clip
        :rtype: XAKeynoteAudioClip

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("audioClips", properties, XAKeynoteAudioClip)

    def first_audio_clip(self) -> 'XAKeynoteAudioClip':
        """Returns the audio clip at the zero index of the audio clips array.

        :return: The first image
        :rtype: XAKeynoteAudioClip

        .. versionadded:: 0.0.2
        """
        return super().first_element("audioClips", XAKeynoteAudioClip)

    def last_audio_clip(self) -> 'XAKeynoteAudioClip':
        """Returns the audio clip at the last (-1) index of the audio clips array.

        :return: The last audio clip
        :rtype: XAKeynoteAudioClip

        .. versionadded:: 0.0.2
        """
        return super().last_element("audioClips", XAKeynoteAudioClip)

    # Charts
    def charts(self, properties: Union[dict, None] = None) -> List['XAKeynoteChart']:
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: List[XAKeynoteChart]

        .. versionadded:: 0.0.2
        """
        return super().elements("charts", properties, XAKeynoteChart)

    def chart(self, properties: Union[int, dict]) -> 'XAKeynoteChart':
        """Returns the first image matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned chart will have
        :type filter: Union[int, dict]
        :return: The chart
        :rtype: XAKeynoteChart

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("charts", properties, XAKeynoteChart)

    def first_chart(self) -> 'XAKeynoteChart':
        """Returns the chart at the zero index of the charts array.

        :return: The first image
        :rtype: XAKeynoteChart

        .. versionadded:: 0.0.2
        """
        return super().first_element("charts", XAKeynoteChart)

    def last_chart(self) -> 'XAKeynoteChart':
        """Returns the chart at the last (-1) index of the charts array.

        :return: The last chart
        :rtype: XAKeynoteChart

        .. versionadded:: 0.0.2
        """
        return super().last_element("charts", XAKeynoteChart)

    # Images
    def images(self, properties: Union[dict, None] = None) -> List['XAKeynoteImage']:
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: List[XAKeynoteImage]

        .. versionadded:: 0.0.2
        """
        return super().elements("images", properties, XAKeynoteImage)

    def image(self, properties: Union[int, dict]) -> 'XAKeynoteImage':
        """Returns the first image matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned image will have
        :type filter: Union[int, dict]
        :return: The image
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("images", properties, XAKeynoteImage)

    def first_image(self) -> 'XAKeynoteImage':
        """Returns the image at the zero index of the images array.

        :return: The first image
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        return super().first_element("images", XAKeynoteImage)

    def last_image(self) -> 'XAKeynoteImage':
        """Returns the image at the last (-1) index of the images array.

        :return: The last image
        :rtype: XAKeynoteImage

        .. versionadded:: 0.0.2
        """
        return super().last_element("images", XAKeynoteImage)

    # Groups
    def groups(self, properties: Union[dict, None] = None) -> List['XAKeynoteGroup']:
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: List[XAKeynoteGroup]

        .. versionadded:: 0.0.2
        """
        return super().elements("groups", properties, XAKeynoteGroup)

    def group(self, properties: Union[int, dict]) -> 'XAKeynoteGroup':
        """Returns the first group matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned group will have
        :type filter: Union[int, dict]
        :return: The group
        :rtype: XAKeynoteGroup

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("groups", properties, XAKeynoteGroup)

    def first_group(self) -> 'XAKeynoteGroup':
        """Returns the group at the zero index of the groups array.

        :return: The first group
        :rtype: XAKeynoteGroup

        .. versionadded:: 0.0.2
        """
        return super().first_element("groups", XAKeynoteGroup)

    def last_group(self) -> 'XAKeynoteGroup':
        """Returns the group at the last (-1) index of the groups array.

        :return: The last group
        :rtype: XAKeynoteGroup

        .. versionadded:: 0.0.2
        """
        return super().last_element("groups", XAKeynoteGroup)

    # Lines
    def lines(self, properties: Union[dict, None] = None) -> List['XAKeynoteLine']:
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: List[XAKeynoteLine]

        .. versionadded:: 0.0.2
        """
        return super().elements("lines", properties, XAKeynoteLine)

    def line(self, properties: Union[int, dict]) -> 'XAKeynoteLine':
        """Returns the first line matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned line will have
        :type filter: Union[int, dict]
        :return: The line
        :rtype: XAKeynoteLine

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("lines", properties, XAKeynoteLine)

    def first_line(self) -> 'XAKeynoteLine':
        """Returns the line at the zero index of the lines array.

        :return: The first line
        :rtype: XAKeynoteLine

        .. versionadded:: 0.0.2
        """
        return super().first_element("lines", XAKeynoteLine)

    def last_line(self) -> 'XAKeynoteLine':
        """Returns the line at the last (-1) index of the lines array.

        :return: The last line
        :rtype: XAKeynoteLine

        .. versionadded:: 0.0.2
        """
        return super().last_element("lines", XAKeynoteLine)

    # Movies
    def movies(self, properties: Union[dict, None] = None) -> List['XAKeynoteMovie']:
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: List[XAKeynoteMovie]

        .. versionadded:: 0.0.2
        """
        return super().elements("movies", properties, XAKeynoteMovie)

    def movie(self, properties: Union[int, dict]) -> 'XAKeynoteMovie':
        """Returns the first movie matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned movie will have
        :type filter: Union[int, dict]
        :return: The movie
        :rtype: XAKeynoteMovie

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("movies", properties, XAKeynoteMovie)

    def first_movie(self) -> 'XAKeynoteMovie':
        """Returns the movie at the zero index of the movies array.

        :return: The first movie
        :rtype: XAKeynoteMovie

        .. versionadded:: 0.0.2
        """
        return super().first_element("movies", XAKeynoteMovie)

    def last_movie(self) -> 'XAKeynoteMovie':
        """Returns the movie at the last (-1) index of the movies array.

        :return: The last movie
        :rtype: XAKeynoteMovie

        .. versionadded:: 0.0.2
        """
        return super().last_element("movies", XAKeynoteMovie)

    # Shapes
    def shapes(self, properties: Union[dict, None] = None) -> List['XAKeynoteShape']:
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: List[XAKeynoteShape]

        .. versionadded:: 0.0.2
        """
        return super().elements("shapes", properties, XAKeynoteShape)

    def shape(self, properties: Union[int, dict]) -> 'XAKeynoteShape':
        """Returns the first shape matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned shape will have
        :type filter: Union[int, dict]
        :return: The shape
        :rtype: XAKeynoteShape

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("shapes", properties, XAKeynoteShape)

    def first_shape(self) -> 'XAKeynoteShape':
        """Returns the shape at the zero index of the shapes array.

        :return: The first shape
        :rtype: XAKeynoteShape

        .. versionadded:: 0.0.2
        """
        return super().first_element("shapes", XAKeynoteShape)

    def last_shape(self) -> 'XAKeynoteShape':
        """Returns the shape at the last (-1) index of the shapes array.

        :return: The last shape
        :rtype: XAKeynoteShape

        .. versionadded:: 0.0.2
        """
        return super().last_element("shapes", XAKeynoteShape)

    # Tables
    def tables(self, properties: Union[dict, None] = None) -> List['XAKeynoteTable']:
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: List[XAKeynoteTable]

        .. versionadded:: 0.0.2
        """
        return super().elements("tables", properties, XAKeynoteTable)

    def table(self, properties: Union[int, dict]) -> 'XAKeynoteTable':
        """Returns the first table matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned table will have
        :type filter: Union[int, dict]
        :return: The table
        :rtype: XAKeynoteTable

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("tables", properties, XAKeynoteTable)

    def first_table(self) -> 'XAKeynoteTable':
        """Returns the table at the zero index of the tables array.

        :return: The first table
        :rtype: XAKeynoteTable

        .. versionadded:: 0.0.2
        """
        return super().first_element("tables", XAKeynoteTable)

    def last_table(self) -> 'XAKeynoteTable':
        """Returns the table at the last (-1) index of the tables array.

        :return: The last table
        :rtype: XAKeynoteTable

        .. versionadded:: 0.0.2
        """
        return super().last_element("tables", XAKeynoteTable)

    # Text Items
    def text_items(self, properties: Union[dict, None] = None) -> List['XAKeynoteTextItem']:
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: List[XAKeynoteTextItem]

        .. versionadded:: 0.0.2
        """
        return super().elements("text_items", properties, XAKeynoteTextItem)

    def text_item(self, properties: Union[int, dict]) -> 'XAKeynoteTextItem':
        """Returns the first text_item matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned text_item will have
        :type filter: Union[int, dict]
        :return: The text_item
        :rtype: XAKeynoteTextItem

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("text_items", properties, XAKeynoteTextItem)

    def first_text_item(self) -> 'XAKeynoteTextItem':
        """Returns the text_item at the zero index of the text_items array.

        :return: The first text_item
        :rtype: XAKeynoteTextItem

        .. versionadded:: 0.0.2
        """
        return super().first_element("text_items", XAKeynoteTextItem)

    def last_text_item(self) -> 'XAKeynoteTextItem':
        """Returns the text_item at the last (-1) index of the text_items array.

        :return: The last text_item
        :rtype: XAKeynoteTextItem

        .. versionadded:: 0.0.2
        """
        return super().last_element("text_items", XAKeynoteTextItem)

class XAKeynoteSlide(XAKeynoteContainer):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`, :class:`XAKeynoteiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict = self.xa_elem.properties()
        self.body_showing: bool = self.properties["bodyShowing"]
        self.skipped: bool = self.properties["skipped"]
        self.slide_number: int = self.properties["slideNumber"]
        self.title_showing: bool = self.properties["titleShowing"]
        self.__base_layout = None
        self.__default_body_item = None
        self.__default_title_item = None
        self.__presenter_notes = None
        self.__transition_properties = None

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

    def add_chart(self, row_names: List[str], column_names: List[str], data: List[List[Any]], type: int = _KeynoteLegacyChartType.KeynoteLegacyChartTypeLine_2d.value, group_by: int = _KeynoteLegacyChartGrouping.KeynoteLegacyChartGroupingChartRow.value) -> 'XAKeynoteChart':
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


class XAKeynoteSlideLayout(XABaseScriptable.XASBObject):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteSlide`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name = self.xa_elem.name()


class XAKeynoteiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Keynote.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int = self.xa_elem.height()
        self.locked: bool = self.xa_elem.locked()
        self.width: int = self.xa_elem.width()
        self.__parent = None
        self.__position = None

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

class XAKeynoteGroup(XAKeynoteiWorkItem):
    """A class for managing and interacting with iWork item groups in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteImage(XAKeynoteiWorkItem):
    """A class for managing and interacting with images in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.description: str = self.xa_elem.objectDescription()
        self.file = self.xa_elem.file()
        self.file_name: str = self.xa_elem.fileName().get()
        self.opacity: int = self.xa_elem.opacity()
        self.reflection_showing: bool = self.xa_elem.reflectionShowing()
        self.reflection_value: int = self.xa_elem.reflectionValue()
        self.rotation: int = self.xa_elem.rotation()

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

class XAKeynoteAudioClip(XAKeynoteiWorkItem):
    """A class for managing and interacting with audio clips in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str = self.xa_elem.fileName()
        self.clip_volume: int = self.xa_elem.clipVolume()
        self.repitition_method: int = self.xa_elem.repetitionMethod()

class XAKeynoteShape(XAKeynoteiWorkItem):
    """A class for managing and interacting with shapes in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: int = self.xa_elem.backgroundFillType()
        self.text: str = self.xa_elem.objectText()
        self.opacity: int = self.xa_elem.opacity()
        self.reflection_showing: bool = self.xa_elem.reflectionShowing()
        self.reflection_value: int = self.xa_elem.reflectionValue()
        self.rotation: int = self.xa_elem.rotation()

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

class XAKeynoteChart(XAKeynoteiWorkItem):
    """A class for managing and interacting with charts in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteLine(XAKeynoteiWorkItem):
    """A class for managing and interacting with lines in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteMovie(XAKeynoteiWorkItem):
    """A class for managing and interacting with movie containers in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteTextItem(XAKeynoteiWorkItem):
    """A class for managing and interacting with text items in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteTable(XAKeynoteiWorkItem):
    """A class for managing and interacting with tables in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAKeynoteRange(XABase.XAObject):
    """A class for managing and interacting with ranges of table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties = self.xa_elem.properties()
        self.font_name: str = self.properties["fontName"]

class XAKeynoteRow(XAKeynoteRange):
    """A class for managing and interacting with table rows in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int = self.xa_elem.address()
        self.height: float = self.xa_elem.height()

class XAKeynoteColumn(XAKeynoteRange):
    """A class for managing and interacting with table columns in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int = self.xa_elem.address()
        self.width: float = self.xa_elem.width()

class XAKeynoteCell(XAKeynoteRange):
    """A class for managing and interacting with table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.formatted_value: str = self.xa_elem.formattedValue()
        self.formula:str = self.xa_elem.formula()
        self.value = self.xa_elem.value()
        print(self.value)
        self.__column = None
        self.__row = None