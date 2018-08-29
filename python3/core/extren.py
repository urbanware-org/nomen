#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# Extension Renamer core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/nomen
# ============================================================================

__version__ = "2.3.5"

import os
import re
from datetime import datetime as dt
from . import common
from . import paval as pv


def convert_case(directory, case, conflict_mode, recursive=False,
                 report_file=None, ignore_symlinks=False):
    """
        Convert the case of the file extensions.
    """
    pv.path(directory, "given", False, True)
    pv.compstr(case, "case", ["lower", "title", "upper"])
    pv.compstr(conflict_mode, "conflict mode", ["rename", "skip"])

    case = case.lower()
    conflict_mode = conflict_mode.lower()
    directory = os.path.abspath(directory)
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    if report_file is None:
        simulate = False
    else:
        pv.path(report_file, "report", True, False)
        report_file = os.path.abspath(report_file)
        simulate = True

    time_start = dt.now()

    list_content = []
    list_excluded = []
    list_renamed = []
    list_skipped = []
    regex = re.compile("(.*)")

    list_content, list_excluded = \
        common.get_files(directory, recursive, True, regex, False,
                         ignore_symlinks)
    for item in list_content:
        list_files = item[1]
        list_renamed, list_skipped = \
            __convert_case(list_files, list_renamed, list_skipped, case,
                           conflict_mode, recursive)

    if simulate:
        list_header = []
        list_header.append("Nomen Extension Case Converter simulation report")
        list_header.append(["Report file name:", report_file])
        list_header.append(["Directory:", directory])
        list_header.append(["Recursive:", recursive])
        list_header.append(["Ignore symlinks:", ignore_symlinks])
        list_header.append(["Conflict mode:", conflict_mode.capitalize()])
        list_header.append(["Case:", case.capitalize()])

        common.report(report_file, list_header, list_renamed, list_excluded,
                      list_skipped, time_start)
    else:
        common.rename(list_renamed)


def get_version():
    """
        Return the version of this module.
    """
    return __version__


def rename_extensions(directory, conflict_mode, extension, extension_target,
                      recursive=False, ignore_case=True, report_file=None,
                      ignore_symlinks=False):
    """
        Rename the file extensions in the given directory and all of its
        sub-directories (if requested).
    """
    pv.path(directory, "given", False, True)
    pv.compstr(conflict_mode, "conflict mode", ["rename", "skip"])
    pv.string(extension, "extension", False, common.get_invalid_chars())
    pv.string(extension_target, "target extension", False,
              common.get_invalid_chars())

    conflict_mode = conflict_mode.lower()
    directory = os.path.abspath(directory)
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    if report_file is None:
        simulate = False
    else:
        pv.path(report_file, "report", True, False)
        report_file = os.path.abspath(report_file)
        simulate = True

    time_start = dt.now()

    list_content = []
    list_excluded = []
    list_extensions = []
    list_renamed = []
    list_skipped = []

    if ";" in extension:
        while ";" * 2 in extension:
            extension = extension.replace((";" * 2), ";")

        list_temp = extension.split(";")
        for extension in list_temp:
            if not extension == "":
                list_extensions.append(extension)

        if not list_extensions:
            raise Exception("The given extension list does not contain any "
                            "extensions.")
    else:
        list_extensions.append(extension)

    pattern = ""
    for extension in list_extensions:
        pattern += "(.*\." + str(extension) + "$)|"
    pattern = pattern.rstrip("|")

    if ignore_case:
        regex = re.compile(pattern, re.IGNORECASE)
    else:
        regex = re.compile(pattern)

    list_content, list_excluded = \
        common.get_files(directory, recursive, ignore_case, regex, False,
                         ignore_symlinks)
    for item in list_content:
        list_files = item[1]
        list_renamed, list_skipped = \
            __rename_extensions(list_files, list_extensions, list_renamed,
                                list_skipped, conflict_mode, extension_target)

    if simulate:
        list_header = []
        list_header.append("Nomen Extension Renamer simulation report")
        list_header.append(["Report file name:", report_file])
        list_header.append(["Directory:", directory])
        list_header.append(["Recursive:", recursive])
        list_header.append(["Ignore symlinks:", ignore_symlinks])
        list_header.append(["Conflict mode:", conflict_mode.capitalize()])
        list_header.append(["Extensions:", extension])
        list_header.append(["Target extension:", extension_target])
        list_header.append(["Ignore case:", ignore_case])

        common.report(report_file, list_header, list_renamed, list_excluded,
                      list_skipped, time_start)
    else:
        common.rename(list_renamed)


def __convert_case(list_files, list_renamed, list_skipped, case,
                   conflict_mode, recursive):
    """
        Core method to convert the case of the file extensions.
    """
    fs_case = common.get_fs_case_sensitivity(os.path.dirname(list_files[0]))

    for file_path in list_files:
        num = 1
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]
        file_ext = os.path.splitext(file_name)[1]

        if file_ext == "":
            list_skipped.append(file_path)
            continue

        if case == "lower":
            extension_target = file_ext.lower()
        elif case == "title":
            extension_target = file_ext.title()
        elif case == "upper":
            extension_target = file_ext.upper()

        file_newpath = file_path.replace(file_ext, extension_target)
        if file_path == file_newpath:
            list_skipped.append(file_path)
            continue

        if conflict_mode == "rename":
            while True:
                if common.file_exists(file_newpath, list_renamed, fs_case):
                    if not fs_case:
                        if file_path.lower() == file_newpath.lower():
                            break

                    file_newpath = \
                        file_path.replace(file_ext,
                                          "_" + str(num) + extension_target)
                    num += 1
                else:
                    break
        elif conflict_mode == "skip":
            if common.file_exists(file_newpath, list_renamed, fs_case):
                if not fs_case:
                    if not file_path.lower() == file_newpath.lower():
                        list_skipped.append(file_newpath)
                        continue
                else:
                    list_skipped.append(file_newpath)
                    continue

        if os.path.exists(file_path):
            list_renamed.append([file_path, file_newpath + ".__temp__",
                                 file_newpath])

    return list_renamed, list_skipped


def __rename_extensions(list_files, list_extensions, list_renamed,
                        list_skipped, conflict_mode, extension_target):
    """
        Core method to rename the file extensions.
    """
    fs_case = common.get_fs_case_sensitivity(os.path.dirname(list_files[0]))

    for file_path in list_files:
        num = 1
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]
        file_ext = os.path.splitext(file_name)[1]

        if file_ext == "":
            list_skipped.append(file_path)
            continue

        file_newpath = file_path.replace(file_ext,
                                         os.path.extsep + extension_target)
        if file_path == file_newpath:
            list_skipped.append(file_path)
            continue

        if conflict_mode == "rename":
            while True:
                if common.file_exists(file_newpath, list_renamed, fs_case):
                    if not fs_case:
                        if file_path.lower() == file_newpath.lower():
                            break
                    file_newpath = file_path.replace(file_ext, "_" +
                                                     str(num) +
                                                     os.path.extsep +
                                                     extension_target)
                    num += 1
                else:
                    break
        elif conflict_mode == "skip":
            if common.file_exists(file_newpath, list_renamed, fs_case):
                if not fs_case:
                    if not file_path.lower() == file_newpath.lower():
                        list_skipped.append(file_path)
                        continue
                else:
                    list_skipped.append(file_path)
                    continue

        if os.path.exists(file_path):
            list_renamed.append([file_path, file_newpath + ".__temp__",
                                 file_newpath])

    return list_renamed, list_skipped

# EOF
