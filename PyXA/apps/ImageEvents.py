from datetime import datetime
from enum import Enum
from typing import Any, Callable, Tuple, Union, List, Dict

import AppKit
import ScriptingBridge

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAEvents import event_from_int
from ..XAProtocols import XACanOpenPath, XAClipboardCodable

class XAImageEventsApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for interacting with Image Events.app.

    .. versionadded:: 0.1.0
    """
    class Format(Enum):
        """Disk format options.
        """
        APPLE_PHOTO     = XABase.OSType("dfph")
        APPLESHARE      = XABase.OSType("dfas")
        AUDIO           = XABase.OSType("dfau")
        HIGH_SIERRA     = XABase.OSType("dfhs")
        ISO_9660        = XABase.OSType("fd96")
        MACOS_EXTENDED  = XABase.OSType("dfh+")
        MACOS           = XABase.OSType("dfhf")
        MSDOS           = XABase.OSType("dfms")
        NFS             = XABase.OSType("dfnf")
        PRODOS          = XABase.OSType("dfpr")
        QUICKTAKE       = XABase.OSType("dfqt")
        UDF             = XABase.OSType("dfud")
        UFS             = XABase.OSType("dfuf")
        UNKNOWN         = XABase.OSType("df$$")
        WEBDAV          = XABase.OSType("dfwd")

    class BitDepth(Enum):
        """Bit depth options.
        """
        BEST                            = XABase.OSType("best")
        BLACK_AND_WHITE                 = XABase.OSType("b&amp;w ")
        COLOR                           = XABase.OSType("colr")
        FOUR_COLORS                     = XABase.OSType("4clr")
        FOUR_GRAYS                      = XABase.OSType("4gry")
        GRAYSCALE                       = XABase.OSType("gray")
        MILLIONS_OF_COLORS              = XABase.OSType("mill")
        MILLIONS_OF_COLORS_PLUS         = XABase.OSType("mil+")
        SIXTEEN_COLORS                  = XABase.OSType("16cl")
        SIXTEEN_GRAYS                   = XABase.OSType("16gr")
        THOUSANDS_OF_COLORS             = XABase.OSType("thou")
        TWO_HUNDRED_FIFTY_SIX_COLORS    = XABase.OSType("256c")
        TWO_HUNDRED_FIFTY_SIX_GRAYS     = XABase.OSType("256g")

    class DeviceClass(Enum):
        """Profile device class options.
        """
        ABSTRACT    = XABase.OSType("abst")
        COLORSPACE  = XABase.OSType("spac")
        INPUT       = XABase.OSType("scnr")
        LINK        = XABase.OSType("link")
        MONITOR     = XABase.OSType("mntr")
        NAMED       = XABase.OSType("nmcl")
        OUTPUT      = XABase.OSType("prtr")
    
    class ConnectionSpace(Enum):
        """Profile connection space options.
        """
        LAB     = XABase.OSType("Lab ")
        XYZ     = XABase.OSType("XYZ ")

    class CompressionLevel(Enum):
        """Compression options.
        """
        HIGH    = XABase.OSType("high")
        MEDIUM  = XABase.OSType("medi")
        LOW     = XABase.OSType("low ")

    class FileType(Enum):
        """Image file type options.
        """
        BMP         = XABase.OSType("BMPf")
        GIF         = XABase.OSType("GIF ")
        JPEG        = XABase.OSType("JPEG")
        JPEG2       = XABase.OSType("jpg2")
        MACPAINT    = XABase.OSType("PNTG")
        PDF         = XABase.OSType("PDF ")
        PHOTOSHOP   = XABase.OSType("8BPS")
        PICT        = XABase.OSType("PICT")
        PNG         = XABase.OSType("PNGf")
        PSD         = XABase.OSType("pdf ")
        QUICKTIME   = XABase.OSType("qtif")
        SGI         = XABase.OSType(".SGI")
        TEXT        = XABase.OSType("TEXT")
        TGA         = XABase.OSType("tga ")
        TIFF        = XABase.OSType("TIFF")

    class ProfileQuality(Enum):
        """Profile quality options.
        """
        BEST    = XABase.OSType("Qua2")
        NORMAL  = XABase.OSType("Qua0")
        DRAFT   = XABase.OSType("Qua1")

    class ColorSpace(Enum):
        """Color space options.
        """
        CMYK            = XABase.OSType("CMYK")
        EIGHT_CHANNEL   = XABase.OSType("MCH8")
        EIGHT_COLOR     = XABase.OSType("8CLR")
        FIVE_CHANNEL    = XABase.OSType("MCH5")
        FIVE_COLOR      = XABase.OSType("5CLR")
        GRAY            = XABase.OSType("GRAY")
        LAB             = XABase.OSType("Lab ")
        NAMED           = XABase.OSType("NAME")
        RGB             = XABase.OSType("RGB ")
        SEVEN_CHANNEL   = XABase.OSType("MCH7")
        SEVEN_COLOR     = XABase.OSType("7CLR")
        SIX_CHANNEL     = XABase.OSType("MCH6")
        SIX_COLOR       = XABase.OSType("6CLR")
        XYZ             = XABase.OSType("XYZ ")

    class RenderingIntent(Enum):
        """Rendering intent options.
        """
        ABSOLUTE_COLORIMETRIC   = XABase.OSType("Rdr3")
        PERCEPTUAL               = XABase.OSType("Rdr0")
        RELATIVE_COLORIMETRIC   = XABase.OSType("R1r2")
        SATURATION              = XABase.OSType("Rdr2")

    class ImageQuality(Enum):
        """Image quality options.
        """
        BEST    = XABase.OSType("best")
        HIGH    = XABase.OSType("high")
        MEDIUM  = XABase.OSType("medi")
        LOW     = XABase.OSType("low ")
        LEAST   = XABase.OSType("leas")

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application.

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Image Events is the frontmost application.

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of the application.

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.version()

    @property
    def application_support_folder(self) -> 'XAImageEventsFolder':
        """The Application Support folder.

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.application_support_folder()

    @property
    def applications_folder(self) -> 'XAImageEventsFolder':
        """The user's Applications folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.applications_folder()

    @property
    def classic_domain(self) -> 'XAImageEventsClassicDomainObject':
        """the collection of folders belonging to the Classic System

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.classic_domain()

    @property
    def desktop_folder(self) -> 'XAImageEventsFolder':
        """The user's Desktop folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.desktop_folder()

    @property
    def desktop_pictures_folder(self) -> 'XAImageEventsFolder':
        """The Desktop Pictures folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.desktop_pictures_folder()

    @property
    def documents_folder(self) -> 'XAImageEventsFolder':
        """The user's Documents folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.documents_folder()

    @property
    def downloads_folder(self) -> 'XAImageEventsFolder':
        """The user's Downloads folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.downloads_folder()

    @property
    def favorites_folder(self) -> 'XAImageEventsFolder':
        """The user's Favorites folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.favorites_folder()

    @property
    def folder_action_scripts_folder(self) -> 'XAImageEventsFolder':
        """The user's Folder Action Scripts folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.folder_action_scripts_folder()

    @property
    def fonts_folder(self) -> 'XAImageEventsFolder':
        """The Fonts folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.fonts_folder()

    @property
    def home_folder(self) -> 'XAImageEventsFolder':
        """The Home folder of the currently logged in user

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.home_folder()

    @property
    def library_folder(self) -> 'XAImageEventsFolder':
        """The Library folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.library_folder()

    @property
    def local_domain(self) -> 'XAImageEventsLocalDomainObject':
        """the collection of folders residing on the Local machine

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.local_domain()

    @property
    def movies_folder(self) -> 'XAImageEventsFolder':
        """The user's Movies folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.movies_folder()

    @property
    def music_folder(self) -> 'XAImageEventsFolder':
        """The user's Music folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.music_folder()

    @property
    def network_domain(self) -> 'XAImageEventsNetworkDomainObject':
        """the collection of folders residing on the Network

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.network_domain()

    @property
    def pictures_folder(self) -> 'XAImageEventsFolder':
        """The user's Pictures folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.pictures_folder()

    @property
    def preferences_folder(self) -> 'XAImageEventsFolder':
        """The user's Preferences folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.preferences_folder()

    @property
    def public_folder(self) -> 'XAImageEventsFolder':
        """The user's Public folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.public_folder()

    @property
    def scripting_additions_folder(self) -> 'XAImageEventsFolder':
        """The Scripting Additions folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.scripting_additions_folder()

    @property
    def scripts_folder(self) -> 'XAImageEventsFolder':
        """The user's Scripts folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.scripts_folder()

    @property
    def shared_documents_folder(self) -> 'XAImageEventsFolder':
        """The Shared Documents folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.shared_documents_folder()

    @property
    def sites_folder(self) -> 'XAImageEventsFolder':
        """The user's Sites folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.sites_folder()

    @property
    def speakable_items_folder(self) -> 'XAImageEventsFolder':
        """The Speakable Items folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.speakable_items_folder()

    @property
    def startup_disk(self) -> 'XAImageEventsDisk':
        """the disk from which Mac OS X was loaded

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.startup_disk()

    @property
    def system_domain(self) -> 'XAImageEventsSystemDomainObject':
        """the collection of folders belonging to the System

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.system_domain()

    @property
    def temporary_items_folder(self) -> 'XAImageEventsFolder':
        """The Temporary Items folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.temporary_items_folder()

    @property
    def trash(self) -> 'XAImageEventsFolder':
        """The user's Trash folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.trash()

    @property
    def user_domain(self) -> 'XAImageEventsUserDomainObject':
        """the collection of folders belonging to the User

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.user_domain()

    @property
    def utilities_folder(self) -> 'XAImageEventsFolder':
        """The Utilities folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.utilities_folder()

    @property
    def workflows_folder(self) -> 'XAImageEventsFolder':
        """The Automator Workflows folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.workflows_folder()

    @property
    def default_cmyk_profile(self) -> 'XAImageEventsProfile':
        """the default CMYK profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_cmyk_profile()

    @property
    def default_cmyk_profile_location(self) -> 'XAImageEventsFile':
        """the default CMYK profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_cmyk_profile_location()

    @property
    def default_gray_profile(self) -> 'XAImageEventsProfile':
        """the default Gray profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_gray_profile()

    @property
    def default_gray_profile_location(self) -> 'XAImageEventsFile':
        """the default Gray profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_gray_profile_location()

    @property
    def default_lab_profile(self) -> 'XAImageEventsProfile':
        """the default Lab profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_lab_profile()

    @property
    def default_lab_profile_location(self) -> 'XAImageEventsFile':
        """the default Lab profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_lab_profile_location()

    @property
    def default_rgb_profile(self) -> 'XAImageEventsProfile':
        """the default RGB profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_rgb_profile()

    @property
    def default_rgb_profile_location(self) -> 'XAImageEventsFile':
        """the default RGB profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_rgb_profile_location()

    @property
    def default_xyz_profile(self) -> 'XAImageEventsProfile':
        """the default XYZ profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_xyz_profile()

    @property
    def default_xyz_profile_location(self) -> 'XAImageEventsFile':
        """the default XYZ profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.default_xyz_profile_location()

    @property
    def preferred_cmm(self) -> 'str':
        """specifies preferred Color Management Module to use, or "automatic"

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.preferred_cmm()

    @property
    def profile_folder(self) -> 'XAImageEventsAlias':
        """the ColorSync profile folder

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.profile_folder()

    @property
    def quit_delay(self) -> 'int':
        """the time in seconds the application will idle before quitting; if set to zero, idle time will not cause the application to quit

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.quit_delay()

    @property
    def system_profile(self) -> 'XAImageEventsProfile':
        """the default system profile

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.system_profile()

    @property
    def system_profile_location(self) -> 'XAImageEventsFile':
        """the default system profile location

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.system_profile_location()

    def aliases(self, filter: Union[dict, None] = None) -> 'XAImageEventsAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.aliases(), XAImageEventsAliasList, filter)

    def disks(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskList':
        """Returns a list of disks, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.disks(), XAImageEventsDiskList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.diskItems(), XAImageEventsDiskItemList, filter)

    def domains(self, filter: Union[dict, None] = None) -> 'XAImageEventsDomainList':
        """Returns a list of domains, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.domains(), XAImageEventsDomainList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAImageEventsFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.files(), XAImageEventsFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAImageEventsFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.filePackages(), XAImageEventsFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folders(), XAImageEventsFolderList, filter)

    def items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.items(), XAImageEventsDiskItemList, filter)

    def displays(self, filter: Union[dict, None] = None) -> 'XAImageEventsDisplayList':
        """Returns a list of displays, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.displays(), XAImageEventsDisplayList, filter)

    def images(self, filter: Union[dict, None] = None) -> 'XAImageEventsImageList':
        """Returns a list of images, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.images(), XAImageEventsImageList, filter)

    def profiles(self, filter: Union[dict, None] = None) -> 'XAImageEventsProfileList':
        """Returns a list of profiles, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.profiles(), XAImageEventsProfileList, filter)

    def open(self, *paths: Union[List[XABase.XAPath], XABase.XAPath, str]) -> 'XAImageEventsImage':
        """Opens the disk item at the given filepath.

        :param path: The path to a file or the URL to a website to open.
        :type path: Union[List[XABase.XAPath], XABase.XAPath, str]
        :return: A reference to the opened file, or None if no file was created or it cannot be found
        :rtype: Any

        .. versionadded:: 0.0.1
        """
        if len(paths) > 1:
            # Open multiple paths
            new_files = []
            for path in paths:
                if isinstance(path, str):
                    path = XABase.XAPath(path)
                new_files.append(self.xa_scel.open_(path.xa_elem))
            return self._new_element(new_files, XAImageEventsImageList)

        # Open a single path
        if isinstance(paths[0], str):
            paths = XABase.XAPath(paths[0])
        file = self.xa_scel.open_(paths.xa_elem)
        return self._new_element(file, XAImageEventsImage)




