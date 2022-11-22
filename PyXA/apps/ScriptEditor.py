""".. versionadded:: 0.0.9

Control Script Editor using JXA-like syntax.
"""

from typing import Literal, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable, XACloseable, XADeletable, XAPrintable

class XAScriptEditorItemList(XABase.XAList):
    """A wrapper around lists of Script Editor items that employs fast enumeration techniques.

    All properties of items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAScriptEditorItem
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        """Gets the properties each item in the list.

        :return: A list of property dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def by_properties(self, properties: dict) -> 'XAScriptEditorItem':
        """Retrieves the item whose properties dictionary matches the given properties dictionary, if one exists.

        :return: The desired item, if it is found
        :rtype: Union[XAScriptEditorItem, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("properties", properties)

class XAScriptEditorItem(XABase.XAObject):
    """An item in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All of the object's properties.
        """
        return self.xa_elem.properties()

    def exists(self) -> bool:
        """Verifies that an object exists.

        :return: True if the object exists.
        :rtype: bool

        .. versionadded:: 0.0.9
        """
        return self.xa_elem.exists()
    

class XAScriptEditorApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAScriptEditorWindow

    @property
    def frontmost(self) -> bool:
        """Whether Script Editor is the active application.
        """
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of Script Editor.app.
        """
        return self.xa_scel.version()

    @property
    def selection(self) -> 'XAScriptEditorSelectionObject':
        """The current selection.
        """
        return self._new_element(self.xa_scel.selection(), XAScriptEditorSelectionObject)

    @selection.setter
    def selection(self, selection: 'XAScriptEditorSelectionObject'):
        self.set_property('selection', selection.xa_elem)

    def documents(self, filter: dict = None) -> 'XAScriptEditorDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.documents(), XAScriptEditorDocumentList, filter)

    def classes(self, filter: dict = None) -> 'XAScriptEditorObjectClassList':
        """Returns a list of classes, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.classes(), XAScriptEditorObjectClassList, filter)

    def languages(self, filter: dict = None) -> 'XAScriptEditorLanguageList':
        """Returns a list of languages matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_scel.languages(), XAScriptEditorLanguageList, filter)
    

    

