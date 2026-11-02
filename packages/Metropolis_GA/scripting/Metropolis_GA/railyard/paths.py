# -*- coding: utf-8 -*-
# Copyright (C) 2022 Prover Technology, all rights reserved

"""
Generate paths

A path is a directed section of a track. It is a low-level type.
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

import prover.specification.types as T

import platform

import clr
clr.AddReference("Prover-iLock-api")
from Prover.iLock.Scripting.Model.Geography import IGraph

import UtilityAPI

from PredefinedAttributes import (
    ATTRIBUTE_PROJECT_TREE_PATH,
    ATTRIBUTE_DIRECTION_LEG,
    ATTRIBUTE_BENT_LEG,
    ATTRIBUTE_HIGHLIGHTING_COLOR)

from iLock_Geography.geo_algorithms import (
    DirObj2DirObjPaths,
    DirObj2EndPaths,
    isPositive,
    outObjIter,
    isSwitch,
    createPath)

from ilock_utils.utils import document_time

from path_name import (
    path_name_si_si)
from path_triple import (
    path_dir_is_pos,
    intersects_at_most_once,
    covered_by_area_types)

from Metropolis_GA.lcf.geotypes import resolve_union_type


# --------------------------------------------------------
# Helpers
# --------------------------------------------------------

unique_names = set([])
def get_name_fun(prefix=""):
    def path_name(railyard, path_triple, start_obj, end_obj):
        """ Return name for path. """
        name, _ = path_name_si_si(railyard, start_obj, end_obj, prefix, unique_names)
        return name
    return path_name

def get_name_route_section_fun(prefix=""):
    def path_name(railyard, path_triple, start_obj, end_obj):
        first_edge = path_triple[1][0]
        if path_dir_is_pos(path_triple, railyard):
            suffix = "E"
        else:
            suffix = "W"
        for a in railyard.EdgeToAreas(first_edge):
            name = "%s%s" % (a.Name, suffix)
            if name in unique_names:
                n = 1
                name = "%s%d" % (name, n)
                while name in unique_names:
                    n = n + 1
                    name = "%s%d" % (name[:-1], n)
            unique_names.add(name)
            return name
        UtilityAPI.LogError("The path from %s to %s contains an edge that is not in an area." %
                            (start_obj.Name, end_obj.Name))
        return "%s-%s" % (start_obj.Name, end_obj.Name)
    return path_name

def __keep_route(railyard, path_triple):
    """
    Return True iff path_triple is to be kept for a path.

    Keep path triple for a path iff:
    1. the path triple intersect TCs at most once (no loops)
    """
    area_types = resolve_union_type("RY_TRACK_CIRCUIT")
    return (
        intersects_at_most_once(
            railyard, path_triple, area_types))


def __keep_protection_path(railyard, path_triple):
    """
    For protection paths
    1. Never go past a trailing signal.
    """
    start_ni, edges, end_ni = path_triple

    # Trailing signals
    signal_types = resolve_union_type("RY_SIGNAL")
    curr_ni = start_ni
    for i, e in enumerate(edges[:-1]):
        end_ni = e.Other(curr_ni)
        for o in end_ni.Node.Objects:
            if (o.Subtype in signal_types and
                o[ATTRIBUTE_DIRECTION_LEG] == str(end_ni.Index)):
                return False
        curr_ni = edges[i+1].NodeIndex(end_ni.Node)
    return True

# --------------------------------------------------------
# Interface
# --------------------------------------------------------


def generate(railyard, predicate_storage):
    # Routes from signal to signal
    path_type = "g_route"
    document_time(
        lambda: create_paths(
            railyard,
            # Path generator
            DirObj2DirObjPaths(railyard,
                               # From
                               gType=resolve_union_type("RY_SIGNAL"),
                               # To
                               gTypeEnd=resolve_union_type("RY_ROUTE_END"),
                               beginFacing=True,
                               endFacing=True),
            # Subdir
            "Routes",
            # Geo type name
            path_type,
            name_callback=get_name_fun(),
            path_triple_ok_callback=__keep_route,
            color="Green"),
        "Time [Path generation (%s)]" % path_type,
        issue_log_note=False)

    # Route sections from delimiter to delimiter
    path_type = "g_route_section"
    document_time(
        lambda: create_paths(
            railyard,
            # Path generator
            DirObj2DirObjPaths(railyard,
                               # From
                               gType=["g_track_circuit_delimiter"],
                               # To
                               gTypeEnd=["g_track_circuit_delimiter"],
                               beginFacing=None,
                               endFacing=None),
            # Subdir
            "Route sections",
            # Geo type name
            path_type,
            name_callback=get_name_route_section_fun(),
            path_triple_ok_callback=__keep_route,
            color="Green"),
        "Time [Path generation (%s)]" % path_type,
        issue_log_note=False)

    # Flank protection (sidoskydd)
    path_type = "g_protection_path"
    document_time(
        lambda: create_paths(
            railyard,
            # Path generator
            DirObj2DirObjPaths(railyard,
                               # From
                               gType=["g_switch"],
                               # To
                               gTypeEnd=(
                                   resolve_union_type("RY_SIGNAL") +
                                   resolve_union_type("RY_SWITCH")),
                               beginFacing=True,
                               endFacing=False,
                               noPrefix=False),
            # Subdir
            "Protection paths",
            # Geo type name
            path_type,
            name_callback=get_name_fun("flank_"),
            path_triple_ok_callback=__keep_protection_path,
            color="Red"),
        "Time [Path generation (%s)]" % path_type,
        issue_log_note=False)
    path_type = "g_protection_path"
    document_time(
        lambda: create_paths(
            railyard,
            # Path generator
            DirObj2DirObjPaths(railyard,
                               # From
                               gType=["g_track_crossing"],
                               # To
                               gTypeEnd=(
                                   resolve_union_type("RY_SIGNAL") +
                                   resolve_union_type("RY_SWITCH")),
                               beginFacing=True,
                               endFacing=False,
                               noPrefix=False),
            # Subdir
            "Protection paths",
            # Geo type name
            path_type,
            name_callback=get_name_fun("flank_"),
            path_triple_ok_callback=__keep_protection_path,
            color="Red"),
        "Time [Path generation (%s)]" % path_type,
        issue_log_note=False)

    # Front protection (frontskydd)
    path_type = "g_protection_path"
    document_time(
        lambda: create_paths(
            railyard,
            # Path generator
            DirObj2DirObjPaths(railyard,
                               # From
                               gType=resolve_union_type("RY_SIGNAL"),
                               # To
                               gTypeEnd=(
                                   resolve_union_type("RY_SIGNAL") +
                                   resolve_union_type("RY_SWITCH")),
                               beginFacing=True,
                               endFacing=False,
                               noPrefix=False),
            # Subdir
            "Protection paths",
            # Geo type name
            path_type,
            name_callback=get_name_fun("front_"),
            path_triple_ok_callback=__keep_protection_path,
            color="Orange"),
        "Time [Path generation (%s)]" % path_type,
        issue_log_note=False)


def create_paths(railyard,
                 path_generator,
                 subdir,
                 geo_type,
                 name_callback,
                 path_triple_ok_callback=None,
                 reverse_paths=False,
                 color="Green"):
    for path_triple in path_generator.generate():
        if ((path_triple_ok_callback is not None and
             not path_triple_ok_callback(railyard, path_triple))):
            continue
        start_ni, edges, end_ni = path_triple

        # Loop over start objects
        for start_obj in path_generator.startObjects(start_ni):
            # Get first matching end object
            end_obj = next(path_generator.endObjects(end_ni))

            if reverse_paths:
                start_obj, end_obj = end_obj, start_obj
                path_triple = end_ni, tuple(reversed(edges)), start_ni
                start_ni, edges, end_ni = path_triple

            # Get appropriate name
            path_name = name_callback(railyard, path_triple, start_obj, end_obj)

            # Get folder (subpath of start_obj)
            try:
                folder = '/'.join([start_obj[ATTRIBUTE_PROJECT_TREE_PATH],
                                   start_obj.Name,
                                   subdir])
            except:
                try:
                    folder = '/'.join([end_obj[ATTRIBUTE_PROJECT_TREE_PATH],
                                       end_obj.Name,
                                       subdir])
                except:
                    folder = '/'.join(['Design', 'Unknown'])

            # Greate geo path
            path = createPath(
                subtype=geo_type,
                name=path_name,
                start_node=start_ni.Node,
                edges=edges,
                start_obj=start_obj,
                end_obj=end_obj)
            path[ATTRIBUTE_HIGHLIGHTING_COLOR] = color
            path[ATTRIBUTE_PROJECT_TREE_PATH] = folder
            path_dir = "1" if start_ni != edges[0].Positive else "0"
            path[ATTRIBUTE_DIRECTION_LEG] = path_dir
            railyard.Paths.Add(path)
