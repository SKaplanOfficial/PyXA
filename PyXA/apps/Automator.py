""".. versionadded:: 0.0.4

Control Automator using JXA-like syntax.
"""

from enum import Enum
from turtle import st
from typing import Any, List, Tuple, Union
from AppKit import NSFileManager, NSURL, NSSet

from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

class XAAutomatorApplication(XABaseScriptable.XASBApplication, XABase.XACanOpenPath):
    """A class for managing and interacting with Automator.app.

    .. seealso:: :class:`XAAutomatorWindow`, :class:`XAAutomatorDocument`

    .. versionadded:: 0.0.4
    """
    class SaveOption(Enum):
        """Options for whether to save documents when closing them.
        """
        YES = XABase.OSType('yes ') #: Save the file
        NO  = XABase.OSType('no  ') #: Do not save the file
        ASK = XABase.OSType('ask ') #: Ask user whether to save the file (bring up dialog)

    class WarningLevel(Enum):
        """Options for warning level in regard to likelihood of data loss.
        """
        IRREVERSIBLE    = XABase.OSType("irrv")
        NONE            = XABase.OSType('none')
        REVERSIBLE      = XABase.OSType('rvbl')

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing.
        """
        STANDARD = 'lwst' #: Standard PostScript error handling
        DETAILED = 'lwdt' #: Print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAAutomatorWindow

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Chromium is the active application
        self.version: str #: The version of Chromium

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def add(self, action: 'XAAutomatorAction', workflow: 'XAAutomatorWorkflow', index: int = -1) -> 'XAAutomatorApplication':
        self.xa_scel.add_to_atIndex_(action.xa_elem, workflow.xa_elem, index)
        return self


    def documents(self, filter: Union[dict, None] = None) -> 'XAAutomatorDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter documents by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of documents
        :rtype: XAAutomatorDocumentList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.documents(), XAAutomatorDocumentList, filter)

    def automator_actions(self, filter: Union[dict, None] = None) -> 'XAAutomatorActionList':
        """Returns a list of Automator actions, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter actions by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of actions
        :rtype: XAAutomatorActionList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.AutomatorActions(), XAAutomatorActionList, filter)

    def variables(self, filter: Union[dict, None] = None) -> 'XAAutomatorVariableList':
        """Returns a list of Automator variables, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter variables by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of variables
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.variables(), XAAutomatorVariableList, filter)

    def workflows(self, filter: Union[dict, None] = None) -> 'XAAutomatorWorkflowList':
        """Returns a list of Automator workflows, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter workflows by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of workflows
        :rtype: XAAutomatorWorkflowList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.workflows(), XAAutomatorWorkflowList, filter)

    def make(self, specifier: str, properties: dict):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.4
        """
        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "workflow":
            return self._new_element(obj, XAAutomatorWindow)
        elif specifier == "variable":
            return self._new_element(obj, XAAutomatorVariable)
        elif specifier == "document":
            return self._new_element(obj, XAAutomatorDocument)
        elif specifier == "action":
            return self._new_element(obj, XAAutomatorAction)
        elif specifier == "requiredResource":
            return self._new_element(obj, XAAutomatorRequiredResource)
        elif specifier == "setting":
            return self._new_element(obj, XAAutomatorSetting)

class XAAutomatorWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Automator windows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The full title of the window
        self.id: int #: The unique identifier for the window
        self.index: int #: The index of the window in the front-to-back ordering
        self.bounds: Tuple[Tuple[int, int], Tuple[int, int]] #: The bounding rectangle of the window
        self.floating: bool #: Whether the window float
        self.modal: bool #: Whether the window is a modal window
        self.closeable: bool #: Whether the window has a close button
        self.miniaturizable: bool #: Whether the window can be minimized
        self.miniaturized: bool #: Whether the window is currently minimized
        self.resizable: bool #: Whether the window can be resized
        self.visible: bool #: Whether the window is currently visible
        self.zoomable: bool #: Whether the window can be zoomed
        self.zoomed: bool #: Whether the window is currently zoomed
        self.titled: bool #: Whether the window has a title bar
        self.document: XAAutomatorDocument #: The document currently displayed in the window

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def id(self) -> int:
        return self.xa_scel.id()

    @property
    def index(self) -> int:
        return self.xa_scel.index()

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.xa_scel.bounds()

    @property
    def floating(self) -> bool:
        return self.xa_scel.floating()

    @property
    def modal(self) -> bool:
        return self.xa_scel.modal()

    @property
    def closeable(self) -> bool:
        return self.xa_scel.closeable()

    @property
    def miniaturizable(self) -> bool:
        return self.xa_scel.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        return self.xa_scel.miniaturized()

    @property
    def resizable(self) -> bool:
        return self.xa_scel.resizable()

    @property
    def visible(self) -> bool:
        return self.xa_scel.visible()

    @property
    def zoomable(self) -> bool:
        return self.xa_scel.zoomable()

    @property
    def zoomed(self) -> bool:
        return self.xa_scel.zoomed()

    @property
    def titled(self) -> bool:
        return self.xa_scel.titled()

    @property
    def document(self) -> 'XAAutomatorDocument':
        return self._new_element(self.xa_scel.document(), XAAutomatorDocument)


class XAAutomatorDocumentList(XABase.XAList):
    """A wrapper around a list of Automator documents which utilizes fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorDocument, filter)

    def id(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def title(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def by_id(self, id: int) -> 'XAAutomatorDocument':
        return self.by_property("id", id)

    def by_title(self, title: str) -> 'XAAutomatorDocument':
        return self.by_property("title", title)

    def by_index(self, index: int) -> 'XAAutomatorDocument':
        return self.by_property("index", index)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAAutomatorDocument(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Automator windows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.modified: bool #: Whether the document has been modified since its last save
        self.name: str #: The title of the document
        self.path: str #: The path to the document on the disk

    @property
    def modified(self) -> bool:
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorActionList(XABase.XAList):
    """A wrapper around a list of Automator required resources which utilizes fast enumeration techniques.

    All properties of required resources can be called as methods on the wrapped list, returning a list containing each resource's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorAction, filter)

    def bundle_id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bundleId"))

    def category(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("category"))

    def comment(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment"))

    def enabled(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled"))

    def execution_error_message(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorMessage"))

    def execution_error_number(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorNumber"))

    def execution_result(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionResult"))

    def icon_name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("iconName"))

    def ignores_input(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ignoresInput"))

    def index(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index"))

    def input_types(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("inputTypes"))

    def keywords(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("keywords"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def output_types(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("outputTypes"))

    def parent_workflow(self) -> 'XAAutomatorWorkflowList':
        ls = self.xa_elem.arrayByApplyingSelector_("parentWorkflow")
        return self._new_element(ls, XAAutomatorWorkflowList)

    def path(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path"))

    def show_action_when_run(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("showActionWhenRun"))

    def target_application(self) -> List[List[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("targetApplication"))

    def version(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def warning_action(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("warningAction"))

    def warning_level(self) -> List[XAAutomatorApplication.WarningLevel]:
        ls = self.xa_elem.arrayByApplyingSelector_("warningLevel")
        return [XAAutomatorApplication.WarningLevel(x) for x in ls]

    def warning_message(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("warningMessage"))

    def by_bundle_id(self, bundle_id: str) -> 'XAAutomatorAction':
        return self.by_property("bundleId", bundle_id)

    def by_category(self, category: List[str]) -> 'XAAutomatorAction':
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> 'XAAutomatorAction':
        return self.by_property("comment", comment)

    def by_enabled(self, enabled: bool) -> 'XAAutomatorAction':
        return self.by_property("enabled", enabled)

    def by_execution_error_message(self, execution_error_message: str) -> 'XAAutomatorAction':
        return self.by_property("executionErrorMessage", execution_error_message)

    def by_execution_error_number(self, execution_error_number: int) -> 'XAAutomatorAction':
        return self.by_property("executionErrorNumber", execution_error_number)

    def by_execution_result(self, execution_result: Any) -> 'XAAutomatorAction':
        return self.by_property("executionResult", execution_result)

    def by_icon_name(self, icon_name: str) -> 'XAAutomatorAction':
        return self.by_property("iconName", icon_name)

    def by_id(self, id: str) -> 'XAAutomatorAction':
        return self.by_property("id", id)

    def by_ignores_input(self, ignores_input: bool) -> 'XAAutomatorAction':
        return self.by_property("ignoresInput", ignores_input)

    def by_input_types(self, input_types: List[str]) -> 'XAAutomatorAction':
        return self.by_property("inputTypes", input_types)

    def by_keywords(self, keywords: List[str]) -> 'XAAutomatorAction':
        return self.by_property("keywords", keywords)

    def by_name(self, name: str) -> 'XAAutomatorAction':
        return self.by_property("name", name)

    def by_output_types(self, output_types: List[str]) -> 'XAAutomatorAction':
        return self.by_property("outputTypes", output_types)

    def by_parent_workflow(self, parent_workflow: 'XAAutomatorWorkflow') -> 'XAAutomatorAction':
        return self.by_property("parentWorkflow", parent_workflow.xa_elem)

    def by_path(self, path: str) -> 'XAAutomatorAction':
        return self.by_property("path", path)

    def by_show_action_when_run(self, show_action_when_run: bool) -> 'XAAutomatorAction':
        return self.by_property("show_action_when_run", show_action_when_run)

    def by_target_application(self, target_application: List[str]) -> 'XAAutomatorAction':
        return self.by_property("targetApplication", target_application)

    def by_version(self, version: str) -> 'XAAutomatorAction':
        return self.by_property("version", version)

    def by_warning_action(self, warning_action: str) -> 'XAAutomatorAction':
        return self.by_property("warningAction", warning_action)

    def by_warning_level(self, warning_level: XAAutomatorApplication.WarningLevel) -> 'XAAutomatorAction':
        return self.by_property("warningLevel", warning_level.value)

    def by_warning_message(self, warning_message: str) -> 'XAAutomatorAction':
        return self.by_property("warningMessage", warning_message)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorAction(XABaseScriptable.XASBObject):
    """A class for managing and interacting with actions in Automator.app.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.bundle_id: str #: The bundle identifier for the action
        self.category: List[str] #: The category that contains the action
        self.comment: str #: The comment for the name of the action
        self.enabled: bool #: Whether the action is enabled
        self.execution_error_message: str #: The text error message generated by execution of the action
        self.execution_error_number: int #: The numeric error code generated by execution of the action
        self.execution_result: Any #: The result of the action, passed as input to the next action
        self.icon_name: str #: The name for the icon associated with the action
        self.id: str #: The unique identifier for the action
        self.ignores_input: bool #: Whether the action ignores input when run
        self.index: int #: The index of the action from the first action in the workflow
        self.input_types: List[str] #: The input types accepted by the action
        self.keywords: List[str] #: The keywords that describe the action
        self.name: str #: The localized name of the action
        self.output_types: List[str] #: The output types produces by the action
        self.parent_workflow: XAAutomatorWorkflow #: The workflow that contains the action
        self.path: str #: The path of the file that contains the action
        self.show_action_when_run: bool #: Whether the action should show its user interface when run
        self.target_application: List[str] #: The application(s) with which the action communicates
        self.version: str #: The version of the action
        self.warning_action: str #: The action suggested by the warning, if any
        self.warning_level: XAAutomatorApplication.WarningLevel #: The level of the warning, increasing in likelihood of data loss
        self.warning_message: str #: The message that accompanies the warning, if any

    @property
    def bundle_id(self) -> str:
        return self.xa_elem.bundleId()

    @property
    def category(self) -> List[str]:
        return self.xa_elem.category()

    @property
    def comment(self) -> str:
        return self.xa_elem.comment()

    @property
    def enabled(self) -> bool:
        return self.xa_elem.enabled()

    @property
    def execution_error_message(self) -> str:
        return self.xa_elem.executionErrorMessage()

    @property
    def execution_error_number(self) -> int:
        return self.xa_elem.executionErrorNumber()

    @property
    def execution_result(self) -> Any:
        return self.xa_elem.executionResult()

    @property
    def icon_name(self) -> str:
        return self.xa_elem.iconName()

    @property
    def id(self) -> str:
        return self.xa_elem.id()

    @property
    def ignores_input(self) -> bool:
        return self.xa_elem.ignoresInput()

    @property
    def index(self) -> int:
        return self.xa_elem.index()

    @property
    def input_types(self) -> List[str]:
        return self.xa_elem.inputTypes()

    @property
    def keywords(self) -> List[str]:
        return self.xa_elem.keywords()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def output_types(self) -> List[str]:
        return self.xa_elem.outputTypes()

    @property
    def parent_workflow(self) -> 'XAAutomatorWorkflow':
        return self._new_element(self.xa_elem.parentWorkflow(), XAAutomatorWorkflow)

    @property
    def path(self) -> str:
        return self.xa_elem.path()

    @property
    def show_action_when_run(self) -> bool:
        return self.xa_elem.showActionWehnRun()

    @property
    def target_application(self) -> List[str]:
        return self.xa_elem.targetApplication()

    @property
    def version(self) -> str:
        return self.xa_elem.version()

    @property
    def warning_action(self) -> str:
        return self.xa_elem.warningAction()

    @property
    def warning_level(self) -> XAAutomatorApplication.WarningLevel:
        return XAAutomatorApplication.WarningLevel(self.xa_elem.warningLevel())

    @property
    def warning_message(self) -> str:
        return self.xa_elem.warningMessage()

    def required_resources(self, filter: Union[dict, None] = None) -> 'XAAutomatorRequiredResourceList':
        """Returns a list of required resource, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter resources by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of required resources
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.requiredResources(), XAAutomatorRequiredResourceList, filter)

    def settings(self, filter: Union[dict, None] = None) -> 'XAAutomatorSettingList':
        """Returns a list of settings, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter settings by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of settings
        :rtype: XAAutomatorWorkflowList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.settings(), XAAutomatorSettingList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorRequiredResourceList(XABase.XAList):
    """A wrapper around a list of Automator required resources which utilizes fast enumeration techniques.

    All properties of required resources can be called as methods on the wrapped list, returning a list containing each resource's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorRequiredResource, filter)

    def kind(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def resource(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("resource"))

    def version(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("version"))

    def by_kind(self, kind: str) -> 'XAAutomatorRequiredResource':
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> 'XAAutomatorRequiredResource':
        return self.by_property("name", name)

    def by_resource(self, resource: str) -> 'XAAutomatorRequiredResource':
        return self.by_property("resource", resource)

    def by_version(self, version: int) -> 'XAAutomatorRequiredResource':
        return self.by_property("version", version)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAAutomatorRequiredResource(XABaseScriptable.XASBObject):
    """A class for managing and interacting with required resources in Automator.app.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.kind: str #: The kind of required resource
        self.name: str #: The name of the required resource
        self.resource: str #: The specification of the required resource
        self.version: int #: The minimum acceptable version of the required resource

    @property
    def kind(self) -> str:
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def resource(self) -> str:
        return self.xa_elem.resource()

    @property
    def version(self) -> int:
        return self.xa_elem.version()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorSettingList(XABase.XAList):
    """A wrapper around a list of Automator settings which utilizes fast enumeration techniques.

    All properties of settings can be called as methods on the wrapped list, returning a list containing each setting's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorSetting, filter)

    def default_value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultValue"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def by_default_value(self, default_value: Any) -> 'XAAutomatorSetting':
        if isinstance(default_value, XABase.XAObject):
            default_value = default_value.xa_elem
        return self.by_property("defaultValue", default_value)

    def by_name(self, name: str) -> 'XAAutomatorSetting':
        return self.by_property("name", name)

    def by_value(self, value: Any) -> 'XAAutomatorSetting':
        if isinstance(value, XABase.XAObject):
            value = value.xa_elem
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAAutomatorSetting(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Automator settings (i.e. named values).

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.default_value: Any #: The default value of the setting
        self.name: str #: The name of the setting
        self.value: Any #: The value of the setting

    @property
    def default_value(self) -> Any:
        return self.xa_elem.defaultValue()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorVariableList(XABase.XAList):
    """A wrapper around a list of Automator variables which utilizes fast enumeration techniques.

    All properties of variables can be called as methods on the wrapped list, returning a list containing each variable's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorVariable, filter)

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def settable(self) -> List[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("settable"))

    def value(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value"))

    def by_name(self, name: str) -> 'XAAutomatorVariable':
        return self.by_property("name", name)

    def by_settable(self, settable: bool) -> 'XAAutomatorVariable':
        return self.by_property("settable", settable)

    def by_value(self, value: Any) -> 'XAAutomatorVariable':
        if isinstance(value, XABase.XAObject):
            value = value.xa_elem
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAAutomatorVariable(XABaseScriptable.XASBObject):
    """A class for managing and interacting with Automator variables.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name: str #: The name of the variable
        self.settable: bool #: Whether the name and value of the variable can be changed
        self.value: Any #: The value of the variable

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def settable(self) -> bool:
        return self.xa_elem.settable()

    @property
    def value(self) -> Any:
        return self.xa_elem.value()
        
    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorWorkflowList(XABase.XAList):
    """A wrapper around a list of Automator workflows which utilizes fast enumeration techniques.

    All properties of workflows can be called as methods on the wrapped list, returning a list containing each workflow's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorWorkflow, filter)

    def current_action(self) -> XAAutomatorActionList:
        ls = self.xa_elem.arrayByApplyingSelector_("currentAction")
        return self._new_element(ls, XAAutomatorActionList)

    def execution_error_message(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorMessage"))

    def execution_error_number(self) -> List[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorNumber"))

    def execution_id(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionId"))

    def execution_result(self) -> List[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionResult"))

    def name(self) -> List[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def by_current_action(self, current_action: XAAutomatorAction) -> 'XAAutomatorWorkflow':
        return self.by_property("currentAction", current_action.xa_elem)

    def by_execution_error_message(self, execution_error_message: str) -> 'XAAutomatorWorkflow':
        return self.by_property("executionErrorMessage", execution_error_message)

    def by_execution_error_number(self, execution_error_number: int) -> 'XAAutomatorWorkflow':
        return self.by_property("executionErrorNumber", execution_error_number)

    def by_execution_id(self, execution_id: str) -> 'XAAutomatorWorkflow':
        return self.by_property("executionId", execution_id)

    def by_execution_result(self, result: Any) -> 'XAAutomatorWorkflow':
        return self.by_property("result", result)

    def by_name(self, name: str) -> 'XAAutomatorWorkflow':
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAAutomatorWorkflow(XAAutomatorDocument):
    """A class for managing and interacting with Automator workflows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.current_action: XAAutomatorAction #: The current or most recent action of the workflow
        self.execution_error_message: str #: The text error message generated by the most recent execution
        self.execution_error_number: int #: The numeric error code generated by the most recent execution
        self.execution_id: str #: The unique identifier for the current or most recent execution
        self.execution_result: Any #: The result of the most resent execution
        self.name: str #: The name of the workflow

    @property
    def current_action(self) -> XAAutomatorAction:
        return self._new_element(self.xa_elem.currentAction(), XAAutomatorAction)

    @property
    def execution_error_message(self) -> str:
        return self.xa_elem.executionErrorMessage()

    @property
    def execution_error_number(self) -> int:
        return self.xa_elem.executionErrorNumber()

    @property
    def execution_id(self) -> str:
        return self.xa_elem.executionId()

    @property
    def execution_result(self) -> Any:
        return self.xa_elem.executionResult()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    def execute(self):
        self.xa_elem.execute()

    def automator_actions(self, filter: Union[dict, None] = None) -> 'XAAutomatorActionList':
        """Returns a list of actions, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter actions by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of actions
        :rtype: XAAutomatorActionList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.AutomatorActions(), XAAutomatorActionList, filter)

    def variables(self, filter: Union[dict, None] = None) -> 'XAAutomatorVariableList':
        """Returns a list of variables, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter variables by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of variables
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.variables(), XAAutomatorVariableList, filter)

    def delete(self):
        """Closes the workflow.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"