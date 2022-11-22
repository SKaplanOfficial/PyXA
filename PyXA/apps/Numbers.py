""".. versionadded:: 0.0.8

Control the macOS Numbers application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, Union, Self

import AppKit
import logging

from PyXA import XABase
from PyXA.XABase import OSType

from . import iWorkApplicationBase

logger = logging.getLogger("numbers")

class XANumbersApplication(iWorkApplicationBase.XAiWorkApplication):
    """A class for managing and interacting with Numbers.app.

    .. seealso:: :class:`XANumbersWindow`, :class:`XANumbersDocument`

    .. versionadded:: 0.0.8
    """
    class ExportFormat(Enum):
        """Options for what format to export a Numbers project as.
        """
        NUMBERS                 = OSType('Nuff') #: The Numbers native file format 
        PDF                     = OSType('Npdf') #: PDF format
        MICROSOFT_EXCEL         = OSType('Nexl') #: Excel format
        CSV                     = OSType('Ncsv') #: CSV format
        NUMBERS_09              = OSType('Nnmb') #: Numbers 2009 format

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XANumbersWindow

    def new_sheet(self, document: 'XANumbersDocument', properties: dict = None) -> 'XANumbersSheet':
        """Creates a new sheet with the specified properties in the given document.

        :param document: The document to create the new sheet in
        :type document: XANumbersDocument
        :param properties: The properties to initialize the new sheet with, defaults to None
        :type properties: dict, optional
        :return: The newly created sheet object
        :rtype: XANumbersSheet

        .. versionadded:: 0.0.8
        """
        if properties is None:
            properties = {}

        new_sheet = self.make("sheet", properties)
        return self.current_document.sheets().push(new_sheet)

    def documents(self, filter: Union[dict, None] = None) -> 'XANumbersDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XANumbersDocumentList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.documents(), XANumbersDocumentList, filter)

    def new_document(self, file_path: Union[str, XABase.XAPath] = "./Untitled.numbers", template: 'XANumbersSheet' = None) -> 'XANumbersDocument':
        """Creates a new document at the specified path and with the specified template.

        :param file_path: The path to create the document at, defaults to "./Untitled.key"
        :type file_path: str, optional
        :param template: The template to initialize the document with, defaults to None
        :type template: XANumbersSheet, optional
        :return: The newly created document object
        :rtype: XANumbersDocument

        .. versionadded:: 0.0.8
        """
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)

        properties = {
            "file": file_path.xa_elem,
        }

        if template is not None:
            properties["documentTemplate"] = template.xa_elem

        new_document = self.make("document", properties)
        return self.documents().push(new_document)

    def templates(self, filter: Union[dict, None] = None) -> 'XANumbersTemplateList':
        """Returns a list of templates, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned templates will have, or None
        :type filter: Union[dict, None]
        :return: The list of templates
        :rtype: XANumbersTemplateList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.templates(), XANumbersTemplateList, filter)

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
        >>> Numbers = PyXA.Application("Numbers")
        >>> new_doc = Numbers.make("document", {"bodyText": "This is a whole new document!"})
        >>> Numbers.documents().push(new_doc)

        :Example 3: Making new elements on a page

        >>> import PyXA
        >>> Numbers = PyXA.Application("Numbers")
        >>> new_line = Numbers.make("line", {"startPoint": (100, 100), "endPoint": (200, 200)})
        >>> Numbers.documents()[0].sheets()[0].lines().push(new_line)

        .. versionadded:: 0.0.8
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XANumbersDocument)
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
        elif specifier == "sheet":
            return self._new_element(obj, XANumbersSheet)
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




class XANumbersWindow(iWorkApplicationBase.XAiWorkWindow):
    """A window of Numbers.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> 'XANumbersDocument':
        """The document currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XANumbersDocument)




