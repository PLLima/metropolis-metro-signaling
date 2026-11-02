Package Input
=============

The inputs to the variable_alias module are two configuration files and any
CodeName attributes found in the PiSpec classes.

The configuration files are either in .xls or .csv format and comes in two flavors,
one is generic and should be located in the package_folder/configuration folder and
the other should be located in the project_folder/config folder and is project
specific.

An example input csv file is found below::

  Object,Variable,Pattern,Name,Comment
  TRACK_CIRCUIT,VACANT,(.*),\1.VACANT,Comment #1
  S1:S2,SET,.*,S1S2.SET,Comment #2

The two examples above illustrate the two different use cases:

* In the first case a regular expression pattern is used to name all variables VACANT for all objects
  of type TRACK_CIRCUIT to a object specific name (\1 in the Name column is the first match group
  in the regular expression in the Pattern column).
* In the second case instead of matching all objects of a certain type we match an object with
  a specific name and omit using any \1 or similar in the name pattern since we are re-naming
  a specific instance.
