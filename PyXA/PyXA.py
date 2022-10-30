from datetime import datetime
from time import sleep
from typing import Any, Callable, List, Union
import importlib

import AppKit
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

from .XABase import *
from PyXA import XABaseScriptable
from .apps import application_classes

from .XAErrors import ApplicationNotFoundError

VERSION = "0.1.0" #: The installed version of PyXA

supported_applications: List[str] = list(application_classes.keys()) #: A list of names of supported scriptable applications

class XAApplicationList(XAList):
    """A wrapper around a list of applications.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAApplication, filter)

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA application object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(0)

    def last(self) -> XAObject:
        """Retrieves the last element of the list as a wrapped PyXA application object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(-1)

    def pop(self, index: int = -1) -> XAObject:
        """Removes the application at the specified index from the list and returns it.

        .. versionadded:: 0.0.5
        """
        removed = self.xa_elem.lastObject()
        self.xa_elem.removeLastObject()
        app_name = removed["kCGWindowOwnerName"]
        return Application(app_name)

    def __getitem__(self, key: Union[int, slice]):
        """Retrieves the wrapped application object(s) at the specified key."""
        if isinstance(key, slice):
            arr = AppKit.NSArray.alloc().initWithArray_([self.xa_elem[index] for index in range(key.start, key.stop, key.step or 1)])
            return self._new_element(arr, self.__class__)
        app_name = self.xa_elem[key]["kCGWindowOwnerName"]
        return Application(app_name)

    def bundle_identifier(self) -> List[str]:
        """Gets the bundle identifier of every application in the list.

        :return: The list of application bundle identifiers
        :rtype: List[str]

        .. versionadded:: 0.0.5
        """
        return [app.bundle_identifier for app in self]

    def bundle_url(self) -> List[XAURL]:
        """Gets the bundle URL of every application in the list.

        :return: The list of application bundle URLs
        :rtype: List[XAURL]

        .. versionadded:: 0.0.5
        """
        return [XAURL(app.bundle_url)for app in self]

    def executable_url(self) -> List[XAURL]:
        """Gets the executable URL of every application in the list.

        :return: The list of application executable URLs
        :rtype: List[XAURL]

        .. versionadded:: 0.0.5
        """
        return [XAURL(app.executable_url) for app in self]

    def launch_date(self) -> List[datetime]:
        """Gets the launch date of every application in the list.

        :return: The list of application launch dates
        :rtype: List[str]

        .. versionadded:: 0.0.5
        """
        return [app.launch_date for app in self]

    def localized_name(self) -> List[str]:
        """Gets the localized name of every application in the list.

        :return: The list of application localized names
        :rtype: List[str]

        .. versionadded:: 0.0.5
        """
        return [x.get("kCGWindowOwnerName") for x in self.xa_elem]

    def process_identifier(self) -> List[str]:
        """Gets the process identifier of every application in the list.

        :return: The list of application process identifiers
        :rtype: List[str]

        .. versionadded:: 0.0.5
        """
        return [x.get("kCGWindowOwnerPID") for x in self.xa_elem]

    def hide(self):
        """Hides all applications in the list.

        :Example 1: Hide all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.hide()

        .. seealso:: :func:`unhide`

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.hide()

    def unhide(self):
        """Unhides all applications in the list.

        :Example 1: Hide then unhide all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.hide()
        >>> apps.unhide()

        .. seealso:: :func:`hide`

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.unhide()

    def terminate(self):
        """Quits (terminates) all applications in the list. Synonymous with :func:`quit`.

        :Example 1: Terminate all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.terminate()
        
        .. versionadded:: 0.0.5
        """
        for app in self:
            app.terminate()

    def quit(self):
        """Quits (terminates) all applications in the list. Synonymous with :func:`terminate`.

        :Example 1: Quit all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.quit()
        
        .. versionadded:: 0.0.5
        """
        for app in self:
            app.terminate()

    def windows(self) -> 'XACombinedWindowList':
        """Retrieves a list of every window belonging to each application in the list.

        Operations on the list of windows will specialized to scriptable and non-scriptable application window operations as necessary.

        :return: A list containing both scriptable and non-scriptable windows
        :rtype: XACombinedWindowList

        :Example:

        >>> import PyXA
        >>> windows = PyXA.running_applications().windows()
        >>> windows.collapse()
        >>> sleep(1)
        >>> windows.uncollapse()

        .. versionadded:: 0.0.5
        """
        ls = []
        for app in self:
            ls.extend(app.windows().xa_elem)
        ls = AppKit.NSArray.alloc().initWithArray_(ls)
        window_list = self._new_element(ls, XACombinedWindowList)
        return window_list

    def __iter__(self):
        return (Application(object["kCGWindowOwnerName"]) for object in self.xa_elem.objectEnumerator())

    def __contains__(self, item):
        if isinstance(item, XAApplication):
            return item.process_identifier in self.process_identifier()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.localized_name()) + ">"

