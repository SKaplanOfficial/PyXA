""".. versionadded:: 0.0.2

Control the macOS Contacts application using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Union

import AppKit

from PyXA import XABase, XAEvents
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath


class XAContactsApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Contacts.app.

    .. seealso:: :class:`XAContactsGroup`, :class:`XAContactsPerson`

    .. versionadded:: 0.0.2
    """
    class Format(Enum):
        """Format options when saving documents.
        """
        ARCHIVE = XABase.OSType('abbu') #: The native Address Book file format

    class ServiceType(Enum):
        """Service types for social media accounts.
        """
        AIM         = XABase.OSType('az85')
        GADU_GADU   = XABase.OSType('az86')
        GOOGLE_TALK = XABase.OSType('az87')
        ICQ         = XABase.OSType('az88')
        JABBER      = XABase.OSType('az89')
        MSN         = XABase.OSType('az90')
        QQ          = XABase.OSType('az91')
        SKYPE       = XABase.OSType('az92')
        YAHOO       = XABase.OSType('az93')
        FACEBOOK    = XABase.OSType('az94')

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Contacts is the frontmost application.
        """
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property('frontmost', frontmost)

    @property
    def version(self) -> str:
        """The version of Contacts.app.
        """
        return self.xa_scel.version()

    @property
    def my_card(self) -> 'XAContactsPerson':
        """The user's contact card.
        """
        return self._new_element(self.xa_scel.myCard(), XAContactsPerson)

    @my_card.setter
    def my_card(self, my_card: 'XAContactsPerson'):
        self.set_property('myCard', my_card)

    @property
    def unsaved(self) -> bool:
        """Whether there are any unsaved changed.
        """
        return self.xa_scel.unsaved()

    @property
    def selection(self) -> 'XAContactsPersonList':
        """The currently selected entries.
        """
        return self._new_element(self.xa_scel.selection(), XAContactsPersonList)

    @selection.setter
    def selection(self, selection: Union['XAContactsPersonList', list['XAContactsPerson']]):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property("selection", selection)
        else:
            self.set_property('selection', selection.xa_elem)

    @property
    def default_country_code(self) -> str:
        """The default country code for addresses.
        """
        return self.xa_scel.defaultCountryCode().get() or ""

    def open(self, file_path: str):
        """Opens a document and prompts whether to import the contact(s) contained in the document.

        :param file_path: The path to the file to import
        :type file_path: str

        .. versionadded:: 0.0.7
        """
        self.xa_scel.open_(file_path)

    def save(self):
        """Saves all changes to the address book.

        .. versionadded:: 0.0.7
        """
        self.xa_scel.save()

    def documents(self, filter: Union[dict, None] = None) -> 'XAContactsDocumentList':
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAContactsDocumentList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.documents(), XAContactsDocumentList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAContactsGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAContactsGroupList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Contacts")
        >>> print(app.groups())
        <<class 'PyXA.apps.Contacts.XAContactsGroupList'>['Example Group 1', 'Example Group 2', ...]>

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.groups(), XAContactsGroupList, filter)

    def people(self, filter: Union[dict, None] = None) -> 'XAContactsPersonList':
        """Returns a list of people, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned people will have, or None
        :type filter: Union[dict, None]
        :return: The list of people
        :rtype: XAContactsPersonList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Contacts")
        >>> print(app.people())
        <<class 'PyXA.apps.Contacts.XAContactsPersonList'>['Example Contact 1', 'Example Contact 2', ...]>

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_scel.people(), XAContactsPersonList, filter)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Add a URL to a contact

        >>> import PyXA
        >>> app = PyXA.Application("Contacts")
        >>> contact = app.people().by_name("Example Contact")
        >>> new_url = app.make("url", {"label": "Google", "value": "www.google.com"})
        >>> contact.urls().push(new_url)
        >>> app.save()

        .. versionadded:: 0.0.7
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "document":
            return self._new_element(obj, XAContactsDocument)
        elif specifier == "person":
            return self._new_element(obj, XAContactsPerson)
        elif specifier == "group":
            return self._new_element(obj, XAContactsGroup)
        elif specifier == "url":
            return self._new_element(obj, XAContactsURL)




