# RSL XML SVD

## About this repo

This repo is supposed to hold the SVD description of the `shearwater`
register map and the tools to work with this description.

## What is SVD and why we want to use it

For the `shearwater` board we will use the SVD-like peripheral description
format to describe the register map.
The SVD (or **S**ystem **V**iew **D**escription) is a standard way in 
CMSIS (Arm **C**ortex **M**icrocontroller **S**oftware **I**nterface **S**tardard)
to describe the memory mapped registers of peripherals.
The advantage of using such a description (against our re-invented one) that
when the description is compliant with the SVD schema, we can benefit from
the existing tools to generate the C-defines/C-structs 
from the SVD description, essentially using such description
as a live data sheet for the user.

## More on SVD

The SVD is essentially XML description of the peripherals, the details
can be found [here](https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html).

The `SVDConv` tool from ARM to validate the SVD description and generate 
defines and structs from SVD descriptions is available in the 
[CMSIS_5](https://github.com/ARM-software/CMSIS_5/) repo, and 
essentially in 
[CMSIS/Utilities/Linux-gcc-4.8.3/SVDConv](https://github.com/ARM-software/CMSIS_5/blob/develop/CMSIS/Utilities/Linux-gcc-4.8.3/SVDConv)
section of the repo.

In addition to this tool, we also plan to create the tool to create the 
JSON description from the XML, which will be used by our python driver.

