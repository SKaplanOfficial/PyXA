from typing import Union

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable


class XABookMarkableApplication(XABaseScriptable.XASBApplication):
	"""The application's top-level scripting object.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties):
		super().__init__(properties)
		self.xa_wcls = XABookMarkableWindow

	@property
	def name(self) -> 'str':
		"""The name of the application.

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.name()

	@property
	def frontmost(self) -> 'bool':
		"""Is this the frontmost (active) application?

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.frontmost()

	@property
	def version(self) -> 'str':
		"""The version of the application.

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.version()

	@property
	def working(self) -> 'bool':
		"""BookMarkable is working on something

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.working()

	@property
	def current_bookmark(self) -> 'XABookMarkableBookmark':
		"""Current Bookmark

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.current_bookmark()

	@property
	def current_url(self) -> 'str':
		"""URL of currently selected document. May not be a bookmark yet.

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.current_url()

	@property
	def current_path(self) -> 'str':
		"""file path of currently selected document (if it is a file). May not be a bookmark yet.

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.current_path()

	@property
	def default_keywords(self) -> 'XABookMarkable':
		"""List of default keywords (tags)

		.. versionadded:: 0.1.0
		"""
		return self.xa_scel.default_keywords()

	def panels(self, filter: Union[dict, None] = None) -> 'XABookMarkablePanel':
		"""Returns a list of panels, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		return self._new_element(self.xa_scel.panels(), XABookMarkablePanelList, filter)

	def bookmarks(self, filter: Union[dict, None] = None) -> 'XABookMarkableBookmark':
		"""Returns a list of bookmarks, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		return self._new_element(self.xa_scel.bookmarks(), XABookMarkableBookmarkList, filter)




class XABookMarkableDocument:
	"""A document.

	.. versionadded:: 0.1.0
	"""

	@property
	def name(self) -> 'str':
		"""The document's name.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.name()

	@property
	def modified(self) -> 'bool':
		"""Has the document been modified since the last save?

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.modified()

	@property
	def file(self) -> 'XABase.XAURL':
		"""The document's location on disk.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.file()




class XABookMarkableWindow:
	"""A window.

	.. versionadded:: 0.1.0
	"""

	@property
	def name(self) -> 'str':
		"""The full title of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.name()

	@property
	def id(self) -> 'int':
		"""The unique identifier of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.id()

	@property
	def index(self) -> 'int':
		"""The index of the window, ordered front to back.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.index()

	@property
	def bounds(self) -> 'tuple[int,int,int,int]':
		"""The bounding rectangle of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.bounds()

	@property
	def closeable(self) -> 'bool':
		"""Whether the window has a close box.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.closeable()

	@property
	def minimizable(self) -> 'bool':
		"""Whether the window can be minimized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.minimizable()

	@property
	def minimized(self) -> 'bool':
		"""Whether the window is currently minimized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.minimized()

	@property
	def resizable(self) -> 'bool':
		"""Whether the window can be resized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.resizable()

	@property
	def visible(self) -> 'bool':
		"""Whether the window is currently visible.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.visible()

	@property
	def zoomable(self) -> 'bool':
		"""Whether the window can be zoomed.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.zoomable()

	@property
	def zoomed(self) -> 'bool':
		"""Whether the window is currently zoomed.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.zoomed()

	@property
	def document(self) -> 'XABookMarkableDocument':
		"""The document whose contents are being displayed in the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.document()



class XABookMarkablePanelList(XABase.XAList):
	"""A wrapper around lists of panels that employs fast enumeration techniques.

	All properties of panels can be called as methods on the wrapped list, returning a list containing each panel's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkablePanel, filter)

	def name(self) -> list['str']:
		"""The full title of the window.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("name"))

	def id(self) -> list['int']:
		"""The unique identifier of the window.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("id"))

	def index(self) -> list['int']:
		"""The index of the window, ordered front to back.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("index"))

	def bounds(self) -> list['tuple[int,int,int,int]']:
		"""The bounding rectangle of the window.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("bounds"))

	def closeable(self) -> list['bool']:
		"""Whether the window has a close box.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("closeable"))

	def minimizable(self) -> list['bool']:
		"""Whether the window can be minimized.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("minimizable"))

	def minimized(self) -> list['bool']:
		"""Whether the window is currently minimized.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("minimized"))

	def resizable(self) -> list['bool']:
		"""Whether the window can be resized.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("resizable"))

	def visible(self) -> list['bool']:
		"""Whether the window is currently visible.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("visible"))

	def zoomable(self) -> list['bool']:
		"""Whether the window can be zoomed.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("zoomable"))

	def zoomed(self) -> list['bool']:
		"""Whether the window is currently zoomed.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("zoomed"))

	def by_name(self, name) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose name matches the given name.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("name", name)

	def by_id(self, id) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose id matches the given id.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("id", id)

	def by_index(self, index) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose index matches the given index.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("index", index)

	def by_bounds(self, bounds) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose bounds matches the given bounds.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("bounds", bounds)

	def by_closeable(self, closeable) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose closeable matches the given closeable.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("closeable", closeable)

	def by_minimizable(self, minimizable) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose minimizable matches the given minimizable.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("minimizable", minimizable)

	def by_minimized(self, minimized) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose minimized matches the given minimized.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("minimized", minimized)

	def by_resizable(self, resizable) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose resizable matches the given resizable.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("resizable", resizable)

	def by_visible(self, visible) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose visible matches the given visible.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("visible", visible)

	def by_zoomable(self, zoomable) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose zoomable matches the given zoomable.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("zoomable", zoomable)

	def by_zoomed(self, zoomed) -> 'XABookMarkablePanel':
		"""Retrieves the A Panel.whose zoomed matches the given zoomed.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("zoomed", zoomed)

