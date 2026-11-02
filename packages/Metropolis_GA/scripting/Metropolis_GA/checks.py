#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#
"""
Various checks that can be called from other scripts.
"""


# --------------------------------------------------------
# Imports
# --------------------------------------------------------


from ilock_utils.checks import (
    check_argument_variable_names,
    check_cardinality,
)


def main():
    check_argument_variable_names()
    check_cardinality()
