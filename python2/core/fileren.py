#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# File Renamer core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/nomen
# GitLab: https://gitlab.com/urbanware-org/nomen
# ============================================================================

__version__ = "2.3.5"

import common
import os
import paval as pv
import re
import statcase

from datetime import datetime as dt

def convert_case(directory, case, conflict_mode, recursive=False,
                 cfg_lower=None, cfg_mixed=None, cfg_title=None,
                 cfg_upper=None, report_file=None, ignore_symlinks=False):
    """
        Convert the case of the base name of files.
    """
    pv.path(directory, "given", False, True)
    pv.compstr(case, "case", ["lower", "title", "upper", "config"])
    pv.compstr(conflict_mode, "conflict mode", ["rename", "skip"])

    case = case.lower()
    conflict_mode = conflict_mode.lower()
    directory = os.path.abspath(directory)
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    if report_file == None:
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

    __check_config_mismatch(case, cfg_lower, cfg_title, cfg_mixed, cfg_upper)
    list_content, list_excluded = \
        common.get_files(directory, recursive, True, regex, False,
                         ignore_symlinks)

    for item in list_content:
        list_files = item[1]
        list_renamed, list_skipped = \
            __convert_case(list_files, list_renamed, list_skipped, case,
                           conflict_mode, recursive, cfg_lower, cfg_mixed,
                           cfg_title, cfg_upper)

    if simulate:
        list_header = []
        list_header.append("Nomen File Name Case Converter simulation report")
        list_header.append(["Report file name:", report_file])
        list_header.append(["Directory:", directory])
        list_header.append(["Recursive:", recursive])
        list_header.append(["Ignore symlinks:", ignore_symlinks])
        list_header.append(["Conflict mode:", conflict_mode.capitalize()])
        list_header.append(["Case:", case.capitalize()])
        list_header.append(["Lowercase config:", cfg_lower])
        list_header.append(["Mixed case config:", cfg_mixed])
        list_header.append(["Title case config:", cfg_title])
        list_header.append(["Uppercase config:", cfg_upper])

        common.report(report_file, list_header, list_renamed, list_excluded,
                      list_skipped, time_start)
    else:
        common.rename(list_renamed)

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def modify_names(directory, action, position, input_string,
                 replace_string=None, recursive=False, exclude=None,
                 pattern=None, ignore_case=True, regex_syntax=False,
                 report_file=None, ignore_symlinks=False, strip_chars=None):
    """
        Modify the base name of files by adding, removing or replacing a
        user-defined string.
    """
    pv.path(directory, "given", False, True)
    pv.compstr(action, "action", ["add", "remove", "replace"])
    pv.compstr(position, "position", ["any", "prefix", "suffix"])
    pv.string(input_string, "input string", False, common.get_invalid_chars())

    action = action.lower()
    position = position.lower()
    directory = os.path.abspath(directory)
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    if report_file == None:
        simulate = False
    else:
        pv.path(report_file, "report", True, False)
        report_file = os.path.abspath(report_file)
        simulate = True

    if not replace_string == None:
        if not action == "replace":
            raise Exception("The replace string argument can only be used " \
                            "together with the action 'replace'.")
        else:
            pv.string(replace_string, "string False", False,
                      common.get_invalid_chars())

    if action == "add" and position == "any":
        raise Exception("The position 'any' cannot be used together with " \
                        "the action 'add'.")

    if len(input_string) == 0:
        raise Exception("The input string must not be empty.")
    else:
        pv.string(input_string, "input string", False,
                  common.get_invalid_chars())

    if not strip_chars == None:
        pv.string(strip_chars, "strip chars string", False,
                  common.get_invalid_chars())

    time_start = dt.now()

    list_content = []
    list_excluded = []
    list_renamed = []
    list_skipped = []
    regex = None
    if not pattern == None:
        regex = common.compile_regex(pattern, ignore_case, regex_syntax)

    list_content, list_excluded = \
        common.get_files(directory, recursive, ignore_case, regex, exclude,
                         ignore_symlinks)
    for item in list_content:
        list_files = item[1]
        __modify_names(list_files, list_renamed, list_skipped, action,
                       position, input_string, replace_string, strip_chars)

    if simulate:
        explicit = None
        if exclude == None:
            exclude = False
            explicit = False
        elif exclude:
            explicit = False
        else:
            explicit = True

        list_header = []
        list_header.append("Nomen File Name Modifier simulation report")
        list_header.append(["Report file name:", report_file])
        list_header.append(["Directory:", directory])
        list_header.append(["Recursive:", recursive])
        list_header.append(["Ignore symlinks:", ignore_symlinks])
        list_header.append(["Action to perform:", action.capitalize()])
        list_header.append(["Position:", position.capitalize()])
        list_header.append(["Input string:", "\"" + input_string + "\" " \
                            "(without double quotes)"])
        if not replace_string == None:
            list_header.append(["Replace string:", "\"" + replace_string + \
                                "\" (without double quotes)"])
        if strip_chars == None:
            list_header.append(["Strip chars:", "None"])
        else:
            list_header.append(["Strip chars:", "\"" + strip_chars + "\" " \
                                "(without double quotes)"])

        list_header.append(["Exclude files:", exclude])
        list_header.append(["Explicit files:", explicit])
        list_header.append(["Pattern:", pattern])
        list_header.append(["Ignore case:", ignore_case])
        list_header.append(["Regex syntax:", regex_syntax])

        common.report(report_file, list_header, list_renamed, list_excluded,
                      list_skipped, time_start)
    else:
        common.rename(list_renamed)

