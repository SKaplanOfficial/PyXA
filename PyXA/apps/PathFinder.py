""".. versionadded:: 0.3.0

Control OmniWeb using JXA-like syntax.
"""

from enum import Enum
from typing import Union
from datetime import datetime
import threading

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import (
    XACanOpenPath,
    XACanPrintPath,
    XAClipboardCodable,
    XACloseable,
    XADeletable,
    XAPrintable,
)
from ..XAErrors import UnconstructableClassError
from ..XAEvents import event_from_str


class XAPathFinderApplication(
    XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath
):
    """A class for managing and interacting with Path Finder.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAPathFinderWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Path Finder is the frontmost application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of Path Finder.app."""
        return self.xa_scel.version()

    @property
    def home(self) -> "XAPathFinderFolder":
        return self._new_element(self.xa_scel.home(), XAPathFinderFolder)

    @property
    def selection(self) -> "XAPathFinderItemList":
        return self._new_element(self.xa_scel.selection(), XAPathFinderItemList)

    @property
    def startup_disk(self) -> "XAPathFinderDisk":
        return self._new_element(self.xa_scel.startupDisk(), XAPathFinderDisk)

    @property
    def desktop(self) -> "XAPathFinderFolder":
        return self._new_element(self.xa_scel.desktop(), XAPathFinderFolder)

    @property
    def trash(self) -> "XAPathFinderFolder":
        return self._new_element(self.xa_scel.trash(), XAPathFinderFolder)

    def disks(self) -> "XAPathFinderDiskList":
        """Returns a list of the disks in Path Finder."""
        return self._new_element(self.xa_scel.disks(), XAPathFinderDiskList)

    def finder_windows(self) -> "XAPathFinderFinderWindowList":
        """Returns a list of the finder windows in Path Finder."""
        return self._new_element(
            self.xa_scel.finderWindows(), XAPathFinderFinderWindowList
        )

    def info_windows(self) -> "XAPathFinderInfoWindowList":
        """Returns a list of the info windows in Path Finder."""
        return self._new_element(self.xa_scel.infoWindows(), XAPathFinderInfoWindowList)

    def add_toolbar_item(
        self, item: Union[str, "XAPathFinderItem", "XABase.XAPath"], position: int = 0
    ) -> int:
        """Adds an item to the toolbar.

        :param item: The item to add.
        :type item: Union[str, XAPathFinderItem]
        :param position: The target position to add the item at, defaults to 0.
        :type position: int, optional
        :returns: The actual position of the item.
        """
        if isinstance(item, str):
            item = XABase.XAPath(item)
        elif isinstance(item, XAPathFinderItem):
            item = item.posix_path
        return self.xa_scel.addToolbarItem_atPosition_(item.path, position)

    def remove_toolbar_item(
        self, item: Union[str, "XAPathFinderItem", "XABase.XAPath"]
    ) -> int:
        """Removes an item from the toolbar.

        :param item: The item to remove.
        :type item: Union[str, XAPathFinderItem]
        :returns: The position of the item prior to removal.
        """
        if isinstance(item, XAPathFinderItem) or isinstance(item, XABase.XAPath):
            item = item.name
        elif isinstance(item, str) and item.startswith("/"):
            item = XABase.XAPath(item).name
        return self.xa_scel.removeToolbarItem_(item)

    def empty(self) -> None:
        """Empties the trash."""
        self.xa_scel.empty()


class XAPathFinderWindow(XABaseScriptable.XASBWindow):
    """A window of Path Finder.app.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def document(self) -> "XAPathFinderDocument":
        """The active document."""
        return self._new_element(self.xa_elem.document(), XAPathFinderDocument)


class XAPathFinderFinderWindowList(XABaseScriptable.XASBWindowList):
    """A wrapper around lists of Path Finder finder windows that employs fast enumeration techniques.

    All properties of windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderFinderWindow)

    def target(self) -> "XAPathFinderContainerList":
        """The active target."""
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("target") or [],
            XAPathFinderContainerList,
        )

    def current_view(self) -> list[str]:
        """The current view."""
        return list(self.xa_elem.arrayByApplyingSelector_("currentView") or [])

    def by_target(
        self, target: "XAPathFinderContainer"
    ) -> Union["XAPathFinderFinderWindow", None]:
        return self.by_property("target", target.xa_elem)

    def by_current_view(
        self, current_view: str
    ) -> Union["XAPathFinderFinderWindow", None]:
        return self.by_property("currentView", current_view)


