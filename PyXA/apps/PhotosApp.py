""".. versionadded:: 0.0.2

Control the macOS Photos application using JXA-like syntax.

.. todo::

   - Add support for folders and containers
   - Add image operations such as rotate, flip
   - Add ability to add new albums
   - Add ability to move photos to albums/folders
"""
from datetime import datetime
from time import sleep
from typing import List, Union
import threading

import Photos
from AppKit import NSPredicate, NSImage, NSURL
from Foundation import NSSortDescriptor

from PyXA import XAEvents

from PyXA import XABase
from PyXA import XABaseScriptable

class XAPhotosApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Photos.app.

    .. seealso:: :class:`XATextEditWindow`, :class:`XAPhotosMediaItem`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_plib = Photos.PHPhotoLibrary.alloc().initSharedLibrary()

    # Albums
    def __new_album(self, album_obj: Photos.PHAssetCollection) -> 'XAPhotosAlbum':
        """Wrapper for creating a new XAPhotosAlbum object.

        :param album_obj: The PHAssetCollection object to wrap.
        :type album_obj: Photos.PHAssetCollection
        :return: A reference to a PyXA photo asset object.
        :rtype: XAPhotosAlbum

        .. versionadded:: 0.0.2
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": album_obj.localIdentifier()}))
        scriptable_albums = self.xa_scel.albums()
        scriptable_album = scriptable_albums.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": album_obj,
            "scriptable_element": scriptable_album,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "photo_library": self.xa_plib,
        }
        return XAPhotosAlbum(properties)

    def albums(self, filter: dict = None) -> List['XAPhotosAlbum']:
        """Returns a list of albums, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned albums will have
        :type filter: dict
        :return: The list of albums
        :rtype: List[XAPhotosAlbum]

        :Example 1: Listing all albums

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.albums())
        [<<class 'PyXA.apps.PhotosApp.XAPhotosAlbum'>Example Album, id=7E62F87B-90C4-4B83-9383-E6F2917C11B3/L0/040>, <<class 'PyXA.apps.PhotosApp.XAPhotosAlbum'>Another Album, id=BA978E66-36E3-42B2-9F09-2484B4CFFC1E/L0/040>, ...]

        :Example 2: Listing albums after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.albums({"title": "Example Album"}))
        [<<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=54ECE9C9-12AD-4985-82F1-265D5A47F325/L0/001>]

        .. versionadded:: 0.0.2
        """
        fetchOptions = Photos.PHFetchOptions.alloc().init()

        # Apply Filter
        if filter is not None:
            if "id" in filter:
                filter["localIdentifier"] = filter["id"]
                filter.pop("id")
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            fetchOptions.setPredicate_(predicate)

        albums = Photos.PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(Photos.PHAssetCollectionTypeAlbum, Photos.PHAssetCollectionSubtypeAny, fetchOptions)
        return [self.__new_album(albums.objectAtIndex_(i)) for i in range(0, albums.count())]

    def album(self, filter: Union[int, dict]) -> 'XAPhotosAlbum':
        """Returns the first album matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned album will have
        :type filter: Union[int, dict]
        :return: The media item
        :rtype: XAPhotosAlbum

        :Example 1: Getting an album by index

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.album(2))
        <<class 'PyXA.apps.PhotosApp.XAPhotosAlbum'>Snapchat, id=0CB8EA43-A0BB-4D14-A71A-212A890A64D2/L0/040>

        :Example 2: Getting an album by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.album({"title": "PyXA Photos"}))
        <<class 'PyXA.apps.PhotosApp.XAPhotosAlbum'>Summer Camp 2018, id=7E62F87B-90C4-4B83-9383-E6F2917C11B3/L0/040>

        .. versionadded:: 0.0.2
        """
        fetchOptions = Photos.PHFetchOptions.alloc().init()

        if isinstance(filter, int):
            albums = Photos.PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(Photos.PHAssetCollectionTypeAlbum, Photos.PHAssetCollectionSubtypeAny, fetchOptions)
            return self.__new_album(albums.objectAtIndex_(filter))

        if "id" in filter:
            filter["localIdentifier"] = filter["id"]
            filter.pop("id")

        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
        fetchOptions.setPredicate_(predicate)
        albums = Photos.PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(Photos.PHAssetCollectionTypeAlbum, Photos.PHAssetCollectionSubtypeAny, fetchOptions)
        return self.__new_album(albums.objectAtIndex_(0))

    def first_album(self) -> 'XAPhotosAlbum':
        """Returns the album at the zero index of the media albums array.

        :return: The first album
        :rtype: XAPhotosAlbum

        .. versionadded:: 0.0.2
        """
        fetchOptions = Photos.PHFetchOptions.alloc().init()
        albums = Photos.PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(Photos.PHAssetCollectionTypeAlbum, Photos.PHAssetCollectionSubtypeAny, fetchOptions)
        return self.__new_album(albums.firstObject())

    def last_album(self) -> 'XAPhotosAlbum':
        """Returns the album at the last (-1) index of the media albums array.

        :return: The last album
        :rtype: XAPhotosAlbum

        .. versionadded:: 0.0.2
        """
        fetchOptions = Photos.PHFetchOptions.alloc().init()
        albums = Photos.PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(Photos.PHAssetCollectionTypeAlbum, Photos.PHAssetCollectionSubtypeAny, fetchOptions)
        return self.__new_album(albums.lastObject())

    # Media Items
    def __new_media_item(self, photo_obj: Photos.PHAsset, elements: List['XAPhotosMediaItem'] = None) -> Union['XAPhotosMediaItem', None]:
        """Wrapper for creating a new XAPhoto object.

        :param photo_obj: The PHAsset object to wrap.
        :type photo_obj: Photos.PHAsset
        :param elements: A list to directly store the created XAPhoto element into, instead of returning it.
        :type elements: List[XAPhoto]
        :return: A reference to a PyXA photo asset object.
        :rtype: Union[XAPhoto, None]

        .. versionadded:: 0.0.2
        """
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": photo_obj.localIdentifier()}))
        scriptable_photos = self.xa_scel.mediaItems()
        scriptable_photo = scriptable_photos.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": photo_obj,
            "scriptable_element": scriptable_photo,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "photo_library": self.xa_plib,
        }
        if elements is None:
            return XAPhotosMediaItem(properties)
        elements.append(XAPhotosMediaItem(properties))

    def media_items(self, filter: dict = None) -> List['XAPhotosMediaItem']:
        """Returns a list of media items, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned media items will have
        :type filter: dict
        :return: The list of media items
        :rtype: List[XAPhotosMediaItem]

        :Example 1: Listing all media items

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.media_items())
        [<<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=09B91497-7528-43B0-9143-37BB84724201/L0/001>, <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=4F311B01-20A5-4413-97B5-43F7B7854981/L0/001>, ...]

        :Example 2: Listing media items after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.media_items({"favorite": True}))
        [<<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=54ECE9C9-12AD-4985-82F1-265D5A47F325/L0/001>, <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=1F41A2F0-E77C-46F4-AE57-245E2D7846E0/L0/001>, ...]

        .. versionadded:: 0.0.2
        """
        # Set up request to get all photos
        allPhotosOptions = Photos.PHFetchOptions.alloc().init()
        allPhotosOptions.setSortDescriptors_([NSSortDescriptor.alloc().initWithKey_ascending_("creationDate", True)])

        # Apply Filter
        if filter is not None:
            if "id" in filter:
                filter["localIdentifier"] = filter["id"]
                filter.pop("id")
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            allPhotosOptions.setPredicate_(predicate)

        # Execute request
        photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
        
        # Spawn threads to create PyXA objects
        elements = []
        for i in range(0, photos.count()):
            lookup_thread = threading.Thread(target=self.__new_media_item, args=(photos.objectAtIndex_(i), elements), name="Lookup Scriptable Photo", daemon=True)
            lookup_thread.start()

        # Return elements once all threads are complete
        while len(elements) != photos.count():
            sleep(0.1)
        return elements

    def media_item(self, filter: Union[int, dict]) -> 'XAPhotosMediaItem':
        """Returns the first media item matching the given filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned media item will have
        :type filter: Union[int, dict]
        :return: The media item
        :rtype: XAPhotosMediaItem

        :Example 1: Getting a media item by index

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.media_item(7))
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=99301EE7-9FC0-4535-9987-382CF4E028EB/L0/001>

        :Example 2: Getting a media item by using a filter

        >>> import PyXA
        >>> app = PyXA.application("Photos")
        >>> print(app.media_item({"id": "1F41A2F0-E77C-46F4-AE57-245E2D7846E0/L0/001"}))
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=1F41A2F0-E77C-46F4-AE57-245E2D7846E0/L0/001>

        .. versionadded:: 0.0.2
        """
        if isinstance(filter, int):
            allPhotosOptions = Photos.PHFetchOptions.alloc().init()
            allPhotosOptions.setSortDescriptors_([NSSortDescriptor.alloc().initWithKey_ascending_("creationDate", True)])
            photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
            return self.__new_media_item(photos.objectAtIndex_(filter))

        if "id" in filter:
            filter["localIdentifier"] = filter["id"]
            filter.pop("id")
        
        allPhotosOptions = Photos.PHFetchOptions.alloc().init()
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
        allPhotosOptions.setPredicate_(predicate)
        photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
        if photos.count() > 0:
            return self.__new_media_item(photos.objectAtIndex_(0))

    def first_media_item(self) -> 'XAPhotosMediaItem':
        """Returns the item at the zero index of the media items array.

        :return: The first media item
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.2
        """
        allPhotosOptions = Photos.PHFetchOptions.alloc().init()
        allPhotosOptions.setSortDescriptors_([NSSortDescriptor.alloc().initWithKey_ascending_("creationDate", True)])
        photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
        return self.__new_media_item(photos.firstObject())

    def last_media_item(self) -> 'XAPhotosMediaItem':
        """Returns the item at the last (-1) index of the media items array.

        :return: The last media item
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.2
        """
        allPhotosOptions = Photos.PHFetchOptions.alloc().init()
        allPhotosOptions.setSortDescriptors_([NSSortDescriptor.alloc().initWithKey_ascending_("creationDate", True)])
        photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
        return self.__new_media_item(photos.lastObject())

class XAPhotosContainer(XABase.XAHasElements):
    """A generic class for managing and interacting with containers (folders and albums) in Photos.app.

    .. seealso:: :class:`XAPhotosApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAPhotosAlbum(XAPhotosContainer):
    """A class for managing and interacting with albums in Photos.app.

    .. seealso:: :class:`XAPhotosApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_plib = properties["photo_library"]

        self.id = self.xa_elem.localIdentifier() #: A unique identifier for this album
        self.title = self.xa_elem.title() #: The title of the album
        self.earliest_date: datetime = self.xa_elem.startDate() #: The earliest date an item in the album was captured
        self.latest_date: datetime = self.xa_elem.endDate() #: The most recent date an item in the album was captured
        self.count: int = self.xa_elem.approximateCount() #: The number of items in the album

        location = self.xa_elem.approximateLocation()
        self.location = None #: A general location encompassing the locations of all items in the album
        if location is not None:
            self.location = XABase.XALocation(
                latitude = location.coordinate()[0],
                longitude = location.coordinate()[1],
                altitude = location.altitude(),
                raw_value = location,
            )

    def __repr__(self):
        return "<" + str(type(self)) + self.title + ", id=" + self.id + ">"