class Application(XAObject):
    _shared_app = None
    _workspace = None
    app_paths: List[str] = [] #: A list containing the path to each application

    def __init__(self, app_name: str):
        """Creates a new application object.

        :param app_name: The name of the target application
        :type app_name: str

        .. versionadded:: 0.1.0
        """
        # Elevate to XAApplication
        new_self = self.__get_application(app_name)
        self.__class__ = new_self.__class__
        self.__dict__.update(new_self.__dict__)

    @property
    def shared_app(self):
        if Application._shared_app == None:
            Application._shared_app = AppKit.NSApplication.sharedApplication()
        yield Application._shared_app

    @property
    def workspace(self):
        if Application._workspace == None:
            Application._workspace = AppKit.NSWorkspace.sharedWorkspace()
        return Application._workspace

    def __xa_get_path_to_app(self, app_identifier: str) -> str:
        self.__xa_load_app_paths()
        for path in self.app_paths:
            if app_identifier.lower() in path.lower():
                return path

        raise ApplicationNotFoundError(app_identifier)

    def __xa_load_app_paths(self):
        if self.app_paths == []:
            search = XASpotlight()
            search.predicate = "kMDItemContentType == 'com.apple.application-bundle'"
            search.run()
            self.app_paths = [x.path for x in search.results]

    def __get_application(self, app_identifier: str) -> XAApplication:
        """Retrieves a PyXA application object representation of the target application without launching or activating the application.

        :param app_identifier: The name of the application to get an object of.
        :type app_identifier: str
        :return: A PyXA application object referencing the target application.
        :rtype: XAApplication

        .. versionadded:: 0.0.1
        """
        app_identifier_l = app_identifier.lower()

        def _match_open_app(obj, index, stop):
            res = obj.localizedName().lower() == app_identifier_l
            return res, res

        idx_set = self.workspace.runningApplications().indexesOfObjectsPassingTest_(_match_open_app)
        if idx_set.count() == 1:
            index = idx_set.firstIndex()
            app = self.workspace.runningApplications()[index]
            properties = {
                "parent": None,
                "appspace": self.shared_app,
                "workspace": self.workspace,
                "element": app,
                "appref": app,
            }

            app_obj = application_classes.get(app_identifier_l, XAApplication)
            if isinstance(app_obj, tuple):
                module = importlib.import_module("PyXA.apps." + app_obj[0])
                app_class = getattr(module, app_obj[1], None)
                if app_class is not None:
                    application_classes[app_identifier_l] = app_class
                    app = app_class
                else:
                    raise NotImplementedError()

            # Check if the app is supported by PyXA
            app_ref = application_classes.get(app_identifier_l, XAApplication)(properties)
            return app_ref

        app_path = app_identifier
        if not app_identifier.startswith("/"):
            app_path = self.__xa_get_path_to_app(app_identifier)
        bundle = AppKit.NSBundle.alloc().initWithPath_(app_path)
        url = self.workspace.URLForApplicationWithBundleIdentifier_(bundle.bundleIdentifier())

        config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
        config.setActivates_(False)
        config.setHides_(True)

        app_ref = None
        def _launch_completion_handler(app, _error):
            nonlocal app_ref
            properties = {
                "parent": None,
                "appspace": self.shared_app,
                "workspace": self.workspace,
                "element": app,
                "appref": app,
            }

            app_obj = application_classes.get(app_identifier_l, None)
            if isinstance(app_obj, tuple):
                module = importlib.import_module("PyXA.apps." + app_obj[0])
                app_class = getattr(module, app_obj[1], None)
                if app_class is not None:
                    application_classes[app_identifier_l] = app_class
                    app = app_class
                else:
                    raise NotImplementedError()

            app_ref = application_classes.get(app_identifier_l, XAApplication)(properties)
        
        self.workspace.openApplicationAtURL_configuration_completionHandler_(url, config, _launch_completion_handler)
        while app_ref is None:
            sleep(0.01)
        return app_ref