class XAContactsWindow(XABaseScriptable.XASBWindow):
    """A window of Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> 'XAContactsDocument':
        """The documents currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XAContactsDocument)




class XAContactsDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAContactsDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAURL(x) for x in ls]

    def by_name(self, name: str) -> Union['XAContactsDocument', None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union['XAContactsDocument', None]:
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAURL) -> Union['XAContactsDocument', None]:
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAContactsDocument(XABase.XAObject):
    """A document in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the document.
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since it was last saved.
        """
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAURL:
        """The location of the document of the disk, if one exists.
        """
        return XABase.XAURL(self.xa_elem.file())




class XAContactsAddressList(XABase.XAList):
    """A wrapper around lists of addresses that employs fast enumeration techniques.

    All properties of addresses can be called as methods on the wrapped list, returning a list containing each address' value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAContactsAddress, filter)

    def city(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("city") or [])

    def formatted_address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("formattedAddress") or [])

    def street(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("street") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def zip(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("zip") or [])

    def country(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("country") or [])

    def label(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("label") or [])

    def country_code(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("countryCode") or [])

    def state(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("state") or [])

    def by_city(self, city: str) -> Union['XAContactsAddress', None]:
        return self.by_property("city", city)

    def by_formatted_address(self, formatted_address: str) -> Union['XAContactsAddress', None]:
        return self.by_property("formattedAddress", formatted_address)

    def by_street(self, street: str) -> Union['XAContactsAddress', None]:
        return self.by_property("street", street)

    def by_id(self, id: str) -> Union['XAContactsAddress', None]:
        return self.by_property("id", id)

    def by_zip(self, zip: str) -> Union['XAContactsAddress', None]:
        return self.by_property("zip", zip)

    def by_country(self, country: str) -> Union['XAContactsAddress', None]:
        return self.by_property("country", country)

    def by_label(self, label: str) -> Union['XAContactsAddress', None]:
        return self.by_property("label", label)

    def by_country_code(self, country_code: str) -> Union['XAContactsAddress', None]:
        return self.by_property("countryCode", country_code)

    def by_state(self, state: str) -> Union['XAContactsAddress', None]:
        return self.by_property("state", state)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.label()) + ">"

class XAContactsAddress(XABase.XAObject):
    """An address associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def city(self) -> str:
        """The city part of the address.
        """
        return self.xa_elem.city()

    @city.setter
    def city(self, city: str):
        self.set_property('city', city)

    @property
    def formatted_address(self) -> str:
        """The formatted string for the address.
        """
        return self.xa_elem.formattedAddress()

    @property
    def street(self) -> str:
        """The street part of the address.
        """
        return self.xa_elem.street()

    @street.setter
    def street(self, street: str):
        self.set_property('street', street)

    @property
    def id(self) -> str:
        """The unique identifier for the address.
        """
        return self.xa_elem.id()

    @property
    def zip(self) -> str:
        """The zip code or postal code part of the address.
        """
        return self.xa_elem.zip()

    @zip.setter
    def zip(self, zip: str):
        self.set_property('zip', zip)

    @property
    def country(self) -> str:
        """The country part of the address.
        """
        return self.xa_elem.country()

    @country.setter
    def country(self, country: str):
        self.set_property('country', country)

    @property
    def label(self) -> str:
        """The label associated with the address.
        """
        return self.xa_elem.label()

    @label.setter
    def label(self, label: str):
        self.set_property('label', label)

    @property
    def country_code(self) -> str:
        """The country code part of the address.
        """
        return self.xa_elem.countryCode()

    @country_code.setter
    def country_code(self, country_code: str):
        self.set_property('countryCode', country_code)

    @property
    def state(self) -> str:
        """The state, province, or region part of the address.
        """
        return self.xa_elem.state()

    @state.setter
    def state(self, state: str):
        self.set_property('state', state)




