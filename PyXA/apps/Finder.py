""".. versionadded:: 0.0.1

Control Finder using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Any, List, Tuple, Union
from Foundation import NSFileManager

from AppKit import NSString, NSURL, NSArray, NSPoint, NSValue, NSMakeRect
from ScriptingBridge import SBObject

from PyXA import XABase
from PyXA.XABase import OSType, XAImage, XAList
from PyXA import XABaseScriptable

class XAFinderApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Finder.app.

    .. versionchanged:: 0.0.3

       Added methods and properties to reach parity with Finder.h.

    .. versionadded:: 0.0.1
    """
    class PrivacySetting(Enum):
        """Options for privacy settings on Finder items.
        """
        READ_ONLY   = OSType('read')
        READ_WRITE  = OSType('rdwr')
        WRITE_ONLY  = OSType('writ')
        NONE        = OSType('none')

    class ItemFormat(Enum):
        """Options for file and disk formats of Finder items.
        """
        MACOS               = OSType('dfhf')
        MACOS_EXTENDED      = OSType('dfh+')
        UFS                 = OSType('dfuf')
        NFS                 = OSType('dfnf')
        AUDIO               = OSType('dfau')
        PRO_DOS             = OSType('dfpr')
        MSDOS               = OSType('dfms')
        NTFS                = OSType('dfnt')
        ISO9660             = OSType('df96')
        HIGH_SIERRA         = OSType('dfhs')
        QUICKTAKE           = OSType('dfqt')
        APPLE_PHOTO         = OSType('dfph')
        APPLE_SHARE         = OSType('dfas')
        UDF                 = OSType('dfud')
        WEBDAV              = OSType('dfwd')
        FTP                 = OSType('dfft')
        PACKET_WRITTEN_UDF  = OSType('dfpu')
        XSAN                = OSType('dfac')
        APFS                = OSType('dfap')
        EXFAT               = OSType('dfxf')
        SMB                 = OSType('dfsm')
        UNKNOWN             = OSType('df\?\?')

    class Panel(Enum):
        """Options for information panels in Finder.
        """
        GENERAL_INFORMATION     = OSType('gpnl')
        SHARING                 = OSType('spnl')
        MEMORY                  = OSType('mpnl')
        PREVIEW                 = OSType('vpnl')
        APPLICATION             = OSType('apnl')
        LANGUAGES               = OSType('pklg')
        PLUGINS                 = OSType('pkpg')
        NAME_EXTENSION          = OSType('npnl')
        COMMENTS                = OSType('cpnl')
        CONTENT_INDEX           = OSType('cinl')
        BURNING                 = OSType('bpnl')
        MORE_INFO               = OSType('minl')
        SIMPLE_HEADER           = OSType('shnl')
        GENERAL_PREFERENCES     = OSType('pgnp')
        LABEL_PREFERENCES       = OSType('plbp')
        SIDEBAR_PREFERENCES     = OSType('psid')
        ADVANCED_PREFERENCES    = OSType('padv')

    class ViewSetting(Enum):
        """View options for lists of items in Finder windows.
        """
        ICON_VIEW   = OSType('icnv')
        LIST_VIEW   = OSType('lsvw')
        COLUMN_VIEW = OSType('clvw')
        GROUP_VIEW  = OSType('flvw')
        FLOW_VIEW   = OSType('flvw')

    class Arrangement(Enum):
        """Arrangement options for lists of items in Finder windows.
        """
        NOT_ARRANGED            = OSType('narr')
        SNAP_TO_GRID            = OSType('grda')
        BY_NAME                 = OSType('nama')
        BY_MODIFICATION_DATE    = OSType('mdta')
        BY_CREATION_DATE        = OSType('cdta')
        BY_SIZE                 = OSType('siza')
        BY_KIND                 = OSType('kina')
        BY_LABEL                = OSType('laba')

    class LabelPosition(Enum):
        """Options for the label position of items in Finder windows.
        """
        RIGHT   = OSType('lrgt')
        BOTTOM  = OSType('lbot')

    class SortDirection(Enum):
        """Options for sort direction of lists of Finder items.
        """
        NORMAL      = OSType('snrm')
        REVERSED    = OSType('srvs')

    class ColumnName(Enum):
        """Columns in Finder windows.
        """
        NAME            = OSType('esln')
        MODIFICATE_DATE = OSType('elsm')
        CREATION_DATE   = OSType('elsc')
        SIZE            = OSType('elss')
        KIND            = OSType('elsk')
        LABEL           = OSType('elsl')
        VERSION         = OSType('elsv')
        COMMENT         = OSType('elsC')

    class IconSize(Enum):
        """Options for the size of icons in Finder windows.
        """
        SMALL   = OSType('smic')
        LARGE   = OSType('lgic')

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFinderWindow
        self.xa_fmgr = NSFileManager.defaultManager()

        self.name: str #: The name of Finder
        self.visible: bool #: Whether Finder is currently visible
        self.frontmost: bool #: Whether Finder is the active application
        self.product_version: str #: The system software version
        self.version: str #: The version of Finder
        self.selection: XAFinderItemList #: The currently selected items in Finder
        self.insertion_location: XAFinderFolder #: The container in which a new folder would be created in by default in the frontmost window
        self.startup_disk: XAFinderDisk #: The startup disk for this system
        self.desktop: XAFinderDesktop #: The user's desktop
        self.trash: XAFinderTrash #: The system Trash
        self.home: XAFinderFolder #: The home directory
        self.computer_container #: The computer directory
        self.finder_preferences #: Preferences for Finder as a whole
        self.desktop_picture: XAFinderFile #: The desktop picture of the main monitor

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def product_version(self) -> str:
        return self.xa_scel.productVersion()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def selection(self) -> 'XAFinderItemList':
        return self._new_element(self.xa_scel.selection().get(), XAFinderItemList)

    @property
    def insertion_location(self) -> 'XAFinderApplication':
        folder_obj = self.xa_scel.windows()[0].target()
        return self._new_element(folder_obj, XAFinderFolder)

    @property
    def startup_disk(self) -> 'XAFinderDisk':
        disk_obk = self.xa_scel.startupDisk()
        return self._new_element(disk_obk, XAFinderDisk)

    @property
    def desktop(self) -> 'XAFinderDesktop':
        desktop_obj = self.xa_scel.desktop()
        return self._new_element(desktop_obj, XAFinderDesktop)

    @property
    def trash(self) -> 'XAFinderTrash':
        trash_obj = self.xa_scel.trash()
        return self._new_element(trash_obj, XAFinderTrash)

    @property
    def home(self) -> 'XAFinderFolder':
        return self.home_directory()

    @property
    def computer_container(self) -> 'XAFinderComputer':
        computer_obj = self.xa_scel.computerContainer()
        return self._new_element(computer_obj, XAFinderComputer)

    @property
    def finder_preferences(self) -> 'XAFinderPreferences':
        prefs_obj = self.xa_scel.FinderPreferences()
        return self._new_element(prefs_obj, XAFinderPreferences)

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
        
        This opens a new tab of Finder for each different parent folder in the list of paths to select. This method utilizes fast specialized methods from Objective-C to improve the performance of selecting large amounts of files. As such, when dealing with multiple file paths, this method should always be used instead of calling :func:`select_item` repeatedly.

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
        self.temp_urls = []
        def resolve(path: Union[str, NSURL], index: int, stop: bool):
            url = NSURL.alloc().initWithString_(self._resolve_symlinks(path))
            self.temp_urls.append(url)
        NSArray.alloc().initWithArray_(paths).enumerateObjectsUsingBlock_(resolve)
        self.xa_wksp.activateFileViewerSelectingURLs_(self.temp_urls)
        return self

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
            if path.startswith("file://"):
                path = NSURL.alloc().initWithString_(path)
            else:
                path = NSURL.alloc().initFileURLWithPath_(path)
        self.xa_fmgr.trashItemAtURL_resultingItemURL_error_(path, None, None)
        return self

    def recycle_items(self, paths: List[Union[str, NSURL]]) -> 'XAFinderApplication':
        """Moves the files or folders at the specified paths to the trash.

        This method utilizes fast enumeration methods from Objective-C to improve the performance of recycling large amounts of files. As such, it is preferred over calling :func:`recycle_item` repeatedly, especially when dealing with large lists of paths.

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
        def recycle(path: Union[str, NSURL], index: int, stop: bool):
            self.recycle_item(path)
        NSArray.alloc().initWithArray_(paths).enumerateObjectsUsingBlock_(recycle)
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
            if path.startswith("file://"):
                path = NSURL.alloc().initWithString_(path)
            else:
                path = NSURL.alloc().initFileURLWithPath_(path)
        self.xa_fmgr.removeItemAtURL_error_(path, None)
        return self

    def delete_items(self, paths: List[Union[str, NSURL]]) -> 'XAFinderApplication':
        """Permanently deletes the files or folders at the specified paths.

        This method utilizes fast enumeration methods from Objective-C to improve the performance of deleting large amounts of files. As such, it is preferred over calling :func:`delete_item` repeatedly, especially when dealing with large lists of paths.

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
        def delete(path: Union[str, NSURL], index: int, stop: bool):
            self.delete_item(path)
        NSArray.alloc().initWithArray_(paths).enumerateObjectsUsingBlock_(delete)
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
            if path.startswith("file://"):
                path = NSURL.alloc().initWithString_(path)
            else:
                path = NSURL.alloc().initFileURLWithPath_(path)
        new_path = path

        copy_num = 1
        while new_path.checkResourceIsReachableAndReturnError_(None)[0]:
            if path.hasDirectoryPath():
                new_path = path.path() + f" {copy_num}"
            else:
                new_path = path.path().replace("." + path.pathExtension(), f" {copy_num}." + path.pathExtension())
            new_path = NSURL.alloc().initFileURLWithPath_(new_path)
            copy_num += 1
        self.xa_fmgr.copyItemAtURL_toURL_error_(path, new_path, None)
        return self

    def duplicate_items(self, paths: List[str]) -> 'XAFinderApplication':
        """Duplicates the specified files or folders in their containing folder.

        The duplicated items will have the name of the original with " 2" added to the end. This method utilizes fast enumeration methods from Objective-C to improve the performance of duplicating large amounts of files. As such, it is preferred over calling :func:`duplicate_item` repeatedly, especially when dealing with large lists of paths.

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
        def duplicate(path: Union[str, NSURL], index: int, stop: bool):
            self.duplicate_item(path)
        NSArray.alloc().initWithArray_(paths).enumerateObjectsUsingBlock_(duplicate)
        return self

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
        path = self.xa_fmgr.homeDirectoryForCurrentUser()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def temp_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the temporary directory for the current user.

        :return: A PyXA reference to the user's temporary directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = self.xa_fmgr.temporaryDirectory()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def documents_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's documents directory.

        :return: A PyXA reference to the user's documents directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Documents")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def downloads_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's downloads directory.

        :return: A PyXA reference to the user's downloads directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Downloads")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def pictures_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's pictures directory.

        :return: A PyXA reference to the user's pictures directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Pictures")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def movies_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's movies directory.

        :return: A PyXA reference to the user's movies directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Movies")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def music_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the current user's music directory.

        :return: A PyXA reference to the user's music directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Music")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def public_directory(self) -> 'XAFinderFolder':
        """Obtains a reference to the public directory.

        :return: A PyXA reference to the public directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Public")
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
        path = NSURL.alloc().initFileURLWithPath_(self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Trash")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def items(self, filter: dict = None) -> 'XAFinderItemList':
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.items(), XAFinderItemList, filter)

    def containers(self, filter: dict = None) -> 'XAFinderContainerList':
        """Returns a list of containers matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.containers(), XAFinderContainerList, filter)

    def disks(self, filter: dict = None) -> 'XAFinderDiskList':
        """Returns a list of disks matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.disks(), XAFinderDiskList, filter)

    def folders(self, filter: dict = None) -> 'XAFinderFolderList':
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.folders(), XAFinderFolderList, filter)

    def files(self, filter: dict = None) -> 'XAFinderFileList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.files(), XAFinderFileList, filter)

    def alias_files(self, filter: dict = None) -> 'XAFinderAliasFileList':
        """Returns a list of alias files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.aliasFiles(), XAFinderAliasFileList, filter)

    def application_files(self, filter: dict = None) -> 'XAFinderApplicationFileList':
        """Returns a list of application files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.applicationFiles(), XAFinderApplicationFileList, filter)

    def document_files(self, filter: dict = None) -> 'XAFinderDocumentFileList':
        """Returns a list of document files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.documentFiles(), XAFinderDocumentFileList, filter)

    def internet_location_files(self, filter: dict = None) -> 'XAFinderInternetLocationFileList':
        """Returns a list of internet location files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.internetLocationFiles(), XAFinderInternetLocationFileList, filter)

    def clippings(self, filter: dict = None) -> 'XAFinderClippingList':
        """Returns a list of clippings matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.clippings(), XAFinderClippingList, filter)

    def packages(self, filter: dict = None) -> 'XAFinderPackageList':
        """Returns a list of packages matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.packages(), XAFinderPackageList, filter)

    def finder_windows(self, filter: dict = None) -> 'XAFinderFinderWindowList':
        """Returns a list of Finder windows matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.finderWindows(), XAFinderFinderWindowList, filter)

    def clipping_windows(self, filter: dict = None) -> 'XAFinderClippingWindowList':
        """Returns a list of clipping windows matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.clippingWindows(), XAFinderClippingWindowList, filter)