class XAImageEventsDiskItemList(XABase.XAList):
    """A wrapper around lists of disk items that employs fast enumeration techniques.

    All properties of disk items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XAImageEventsDiskItem
        super().__init__(properties, object_class, filter)

    def busy_status(self) -> List['bool']:
        """Retrieves the busy status of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("busyStatus"))

    def container(self) -> 'XAImageEventsDiskItemList':
        """Retrieves the containing folder or disk of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("container")
        return self._new_element(ls, XAImageEventsDiskItemList)

    def creation_date(self) -> List['datetime']:
        """Retrieves the creation date of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def displayed_name(self) -> List['str']:
        """Retrieves the displayed name of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName"))

    def id(self) -> List['str']:
        """Retrieves the unique ID of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def modification_date(self) -> List['datetime']:
        """Retrieves the last modified date of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def name(self) -> List['str']:
        """Retrieves the name of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def name_extension(self) -> List['str']:
        """Retrieves the name extension of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("nameExtension"))

    def package_folder(self) -> List['bool']:
        """Retrieves the package folder status of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("packageFolder"))

    def path(self) -> List['XABase.XAPath']:
        """Retrieves the file system path of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XABase.XAPath(x) for x in ls]

    def physical_size(self) -> List['int']:
        """Retrieves the actual disk space used by each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize"))

    def posix_path(self) -> List['str']:
        """Retrieves the POSIX file system path of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("posixPath"))

    def size(self) -> List['int']:
        """Retrieves the logical size of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def url(self) -> List['XABase.XAURL']:
        """Retrieves the URL of each disk item in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("URL")
        return [XABase.XAURL(x) for x in ls]

    def visible(self) -> List['bool']:
        """Retrieves the visible status of each item in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("visible"))

    def volume(self) -> List['str']:
        """Retrieves the volume on which each item in the list resides.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("volume"))

    def by_busy_status(self, busy_status: bool) -> 'XAImageEventsDiskItem':
        """Retrieves item whose busy status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("busyStatus", busy_status)

    def by_container(self, container: 'XAImageEventsDiskItem') -> 'XAImageEventsDiskItem':
        """Retrieves item whose container matches the given disk item.

        .. versionadded:: 0.1.0
        """
        return self.by_property("container", container.xa_elem)

    def by_creation_date(self, creation_date: datetime) -> 'XAImageEventsDiskItem':
        """Retrieves item whose creation date matches the given date.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creationDate", creation_date)

    def by_displayed_name(self, displayed_name: str) -> 'XAImageEventsDiskItem':
        """Retrieves item whose displayed name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("displayedName", displayed_name)

    def by_id(self, id: str) -> 'XAImageEventsDiskItem':
        """Retrieves item whose ID matches the given ID.

        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_modification_date(self, modification_date: datetime) -> 'XAImageEventsDiskItem':
        """Retrieves item whose date matches the given date.

        .. versionadded:: 0.1.0
        """
        return self.by_property("modificationDate", modification_date)

    def by_name(self, name: str) -> 'XAImageEventsDiskItem':
        """Retrieves item whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_name_extension(self, name_extension: str) -> 'XAImageEventsDiskItem':
        """Retrieves item whose name extension matches the given extension.

        .. versionadded:: 0.1.0
        """
        return self.by_property("nameExtension", name_extension)

    def by_package_folder(self, package_folder: bool) -> 'XAImageEventsDiskItem':
        """Retrieves item whose package folder status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("packageFolder", package_folder)

    def by_path(self, path: Union[XABase.XAPath, str]) -> 'XAImageEventsDiskItem':
        """Retrieves item whose path matches the given path.

        .. versionadded:: 0.1.0
        """
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_physical_size(self, physical_size: int) -> 'XAImageEventsDiskItem':
        """Retrieves item whose physical size matches the given size.

        .. versionadded:: 0.1.0
        """
        return self.by_property("physicalSize", physical_size)

    def by_posix_path(self, posix_path: str) -> 'XAImageEventsDiskItem':
        """Retrieves item whose POSIX path matches the given POSIX path.

        .. versionadded:: 0.1.0
        """
        return self.by_property("posixPath", posix_path)

    def by_size(self, size: int) -> 'XAImageEventsDiskItem':
        """Retrieves item whose size matches the given size.

        .. versionadded:: 0.1.0
        """
        return self.by_property("size", size)

    def by_url(self, url: XABase.XAURL) -> 'XAImageEventsDiskItem':
        """Retrieves the item whose URL matches the given URL.

        .. versionadded:: 0.1.0
        """
        return self.by_property("URL", url.xa_elem)

    def by_visible(self, visible: bool) -> 'XAImageEventsDiskItem':
        """Retrieves the item whose visible status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("visible", visible)

    def by_volume(self, volume: str) -> 'XAImageEventsDiskItem':
        """Retrieves the item whose volume matches the given volume.

        .. versionadded:: 0.1.0
        """
        return self.by_property("volume", volume)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsDiskItem(XABase.XAObject):
    """An item stored in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def busy_status(self) -> 'bool':
        """Whether the disk item is busy.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.busyStatus()

    @property
    def container(self) -> 'XAImageEventsDiskItem':
        """The folder or disk which has this disk item as an element.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.container(), XAImageEventsDiskItem)

    @property
    def creation_date(self) -> 'datetime':
        """The date on which the disk item was created.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creationDate()

    @property
    def displayed_name(self) -> 'str':
        """The name of the disk item as displayed in the User Interface.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.displayedName()

    @property
    def id(self) -> 'str':
        """The unique ID of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def modification_date(self) -> 'datetime':
        """The date on which the disk item was last modified.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.modificationDate()

    @property
    def name(self) -> 'str':
        """The name of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def name_extension(self) -> 'str':
        """The extension portion of the name.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.nameExtension()

    @property
    def package_folder(self) -> 'bool':
        """Whether the disk item is a package.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.packageFolder()

    @property
    def path(self) -> 'XABase.XAPath':
        """The file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return XABase.XAPath(self.xa_elem.path())

    @property
    def physical_size(self) -> 'int':
        """The actual space used by the disk item on disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.physicalSize()

    @property
    def posix_path(self) -> 'str':
        """The POSIX file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.posixPath()

    @property
    def size(self) -> 'int':
        """The logical size of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.size()

    @property
    def url(self) -> 'XABase.XAURL':
        """The URL of the disk item.

        .. versionadded:: 0.1.0
        """
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def visible(self) -> 'bool':
        """Whether the disk item is visible.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.visible()

    @property
    def volume(self) -> 'str':
        """The volume on which the disk item resides.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.volume()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAImageEventsAliasList(XAImageEventsDiskItemList):
    """A wrapper around lists of aliases that employs fast enumeration techniques.

    All properties of aliases can be called as methods on the wrapped list, returning a list containing each alias' value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAImageEventsAlias)

    def creator_type(self) -> List['str']:
        """Retrieves the OSType identifying the application that created each alias in the list

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def default_application(self) -> 'XAImageEventsDiskItemList':
        """Retrieves the applications that will launch if each alias in the list is opened.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication")
        return self._new_element(ls, XAImageEventsDiskItemList)

    def file_type(self) -> List['str']:
        """Retrieves the OSType identifying the type of data contained in each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def kind(self) -> List['str']:
        """Retrieves the kind of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def product_version(self) -> List['str']:
        """Retrieves the product version of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def short_version(self) -> List['str']:
        """Retrieves the short version of the application bundle referenced by each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion"))

    def stationery(self) -> List['bool']:
        """Retrieves the stationery status of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def type_identifier(self) -> List['str']:
        """Retrieves the type identifier of each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier"))

    def version(self) -> List['str']:
        """Retrieves the version of the application bundle referenced by each alias in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_creator_type(self, creator_type: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose creator type matches the given creator type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creatorType", creator_type)

    def by_default_application(self, default_application: 'XAImageEventsDiskItem') -> 'XAImageEventsAlias':
        """Retrieves the alias whose default application matches the given application.

        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose kind matches the given kind.

        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose product version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose short version matches the given text.

        .. versionadded:: 0.1.0
        """
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> 'XAImageEventsAlias':
        """Retrieves the alias whose stationery status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose type identifier matches the given type identifier.

        .. versionadded:: 0.1.0
        """
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> 'XAImageEventsAlias':
        """Retrieves the alias whose version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("version", version)

class XAImageEventsAlias(XAImageEventsDiskItem):
    """An alias in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> 'str':
        """The OSType identifying the application that created the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> 'XAImageEventsDiskItem':
        """The application that will launch if the alias is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XAImageEventsDiskItem)

    @property
    def file_type(self) -> 'str':
        """The OSType identifying the type of data contained in the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> 'str':
        """The kind of alias, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> 'str':
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> 'str':
        """The short version of the application bundle referenced by the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> 'bool':
        """Whether the alias is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> 'str':
        """The type identifier of the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> 'str':
        """The version of the application bundle referenced by the alias (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()

    def aliases(self, filter: Union[dict, None] = None) -> 'XAImageEventsAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAImageEventsAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XAImageEventsDiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAImageEventsFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAImageEventsFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAImageEventsFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAImageEventsFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)




class XAImageEventsDiskList(XAImageEventsDiskItemList):
    """A wrapper around lists of disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAImageEventsDisk)

    def capacity(self) -> List['float']:
        """Retrieves the total number of bytes (free or used) on each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("capacity"))

    def ejectable(self) -> List['bool']:
        """Retrieves the ejectable status of each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable"))

    def format(self) -> List['XAImageEventsApplication.Format']:
        """Retrieves the file system format of each disk in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("format")
        return [XAImageEventsApplication.Format(XABase.OSType(x.stringValue())) for x in ls]

    def free_space(self) -> List['float']:
        """Retrieves the number of free bytes left on each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace"))

    def ignore_privileges(self) -> List['bool']:
        """Retrieves the ignore privileges status for each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("ignorePrivileges"))

    def local_volume(self) -> List['bool']:
        """Retrieves the local volume status for each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume"))

    def server(self) -> List['str']:
        """Retrieves the server on which each disk in the list resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("server"))

    def startup(self) -> List['bool']:
        """Retrieves the startup disk status of each disk in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("startup"))

    def zone(self) -> List['str']:
        """Retrieves the zone in which each disk's server resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("zone"))

    def by_capacity(self, capacity: float) -> 'XAImageEventsDisk':
        """Retrieves the disk whose capacity matches the given capacity.

        .. versionadded:: 0.1.0
        """
        return self.by_property("capacity", capacity)

    def by_ejectable(self, ejectable: bool) -> 'XAImageEventsDisk':
        """Retrieves the disk whose ejectable status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("ejectable", ejectable)

    def by_format(self, format: XAImageEventsApplication.Format) -> 'XAImageEventsDisk':
        """Retrieves the disk whose format matches the given format.

        .. versionadded:: 0.1.0
        """
        return self.by_property("format", format.value)

    def by_free_space(self, free_space: float) -> 'XAImageEventsDisk':
        """Retrieves the disk whose free space matches the given amount.

        .. versionadded:: 0.1.0
        """
        return self.by_property("freeSpace", free_space)

    def by_ignore_privileges(self, ignore_privileges: bool) -> 'XAImageEventsDisk':
        """Retrieves the disk whose ignore privileges status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("ignorePrivileges", ignore_privileges)

    def by_local_volume(self, local_volume: bool) -> 'XAImageEventsDisk':
        """Retrieves the disk whose local volume status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("localVolume", local_volume)

    def by_server(self, server: str) -> 'XAImageEventsDisk':
        """Retrieves the disk whose server matches the given server.

        .. versionadded:: 0.1.0
        """
        return self.by_property("server", server)

    def by_startup(self, startup: bool) -> 'XAImageEventsDisk':
        """Retrieves the disk whose startup status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("startup", startup)

    def by_zone(self, zone: str) -> 'XAImageEventsDisk':
        """Retrieves the disk whose zone matches the given zone.

        .. versionadded:: 0.1.0
        """
        return self.by_property("zone", zone)

