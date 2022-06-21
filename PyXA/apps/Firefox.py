""".. versionadded:: 0.0.3

Control Firefox using JXA-like syntax.
"""

from typing import Union
from AppKit import NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

class XAFirefoxApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Firefox.app.

    .. seealso:: :class:`XAFirefoxWindow`, :class:`XAFirefoxDocument`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFirefoxWindow

        self.frontmost: bool = self.xa_scel.frontmost() #: Whether Firefox is the active application
        self.name: str = self.xa_scel.name() #: The name of the Firefox application
        self.version: str = self.xa_scel.version() #: The currently installed version of Firefox 

    def open(self, url: Union[str, NSURL] = "https://google.com") -> 'XAFirefoxApplication':
        """Opens a URL in a new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Safari application object.
        :rtype: XAFirefoxApplication

        :Example:

           >>> import PyXA
           >>> app = PyXA.application("Firefox")
           >>> app.open("https://www.google.com")
           >>> app.open("google.com")
           >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.3
        """
        if isinstance(url, str):
            if url.startswith("/"):
                # URL is a path to file
                self.xa_wksp.openFile_application_(url, self.xa_scel)
                return self
            # Otherwise, URL is web address
            elif not url.startswith("http"):
                url = "http://" + url
            url = XABase.xa_url(url)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self

class XAFirefoxWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAHasElements):
    """A class for managing and interacting with windows in Firefox.app.

    .. seealso:: :class:`XAFirefoxApplication`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.__document = None
        
    @property
    def document(self) -> 'XAFirefoxDocument':
        if self.__document is None:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": self.xa_scel.document(),
                "scriptable_element": self.xa_scel.document(),
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            self.__document = XAFirefoxDocument(properties)
        return self.__document

class XAFirefoxDocument(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with documents in Firefox.app.

    .. seealso:: :class:`XAFirefoxWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.properties: dict = self.xa_elem.properties()
        self.modified: bool = self.properties["modified"]
        self.name: str = self.properties["name"]
        self.path: str = self.properties["path"]