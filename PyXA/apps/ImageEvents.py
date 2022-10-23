from datetime import datetime
from enum import Enum
from typing import Any, Callable, Tuple, Union, List, Dict
from time import sleep, time
from threading import Timer

import AppKit
import ScriptingBridge
from PyObjCTools import AppHelper

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAEvents import event_from_int, event_from_str
from ..XAProtocols import XACanOpenPath, XAClipboardCodable, XAImageLike

class XAImageEventsApplication(XABase.XAEventsApplication, XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for interacting with Image Events.app.

    .. versionadded:: 0.1.0
    """
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
        PSD         = XABase.OSType("psd ")
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
    def application_support_folder(self) -> 'XABase.XAFolder':
        """The Application Support folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.applicationSupportFolder(), XABase.XAFolder)

    @property
    def applications_folder(self) -> 'XABase.XAFolder':
        """The user's Applications folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.applicationsFolder(), XABase.XAFolder)

    @property
    def classic_domain(self) -> 'XABase.XAClassicDomainObject':
        """The collection of folders belonging to the Classic System.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.classicDomain(), XABase.XAClassicDomainObject)

    @property
    def desktop_folder(self) -> 'XABase.XAFolder':
        """The user's Desktop folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.desktopFolder(), XABase.XAFolder)

    @property
    def desktop_pictures_folder(self) -> 'XABase.XAFolder':
        """The Desktop Pictures folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.desktopPicturesFolder(), XABase.XAFolder)

    @property
    def documents_folder(self) -> 'XABase.XAFolder':
        """The user's Documents folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.documentsFolder(), XABase.XAFolder)

    @property
    def downloads_folder(self) -> 'XABase.XAFolder':
        """The user's Downloads folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.downloadsFolder(), XABase.XAFolder)

    @property
    def favorites_folder(self) -> 'XABase.XAFolder':
        """The user's Favorites folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.favoritesFolder(), XABase.XAFolder)

    @property
    def folder_action_scripts_folder(self) -> 'XABase.XAFolder':
        """The user's Folder Action Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folderActionScriptsFolder(), XABase.XAFolder)

    @property
    def fonts_folder(self) -> 'XABase.XAFolder':
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.fontsFolder(), XABase.XAFolder)

    @property
    def home_folder(self) -> 'XABase.XAFolder':
        """The Home folder of the currently logged in user.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.homeFolder(), XABase.XAFolder)

    @property
    def library_folder(self) -> 'XABase.XAFolder':
        """The Library folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.libraryFolder(), XABase.XAFolder)

    @property
    def local_domain(self) -> 'XABase.XALocalDomainObject':
        """The collection of folders residing on the Local machine.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.localDomain(), XABase.XALocalDomainObject)

    @property
    def movies_folder(self) -> 'XABase.XAFolder':
        """The user's Movies folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.moviesFolder(), XABase.XAFolder)

    @property
    def music_folder(self) -> 'XABase.XAFolder':
        """The user's Music folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.musicFolder(), XABase.XAFolder)

    @property
    def network_domain(self) -> 'XABase.XANetworkDomainObject':
        """The collection of folders residing on the Network.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.networkDomain(), XABase.XANetworkDomainObject)

    @property
    def pictures_folder(self) -> 'XABase.XAFolder':
        """The user's Pictures folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.picturesFolder(), XABase.XAFolder)

    @property
    def preferences_folder(self) -> 'XABase.XAFolder':
        """The user's Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.preferencesFolder(), XABase.XAFolder)

    @property
    def public_folder(self) -> 'XABase.XAFolder':
        """The user's Public folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.publicFolder(), XABase.XAFolder)

    @property
    def scripting_additions_folder(self) -> 'XABase.XAFolder':
        """The Scripting Additions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.scriptingAdditionsFolder(), XABase.XAFolder)

    @property
    def scripts_folder(self) -> 'XABase.XAFolder':
        """The user's Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.scriptsFolder(), XABase.XAFolder)

    @property
    def shared_documents_folder(self) -> 'XABase.XAFolder':
        """The Shared Documents folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.sharedDocumentsFolder(), XABase.XAFolder)

    @property
    def sites_folder(self) -> 'XABase.XAFolder':
        """The user's Sites folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.sitesFolder(), XABase.XAFolder)

    @property
    def speakable_items_folder(self) -> 'XABase.XAFolder':
        """The Speakable Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.speakableItemsFolder(), XABase.XAFolder)

    @property
    def startup_disk(self) -> 'XABase.XADisk':
        """The disk from which Mac OS X was loaded.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.startupDisk(), XABase.XADisk)

    @property
    def system_domain(self) -> 'XABase.XASystemDomainObject':
        """The collection of folders belonging to the System.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.systemDomain(), XABase.XASystemDomainObject)

    @property
    def temporary_items_folder(self) -> 'XABase.XAFolder':
        """The Temporary Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.temporaryItemsFolder(), XABase.XAFolder)

    @property
    def trash(self) -> 'XABase.XAFolder':
        """The user's Trash folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.trash(), XABase.XAFolder)

    @property
    def user_domain(self) -> 'XABase.XAUserDomainObject':
        """The collection of folders belonging to the User.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.userDomain(), XABase.XAUserDomainObject)

    @property
    def utilities_folder(self) -> 'XABase.XAFolder':
        """The Utilities folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.utilitiesFolder(), XABase.XAFolder)

    @property
    def workflows_folder(self) -> 'XABase.XAFolder':
        """The Automator Workflows folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.workflowsFolder(), XABase.XAFolder)

    @property
    def default_cmyk_profile(self) -> 'XAImageEventsProfile':
        """The default CMYK profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultCMYKProfile(), XAImageEventsProfile)

    @property
    def default_cmyk_profile_location(self) -> 'XABase.XAFile':
        """The default CMYK profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultCMYKProfileLocation(), XABase.XAFile)

    @property
    def default_gray_profile(self) -> 'XAImageEventsProfile':
        """The default Gray profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultGrayProfile(), XAImageEventsProfile)

    @property
    def default_gray_profile_location(self) -> 'XABase.XAFile':
        """The default Gray profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultGrayProfileLocation(), XABase.XAFile)

    @property
    def default_lab_profile(self) -> 'XAImageEventsProfile':
        """The default Lab profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultLabProfile(), XAImageEventsProfile)

    @property
    def default_lab_profile_location(self) -> 'XABase.XAFile':
        """The default Lab profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultLabProfileLocation(), XABase.XAFile)

    @property
    def default_rgb_profile(self) -> 'XAImageEventsProfile':
        """The default RGB profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultRGBProfile(), XAImageEventsProfile)

    @property
    def default_rgb_profile_location(self) -> 'XABase.XAFile':
        """The default RGB profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultRGBProfileLocation(), XABase.XAFile)

    @property
    def default_xyz_profile(self) -> 'XAImageEventsProfile':
        """The default XYZ profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultXYZProfile(), XAImageEventsProfile)

    @property
    def default_xyz_profile_location(self) -> 'XABase.XAFile':
        """The default XYZ profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.defaultXYZProfileLocation(), XABase.XAFile)

    @property
    def preferred_cmm(self) -> 'str':
        """Specifies preferred Color Management Module to use, or "automatic".

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.preferredCMM()

    @property
    def profile_folder(self) -> 'XABase.XAAlias':
        """The ColorSync profile folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.profileFolder(), XABase.XAAlias)

    @property
    def quit_delay(self) -> 'int':
        """The time in seconds the application will idle before quitting; if set to zero, idle time will not cause the application to quit.

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.quitDelay()

    @property
    def system_profile(self) -> 'XAImageEventsProfile':
        """The default system profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.systemProfile(), XAImageEventsProfile)

    @property
    def system_profile_location(self) -> 'XABase.XAFile':
        """The default system profile location.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.systemProfileLocation(), XABase.XAFile)

    def aliases(self, filter: Union[dict, None] = None) -> 'XABase.XAAliasList':
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.aliases(), XABase.XAAliasList, filter)

    def disks(self, filter: Union[dict, None] = None) -> 'XABase.XADiskList':
        """Returns a list of disks, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.disks(), XABase.XADiskList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> 'XABase.XADiskItemList':
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.diskItems(), XABase.XADiskItemList, filter)

    def domains(self, filter: Union[dict, None] = None) -> 'XABase.XADomainList':
        """Returns a list of domains, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.domains(), XABase.XADomainList, filter)

    def files(self, filter: Union[dict, None] = None) -> 'XABase.XAFileList':
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.files(), XABase.XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> 'XABase.XAFilePackageList':
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.filePackages(), XABase.XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XABase.XAFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folders(), XABase.XAFolderList, filter)

    def items(self, filter: Union[dict, None] = None) -> 'XABase.XADiskItemList':
        """Returns a list of items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.items(), XABase.XADiskItemList, filter)

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
        else:
            paths = paths[0]
        file = self.xa_scel.open_(paths.xa_elem)
        return self._new_element(file, XAImageEventsImage)




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

    def properties(self) -> List[Dict]:
        pyxa_dicts = []
        ls = self.xa_elem.arrayByApplyingSelector_("properties")
        for raw_dict in ls:
            pyxa_dict = {
                "color_space": XAImageEventsApplication.ColorSpace(XABase.OSType(raw_dict["colorSpace"].stringValue())),
                "image_file": self._new_element(raw_dict["imageFile"], XABase.XAFile),
                "bit_depth": XAImageEventsApplication.BitDepth(XABase.OSType(raw_dict["bitDepth"].stringValue())),
                "dimensions": tuple(raw_dict["dimensions"]),
                "location": self._new_element(raw_dict["location"], XABase.XAFolder),
                "embedded_profile": self._new_element(raw_dict["embeddedProfile"], XAImageEventsProfile),
                "file_type": XAImageEventsApplication.FileType(XABase.OSType(raw_dict["fileType"].stringValue())),
                "class": "image",
                "name": raw_dict["name"],
                "resolution": tuple(raw_dict["resolution"])
            }
            pyxa_dicts.append(pyxa_dict)
        return pyxa_dicts

    def original_image_objects(self) -> XABase.XAImageList:
        """Retrieves the raw image contained in each image file, without modifications.

        :return: The images stored in each image file of the list
        :rtype: XABase.XAImage

        .. versionadded:: 0.1.0
        """
        image_paths = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            image_paths[index] = image.imageFile().POSIXPath()

        images = self._new_element(image_paths, XABase.XAImageList)
        return images

    def modified_image_objects(self) -> XABase.XAImageList:
        """Retrieves each image of the list as stored in active memory, including modifications.

        :return: The images in the list as stored in active memory
        :rtype: XABase.XAImage

        .. versionadded:: 0.1.0
        """
        image_paths = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            image_paths[index] =  image.imageFile().POSIXPath() + "-tmp." + image.imageFile().nameExtension()
            file_type = XABase.OSType(image.fileType().get().stringValue())
            image.saveAs_icon_in_PackBits_withCompressionLevel_(file_type, False, image_paths[index], False, XAImageEventsApplication.CompressionLevel.LOW.value)
        
        images = self._new_element(image_paths, XABase.XAImageList)

        def cleanup():
            for path in image_paths:
                AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(path, None) 
        
        t = Timer(1, cleanup)
        t.start()
        return images

    def bit_depth(self) -> List['XAImageEventsApplication.BitDepth']:
        """Retrieves the bit depth of each image in the list.

        .. versionadded:: 0.1.0
        """
        return [x.bit_depth for x in self]

    def color_space(self) -> List['XAImageEventsApplication.ColorSpace']:
        """Retrieves the color space of each image in the list.

        .. versionadded:: 0.1.0
        """
        return [x.color_space for x in self]

    def dimensions(self) -> List[List[int]]:
        """Retrieves the width and height of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("dimensions")
        return [tuple(x) for x in ls]

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
        return [XAImageEventsApplication.FileType(XABase.OSType(x.get().stringValue())) for x in ls]

    def image_file(self) -> 'XABase.XAFileList':
        """Retrieves the file of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("imageFile")
        return self._new_element(ls, XABase.XAFileList)

    def location(self) -> List['XABase.XADiskItem']:
        """Retrieves the folder or disk that encloses the file that contains each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return self._new_element(ls, XABase.XADiskItemList)

    def name(self) -> List['str']:
        """Retrieves the name of each image in the list.

        .. versionadded:: 0.1.0
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def resolution(self) -> List['float']:
        """Retrieves the horizontal and vertical pixel density of each image in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("resolution")
        return [tuple(x) for x in ls]

    def by_bit_depth(self, bit_depth) -> 'XAImageEventsApplication.BitDepth':
        """Retrieves the image whose bit depth matches the given bit depth.

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            if x.bitDepth() == bit_depth.value:
                return x

    def by_color_space(self, color_space: 'XAImageEventsApplication.ColorSpace') -> 'XAImageEventsImage':
        """Retrieves the image whose color space matches the given color space.

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            if x.colorSpace() == color_space.value:
                return x

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
        """Retrieves the first image whose file type matches the given file type.

        .. versionadded:: 0.1.0
        """
        for x in self.xa_elem:
            if x.fileType().get().stringValue() == XABase.unOSType(file_type.value):
                return x

    def by_image_file(self, image_file: 'XABase.XAFile') -> 'XAImageEventsImage':
        """Retrieves the image whose image file matches the given image file.

        .. versionadded:: 0.1.0
        """
        return self.by_property("imageFile", image_file.xa_elem)

    def by_location(self, location: 'XABase.XADiskItem') -> 'XAImageEventsImage':
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
            color = [color.red_value * 65535, color.green_value * 65535, color.blue_value * 65535]

        def pad_img(image, index, stop):
            dimensions = [image.dimensions()[0] + horizontal_padding, image.dimensions()[1] + vertical_padding]
            image.padToDimensions_withPadColor_(dimensions, color)

        self.xa_elem.enumerateObjectsUsingBlock_(pad_img)
        return self

    def rotate(self, angle: float) -> 'XAImageEventsImageList':
        """Rotates each image in the list to the specified angle.

        :param angle: The angle to rotate the images by
        :type angle: float
        :return: The list of images
        :rtype: XAImageEventsImageList

        .. versionadded:: 0.1.0
        """
        def rotate_img(image, index, stop):
            image.rotateToAngle_(angle)

        self.xa_elem.enumerateObjectsUsingBlock_(rotate_img)
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

        files = []
        def save_img(index, image):
            nonlocal file_type
            if file_type is None:
                file_type = XABase.OSType(image.fileType().get().stringValue())
            files.append(image.saveAs_icon_in_PackBits_withCompressionLevel_(file_type, add_icons, file_paths[index], pack_bits, compression_level.value))

        for index, image in enumerate(self.xa_elem):
            self._spawn_thread(save_img, [index, image])

        while len(files) != len(self.xa_elem):
            sleep(0.01)

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

        def scale_img(image, index, stop):
            nonlocal scale_factor
            if scale_factor != None:
                width = image.dimensions()[0] * scale_factor
            elif width != None:
                scale_factor = width / image.dimensions()[0]
                
            image.scaleByFactor_toSize_(scale_factor, width)

        self.xa_elem.enumerateObjectsUsingBlock_(scale_img)
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
        tmp_paths = [image.imageFile().POSIXPath() + "-tmp." + image.imageFile().nameExtension() for image in self.xa_elem]
        self.save(file_paths=tmp_paths)
        clipboard_reps = self._new_element(tmp_paths, XABase.XAImageList).get_clipboard_representation()

        def cleanup():
            nonlocal tmp_paths
            for path in tmp_paths:
                AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(path, None) 

        t = Timer(1, cleanup)
        t.start()
        return clipboard_reps

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAImageEventsImage(XABase.XAObject, XAClipboardCodable, XAImageLike):
    """An image contained in a file.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def __temp_save(self):
        path =  self.image_file.posix_path + "-tmp." + self.image_file.name_extension
        self.save(file_path=path)

        def cleanup(path):
            AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(path, None) 
        
        t = Timer(1, cleanup, [path])
        t.start()

    @property
    def properties(self) -> Dict:
        """All properties of the image.

        .. versionadded:: 0.1.0
        """
        raw_dict = self.xa_elem.properties()
        pyxa_dict = {
            "color_space": XAImageEventsApplication.ColorSpace(XABase.OSType(raw_dict["colorSpace"].stringValue())),
            "image_file": self._new_element(raw_dict["imageFile"], XABase.XAFile),
            "bit_depth": XAImageEventsApplication.BitDepth(XABase.OSType(raw_dict["bitDepth"].stringValue())),
            "dimensions": tuple(raw_dict["dimensions"]),
            "location": self._new_element(raw_dict["location"], XABase.XAFolder),
            "embedded_profile": self._new_element(raw_dict["embeddedProfile"], XAImageEventsProfile),
            "file_type": XAImageEventsApplication.FileType(XABase.OSType(raw_dict["fileType"].stringValue())),
            "class": "image",
            "name": raw_dict["name"],
            "resolution": tuple(raw_dict["resolution"])
        }
        return pyxa_dict

    @property
    def original_image_object(self) -> XABase.XAImage:
        """The original image contained in the file, without any modification.

        :return: The image object stored in the file
        :rtype: XABase.XAImage

        .. versionadded:: 0.1.0
        """
        path = self.image_file.posix_path
        img = XABase.XAImage(path)
        return img

    @property
    def modified_image_object(self) -> XABase.XAImage:
        """The image stored in active memory, including modifications.

        :return: The image object stored in active memory
        :rtype: XABase.XAImage

        .. versionadded:: 0.1.0
        """
        path =  self.image_file.posix_path + "-tmp." + self.image_file.name_extension
        self.save(file_path=path)
        img = XABase.XAImage(path)

        def cleanup(path):
            AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(path, None) 
        
        t = Timer(1, cleanup, [path])
        t.start()

        return img

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
    def dimensions(self) -> 'Tuple[int, int]':
        """The width and height of the image, respectively, in pixels.

        .. versionadded:: 0.1.0
        """
        if hasattr(self, "_dimensions"):
            return getattr(self, "_dimensions")
        return tuple(self.xa_elem.dimensions())

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
    def image_file(self) -> 'XABase.XAFile':
        """The file that contains the image.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.imageFile(), XABase.XAFile)

    @property
    def location(self) -> 'XABase.XADiskItem':
        """The folder or disk that encloses the file that contains the image.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.location(), XABase.XADiskItem)

    @property
    def name(self) -> 'str':
        """The name of the image.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def resolution(self) -> 'Tuple[float, float]':
        """The horizontal and vertical pixel density of the image, respectively, in dots per inch.

        .. versionadded:: 0.1.0
        """
        return tuple(self.xa_elem.resolution())

    def crop(self, width: int, height: int) -> 'XAImageEventsImage':
        """Crops the image to the specified width and height, originating at the center of the image.

        :param width: The width of the new image, in pixels
        :type width: int
        :param height: The height of the new image, in pixels
        :type height: int
        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cropToDimensions_([width, height])
        self._dimensions = (width, height)
        self.__temp_save()
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
        self.__temp_save()
        return self

    def flip_horizontally(self) -> 'XAImageEventsImage':
        """Flips the image horizontally.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.flipHorizontal_vertical_(True, False)
        self.__temp_save()
        return self

    def flip_vertically(self) -> 'XAImageEventsImage':
        """Flips the image vertically.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.flipHorizontal_vertical_(False, True)
        self.__temp_save()
        return self

    def pad(self, horizontal_padding: int = 10, vertical_padding: int = 10, color: Union[XABase.XAColor, List[int], None] = None) -> 'XAImageEventsImage':
        """Pads the image with a border of the specified color, or white by default.
        
        This will always replace transparent pixels, even when the padding in a given axis is set to 0.

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
            color = [color.red_value * 65535, color.green_value * 65535, color.blue_value * 65535]

        self.xa_elem.padToDimensions_withPadColor_(dimensions, color)
        self._dimensions = tuple(dimensions)
        self.__temp_save()
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

    def save(self, file_type: Union[XAImageEventsApplication.FileType, None] = None, add_icon: bool = False, file_path: Union[XABase.XAPath, str, None] = None, pack_bits: bool = False, compression_level: XAImageEventsApplication.CompressionLevel = XAImageEventsApplication.CompressionLevel.LOW) -> bool:
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
        :return: True if the image is successfully saved to the desired file location
        :rtype: bool

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, XABase.XAPath):
            file_path = file_path.path

        if file_type is not None:
            file_type = file_type.value
            file_path = "".join(self.image_file.posix_path.split(".")[:-1]) + "." + XABase.unOSType(file_type).lower().strip()
        else:
            file_type = self.file_type.value

        save_file = self.xa_elem.saveAs_icon_in_PackBits_withCompressionLevel_(file_type, add_icon, file_path, pack_bits, compression_level.value)
        if save_file is None:
            return False

        self.xa_elem = self.xa_elem.open_(save_file)
        return True

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
        self._dimensions = (self.dimensions[0] * scale_factor, self.dimensions[1] * scale_factor)
        # self.__temp_save()
        return self

    def unembed(self) -> 'XAImageEventsImage':
        """Removes any embedded ICC profiles from the image.

        :return: The image object
        :rtype: XAImageEventsImage

        .. versionadded:: 0.1.0
        """
        self.xa_elem.unembed()
        self.__temp_save()
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

    def get_clipboard_representation(self) -> AppKit.NSImage:
        """Gets a clipboard-codable representation of the image.

        When the clipboard content is set to an image, the image's raw data is added to the clipboard, including all current modifications.

        :return: The raw data of the image
        :rtype: AppKit.NSImage

        .. versionadded:: 0.1.0
        """
        file_path = "".join(self.image_file.posix_path.split(".")[:-1]) + "-tmp." + self.image_file.name_extension
        status = self.save(file_path=file_path)
        if (status):
            clipboard_rep = XABase.XAImage(file_path).get_clipboard_representation()
            AppKit.NSFileManager.defaultManager().removeFileAtPath_handler_(file_path, None)
            return clipboard_rep

    def get_image_representation(self) -> AppKit.NSImage:
        """Gets a representation of the object that can be used to initialize an :class:`~PyXA.XABase.XAImage` object.

        :return: The XAImage-compatible form of this object
        :rtype: AppKit.NSImage
        """
        return self.get_clipboard_representation()

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

    def location(self) -> 'XABase.XAAliasList':
        """Retrieves the file location of each profile in the list.

        .. versionadded:: 0.1.0
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return self._new_element(ls, XABase.XAAliasList)

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

    def by_location(self, location: 'XABase.XAAlias') -> 'XAImageEventsProfile':
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
    def location(self) -> 'XABase.XAAlias':
        """The file location of the profile.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.location(), XABase.XAAlias)

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