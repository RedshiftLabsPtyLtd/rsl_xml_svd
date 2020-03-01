import xml.etree.ElementTree as ET

root = ET.parse('./shearwater.svd').getroot()

regs = root.findall('.//register')

cregs = [el for el in regs if 'CREG' in el.find('./name').text]

dregs = [el for el in regs if 'DREG' in el.find('./name').text]

commands = [el for el in regs if int(el.find('./addressOffset').text, 16) / 4 >= 0xAA]