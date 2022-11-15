""".. versionadded:: 0.0.2

Control the macOS Keynote application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, Union, Self

import AppKit
import logging

from PyXA import XABase
from PyXA import XAEvents
from PyXA.XABase import OSType

from . import iWorkApplicationBase

logger = logging.getLogger("keynote")

class XAKeynoteApplication(iWorkApplicationBase.XAiWorkApplication):
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

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAKeynoteWindow

        logger.debug("Initialized XAKeynoteApplication")

    @property
    def properties(self) -> dict:
        """All properties of the Keynote application.
        """
        raw_dict = self.xa_scel.properties()
        return {
            "slide_switcher_visible": raw_dict["slideSwitcherVisible"] == 1,
            "frontmost": self.frontmost,
            "playing": self.playing,
            "version": self.version,
            "name": self.name,
        }

    @property
    def playing(self) -> bool:
        """Whether a slideshow is currently playing.
        """
        return self.xa_scel.playing()

    @property
    def slide_switcher_visible(self) -> bool:
        """Whether the slide switcher is visible.
        """
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

    def new_document(self, file_path: Union[str, XABase.XAPath] = "./Untitled.key", theme: 'XAKeynoteTheme' = None) -> 'XAKeynoteDocument':
        """Creates a new document at the specified path and with the specified theme.

        :param file_path: The path to create the document at, defaults to "./Untitled.key"
        :type file_path: str, optional
        :param template: The theme to initialize the document with, defaults to None
        :type template: XAKeynoteTheme, optional
        :return: The newly created document object
        :rtype: XAKeynoteDocument

        .. versionadded:: 0.0.8
        """
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)

        properties = {
            "file": file_path.xa_elem,
        }

        if theme is not None:
            properties["documentTheme"] = theme.xa_elem

        new_document = self.make("document", properties)
        return self.documents().push(new_document)

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
            return self._new_element(obj, iWorkApplicationBase.XAiWorkShape)
        elif specifier == "table":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkTable)
        elif specifier == "audioClip":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkAudioClip)
        elif specifier == "chart":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkChart)
        elif specifier == "image":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkImage)
        elif specifier == "slide":
            return self._new_element(obj, XAKeynoteSlide)
        elif specifier == "line":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkLine)
        elif specifier == "movie":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkMovie)
        elif specifier == "textItem":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkTextItem)
        elif specifier == "group":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkGroup)
        elif specifier == "iWorkItem":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkiWorkItem)
        elif specifier == "TransitionSettings":
            return self._new_element(obj, XAKeynoteTransitionSettings)




class XAKeynoteWindow(iWorkApplicationBase.XAiWorkWindow):
    """A class for managing and interacting with windows in Keynote.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> 'XAKeynoteDocument':
        """The document currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XAKeynoteDocument)




class XAKeynoteDocumentList(iWorkApplicationBase.XAiWorkDocumentList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAKeynoteDocument)
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
                "selection": [self._new_element(x, iWorkApplicationBase.XAiWorkiWorkItem) for x in document.selection()],
                "password_protected": document.passwordProtected(),
            }
        return pyxa_dicts

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

    def by_selection(self, selection: 'iWorkApplicationBase.XAiWorkiWorkItemList') -> Union['XAKeynoteDocument', None]:
        return self.by_property("selection", selection.xa_elem)

    def by_password_protected(self, password_protected: bool) -> Union['XAKeynoteDocument', None]:
        return self.by_property("passwordProtected", password_protected)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XAKeynoteDocument(iWorkApplicationBase.XAiWorkDocument):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAKeynoteApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document.
        """
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
            "selection": self._new_element(self.xa_elem.selection(), iWorkApplicationBase.XAiWorkiWorkItemList),
            "password_protected": self.xa_elem.passwordProtected(),
        }
        return pyxa_dict

    @property
    def name(self) -> str:
        """The name of the document.
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save.
        """
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        """The location of the document on the disk, if one exists.
        """
        return self.xa_elem.file()

    @property
    def id(self) -> str:
        """The unique identifier for the document.
        """
        return self.xa_elem.id()

    @property
    def slide_numbers_showing(self) -> bool:
        """Whether slide numbers are displayed.
        """
        return self.xa_elem.slideNumbersShowing()

    @slide_numbers_showing.setter
    def slide_numbers_showing(self, slide_numbers_showing: bool):
        self.set_property('slideNumbersShowing', slide_numbers_showing)

    @property
    def document_theme(self) -> 'XAKeynoteTheme':
        """The theme assigned to the document.
        """
        return self._new_element(self.xa_elem.documentTheme(), XAKeynoteTheme)

    @document_theme.setter
    def document_theme(self, document_theme: 'XAKeynoteTheme'):
        self.set_property('documentTheme', document_theme.xa_elem)

    @property
    def auto_loop(self) -> bool:
        """Whether the slideshow should play repeatedly.
        """
        return self.xa_elem.autoLoop()

    @auto_loop.setter
    def auto_loop(self, auto_loop: bool):
        self.set_property('autoLoop', auto_loop)

    @property
    def auto_play(self) -> bool:
        """Whether the slideshow should automatically play when opening the file.
        """
        return self.xa_elem.autoPlay()

    @auto_play.setter
    def auto_play(self, auto_play: bool):
        self.set_property('autoPlay', auto_play)

    @property
    def auto_restart(self) -> bool:
        """Whether the slideshow should restart if its inactive for the maximum idle duration.
        """
        return self.xa_elem.autoRestart()

    @auto_restart.setter
    def auto_restart(self, auto_restart: bool):
        self.set_property('autoRestart', auto_restart)

    @property
    def maximum_idle_duration(self) -> int:
        """The duration before which the slideshow restarts due to inactivity.
        """
        return self.xa_elem.maximumIdleDuration()

    @maximum_idle_duration.setter
    def maximum_idle_duration(self, maximum_idle_duration: int):
        self.set_property('maximumIdleDuration', maximum_idle_duration)

    @property
    def current_slide(self) -> 'XAKeynoteSlide':
        """The currently selected slide, or the slide that would display is the presentation was started.
        """
        return self._new_element(self.xa_elem.currentSlide(), XAKeynoteSlide)

    @current_slide.setter
    def current_slide(self, current_slide: 'XAKeynoteSlide'):
        self.set_property('currentSlide', current_slide.xa_elem)

    @property
    def height(self) -> int:
        """The height of the document in points; standard is 768; wide slide height is 1080.
        """
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def width(self) -> int:
        """The width of the document in points; standard is 1080; wide slide width is 1920.
        """
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def selection(self) -> 'iWorkApplicationBase.XAiWorkiWorkItemList':
        """A list of the currently selected items.
        """
        return self._new_element(self.xa_elem.selection(), iWorkApplicationBase.XAiWorkiWorkItemList)

    @selection.setter
    def selection(self, selection: Union['iWorkApplicationBase.XAiWorkiWorkItemList', list['iWorkApplicationBase.XAiWorkiWorkItem']]):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property('selection', selection)
        else:
            self.set_property('selection', selection.xa_elem)

    @property
    def password_protected(self) -> bool:
        """Whether the document is password protected.
        """
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

    @property
    def properties(self) -> dict:
        """All properties of the theme.
        """
        return {
            "id": self.xa_elem.id(),
            "name": self.xa_elem.name()
        }

    @property
    def id(self) -> str:
        """The unique identifier for the theme.
        """
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the theme.
        """
        return self.xa_elem.name()

    def __repr__(self):
        return f"<{str(type(self))}{self.name}, id={str(self.id)}>"




class XAKeynoteContainerList(iWorkApplicationBase.XAiWorkContainerList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAKeynoteContainer
        self._xa_ccls = XAKeynoteSlideList
        super().__init__(properties, filter, obj_class)
        logger.debug("Got list of containers")

class XAKeynoteContainer(iWorkApplicationBase.XAiWorkContainer):
    """A class for managing and interacting with containers in Keynote.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        self._xa_ccls = XAKeynoteSlideList
        super().__init__(properties)




