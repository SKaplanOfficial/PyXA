""".. versionadded:: 0.0.6

Control the macOS Pages application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, Union, Self

import AppKit, ScriptingBridge
import logging

from PyXA import XABase
from PyXA.XABase import OSType
from . import iWorkApplicationBase

logger = logging.getLogger("pages")

class XAPagesApplication(iWorkApplicationBase.XAiWorkApplication):
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

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAPagesWindow

    def documents(self, filter: Union[dict, None] = None) -> 'XAPagesDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAPagesDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XAPagesDocumentList, filter)

    def new_document(self, file_path: Union[str, XABase.XAPath] = "./Untitled.pages", template: 'XAPagesTemplate' = None) -> 'XAPagesDocument':
        """Creates a new document at the specified path and with the specified template.

        :param file_path: The path to create the document at, defaults to "./Untitled.key"
        :type file_path: str, optional
        :param template: The template to initialize the document with, defaults to None
        :type template: XAPagesPage, optional
        :return: The newly created document object
        :rtype: XAPagesDocument

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
            return self._new_element(obj, iWorkApplicationBase.XAiWorkShape)
        elif specifier == "table":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkTable)
        elif specifier == "audioClip":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkAudioClip)
        elif specifier == "chart":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkChart)
        elif specifier == "image":
            return self._new_element(obj, iWorkApplicationBase.XAiWorkImage)
        elif specifier == "page":
            return self._new_element(obj, XAPagesPage)
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




class XAPagesWindow(iWorkApplicationBase.XAiWorkWindow):
    """A class for managing and interacting with windows in Pages.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> 'XAPagesDocument':
        """The document currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XAPagesDocument)




