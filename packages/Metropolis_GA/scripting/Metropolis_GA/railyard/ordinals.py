# Copyright (C) 2021 Prover Technology, all rights reserved

"""
Generate ordinals based on paths in railyard.
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

from Metropolis_GA.lcf.geotypes import resolve_union_type

from iLock_Geography.geo_util import (
    createOrdinalRange)
from iLock_Geography.geo_algorithms import (
    areaIter)
from lcf_utils.tables import make_lcf_table
import UtilityAPI

# --------------------------------------------------------
# Utility functions
# --------------------------------------------------------


def _create_ordinals(railyard, table_storage, area_types, path_types, geo_type):
    """
    Create ordinal numbers (represented by instances
    of the provided PiSPEC class name geo_type) based on
    the maximum length of paths in the railyard (in terms of
    areas that the paths intersect).

    Build ordinal numbers based on the maximum number of
    areas (of type in area_types) in paths registered in the
    railyard (of type in path_types).

    If path_types is None, all paths are used.
    """
    assert type(geo_type) == str
    assert path_types is None or type(path_types) == list
    assert type(area_types) == list
    for item in area_types:
        assert type(item) == str

    # Iterator over the areas in a path p
    def area_iter(p):
        return areaIter(p, railyard, area_types)

    max_len = 0
    for path in railyard.Paths:
        if ((path_types is not None and
             path.Subtype not in path_types)):
            continue

        path_len = len(list(area_iter(path)))
        if path_len > max_len:
            max_len = path_len

    proj_tree_path = "Auxiliary/Ordinals"
    if max_len == 0:
        # We force a range of 1 so that the tables below can be created
        createOrdinalRange(geo_type, 1, railyard, proj_tree_path, valueAttribute="value")
    else:
        createOrdinalRange(geo_type, max_len, railyard, proj_tree_path, valueAttribute="value")

    # Create table
    # t_ordinal_value (ordinal, int)
    table_rows = list()
    for o in railyard.AuxiliaryObjects:
        if o.Subtype == geo_type:
            table_rows.append((o.Name, int(o["value"])))
    table_storage.append(
        make_lcf_table("t_ordinal_value", table_rows,
                       "the integer value of each ordinal"))

    # t_track_number (path, track_circuit, int)
    table_rows = list()
    edge_to_track_dict = dict()
    for t in railyard.Areas:
        if t.Subtype in area_types:
            for e in t.Edges:
                edge_to_track_dict[e] = t
    for p in railyard.Paths:
        if path_types is None or p.Subtype in path_types:
            tracks = list()
            for e in p.Iterator:
                if not e in edge_to_track_dict:
                    UtilityAPI.LogError(
                        "Path %s goes over an edge that is not a "
                        "track circuit." % p.Name)
                    continue
                curr_track = edge_to_track_dict[e]
                if len(tracks) == 0 or not tracks[-1] == curr_track:
                    tracks.append(curr_track)
                if curr_track in tracks[:-1]:
                    UtilityAPI.LogError(
                        "Path %s visits track %s multiple times." %
                        (p.Name, curr_track.Name))
            for i, t in enumerate(tracks):
                table_rows.append((p.Name, t.Name, i))
    table_storage.append(
        make_lcf_table("t_track_number", table_rows,
                       "the index of tracks in paths"))

# --------------------------------------------------------
# Interface
# --------------------------------------------------------

def generate(railyard, table_storage):
    """
    Generate ordinals based on all paths in the railyard.
    """
    _create_ordinals(railyard, table_storage,
                     area_types=resolve_union_type("RY_TRACK_CIRCUIT"),
                     path_types=None,
                     geo_type="g_ordinal")
