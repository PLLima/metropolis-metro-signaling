# -*- coding: utf-8 -*-
# Copyright (C) 2022 Prover Technology, all rights reserved

"""
Generate protection areas; representing sets of protection paths.
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

# Python2
from itertools import izip_longest as zip_longest
from collections import defaultdict

import prover.specification.types as T

import UtilityAPI

from PredefinedAttributes import (
    ATTRIBUTE_PROJECT_TREE_PATH,
    ATTRIBUTE_DIRECTION_LEG,
    ATTRIBUTE_HIGHLIGHTING_COLOR)

from lcf_utils.tables import make_lcf_table

from iLock_Geography.geo_algorithms import (
    generateArea,
    createArea)

from Metropolis_GA.lcf.geotypes import resolve_union_type


# Helpers


def __prefix_path(path_a, path_b):
    """ True if path A contains path B as a strict subpath starting in the same node. """
    if path_a.Start != path_b.Start:
        return False
    for ea, eb in zip_longest((e for e in path_a.Iterator), (e for e in path_b.Iterator)):
        if ea is None:
            # A has ended before B
            return False
        if eb is None:
            # B has ended before A without diffs
            return True
        if ea != eb:
            # Diff Found
            return False
    # Paths must have been equal if no diff has been found; strict means "False"
    return False


# --------------------------------------------------------
# Interface
# --------------------------------------------------------


def generate(railyard, table_storage):
    # Collection of primary table data
    table_rows = list()

    # Collect protection paths per protection object
    name_to_paths = defaultdict(list)
    for p in railyard.Paths:
        if p.Subtype != "g_protection_path":
            continue
        edges = list((e for e in p.Iterator))

        # Start object is either a main signal (for front protection),
        # or a switch or track crossing (for flank protection)
        for o in p.Start.Objects:
            # Facing signal with front protection paths
            if (o.Subtype in resolve_union_type("RY_MAIN_SIGNAL") and
                o[ATTRIBUTE_DIRECTION_LEG] == str(edges[0].NodeIndex(p.Start).Index)):
                name_to_paths["front_" + o.Name].append(p)
            # Facing switch with flank protection paths
            elif (o.Subtype in resolve_union_type("RY_SWITCH") or
                  o.Subtype in resolve_union_type("RY_TRACK_CROSSING")):
                leg = str(edges[0].NodeIndex(p.Start).Index)
                name_to_paths["flank_" + o.Name + "leg" + leg].append(p)

    # Create area objects...
    def recurse(found, remaining):
        for i, cand in enumerate(remaining):
            if any(__prefix_path(cand, other) for other in found):
                continue
            found.append(cand)
            if i+1 < len(remaining):
                recurse(list(found), remaining[i+1:])
        yield set(found)
    for name, path_list in name_to_paths.items():
        # Set of path sets where each path set shall become an area
        path_sets = list()
        for i, p in enumerate(path_list):
            found = [p]
            path_sets.extend(recurse(found, path_list[i+1:]))

        # The above will over-generate some sets;
        # remove sets that are subsets of other sets
        path_sets = [ps for ps in path_sets
                     if not any(ps.issubset(ps2)
                                for ps2 in path_sets
                                if ps is not ps2)]

        # There may also be some inconsistent sets; where points are required
        # to be both left and right, lets leave them for now...

        # Create one area per set
        for i, path_set in enumerate(path_sets):
            # Create area
            edges = set(e for p in path_set for e in p.Iterator)
            if len(path_sets) > 0:
                area_name = name + ":" + str(i+1)
            else:
                area_name = name
            area = createArea("g_protection_area", area_name, edges=edges)
            area[ATTRIBUTE_HIGHLIGHTING_COLOR] = path_list[0][ATTRIBUTE_HIGHLIGHTING_COLOR]
            folder = '/'.join(path_list[0][ATTRIBUTE_PROJECT_TREE_PATH].split("/")[:3] +
                              ["Protection areas"])
            area[ATTRIBUTE_PROJECT_TREE_PATH] = folder
            railyard.Areas.Add(area)

            # Create a primary LCF table data
            for path in path_set:
                table_rows.append((area.Name, path.Name))

    # Primary table data ready
    table_storage.append(
        make_lcf_table("t_protection_area_paths", table_rows,
                       "protection area is based on the given protection paths"))
