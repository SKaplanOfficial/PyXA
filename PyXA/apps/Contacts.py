""".. versionadded:: 0.0.2

Control the macOS Contacts application using JXA-like syntax.
"""
from datetime import datetime
import os, sys
from typing import List, Union
from AppKit import NSFileManager, NSURL, NSSet

import Contacts
import objc
from AppKit import NSPredicate, NSMutableArray

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
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            groups = groups.filteredArrayUsingPredicate_(predicate)

        elements = []
        for group in groups:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": group.identifier()}))
            scriptable_groups = self.xa_scel.groups()
            scriptable_group = scriptable_groups.filteredArrayUsingPredicate_(predicate)[0]
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

        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": contact.identifier()}))
        scriptable_contacts = self.xa_scel.people()
        scriptable_contact = scriptable_contacts.filteredArrayUsingPredicate_(predicate)[0]
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
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            contacts = contacts.filteredArrayUsingPredicate_(predicate)

        elements = []
        for contact in contacts:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"id": contact.identifier()}))
            scriptable_contacts = self.xa_scel.people()
            scriptable_contact = scriptable_contacts.filteredArrayUsingPredicate_(predicate)[0]
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

class XAContactGroup(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with groups in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this group
        self.name: str = self.xa_elem.name()
        self.creation_date: datetime = self.xa_elem.creationDate()
        self.modification_date: datetime = self.xa_elem.modificationDate()

class XAContactPerson(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with individual contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this contact
        self.type = self.xa_elem.contactType()
        self.given_name: str = self.xa_elem.givenName() #: The contact's first name
        self.middle_name: str = self.xa_elem.middleName() #: The contact's middle name
        self.family_name: str = self.xa_elem.familyName() #: The contact's last name
        self.name_prefix: str = self.xa_elem.namePrefix() #: The contact's title, such as Dr.
        self.name_suffix: str = self.xa_elem.nameSuffix() #: Post-nominal letters such as PhD. or III
        self.nickname: str = self.xa_elem.nickname() #: The contact's nickname
        self.creation_date: datetime = self.xa_elem.creationDate() #: The date the contact was created
        self.modification_date: datetime = self.xa_elem.modificationDate() #: The date the contact was last modified
        self.birthday: datetime = self.xa_elem.birthday() #: The contact's birthday
        self.job_title: str = self.xa_elem.jobTitle() #: The name of the contact's job position
        self.linked_contacts = self.xa_elem.linkedContacts()
        self.maps_data = self.xa_elem.mapsData()
        self.note: str = self.xa_elem.note()
        self.organization_name: str = self.xa_elem.organizationName()
        self.snapshot = self.xa_elem.snapshot()
        self.social_profiles = self.xa_elem.socialProfiles()
        self.sorting_family_name: str = self.xa_elem.sortingFamilyName()
        self.sorting_given_name: str = self.xa_elem.sortingGivenName()
        self.text_alert = self.xa_elem.textAlert()
        self.call_alert = self.xa_elem.callAlert()
        self.image_data = self.xa_elem.imageData()
        self.thumbnail_image_data = self.xa_elem.thumbnailImageData()
        self.memoji_metadata = self.xa_elem.memojiMetadata()
        self.contact_relations = self.xa_elem.contactRelations()

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

    def vcard(self) -> bytes:
        """Gets the vcard representation of the contact.

        :return: The vcard format of the contact in bytes.
        :rtype: bytes

        .. versionadded:: 0.0.2
        """
        return Contacts.CNContactVCardSerialization.dataWithContacts_error_([self.xa_elem], None)[0]

    def __repr__(self):
        return "<" + str(type(self)) + self.given_name + " " + self.family_name + ", id=" + self.id + ">"


class XAContactPhoneNumber(XABaseScriptable.XASBObject):
    """A class for managing and interacting with phone numbers of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]
        
        self.id: str = self.xa_elem.identifier() #: A unique identifier for this phone number
        self.label: str = self.xa_elem.label() #: The label, such as `Home`, given to this phone number
        self.value: str = self.xa_elem.value().stringValue() #: The phone number as a string
        self.country_code: str = self.xa_elem.value().initialCountryCode() #: The user-specified country code

    def __repr__(self):
        return "<" + str(type(self)) + self.value + ", id=" + self.id + ">"


class XAContactPostalAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with postal addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this address
        self.label: str = self.xa_elem.label()
        self.street: str = self.xa_elem.value().street()
        self.sub_locality: str = self.xa_elem.value().subLocality()
        self.city: str = self.xa_elem.value().city()
        self.sub_administrative_area: str = self.xa_elem.value().subAdministrativeArea()
        self.state: str = self.xa_elem.value().state()
        self.postal_code: str = self.xa_elem.value().postalCode()
        self.country: str = self.xa_elem.value().country()
        self.country_code: str = self.xa_elem.value().ISOCountryCode()


class XAContactEmailAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with email addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this address
        self.label: str = self.xa_elem.label() #: The label, such as "Work", given to this email address
        self.value = self.xa_elem.value() #: The email address as a string


class XAContactMessageAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with instant message addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this address
        self.label: str = self.xa_elem.label() #: The label, such as `Other`, given to this IM address
        self.username: str = self.xa_elem.value().username() #: The user-provided username for this address entry
        self.service: str = self.xa_elem.value().service() #: The IM service this address applies to

    
class XAContactURLAddress(XABaseScriptable.XASBObject):
    """A class for managing and interacting with URL addresses of contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id: str = self.xa_elem.identifier() #: A unique identifier for this address
        self.label: str = self.xa_elem.label() #: The label, such as `Homepage`, given to this URL
        self.value: str = self.xa_elem.value() #: The URL as a string