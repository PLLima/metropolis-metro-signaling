#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Constant lists of railyard types

The idea is to abstract from railyard types.
"""

import LayoutEditorAPI
types = LayoutEditorAPI.GetCurrentLCFPackageData()

def resolve_union_type(union_type):
    """ Return list of base types in the given union type. """
    ut = types.GetUnionTypes()[union_type]
    return list((bt for bt in ut.UserBaseTypes))
