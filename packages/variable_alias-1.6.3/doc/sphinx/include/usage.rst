Package Usage
=============

Call the variable_alias module in the code phase (code.py) supplied with the
name of the configuration files and the output file.

Example usage::

  import variable_alias.variable_name as variable_name
  outfname = "variablealiases.txt"
  fname = "variablealias.csv"
  renamer = variable_name.read_files(out_file=outfname,
                                     code_alias_local_file_name=fname,
                                     code_alias_file_name=fname)
  renamer.update_variable_names()

This will update the variable names according to the configuration files
found in project_folder/config/variableablias.csv,
package_folder/configuration/variablealias.csv and the CodeName attributes.

The list of program and variables and their old and new names will be written
to project_folder/code/variablealiases.txt.