class XACombinedWindowList(XAList):
    """A wrapper around a combined list of both scriptable and non-scriptable windows.

    This class contains methods that specialize to XAWindow and XASBWindow methods as necessary.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAWindow, filter)

    def collapse(self) -> 'XACombinedWindowList':
        """Collapses all windows in the list.

        :return: The window list object
        :rtype: XACombinedWindowList

        :Example 1: Collapse all windows for all currently visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.windows().collapse()

        .. versionadded:: 0.0.5
        """
        for window in self:
            if not hasattr(window.xa_elem, "buttons"):
                # Specialize to XASBWindow
                window = self.xa_prnt._new_element(window.xa_elem, XABaseScriptable.XASBWindow)
            window.collapse()
        return self

    def uncollapse(self) -> 'XACombinedWindowList':
        """Uncollapses all windows in the list.

        :return: The window list object
        :rtype: XACombinedWindowList

        .. versionadded:: 0.1.0
        """
        for window in self:
            if not hasattr(window.xa_elem, "buttons"):
                # Specialize to XASBWindow
                window = self.xa_prnt._new_element(window.xa_elem, XABaseScriptable.XASBWindow)
            window.uncollapse()
        return self




def running_applications() -> List[XAApplication]:
    """Gets PyXA references to all currently visible (not hidden or minimized) running applications whose app bundles are stored in typical application directories.

    :return: A list of PyXA application objects.
    :rtype: List[XAApplication]

    :Example 1: Get the name of each running application

    >>> import PyXA
    >>> apps = PyXA.running_applications()
    >>> print(apps.localized_name())
    ['GitHub Desktop', 'Safari', 'Code', 'Terminal', 'Notes', 'Messages', 'TV']
    
    .. versionadded:: 0.0.1
    """
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    ls = XAPredicate.evaluate_with_format(windows, "kCGWindowIsOnscreen == 1 && kCGWindowLayer == 0")
    properties = {
        "appspace": AppKit.NSApplication.sharedApplication(),
        "workspace": AppKit.NSWorkspace.sharedWorkspace(),
        "element": ls,
    }
    arr = XAApplicationList(properties)
    return arr




def current_application() -> XAApplication:
    """Retrieves a PyXA representation of the frontmost application.

    :return: A PyXA application object referencing the current application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """
    return Application(AppKit.NSWorkspace.sharedWorkspace().frontmostApplication().localizedName())




def application(app_identifier: str) -> XAApplication:
    """Retrieves a PyXA application object representation of the target application without launching or activating the application.

    :param app_identifier: The name of the application to get an object of.
    :type app_identifier: str
    :return: A PyXA application object referencing the target application.
    :rtype: XAApplication

    .. deprecated:: 0.1.0
    
       Use :class:`Application` instead.

    .. versionadded:: 0.0.1
    """
    return Application(app_identifier)