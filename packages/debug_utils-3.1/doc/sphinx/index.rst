=============
Documentation
=============

This package contains utility functions for noise reduction in counter
examples.

Typical usage is to add these calls to code.py:

  normal_values.add_soft_constraints()
  soft_constraints.add_soft_constraints()

This adds normal value soft constraints plus general soft constraints
to the SafetyProgram. Each variable can only have one specified normal
value, but an arbitrary number of soft constraints can be added.
General soft constraints is a more generic mechanism, but also a bit
more verbose.

Configuration of normal values
==============================

The configuration required is for the package to define "normal
values" for variables in the package. The normal values can be
configured in a number of ways:

- through a default that is applied to all input variables in the
  design this default is given as an argument to the main function of
  the normal_values.py module.

- through PiSPEC functions. The normal value is often dynamic; e.g.
  for a lamp proving input, the "normal value" is for the input to be
  equal to the corresponding output (possibly with a delay). To
  specify this type of dynamic normal values, in the absence of
  dynamic attributes, PiSPEC functions are used. A unary PiSPEC
  function named normal__X (e.g. a variable name prefixed by
  "normal__") in GDS or GSS class Y will be interpreted as defining
  the normal value of PiSPEC variable X in that class. The function
  value is the normal value and if the function is abstract the normal
  value is "don't care". Explicitly setting the normal value to "don't
  care" is useful for variables that would otherwise use the default
  normal value.

- through attributes (set from PiSPEC or python). The attribute name
  is NormalValue (can be found in the attributes.py module). The value
  of the attribute can be the ToString() representation of a CodeAPI
  expression, or the special values "True", "False", or "DONT_CARE".

The order of priority of these alternatives is given by the order in
this list; PiSPEC functions override the default and the attribute
overrides both.

Configuration of general soft constraints
=========================================

Soft constraints are configured using PiSPEC functions (in lieu of a
built in PiSPEC construct).

Soft constraints are specified per class. The constraint is added for
all instances of the class. A unary, boolean PiSPEC function named
soft_constraint__X (e.g. an arbitrary name for the constraint prefixed
by "soft_constraint__") in GDS or GSS class C will result in a soft
contraint expression added per instance of type C. By adding multiple
identical soft constraints (with different names) the weight of the
constraint can be increased.

Revision history
================

Version 3.1
-----------
- Remove inefficiency in normal value attribute parsing.
- Bugfix in the setting default normal value

Version 3.0
-----------

- Support for normal values for integer variables
- Support for more general "soft constraints"

Version 2.0.3
-------------

- Bump bool_expression_parser

Version 2.0.2
-------------

- Bump bool_expression_parser

Version 2.0.1
-------------

- Prevent error for normal values that have been assigned generically to
  objects that have not been instantiated

Version 2.0
-----------

- Added function for adding normal values as "soft constraints".
- Removed old "noise reduction" prototype in favor of new built-in
  support for soft constraints.

Version 1.3.1
-------------

- Python 3 compatibility

Version 1.3
-----------

- Noise report generation stopped working after a change in Prover
  iLock around v5.1.1. Now fixed.

Version 1.2
-----------

- Added "noise report"
- Bugfix; ignore variables outside system model
- Support for debugging "deviation relevance analysis" POs

Version 1.1
-----------

- Abstract functions can be used to specify "don't care" values.

Version 1.0
-----------

- First version.
