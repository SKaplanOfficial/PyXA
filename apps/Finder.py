""".. versionadded:: 0.0.1

Control Finder using JXA-like syntax.
"""

from typing import List, Union
from Foundation import NSFileManager

from AppKit import NSString, NSURL

import XABase
import XABaseScriptable

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

    def resolve_symlinks(self, path: str) -> str:
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

        .. seealso:: :func:`select_files`

        .. versionadded:: 0.0.1
        """
        path = self.resolve_symlinks(path)
        self.properties["workspace"].selectFile_inFileViewerRootedAtPath_(path, None)
        return self

    def select_items(self, paths: List[str]) -> 'XAFinderApplication':
        """Selects the files or folders at the specified paths.
        
        This opens a new tab of Finder for each different parent folder in the list of paths to select.

        :param path: The paths to select.
        :type filepath: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        .. seealso:: :func:`select_file`

        .. versionadded:: 0.0.1
        """
        paths = [self.resolve_symlinks(x) for x in paths]
        self.properties["workspace"].activateFileViewerSelectingURLs_(paths)
        return self

    def recycle_item(self, path: Union[str, NSURL]) -> 'XAFinderApplication':
        """Moves the file or folder at the specified path to the trash.

        :param path: The path of the file or folder to recycle.
        :type path: Union[str, NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

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

        .. versionadded:: 0.0.1
        """
        self.properties["sb_element"].emptySecurity_(True)
        return self

    def delete_item(self, path: Union[str, NSURL]) -> 'XAFinderApplication':
        """Permanently deletes the file or folder at the specified path.

        :param path: The path of the file or folder to delete.
        :type path: Union[str, NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

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

        .. seealso:: :func:`recycle_item`

        .. versionadded:: 0.0.1
        """
        for path in paths:
            self.recycle_item(path)
        return self

    def duplicate_item(self, path: str) -> 'XAFinderApplication':
        """Duplicates the specified file or folder in its containing folder.

        The duplicated item will have the name of the original with " 2" added to the end.

        :param path: The path of the file or folder to duplicate.
        :type path: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

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
        self.properties["workspace"].showSearchResultsForQueryString_(query)
        return self

    def get_labels(self) -> List[str]:
        """Gets the list of file labels.

        :return: The list of file labels.
        :rtype: str

        .. versionadded:: 0.0.1
        """
        return self.properties["workspace"].fileLabels()

    def selection(self) -> List['XAFinderItem']:
        """Obtains PyXA references to the selected items in Finder.

        :return: The list of selected items.
        :rtype: List[XAFinderItem]

        .. versionadded:: 0.0.1
        """
        selected_items = []
        items = self.properties["sb_element"].selection().get()
        for item in items:
            kind = item.kind()
            if kind == "Folder":
                selected_items.append(self._new_element(item, XAFinderFolder))
            else:
                selected_items.append(self._new_element(item, XAFinderFile))
        return selected_items

    def insertion_location(self) -> 'XAFinderApplication':
        """Gets a reference to the directory in which a new folder would be created if a user were to press the "New Folder" button.add()

        This effectively gets a reference of the current folder open in the frontmost Finder window.

        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        .. versionadded:: 0.0.1
        """
        folder_obj = self.properties["sb_element"].insertionLocation().get()
        return self._new_element(folder_obj, XAFinderFolder)

    # def make(self, type: str, at: str, name_and_ext: str):
    #     script = f"{self.specifier}.make({{new: '{type}', at: Path('{at}'), withProperties: {{name: '{name_and_ext}'}}}});"
    #     self.item.make()

    # Directories
    def directory(self, path: Union[str, NSURL]):
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)
        
    def home_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's home directory.

        :return: A PyXA reference to the user's home directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = fm.homeDirectoryForCurrentUser()
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def temp_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the temporary directory for the current user.

        :return: A PyXA reference to the user's temporary directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = fm.temporaryDirectory()
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def documents_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's documents directory.

        :return: A PyXA reference to the user's documents directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Documents")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def downloads_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's downloads directory.

        :return: A PyXA reference to the user's downloads directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Downloads")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def pictures_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's pictures directory.

        :return: A PyXA reference to the user's pictures directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Pictures")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def movies_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's movies directory.

        :return: A PyXA reference to the user's movies directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Movies")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def music_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's music directory.

        :return: A PyXA reference to the user's music directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Music")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def public_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the public directory.

        :return: A PyXA reference to the public directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Public")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def applications_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the system applications directory.

        :return: A PyXA reference to the system applications directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_("/Applications")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def trash_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's trash directory.

        :return: A PyXA reference to the user's trash directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(fm.homeDirectoryForCurrentUser().path() + "/Trash")
        folder_obj = self.properties["sb_element"].folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    # Folders
    def folders(self, filter: dict = None) -> List['XAFinderFolder']:
        """Returns a list of folders matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("folders", filter, XAFinderFolder)

    def folder(self, filter: Union[int, dict]) -> 'XAFinderFolder':
        """Returns the first folder that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("folders", filter, XAFinderFolder)

    def first_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the first index of the folders array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("folders", XAFinderFolder)

    def last_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the last (-1) index of the folders array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("folders", XAFinderFolder)

    # Files
    def files(self, filter: dict = None) -> List['XAFinderFile']:
        """Returns a list of files matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("files", filter, XAFinderFile)

    def file(self, filter: Union[int, dict]) -> 'XAFinderFile':
        """Returns the first file that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("files", filter, XAFinderFile)

    def first_file(self) -> 'XAFinderFile':
        """Returns the file at the first index of the files array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("files", XAFinderFile)

    def last_file(self) -> 'XAFinderFile':
        """Returns the file at the last (-1) index of the files array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("files", XAFinderFile)

class XAFinderItem(XABase.XARevealable, XABase.XASelectable, XABase.XADeletable):
    """A generic class with methods common to the various item classes of Finder.

    .. seealso:: :class:`XAFinderFolder`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

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
        return self.properties["element"].exists()

    # Folders
    def folders(self, filter: dict = None) -> List['XAFinderFolder']:
        """Returns a list of folders matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("folders", filter, XAFinderFolder)

    def folder(self, filter: Union[int, dict]) -> 'XAFinderFolder':
        """Returns the first folder that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("folders", filter, XAFinderFolder)

    def first_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the first index of the folders array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("folders", XAFinderFolder)

    def last_folder(self) -> 'XAFinderFolder':
        """Returns the folder at the last (-1) index of the folders array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("folders", XAFinderFolder)

    # Files
    def files(self, filter: dict = None) -> List['XAFinderFile']:
        """Returns a list of files matching the filter.

        .. seealso:: :func:`scriptable_elements`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("files", filter, XAFinderFile)

    def file(self, filter: Union[int, dict]) -> 'XAFinderFile':
        """Returns the first file that matches the filter.

        .. seealso:: :func:`scriptable_element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("files", filter, XAFinderFile)

    def first_file(self) -> 'XAFinderFile':
        """Returns the file at the first index of the files array.

        .. seealso:: :func:`first_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("files", XAFinderFile)

    def last_file(self) -> 'XAFinderFile':
        """Returns the file at the last (-1) index of the files array.

        .. seealso:: :func:`last_scriptable_element`

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("files", XAFinderFile)


class XAFinderFolder(XAFinderItem):
    """A class for managing and interacting with folders in Finder.

    .. seealso:: :class:`XAFinderItem`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAFinderFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. seealso:: :class:`XAFinderItem`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)