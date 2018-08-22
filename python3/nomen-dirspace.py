#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# Directory name space modifier script
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
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Modify a directory name by removing leading, " \
                      "trailing and duplicate spaces or by inserting and " \
                      "removing spaces next to punctuation characters.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)

    # Optional arguments
    p.add_switch("-b", "--brackets", "insert and remove spaces next to " \
                 "brackets", "brackets", True, False)
    p.add_avalue(None, "--exclude", "pattern to exclude certain files " \
                 "(case-insensitive, multiple patterns separated via " \
                 "semicolon)", "exclude_pattern", None, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--hyphens", "insert spaces next to hyphens", \
                 "hyphens", True, False)
    p.add_switch(None, "--ignore-symlinks", "ignore symbolic links",
                 "ignore_symlinks", True, False)
    p.add_switch("-l", "--remove-leading", "remove leading spaces",
                 "remove_leading", True, False)
    p.add_switch("-r", "--recursive", "process the given directory " \
                 "recursively", "recursive", True, False)
    p.add_switch("-p", "--punctuation", "insert and remove spaces next to " \
                 "punctuation characters", "punctuation", True, False)
    p.add_switch("-s", "--remove-duplicate", "remove duplicate spaces",
                 "remove_duplicate", True, False)
    p.add_switch("-t", "--remove-trailing", "remove trailing spaces",
                 "remove_trailing", True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print(fileren.get_version())
        sys.exit(0)

    try:
        args = p.parse_args()
        if not args.punctuation and not args.remove_duplicate and \
           not args.remove_leading and not args.remove_trailing:
            p.error("Nothing to do (no optional arguments were given).")

        common.dir_space_modifier(args.directory, args.remove_duplicate,
                                  args.remove_leading, args.remove_trailing,
                                  args.brackets, args.hyphens,
                                  args.punctuation, args.ignore_symlinks,
                                  args.recursive, args.exclude_pattern)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

