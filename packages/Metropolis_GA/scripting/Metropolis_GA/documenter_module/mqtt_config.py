#! /usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import itertools
import sys
from collections import defaultdict

import prover.specification.types as T
import prover.specification.parameters as P
import prover.specification.functions as F

import CodeAPI
import GeneratorAPI
import ProjectAPI
import PiExpressionFactory as xpf

from lcf_utils import prettyprint


def __pp(o1, o2):
    return prettyprint.PPList([o1, o2], inline=True)


def write_rjson(rjson_name, inbound, outbound, program_name=None, prefix=None):
    rjson_dict = dict()
    rjson_dict['server'] = os.environ.get('METROPOLIS_MQTT_SERVER', 'localhost')
    rjson_dict['port'] = 1883
    io_dict_out = dict()
    io_dict_out['program'] = program_name
    io_dict_out['prefix'] = prefix + "/"
    io_dict_out['cleanup-on-disconnect'] = True
    io_dict_out['outbound'] = sorted(outbound, key=lambda x:x.to_rjson(0))
    io_dict_in = dict()
    io_dict_in['program'] = program_name
    io_dict_in['prefix'] = prefix + "/"
    io_dict_in['default-bool'] = False
    io_dict_in['default-int'] = 0
    io_dict_in['inbound'] = sorted(inbound, key=lambda x:x.to_rjson(0))
    rjson_dict['io'] = [io_dict_out, io_dict_in]

    with io.open(rjson_name, "w", encoding="utf-8") as jf:
        to_write = prettyprint.to_rjson(rjson_dict)
        jf.write(to_write)


def export_mqtt_config():
    """
    Export MQTT config.
    """
    config_dir = os.path.join(
        ProjectAPI.Location, "config")
    mqtt_file = os.path.join(
        config_dir,
        "io_%s.rjson" % ProjectAPI.Name.lower())
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    # Dictionary instance -> generic variable name -> variable
    var_dict = defaultdict(dict)
    for p in CodeAPI.Programs:
        for c in itertools.chain((i for i in p.Inputs),
                                 (e for e in p.Equations)):
            if c.Variable.InstanceName:
                inst = GeneratorAPI.GetInstance(c.Variable.InstanceName)
                var_dict[inst][c.Variable.DesignName] = c.Variable

    # Outputs and inputs
    outbound = list()
    inbound = list()

    # Exit signal i/os
    for i in GeneratorAPI.GetAllInstancesTransitive(T.EXIT_SIGNAL):
        n = var_dict[i]["LineOutput"].Name
        outbound.append(__pp(n, n))
        n = var_dict[i]["LineInput"].Name
        if "E.LineInput" in n:
            nr = n.replace("E.LineInput", "W.LineOutput")
        else:
            nr = n.replace("W.LineInput", "E.LineOutput")
        inbound.append(__pp(n, nr))
    for i in GeneratorAPI.GetAllInstancesTransitive(T.TRACK_CIRCUIT):
        if not F.exit_track.GetValue(i):
            continue
        n = var_dict[i]["Clear"].Name
        outbound.append(__pp(n, n))
        inbound.append(__pp(n, n))

    prefix = "metropolis_line"
    program_name = p.Name
    write_rjson(mqtt_file, inbound, outbound,
                program_name=program_name, prefix=prefix)
    print("MQTT config for vital link exported to file:\n  %s" % mqtt_file)


export_mqtt_config()
