# Copyright (C) 2022 Prover Technology, All Rights Reserved

# ------------------------------------------------------------------------------
# Standard libraries imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Prover iLock imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Package imports
# ------------------------------------------------------------------------------
from ilock_utils.utils import document_time
from iLock_Geography import railyard_import
from iLock_Geography.geo_algorithms import (
    inObjIter,
)

# ------------------------------------------------------------------------------
# Local imports
# ------------------------------------------------------------------------------
from Metropolis_GA.typecheck import typedoc
from Metropolis_GA.lcf.geotypes import resolve_union_type

import ordinals
import paths
import protection_areas
import crossovers
import checks

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------
def setup():
    """
    Fetches the railyard from the layout editor and modifies it.

    Returns the updated railyard and any LCF tables generated in
    the process.
    """
    ry = railyard_import.fromLayoutEditor(mutable=True)
    railyard = ry.railyard(locked=False)

    tables = _complete_railyard(railyard)
    return railyard, tables


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------
@typedoc
def _complete_railyard(railyard):
    """
    Add automatically generated railyard objects.
    Returns a dict of computed predicates for the generated objects.

    @type railyard: IRailyard
    @rtype: list(LCFTable)
    """
    _rename_railyard_objects(railyard)
    return _generate_railyard_objects(railyard)


@typedoc
def _rename_railyard_objects(railyard):
    """
    Apply standard object and node renamings.

    @type railyard: IRailyard
    """
    area_types = resolve_union_type("RY_TRACK_CIRCUIT")
    area_delim_types = resolve_union_type("RY_TRACK_CIRCUIT_DELIMITER")
    delim_types = resolve_union_type("RY_TRACK_CIRCUIT_DELIMITER")

    for item in [area_types, area_delim_types, delim_types]:
        assert type(item) == list

    objs_delim = [s for s in inObjIter(railyard) if
                  s.Subtype in delim_types]
    if any(obj.Name.startswith(obj.Subtype) for obj in objs_delim):
        # Rename the automatically named delimiters
        _rename_nodes_and_objects(
            railyard,
            area_types=area_types,
            area_delim_types=area_delim_types)


@typedoc
def _rename_nodes_and_objects(railyard, area_types,
                              area_delim_types):
    """
    Apply standard renaming of railyard objects that have
    auto-generated names (names not provided by the user).

    @param area_types: list of area types
    @type area_types: list(str)
    @param area_delim_types: list of area delimiter types
    @type area_delim_types: list(str)
    @type railyard: IRailyard
    """
    # Set of new names created for delimiter objects
    # in nodes with more than 1 adjacent areas of a type
    # in area_types
    new_names = set()
    cnt = 0
    for node in [n for n in railyard.Graph.Nodes if
                 n.Subtype == 'PassageNode']:
        for obj in [o for o in node.Objects if o.Subtype in
                    area_delim_types]:
            areas = [a for a in railyard.NodeToAreas(node) if
                     a.Subtype in area_types]
            if len(areas) == 0:
                new_name = "Unknown"
            elif len(areas) == 1:
                new_name = '|'.join(
                    sorted([a.Name for a in areas] + ["None"]))
            else:
                # Name track circuit delimiter objects based on
                # the connecting areas; if there's already an object
                # with that name, add a suffix
                new_name = '|'.join(
                    sorted([a.Name for a in areas]))
            if new_name in new_names:
                new_name = new_name + "_%s" % cnt
                cnt += 1
            new_names.add(new_name)
            obj.Name = new_name


@typedoc
def _generate_railyard_objects(railyard):
    """
    Generate non-user railyard objects

    Create all those railyard objects not directly drawn by the user.
    Typical examples are routes, protection areas, crossover areas.

    The function also returns a list of LCF tables. Sometimes a generated
    object needs some additional information attached in order to complete
    the subsequent instantiation and parameterisation. For example, a
    generated area maybe should be associated with the object(s) from which
    it was generated and if this is not a simple geographical relation
    (that is better captured by a table method), a LCF table can be the
    solution and can be easy to produce during area generation.

    @param railyard: the railyard
    @type railyard: IRailyard
    @rtype: list(LCFTable)
    """
    table_storage = list()

    # Generate various objects (and sometimes create tables)
    paths.generate(railyard, table_storage)
    protection_areas.generate(railyard, table_storage)
    crossovers.generate(railyard, table_storage)
    ordinals.generate(railyard, table_storage) # Should be after path generation

    # Check
    checks.check(railyard)

    # Return create tables
    return table_storage
