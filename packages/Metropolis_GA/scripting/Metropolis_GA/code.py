#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#
"""
Prover iLock transition to Tools, phase 4: code
"""


# --------------------------------------------------------
# Imports
# --------------------------------------------------------
# Python and third party libraries
import os

# Import Prover iLock APIs
import CodeAPI
import PiSpecAPI
import ProjectAPI
import UtilityAPI
from prover.utils.split_universal import processRequirements

# Import Prover generic packages
from ilock_utils.utils import document_time
from ilock_utils.deviation_utils import set_deviation_name_attribute
from om_integration.api import IntegrationConfig
import rewriting.normal as normal
import rewriting.simplify as simplify
import rewriting.util
from variable_alias.lmc import AliasConfig
from debug_utils import normal_values

# Local imports

# --------------------------------------------------------
# Utility functions
# --------------------------------------------------------


def rename_variables():
    alias_cfg = AliasConfig()

    package_alias = os.path.join(
        ProjectAPI.PackageLocation(ProjectAPI.TopPackage),
        "config", "variablename.rjson")
    alias_cfg.set_package_alias_rules(package_alias)

    project_conf = os.path.join(ProjectAPI.Location, "config")
    project_alias = os.path.join(project_conf, "variablename.rjson")
    if os.path.exists(project_alias):
        alias_cfg.set_project_alias_rules(project_alias)
    project_instance_alias = os.path.join(project_conf,
                                          "instance-variablename.rjson")
    if os.path.exists(project_instance_alias):
        alias_cfg.set_project_instance_alias_rules(project_instance_alias)

    for prog in CodeAPI.Programs:
        alias_cfg.rename_variables(prog)

    return alias_cfg


def integrate(alias_cfg):
    intg_cfg = IntegrationConfig(CodeAPI.Programs, [ProjectAPI.TopPackage])
    intg_cfg.use_alias_configuration(alias_cfg)
    lcf2intg_proj_path = os.path.join(ProjectAPI.Location, "config",
                                      "LCF2IntgProj.rjson")
    if os.path.exists(lcf2intg_proj_path):
        intg_cfg.set_project_specific_integration(lcf2intg_proj_path)
    intg_cfg.integrate_safety_program()
    intg_cfg.store_config()



# --------------------------------------------------------
# Interface
# --------------------------------------------------------


def main():
    """
    Prepare the code for formal verification

    Set variable code names for non C targets.

    Set simulator initial values.

    Simplify programs equations.

    Add extra test cases in SEIF format.

    Split all safety requirements.
    """

    # Set variable code names
    alias_cfg = rename_variables()

    # Code import
    # this is the place for import

    # Add soft constraints
    normal_values.add_soft_constraints()

    # Do integration
    integrate(alias_cfg)

    # Do simplification
    for prog in CodeAPI.Programs:
        normal.normalize_equations(prog)
        # simplify.simplify_equations(prog)

    # Set deviation name attribute
    set_deviation_name_attribute()

    # Split all safety properties in all GSS classes
    document_time(
        lambda: processRequirements(
            [cl.Name for cl in PiSpecAPI.GSSClasses]),
        "Time [code.py: _split_properties()]",
        issue_log_note=False)

    # Run MQTT generation script
    import documenter_module.mqtt_config


document_time(
    main,
    "Time [code.py: main()]",
    issue_log_note=True)
