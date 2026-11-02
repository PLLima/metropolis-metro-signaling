=============
Documentation
=============

This package is used for importing a Prover-iLock system
from a SEIF specification. And also for exporting such a system to a
SEIF specification.


The SEIF format itself has separate documentation, which can
be found in archive::

    <svn>/devel/Prover-iLock_Packages/SEIF_lib/trunk/doc/seif


The content of the package is owned by Prover Technology AB.

Package Input
=============

When the package is used for SEIF import, the input is a SEIF specification.
See the SEIF manual for the correct format. Typically the SEIF specification
has not been written manually but has been produced by a translator from
customer input.

Documentation and support libraries for translation to SEIF from customer
formats can be found in archive::

    <svn>/devel/to_seif_translators

Package Output
==============

When the package is used for SEIF export, the output is a SEIF specification.


Package Content
===============

Prover iLock Package for SEIF import/export.

Package Usage
=============

SEIF Export
-----------

Register an entry for exporting SEIF in <PKG>/scripting/scripts.xml
and install a script for performing the export in directory
<PKG>/scripting/tools_scripts. The script shall import the python
module ``code_export`` and call the public function ``main`` to export
the current contents of the CodeAPI. There are no mandatory arguments
but see the code documentation in code_export.py for optional
arguments. It is also possible to export only a subset of Prover iLock
programs, see documentation of the ``programNames`` parameter or to
export a singlle program (see the function ``exportProgram``).

Example usage::

  import iLock_SEIF.code_export

  ...
  iLock_SEIF.code_export.main()
  ...

SEIF Import
-----------

Import the ``code_import`` module from ``code.py`` and call the public
function ``main``. This function has two mandatory arguments, the path to
the SEIF file to import and a list of pairs (PiProgram, SEIF_ProgramName)
which defines which Prover iLock program that shall be extended with
the contents of a corresponding SEIF program.  If the first element of
the pair is ``None``, a new Prover iLock program is created from
the named SEIF program.

The import function has numerous optional arguments, see code
documentation in ``code_import.py`` for descriptions.

Example usage::

  import iLock_SEIF.code_import

  def main():
      ...
      _import_program_from_seif()
      ...

  def _import_program_from_seif():
      filename = os.path.join(
          ilock_utils.utils.project_folder("code_import"),
          "code.seif")
      ps = dict([(p.Name, p) for p in CodeAPI.Programs])
      pmap = [(ps["Program1"], "Program1"), (ps["Program2"], "Program2")]
      iLock_SEIF.code_import.main(
          filename, pmap,
          importOutputs=True,
          warnFreeOutput=False,
          replaceUnmatchedStub=iLock_SEIF.code_import.OK)


Revision history
================

Version 1.7.6
-------------
* Adding function for building standalone PiPrograms from an ast.

Version 1.7.5
-------------
* Python syntax and compatibility fixes.

Version 1.7.4
-------------
* Adding function for exporting single PiProgram to file
* Bug fixes in Python 3 compatibility.

Version 1.7.3
-------------
* Minor bug fix for the SEIF parser.

Version 1.7.2
-------------
* iLock_SEIF is now compatible with Python 3 and Python.NET.

Version 1.7.1
-------------
* Error messages from inconsistency check were hidden from user when running from iLock.

Version 1.7
-----------
* Moved some constants used in code_import to separate module ``constants``
  in order to enable these to be used in any Prover iLock phase.

* Added option ``ignoreDefinedInput`` to code_import to allow SEIF
  input and corresponding PiLock equation.

* Added option ``replaceInputWithEquation`` to code_import to allow PiLock
  input be overwritten by SEIF equation.

Version 1.6
-----------
* Implemented new C python parser for SEIF, which is to be used for
  standalone SEIF translation. The previous ANTLR-generated parser for
  C python was too inefficient to be used for larger inputs.

Version 1.5
-----------
* Implemented Timer Condition expression.

* Add script for parsing graphical representation of equations in GEIF.

Version 1.4
-----------
* Introduced ``code_import.import_ast`` to import an already parsed SEIF file.


Version 1.3.2
-------------
* Minor bugfixes for SEIF export


Version 1.3.1
-------------

* Add external program vars to Visualization Programs.
* Updated handling of feedbacks.
* Sorted external declarations.


Version 1.3
-----------

Changes to SEIF export:

* New parameter ``programNames`` which enables export of a subset
  of Prover iLock programs. If needed referred programs not in the
  subset are declared external to ensure that the exported SEIF file is
  consistent.

Changes to SEIF import:

* New parameter  ``replaceStubWithInput`` to enable replacement of a
  PiLock stub equation with a SEIF input.
* Corrections regarding the handling of externally declared programs
  and variables. It shall now work to import only the test or
  the safety program.
* Miscellaneous fixes regarding feedback variables.


Version 1.2.3
-------------
Bug fixes in consistency checker and enabling
parser to run with ipython without Prover iLock.

Version 1.2.2
-------------
Minor bug fixes.

Version 1.2.1
-------------
Cleanup of documentation and code comments.

Version 1.2
-----------
Slight change to the grammar for Visualization programs, which now
have a limited set of subsections.

Several changes to SEIF import:

* Several corrections connected to handling of external variables.
* Additions to merge also variable properties (``InstanceName`` and
  ``DesignName``).
* New flag ``replaceVarProperty`` for handling variable property
  collisions.
* Possibility for ignoring all postprocessing of stub equations, see
  option ``replaceUnmatchedStub``.
* Simplified call syntax for importing all SEIF programs and for
  merging all PiLock programs.

Version 1.1
-----------

Adding new optional program section ``EXTERNALS`` which allows to
declare and use variables and program names which is not declared
elsewhere in the SEIF specification. This allows to import SEIF fragments
into a Prover iLock system where the external names must instead be
found in the imported Prover iLock system. This addition is
backward compatible with earlier sections.

Version 1.0.2
-------------

Adding new script ``add_testcases.py`` to enable importing testcases
from a fragment SEIF file.  The SEIF file may be incomplete and refer
to variables which only exists in a PiLock system.

Version 1.0.1
-------------

Moving .dll-files to package-root/dll to make it compatible with encrypting
Prover-iLock packages.

Version 1.0
-----------

Initial version of package. Supports version 1.0 of the SEIF format.