class XAScriptEditorDocumentList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorDocument)

    def modified(self) -> list[bool]:
        """Gets the modified status of each document in the list.

        :return: A list of modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each document in the list.

        :return: A list of document paths
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XABase.XAPath(x) for x in ls]

    def contents(self) -> 'XAScriptEditorTextList':
        """Gets the contents of each document in the list.

        :return: A list of document contents
        :rtype: XAScriptEditorTextList
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("contents")
        return self._new_element(ls, XAScriptEditorTextList)

    def object_description(self) -> list[str]:
        """Gets the object description of each document in the list.

        :return: A list of document object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def event_log(self) -> list[str]:
        """Gets the event log of each document in the list.

        :return: A list of document event logs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("eventLog"))

    def language(self) -> 'XAScriptEditorLanguageList':
        """Gets the language of each document in the list.

        :return: A list of document languages
        :rtype: XAScriptEditorLanguageList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("language")
        return self._new_element(ls, XAScriptEditorLanguageList)

    def selection(self) -> 'XAScriptEditorSelectionObjectList':
        """Gets the selection of each document in the list.

        :return: A list of document selection objects
        :rtype: XAScriptEditorSelectionObjectList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("selection")
        return self._new_element(ls, XAScriptEditorSelectionObjectList)
    
    def text(self) -> 'XAScriptEditorTextList':
        """Gets the text of each document in the list.

        :return: A list of document text
        :rtype: XAScriptEditorTextList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("text")
        return self._new_element(ls, XAScriptEditorTextList)

    def by_modified(self, modified: bool) -> 'XAScriptEditorDocument':
        """Retrieves the tab whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("modified", modified)

    def by_name(self, name: str) -> 'XAScriptEditorDocument':
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("name", name)

    def by_path(self, path: XABase.XAPath) -> 'XAScriptEditorDocument':
        """Retrieves the document whose path matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("path", path.xa_elem)

    def by_contents(self, contents: 'XAScriptEditorText') -> 'XAScriptEditorDocument':
        """Retrieves the document whose contents match the given contents, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("contents", contents.xa_elem)

    def by_object_description(self, object_description: str) -> 'XAScriptEditorDocument':
        """Retrieves the document whose object description matches the given description, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("objectDescription", object_description)

    def by_event_log(self, event_log: str) -> 'XAScriptEditorDocument':
        """Retrieves the document whose event log matches the given string, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("eventLog", event_log)

    def by_language(self, language: 'XAScriptEditorLanguage') -> 'XAScriptEditorDocument':
        """Retrieves the document whose language matches the given language, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("language", language.xa_elem)

    def by_selection(self, selection: 'XAScriptEditorSelectionObject') -> 'XAScriptEditorDocument':
        """Retrieves the document whose selection matches the given selection object, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("selection", selection.xa_elem)

    def by_text(self, text: 'XAScriptEditorText') -> 'XAScriptEditorDocument':
        """Retrieves the document whose text matches the given text, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAScriptEditorDocument, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("text", text.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAScriptEditorDocument(XAScriptEditorItem, XACloseable, XADeletable, XAPrintable, XAClipboardCodable):
    """A script document in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since it was last saved.
        """
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        """The document's name.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def path(self) -> XABase.XAPath:
        """The document's path.
        """
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: Union[XABase.XAPath, str]):
        if isinstance(path, XABase.XAPath):
            path = path.path 
        self.set_property('path', path)

    @property
    def contents(self) -> XABase.XAText:
        """The contents of the document.
        """
        return self._new_element(self.xa_elem.contents(), XAScriptEditorText)

    @contents.setter
    def contents(self, contents: str):
        self.set_property('contents', contents)

    @property
    def object_description(self) -> str:
        """The description of the document.
        """
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property('objectDescription', object_description)

    @property
    def event_log(self) -> str:
        """The event log of the document.
        """
        return self.xa_elem.eventLog().get()

    @property
    def language(self) -> 'XAScriptEditorLanguage':
        """The scripting language.
        """
        return self._new_element(self.xa_elem.language(), XAScriptEditorLanguage)

    @language.setter
    def language(self, language: str):
        self.set_property('language', language)

    @property
    def selection(self) -> 'XAScriptEditorSelectionObject':
        """The current selection.
        """
        return self._new_element(self.xa_elem.selection(), XAScriptEditorSelectionObject)

    @selection.setter
    def selection(self, selection: 'XAScriptEditorSelectionObject'):
        self.set_property('selection', selection.xa_elem)

    @property
    def text(self) -> XABase.XAText:
        """The text of the document.
        """
        return self._new_element(self.xa_elem.text(), XAScriptEditorText)

    @text.setter
    def text(self, text: Union[str, XABase.XAText]):
        if isinstance(text, XABase.XAText):
            text = text.xa_elem
        self.set_property('text', text)

    def save(self, type: Literal["script", "script bundle", "application", "text"], path: Union[str, XABase.XAPath], run_only: bool = False, show_startup_screen: bool  = False, stay_open: bool = False):
        """Saves the document as the specified file type.

        :param type: The file type in which to save the data
        :type type: Literal['script', 'script bundle', 'application', 'text']
        :param path: The file path in which to save the data
        :type path: Union[str, XABase.XAPath]
        :param run_only: Should the script be saved as Run-Only? If it is, you will not be able to edit the contents of the script again, defaults to False. (Applies to all script types except for "text")
        :type run_only: bool, optional
        :param show_startup_screen: Show the startup screen? Defaults to False. (Only applies to scripts saved as "application")
        :type show_startup_screen: bool, optional
        :param stay_open: Should the application remain open after it is launched? Defaults to False. (Only applies to scripts saved as "application")
        :type stay_open: bool, optional

        .. versionadded:: 0.0.9
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        self.xa_elem.saveAs_in_runOnly_startupScreen_stayOpen_(type, path.xa_elem, run_only, show_startup_screen, stay_open)

    def check_syntax(self):
        """Check the syntax of the document.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.checkSyntax()
    
    def compile(self) -> bool:
        """Compile the script of the document.

        .. versionadded:: 0.0.9
        """
        return self.xa_elem.compile()

    def print(self, print_properties: Union[dict, None] = None, show_dialog: bool = True) -> 'XAPrintable':
        """Prints the object.

        Child classes of XAPrintable should override this method as necessary.

        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :return: A reference to the PyXA object that called this method.
        :rtype: XACanPrintPath

        .. versionadded:: 0.0.9
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.print_printDialog_withProperties_(self.xa_elem, show_dialog, print_properties)
        return self

    def get_clipboard_representation(self) -> list[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a Script Editor document, the document's URL and source code are added to the clipboard.

        :return: The document's path and text content
        :rtype: list[Union[AppKit.NSURL, str]]

        .. versionadded:: 0.0.9
        """
        return [self.path.xa_elem, str(self.text)]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
    