def rename_files(directory, rename_mode, separator=" ", recursive=False,
                 padding=0, exclude=None, pattern=None, ignore_case=True,
                 regex_syntax=False, report_file=None, ignore_symlinks=False,
                 ignore_file_ext=False, custom_name=None, step=1,
                 order_by=None):
    """
        Rename the base name of files based on the name of the directory where
        they are stored in and add a numeric ID.
    """
    pv.path(directory, "given", False, True)
    pv.compstr(rename_mode, "rename mode",
               ["fill-gaps", "increase", "keep-order", "rename-new"])
    pv.intrange(padding, "padding", 0, 12, True)
    pv.string(separator, "seperator", False, common.get_invalid_chars())
    pv.intvalue(step, "step", True, False, False)

    if not order_by == None:
        pv.compstr(order_by, "order by", ["accessed", "created", "modified"])
        if not rename_mode == "keep-order":
            raise Exception("The order-by argument can only be used in " \
                            "combination with keep-order mode.")

    step = int(step)
    rename_mode = rename_mode.lower()
    directory = os.path.abspath(directory)
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    if report_file == None:
        simulate = False
    else:
        pv.path(report_file, "report", True, False)
        report_file = os.path.abspath(report_file)
        simulate = True

    if not custom_name == None:
        pv.string(custom_name, "custom file name", False,
                  common.get_invalid_chars())

    time_start = dt.now()

    list_content = []
    list_excluded = []
    list_renamed = []
    list_skipped = []
    regex = None
    if not pattern == None:
        regex = common.compile_regex(pattern, ignore_case, regex_syntax)

    list_content, list_excluded = \
        common.get_files(directory, recursive, ignore_case, regex, exclude,
                         ignore_symlinks, order_by)

    for item in list_content:
        list_files = item[1]
        if rename_mode == "fill-gaps":
            list_renamed, list_skipped = \
                __rename_files_fill(list_files, list_renamed, list_skipped,
                                    separator, padding, True, ignore_file_ext,
                                    custom_name, step)
        elif rename_mode == "rename-new":
            list_renamed, list_skipped = \
                __rename_files_fill(list_files, list_renamed, list_skipped,
                                    separator, padding, False,
                                    ignore_file_ext, custom_name, step)
        elif rename_mode == "keep-order":
            list_renamed, list_skipped = \
                __rename_files_keep_order(list_files, list_renamed,
                                          list_skipped, separator, padding,
                                          ignore_file_ext, custom_name, step,
                                          order_by)
        else:
            raise Exception("An invalid rename mode was given.")

    if simulate:
        if padding == 0:
            padding = "Set automatically"
        else:
            padding = str(padding)

        explicit = None
        if exclude == None:
            exclude = False
            explicit = False
        elif exclude:
            explicit = False
        else:
            explicit = True

        if order_by == "accessed":
            order_by = "Access time"
        elif order_by == "created":
            order_by = "Creation time"
        elif order_by == "modified":
            order_by = "Modification time"
        else:
            order_by = "False"

        list_header = []
        list_header.append("Nomen File Renamer simulation report")
        list_header.append(["Report file name:", report_file])
        list_header.append(["Directory:", directory])
        list_header.append(["Recursive:", recursive])
        list_header.append(["Ignore symlinks:", ignore_symlinks])
        list_header.append(["Rename mode:", rename_mode.capitalize()])
        list_header.append(["Order by time:", order_by])
        list_header.append(["Separator:", "\"" + separator + "\" " \
                            "(without double quotes)"])
        list_header.append(["Numeric padding:", padding])
        list_header.append(["Step size:", step])
        list_header.append(["Exclude files:", exclude])
        list_header.append(["Explicit files:", explicit])
        list_header.append(["Pattern:", pattern])
        list_header.append(["Ignore case:", ignore_case])
        list_header.append(["Regex syntax:", regex_syntax])

        common.report(report_file, list_header, list_renamed, list_excluded,
                      list_skipped, time_start)
    else:
        common.rename(list_renamed)

