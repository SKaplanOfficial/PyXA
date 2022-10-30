""".. versionadded:: 0.0.2

Control the macOS Photos application using JXA-like syntax.

.. todo::

   - Add support for folders and containers
   - Add image operations such as rotate, flip
   - Add ability to add new albums
   - Add ability to move photos to albums/folders
"""
from curses import meta
from datetime import datetime
from pprint import pprint
from typing import Any, Union
from AppKit import NSImage, NSURL, NSFileManager

import AppKit
import Photos
import PhotosUI
import Quartz

from PyObjCTools import AppHelper

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable, XAImageLike
from ..XAErrors import AuthenticationError

class XAPhotosApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Photos.app.

    .. versionadded:: 0.0.2
    """
    def __check_authorization(self):
        # Check current authorization status
        auth_status = Photos.PHPhotoLibrary.authorizationStatusForAccessLevel_(Photos.PHAccessLevelReadWrite)

        # Request authorization if necessary
        if auth_status != Photos.PHAuthorizationStatusAuthorized:
            auth_status = Photos.PHPhotoLibrary.requestAuthorizationForAccessLevel_handler_(Photos.PHAccessLevelReadWrite, None)

        # Raise error on insufficient authorization status
        if auth_status != Photos.PHAuthorizationStatusAuthorized:
            raise AuthenticationError("You must grant PyXA access to the Photos library in order to use this module.")

    def __init__(self, properties):
        super().__init__(properties)

        # Ensure authorization to Photos library
        self.__check_authorization()

        self.__photos_library = Photos.PHPhotoLibrary.sharedPhotoLibrary()
        self.__image_manager = Photos.PHCachingImageManager.defaultManager()
        
        self.properties: dict #: All properties of the application
        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Photos is the frontmost application
        self.version: str #: The version of Photos.app
        self.selection: XAPhotosMediaItemList #: The currently selected media items in the application
        self.favorites_album: XAPhotosAlbum #: Favorited media items album.
        self.slideshow_running: bool #: Returns true if a slideshow is currently running.
        self.recently_deleted_album: XAPhotosAlbum #: The set of recently deleted media items
        self.library_path: XABase.XAPath #: The path to the Photos library container

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

    @property
    def library_path(self) -> XABase.XAPath:
        return XABase.XAPath(self.__photos_library.photoLibraryURL())

    def open(self, path: Union[str, XABase.XAPath, list[Union[str, XABase.XAPath]]]) -> 'XAPhotosApplication':
        """Imports the file at the given filepath without adding it to any particular album.

        :param target: The path to a file to import into photos.
        :type target: Union[str, XABase.XAPath, list[str, list[XABase.XAPath]]]
        :return: The Photos application object
        :rtype: XAPhotosApplication

        .. versionadded:: 0.0.1
        """
        if isinstance(path, list):
            for index, item in enumerate(path):
                if isinstance(item, str):
                    path[index] = XABase.XAPath(item)
            return self.import_files(path)

        if isinstance(path, str):
            return self.import_files([XABase.XAPath(path)])

        return self.import_files([path])

    def import_files(self, files: list[Union[str, NSURL]], destination_album: Union['XAPhotosAlbum', None] = None, skip_duplicate_checking: bool = False) -> 'XAPhotosMediaItemList':
        """Imports a list of files into the specified album.

        :param files: The files to import
        :type files: list[Union[str, NSURL]]
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
            if not isinstance(file, XABase.XAPath):
                file = XABase.XAPath(file)
            urls.append(file.xa_elem)

        ls = None
        if destination_album is None:
            ls = self.xa_scel.import_into_skipCheckDuplicates_(urls, None, skip_duplicate_checking)
        else:
            ls = self.xa_scel.import_into_skipCheckDuplicates_(urls, destination_album.xa_elem, skip_duplicate_checking)
        return self._new_element(ls, XAPhotosMediaItemList)

    def export(self, media_items: Union['XAPhotosMediaItemList', list['XAPhotosMediaItem']], destination_path: Union[str, NSURL], use_originals: bool = False) -> 'XAPhotosApplication':
        """Exports a list of media items to the specified folder.

        :param media_items: The media items to export
        :type media_items: Union[XAPhotosMediaItemList, list[XAPhotosMediaItem]]
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
        return self._new_element(ls, XAPhotosMediaItemList)

    def add(self, media_items: Union['XAPhotosMediaItemList', list['XAPhotosMediaItem']], album: 'XAPhotosAlbum') -> 'XAPhotosApplication':
        """Adds the given list of media items to the specified album.

        :param media_items: The media items to add
        :type media_items: Union[XAPhotosMediaItemList, list[XAPhotosMediaItem]]
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
        fetch_options = Photos.PHFetchOptions.alloc().init()
        all_photos = Photos.PHAsset.fetchAssetsWithOptions_(fetch_options)
        all_photos_list = all_photos.objectsAtIndexes_(AppKit.NSIndexSet.alloc().initWithIndexesInRange_((0, all_photos.count())))

        list_obj = self._new_element(all_photos_list, XAPhotosMediaItemList, filter)
        list_obj.xa_scel = self.xa_scel.mediaItems()
        return list_obj

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
        >>> app = PyXA.Application("Photos")
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




