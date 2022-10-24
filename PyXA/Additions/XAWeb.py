""".. versionadded:: 0.1.0

Internet-related automation features that extend PyXA scripting functionality.
"""


from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Union
import requests

import AppKit

from .. import XABase

class RSSFeed(XABase.XAObject):
    """An RSS feed reader.

    .. versionadded:: 0.1.0
    """
    def __init__(self, url: Union[str, XABase.XAURL]):
        self.xa_apsp = AppKit.NSApplication.sharedApplication()
        self.xa_wksp = AppKit.NSWorkspace.sharedWorkspace()
        self.xa_aref = None
        self.xa_sevt = None

        if isinstance(url, XABase.XAURL):
            url = url.url
        self.url = url
        request = requests.get(url)
        self.__soup = BeautifulSoup(request.content, features='xml')

    def items(self) -> 'RSSItemList':
        """Retrieves all item and/or entry tags in the RSS feed as :class:`RSSItem` objects.

        :return: The list of items and/or entries
        :rtype: RSSItemList

        :Example:

        >>> import PyXA
        >>> reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
        >>> print(reader.items())
        <<class 'PyXA.extensions.XAWeb.RSSItemList'>['Hold Me Closer - Elton John & Britney Spears', 'Only Ever Wanted - Timcast', "I Ain't Worried - OneRepublic", 'wait in the truck - HARDY & Lainey Wilson', 'Bring Me to Life - Evanescence', 'Running Up That Hill (A Deal with God) - Kate Bush', 'Beer With My Friends - Kenny Chesney & Old Dominion', 'American Pie (Full Length Version) - Don Mclean', 'She Had Me At Heads Carolina - Cole Swindell', 'You Proof - Morgan Wallen']>

        .. versionadded:: 0.1.0
        """
        articles = self.__soup.findAll('entry')
        if articles == []:
            articles = self.__soup.findAll('item')
        
        return self._new_element(articles, RSSItemList)

    def refetch(self):
        """Resends the GET request for the RSS feed URL and updates this object's data accordingly.

        :Example: Get the top 10 songs on iTunes every hour

        >>> import PyXA
        >>> from time import sleep
        >>> reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
        >>> while True:
        >>>     reader.refetch()
        >>>     print(reader.items())
        >>>     sleep(3600)

        .. versionadded:: 0.1.0
        """
        request = requests.get(self.url)
        self.__soup = BeautifulSoup(request.content, features='xml')