class XAPathFinderFinderWindow(XAPathFinderWindow):
    """A class for interacting with finder windows in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def target(self) -> "XAPathFinderContainer":
        """The active target."""
        return self._new_element(self.xa_elem.target(), XAPathFinderContainer)

    @property
    def current_view(self) -> str:
        """The current view."""
        return self.xa_elem.currentView()

    @current_view.setter
    def current_view(self, current_view: str):
        self.set_property("currentView", current_view)

    def open(self) -> None:
        """Opens the window."""
        self.xa_elem.open()


class XAPathFinderInfoWindowList(XABaseScriptable.XASBWindowList):
    """A wrapper around lists of Path Finder info windows that employs fast enumeration techniques.

    All properties of windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderInfoWindow)

    def item(self) -> "XAPathFinderItemList":
        """The active item."""
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("item") or [], XAPathFinderItemList
        )

    def by_item(
        self, item: "XAPathFinderItem"
    ) -> Union["XAPathFinderInfoWindow", None]:
        return self.by_property("item", item.xa_elem)


class XAPathFinderInfoWindow(XAPathFinderWindow):
    """A class for interacting with info windows in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def item(self) -> "XAPathFinderItem":
        """The active item."""
        return self._new_element(self.xa_elem.item(), XAPathFinderItem)


class XAPathFinderDocumentList(XABase.XAList):
    """A wrapper around lists of Path Finder documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPathFinderDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list["XABase.XAPath"]:
        return [
            XABase.XAPath(x)
            for x in self.xa_elem.arrayByApplyingSelector_("file") or []
        ]

    def by_name(self, name: str) -> Union["XAPathFinderDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XAPathFinderDocument", None]:
        return self.by_property("modified", modified)

    def by_file(
        self, file: Union[str, "XABase.XAPath"]
    ) -> Union["XAPathFinderDocument", None]:
        if isinstance(file, XABase.XAPath):
            file = file.path
        return self.by_property("file", file)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAPathFinderDocument(XABase.XAObject):
    """A class for interacting with documents in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def file(self) -> "XABase.XAPath":
        return XABase.XAPath(self.xa_elem.file())


class XAPathFinderItemList(XABase.XAList):
    """A wrapper around lists of Path Finder items that employs fast enumeration techniques.

    All properties of items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAPathFinderItemList
        super().__init__(properties, obj_class, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_name(self, name: str) -> Union["XAPathFinderItem", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAPathFinderItem(XABase.XAObject):
    """A class for interacting with items in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def extension_hidden(self) -> bool:
        return self.xa_elem.extensionHidden()

    @extension_hidden.setter
    def extension_hidden(self, extension_hidden: bool):
        self.set_property("extensionHidden", extension_hidden)

    @property
    def locked(self) -> bool:
        return self.xa_elem.locked()

    @locked.setter
    def locked(self, locked: bool):
        self.set_property("locked", locked)

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def group_privileges(self) -> str:
        return self.xa_elem.groupPrivileges()

    @group_privileges.setter
    def group_privileges(self, group_privileges: str):
        self.set_property("groupPrivileges", group_privileges)

    @property
    def displayed_name(self) -> str:
        return self.xa_elem.displayedName()

    @property
    def label_index(self) -> int:
        return self.xa_elem.labelIndex()

    @property
    def everyones_privileges(self) -> str:
        return self.xa_elem.everyonesPrivileges()

    @everyones_privileges.setter
    def everyones_privileges(self, everyones_privileges: str):
        self.set_property("everyonesPrivileges", everyones_privileges)

    @property
    def disk(self) -> "XAPathFinderDisk":
        return self._new_element(self.xa_elem.disk(), XAPathFinderDisk)

    @property
    def group(self) -> str:
        return self.xa_elem.group()

    @group.setter
    def group(self, group: str):
        self.set_property("group", group)

    @property
    def owner(self) -> str:
        return self.xa_elem.owner()

    @owner.setter
    def owner(self, owner: str):
        self.set_property("owner", owner)

    @property
    def information_window(self) -> "XAPathFinderInfoWindow":
        return self._new_element(
            self.xa_elem.informationWindow(), XAPathFinderInfoWindow
        )

    @property
    def owner_privileges(self) -> str:
        return self.xa_elem.ownerPrivileges()

    @owner_privileges.setter
    def owner_privileges(self, owner_privileges: str):
        self.set_property("ownerPrivileges", owner_privileges)

    @property
    def creation_date(self) -> datetime:
        return self.xa_elem.creationDate()

    @property
    def name_extension(self) -> str:
        return self.xa_elem.nameExtension()

    @property
    def physical_size(self) -> int:
        return self.xa_elem.physicalSize()

    @property
    def container(self) -> "XAPathFinderContainer":
        return self._new_element(self.xa_elem.container(), XAPathFinderContainer)

    @property
    def url(self) -> "XABase.XAURL":
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def posix_path(self) -> "XABase.XAPath":
        return XABase.XAPath(self.xa_elem.posixPath())

    @property
    def path(self) -> "XABase.XAPath":
        return XABase.XAPath(self.xa_elem.path())

    def reveal(self) -> None:
        """Reveals the item in Path Finder."""
        self.xa_elem.reveal()

    def select(self) -> None:
        """Selects the item in Path Finder."""
        self.xa_elem.select()

    def exists(self) -> bool:
        """Returns whether the item exists."""
        return self.xa_elem.exists()

    def delete(self) -> None:
        """Deletes the item."""
        self.xa_elem.delete()

    def eject(self) -> None:
        """Ejects the item."""
        self.xa_elem.eject()

    def open(
        self, application: Union[str, XABase.XAApplication] = "Path Finder"
    ) -> None:
        """Opens the item."""
        if isinstance(application, XABase.XAApplication):
            application = application.bundle_url
        self.xa_elem.PFOpenUsing_(application)

    def show_info(self) -> None:
        """Opens the item's info window."""
        self.xa_elem.PFInfo()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAPathFinderContainerList(XAPathFinderItemList):
    """A wrapper around lists of Path Finder containers that employs fast enumeration techniques.

    All properties of containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAPathFinderContainer
        super().__init__(properties, filter, obj_class)


class XAPathFinderContainer(XAPathFinderItem):
    """A class for interacting with containers in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    def folders(self) -> "XAPathFinderFolderList":
        """Returns a list of the folders in the container."""
        return self._new_element(self.xa_elem.fsFolders(), XAPathFinderFolderList)

    def files(self) -> "XAPathFinderFileList":
        """Returns a list of the files in the container."""
        return self._new_element(self.xa_elem.fsFiles(), XAPathFinderFileList)


class XAPathFinderFolderList(XAPathFinderContainerList):
    """A wrapper around lists of Path Finder folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folder's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderFolder)


class XAPathFinderFolder(XAPathFinderContainer):
    """A class for interacting with Path Finder folders and their contents.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAPathFinderDiskList(XAPathFinderContainerList):
    """A wrapper around lists of Path Finder disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderDisk)

    def local_volume(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume") or [])

    def startup(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("startup") or [])

    def ejectable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable") or [])

    def capacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity") or [])

    def free_space(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace") or [])

    def by_local_volume(self, local_volume: bool) -> Union["XAPathFinderDisk", None]:
        return self.by_property("localVolume", local_volume)

    def by_startup(self, startup: bool) -> Union["XAPathFinderDisk", None]:
        return self.by_property("startup", startup)

    def by_ejectable(self, ejectable: bool) -> Union["XAPathFinderDisk", None]:
        return self.by_property("ejectable", ejectable)

    def by_capacity(self, capacity: int) -> Union["XAPathFinderDisk", None]:
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union["XAPathFinderDisk", None]:
        return self.by_property("freeSpace", free_space)


class XAPathFinderDisk(XAPathFinderContainer):
    """A class for interacting with disks in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def local_volume(self) -> bool:
        return self.xa_elem.localVolume()

    @property
    def startup(self) -> bool:
        return self.xa_elem.startup()

    @property
    def ejectable(self) -> bool:
        return self.xa_elem.ejectable()

    @property
    def capacity(self) -> int:
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        return self.xa_elem.freeSpace()


class XAPathFinderFileList(XAPathFinderItemList):
    """A wrapper around lists of Path Finder files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderFile)

    def file_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def creator_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def by_file_type(self, file_type: str) -> Union["XAPathFinderFile", None]:
        return self.by_property("fileType", file_type)

    def by_creator_type(self, creator_type: str) -> Union["XAPathFinderFile", None]:
        return self.by_property("creatorType", creator_type)


class XAPathFinderFile(XAPathFinderItem):
    """A class for interacting with files in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def file_type(self) -> str:
        return self.xa_elem.fileType()

    @file_type.setter
    def file_type(self, file_type: str):
        self.set_property("fileType", file_type)

    @property
    def creator_type(self) -> str:
        return self.xa_elem.creatorType()

    @creator_type.setter
    def creator_type(self, creator_type: str):
        self.set_property("creatorType", creator_type)


class XAPathFinderActiveTargetList(XAPathFinderContainer):
    """A wrapper around lists of Path Finder active targets that employs fast enumeration techniques.

    All properties of active targets can be called as methods on the wrapped list, returning a list containing each active target's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderActiveTarget)


class XAPathFinderActiveTarget(XAPathFinderContainer):
    """A class for interacting with active targets in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAPathFinderLeftTargetList(XAPathFinderContainer):
    """A wrapper around lists of Path Finder left targets that employs fast enumeration techniques.

    All properties of left targets can be called as methods on the wrapped list, returning a list containing each left target's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderLeftTarget)


class XAPathFinderLeftTarget(XAPathFinderContainer):
    """A class for interacting with left targets in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAPathFinderRightTargetList(XAPathFinderContainer):
    """A wrapper around lists of Path Finder right targets that employs fast enumeration techniques.

    All properties of right targets can be called as methods on the wrapped list, returning a list containing each right target's value for the property.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPathFinderRightTarget)


class XAPathFinderRightTarget(XAPathFinderContainer):
    """A class for interacting with right targets in Path Finder.

    .. versionadded:: 0.3.0
    """

    def __init__(self, properties):
        super().__init__(properties)
