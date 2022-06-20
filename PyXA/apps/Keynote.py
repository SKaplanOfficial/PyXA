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
        return super().scriptable_elements("documents", properties, XAKeynoteDocument)

    def document(self, properties: Union[int, dict]) -> 'XAKeynoteDocument':
        """Returns the first document matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned document will have
        :type filter: Union[int, dict]
        :return: The document
        :rtype: XAKeynoteDocument

        :Example 1: Export the document that has a specific name

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> doc = app.document({"name": "Example1.key"})
        >>> doc.export("/Users/exampleuser/Documents/Example1.pdf", app.ExportFormat.PDF)

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

    # Themes
    def themes(self, properties: Union[dict, None] = None) -> List['XAKeynoteTheme']:
        """Returns a list of themes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned themes will have, or None
        :type filter: Union[dict, None]
        :return: The list of themes
        :rtype: List[XAKeynoteTheme]

        :Example 1: List the name of each theme

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> themes = app.themes()
        >>> print([theme.name for theme in themes])
        ['Basic White', 'Basic Black', 'Classic White', 'White', 'Black', 'Basic Color', 'Color Gradient Light', 'Color Gradient', 'Gradient', 'Showroom', 'Modern Portfolio', 'Slate', 'Photo Essay', 'Bold Color', 'Showcase', 'Briefing', 'Academy', 'Modern Type', 'Exhibition', 'Feature Story', 'Look Book', 'Classic', 'Editorial', 'Cream Paper', 'Industrial', 'Blueprint', 'Graph Paper', 'Chalkboard', 'Photo Portfolio', 'Leather Book', 'Artisan', 'Improv', 'Drafting', 'Kyoto', 'Brushed Canvas', 'Craft', 'Parchment', 'Renaissance', 'Moroccan', 'Hard Cover', 'Linen Book', 'Vintage', 'Typeset', 'Harmony', 'Formal']

        .. versionadded:: 0.0.2
        """
        return super().scriptable_elements("themes", properties, XAKeynoteTheme)

    def theme(self, properties: Union[int, dict]) -> 'XAKeynoteTheme':
        """Returns the first theme matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned theme will have
        :type filter: Union[int, dict]
        :return: The theme
        :rtype: XAKeynoteTheme

        :Example 1: Create a new document with a specific theme

        >>> import PyXA
        >>> app = PyXA.application("Keynote")
        >>> exhibition_theme = app.theme({"name": "Exhibition"})
        >>> app.new_document(theme = exhibition_theme)

        .. versionadded:: 0.0.2
        """
        return super().scriptable_element_with_properties("themes", properties, XAKeynoteTheme)

    def first_theme(self) -> 'XAKeynoteTheme':
        """Returns the theme at the zero index of the themes array.

        :return: The first theme
        :rtype: XAKeynoteTheme

        .. versionadded:: 0.0.2
        """
        return super().first_scriptable_element("themes", XAKeynoteTheme)

    def last_theme(self) -> 'XAKeynoteTheme':
        """Returns the theme at the last (-1) index of the themes array.

        :return: The last theme
        :rtype: XAKeynoteTheme

        .. versionadded:: 0.0.2
        """
        return super().last_scriptable_element("themes", XAKeynoteTheme)

class XAKeynoteWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Keynote.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        
    @property
    def document(self) -> 'XAKeynoteDocument':
        if self.__document is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_scel.document(),
                "scriptable_element": self.xa_scel.document(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__column = XAKeynoteDocument(properties)
        return self.__document

class XAKeynoteDocument(XABase.XAHasElements, XABaseScriptable.XASBPrintable, XABaseScriptable.XASBCloseable, XABase.XAAcceptsPushedElements, XABase.XACanConstructElement):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict = self.xa_elem.properties()
        self.name: str = self.xa_elem.name()
        self.modified: bool = self.xa_elem.modified()
        self.file: str = self.xa_elem.file()
        self.id: str = self.xa_elem.id()
        self.slide_numbers_showing: bool = self.xa_elem.slideNumbersShowing()
        self.auto_loop: bool = self.xa_elem.autoLoop()
        self.auto_play: bool = self.xa_elem.autoPlay()
        self.auto_restart: bool = self.xa_elem.autoRestart()
        self.maximum_idle_duration: int = self.xa_elem.maximumIdleDuration()
        self.height: int = self.xa_elem.height()
        self.width: int = self.xa_elem.width()
        self.password_protected: bool = self.xa_elem.passwordProtected()
        self.__document_theme: 'XAKeynoteTheme' = None
        self.__current_slide: 'XAKeynoteSlide' = None
        self.__selection: List['XAKeynoteiWorkItem'] = None

    @property
    def document_theme(self) -> 'XAKeynoteTheme':
        if self.__document_theme is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.documentTheme(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__document_theme = XAKeynoteTheme(properties)
        return self.__document_theme

    @property
    def current_slide(self) -> 'XAKeynoteSlide':
        if self.__current_slide is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.currentSlide(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__current_slide = XAKeynoteSlide(properties)
        return self.__current_slide

    @property
    def selection(self) -> 'XAKeynoteiWorkItem':
        if self.__selection is None:
            objects = []
            items = self.xa_elem.selection()
            for item in items:
                properties = {
                    "parent": self,
                    "appspace": self.xa_apsp,
                    "workspace": self.xa_wksp,
                    "element": item,
                    "appref": self.xa_aref,
                    "system_events": self.xa_sevt,
                }
                description = item.specifierDescription()
                element_class = XAKeynoteiWorkItem
                if "defaultBodyItem" in description or "defaultTitleItem" in description or "sshp" in description:
                    element_class = XAKeynoteShape
                elif "shtx" in description:
                    element_class = XAKeynoteTextItem
                elif "imag" in description:
                    element_class = XAKeynoteImage
                elif "igrp" in description:
                    element_class = XAKeynoteGroup
                elif 'iWln' in description:
                    element_class = XAKeynoteLine
                elif "NmTb" in description:
                    element_class = XAKeynoteTable
                elif "shau" in description:
                    element_class = XAKeynoteAudioClip
                elif "shmv" in description:
                    element_class = XAKeynoteMovie
                elif "shct" in description:
                    element_class = XAKeynoteChart
                objects.append(element_class(properties))
            self.__selection = objects
        return self.__selection

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

    # Slides
    def slides(self, properties: Union[dict, None] = None) -> List['XAKeynoteSlide']:
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
        return super().elements("slides", properties, XAKeynoteSlide)

    def slide(self, properties: Union[int, dict]) -> 'XAKeynoteSlide':
        """Returns the first slide matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned slide will have
        :type filter: Union[int, dict]
        :return: The slide
        :rtype: XAKeynoteSlide

        :Example 1: Get a slide by index

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.pane(0))

        :Example 2: Get a slide by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
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

    # Slide Layouts
    def slide_layouts(self, properties: Union[dict, None] = None) -> List['XAKeynoteSlideLayout']:
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
        return super().elements("slideLayouts", properties, XAKeynoteSlideLayout)

    def slide_layout(self, properties: Union[int, dict]) -> 'XAKeynoteSlideLayout':
        """Returns the first slide_layout matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned slide_layout will have
        :type filter: Union[int, dict]
        :return: The slide_layout
        :rtype: XAKeynoteSlideLayout

        :Example 1: Get a slide_layout by index

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.pane(0))

        :Example 2: Get a slide_layout by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Keynotes")
        >>> print(app.panes({"name": "Accessibility"}))

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("slideLayouts", properties, XAKeynoteSlideLayout)

    def first_slide_layout(self) -> 'XAKeynoteSlideLayout':
        """Returns the slide_layout at the zero index of the slide_layouts array.

        :return: The first slide_layout
        :rtype: XAKeynoteSlideLayout

        .. versionadded:: 0.0.2
        """
        return super().first_element("slideLayouts", XAKeynoteSlideLayout)

    def last_slide_layout(self) -> 'XAKeynoteSlideLayout':
        """Returns the slide_layout at the last (-1) index of the slide_layouts array.

        :return: The last slide_layout
        :rtype: XAKeynoteSlideLayout

        .. versionadded:: 0.0.2
        """
        return super().last_element("slideLayouts", XAKeynoteSlideLayout)


class XAKeynoteTheme(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Keynote themes.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.xa_elem.id()
        self.name = self.xa_elem.name()

    def __repr__(self):
        return f"<{str(type(self))}{self.name}, id={str(self.id)}>"

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
        self.transition_properties: dict = self.properties["transitionProperties"]
        self.__base_layout = None
        self.__default_body_item = None
        self.__default_title_item = None
        self.__presenter_notes = None

    @property
    def base_layout(self) -> 'XAKeynoteSlideLayout':
        if self.__base_layout is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.baseLayout(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__base_layout = XAKeynoteSlideLayout(properties)
        return self.__base_layout

    @property
    def default_body_item(self) -> 'XAKeynoteSlideLayout':
        if self.__default_body_item is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.defaultBodyItem(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__default_body_item = XAKeynoteShape(properties)
        return self.__default_body_item

    @property
    def default_title_item(self) -> 'XAKeynoteSlideLayout':
        if self.__default_title_item is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.defaultTitleItem(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__default_title_item = XAKeynoteShape(properties)
        return self.__default_title_item

    @property
    def presenter_notes(self) -> 'XAKeynoteSlideLayout':
        if self.__presenter_notes is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.presenterNotes(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__presenter_notes = XABase.XAText(properties)
        return self.__presenter_notes

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


class XAKeynoteSlideLayout(XAKeynoteSlide):
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
        self.position: Tuple[int, int] = self.xa_elem.position()
        self.__parent = None

    @property
    def parent(self):
        if self.__parent == None:
            self.__parent = self.xa_prnt
        return self.__parent

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

class XAKeynoteGroup(XAKeynoteContainer):
    """A class for managing and interacting with iWork item groups in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.height: int = self.xa_elem.height()
        self.position: Tuple[int, int] = self.xa_elem.position()
        self.width: int = self.xa_elem.width()
        self.rotation: int = self.xa_elem.rotation()
        self.__parent = None

    @property
    def parent(self):
        if self.__parent == None:
            self.__parent = self.xa_prnt
        return self.__parent

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
        self.end_point: Tuple[int, int] = self.xa_elem.endPoint()
        self.reflection_showing: bool = self.xa_elem.reflectionShowing()
        self.reflection_value: int = self.xa_elem.reflectionValue()
        self.rotation: int = self.xa_elem.rotation()
        self.start_point: Tuple[int, int] = self.xa_elem.startPoint()

