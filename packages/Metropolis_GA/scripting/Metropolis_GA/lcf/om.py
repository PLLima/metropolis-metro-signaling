# Copyright (C) 2018 Prover Technology, All Rights Reserved

"""
Package entry point: create railyard entities and PiSPEC instantiation rules.
"""

# ------------------------------------------------------------------------------
# Standard libraries imports
# ------------------------------------------------------------------------------
import os.path
import sys
# import clr

# ------------------------------------------------------------------------------
# Prover iLock imports
# ------------------------------------------------------------------------------
import LCFTableAPI
import ProjectAPI
import UtilityAPI

# ------------------------------------------------------------------------------
# Package imports
# ------------------------------------------------------------------------------
from iLock_Geography.geo_algorithms import inObjIter
from iLock_Geography.geo_error import GeoError
from lcf_utils.tables import make_lcf_table
from geotypes import resolve_union_type

import table_methods

from Metropolis_GA.typecheck import typedoc


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------
@typedoc
def setup(lcf2pis, instantiate_pispec):
    """
    LCF setup. Adds railyard objects and LCF configuration.

    @param instantiate_pispec: If false, no instantiation rules are added.
      This is useful when a design package implementes the OM.
    @type instantiate_pispec: bool
    @type lcf2pis: LCFWorkflow
    """
    try:
        pack = ProjectAPI.PackageLocation(ProjectAPI.TopPackage)
        conf = os.path.join(pack, "Prover-iLock-config")

        # 1. Configure PiSPEC instantiation
        lcf2inst = os.path.join(conf, "LCF2Inst.lmc")
        lcf2pis.addInstanceValidationRules(lcf2inst)
        if instantiate_pispec:
            lcf2pis.addLCF2Inst(lcf2inst)

        # 2. Register table calculation rules
        table_methods.register_table_methods(lcf2pis)
        lcf2pis.addLCF2Tab(os.path.join(conf, "LCF2Tab.lmc"))

        # 3. Setup parameter rules
        lcf2pis.addLCF2Par(os.path.join(conf, "LCF2Par.lmc"))
    except GeoError as e:
        UtilityAPI.LogError(
            "Object model LCF setup failed: %s" % str(e))
        sys.exit()


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------