class XAContactsContactInfoList(XABase.XAList):
    """A wrapper around lists of contact information entries that employs fast enumeration techniques.

    All properties of contact information entries can be called as methods on the wrapped list, returning a list containing each entry's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAContactsContactInfo
        super().__init__(properties, obj_class, filter)

    def label(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("label") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def by_label(self, label: str) -> Union['XAContactsContactInfo', None]:
        return self.by_property("label", label)

    def by_value(self, value: Any) -> Union['XAContactsContactInfo', None]:
        return self.by_property("value", value)
    
    def by_id(self, id: str) -> Union['XAContactsContactInfo', None]:
        return self.by_property("id", id)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.label()) + "::" + str(self.value()) + ">"

class XAContactsContactInfo(XABase.XAObject):
    """Contact information associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def label(self) -> str:
        """The label associated with the information entry.
        """
        return self.xa_elem.label()

    @label.setter
    def label(self, label: str):
        self.set_property('label', label)

    @property
    def value(self) -> Union[str, datetime, None]:
        """The value of the information entry.
        """
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Union[str, datetime, None]):
        self.set_property('value', value)

    @property
    def id(self) -> str:
        """The persistent unique identifier for the information entry.
        """
        return self.xa_elem.id()




class XAContactsCustomDateList(XAContactsContactInfoList):
    """A wrapper around lists of contact custom dates that employs fast enumeration techniques.

    All properties of contact custom dates can be called as methods on the wrapped list, returning a list containing each custom date's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsCustomDate)

class XAContactsCustomDate(XAContactsContactInfo):
    """A custom date associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAContactsEmailList(XAContactsContactInfoList):
    """A wrapper around lists of contact email addresses that employs fast enumeration techniques.

    All properties of contact email addresses can be called as methods on the wrapped list, returning a list containing each email address's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsEmail)

class XAContactsEmail(XAContactsContactInfo):
    """A document in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAContactsEntryList(XABase.XAList):
    """A wrapper around lists of contact entries that employs fast enumeration techniques.

    All properties of contact entries can be called as methods on the wrapped list, returning a list containing each entry's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None, obj_class = None):
        if obj_class is None:
            obj_class = XAContactsEntry
        super().__init__(properties, obj_class, filter)

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def creation_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def by_modification_date(self, modification_date: datetime) -> Union['XAContactsEntry', None]:
        return self.by_property("modificationDate", modification_date)

    def by_creation_date(self, creation_date: datetime) -> Union['XAContactsEntry', None]:
        return self.by_property("creationDate", creation_date)

    def by_id(self, id: str) -> Union['XAContactsEntry', None]:
        return self.by_property("id", id)

    def by_selected(self, selected: bool) -> Union['XAContactsEntry', None]:
        return self.by_property("selected", selected)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"

class XAContactsEntry(XABase.XAObject):
    """An entry in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def modification_date(self) -> datetime:
        """The last modification date of the contact entry.
        """
        return self.xa_elem.modificationDate()

    @property
    def creation_date(self) -> datetime:
        """The creation date of the contact entry.
        """
        return self.xa_elem.creationDate()

    @property
    def id(self) -> str:
        """The unique persistent identifier for the entry.
        """
        return self.xa_elem.id()

    @property
    def selected(self) -> bool:
        """Whether the entry is selected.
        """
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property('selected', selected)

    def add_to(self, parent: XABase.XAObject) -> 'XAContactsPerson':
        """Adds a child object to an entry.

        :param parent: The entry to add this entry as a child to
        :type parent: XABase.XAObject

        :Example 1: Add a contact to a group

        >>> import PyXA
        >>> app = PyXA.Application("Contacts")
        >>> group = app.groups().by_name("Example Group")
        >>> app.people()[0].add_to(group)
        >>> app.save()

        .. versionadded:: 0.0.7
        """
        person = self.xa_elem.addTo_(parent.xa_elem)
        return self._new_element(person, XAContactsPerson)

    def remove_from(self, elem) -> 'XAContactsPerson':
        """Removes a child object from an entry.

        :param parent: The entry to removes this entry as a child from
        :type parent: XABase.XAObject

        :Example 1: Remove a contact from a group

        >>> import PyXA
        >>> app = PyXA.Application("Contacts")
        >>> group = app.groups().by_name("Example Group")
        >>> app.people()[0].add_to(group)
        >>> app.people()[0].remove_from(group)
        >>> app.save()

        .. versionadded:: 0.0.7
        """
        person = self.xa_elem.removeFrom_(elem.xa_elem)
        return self._new_element(person, XAContactsPerson)

    def delete(self):
        """Deletes the entry. Only entries creates in the current session can be deleted.

        .. versionadded:: 0.0.7
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id) + ">"




class XAContactsGroupList(XAContactsEntryList):
    """A wrapper around lists of contact groups that employs fast enumeration techniques.

    All properties of contact groups can be called as methods on the wrapped list, returning a list containing each group's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsGroup)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_name(self, name: str) -> Union['XAContactsGroup', None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAContactsGroup(XAContactsEntry):
    """A group in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the group.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    def groups(self, filter: Union[dict, None] = None) -> 'XAContactsGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAContactsGroupList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.groups(), XAContactsGroupList, filter)

    def people(self, filter: Union[dict, None] = None) -> 'XAContactsPersonList':
        """Returns a list of people, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned people will have, or None
        :type filter: Union[dict, None]
        :return: The list of people
        :rtype: XAContactsPersonList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.people(), XAContactsPersonList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAContactsInstantMessageList(XAContactsContactInfoList):
    """A wrapper around lists of IM addresses that employs fast enumeration techniques.

    All properties of IM addresses can be called as methods on the wrapped list, returning a list containing each IM address's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsInstantMessage)

    def service_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("serviceName") or [])

    def service_type(self) -> list[XAContactsApplication.ServiceType]:
        ls = self.xa_elem.arrayByApplyingSelector_("serviceType") or []
        return [XAContactsApplication.ServiceType(XABase.OSType(x.stringValue())) for x in ls]

    def user_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userName") or [])

    def by_service_name(self, service_name: str) -> Union['XAContactsInstantMessage', None]:
        return self.by_property("serviceName", service_name)

    def by_service_type(self, service_type: XAContactsApplication.ServiceType) -> Union['XAContactsInstantMessage', None]:
        event = XAEvents.event_from_int(service_type.value)
        return self.by_property("serviceType", event)

    def by_user_name(self, user_name: str) -> Union['XAContactsInstantMessage', None]:
        return self.by_property("userName", user_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.service_name()) + ">"

class XAContactsInstantMessage(XAContactsContactInfo):
    """An instant message (IM) address associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def service_name(self) -> str:
        """The service name of the IM address.
        """
        return self.xa_elem.serviceName().get()

    @property
    def service_type(self) -> XAContactsApplication.ServiceType:
        """The service type of the IM address.
        """
        return XAContactsApplication.ServiceType(self.xa_elem.serviceType())

    @service_type.setter
    def service_type(self, service_type: XAContactsApplication.ServiceType):
        self.set_property('serviceType', service_type.value)

    @property
    def user_name(self) -> str:
        """The user name of the the IM address.
        """
        return self.xa_elem.userName().get()

    @user_name.setter
    def user_name(self, user_name: str):
        self.set_property('userName', user_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.service_name) + ">"




