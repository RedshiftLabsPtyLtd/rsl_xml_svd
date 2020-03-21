import os
import os.path
import pytest
from rsl_svd_parser import RslSvdParser, Register


@pytest.fixture
def rsl_svd_parser():
    return RslSvdParser()


def test_rls_svd_parser_init(rsl_svd_parser):
    assert os.path.exists(rsl_svd_parser.svd_xml_file), "NO SVD file found!"

    assert len(rsl_svd_parser.svd_cregs) > 0, "NO config registers found!"
    assert len(rsl_svd_parser.svd_dregs) > 0, "NO data registers found!"
    assert len(rsl_svd_parser.svd_commands) > 0, "NO command registers found"

    assert len(rsl_svd_parser.svd_regs) == \
           len(rsl_svd_parser.svd_cregs) + \
           len(rsl_svd_parser.svd_dregs) + \
           len(rsl_svd_parser.svd_commands), \
                                                "Total registers not equal to `cregs`, `dregs`, `commands`"


def test_svd_registers(rsl_svd_parser):
    xml_regs = rsl_svd_parser.svd_regs
    for reg in xml_regs:
        register = rsl_svd_parser.extract_register_fields(reg)
        assert len(register.name) > 0, f"NO register name for offset {register.address_offset}!"
        assert register.access in ['read-only', 'write-only', 'read-write'], f"INVALID register access for {register.name}!"
        assert len(register.description) > 0, f"NO register description available for {register.name}!"
        assert register.address_offset >= 0, f"Address offset is incorrect for {register.name}"
        assert len(register.fields) > 0, f"NO Fields in register {register.name}"


def test_get_cregs_objects(rsl_svd_parser):
    cregs = rsl_svd_parser.get_cregs_objects()
    assert len(cregs) > 0, "No command registers found!"
    assert cregs[0].name == 'CREG_COM_SETTINGS', "First register name is incorrect!"


def test_find_register_by(rsl_svd_parser):
    reg = rsl_svd_parser.find_register_by(name='CREG_COM_SETTINGS')
    assert reg is not None, "NO CREG_COM_SETTINGS register found!"
    dreg_gyro_1_raw_z = rsl_svd_parser.find_register_by(address=87)
    assert dreg_gyro_1_raw_z is not None, "NO register with address 87 found!"