class XANumbersDocumentList(iWorkApplicationBase.XAiWorkDocumentList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersDocument)
        logger.debug("Got list of documents")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, document in enumerate(self):
            pyxa_dicts[index] = {
                "name": document.name,
                "modified": document.modified,
                "file": document.file,
                "id": document.id,
                "document_template": document.document_template,
                "active_sheet": document.active_sheet,
                "selection": document.selection,
                "password_protected": document.password_protected
            }
        return pyxa_dicts

    def document_template(self) -> 'XANumbersTemplateList':
        """Gets the document template of each document in the list.

        :return: A list of templates used by the documents of the list
        :rtype: XANumbersTemplateList
        
        .. versionadded:: 0.0.8
        """
        ls = self.xa_elem.arrayByApplyingSelector_("documentTemplate")
        return self._new_element(ls, XANumbersTemplateList)

    def active_sheet(self) -> 'XANumbersSheetList':
        """Gets the active sheet of each document in the list.

        :return: A list of active sheets in documents of the list
        :rtype: XANumbersSheetList
        
        .. versionadded:: 0.0.8
        """
        ls = self.xa_elem.arrayByApplyingSelector_("activeSheet")
        return self._new_element(ls, XANumbersSheetList)

    def by_properties(self, properties: dict) -> Union['XANumbersDocument', None]:
        """Retrieves the first document whose properties dictionary matches the given properties, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XANumbersDocument, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "id" in properties:
            raw_dict["id"] = properties["id"]

        if "active_sheet" in properties:
            raw_dict["activeSheet"] = properties["active_sheet"].xa_elem

        if "file" in properties:
            if isinstance(properties["file"], str):
                raw_dict["file"] = properties["file"]
            else:
                raw_dict["file"] = properties["file"].xa_elem

        if "modified" in properties:
            raw_dict["modified"] = properties["modified"]

        if "document_template" in properties:
            raw_dict["documentTemplate"] = properties["document_template".xa_elem]

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
                return self._new_element(document, XANumbersDocument)

    def by_document_template(self, document_template: 'XANumbersTemplate') -> Union['XANumbersDocument', None]:
        """Retrieves the first document whose template matches the given template, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XANumbersDocument, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("documentTemplate", document_template.xa_elem)

    def by_active_sheet(self, active_sheet: 'XANumbersSheet') -> Union['XANumbersDocument', None]:
        """Retrieves the first document whose active sheet matches the given sheet, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XANumbersDocument, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("activeSheet", active_sheet.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XANumbersDocument(iWorkApplicationBase.XAiWorkDocument):
    """A class for managing and interacting with Numbers documents.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document.
        """
        return {
            "name": self.name,
            "modified": self.modified,
            "file": self.file,
            "id": self.id,
            "document_template": self.document_template,
            "active_sheet": self.active_sheet,
            "selection": self.selection,
            "password_protected": self.password_protected
        }

    @property
    def document_template(self) -> 'XANumbersTemplate':
        """The template assigned to the document.
        """
        return self._new_element(self.xa_elem.documentTemplate(), XANumbersTemplate)

    @property
    def active_sheet(self) -> 'XANumbersSheet':
        """The active sheet of the document.
        """
        return self._new_element(self.xa_elem.activeSheet(), XANumbersSheet)

    @active_sheet.setter
    def active_sheet(self, active_sheet: 'XANumbersSheet'):
        self.set_property('activeSheet', active_sheet.xa_elem)

    def save(self):
        """Saves the Numbers document.
        
        .. versionadded:: 0.1.1
        """
        export_format = XANumbersApplication.ExportFormat.NUMBERS.value
        self.xa_elem.saveIn_as_(self.file, export_format)

    def export(self, file_path: Union[str, AppKit.NSURL] = None, format: XANumbersApplication.ExportFormat = XANumbersApplication.ExportFormat.PDF):
        """Exports the document in the specified format.

        :param file_path: The path to save the exported file at, defaults to None
        :type file_path: Union[str, AppKit.NSURL], optional
        :param format: The format to export the file in, defaults to XANumbersApplication.ExportFormat.PDF
        :type format: XANumbersApplication.ExportFormat, optional

        .. versionadded:: 0.0.8
        """
        if file_path is None:
            file_path = self.file.path()[:-4] + ".pdf"
        if isinstance(file_path, str):
            file_path = XABase.XAPath(file_path)
        self.xa_elem.exportTo_as_withProperties_(file_path.xa_elem, format.value, None)

    def new_sheet(self, properties: dict = None) -> 'XANumbersSheet':
        """Creates a new sheet at the end of the document.

        :param properties: The properties to give the new page
        :type properties: dict
        :return: A reference to the newly created sheet object
        :rtype: XANumbersSheet

        .. versionadded:: 0.0.8
        """
        return self.xa_prnt.xa_prnt.new_sheet(self, properties)

    def sheets(self, filter: Union[dict, None] = None) -> 'XANumbersSheetList':
        """Returns a list of sheets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned sheets will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XANumbersSheetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.sheets(), XANumbersSheetList, filter)




