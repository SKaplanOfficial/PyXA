""".. versionadded:: 0.0.2

Control the macOS Contacts application using JXA-like syntax.
"""
import os, sys
from typing import List, Union
from AppKit import NSFileManager, NSURL, NSSet

import Contacts
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

        self.id = self.xa_elem.identifier()
        self.name = self.xa_elem.name()
        self.creation_date = self.xa_elem.creationDate()
        self.modification_date = self.xa_elem.modificationDate()

class XAContactPerson(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with individual contacts in Contacts.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_cstr = properties["contact_store"]

        self.id = self.xa_elem.identifier()
        self.birthday = self.birthday = self.xa_elem.birthday()
        self.type = self.xa_elem.contactType()
        self.creation_date = self.xa_elem.creationDate()
        self.family_name = self.xa_elem.familyName()
        self.given_name = self.xa_elem.givenName()
        self.xa_elem.imageData()
        self.xa_elem.instantMessageAddresses()
        self.xa_elem.jobTitle()
        self.xa_elem.linkedContacts()
        self.xa_elem.mapsData()
        self.xa_elem.middleName()
        self.xa_elem.modificationDate()
        self.xa_elem.nickname()
        self.xa_elem.namePrefix()
        self.xa_elem.nameSuffix()
        self.xa_elem.note()
        self.xa_elem.organizationName()
        self.xa_elem.phoneNumbers()
        self.xa_elem.postalAddresses()
        self.xa_elem.snapshot()
        self.xa_elem.socialProfiles()
        self.xa_elem.sortingFamilyName()
        self.xa_elem.sortingGivenName()
        self.xa_elem.urlAddresses()
        self.xa_elem.textAlert()
        self.xa_elem.callAlert()
        self.xa_elem.thumbnailImageData()
        self.xa_elem.memojiMetadata()
        self.xa_elem.contactRelations()

        # print(self.xa_elem.identifier())

    def show(self):
        """Shows the contact card for this contact in Contacts.app.
        """
        self.xa_wksp.openURL_(NSURL.alloc().initWithString_("addressbook://" + self.id))
        return self

    def delete(self):
        """Permanently deletes the contact.
        """
        request = Contacts.CNSaveRequest.alloc().init()
        request.deleteContact_(self.xa_elem.mutableCopy())
        self._exec_suppresed(self.xa_cstr.executeSaveRequest_error_, request, None)