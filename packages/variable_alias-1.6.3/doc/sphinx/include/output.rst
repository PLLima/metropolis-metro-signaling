Package Output
==============

All variables in the supplied PiProgram are re-named according to the given
configuration files and CodeName attributes.

All variable names are exported to the supplied out file name in the project_folder/code/ folder.
The output format is given below::

  Program    Code-variable    PiSpec-variable
  P0         FOO.BAR          FOO:BAR

In the example above the PiSpec-variable FOO:BAR has been given the alias
FOO.BAR in program P0.
