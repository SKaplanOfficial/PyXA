""".. versionadded:: 0.0.1

Control Finder using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from operator import contains
import os
from select import select
import threading
from time import sleep
from typing import List, Tuple, Union
from Foundation import NSFileManager

from AppKit import NSString, NSURL, NSArray
from ScriptingBridge import SBObject
from numpy import isin

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

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
        self.xa_fmgr = NSFileManager.defaultManager()

        self.name: str = self.xa_scel.name() #: The name of Finder
        self.visible: bool = self.xa_scel.visible() #: Whether Finder is currently visible
        self.frontmost: bool = self.xa_scel.frontmost() #: Whether Finder is the active application
        self.product_version: str = self.xa_scel.productVersion() #: The system software version
        self.version: str = self.xa_scel.version() #: The version of Finder

        self.selection: XAFinderItemList #: The currently selected items in Finder
        self.insertion_location: XAFinderFolder #: The container in which a new folder would be created in by default in the frontmost window
        self.startup_disk: XAFinderDisk #: The startup disk for this system
        self.desktop: XAFinderDesktop #: The user's desktop
        self.trash: XAFinderTrash #: The system Trash
        self.home: XAFinderFolder #: The home directory
        self.computer_container #: The computer directory
        self.finder_preferences #: Preferences for Finder as a whole

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
        print(self.temp_urls)
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

    def conainers(self, filter: dict = None) -> 'XAFinderContainerList':
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.containers(), XAFinderContainerList, filter)

    def disks(self, filter: dict = None) -> 'XAFinderDiskList':
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.1
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
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.aliasFiles(), XAFinderAliasFileList, filter)

    def application_files(self, filter: dict = None) -> 'XAFinderApplicationFileList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.applicationFiles(), XAFinderApplicationFileList, filter)

    def document_files(self, filter: dict = None) -> 'XAFinderDocumentFileList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.documentFiles(), XAFinderDocumentFileList, filter)

    def internet_location_files(self, filter: dict = None) -> 'XAFinderInternetLocationFileList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.internetLocationFiles(), XAFinderInternetLocationFileList, filter)

    def clippings(self, filter: dict = None) -> 'XAFinderClippingList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.clippings(), XAFinderClippingList, filter)

    def packages(self, filter: dict = None) -> 'XAFinderPackageList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.packages(), XAFinderPackageList, filter)

    def finder_windows(self, filter: dict = None) -> 'XAFinderFinderWindowList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.finderWindows(), XAFinderFinderWindowList, filter)

    def clipping_windows(self, filter: dict = None) -> 'XAFinderClippingWindowList':
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.clippingWindows(), XAFinderClippingWindowList, filter)


class XAFinderItemList(XABase.XAList):
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

    def extension_hidden(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("extensionHidden"))

    def index(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def position(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("position"))

    def desktop_position(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("desktopPosition"))

    def bounds(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

    def label_index(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("labelIndex"))

    def locked(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked"))

    def kind(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def description(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("description"))

    def comment(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def size(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def physical_size(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize"))

    def creation_date(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def url(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL"))

    def owner(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("owner"))

    def group(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("group"))

class XAFinderItem(XABase.XARevealable, XABase.XASelectable, XABase.XADeletable):
    """A generic class with methods common to the various item classes of Finder.

    .. seealso:: :class:`XAFinderContainer`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties = self.xa_elem.properties()
        self.name: str #: The name of the item
        self.displayed_name: str #: The user-visible name of the item
        self.name_extension: str #: The file extension of the item
        self.extension_hidden: bool #: Whether the file extension is hidden
        self.index: int #: The index within the containing folder/disk
        self.position: Tuple[int, int] #: The position of the item within the parent window
        self.desktop_position: Tuple[int, int] #: The position of an item on the desktop
        self.bounds: Tuple[int, int] #: The bounding rectangle of an item
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

        # self.__owner_privileges #: The privilege level of the owner, e.g. "read only"
        # self.__group_privileges #: The privilege level of the group, e.g. "write only"
        # self.__everyones_privileges #: The privilege level of everyone else, e.g. "none"

        self.container: XAFinderContainer
        self.disk: XAFinderDisk
        self.icon: XABase.XAImage
        # self.information_window: XAFinderWindow
        # TODO

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
    def bounds(self) -> Tuple[int, int]:
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

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAFinderContainerList(XABase.XAList):
    def __init__(self, properties: dict, object_class = None, filter: Union[dict, None] = None):
        if object_class is None:
            object_class = XAFinderContainer
        super().__init__(properties, object_class, filter)

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