class XAFinderItemList(XABase.XAList):
    """A wrapper around lists of Finder items that employs fast enumeration techniques.

    All properties of Finder items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, object_class = None, filter: Union[dict, None] = None):
        if object_class is None:
            object_class = XAFinderItem
        super().__init__(properties, object_class, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def displayed_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def name_extension(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("nameExtension"))

    def extension_hidden(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("extensionHidden"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def desktop_position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("desktopPosition"))

    def bounds(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def label_index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("labelIndex"))

    def locked(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def kind(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def description(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("description"))

    def comment(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def size(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def physical_size(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize"))

    def creation_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def owner(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("owner"))

    def group(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("group"))

    def owner_privileges(self) -> List[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("ownerPrivileges"))

    def group_privileges(self) -> List[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("groupPrivileges"))

    def everyone_privileges(self) -> List[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("everyonePrivileges"))

    def container(self) -> 'XAFinderContainerList':
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XAFinderContainerList)

    def disk(self) -> 'XAFinderDiskList':
        ls = self.xa_elem.arrayByApplyingSelector_("disk")
        return self._new_element(ls, XAFinderDiskList)

    def icon(self) -> XABase.XAImageList:
        ls = self.xa_elem.arrayByApplyingSelector_("icon")
        return self._new_element(ls, XABase.XAImageList)

    def information_window(self) -> 'XAFinderInformationWindowList':
        ls = self.xa_elem.arrayByApplyingSelector_("informationWindow")
        return self._new_element(ls, XAFinderInformationWindowList)

    def by_name(self, name: str) -> 'XAFinderItem':
        return self.by_property("name", name)

    def by_displayed_name(self, displayed_name: str) -> 'XAFinderItem':
        return self.by_property("displayedName", displayed_name)

    def by_name_extension(self, name_extension: str) -> 'XAFinderItem':
        return self.by_property("nameExtension", name_extension)

    def by_extension_hidden(self, extension_hidden: bool) -> 'XAFinderItem':
        return self.by_property("extensionHidden", extension_hidden)

    def by_index(self, index: int) -> 'XAFinderItem':
        return self.by_property("index", index)

    def by_position(self, position: Tuple[int, int]) -> 'XAFinderItem':
        return self.by_property("position", position)

    def by_desktop_position(self, desktop_position: Tuple[int, int]) -> 'XAFinderItem':
        return self.by_property("desktopPosition", desktop_position)

    def by_bounds(self, bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> 'XAFinderItem':
        return self.by_property("bounds", bounds)

    def by_label_index(self, label_index: index) -> 'XAFinderItem':
        return self.by_property("labelIndex", label_index)

    def by_locked(self, locked: bool) -> 'XAFinderItem':
        return self.by_property("locked", locked)

    def by_kind(self, kind: str) -> 'XAFinderItem':
        return self.by_property("kind", kind)

    def by_description(self, description: str) -> 'XAFinderItem':
        return self.by_property("description", description)

    def by_comment(self, comment: str) -> 'XAFinderItem':
        return self.by_property("comment", comment)

    def by_size(self, size: int) -> 'XAFinderItem':
        return self.by_property("size", size)

    def by_physical_size(self, physical_size: int) -> 'XAFinderItem':
        return self.by_property("physicalSize", physical_size)

    def by_creation_date(self, creation_date: datetime) -> 'XAFinderItem':
        return self.by_property("creationDate", creation_date)

    def by_modification_date(self, modification_date: datetime) -> 'XAFinderItem':
        return self.by_property("modificationDate", modification_date)

    def by_url(self, url: str) -> 'XAFinderItem':
        return self.by_property("URL", url)

    def by_owner(self, owner: str) -> 'XAFinderItem':
        return self.by_property("owner", owner)

    def by_group(self, group: str) -> 'XAFinderItem':
        return self.by_property("group", group)

    def by_owner_privileges(self, owner_privileges: XAFinderApplication.PrivacySetting) -> 'XAFinderItem':
        return self.by_property("ownerPrivileges", owner_privileges)

    def by_group_privileges(self, group_privileges: XAFinderApplication.PrivacySetting) -> 'XAFinderItem':
        return self.by_property("groupPrivileges", group_privileges)

    def by_everyone_privileges(self, everyone_privileges: XAFinderApplication.PrivacySetting) -> 'XAFinderItem':
        return self.by_property("everyonePrivileges", everyone_privileges)

    def by_container(self, container: 'XAFinderContainer') -> 'XAFinderItem':
        return self.by_property("container", container.xa_elem)

    def by_disk(self, disk: 'XAFinderDisk') -> 'XAFinderItem':
        return self.by_property("disk", disk.xa_elem)

    def by_icon(self, icon: XAImage) -> 'XAFinderItem':
        return self.by_property("icon", icon.value)

    def by_information_window(self, information_window: 'XAFinderInformationWindow') -> 'XAFinderItem':
        return self.by_property("informationWindow", information_window.xa_elem)

    def __repr__(self):
        return str(self.name())

class XAFinderItem(XABase.XASelectable, XABase.XADeletable):
    """A generic class with methods common to the various item classes of Finder.

    .. seealso:: :class:`XAFinderContainer`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict #: Every property of an item
        self.name: str #: The name of the item
        self.displayed_name: str #: The user-visible name of the item
        self.name_extension: str #: The file extension of the item
        self.extension_hidden: bool #: Whether the file extension is hidden
        self.index: int #: The index within the containing folder/disk
        self.position: Tuple[int, int] #: The position of the item within the parent window
        self.desktop_position: Tuple[int, int] #: The position of an item on the desktop
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of an item
        self.label_index: int #: The label assigned to the item
        self.locked: bool #: Whether the file is locked
        self.kind: str #: The kind of the item, e.g. "Folder" or "File"
        self.description: str #: The description of the item
        self.comment: str #: The user-specified comment on the item
        self.size: int #: The logical size of the item
        self.physical_size: int #: The actual disk space used by the item
        self.creation_date: datetime #: The date the item was created
        self.modification_date: datetime #: The date the item was last modified
        self.url: str #: The URL of the item
        self.owner: str #: The name of the user that owns the item
        self.group: str #: The name of the group that has access to the item
        self.owner_privileges: XAFinderApplication.PrivacySetting #: The privilege level of the owner, e.g. "read only"
        self.group_privileges: XAFinderApplication.PrivacySetting #: The privilege level of the group, e.g. "write only"
        self.everyones_privileges: XAFinderApplication.PrivacySetting #: The privilege level of everyone else, e.g. "none"
        self.container: XAFinderContainer #: The container of the item
        self.disk: XAFinderDisk #: The disk on which the item is stored
        self.icon: XABase.XAImage #: The icon bitmap of the item's icon
        self.information_window: XAFinderWindow #: The information window for this item

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def name_extension(self) -> str:
        return self.xa_elem.nameExtension()

    @property
    def extension_hidden(self) -> bool:
        return self.xa_elem.extensionHidden()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    @property
    def desktop_position(self) -> Tuple[int, int]:
        return self.xa_elem.desktopPosition()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def label_index(self) -> int:
        return self.xa_elem.labelIndex()

    @property
    def locked(self) -> bool:
        return self.xa_elem.locked()

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def description(self) -> str:
        return self.xa_elem.description()

    @property
    def comment(self) -> str:
        return self.xa_elem.comment()

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def physical_size(self) -> int:
        return self.xa_elem.physicalSize()

    @property
    def creation_date(self) -> datetime:
        return self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def url(self) -> str:
        return self.xa_elem.URL()

    @property
    def owner(self) -> str:
        return self.xa_elem.owner()

    @property
    def group(self) -> str:
        return self.xa_elem.group()

    @property
    def owner_privileges(self) -> XAFinderApplication.PrivacySetting:
        return self.xa_elem.ownerPrivileges()

    @property
    def group_privileges(self) -> XAFinderApplication.PrivacySetting:
        return self.xa_elem.groupPrivileges()

    @property
    def everyone_privileges(self) -> XAFinderApplication.PrivacySetting:
        return self.xa_elem.everyonePrivileges()

    @property
    def container(self) -> 'XAFinderContainer':
        container_obj = self.xa_elem.container()
        kind = container_obj.kind()
        if kind == "Folder":
            return self._new_element(container_obj, XAFinderFolder)
        elif kind == "Volume":
            return self._new_element(container_obj, XAFinderDisk)
        elif kind == "":
            # TODO: Computer container 
            print("item container todo")
            pass

    @property
    def disk(self) -> 'XAFinderDisk':
        disk_obj = self.xa_elem.disk()
        return self._new_element(disk_obj, XAFinderDisk)

    @property
    def icon(self) -> XAImage:
        icon_obj = self.xa_elem.icon()
        return self._new_element(icon_obj, XAImage)

    @property
    def information_window(self) -> 'XAFinderInformationWindow':
        window_obj = self.xa_elem.informationWindow()
        return self._new_element(window_obj, XAFinderInformationWindow)

    def reveal(self) -> 'XAFinderItem':
        """Reveals the item in the frontmost Finder window.

        :return: A reference to the item object
        :rtype: XAFinderItem

        .. versionadded:: 0.0.4
        """
        self.xa_elem.reveal()
        return self

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
        self.xa_fmgr.moveItemAtURL_toURL_error_(old_path, new_path, None)
        return self

    def exists(self) -> bool:
        """Checks whether the item exists on the disk or not.

        :return: True if the item exists, false otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.exists()

    def open(self):
        """Opens the item in its default application.

        .. versionadded:: 0.0.2
        """
        url = NSURL.alloc().initWithString_(self.url)
        self.xa_wksp.openURL_(url)

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = NSValue.valueWithPoint_(NSPoint(value[0], value[1]))
            elif isinstance(value[0], tuple):
                # Value is a rectangle boundary
                x = value[0][0]
                y = value[0][1]
                w = value[1][0]
                h = value[1][1]
                value = NSValue.valueWithRect_(NSMakeRect(x, y, w, h))
        super().set_property(property_name, value)

    def delete(self):
        """Permanently deletes the item.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAFinderContainerList(XAFinderItemList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    All properties of containers can be called as methods on the wrapped list, returning a list with each container's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, object_class = None, filter: Union[dict, None] = None):
        if object_class is None:
            object_class = XAFinderContainer
        super().__init__(properties, object_class, filter)

    def entire_contents(self) -> List[XAFinderItemList]:
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents")

    def container_window(self) -> List['XAFinderFinderWindow']:
        ls = self.xa_elem.arrayByApplyingSelector_("containerWindow")
        return self._new_element(ls, XAFinderFinderWindowList)

    def items(self) -> XAFinderItemList:
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("items"), XAFinderItemList)

    def containers(self) -> 'XAFinderContainerList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("containers"), XAFinderContainerList)

    def folders(self) -> 'XAFinderFolderList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("folders"), XAFinderFolderList)

    def files(self) -> 'XAFinderFileList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("files"), XAFinderFileList)

    def alias_files(self) -> 'XAFinderAliasFileList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("aliasFiles"), XAFinderAliasFileList)

    def application_files(self) -> 'XAFinderApplicationFileList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("applicationFiles"), XAFinderApplicationFileList)

    def document_files(self) -> 'XAFinderDocumentFileList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("documentFiles"), XAFinderDocumentFileList)

    def internet_location_files(self) -> 'XAFinderInternetLocationFileList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("internetLocationFiles"), XAFinderInternetLocationFileList)

    def clippings(self) -> 'XAFinderClippingList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("clippings"), XAFinderClippingList)

    def packages(self) -> 'XAFinderPackageList':
        return self._new_element(self.xa_elem.arrayByApplyingSelector_("packages"), XAFinderPackageList)

    def by_entire_contents(self, entire_contents: XAFinderItemList) -> 'XAFinderContainer':
        return self.by_property("entireContents", entire_contents.xa_elem)

    def by_container_window(self, container_window: 'XAFinderFinderWindow') -> 'XAFinderContainer':
        return self.by_property("containerWindow", container_window.xa_elem)

