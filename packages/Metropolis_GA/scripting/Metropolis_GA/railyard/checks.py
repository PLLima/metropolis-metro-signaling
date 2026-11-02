#
#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Generic checks of a railyard model.
"""

import UtilityAPI

from iLock_Geography.geo_algorithms import (
    inObjIter,
    outObjIter)

from Metropolis_GA.typecheck import typedoc
from Metropolis_GA.lcf.geotypes import resolve_union_type


@typedoc
def check_oriented(railyard):
    """
    Checks whether the railyard is oriented.

    @param railyard: the railyard
    @type railyard: IRailyard
    @rtype: (bool, str)
    """
    if not railyard.Graph.Oriented:
        return False, "Railyard is not oriented"
    return True, ''


@typedoc
def check_two_directions(railyard, types):
    """
    Checks whether the railyard contains two instances
    of GenericOutside objects of a type in types.

    @param railyard: the railyard
    @type railyard: IRailyard
    @param types: the type names
    @type types: list(str)
    @rtype: tuple(bool, str)
    """
    objs = [obj for obj in outObjIter(railyard) if
            obj.Subtype in types]
    if types and len(objs) != 2:
        return False, (
            "Railyard does not contain "
            "two direction instances:\n  %s" % (
                ', '.join(sorted([obj.Name for obj in objs]))))
    return True, ''


@typedoc
def check_coplaced_with_delim(railyard, obj_types, delim_types):
    """
    Check that object are coplaced with delimiters (same node).

    @param railyard: the railyard
    @type railyard: IRailyard
    @param obj_types: the object type names
    @type obj_types: list(str)
    @param delim_types: the delimiter type names
    @type delim_types: list(str)
    @rtype: tuple(bool, str)
    """
    objs = set(obj for obj in inObjIter(railyard) if
               obj.Subtype in obj_types)
    objs_on_delims = set()
    delim_objs = [obj for obj in inObjIter(railyard) if
                  obj.Subtype in delim_types]
    for obj in delim_objs:
        for node in railyard.RailyardObjectToNodes(obj):
            for obj0 in node.Objects:
                if obj0.Subtype in obj_types:
                    objs_on_delims.add(obj0)
    lost_objs = objs - objs_on_delims
    if len(lost_objs) > 0:
        return False, 'Object(s) not coplaced with delimiter(s): %s' % (
            ','.join(sorted([x.Name for x in lost_objs])))

    return True, ''


@typedoc
def check_areas_dont_intersect(railyard, area_types):
    """
    Check that no edge in the railyard is contained in
    multiple areas (of area type).

    @param railyard: the railyard
    @type railyard: IRailyard
    @param area_types: the object type names
    @type area_types: list(str)
    @rtype: tuple(bool, str)
    """
    if railyard is None:
        return False, 'No railyard'
    errors = set()
    for edge in railyard.Graph.Edges:
        tcs = set(a for a in railyard.EdgeToAreas(edge) if
                  a.Subtype in area_types)
        if len(tcs) >= 2:
            tc1, tc2 = list(tcs)[:2]
            errors.add((tc1, tc2))

    if len(errors) > 0:
        return False, (
            "The following pairs of areas share a common edge:\n  %s" % (
                '\n  '.join([
                    str((tc1.Name, tc2.Name)) for tc1, tc2 in sorted(errors)])))

    return True, ''


@typedoc
def check_railyard_covered_by_areas(railyard, area_types):
    """
    Check all edges in the railyard contained in an area
    (area) of the specified type(s).

    @param railyard: the railyard
    @type railyard: IRailyard
    @param area_types: the object type names
    @type area_types: list(str)
    @rtype: tuple(bool, str)
    """
    errors = list()
    for edge in railyard.Graph.Edges:
        tcs = set(a for a in railyard.EdgeToAreas(edge) if
                  a.Subtype in area_types)
        if not tcs:
            ni1, ni2 = edge
            errors.append((ni1, ni2))

    if len(errors) > 0:
        return (False,
                "The edges between the following nodes are not "
                "contained in an area of a type in %s:\n  %s" % (
                    area_types,
                    '\n  '.join([
                        str((ni1.Node.Name, ni2.Node.Name)) for
                        ni1, ni2 in errors])))

    return True, ''


@typedoc
def check_object_names(railyard):
    """
    Check that legal object names are used.

    - Exit signal names must end with "E" or "W"

    @param railyard: the railyard
    @type railyard: IRailyard
    @rtype: tuple(bool, str)
    """
    errors = list()
    for n in railyard.Graph.Nodes:
        for o in n:
            if o.Subtype == "g_exit_signal":
                if not o.Name[-1] in ("E", "W"):
                    errors.append(o.Name)
    if len(errors) > 0:
        return (False,
                "Exit signal object names should end in 'E' or 'W':\n %s" % (
                    ", ".join(errors)))

    return True, ''

# ------------------------------------------
# Interface
# ------------------------------------------


@typedoc
def check(railyard):
    """
    Check that the layout is ok w.r.t. various consistency rules.
    Returns True iff all checks passed.
    If some check failed, a note/warning/error message is raised.

    @param railyard: the railyard
    @type railyard: IRailyard
    @rtype: bool
    """
    notes, warnings, errors = [], [], []

    # passed, msg = check_oriented(railyard)
    # if not passed:
    #     errors.append(msg)

    # passed, msg = check_two_directions(
    #     railyard,
    #     types=resolve_union_type("RY_DIRECTION"))
    # if not passed:
    #     warnings.append(msg)

    passed, msg = check_coplaced_with_delim(
        railyard,
        obj_types=resolve_union_type("RY_SIGNAL"),
        delim_types=resolve_union_type("RY_TRACK_CIRCUIT_DELIMITER"))
    if not passed:
        errors.append(msg)

    passed, msg = check_areas_dont_intersect(
        railyard,
        area_types=resolve_union_type("RY_TRACK_CIRCUIT"))
    if not passed:
        errors.append(msg)

    # passed, msg = check_railyard_covered_by_areas(
    #     railyard,
    #     area_types=resolve_union_type("RY_TRACK_CIRCUIT"))
    # if not passed:
    #     warnings.append(msg)

    passed, msg = check_object_names(
        railyard)
    if not passed:
        errors.append(msg)

    if len(notes) > 0:
        for msg in notes:
            UtilityAPI.LogNote(msg)

    if len(warnings) > 0:
        for msg in warnings:
            UtilityAPI.LogWarning(msg)

    if len(errors) > 0:
        for msg in errors:
            UtilityAPI.LogError(msg)

    return len(errors) == 0