class RSSItemList(XABase.XAList):
    def __init__(self, properties):
        super().__init__(properties, RSSItem)

    def xml(self) -> List[str]:
        """Gets the raw XML of each item in the list.

        :return: The list of XML strings
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [str(x) for x in self.xa_elem]

    def content(self) -> 'RSSItemContentList':
        """Gets the content of each item as :class:`RSSItemContent` objects.

        :return: The list of item contents
        :rtype: RSSItemContentList

        .. versionadded:: 0.1.0
        """
        contents = []
        for item in self.xa_elem:
            html = str(item.find("content").string)
            content_object = BeautifulSoup(html, 'html.parser')
            contents.append(content_object)
        return self._new_element(contents, RSSItemContentList)

    def title(self) -> List[str]:
        """Gets the title of each item in the list.

        :return: The list of RSS item titles
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("title").text for x in self.xa_elem]

    def author(self) -> List[str]:
        """Gets the author of each item in the list.

        :return: The list of RSS item authors
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("author").text for x in self.xa_elem]

    def category(self) -> List[str]:
        """Gets the category of each item in the list.

        :return: The list of RSS item categories
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("category").text for x in self.xa_elem]

    def comments(self) -> List[str]:
        """Gets the comments of each item in the list.

        :return: The list of RSS item comments
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("comments").text for x in self.xa_elem]

    def description(self) -> 'RSSItemContentList':
        """Gets the description of each item as :class:`RSSItemContent` objects.

        :return: The list of item descriptions
        :rtype: RSSItemContentList

        .. versionadded:: 0.1.0
        """
        contents = []
        for item in self.xa_elem:
            html = str(item.find("description").string)
            content_object = BeautifulSoup(html, 'html.parser')
            contents.append(content_object)
        return self._new_element(contents, RSSItemContentList)

    def enclosure(self) -> List[str]:
        """Gets the enclosure of each item in the list.

        :return: The list of RSS item enclosures
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("enclosure").text for x in self.xa_elem]

    def link(self) -> List[str]:
        """Gets the link of each item in the list.

        :return: The list of RSS item links
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [XABase.XAURL(x.find("link").text) for x in self.xa_elem]

    def publication_date(self) -> List[datetime]:
        """Gets the publication date of each item in the list.

        :return: The list of RSS item publication dates
        :rtype: List[datetime]

        .. versionadded:: 0.1.0
        """
        return [x.find("pubDate").text for x in self.xa_elem]

    def source(self) -> List[str]:
        """Gets the source of each item in the list.

        :return: The list of RSS item sources
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("source").text for x in self.xa_elem]

    def copyright(self) -> List[str]:
        """Gets the copyright of each item in the list.

        :return: The list of RSS item copyrights
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.find("copyright").text for x in self.xa_elem]

    def text(self) -> List[str]:
        """Gets the text of each item in the list.

        :return: The list of RSS item texts
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.text for x in self.xa_elem]

    def links(self) -> List[XABase.XAURL]:
        """Gets the links contained in each item of the list as :class:`XABase.XAURL` objects.

        :return: The list of links
        :rtype: List[XABase.XAURL]

        .. versionadded:: 0.1.0
        """
        return [x for y in self for x in y.links()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class RSSItem(XABase.XAObject):
    """An item or entry in an RSS feed.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)
        
        self.xml: str #: The raw XML of the entry
        self.content: str #: The raw content of the entry
        self.author: str #: The author of the entry
        self.category: str #: The category of the entry
        self.comments: str #: The comments of the entry
        self.description: str #: The description of the entry
        self.enclosure: str #: The media idea enclosed in the entry
        self.link: str #: The hyperlink to the entry
        self.publication_date: datetime #: The most recent publication date of the entry
        self.source: str #: The third-party source of the entry
        self.title: str #: The title of the RSS entry
        self.copyright: str #: The copyright text of the entry
        self.text: str #: All text within the entry (not just the description/content text!)

    @property
    def xml(self) -> str:
        return str(self.xa_elem)

    @property
    def content(self) -> type:
        html = str(self.xa_elem.find("content").string)
        content_object = BeautifulSoup(html, 'html.parser')
        return self._new_element(content_object, RSSItemContent)

    @property
    def author(self) -> str:
        tag = self.xa_elem.find("author")
        if tag is not None:
            return tag.text

    @property
    def category(self) -> str:
        tag = self.xa_elem.find("category")
        if tag is not None:
            return tag.get("label")

    @property
    def comments(self) -> str:
        tag = self.xa_elem.find("comments")
        if tag is not None:
            return tag.text

    @property
    def description(self) -> str:
        tag = self.xa_elem.find("description")
        if tag is not None:
            return tag.string

    @property
    def enclosure(self) -> str:
        return self.xa_elem.find("enclosure").get("url")

    @property
    def link(self) -> Union[str, None]:
        tag = self.xa_elem.find("link")
        if tag is not None:
            return tag.text

    @property
    def publication_date(self) -> Union[str, None]:
        tag = self.xa_elem.find("pubDate")
        if tag is not None:
            return tag.text

    @property
    def source(self) -> str:
        tag = self.xa_elem.find("source")
        if tag is not None:
            return tag.text

    @property
    def title(self) -> str:
        tag = self.xa_elem.find("title")
        if tag is not None:
            return tag.text

    @property
    def copyright(self) -> str:
        tag = self.xa_elem.find("copyright")
        if tag is None:
            tag = self.xa_elem.find("rights")
        if tag is not None:
            return tag.text

    @property
    def text(self) -> str:
        return self.xa_elem.text()

    def links(self) -> List[XABase.XAURL]:
        """Retrieves the URL referenced by each link tag as a list of :class:`XABase.XAURL` objects.

        :return: The list of link URLs
        :rtype: List[XABase.XAURL]

        :Example:

        >>> import PyXA
        >>> reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
        >>> item = reader.items()[0]
        >>> print(item.links())
        [<<class 'PyXA.XABase.XAURL'>https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview122/v4/7a/24/60/7a246091-cef8-1df4-1435-a107ed3c6980/mzaf_8623157179635634843.plus.aac.p.m4a>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/album/hold-me-closer-single/1641082201?uo=2>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/album/hold-me-closer/1641082201?i=1641082205&uo=2>]

        .. versionadded:: 0.1.0
        """
        tags = self.xa_elem.findAll("link")
        return [XABase.XAURL(x.get("href")) for x in set(tags)]

    def __repr__(self):
        return "<" + str(type(self)) + self.title + ">"




class RSSItemContentList(XABase.XAList):
    def __init__(self, properties):
        super().__init__(properties, RSSItemContent)

    def html(self) -> List[str]:
        """Gets the raw HTML of each item in the list.

        :return: The list of HTML strings
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [str(x) for x in self.xa_elem]

    def text(self) -> List[str]:
        """Gets the text of each item in the list.

        :return: The list of content texts
        :rtype: List[str]

        .. versionadded:: 0.1.0
        """
        return [x.text for x in self.xa_elem]

    def links(self) -> List[XABase.XAURL]:
        """Gets the links contained in each item of the list as :class:`XABase.XAURL` objects.

        :return: The list of links
        :rtype: List[XABase.XAURL]

        .. versionadded:: 0.1.0
        """
        return [x for y in self for x in y.links()]

    def images(self) -> List[XABase.XAImage]:
        """Gets the images contained in each item of the list as :class:`XABase.XAImage` objects.

        :return: The list of links
        :rtype: List[XABase.XAImage]

        .. versionadded:: 0.1.0
        """
        img_objects = []
        for content_item in self.xa_elem:
            imgs = content_item.findAll("img")
            img_objects.extend([AppKit.NSImage.alloc().initWithContentsOfURL_(AppKit.NSURL.alloc().initWithString_(x.get("src"))) for x in imgs])
        return self._new_element(img_objects, XABase.XAImageList)

    def __repr__(self):
        return "<" + str(type(self)) + "Length: " + str(len(self)) + ">"

class RSSItemContent(XABase.XAObject):
    """The content of an RSS entry.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.html: str #: The raw html of the content
        self.text: str #: The visible text of the content

    @property
    def html(self) -> str:
        return str(self.xa_elem)

    @property
    def text(self) -> str:
        return self.xa_elem.text

    def links(self) -> List[XABase.XAURL]:
        """Retrieves the URL referenced by each anchor element as a list of :class:`XABase.XAURL` objects.

        :return: The list of link URLs
        :rtype: List[XABase.XAURL]

        :Example:

        >>> import PyXA
        >>> reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
        >>> content = reader.items()[0].content
        >>> print(content.links())
        [<<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/album/hold-me-closer/1641082201?i=1641082205&uo=2>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/album/hold-me-closer/1641082201?i=1641082205&uo=2>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/album/hold-me-closer-single/1641082201?uo=2>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/artist/elton-john/54657?uo=2>, <<class 'PyXA.XABase.XAURL'>https://music.apple.com/us/genre/music-pop/id14?uo=2>]

        .. versionadded:: 0.1.0
        """
        links = self.xa_elem.findAll("a")
        return [XABase.XAURL(link.get("href")) for link in links]

    def images(self) -> List[XABase.XAImage]:
        """Retrieves the image referenced by each image element as a list of :class:`XABase.XAImage` objects.

        :return: The list of images
        :rtype: List[XABase.XAImage]

        :Example:

        >>> import PyXA
        >>> reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
        >>> content = reader.items()[0].content
        >>> print(content.images())
        [<PyXA.XABase.XAImage object at 0x10635ee80>, <PyXA.XABase.XAImage object at 0x10635ebb0>]

        .. versionadded:: 0.1.0
        """
        imgs = self.xa_elem.findAll("img")
        img_objects = [AppKit.NSImage.alloc().initWithContentsOfURL_(AppKit.NSURL.alloc().initWithString_(x.get("src"))) for x in imgs]
        return self._new_element(img_objects, XABase.XAImageList)