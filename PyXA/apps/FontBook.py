""".. versionadded:: 0.0.6

Control the macOS FontBook application using JXA-like syntax.
"""

from typing import List, Tuple, Union

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable

class XAFontBookApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Font Book.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFontBookWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Font Book is the active application
        self.version: str #: The version of the Font Book application
        self.validate_fonts_before_installing: bool #: Whether to validate fonts before installing them
        self.installation_target: XAFontBookFontLibrary #: The library where new fonts are installed
        self.fonts_library: XAFontBookFontBookAllFontsLibraryObject #: The All Fonts library
        self.selection: XAFontBookTypefaceList #: The currently selected typefaces
        self.selected_font_families: XAFontBookFontFamilyList #: The currently selected font families
        self.selected_collections: XAFontBookFontCollectionList #: The currently selected collections

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def validate_fonts_before_installing(self) -> bool:
        return self.xa_scel.validateFontsBeforeInstalling()

    @property
    def installation_target(self) -> 'XAFontBookFontLibrary':
        return self._new_element(self.xa_scel.installationTarget(), XAFontBookFontLibrary)

    @property
    def fonts_library(self) -> 'XAFontBookFontBookAllFontsLibraryObject':
        return self._new_element(self.xa_scel.fontsLibrary(), XAFontBookFontBookAllFontsLibraryObject)

    @property
    def selection(self) -> 'XAFontBookTypefaceList':
        ls = self.xa_scel.selection()
        return self._new_element(ls, XAFontBookTypefaceList)

    @property
    def selected_font_families(self) -> 'XAFontBookFontFamilyList':
        ls = self.xa_scel.selectedFontFamilies()
        return self._new_element(ls, XAFontBookFontFamilyList)

    @property
    def selected_collections(self) -> 'XAFontBookFontCollectionList':
        ls = self.xa_scel.selectedCollections()
        return self._new_element(ls, XAFontBookFontCollectionList)

    def documents(self, filter: dict = None) -> 'XAFontBookDocumentList':
        """Returns a list of documents matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.documents(), XAFontBookDocumentList, filter)

    def font_families(self, filter: dict = None) -> 'XAFontBookFontFamilyList':
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.fontFamilies(), XAFontBookFontFamilyList, filter)

    def typefaces(self, filter: dict = None) -> 'XAFontBookTypefaceList':
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.typefaces(), XAFontBookTypefaceList, filter)

    def font_collections(self, filter: dict = None) -> 'XAFontBookFontCollectionList':
        """Returns a list of font collections matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.fontCollections(), XAFontBookFontCollectionList, filter)

    def font_domains(self, filter: dict = None) -> 'XAFontBookFontDomainList':
        """Returns a list of font domains matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.fontDomains(), XAFontBookFontDomainList, filter)

    def font_libraries(self, filter: dict = None) -> 'XAFontBookFontLibraryList':
        """Returns a list of font libraries matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.fontLibraries(), XAFontBookFontLibraryList, filter)

    def font_containers(self, filter: dict = None) -> 'XAFontBookFontContainerList':
        """Returns a list of font containers matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.fontContainers(), XAFontBookFontContainerList, filter)




# class XAFontBookWindowList(XABase.XAList):
#     """A wrapper around lists of Font Book windows that employs fast enumeration techniques.

#     All properties of windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

#     .. versionadded:: 0.0.6
#     """
#     def __init__(self, properties: dict, filter: Union[dict, None] = None):
#         super().__init__(properties, XAFontBookDocument, filter)

#     def path(self) -> List[str]:
#         return list(self.xa_elem.arrayByApplyingSelector_("path"))

#     def modified(self) -> List[bool]:
#         return list(self.xa_elem.arrayByApplyingSelector_("modified"))

#     def name(self) -> List[str]:
#         return list(self.xa_elem.arrayByApplyingSelector_("name"))

#     def by_path(self, path: str) -> 'XAFontBookDocument':
#         return self.by_property("path", path)

#     def by_modified(self, modified: bool) -> 'XAFontBookDocument':
#         return self.by_property("modified", modified)

#     def by_name(self, name: str) -> 'XAFontBookDocument':
#         return self.by_property("name", name)

