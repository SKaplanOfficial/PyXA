""".. versionadded:: 0.1.1

Control iWork applications using JXA-like syntax.
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

logger = logging.getLogger("iwork")

class XAiWorkApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with iWork applications.

    .. versionadded:: 0.1.1
    """
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
        ROW      = OSType('KCgr') #: Group by row
        COLUMN   = OSType('KCgc') #: Group by column

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
        NONE                    = OSType('mvrn') #: Clip does not repeat
        LOOP                    = OSType('mvlp') #: Clip repeats sequentially
        LOOP_BACK_AND_FORTH     = OSType('mvbf') #: Clip boomerangs back and forth repeatedly

    class KeyAction(Enum):
        """Options for key states and interactions.
        """
        COMMAND_DOWN = OSType('Kcmd')
        CONTROL_DOWN = OSType('Kctl')
        OPTION_DOWN  = OSType('Kopt')
        SHIFT_DOWN   = OSType('Ksft')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAiWorkWindow

    @property
    def properties(self) -> dict:
        """All properties of the Keynote application.
        """
        raw_dict = self.xa_scel.properties()
        return {
            "frontmost": self.frontmost,
            "version": self.version,
            "name": self.name,
        }

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether this application is the active application.
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The application version number.
        """
        return self.xa_scel.version()

    @property
    def current_document(self) -> 'XAiWorkDocument':
        """The current document of the front window.
        """
        return self.front_window.document

    def print(self, item: Union['XAiWorkDocument', XABaseScriptable.XASBWindow], print_properties: dict = None, show_dialog: bool = True) -> Self:
        """Prints a document or window.

        :param item: The document or window to print
        :type item: Union[XAiWorkDocument, XABaseScriptable.XASBWindow]
        :param print_properties: The settings to pre-populate the print dialog with, defaults to None
        :type print_properties: dict, optional
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: A reference to the PyXA application object
        :rtype: Self

        .. versionadded:: 0.1.1
        """
        if print_properties is None:
            print_properties = {}
        self.xa_scel.print_withProperties_printDialog_(item.xa_elem, print_properties, show_dialog)
        return self

    def open(self, path: Union[str, XABase.XAPath]) -> 'XAiWorkDocument':
        """Opens the file at the given filepath.

        :param target: The path of the file to open.
        :type target: Union[str, XABase.XAPath]
        :return: A reference to newly created document object
        :rtype: XAiWorkDocument

        .. versionadded:: 0.1.1
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self.documents()[0]

    def set_password(self, document: 'XAiWorkDocument', password: str, hint: str, save_in_keychain: bool = True) -> Self:
        """Sets the password of an unencrypted document, optionally storing the password in the user's keychain.

        :param document: The document to set the password for
        :type document: XAiWorkDocument
        :param password: The password
        :type password: str
        :param hint: A hint for the password
        :type hint: str
        :param save_in_keychain: Whether to save the password in the user's keychain, defaults to True
        :type save_in_keychain: bool, optional
        :return: A reference to the PyXA application object
        :rtype: Self

        .. versionadded:: 0.1.1
        """
        self.xa_scel.setPassword_to_hint_savingInKeychain_(password, document.xa_elem, hint, save_in_keychain)
        return self

    def remove_password(self, document: 'XAiWorkDocument', password: str) -> Self:
        """Removes the password from a document.

        :param document: The document to remove the password to
        :type document: XAiWorkDocument
        :param password: The current password
        :type password: str
        :return: A reference to the PyXA application object
        :rtype: Self

        .. versionadded:: 0.1.1
        """
        self.xa_scel.removePassword_from_(password, document.xa_elem)
        return self




class XAiWorkWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject):
    """A window of an iWork application.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAiWorkDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAiWorkDocumentList
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of documents")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
        """
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, document in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "name": document.name(),
                "modified": document.modified(),
                "file": XABase.XAPath(document.file()),
                "id": document.id(),
            }
        return pyxa_dicts

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def file(self) -> list[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of document file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def id(self) -> list[str]:
        """Gets the ID of each document in the list.

        :return: A list of document IDs
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def selection(self) -> 'XAiWorkiWorkItemList':
        """Gets the selection of each document in the list.

        :return: A list of selected items in each document of the list
        :rtype: XAiWorkiWorkItemList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        ls = [x for t in ls for x in t]
        return self._new_element(ls, XAiWorkiWorkItemList)

    def password_protected(self) -> list[bool]:
        """Gets the password protected status of each document in the list.

        :return: A list of document password protect status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected"))

    def by_properties(self, properties: dict) -> Union['XAiWorkDocument', None]:
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
                return self._new_element(document, XAiWorkDocument)

    def by_name(self, name: str) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("modified", modified)

    def by_file(self, file: Union[str, XABase.XAPath]) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose file path matches the given file, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        if isinstance(file, XABase.XAPath):
            file = file.url
        return self.by_property("file", file)

    def by_id(self, id: str) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose ID matches the given ID, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("id", id)

    def by_selection(self, selection: Union['XAiWorkiWorkItemList', list['XAiWorkiWorkItem']]) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose selection matches the given list of objects, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
        elif isinstance(selection, XAiWorkiWorkItemList):
            selection = selection.xa_elem
        return self.by_property("selection", selection)

    def by_password_protected(self, password_protected: bool) -> Union['XAiWorkDocument', None]:
        """Retrieves the first document whose password protected status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAiWorkDocument, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("passwordProtected", password_protected)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XAiWorkDocument(XABaseScriptable.XASBPrintable, XACloseable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XAiWorkApplication`

    .. versionadded:: 0.1.1
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
    def file(self) -> XABase.XAPath:
        """The location of the document on the disk, if one exists.
        """
        file = self.xa_elem.file()
        if file is not None:
            return XABase.XAPath(file)

    @property
    def id(self) -> str:
        """The unique identifier for the document.
        """
        return self.xa_elem.id()

    @property
    def selection(self) -> 'XAiWorkiWorkItemList':
        """A list of the currently selected items.
        """
        return self._new_element(self.xa_elem.selection(), XAiWorkiWorkItemList)

    @selection.setter
    def selection(self, selection: Union['XAiWorkiWorkItemList', 'XAiWorkiWorkItem']):
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

    def __repr__(self):
        return f"<{str(type(self))}{self.name}>"




class XAiWorkContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAiWorkContainer
        super().__init__(properties, obj_class, filter)

        # Specialize to group or specific container type
        if self.__class__ == XAiWorkContainerList:
            if all([x.parent().get() == None for x in self.xa_elem]):
                if hasattr(self, "_xa_ccls"):
                    new_self = self._new_element(self.xa_elem, self._xa_ccls)
                    self.__class__ = new_self.__class__
                    self.__dict__.update(new_self.__dict__)

            elif all([x.parent().get() != None for x in self.xa_elem]):
                new_self = self._new_element(self.xa_elem, XAiWorkGroupList)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)

    def charts(self, filter: Union[dict, None] = None) -> 'XAiWorkChartList':
        """Returns the charts of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's charts
        :rtype: XAiWorkChartList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("charts")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAiWorkGroupList':
        """Returns the groups of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's groups
        :rtype: XAiWorkGroupList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("groups")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAiWorkImageList':
        """Returns the images of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's images
        :rtype: XAiWorkImageList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("images")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAiWorkiWorkItemList':
        """Returns the iWork items of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's iWork items
        :rtype: XAiWorkiWorkItemList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("iWorkItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAiWorkLineList':
        """Returns the lines of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's lines
        :rtype: XAiWorkLineList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("lines")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'XAiWorkMovieList':
        """Returns the movies of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's movies
        :rtype: XAiWorkMovieList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("movies")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAiWorkShapeList':
        """Returns the shapes of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's shapes
        :rtype: XAiWorkShapeList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("shapes")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAiWorkTableList':
        """Returns the tables of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's tables
        :rtype: XAiWorkTableList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("tables")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAiWorkTextItemList':
        """Returns the text items of each container in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every container's text items
        :rtype: XAiWorkTextItemList

        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, XAiWorkTableList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self.xa_elem)) + ">"

class XAiWorkContainer(XABase.XAObject):
    """A class for managing and interacting with containers in Keynote.

    .. seealso:: :class:`XAiWorkApplication`, :class:`XAiWorkiWorkItem`

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        # Specialize to group or specific container type
        if self.__class__ == XAiWorkContainer:
            if self.xa_elem.baseLayout().get() is not None:
                if hasattr(self, "_xa_ccls"):
                    new_self = self._new_element(self.xa_elem, self._xa_ccls)
                    self.__class__ = new_self.__class__
                    self.__dict__.update(new_self.__dict__)

            elif self.xa_elem.parent().get() is not None:
                new_self = self._new_element(self.xa_elem, XAiWorkGroup)
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'XAiWorkiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: XAiWorkiWorkItemList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.iWorkItems(), XAiWorkiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'XAiWorkAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: XAiWorkAudioClipList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.audioClips(), XAiWorkAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'XAiWorkChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: XAiWorkChartList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.charts(), XAiWorkChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAiWorkImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XAiWorkImageList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.images(), XAiWorkImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAiWorkGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAiWorkGroupList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.groups(), XAiWorkGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'XAiWorkLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: XAiWorkLineList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.lines(), XAiWorkLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'XAiWorkMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: XAiWorkMovieList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.movies(), XAiWorkMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'XAiWorkShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: XAiWorkShapeList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.shapes(), XAiWorkShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'XAiWorkTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XAiWorkTableList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.tables(), XAiWorkTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'XAiWorkTextItemList':
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: XAiWorkTextItemList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.textItems(), XAiWorkTextItemList, filter)




class XAiWorkiWorkItemList(XABase.XAList):
    """A wrapper around a list of documents.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAiWorkiWorkItem
        super().__init__(properties, obj_class, filter)
        logger.debug("Got list of iWork items")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each iWork item in the list.

        :return: A list of item properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
        """
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, item in enumerate(self.xa_elem):
            pyxa_dicts[index] = {
                "parent": self._new_element(item.parent(), XAiWorkiWorkItem),
                "locked": item.locked(),
                "height": item.height(),
                "position": tuple(item.position()),
                "width": item.width(),
            }
        return pyxa_dicts

    def height(self) -> list[int]:
        """Gets the height of each iWork item in the list.

        :return: A list of item heights
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def locked(self) -> list[bool]:
        """Gets the locked status of each iWork item in the list.

        :return: A list of item locked status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def width(self) -> list[int]:
        """Gets the width of each iWork item in the list.

        :return: A list of item widths
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def parent(self) -> XAiWorkContainerList:
        """Gets the parent of each iWork item in the list.

        :return: A list of containers
        :rtype: XAiWorkContainerList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAiWorkContainerList)

    def position(self) -> list[tuple[int, int]]:
        """Gets the position of each iWork item in the list.

        :return: A list of iWork item positions
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("position")
        return [tuple(x.pointValue()) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose properties dictionary matches the given properties, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
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
                return self._new_element(item, XAiWorkiWorkItem)

    def by_height(self, height: int) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose height matches the given height, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("height", height)

    def by_locked(self, locked: bool) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose locked status matches the given boolean value, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("locked", locked)

    def by_width(self, width: int) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose width matches the given width, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("width", width)

    def by_parent(self, parent: XAiWorkContainer) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose parent matches the given object, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("parent", parent.xa_elem)

    def by_position(self, position: tuple[int, int]) -> Union['XAiWorkiWorkItem', None]:
        """Retrieves the first iWork item whose position matches the given position, if one exists.

        :return: The desired iWork item, if it is found
        :rtype: Union[XAiWorkiWorkItem, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("position", position)

    def __repr__(self):
        return "<" + str(type(self)) + "length:" + str(len(self.xa_elem)) + ">"

class XAiWorkiWorkItem(XABase.XAObject):
    """A class for managing and interacting with text, shapes, images, and other elements in Keynote.

    .. seealso:: :class:`XAiWorkApplication`

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        if self.__class__ == XAiWorkiWorkItem:
            description = self.xa_elem.get().description()

            # Specialize to some iWork Item type
            new_self = None
            if ": defaultTitleItem" in description or ": defaultBodyItem" in description or ": <class 'sshp'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkShape)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkShape")
            elif ": <class 'imag'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkImage)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkImage")
            elif ": <class 'igrp'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkGroup)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkGroup")
            elif ": <class 'shtx'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkTextItem)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkTextItem")
            elif ": <class 'NmTb'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkTable)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkTable")
            elif ": <class 'iWln'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkLine)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkLine")
            elif ": <class 'shmv'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkMovie)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkMovie")
            elif ": <class 'shau'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkAudioClip)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkAudioClip")
            elif ": <class 'shct'>" in description:
                new_self = self._new_element(self.xa_elem, XAiWorkChart)
                logger.debug("Specialized XAiWorkiWorkItem to XAiWorkChart")

            if new_self is not None:
                new_self.xa_prnt = self.xa_prnt
                self.__class__ = new_self.__class__
                self.__dict__.update(new_self.__dict__)
            else:
                print(description)

    @property
    def height(self) -> int:
        """The height of the iWork item.
        """
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def locked(self) -> bool:
        """Whether the object is locked.
        """
        return self.xa_elem.locked()

    @locked.setter
    def locked(self, locked: bool):
        self.set_property('locked', locked)

    @property
    def width(self) -> int:
        """The width of the iWork item.
        """
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def parent(self) -> XAiWorkContainer:
        """The iWork container that contains the iWork item.
        """
        return self._new_element(self.xa_elem.parent(), XAiWorkContainer)

    @property
    def position(self) -> tuple[int, int]:
        """The horizontal and vertical coordinates of the top left point of the iWork item.
        """
        return tuple(self.xa_elem.position())

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    def delete(self):
        """Deletes the item.

        .. versionadded:: 0.1.1
        """
        self.xa_elem.delete()

    def duplicate(self) -> 'XAiWorkiWorkItem':
        """Duplicates the item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAiWorkiWorkItem

        .. versionadded:: 0.1.1
        """
        if isinstance(self.xa_prnt, XAiWorkiWorkItemList):
            self.xa_elem.duplicateTo_withProperties_(self.xa_elem.positionAfter(), {})
        else:
            self.xa_elem.duplicateTo_withProperties_(self.xa_prnt.xa_elem.iWorkItems(), {})
        return self

    def resize(self, width: int, height: int) -> 'XAiWorkiWorkItem':
        """Sets the width and height of the item.

        :param width: The desired width, in pixels
        :type width: int
        :param height: The desired height, in pixels
        :type height: int
        :return: The iWork item
        :rtype: XAiWorkiWorkItem

        .. versionadded:: 0.1.1
        """
        self.set_properties({
            "width": width,
            "height": height,
        })
        return self

    def lock(self) -> 'XAiWorkiWorkItem':
        """Locks the properties of the item, preventing changes.

        :return: The iWork item
        :rtype: XAiWorkiWorkItem

        .. versionadded:: 0.1.1
        """
        self.set_property("locked", True)
        return self

    def unlock(self) -> 'XAiWorkiWorkItem':
        """Unlocks the properties of the item, allowing changes.

        :return: The iWork item
        :rtype: XAiWorkiWorkItem

        .. versionadded:: 0.1.1
        """
        self.set_property("locked", False)
        return self

    def set_position(self, x: int, y: int) -> 'XAiWorkiWorkItem':
        position = AppKit.NSValue.valueWithPoint_(AppKit.NSPoint(x, y))
        self.xa_elem.setValue_forKey_(position, "position")

    def __repr__(self):
        return "<" + str(type(self)) + "position: " + str(self.position) + ">"





class XAiWorkGroupList(XAiWorkContainerList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkGroup)
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

    def parent(self) -> XAiWorkContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAiWorkContainerList)

    def by_height(self, height: int) -> 'XAiWorkGroup':
        return self.by_property("height", height)

    def by_position(self, position: tuple[int, int]) -> 'XAiWorkGroup':
        return self.by_property("position", position)

    def by_width(self, width: int) -> 'XAiWorkGroup':
        return self.by_property("width", width)

    def by_rotation(self, rotation: int) -> 'XAiWorkGroup':
        return self.by_property("rotation", rotation)

    def by_parent(self, parent: XAiWorkContainer) -> 'XAiWorkGroup':
        return self.by_property("parent", parent.xa_elem)

class XAiWorkGroup(XAiWorkContainer):
    """A class for managing and interacting with iWork item groups in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def height(self) -> int:
        """The height of the group.
        """
        return self.xa_elem.height()

    @height.setter
    def height(self, height: int):
        self.set_property('height', height)

    @property
    def position(self) -> tuple[int, int]:
        """The horizontal and vertical coordinates of the top left point of the group.
        """
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property('position', position)

    @property
    def width(self) -> int:
        """The width of the group.
        """
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property('width', width)

    @property
    def rotation(self) -> int:
        """The rotation of the group, in degrees from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def parent(self) -> XAiWorkContainer:
        """The container which contains the group.
        """
        return self._new_element(self.xa_elem.parent(), XAiWorkContainer)




class XAiWorkImageList(XAiWorkiWorkItemList):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkImage)
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

    def by_description(self, description: str) -> 'XAiWorkImage':
        return self.by_property("objectDescription", description)

    def by_file(self, file: str) -> 'XAiWorkImage':
        return self.by_property("file", file)

    def by_file_name(self, file_name: str) -> 'XAiWorkImage':
        return self.by_property("fileName", file_name)

    def by_opacity(self, opacity: int) -> 'XAiWorkImage':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAiWorkImage':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAiWorkImage':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAiWorkImage':
        return self.by_property("rotation", rotation)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XAiWorkImage(XAiWorkiWorkItem):
    """A class for managing and interacting with images in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def description(self) -> str:
        """Text associated with the image, read aloud by VoiceOVer.
        """
        return self.xa_elem.object_description()

    @description.setter
    def description(self, description: str):
        self.set_property('description', description)

    @property
    def file(self) -> str:
        """The image file.
        """
        return self.xa_elem.file()

    @property
    def file_name(self) -> str:
        """The name of the image file.
        """
        return self.xa_elem.fileName().get()

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def opacity(self) -> int:
        """The opacity of the image, in percent from 0 to 100.
        """
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        """Whether the image displays a reflection.
        """
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        """The percentage of reflection of the image, from 0 to 100.
        """
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        """The rotation of the image, in degrees from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> 'XAiWorkImage':
        """Rotates the image by the specified number of degrees.

        :param degrees: The amount to rotate the image, in degrees, from -359 to 359
        :type degrees: int
        :return: The image.
        :rtype: XAiWorkImage

        .. deprecated:: 0.1.1

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.1.1
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def replace_with(self, img_path: Union[str, XABase.XAPath, XABase.XAURL]) -> 'XAiWorkImage':
        """Removes the image and inserts another in its place with the same width and height.

        :param img_path: The path to the new image file.
        :type img_path: Union[str, XABase.XAPath, XABase.XAURL]
        :return: A reference to the new PyXA image object.
        :rtype: XAiWorkImage

        .. versionadded:: 0.1.1
        """
        self.delete()
        if isinstance(img_path, str):
            if "://" in img_path:
                img_path = XABase.XAURL(img_path)
            else:
                img_path = XABase.XAPath(img_path)

        parent = self.xa_prnt
        while not hasattr(parent, "add_image"):
            parent = parent.xa_prnt

        return parent.add_image(img_path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAiWorkAudioClipList(XAiWorkiWorkItemList):
    """A wrapper around lists of audio clips that employs fast enumeration techniques.

    All properties of audio clips can be called as methods on the wrapped list, returning a list containing each audio clips's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkAudioClip)
        logger.debug("Got list of audio clips")

    def file_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName"))

    def clip_volume(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("clipVolume"))

    def repetition_method(self) -> list[XAiWorkApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAiWorkApplication.RepetitionMethod(XABase.OSType(x.stringValue())) for x in ls]

    def by_file_name(self, file_name: str) -> 'XAiWorkAudioClip':
        return self.by_property("fileName", file_name)

    def by_clip_volume(self, clip_volume: int) -> 'XAiWorkAudioClip':
        return self.by_property("clipVolume", clip_volume)

    def by_repetition_method(self, repetition_method: XAiWorkApplication.RepetitionMethod) -> 'XAiWorkAudioClip':
        for audio_clip in self.xa_elem:
            if audio_clip.repetitionMethod() == repetition_method.value:
                return self._new_element(audio_clip, XAiWorkAudioClip)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"

class XAiWorkAudioClip(XAiWorkiWorkItem):
    """A class for managing and interacting with audio clips in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def file_name(self) -> str:
        """The name of the audio file.
        """
        return self.xa_elem.fileName().get()

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def clip_volume(self) -> int:
        """The volume setting for the audio clip, from 0 to 100.
        """
        return self.xa_elem.clipVolume()

    @clip_volume.setter
    def clip_volume(self, clip_volume: int):
        self.set_property('clipVolume', clip_volume)

    @property
    def repetition_method(self) -> XAiWorkApplication.RepetitionMethod:
        """Whether or how the audio clip  repeats.
        """
        return XAiWorkApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAiWorkApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name) + ">"




class XAiWorkShapeList(XAiWorkiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkShape)
        logger.debug("Got list of shapes")

    def properties(self) -> list[dict]:
        return [{
            "reflection_showing": shape.reflectionShowing(),
            "rotation": shape.rotation(),
            "position": tuple(shape.position()),
            "parent": self._new_element(shape.parent(), XAiWorkContainer),
            "width": shape.width(),
            "opacity": shape.opacity(),
            "locked": shape.locked(),
            "height": shape.height(),
            "background_fill_type": XAiWorkApplication.FillOption(shape.backgroundFillType()),
            "reflection_value": shape.reflectionValue(),
            "object_text": shape.objectText().get()
        } for shape in self.xa_elem]

    def background_fill_type(self) -> list[XAiWorkApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundFillType")
        return [XAiWorkApplication.FillOption(XABase.OSType(x.stringValue())) for x in ls]

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

    def by_properties(self, properties: dict) -> Union['XAiWorkShape', None]:
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
                return self._new_element(shape, XAiWorkShape)

    def by_background_fill_type(self, background_fill_type: XAiWorkApplication.FillOption) -> Union['XAiWorkShape', None]:
        for shape in self.xa_elem:
            if shape.backgroundFillType() == background_fill_type.value:
                return self._new_element(shape, XAiWorkShape)

    def by_object_text(self, object_text: Union[str, XABase.XAText]) -> Union['XAiWorkShape', None]:
        if isinstance(object_text, str):
            return self.by_property('objectText', object_text)
        else:
            return self.by_property('objectText', object_text.xa_elem)

    def by_opacity(self, opacity: int) -> Union['XAiWorkShape', None]:
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> Union['XAiWorkShape', None]:
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> Union['XAiWorkShape', None]:
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> Union['XAiWorkShape', None]:
        return self.by_property("rotation", rotation)

class XAiWorkShape(XAiWorkiWorkItem):
    """A class for managing and interacting with shapes in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the shape.
        """
        return self.xa_elem.properties()

    @property
    def background_fill_type(self) -> XAiWorkApplication.FillOption:
        """The background, if any, for the shape.
        """
        return XAiWorkApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def object_text(self) -> XABase.XAText:
        """The text contained within the shape.
        """
        return self._new_element(self.xa_elem.objectText(), XABase.XAText)

    @object_text.setter
    def object_text(self, object_text: Union[str, XABase.XAText]):
        if isinstance(object_text, str):
            self.set_property('objectText', object_text)
        else:
            self.set_property('objectText', object_text.xa_elem)

    @property
    def opacity(self) -> int:
        """The percent opacity of the object.
        """
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        """Whether the iWork item displays a reflection.
        """
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        """The percentage of relfection that the iWork item displays, from 0 to 100.
        """
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        """The rotation of the iWork item, in degrees, from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    def rotate(self, degrees: int) -> 'XAiWorkShape':
        """Rotates the shape by the specified number of degrees.

        :param degrees: The amount to rotate the shape, in degrees, from -359 to 359
        :type degrees: int
        :return: The shape.
        :rtype: XAiWorkShape

        .. deprecated:: 0.1.1

           Set the :attr:`rotation` attribute directly instead.

        .. versionadded:: 0.1.1
        """
        self.set_property("rotation", self.rotation + degrees)
        return self

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = AppKit.NSValue.valueWithPoint_(AppKit.NSPoint(value[0], value[1]))
        super().set_property(property_name, value)




class XAiWorkChartList(XAiWorkiWorkItemList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkChart)
        logger.debug("Got list of charts")

class XAiWorkChart(XAiWorkiWorkItem):
    """A class for managing and interacting with charts in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAiWorkLineList(XAiWorkiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkLine)
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

    def by_end_point(self, end_point: tuple[int, int]) -> 'XAiWorkLine':
        return self.by_property("endPoint", end_point)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAiWorkLine':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAiWorkLine':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAiWorkLine':
        return self.by_property("rotation", rotation)

    def by_start_point(self, start_point: tuple[int, int]) -> 'XAiWorkLine':
        return self.by_property("startPoint", start_point)

class XAiWorkLine(XAiWorkiWorkItem):
    """A class for managing and interacting with lines in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def end_point(self) -> tuple[int, int]:
        """A list of two numbers indicating the horizontal and vertical position of the line ending point.
        """
        return self.xa_elem.endPoint()

    @end_point.setter
    def end_point(self, end_point: tuple[int, int]):
        self.set_property('endPoint', end_point)

    @property
    def reflection_showing(self) -> bool:
        """Whether the line displays a reflection.
        """
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        """The percent of reflection of the line, from 0 to 100.
        """
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        """The rotation of the line, in degrees from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)

    @property
    def start_point(self) -> tuple[int, int]:
        """A list of two numbers indicating the horizontal and vertical position of the line starting point.
        """
        return self.xa_elem.startPoint()

    @start_point.setter
    def start_point(self, start_point: tuple[int, int]):
        self.set_property('startPoint', start_point)




class XAiWorkMovieList(XAiWorkiWorkItemList):
    """A wrapper around lists of movies that employs fast enumeration techniques.

    All properties of movies can be called as methods on the wrapped list, returning a list containing each movie's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkMovie)
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

    def reflection_value(self) -> list[XAiWorkApplication.RepetitionMethod]:
        ls = self.xa_elem.arrayByApplyingSelector_("repetitionMethod")
        return [XAiWorkApplication.RepetitionMethod(x) for x in ls]

    def rotation(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("rotation"))

    def by_file_name(self, file_name: str) -> 'XAiWorkMovie':
        return self.by_property("fileName", file_name)

    def by_movie_volume(self, movie_volume: int) -> 'XAiWorkMovie':
        return self.by_property("movieVolume", movie_volume)

    def by_opacity(self, opacity: int) -> 'XAiWorkMovie':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAiWorkMovie':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAiWorkMovie':
        return self.by_property("reflectionValue", reflection_value)

    def by_repetition_method(self, repetition_method: XAiWorkApplication.RepetitionMethod) -> 'XAiWorkMovie':
        return self.by_property("repetitionMethod", repetition_method.value)

    def by_rotation(self, rotation: int) -> 'XAiWorkMovie':
        return self.by_property("rotation", rotation)

class XAiWorkMovie(XAiWorkiWorkItem):
    """A class for managing and interacting with movie containers in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def file_name(self) -> str:
        """The name of the movie file.
        """
        return self.xa_elem.fileName()

    @file_name.setter
    def file_name(self, file_name: str):
        self.set_property('fileName', file_name)

    @property
    def movie_volume(self) -> int:
        """The volume setting for the movie, from 0 to 100.
        """
        return self.xa_elem.movieVolume()

    @movie_volume.setter
    def movie_volume(self, movie_volume: int):
        self.set_property('movieVolume', movie_volume)

    @property
    def opacity(self) -> int:
        """The percent opacity of the object.
        """
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        """Whether the movie displays a reflection.
        """
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        """The percentage of reflection of the movie, from 0 to 100.
        """
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflection_value', reflection_value)

    @property
    def repetition_method(self) -> XAiWorkApplication.RepetitionMethod:
        """Whether or how the movie repeats.
        """
        return XAiWorkApplication.RepetitionMethod(self.xa_elem.repetitionMethod())

    @repetition_method.setter
    def repetition_method(self, repetition_method: XAiWorkApplication.RepetitionMethod):
        self.set_property('repetitionMethod', repetition_method.value)

    @property
    def rotation(self) -> int:
        """The rotation of the movie, in degrees from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)




class XAiWorkTextItemList(XAiWorkiWorkItemList):
    """A wrapper around lists of text items that employs fast enumeration techniques.

    All properties of text items can be called as methods on the wrapped list, returning a list containing each text item's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkTextItem)
        logger.debug("Got list of text items")

    def background_fill_type(self) -> list[XAiWorkApplication.FillOption]:
        ls = self.xa_elem.arrayByApplyingSelector_("fileName")
        return [XAiWorkApplication.FillOption(x) for x in ls]

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

    def by_background_fill_type(self, background_fill_type: XAiWorkApplication.FillOption) -> 'XAiWorkTextItem':
        return self.by_property("backgroundFillType", background_fill_type.value)

    def by_text(self, text: Union[str, XABase.XAText]) -> 'XAiWorkTextItem':
        if isinstance(text, str):
            self.by_property('text', text)
        else:
            self.by_property('text', text.xa_elem)

    def by_opacity(self, opacity: int) -> 'XAiWorkTextItem':
        return self.by_property("opacity", opacity)

    def by_reflection_showing(self, reflection_showing: bool) -> 'XAiWorkTextItem':
        return self.by_property("reflectionShowing", reflection_showing)

    def by_reflection_value(self, reflection_value: int) -> 'XAiWorkTextItem':
        return self.by_property("reflectionValue", reflection_value)

    def by_rotation(self, rotation: int) -> 'XAiWorkTextItem':
        return self.by_property("rotation", rotation)

class XAiWorkTextItem(XAiWorkiWorkItem):
    """A class for managing and interacting with text items in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def background_fill_type(self) -> XAiWorkApplication.FillOption:
        """The background of the text item.
        """
        return XAiWorkApplication.FillOption(self.xa_elem.backgroundFillType())

    @property
    def text(self) -> XABase.XAText:
        """The text contained within the text item.
        """
        return self._new_element(self.xa_elem.text(), XABase.XAText)

    @text.setter
    def text(self, text: Union[str, XABase.XAText]):
        if isinstance(text, str):
            self.set_property('text', text)
        else:
            self.set_property('text', text.xa_elem)

    @property
    def opacity(self) -> int:
        """The opacity of the text item.
        """
        return self.xa_elem.opacity()

    @opacity.setter
    def opacity(self, opacity: int):
        self.set_property('opacity', opacity)

    @property
    def reflection_showing(self) -> bool:
        """Whether the text item displays a reflection.
        """
        return self.xa_elem.reflectionShowing()

    @reflection_showing.setter
    def reflection_showing(self, reflection_showing: bool):
        self.set_property('reflectionShowing', reflection_showing)

    @property
    def reflection_value(self) -> int:
        """The percentage of reflection of the text item, from 0 to 100.
        """
        return self.xa_elem.reflectionValue()

    @reflection_value.setter
    def reflection_value(self, reflection_value: int):
        self.set_property('reflectionValue', reflection_value)

    @property
    def rotation(self) -> int:
        """The rotation of the text item, in degrees from 0 to 359.
        """
        return self.xa_elem.rotation()

    @rotation.setter
    def rotation(self, rotation: int):
        self.set_property('rotation', rotation)




class XAiWorkTableList(XAiWorkiWorkItemList):
    """A wrapper around lists of shapes that employs fast enumeration techniques.

    All properties of shapes can be called as methods on the wrapped list, returning a list containing each shape's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkTable)

    def name(self) -> list[str]:
        """Gets the name of each table in the list.

        :return: A list of table names
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def row_count(self) -> list[int]:
        """Gets the row count of each table in the list.

        :return: A list of table row counts
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("rowCount"))

    def column_count(self) -> list[int]:
        """Gets the column count of each table in the list.

        :return: A list of table column counts
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("columnCount"))

    def header_row_count(self) -> list[int]:
        """Gets the header row count of each table in the list.

        :return: A list of table header row counts
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("headerRowCount"))

    def header_column_count(self) -> list[int]:
        """Gets the header column count of each table in the list.

        :return: A list of table header column counts
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("headerColumnCount"))

    def footer_row_count(self) -> list[int]:
        """Gets the footer row count of each table in the list.

        :return: A list of table footer row counts
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("footerRowCount"))

    def cell_range(self) -> 'XAiWorkRangeList':
        """Gets the total cell range of each table in the list.

        :return: A list of table cell ranges
        :rtype: XAiWorkRangeList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("cellRange")
        return self._new_element(ls, XAiWorkRangeList)

    def selection_range(self) -> 'XAiWorkRangeList':
        """Gets the selected cell range of each table in the list.

        :return: A list of selected table cell ranges
        :rtype: XAiWorkRangeList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selectionRange")
        return self._new_element(ls, XAiWorkRangeList)

    def by_name(self, name: str) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose name matches the given name, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("name", name)

    def by_row_count(self, row_count: int) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("rowCount", row_count)

    def by_column_count(self, column_count: int) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("columnCount", column_count)

    def by_header_row_count(self, header_row_count: int) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose header row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("headerRowCount", header_row_count)

    def by_header_column_count(self, header_column_count: int) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose header column count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("headerColumnCount", header_column_count)

    def by_footer_row_count(self, footer_row_count: int) -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose footer row count matches the given number, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("footerRowCount", footer_row_count)

    def by_cell_range(self, cell_range: 'XAiWorkRange') -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose cell range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("cellRange", cell_range.xa_elem)

    def by_selection_range(self, selection_range: 'XAiWorkRange') -> Union['XAiWorkTable', None]:
        """Retrieves the first table whose selection range matches the given range, if one exists.

        :return: The desired table, if it is found
        :rtype: Union[XAiWorkTable, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("selectionRange", selection_range.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAiWorkTable(XAiWorkiWorkItem):
    """A class for managing and interacting with tables in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)
    
    @property
    def name(self) -> str:
        """The name of the table.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def row_count(self) -> int:
        """The number of rows in the table.
        """
        return self.xa_elem.rowCount()

    @row_count.setter
    def row_count(self, row_count: int):
        self.set_property('rowCount', row_count)

    @property
    def column_count(self) -> int:
        """The number of columns in the table.
        """
        return self.xa_elem.columnCount()

    @column_count.setter
    def column_count(self, column_count: int):
        self.set_property('columnCount', column_count)

    @property
    def header_row_count(self) -> int:
        """The number of header rows in the table.
        """
        return self.xa_elem.headerRowCount()

    @header_row_count.setter
    def header_row_count(self, header_row_count: int):
        self.set_property('headerRowCount', header_row_count)

    @property
    def header_column_count(self) -> int:
        """The number of header columns in the table.
        """
        return self.xa_elem.headerColumnCount()

    @header_column_count.setter
    def header_column_count(self, header_column_count: int):
        self.set_property('headerColumnCount', header_column_count)

    @property
    def footer_row_count(self) -> int:
        """The number of footer rows in the table.
        """
        return self.xa_elem.footerRowCount()

    @footer_row_count.setter
    def footer_row_count(self, footer_row_count: int):
        self.set_property('footerRowCount', footer_row_count)

    @property
    def cell_range(self) -> 'XAiWorkRange':
        """The range of all cells in the table.
        """
        return self._new_element(self.xa_elem.cellRange(), XAiWorkRange)

    @property
    def selection_range(self) -> 'XAiWorkRange':
        """The currently selected cells.
        """
        return self._new_element(self.xa_elem.selectionRange(), XAiWorkRange)

    @selection_range.setter
    def selection_range(self, selection_range: 'XAiWorkRange'):
        self.set_property('selectionRange', selection_range.xa_elem)

    def sort(self, by_column: 'XAiWorkColumn', in_rows: Union[list['XAiWorkRow'], 'XAiWorkRowList', None] = None, direction: XAiWorkApplication.SortDirection = XAiWorkApplication.SortDirection.ASCENDING) -> Self:
        """Sorts the table according to the specified column, in the specified sorting direction.

        :param by_column: The column to sort by
        :type by_column: XAiWorkColumn
        :param in_rows: The rows to sort, or None to sort the whole table, defaults to None
        :type in_rows: Union[list[XAiWorkRow], XAiWorkRowList, None], optional
        :param direction: The direction to sort in, defaults to XAiWorkApplication.SortDirection.ASCENDING
        :type direction: XAiWorkApplication.SortDirection, optional
        :return: The table object
        :rtype: Self

        .. versionadded:: 0.1.1
        """
        if isinstance(in_rows, list):
            in_rows = [row.xa_elem for row in in_rows]
        elif isinstance(in_rows, XABase.XAList):
            in_rows = in_rows.xa_elem

        self.xa_elem.sortBy_direction_inRows_(by_column.xa_elem, direction.value, in_rows)
        return self

    def cells(self, filter: Union[dict, None] = None) -> 'XAiWorkCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAiWorkCellList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.cells(), XAiWorkCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAiWorkColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAiWorkColumnList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.columns(), XAiWorkColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAiWorkRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAiWorkRowList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.rows(), XAiWorkRowList, filter)

    def ranges(self, filter: Union[dict, None] = None) -> 'XAiWorkRangeList':
        """Returns a list of ranges, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned ranges will have, or None
        :type filter: Union[dict, None]
        :return: The list of ranges
        :rtype: XAiWorkRangeList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.ranges(), XAiWorkRangeList, filter)

    def __repr__(self):
        try:
            return "<" + str(type(self)) + str(self.name) + ">"
        except AttributeError:
            # Probably dealing with a proxy object created via make()
            return "<" + str(type(self)) + str(self.xa_elem) + ">"




class XAiWorkRangeList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAiWorkRange
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each range in the list.

        :return: A list of range properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "background_color": XABase.XAColor(raw_dict["backgroundColor"]) if raw_dict["backgroundColor"] is not None else None,
                "font_size": raw_dict["fontSize"],
                "name": raw_dict["name"],
                "format": XAiWorkApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
                "vertical_alignment": XAiWorkApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
                "font_name": raw_dict["fontName"],
                "alignment": XAiWorkApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
                "text_wrap": raw_dict["textWrap"],
                "text_color": XABase.XAColor(raw_dict["textColor"]),
            }
        return pyxa_dicts

    def font_name(self) -> list[str]:
        """Gets the font name of each range in the list.

        :return: A list of range font names
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontName"))

    def font_size(self) -> list[float]:
        """Gets the font size of each range in the list.

        :return: A list of range font sizes
        :rtype: list[float]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize"))

    def format(self) -> list[XAiWorkApplication.CellFormat]:
        """Gets the cell format of each range in the list.

        :return: A list of range cell formats
        :rtype: list[XAiWorkApplication.CellFormat]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAiWorkApplication.CellFormat(x) for x in ls]

    def alignment(self) -> list[XAiWorkApplication.Alignment]:
        """Gets the alignment setting of each range in the list.

        :return: A list of range alignment settings
        :rtype: list[XAiWorkApplication.Alignment]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("alignment")
        return [XAiWorkApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def text_color(self) -> list[XABase.XAColor]:
        """Gets the text color of each range in the list.

        :return: A list of range text colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textColor")
        return [XABase.XAColor(x) for x in ls]

    def text_wrap(self) -> list[bool]:
        """Gets the text wrap setting of each range in the list.

        :return: A list of range text wrap settings
        :rtype: list[bool]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("textWrap"))

    def background_color(self) -> list[XABase.XAColor]:
        """Gets the background color of each range in the list.

        :return: A list of range background colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor")
        return [XABase.XAColor(x) for x in ls]

    def vertical_alignment(self) -> list[XAiWorkApplication.Alignment]:
        """Gets the vertical alignment setting of each range in the list.

        :return: A list of range vertical alignment settings
        :rtype: list[XAiWorkApplication.Alignment]
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("verticalAlignment")
        return [XAiWorkApplication.Alignment(XABase.OSType(x.stringValue())) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
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
                return self._new_element(page_range, XAiWorkRange)

    def by_font_name(self, font_name: str) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose font name matches the given font name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: float) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose font size matches the given font size, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("fontSize", font_size)

    def by_format(self, format: XAiWorkApplication.CellFormat) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose cell format matches the given format, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("format", format.value)

    def by_alignment(self, alignment: XAiWorkApplication.Alignment) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        for page_range in self.xa_elem:
            if page_range.alignment() == alignment.value:
                return self._new_element(page_range, XAiWorkRange)

    def by_name(self, name: str) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose name matches the given name, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("name", name)

    def by_text_color(self, text_color: XABase.XAColor) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose text color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("textColor", text_color.xa_elem)

    def by_text_wrap(self, text_wrap: bool) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose text wrap setting matches the given boolean value, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("textWrap", text_wrap)

    def by_background_color(self, background_color: XABase.XAColor) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose background color matches the given color, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("backgroundColor", background_color.xa_elem)

    def by_vertical_alignment(self, vertical_alignment: XAiWorkApplication.Alignment) -> Union['XAiWorkRange', None]:
        """Retrieves the first range whose vertical alignment setting matches the given alignment, if one exists.

        :return: The desired range, if it is found
        :rtype: Union[XAiWorkRange, None]
        
        .. versionadded:: 0.1.1
        """
        for page_range in self.xa_elem:
            if page_range.verticalAlignment() == vertical_alignment.value:
                return self._new_element(page_range, XAiWorkRange)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAiWorkRange(XABase.XAObject):
    """A class for managing and interacting with ranges of table cells in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the range.
        """
        raw_dict = self.xa_elem.properties()
        return {
            "background_color": XABase.XAColor(raw_dict["backgroundColor"]),
            "font_size": raw_dict["fontSize"],
            "name": raw_dict["name"],
            "format": XAiWorkApplication.CellFormat(XABase.OSType(raw_dict["format"].stringValue())),
            "vertical_alignment": XAiWorkApplication.Alignment(XABase.OSType(raw_dict["verticalAlignment"].stringValue())),
            "font_name": raw_dict["fontName"],
            "alignment": XAiWorkApplication.Alignment(XABase.OSType(raw_dict["alignment"].stringValue())),
            "text_wrap": raw_dict["textWrap"],
            "text_color": XABase.XAColor(raw_dict["textColor"])
        }

    @property
    def font_name(self) -> str:
        """The font of the range's cells.
        """
        return self.xa_elem.fontName()

    @font_name.setter
    def font_name(self, font_name: str):
        self.set_property('fontName', font_name)

    @property
    def font_size(self) -> float:
        """The font size of the range's cells.
        """
        return self.xa_elem.fontSize()

    @font_size.setter
    def font_size(self, font_size: float):
        self.set_property('fontSize', font_size)

    @property
    def format(self) -> XAiWorkApplication.CellFormat:
        """The format of the range's cells.
        """
        return XAiWorkApplication.CellFormat(self.xa_elem.format())

    @format.setter
    def format(self, format: XAiWorkApplication.CellFormat):
        self.set_property('format', format.value)

    @property
    def alignment(self) -> XAiWorkApplication.Alignment:
        """The horizontal alignment of content within the range's cells.
        """
        return XAiWorkApplication.Alignment(self.xa_elem.alignment())

    @alignment.setter
    def alignment(self, alignment: XAiWorkApplication.Alignment):
        self.set_property('alignment', alignment.value)

    @property
    def name(self) -> str:
        """The range's coordinates.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def text_color(self) -> XABase.XAColor:
        """The text color of the range's cells.
        """
        return XABase.XAColor(self.xa_elem.textColor())

    @text_color.setter
    def text_color(self, text_color: XABase.XAColor):
        self.set_property('textColor', text_color.xa_elem)

    @property
    def text_wrap(self) -> bool:
        """Whether text within the range's cell should wrap.
        """
        return self.xa_elem.textWrap()

    @text_wrap.setter
    def text_wrap(self, text_wrap: bool):
        self.set_property('textWrap', text_wrap)

    @property
    def background_color(self) -> XABase.XAColor:
        """The background color of the range's cells.
        """
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property('backgroundColor', background_color.xa_elem)

    @property
    def vertical_alignment(self) -> XAiWorkApplication.Alignment:
        """The vertical alignment of content in the range's cells.
        """
        return XAiWorkApplication.Alignment(self.xa_elem.verticalAlignment())

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment: XAiWorkApplication.Alignment):
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

        .. versionadded:: 0.1.1
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

        .. versionadded:: 0.1.1
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

        .. versionadded:: 0.1.1
        """
        self.xa_elem.unmerge()
        return self

    def cells(self, filter: Union[dict, None] = None) -> 'XAiWorkCellList':
        """Returns a list of cells, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned cells will have, or None
        :type filter: Union[dict, None]
        :return: The list of cells
        :rtype: XAiWorkCellList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.cells(), XAiWorkCellList, filter)

    def columns(self, filter: Union[dict, None] = None) -> 'XAiWorkColumnList':
        """Returns a list of columns, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned columns will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XAiWorkColumnList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.columns(), XAiWorkColumnList, filter)

    def rows(self, filter: Union[dict, None] = None) -> 'XAiWorkRowList':
        """Returns a list of rows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned rows will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XAiWorkRowList

        .. versionadded:: 0.1.1
        """
        return self._new_element(self.xa_elem.rows(), XAiWorkRowList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAiWorkRowList(XAiWorkRangeList):
    """A wrapper around lists of rows that employs fast enumeration techniques.

    All properties of rows can be called as methods on the wrapped list, returning a list containing each row's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkRow)
        logger.debug("Got list of table rows")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each row in the list.

        :return: A list of row properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
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
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def height(self) -> list[int]:
        """Gets the height of each row in the list.

        :return: A list of row heights
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def by_properties(self, properties: dict) -> Union['XAiWorkRow', None]:
        """Retrieves the first row whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAiWorkRow, None]
        
        .. versionadded:: 0.1.1
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
                return self._new_element(page_range, XAiWorkRow)

    def by_address(self, address: float) -> Union['XAiWorkRow', None]:
        """Retrieves the first row whose address matches the given address, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAiWorkRow, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("address", address)

    def by_height(self, height: int) -> Union['XAiWorkRow', None]:
        """Retrieves the first row whose height matches the given height, if one exists.

        :return: The desired row, if it is found
        :rtype: Union[XAiWorkRow, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("height", height)

class XAiWorkRow(XAiWorkRange):
    """A class for managing and interacting with table rows in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the row.
        """
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["address"] = raw_dict["address"]
        properties["height"] = raw_dict["height"]
        return properties

    @property
    def address(self) -> int:
        """The index of the row in the table.
        """
        return self.xa_elem.address()

    @property
    def height(self) -> float:
        """The height of the row in pixels.
        """
        return self.xa_elem.height()

    @height.setter
    def height(self, height: float):
        self.set_property('height', height)




class XAiWorkColumnList(XAiWorkRangeList):
    """A wrapper around lists of columns that employs fast enumeration techniques.

    All properties of columns can be called as methods on the wrapped list, returning a list containing each column's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkColumn)
        logger.debug("Got list of table columns")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each column in the list.

        :return: A list of column properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
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
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("address"))

    def width(self) -> list[int]:
        """Gets the width of each column in the list.

        :return: A list of column widths
        :rtype: list[int]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def by_properties(self, properties: dict) -> Union['XAiWorkColumn', None]:
        """Retrieves the first column whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAiWorkColumn, None]
        
        .. versionadded:: 0.1.1
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
                return self._new_element(page_range, XAiWorkColumn)

    def by_address(self, address: float) -> Union['XAiWorkColumn', None]:
        """Retrieves the first column whose address matches the given address, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAiWorkColumn, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("address", address)

    def by_width(self, width: int) -> Union['XAiWorkColumn', None]:
        """Retrieves the first column whose width matches the given width, if one exists.

        :return: The desired column, if it is found
        :rtype: Union[XAiWorkColumn, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("width", width)

class XAiWorkColumn(XAiWorkRange):
    """A class for managing and interacting with table columns in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the column.
        """
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["address"] = raw_dict["address"]
        properties["width"] = raw_dict["width"]
        return properties

    @property
    def address(self) -> int:
        """The index of the column in the table.
        """
        return self.xa_elem.address()

    @property
    def width(self) -> float:
        """The width of the column in pixels.
        """
        return self.xa_elem.width()

    @width.setter
    def width(self, width: float):
        self.set_property('width', width)




class XAiWorkCellList(XAiWorkRangeList):
    """A wrapper around lists of cells that employs fast enumeration techniques.

    All properties of cells can be called as methods on the wrapped list, returning a list containing each cell's value for the property.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAiWorkCell)
        logger.debug("Got list of table cells")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each cell in the list.

        :return: A list of cell properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.1
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = super().properties()
        for index, raw_dict in enumerate(raw_dicts):
            properties = pyxa_dicts[index]
            properties["formatted_value"] = raw_dict["formattedValue"]
            properties["formula"] = raw_dict["formula"]
            properties["value"] = raw_dict["value"]
            properties["column"] = self._new_element(raw_dict["column"], XAiWorkColumn)
            properties["row"] = self._new_element(raw_dict["row"], XAiWorkRow)
        return pyxa_dicts

    def formatted_value(self) -> list[str]:
        """Gets the formatted value of each cell in the list.

        :return: A list of cell formatted values
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("formattedValue"))

    def formula(self) -> list[str]:
        """Gets the formula of each cell in the list.

        :return: A list of cell formulae
        :rtype: list[str]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("formula"))

    def value(self) -> list[Any]:
        """Gets the value of each cell in the list.

        :return: A list of cell values
        :rtype: list[Any]
        
        .. versionadded:: 0.1.1
        """
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def column(self) -> XAiWorkColumnList:
        """Gets the column of each cell in the list.

        :return: A list of cell columns
        :rtype: XAiWorkColumnList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("column")
        return self._new_element(ls, XAiWorkColumnList)

    def row(self) -> XAiWorkRowList:
        """Gets the row of each cell in the list.

        :return: A list of cell rows
        :rtype: XAiWorkRowList
        
        .. versionadded:: 0.1.1
        """
        ls = self.xa_elem.arrayByApplyingSelector_("row")
        return self._new_element(ls, XAiWorkRowList)

    def by_properties(self, properties: dict) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
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
                return self._new_element(page_range, XAiWorkCell)

    def by_formatted_value(self, formatted_value: str) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose formatted value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("formattedValue", formatted_value)

    def by_formula(self, formula: str) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose formula matches the given formula, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("formula", formula)

    def by_value(self, value: Any) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose value matches the given value, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("value", value)

    def by_column(self, column: XAiWorkColumn) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose column matches the given column, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("column", column.xa_elem)

    def by_row(self, row: XAiWorkRow) -> Union['XAiWorkCell', None]:
        """Retrieves the first cell whose row matches the given row, if one exists.

        :return: The desired cell, if it is found
        :rtype: Union[XAiWorkCell, None]
        
        .. versionadded:: 0.1.1
        """
        return self.by_property("row", row.xa_elem)

class XAiWorkCell(XAiWorkRange):
    """A class for managing and interacting with table cells in Keynote.

    .. versionadded:: 0.1.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the cell.
        """
        raw_dict = self.xa_elem.properties()
        properties = super().properties
        properties["formatted_value"] = raw_dict["formattedValue"]
        properties["formula"] = raw_dict["formula"]
        properties["value"] = raw_dict["value"]
        properties["column"] = self._new_element(raw_dict["column"], XAiWorkColumn)
        properties["row"] = self._new_element(raw_dict["row"], XAiWorkRow)
        return properties

    @property
    def formatted_value(self) -> str:
        """The formatted form of the value stored in the cell.
        """
        return self.xa_elem.formattedValue()

    @property
    def formula(self) -> str:
        """The formula in the cell as text.
        """
        return self.xa_elem.formula()

    @property
    def value(self) -> Union[int, float, datetime, str, bool, None]:
        """The value stored in the cell.
        """
        return self.xa_elem.value().get()

    @value.setter
    def value(self, value: Union[int, float, datetime, str, bool, None]):
        self.set_property('value', value)

    @property
    def column(self) -> XAiWorkColumn:
        """The cell's column.
        """
        return self._new_element(self.xa_elem.column(), XAiWorkColumn)

    @property
    def row(self) -> XAiWorkRow:
        """The cell's row.
        """
        return self._new_element(self.xa_elem.row(), XAiWorkRow)