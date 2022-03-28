# RSL XML SVD

[![lint and test](https://github.com/RedshiftLabsPtyLtd/rsl_xml_svd/actions/workflows/test.yml/badge.svg)](https://github.com/RedshiftLabsPtyLtd/rsl_xml_svd/actions/workflows/test.yml)

## About this repo

This repo holds the SVD description of the **Redshift Labs Pty Ltd**
`UM7`, `UM8`, and `shearwater` register maps and the tools to work with this description.

The repo overview:

* [`./test`](./test) are [`pytest`](https://docs.pytest.org/en/latest/) tests for the repo;
* [`./RSL-SVD.xsd`](./RSL-SVD.xsd) is SVD (**s**ystem **v**iew **d**escription) XML schema with our extensions;
* [`./pytest.ini`](./pytest.ini) is pytest configuration (all test have the `svd` mark);
* [`./README.md`](./README.md) the file you are currently reading;
* [`./rsl_svd_parser.py`](./rsl_svd_parser.py) python XML parser in *dataclasses*;
* [`./shearwater.svd`](./shearwater.svd) is the `SVD` file for the `shearwater` register map;
* [`./um7.svd`](./um7.svd) is the `SVD` file for the `UM7` register map;
* [`./um8.svd`](./um8.svd) is the `SVD` file for the `UM8` register map;
* [`./svd_stylesheet.xsl`](./svd_stylesheet.xsl) stylesheet for the SVD schema.

## What is SVD and why we use it

For the `um7`, `um8`, `shearwater` boards we use the SVD-like peripheral description
format to describe the register map.
The SVD (or **S**ystem **V**iew **D**escription) is a standard way used by ARM in 
CMSIS (Arm **C**ortex **M**icrocontroller **S**oftware **I**nterface **S**tardard)
to describe the memory mapped registers of peripherals.
The advantage of using such a description (against our re-invented one) that
when the description is compliant with the SVD schema, we can benefit from
the existing tools to generate the C-defines/C-structs 
from the SVD description, essentially using such description
as a live data sheet for the user.

## SVD Format Basics

SVD format essentially describes the register map, which essentially a
user interface for the sensor. 

Each `register` comprises of the following elements:

* `name`: register name as from the register map;
* `description`: register description summary;
* `access`: one of `read-only` / `write-only` / `read-write` access type;
* `address`: address of register in a device (in RedshiftLabs Pty Ltd boards 
the 4-byte words are addressable, not single bytes, e.g. first 4-byte register
has address 0, second 4-byte register has address 1, etc.);
* `fields`: a set of register fields.

Each `field` in the register includes the following information:

* `name`: field name as from the register map;
* `description`: field description text;
* `bit_range`: start and end bit positions, e.g. `[0,7]` is 8-bit wide field, `[1,1]` is 1-bit field;
* `data_type`: one of `bitField` / `uint8_t` / `int8_t` / `uint16_t` / `int16_t` / 
`uint32_t` / `int32_t` / `float` / `string`. The `bitField` type used for fields that 
hold arbitrary-bit size settings (usually as enums), and cannot be interpreted as `c`-types, 
the `string` is a 4-character content, which denotes code;
* `access`: one of `read-only` / `write-only` / `read-write` access type;
* `enumerated_values`: values for enums of type `bitField`;

Each entry in the `enumerated_values` consists of:
* `name`: is the actual setting of the enum, e.g. "10_hz", 
`name` **should not include spaces or special characters**, as it is used in the 
code generation; 
* `description`: description of this setting (e.g. "10 Hz transmission rate");
* `value`: is an actual bit value, which shall be written in the register.


## Our SVD extensions

We extended the SVD schema to hold additional information about the data type for 
each field, e.g. `DREG_GYRO_1_RAW_XY` hold two fields `GYRO_1_RAW_X` and `GYRO_1_RAW_Y` each of type 
`int16_t`.

## More on SVD

The SVD is essentially XML description of the peripherals, the details
can be found [here](https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html).

We also provide description of the SVD tools from arm in the 
[svd how-to page](./SVD_HOWTO.md).


## Maintainer

[Dr. Konstantin Selyunin](http://selyunin.com/), for
suggestions / questions / comments please contact: selyunin [dot] k [dot] v [at] gmail [dot] com