class XAFinderContainer(XAFinderItem, XABase.XAHasElements):
    """A class for managing and interacting with containers in Finder.

    .. seealso:: :class:`XAFinderDisk`, :class:`XAFinderFolder`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.entire_contents: XABaseScriptable.XASBObject #: The entire contents of the container, including the contents of its children
        self.container_window: XAFinderFinderWindow #: The container window for this folder

    @property
    def entire_contents(self):
        obj = self.xa_elem.entireContents().get()
        return self._new_element(obj, XAFinderItemList)

    @property
    def container_window(self):
        window_obj = self.xa_elem.containerWindow()
        return self._new_element(window_obj, XABaseScriptable.XASBObject)

    def items(self, filter: dict = None) -> 'XAFinderItemList':
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.items(), XAFinderItemList, filter)

    def containers(self, filter: dict = None) -> 'XAFinderContainerList':
        """Returns a list of containers matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.containers(), XAFinderContainerList, filter)

    def folders(self, filter: dict = None) -> 'XAFinderFolderList':
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.folders(), XAFinderFolderList, filter)

    def files(self, filter: dict = None) -> 'XAFinderFileList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.files(), XAFinderFileList, filter)

    def alias_files(self, filter: dict = None) -> 'XAFinderAliasFileList':
        """Returns a list of alias files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.aliasFiles(), XAFinderAliasFileList, filter)

    def application_files(self, filter: dict = None) -> 'XAFinderApplicationFileList':
        """Returns a list of application files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.applicationFiles(), XAFinderApplicationFileList, filter)

    def document_files(self, filter: dict = None) -> 'XAFinderDocumentFileList':
        """Returns a list of document files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.documentFiles(), XAFinderDocumentFileList, filter)

    def internet_location_files(self, filter: dict = None) -> 'XAFinderInternetLocationFileList':
        """Returns a list of internet location files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.internetLocationFiles(), XAFinderInternetLocationFileList, filter)

    def clippings(self, filter: dict = None) -> 'XAFinderClippingList':
        """Returns a list of clippings matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.clippings(), XAFinderClippingList, filter)

    def packages(self, filter: dict = None) -> 'XAFinderPackageList':
        """Returns a list of packages matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.packages(), XAFinderPackageList, filter)


