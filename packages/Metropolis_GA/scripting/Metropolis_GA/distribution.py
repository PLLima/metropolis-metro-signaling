#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Prover iLock transition to Tools, phase 3: distribution
"""

import os

import PiSpecAPI
import UtilityAPI
import ProjectAPI

import prover.specification.types as T
import prover.specification.parameters as P
import prover.specification.functions as F

from ilock_utils.utils import document_time
from ilock_utils.visualization import set_interactive_object
import ilock_utils
from GeneratorAPI import GetAllInstancesTransitive as GIT
from GeneratorAPI import CreateInstance as CI
from PredefinedAttributes import (ATTRIBUTE_SORT_ORDER,
                                  ATTRIBUTE_VERIFIER_SEQUENTIAL_TIMER_LOCATION,
                                  VALUE_AFTER_INPUTS,
                                  VALUE_IN_PLACE)

from Metropolis_GA.typecheck import typedoc

# ------------------------------------------
# Utility functions
# ------------------------------------------


@typedoc
def _distribute(code_container):
    """
    Put all GDS class instances on the supplied code container,
    as well as the code container itself.

    Note: a code container has to contain at least one
    object (such as itself); otherwise, no code program
    will be created for the code container.

    @type code_container: PiInstance
    """
    P.contains.SetValue(True, code_container, code_container)

    gds_names = set(cl.Name for cl in PiSpecAPI.GDSClasses)
    for obj in GIT(T.OBJECT):
        if obj.Type.Name in gds_names:
            P.contains.SetValue(True, code_container, obj)


@typedoc
def _get_code_container():
    """
    Create a code container and return it.

    If no LOCATION object exists, create one with same name as project.

    @rtype: PiInstance
    """
    cc_name = ProjectAPI.Name
    cc = CI(T.CODE_CONTAINER, cc_name)
    return cc


@typedoc
def _set_sort_string(code_container):
    """
    @type code_container: PiInstance
    """
    fname = os.path.join(ProjectAPI.PackageLocation(ProjectAPI.TopPackage),
                         "config", "distribution_sort_order.csv")
    if os.path.exists(fname):
        class_order = [line.strip() for line in open(fname)]
    else:
        class_order = ""

    # Sort by user defined class name, then instance name,
    # then module position
    if class_order:
        class_string = "[" + ", ".join(class_order) + "]"
    else:
        class_string = ""
    sort_string = "$c %s ( $i ( ExecutionOrder ( $f )))" % class_string

    code_container.SetAttribute(ATTRIBUTE_SORT_ORDER, sort_string)


def _set_timer_model(cc):
    cc.SetAttribute(ATTRIBUTE_VERIFIER_SEQUENTIAL_TIMER_LOCATION,
                    VALUE_AFTER_INPUTS)


# ------------------------------------------
# Main function
# ------------------------------------------

def main():
    """
    Distribute the PiSPEC instances in the code container

    Create a code container named after the LOCATION.

    Put all GDS instances on the code container.

    Set the execution model and the execution time.

    Set the distribution evaluation order.

    Set interactive simulation attributes.
    """
    cc = _get_code_container()
    _distribute(cc)
    ilock_utils.utils.set_code_container_attributes(cc)
    _set_timer_model(cc)
    _set_sort_string(cc)


document_time(
    main,
    "Time [distribution.py: main()]",
    issue_log_note=True)
