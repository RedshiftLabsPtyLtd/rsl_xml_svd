import datetime
import os.path

from jinja2 import DictLoader, Environment

from rsl_svd_parser import RslSvdParser

if __name__ == '__main__':
    template_file = os.path.abspath('templates/register_map.h.jinja2')
    today = datetime.datetime.now().strftime('%Y.%m.%d')

    with open(template_file, 'r') as fd:
        RSL_HEADER = fd.read()

    template = Environment(loader=DictLoader(globals()))
    svd_parser = RslSvdParser()
    regs = svd_parser.regs

    print(template.get_template('RSL_HEADER').render(
            {'version': 'v0.1',
             'date': today,
             'regs': regs}
        )
    )