class XAScriptEditorWindow(XABaseScriptable.XASBWindow):
    """A window of Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> XAScriptEditorDocument:
        """The document currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XAScriptEditorDocument)

    @property
    def floating(self) -> bool:
        """Whether the window floats.
        """
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is the application's current modal window.
        """
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar.
        """
        return self.xa_elem.titled()


    

class XAScriptEditorObjectClassList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor classes that employs fast enumeration techniques.

    All properties of classes can be called as methods on the wrapped list, returning a list containing each class's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorObjectClass)

class XAScriptEditorObjectClass(XAScriptEditorItem):
    """A class in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAScriptEditorInsertionPointList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor insertion points that employs fast enumeration techniques.

    All properties of insertion points can be called as methods on the wrapped list, returning a list containing each insertion point's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorInsertionPoint)

    def contents(self) -> XAScriptEditorItemList:
        """Gets the contents status of each insertion point in the list.

        :return: A list of insertion point contents
        :rtype: XAScriptEditorItemList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("contents")
        return self._new_element(ls, XAScriptEditorItemList)

    def by_contents(self, contents: XAScriptEditorItem) -> 'XAScriptEditorInsertionPoint':
        """Retrieves the insertion point whose contents match the given contents, if one exists.

        :return: The desired insertion point, if it is found
        :rtype: Union[XAScriptEditorInsertionPoint, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents()) + ">"

class XAScriptEditorInsertionPoint(XAScriptEditorItem):
    """An insertion point between two objects in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def contents(self) -> XAScriptEditorItem:
        return self._new_element(self.xa_elem.contents(), XAScriptEditorItem)

    @contents.setter
    def contents(self, contents: XAScriptEditorItem):
        """The contents of the insertion point.
        """
        self.set_property('contents', contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem.contents().get()) + ">"




