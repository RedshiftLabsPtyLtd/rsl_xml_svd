#!/usr/bin/env python

# Author: Dr. Konstantin Selyunin
# License: MIT

import os
import os.path

from dataclasses import dataclass
from typing import Any, List, Tuple
from xml.etree import ElementTree as ET


@dataclass
class EnumeratedValue:
    name: str
    description: str
    value: int

    def __repr__(self):
        return f"EnumeratedValue(name={self.name} -> value={self.value})"


@dataclass
class Field:
    name: str
    description: str
    bit_range: Tuple[int]
    data_type: str
    access: str
    enumerated_values: Tuple[EnumeratedValue] = tuple()

    def __repr__(self):
        return f"Field(name={self.name}, "\
               f"bit_range={self.bit_range}, data_type={self.data_type}, "\
               f"access={self.access}, enumerated_values={self.enumerated_values})"


@dataclass
class Register:
    name: str
    description: str
    access: str
    address: int
    address_offset: int
    fields: List[Field]

    def __repr__(self):
        return f"Register(name={self.name}, address={self.address}, access={self.access}, fields={self.fields})"


class RslSvdParser:

    def __init__(self, *args, **kwargs):
        self.svd_xml_file = os.path.abspath('./shearwater.svd') if not kwargs.get('svd_file') else kwargs.get('svd_file')
        self.svd_xml_root = RslSvdParser.parse_svd_file(self.svd_xml_file)
        self.svd_regs = self.find_all_register_xml_root_in_svd()
        self.svd_cregs = self.find_cregs_in_svd()
        self.svd_dregs = self.get_dregs_from_svd()
        self.svd_commands = self.get_commands_from_svd()
        self.cregs = self.get_cregs_objects()
        self.dregs = self.get_dreg_objects()
        self.commands = self.get_commands_objects()
        self.regs = self.cregs + self.dregs + self.commands

    @staticmethod
    def parse_svd_file(file_to_parse: str):
        if not os.path.exists(file_to_parse):
            raise FileNotFoundError(f"Non-existing SVD file provided, check if ``{file_to_parse}`` exists!")
        return ET.parse(file_to_parse).getroot()

    def find_all_register_xml_root_in_svd(self) -> ET.Element:
        return self.svd_xml_root.findall('.//register')

    def find_cregs_in_svd(self) -> Tuple[Any, ...]:
        return tuple(el for el in self.svd_regs if 'CREG' in el.find('./name').text)

    def get_dregs_from_svd(self) -> Tuple[Any, ...]:
        return tuple(el for el in self.svd_regs if 'DREG' in el.find('./name').text)

    def get_commands_from_svd(self) -> Tuple[Any, ...]:
        return tuple(el for el in self.svd_regs if int(el.find('./addressOffset').text, 16) / 4 >= 0xAA)

    def get_cregs_objects(self) -> Tuple[Register]:
        return tuple(self.extract_register_fields(el) for el in self.svd_cregs)

    def get_dreg_objects(self) -> Tuple[Register]:
        return tuple(self.extract_register_fields(el) for el in self.svd_dregs)

    def get_commands_objects(self) -> Tuple[Register]:
        return tuple(self.extract_register_fields(el) for el in self.svd_commands)

    def find_register_by(self, **kw):
        regs = self.get_cregs_objects() + self.get_dreg_objects() + self.get_commands_objects()
        if len(kw) > 1:
            raise NotImplementedError("Only one property is currently implemented!")
        (prop, value), = kw.items()
        found_register = next(filter(lambda x: getattr(x, prop) == value, regs), None)
        return found_register

    @staticmethod
    def get_enumerated_value(enum_value: ET.Element) -> EnumeratedValue:
        name = enum_value.find('.//name').text
        description = enum_value.find('.//description').text
        value = int(enum_value.find('.//value').text)
        return EnumeratedValue(name=name, description=description, value=value)

    def get_enumerated_values(self, enum_values: ET.Element) -> Tuple[EnumeratedValue]:
        if enum_values:
            return tuple(self.get_enumerated_value(child) for child in enum_values)

    def extract_field_info(self, field: ET.Element) -> Field:
        name = field.find('.//name').text
        description = field.find('.//description').text
        bit_range_str = field.find('.//bitRange').text
        bit_range = tuple(int(el) for el in bit_range_str.strip('[]').split(':'))
        access = field.find('.//access').text
        data_type = field.find('.//dataType').text
        enumerated_values = self.get_enumerated_values(field.find('.//enumeratedValues'))
        return Field(name=name,
                     description=description,
                     bit_range=bit_range,
                     data_type=data_type,
                     access=access,
                     enumerated_values=enumerated_values)

    def extract_register_fields(self, reg_desc: ET.Element) -> Register:
        reg_name = reg_desc.find('.//name').text
        reg_access = reg_desc.find('.//access').text
        description = reg_desc.find('.//description').text
        address_offset = int(reg_desc.find('.//addressOffset').text, 16)
        address = int(address_offset / 4)
        fields = reg_desc.findall('.//field')
        field_info = [self.extract_field_info(field) for field in fields]
        return Register(name=reg_name,
                        access=reg_access,
                        description=description,
                        address=address,
                        address_offset=address_offset,
                        fields=field_info)


if __name__ == '__main__':
    pass