class XAContactsPersonList(XAContactsEntryList):
    """A wrapper around lists of people that employs fast enumeration techniques.

    All properties of people can be called as methods on the wrapped list, returning a list containing each IM person's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsPerson)

    def nickname(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("nickname") or [])

    def organization(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("organization") or [])

    def maiden_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("maidenName") or [])

    def suffix(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("suffix") or [])

    def vcard(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("vcard") or [])

    def home_page(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("homePage") or [])

    def birth_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("birthdate") or [])

    def phonetic_last_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("phoneticLastName") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def phonetic_middle_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("phoneticMiddleName") or [])

    def department(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("department") or [])

    def image(self) -> list[XABase.XAImage]:
        ls = self.xa_elem.arrayByApplyingSelector_("image") or []
        return [XABase.XAImage(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def note(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("note") or [])

    def company(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("company") or [])

    def middle_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("middleName") or [])

    def phonetic_first_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("phoneticFirstName") or [])

    def job_title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("jobTitle") or [])

    def last_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("lastName") or [])

    def first_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("firstName") or [])

    def by_nickname(self, nickname: str) -> Union['XAContactsPerson', None]:
        return self.by_property("nickname", nickname)

    def by_organization(self, organization: str) -> Union['XAContactsPerson', None]:
        return self.by_property("organization", organization)

    def by_maiden_name(self, maiden_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("maidenName", maiden_name)

    def by_suffix(self, suffix: str) -> Union['XAContactsPerson', None]:
        return self.by_property("suffix", suffix)

    def by_vcard(self, vcard: str) -> Union['XAContactsPerson', None]:
        return self.by_property("vcard", vcard)

    def by_home_page(self, home_page: str) -> Union['XAContactsPerson', None]:
        # TODO - URL?
        return self.by_property("homePage", home_page)

    def by_birth_date(self, birth_date: datetime) -> Union['XAContactsPerson', None]:
        return self.by_property("birthDate", birth_date)

    def by_phonetic_last_name(self, phonetic_last_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("phoneticLastName", phonetic_last_name)

    def by_title(self, title: str) -> Union['XAContactsPerson', None]:
        return self.by_property("title", title)

    def by_phonetic_middle_name(self, phonetic_middle_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("phoneticMiddleName", phonetic_middle_name)

    def by_department(self, department: str) -> Union['XAContactsPerson', None]:
        return self.by_property("department", department)

    def by_image(self, image: XABase.XAImage) -> Union['XAContactsPerson', None]:
        return self.by_property("image", image.xa_elem)

    def by_name(self, name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("name", name)

    def by_note(self, note: str) -> Union['XAContactsPerson', None]:
        return self.by_property("note", note)

    def by_company(self, company: bool) -> Union['XAContactsPerson', None]:
        return self.by_property("company", company)

    def by_middle_name(self, middle_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("middleName", middle_name)

    def by_phonetic_first_name(self, phonetic_first_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("phoneticFirstName", phonetic_first_name)

    def by_job_title(self, job_title: str) -> Union['XAContactsPerson', None]:
        return self.by_property("jobTitle", job_title)

    def by_last_name(self, last_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("lastName", last_name)

    def by_first_name(self, first_name: str) -> Union['XAContactsPerson', None]:
        return self.by_property("firstName", first_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"

class XAContactsPerson(XAContactsEntry):
    """A person in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def nickname(self) -> str:
        """The nickname of the person.
        """
        return self.xa_elem.nickname().get()

    @nickname.setter
    def nickname(self, nickname: str):
        self.set_property('nickname', nickname)

    @property
    def organization(self) -> str:
        """The organization that employs the person.
        """
        return self.xa_elem.organization().get()

    @organization.setter
    def organization(self, organization: str):
        self.set_property('organization', organization)

    @property
    def maiden_name(self) -> str:
        """The maiden name of the person.
        """
        return self.xa_elem.maidenName().get()

    @maiden_name.setter
    def maiden_name(self, maiden_name: str):
        self.set_property('maidenName', maiden_name)

    @property
    def suffix(self) -> str:
        """The suffix of the person's name.
        """
        return self.xa_elem.suffix().get()

    @suffix.setter
    def suffix(self, suffix: str):
        self.set_property('suffix', suffix)

    @property
    def vcard(self) -> str:
        """The person's information in vCard format.
        """
        return self.xa_elem.vcard().get()

    @property
    def home_page(self) -> str:
        """The homepage of the person.
        """
        return self.xa_elem.homePage().get()

    @home_page.setter
    def home_page(self, home_page: str):
        self.set_property('homePage', home_page)

    @property
    def birth_date(self) -> datetime:
        """The birthdate of the person.
        """
        return self.xa_elem.birthDate().get()

    @birth_date.setter
    def birth_date(self, birth_date: datetime):
        self.set_property('birthDate', birth_date)

    @property
    def phonetic_last_name(self) -> str:
        """The phonetic version of the person's last name.
        """
        return self.xa_elem.phoneticLastName().get()

    @phonetic_last_name.setter
    def phonetic_last_name(self, phonetic_last_name: str):
        self.set_property('phoneticLastName', phonetic_last_name)

    @property
    def title(self) -> str:
        """The title of the person.
        """
        return self.xa_elem.title().get()

    @title.setter
    def title(self, title: str):
        self.set_property('title', title)

    @property
    def phonetic_middle_name(self) -> str:
        """The phonetic version of the person's middle name.
        """
        return self.xa_elem.phoneticMiddleNamne().get()

    @phonetic_middle_name.setter
    def phonetic_middle_name(self, phonetic_middle_name: str):
        self.set_property('phoneticMiddleName', phonetic_middle_name)

    @property
    def department(self) -> str:
        """The department that the person works for.
        """
        return self.xa_elem.department().get()

    @department.setter
    def department(self, department: str):
        self.set_property('department', department)

    @property
    def image(self) -> XABase.XAImage:
        """The image for the person.
        """
        return XABase.XAImage(self.xa_elem.image().get())

    @image.setter
    def image(self, image: XABase.XAImage):
        self.set_property('image', image.xa_elem)

    @property
    def name(self) -> str:
        """The first and last name of the person.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property('name', name)

    @property
    def note(self) -> str:
        """The notes for the person.
        """
        return self.xa_elem.note().get()

    @note.setter
    def note(self, note: str):
        self.set_property('note', note)

    @property
    def company(self) -> bool:
        """Whether the record is for a company or not (if not, the record is for a person).
        """
        return self.xa_elem.company().get()

    @company.setter
    def company(self, company: bool):
        self.set_property('company', company)

    @property
    def middle_name(self) -> str:
        """The middle name of the person.
        """
        return self.xa_elem.middleName().get()

    @middle_name.setter
    def middle_name(self, middle_name: str):
        self.set_property('middleName', middle_name)

    @property
    def phonetic_first_name(self) -> str:
        """The phonetic version of the person's first name.
        """
        return self.xa_elem.phoneticFirstName().get()

    @phonetic_first_name.setter
    def phonetic_first_name(self, phonetic_first_name: str):
        self.set_property('phoneticFirstName', phonetic_first_name)

    @property
    def job_title(self) -> str:
        """The job title of the person.
        """
        return self.xa_elem.jobTitle().get()

    @job_title.setter
    def job_title(self, job_title: str):
        self.set_property('jobTitle', job_title)

    @property
    def last_name(self) -> str:
        """The last name of the person.
        """
        return self.xa_elem.lastName().get()

    @last_name.setter
    def last_name(self, last_name: str):
        self.set_property('lastName', last_name)

    @property
    def first_name(self) -> str:
        """The first name of the person.
        """
        return self.xa_elem.firstName().get()

    @first_name.setter
    def first_name(self, first_name: str):
        self.set_property('firstName', first_name)

    def show(self) -> 'XAContactsPerson':
        """Shows the contact card for this contact in Contacts.app.

        :return: The contact person object
        :rtype: XAContactsPerson

        .. versionadded:: 0.0.7
        """
        vcard = self.vcard
        id = vcard[vcard.index("X-ABUID") + 8: vcard.index(":ABPerson")] + "%3AABPerson"
        XABase.XAURL("addressbook://" + id).open()
        return self

    def urls(self, filter: Union[dict, None] = None) -> 'XAContactsURLList':
        """Returns a list of URLs, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned URLs will have, or None
        :type filter: Union[dict, None]
        :return: The list of URLs
        :rtype: XAContactsURLList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.urls(), XAContactsURLList, filter)

    def addresses(self, filter: Union[dict, None] = None) -> 'XAContactsAddressList':
        """Returns a list of addresses, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned addresses will have, or None
        :type filter: Union[dict, None]
        :return: The list of addresses
        :rtype: XAContactsAddressList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.addresses(), XAContactsAddressList, filter)

    def phones(self, filter: Union[dict, None] = None) -> 'XAContactsPhoneList':
        """Returns a list of phone numbers, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned phone numbers will have, or None
        :type filter: Union[dict, None]
        :return: The list of phone numbers
        :rtype: XAContactsPhoneList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.phones(), XAContactsPhoneList, filter)

    def groups(self, filter: Union[dict, None] = None) -> 'XAContactsGroupList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAContactsGroupList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.phones(), XAContactsGroupList, filter)

    def custom_dates(self, filter: Union[dict, None] = None) -> 'XAContactsCustomDateList':
        """Returns a list of groups, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned groups will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XAContactsCustomDateList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.customDates(), XAContactsCustomDateList, filter)

    def instant_messages(self, filter: Union[dict, None] = None) -> 'XAContactsInstantMessageList':
        """Returns a list of IM addresses, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned IM addresses will have, or None
        :type filter: Union[dict, None]
        :return: The list of IM addresses
        :rtype: XAContactsInstantMessageList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.instantMessages(), XAContactsInstantMessageList, filter)

    def social_profiles(self, filter: Union[dict, None] = None) -> 'XAContactsSocialProfileList':
        """Returns a list of social profiles, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned social profiles will have, or None
        :type filter: Union[dict, None]
        :return: The list of social profiles
        :rtype: XAContactsSocialProfileList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.socialProfiles(), XAContactsSocialProfileList, filter)

    def related_names(self, filter: Union[dict, None] = None) -> 'XAContactsRelatedNameList':
        """Returns a list of related names, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned related names will have, or None
        :type filter: Union[dict, None]
        :return: The list of related names
        :rtype: XAContactsRelatedNameList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.relatedNames(), XAContactsRelatedNameList, filter)

    def emails(self, filter: Union[dict, None] = None) -> 'XAContactsEmailList':
        """Returns a list of email addresses, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned email addresses will have, or None
        :type filter: Union[dict, None]
        :return: The list of email addresses
        :rtype: XAContactsEmailList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.emails(), XAContactsEmailList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"




class XAContactsPhoneList(XAContactsContactInfoList):
    """A wrapper around lists of contact phone numbers that employs fast enumeration techniques.

    All properties of contact phone numbers can be called as methods on the wrapped list, returning a list containing each phone numbers's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsPhone)

