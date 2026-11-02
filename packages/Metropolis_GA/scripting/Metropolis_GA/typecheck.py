# (C) COPYRIGHT 2016 BY PROVER TECHNOLOGY AB, SWEDEN
# ALL RIGHTS RESERVED. THE USE OF THIS PRODUCT IS
# CONDITIONAL UPON AND SUBJECT TO THE TERMS OF A
# VALID LICENSE AGREEMENT WITH PROVER TECHNOLOGY.

try:
    import prover.types.railyard_types as ryTypes
except ImportError:
    pass
import prover.types.generic_types as gTypes
from prover.types.generator_types import PiType

from prover.types.typecheck.typecheck import Typechecker
import LCFTableAPI
import UtilityAPI
from GeneratorAPI import (CreateInstance, DeleteInstance)
import prover.specification.types as T

import clr
clr.AddReference("Prover-iLock-api")
from System.Collections.Generic import List
from Prover.LCF.API import TableCell

__all__ = ["typedoc"]

###############################################################################

# Switch that controls type checking of the geo package
ENABLE_TYPE_CHECK = UtilityAPI.ConfigurationValue("developer_mode") == "true"
###############################################################################


def _getAll(module):
    return {t: getattr(module, t) for t in module.__all__}


if ENABLE_TYPE_CHECK:
    # Dictionary for collecting types
    usertypes = {}

    # Collect generic types
    usertypes.update(_getAll(gTypes))
    del gTypes

    # Collect generator types
    usertypes["PiType"] = PiType
    inst = CreateInstance(T.CODE_CONTAINER, "_typecheck")
    usertypes["PiInstance"] = type(inst)
    DeleteInstance(inst)
    del PiType, CreateInstance, T, DeleteInstance

    # Add referenced types
    try:
        from iLock_Geography.lcf.api import LCFWorkflow
        from iLock_Geography.geo_type import GeoType

        # Collect railyard types
        usertypes.update(_getAll(ryTypes))
        del ryTypes

        usertypes["LCFWorkflow"] = type(LCFWorkflow(None, False))
        del LCFWorkflow

        usertypes["LCFTable"] = type(LCFTableAPI.CreateTable(
            "typecheck", List[List[TableCell]](), ""))

        usertypes["GeoType"] = type(GeoType("_typecheck", []))
        del GeoType
    except ImportError:
        pass

    # Create 'typedoc', a configured type checker
    typedoc = Typechecker(dotypecheck=ENABLE_TYPE_CHECK, usertypes=usertypes)

    del usertypes
else:
    def typedoc(x):
        return x

del _getAll, Typechecker, ENABLE_TYPE_CHECK
