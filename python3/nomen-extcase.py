#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# Extension case converter script
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
    from core import extren

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Convert the case of the extension of all files " \
                      "inside a directory and (if requested) in all of its " \
                      "sub-directories.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_predef("-c", "--case", "target extension case", "case",
                 ["lower", "title", "upper"], True)
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)
    p.add_predef("-m", "--conflict-mode", "conflict mode (in case of " \
                 "duplicate file names)", "conflict_mode", ["rename", "skip"],
                 True)

    # Optional arguments
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
        print(extren.get_version())
        sys.exit(0)

    args = p.parse_args()
    if args.confirm and not args.report_file == None:
        p.error("The confirm and the simulate argument cannot be given at " \
                "the same time.")

    try:
        if not args.confirm and args.report_file == None:
            if not common.confirm_notice():
                sys.exit(0)

        extren.convert_case(args.directory, args.case, args.conflict_mode,
                            args.recursive, args.report_file,
                            args.ignore_symlinks)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

