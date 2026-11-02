=============
Documentation
=============

This package contains generic utility functions that can be used when
developing Prover iLock packages.


Revision history
================

Version 3.0
-----------

* Added deviation_utils module for deviation related utils, e.g.
  setting "deviation name" attribute.
* The function package_folder has been changed so that it does
  not try to to create a folder if it does not exist.
* Python 3 compatibility

Version 2.0
-----------

* The expression_parser has been moved to the bool_expression_parser
  package.

Version 1.4.2
-----------

* Added simple expression parser for reading snippets of code e.g.
  in config files.
* Added module for generating SHA-1 sums for files.


Version 1.4.1
-----------

* Add ignore_instances optional parameters to check_cardinality


Version 1.4
-----------

* Added get_match, for retrieving the first matching tuple.
* Convenience method for sorting by PiInstance.Name.
* Added get_matches function that is a nicer interface to the GetMatches function in the GeneratorAPI.
* Added function for shifting to lowercase also åäö.
* Added module with common checks.


Version 1.3.1
-------------

* Removed dependency on package dialogs. Removed "Session",
  "refine_folder", and "open_folder_if_desired" from utils.py.


Version 1.3
-----------
* tools_scripts.py

  - check_gss_function_documentation:
    Accept more patterns when detecting argument name in docstring

* pispec_instances.py

  - Fixed bug where an import of pispec_instances would throw an exception if
    the predicate gds_inst was not defined.


Version 1.2.1
-------------
.. 2016-05-16

* Added function for getting GSS/GVS pairs (in addition to GDS/GVS
  pairs) for visualization. Also opened up interface to enable getting
  other type pair combinations based on type name prefix matching.


Version 1.2
-----------

* export.py

  - New file, used to dump model(s) to file

* pispec_instances.py

  - Functions to return sensible default GDS/GTS and GDS/GVS pairs

  - Functions to warn for missing gts or gvs pairs

* tools_scripts.py

  - New file, functionality to warn if a GSS contains bad docstrings
    (does not mention the parameters to the function)

* utils.py

  - Imported update_kv_list from demo package

* visualization.py

  - New file, has functions for setting interactive objects