class XAPagesDocumentList(iWorkApplicationBase.XAiWorkDocumentList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesDocument)

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
                "selection": self._new_element(raw_dicts[index]["selection"], iWorkApplicationBase.XAiWorkiWorkItemList),
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

    def audio_clips(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkAudioClipList':
        """Returns the audio clips of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's audio clips
        :rtype: iWorkApplicationBase.XAiWorkAudioClipList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("audioClips")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkChartList':
        """Returns the charts of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's charts
        :rtype: iWorkApplicationBase.XAiWorkChartList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("charts")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkGroupList':
        """Returns the groups of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's groups
        :rtype: iWorkApplicationBase.XAiWorkGroupList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("groups")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkImageList':
        """Returns the images of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's images
        :rtype: iWorkApplicationBase.XAiWorkImageList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("images")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkiWorkItemList':
        """Returns the iWork items of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's iWork items
        :rtype: iWorkApplicationBase.XAiWorkiWorkItemList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("iWorkItems")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkLineList':
        """Returns the lines of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's lines
        :rtype: iWorkApplicationBase.XAiWorkLineList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("lines")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkMovieList':
        """Returns the movies of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's movies
        :rtype: iWorkApplicationBase.XAiWorkMovieList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("movies")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkMovieList, filter)

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

    def shapes(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkShapeList':
        """Returns the shapes of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's shapes
        :rtype: iWorkApplicationBase.XAiWorkShapeList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("shapes")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTableList':
        """Returns the tables of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's tables
        :rtype: iWorkApplicationBase.XAiWorkTableList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("tables")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTextItemList':
        """Returns the text items of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's text items
        :rtype: iWorkApplicationBase.XAiWorkTextItemList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("textItems")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkTableList, filter)

    def placeholder_texts(self, filter: Union[dict, None] = None) -> 'XAPagesPlaceholderTextList':
        """Returns the placeholder texts of each document in the list.

        :param filter: A dictionary specifying property-value pairs that all returned placeholder texts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every document's placeholder texts
        :rtype: XAPagesPlaceholderTextList

        .. versionadded:: 0.1.0
        """
        ls = [x for x in self.xa_elem.arrayByApplyingSelector_("placeholderTexts")]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkTableList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPagesDocument(iWorkApplicationBase.XAiWorkDocument):
    """A class for managing and interacting with Pages documents.

    .. seealso:: :class:`XAPagesApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document.
        """
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
                "selection": self._new_element(raw_dict["selection"], iWorkApplicationBase.XAiWorkiWorkItemList),
                "name": raw_dict["name"],
                "password_protected": raw_dict["passwordProtected"]
        }
        return pyxa_dict

    @property
    def document_template(self) -> 'XAPagesTemplate':
        """The template assigned to the document.
        """
        return self._new_element(self.xa_elem.documentTemplate(), XAPagesTemplate)

    @property
    def body_text(self) -> XABase.XAText:
        """The document body text.
        """
        return self._new_element(self.xa_elem.bodyText(), XABase.XAText)

    @body_text.setter
    def body_text(self, body_text: Union[XABase.XAText, str]):
        if isinstance(body_text, str):
            self.set_property('bodyText', body_text)
        else:
            self.set_property('bodyText', str(body_text))

    @property
    def document_body(self) -> bool:
        """Whether the document has body text.
        """
        return self.xa_elem.documentBody()

    @property
    def facing_pages(self) -> bool:
        """Whether the document has facing pages.
        """
        return self.xa_elem.facingPages()

    @facing_pages.setter
    def facing_pages(self, facing_pages: bool):
        self.set_property('facingPages', facing_pages)

    @property
    def current_page(self) -> 'XAPagesPage':
        """The current page of the document.
        """
        return self._new_element(self.xa_elem.currentPage(), XAPagesPage)

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

    def audio_clips(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: iWorkApplicationBase.XAiWorkAudioClipList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.audioClips(), iWorkApplicationBase.XAiWorkAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: iWorkApplicationBase.XAiWorkChartList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.charts(), iWorkApplicationBase.XAiWorkChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: iWorkApplicationBase.XAiWorkGroupList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.groups(), iWorkApplicationBase.XAiWorkGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: iWorkApplicationBase.XAiWorkImageList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.images(), iWorkApplicationBase.XAiWorkImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: iWorkApplicationBase.XAiWorkiWorkItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.iWorkItems(), iWorkApplicationBase.XAiWorkiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: iWorkApplicationBase.XAiWorkLineList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.lines(), iWorkApplicationBase.XAiWorkLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: iWorkApplicationBase.XAiWorkMovieList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.movies(), iWorkApplicationBase.XAiWorkMovieList, filter)

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

    def shapes(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: iWorkApplicationBase.XAiWorkShapeList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.shapes(), iWorkApplicationBase.XAiWorkShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: iWorkApplicationBase.XAiWorkTableList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.tables(), iWorkApplicationBase.XAiWorkTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTextItemList':
        """Returns a list of text items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text items
        :rtype: iWorkApplicationBase.XAiWorkTextItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.textItems(), iWorkApplicationBase.XAiWorkTextItemList, filter)

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

    def audio_clips(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkAudioClipList':
        """Returns the audio clips of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's audio clips
        :rtype: iWorkApplicationBase.XAiWorkAudioClipList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("audioClips")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkChartList':
        """Returns the charts of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's charts
        :rtype: iWorkApplicationBase.XAiWorkChartList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("charts")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkChartList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkGroupList':
        """Returns the groups of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's groups
        :rtype: iWorkApplicationBase.XAiWorkGroupList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("groups")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkGroupList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkImageList':
        """Returns the images of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's images
        :rtype: iWorkApplicationBase.XAiWorkImageList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("images")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkImageList, filter)

    def iwork_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkiWorkItemList':
        """Returns the iWork items of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's iWork items
        :rtype: iWorkApplicationBase.XAiWorkiWorkItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("iWorkItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkiWorkItemList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkLineList':
        """Returns the lines of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's lines
        :rtype: iWorkApplicationBase.XAiWorkLineList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("lines")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkLineList, filter)
    
    def movies(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkMovieList':
        """Returns the movies of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's movies
        :rtype: iWorkApplicationBase.XAiWorkMovieList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("movies")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkShapeList':
        """Returns the shapes of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's shapes
        :rtype: iWorkApplicationBase.XAiWorkShapeList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("shapes")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkShapeList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTableList':
        """Returns the tables of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's tables
        :rtype: iWorkApplicationBase.XAiWorkTableList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("tables")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkTableList, filter)

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

    def text_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTextItemList':
        """Returns the text items of each section in the list.

        :param filter: A dictionary specifying property-value pairs that all returned text items will have, or None
        :type filter: Union[dict, None]
        :return: The list of every section's text items
        :rtype: iWorkApplicationBase.XAiWorkTextItemList

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("textItems")
        if isinstance(ls[0], ScriptingBridge.SBElementArray):
            ls = [x for sublist in ls for x in sublist]
        else:
            ls = [x for x in ls]
        return self._new_element(ls, iWorkApplicationBase.XAiWorkTableList, filter)

    def __repr__(self):
        return f"<{str(type(self))}length:{len(self.xa_elem)}>"

class XAPagesSection(XABase.XAObject):
    """A class for managing and interacting with sections in Pages.

    .. seealso:: :class:`XAPagesApplication`, :class:`iWorkApplicationBase.XAiWorkiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def body_text(self) -> XABase.XAText:
        """The section body text.
        """
        return self._new_element(self.xa_elem.bodyText(), XABase.XAText)

    @body_text.setter
    def body_text(self, body_text: Union[XABase.XAText, str]):
        if isinstance(body_text, str):
            self.set_property('bodyText', body_text)
        else:
            self.set_property('bodyText', str(body_text))

    def iwork_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkiWorkItemList':
        """Returns a list of iWork items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned iWork items will have, or None
        :type filter: Union[dict, None]
        :return: The list of iWork items
        :rtype: iWorkApplicationBase.XAiWorkiWorkItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.iWorkItems(), iWorkApplicationBase.XAiWorkiWorkItemList, filter)

    def audio_clips(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkAudioClipList':
        """Returns a list of audio clips, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio clips will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio clips
        :rtype: iWorkApplicationBase.XAiWorkAudioClipList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.audioClips(), iWorkApplicationBase.XAiWorkAudioClipList, filter)

    def charts(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkChartList':
        """Returns a list of charts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned charts will have, or None
        :type filter: Union[dict, None]
        :return: The list of charts
        :rtype: iWorkApplicationBase.XAiWorkChartList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.charts(), iWorkApplicationBase.XAiWorkChartList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned images will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: iWorkApplicationBase.XAiWorkImageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.images(), iWorkApplicationBase.XAiWorkImageList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: iWorkApplicationBase.XAiWorkGroupList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.groups(), iWorkApplicationBase.XAiWorkGroupList, filter)

    def lines(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkLineList':
        """Returns a list of lines, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lines will have, or None
        :type filter: Union[dict, None]
        :return: The list of lines
        :rtype: iWorkApplicationBase.XAiWorkLineList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.lines(), iWorkApplicationBase.XAiWorkLineList, filter)

    def movies(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkMovieList':
        """Returns a list of movies, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned movies will have, or None
        :type filter: Union[dict, None]
        :return: The list of movies
        :rtype: iWorkApplicationBase.XAiWorkMovieList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.movies(), iWorkApplicationBase.XAiWorkMovieList, filter)

    def shapes(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkShapeList':
        """Returns a list of shapes, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned shapes will have, or None
        :type filter: Union[dict, None]
        :return: The list of shapes
        :rtype: iWorkApplicationBase.XAiWorkShapeList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shapes(), iWorkApplicationBase.XAiWorkShapeList, filter)

    def pages(self, filter: Union[dict, None] = None) -> 'XAPagesPageList':
        """Returns a list of pages, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned pages will have, or None
        :type filter: Union[dict, None]
        :return: The list of pages
        :rtype: XAPagesPageList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.pages(), XAPagesPageList, filter)

    def tables(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTableList':
        """Returns a list of tables, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tables will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: iWorkApplicationBase.XAiWorkTableList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.tables(), iWorkApplicationBase.XAiWorkTableList, filter)

    def text_items(self, filter: Union[dict, None] = None) -> 'iWorkApplicationBase.XAiWorkTextItemList':
        """Returns a list of text_items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned text_items will have, or None
        :type filter: Union[dict, None]
        :return: The list of text_items
        :rtype: iWorkApplicationBase.XAiWorkTextItemList

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.textItems(), iWorkApplicationBase.XAiWorkTextItemList, filter)



class XAPagesContainerList(iWorkApplicationBase.XAiWorkContainerList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAPagesContainer
        self._xa_ccls = XAPagesPageList
        super().__init__(properties, filter, obj_class)
        logger.debug("Got list of containers")

class XAPagesContainer(iWorkApplicationBase.XAiWorkContainer):
    """A class for managing and interacting with containers in Pages.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        self._xa_ccls = XAPagesPageList
        super().__init__(properties)




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

    .. seealso:: :class:`XAPagesApplication`, :class:`iWorkApplicationBase.XAiWorkiWorkItem`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the page.
        """
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "body_text": self._new_element(raw_dict["bodyText"], XABase.XAText)
        }
        return pyxa_dict

    @property
    def body_text(self) -> XABase.XAText:
        """The page body text.
        """
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

    # def add_chart(self, row_names: list[str], column_names: list[str], data: list[list[Any]], type: int = XAPagesApplication.ChartType.LINE_2D.value, group_by: int = XAPagesApplication.ChartGrouping.ROW.value) -> 'iWorkApplicationBase.XAiWorkChart':
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
    #     :rtype: iWorkApplicationBase.XAiWorkChart

    #     .. versionadded:: 0.0.2
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
    #     return iWorkApplicationBase.XAiWorkChart(properties)




class XAPagesPlaceholderTextList(XABase.XATextList):
    """A wrapper around lists of placeholder texts that employs fast enumeration techniques.

    All properties of placeholder texts can be called as methods on the wrapped list, returning a list containing each text's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPagesPlaceholderText)

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

    @property
    def tag(self) -> str:
        """The placeholder text's script tag.
        """
        return self.xa_elem.tag()

    @tag.setter
    def tag(self, tag: str):
        self.set_property('tag', tag)