def __check_config_mismatch(case, cfg_lower, cfg_title, cfg_mixed, cfg_upper):
    """
        Check for a case config mismatch.
    """
    cfg_mismatch = False

    if case == "lower":
        if not cfg_lower == None:
            cfg_mismatch = True
    elif case == "title":
        if not cfg_title == None:
            cfg_mismatch = True
    elif case == "upper":
        if not cfg_upper == None:
            cfg_mismatch = True
    elif case == "config":
        if cfg_lower == None and \
           cfg_mixed == None and \
           cfg_title == None and \
           cfg_upper == None:
            raise Exception("The config target case requires at least one " \
                            "case config file to operate.")
    else:
        raise Exception("An unsupported case string was given.")

    if cfg_mismatch:
        if case == "title":
            case += " "
        raise Exception("Config file mismatch (cannot use %scase config " \
                        "file when using %scase as target case anyway)." % \
                        (case, case))

def __convert_case(list_files, list_renamed, list_skipped, case,
                   conflict_mode, recursive, cfg_lower, cfg_mixed, cfg_title,
                   cfg_upper):
    """
        Core method to convert the case of the base name of files.
    """
    file_ext = ""
    list_lower = []
    list_mixed = []
    list_title = []
    list_upper = []

    fs_case = common.get_fs_case_sensitivity(os.path.dirname(list_files[0]))

    if cfg_lower == None and cfg_mixed == None and \
       cfg_title == None and cfg_upper == None:
        static_case = False
    else:
        list_lower, list_mixed, list_title, list_upper = \
            statcase.parse_case_configs(cfg_lower, cfg_mixed, cfg_title,
                                        cfg_upper)
        static_case = True

    for file_path in list_files:
        num = 1
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]

        if os.path.extsep in file_name:
            file_ext = os.path.splitext(file_name)[1]
        else:
            file_ext = ""

        base_name = os.path.splitext(file_name)[0]
        if case == "lower":
            base_name_target = base_name.lower()
        elif case == "title":
            base_name_target = base_name.title()
        elif case == "upper":
            base_name_target = base_name.upper()
        else:
            base_name_target = base_name

        if static_case:
            base_name_target = __static_case(base_name_target, case,
                                             list_lower, list_mixed,
                                             list_title,
                                             list_upper).rstrip()

        file_newpath = file_path.replace(base_name + file_ext,
                                         base_name_target + file_ext)
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
                        file_path.replace(base_name,
                                          base_name_target + "_" + str(num))
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

