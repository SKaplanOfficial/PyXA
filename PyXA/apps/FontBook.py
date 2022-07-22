""".. versionadded:: 0.0.6

Control the macOS FontBook application using JXA-like syntax.
"""

from typing import List, Tuple, Union

from PyXA import XABase
from PyXA import XABaseScriptable

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

class XAFontBookWindow(XABaseScriptable.XASBObject):
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

class XAFontBookDocument(XABaseScriptable.XASBObject):
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




class XAFontBookFontFamilyList(XABase.XAList):
    """A wrapper around lists of Font Book font families that employs fast enumeration techniques.

    All properties of font families can be called as methods on the wrapped list, returning a list containing each font family's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontFamily, filter)

    # TODO
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

    def by_name(self, name: str) -> 'XAFontBookDocument':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAFontBookFontFamily(XABaseScriptable.XASBObject):
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




class XAFontBookTypefaceList(XABase.XAList):
    """A wrapper around lists of Font Book documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookTypeface, filter)

    # TODO
    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def id(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def by_name(self, name: str) -> 'XAFontBookDocument':
        return self.by_property("name", name)

class XAFontBookTypeface(XABaseScriptable.XASBObject):
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
        self.font_container: blah #: The container of the typeface
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




class XAFontBookFontContainerList(XABase.XAList):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontContainer, filter)

    # TODO
    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def by_name(self, name: str) -> 'XAFontBookDocument':
        return self.by_property("name", name)

class XAFontBookFontContainer(XABaseScriptable.XASBObject):
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




class XAFontBookFontCollectionList(XABase.XAList):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, obj_class = None, filter: Union[dict, None] = None):
        if obj_class is None:
            obj_class = XAFontBookFontCollection
        super().__init__(properties, obj_class, filter)

    # TODO
    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def by_name(self, name: str) -> 'XAFontBookDocument':
        return self.by_property("name", name)

class XAFontBookFontCollection(XABaseScriptable.XASBObject):
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




class XAFontBookFontLibraryList(XAFontBookFontCollectionList):
    """A wrapper around lists of Font Book font libraries that employs fast enumeration techniques.

    All properties of font libraries can be called as methods on the wrapped list, returning a list containing each library's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontLibrary, filter)

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
        super().__init__(properties, XAFontBookFontDomain, filter)

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