class XAFontBookWindow(XABase.XAObject):
    """A class for managing and interacting with documents in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The full title of the window
        self.id: int #: The unique identifier for the window
        self. bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.closeable: bool #: Whether the window has a close button
        self.titled: bool # Whether the window has a title bar
        self.index: int #: The index of the window in the front-to-back window ordering
        self.floating: bool #: Whether the window floats
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.modal: bool #: Whether the window is a modal window
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
    



class XAFontBookDocumentList(XABase.XAList):
    """A wrapper around lists of Font Book documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookDocument, filter)

    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def modified(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_path(self, path: str) -> 'XAFontBookDocument':
        return self.by_property("path", path)

    def by_modified(self, modified: bool) -> 'XAFontBookDocument':
        return self.by_property("modified", modified)

    def by_name(self, name: str) -> 'XAFontBookDocument':
        return self.by_property("name", name)

class XAFontBookDocument(XABase.XAObject):
    """A class for managing and interacting with documents in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.path: str #: The file path of the document
        self.modified: bool #: Whether the document has been modified since its last save
        self.name: str #: The name of the document

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        return self.xa_elem.name()




class XAFontBookFontFamilyList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font families that employs fast enumeration techniques.

    All properties of font families can be called as methods on the wrapped list, returning a list containing each font family's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontFamily, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def display_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName"))

    def displayed_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def duplicated(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("duplicated"))

    def files(self) -> List[List[XABase.XAPath]]:
        ls = self.xa_elem.arrayByApplyingSelector_("files")
        return [XABase.XAURL(x) for x in [y for y in ls]]

    def by_properties(self, properties: dict) -> 'XAFontBookFontFamily':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAFontBookFontFamily':
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> 'XAFontBookFontFamily':
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> 'XAFontBookFontFamily':
        return self.by_property("displayedName", displayed_name)

    def by_enabled(self, enabled: bool) -> 'XAFontBookFontFamily':
        return self.by_property("enabled", enabled)

    def by_duplicates(self, duplicated: bool) -> 'XAFontBookFontFamily':
        return self.by_property("duplicated", duplicated)

    def by_files(self, files: List[XABase.XAPath]) -> 'XAFontBookFontFamily':
        return files == self.files()

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each font family in the list.

        When the clipboard content is set to a list of font families, the name of each font family is added to the clipboard.

        :return: The list of font family names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFontBookFontFamily(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font families in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the font family
        self.name: str #: The name of the font family
        self.display_name: str #: The display name of the font family
        self.displayed_name: str #: The display name of the font family
        self.enabled: bool #: Whether the font family is enabled
        self.duplicated: bool #: Whether teh font family contains duplicated faces
        self.files: List[XABase.XAPath] #: The font files of the font family

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def duplicated(self) -> bool:
        return self.xa_elem.duplicated()

    @property
    def files(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    def delete(self):
        """Permanently deletes the typeface.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.delete()

    def typefaces(self, filter: dict = None) -> 'XAFontBookTypefaceList':
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.typefaces(), XAFontBookTypefaceList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the font family.

        When the clipboard content is set to a font family, the name of the font family is added to the clipboard.

        :return: The name of the font family
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAFontBookTypefaceList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookTypeface, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def display_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName"))

    def displayed_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def font_family(self) -> XAFontBookFontFamilyList:
        ls = self.xa_elem.arrayByApplyingSelector_("fontFamily")
        return self._new_element(ls, XAFontBookFontFamilyList)

    def family_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("familyName"))

    def style_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("styleName"))

    def post_script_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("postScriptName"))

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def duplicated(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("duplicated"))

    def font_type(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontType"))

    def copyright(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("copyright"))

    def font_container(self) -> 'XAFontBookFontContainerList':
        ls = self.xa_elem.arrayByApplyingSelector_("fontContainer")
        return self._new_element(ls, XAFontBookFontContainerList)

    def files(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("files")
        return [XABase.XAPath(x) for x in ls]

    def by_properties(self, properties: dict) -> 'XAFontBookTypeface':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAFontBookTypeface':
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> 'XAFontBookTypeface':
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> 'XAFontBookTypeface':
        return self.by_property("displayedName", displayed_name)

    def by_font_family(self, font_family: XAFontBookFontFamily) -> 'XAFontBookTypeface':
        return self.by_property("fontFamily", font_family.xa_elem)

    def by_family_name(self, family_name: str) -> 'XAFontBookTypeface':
        return self.by_property("familyName", family_name)

    def by_style_name(self, style_name: str) -> 'XAFontBookTypeface':
        return self.by_property("styleName", style_name)

    def by_post_script_name(self, post_script_name: str) -> 'XAFontBookTypeface':
        return self.by_property("postScriptName", post_script_name)

    def by_id(self, id: str) -> 'XAFontBookTypeface':
        return self.by_property("id", id)

    def by_enabled(self, enabled: bool) -> 'XAFontBookTypeface':
        return self.by_property("enabled", enabled)

    def by_duplicated(self, duplicated: bool) -> 'XAFontBookTypeface':
        return self.by_property("duplicated", duplicated)

    def by_font_type(self, font_type: str) -> 'XAFontBookTypeface':
        return self.by_property("fontType", font_type)

    def by_copyright(self, copyright: str) -> 'XAFontBookTypeface':
        return self.by_property("copyright", copyright)

    def by_font_container(self, font_container: 'XAFontBookFontContainer') -> 'XAFontBookTypeface':
        return self.by_property("fontContainer", font_container.xa_elem)

    def by_files(self, files: List[XABase.XAPath]) -> 'XAFontBookTypeface':
        for typeface in self:
            if typeface.files == files:
                return typeface

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each typeface in the list.

        When the clipboard content is set to a list of typefaces, the name of each typeface is added to the clipboard.

        :return: The list of typeface names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFontBookTypeface(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with typefaces in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the typeface
        self.name: str #: The name of the typeface
        self.display_name: str #: The display name of the typeface
        self.displayed_name: str #: The display name of the typeface
        self.font_family: XAFontBookFontFamily #: The font family that contains the typeface
        self.family_name: str #: The name of the typeface's font family
        self.style_name: str #: The name of the typeface's style
        self.post_script_name: str #: The PostScript font name
        self.id: str #: The unique identifier for the typeface
        self.enabled: bool #: Whether the typeface is enabled
        self.duplicated: bool #: Whether the typeface is duplicated
        self.font_type: str #: The type of the typeface
        self.copyright: str #: The copyright string for the typeface
        self.font_container: XAFontBookFontContainer #: The container of the typeface
        self.files: List[XABase.XAPath] #: The font files for the typeface

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def font_family(self) -> XAFontBookFontFamily:
        return self._new_element(self.xa_elem.fontFamily(), XAFontBookFontFamily)

    @property
    def family_name(self) -> str:
        return self.xa_elem.familyName()

    @property
    def style_name(self) -> str:
        return self.xa_elem.styleName()

    @property
    def post_script_name(self) -> str:
        return self.xa_elem.PostScriptName()

    @property
    def id(self) -> str:
        return self.xa_elem.ID()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def duplicated(self) -> bool:
        return self.xa_elem.duplicated()

    @property
    def font_type(self) -> str:
        return self.xa_elem.fontType()

    @property
    def copyright(self) -> str:
        return self.xa_elem.copyright()

    @property
    def font_container(self) -> 'XAFontBookFontContainer':
        return self._new_element(self.xa_elem.fontContainer(), XAFontBookFontContainer)

    @property
    def files(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the typeface.

        When the clipboard content is set to a typeface, the name of the typeface is added to the clipboard.

        :return: The name of the typeface
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAFontBookFontContainerList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontContainer, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def files(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("files")
        return [XABase.XAPath(x) for x in ls]

    def domain(self) -> 'XAFontBookFontDomainList':
        ls = self.xa_elem.arrayByApplyingSelector_("domain")
        return self._new_element(ls, XAFontBookFontDomainList)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def by_properties(self, properties: dict) -> 'XAFontBookFontContainer':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAFontBookFontContainer':
        return self.by_property("name", name)

    def by_path(self, path: str) -> 'XAFontBookFontContainer':
        return self.by_property("path", path)

    def by_files(self, files: List[XABase.XAPath]) -> 'XAFontBookFontContainer':
        return files == self.files()

    def by_domain(self, domain: 'XAFontBookFontDomain') -> 'XAFontBookFontContainer':
        return self.by_property("domain", domain.xa_elem)

    def by_id(self, id: str) -> 'XAFontBookFontContainer':
        return self.by_property("id", id)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each container in the list.

        When the clipboard content is set to a list of containers, the name of each container is added to the clipboard.

        :return: The list of container names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFontBookFontContainer(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font containers in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the container
        self.name: str #: The name of the container
        self.path: str #: The path to the main container
        self.files: List[XABase.XAPath] #: The files for the container
        self.domain: XAFontBookFontDomain #: The font domain for the container
        self.id: str #: The unique identifier of the container

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def files(self) -> List[XABase.XAPath]:
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    @property
    def domain(self) -> 'XAFontBookFontDomain':
        return self._new_element(self.xa_elem.domain(), XAFontBookFontDomain)

    @property
    def id(self) -> str:
        return self.xa_elem.ID()

    def font_families(self, filter: dict = None) -> 'XAFontBookFontFamilyList':
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.fontFamilies(), XAFontBookFontFamilyList, filter)

    def typefaces(self, filter: dict = None) -> 'XAFontBookTypefaceList':
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.typefaces(), XAFontBookTypefaceList, filter)

    def font_domains(self, filter: dict = None) -> 'XAFontBookFontDomainList':
        """Returns a list of font domains matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.fontDomains(), XAFontBookFontDomainList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the container.

        When the clipboard content is set to a container, the name of the container is added to the clipboard.

        :return: The name of the container
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAFontBookFontCollectionList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAFontBookFontCollection
        super().__init__(properties, obj_class, filter)

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def display_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName"))

    def displayed_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def by_properties(self, properties: dict) -> 'XAFontBookFontCollection':
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> 'XAFontBookFontCollection':
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> 'XAFontBookFontCollection':
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> 'XAFontBookFontCollection':
        return self.by_property("displayedName", displayed_name)

    def by_enabled(self, enabled: bool) -> 'XAFontBookFontCollection':
        return self.by_property("enabled", enabled)

    def get_clipboard_representation(self) -> List[str]:
        """Gets a clipboard-codable representation of each collection in the list.

        When the clipboard content is set to a list of collections, the name of each collection is added to the clipboard.

        :return: The list of collection names
        :rtype: List[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFontBookFontCollection(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font collections in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: All properties of the collection
        self.name: str #: The name of the collection
        self.display_name: str #: The display name of the collection
        self.displayed_name: str #: The display name of the collection
        self.enabled: bool #: Whether the collection is enabled 

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def display_name(self) -> str:
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    def font_families(self, filter: dict = None) -> 'XAFontBookFontFamilyList':
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.fontFamilies(), XAFontBookFontFamilyList, filter)

    def typefaces(self, filter: dict = None) -> 'XAFontBookTypefaceList':
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.typefaces(), XAFontBookTypefaceList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the collection.

        When the clipboard content is set to a collection, the name of the collection is added to the clipboard.

        :return: The name of the collection
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAFontBookFontLibraryList(XAFontBookFontCollectionList):
    """A wrapper around lists of Font Book font libraries that employs fast enumeration techniques.

    All properties of font libraries can be called as methods on the wrapped list, returning a list containing each library's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFontBookFontLibrary)

class XAFontBookFontLibrary(XAFontBookFontCollection):
    """A class for managing and interacting with font libraries in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The unique identifier of the domain

    @property
    def id(self) -> str:
        return self.xa_elem.ID()

    def font_containers(self, filter: dict = None) -> 'XAFontBookFontContainerList':
        """Returns a list of font containers matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.fontContainers(), XAFontBookFontContainerList, filter)


class XAFontBookFontDomainList(XAFontBookFontLibraryList):
    """A wrapper around lists of Font Book font domains that employs fast enumeration techniques.

    All properties of font domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFontBookFontDomain)

class XAFontBookFontDomain(XAFontBookFontLibrary):
    """A class for managing and interacting with font domains in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAFontBookFontBookAllFontsLibraryObject(XAFontBookFontDomain):
    """A class for managing and interacting with the all fonts library object in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)