def __fill_num_gaps(list_files, separator, padding, list_renamed,
                    list_skipped, fs_case, step):
    """
        Core method to fill numeration gaps.
    """
    list_temp = []
    list_temp.extend(list_skipped)

    for i in list_renamed:
        list_temp.append(i[2])
    list_temp.sort()
    list_gaps = __get_num_gaps(list_files, separator, padding, step)

    if len(list_gaps) > 0:
        list_gaps.sort(reverse=True)
        list_skipped.sort(reverse=True)

        while len(list_gaps) > 0:
            if len(list_skipped) < 1:
                break

            file_path = list_skipped.pop(0)
            list_path = file_path.split(os.path.sep)
            file_dir = list_path[-2]
            file_name = list_path[-1]

            if os.path.extsep in file_name:
                file_ext = os.path.splitext(file_name)[1]
            else:
                file_ext = ""

            num = list_gaps.pop(0)
            file_num = str(num).rjust(int(padding), "0")
            file_newname = file_dir + separator + \
                           file_num.replace(" ", "0") + file_ext
            file_newpath = file_path.replace(file_name, file_newname)

            if common.file_exists(file_newpath, list_renamed, fs_case):
                list_skipped.append(file_path)
            else:
                list_renamed.append([file_path, None, file_newpath])

    return list_renamed, list_skipped

def __get_num_gaps(list_files, separator, padding, step):
    """
        Method to determine numeration gaps.
    """
    list_gaps = []

    for i in range(len(list_files)):
        x = (i + 1) * step
        n = separator + str(x).rjust(int(padding),"0")
        if not any(n in s for s in list_files):
            list_gaps.append(int(n.replace(separator, "")))

    return list_gaps

def __modify_name_add(file_name, string, position):
    """
        Core method to add a string to the base name of a file.
    """
    file_newname = ""

    if position == "prefix":
        file_newname = string + file_name
    elif position == "suffix":
        file_newname = file_name + string

    return file_newname

def __modify_name_remove(file_name, string, position):
    """
        Core method to remove a string from the base name of a file.
    """
    file_newname = ""

    if position == "any":
        file_newname = file_name.replace(string, "")
    elif position == "prefix":
        file_newname = re.sub("^" + string, "", file_name)
    elif position == "suffix":
        file_newname = re.sub(string + "$", "", file_name)

    return file_newname

def __modify_name_replace(file_name, string, replace_string, position):
    """
        Core method to replace a string inside the base name of a file.
    """
    file_newname = ""

    if position == "any":
        file_newname = file_name.replace(string, replace_string)
    elif position == "prefix":
        file_newname = re.sub("^" + string, replace_string, file_name)
    elif position == "suffix":
        file_newname = re.sub(string + "$", replace_string, file_name)

    return file_newname

def __modify_names(list_files, list_renamed, list_skipped, action, position,
                   input_string, replace_string, strip_chars):
    """
        Core method to modify the base name of files by adding, removing or
        replacing a user-defined string.
    """
    for file_path in list_files:
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]
        file_newname = ""
        file_newpath = ""

        if os.path.extsep in file_name:
            file_temp = os.path.splitext(file_name)
            file_name = file_temp[0]
            file_ext = file_temp[1]
        else:
            file_ext = ""

        if action == "add":
            file_newname = __modify_name_add(file_name, input_string,
                                             position)
        elif action == "remove":
            file_newname = __modify_name_remove(file_name, input_string,
                                                position)
        elif action == "replace":
            file_newname = __modify_name_replace(file_name, input_string,
                                                 replace_string, position)

        if not strip_chars == None:
            if len(strip_chars) > 0:
                file_newname = file_newname.strip(strip_chars)

        file_newname += file_ext
        file_newpath = file_path.replace(file_name + file_ext, file_newname)
        if file_newpath == "":
            list_skipped.append(file_path)
        elif file_newname == "" or file_newname == file_ext:
            list_skipped.append(file_path)
        else:
            if file_path == file_newpath:
                list_skipped.append(file_path)
            else:
                if os.path.exists(file_newpath):
                    list_skipped.append(file_path)
                else:
                    list_renamed.append([file_path, None, file_newpath])

    return list_renamed, list_skipped

