"""Control Pages using JXA-like syntax.
"""

from AppKit import NSFileManager

from PyXA import XABase
from PyXA import XABaseScriptable

class XAPagesApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements):
    def __init__(self, properties):
        super().__init__(properties)

    def documents(self):
        return super().elements("documents", XAPagesDocument)

    def documents_with_properties(self, properties: dict):
        return super().elements_with_properties("documents", properties, XAPagesDocument)

    def document(self, index: int):
        return super().element_at_index("documents", index, XAPagesDocument)

    def first_document(self):
        return super().first_element("documents", XAPagesDocument)

    def last_document(self):
        return super().last_element("documents", XAPagesDocument)

    def new_document(self, name = "Untitled", text = ""):
        location = NSFileManager.alloc().homeDirectoryForCurrentUser().relativePath() + "/Documents/" + name
        print(location)
        return self.push("document", {"name": name, "text": text, "path": location}, self.properties["element"].documents())


class XAPagesDocument(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument):
    def __init__(self, properties):
        super().__init__(properties)

    ## Sections
    def sections(self):
        return super().elements("sections", XAPagesSection)

    def sections_with_properties(self, properties: dict):
        return super().elements_with_properties("sections", properties, XAPagesSection)

    def section(self, index: int):
        return super().element_at_index("sections", index, XAPagesSection)

    def first_section(self):
        return super().first_element("sections", XAPagesSection)

    def last_section(self):
        return super().last_element("sections", XAPagesSection)

    def new_section(self):
        return self.push("section", {}, self.properties["element"].sections())

    ## Pages
    def pages(self):
        return super().elements("pages", XAPagesPage)

    def pages_with_properties(self, properties: dict):
        return super().elements_with_properties("pages", properties, XAPagesPage)

    def page(self, index: int):
        return super().element_at_index("pages", index, XAPagesPage)

    def first_page(self):
        return super().first_element("pages", XAPagesPage)

    def last_page(self):
        return super().last_element("pages", XAPagesPage)

    def new_page(self):
        return self.push("page", {}, self.properties["element"].pages())

    ## Shapes
    def shapes(self):
        return super().elements("shapes", XAPagesShape)

    def shapes_with_properties(self, properties: dict):
        return super().elements_with_properties("shapes", properties, XAPagesShape)

    def shape(self, index: int):
        return super().element_at_index("shapes", index, XAPagesShape)

    def first_shape(self):
        return super().first_element("shapes", XAPagesShape)

    def last_shape(self):
        return super().last_element("shapes", XAPagesShape)

    # def new_shape(self):
    #     return self.push("shape", {"backgroundFillType": "color fill", "width": 100, "height": 100, "position": {"x": 213, "y": 446}}, self.element.pages())


class XAPagesSection(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument):
    def __init__(self, properties):
        super().__init__(properties)


class XAPagesPage(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument):
    def __init__(self, properties):
        super().__init__(properties)


class XAPagesShape(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument):
    def __init__(self, properties):
        super().__init__(properties)