class XABookMarkablePanel(XABase.XAObject):
	"""A Panel.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties):
		super().__init__(properties)

	@property
	def name(self) -> 'str':
		"""The full title of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.name()

	@property
	def id(self) -> 'int':
		"""The unique identifier of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.id()

	@property
	def index(self) -> 'int':
		"""The index of the window, ordered front to back.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.index()

	@property
	def bounds(self) -> 'tuple[int,int,int,int]':
		"""The bounding rectangle of the window.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.bounds()

	@property
	def closeable(self) -> 'bool':
		"""Whether the window has a close box.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.closeable()

	@property
	def minimizable(self) -> 'bool':
		"""Whether the window can be minimized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.minimizable()

	@property
	def minimized(self) -> 'bool':
		"""Whether the window is currently minimized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.minimized()

	@property
	def resizable(self) -> 'bool':
		"""Whether the window can be resized.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.resizable()

	@property
	def visible(self) -> 'bool':
		"""Whether the window is currently visible.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.visible()

	@property
	def zoomable(self) -> 'bool':
		"""Whether the window can be zoomed.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.zoomable()

	@property
	def zoomed(self) -> 'bool':
		"""Whether the window is currently zoomed.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.zoomed()



class XABookMarkableRichTextList:
	"""A wrapper around lists of XABookMarkablerich texts that employs fast enumeration techniques.

	All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableRichText, filter)

	def color(self) -> list['XABookMarkableColor']:
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("color"))

	def font(self) -> list['str']:
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("font"))

	def size(self) -> list['int']:
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("size"))

	def by_color(self, color) -> 'XABookMarkableRichText':
		"""Retrieves the Rich (styled) textwhose color matches the given color.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("color", color)

	def by_font(self, font) -> 'XABookMarkableRichText':
		"""Retrieves the Rich (styled) textwhose font matches the given font.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("font", font)

	def by_size(self, size) -> 'XABookMarkableRichText':
		"""Retrieves the Rich (styled) textwhose size matches the given size.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("size", size)

