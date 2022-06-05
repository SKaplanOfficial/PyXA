""".. versionadded:: 0.0.1

Control the macOS Preview application using JXA-like syntax.
"""

from typing import List, Union
from AppKit import NSFileManager, NSURL, NSDocumentController

from PyXA import XABase
from PyXA import XABaseScriptable

# Preview constants
_YES = 2036691744
_NO = 1852776480
_ASK = 1634954016
_STANDARD_ERRORS = 1819767668
_DETAILED_ERRORS = 1819763828

class XAPreviewApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with Preview.app.

     .. seealso:: :class:`XAPreviewWindow`, :class:`XAPreviewDocument`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties["window_class"] = XAPreviewWindow

    def print(self, path: Union[str, NSURL], show_prompt: bool = True):
        """Opens the print dialog for the file at the given path, if the file can be opened in Preview.

        :param path: The path of the file to print.
        :type path: Union[str, NSURL]
        :param show_prompt: Whether to show the print dialog or skip directly printing, defaults to True
        :type show_prompt: bool, optional

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        self.properties["sb_element"].print_printDialog_withProperties_(path, show_prompt, None)

    # Documents
    def documents(self, filter: dict = None) -> List['XAPreviewDocument']:
        """Returns a list of documents matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("documents", filter, XAPreviewDocument)

    def document(self, filter: Union[int, dict]) -> 'XAPreviewDocument':
        """Returns the first document that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("documents", filter, XAPreviewDocument)

    def first_document(self) -> 'XAPreviewDocument':
        """Returns the document at the first index of the documents array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("documents", XAPreviewDocument)

    def last_document(self) -> 'XAPreviewDocument':
        """Returns the document at the last (-1) index of the documents array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("documents", XAPreviewDocument)

class XAPreviewWindow(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with Preview windows.

    .. seealso:: :class:`XAPreviewApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.document = self._new_element(self.document, XAPreviewDocument)

class XAPreviewDocument(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with documents in Preview.

    .. seealso:: :class:`XAPreviewApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def __repr__(self):
        return self.name