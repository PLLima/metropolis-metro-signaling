#
# Copyright (C) 2018 Prover Technology, All Rights Reserved
#

"""
Defines package specific table methods.
"""
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from itertools import chain
from iLock_Geography.lcf.table_methods import (
    arguments,
    opt,
    CustomTableMethodImplementation
)



# ------------------------------------------------------------------------------
# Table methods
# ------------------------------------------------------------------------------


@arguments(attribute=str, boolean=opt(bool, False))
class AttributeT(CustomTableMethodImplementation):
    """
    Produces a table of two columns [object, value], where "value" is the
    value of the named attribute in object. The value can be e.g. the name
    of an object or an enum or integer value, depending on the declaration
    in the Types file. If argument 'boolean' is set, the produced table will
    have a single column with a row for each object with value "True".

    :param attribute: The name of the attribute to be read.
    :param boolean: If true, only value "True" is interpreted, producing a
       table with a single column.
    """
    def __init__(self, attribute, boolean):
        self.attribute = attribute
        self.boolean = boolean

    def rows(self):
        tabRows = set()
        for o in chain(
                (o for o in self.railyard.AuxiliaryObjects),
                (o for n in self.railyard.Graph.Nodes for o in n.Objects),
                (a for a in self.railyard.Areas),
                (p for p in self.railyard.Paths)):
            val = o[self.attribute]
            if self.boolean:
                if val == "True":
                    tabRows.add((o, ))
            else:
                if val is not None:
                    tabRows.add((o, val))

        return tabRows

    def arity(self):
        if self.boolean:
            return 1
        else:
            return 2


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------
def register_table_methods(lcf2pis):
    lcf2pis.addTableMethod("AttributeT", AttributeT)
# @TEMPLATE_PKG_REMOVE_BEGIN@
# @TEMPLATE_PKG_REMOVE_END@
