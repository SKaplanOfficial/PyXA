from datetime import datetime
from enum import Enum
import os
from time import sleep
from typing import Any, Callable, List, Union
import importlib

import AppKit
from AppKit import (
    NSWorkspace,
    NSApplication,
    NSPasteboard,
    NSArray,
    NSPasteboardTypeString,
    NSAppleScript,
)
from Foundation import NSURL, NSBundle

from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

from .XABase import *
from .XABaseScriptable import *
from .XAErrors import ApplicationNotFoundError
from .apps import application_classes
from PyXA import XABaseScriptable

VERSION = "0.0.9"
DATE = str(datetime.now())

appspace = NSApplication.sharedApplication()
workspace = NSWorkspace.sharedWorkspace()
app_paths: List[str] = []

scriptable_applications: List[str] = list(application_classes.keys()) #: A list of names of scriptable applications

# class _staticproperty(staticmethod):
#     def __get__(self, *_):         
#         return self.__func__()

# class Application(XAObject):
#     shared_app = NSApplication.sharedApplication()
#     workspace = NSWorkspace.sharedWorkspace()
#     app_paths: List[str] = [] #: A list containing the path to each application
#     current_application: XAApplication #: The currently active application

#     def __init__(self, app_identifier: str):
#         """Creates an application object.

#         :param app_identifier: The name of an application
#         :type app_identifier: str

#         .. versionadded:: 0.0.9
#         """
#         self.app = 

#     def _get_path_to_app(app_identifier: str) -> str:
#         Application._xa_load_app_paths()
#         for path in app_paths:
#             if app_identifier in path:
#                 return path

#         raise ApplicationNotFoundError(app_identifier)

#     def _xa_load_app_paths():
#         if Application.app_paths == []:
#             search = XASpotlight()
#             search.predicate = "kMDItemContentType == 'com.apple.application-bundle'"
#             search.run()
#             app_paths = [x.path for x in search.results]

#     @_staticproperty
#     def current_application() -> XAApplication:
#         return application(workspace.frontmostApplication().localizedName())

#     def _xa_get_open_app(app_identifier: str):
#         def _match_open_app(obj, index, stop):
#             return (obj.localizedName() == app_identifier, stop)

#         idx_set = workspace.runningApplications().indexesOfObjectsPassingTest_(_match_open_app)
#         if idx_set.count() == 1:
#             index = idx_set.firstIndex()
#             app = workspace.runningApplications()[index]
#             return Application._xa_get_app_ref(app_identifier.lower(), app)

#     def _xa_get_app_ref(app_identifier: str, app_object):
#         properties = {
#             "parent": None,
#             "appspace": Application.shared_app,
#             "workspace": Application.workspace,
#             "element": app_object,
#             "appref": app_object,
#         }

#         app_obj = application_classes.get(app_identifier, XAApplication)
#         if isinstance(app_obj, tuple):
#             module = importlib.import_module("PyXA.apps." + app_obj[0])
#             app_class = getattr(module, app_obj[1], None)
#             if app_class is not None:
#                 application_classes[app_identifier] = app_class
#                 app = app_class
#             else:
#                 raise NotImplementedError()

#         return application_classes.get(app_identifier, XAApplication)(properties)

#     def _xa_get_application(app_identifier: str) -> XAApplication:
#         """Retrieves a PyXA application object representation of the target application without launching or activating the application.

#         :param app_identifier: The name of the application to get an object of.
#         :type app_identifier: str
#         :return: A PyXA application object referencing the target application.
#         :rtype: XAApplication

#         .. versionadded:: 0.0.9
#         """
#         open_app = Application._xa_get_open_app(app_identifier)
#         if open_app is not None:
#             return open_app

#         app_path = _get_path_to_app(app_identifier)
#         bundle = NSBundle.alloc().initWithPath_(app_path)
#         url = workspace.URLForApplicationWithBundleIdentifier_(bundle.bundleIdentifier())

#         config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
#         config.setActivates_(False)
#         config.setHides_(True)

#         app_ref = None
#         def _launch_completion_handler(app, _error):
#             nonlocal app_ref
#             app_ref = Application._xa_get_app_ref(app_identifier.lower(), app)

