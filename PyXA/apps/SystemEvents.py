"""Control the macOS System Events application using JXA-like syntax.
"""

from PyXA import XABase

class XASystemEventsApplication(XABase.XAApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    def __init__(self, properties):
        super().__init__(properties)

    def processes(self):
        return super().elements("applicationProcesses", XABase.XAApplicationProcess)

    def processes_with_properties(self, properties):
        return super().elements_with_properties("applicationProcesses", properties, XABase.XAApplicationProcess)
    
    def process(self, index: int):
        return super().element_at_index("applicationProcesses", index, XABase.XAApplicationProcess)

    def first_process(self):
        return super().first_element("applicationProcesses", XABase.XAApplicationProcess)

    def last_process(self):
        return super().last_element("applicationProcesses", XABase.XAApplicationProcess)


class XAApplicationProcess(XABase.XAHasElements, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    def __init__(self, properties):
        super().__init__(properties)

    def windows(self):
        return super().elements("windows", XASystemEventsWindow)

    def windows_with_properties(self, properties: dict):
        return super().elements_with_properties("windows", properties, XASystemEventsWindow)

    def window(self, index: int):
        return super().element_at_index("windows", index, XASystemEventsWindow)

    def first_window(self):
        return super().first_element("windows", XASystemEventsWindow)

    def last_window(self):
        return super().last_element("windows", XASystemEventsWindow)

class XASystemEventsUIElement(XABase.XAHasElements):
    def __init__(self, properties):
        super().__init__(properties)
        self.shortcuts = {}

    def entire_contents(self) -> 'XASystemEventsUIElement':
        print(self.properties["element"].entireContents())
        return self

    def all(self, specifier, in_class = "groups", force_update = False):
        if (specifier, in_class) in self.shortcuts and not force_update:
            return self.shortcuts[(specifier, in_class)]

        valid_specifiers = {
            "windows": XASystemEventsWindow,
            "groups": XASystemEventsGroup,
            "text_fields": XASystemEventsTextField,
            "text_areas": XASystemEventsTextArea,
            "buttons": XASystemEventsButton,
            "actions": XASystemEventsAction,
        }
        target_class = valid_specifiers[specifier]

        target_objects = []
        sub_objects = self.__getattribute__(in_class)()
        for item in sub_objects:
            target_objects.extend(item.all(specifier, in_class))

        if isinstance(self, target_class):
            target_objects.append(self)
        else:
            target_objects.extend(self.__getattribute__(specifier)())

        self.shortcuts[(specifier, in_class)] = target_objects
        return target_objects

    ## Windows
    def windows(self):
        return super().elements("windows", XASystemEventsWindow)

    def windows_with_properties(self, properties: dict):
        return super().elements_with_properties("windows", properties, XASystemEventsWindow)

    def window(self, index: int):
        return super().element_at_index("windows", index, XASystemEventsWindow)

    def first_window(self):
        return super().first_element("windows", XASystemEventsWindow)

    def last_window(self):
        return super().last_element("windows", XASystemEventsWindow)

    ## Toolbars
    def toolbars(self):
        return super().elements("toolbars", XASystemEventsToolbar)

    def toolbars_with_properties(self, properties: dict):
        return super().elements_with_properties("toolbars", properties, XASystemEventsToolbar)

    def toolbar(self, index: int):
        return super().element_at_index("toolbars", index, XASystemEventsToolbar)

    def first_toolbar(self):
        return super().first_element("toolbars", XASystemEventsToolbar)

    def last_toolbar(self):
        return super().last_element("toolbars", XASystemEventsToolbar)

    ## Groups
    def groups(self):
        return super().elements("groups", XASystemEventsGroup)

    def groups_with_properties(self, properties: dict):
        return super().elements_with_properties("groups", properties, XASystemEventsGroup)

    def group(self, index: int):
        return super().element_at_index("groups", index, XASystemEventsGroup)

    def first_group(self):
        return super().first_element("groups", XASystemEventsGroup)

    def last_group(self):
        return super().last_element("groups", XASystemEventsGroup)

    ## TextFields
    def text_fields(self):
        return super().elements("textFields", XASystemEventsTextField)

    def text_fields_with_properties(self, properties: dict):
        return super().elements_with_properties("textFields", properties, XASystemEventsTextField)

    def text_field(self, index: int):
        return super().element_at_index("textFields", index, XASystemEventsTextField)

    def first_text_field(self):
        return super().first_element("textFields", XASystemEventsTextField)

    def last_text_field(self):
        return super().last_element("textFields", XASystemEventsTextField)

    ## TextAreas
    def text_areas(self):
        return super().elements("textAreas", XASystemEventsTextArea)

    def text_areas_with_properties(self, properties: dict):
        return super().elements_with_properties("textAreas", properties, XASystemEventsTextArea)

    def text_area(self, index: int):
        return super().element_at_index("textAreas", index, XASystemEventsTextArea)

    def first_text_area(self):
        return super().first_element("textAreas", XASystemEventsTextArea)

    def last_text_area(self):
        return super().last_element("textAreas", XASystemEventsTextArea)

    ## Buttons
    def buttons(self):
        return super().elements("buttons", XASystemEventsButton)

    def buttons_with_properties(self, properties: dict):
        return super().elements_with_properties("buttons", properties, XASystemEventsButton)

    def button(self, index: int):
        return super().element_at_index("buttons", index, XASystemEventsButton)

    def first_button(self):
        return super().first_element("buttons", XASystemEventsButton)

    def last_button(self):
        return super().last_element("buttons", XASystemEventsButton)

    ## Actions
    def actions(self):
        return super().elements("actions", XASystemEventsAction)

    def actions_with_properties(self, properties: dict):
        return super().elements_with_properties("actions", properties, XASystemEventsAction)

    def action(self, index: int):
        return super().element_at_index("actions", index, XASystemEventsAction)

    def first_action(self):
        return super().first_element("actions", XASystemEventsAction)

    def last_action(self):
        return super().last_element("actions", XASystemEventsAction)

    def __repr__(self):
        return str(self.properties["role"]) + "/" + str(self.properties["subrole"]) + "/" + str(self.properties["roleDescription"]) + "/" + str(self.properties["objectDescription"])

class XASystemEventsWindow(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)

    def activate(self):
        self.actions_with_properties({"name": "AXRaise"})[0].perform()
        return self

    def close_button(self):
        self.buttons_with_properties({"subrole": "AXCloseButton"})[0]
        return self

    def fullscreen_button(self):
        self.actions_with_properties({"subrole": "AXFullScreenButton"})[0]
        return self

    def minimize_button(self):
        self.actions_with_properties({"subrole": "AXMinimizeButton"})[0]
        return self


class XASystemEventsAction(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)

    def perform(self):
        self.properties["element"].perform()
        return self


class XASystemEventsToolbar(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsMenu(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsMenuBar(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsMenuBarItem(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsMenuButton(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsMenuItem(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsGroup(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsTabGroup(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsScrollArea(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsScrollBar(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsTable(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsTextArea(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsTextField(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsButton(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)

    def click(self):
        self.actions_with_properties({"name": "AXPress"})[0].perform()
        return self

    def press(self):
        self.actions_with_properties({"name": "AXPress"})[0].perform()
        return self

    def option_click(self):
        self.actions_with_properties({"name": "AXZoomWindow"})[0].perform()
        return self

    def show_menu(self):
        self.actions_with_properties({"name": "AXShowMenu"})[0].perform()
        return self


class XASystemEventsCheckbox(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsRadioGroups(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsRadioButtons(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsStaticText(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsImage(XASystemEventsUIElement):
    def __init__(self, properties):
        super().__init__(properties)