def __process_case_list(case, case_list):
    """
        Process a case list and separate words from regular expressions.
    """
    list_strings = []
    list_words = []

    for item in case_list:
        if case == "lower":
            if item.startswith("$("):
                list_strings.append(item.replace("$", "").lower())
            else:
                list_words.append(item.lower())
        elif case == "title":
            if item.startswith("$("):
                list_strings.append(item.replace("$", "").title())
            else:
                list_words.append(item.title())
        elif case == "upper":
            if item.startswith("$("):
                list_strings.append(item.replace("$", "").upper())
            else:
                list_words.append(item.upper())
        else:
            if item.startswith("$("):
                list_strings.append(item.replace("$", ""))
            else:
                list_words.append(item)

    return list_words, list_strings

def __rename_files_fill(list_files, list_renamed, list_skipped, separator,
                        padding, fill_gaps=False, ignore_file_ext=False,
                        custom_name=None, step=1):
    """
        Core method to rename the base name of files based on the name of the
        directory where they are stored in using one of the "fill" rename
        modes (such as "fill-gaps" and "rename-new").
    """
    file_newpath = ""
    num = 0

    fs_case = common.get_fs_case_sensitivity(os.path.dirname(list_files[0]))

    if fill_gaps:
        list_temp_renamed = []
        list_temp_skipped = []
        obj_ren = list_temp_renamed
        obj_skip = list_temp_skipped
    else:
        obj_ren = list_renamed
        obj_skip = list_skipped

    if padding == 0:
        padding = len(str(len(list_files)))

    for file_path in list_files:
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]

        if custom_name == None:
            file_dir = list_path[-2]
        else:
            file_dir = custom_name

        if os.path.extsep in file_name:
            file_ext = os.path.splitext(file_name)[1]
        else:
            file_ext = ""

        if file_name.startswith(file_dir + separator):
            try:
                temp = file_name.replace(file_dir + separator, "")
                list_pad = temp.split(".")
                file_padding = len(list_pad[0])

                if step > 1:
                    if int(list_pad[0]) % step == 0:
                        obj_skip.append(file_path)
                        continue
                else:
                    if int(padding) == file_padding:
                        obj_skip.append(file_path)
                        continue
            except:
                pass

        if not ignore_file_ext:
            num = 0

        file_newpath = file_path
        while common.file_exists(file_newpath, obj_ren, fs_case) or \
              common.file_exists(file_newpath, obj_skip, fs_case):
            num += step
            file_num = str(num).rjust(int(padding), "0")
            file_newname = \
                file_dir + separator + file_num.replace(" ", "0") + file_ext
            file_newpath = file_path.replace(file_name, file_newname)

        if os.path.exists(file_path):
            if file_path == file_newpath:
                obj_skip.append(file_path)
            else:
                obj_ren.append([file_path, None, file_newpath])

    if fill_gaps:
        list_temp_renamed, list_temp_skipped = \
             __fill_num_gaps(list_files, separator, padding,
                             list_temp_renamed, list_temp_skipped,
                             fs_case, step)
        list_renamed.extend(list_temp_renamed)
        list_skipped.extend(list_temp_skipped)

    return list_renamed, list_skipped

