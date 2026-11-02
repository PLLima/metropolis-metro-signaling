# Copyright (C) 2018 Prover Technology, All Rights Reserved

"""
Package entry point: create railyard entities and PiSPEC instances.
"""

# ------------------------------------------------------------------------------
# Standard libraries imports
# ------------------------------------------------------------------------------
import sys
import os.path

# ------------------------------------------------------------------------------
# Prover iLock imports
# ------------------------------------------------------------------------------
import GeneratorAPI
from PredefinedAttributes import ATTRIBUTE_PROJECT_TREE_PATH
import ProjectAPI
import RailyardFactory
import UtilityAPI

# ------------------------------------------------------------------------------
# Package imports
# ------------------------------------------------------------------------------
from iLock_Geography.lcf.parse import (parseLCF2Inst,
                                       InstRule)
from iLock_Geography.geo_error import GeoError


def translate_rules(rules, prefix, skip_unmatched):
    """
    Translate the supplied rules to instead instantiate classes with
    the given prefix added to the type name.

    @type prefix: str
    @param prefix: The prefix to add to the user-types in the translated rules.
    @type skip_unmatched: bool
    @param skip_unmatched: If true, the rules for which there is no matching
      class with the given prefix are ignored. Otherwise, the rules are
      included in the output unchanged (without the prefix).
    """
    existing_types = set((t.Name for t in GeneratorAPI.GetAllTypes()))
    new_rules = []
    for rule in rules:
        new_type_name = prefix + rule.destTypeName
        if new_type_name in existing_types:
            # Replace rule by adding prefix
            designRule = InstRule(rule.source, rule.userType,
                                  new_type_name, rule.filter,
                                  rule.category)
            new_rules.append(designRule)
        elif not skip_unmatched:
            # Use unchanged rule
            new_rules.append(rule)
        else:
            # Skip this rule
            pass

    return new_rules


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------
def setup(lcf2pis):
    """
    Instantiate PiSPEC.
    """
    pack = ProjectAPI.PackageLocation(ProjectAPI.TopPackage)
    conf = os.path.join(pack, "Prover-iLock-config")
    try:
        # For every rule in OM, create a corresponding GDS rule
        # for instanting the GDS_ class instead of the OM class.
        om_lcf2inst = os.path.join(conf, "LCF2Inst.lmc")
        user_type_to_inst_rules = {}
        for userType, rules in parseLCF2Inst(om_lcf2inst).items():
            inst_rules = translate_rules(rules,
                                         prefix="GDS_",
                                         skip_unmatched=False)
            user_type_to_inst_rules[userType] = inst_rules
        lcf2pis.addLCF2Inst(user_type_to_inst_rules)
    except GeoError as e:
        UtilityAPI.LogError(
            "Design package LCF setup failed:%s" % e.message)
        sys.exit()