class XAPhotosMediaItemList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of media items that employs fast enumeration techniques.

    All properties of media items can be called as methods on the wrapped list, returning a list containing each media item's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPhotosMediaItem, filter)

        self.__resource_manager = Photos.PHAssetResourceManager.defaultManager()
        self.__image_manager = Photos.PHCachingImageManager.defaultManager()
        self.__metadata_storage = []

    def __get_metadata(self, asset, storage):
        def result_handler(img_data, img_uti, img_orientation, img_info):
            source = Quartz.CGImageSourceCreateWithData(img_data, {Quartz.kCGImageSourceShouldCache: True})
            metadata = Quartz.CGImageSourceCopyPropertiesAtIndex(source, 0, {Quartz.kCGImageSourceShouldCache: True})
            if metadata is not None:
                storage.append(metadata)
                print(metadata)

        options = Photos.PHImageRequestOptions.alloc().init()
        options.setSynchronous_(True)
        options.setDeliveryMode_(Photos.PHImageRequestOptionsDeliveryModeHighQualityFormat)

        self.__image_manager.requestImageDataAndOrientationForAsset_options_resultHandler_(asset, options, result_handler)

    def _new_element(self, obj: AppKit.NSObject, obj_class: type = XABase.XAObject, *args: list[Any]) -> 'XABase.XAObject':
        element = super()._new_element(obj, obj_class, *args)
        predicate = XABase.XAPredicate()
        predicate.add_eq_condition("id", obj.localIdentifier())
        ls = predicate.evaluate(self.xa_scel)
        element.xa_scel = ls[0]
        return element

    def properties(self) -> list[dict]:
        """Gets the properties of each media item in the list.

        :return: A list of media item properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_scel.arrayByApplyingSelector_("properties"))

    def keywords(self) -> list[list[str]]:
        """Gets the keywords of each media item in the list.

        :return: A list of media item keywords
        :rtype: list[list[str]]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_scel.arrayByApplyingSelector_("keywords")
        return [keyword for keywordlist in ls for keyword in keywordlist]

    def duration(self) -> list[float]:
        """Gets the duration of each media item in the list.

        :return: A list of media item durations
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        return [x.duration() for x in self.xa_elem]

    def title(self) -> list[str]:
        """Gets the title of each media item in the list.

        :return: A list of media item titles
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def file_path(self) -> list[XABase.XAPath]:
        """Gets the file path of each media item in the list.

        :return: A list of media item original file paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("mainFileURL")
        return [XABase.XAPath(x) for x in ls]

    def object_description(self) -> list[str]:
        """Gets the object description of each media item in the list.

        :return: A list of media item descriptions
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_scel.arrayByApplyingSelector_("objectDescription"))

    def favorite(self) -> list[bool]:
        """Gets the favorited status of each media item in the list.

        :return: A list of media item favorited status boolean values
        :rtype: list[bool]
        
        .. versionadded:: 0.0.6
        """
        return [x.isFavorite() for x in self.xa_elem]

    def creation_date(self) -> list[datetime]:
        """Gets the creation date of each media item in the list.

        :return: A list of media item creation dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate"))

    def modification_date(self) -> list[datetime]:
        """Gets the last modification date of each media item in the list.

        :return: A list of media item modification dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate"))

    def is_burst(self) -> list[bool]:
        """Gets the is burst status of each media item in the list.

        :return: A list of media item is burst status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return [x.representsBurst() for x in self.xa_elem]

    def is_video(self) -> list[bool]:
        """Gets the is video status of each media item in the list.

        :return: A list of media item is video status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return [x.isVideo() for x in self.xa_elem]

    def is_hidden(self) -> list[bool]:
        """Gets the is hidden status of each media item in the list.

        :return: A list of media item is hidden status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return [x.isHidden() for x in self.xa_elem]

    def is_photo(self) -> list[bool]:
        """Gets the is photo status of each media item in the list.

        :return: A list of media item is photo status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.1.0
        """
        return [x.isPhoto() for x in self.xa_elem]

    def id(self) -> list[str]:
        """Gets the ID of each media item in the list.

        :return: A list of media item IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("localIdentifier"))

    def height(self) -> list[int]:
        """Gets the height of each media item in the list.

        :return: A list of media item heights
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return [x.pixelHeight() for x in self.xa_elem]

    def width(self) -> list[int]:
        """Gets the width of each media item in the list.

        :return: A list of media item widths
        :rtype: list[int]
        
        .. versionadded:: 0.0.6
        """
        return [x.pixelWidth() for x in self.xa_elem]

    def filename(self) -> list[str]:
        """Gets the filename of each media item in the list.

        :return: A list of media item filenames
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("filename"))

    def altitude(self) -> list[float]:
        """Gets the altitude of each media item in the list.

        :return: A list of media item altitudes
        :rtype: list[float]
        
        .. versionadded:: 0.0.6
        """
        locations = self.xa_elem.arrayByApplyingSelector_("location")
        return [x.altitude() for x in locations]

    def size(self) -> list[tuple[float, float]]:
        """Gets the file size, in bytes, of each media item in the list.

        :return: A list of media item file sizes
        :rtype: list[tuple[float, float]]
        
        .. versionadded:: 0.0.6
        """
        paths = self.file_path()
        file_manager = AppKit.NSFileManager.defaultManager()
        attributes = [file_manager.attributesOfItemAtPath_error_(x.path, None) for x in paths]
        return [x[0][AppKit.NSFileSize] for x in attributes if x is not None and x[0] is not None]

    def location(self) -> list[list[Union[float, None]]]:
        """Gets the location of each media item in the list.

        :return: A list of media item locations
        :rtype: list[list[Union[float, None]]]
        
        .. versionadded:: 0.0.6
        """
        ls = self.xa_elem.arrayByApplyingSelector_("location")
        return [XABase.XALocation(
            latitude = x.coordinate()[0],
            longitude = x.coordinate()[1],
            altitude = x.altitude(),
            radius = x.horizontalAccuracy()
        ) for x in ls]

    def by_properties(self, properties: dict) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose properties matches the given properties dictionary, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        predicate = XABase.XAPredicate()
        predicate.add_eq_condition("properties", properties)
        ls = predicate.evaluate(self.xa_scel).get()
        obj = ls[0]
        return self._new_element(obj, self.xa_ocls)

    def by_keywords(self, keywords: list[str]) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose keywords list matches the given keywords, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("keywords", keywords)

    def by_title(self, title: str) -> Union['XAPhotosMediaItem', None]:
        """Retrieves the media item whose title matches the given title string, if one exists.

        :return: The desired media item, if it is found
        :rtype: Union[XAPhotosMediaItem, None]
        
        .. versionadded:: 0.0.6
        """
        return self.by_property("title", title)

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

    def get_clipboard_representation(self) -> list[NSURL]:
        """Gets a clipboard-codable representation of each media item in the list.

        When the clipboard content is set to a list of media items, each item's file URL is added to the clipboard.

        :return: A list of media item file URLs
        :rtype: list[NSURL]

        .. versionadded:: 0.0.8
        """
        return [x._get_url() for x in self]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XAPhotosMediaItem(XABase.XAObject, XAClipboardCodable, XAImageLike):
    """A photo or video in Photos.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.properties: dict #: All properties of the media item
        self.keywords: list[str] #: A list of keywords to associate with a media item
        self.name: str #: The name (title) of the media item.
        self.object_description: str #: A description of the media item.
        self.favorite: bool #: Whether the media item has been favorited.
        self.creation_date: datetime #: The creation date of the media item
        self.modification_date: datetime #: The last modification date of the media item
        self.id: str #: The unique ID of the media item
        self.height: int #: The height of the media item in pixels.
        self.width: int #: The width of the media item in pixels.
        self.filename: str #: The name of the file on disk.
        self.altitude: float #: The GPS altitude in meters.
        self.size: int #: The selected media item file size.
        self.location: XABase.XALocation #: The GPS latitude and longitude, in an ordered list of 2 numbers or missing values. Latitude in range -90.0 to 90.0, longitude in range -180.0 to 180.0.
        self.duration: float #: The duration of the media item
        self.is_video: bool #: Whether the media item is a video
        self.is_photo: bool #: Whether the media item is a photo
        self.is_burst: bool #: Whether the media item is a burst photo
        self.file_path: XABase.XAPath #: The path to the main file for the media item
        self.is_hidden: bool #: Whether the media item is hidden

        self.__photos_library = Photos.PHPhotoLibrary.sharedPhotoLibrary()
        self.__image_manager = Photos.PHCachingImageManager.defaultManager()
        self.__metadata_storage = []

        fetch_options = Photos.PHFetchOptions.alloc().init()
        all_photos = Photos.PHAsset.fetchAssetsWithOptions_(fetch_options)

    def __get_metadata(self, force: bool = True):
        if self.__metadata_storage != [] and force is False:
            return

        def result_handler(img_data, img_uti, img_orientation, img_info):
            source = Quartz.CGImageSourceCreateWithData(img_data, {Quartz.kCGImageSourceShouldCache: True})
            metadata = Quartz.CGImageSourceCopyPropertiesAtIndex(source, 0, {Quartz.kCGImageSourceShouldCache: True})
            if metadata is not None:
                self.__metadata_storage.append(metadata)

        options = Photos.PHImageRequestOptions.alloc().init()
        options.setSynchronous_(True)
        options.setDeliveryMode_(Photos.PHImageRequestOptionsDeliveryModeHighQualityFormat)

        self.__image_manager.requestImageDataAndOrientationForAsset_options_resultHandler_(self.xa_elem, options, result_handler)

    @property
    def properties(self) -> dict:
        return self.xa_scel.properties()

    @property
    def keywords(self) -> list[str]:
        self.xa_scel = self.xa_scel.get()
        return list(self.xa_scel.keywords())

    @keywords.setter
    def keywords(self, keywords: list[str]):
        self.set_scriptable_property('keywords', keywords)

    @property
    def name(self) -> str:
        return self.xa_elem.title()

    @name.setter
    def name(self, name: str):
        self.set_scriptable_property("name", name)

    @property
    def object_description(self) -> str:
        return self.xa_scel.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_scriptable_property('objectDescription', object_description)

    @property
    def favorite(self) -> bool:
        return self.xa_elem.favorite()

    @favorite.setter
    def favorite(self, favorite: bool):
        self.set_property('favorite', favorite)

    @property
    def creation_date(self) -> datetime:
        return self.xa_elem.creationDate()

    @creation_date.setter
    def creation_date(self, creation_date: datetime):
        self.set_scriptable_property('date', creation_date)

    @property
    def modification_date(self) -> datetime:
        return self.xa_elem.modificationDate()

    @property
    def is_photo(self) -> bool:
        return self.xa_elem.isPhoto()

    @property
    def duration(self) -> float:
        return self.xa_elem.duration()

    @property
    def file_path(self) -> XABase.XAPath:
        return XABase.XAPath(self.xa_elem.mainFileURL())

    @property
    def is_video(self) -> bool:
        return self.xa_elem.isVideo()

    @property
    def is_hidden(self) -> bool:
        return self.xa_elem.isHidden()

    @property
    def is_burst(self) -> bool:
        return self.xa_elem.representsBurst()

    @property
    def id(self) -> str:
        return self.xa_elem.localIdentifier()

    @property
    def height(self) -> int:
        return self.xa_elem.pixelHeight()

    @property
    def width(self) -> int:
        return self.xa_elem.pixelWidth()

    @property
    def filename(self) -> str:
        return self.xa_elem.filename()

    @property
    def altitude(self) -> float:
        return self.xa_scel.altitude()

    @property
    def size(self) -> int:
        return self.xa_scel.size()

    @property
    def location(self) -> XABase.XALocation:
        loc = self.xa_elem.location()
        return XABase.XALocation(
            latitude = loc.coordinate()[0],
            longitude = loc.coordinate()[1],
            altitude = loc.altitude(),
            radius = loc.horizontalAccuracy()
        )

    @location.setter
    def location(self, location: Union[XABase.XALocation, list[float]]):
        if isinstance(location, list):
            self.set_property('location', location)
        else:
            self.set_property('location', [location.latitude, location.longitude])

    def spotlight(self) -> 'XAPhotosMediaItem':
        """Shows the media item in the front window of Photos.app.

        :return: The media item object
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.6
        """
        self.xa_scel.spotlight()
        return self

    def duplicate(self) -> 'XAPhotosMediaItem':
        """Duplicates the media item.

        :return: The newly created media item object
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.2
        """
        return self.xa_scel.duplicate()

    def show_in_preview(self):
        """Opens the media item in Preview.app.

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.openURL_(self.file_path.xa_elem)

    def reveal_in_finder(self):
        """Opens a Finder window or tab focused on the media item's containing folder with the media item selected.

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.activateFileViewerSelectingURLs_([self.file_path.xa_elem])

    def get_clipboard_representation(self) -> NSURL:
        """Gets a clipboard-codable representation of the media item.

        When the clipboard content is set to a media item, the item's file URL is added to the clipboard.

        :return: The media item's file URL
        :rtype: NSURL

        .. versionadded:: 0.0.8
        """
        return self.file_path.xa_elem

    def get_image_representation(self) -> XABase.XAPath:
        """Gets a representation of the object that can be used to initialize an :class:`~PyXA.XABase.XAImage` object.

        :return: The XAImage-compatible form of this object
        :rtype: XABase.XAPath
        """
        return self.file_path

    def __repr__(self):
        if self.name is None:
            return "<" + str(type(self)) + "id=" + self.id + ">"
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"




class XAPhotosContainerList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    All properties of containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAPhotosContainer
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        """Gets the properties of each container in the list.

        :return: A list of container properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def id(self) -> list[str]:
        """Gets the ID of each container in the list.

        :return: A list of container IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.6
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        """Gets the name of each container in the list.

        :return: A list of container names
        :rtype: list[str]
        
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

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of each container in the list.

        When the clipboard content is set to a list of containers, each containers's name is added to the clipboard.

        :return: The container's name
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAPhotosContainer(XABase.XAObject, XAClipboardCodable):
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

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

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

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the container.

        When the clipboard content is set to a container, the containers's name is added to the clipboard.

        :return: The container's name
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + self.id + ">"




class XAPhotosAlbumList(XAPhotosContainerList):
    """A wrapper around lists of albums that employs fast enumeration techniques.

    All properties of albums can be called as methods on the wrapped list, returning a list containing each album's value for the property.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAPhotosAlbum)

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
        super().__init__(properties, filter, XAPhotosFolder)

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