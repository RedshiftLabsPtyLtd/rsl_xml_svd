# RSL XML SVD

## About this repo

This repo holds the SVD description of the **Redshift Labs Pty Ltd**
`shearwater` register map and the tools to work with this description.

The repo overview:

* [`./templates`](./templates) holds `jinja2` template files for `C/C++` header generation;
* [`./test`](./test) are `pytest` tests for the repo;
* [`./CMSIS-SVD.xsd`](./CMSIS-SVD.xsd) is XML schema with our extensions;
* [`./pytest.ini`](./pytest.ini) is pytest configuration (all test have a mark);
* [`./README.md`](./README.md) the file you are currently reading;
* [`./rsl_reg_map_generator.py`](./rsl_reg_map_generator.py) is a template creation script;
* [`./rsl_svd_parser.py`](./rsl_svd_parser.py) python XML parser in *dataclasses*;
* [`./shearwater.svd`](./shearwater.svd) is the `SVD` file for the `shearwater` register map;
* [`./svd_stylesheet.xsl`](./svd_stylesheet.xsl) stylesheet for the SVD schema.

## What is SVD and why we use it

For the `shearwater` board we use the SVD-like peripheral description
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
* `address_offset`: address offset of register from 0 in **bytes**, i.e. `address * 4`;
* `fields`: a set of register fields.

**TODO**: extend / change schema to use the address directly, instead of 
address offset.

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

## SVDConv tool from ARM

**TL;DR**: you do not need to read this section. Currently we use our own generator
and our code generation is entirely python based. This is how we started.

The `SVDConv` tool from ARM can be used to validate the SVD description 
and generate defines and structs from SVD descriptions.
The tool can be downloaded from the 
[CMSIS_5](https://github.com/ARM-software/CMSIS_5/) repo, and 
essentially in 
[CMSIS/Utilities/Linux-gcc-4.8.3/SVDConv](https://github.com/ARM-software/CMSIS_5/blob/develop/CMSIS/Utilities/Linux-gcc-4.8.3/SVDConv)
section of the repo.
The file shall be donwloaded using the `git lfs`.

Since we did extend the `SVD` description for the `shearwater` with the 
data type information (which is no longer is CMSIS conform), when invoking
`SVDConv` tool on the latest version of the `shearwater.svd` the program 
will fail. This is expected, since the extensions we did are not 
present in original `CMSIS.xsd` schema.

We though saved the CMSIS-confirm version of the file,
for which the `SVDConv` can be used with the tag: `shearwater-svd-cmsis-conform`.
If you want to experiment with the `SVDConv` tool, check out the above tag, 
and proceed as described below.

The `SVDConv` tool can be used as described below.

Generate enums (replace `/path/to/` with paths relative to your PC):

```sh
/path/to/SVDConv /path/to/shearwater.svd -o /path/to/out/folder -b /path/to/log --generate=header --debug-headerfile --fields=enum 
```

Generate macros:

```sh
/path/to/SVDConv /path/to/shearwater.svd -o /path/to/out/folder -b /path/to/log --generate=header --debug-headerfile --fields=macro 
```

Generate structs:

```sh
/path/to/SVDConv /path/to/shearwater.svd -o /path/to/out/folder -b /path/to/log --generate=header --debug-headerfile --fields=struct 
```

Generate ANSI-C type structs:

```sh
/path/to/SVDConv /path/to/shearwater.svd -o /path/to/out/folder -b /path/to/log --generate=header --debug-headerfile --fields=ansic 
```
