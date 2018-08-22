#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# File name modifier script
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

    p.set_description("Modify the base name of files by adding, removing " \
                      "or replacing a user-defined string.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_predef("-a", "--action", "action to perform", "action",
                 ["add", "remove", "replace"], True)
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)
    p.add_predef("-p", "--position", "position where to perform the action",
                 "position", ["any", "prefix", "suffix"], True)
    p.add_avalue("-s", "--string", "input string to perform the action " \
                 "with (case-sensitive)", "input_string", None, True)

    # Optional arguments
    p.add_switch("-c", "--case-sensitive", "do not ignore the case of the " \
                 "given exclude or explicit pattern", "case", False, False)
    p.add_switch(None, "--confirm", "skip the confirmation prompt and " \
                 "instantly rename files", "confirm", True, False)
    p.add_avalue(None, "--exclude", "pattern to exclude certain files " \
                 "(case-insensitive, multiple patterns separated via " \
                 "semicolon)", "exclude_pattern", None, False)
    p.add_avalue(None, "--explicit", "explicit pattern to only process " \
                 "certain files (case-insensitive, multiple patterns " \
                 "separated via semicolon)", "explicit_pattern", None, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--ignore-symlinks", "ignore symbolic links",
                 "ignore_symlinks", True, False)
    p.add_switch("-r", "--recursive", "process the given directory " \
                 "recursively", "recursive", True, False)
    p.add_switch(None, "--regex", "use regex syntax for the exclude or " \
                 "explicit pattern instead of just asterisk wildcards and " \
                 "semicolon separators (for details see the section " \
                 "'Regular expression operations' inside the official " \
                 "Python documentation)", "regex_syntax", True, False)
    p.add_avalue(None, "--replace-string", "string to replace the input" \
                 "string with (when using the action 'replace')",
                 "replace_string", None, False)
    p.add_avalue(None, "--simulate", "simulate the rename process and " \
                 "write the details into a report file", "report_file", None,
                 False)
    p.add_avalue(None, "--strip", "remove certain leading and trailing " \
                 "characters from the base name", "strip_chars", None, False)
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

    args = p.parse_args()
    if args.confirm and not args.report_file == None:
        p.error("The confirm and the simulate argument cannot be given at " \
                "the same time.")
    if args.exclude_pattern and args.explicit_pattern:
        p.error("The exclude and the explicit pattern argument cannot be " \
                "given at the same time.")

    try:
        if not args.confirm and args.report_file == None:
            if not common.confirm_notice():
                sys.exit(0)

        if args.exclude_pattern:
            pattern = args.exclude_pattern
            exclude = True
        elif args.explicit_pattern:
            exclude = False
            pattern = args.explicit_pattern
        else:
            exclude = None
            pattern = None

        fileren.modify_names(args.directory, args.action, args.position,
                             args.input_string, args.replace_string,
                             args.recursive, exclude, pattern, args.case,
                             args.regex_syntax, args.report_file,
                             args.ignore_symlinks, args.strip_chars)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