class XAFinderDiskList(XAFinderContainerList):
    """A wrapper around lists of disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderDisk, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def capacity(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity"))

    def free_space(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace"))

    def ejectable(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable"))

    def local_volume(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume"))

    def startup(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("startup"))

    def format(self) -> List[XAFinderApplication.ItemFormat]:
        return list(self.xa_elem.arrayByApplyingSelector_("format"))

    def journaling_enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("journalingEnabled"))

    def ignore_privileges(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ignorePrivileges"))

    def by_id(self, id: int) -> 'XAFinderDisk':
        return self.by_property("id", id)

    def by_capacity(self, capacity: int) -> 'XAFinderDisk':
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> 'XAFinderDisk':
        return self.by_property("freeSpace", free_space)

    def by_ejectable(self, ejectable: bool) -> 'XAFinderDisk':
        return self.by_property("ejectable", ejectable)

    def by_local_volume(self, local_volume: bool) -> 'XAFinderDisk':
        return self.by_property("localVolume", local_volume)

    def by_startup(self, startup: bool) -> 'XAFinderDisk':
        return self.by_property("startup", startup)

    def by_format(self, format: XAFinderApplication.ItemFormat) -> 'XAFinderDisk':
        return self.by_property("format", format)

    def by_journaling_enabled(self, journaling_enabled: bool) -> 'XAFinderDisk':
        return self.by_property("journalingEnabled", journaling_enabled)

    def by_ignore_privileges(self, ignore_privileges: bool) -> 'XAFinderDisk':
        return self.by_property("ignorePrivileges", ignore_privileges)

class XAFinderDisk(XAFinderContainer):
    """A class for managing and interacting with disks in Finder.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: A unique identifier for the disk that is persistent for as long as the disc is connected and Finder is running
        self.capacity: int #: The total number of bytes on the disk
        self.free_space: int #: The number of free bytes left on the disk
        self.ejectable: bool #: Whether the disk can be ejected
        self.local_volume: bool #: Whether the disk is a local volume vs. a file server
        self.startup: bool#: Whether the disk is the boot disk
        self.format: XAFinderApplication.ItemFormat #: The format of the disk, e.g. "APFS format"
        self.journaling_enabled: bool #: Whether the disk does file system journaling
        self.ignore_privileges: bool #: Whether to ignore permissions on the disk

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def capacity(self) -> int:
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        return self.xa_elem.freeSpace()

    @property
    def ejectable(self) -> bool:
        return self.xa_elem.ejectable()

    @property
    def local_volume(self) -> bool:
        return self.xa_elem.localVolume()

    @property
    def startup(self) -> bool:
        return self.xa_elem.startup()

    @property
    def format(self) -> XAFinderApplication.ItemFormat:
        return self.xa_elem.format()

    @property
    def journaling_enabled(self) -> bool:
        return self.xa_elem.journalingEnabled()

    @property
    def ignore_privileges(self) -> bool:
        return self.xa_elem.ignorePrivileges()


