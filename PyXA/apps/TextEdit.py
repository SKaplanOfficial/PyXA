""".. versionadded:: 0.0.1

Control the macOS TextEdit application using JXA-like syntax.
"""

from enum import Enum
from typing import List, Tuple, Union
from AppKit import NSFileManager, NSURL

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XATextEditApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with TextEdit.app.

    .. seealso:: :class:`XATextEditWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.1
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = OSType('yes ') #: Save the file
        NO  = OSType('no  ') #: Do not save the file
        ASK = OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATextEditWindow

        self.frontmost: bool #: Whether TextEdit is the active application
        self.name: str #: The name of the application
        self.version: str #: The version of the TextEdit application

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def print(self, file: Union[str, NSURL, 'XATextEditDocument'], show_prompt: bool = True, print_settings: dict = None):
        """Prints a TextEdit document.

        :param file: The document or path to a document to print
        :type file: Union[str, NSURL, &#39;XATextEditDocument&#39;]
        :param show_prompt: Whether to show the print dialog, defaults to True
        :type show_prompt: bool, optional
        :param print_settings: Settings to print with or to preset in the print dialog, defaults to None
        :type print_settings: dict, optional

        :Example 1: Printing a document with print settings

        >>> import PyXA
        >>> from datetime import datetime, timedelta
        >>> app = PyXA.application("TextEdit")
        >>> doc = app.documents()[0]
        >>> print_time = datetime.now() + timedelta(minutes=1)
        >>> settings = {
        >>>     "copies": 3,
        >>>     "collating": False,
        >>>     "startingPage": 1,
        >>>     "endingPage": 10,
        >>>     "pagesAcross": 3,
        >>>     "pagesDown": 3,
        >>>     "requestedPrintTime": print_time,
        >>>     "errorHandling": app.PrintErrorHandling.DETAILED.value,
        >>>     "faxNumber": "",
        >>>     "targetPrinter": ""
        >>> }
        >>> app.print(doc, print_settings=settings)

        .. versionadded:: 0.0.3
        """
        if isinstance(file, str):
            file = NSURL.alloc().initFileURLWithPath_(file)
        elif isinstance(file, XATextEditDocument):
            file = NSURL.alloc().initFileURLWithPath_(file.path)
        self.xa_scel.print_printDialog_withProperties_(file, show_prompt, print_settings)

    # Documents
    def documents(self, filter: dict = None) -> 'XATextEditDocumentList':
        """Returns a list of documents matching the filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have
        :type filter: dict
        :return: The list of documents
        :rtype: List[XATextEditDocument]

        :Example 1: Listing all documents

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(list(app.documents()))
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Current Document.txt>, <<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document.txt>, ...]

        :Example 2: List documents after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(list(app.documents({"name": "Another Document.txt"})))
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document.txt>]

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.documents(), XATextEditDocumentList, filter)

    def new_document(self, name: Union[str, None] = "Untitled.txt", text: Union[str, None] = "", location: Union[str, None] = None) -> 'XATextEditDocument':
        """Creates a new document with the given name and initializes it with the supplied text. If no location is provided, the document file is created in the user's Documents folder.

        :param name: The name (including file extension) of the document, defaults to "Untitled.txt"
        :type name: Union[str, None], optional
        :param text: The initial text of the document, defaults to ""
        :type text: Union[str, None], optional
        :param location: The containing folder of the new document, defaults to None.
        :type location: Union[str, None]
        :return: A reference to the newly created document.
        :rtype: XATextEditDocument

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> doc = app.new_document("New.txt", "Example text")
        >>> print(doc.properties)
        {
            modified = 0;
            name = "New.txt";
            objectClass = "<NSAppleEventDescriptor: 'docu'>";
            path = "/Users/exampleuser/Documents/New.txt";
            text = "Example text";
        }

        .. seealso:: :class:`XATextEditDocument`

        .. versionadded:: 0.0.1
        """
        if location is None:
            location = NSFileManager.alloc().homeDirectoryForCurrentUser().relativePath() + "/Documents/" + name
        else:
            location = location + name
        return self.push("document", {"name": name, "text": text, "path": location}, self.xa_scel.documents(), XATextEditDocument)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.3
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XATextEditDocument)


class XATextEditWindow(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit windows.

    .. seealso:: :class:`XATextEditApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.document: XATextEditDocument #: The active document
        self.floating: bool #: Whether the window floats
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in front-to-back ordering
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.modal: bool #: Whether the window is a modal window
        self.name: str #: The full title of the window
        self.resizable: bool #: Whether the window can be resized
        self.titled: bool #: Whether the window has a title bar
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def document(self) -> 'XATextEditDocument':
        doc_obj = self.xa_elem.document()
        return self._new_element(doc_obj, XATextEditDocument)

    @property
    def floating(self) -> bool:
        return self.xa_elem.floating()

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_elem.miniaturized()

    @property
    def modal(self) -> bool:
        return self.xa_elem.modal()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def titled(self) -> bool:
        return self.xa_elem.titled()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()


class XATextEditDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each documents's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XATextEditDocument, filter)

    def path(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def modified(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def by_properties(self, properties: dict) -> 'XATextEditDocument':
        return self.by_property("properties", properties)

    def by_path(self, path: str) -> 'XATextEditDocument':
        return self.by_property("path", path)

    def by_name(self, name: str) -> 'XATextEditDocument':
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> 'XATextEditDocument':
        return self.by_property("modified", modified)


class XATextEditDocument(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XATextEditApplication`

    .. versionchanged:: 0.0.2

       Added :func:`close`, :func:`save`, and :func:`copy`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the document
        self.path: str #: The path at which the document is stored
        self.name: str #: The name of the document, including the file extension
        self.modified: bool #: Whether the document has been modified since the last save

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    def close(self, save: XATextEditApplication.SaveOption = XATextEditApplication.SaveOption.YES.value):
        """Closes the document.

        .. versionadded:: 0.0.2
        """
        self.xa_elem.closeSaving_savingIn_(save, None)

    def save(self, file_path: str = None):
        """Saves the document.

        If a file path is provided, TextEdit will attempt to create a new file at the target location and of the specified file extension. If no file path is provided, a save dialog for the document will open.

        :param file_path: The path to save the document at, defaults to None
        :type file_path: str, optional

        :Example 1: Save all currently open documents

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> for doc in app.documents():
        >>>     doc.save()

        .. versionadded:: 0.0.2
        """
        if file_path is not None:
            url = NSURL.alloc().initFileURLWithPath_(file_path)
            self.xa_elem.saveAs_in_(None, url)
        else:
            self.xa_elem.saveAs_in_(None, None)

    def copy(self):
        """Copies the document file and its contents to the clipboard.

        .. versionadded:: 0.0.2
        """
        url =  NSURL.alloc().initFileURLWithPath_(self.path)
        self.set_clipboard([self.text, url])

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"