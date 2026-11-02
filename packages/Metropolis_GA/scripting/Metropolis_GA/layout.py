#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Prover iLock transition to Tools, phase 1: PiSPEC instantiation
"""

# ------------------------------------------
# Imports
# ------------------------------------------

from ilock_utils.utils import document_time
from ilock_utils.visualization import set_interactive_object
from iLock_Geography import railyard_import
from iLock_Geography.lcf.api import LCFWorkflow

import prover.specification.types as T
import prover.specification.parameters as P
import prover.specification.functions as F

import railyard.main
import lcf.tables
import lcf.om
import lcf.gds
import lcf.gts
import lcf.gvs
import checks


# ------------------------------------------
# Helpers
# ------------------------------------------

def _set_interactive_simulation_attributes():
    """
    Sets attributes used for interactive simulation.
    - The attribute for "interactive object" is used for objects that
      do not have an immediate representation in the railyard. Typically
      it is used for routes for which the start signal is used as the
      "interactive object". This makes it possible to access the
      interactive features of the route by right-click the start signal.
    """
    # @TEMPLATE_PKG_REMOVE_BEGIN@
    # @TEMPLATE@ Reference to explicit PiSPEC names
    set_interactive_object(T.ROUTE, [(P.start_signal, T.SIGNAL), ])
    set_interactive_object(T.GTS_ROUTE, [(P.gds_inst, T.ROUTE),
                                         (P.start_signal, T.SIGNAL)])
    # @TEMPLATE_PKG_REMOVE_END@


# ------------------------------------------
# Interface
# ------------------------------------------

def main():
    """
    Adjust railyard, then
    generate OM, GDS, GTS, and GVS PiSPEC instances.
    """
    # The drawn railyard is often not enough and the script railyard.main
    # can be used to finalize the railyard; for example by cleaning
    # up, renaming objects, generating paths and areas, etc.
    #   As a side effect some LCF tables may be generated in the
    # process. This is useful when there are relations between objects
    # that are not easy to express using the ordinary table method
    # framwork but are easy to capture when the involved objects are
    # being generated (typically paths and areas).
    ry, tables = document_time(lambda: railyard.main.setup(),
                               "Time [setup railyard]")

    # Import other configuration data and translate to LCF tables,
    # then append to list 'tables'
    pass

    # Set up the "LCF workflow" configuration object for collecting
    # lcf configuration from various sources.
    lcf2pis = LCFWorkflow(ry, importedLayout=False,
                          useDefaultTypesFile=True)
    lcf2pis.modifyRailyard(lambda r: r) # Triggers type check

    # Read primary LCF tables
    document_time(lambda: lcf.tables.setup(lcf2pis, generated_tables=tables),
                  "Time [setup LCF tables]")

    # Collect LCF configuration
    document_time(lambda: lcf.om.setup(lcf2pis, instantiate_pispec=False),
                  "Time [setup OM]")
    document_time(lambda: lcf.gds.setup(lcf2pis),
                  "Time [setup GDS]")
    document_time(lambda: lcf.gts.setup(lcf2pis),
                  "Time [setup GTS]")
    document_time(lambda: lcf.gvs.setup(lcf2pis),
                  "Time [setup GVS]")

    # Do the instantiation based on all configuration collected above
    document_time(lcf2pis.run,
                  "Time [instantiation]")
    checks.main()

    # Post instantiation setup
    _set_interactive_simulation_attributes()


document_time(main,
              "Time [layout.py: main()]")