class XAFinderFolderList(XAFinderContainerList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFolder, filter)

class XAFinderFolder(XAFinderContainer):
    """A class for managing and interacting with folders in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderTrash(XAFinderContainer):
    """A class for managing and interacting with Finder's Trash.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.warns_before_emptying: bool #: Whether to display a dialog before emptying the Trash

    @property
    def warns_before_emptying(self) -> bool:
        return self.xa_elem.warnsBeforeEmptying() 


class XAFinderComputer(XAFinderItem):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderFileList(XAFinderItemList):
    """A wrapper around lists of files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFile, filter)

    def file_type(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def creator_type(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def stationery(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def product_version(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def version(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_file_type(self, file_type: int) -> 'XAFinderFile':
        return self.by_property("fileType", file_type)

    def by_creator_type(self, creator_type: int) -> 'XAFinderFile':
        return self.by_property("creatorType", creator_type)

    def by_stationery(self, stationery: bool) -> 'XAFinderFile':
        return self.by_property("stationery", stationery)

    def by_product_version(self, product_version: str) -> 'XAFinderFile':
        return self.by_property("productVersion", product_version)

    def by_version(self, version: str) -> 'XAFinderFile':
        return self.by_property("version", version)

class XAFinderFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.file_type: int #: The OSType of the file and the data within it
        self.creator_type: int #: The OSType of the application that created the file
        self.stationery: bool #: Whether the file is a stationery pad
        self.product_version: str #: The version of the application the file was created with
        self.version: str #: The version of the file

    @property
    def file_type(self) -> int:
        return self.xa_elem.fileType()

    @property
    def creator_type(self) -> int:
        return self.xa_elem.creatorType()

    @property
    def stationery(self) -> bool:
        return self.xa_elem.stationery()

    @property
    def product_version(self) -> str:
        return self.xa_elem.productVersion()

    @property
    def version(self) -> str:
        return self.xa_elem.version()


class XAFinderAliasFileList(XAFinderFileList):
    """A wrapper around lists of alias files that employs fast enumeration techniques.

    All properties of alias files can be called as methods on the wrapped list, returning a list containing each alias files's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderAliasFile, filter)

    def original_item(self) -> List[XAFinderItem]:
        return list(self.xa_elem.arrayByApplyingSelector_("originalItem"))

    def by_original_item(self, original_item: XAFinderItem) -> 'XAFinderAliasFile':
        return self.by_property("originalItem", original_item)

class XAFinderAliasFile(XAFinderFile):
    """A class for managing and interacting with alias files in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.original_item: XAFinderItem #: The original item pointed to by the alias

    @property
    def original_item(self) -> XAFinderItem:
        item_obj = self.xa_elem.originalItem()
        return self._new_element(item_obj, XAFinderItem)


class XAFinderApplicationFileList(XAFinderFileList):
    """A wrapper around lists of application files that employs fast enumeration techniques.

    All properties of application files can be called as methods on the wrapped list, returning a list containing each application file's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderApplicationFile, filter)

    def id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def has_scripting_terminology(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hasScriptingTerminology"))

    def by_id(self, id: str) -> 'XAFinderApplicationFile':
        return self.by_property("id", id)

    def by_has_scripting_terminology(self, has_scripting_terminology: bool) -> 'XAFinderApplicationFile':
        return self.by_property("hasScriptingTerminology", has_scripting_terminology)

class XAFinderApplicationFile(XAFinderFile):
    """A class for managing and interacting with application files in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: str #: The bundle identifier or creator type of the application
        self.has_scripting_terminology: bool #: Whether the process can be scripted

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def has_scripting_terminology(self) -> bool:
        return self.xa_elem.hasScriptingTerminology()


class XAFinderDocumentFileList(XAFinderFileList):
    """A wrapper around lists of document files that employs fast enumeration techniques.

    All properties of document files can be called as methods on the wrapped list, returning a list containing each document file's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderDocumentFile, filter)

class XAFinderDocumentFile(XAFinderFile):
    """A class for managing and interacting with document files in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderInternetLocationFileList(XAFinderFileList):
    """A wrapper around lists of internet location files that employs fast enumeration techniques.

    All properties of internet location files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderInternetLocationFile, filter)

    def location(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("location"))

    def by_location(self, location: str) -> 'XAFinderInternetLocationFile':
        return self.by_property("location", location)

class XAFinderInternetLocationFile(XAFinderFile):
    """A class for managing and interacting with internet location files in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.location: str #: The internet location

    @property
    def location(self) -> str:
        return self.xa_elem.location()


class XAFinderClippingList(XAFinderFileList):
    """A wrapper around lists of clippings that employs fast enumeration techniques.

    All properties of clippings can be called as methods on the wrapped list, returning a list containing each clipping's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderClipping, filter)

