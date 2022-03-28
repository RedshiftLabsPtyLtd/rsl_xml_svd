
## SVDConv tool from ARM

**TL;DR**: you do not need to read this section, this is provided for consistency only. Currently we use our own generator
and our code generation is entirely python based.
We generate `C` headers and `python` accessors (i.e. *properties*) using `jinja2` templates. 

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