class XAFinderDiskList(XABase.XAList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderDisk, filter)

class XAFinderDisk(XAFinderContainer):
    """A class for managing and interacting with disks in Finder.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.id = self.properties["id"] #: A unique identifier for the disk that is persistent for as long as the disc is connected and Finder is running
        self.capacity = self.properties["capacity"] #: The total number of bytes on the disk
        self.free_space = self.properties["freeSpace"] #: The number of free bytes left on the disk
        self.ejectable = self.properties["ejectable"] #: Whether the disk can be ejected
        self.local_volume = self.properties["localVolume"] #: Whether the disk is a local volume vs. a file server
        self.startup = self.properties["startup"] #: Whether the disk is the boot disk
        self.format = self.properties["format"] #: The format of the disk, e.g. "APFS format"
        self.journaling_enabled = self.properties["journalingEnabled"] #: Whether the disk does file system journaling
        self.ignore_privileges = self.properties["ignorePrivileges"] #: Whether to ignore permissions on the disk


class XAFinderFolderList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFolder, filter)

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

class XAFinderComputer(XAFinderContainer):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderFileList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFile, filter)

    def file_type(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def creator_type(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def stationery(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def product_version(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def version(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

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


class XAFinderAliasFileList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderAliasFile, filter)

class XAFinderList(XABaseScriptable.XASBObject):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAFinderAliasFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderApplicationFileList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderApplicationFile, filter)

class XAFinderApplicationFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderDocumentFileList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderDocumentFile, filter)

class XAFinderDocumentFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderInternetLocationFileList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderInternetLocationFile, filter)

class XAFinderInternetLocationFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderClippingList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderClipping, filter)

class XAFinderClipping(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPackageList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderPackage, filter)

class XAFinderPackage(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderFinderWindowList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderFinderWindow, filter)

class XAFinderFinderWindow(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderClippingWindowList(XAFinderItemList):
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderClippingWindow, filter)

class XAFinderClippingWindow(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPreferences(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAFinderIconViewOptions(XABaseScriptable.XASBObject):
    """A class representing the icon view options of a Finder window.

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.arrangement: XAFinderApplication.Arrangement.value #: The arrangement setting of icons in icon view
        self.icon_size: int #: The size of icons in icon view
        self.shows_item_info: bool #: Whether additional item information is shown in the window
        self.shows_icon_preview: bool #: Whether a preview of the icon is shown in the window
        self.text_size: int #: The size of text in icon view
        self.label_position: XAFinderApplication.LabelPosition.value #: The size of icon label in icon view
        self.background_picture: XAFinderFile #: The background picture of the icon view
        self.background_color: XABase.XAColor #: The background color of the icon view

    @property
    def arrangement(self) -> XAFinderApplication.Arrangement.value:
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
    def label_position(self) -> XAFinderApplication.LabelPosition.value:
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
        self.icon_size: XAFinderApplication.IconSize.value #: The size of icons in the window
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
    def icon_size(self) -> XAFinderApplication.IconSize.value:
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
    def name(self) -> XAFinderApplication.ColumnName.value:
        return self.xa_elem.name()

    @property
    def sort_direction(self) -> XAFinderApplication.SortDirection.value:
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