#! /usr/bin/env python
# -*- coding: latin-1 -*-
#
# FILE: crossovers.py
# CODE: Python
#
# Copyright (C) 2013-2014 Prover Technology, All Rights Reserved
#

"""
Creates crossover and diamond crossover objects,
(GenericOutside objects).
"""

# ------------------------------------------
# Imports
# ------------------------------------------

from collections import defaultdict

import UtilityAPI
from PredefinedAttributes import (
    ATTRIBUTE_PROJECT_TREE_PATH,
    ATTRIBUTE_HIGHLIGHTING_COLOR,
    ATTRIBUTE_BENT_LEG,
)

from iLock_Geography.geo_algorithms import (
    DirObj2DirObjPaths,
    graphObjIter,
    createArea)

from ..lcf.geotypes import resolve_union_type


CROSSOVER_AREA_TYPE = "g_crossover"
DIAMOND_CROSSOVER_AREA_TYPE = "g_dcrossover"
SWITCH_TYPES = resolve_union_type("RY_SWITCH")
SIGNAL_TYPES = resolve_union_type("RY_SIGNAL")
CROSSING_TYPES = resolve_union_type("RY_TRACK_CROSSING")


# ------------------------------------------
# Utility functions
# ------------------------------------------


def crossover_name(sw1, sw2):
    """
    Return the name of the crossover instance to be created for
    switches sw1 and sw2.

    :param sw1: railyard object instance
    :param sw2: railyard object instance
    :rtype: str
    """
    if not acceptable_crossover_name_pair(sw1.Name, sw2.Name):
        UtilityAPI.LogError("Incorrectly named switched in crossover "
                            "(switches: %s and %s)" % (
                                sw1.Name, sw2.Name))
        return ''
    else:
        names = sorted([sw1.Name, sw2.Name])
        name = "%s-%s:crossover" % (names[0], names[1])
        return name


def acceptable_crossover_name_pair(name1, name2):
    """
    The names are acceptable as a crossover pair.
    """
    return True


def dcrossover_name(co1, co2):
    """
    Return the name of the diamon crossover instance to be
    created for crossovers co1 and co2.

    :param co1: railyard object instance
    :param co2: railyard object instance
    :rtype: str
    """
    names = sorted([co1.Name, co2.Name])
    name = "%s-%s:diamond" % (names[0], names[1])
    return name


def __crossover_path_triple_condition(sw1, sw2, pt):
    """
    Only keep paths if they both are reverse/normal,
    and if both are left/right.
    """
    start_ni, edges, end_ni = pt
    start_i, end_i = start_ni.Index, end_ni.Index
    same_leftright = start_i == end_i

    start_reverse = int(sw1[ATTRIBUTE_BENT_LEG]) == start_i
    end_reverse = int(sw2[ATTRIBUTE_BENT_LEG]) == end_i
    same_reverse = start_reverse == end_reverse
    return same_leftright and same_reverse


def __crossover_path_edge_condition(processedNodeIndex, newNodeIndex, railyard):
    """
    When searching for crossovers, do not go past signals.
    """
    for obj in newNodeIndex.Node:
        if obj.Subtype in SIGNAL_TYPES:
            return False
    return True


# ------------------------------------------
# Interface
# ------------------------------------------

def generate(railyard, table_storage):
    """
    Build crossovers and diamond crossovers
    """
    # Crossovers are generated from paths from bent leg to bent leg
    pathgen = DirObj2DirObjPaths(
        railyard,
        branch=False,
        noSuffix=True,
        beginFacing=True,
        endFacing=False,
        gType=SWITCH_TYPES,
        edgeCondition=__crossover_path_edge_condition)
    done = set()
    crossovers = list()
    for path_triple in pathgen.generate():
        start_ni, edges, end_ni = path_triple
        sw1 = next(pathgen.startObjects(start_ni))
        sw2 = next(pathgen.endObjects(end_ni))
        if sw1 in done or sw2 in done:
            continue
        if (not acceptable_crossover_name_pair(sw1.Name, sw2.Name) or
            not __crossover_path_triple_condition(sw1, sw2, path_triple)):
            # Crossovers are only supposed to be generated for specially
            # named switch pairs.
            UtilityAPI.LogNote("crossovers.py: Skipping %s, %s"
                               % (sw1.Name, sw2.Name))
            continue

        # Create crossover area
        area = createArea(CROSSOVER_AREA_TYPE,
                          crossover_name(sw1, sw2),
                          edges=edges)
        area[ATTRIBUTE_PROJECT_TREE_PATH] = "Design/Crossovers"
        area[ATTRIBUTE_HIGHLIGHTING_COLOR] = "Red"
        railyard.Areas.Add(area)
        crossovers.append(area)
        done.add(sw1)
        done.add(sw2)

    # Diamond crossovers are built by finding shared crossings in the
    # generated crossovers
    dcrossovers = list()
    crossing_to_crossovers = defaultdict(list)
    for co in crossovers:
        for o in graphObjIter(co):
            if o.Subtype in CROSSING_TYPES:
                crossing_to_crossovers[o].append(co)
    for cr, cos in crossing_to_crossovers.iteritems():
        if len(cos) > 2:
            UtilityAPI.LogError("Unexpected crossover situation.")
        if len(cos) == 2:
            # Double crossover found! Create area
            area = createArea(DIAMOND_CROSSOVER_AREA_TYPE,
                              dcrossover_name(cos[0], cos[1]),
                              edges=([e for e in cos[0].Edges] +
                                     [e for e in cos[1].Edges]))
            area[ATTRIBUTE_PROJECT_TREE_PATH] = "Design/Diamond crossovers"
            area[ATTRIBUTE_HIGHLIGHTING_COLOR] = "Purple"
            railyard.Areas.Add(area)
            dcrossovers.append(area)

    if len(crossovers) > 0:
        UtilityAPI.LogNote(
            "Created %s crossover object(s): \n  %s" % (
                len(crossovers),
                '\n  '.join(sorted([obj.Name for obj in crossovers]))))
    if len(dcrossovers) > 0:
        UtilityAPI.LogNote(
            "Created %s diamond crossover object(s): \n  %s" % (
                len(dcrossovers),
                '\n  '.join(sorted([obj.Name for obj in dcrossovers]))))