class XAImageEventsDisk(XAImageEventsDiskItem):
    """A disk in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def capacity(self) -> 'float':
        """The total number of bytes (free or used) on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.capacity()

    @property
    def ejectable(self) -> 'bool':
        """Whether the media can be ejected (floppies, CD's, and so on).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ejectable()

    @property
    def format(self) -> 'XAImageEventsApplication.Format':
        """The file system format of the disk.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.Format(self.xa_elem.format())

    @property
    def free_space(self) -> 'float':
        """The number of free bytes left on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.freeSpace()

    @property
    def ignore_privileges(self) -> 'bool':
        """Whether to ignore permissions on this disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ignorePrivileges()

    @property
    def local_volume(self) -> 'bool':
        """Whether the media is a local volume (as opposed to a file server).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.localVolume()

    @property
    def server(self) -> 'str':
        """The server on which the disk resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.server()

    @property
    def startup(self) -> 'bool':
        """Whether this disk is the boot disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.startup()

    @property
    def zone(self) -> 'str':
        """The zone in which the disk's server resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.zone()

    def aliases(self, filter: Union[dict, None] = None) -> 'XAImageEventsAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAImageEventsAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XAImageEventsDiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAImageEventsFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAImageEventsFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAImageEventsFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.fileOackages(), XAImageEventsFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)




