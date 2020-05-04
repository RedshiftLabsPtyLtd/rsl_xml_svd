import datetime
import os.path

from jinja2 import DictLoader, Environment

from rsl_svd_parser import RslSvdParser


def render_template_to_file(template_file: str, out_file: str, params_dict: dict):
    if not os.path.exists(template_file):
        raise FileNotFoundError("Template file to render is not found!")

    with open(template_file, 'r') as fd:
        RSL_HEADER = fd.read()

    template = Environment(loader=DictLoader({'RSL_HEADER': RSL_HEADER}))

    with open(out_file, 'w') as fd:
        fd.write(
            template.get_template('RSL_HEADER').render(
                params_dict
            )
        )


if __name__ == '__main__':
    today = datetime.datetime.now().strftime('%Y.%m.%d')
    svd_parser = RslSvdParser()

    reg_map_template = os.path.abspath('templates/register_map.h.jinja2')
    reg_map_out = 'shearwater.h'
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': svd_parser.regs,
                  'define_guard': 'RSL_SHEARWATER_REGISTER_MAP_H'}
    render_template_to_file(reg_map_template, reg_map_out, param_dict)

    reg_addr_enum_template = os.path.abspath('templates/register_enum.h.jinja2')
    reg_addr_enum_out = 'shearwater_enum.h'
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'cregs': svd_parser.cregs,
                  'dregs': svd_parser.dregs,
                  'commands': svd_parser.commands,
                  'define_guard': 'RSL_SHEARWATER_REGISTER_ENUM_H'}
    render_template_to_file(reg_addr_enum_template, reg_addr_enum_out, param_dict)

    reg_addr_enum_template = os.path.abspath('templates/python_reg_acces.jinja2')
    reg_addr_enum_out = 'shearwater_py_accessor.py'
    param_dict = {'version': 'v0.1',
                  'date': today,
                  'cregs': svd_parser.cregs,
                  'dregs': svd_parser.dregs,
                  'commands': svd_parser.commands}
    render_template_to_file(reg_addr_enum_template, reg_addr_enum_out, param_dict)

    #  HIDDEN_REGISTERS

    hidden_reg_map_template = os.path.abspath('templates/register_map.h.jinja2')
    reg_map_out = 'shearwater_hidden.h'
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': svd_parser.hidden_regs,
                  'define_guard': 'RSL_SHEARWATER_HIDDEN_REGISTER_MAP_H'}
    render_template_to_file(reg_map_template, reg_map_out, param_dict)

    reg_addr_enum_template = os.path.abspath('templates/register_hidden_enum.h.jinja2')
    reg_addr_enum_out = 'shearwater_hidden_enum.h'
    param_dict = {'version': 'v0.1',
                  'date': today,
                  'regs': svd_parser.hidden_regs,
                  'define_guard':  'RSL_SHEARWATER_HIDDEN_REGISTER_ENUM_MAP_H'}
    render_template_to_file(reg_addr_enum_template, reg_addr_enum_out, param_dict)

    reg_addr_enum_template = os.path.abspath('templates/python_hidden_reg_acces.jinja2')
    reg_addr_enum_out = 'shearwater_hidden_py_accessor.py'
    param_dict = {'version': 'v0.1',
                  'date': today,
                  'regs': svd_parser.hidden_regs}
    render_template_to_file(reg_addr_enum_template, reg_addr_enum_out, param_dict)

    reg_python_config_template = os.path.abspath('templates/python_shearwater_config.jinja2')
    reg_python_config_out = 'ShearwaterConfiguration.py'
    param_dict = {'hidden_regs': svd_parser.hidden_regs,
                  'config_regs': svd_parser.cregs,
                  'data_regs': svd_parser.dregs,
                  'command_regs': svd_parser.commands}
    render_template_to_file(reg_python_config_template, reg_python_config_out, param_dict)