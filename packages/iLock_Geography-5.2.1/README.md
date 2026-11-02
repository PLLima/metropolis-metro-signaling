# Overview

This module contains a general framework for dealing with railyards having the IRailyard interface (as defined in Prover iLock). More specifically, it contains functionality for
 - searching and calculating (_geo\_algorithms_),
 - defining and using types (_geo\_type_ and _type\_manager_),
 - defining and using geographical predicates, i.e. python objects that behave
   as logical predicates (_geo\_predicate_, _predicate\_manager_), and
 - mapping IRailyard instances and geo predicates onto PiSPEC instances and
   predicates (_geo2pispec_).

It contains a library of geo_predicates (_predicate\_library_), of which some are pre-configured for direct use builtins.

It also contains various utilities, etc.
