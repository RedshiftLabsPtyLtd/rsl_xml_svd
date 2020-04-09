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
                 'regs': svd_parser.regs}
    render_template_to_file(reg_map_template, reg_map_out, param_dict)

    reg_addr_enum_template = os.path.abspath('templates/register_enum.h.jinja2')
    reg_addr_enum_out = 'shearwater_enum.h'
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'cregs': svd_parser.cregs,
                  'dregs': svd_parser.dregs,
                  'commands': svd_parser.commands}
    render_template_to_file(reg_addr_enum_template, reg_addr_enum_out, param_dict)

