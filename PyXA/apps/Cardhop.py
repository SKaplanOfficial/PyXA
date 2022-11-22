""".. versionadded:: 0.1.0

Control Cardhop using JXA-like syntax.
"""

from enum import Enum
from typing import Union

import AppKit
from ScriptingBridge import SBElementArray

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable, XADeletable, XAPrintable, XAShowable

class XACardhopAppplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """A class for interacting with Cardhop.app.

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

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XACardhopWindow

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Cardhop is the active application.
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of Cardhop.app.
        """
        return self.xa_scel.version()

    def parse_sentence(self, sentence: str, add_immediately: bool = True):
        """Parses the given sentence and carries out the corresponding actions.

        :param sentence: The sentence to parse
        :type sentence: str
        :param add_immediately: Whether to immediately parse the sentence and save resulting changes, instead of having the user confirm changes via the GUI, defaults to True
        :type add_immediately: bool, optional
        """
        self.xa_scel.parseSentence_addImmediately_(sentence, add_immediately)

    def documents(self, filter: dict = None) -> 'XACardhopDocumentList':
        """Returns a list of documents, as PyXA objects, matching the filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have
        :type filter: dict
        :return: The list of documents
        :rtype: XACardhopDocumentList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.documents(), XACardhopDocumentList, filter)




class XACardhopWindow(XABaseScriptable.XASBWindow, XAPrintable):
    """A window of Cardhop.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> 'XACardhopDocument':
        """The document whose contents are displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XACardhopDocument)




class XACardhopDocumentList(XABase.XAList, XAPrintable, XAClipboardCodable):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACardhopDocument, filter)

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

    def file(self) -> list[XABase.XAPath]:
        """Gets the file path of each document in the list.

        :return: A list of document file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("file")
        return [XABase.XAPath(x) for x in ls]

    def by_name(self, name: str) -> Union['XACardhopDocument', None]:
        """Retrieves the first document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACardhopDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XACardhopDocument', None]:
        """Retrieves the first document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACardhopDocument, None]
        
        .. versionadded:: 0.1.0
        """
        return self.by_property("modified", modified)

    def by_file(self, file: Union[XABase.XAPath, str]) -> Union['XACardhopDocument', None]:
        """Retrieves the first document whose file path matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XACardhopDocument, None]
        
        .. versionadded:: 0.1.0
        """
        if isinstance(file, str):
            file = XABase.XAPath(file)
        return self.by_property("file", file.xa_elem)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, each documents's file URL and name are added to the clipboard.

        :return: A list of each document's file URL and name
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        names = self.name()
        paths = self.file()
        for index, text in enumerate(names):
            items.append(str(text), paths[index].xa_elem)
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XACardhopDocument(XABase.XAObject):
    """A document of Cardhop.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The title of the document.
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save.
        """
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        """The location of the document on disk, if it has one.
        """
        return XABase.XAPath(self.xa_elem.file())