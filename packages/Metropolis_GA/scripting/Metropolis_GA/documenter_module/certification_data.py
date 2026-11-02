#
# Copyright (C) 2014 Prover Technology, All Rights Reserved
#

"""
Prover iLock Documenter top level script to generate certification data

Generate SA data in HLL and LCF format.
"""

import os
import shutil
import sys

from PredefinedAttributes import (ATTRIBUTE_HIGHLIGHTING_COLOR,
                                  ATTRIBUTE_PROJECT_TREE_PATH)
import PiSpecAPI
import ProjectAPI
import UtilityAPI

import Certification_LCF_Dump
import gss_export.api
import gss_export.config


# Name of the script runner (aka documenter) parameter controlling
# where HLL files are produced.
PAR_CERT_DIR_NAME = "CertDirName"

# Name of parameter for controlling "strict mode". When parameter is
# true, delete generated files if an error was detected.
PAR_STRICT_MODE = "StrictMode"


def _header():
    top = [
        "*" * 73,
        "             APPLICATION PROGRAM CERTIFICATION DATA",
        "*" * 73,
        "",
        "                        -------- WARNING --------",
        "",
        "       This is safety-critical data for the certifiable verification of",
        "       interlocking system software code.",
        "       The content of the file must not be altered after approval.",
        "",
        "*" * 73,
        ""]
    bottom = [
        "",
        "*" * 73]
    return "\n".join(
        "%-73s //" % line
        for line in (top + bottom))


def main():
    # Set the arguments of certification data generation
    req_classes = [c.Name for c in PiSpecAPI.GSSClasses]
    config_dir = ProjectAPI.Location
    open_output_folder = False
    try:
        import ParametersAPI
        out_dir = ParametersAPI.Get(PAR_CERT_DIR_NAME)
        strict_mode = ParametersAPI.Get(PAR_STRICT_MODE)
        open_output_folder = True
    except ImportError:
        out_dir = "certification"
        strict_mode = True

    def report_note(s):
        print(s)
        UtilityAPI.LogNote(s)

    def report_warning(s):
        print("WARNING: %s" % s)
        UtilityAPI.LogWarning(s)

    def report_error(s):
        print("ERROR: %s" % s)
        UtilityAPI.LogError(s)

    # Do the work
    reporter = gss_export.config.Reporter(report_note, report_warning, report_error)
    config = gss_export.config.Config(
        out_dir=out_dir,
        req_class_names=req_classes,
        reporter=reporter,
        generic_header=_header()
    )
    config.strict_mode = strict_mode
    config.deviations_filename = "verification/deviations.dv"
    config.req_prefix = "GSS_"

    res = gss_export.api.export_gss(config)
    if res.success:
        _gen_lcf_certification_data(out_dir, res)
        _prepare_output_for_lpcert_ct(out_dir)
        if open_output_folder:
            os.startfile(out_dir)

def _prepare_output_for_lpcert_ct(out_dir):
    # Copy LCF2Intg1.lmc to LCF2Intg1.lmc and LCF2Intg2.lmc
    _fake_diversify(os.path.join(out_dir, "LCF2Intg.lmc"))
    _fake_diversify(os.path.join(out_dir, "LCF2IntgProj.lmc"))

def _fake_diversify(orig_path):
    base_path, ext = os.path.splitext(orig_path)
    out1 = "%s1%s" % (base_path, ext)
    out2 = "%s2%s" % (base_path, ext)
    shutil.copyfile(orig_path, out1)
    shutil.copyfile(orig_path, out2)
    os.remove(orig_path)

def _gen_lcf_certification_data(out_dir, gss_export_res):
    config = Certification_LCF_Dump.Config(
        hll_dir=out_dir,
        out_dir=out_dir,
        gss_int_mappings=gss_export_res.int_mappings,
        gss_par_mappings=gss_export_res.par_mappings,
    )

    attr_filter = set([ATTRIBUTE_HIGHLIGHTING_COLOR,
                       ATTRIBUTE_PROJECT_TREE_PATH,
                       "start_obj",
                       "end_obj"])
    config.railyard_attributes_filter |= attr_filter
    Certification_LCF_Dump.generate_certification_lcf(config)


main()
