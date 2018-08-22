#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# File name case converter script
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/nomen
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import common
    from core import fileren

    try:
        p = clap.Parser()
    except Exception as e:
        print "%s: error: %s" % (os.path.basename(sys.argv[0]), e)
        sys.exit(1)

    p.set_description("Convert the case of the base name of all files " \
                      "inside a directory and (if requested) in all of its " \
                      "sub-directories.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_predef("-c", "--case", "target case of the base name", "case",
                 ["lower", "title", "upper", "config"], True)
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)
    p.add_predef("-m", "--conflict-mode", "conflict mode (in case of " \
                 "duplicate file names)", "conflict_mode", ["rename", "skip"],
                 True)

    # Optional arguments
    p.add_avalue(None, "--cfg-lower", "path to the config file for strings " \
                 "which should always be lowercase inside the file " \
                 "name", "cfg_lower", None, False)
    p.add_avalue(None, "--cfg-mixed", "path to the config file for strings " \
                 "which should always be mixed case inside the " \
                 "file name", "cfg_mixed", None, False)
    p.add_avalue(None, "--cfg-title", "path to the config file for strings " \
                 "which should always be title case inside the " \
                 "file name", "cfg_title", None, False)
    p.add_avalue(None, "--cfg-upper", "path to the config file for strings " \
                 "which should always be uppercase inside the file " \
                 "name", "cfg_upper", None, False)
    p.add_switch(None, "--confirm", "skip the confirmation prompt and " \
                 "instantly rename files", "confirm", True, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--ignore-symlinks", "ignore symbolic links",
                 "ignore_symlinks", True, False)
    p.add_switch("-r", "--recursive", "process the given directory " \
                 "recursively", "recursive", True, False)
    p.add_avalue(None, "--simulate", "simulate the rename process and " \
                 "write the details into a report file", "report_file", None,
                 False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print fileren.get_version()
        sys.exit(0)

    args = p.parse_args()
    if args.confirm and not args.report_file == None:
        p.error("The confirm and the simulate argument cannot be given at " \
                "the same time.")

    try:
        if not args.confirm and args.report_file == None:
            if not common.confirm_notice():
                sys.exit(0)

        fileren.convert_case(args.directory, args.case, args.conflict_mode,
                             args.recursive, args.cfg_lower, args.cfg_mixed,
                             args.cfg_title, args.cfg_upper, args.report_file,
                             args.ignore_symlinks)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