class XABookMarkableRichText:
	"""Rich (styled) text

	.. versionadded:: 0.1.0
	"""

	@property
	def color(self) -> 'XABookMarkableColor':
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.color()

	@property
	def font(self) -> 'str':
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.font()

	@property
	def size(self) -> 'int':
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.size()

	def characters(self, filter: Union[dict, None] = None) -> 'XABookMarkableCharacter':
		"""Returns a list of characters, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.characters(), XABookMarkableCharacterList, filter)

	def paragraphs(self, filter: Union[dict, None] = None) -> 'XABookMarkableParagraph':
		"""Returns a list of paragraphs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.paragraphs(), XABookMarkableParagraphList, filter)

	def words(self, filter: Union[dict, None] = None) -> 'XABookMarkableWord':
		"""Returns a list of words, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.words(), XABookMarkableWordList, filter)

	def attribute_runs(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttributeRun':
		"""Returns a list of attribute_runs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attribute_runs(), XABookMarkableAttributeRunList, filter)

	def attachments(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttachment':
		"""Returns a list of attachments, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attachments(), XABookMarkableAttachmentList, filter)



class XABookMarkableCharacterList:
	"""A wrapper around lists of XABookMarkablecharacters that employs fast enumeration techniques.

	All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableCharacter, filter)

	def color(self) -> list['XABookMarkableColor']:
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("color"))

	def font(self) -> list['str']:
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("font"))

	def size(self) -> list['int']:
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("size"))

	def by_color(self, color) -> 'XABookMarkableCharacter':
		"""Retrieves the This subdivides the text into characters.whose color matches the given color.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("color", color)

	def by_font(self, font) -> 'XABookMarkableCharacter':
		"""Retrieves the This subdivides the text into characters.whose font matches the given font.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("font", font)

	def by_size(self, size) -> 'XABookMarkableCharacter':
		"""Retrieves the This subdivides the text into characters.whose size matches the given size.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("size", size)

class XABookMarkableCharacter:
	"""This subdivides the text into characters.

	.. versionadded:: 0.1.0
	"""

	@property
	def color(self) -> 'XABookMarkableColor':
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.color()

	@property
	def font(self) -> 'str':
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.font()

	@property
	def size(self) -> 'int':
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.size()

	def characters(self, filter: Union[dict, None] = None) -> 'XABookMarkableCharacter':
		"""Returns a list of characters, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.characters(), XABookMarkableCharacterList, filter)

	def paragraphs(self, filter: Union[dict, None] = None) -> 'XABookMarkableParagraph':
		"""Returns a list of paragraphs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.paragraphs(), XABookMarkableParagraphList, filter)

	def words(self, filter: Union[dict, None] = None) -> 'XABookMarkableWord':
		"""Returns a list of words, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.words(), XABookMarkableWordList, filter)

	def attribute_runs(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttributeRun':
		"""Returns a list of attribute_runs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attribute_runs(), XABookMarkableAttributeRunList, filter)

	def attachments(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttachment':
		"""Returns a list of attachments, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attachments(), XABookMarkableAttachmentList, filter)



class XABookMarkableParagraphList:
	"""A wrapper around lists of XABookMarkableparagraphs that employs fast enumeration techniques.

	All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableParagraph, filter)

	def color(self) -> list['XABookMarkableColor']:
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("color"))

	def font(self) -> list['str']:
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("font"))

	def size(self) -> list['int']:
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("size"))

	def by_color(self, color) -> 'XABookMarkableParagraph':
		"""Retrieves the This subdivides the text into paragraphs.whose color matches the given color.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("color", color)

	def by_font(self, font) -> 'XABookMarkableParagraph':
		"""Retrieves the This subdivides the text into paragraphs.whose font matches the given font.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("font", font)

	def by_size(self, size) -> 'XABookMarkableParagraph':
		"""Retrieves the This subdivides the text into paragraphs.whose size matches the given size.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("size", size)

