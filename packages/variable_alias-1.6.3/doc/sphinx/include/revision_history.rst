Revision history
================

Version 1.6.3
-----------
* Updated lcf_utils version.

Version 1.6.2
-----------
* Bump lcf_utils

Version 1.6.1
-----------
* Bump lcf_utils

Version 1.6
-----------
* Added support for the LCF2INTG-XXX-2.0 formats (via lcf_utils 2.0).

Version 1.5.2
-------------
* Allow different programs to share code variable names when updating variable names.


Version 1.5.1
-------------
* Python 3 compatibility
* Fixed a bug when producing error message for regexp mismatch.

Version 1.5.0
-------------
* Replace lmc.AliasConfig.dump_config with getters for getting a Python
  representation of the configuration.
* Aliasing via files in LCF2Intg format is now officially supported.
* Fix crash in lmc.AliasConfig.rename_variables that occurred if a variable
  did not match any rules.

Version 1.4.2
-------------
* Bug fix: Support reading and dumping files containing non-ascii characters.


Version 1.4.1
-------------
  * Use lcf_utils 1.0.1 to fix crash when parsing RJSON on systems with a .NET framework < 4.7.1

Version 1.4.0
-------------

* Add experimental support for configuring aliasing using LCF2Intg files.

Version 1.3.2
-------------
Release date: Oct 19, 2017.

* If an excel file is requested but not found, a csv with the same name is used
  if present.
* A warning is issued if two configurations file with same name but different
  extension exist.


Version 1.3.1
-------------
Release date: Sep 11, 2017.

Minor improvements.

* Better error message.
* Configuration directory in package is also called "config" not "configuration".

Version 1.3
-----------
Release date: Mar 3, 2015.

* Added argument unused_fname to read_files(). If specified all unused rows
  in the code alias files will be written to file specified by unused_fname
  (relative to the code sub-folder in the project folder). The file format is
  a csv file with two columns: filename,linenumber.

Version 1.2
-----------
Release date: Oct 28, 2014.

* Added documentation.
* More default English instead of Swedish.
* PEP8 code.
* Fixed bug when output file was not written to disk.

Version 1.1
-----------
Release date: Sep 10, 2014.

* Use English instead of Swedish as default language.
* Added the warn_code_name_cb argument to provide a callback that determines
  if a warning should be issued when no matching variable alias can be found.

Version 1.0
-----------
Release date: Mar 6, 2014.

* Initial version.
