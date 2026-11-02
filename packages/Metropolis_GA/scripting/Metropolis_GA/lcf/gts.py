# Copyright (C) 2022 Prover Technology, all rights reserved

"""
Instantiate the Generic Test Specification (GTS) classes.
"""

import glob
import os

import ProjectAPI
import PiSpecAPI

from iLock_Geography.lcf.parse import (parseLCF2Inst,
                                       InstRule,
                                       ParRule)

from common import get_mirror_type_name


def setup(lcf2pis):
    # Generate GTS instances for all object model instances
    # for which a corresponding GTS class has been defined.
    pack = ProjectAPI.PackageLocation(ProjectAPI.TopPackage)
    om_lcf2inst = os.path.join(pack, "Prover-iLock-config", "LCF2Inst.lmc")
    gts_classes = _gts_class_names()
    class_prefix = "GTS_"
    user_type_to_inst_rules = {}
    pred_rules = []
    dest_type_names = set()
    for userType, rules in parseLCF2Inst(om_lcf2inst).items():
        inst_rules = []
        for rule in rules:
            dest_type_name = get_mirror_type_name(
                rule.destTypeName, gts_classes, class_prefix)
            if dest_type_name is None:
                continue
            if rule.category is None:
                category = "gts"
            else:
                category = "gts_" + rule.category
            instRule = InstRule(__file__, rule.userType, dest_type_name,
                                rule.filter, category)
            inst_rules.append(instRule)
            dest_type_names.add(dest_type_name)
        if inst_rules:
            user_type_to_inst_rules[userType] = inst_rules
    for dest_type_name in dest_type_names:
        pred_rules.append(ParRule(__file__, "gds_inst", "t_ID",
                                  dest_type_name, None))

    lcf2pis.addLCF2Inst(user_type_to_inst_rules)
    lcf2pis.addLCF2Par(pred_rules)


def _gts_class_names():
    return set((c.Name for c in PiSpecAPI.GTSClasses))