class XAPhotosFolder(XAPhotosContainer):
    """A class for managing and interacting with folders in Photos.app.

    .. seealso:: :class:`XAPhotosApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAPhotosMediaItem(XABase.XAObject):
    """A class for managing and interacting with photos in Photos.app.

    .. seealso:: :class:`XAPhotosApplication`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_plib = properties["photo_library"]

        resources = Photos.PHAssetResource.assetResourcesForAsset_(self.xa_elem)

        self.id: str = self.xa_elem.localIdentifier() #: A unique identifier for this media item
        self.title: str = self.xa_elem.title() #: The title of the media item
        self.description: str = self.xa_elem.descriptionProperties().assetDescription() #: The caption for the media item
        self.favorite: bool = self.xa_elem.isFavorite() #: Whether the media item is favorited or not
        self.creation_date: datetime = self.xa_elem.creationDate() #: The original creation date of the item
        self.modified_date: datetime = self.xa_elem.modificationDate() #: The date the item was last modified
        self.height: int = self.xa_elem.pixelHeight() #: The height of the media item in pixels
        self.width: int = self.xa_elem.pixelWidth() #: The width of the media item in pixels
        self.aspect_ratio: float = self.xa_elem.aspectRatio() #: The aspect ratio of the item
        self.filename: str = self.xa_elem.filename() #: The name of the associated media file
        self.file_path: str = self.xa_elem.mainFileURL().path() #: The path to the associated media file
        self.size: int = resources[0].fileSize() #: The file size of the media item in bytes
        self.__keywords: List[str] = None #: The keywords associated with the media item

        self.kind = None #: The media type of the item (e.g. image or video)
        kind = self.xa_elem.kind()
        if kind == 0:
            self.kind = "image"
        elif kind == 1:
            self.kind = "video"

        location = self.xa_elem.location()
        self.location = None #: The location the media item was captured
        if location is not None:
            self.location = XABase.XALocation(
                latitude = location.coordinate()[0],
                longitude = location.coordinate()[1],
                altitude = location.altitude(),
                raw_value = location,
            )

    @property
    def keywords(self):
        if self.__keywords is None:
            keyword_thread = threading.Thread(target=self.__get_keywords, name="Get Keywords", daemon=True)
            keyword_thread.start()
        while self.__keywords is None:
            # Wait for keywords to be fetched
            sleep(0.1)
        return self.__keywords

    def __get_keywords(self) -> List[str]:
        """Gets the keywords associated with this image.

        This process can take a moment, so it is recommended to run this method in a separate thread.

        :return: The list of keywords
        :rtype: List[str]

        .. versionadded:: 0.0.2
        """
        keywords = self.xa_scel.keywords()
        if keywords is not None and len(keywords) > 0:
            self.__keywords = list(keywords)
        else:
            self.__keywords = []

    def copy(self):
        """Copies the media file and its data to the clipboard.

        .. versionadded:: 0.0.2
        """
        url = NSURL.alloc().initFileURLWithPath_(self.file_path)
        img = NSImage.alloc().initWithContentsOfFile_(self.file_path)
        self.set_clipboard([img, url])

    def duplicate(self) -> 'XAPhotosMediaItem':
        """Duplicates the media item in the Photo Library.

        :return: A reference to the newly created media item.
        :rtype: XAPhotosMediaItem

        .. versionadded:: 0.0.2
        """
        scriptable_dupe_obj = self.xa_scel.duplicate()
        
        allPhotosOptions = Photos.PHFetchOptions.alloc().init()
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"localIdentifier": scriptable_dupe_obj.id()}))
        allPhotosOptions.setPredicate_(predicate)
        photos = Photos.PHAsset.fetchAssetsWithOptions_(allPhotosOptions)
        dupe_obj = photos.firstObject()

        properties = {
            "parent": self.xa_prnt,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": dupe_obj,
            "scriptable_element": scriptable_dupe_obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "photo_library": self.xa_plib,
        }
        return XAPhotosMediaItem(properties)

    def show(self):
        """Shows the media item in Photos.app.

        .. versionadded:: 0.0.2
        """
        self.xa_scel.spotlight()

    def show_in_preview(self):
        """Opens the media item in Preview.

        .. versionadded:: 0.0.2
        """
        url = NSURL.alloc().initFileURLWithPath_(self.file_path)
        self.xa_wksp.openURL_(url)

    def reveal_in_finder(self):
        """Opens a Finder window focused on the media item's containing folder with the media item selected.

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.activateFileViewerSelectingURLs_([self.file_path])

    def __repr__(self):
        if self.title is None:
            return "<" + str(type(self)) + "id=" + self.id + ">"
        return "<" + str(type(self)) + self.title + ", id=" + self.id + ">"