class XABookMarkableParagraph:
	"""This subdivides the text into paragraphs.

	.. versionadded:: 0.1.0
	"""

	@property
	def color(self) -> 'XABookMarkableColor':
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.color()

	@property
	def font(self) -> 'str':
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.font()

	@property
	def size(self) -> 'int':
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.size()

	def characters(self, filter: Union[dict, None] = None) -> 'XABookMarkableCharacter':
		"""Returns a list of characters, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.characters(), XABookMarkableCharacterList, filter)

	def paragraphs(self, filter: Union[dict, None] = None) -> 'XABookMarkableParagraph':
		"""Returns a list of paragraphs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.paragraphs(), XABookMarkableParagraphList, filter)

	def words(self, filter: Union[dict, None] = None) -> 'XABookMarkableWord':
		"""Returns a list of words, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.words(), XABookMarkableWordList, filter)

	def attribute_runs(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttributeRun':
		"""Returns a list of attribute_runs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attribute_runs(), XABookMarkableAttributeRunList, filter)

	def attachments(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttachment':
		"""Returns a list of attachments, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attachments(), XABookMarkableAttachmentList, filter)



class XABookMarkableWordList:
	"""A wrapper around lists of XABookMarkablewords that employs fast enumeration techniques.

	All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableWord, filter)

	def color(self) -> list['XABookMarkableColor']:
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("color"))

	def font(self) -> list['str']:
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("font"))

	def size(self) -> list['int']:
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("size"))

	def by_color(self, color) -> 'XABookMarkableWord':
		"""Retrieves the This subdivides the text into words.whose color matches the given color.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("color", color)

	def by_font(self, font) -> 'XABookMarkableWord':
		"""Retrieves the This subdivides the text into words.whose font matches the given font.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("font", font)

	def by_size(self, size) -> 'XABookMarkableWord':
		"""Retrieves the This subdivides the text into words.whose size matches the given size.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("size", size)

class XABookMarkableWord:
	"""This subdivides the text into words.

	.. versionadded:: 0.1.0
	"""

	@property
	def color(self) -> 'XABookMarkableColor':
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.color()

	@property
	def font(self) -> 'str':
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.font()

	@property
	def size(self) -> 'int':
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.size()

	def characters(self, filter: Union[dict, None] = None) -> 'XABookMarkableCharacter':
		"""Returns a list of characters, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.characters(), XABookMarkableCharacterList, filter)

	def paragraphs(self, filter: Union[dict, None] = None) -> 'XABookMarkableParagraph':
		"""Returns a list of paragraphs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.paragraphs(), XABookMarkableParagraphList, filter)

	def words(self, filter: Union[dict, None] = None) -> 'XABookMarkableWord':
		"""Returns a list of words, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.words(), XABookMarkableWordList, filter)

	def attribute_runs(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttributeRun':
		"""Returns a list of attribute_runs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attribute_runs(), XABookMarkableAttributeRunList, filter)

	def attachments(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttachment':
		"""Returns a list of attachments, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attachments(), XABookMarkableAttachmentList, filter)



class XABookMarkableAttributeRunList:
	"""A wrapper around lists of XABookMarkableattribute runs that employs fast enumeration techniques.

	All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableAttributeRun, filter)

	def color(self) -> list['XABookMarkableColor']:
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("color"))

	def font(self) -> list['str']:
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("font"))

	def size(self) -> list['int']:
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("size"))

	def by_color(self, color) -> 'XABookMarkableAttributeRun':
		"""Retrieves the This subdivides the text into chunks that all have the same attributes.whose color matches the given color.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("color", color)

	def by_font(self, font) -> 'XABookMarkableAttributeRun':
		"""Retrieves the This subdivides the text into chunks that all have the same attributes.whose font matches the given font.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("font", font)

	def by_size(self, size) -> 'XABookMarkableAttributeRun':
		"""Retrieves the This subdivides the text into chunks that all have the same attributes.whose size matches the given size.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("size", size)

