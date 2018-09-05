#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# Static case core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/nomen
# GitLab: https://gitlab.com/urbanware-org/nomen
# ============================================================================

__version__ = "2.3.6"

import os
import sys
from . import paval as pv


def get_version():
    """
        Return the version of this module.
    """
    return __version__


def parse_case_configs(cfg_lower=None, cfg_mixed=None, cfg_title=None,
                       cfg_upper=None):
    """
        Parse the configuration files for static file name case
        conversion.
    """
    list_lower = []
    list_mixed = []
    list_title = []
    list_upper = []

    if cfg_lower is not None:
        list_lower = __read_config(__config_abspath(cfg_lower, "lowercase"))
    if cfg_mixed is not None:
        list_mixed = __read_config(__config_abspath(cfg_mixed, "mixed case"))
    if cfg_title is not None:
        list_title = __read_config(__config_abspath(cfg_title, "title case"))
    if cfg_upper is not None:
        list_upper = __read_config(__config_abspath(cfg_upper, "uppercase"))

    __check_dupes(list_lower, list_mixed, list_title, list_upper)

    return list_lower, list_mixed, list_title, list_upper


def __check_dupes(list_lower, list_mixed, list_title, list_upper):
    """
        Check for duplicate case list entries.
    """
    list_diff = []

    list_diff = __process_case_list(list_lower, list_diff)
    list_diff = __process_case_list(list_mixed, list_diff)
    list_diff = __process_case_list(list_title, list_diff)
    __process_case_list(list_upper, list_diff)


def __config_abspath(config, description):
    """
        Get the absolute path of a config file.
    """
    description += " config"
    try:
        pv.path(config, description, True, True)
    except:
        config_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        config = os.path.join(config_dir, "cfg", os.path.basename(config))
        pv.path(config, description, True, True)
    config = os.path.abspath(config)

    return config


def __process_case_list(list_input, list_output):
    """
        Process a case list and raise an exception in case of duplicate
        entries.
    """
    duplicate = ""

    for item in list_input:
        if item is None or item == "":
            continue
        elif item.lower() in list_output:
            duplicate = item
            break
        else:
            list_output.append(item.lower())

    if duplicate != "":
        raise Exception("Duplicate config file entries. The same string "
                        "must not exist in multiple config files. The "
                        "duplicate string was \"%s\" (without the "
                        "enclosing quotes)." % duplicate)

    return list_output


def __read_config(config_file):
    """
        Read out the contents of a config file.
    """
    list_config = []

    fh_config = open(config_file, "r")
    for line in fh_config:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        list_config.append(line.replace("\n", ""))
    fh_config.close()
    list_config.sort

    return list_config

# EOF
