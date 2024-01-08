""".. versionadded:: 0.2.0

Control the macOS Database Events application using JXA-like syntax.
"""
from enum import Enum
from typing import Any, Union

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath


class XADatabaseEventsApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """The Database Events program.

    .. versionadded:: 0.2.0
    """

    class ObjectType(Enum):
        """Types of objects that can be created."""

        DATABASE = "database"
        RECORD = "record"
        FIELD = "field"

    class StoreType(Enum):
        """Types of storage used by databases."""

        BINARY = XABase.OSType("bin ")
        MEMORY = XABase.OSType("mem ")
        SQLITE = XABase.OSType("sqlt")
        XML = XABase.OSType("xml ")
        NONE = 0

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    @property
    def quit_delay(self) -> int:
        return self.xa_scel.quitDelay()

    def open(self, path: Union[str, XABase.XAPath]) -> "XADatabaseEventsDatabase":
        """Opens the database at the given filepath.

        :param path: The path of the .dbev file to open.
        :type path: Union[str, XABase.XAPath]
        :return: A reference to newly opened database object
        :rtype: XADatabaseEventsDatabase

        .. versionadded:: 0.1.1
        """
        if isinstance(path, XABase.XAPath):
            path = path.path

        name = ".".join(path.split("/")[-1][::-1].split(".")[1:])[::-1]
        location = XABase.XAPath("/".join(path.split("/")[:-1])).xa_elem

        for db in self.databases().xa_elem:
            if db.name() == name and db.location() == location:
                return self._new_element(db, XADatabaseEventsDatabase)

        new_db = (
            self.xa_scel.classForScriptingClass_("database")
            .alloc()
            .initWithProperties_({"name": name, "location": location})
        )
        self.xa_scel.databases().addObject_(new_db)
        return self._new_element(self.xa_scel.open_(new_db), XADatabaseEventsDatabase)

    def databases(
        self, filter: Union[dict, None] = None
    ) -> "XADatabaseEventsDatabaseList":
        """Returns a list of databases, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned databases will have, or None
        :type filter: Union[dict, None]
        :return: The list of databases
        :rtype: XADatabaseEventsDatabaseList

        .. versionadded:: 0.2.0
        """
        return self._new_element(
            self.xa_scel.databases(), XADatabaseEventsDatabaseList, filter
        )

    def new_database(
        self,
        name: str,
        location: Union[XABase.XAPath, str, None] = None,
        store_type: StoreType = StoreType.SQLITE,
    ) -> "XADatabaseEventsDatabase":
        """Creates a new database.

        :param name: The name of the databases
        :type name: str
        :param location: The folder that contains the database, defaults to None
        :type location: Union[XABase.XAPath, str, None], optional
        :param store_type: The type of storage used by the database, defaults to StoreType.SQLite
        :type store_typre: StoreType, optional
        :return: The newly created database object
        :rtype: XADatabaseEventsDatabase

        .. versionadded:: 0.2.0
        """
        if isinstance(location, XABase.XAPath):
            location = location.path

        new_db = self.make(
            "database",
            {"name": name, "location": location, "storeType": store_type.value},
        )
        return self.databases().push(new_db)

    def make(
        self,
        specifier: Union[str, "XADatabaseEventsApplication.ObjectType"],
        properties: dict = None,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XADatabaseEventsApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.2.0
        """
        if isinstance(specifier, XADatabaseEventsApplication.ObjectType):
            specifier = specifier.value

        if data is None:
            camelized_properties = {}

            if properties is None:
                properties = {}

            for key, value in properties.items():
                if key == "url":
                    key = "URL"

                camelized_properties[XABase.camelize(key)] = value

            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithProperties_(camelized_properties)
            )
        else:
            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithData_(data)
            )

        if specifier == "database":
            return self._new_element(obj, XADatabaseEventsDatabase)
        elif specifier == "record":
            return self._new_element(obj, XADatabaseEventsRecord)
        elif specifier == "field":
            return self._new_element(obj, XADatabaseEventsField)


class XADatabaseEventsDatabaseList(XABase.XAList):
    """A wrapper around lists of databases that employs fast enumeration techniques.

    All properties of databases can be called as methods on the wrapped list, returning a list containing each database's value for the property.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADatabaseEventsDatabase, filter)

    def location(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("location") or []
        return [XABase.XAPath(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def store_type(self) -> list[XADatabaseEventsApplication.StoreType]:
        ls = self.xa_elem.arrayByApplyingSelector_("storeType") or []
        return [
            XADatabaseEventsApplication.StoreType(XABase.OSType(x.stringValue()))
            for x in ls
        ]

    def by_location(
        self, location: Union[XABase.XAPath, str]
    ) -> Union["XADatabaseEventsDatabase", None]:
        if isinstance(location, XABase.XAPath):
            location = location.path
        return self.by_property("location", location)

    def by_name(self, name: str) -> Union["XADatabaseEventsDatabase", None]:
        return self.by_property("name", name)

    def by_store_type(
        self, store_type: XADatabaseEventsApplication.StoreType
    ) -> Union["XADatabaseEventsDatabase", None]:
        return self.by_property("storeType", store_type)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XADatabaseEventsDatabase(XABase.XAObject):
    """A collection of records, residing at a location in the file system.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def location(self) -> XABase.XAPath:
        """The folder that contains the database."""
        return XABase.XAPath(self.xa_elem.location())

    @property
    def name(self) -> str:
        """The name of the database."""
        return self.xa_elem.name()

    @property
    def store_type(self) -> XADatabaseEventsApplication.StoreType:
        """The type of storage used by the database; may be specified upon creation, but not thereafter; defaults to SQLite."""
        return XADatabaseEventsApplication.StoreType(self.xa_elem.storeType())

    def delete(self):
        """Deletes the database.

        .. versionadded:: 0.2.0
        """
        self.xa_elem.delete()

    def save(self):
        """Saves the database in the folder specified by the :attr:`location` attribute.

        .. versionadded:: 0.2.0
        """
        self.xa_elem.saveAs_in_(None, None)

    def new_record(self, name: str) -> "XADatabaseEventsRecord":
        """Creates a new record attached to this database.

        :param name: The name of the record
        :type name: str
        :return: The newly created record object
        :rtype: XADatabaseEventsRecord

        .. versionadded:: 0.2.0
        """
        parent = self.xa_prnt
        while not hasattr(parent, "databases"):
            parent = parent.xa_prnt

        new_record = parent.make("record", {"name": name})
        return self.records().push(new_record)

    def records(self, filter: Union[dict, None] = None) -> "XADatabaseEventsRecordList":
        """Returns a list of records, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned records will have, or None
        :type filter: Union[dict, None]
        :return: The list of records
        :rtype: XADatabaseEventsRecordList

        .. versionadded:: 0.2.0
        """
        return self._new_element(
            self.xa_elem.records(), XADatabaseEventsRecordList, filter
        )

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XADatabaseEventsFieldList(XABase.XAList):
    """A wrapper around lists of fields that employs fast enumeration techniques.

    All properties of fields can be called as methods on the wrapped list, returning a list containing each field's value for the property.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADatabaseEventsField, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_id(self, id: int) -> Union["XADatabaseEventsField", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XADatabaseEventsField", None]:
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union["XADatabaseEventsField", None]:
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XADatabaseEventsField(XABase.XAObject):
    """A named piece of data, residing in a record.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique ID of the field."""
        return self.xa_elem.id().get()

    @property
    def name(self) -> str:
        """The name of the field."""
        return self.xa_elem.name().get()

    @property
    def value(self) -> Any:
        """The value of the field."""
        return self.xa_elem.value().get()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def delete(self):
        """Deletes the field.

        .. versionadded:: 0.2.0
        """
        self.xa_elem.delete()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XADatabaseEventsRecordList(XABase.XAList):
    """A wrapper around lists of records that employs fast enumeration techniques.

    All properties of records can be called as methods on the wrapped list, returning a list containing each record's value for the property.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADatabaseEventsRecord, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_id(self, id: int) -> Union["XADatabaseEventsRecord", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XADatabaseEventsRecord", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XADatabaseEventsRecord(XABase.XAObject):
    """A collection of fields, residing in a database.

    .. versionadded:: 0.2.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique ID of the record."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the record, equivalent to the value of the "name" field."""
        return self.xa_elem.name()

    def delete(self):
        """Deletes the record.

        .. versionadded:: 0.2.0
        """
        self.xa_elem.delete()

    def new_field(self, name: str, value: Any = None) -> "XADatabaseEventsRecord":
        """Creates a new field and adds it to this record.

        :param name: The name of the field
        :type name: str
        :param value: The initial value of the field, defaults to None
        :type value: Any
        :return: The newly created field object
        :rtype: XADatabaseEventsRecord

        .. versionadded:: 0.2.0
        """
        parent = self.xa_prnt
        while not hasattr(parent, "databases"):
            parent = parent.xa_prnt

        new_field = parent.make("field", {"name": name, "value": value})
        return self.fields().push(new_field)

    def fields(self, filter: Union[dict, None] = None) -> "XADatabaseEventsFieldList":
        """Returns a list of fields, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned fields will have, or None
        :type filter: Union[dict, None]
        :return: The list of fields
        :rtype: XADatabaseEventsFieldList

        .. versionadded:: 0.2.0
        """
        return self._new_element(
            self.xa_elem.fields(), XADatabaseEventsFieldList, filter
        )

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