class XABookMarkableAttributeRun:
	"""This subdivides the text into chunks that all have the same attributes.

	.. versionadded:: 0.1.0
	"""

	@property
	def color(self) -> 'XABookMarkableColor':
		"""The color of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.color()

	@property
	def font(self) -> 'str':
		"""The name of the font of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.font()

	@property
	def size(self) -> 'int':
		"""The size in points of the first character.

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.size()

	def characters(self, filter: Union[dict, None] = None) -> 'XABookMarkableCharacter':
		"""Returns a list of characters, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.characters(), XABookMarkableCharacterList, filter)

	def paragraphs(self, filter: Union[dict, None] = None) -> 'XABookMarkableParagraph':
		"""Returns a list of paragraphs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.paragraphs(), XABookMarkableParagraphList, filter)

	def words(self, filter: Union[dict, None] = None) -> 'XABookMarkableWord':
		"""Returns a list of words, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.words(), XABookMarkableWordList, filter)

	def attribute_runs(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttributeRun':
		"""Returns a list of attribute_runs, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attribute_runs(), XABookMarkableAttributeRunList, filter)

	def attachments(self, filter: Union[dict, None] = None) -> 'XABookMarkableAttachment':
		"""Returns a list of attachments, as PyXA objects, matching the given filter.

		.. versionadded:: 0.1.0
		"""
		self._new_element(self.xa_elem.attachments(), XABookMarkableAttachmentList, filter)



class XABookMarkableAttachmentList:
	"""A wrapper around lists of attachments that employs fast enumeration techniques.

	All properties of attachments can be called as methods on the wrapped list, returning a list containing each attachments's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableAttachment, filter)

	def file_name(self) -> list['str']:
		"""The path to the file for the attachment

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("file_name"))

	def by_file_name(self, file_name) -> 'XABookMarkableAttachment':
		"""Retrieves the Represents an inline text attachment. This class is used mainly for make commands.whose file_name matches the given file_name.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("file_name", file_name)

class XABookMarkableAttachment:
	"""Represents an inline text attachment. This class is used mainly for make commands.

	.. versionadded:: 0.1.0
	"""

	@property
	def file_name(self) -> 'str':
		"""The path to the file for the attachment

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.file_name()



class XABookMarkableBookmarkList(XABase.XAList):
	"""A wrapper around lists of books that employs fast enumeration techniques.

	All properties of bookmarks can be called as methods on the wrapped list, returning a list containing each bookmark's value for the property.

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties: dict, filter: Union[dict, None] = None):
		super().__init__(properties, XABookMarkableBookmark, filter)

	def name(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("name"))

	def url(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("url"))

	def open_with(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("open_with"))

	def tags(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("tags"))

	def associations(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("associations"))

	def due_date(self) -> list['XABookMarkableDate']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("due_date"))

	def comments(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("comments"))

	def id(self) -> list['str']:
		"""the record ID

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("id"))

	def alternative_id(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("alternative_id"))

	def alternative_title(self) -> list['str']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("alternative_title"))

	def usage_count(self) -> list['int']:
		"""

		.. versionadded:: 0.1.0
		"""
		return list(self.xa_elem.arrayByApplyingSelector_("usage_count"))

	def by_name(self, name) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose name matches the given name.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("name", name)

	def by_url(self, url) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose url matches the given url.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("url", url)

	def by_open_with(self, open_with) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose open_with matches the given open_with.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("open_with", open_with)

	def by_tags(self, tags) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose tags matches the given tags.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("tags", tags)

	def by_associations(self, associations) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose associations matches the given associations.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("associations", associations)

	def by_due_date(self, due_date) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose due_date matches the given due_date.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("due_date", due_date)

	def by_comments(self, comments) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose comments matches the given comments.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("comments", comments)

	def by_id(self, id) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose id matches the given id.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("id", id)

	def by_alternative_id(self, alternative_id) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose alternative_id matches the given alternative_id.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("alternative_id", alternative_id)

	def by_alternative_title(self, alternative_title) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose alternative_title matches the given alternative_title.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("alternative_title", alternative_title)

	def by_usage_count(self, usage_count) -> 'XABookMarkableBookmark':
		"""Retrieves the Bookmarkwhose usage_count matches the given usage_count.

		.. versionadded:: 0.1.0
		"""
		return self.by_property("usage_count", usage_count)

class XABookMarkableBookmark(XABase.XAObject):
	"""Bookmark

	.. versionadded:: 0.1.0
	"""
	def __init__(self, properties):
		super().__init__(properties)

	@property
	def name(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.name()

	@property
	def url(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.url()

	@property
	def open_with(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.open_with()

	@property
	def tags(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.tags()

	@property
	def associations(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.associations()

	@property
	def due_date(self) -> 'XABookMarkableDate':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.due_date()

	@property
	def comments(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.comments()

	@property
	def id(self) -> 'str':
		"""the record ID

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.id()

	@property
	def alternative_id(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.alternative_id()

	@property
	def alternative_title(self) -> 'str':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.alternative_title()

	@property
	def usage_count(self) -> 'int':
		"""

		.. versionadded:: 0.1.0
		"""
		return self.xa_elem.usage_count()