class XANumbersTemplateList(XABase.XAList):
    """A wrapper around lists of templates that employs fast enumeration techniques.

    All properties of templates can be called as methods on the wrapped list, returning a list containing each template's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANumbersTemplate, filter)
        logger.debug("Got list of templates")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each template in the list.

        :return: A list of template properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "id": raw_dict["id"],
                "name": raw_dict["name"],
            }
        return pyxa_dicts

    def id(self) -> list[str]:
        """Gets the ID of each template in the list.

        :return: A list of template IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        """Gets the name of each template in the list.

        :return: A list of template names
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_properties(self, properties: dict) -> Union['XANumbersTemplate', None]:
        """Retrieves the first template whose properties dictionary matches the given properties, if one exists.

        :return: The desired template, if it is found
        :rtype: Union[XANumbersTemplate, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "id" in properties:
            raw_dict["id"] = properties["id"]

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        for template in self.xa_elem:
            if all(raw_dict[x] == template.properties()[x] for x in raw_dict):
                return self._new_element(template, XANumbersTemplate)

    def by_id(self, id: str) -> Union['XANumbersTemplate', None]:
        """Retrieves the first template whose ID matches the given ID, if one exists.

        :return: The desired template, if it is found
        :rtype: Union[XANumbersTemplate, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XANumbersTemplate', None]:
        """Retrieves the first template whose name matches the given name, if one exists.

        :return: The desired template, if it is found
        :rtype: Union[XANumbersTemplate, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("name", name)

    def __repr__(self):
        return f"<{str(type(self))}{self.name()}>"

class XANumbersTemplate(XABase.XAObject):
    """A class for managing and interacting with Numbers templates.

    .. seealso:: :class:`XANumbersApplication`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the template.
        """
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The localized name of the template.
        """
        return self.xa_elem.name()

    def __repr__(self):
        return f"<{str(type(self))}{self.name}>"




class XANumbersContainerList(iWorkApplicationBase.XAiWorkContainerList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XANumbersContainer
        self._xa_ccls = XANumbersSheetList
        super().__init__(properties, filter, obj_class)
        logger.debug("Got list of containers")

class XANumbersContainer(iWorkApplicationBase.XAiWorkContainer):
    """A class for managing and interacting with containers in Numbers.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        self._xa_ccls = XANumbersSheetList
        super().__init__(properties)




class XANumbersSheetList(XANumbersContainerList):
    """A wrapper around lists of Numbers sheets that employs fast enumeration techniques.

    All properties of Numbers sheets can be called as methods on the wrapped list, returning a list containing each sheet's value for the property.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XANumbersSheet)
        logger.debug("Got list of sheets")

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each sheet in the list.

        :return: A list of sheet properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.1.0
        """
        raw_dicts = self.xa_elem.arrayByApplyingSelector_("properties")
        pyxa_dicts = [None] * len(self.xa_elem)
        for index, raw_dict in enumerate(raw_dicts):
            pyxa_dicts[index] = {
                "name": raw_dict["name"]
            }
        return pyxa_dicts

    def body_text(self) -> XABase.XATextList:
        """Gets the body text of each sheet in the list.

        :return: A list of sheet body texts
        :rtype: XABase.XATextList
        
        .. versionadded:: 0.0.8
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bodyText")
        return self._new_element(ls, XABase.XATextList)

    def by_properties(self, properties: dict) -> Union['XANumbersSheet', None]:
        """Retrieves the first sheet whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired sheet, if it is found
        :rtype: Union[XANumbersSheet, None]
        
        .. versionadded:: 0.1.0
        """
        raw_dict = {}

        if "name" in properties:
            raw_dict["name"] = properties["name"]

        for sheet in self.xa_elem:
            if all([raw_dict[x] == sheet.properties()[x] for x in raw_dict]):
                return self._new_element(sheet, XANumbersSheet)

    def by_body_text(self, body_text: Union[str, XABase.XAText]) -> Union['XANumbersSheet', None]:
        """Retrieves the first sheet whose body text matches the given text, if one exists.

        :return: The desired sheet, if it is found
        :rtype: Union[XANumbersSheet, None]
        
        .. versionadded:: 0.0.8
        """
        if isinstance(body_text, str):
            self.by_property('bodyText', body_text)
        else:
            self.by_property('bodyText', body_text.xa_elem)

class XANumbersSheet(XANumbersContainer):
    """A class for managing and interacting with Numbers in Numbers documents.

    .. seealso:: :class:`XANumbersApplication`, :class:`XANumbersiWorkItem`

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the sheet.
        """
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "name": raw_dict["name"]
        }
        return pyxa_dict

    @property
    def name(self) -> str:
        """The name of the sheet.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    # def duplicate(self) -> 'XANumbersPage':
    #     """Duplicates the page, mimicking the action of copying and pasting the page manually.

    #     :return: A reference to the PyXA page object that called this command.
    #     :rtype: XANumbersPage

    #     .. versionadded:: 0.0.8
    #     """
    #     new_page = self.xa_prnt.xa_prnt.xa_prnt.xa_prnt.make("page", {})
    #     self.xa_prnt.xa_prnt.sheets().push(new_page)
    #     for item in self.xa_elem.lines():
    #         print("ya")
    #         item.duplicateTo_withProperties_(new_page.xa_elem.lines()[0].positionAfter(), None)
    #     return self

    # def move_to(self, document):
    #     self.xa_elem.moveTo_(document.xa_elem.sheets())

    # def delete(self):
    #     """Deletes the page.

    #     .. versionadded:: 0.0.8
    #     """
    #     self.xa_elem.get().delete()

    def add_image(self, file_path: Union[str, XABase.XAPath, XABase.XAImage]) -> 'iWorkApplicationBase.XAiWorkImage':
        """Adds the image at the specified path to the page.

        :param file_path: The path to the image file
        :type file_path: Union[str, XABase.XAPath, XABase.XAImage]
        :return: The newly created image object
        :rtype: iWorkApplicationBase.XAiWorkImage

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

    # def add_chart(self, row_names: list[str], column_names: list[str], data: list[list[Any]], type: int = XANumbersApplication.ChartType.LINE_2D.value, group_by: int = XANumbersApplication.ChartGrouping.ROW.value) -> 'XANumbersChart':
    #     """_summary_

    #     _extended_summary_

    #     :param row_names: A list of row names.
    #     :type row_names: list[str]
    #     :param column_names: A list of column names.
    #     :type column_names: list[str]
    #     :param data: A 2d array 
    #     :type data: list[list[Any]]
    #     :param type: The chart type, defaults to _NumbersLegacyChartType.NumbersLegacyChartTypeLine_2d.value
    #     :type type: int, optional
    #     :param group_by: The grouping schema, defaults to _NumbersLegacyChartGrouping.NumbersLegacyChartGroupingChartRow.value
    #     :type group_by: int, optional
    #     :return: A reference to the newly created chart object.
    #     :rtype: XANumbersChart

    #     .. versionadded:: 0.0.8
    #     """
    #     self.xa_prnt.set_property("currentSlide", self.xa_elem)
    #     self.xa_elem.addChartRowNames_columnNames_data_type_groupBy_(row_names, column_names, data, type, group_by)
    #     chart = self.xa_elem.charts()[-1].get()
    #     properties = {
    #         "parent": self,
    #         "element": chart,
    #         "appref": self.xa_aref,
    #         "system_events": self.xa_sevt,
    #     }
    #     return XANumbersChart(properties)