class XAContactsPhone(XAContactsContactInfo):
    """A phone number associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAContactsRelatedNameList(XAContactsContactInfoList):
    """A wrapper around lists of contact related names that employs fast enumeration techniques.

    All properties of contact related names can be called as methods on the wrapped list, returning a list containing each related names's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsRelatedName)

class XAContactsRelatedName(XAContactsContactInfo):
    """A related name of a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)




class XAContactsSocialProfileList(XABase.XAList):
    """A wrapper around lists of contact social profiles that employs fast enumeration techniques.

    All properties of contact social profiles can be called as methods on the wrapped list, returning a list containing each social profile's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAContactsSocialProfile, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def service_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("serviceName") or [])

    def user_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userName") or [])

    def user_identifier(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("userIdentifier") or [])

    def url(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("URL") or [])

    def by_id(self, id: str) -> Union['XAContactsSocialProfile', None]:
        return self.by_property("id", id)

    def by_service_name(self, service_name: str) -> Union['XAContactsSocialProfile', None]:
        return self.by_property("serviceName", service_name)

    def by_user_name(self, user_name: str) -> Union['XAContactsSocialProfile', None]:
        return self.by_property("userName", user_name)

    def by_user_identifier(self, user_identifier: str) -> Union['XAContactsSocialProfile', None]:
        return self.by_property("userIdentifier", user_identifier)

    def by_url(self, url: str) -> Union['XAContactsSocialProfile', None]:
        return self.by_property("URL", url)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.user_name()) + ">"

