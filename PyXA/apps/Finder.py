""".. versionadded:: 0.0.1

Control Finder using JXA-like syntax.
"""

from operator import contains
from typing import List, Union
from Foundation import NSFileManager

from AppKit import NSString, NSURL
from numpy import isin

from PyXA import XABase
from PyXA import XABaseScriptable

fm = NSFileManager.defaultManager()

_PRIVACY_READ_ONLY = 1919246692
_PRIVACY_READ_WRITE = 1919186802
_PRIVACY_WRITE_ONLY = 2003986804
_PRIVACY_NONE = 1852796517
_MACOS_FORMAT = 1684432998
_MACOS_EXTENDED_FORMAT = 1684432939
_UFS_FORMAT = 1684436326
_NFS_FORMAT = 1684434534
_AUDIO_FORMAT = 1684431221
_PRO_DOS_FORMAT = 1684435058
_MSDOS_FORMAT = 1684434291
_NTFS_FORMAT = 1684434548
_ISO9660_FORMAT = 1684420918
_HIGH_SIERRA_FORMAT = 1684433011
_QUICKTAKE_FORMAT = 1684433011
_APPLE_PHOTO_FORMAT = 1684435316
_APPLE_SHARE_FORMAT = 1684431219
_UDF_FORMAT = 1684436324
_WEBDAV_FORMAT = 1684436836
_FTP_FORMAT = 1684432500
_PACKET_WRITTEN_UDF_FORMAT = 1684435061 
_XSAN_FORMAT = 1684431203
_APFS_FORMAT = 1684431216
_EXFAT_FORMAT = 1684437094
_SMB_FORMAT = 1684435821
_UNKNOWN_FORMAT = 1684422463

class XAFinderApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Finder.app.

    .. seealso:: :class:`XAFinderFolder`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str = self.xa_scel.name() #: The name of Finder
        self.visible: bool = self.xa_scel.visible() #: Whether Finder is currently visible
        self.frontmost: bool = self.xa_scel.frontmost() #: Whether Finder is the active application
        self.product_version: str = self.xa_scel.productVersion() #: The system software version

        self.__selection = None #: The currently selected items in Finder
        self.__insertion_location = None #: The container in which a new folder would be created in by default in the frontmost window
        self.__startup_disk = None #: The startup disk for this system
        self.__desktop = None #: The user's desktop
        self.__trash = None #: The system Trash
        self.__home = None #: The home directory
        self.__computer_container = None #: The computer directory
        self.__finder_preferences = None #: Preferences for Finder as a whole

    @property
    def desktop(self) -> 'XAFinderDesktop':
        if self.__desktop is None:
            desktop_obj = self.xa_scel.desktop()
            self.__desktop = self._new_element(desktop_obj, XAFinderDesktop)
        return self.__desktop

    @property
    def trash(self) -> 'XAFinderTrash':
        if self.__trash is None:
            trash_obj = self.xa_scel.trash()
            self.__trash = self._new_element(trash_obj, XAFinderTrash)
        return self.__trash

    def _resolve_symlinks(self, path: str) -> str:
        """Resolves all symlinks in the specified path.

        :param path: The path to resolve.
        :type path: str
        :return: The fully resolved path as a string.
        :rtype: str

        .. versionadded:: 0.0.1
        """
        NS_str = NSString.alloc().initWithString_(path)
        return NS_str.stringByResolvingSymlinksInPath()

    def select_item(self, path: str) -> 'XAFinderApplication':
        """Selects the file or folder at the specified path.
        
        This opens a new tab of Finder unless the current tab is the parent folder of the provided path and no item is currently selected.

        :param path: The path of the file or folder to select.
        :type path: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> app.select_item("/Users/exampleuser/Documents/Example.txt")

        .. seealso:: :func:`select_items`

        .. versionadded:: 0.0.1
        """
        path = self._resolve_symlinks(path)
        self.xa_wksp.selectFile_inFileViewerRootedAtPath_(path, None)
        return self

    def select_items(self, paths: List[str]) -> 'XAFinderApplication':
        """Selects the files or folders at the specified paths.
        
        This opens a new tab of Finder for each different parent folder in the list of paths to select.

        :param path: The paths to select.
        :type filepath: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.select_item(items)

        .. seealso:: :func:`select_item`

        .. versionadded:: 0.0.1
        """
        paths = [self._resolve_symlinks(x) for x in paths]
        self.xa_wksp.activateFileViewerSelectingURLs_(paths)
        return self

    def selection(self) -> List['XAFinderItem']:
        """Obtains PyXA references to the selected items in Finder.

        :return: The list of selected items.
        :rtype: List[XAFinderItem]

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.select_item(items)
        >>> print(app.selection())
        [<<class 'PyXA.apps.Finder.XAFinderFile'>Example 1.txt>, <<class 'PyXA.apps.Finder.XAFinderFile'>Example 2.txt>]

        .. versionadded:: 0.0.1
        """
        selected_items = []
        items = self.xa_scel.selection().get()
        for item in items:
            kind = item.kind()
            if kind == "Folder":
                selected_items.append(self._new_element(item, XAFinderFolder))
            else:
                selected_items.append(self._new_element(item, XAFinderFile))
        return selected_items

    def recycle_item(self, path: Union[str, NSURL]) -> 'XAFinderApplication':
        """Moves the file or folder at the specified path to the trash.

        :param path: The path of the file or folder to recycle.
        :type path: Union[str, NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

       :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> app.recycle_item("/Users/exampleuser/Documents/Example.txt")

        .. seealso:: :func:`recycle_items`

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        fm.trashItemAtURL_resultingItemURL_error_(path, None, None)
        return self

    def recycle_items(self, paths: List[Union[str, NSURL]]) -> 'XAFinderApplication':
        """Moves the files or folders at the specified paths to the trash.

        :param path: The paths of the file and/or folders to recycle.
        :type path: List[Union[str, NSURL]]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.recycle_items(items)

        .. seealso:: :func:`recycle_item`

        .. versionadded:: 0.0.1
        """
        for path in paths:
            self.recycle_item(path)
        return self

    def empty_trash(self) -> 'XAFinderApplication':
        """Empties the trash.

        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

       :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> app.empty_trash()

        .. versionadded:: 0.0.1
        """
        self.xa_scel.emptySecurity_(True)
        return self

    def delete_item(self, path: Union[str, NSURL]) -> 'XAFinderApplication':
        """Permanently deletes the file or folder at the specified path.

        :param path: The path of the file or folder to delete.
        :type path: Union[str, NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

       :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> app.delete_item("/Users/exampleuser/Documents/Example.txt")

        .. seealso:: :func:`delete_items`

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        fm.removeItemAtURL_error_(path, None)
        return self

    def delete_items(self, paths: List[Union[str, NSURL]]) -> 'XAFinderApplication':
        """Permanently deletes the files or folders at the specified paths.

        :param path: The paths of the files and/or folders to delete.
        :type path: Union[str, NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.delete_items(items)

        .. seealso:: :func:`delete_items`

        .. versionadded:: 0.0.1
        """
        for path in paths:
            self.delete_item(path)
        return self

    def duplicate_item(self, path: str) -> 'XAFinderApplication':
        """Duplicates the specified file or folder in its containing folder.

        The duplicated item will have the name of the original with " 2" added to the end.

        :param path: The path of the file or folder to duplicate.
        :type path: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

       :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> app.duplicate_item("/Users/exampleuser/Documents/Example.txt")

        .. seealso:: :func:`duplicate_items`

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        new_path = path
        if path.hasDirectoryPath():
            new_path = path.path() + " 2"
        else:
            new_path = path.path().replace("." + path.pathExtension(), " 2." + path.pathExtension())
        path2 = NSURL.alloc().initFileURLWithPath_(new_path)
        fm.copyItemAtURL_toURL_error_(path, path2, None)
        return self

    def duplicate_items(self, paths: List[str]) -> 'XAFinderApplication':
        """Duplicates the specified files or folders in their containing folder.

        The duplicated items will have the name of the original with " 2" added to the end.

        :param path: The paths of the files and/or folders to duplicate.
        :type path: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.duplicate_items(items)

        .. seealso:: :func:`duplicate_item`

        .. versionadded:: 0.0.1
        """
        for path in paths:
            self.duplicate_item(path)
        return self

    def search(self, query: str) -> 'XAFinderApplication':
        """Opens a Finder search window and searches for the specified term.

        :param query: The term to search.
        :type query: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        .. versionadded:: 0.0.1
        """
        self.xa_wksp.showSearchResultsForQueryString_(query)
        return self

    def get_labels(self) -> List[str]:
        """Gets the list of file labels.

        :return: The list of file labels.
        :rtype: str

        .. versionadded:: 0.0.1
        """
        return self.xa_wksp.fileLabels()

    def insertion_location(self) -> 'XAFinderApplication':
        """Gets a reference to the directory in which a new folder would be created if a user were to press the "New Folder" button.add()

        This effectively gets a reference of the current folder open in the frontmost Finder window.

        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        .. versionadded:: 0.0.1
        """
        folder_obj = self.xa_scel.insertionLocation().get()
        return self._new_element(folder_obj, XAFinderFolder)

    # def make(self, type: str, at: str, name_and_ext: str):
    #     script = f"{self.specifier}.make({{new: '{type}', at: Path('{at}'), withProperties: {{name: '{name_and_ext}'}}}});"
    #     self.item.make()

    # Directories
    def directory(self, path: Union[str, NSURL]):
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)
        
    def home_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's home directory.

        :return: A PyXA reference to the user's home directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = fm.homeDirectoryForCurrentUser()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def temp_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the temporary directory for the current user.

        :return: A PyXA reference to the user's temporary directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = fm.temporaryDirectory()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def documents_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's documents directory.

        :return: A PyXA reference to the user's documents directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Documents")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def downloads_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's downloads directory.

        :return: A PyXA reference to the user's downloads directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Downloads")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def pictures_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's pictures directory.

        :return: A PyXA reference to the user's pictures directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Pictures")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def movies_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's movies directory.

        :return: A PyXA reference to the user's movies directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Movies")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def music_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's music directory.

        :return: A PyXA reference to the user's music directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Music")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def public_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the public directory.

        :return: A PyXA reference to the public directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Public")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def applications_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the system applications directory.

        :return: A PyXA reference to the system applications directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_("/Applications")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def trash_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's trash directory.

        :return: A PyXA reference to the user's trash directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Trash")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    # Folders
    def folders(self, filter: dict = None) -> List['XAFinderFolder']:
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("folders", filter, XAFinderFolder)

    def folder(self, filter: Union[int, dict]) -> 'XAFinderFolder':
        """Returns the first folder that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("folders", filter, XAFinderFolder)

    def first_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the first index of the folders array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("folders", XAFinderFolder)

    def last_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the last (-1) index of the folders array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("folders", XAFinderFolder)

    # Files
    def files(self, filter: dict = None) -> List['XAFinderFile']:
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("files", filter, XAFinderFile)

    def file(self, filter: Union[int, dict]) -> 'XAFinderFile':
        """Returns the first file that matches the filter.

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("files", filter, XAFinderFile)

    def first_file(self) -> 'XAFinderFile':
        """Returns the file at the first index of the files array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("files", XAFinderFile)

    def last_file(self) -> 'XAFinderFile':
        """Returns the file at the last (-1) index of the files array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("files", XAFinderFile)


class XAFinderItem(XABase.XARevealable, XABase.XASelectable, XABase.XADeletable):
    """A generic class with methods common to the various item classes of Finder.

    .. seealso:: :class:`XAFinderContainer`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name = self.xa_elem.name() #: The name of the item
        self.displayed_name = self.xa_elem.displayedName() #: The user-visible name of the item
        self.name_extension = self.xa_elem.nameExtension() #: The file extension of the item
        self.extension_hidden = self.xa_elem.extensionHidden() #: Whether the file extension is hidden
        self.index = self.xa_elem.index() #: The index within the containing folder/disk
        self.position = self.xa_elem.position() #: The position of the item within the parent window
        self.desktop_position = self.xa_elem.position() #: The position of an item on the desktop
        self.bounds = self.xa_elem.bounds() #: The bounding rectangle of an item
        self.label_index = self.xa_elem.labelIndex() #: The label assigned to the item
        self.locked = self.xa_elem.locked() #: Whether the file is locked
        self.kind = self.xa_elem.kind() #: The kind of the item, e.g. "Folder" or "File"
        self.description = self.xa_elem.description() #: The description of the item
        self.comment = self.xa_elem.comment() #: The user-specified comment on the item
        self.size: int = self.xa_elem.size() #: The logical size of the item
        self.physical_size: int = self.xa_elem.size() #: The actual disk space used by the item
        self.creation_date = self.xa_elem.creationDate() #: The date the item was created
        self.modification_date = self.xa_elem.modificationDate() #: The date the item was last modified
        self.url = self.xa_elem.URL() #: The URL of the item
        self.owner = self.xa_elem.owner() #: The name of the user that owns the item
        self.group = self.xa_elem.group() #: The name of the group that has access to the item
        self.owner_privileges = self.xa_elem.ownerPrivileges() #: The privilege level of the owner, e.g. "read only"
        self.group_privileges = self.xa_elem.groupPrivileges() #: The privilege level of the group, e.g. "write only"
        self.everyones_privileges = self.xa_elem.everyonesPrivileges() #: The privilege level of everyone else, e.g. "none"

        self.__container = None
        self.__disk = None
        self.__icon = None
        self.__information_window = None

    @property
    def container(self):
        """The containing folder or disk
        """
        if self.__container is None:
            container_obj = self.xa_elem.container()
            kind = container_obj.kind()
            if kind == "Folder":
                self.__container = self._new_element(container_obj, XAFinderFolder)
            elif kind == "Volume":
                self.__container = self._new_element(container_obj, XAFinderDisk)
            elif kind == "":
                # TODO: Computer container 
                pass
        return self.__container

    @property
    def disk(self):
        """The disk that the item is stored on
        """
        if self.__disk is None:
            obj = self.xa_elem.disk()
            self.__disk = self._new_element(obj, XAFinderDisk)
        return self.__disk

    @property
    def icon(self):
        """The item's icon bitmap
        """
        pass

    @property
    def information_window(self):
        """The information window for the item
        """
        pass

    def copy(self) -> 'XAFinderItem':
        """Copies the item to the clipboard.

        :return: A reference to the Finder item that called this method.
        :rtype: XAFinderItem

        .. versionadded:: 0.0.1
        """
        url = NSURL.alloc().initWithString_(self.URL).absoluteURL()
        self.set_clipboard(url)
        return self

    def move_to(self, new_path: Union[str, NSURL], overwrite: bool = False) -> 'XAFinderItem':
        """Moves the item to the specified path.

        :param new_path: The path to move the item to.
        :type new_path: Union[str, NSURL]
        :param overwrite: Whether to overwrite existing files of the same name at the target path, defaults to False
        :type overwrite: bool, optional
        :return: A reference to the Finder item that called this method.
        :rtype: XAFinderItem

        .. versionadded:: 0.0.1
        """
        if isinstance(new_path, str):
            new_path = NSURL.alloc().initFileURLWithPath_(new_path)
        old_path = NSURL.alloc().initWithString_(self.URL)
        fm.moveItemAtURL_toURL_error_(old_path, new_path, None)
        return self

    def exists(self) -> bool:
        """Checks whether the item exists on the disk or not.

        :return: True if the item exists, false otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.exists()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"

class XAFinderContainer(XAFinderItem, XABase.XAHasElements):
    """A class for managing and interacting with containers in Finder.

    .. seealso:: :class:`XAFinderDisk`, :class:`XAFinderFolder`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__entire_contents = None
        self.__container_window = None

    @property
    def entire_contents(self):
        """The entire contents of the container, including the contents of its children (recursive)
        """
        if self.__entire_contents is None:
            self.__entire_contents = self.__get_contents()
        return self.__entire_contents

    def __get_contents(self):
        elements = []
        for folder in self.folders():
            elements.append(folder.__get_contents())
        for file in self.files():
            elements.append(file)
        return elements

    @property
    def container_window(self):
        """An object with the properties of the window that contains or would contain this folder
        """
        pass

    # Folders
    def folders(self, filter: dict = None) -> List['XAFinderFolder']:
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.elements("folders", filter, XAFinderFolder)

    def folder(self, filter: Union[int, dict]) -> 'XAFinderFolder':
        """Returns the first folder that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.element_with_properties("folders", filter, XAFinderFolder)

    def first_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the first index of the folders array.

        .. versionadded:: 0.0.2
        """
        return self.first_element("folders", XAFinderFolder)

    def last_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the last (-1) index of the folders array.

        .. versionadded:: 0.0.2
        """
        return self.last_element("folders", XAFinderFolder)

    # Files
    def files(self, filter: dict = None) -> List['XAFinderFile']:
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.2
        """
        return self.elements("files", filter, XAFinderFile)

    def file(self, filter: Union[int, dict]) -> 'XAFinderFile':
        """Returns the first file that matches the filter.

        .. versionadded:: 0.0.2
        """
        return self.element_with_properties("files", filter, XAFinderFile)

    def first_file(self) -> 'XAFinderFile':
        """Returns the file at the first index of the files array.

        .. versionadded:: 0.0.2
        """
        return self.first_element("files", XAFinderFile)

    def last_file(self) -> 'XAFinderFile':
        """Returns the file at the last (-1) index of the files array.

        .. versionadded:: 0.0.2
        """
        return self.last_element("files", XAFinderFile)


class XAFinderDisk(XAFinderContainer, XABase.XARevealable, XABase.XASelectable, XABase.XADeletable):
    """A class for managing and interacting with disks in Finder.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.xa_elem.id() #: A unique identifier for the disk that is persistent for as long as the disc is connected and Finder is running
        self.capacity = self.xa_elem.capacity() #: The total number of bytes on the disk
        self.free_space = self.xa_elem.freeSpace() #: The number of free bytes left on the disk
        self.ejectable = self.xa_elem.ejectable() #: Whether the disk can be ejected
        self.local_volume = self.xa_elem.localVolume() #: Whether the disk is a local volume vs. a file server
        self.startup = self.xa_elem.startup() #: Whether the disk is the boot disk
        self.format = self.xa_elem.format() #: The format of the disk, e.g. "APFS format"
        self.journaling_enabled = self.xa_elem.journalingEnabled() #: Whether the disk does file system journaling
        self.ignore_privileges = self.xa_elem.ignorePrivileges() #: Whether to ignore permissions on the disk


class XAFinderFolder(XAFinderContainer):
    """A class for managing and interacting with folders in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderDesktop(XAFinderContainer):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderTrash(XAFinderContainer):
    """A class for managing and interacting with Finder's Trash.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.warns_before_emptying: bool = self.xa_elem.warnsBeforeEmptying() #: Whether to display a dialog before emptying the Trash


class XAFinderFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_type = self.xa_elem.fileType() #: The OSType of the file and the data within it
        self.creator_type = self.xa_elem.creatorType() #: The OSType of the application that created the file
        self.stationery = self.xa_elem.stationery() #: Whether the file is a stationery pad
        self.product_version = self.xa_elem.productVersion() #: The version of the application the file was created with
        self.version = self.xa_elem.version() #: The version of the file