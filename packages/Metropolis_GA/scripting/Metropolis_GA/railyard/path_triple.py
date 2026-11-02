#
#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Utility functions for path triples.
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

import RailyardFactory as RF

from iLock_Geography.geo_algorithms import (
    areaIter,
    isPositive,
    isSwitch,
    objectConnectorIter)

DUMMY = 'DUMMY'

# --------------------------------------------------------
# Interface functions
# --------------------------------------------------------


def path_dir_is_pos(path_triple, railyard):
    """
    Return True iff path_triple has positive direction
    in the railyard.
    """
    start_ni, edges, _ = path_triple
    dpath = RF.Path(DUMMY, DUMMY, start_ni.Node, edges)
    return isPositive(dpath, railyard)


def covered_by_area_types(railyard, path_triple_set, area_types):
    """
    Return True iff all edges of the path triples
    (can be seen as an area) are covered by
    an area of a type in area_types.
    """
    assert type(area_types) == list
    for item in area_types:
        assert type(item) == str

    edges = set()
    for path_triple in path_triple_set:
        _, edges, _ = path_triple
        for edge in edges:
            tracks = set(
                a for a in railyard.EdgeToAreas(edge) if
                a.Subtype in area_types)
            if len(tracks) == 0:
                return False
    return True


def intersects_at_most_once(railyard, path_triple, block_types):
    """
    Return true iff the path triple intersect
    a block of the provided block_types at most once.
    """
    assert type(block_types) == list
    for item in block_types:
        assert type(item) == str

    start_ni, edges, _ = path_triple
    path = RF.Path(DUMMY, DUMMY, start_ni.Node, edges)
    tracks = []
    for area in areaIter(path, railyard, block_types):
        area = list(area)
        tracks.append(area[0].Name)
    if len(tracks) == len(set(tracks)):
        return True
    return False


def switches_left_right(path_triple):
    """
    Return (left, right) where left/right are the switches traversed
    left/right in the provided path triple.
    """
    start_ni, edges, _ = path_triple
    dpath = RF.Path(DUMMY, DUMMY, start_ni.Node, edges)
    left, right = set(), set()
    for in_index, obj, out_index in objectConnectorIter(dpath):
        if isSwitch(obj):
            if in_index == 0 and out_index == 1:
                left.add(obj)
            elif in_index == 0 and out_index == 2:
                right.add(obj)

    return left, right


def path_triple_ok_1(path_triple, left, right):
    """
    Return True iff that path triple does not traverse
    a switch in violation of the provided switch positions:

    * the path_triple does not traverse a switch left,
      while that switch is in `rigth`
    * the path_triple does not traverse a switch right,
      while that switch is in `left`
    """
    left0, right0 = switches_left_right(path_triple)
    if any([obj in right for obj in left0]):
        return False
    elif any([obj in left for obj in right0]):
        return False
    return True


def without_facing_object(railyard, path_triple, types):
    """
    Callback used in "via path" generation.

    Returns False iff the path contains a facing object
    of a type in `types`  (excluding the 1st and last
    nodes in the path, however).
    """
    def _nodes_in_path_triple_ordered(path_triple):
        """
        Return list of nodes in path triple.
        The list is ordered.

        Copied from iLock_prot_area.common
        """
        start_ni, edges, _ = path_triple
        nodes = []
        for i, edge in enumerate(edges):
            ni1, ni2 = edge.NodeIndices
            if i == 0:
                if ni1 == start_ni:
                    nodes.append(ni1.Node)
                else:
                    nodes.append(ni2.Node)
            else:
                if ni1.Node == nodes[-1]:
                    nodes.append(ni2.Node)
                else:
                    nodes.append(ni1.Node)

        return nodes

    start_ni, edges, _ = path_triple
    nodes = _nodes_in_path_triple_ordered(path_triple)
    for i, node in enumerate(nodes):
        if i == 0 or i == len(nodes) - 1:
            continue
        for obj in node:
            if obj.Subtype in types:
                path = RF.Path(DUMMY, DUMMY, start_ni.Node, edges)
                if (isPositive(obj, railyard) == isPositive(path, railyard)):
                    return False
    return True
