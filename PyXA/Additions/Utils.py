""".. versionadded:: 0.1.1

A collection of classes for interacting with macOS features in various ways.
"""

import AppKit
import xml.etree.ElementTree as ET
from typing import Union, Callable, Any, Literal
from PyObjCTools import AppHelper
from PyXA import XABase
from datetime import datetime, timedelta
from enum import Enum
from time import sleep

class SDEFParser():
    def __init__(self, sdef_file: Union['XABase.XAPath', str]):
        if isinstance(sdef_file, str):
            sdef_file = XABase.XAPath(sdef_file)
        self.file = sdef_file #: The full path to the SDEF file to parse

        self.app_name = ""
        self.scripting_suites = []

    def parse(self):
        app_name = self.file.path.split("/")[-1][:-5].title()
        xa_prefix = "XA" + app_name

        tree = ET.parse(self.file.path)

        suites = []

        scripting_suites = tree.findall("suite")
        for suite in scripting_suites:
            classes = []
            commands = {}

            ### Class Extensions
            class_extensions = suite.findall("class-extension")
            for extension in class_extensions:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + extension.attrib.get("extends", "").title()
                class_comment = extension.attrib.get("description", "")

                ## Class Extension Properties
                class_properties = extension.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Extension Elements
                class_elements = extension.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Extension Responds-To Commands
                class_responds_to_commands = extension.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })

            ### Classes
            scripting_classes = suite.findall("class")
            for scripting_class in scripting_classes:
                properties = []
                elements = []
                responds_to_commands = []

                class_name = xa_prefix + scripting_class.attrib.get("name", "").title()
                class_comment = scripting_class.attrib.get("description", "")

                ## Class Properties
                class_properties = scripting_class.findall("property")
                for property in class_properties:
                    property_type = property.attrib.get("type", "")
                    if property_type == "text":
                        property_type = "str"
                    elif property_type == "boolean":
                        property_type = "bool"
                    elif property_type == "number":
                        property_type = "float"
                    elif property_type == "integer":
                        property_type = "int"
                    elif property_type == "rectangle":
                        property_type = "tuple[int, int, int, int]"
                    else:
                        property_type = "XA" + app_name + property_type.title()

                    property_name = property.attrib.get("name", "").replace(" ", "_").lower()
                    property_comment = property.attrib.get("description", "")

                    properties.append({
                        "type": property_type,
                        "name": property_name,
                        "comment": property_comment
                    })

                ## Class Elements
                class_elements = scripting_class.findall("element")
                for element in class_elements:
                    element_name = (element.attrib.get("type", "") + "s").replace(" ", "_").lower()
                    element_type = "XA" + app_name + element.attrib.get("type", "").title()

                    elements.append({
                        "name": element_name,
                        "type": element_type
                    })

                ## Class Responds-To Commands
                class_responds_to_commands = scripting_class.findall("responds-to")
                for command in class_responds_to_commands:
                    command_name = command.attrib.get("command", "").replace(" ", "_").lower()
                    responds_to_commands.append(command_name)

                classes.append({
                    "name": class_name,
                    "comment": class_comment,
                    "properties": properties,
                    "elements": elements,
                    "responds-to": responds_to_commands
                })


            ### Commands
            script_commands = suite.findall("command")
            for command in script_commands:
                command_name = command.attrib.get("name", "").lower().replace(" ", "_")
                command_comment = command.attrib.get("description", "")

                parameters = []
                direct_param = command.find("direct-parameter")
                if direct_param is not None:
                    direct_parameter_type = direct_param.attrib.get("type", "")
                    if direct_parameter_type == "specifier":
                        direct_parameter_type = "XABase.XAObject"

                    direct_parameter_comment = direct_param.attrib.get("description")

                    parameters.append({
                        "name": "direct_param",
                        "type": direct_parameter_type,
                        "comment": direct_parameter_comment
                    })

                if not "_" in command_name and len(parameters) > 0:
                    command_name += "_"

                command_parameters = command.findall("parameter")
                for parameter in command_parameters:
                    parameter_type = parameter.attrib.get("type", "")
                    if parameter_type == "specifier":
                        parameter_type = "XAObject"

                    parameter_name = parameter.attrib.get("name", "").lower().replace(" ", "_")
                    parameter_comment = parameter.attrib.get("description", "")

                    parameters.append({
                        "name": parameter_name,
                        "type": parameter_type,
                        "comment": parameter_comment,
                    })

                commands[command_name] = {
                    "name": command_name,
                    "comment": command_comment,
                    "parameters": parameters
                }

            suites.append({
                "classes": classes,
                "commands": commands
            })

        self.scripting_suites = suites
        return suites

    def export(self, output_file: Union['XABase.XAPath', str]):
        if isinstance(output_file, XABase.XAPath):
            output_file = output_file.path

        lines = []

        lines.append("from typing import Any, Callable, Union")
        lines.append("\nfrom PyXA import XABase")
        lines.append("from PyXA.XABase import OSType")
        lines.append("from PyXA import XABaseScriptable")

        for suite in self.scripting_suites:
            for scripting_class in suite["classes"]:
                lines.append("\n\n")
                lines.append("class " + scripting_class["name"].replace(" ", "") + "List:")
                lines.append("\t\"\"\"A wrapper around lists of " + scripting_class["name"].lower() + "s that employs fast enumeration techniques.")
                lines.append("\n\tAll properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.")
                lines.append("\n\t.. versionadded:: " + XABase.VERSION)
                lines.append("\t\"\"\"")

                lines.append("\tdef __init__(self, properties: dict, filter: Union[dict, None] = None):")
                lines.append("\t\tsuper().__init__(properties, " + scripting_class["name"].replace(" ", "") + ", filter)")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef " + property["name"] + "(self) -> list['" + property["type"].replace(" ", "") + "']:")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn list(self.xa_elem.arrayByApplyingSelector_(\"" + property["name"] + "\"))")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\tdef by_" + property["name"] + "(self, " + property["name"] + ") -> '" + scripting_class["name"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Retrieves the " + scripting_class["comment"] + "whose " + property["name"] + " matches the given " + property["name"] + ".\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.by_property(\"" + property["name"] + "\", " + property["name"] + ")")


                lines.append("")
                lines.append("class " + scripting_class["name"].replace(" ", "") + ":")
                lines.append("\t\"\"\"" + scripting_class["comment"] + "\n\n\t.. versionadded:: " + XABase.VERSION + "\n\t\"\"\"")

                for property in scripting_class["properties"]:
                    lines.append("")
                    lines.append("\t@property")
                    lines.append("\tdef " + property["name"] + "(self) -> '" + property["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"" + property["comment"] + "\n\n\t\t.. versionadded:: " + XABase.VERSION + "\n\t\t\"\"\"")
                    lines.append("\t\treturn self.xa_elem." + property["name"] + "()")

                for element in scripting_class["elements"]:
                    lines.append("")
                    lines.append("\tdef " + element["name"].replace(" ", "") + "(self, filter: Union[dict, None] = None) -> '" + element["type"].replace(" ", "") + "':")
                    lines.append("\t\t\"\"\"Returns a list of " + element["name"] + ", as PyXA objects, matching the given filter.")
                    lines.append("\n\t\t.. versionadded:: " + XABase.VERSION)
                    lines.append("\t\t\"\"\"")
                    lines.append("\t\tself._new_element(self.xa_elem." + element["name"] + "(), " + element["type"].replace(" ", "") + "List, filter)")

                for command in scripting_class["responds-to"]:
                    if command in suite["commands"]:
                        lines.append("")
                        command_str = "\tdef " + suite["commands"][command]["name"] + "(self, "

                        for parameter in suite["commands"][command]["parameters"]:
                            command_str += parameter["name"] + ": '" + parameter["type"] + "', "

                        command_str = command_str[:-2] + "):"
                        lines.append(command_str)

                        lines.append("\t\t\"\"\"" + suite["commands"][command]["comment"])
                        lines.append("\n\t\t.. versionadded:: " + XABase.VERSION)
                        lines.append("\t\t\"\"\"")

                        cmd_call_str = "self.xa_elem." + suite["commands"][command]["name"] + "("

                        if len(suite["commands"][command]["parameters"]) > 0:
                            for parameter in suite["commands"][command]["parameters"]:
                                cmd_call_str += parameter["name"] + ", "
                            
                            cmd_call_str = cmd_call_str[:-2] + ")"
                        else:
                            cmd_call_str += ")"

                        lines.append("\t\t" + cmd_call_str)

        data = "\n".join(lines)
        with open(output_file, "w") as f:
            f.write(data)