#         workspace.openApplicationAtURL_configuration_completionHandler_(url, config, _launch_completion_handler)
#         while app_ref is None:
#             sleep(0.01)
#         return app_ref


def _xa_get_path_to_app(app_identifier: str) -> str:
    _xa_load_app_paths()
    for path in app_paths:
        if app_identifier in path:
            return path

    raise ApplicationNotFoundError(app_identifier)

def _xa_load_app_paths():
    global app_paths
    if app_paths == []:
        search = XASpotlight()
        search.predicate = "kMDItemContentType == 'com.apple.application-bundle'"
        search.run()
        app_paths = [x.path for x in search.results]


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
        "appspace": appspace,
        "workspace": workspace,
        "element": ls,
    }
    arr = XAApplicationList(properties)
    return arr


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
        return application(app_name)

    def __getitem__(self, key: Union[int, slice]):
        """Retrieves the wrapped application object(s) at the specified key."""
        if isinstance(key, slice):
            arr = AppKit.NSArray.alloc().initWithArray_([self.xa_elem[index] for index in range(key.start, key.stop, key.step or 1)])
            return self._new_element(arr, self.__class__)
        app_name = self.xa_elem[key]["kCGWindowOwnerName"]
        return application(app_name)

    def bundle_identifier(self) -> List[str]:
        return [app.bundle_identifier for app in self]

    def bundle_url(self) -> List[str]:
        return [app.bundle_url for app in self]

    def executable_url(self) -> List[str]:
        return [app.executable_url for app in self]

    def launch_date(self) -> List[datetime]:
        return [app.launch_date for app in self]

    def localized_name(self) -> List[str]:
        return [x.get("kCGWindowOwnerName") for x in self.xa_elem]

    def process_identifier(self) -> List[str]:
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

        .. versionadded:: 0.0.5
        """
        ls = []
        for app in self:
            ls.extend(app.windows().xa_elem)
        ls = AppKit.NSArray.alloc().initWithArray_(ls)
        window_list = self._new_element(ls, XACombinedWindowList)
        return window_list

    def __iter__(self):
        return (application(object["kCGWindowOwnerName"]) for object in self.xa_elem.objectEnumerator())

    def __repr__(self):
        return "<" + str(type(self)) + str(self.localized_name()) + ">"




class XACombinedWindowList(XAList):
    """A wrapper around a combined list of both scriptable and non-scriptable windows.

    This class contains methods that specialize to XAWindow and XASBWindow methods as necessary.

    .. versionadded:: 0.0.5
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAWindow, filter)

    def collapse(self):
        """Collapses all windows in the list.

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


def current_application() -> XAApplication:
    """Retrieves a PyXA representation of the frontmost application.

    :return: A PyXA application object referencing the current application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """
    return application(workspace.frontmostApplication().localizedName())


def application(app_identifier: str) -> XAApplication:
    """Retrieves a PyXA application object representation of the target application without launching or activating the application.

    :param app_identifier: The name of the application to get an object of.
    :type app_identifier: str
    :return: A PyXA application object referencing the target application.
    :rtype: XAApplication

    .. versionadded:: 0.0.1
    """
    app_identifier_l = app_identifier.lower()

    def _match_open_app(obj, index, stop):
        return (obj.localizedName() == app_identifier, stop)

    idx_set = workspace.runningApplications().indexesOfObjectsPassingTest_(_match_open_app)
    if idx_set.count() == 1:
        index = idx_set.firstIndex()
        app = workspace.runningApplications()[index]
        properties = {
            "parent": None,
            "appspace": appspace,
            "workspace": workspace,
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

        app_ref = application_classes.get(app_identifier_l, XAApplication)(properties)
        return app_ref

    app_path = _xa_get_path_to_app(app_identifier)
    bundle = NSBundle.alloc().initWithPath_(app_path)
    url = workspace.URLForApplicationWithBundleIdentifier_(bundle.bundleIdentifier())

    config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
    config.setActivates_(False)
    config.setHides_(True)

    app_ref = None
    def _launch_completion_handler(app, _error):
        nonlocal app_ref
        properties = {
            "parent": None,
            "appspace": appspace,
            "workspace": workspace,
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

    
    workspace.openApplicationAtURL_configuration_completionHandler_(url, config, _launch_completion_handler)
    while app_ref is None:
        sleep(0.01)
    return app_ref