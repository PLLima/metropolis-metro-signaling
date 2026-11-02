# Copyright (C) 2022 Prover Technology, all rights reserved

"""
Utility functions for naming of paths (used as callback functions,
typically).
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

from Prover.iLock.Scripting.Exceptions import (
    UnknownArgumentException)


# --------------------------------------------------------
# Interface functions
# --------------------------------------------------------

def path_name_1(railyard, start_obj, path_type):
    """
    Return a name to use for a path to be registered in the
    railyard, using the following naming pattern, where index
    is the smallest natural number possible:

    "%s:%s-%s" % (start_obj.Name, path_type, index)
    """
    assert type(path_type) == str
    i = 0
    while True:
        name = "%s:%s-%s" % (
            str(start_obj.Name), str(path_type), i)
        try:
            _ = railyard.getRailyardComponent(name)
        except UnknownArgumentException:
            break
        i += 1

    return name


def path_name_2(railyard, start_obj, end_obj, path_type=None):
    """
    Return a name to use for a path to be registered in the
    railyard, using the following naming pattern, where index
    is the smallest natural number possible:

    "%s.%s:%s-%s" % (start_obj.Name, end_obj.Name, path_type, index)
    """
    if path_type is None:
        path_type = 'None'
    assert type(path_type) == str
    path_type = ':%s' % path_type
    i = 0
    while True:
        name = start_obj.Name + '.' + end_obj.Name + '%s-%s' % (path_type, i)
        try:
            _ = railyard.getRailyardComponent(name)
        except UnknownArgumentException:
            break
        i += 1

    return name


def path_name_si_si(railyard, start_obj, end_obj, path_type, unique_names):
    """
    Return a name to use for a path to be registered in the
    railyard, using the following naming pattern if it is unique:

    "%s-%s" % (start_obj.Name, end_obj.Name)

    if more than one path exits between start and end, adds a suffix _index
    where index starts at 2.
    """
    assert type(path_type) == str
    i = 1
    while True:
        name = "%s-%s" % (
            start_obj.Name, end_obj.Name)
        if name in unique_names:
            i += 1
            name += "_" + str(i)
        try:
            inst = railyard.getRailyardComponent(name)
        except UnknownArgumentException:
            break
    unique_names.add(name)
    return name, unique_names


def crossover_name_1(railyard, sw1, sw2, sep='-'):
    """
    Return a name to use for a crossover to be registered in the
    railyard, using the following naming pattern:

    "%s-%s" % (sw1.Name, sw2.Name)

    The '-' is the default separator (`sep`).
    If this name already exists, a suffix is added, where index
    in this pattern is the smallest natural number possible:

    "%s-%s:%s" % (sw1.Name, sw2.Name, index)

    :param str sep: Separator ('-' by default)
    """
    names = sorted([sw1.Name, sw2.Name])
    name = "%s%s%s" % (names[0], sep, names[1])
    try:
        _ = railyard.getRailyardComponent(name)
    except UnknownArgumentException:
        return name

    i = 0
    while True:
        name = "%s%s%s:%s" % (names[0], sep, names[1], i)
        try:
            _ = railyard.getRailyardComponent(name)
        except UnknownArgumentException:
            break
        i += 1

    return name