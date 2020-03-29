import os
import os.path
import pytest
from rsl_svd_parser import RslSvdParser, Register, Field, EnumeratedValue


@pytest.fixture
def rsl_svd_parser() -> RslSvdParser:
    return RslSvdParser()


@pytest.mark.svd
def test_rls_svd_parser_init(rsl_svd_parser: RslSvdParser):
    assert os.path.exists(rsl_svd_parser.svd_xml_file), "NO SVD file found!"

    assert len(rsl_svd_parser.svd_cregs) > 0, "NO config registers found!"
    assert len(rsl_svd_parser.svd_dregs) > 0, "NO data registers found!"
    assert len(rsl_svd_parser.svd_commands) > 0, "NO command registers found"

    assert len(rsl_svd_parser.svd_regs) == \
           len(rsl_svd_parser.svd_cregs) + \
           len(rsl_svd_parser.svd_dregs) + \
           len(rsl_svd_parser.svd_commands), \
                                                "Total registers not equal to `cregs`, `dregs`, `commands`"


@pytest.mark.svd
def test_svd_registers(rsl_svd_parser: RslSvdParser):
    xml_regs = rsl_svd_parser.svd_regs
    for reg in xml_regs:
        register = rsl_svd_parser.extract_register_fields(reg)
        assert len(register.name) > 0, f"NO register name for offset {register.address_offset}!"
        assert register.access in ['read-only', 'write-only', 'read-write'], f"INVALID register access for {register.name}!"
        assert len(register.description) > 0, f"NO register description available for {register.name}!"
        assert register.address_offset >= 0, f"Address offset is incorrect for {register.name}"
        assert len(register.fields) > 0, f"NO Fields in register {register.name}"


@pytest.mark.svd
def test_get_cregs_objects(rsl_svd_parser: RslSvdParser):
    cregs = rsl_svd_parser.get_cregs_objects()
    assert len(cregs) > 0, "No command registers found!"
    assert cregs[0].name == 'CREG_COM_SETTINGS', "First register name is incorrect!"


@pytest.mark.svd
def test_find_register_by(rsl_svd_parser: RslSvdParser):
    reg = rsl_svd_parser.find_register_by(name='CREG_COM_SETTINGS')
    assert reg is not None, "NO CREG_COM_SETTINGS register found!"
    assert type(reg) == Register, "`Register` type is expected for the found object!"
    dreg_gyro_1_raw_z = rsl_svd_parser.find_register_by(address=87)
    assert dreg_gyro_1_raw_z is not None, "NO register with address 87 found!"


@pytest.mark.svd
def test_find_field_by(rsl_svd_parser: RslSvdParser):
    reg = rsl_svd_parser.find_register_by(name='CREG_COM_SETTINGS')
    field = reg.find_field_by(name='BAUD_RATE')
    assert type(field) == Field, "`Field` type is expected for the found object!"
    assert field.data_type is not None, "Data type is empty!"
    assert field.bit_range[0] >= field.bit_range[1], "Bit range shall be in format: MSB, LSB"
    assert len(field.description) > 0, "Field description is empty!"


@pytest.mark.svd
def test_find_enum_entry_by(rsl_svd_parser: RslSvdParser):
    reg = rsl_svd_parser.find_register_by(name='CREG_COM_SETTINGS')
    field = reg.find_field_by(name='BAUD_RATE')
    enum = field.find_enum_entry_by(value=4)
    assert type(enum) == EnumeratedValue, f"EnumeratedValue expected, but got: {type(enum)}"
    assert enum.value == 4, f"Expecting 4, but got {enum.value}"
    assert enum.name == '57600', f"Expecting name: 57600, but got {enum.name}"
    assert len(enum.description) > 0, "Empty enum description!"


@pytest.mark.svd
def test_regs(rsl_svd_parser: RslSvdParser):
    regs = rsl_svd_parser.regs
    assert id(regs) == id(rsl_svd_parser.regs), f"different IDs, not the same objects"
    print(regs)
