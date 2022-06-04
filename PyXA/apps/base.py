"""Control the macOS ___ application using JXA-like syntax.
"""

# import EventKit
# from pprint import pprint

# from ScriptingBridge import SBElementArray

# from XABase import XAApplication, XAWindow, XAObject
# from XABaseScriptable import XAApplication, XAObject
# from mixins.XAActions import XACanConstructElement, XAAcceptsPushedElements
# from mixins.XARelations import XAHasElements

# class XANotesApplication(XAApplication, XACanConstructElement, XAAcceptsPushedElements):
#     def __init__(self, parent, appspace, workspace, name, app = None):
#         super().__init__(parent, appspace, workspace, name, app)

#     def notes(self):
#         return super().elements("notes", XANote)

#     def notes_with_properties(self, properties: dict):
#         return super().elements_with_properties("notes", properties, XANote)

#     def note(self, index: int):
#         return super().element_at_index("notes", index, XANote)

#     def first_note(self):
#         return super().first_element("notes", XANote)

#     def last_note(self):
#         return super().last_element("notes", XANote)

#     def new_note(self, name, body):
#         return self.push("note", {"body": f"<b>{name}</b><br />{body}"}, self.element.notes())

#     def new_folder(self, name):
#         return self.push("folder", {"name": name}, self.element.folders())

# class XANote(XACanConstructElement, XAAcceptsPushedElements):
#     def __init__(self, parent, appspace, workspace, name, element, appref):
#         super().__init__(parent, appspace, workspace, name, element, appref)