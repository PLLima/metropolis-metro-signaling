=============
Documentation
=============

The rewriting package is a library of general term rewriting rules of
Boolean algebra. Every rule rewrites a Boolean expression to an
equivalent Boolean expression. It can be used to obtain simpler
Boolean expressions either to make them easier to read or to
make them easier to execute.

The package contains a single Python module rewriting.simplify, and nothing else.

The content of the package is owned by Prover Technology AB.

Package Input
=============

The rules operate on the internal code model of Prover iLock.

Package Output
==============

There is no "output" in the sense of created data, rather the data
used as input is being changed by the package.

Package Content
===============

There are simple rewriting rules that typically solve one isolated problem.

There are also rewriting strategies, typically consisting of a number
of calls to simple rewriting rules, performed in a certain way to
obtain an optimal result.

Package Usage
=============

Import the python module rewriting.simplify offered by the package and
call one or several of the offered functions to simplify expressions.

Revision history
================

Version 1.9.3
-------------

* Ignore abstract equations

Version 1.9.2
-------------

* Ignore integer valued equations

Version 1.9.1
-------------

* Python 3 compatibility

Version 1.9
-----------

    * Critical bug fix to COND support; rewrite would sometimes not be
      equivalent. COND expressions were treated as variables in some
      places and operators in some. Now COND are eliminated before
      rewriting, just like PRE, so they are consistently treated as
      variables.

Version 1.8.1
-------------

    * Bug fix. Parts of expressions that contain operator COND can get
      lost in factorise (#8327).

Version 1.8
-----------

    * Support the COND operator.

Version 1.7.1
-------------

   * Bug fix.

Version 1.7
-----------

   * Added simplify.factorise_negations which collects negated parts
     using fewer negations.

Version 1.6
-----------

   * Functionality to rename variables in 'tecla_str' has been added.
     A bug was fixed in 'conjunctiveSplit', now the 'bound' argument
     works as intended.

Version 1.5
-----------

   * Function propagate_variables in program.simplify is much faster
     and takes three arguments: the first argument is the program to
     evaluate constants in, the second (optional) argument is a list
     of programs to simplify given the constant values (default
     consisting only of the first argument), and the third (optional)
     argument is True/False (default False) deciding if an additional
     absorbtion should be made in the end.
