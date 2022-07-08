""".. versionadded:: 0.0.2

Control the macOS Contacts application using JXA-like syntax.
"""
from datetime import datetime
from typing import List, Union
from AppKit import NSURL

import Contacts
from AppKit import NSPredicate

from PyXA import XABase
from PyXA import XABaseScriptable


class XAContactsApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Contacts.app.

    .. seealso:: :class:`XAContactGroup`, :class:`XAContactPerson`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = Contacts.CNContactStore.alloc().init()
    
    def selection(self):
        selected_contacts = self.xa_scel.selection()

        elements = []
        for scriptable_contact in selected_contacts:
            contact_predicate = Contacts.CNContact.predicateForContactsWithIdentifiers_([scriptable_contact.id()])
            keys = list(Contacts.CNContact.alloc().init().availableKeys())
            contact = self.xa_cstr.unifiedContactsMatchingPredicate_keysToFetch_error_(contact_predicate, keys, None)[0][0]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": contact,
                "scriptable_element": scriptable_contact,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactPerson(properties))
        return elements

    # Groups
    def groups(self, filter: dict = None) -> List['XAContactGroup']:
        """Returns a list of groups matching the filter.

        .. versionadded:: 0.0.2
        """
        groups_predicate = Contacts.CNGroup.predicateForAllGroups()
        groups = self.xa_cstr.groupsMatchingPredicate_error_(groups_predicate, None)[0]

        if filter is not None:
            groups = XABase.XAPredicate.evaluate_with_dict(groups, filter)

        elements = []
        for group in groups:
            scriptable_group = XABase.XAPredicate.evaluate_with_format(self.xa_scel.groups(), f"( id == '{group.identifier()}' )")[0]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": group,
                "scriptable_element": scriptable_group,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactGroup(properties))
        return elements

    # Contacts
    def new_contact(self, properties: dict) -> 'XAContactPerson':
        """Creates a new contact.


        :param properties: Properties and values to give to the new contact
        :type properties: dict
        :return: The newly created PyXA contact object.
        :rtype: XAContactPerson

        .. versionadded:: 0.0.2
        """
        contact = Contacts.CNMutableContact.alloc().init()

        contact.setGivenName_(properties.get("givenName") or properties.get("given_name"))
        contact.setMiddleName_(properties.get("middleName") or properties.get("middle_name"))
        contact.setFamilyName_(properties.get("familyName") or properties.get("family_name"))
        contact.setNamePrefix_(properties.get("namePrefix") or properties.get("name_prefix"))
        contact.setNameSuffix_(properties.get("nameSuffix") or properties.get("name_suffix"))
        contact.setNickname_(properties.get("nickname"))
        contact.setBirthday_(properties.get("birthday"))
        contact.setJobTitle_(properties.get("jobTitle") or properties.get("job_title"))
        contact.setNote_(properties.get("note"))

        request = Contacts.CNSaveRequest.alloc().init()
        request.addContact_toContainerWithIdentifier_(contact, None)
        self._exec_suppresed(self.xa_cstr.executeSaveRequest_error_, request, None)

        scriptable_contact = XABase.XAPredicate.evaluate_with_format(self.xa_scel.people(), f"( id == '{contact.identifier()}' )")[0]
        properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": contact,
                "scriptable_element": scriptable_contact,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
        return XAContactPerson(properties)

    def contacts(self, filter: dict = None) -> List['XAContactPerson']:
        """Returns a list of contacts matching the filter.

        .. versionadded:: 0.0.2
        """
        contacts_predicate = Contacts.CNContact.predicateForAllContacts()
        keys = list(Contacts.CNContact.alloc().init().availableKeys())
        contacts = self._exec_suppresed(self.xa_cstr.unifiedContactsMatchingPredicate_keysToFetch_error_, contacts_predicate, keys, None)[0]

        if filter is not None:
            contacts = XABase.XAPredicate.evaluate_with_dict(contacts, filter)

        elements = []
        for contact in contacts:
            scriptable_contact = XABase.XAPredicate.evaluate_with_format(self.xa_scel.people(), f"( id == '{contact.identifier()}' )")[0]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": contact,
                "scriptable_element": scriptable_contact,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactPerson(properties))
        return elements

class XAContactEntry(XABase.XAObject):
    """A class for managing and interacting with groups in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.identifier: str #: A unique identifier for this group
        self.name: str #: The name of the entry
        self.creation_date: datetime #: The date that the entry was created
        self.modification_date: datetime #: The date that the entry was last modified
        self.selected: bool #: Whether the entry is currently selected

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def name(self) -> str:
        return self.xa_elem.name()

    @property
    def creation_date(self) -> datetime:
        return self.xa_scel.creationDate()

    @property
    def modification_date(self) -> datetime:
        return self.xa_scel.modificationDate()

    @property
    def selected(self) -> bool:
        return self.xa_scel.selected()

class XAContactGroup(XAContactEntry):
    """A class for managing and interacting with groups in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