class XAKeynoteSlideList(XAKeynoteContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAKeynoteSlide
        super().__init__(properties, filter, obj_class)
        logger.debug("Got list of slides")

    def properties(self) -> list[dict]:
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "default_title_item": self._new_element(raw_dict["defaultTitleItem"], iWorkApplicationBase.XAiWorkShape),
                "slide_number": raw_dict["slideNumber"],
                "default_body_item": self._new_element(raw_dict["defaultBodyItem"], iWorkApplicationBase.XAiWorkShape),
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

    def default_body_item(self) -> 'iWorkApplicationBase.XAiWorkShapeList':
        ls = self.xa_elem.arrayByApplyingSelector_("defaultBodyItem")
        return self._new_element(ls, iWorkApplicationBase.XAiWorkShapeList)

    def default_title_item(self) -> 'iWorkApplicationBase.XAiWorkShapeList':
        ls = self.xa_elem.arrayByApplyingSelector_("defaultTitleItem")
        return self._new_element(ls, iWorkApplicationBase.XAiWorkShapeList)

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

    def by_default_body_item(self, default_body_item: 'iWorkApplicationBase.XAiWorkShape') -> 'XAKeynoteSlide':
        return self.by_property("defaultBodyItem", default_body_item.xa_elem)

    def by_default_text_item(self, default_text_item: 'iWorkApplicationBase.XAiWorkShape') -> 'XAKeynoteSlide':
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

    .. seealso:: :class:`XAKeynoteApplication`, :class:`iWorkApplicationBase.XAiWorkiWorkItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the slide.
        """
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "default_title_item": self._new_element(raw_dict["defaultTitleItem"], iWorkApplicationBase.XAiWorkShape),
            "slide_number": raw_dict["slideNumber"],
            "default_body_item": self._new_element(raw_dict["defaultBodyItem"], iWorkApplicationBase.XAiWorkShape),
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
        """Whether the default body text is displayed.
        """
        return self.xa_elem.bodyShowing()

    @body_showing.setter
    def body_showing(self, body_showing: bool):
        self.set_property('bodyShowing', body_showing)

    @property
    def skipped(self) -> bool:
        """Whether the slide is skipped.
        """
        return self.xa_elem.skipped()

    @skipped.setter
    def skipped(self, skipped: bool):
        self.set_property('skipped', skipped)

    @property
    def slide_number(self) -> int:
        """The index of the slide in the document.
        """
        return self.xa_elem.slideNumber()

    @property
    def title_showing(self) -> bool:
        """Whether the default slide title is displayed.
        """
        return self.xa_elem.titleShowing()

    @title_showing.setter
    def title_showing(self, title_showing: bool):
        self.set_property('titleShowing', title_showing)

    @property
    def transition_properties(self) -> dict:
        """The transition settings applied to the slide.
        """
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
        """The slide layout this slide is based on.
        """
        return self._new_element(self.xa_elem.baseLayout(), XAKeynoteSlideLayout)

    @base_layout.setter
    def base_layout(self, base_layout: 'XAKeynoteSlideLayout'):
        self.set_property('baseLayout', base_layout.xa_elem)

    @property
    def default_body_item(self) -> 'iWorkApplicationBase.XAiWorkShape':
        """The default body container of the slide.
        """
        return self._new_element(self.xa_elem.defaultBodyItem(), iWorkApplicationBase.XAiWorkShape)

    @property
    def default_title_item(self) -> 'iWorkApplicationBase.XAiWorkShape':
        """The default title container of the slide.
        """
        return self._new_element(self.xa_elem.defaultTitleItem(), iWorkApplicationBase.XAiWorkShape)

    @property
    def presenter_notes(self) -> XABase.XAText:
        """The presenter notes for the slide.
        """
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

    def add_image(self, file_path: Union[str, XABase.XAPath, XABase.XAURL]) -> 'iWorkApplicationBase.XAiWorkImage':
        """Adds the image at the specified path to the slide.

        :param file_path: The path to the image file.
        :type file_path: Union[str, XABase.XAPath, XABase.XAURL]
        :return: The newly created image object.
        :rtype: iWorkApplicationBase.XAiWorkImage

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

    def add_chart(self, row_names: list[str], column_names: list[str], data: list[list[Any]], type: int = XAKeynoteApplication.ChartType.LINE_2D.value, group_by: int = XAKeynoteApplication.ChartGrouping.ROW.value) -> 'iWorkApplicationBase.XAiWorkChart':
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
        :rtype: iWorkApplicationBase.XAiWorkChart

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
        return self._new_element(chart, iWorkApplicationBase.XAiWorkChart)

    def __repr__(self):
        return "<" + str(type(self)) + "slide number: " + str(self.slide_number) + ">"




class XAKeynoteSlideLayoutList(XAKeynoteSlideList):
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

    @property
    def name(self) -> str:
        """The name of the slide layout.
        """
        return self.xa_elem.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




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