class XAScriptEditorTextList(XABase.XATextList):
    """A wrapper around lists of Script Editor texts that employs fast enumeration techniques.

    All properties of texts can be called as methods on the wrapped list, returning a list containing each text's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorText)

    def color(self) -> list[XABase.XAColor]:
        """Gets the color each text in the list.

        :return: A list of text colors
        :rtype: list[XABase.XAColor]
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("color")
        return [XABase.XAColor(x) for x in ls]

    def font(self) -> list[str]:
        """Gets the font name each text in the list.

        :return: A list of text fonts
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("font"))

    def size(self) -> list[int]:
        """Gets the font size each text in the list.

        :return: A list of text font sizes
        :rtype: list[int]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def by_color(self, color: XABase.XAColor) -> 'XAScriptEditorText':
        """Retrieves the text whose font color matches the given color, if one exists.

        :return: The desired text, if it is found
        :rtype: Union[XAScriptEditorText, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("color", color.xa_elem)

    def by_font(self, font: str) -> 'XAScriptEditorText':
        """Retrieves the text whose font name matches the given font name, if one exists.

        :return: The desired text, if it is found
        :rtype: Union[XAScriptEditorText, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("font", font)

    def by_size(self, size: int) -> 'XAScriptEditorText':
        """Retrieves the text whose font size matches the given value, if one exists.

        :return: The desired text, if it is found
        :rtype: Union[XAScriptEditorText, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("size", size)

class XAScriptEditorText(XABase.XAText):
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def color(self) -> XABase.XAColor:
        """The color of the first character.
        """
        return XABase.XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: XABase.XAColor):
        self.set_property('color', color.xa_elem)

    @property
    def font(self) -> str:
        """The name of the font of the first character.
        """
        return self.xa_elem.font()

    @font.setter
    def font(self, font: str):
        self.set_property('font', font)

    @property
    def size(self) -> int:
        """The size in points of the first character.
        """
        return self.xa_elem.size()

    @size.setter
    def size(self, size: int):
        self.set_property('size', size)

    def insertion_points(self, filter: dict = None) -> 'XAScriptEditorInsertionPointList':
        """Returns a list of insertion points matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(self.xa_elem.insertionPoints(), XAScriptEditorInsertionPointList, filter)




class XAScriptEditorLanguageList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor languages that employs fast enumeration techniques.

    All properties of languages can be called as methods on the wrapped list, returning a list containing each language's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorLanguage)

    def object_description(self) -> list[str]:
        """Gets the object description each language in the list.

        :return: A list of language object descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def id(self) -> list[str]:
        """Gets the ID each language in the list.

        :return: A list of language IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        """Gets the name each language in the list.

        :return: A list of language names
        :rtype: list[str]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def supports_compiling(self) -> list[bool]:
        """Gets the supports compiling status each language in the list.

        :return: A list of supports compiling status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("supportsCompiling"))

    def supports_recording(self) -> list[bool]:
        """Gets the supports recording status each language in the list.

        :return: A list of supports recording status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("supportsRecording"))

    def by_object_description(self, object_description: str) -> 'XAScriptEditorLanguage':
        """Retrieves the language whose object description matches the given description, if one exists.

        :return: The desired language, if it is found
        :rtype: Union[XAScriptEditorLanguage, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("objectDescription", object_description)

    def by_id(self, id: str) -> 'XAScriptEditorLanguage':
        """Retrieves the language whose ID matches the given ID, if one exists.

        :return: The desired language, if it is found
        :rtype: Union[XAScriptEditorLanguage, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAScriptEditorLanguage':
        """Retrieves the language whose name matches the given name, if one exists.

        :return: The desired language, if it is found
        :rtype: Union[XAScriptEditorLanguage, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("name", name)

    def by_supports_compiling(self, supports_compiling: bool) -> 'XAScriptEditorLanguage':
        """Retrieves the first language whose supports compiling status matches the given boolean value, if one exists.

        :return: The desired language, if it is found
        :rtype: Union[XAScriptEditorLanguage, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("supportsCompiling", supports_compiling)

    def by_supports_recording(self, supports_recording: bool) -> 'XAScriptEditorLanguage':
        """Retrieves the first language whose supports recording status matches the given boolean value, if one exists.

        :return: The desired language, if it is found
        :rtype: Union[XAScriptEditorLanguage, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("supportsRecording", supports_recording)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAScriptEditorLanguage(XAScriptEditorItem):
    """A scripting language in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_description(self) -> str:
        """The description of the language.
        """
        return self.xa_elem.objectDescription()

    @property
    def id(self) -> str:
        """The unique id of the language.
        """
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the language.
        """
        return self.xa_elem.name()

    @property
    def supports_compiling(self) -> bool:
        """Is the language compilable?
        """
        return self.xa_elem.supportsCompiling()

    @property
    def supports_recording(self) -> bool:
        """Is the language recordable?
        """
        return self.xa_elem.supportsRecording()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAScriptEditorSelectionObjectList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor selection objects that employs fast enumeration techniques.

    All properties of selection objects can be called as methods on the wrapped list, returning a list containing each selection objects's value for the property.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorSelectionObject)

    def character_range(self) -> list[tuple[int, int]]:
        """Gets the character range each selection object in the list.

        :return: A list of character ranges
        :rtype: list[tuple[int, int]]
        
        .. versionadded:: 0.0.9
        """
        return list(self.xa_elem.arrayByApplyingSelector_("characterRange"))

    def contents(self) -> XAScriptEditorItemList:
        """Gets the character range each selection object in the list.

        :return: A list of character ranges
        :rtype: XAScriptEditorItemList
        
        .. versionadded:: 0.0.9
        """
        ls = self.xa_elem.arrayByApplyingSelector_("contents")
        return self._new_element(ls, XAScriptEditorItemList)

    def by_character_range(self, character_range: tuple[int, int]) -> 'XAScriptEditorSelectionObject':
        """Retrieves the selection object whose character range matches the given character range, if one exists.

        :return: The desired selection object, if it is found
        :rtype: Union[XAScriptEditorSelectionObject, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("characterRange", character_range)

    def by_contents(self, contents: XAScriptEditorItem) -> 'XAScriptEditorSelectionObject':
        """Retrieves the selection object whose contents match the given contents, if one exists.

        :return: The desired selection object, if it is found
        :rtype: Union[XAScriptEditorSelectionObject, None]
        
        .. versionadded:: 0.0.9
        """
        return self.by_property("contents", contents.xa_elem)

class XAScriptEditorSelectionObject(XAScriptEditorItem):
    """The state of the current selection in Script Editor.app.

    .. versionadded:: 0.0.9
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def character_range(self) -> tuple[int, int]:
        """The range of characters in the selection.
        """
        return self.xa_elem.characterRange()

    @property
    def contents(self) -> XAScriptEditorItem:
        """The contents of the selection.
        """
        return self.xa_elem.contents().get()

    @contents.setter
    def contents(self, contents: XAScriptEditorItem):
        self.set_property('contents', contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents) + ">"