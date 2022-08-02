""".. versionadded:: 0.0.2

Control the macOS Photos application using JXA-like syntax.

.. todo::

   - Add support for folders and containers
   - Add image operations such as rotate, flip
   - Add ability to add new albums
   - Add ability to move photos to albums/folders
"""
from datetime import datetime
from typing import Union, List
from AppKit import NSImage, NSURL, NSFileManager

from PyXA import XABase
from PyXA import XABaseScriptable
        

class XAPhotosApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Photos.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the application
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Photos is the frontmost application
        self.version: str #: The version of Photos.app
        self.selection: XAPhotosMediaItemList #: The currently selected media items in the application
        self.favorites_album: XAPhotosAlbum #: Favorited media items album.
        self.slideshow_running: bool #: Returns true if a slideshow is currently running.
        self.recently_deleted_album: XAPhotosAlbum #: The set of recently deleted media items

    @property
    def properties(self) -> dict:
        return self.xa_scel.properties()

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
    def selection(self) -> 'XAPhotosMediaItemList':
        return self._new_element(self.xa_scel.selection(), XAPhotosMediaItemList)

    @property
    def favorites_album(self) -> 'XAPhotosAlbum':
        return self._new_element(self.xa_scel.favoritesAlbum(), XAPhotosAlbum)

    @property
    def slideshow_running(self) -> bool:
        return self.xa_scel.slideshowRunning()

    @property
    def recently_deleted_album(self) -> 'XAPhotosAlbum':
        return self._new_element(self.xa_scel.recentlyDeletedAlbum(), XAPhotosAlbum)

    def open(self, path: Union[str, NSURL]) -> 'XAPhotosApplication':
        """Imports the file at the given filepath without adding it to any particular album.

        :param target: The path to a file to import into photos.
        :type target: Union[str, NSURL]
        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.1
        """
        return self.import_files([path])

    def import_files(self, files: List[Union[str, NSURL]], destination_album: Union['XAPhotosAlbum', None] = None, skip_duplicate_checking: bool = False) -> 'XAPhotosMediaItemList':
        """Imports a list of files into the specified album.

        :param files: The files to import
        :type files: List[Union[str, NSURL]]
        :param destination_album: The album to import items into, defaults to None
        :type destination_album: Union[XAPhotosAlbum, None], optional
        :param skip_duplicate_checking: Whether the skip checking duplicates and import everything, defaults to False
        :type skip_duplicate_checking: bool, optional
        :return: The list of imported media items
        :rtype: XAPhotosMediaItemList

        .. versionadded:: 0.0.6
        """
        urls = []
        for file in files:
            if not isinstance(file, NSURL):
                file = XABase.XAPath(file).xa_elem
            urls.append(file)

        ls = None
        if destination_album is None:
            ls = self.xa_scel.import_into_skipCheckDuplicates_(urls, None, skip_duplicate_checking)
        else:
            ls = self.xa_scel.import_into_skipCheckDuplicates_(urls, destination_album.xa_elem, skip_duplicate_checking)
        return self._new_element(ls, XAPhotosMediaItemList)

    def export(self, media_items: Union['XAPhotosMediaItemList', List['XAPhotosMediaItem']], destination_path: Union[str, NSURL], use_originals: bool = False) -> 'XAPhotosApplication':
        """Exports a list of media items to the specified folder.

        :param media_items: The media items to export
        :type media_items: Union[XAPhotosMediaItemList, List[XAPhotosMediaItem]]
        :param destination_path: The folder to store the exported files in
        :type destination_path: Union[str, NSURL]
        :param use_originals: Whether to export the original files or rendered jpgs, defaults to False
        :type use_originals: bool, optional
        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        if not isinstance(destination_path, NSURL):
            destination_path = XABase.XAPath(destination_path).xa_elem
        if isinstance(media_items, XAPhotosMediaItemList):
            self.xa_scel.export_to_usingOriginals_(media_items.xa_elem, destination_path, use_originals)
        else:
            self.xa_scel.export_to_usingOriginals_(media_items, destination_path, use_originals)
        return self


    def search(self, query: str) -> 'XAPhotosMediaItemList':
        """Searches for items matching the given search string.

        :param query: The string to search
        :type query: str
        :return: A list of media items matching the search query
        :rtype: XAPhotosMediaItemList

        .. versionadded:: 0.0.6
        """
        ls = self.xa_scel.searchFor_(query)
        print(ls)
        return self._new_element(ls, XAPhotosMediaItemList)

    def add(self, media_items: Union['XAPhotosMediaItemList', List['XAPhotosMediaItem']], album: 'XAPhotosAlbum') -> 'XAPhotosApplication':
        """Adds the given list of media items to the specified album.

        :param media_items: The media items to add
        :type media_items: Union[XAPhotosMediaItemList, List[XAPhotosMediaItem]]
        :param album: The album to add the media items to
        :type album: XAPhotosAlbum
        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        if isinstance(media_items, XAPhotosMediaItemList):
            self.xa_scel.add_to_(media_items.xa_elem, album.xa_elem)
        else:
            self.xa_scel.add_to_(media_items, album.xa_elem)
        return self

    def start_slideshow(self, item_list: Union['XAPhotosMediaItemList', 'XAPhotosAlbum', 'XAPhotosFolder']) -> 'XAPhotosApplication':
        """Starts an ad-hoc slideshow from the given list of media items, an album, or a folder.

        :param item_list: The list of media items, an album, or a folder to create a slideshow from
        :type item_list: Union['XAPhotosMediaItemList', 'XAPhotosAlbum', 'XAPhotosFolder']
        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.startSlideshowUsing_(item_list.xa_elem)
        return self

    def stop_slideshow(self) -> 'XAPhotosApplication':
        """Stops the currently playing slideshow.

        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.endSlideshow()
        return self

    def next_slide(self) -> 'XAPhotosApplication':
        """Skips to the next slide in the currently playing slideshow.

        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.nextSlide()
        return self

    def previous_slide(self) -> 'XAPhotosApplication':
        """Skips to the previous slide in the currently playing slideshow.

        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.previousSlide()
        return self

    def pause_slideshow(self) -> 'XAPhotosApplication':
        """Pauses the currently playing slideshow.

        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.pauseSlideshow()
        return self

    def resume_slideshow(self) -> 'XAPhotosApplication':
        """Resumes the currently playing slideshow (from a paused state).

        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.resumeSlideshow()
        return self

    def containers(self, filter: Union[dict, None] = None) -> 'XAPhotosContainerList':
        """Returns a list of containers, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned containers will have, or None
        :type filter: Union[dict, None]
        :return: The list of containers
        :rtype: XAPhotosContainerList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.containers(), XAPhotosContainerList, filter)

    def albums(self, filter: Union[dict, None] = None) -> 'XAPhotosAlbumList':
        """Returns a list of albums, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned albums will have, or None
        :type filter: Union[dict, None]
        :return: The list of albums
        :rtype: XAPhotosAlbumList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.albums(), XAPhotosAlbumList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAPhotosFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XAPhotosFolderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.folders(), XAPhotosFolderList, filter)

    def media_items(self, filter: Union[dict, None] = None) -> 'XAPhotosMediaItemList':
        """Returns a list of media items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned media items will have, or None
        :type filter: Union[dict, None]
        :return: The list of media items
        :rtype: XAPhotosMediaItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.mediaItems(), XAPhotosMediaItemList, filter)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new album

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> new_album = app.make("album", {"name": "PyXA"})
        >>> app.albums().push(new_album)

        .. versionadded:: 0.0.6
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "album":
            elem = self._new_element(obj, XAPhotosAlbum)
            return elem
        elif specifier == "folder":
            elem = self._new_element(obj, XAPhotosFolder)
            return elem





class XAPhotosMediaItemList(XABase.XAList):
    """A wrapper around lists of media items that employs fast enumeration techniques.

    All properties of media items can be called as methods on the wrapped list, returning a list containing each media item's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPhotosMediaItem, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each media item in the list.

        :return: A list of media item properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def keywords(self) -> List[List[str]]:
        """Gets the keywords of each media item in the list.

        :return: A list of media item keywords
        :rtype: List[List[str]]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("keywords"))

    def name(self) -> List[str]:
        """Gets the name of each media item in the list.

        :return: A list of media item names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def object_description(self) -> List[str]:
        """Gets the object description of each media item in the list.

        :return: A list of media item descriptions
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription"))

    def favorite(self) -> List[bool]:
        """Gets the favorited status of each media item in the list.

        :return: A list of media item favorited status boolean values
        :rtype: List[bool]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def date(self) -> List[datetime]:
        """Gets the date of each media item in the list.

        :return: A list of media item dates
        :rtype: List[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("date"))

    def id(self) -> List[str]:
        """Gets the ID of each media item in the list.

        :return: A list of media item IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def height(self) -> List[int]:
        """Gets the height of each media item in the list.

        :return: A list of media item heights
        :rtype: List[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("height"))

    def width(self) -> List[int]:
        """Gets the width of each media item in the list.

        :return: A list of media item widths
        :rtype: List[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("width"))

    def filename(self) -> List[str]:
        """Gets the filename of each media item in the list.

        :return: A list of media item filenames
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("filename"))

    def altitude(self) -> List[float]:
        """Gets the altitude of each media item in the list.

        :return: A list of media item altitudes
        :rtype: List[float]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("altitude"))

    def size(self) -> List[int]:
        """Gets the file size of each media item in the list.

        :return: A list of media item file sizes
        :rtype: List[int]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("size"))

    def location(self) -> List[List[Union[float, None]]]:
        """Gets the location of each media item in the list.

        :return: A list of media item locations
        :rtype: List[List[Union[float, None]]]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XALocation(
            latitude = x.get()[0],
            longitude = x.get()[1],
        ) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose properties matches the given properties dictionary, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_keywords(self, keywords: List[str]) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose keywords list matches the given keywords, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("keywords", keywords)

    def by_name(self, name: str) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose name matches the given name string, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_object_description(self, object_description: str) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose object description matches the given description, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("objectDescription", object_description)

    def by_favorite(self, favorite: bool) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose favorited status matches the given boolean value, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("favorite", favorite)

    def by_date(self, date: datetime) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose date matches the given date, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("date", date)

    def by_id(self, id: str) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose ID matches the given ID, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_height(self, height: int) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose height matches the given height, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("height", height)

    def by_width(self, width: int) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose width matches the given width, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("width", width)

    def by_filename(self, filename: str) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose filename matches the given filename, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("filename", filename)

    def by_altitude(self, altitude: float) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose altitude matches the given altitude, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("altitude", altitude)

    def by_size(self, size: int) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose file size matches the given size, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("size", size)

    def by_location(self, location: XABase.XALocation) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose location matches the given location, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        loc = (location.latitude, location.longitude)
        return self.by_property("location", loc)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XAPhotosMediaItem(XABase.XAObject):
    """A photo or video in Photos.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the media item
        self.keywords: List[str] #: A list of keywords to associate with a media item
        self.name: str #: The name (title) of the media item.
        self.object_description: str #: A description of the media item.
        self.favorite: bool #: Whether the media item has been favorited.
        self.date: datetime #: The date of the media item
        self.id: str #: The unique ID of the media item
        self.height: int #: The height of the media item in pixels.
        self.width: int #: The width of the media item in pixels.
        self.filename: str #: The name of the file on disk.
        self.altitude: float #: The GPS altitude in meters.
        self.size: int #: The selected media item file size.
        self.location: XABase.XALocation #: The GPS latitude and longitude, in an ordered list of 2 numbers or missing values. Latitude in range -90.0 to 90.0, longitude in range -180.0 to 180.0.

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def keywords(self) -> List[str]:
        return self.xa_elem.keywords()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def object_description(self) -> str:
        return self.xa_elem.objectDescription()

    @property
    def favorite(self) -> bool:
        return self.xa_elem.favorite()

    @property
    def date(self) -> datetime:
        return self.xa_elem.date()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def height(self) -> int:
        return self.xa_elem.height()

    @property
    def width(self) -> int:
        return self.xa_elem.width()

    @property
    def filename(self) -> str:
        return self.xa_elem.filename()

    @property
    def altitude(self) -> float:
        return self.xa_elem.altitude()

    @property
    def size(self) -> int:
        return self.xa_elem.size()

    @property
    def location(self) -> XABase.XALocation:
        loc = self.xa_elem.location().get()
        return XABase.XALocation(
            latitude = loc[0],
            longitude = loc[1],
            altitude = self.altitude,
        )

    def spotlight(self) -> 'XAPhotosMediaItem':
        """Shows the media item in the front window of Photos.app.

        :return: The media item object
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.6
        """
        self.xa_elem.spotlight()
        return self

    def duplicate(self) -> 'XAPhotosMediaItem':
        """Duplicates the media item.

        :return: The newly created media item object
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.2
        """
        return self.xa_elem.duplicate()

    def show_in_preview(self):
        """Opens the media item in Preview.app.

        .. versionadded:: 0.0.2
        """
        home = NSFileManager.defaultManager().homeDirectoryForCurrentUser()
        url = home.URLByAppendingPathComponent_("Pictures/Photos Library.photoslibrary/originals/")
        url = url.URLByAppendingPathComponent_(self.id[0])
        url = url.URLByAppendingPathComponent_(self.id[:-7] + self.filename[self.filename.index("."):].lower())
        self.xa_wksp.openURL_(url)

    def reveal_in_finder(self):
        """Opens a Finder window or tab focused on the media item's containing folder with the media item selected.

        .. versionadded:: 0.0.2
        """
        home = NSFileManager.defaultManager().homeDirectoryForCurrentUser()
        url = home.URLByAppendingPathComponent_("Pictures/Photos Library.photoslibrary/originals/")
        url = url.URLByAppendingPathComponent_(self.id[0])
        url = url.URLByAppendingPathComponent_(self.id[:-7] + self.filename[self.filename.index("."):].lower())
        self.xa_wksp.activateFileViewerSelectingURLs_([url])

    def copy_to_clipboard(self):
        """Copies the media file and its data to the clipboard.

        .. versionadded:: 0.0.2
        """
        home = NSFileManager.defaultManager().homeDirectoryForCurrentUser()
        url = home.URLByAppendingPathComponent_("Pictures/Photos Library.photoslibrary/originals/")
        url = url.URLByAppendingPathComponent_(self.id[0])
        url = url.URLByAppendingPathComponent_(self.id[:-7] + self.filename[self.filename.index("."):].lower())
        img = NSImage.alloc().initWithContentsOfFile_(url.path())
        self.set_clipboard([url])

    def __repr__(self):
        if self.name is None:
            return "<" + str(type(self)) + "id=" + self.id + ">"
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"




class XAPhotosContainerList(XABase.XAList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    All properties of containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, obj_class = None, filter: Union[dict, None] = None):
        if obj_class is None:
            obj_class = XAPhotosContainer
        super().__init__(properties, obj_class, filter)

    def properties(self) -> List[dict]:
        """Gets the properties of each container in the list.

        :return: A list of container properties dictionaries
        :rtype: List[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def id(self) -> List[str]:
        """Gets the ID of each container in the list.

        :return: A list of container IDs
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> List[str]:
        """Gets the name of each container in the list.

        :return: A list of container names
        :rtype: List[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def parent(self) -> 'XAPhotosFolderList':
        """Gets the parent of each container in the list.

        :return: A list of container parent folders
        :rtype: XAPhotosFolderList
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("parent")
        return self._new_element(ls, XAPhotosFolderList)

    def by_properties(self, properties: dict) -> Union['XAPhotosContainer', None]:
        """Retrieves the container whose properties matches the given properties dictionary, if one exists.

        :return: The desired container, if it is found
        :rtype: Union[XAPhotosContainer, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("properties", properties)

    def by_id(self, id: str) -> Union['XAPhotosContainer', None]:
        """Retrieves the container whose ID matches the given ID, if one exists.

        :return: The desired container, if it is found
        :rtype: Union[XAPhotosContainer, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XAPhotosContainer', None]:
        """Retrieves the first container whose name matches the given name, if one exists.

        :return: The desired container, if it is found
        :rtype: Union[XAPhotosContainer, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("name", name)

    def by_parent(self, parent: 'XAPhotosFolder') -> Union['XAPhotosContainer', None]:
        """Retrieves the first container whose parent matches the given folder, if one exists.

        :return: The desired container, if it is found
        :rtype: Union[XAPhotosContainer, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("parent", parent.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPhotosContainer(XABase.XAObject):
    """A class for...
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the container
        self.id: str #: The unique ID of this container
        self.name: str #: The name of this container
        self.parent: XAPhotosFolder #: This container's parent folder, if any

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def parent(self) -> 'XAPhotosFolder':
        return self._new_element(self.xa_elem.parent(), XAPhotosFolder)

    def spotlight(self) -> 'XAPhotosContainer':
        """Shows the container in the front window of Photos.app.

        :return: The container object
        :rtype: XAPhotosContainer

        .. versionadded:: 0.0.6
        """
        self.xa_elem.spotlight()
        return self

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"




class XAPhotosAlbumList(XAPhotosContainerList):
    """A wrapper around lists of albums that employs fast enumeration techniques.

    All properties of albums can be called as methods on the wrapped list, returning a list containing each album's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPhotosAlbum, filter)

    def push(self, container: 'XAPhotosContainer'):
        name = "New Album"
        desc = container.xa_elem.description()
        if "name" in desc:
            name = desc[desc.index("name") + 7:desc.index(";")]
        super().push(container)
        container.set_property("name", name)

class XAPhotosAlbum(XAPhotosContainer):
    """An album in Photos.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
    
    def media_items(self, filter: Union[dict, None] = None) -> 'XAPhotosMediaItemList':
        """Returns a list of media items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned media items will have, or None
        :type filter: Union[dict, None]
        :return: The list of media items
        :rtype: XAPhotosMediaItemList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.mediaItems(), XAPhotosMediaItemList, filter)




class XAPhotosFolderList(XAPhotosContainerList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folder's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPhotosFolder, filter)

    def push(self, container: 'XAPhotosContainer'):
        name = "New Folder"
        desc = container.xa_elem.description()
        if "name" in desc:
            name = desc[desc.index("name") + 7:desc.index(";")]
        super().push(container)
        container.set_property("name", name)

class XAPhotosFolder(XAPhotosContainer):
    """A folder in Photos.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def containers(self, filter: Union[dict, None] = None) -> 'XAPhotosContainerList':
        """Returns a list of containers, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned containers will have, or None
        :type filter: Union[dict, None]
        :return: The list of containers
        :rtype: XAPhotosContainerList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.containers(), XAPhotosContainerList, filter)

    def albums(self, filter: Union[dict, None] = None) -> 'XAPhotosAlbumList':
        """Returns a list of albums, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned albums will have, or None
        :type filter: Union[dict, None]
        :return: The list of albums
        :rtype: XAPhotosAlbumList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.albums(), XAPhotosAlbumList, filter)

    def folders(self, filter: Union[dict, None] = None) -> 'XAPhotosFolderList':
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XAPhotosFolderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.folders(), XAPhotosFolderList, filter)