class XAContactPerson(XAContactEntry):
    """A class for managing and interacting with individual contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.phonetic_first_name: str #: The phonetic version of the first name of the contact
        self.phonetic_middle_name: str #: The phonetic version of the middle name of the contact
        self.phonetic_last_name: str #: The phonetic version of the last name of the contact
        self.mainden_name: str #: The maiden name of the person
        self.first_name: str #: The contact's first name
        self.middle_name: str #: The contact's middle name
        self.last_name: str #: The contact's last name
        self.name_prefix: str #: The contact's title, such as Dr.
        self.name_suffix: str #: Post-nominal letters such as PhD. or III
        self.nickname: str #: The contact's nickname
        self.birth_date: datetime #: The contact's birthday
        self.job_title: str #: The name of the contact's job position
        self.linked_contacts #: Contacts linked to this contact by some relation
        self.maps_data #: Location data for this contact
        self.note: str #: The user-inputted note for this contact
        self.organization: str #: The organization that the person works for
        self.sorting_family_name: str #: The last name used when sorting by last name
        self.sorting_given_name: str #: The first name used when sorting by first name
        self.text_alert #: The text alert assigned to this contact
        self.call_alert #: The call alert assigned to this contact
        self.image #: The image for this person
        self.thumbnail_image_data #: The raw data for the thumbnail image for this contact
        self.memoji_metadata #: The memoji metadata for this contact
        self.contact_relations #: Related contacts
        self.company: bool #: Whether the record represents a company or a person
        self.department: str #: The department that the person works for
        self.home_page: str #: The home page URL for this contact
        self.vcard: str #: The contact's information in vCard 3.0 format
        self.title: str #: The title of the person (same as prefix)

    @property
    def company(self) -> bool:
        return self.xa_scel.company()

    @property
    def phonetic_first_name(self) -> str:
        return self.xa_scel.phoneticFirstName()

    @property
    def first_name(self) -> str:
        return self.xa_scel.firstName()

    @property
    def middle_name(self) -> str:
        return self.xa_scel.middleName()

    @property
    def phonetic_middle_name(self) -> str:
        return self.xa_scel.phoneticMiddleName()

    @property
    def last_name(self) -> str:
        return self.xa_scel.lastName()

    @property
    def phonetic_last_name(self) -> str:
        return self.xa_scel.phoneticLastName()

    @property
    def name_prefix(self) -> str:
        return self.xa_elem.namePrefix()

    @property
    def title(self) -> str:
        return self.xa_scel.title()

    @property
    def name_suffix(self) -> str:
        return self.xa_elem.nameSuffix()

    @property
    def nickname(self) -> str:
        return self.xa_elem.nickname()

    @property
    def birth_date(self) -> str:
        return self.xa_scel.birthDate()

    @property
    def job_title(self) -> str:
        return self.xa_elem.jobTitle()

    @property
    def linked_contacts(self) -> str:
        return self.xa_elem.linkedContacts()

    @property
    def maps_data(self) -> str:
        return self.xa_elem.mapsData()

    @property
    def note(self) -> str:
        return self.xa_elem.node()

    @property
    def organization(self) -> str:
        return self.xa_scel.organization()

    @property
    def department(self) -> str:
        return self.xa_scel.department()

    @property
    def sorting_family_name(self) -> str:
        return self.xa_elem.sortingFamilyName()

    @property
    def sorting_given_name(self) -> str:
        return self.xa_elem.sortingGivenName()

    @property
    def text_alert(self) -> str:
        return self.xa_elem.textAlert()

    @property
    def call_alert(self) -> str:
        return self.xa_elem.callAlert()

    @property
    def image(self) -> str:
        return self.xa_scel.image()

    @property
    def thumbnail_image_data(self) -> str:
        return self.xa_elem.thumbnailImageDate()

    @property
    def memoji_metadata(self) -> str:
        return self.xa_elem.memojiMetadata()

    @property
    def contact_relations(self) -> str:
        return self.xa_elem.contactRelations()

    @property
    def homePage(self) -> str:
        return self.xa_scel.homePage()

    @property
    def vcard(self) -> str:
        return self.xa_scel.vcard()

    def show(self) -> None:
        """Shows the contact card for this contact in Contacts.app.
        """
        self.xa_wksp.openURL_(NSURL.alloc().initWithString_("addressbook://" + self.id))
        return self

    def delete(self) -> None:
        """Permanently deletes the contact.
        """
        request = Contacts.CNSaveRequest.alloc().init()
        request.deleteContact_(self.xa_elem.mutableCopy())
        self._exec_suppresed(self.xa_cstr.executeSaveRequest_error_, request, None)

    def phone_numbers(self) -> List['XAContactPhoneNumber']:
        """Gets a list of phone numbers associated with the contact.

        :return: The list of phone numbers.
        :rtype: XAContactPhoneNumber

        .. versionadded:: 0.0.2
        """
        numbers = self.xa_elem.phoneNumbers()
        elements = []
        for number in numbers:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": number,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactPhoneNumber(properties))
        return elements

    def addresses(self) -> List[Union['XAContactPostalAddress', 'XAContactEmailAddress', 'XAContactMessageAddress', 'XAContactURLAddress']]:
        """Gets a list of all addresses (of all types) associated with the contact.

        :return: The list of addresses.
        :rtype: List[Union[XAContactPostalAddress, XAContactEmailAddress, XAContactMessageAddress, XAContactURLAddress]]

        .. versionadded:: 0.0.2
        """
        elements = self.postal_addresses()
        elements.extend(self.email_addresses())
        elements.extend(self.message_addresses())
        elements.extend(self.url_addresses())
        return elements

    def postal_addresses(self) -> List['XAContactPostalAddress']:
        """Gets a list of the contact's postal addresses.

        :return: The list of postal addresses.
        :rtype: List[XAContactPostalAddress]

        .. versionadded:: 0.0.2
        """
        addresses = self.xa_elem.postalAddresses()
        elements = []
        for address in addresses:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": address,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactPostalAddress(properties))
        return elements

    def email_addresses(self) -> List['XAContactEmailAddress']:
        """Gets a list of the contact's email addresses.

        :return: The list of email addresses.
        :rtype: List[XAContactEmailAddress]

        .. versionadded:: 0.0.2
        """
        addresses = self.xa_elem.emailAddresses()
        elements = []
        for address in addresses:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": address,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactEmailAddress(properties))
        return elements

    def message_addresses(self) -> List['XAContactMessageAddress']:
        """Gets a list of the contact's instant message address objects.

        :return: The list of instant message addresses.
        :rtype: List[XAContactMessageAddress]

        .. versionadded:: 0.0.2
        """
        addresses = self.xa_elem.instantMessageAddresses()
        elements = []
        for address in addresses:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": address,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactMessageAddress(properties))
        return elements

    def url_addresses(self) -> List['XAContactURLAddress']:
        """Gets a list of the contact's URL address objects.

        :return: The list of URL addresses.
        :rtype: List[XAContactURLAddress]

        .. versionadded:: 0.0.2
        """
        addresses = self.xa_elem.urlAddresses()
        elements = []
        for address in addresses:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": address,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
                "contact_store": self.xa_cstr,
            }
            elements.append(XAContactURLAddress(properties))
        return elements


class XAContactPhoneNumber(XABaseScriptable.XASBObject):
    """A class for managing and interacting with phone numbers of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]
        
        self.identifier: str #: A unique identifier for this phone number
        self.label: str #: The label, such as `Home`, given to this phone number
        self.value: str #: The phone number as a string
        self.initial_country_code: str #: The user-specified country code

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def label(self) -> str:
        return self.xa_elem.label()

    @property
    def value(self) -> str:
        return self.xa_elem.value()

    @property
    def initial_country_code(self) -> str:
        return self.xa_elem.initialCountryCode()

    def __repr__(self):
        return "<" + str(type(self)) + self.value + ", id=" + self.id + ">"


class XAContactPostalAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with postal addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.identifier: str #: A unique identifier for this address
        self.label: str #: The label, such as "Home", given to this postal address
        self.street: str #: The street of the address
        self.sub_locality: str #: Additional information about a location, such as neighborhood or landmark
        self.city: str #: The city the address is in
        self.sub_administrative_area: str #: The county or region the address is in
        self.state: str #: The state that the address is in
        self.postal_code: str #: The postal code of the address
        self.country: str #: The country that the address is in
        self.iso_country_code: str #: The country code of the country the address is in

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def label(self) -> str:
        return self.xa_elem.label()

    @property
    def street(self) -> str:
        return self.xa_elem.street()

    @property
    def sub_locality(self) -> str:
        return self.xa_elem.subLocality()

    @property
    def city(self) -> str:
        return self.xa_elem.city()

    @property
    def sub_administrative_area(self) -> str:
        return self.xa_elem.subAdministrativeArea()

    @property
    def state(self) -> str:
        return self.xa_elem.state()

    @property
    def postal_code(self) -> str:
        return self.xa_elem.postalCode()

    @property
    def country(self) -> str:
        return self.xa_elem.country()

    @property
    def iso_country_code(self) -> str:
        return self.xa_elem.ISOCountryCode()


class XAContactEmailAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with email addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.identifier: str #: A unique identifier for this address
        self.label: str #: The label, such as "Work", given to this email address
        self.value #: The email address as a string

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def label(self) -> str:
        return self.xa_elem.label()

    @property
    def value(self) -> str:
        return self.xa_elem.value()


class XAContactMessageAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with instant message addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.identifier: str #: A unique identifier for this address
        self.label: str #: The label, such as `Other`, given to this IM address
        self.username: str #: The user-provided username for this address entry
        self.service: str #: The IM service this address applies to

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def label(self) -> str:
        return self.xa_elem.label()

    @property
    def username(self) -> str:
        return self.xa_elem.username()

    @property
    def service(self) -> str:
        return self.xa_elem.service()

    
class XAContactURLAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with URL addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.identifier: str #: A unique identifier for this address
        self.label: str #: The label, such as `Homepage`, given to this URL
        self.value: str #: The URL as a string

    @property
    def identifier(self) -> str:
        return self.xa_elem.identifier()

    @property
    def label(self) -> str:
        return self.xa_elem.label()

    @property
    def value(self) -> str:
        return self.xa_elem.value()