class XAFinderClipping(XAFinderFile):
    """A class for managing and interacting with clippings in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPackageList(XAFinderItemList):
    """A wrapper around lists of packages that employs fast enumeration techniques.

    All properties of packages can be called as methods on the wrapped list, returning a list containing each package's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderPackage, filter)

class XAFinderPackage(XAFinderItem):
    """A class for managing and interacting with packages in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderWindowList(XAList):
    """A wrapper around lists of Finder windows that employs fast enumeration techniques.

    All properties of Finder windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderPackage, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def position(self) -> List[Tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def bounds(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def titled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("titled"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def index(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def closeable(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("closeable"))

    def floating(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("floating"))

    def modal(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modal"))

    def resizable(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("resizable"))

    def zoomable(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable"))

    def zoomed(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed"))

    def visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def collapsed(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed"))

    def properties(self) -> List[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def by_id(self, id: int) -> 'XAFinderWindow':
        return self.by_property("id", id)

    def by_position(self, position: Tuple[int, int]) -> 'XAFinderWindow':
        return self.by_property("position", position)

    def by_bounds(self, bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> 'XAFinderWindow':
        return self.by_property("bounds", bounds)

    def by_titled(self, titled: bool) -> 'XAFinderWindow':
        return self.by_property("titled", titled)

    def by_name(self, name: str) -> 'XAFinderWindow':
        return self.by_property("name", name)

    def by_index(self, index: int) -> 'XAFinderWindow':
        return self.by_property("index", index)

    def by_closeable(self, closeable: bool) -> 'XAFinderWindow':
        return self.by_property("closeable", closeable)

    def by_floating(self, floating: bool) -> 'XAFinderWindow':
        return self.by_property("floating", floating)

    def by_modal(self, modal: bool) -> 'XAFinderWindow':
        return self.by_property("modal", modal)

    def by_resizable(self, resizable: bool) -> 'XAFinderWindow':
        return self.by_property("resizable", resizable)

    def by_zoomable(self, zoomable: bool) -> 'XAFinderWindow':
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> 'XAFinderWindow':
        return self.by_property("zoomed", zoomed)

    def by_visible(self, visible: bool) -> 'XAFinderWindow':
        return self.by_property("visible", visible)

    def by_collapsed(self, collapsed: bool) -> 'XAFinderWindow':
        return self.by_property("collapsed", collapsed)

    def by_properties(self, properties: dict) -> 'XAFinderWindow':
        return self.by_property("properties", properties)

class XAFinderWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with windows of Finder.app.

    :Example 1: Setting the bounds of a Finder window

    >>> import PyXA
    >>> app = PyXA.application("Finder")
    >>> window = app.windows()[0]
    >>> lock = False
    >>> (old_w, old_h) = (0,0)
    >>> while True:
    >>>     if window.position.y < 50 and lock is False:
    >>>         # Increase height of window when user drags it to the top
    >>>         (old_w, old_h) = window.bounds.size
    >>>         (x, y) = window.position
    >>>         window.set_property("bounds", ((x, y), (old_w, 2000)))
    >>>         lock = True
    >>>     if lock is True and window.position.y > 55:
    >>>         # Return to original size if user moves window down
    >>>         (x, y) = window.position
    >>>         window.set_property("bounds", ((x, y), (old_w, old_h)))
    >>>         lock = False

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id: int #: The unique identifier for the window
        self.position: Tuple[int, int] #: The upper left position of the window
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The boundary rectangle for the window
        self.titled: bool #: Whether the window has a title bar
        self.name: str #: The name of the window
        self.index: int #: The index of the window in the front-to-back order of Finder windows
        self.closeable: bool #: Whether the window has a close button
        self.floating: bool #: Whether the window has a title bar
        self.modal: bool #: Whether the window is modal
        self.resizable: bool #: Whether the window can be resized
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is zoomed
        self.visible: bool #: Whether the window is visible
        self.collapsed: bool #: Whether the window is collapsed
        self.properties: dict #: Every property of a Finder window

    @property
    def id(self) -> int:
        return self.xa_elem.id()

    @property
    def position(self) -> Tuple[int, int]:
        return self.xa_elem.position()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_elem.bounds()

    @property
    def titled(self) -> bool:
        return self.xa_elem.titled()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def closeable(self) -> bool:
        return self.xa_elem.closeable()

    @property
    def floating(self) -> bool:
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        return self.xa_elem.modal()

    @property
    def resizable(self) -> bool:
        return self.xa_elem.resizable()

    @property
    def zoomable(self) -> bool:
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_elem.zoomed()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()

    @property
    def collapsed(self) -> bool:
        return self.xa_elem.collapsed()

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    def set_property(self, property_name: str, value: Any):
        if isinstance(value, tuple):
            if isinstance(value[0], int):
                # Value is a position
                value = NSValue.valueWithPoint_(NSPoint(value[0], value[1]))
            elif isinstance(value[0], tuple):
                # Value is a rectangle boundary
                x = value[0][0]
                y = value[0][1]
                w = value[1][0]
                h = value[1][1]
                value = NSValue.valueWithRect_(NSMakeRect(x, y, w, h))
        super().set_property(property_name, value)


class XAFinderFinderWindowList(XAFinderItemList):
    """A wrapper around lists of Finder internal windows (such as preference and information windows) that employs fast enumeration techniques.

    All properties of the windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFinderWindow, filter)

    def current_view(self) -> List[XAFinderApplication.ViewSetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentView"))

    def toolbar_visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("toolbarVisible"))

    def statusbar_visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("statusbarVisible"))

    def pathbar_visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("pathbarVisible"))

    def sidebar_width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("sidebarWidth"))

    def target(self) -> List[XAFinderContainer]:
        ls = self.xa_elem.arrayByApplyingSelector_("target")
        return self._new_element(ls, XAFinderContainerList)

    def icon_view_options(self) -> List['XAFinderIconViewOptions']:
        return list(self.xa_elem.arrayByApplyingSelector_("iconViewOptions"))

    def list_view_options(self) -> List['XAFinderListViewOptions']:
        return list(self.xa_elem.arrayByApplyingSelector_("listViewOptions"))

    def column_view_options(self) -> List['XAFinderColumnViewOptions']:
        return list(self.xa_elem.arrayByApplyingSelector_("columnViewOptions"))

    def by_current_view(self, current_view: XAFinderApplication.ViewSetting) -> 'XAFinderFinderWindow':
        return self.by_property("currentView", current_view)

    def by_toolbar_visible(self, toolbar_visible: bool) -> 'XAFinderFinderWindow':
        return self.by_property("toolbarVisible", toolbar_visible)

    def by_statusbar_visible(self, statusbar_visible: bool) -> 'XAFinderFinderWindow':
        return self.by_property("statusbarVisible", statusbar_visible)

    def by_pathbar_visible(self, pathbar_visible: bool) -> 'XAFinderFinderWindow':
        return self.by_property("pathbarVisible", pathbar_visible)

    def by_sidebar_width(self, sidebar_width: int) -> 'XAFinderFinderWindow':
        return self.by_property("sidebarWidth", sidebar_width)

    def by_target(self, target: XAFinderContainer) -> 'XAFinderFinderWindow':
        return self.by_property("target", target)

    def by_icon_view_options(self, icon_view_options: 'XAFinderIconViewOptions') -> 'XAFinderFinderWindow':
        return self.by_property("iconViewOptions", icon_view_options)

    def by_list_view_options(self, list_view_options: 'XAFinderListViewOptions') -> 'XAFinderFinderWindow':
        return self.by_property("listViewOptions", list_view_options)

    def by_column_view_options(self, column_view_options: 'XAFinderColumnViewOptions') -> 'XAFinderFinderWindow':
        return self.by_property("columnViewOptions", column_view_options)

class XAFinderFinderWindow(XAFinderWindow):
    """A class for managing and interacting with internal windows within Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.current_view: XAFinderApplication.ViewSetting #: The current view for the container window
        self.toolbar_visible: bool #: Whether the window's toolbar is visible
        self.statusbar_visible: bool #: Whether the window's status bar is visible
        self.pathbar_visible: bool #: Whether the window's path bar is visible
        self.sidebar_width: int #: The width of the sidebar in pixels
        self.target: XAFinderContainer #: The container at which this file viewer is targeted
        self.icon_view_options: XAFinderIconViewOptions #: The icon view options for the container window
        self.list_view_options: XAFinderListViewOptions #: The list view options for the container window
        self.column_view_options: XAFinderColumnViewOptions #: The column view options for the container window

    @property
    def current_view(self) -> XAFinderApplication.ViewSetting:
        return self.xa_elem.currentView()

    @property
    def toolbar_visible(self) -> bool:
        return self.xa_elem.toolbarVisible()

    @property
    def statusbar_visible(self) -> bool:
        return self.xa_elem.statusbarVisible()

    @property
    def pathbar_visible(self) -> bool:
        return self.xa_elem.pathbarVisible()

    @property
    def sidebar_width(self) -> int:
        return self.xa_elem.sidebarWidth()

    @property
    def target(self) -> XAFinderContainer:
        obj = self.xa_elem.target()
        return self._new_element(obj, XAFinderContainer)

    @property
    def icon_view_options(self) -> 'XAFinderIconViewOptions':
        options_obj = self.xa_elem.iconViewOptions()
        return self._new_element(options_obj, XAFinderIconViewOptions)

    @property
    def list_view_options(self) -> 'XAFinderListViewOptions':
        options_obj = self.xa_elem.listViewOptions()
        return self._new_element(options_obj, XAFinderListViewOptions)

    @property
    def column_view_options(self) -> 'XAFinderColumnViewOptions':
        options_obj = self.xa_elem.columnViewOptions()
        return self._new_element(options_obj, XAFinderColumnViewOptions)


class XAFinderDesktop(XAFinderContainer):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAFinderDesktopWindow(XAFinderWindow):
    """A class representing the containing window around Finder's desktop element.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderClippingWindowList(XAFinderItemList):
    """A wrapper around lists of clipping windows that employs fast enumeration techniques.

    All properties of clipping windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderClippingWindow, filter)

class XAFinderClippingWindow(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with clipping windows in Finder.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPreferences(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing general preferences of Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.folders_spring_open: bool #: Whether folders spring open after a delay
        self.delay_before_springing: float #: The delay, in seconds, before springing open folders
        self.desktop_shows_hard_disks: bool #: Whether hard drives appear on the desktop
        self.desktop_shows_external_hard_disks: bool #: Whether external hard disks appear on the desktop
        self.desktop_shows_removable_media: bool #: Whether CDs, DVDs, and iPods appear on the desktop
        self.desktop_shows_connected_servers: bool #: Whether connected servers appear on the desktop
        self.folders_open_in_new_windows: bool #: Whether folders open into new windows
        self.folders_open_in_new_tabs: bool #: Whether folders open into new tabs
        self.new_windows_open_in_column_view: bool #: Whether new Finder windows open in column view
        self.all_name_extensions_showing: bool #: Whether all name extensions are shown regardless of the "extension hidden" setting
        self.window: XAFinderPreferencesWindow #: The Finder preferences window
        self.icon_view_options: XAFinderIconViewOptions #: The default icon view options
        self.list_view_options: XAFinderListViewOptions #: The default list view options
        self.column_view_options: XAFinderColumnViewOptions #: The default column view options
        self.new_window_target: SBObject #: The target location for a newly opened Finder window

    @property
    def folders_spring_open(self) -> bool:
        return self.xa_elem.foldersSpringOpen()

    @property
    def delay_before_springing(self) -> bool:
        return self.xa_elem.delayBeforeSpringing()

    @property
    def desktop_shows_hard_disks(self) -> bool:
        return self.xa_elem.desktopShowsHardDisks()

    @property
    def desktop_shows_external_hard_disks(self) -> bool:
        return self.xa_elem.desktopShowsExternalHardDisks()

    @property
    def desktop_shows_removable_media(self) -> bool:
        return self.xa_elem.desktopShowsRemovableMedia()

    @property
    def desktop_shows_connected_servers(self) -> bool:
        return self.xa_elem.desktopShowsConnectedServers()

    @property
    def folders_open_in_new_windows(self) -> bool:
        return self.xa_elem.foldersOpenInNewWindows()

    @property
    def folders_open_in_new_tabs(self) -> bool:
        return self.xa_elem.foldersOpenInNewTabs()

    @property
    def new_windows_open_in_column_view(self) -> bool:
        return self.xa_elem.newWindowsOpenInColumnView()

    @property
    def all_name_extensions_showing(self) -> bool:
        return self.xa_elem.allNameExtensionsShowing()

    @property
    def window(self) -> bool:
        window_obj = self.xa_elem.window()
        return self._new_element(window_obj, XAFinderPreferencesWindow)

    @property
    def icon_view_options(self) -> 'XAFinderIconViewOptions':
        options_obj = self.xa_elem.iconViewOptions()
        return self._new_element(options_obj, XAFinderIconViewOptions)

    @property
    def list_view_options(self) -> 'XAFinderListViewOptions':
        options_obj = self.xa_elem.listViewOptions()
        return self._new_element(options_obj, XAFinderListViewOptions)

    @property
    def column_view_options(self) -> 'XAFinderColumnViewOptions':
        options_obj = self.xa_elem.columnViewOptions()
        return self._new_element(options_obj, XAFinderColumnViewOptions)

    @property
    def new_window_target(self) -> XAFinderAliasFile:
        target_obj = self.xa_elem.newWindowTarget()
        return self._new_element(target_obj, XAFinderAliasFile)

class XAFinderPreferencesWindow(XAFinderWindow):
    """A class for managing and interacting with preference windows in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.current_panel: XAFinderApplication.Panel #: The current panel in the Finder preferences window

    @property
    def current_panel(self) -> XAFinderApplication.Panel:
        return self.xa_elem.currentPanel()


class XAFinderInformationWindowList(XAFinderWindowList):
    """A wrapper around lists of info windows that employs fast enumeration techniques.

    All properties of info windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderClippingWindow, filter)

    def item(self) -> XAFinderItemList:
        ls = self.xa_elem.arrayByApplyingSelector_("item")
        return self._new_element(ls, XAFinderItemList)

    def current_panel(self) -> List[XAFinderApplication.Panel]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentPanel"))

    def by_item(self, item: XAFinderItem) -> 'XAFinderInformationWindow':
        return self.by_property("item", item)

    def by_current_panel(self, current_panel: XAFinderApplication.Panel) -> 'XAFinderInformationWindow':
        return self.by_property("currentPanel", current_panel)

class XAFinderInformationWindow(XAFinderWindow):
    """A class for interacting with information windows in Finder.app.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.item: XAFinderItem #: The item from which this window was opened
        self.current_panel: XAFinderApplication.Panel #: The current panel in the information window

    @property
    def item(self) -> XAFinderItem:
        item_obj = self.xa_elem.item()
        return self._new_element(item_obj, XAFinderItem)

    @property
    def current_panel(self) -> XAFinderApplication.Panel:
        return self.xa_elem.currentPanel()


class XAFinderIconViewOptions(XABaseScriptable.XASBObject):
    """A class representing the icon view options of a Finder window.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.arrangement: XAFinderApplication.Arrangement #: The arrangement setting of icons in icon view
        self.icon_size: int #: The size of icons in icon view
        self.shows_item_info: bool #: Whether additional item information is shown in the window
        self.shows_icon_preview: bool #: Whether a preview of the icon is shown in the window
        self.text_size: int #: The size of text in icon view
        self.label_position: XAFinderApplication.LabelPosition #: The size of icon label in icon view
        self.background_picture: XAFinderFile #: The background picture of the icon view
        self.background_color: XABase.XAColor #: The background color of the icon view

    @property
    def arrangement(self) -> XAFinderApplication.Arrangement:
        return self.xa_elem.arrangement()

    @property
    def icon_size(self) -> int:
        return self.xa_elem.iconSize()

    @property
    def shows_item_info(self) -> bool:
        return self.xa_elem.showsItemInfo()

    @property
    def shows_icon_preview(self) -> bool:
        return self.xa_elem.showsIconPreview()

    @property
    def text_size(self) -> int:
        return self.xa_elem.textSize()

    @property
    def label_position(self) -> XAFinderApplication.LabelPosition:
        return self.xa_elem.labelPosition()

    @property
    def background_picture(self) -> XAFinderFile:
        bg_obj = self.xa_elem.backgroundPicture()
        return self._new_element(bg_obj, XAFinderFile)

    @property
    def background_color(self) -> XABase.XAColor:
        bg_obj = self.xa_elem.backgroundColor()
        return self._new_element(bg_obj, XABase.XAColor)


class XAFinderColumnViewOptions(XABaseScriptable.XASBObject):
    """A class representing the column view options of a Finder window.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.text_size: int #: The size of text in the column view
        self.shows_icon: bool #: Whether icons are shown in the column view
        self.shows_icon_preview: bool #: Whether icon previews are shown in the column view
        self.shows_preview_column: bool #: Whether the preview column is shown in the column view
        self.discloses_preview_pane: bool #: Whether the preview pane is disclosed in the column view

    @property
    def text_size(self) -> int:
        return self.xa_elem.textSize()

    @property
    def shows_icon(self) -> bool:
        return self.xa_elem.showsIcon()

    @property
    def shows_icon_preview(self) -> bool:
        return self.xa_elem.showsIconPreview()

    @property
    def shows_preview_column(self) -> bool:
        return self.xa_elem.showsPreviewColumn()

    @property
    def discloses_preview_pane(self) -> bool:
        return self.xa_elem.disclosesPreviewPane()


class XAFinderListViewOptions(XABaseScriptable.XASBObject):
    """A class representing the list view options in a Finder window.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.calculates_folder_sizes: bool #: Whether folder sizes are calculated and displayed in the window
        self.shows_icon_preview: bool #: Whether a preview of the item is shown in the window
        self.icon_size: XAFinderApplication.IconSize #: The size of icons in the window
        self.text_size: int #: The size of text in the window
        self.uses_relative_dates: bool #: The column that the list view is sorted on
        self.sort_column: XAFinderColumn #: Whether relative dates are shown in the window

    @property
    def calculates_folder_sizes(self) -> bool:
        return self.xa_elem.calculatesFolderSizes()

    @property
    def shows_icon_preview(self) -> bool:
        return self.xa_elem.showsIconPreview()

    @property
    def icon_size(self) -> XAFinderApplication.IconSize:
        return self.xa_elem.iconSize()

    @property
    def text_size(self) -> int:
        return self.xa_elem.textSize()

    @property
    def uses_relative_dates(self) -> bool:
        return self.xa_elem.usesRelativeDates()

    @property
    def sort_column(self) -> 'XAFinderColumn':
        column_obj = self.xa_elem.sortColumn()
        return self._new_element(column_obj, XAFinderColumn)

    def columns(self, filter: dict = None) -> 'XAFinderColumn':
        """Returns a list of columns matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.columns(), XAFinderColumn, filter)


class XAFinderColumnList(XABase.XAList):
    """A wrapper around lists of Finder columns that employs fast enumeration techniques.

    All properties of Finder columns can be called as methods on the wrapped list, returning a list containing each columns's value for the property.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderColumn, filter)

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def sort_direction(self) -> List[XAFinderApplication.SortDirection]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortDirection"))

    def width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def minimum_width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("minimum_width"))

    def maximum_width(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximum_width"))

    def visible(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def by_index(self, index: int) -> 'XAFinderColumn':
        return self.by_property("index", index)

    def by_name(self, name: str) -> 'XAFinderColumn':
        return self.by_property("name", name)

    def by_sort_direction(self, sort_direction: XAFinderApplication.SortDirection) -> 'XAFinderColumn':
        return self.by_property("sortDirection", sort_direction.value)

    def by_width(self, width: int) -> 'XAFinderColumn':
        return self.by_property("width", width)

    def by_minimum_width(self, minimum_width: int) -> 'XAFinderColumn':
        return self.by_property("minimumWidth", minimum_width)

    def by_maximum_width(self, maximum_width: int) -> 'XAFinderColumn':
        return self.by_property("maximumWidth", maximum_width)

    def by_visible(self, visible: bool) -> 'XAFinderColumn':
        return self.by_property("visible", visible)

class XAFinderColumn(XABaseScriptable.XASBObject):
    """A class for managing and interacting with columns in Finder windows.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.index: int #: The index of the column in the front-to-back ordering within the containing window
        self.name: XAFinderApplication.ColumnName.value #: The column name
        self.sort_direction: XAFinderApplication.SortDirection.value #: The direction which the window is sorted
        self.width: int #: The current width of the column in pixels
        self.minimum_width: int #: The minimum width allowed for the column in pixels
        self.maximum_width: int #: The maximum width allowed for the column in pixels
        self.visible: bool #: Whether the column is visible

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def name(self) -> XAFinderApplication.ColumnName:
        return self.xa_elem.name()

    @property
    def sort_direction(self) -> XAFinderApplication.SortDirection:
        return self.xa_elem.sortDirection()

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @property
    def minimum_width(self) -> int:
        return self.xa_elem.minimumWidth()

    @property
    def maximum_width(self) -> int:
        return self.xa_elem.maximumWidth()

    @property
    def visible(self) -> bool:
        return self.xa_elem.visible()