class XAImageEventsDomainList(XABase.XAList):
    """A wrapper around lists of domains that employs fast enumeration techniques.

    All properties of domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImageEventsDomain, filter)

    def id(self) -> List['str']:
        """Retrieves the unique identifier of each domain in the list

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List['str']:
        """Retrieves the name of each domain in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_id(self, id: str) -> 'XAImageEventsDomain':
        """Retrieves the domain whose ID matches the given ID.

        .. versionadded:: 0.1.0
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> 'XAImageEventsDomain':
        """Retrieves the domain whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsDomain(XABase.XAObject):
    """A domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def application_support_folder(self) -> 'XAImageEventsFolder':
        """The Application Support folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationSupportFolder(), XAImageEventsFolder)

    @property
    def applications_folder(self) -> 'XAImageEventsFolder':
        """The Applications folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationsFolder(), XAImageEventsFolder)

    @property
    def desktop_pictures_folder(self) -> 'XAImageEventsFolder':
        """The Desktop Pictures folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopPicturesFolder(), XAImageEventsFolder)

    @property
    def folder_action_scripts_folder(self) -> 'XAImageEventsFolder':
        """The Folder Action Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folderActionScriptsFolder(), XAImageEventsFolder)

    @property
    def fonts_folder(self) -> 'XAImageEventsFolder':
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAImageEventsFolder)

    @property
    def id(self) -> 'str':
        """The unique identifier of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def library_folder(self) -> 'XAImageEventsFolder':
        """The Library folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.libraryFolder(), XAImageEventsFolder)

    @property
    def name(self) -> 'str':
        """The name of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def preferences_folder(self) -> 'XAImageEventsFolder':
        """The Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAImageEventsFolder)

    @property
    def scripting_additions_folder(self) -> 'XAImageEventsFolder':
        """The Scripting Additions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingAdditionsFolder(), XAImageEventsFolder)

    @property
    def scripts_folder(self) -> 'XAImageEventsFolder':
        """The Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptsFolder(), XAImageEventsFolder)

    @property
    def shared_documents_folder(self) -> 'XAImageEventsFolder':
        """The Shared Documents folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sharedDocumentsFolder(), XAImageEventsFolder)

    @property
    def speakable_items_folder(self) -> 'XAImageEventsFolder':
        """The Speakable Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.speakableItemsFolder(), XAImageEventsFolder)

    @property
    def utilities_folder(self) -> 'XAImageEventsFolder':
        """The Utilities folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.utilitiesFolder(), XAImageEventsFolder)

    @property
    def workflows_folder(self) -> 'XAImageEventsFolder':
        """The Automator Workflows folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.workflowsFolder(), XAImageEventsFolder)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAImageEventsClassicDomainObject(XAImageEventsDomain):
    """The Classic domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def apple_menu_folder(self) -> 'XAImageEventsFolder':
        """The Apple Menu Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.appleMenuFolder(), XAImageEventsFolder)

    @property
    def control_panels_folder(self) -> 'XAImageEventsFolder':
        """The Control Panels folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlPanelsFolder(), XAImageEventsFolder)

    @property
    def control_strip_modules_folder(self) -> 'XAImageEventsFolder':
        """The Control Strip Modules folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlStripModulesFolder(), XAImageEventsFolder)

    @property
    def desktop_folder(self) -> 'XAImageEventsFolder':
        """The Classic Desktop folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAImageEventsFolder)

    @property
    def extensions_folder(self) -> 'XAImageEventsFolder':
        """The Extensions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.extensionsFolder(), XAImageEventsFolder)

    @property
    def fonts_folder(self) -> 'XAImageEventsFolder':
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAImageEventsFolder)

    @property
    def launcher_items_folder(self) -> 'XAImageEventsFolder':
        """The Launcher Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.launcherItemsFolder(), XAImageEventsFolder)

    @property
    def preferences_folder(self) -> 'XAImageEventsFolder':
        """The Classic Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAImageEventsFolder)

    @property
    def shutdown_folder(self) -> 'XAImageEventsFolder':
        """The Shutdown Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.shutdownFolder(), XAImageEventsFolder)

    @property
    def startup_items_folder(self) -> 'XAImageEventsFolder':
        """The StartupItems folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.startupItemsFolder(), XAImageEventsFolder)

    @property
    def system_folder(self) -> 'XAImageEventsFolder':
        """The System folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.systemFolder(), XAImageEventsFolder)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)




class XAImageEventsFileList(XAImageEventsDiskItemList):
    """A wrapper around lists of files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, object_class = None):
        if object_class is None:
            object_class = XAImageEventsFile
        super().__init__(properties, filter, object_class)

    def creator_type(self) -> List['str']:
        """Retrieves the OSType identifying the application that created each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType"))

    def default_application(self) -> 'XAImageEventsDiskItemList':
        """Retrieves the applications that will launch if each file in the list is opened.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication")
        return self._new_element(ls, XAImageEventsDiskItemList)

    def file_type(self) -> List['str']:
        """Retrieves the OSType identifying the type of data contained in each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("fileType"))

    def kind(self) -> List['str']:
        """Retrieves the kind of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def product_version(self) -> List['str']:
        """Retrieves the product version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion"))

    def short_version(self) -> List['str']:
        """Retrieves the short version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion"))

    def stationery(self) -> List['bool']:
        """Retrieves the stationery status of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("stationery"))

    def type_identifier(self) -> List['str']:
        """Retrieves the type identifier of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier"))

    def version(self) -> List['str']:
        """Retrieves the version of each file in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_creator_type(self, creator_type: str) -> 'XAImageEventsFile':
        """Retrieves the file whose creator type matches the given creator type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creatorType", creator_type)

    def by_default_application(self, default_application: 'XAImageEventsDiskItem') -> 'XAImageEventsFile':
        """Retrieves the file whose default application matches the given application.

        .. versionadded:: 0.1.0
        """
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> 'XAImageEventsFile':
        """Retrieves the file whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> 'XAImageEventsFile':
        """Retrieves the file whose kind matches the given kind.

        .. versionadded:: 0.1.0
        """
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> 'XAImageEventsFile':
        """Retrieves the file whose product version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> 'XAImageEventsFile':
        """Retrieves the file whose short version matches the given text.

        .. versionadded:: 0.1.0
        """
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> 'XAImageEventsFile':
        """Retrieves the file whose stationery status matches the given boolean value.

        .. versionadded:: 0.1.0
        """
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> 'XAImageEventsFile':
        """Retrieves the file whose type identifier matches the given type identifier.

        .. versionadded:: 0.1.0
        """
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> 'XAImageEventsFile':
        """Retrieves the file whose version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("version", version)

class XAImageEventsFile(XAImageEventsDiskItem):
    """A file in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> 'str':
        """The OSType identifying the application that created the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> 'XAImageEventsDiskItem':
        """The application that will launch if the file is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XAImageEventsDiskItem)

    @property
    def file_type(self) -> 'str':
        """The OSType identifying the type of data contained in the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> 'str':
        """The kind of file, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> 'str':
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> 'str':
        """The short version of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> 'bool':
        """Whether the file is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> 'str':
        """The type identifier of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> 'str':
        """The version of the file (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()




class XAImageEventsFilePackageList(XAImageEventsFileList):
    """A wrapper around lists of file packages that employs fast enumeration techniques.

    All properties of file packages can be called as methods on the wrapped list, returning a list containing each package's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAImageEventsFilePackage)

class XAImageEventsFilePackage(XAImageEventsFile):
    """A file package in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> 'XAImageEventsAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAImageEventsAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XAImageEventsDiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAImageEventsFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAImageEventsFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAImageEventsFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAImageEventsFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)




class XAImageEventsFolderList(XAImageEventsDiskItemList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folder's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAImageEventsFolder)

class XAImageEventsFolder(XAImageEventsDiskItem):
    """A folder in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> 'XAImageEventsAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.aliases(), XAImageEventsAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XAImageEventsDiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.diskItems(), XAImageEventsDiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XAImageEventsFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.files(), XAImageEventsFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XAImageEventsFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.filePackages(), XAImageEventsFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAImageEventsFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.folders(), XAImageEventsFolderList, filter)




class XAImageEventsLocalDomainObject(XAImageEventsDomain):
    """The local domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAImageEventsNetworkDomainObject(XAImageEventsDomain):
    """The network domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAImageEventsSystemDomainObject(XAImageEventsDomain):
    """The system domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAImageEventsUserDomainObject(XAImageEventsDomain):
    """The user domain in the file system.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def desktop_folder(self) -> 'XAImageEventsFolder':
        """The user's Desktop folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAImageEventsFolder)

    @property
    def documents_folder(self) -> 'XAImageEventsFolder':
        """The user's Documents folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.documentsFolder(), XAImageEventsFolder)

    @property
    def downloads_folder(self) -> 'XAImageEventsFolder':
        """The user's Downloads folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.downloadsFolder(), XAImageEventsFolder)

    @property
    def favorites_folder(self) -> 'XAImageEventsFolder':
        """The user's Favorites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.favoritesFolder(), XAImageEventsFolder)

    @property
    def home_folder(self) -> 'XAImageEventsFolder':
        """The user's Home folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.homeFolder(), XAImageEventsFolder)

    @property
    def movies_folder(self) -> 'XAImageEventsFolder':
        """The user's Movies folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.moviesFolder(), XAImageEventsFolder)

    @property
    def music_folder(self) -> 'XAImageEventsFolder':
        """The user's Music folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.musicFolder(), XAImageEventsFolder)

    @property
    def pictures_folder(self) -> 'XAImageEventsFolder':
        """The user's Pictures folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.picturesFolder(), XAImageEventsFolder)

    @property
    def public_folder(self) -> 'XAImageEventsFolder':
        """The user's Public folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.publicFolder(), XAImageEventsFolder)

    @property
    def sites_folder(self) -> 'XAImageEventsFolder':
        """The user's Sites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sitesFolder(), XAImageEventsFolder)

    @property
    def temporary_items_folder(self) -> 'XAImageEventsFolder':
        """The Temporary Items folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.temporaryItemsFolder(), XAImageEventsFolder)




class XAImageEventsDisplayList(XABase.XAList):
    """A wrapper around lists of displays that employs fast enumeration techniques.

    All properties of displays can be called as methods on the wrapped list, returning a list containing each display's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImageEventsDisplay, filter)

    def display_number(self) -> List['int']:
        """Retrieves the number of each display in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("displayNumber"))

    def display_profile(self) -> 'XAImageEventsProfileList':
        """Retrieves the profile for each display in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("displayProfile")
        return self._new_element(ls, XAImageEventsProfileList)

    def name(self) -> List['str']:
        """Retrieves the name of each display in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_display_number(self, display_number: int) -> 'XAImageEventsDisplay':
        """Retrieves display whose display number matches the given number.

        .. versionadded:: 0.1.0
        """
        return self.by_property("displayNumber", display_number)

    def by_display_profile(self, display_profile: 'XAImageEventsProfile') -> 'XAImageEventsDisplay':
        """Retrieves display whose display profile matches the given profile.

        .. versionadded:: 0.1.0
        """
        return self.by_property("displayProfile", display_profile.xa_elem)

    def by_name(self, name: str) -> 'XAImageEventsDisplay':
        """Retrieves display whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsDisplay(XABase.XAObject):
    """A monitor connected to the computer.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def display_number(self) -> 'int':
        """The number of the display.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.displayNumber()

    @property
    def display_profile(self) -> 'XAImageEventsProfile':
        """The profile for the display.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.displayProfile(), XAImageEventsProfile)

    @property
    def name(self) -> 'str':
        """The name of the display.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAImageEventsImageList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of images that employs fast enumeration techniques.

    All properties of images can be called as methods on the wrapped list, returning a list containing each image's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImageEventsImage, filter)

    def bit_depth(self) -> List['XAImageEventsApplication.BitDepth']:
        """Retrieves the bit depth of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("bitDepth")
        return [XAImageEventsApplication.BitDepth(XABase.OSType(x.stringValue())) for x in ls]

    def color_space(self) -> List['XAImageEventsApplication.ColorSpace']:
        """Retrieves the color space of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("colorSpace")
        return [XAImageEventsApplication.ColorSpace(XABase.OSType(x.stringValue())) for x in ls]

    def dimensions(self) -> List[List[int]]:
        """Retrieves the width and height of each image in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("dimensions"))

    def embedded_profile(self) -> 'XAImageEventsProfileList':
        """Retrieves the profile, if any, embedded in each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("embeddedProfile")
        return self._new_element(ls, XAImageEventsProfileList)

    def file_type(self) -> List['XAImageEventsApplication.FileType']:
        """Retrieves the file type of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("fileType")
        return [XAImageEventsApplication.FileType(XABase.OSType(x.stringValue())) for x in ls]

    def image_file(self) -> 'XAImageEventsFileList':
        """Retrieves the file of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("imageFile")
        return self._new_element(ls, XAImageEventsFileList)

    def location(self) -> List['XAImageEventsDiskItem']:
        """Retrieves the folder or disk that encloses the file that contains each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return self._new_element(ls, XAImageEventsDiskItemList)

    def name(self) -> List['str']:
        """Retrieves the name of each image in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def resolution(self) -> List['float']:
        """Retrieves the horizontal and vertical pixel density of each image in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("resolution"))

    def by_bit_depth(self, bit_depth) -> 'XAImageEventsApplication.BitDepth':
        """Retrieves the image whose bit depth matches the given bit depth.

        .. versionadded:: 0.1.0
        """
        return self.by_property("bitDepth", event_from_int(bit_depth.value))

    def by_color_space(self, color_space: 'XAImageEventsApplication.ColorSpace') -> 'XAImageEventsImage':
        """Retrieves the image whose color space matches the given color space.

        .. versionadded:: 0.1.0
        """
        return self.by_property("colorSpace", event_from_int(color_space.value))

    def by_dimensions(self, dimensions: List[int]) -> 'XAImageEventsImage':
        """Retrieves the image whose dimensions matches the given dimensions.

        .. versionadded:: 0.1.0
        """
        return self.by_property("dimensions", dimensions)

    def by_embedded_profile(self, embedded_profile: 'XAImageEventsProfile') -> 'XAImageEventsImage':
        """Retrieves the image whose embedded profile matches the given profile.

        .. versionadded:: 0.1.0
        """
        return self.by_property("embeddedProfile", embedded_profile.xa_elem)

    def by_file_type(self, file_type: 'XAImageEventsApplication.FileType') -> 'XAImageEventsImage':
        """Retrieves the image whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        return self.by_property("fileType", event_from_int(file_type.value))

    def by_image_file(self, image_file: 'XAImageEventsFile') -> 'XAImageEventsImage':
        """Retrieves the image whose image file matches the given image file.

        .. versionadded:: 0.1.0
        """
        return self.by_property("imageFile", image_file.xa_elem)

    def by_location(self, location: 'XAImageEventsDiskItem') -> 'XAImageEventsImage':
        """Retrieves the image whose location matches the given location.

        .. versionadded:: 0.1.0
        """
        return self.by_property("location", location.xa_elem)

    def by_name(self, name: str) -> 'XAImageEventsImage':
        """Retrieves the image whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_resolution(self, resolution: List[float]) -> 'XAImageEventsImage':
        """Retrieves the image whose resolution matches the given resolution.

        .. versionadded:: 0.1.0
        """
        return self.by_property("resolution", resolution)

    def crop(self, width: int, height: int) -> 'XAImageEventsImage':
        """Crops each image in the list to the specified with and height.

        :param width: The width of the new images, in pixels
        :type width: int
        :param height: The height of the new images, in pixels
        :type height: int
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.cropToDimensions_([width, height])
        return self

    def embed_profile(self, profile: 'XAImageEventsProfile') -> 'XAImageEventsImageList':
        """Embeds the specified ICC profile in each image in the list.

        :param profile: The ICC profile to embed in the images
        :type profile: XAImageEventsProfile
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.embedWithSource_(profile.xa_elem)
        return self

    def flip_horizontally(self) -> 'XAImageEventsImageList':
        """Flips each image in the list horizontally.

        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.flipHorizontal_vertical_(True, False)
        return self

    def flip_vertically(self) -> 'XAImageEventsImageList':
        """Flips each image in the list vertically.

        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.flipHorizontal_vertical_(False, True)
        return self

    def pad(self, horizontal_padding: int = 10, vertical_padding: int = 10, color: Union[XABase.XAColor, List[int], None] = None) -> 'XAImageEventsImageList':
        """Pads each image in the list with a border of the specified color, or white by default.

        :param horizontal_padding: The width of padding in the horizontal direction, defaults to 10
        :type horizontal_padding: int, optional
        :param vertical_padding: The width of padding in the vertical direction, defaults to 10
        :type vertical_padding: int, optional
        :param color: The color to pad with, defaults to None
        :type color: Union[XABase.XAColor, List[int], None], optional
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        if color is None:
                color = [65535, 65535, 65535]
        elif isinstance(color, XABase.XAColor):
            color = [color.red() * 65535, color.green() * 65535, color.blue() * 65535]

        for x in self.xa_elem:
            dimensions = [x.dimensions()[0] + horizontal_padding, x.dimensions()[1] + vertical_padding]
            x.padToDimensions_withPadColor_(dimensions, color)
        return self

    def rotate(self, angle: float) -> 'XAImageEventsImageList':
        """Rotates each image in the list to the specified angle.

        :param angle: The angle to rotate the images by
        :type angle: float
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.rotateToAngle_(angle)
        return self

    def save(self, file_type: Union[XAImageEventsApplication.FileType, None] = None, add_icons: bool = False, file_paths: Union[List[Union[XABase.XAPath, str, None]], None] = None, pack_bits: bool = False, compression_level: XAImageEventsApplication.CompressionLevel = XAImageEventsApplication.CompressionLevel.LOW):
        """Saves each image in the list

        :param file_type: The file type to save the images as, or None to save as their current file type (usually the type of the original image file), defaults to None
        :type file_type: Union[XAImageEventsApplication.FileType, None], optional
        :param add_icons: Whether to add icons, defaults to False
        :type add_icons: bool, optional
        :param file_paths: The paths to save the images in, or None to save at the path of the original image files, defaults to None
        :type file_paths: Union[List[Union[XABase.XAPath, str, None]], None], optional
        :param pack_bits: Whether to compress the bytes with PackBits (applies only to TIFF files), defaults to False
        :type pack_bits: bool, optional
        :param compression_level: Specifies the compression level of the resultant files (applies only to JPEG files), defaults to XAImageEventsApplication.CompressionLevel.LOW
        :type compression_level: XAImageEventsApplication.CompressionLevel, optional

        .. versionadded:: 0.1.0
        """
        if isinstance(file_paths, list):
            for index, path in enumerate(file_paths):
                if isinstance(path, XABase.XAPath):
                    file_paths[index] = path.path

        if file_type is not None:
            file_type = file_type.value

        for x in self.xa_elem:
            if file_type is None:
                file_type = XABase.OSType(x.fileType().get().stringValue())
            x.saveAs_icon_in_PackBits_withCompressionLevel_(file_type, add_icons, file_paths, pack_bits, compression_level.value)

    def scale(self, scale_factor: Union[float, None] = None, width: Union[int, None] = None) -> 'XAImageEventsImageList':
        """Scales each image in the list by the specified factor or to the specified width.

        :param scale_factor: The factor to scale the images by, from 0 to infinity, or None to scale to a set width instead, defaults to None
        :type scale_factor: float, optional
        :param width: The positive width, in pixels, to scale the images to, or None to scale by a scale factor instead, defaults to None
        :type width: int, optional
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        if scale_factor == None and width == None:
                raise ValueError("Either scale factor or width must be positive.")

        for x in self.xa_elem:
            if scale_factor != None:
                width = x.dimensions()[0] * scale_factor
            elif width != None:
                scale_factor = width / x.dimensions()[0]
                
            x.scaleByFactor_toSize_(scale_factor, width)
        return self

    def unembed(self) -> 'XAImageEventsImageList':
        """Removes all embedded ICC profiles from each image in the list.

        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            x.unembed()
        return self

    def get_clipboard_representation(self) -> List[AppKit.NSURL]:
        """Gets a clipboard-codable representation of each image in the list.

        When the clipboard content is set to a list of images, each image's file URL is added to the clipboard.

        :return: The file URL of each image in the list
        :rtype: List[AppKit.NSURL]

        .. versionadded:: 0.1.0
        """
        return [x.xa_elem for x in self.image_file().url()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsImage(XABase.XAObject, XAClipboardCodable):
    """An image contained in a file.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def bit_depth(self) -> 'XAImageEventsApplication.BitDepth':
        """Bit depth of the image's color representation.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.BitDepth(self.xa_elem.bitDepth())

    @property
    def color_space(self) -> 'XAImageEventsApplication.ColorSpace':
        """Color space of the image's color representation.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.ColorSpace(self.xa_elem.colorSpace())

    @property
    def dimensions(self) -> 'List[int]':
        """The width and height of the image, respectively, in pixels.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.dimensions()

    @property
    def embedded_profile(self) -> 'XAImageEventsProfile':
        """The profile, if any, embedded in the image.

        .. versionadded:: 0.1.0
        """
        return self.new_element(self.xa_elem.embeddedProfile(), XAImageEventsProfile)

    @property
    def file_type(self) -> 'XAImageEventsApplication.FileType':
        """File type of the image's file.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.FileType(OSType(self.xa_elem.fileType().get().stringValue()))

    @property
    def image_file(self) -> 'XAImageEventsFile':
        """The file that contains the image.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.imageFile(), XAImageEventsFile)

    @property
    def location(self) -> 'XAImageEventsDiskItem':
        """The folder or disk that encloses the file that contains the image.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.location(), XAImageEventsDiskItem)

    @property
    def name(self) -> 'str':
        """The name of the image.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def resolution(self) -> 'List[float]':
        """The horizontal and vertical pixel density of the image, respectively, in dots per inch.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.resolution()

    def crop(self, width: int, height: int) -> 'XAImageEventsImage':
        """Crops the image to the specified with and height.

        :param width: The width of the new image, in pixels
        :type width: int
        :param height: The height of the new image, in pixels
        :type height: int
        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cropToDimensions_([width, height])
        return self

    def embed_profile(self, profile: 'XAImageEventsProfile') -> 'XAImageEventsImage':
        """Embeds the specified ICC profile in the image.

        :param profile: The ICC profile to embed in the image
        :type profile: XAImageEventsProfile
        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.embedWithSource_(profile.xa_elem)
        return self

    def flip_horizontally(self) -> 'XAImageEventsImage':
        """Flips the image horizontally.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.flipHorizontal_vertical_(True, False)
        return self

    def flip_vertically(self) -> 'XAImageEventsImage':
        """Flips the image vertically.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.flipHorizontal_vertical_(False, True)
        return self

    def pad(self, horizontal_padding: int = 10, vertical_padding: int = 10, color: Union[XABase.XAColor, List[int], None] = None) -> 'XAImageEventsImage':
        """Pads the image with a border of the specified color, or white by default.

        :param horizontal_padding: The width of padding in the horizontal direction, defaults to 10
        :type horizontal_padding: int, optional
        :param vertical_padding: The width of padding in the vertical direction, defaults to 10
        :type vertical_padding: int, optional
        :param color: The color to pad the image with, defaults to None
        :type color: Union[XABase.XAColor, List[int], None], optional
         :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        dimensions = [self.dimensions[0] + horizontal_padding, self.dimensions[1] + vertical_padding]

        if color is None:
            color = [65535, 65535, 65535]
        elif isinstance(color, XABase.XAColor):
            color = [color.red() * 65535, color.green() * 65535, color.blue() * 65535]

        self.xa_elem.padToDimensions_withPadColor_(dimensions, color)
        return self

    def rotate(self, angle: float) -> 'XAImageEventsImage':
        """Rotates the image to the specified angle.

        :param angle: The angle to rotate the image by
        :type angle: float
        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.rotateToAngle_(angle)
        return self

    def save(self, file_type: Union[XAImageEventsApplication.FileType, None] = None, add_icon: bool = False, file_path: Union[XABase.XAPath, str, None] = None, pack_bits: bool = False, compression_level: XAImageEventsApplication.CompressionLevel = XAImageEventsApplication.CompressionLevel.LOW):
        """Saves the image to a file.

        :param file_type: The file type to save the image as, or None to save as the current file type (usually the type of the original image file), defaults to None
        :type file_type: Union[XAImageEventsApplication.FileType, None], optional
        :param add_icon: Whether to add an icon, defaults to False
        :type add_icon: bool, optional
        :param file_path: The path to save the image in, or None to save at the path of the original image file, defaults to None
        :type file_path: Union[XABase.XAPath, str, None], optional
        :param pack_bits: Whether to compress the bytes with PackBits (applies only to TIFF files), defaults to False
        :type pack_bits: bool, optional
        :param compression_level: Specifies the compression level of the resultant file (applies only to JPEG files), defaults to XAImageEventsApplication.CompressionLevel.LOW
        :type compression_level: XAImageEventsApplication.CompressionLevel, optional

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, XABase.XAPath):
            file_path = file_path.path

        if file_type is not None:
            file_type = file_type.value
        else:
            file_type = self.file_type.value

        self.xa_elem.saveAs_icon_in_PackBits_withCompressionLevel_(file_type, add_icon, file_path, pack_bits, compression_level.value)

    def scale(self, scale_factor: Union[float, None] = None, width: Union[int, None] = None) -> 'XAImageEventsImage':
        """Scales the image by the specified factor or to the specified width.

        :param scale_factor: The factor to scale the image by, from 0 to infinity, or None to scale to a set width instead, defaults to None
        :type scale_factor: float, optional
        :param width: The positive width, in pixels, to scale the image to, or None to scale by a scale factor instead, defaults to None
        :type width: int, optional
        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        if scale_factor == None and width == None:
            raise ValueError("Either scale factor or width must be positive.")
        elif scale_factor != None:
            width = self.dimensions[0] * scale_factor
        elif width != None:
            scale_factor = width / self.dimensions[0]

        self.xa_elem.scaleByFactor_toSize_(scale_factor, width)
        return self

    def unembed(self) -> 'XAImageEventsImage':
        """Removes any embedded ICC profiles from the image.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.unembed()
        return self

    def metadata_tags(self, filter: Union[dict, None] = None) -> 'XAImageEventsMetadataTagList':
        """Returns a list of metadata tags, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.metadataTags(), XAImageEventsMetadataTagList, filter)

    def profiles(self, filter: Union[dict, None] = None) -> 'XAImageEventsProfileList':
        """Returns a list of profiles, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        self._new_element(self.xa_elem.profiles(), XAImageEventsProfileList, filter)

    def get_clipboard_representation(self) -> List[AppKit.NSURL]:
        """Gets a clipboard-codable representation of the image.

        When the clipboard content is set an image, the image's file URL is added to the clipboard.

        :return: The URL of the image file
        :rtype: List[AppKit.NSURL]

        .. versionadded:: 0.1.0
        """
        return [self.image_file.url.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAImageEventsMetadataTagList(XABase.XAList):
    """A wrapper around lists of metadata tags that employs fast enumeration techniques.

    All properties of metadata tags can be called as methods on the wrapped list, returning a list containing each tag's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImageEventsMetadataTag, filter)

    def description(self) -> List['str']:
        """Retrieves the description of each tag's function.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("description"))

    def name(self) -> List['str']:
        """Retrieves the name of each tag in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def value(self) -> List[Union[bool, int, float, str, 'XAImageEventsProfile', any]]:
        """Retrieves the current setting of each tag in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("value")
        for index, value in enumerate(ls):
            if isinstance(value, ScriptingBridge.SBObject):
                ls[index] = self._new_element(value, XAImageEventsProfile)
        return list(ls)

    def by_description(self, description: str) -> 'XAImageEventsMetadataTag':
        """Retrieves the metadata tag whose description matches the given description.

        .. versionadded:: 0.1.0
        """
        return self.by_property("description", description)

    def by_name(self, name: str) -> 'XAImageEventsMetadataTag':
        """Retrieves the metadata tag whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_value(self, value: List[Union[bool, int, float, str, 'XAImageEventsProfile', any]]) -> 'XAImageEventsMetadataTag':
        """Retrieves the metadata tag whose value matches the given value.

        .. versionadded:: 0.1.0
        """
        if isinstance(value, XAImageEventsProfile):
            value = value.xa_elem
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsMetadataTag(XABase.XAObject):
    """A metadata tag: EXIF, IPTC, etc.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def description(self) -> 'str':
        """The description of the tag's function.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.description()

    @property
    def name(self) -> 'str':
        """The name of the tag.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def value(self) -> Union[bool, int, float, str, 'XAImageEventsProfile', any]:
        """The current setting of the tag.

        .. versionadded:: 0.1.0
        """
        value = self.xa_elem.value()
        if isinstance(value, ScriptingBridge.SBObject):
            return self._new_element(value, XAImageEventsProfile)
        return value

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAImageEventsProfileList(XABase.XAList):
    """A wrapper around lists of profiles that employs fast enumeration techniques.

    All properties of profiles can be called as methods on the wrapped list, returning a list containing each profile's value for the property.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAImageEventsProfile, filter)

    def color_space(self) -> List['XAImageEventsApplication.ColorSpace']:
        """Retrieves the color space of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("colorSpace")
        return [XAImageEventsApplication.ColorSpace(XABase.OSType(x.stringValue())) for x in ls]

    def connection_space(self) -> List['XAImageEventsApplication.ConnectionSpace']:
        """Retrieves the connection space of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("connectionSpace")
        return [XAImageEventsApplication.ConnectionSpace(XABase.OSType(x.stringValue())) for x in ls]

    def creation_date(self) -> List['datetime']:
        """Retrieves the creation date of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def creator(self) -> List['str']:
        """Retrieves the creator type of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creator"))

    def device_class(self) -> List['XAImageEventsApplication.DeviceClass']:
        """Retrieves the device class of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("deviceClass")
        return [XAImageEventsApplication.DeviceClass(XABase.OSType(x.stringValue())) for x in ls]

    def device_manufacturer(self) -> List['str']:
        """Retrieves the device manufacturer of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("deviceManufacturer"))

    def device_model(self) -> List['int']:
        """Retrieves the device model of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("deviceModel"))

    def location(self) -> 'XAImageEventsAliasList':
        """Retrieves the file location of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return self._new_element(ls, XAImageEventsAliasList)

    def name(self) -> List['str']:
        """Retrieves the description text of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def platform(self) -> List['str']:
        """Retrieves the intended platform of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("platform"))

    def preferred_cmm(self) -> List['str']:
        """Retrieves the preferred CMM of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("preferredCMM"))

    def quality(self) -> List['XAImageEventsApplication.ProfileQuality']:
        """Retrieves the quality of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("quality")
        return [XAImageEventsApplication.ProfileQuality(XABase.OSType(x.stringValue())) for x in ls]

    def rendering_intent(self) -> List['XAImageEventsApplication.RenderingIntent']:
        """Retrieves the rendering intent of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("renderingIntent")
        return [XAImageEventsApplication.RenderingIntent(XABase.OSType(x.stringValue())) for x in ls]

    def size(self) -> List['int']:
        """Retrieves the size, in bytes, of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def version(self) -> List['str']:
        """Retrieves the version number of each profile in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_color_space(self, color_space: XAImageEventsApplication.ColorSpace) -> 'XAImageEventsProfile':
        """Retrieves profile whose color space matches the given color space.

        .. versionadded:: 0.1.0
        """
        return self.by_property("colorSpace", color_space.value)

    def by_connection_space(self, connection_space: XAImageEventsApplication.ConnectionSpace) -> 'XAImageEventsProfile':
        """Retrieves profile whose connection space matches the given connection space.

        .. versionadded:: 0.1.0
        """
        return self.by_property("connectionSpace", connection_space.value)

    def by_creation_date(self, creation_date: datetime) -> 'XAImageEventsProfile':
        """Retrieves profile whose creation date matches the given date.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creationDate", creation_date)

    def by_creator(self, creator) -> 'XAImageEventsProfile':
        """Retrieves profile whose creator matches the given creator.

        .. versionadded:: 0.1.0
        """
        return self.by_property("creator", creator)

    def by_device_class(self, device_class: XAImageEventsApplication.DeviceClass) -> 'XAImageEventsProfile':
        """Retrieves profile.whose device class matches the given device class.

        .. versionadded:: 0.1.0
        """
        return self.by_property("deviceClass", device_class.value)

    def by_device_manufacturer(self, device_manufacturer: str) -> 'XAImageEventsProfile':
        """Retrieves profile whose device manufacturer matches the given device manufacturer.

        .. versionadded:: 0.1.0
        """
        return self.by_property("deviceManufacturer", device_manufacturer)

    def by_device_model(self, device_model: str) -> 'XAImageEventsProfile':
        """Retrieves profile whose device model matches the given device model.

        .. versionadded:: 0.1.0
        """
        return self.by_property("deviceModel", device_model)

    def by_location(self, location: 'XAImageEventsAlias') -> 'XAImageEventsProfile':
        """Retrieves profile whose location matches the given location.

        .. versionadded:: 0.1.0
        """
        return self.by_property("location", location.xa_elem)

    def by_name(self, name: str) -> 'XAImageEventsProfile':
        """Retrieves profile whose name matches the given name.

        .. versionadded:: 0.1.0
        """
        return self.by_property("name", name)

    def by_platform(self, platform: str) -> 'XAImageEventsProfile':
        """Retrieves profile whose platform matches the given platform.

        .. versionadded:: 0.1.0
        """
        return self.by_property("platform", platform)

    def by_preferred_cmm(self, preferred_cmm: str) -> 'XAImageEventsProfile':
        """Retrieves profile whose preferred_cmm matches the given preferred_cmm.

        .. versionadded:: 0.1.0
        """
        return self.by_property("preferredCMM", preferred_cmm)

    def by_quality(self, quality: XAImageEventsApplication.ProfileQuality) -> 'XAImageEventsProfile':
        """Retrieves profile whose quality matches the given quality.

        .. versionadded:: 0.1.0
        """
        return self.by_property("quality", quality.value)

    def by_rendering_intent(self, rendering_intent: XAImageEventsApplication.RenderingIntent) -> 'XAImageEventsProfile':
        """Retrieves profile whose rendering intent matches the given rendering intent.

        .. versionadded:: 0.1.0
        """
        return self.by_property("renderingIntent", rendering_intent.value)

    def by_size(self, size: int) -> 'XAImageEventsProfile':
        """Retrieves profile whose size matches the given size.

        .. versionadded:: 0.1.0
        """
        return self.by_property("size", size)

    def by_version(self, version: str) -> 'XAImageEventsProfile':
        """Retrieves the profile whose version matches the given version.

        .. versionadded:: 0.1.0
        """
        return self.by_property("version", version)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsProfile(XABase.XAObject):
    """A ColorSync ICC profile.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def color_space(self) -> 'XAImageEventsApplication.ColorSpace':
        """The color space of the profile.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.ColorSpace(self.xa_elem.colorSpace())

    @property
    def connection_space(self) -> 'XAImageEventsApplication.ConnectionSpace':
        """The connection space of the profile.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.ConnectionSpace(self.xa_elem.connectionSpace())

    @property
    def creation_date(self) -> 'datetime':
        """The creation date of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creationDate()

    @property
    def creator(self) -> 'str':
        """The creator type of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creator()

    @property
    def device_class(self) -> 'XAImageEventsApplication.DeviceClass':
        """The device class of the profile.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.DeviceClass(self.xa_elem.deviceClass())

    @property
    def device_manufacturer(self) -> 'str':
        """The device manufacturer of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.deviceManufacturer()

    @property
    def device_model(self) -> 'int':
        """The device model of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.deviceModel()

    @property
    def location(self) -> 'XAImageEventsAlias':
        """The file location of the profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.location(), XAImageEventsAlias)

    @property
    def name(self) -> 'str':
        """The description text of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def platform(self) -> 'str':
        """The intended platform of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.platform()

    @property
    def preferred_cmm(self) -> 'str':
        """The preferred CMM of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.preferredCMM()

    @property
    def quality(self) -> 'XAImageEventsApplication.ProfileQuality':
        """The quality of the profile.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.ProfileQuality(self.xa_elem.quality())

    @property
    def rendering_intent(self) -> 'XAImageEventsApplication.RenderingIntent':
        """The rendering intent of the profile.

        .. versionadded:: 0.1.0
        """
        return XAImageEventsApplication.RenderingIntent(self.xa_elem.renderingIntent())

    @property
    def size(self) -> 'int':
        """The size of the profile in bytes.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.size()

    @property
    def version(self) -> 'str':
        """The version number of the profile.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"