class XAKeynoteMovie(XAKeynoteiWorkItem):
    """A class for managing and interacting with movie containers in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_name: str = self.xa_elem.fileName()
        self.movie_volume: int = self.xa_elem.movieVolume()
        self.opacity: int = self.xa_elem.opacity()
        self.reflection_showing: bool = self.xa_elem.reflectionShowing()
        self.reflection_value: int = self.xa_elem.reflectionValue()
        self.repetition_method: int = self.xa_elem.repetitionMethod()
        self.rotation: int = self.xa_elem.rotation()

class XAKeynoteTextItem(XAKeynoteiWorkItem):
    """A class for managing and interacting with text items in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.background_fill_type: int = self.xa_elem.backgroundFillType()
        self.text = XABase.XAText(self.xa_elem.objectText().properties())
        print(self.text)
        self.opacity: int = self.xa_elem.opacity()
        self.reflection_showing: bool = self.xa_elem.reflectionShowing()
        self.reflection_value: int = self.xa_elem.reflectionValue()
        self.rotation: int = self.xa_elem.rotation()

class XAKeynoteTable(XAKeynoteiWorkItem, XABase.XAHasElements):
    """A class for managing and interacting with tables in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str = self.xa_elem.name() #: The name of the table
        self.row_count: int = self.xa_elem.rowCount() #: The number of rows in the table
        self.column_count: int = self.xa_elem.columnCount() #: The number of columns in the table
        self.header_row_count: int = self.xa_elem.headerRowCount() #: The number of header rows in the table
        self.header_column_count: int = self.xa_elem.headerColumnCount() #: The number of header columns in the table
        self.footer_row_count: int = self.xa_elem.footerRowCount() #: The number of footer rows in the table
        self.__cell_range = None #: The range of all cells in the table
        self.__selection_range = None #: The currently selected cells

    @property
    def cell_range(self) -> 'XAKeynoteRange':
        if self.__cell_range is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.cellRange(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__cell_range = XAKeynoteRange(properties)
        return self.__cell_range

    @property
    def selection_range(self) -> 'XAKeynoteRange':
        if self.__selection_range is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.selectionRange(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__selection_range = XAKeynoteRange(properties)
        return self.__selection_range

    # TODO
    def sort(self, columns: List['XAKeynoteColumn'], rows: List['XAKeynoteRow'], direction: XAKeynoteApplication.SortDirection = XAKeynoteApplication.SortDirection.ASCENDING) -> 'XAKeynoteTable':
        column_objs = [column.xa_elem for column in columns]
        row_objs = [row.xa_elem for row in rows]
        self.xa_elem.sortBy_direction_inRows_(column_objs[0], direction.value, row_objs)
        return self

    # Cells
    def cells(self, properties: Union[dict, None] = None) -> List['XAKeynoteCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAKeynoteCell]

        .. versionadded:: 0.0.2
        """
        return super().elements("cells", properties, XAKeynoteCell)

    def cell(self, properties: Union[int, dict]) -> 'XAKeynoteCell':
        """Returns the first cell matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned cell will have
        :type filter: Union[int, dict]
        :return: The cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("cells", properties, XAKeynoteCell)

    def first_cell(self) -> 'XAKeynoteCell':
        """Returns the cell at the zero index of the cells array.

        :return: The first cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().first_element("cells", XAKeynoteCell)

    def last_cell(self) -> 'XAKeynoteCell':
        """Returns the cell at the last (-1) index of the cells array.

        :return: The last cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().last_element("cells", XAKeynoteCell)

    # Columns
    def columns(self, properties: Union[dict, None] = None) -> List['XAKeynoteColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAKeynoteColumn]

        .. versionadded:: 0.0.2
        """
        return super().elements("columns", properties, XAKeynoteColumn)

    def column(self, properties: Union[int, dict]) -> 'XAKeynoteColumn':
        """Returns the first column matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned column will have
        :type filter: Union[int, dict]
        :return: The column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("columns", properties, XAKeynoteColumn)

    def first_column(self) -> 'XAKeynoteColumn':
        """Returns the column at the zero index of the columns array.

        :return: The first column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().first_element("columns", XAKeynoteColumn)

    def last_column(self) -> 'XAKeynoteColumn':
        """Returns the column at the last (-1) index of the columns array.

        :return: The last column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().last_element("columns", XAKeynoteColumn)

    # Rows
    def rows(self, properties: Union[dict, None] = None) -> List['XAKeynoteRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAKeynoteRow]

        .. versionadded:: 0.0.2
        """
        return super().elements("rows", properties, XAKeynoteRow)

    def row(self, properties: Union[int, dict]) -> 'XAKeynoteRow':
        """Returns the first row matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned row will have
        :type filter: Union[int, dict]
        :return: The row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("rows", properties, XAKeynoteRow)

    def first_row(self) -> 'XAKeynoteRow':
        """Returns the row at the zero index of the rows array.

        :return: The first row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().first_element("rows", XAKeynoteRow)

    def last_row(self) -> 'XAKeynoteRow':
        """Returns the row at the last (-1) index of the rows array.

        :return: The last row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().last_element("rows", XAKeynoteRow)

    # Ranges
    def ranges(self, properties: Union[dict, None] = None) -> List['XAKeynoteRange']:
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: List[XAKeynoteRange]

        .. versionadded:: 0.0.2
        """
        return super().elements("ranges", properties, XAKeynoteRange)

    def range(self, properties: Union[int, dict]) -> 'XAKeynoteRange':
        """Returns the first range matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned range will have
        :type filter: Union[int, dict]
        :return: The range
        :rtype: XAKeynoteRange

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("ranges", properties, XAKeynoteRange)

    def first_range(self) -> 'XAKeynoteRange':
        """Returns the range at the zero index of the ranges array.

        :return: The first range
        :rtype: XAKeynoteRange

        .. versionadded:: 0.0.2
        """
        return super().first_element("ranges", XAKeynoteRange)

    def last_range(self) -> 'XAKeynoteRange':
        """Returns the range at the last (-1) index of the ranges array.

        :return: The last range
        :rtype: XAKeynoteRange

        .. versionadded:: 0.0.2
        """
        return super().last_element("ranges", XAKeynoteRange)

class XAKeynoteRange(XABase.XAHasElements):
    """A class for managing and interacting with ranges of table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties = self.xa_elem.properties()
        self.font_name: str = self.xa_elem.fontName()
        self.font_size: float = self.xa_elem.fontSize()
        self.format: int = self.xa_elem.format()
        self.alignment: int = self.xa_elem.alignment()
        self.name: str = self.xa_elem.name()
        self.text_wrap: bool = self.xa_elem.textWrap()
        self.vertical_alignment: int = self.xa_elem.verticalAlignment()
        self.size: int = len(self.xa_elem.cells()) #: The number of cells in the range
        self.__text_color = None
        self.__background_color = None

    @property
    def text_color(self) -> XABase.XAColor:
        if self.__text_color == None:
            color_obj = self.xa_elem.textColor()
            if color_obj is not None:
                self.__text_color = XABase.XAColor().copy_color(color_obj)
        return self.__text_color

    @property
    def background_color(self) -> XABase.XAColor:
        if self.__background_color == None:
            color_obj = self.xa_elem.backgroundColor()
            if color_obj is not None:
                self.__background_color = XABase.XAColor().copy_color(color_obj)
        return self.__background_color

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

    # Cells
    def cells(self, properties: Union[dict, None] = None) -> List['XAKeynoteCell']:
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: List[XAKeynoteCell]

        .. versionadded:: 0.0.2
        """
        return super().elements("cells", properties, XAKeynoteCell)

    def cell(self, properties: Union[int, dict]) -> 'XAKeynoteCell':
        """Returns the first cell matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned cell will have
        :type filter: Union[int, dict]
        :return: The cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("cells", properties, XAKeynoteCell)

    def first_cell(self) -> 'XAKeynoteCell':
        """Returns the cell at the zero index of the cells array.

        :return: The first cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().first_element("cells", XAKeynoteCell)

    def last_cell(self) -> 'XAKeynoteCell':
        """Returns the cell at the last (-1) index of the cells array.

        :return: The last cell
        :rtype: XAKeynoteCell

        .. versionadded:: 0.0.2
        """
        return super().last_element("cells", XAKeynoteCell)

    # Columns
    def columns(self, properties: Union[dict, None] = None) -> List['XAKeynoteColumn']:
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: List[XAKeynoteColumn]

        .. versionadded:: 0.0.2
        """
        return super().elements("columns", properties, XAKeynoteColumn)

    def column(self, properties: Union[int, dict]) -> 'XAKeynoteColumn':
        """Returns the first column matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned column will have
        :type filter: Union[int, dict]
        :return: The column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("columns", properties, XAKeynoteColumn)

    def first_column(self) -> 'XAKeynoteColumn':
        """Returns the column at the zero index of the columns array.

        :return: The first column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().first_element("columns", XAKeynoteColumn)

    def last_column(self) -> 'XAKeynoteColumn':
        """Returns the column at the last (-1) index of the columns array.

        :return: The last column
        :rtype: XAKeynoteColumn

        .. versionadded:: 0.0.2
        """
        return super().last_element("columns", XAKeynoteColumn)

    # Rows
    def rows(self, properties: Union[dict, None] = None) -> List['XAKeynoteRow']:
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: List[XAKeynoteRow]

        .. versionadded:: 0.0.2
        """
        return super().elements("rows", properties, XAKeynoteRow)

    def row(self, properties: Union[int, dict]) -> 'XAKeynoteRow':
        """Returns the first row matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned row will have
        :type filter: Union[int, dict]
        :return: The row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().element_with_properties("rows", properties, XAKeynoteRow)

    def first_row(self) -> 'XAKeynoteRow':
        """Returns the row at the zero index of the rows array.

        :return: The first row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().first_element("rows", XAKeynoteRow)

    def last_row(self) -> 'XAKeynoteRow':
        """Returns the row at the last (-1) index of the rows array.

        :return: The last row
        :rtype: XAKeynoteRow

        .. versionadded:: 0.0.2
        """
        return super().last_element("rows", XAKeynoteRow)

class XAKeynoteRow(XAKeynoteRange):
    """A class for managing and interacting with table rows in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int = self.xa_elem.address() #: The index of the row in the table
        self.height: float = self.xa_elem.height() #: The height of the row in pixels

class XAKeynoteColumn(XAKeynoteRange):
    """A class for managing and interacting with table columns in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.address: int = self.xa_elem.address() #: The index of the column in the tabel
        self.width: float = self.xa_elem.width() #: The width of the column in pixels

class XAKeynoteCell(XAKeynoteRange):
    """A class for managing and interacting with table cells in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.formatted_value: str = self.xa_elem.formattedValue() #: The formatted form of the value stored in the cell
        self.formula: str = self.xa_elem.formula() #: The formula in the cell as text
        self.value = self.xa_elem.value().get() #: The value stored in the cell
        self.__column: XAKeynoteColumn = None #: The cell's column
        self.__row: XAKeynoteRow = None #: The cell's row

    @property
    def column(self) -> XAKeynoteColumn:
        if self.__column is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.column(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__column = XAKeynoteColumn(properties)
        return self.__column

    @property
    def row(self) -> XAKeynoteRow:
        if self.__row is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_elem.row(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__row = XAKeynoteRow(properties)
        return self.__row