class XAContactsSocialProfile(XABaseScriptable.XASBWindow):
    """A social profile associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """A persistent unique identifier for this profile.
        """
        return self.xa_elem.id()

    @property
    def service_name(self) -> str:
        """The service name of this social profile.
        """
        return self.xa_elem.serviceName().get()

    @service_name.setter
    def service_name(self, service_name: str):
        self.set_property('serviceName', service_name)

    @property
    def user_name(self) -> str:
        """The user name used with this social profile.
        """
        return self.xa_elem.userName().get()

    @user_name.setter
    def user_name(self, user_name: str):
        self.set_property('userName', user_name)

    @property
    def user_identifier(self) -> str:
        """A service-specific identifier used with this social profile.
        """
        return self.xa_elem.userIdentifier().get()

    @user_identifier.setter
    def user_identifier(self, user_identifier: str):
        self.set_property('userIdentifier', user_identifier)

    @property
    def url(self) -> str:
        """The URL of the social profile.
        """
        return self.xa_elem.url()

    @url.setter
    def url(self, url: str):
        self.set_property('url', url)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.user_name) + ">"




class XAContactsURLList(XAContactsContactInfoList):
    """A wrapper around lists of contact URLs that employs fast enumeration techniques.

    All properties of contact URLs can be called as methods on the wrapped list, returning a list containing each URL's value for the property.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAContactsURL)

class XAContactsURL(XAContactsContactInfo):
    """A URL associated with a contact in Contacts.app.

    .. versionadded:: 0.0.7
    """
    def __init__(self, properties):
        super().__init__(properties)