def __rename_files_keep_order(list_files, list_renamed, list_skipped,
                              separator, padding, ignore_file_ext=False,
                              custom_name=None, step=1, order_by=None):
    """
        Core method to rename the base name of files based on the name of the
        directory where they are stored in using "keep-order" rename mode.
    """
    file_newpath = ""
    file_temppath = ""
    temp_file_ext = ""
    list_new = []
    list_ren = []
    num = 0

    fs_case = common.get_fs_case_sensitivity(os.path.dirname(list_files[0]))

    if padding == 0:
        padding = len(str(len(list_files)))

    for file_path in list_files:
        list_path = file_path.split(os.path.sep)
        file_dir = list_path[-2]
        file_name = list_path[-1]

        if file_name.startswith(file_dir + separator):
            list_ren.append(file_path)
        else:
            list_new.append(file_path)

    list_files = []
    list_files.extend(list_ren)
    list_files.extend(list_new)

    for file_path in list_files:
        list_path = file_path.split(os.path.sep)
        file_name = list_path[-1]

        if custom_name == None:
            file_dir = list_path[-2]
        else:
            file_dir = custom_name

        if os.path.extsep in file_name:
            file_ext = os.path.splitext(file_name)[1]
        else:
            file_ext = ""

        if not ignore_file_ext:
            if not file_ext == temp_file_ext:
                num = 0

        file_temppath = file_path
        temp_file_ext = file_ext
        while common.file_exists(file_temppath, list_renamed, fs_case):
            num += step
            file_num = str(num).rjust(int(padding), "0")
            file_newname = \
                file_dir + separator + file_num.replace(" ", "0") + file_ext
            file_newpath = file_path.replace(file_name, file_newname)
            if not file_newpath in list_skipped:
                file_temppath = file_newpath + ".__temp__"

        if os.path.exists(file_path):
            if file_path == file_newpath:
                list_skipped.append(file_path)
            else:
                list_renamed.append([file_path, file_temppath, file_newpath])

    return list_renamed, list_skipped

def __static_case(base_name, case, list_lower, list_mixed, list_title,
                  list_upper):
    """
        Convert the case of the base name of a file to lowercase, mixed case,
        title case or uppercase based on the read out config files.
    """
    list_file_str = base_name.split(" ")
    list_cfg_str, list_cfg_regex = \
        __process_case_list("lower", list_lower)
    base_name = __static_case_word(list_cfg_str, list_file_str)
    base_name = __static_case_string(list_cfg_regex, base_name)

    list_file_str = base_name.split(" ")
    list_cfg_str, list_cfg_regex = \
        __process_case_list("mixed", list_mixed)
    base_name = __static_case_word(list_cfg_str, list_file_str)
    base_name = __static_case_string(list_cfg_regex, base_name)

    list_file_str = base_name.split(" ")
    list_cfg_str, list_cfg_regex = \
        __process_case_list("title", list_title)
    base_name = __static_case_word(list_cfg_str, list_file_str)
    base_name = __static_case_string(list_cfg_regex, base_name)

    list_file_str = base_name.split(" ")
    list_cfg_str, list_cfg_regex = \
        __process_case_list("upper", list_upper)
    base_name = __static_case_word(list_cfg_str, list_file_str)
    base_name = __static_case_string(list_cfg_regex, base_name)

    return base_name

def __static_case_word(list_cfg_str, list_file_str):
    """
        Convert the case of each word of the base name of a file.
    """
    base_name = ""

    for file_str in list_file_str:
        for cfg_str in list_cfg_str:
            spec_chars = "\\?*+$.:; ^|()[]{}"
            for char in spec_chars:
                cfg_str = cfg_str.replace(char, "")

            if file_str.lower() == cfg_str.lower():
                file_str = cfg_str

        base_name += (file_str + " ")

    return base_name

def __static_case_string(list_cfg_regex, base_name):
    """
        Convert the case of a string inside the base name of a file.
    """
    for item in list_cfg_regex:
        spec_chars = "\\?*+$.:;^|()[]{}"
        for char in spec_chars:
            item = item.replace(char, "")

        regex = re.compile(".*" + item.lower() + ".*")
        if regex.match(base_name.lower()):
            base_name = re.sub(item.lower(), item, base_name,
                               flags=re.IGNORECASE)

    return base_name

# EOF
