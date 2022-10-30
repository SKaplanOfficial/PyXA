""".. versionadded:: 0.0.1

Control the macOS TV application using JXA-like syntax.
"""

from typing import Union

from PyXA import XABase, XABaseScriptable

from . import MediaApplicationBase


class XATVApplication(MediaApplicationBase.XAMediaApplication, XABaseScriptable.XASBApplication):
    """A class for managing and interacting with TV.app.

    .. seealso:: :class:`XATVWindow`, class:`XATVSource`, :class:`XATVPlaylist`, :class:`XATVTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATVWindow




class XATVTrackList(MediaApplicationBase.XAMediaItemList):
    """A wrapper around lists of TV tracks that employs fast enumeration techniques.

    All properties of TV tracks can be called as methods on the wrapped list, returning a list containing each track's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XATVTrack
        super().__init__(properties, filter, obj_class)

    def sort_director(self) -> list[str]:
        """Gets the director sort string of each track in the list.

        :return: A list of track director sort strings
        :rtype: list[str]
        
        .. versionadded:: 0.0.7
        """
        return list(self.xa_elem.arrayByApplyingSelector_("sortDirector"))

    def by_sort_director(self, sort_director: str) -> Union['XATVTrack', None]:
        """Retrieves the first track whose director sort string matches the given string, if one exists.

        :return: The desired track, if it is found
        :rtype: Union[XATVTrack, None]
        
        .. versionadded:: 0.0.7
        """
        return self.by_property("sortDirector", sort_director)

class XATVTrack(MediaApplicationBase.XAMediaItem):
    """A class for managing and interacting with tracks in TV.app.

    .. seealso:: :class:`XATVSharedTrack`, :class:`XATVFileTrack`, :class:`XATVRemoteURLTrack`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.sort_director: str #: The string used for this track when sorting by director

    @property
    def sort_director(self) -> str:
        return self.xa_elem.sortDirector()

    @sort_director.setter
    def sort_director(self, sort_director: str):
        self.set_property('sortDirector', sort_director)




class XATVWindow(MediaApplicationBase.XAMediaWindow, XABaseScriptable.XASBWindow):
    """A windows of TV.app.

    .. seealso:: :class:`XATVBrowserWindow`, :class:`XATVPlaylistWindow`, :class:`XATVVideoWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

        obj_class = self.xa_elem.objectClass().data()
        if not hasattr(self, "xa_specialized"):
            if obj_class == b'WrBc':
                self.__class__ = MediaApplicationBase.XAMediaBrowserWindow
            elif obj_class == b'WlPc':
                self.__class__ = MediaApplicationBase.XAMediaPlaylistWindow
            elif obj_class == b'niwc':
                self.__class__ = MediaApplicationBase.XAMediaVideoWindow
            self.xa_specialized = True
            self.__init__(properties)
