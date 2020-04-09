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


@pytest.mark.svd
def test_find_by_field_position(rsl_svd_parser: RslSvdParser):
    cregs_6: Register = rsl_svd_parser.find_register_by(name='CREG_COM_RATES6')
    assert type(cregs_6) == Register, "Expect to find `Register` type from the register map"
    assert cregs_6.name == 'CREG_COM_RATES6', f"Expect to find `CREG_COM_RATES6`, got {cregs_6.name}"
    found_field = cregs_6.find_field_by(bit_position=0)
    assert found_field.name == 'GYRO_BIAS_2_RATE', f"Expect `GYRO_BIAS_2_RATE`, got {found_field}"
    found_field = cregs_6.find_field_by(bit_position=16)
    assert found_field.name == 'HEALTH_RATE', f"Expect `HEALTH_RATE`, got {found_field}"
    found_field = cregs_6.find_field_by(bit_position=23)
    assert found_field is None, f"Expect `None` at this bitfield, got {found_field}"


@pytest.mark.svd
def test_get_fields_and_gaps(rsl_svd_parser: RslSvdParser):
    creg_rates6: Register = rsl_svd_parser.find_register_by(name='CREG_COM_RATES6')
    result = creg_rates6.get_fields_and_gaps()
    expected_creg_rates6 = [{'GYRO_BIAS_2_RATE': 8}, {'GYRO_BIAS_1_RATE': 8}, {'HEALTH_RATE': 4}, {None: 4}, {'POSE_RATE': 8}]
    assert result == expected_creg_rates6, f"Incorrect fields/gaps for {creg_rates6.name}, got: {result}"

    creg_settings: Register = rsl_svd_parser.find_register_by(name='CREG_COM_SETTINGS')
    result = creg_settings.get_fields_and_gaps()
    expected_creg_settings = [{None: 28}, {'BAUD_RATE': 4}]
    assert result == expected_creg_settings, f"Incorrect fields/gaps for {creg_settings.name}, got: {result}"

    creg_rates4: Register = rsl_svd_parser.find_register_by(name='CREG_COM_RATES4')
    result = creg_rates4.get_fields_and_gaps()
    expected_creg_rates4 = [{'ALL_PROC_RATE': 8}, {None: 16}, {'PROC_MAG_2_RATE': 8}]
    assert result == expected_creg_rates4, f"Incorrect fields/gaps for {creg_rates4.name}, got: {result}"

    creg_rates5: Register = rsl_svd_parser.find_register_by(name='CREG_COM_RATES5')
    result = creg_rates5.get_fields_and_gaps()
    expected_creg_rates5 = [{'VELOCITY_RATE': 8}, {'POSITION_RATE': 8}, {'EULER_RATE': 8}, {'QUAT_RATE': 8}]
    assert result == expected_creg_rates5, f"Incorrect fields/gaps for {creg_rates4.name}, got: {result}"

    dreg_gyro_1_raw_xy: Register = rsl_svd_parser.find_register_by(name='DREG_GYRO_1_RAW_XY')
    result = dreg_gyro_1_raw_xy.get_fields_and_gaps()
    expected_dreg_gyro_1_raw_xy = [{'GYRO_1_RAW_Y': 16}, {'GYRO_1_RAW_X': 16}]
    assert result == expected_dreg_gyro_1_raw_xy, f"Incorrect fields/gaps for {dreg_gyro_1_raw_xy.name}, got: {result}"

    dreg_mag_1_raw_x: Register = rsl_svd_parser.find_register_by(name='DREG_MAG_1_RAW_X')
    result = dreg_mag_1_raw_x.get_fields_and_gaps()
    expected_dreg_mag_1_raw_x = [{'MAG_1_RAW_X': 32}]
    assert result == expected_dreg_mag_1_raw_x, f"Incorrect fields/gaps for {dreg_mag_1_raw_x.name}, got: {result}"
