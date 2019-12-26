#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Nomen - Multi-purpose rename tool
# Common core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/nomen
# GitLab: https://gitlab.com/urbanware-org/nomen
# ============================================================================

__version__ = "2.3.6"

import os
import paval as pv
import random
import re
import sys
import tempfile

from datetime import datetime as dt

def compile_regex(string, ignore_case=True, regex_syntax=False):
    """
        Compile a regular expression from the given pattern string.
    """
    pv.string(string, "regular expression", True, None)
    if regex_syntax:
        pattern = ".*" + string + ".*"
    else:
        spec_chars = [ "\\", ".", "^", "$", "+", "?", "{", "}", "[", "]",
                       "|", "(", ")" ]
        for char in spec_chars:
            string = string.replace(char, "\\" + char)
        string = string.strip("*").strip(";")
        while ("*" * 2) in string:
            string = string.replace(("*" * 2), "*")
        while (";" * 2) in string:
            string = string.replace((";" * 2), ";")

        list_string = string.split(";")
        if len(list_string) > 0:
            pattern = ""
            for crit in list_string:
                if not crit == "":
                    pattern += "(.*" + crit.replace("*", ".*") + ".*)|"
            pattern = pattern.rstrip("|")
            if pattern == "":
                raise Exception("The given string does not make sense this " \
                                "way.")

    if ignore_case:
        regex = re.compile(pattern, re.IGNORECASE)
    else:
        regex = re.compile(pattern)

    return regex

def confirm_notice():
    """
        Display a notice which must be confirmed by the user to proceed.
    """
    string = random_string(6, True, True, True, True)
    proceed = False
    notice_text = """           o      o                     o              88
           8      8                                    88
           8      8 .oPYo. oPYo. odYo. o8 odYo. .oPYo. 88
           8  db  8 .oooo8 8  '' 8' '8  8 8' '8 8    8 88
           'b.PY.d' 8    8 8     8   8  8 8   8 8    8
            '8  8'  'YooP8 8     8   8  8 8   8 'YooP8 88
                                                .    8
                                                'oooP'

Please use this tool with care to avoid data damage or loss!

There is no function to undo the changes done by this tool, so you
should be aware of what you are doing. Improper use (e.g. modifying
files inside system directories) will corrupt your system!

If you wish to proceed, type '%s' (case-sensitive, without any
quotes or spaces) and press the <Return> key. Otherwise, the process
will be canceled.""" % string

    print_text_box("", notice_text)
    choice = raw_input("> ")

    if choice == string:
        choice = "Proceeding."
        proceed = True
    else:
        choice = "Canceled."
    print "\n%s\n" % choice

    return proceed

def dir_space_modifier(directory, remove_duplicate=False,
                       remove_leading=False, remove_trailing=False,
                       brackets=False, hyphens=False, punctuation=False,
                       ignore_symlinks=False, recursive=False, exclude=None):
    """
        Modify a directory name by removing leading, trailing and duplicate
        spaces or by inserting and removing spaces next to punctuation
        characters.
    """

    list_exclude = []
    if not exclude == None:
        list_exclude = exclude.split(";")

    for item in os.listdir(directory):
        excluded = False
        if os.path.isdir(os.path.join(directory, item)):
            path = os.path.join(directory, item)
            for excl in list_exclude:
                if excl.lower() in path.lower():
                    excluded = True
                    break
        else:
            continue

        if excluded:
            nextdir = path
        else:
            if remove_duplicate:
                while (" " * 2) in item:
                    item = item.replace((" " * 2), " ")

            if hyphens:
                item = item.replace("-", " - ")
                while "-  " in item:
                    item = item.replace("-  ", "- ")
                while "  -" in item:
                    item = item.replace("  -", " -")

            if brackets:
                while "( " in item:
                    item = item.replace("( ", "(")
                item = item.replace("(", " (")
                while " )" in item:
                    item = item.replace(" )", ")")
                item = item.replace(")", ") ").replace(") .", ").")
                while "[ " in item:
                    item = item.replace("[ ", "[")
                item = item.replace("[", " [")
                while " ]" in item:
                    item = item.replace(" ]", "]")
                item = item.replace("]", "] ").replace("] .", "].")
                item = item.replace("( [", "([").replace("] )", "])")
                item = item.replace("[ (", "[(").replace(") ]", ")]")

            if punctuation:
                item = item.replace(".", ". ")
                while " ." in item:
                    item = item.replace(" .", ".")
                item = item.replace(",", ", ")
                while " ," in item:
                    item = item.replace(" ,", ",")
                item = item.replace(":", ": ")
                while " :" in item:
                    item = item.replace(" :", ":")
                item = item.replace(";", "; ")
                while " ;" in item:
                    item = item.replace(" ;", ";")
                item = item.replace("!", "! ")
                while " !" in item:
                    item = item.replace(" !", "!")
                item = item.replace("?", "? ")
                while " ?" in item:
                    item = item.replace(" ?", "?")
                remove_leading = True
                remove_trailing = True

            if remove_leading:
                item = item.lstrip()
            if remove_trailing:
                item = item.rstrip()

            newpath = os.path.join(directory, item)
            if remove_duplicate:
                # Repeat this step after the replace actions above
                while (" " * 2) in newpath:
                    newpath = newpath.replace((" " * 2), " ")

            if not os.path.exists(newpath):
                os.rename(path, newpath)
                nextdir = newpath
            else:
                nextdir = path

        if recursive:
            dir_space_modifier(nextdir, remove_duplicate, remove_leading,
                               remove_trailing, brackets, hyphens,
                               punctuation, ignore_symlinks, True, exclude)

def file_exists(file_path, list_files, fs_case_sensitive):
    """
        Check if a file already exists on the file system as well as in a
        given list.
    """
    file_path = os.path.abspath(file_path)
    if os.path.exists(file_path):
        file_exists = True
    else:
        file_exists = False

    for item in list_files:
        if item[1] == None:
            item[1] = ""

        if fs_case_sensitive:
            if file_path == item[1] or file_path == item[2]:
                file_exists = True
                break
        else:
            if file_path.lower() == item[1].lower() or \
               file_path.lower() == item[2].lower():
                file_exists = True
                break

    return file_exists

def format_timestamp(float_stamp=0):
    """
       Convert a timestamp float into a readable format.
    """
    return str(dt.fromtimestamp(float(str(float_stamp))))

def get_files(directory, recursive=False, ignore_case=True, regex=None,
              regex_exclude=True, ignore_symlinks=False, order_by=None):
    """
        Get the files and sub-directories from the given directory.
    """
    pv.path(directory, "given", False, True)

    directory = os.path.abspath(directory)
    list_files = []
    list_excluded = []

    list_files, list_excluded = \
        __get_files( \
            directory, ignore_case, regex, regex_exclude, ignore_symlinks,
            recursive, list_files, list_excluded, order_by)

    if order_by == None:
        list_files.sort()
    list_excluded.sort()

    return list_files, list_excluded

def get_fs_case_sensitivity(directory):
    """
        Determine if the file system of the given directory is case-sensitive.
    """
    # This should be done with every directory that is processed, due to the
    # fact, that e.g. a device containing a case-insensitive file system can
    # be mounted into a directory of a case-sensitive file system.

    pv.path(directory, "given", False, True)
    directory = os.path.abspath(directory)

    fd_temp, file_temp = tempfile.mkstemp(dir=directory)
    file_name = os.path.basename(file_temp)
    if os.path.exists(os.path.join(directory, file_name.upper())):
        fs_case_sensitive = False
    else:
        fs_case_sensitive = True
    os.close(fd_temp)
    os.remove(file_temp)

    return fs_case_sensitive

def get_invalid_chars():
    """
        Return the invalid file name characters (which must or should not be
        part of a file name).
    """
    # This list of characters depends on the file system where the files are
    # being renamed on. Due to the fact, that e.g. a device containing a
    # different file system can be mounted into a directory of the local file
    # system, the following characters will be handled as invalid on every
    # file system.
    invalid_chars = "/\\?%*:|\"<>\n\r\t"

    return invalid_chars

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def print_text_box(heading, text):
    """
        Print a text message outlined with an ASCII character frame.
    """
    heading = heading.strip()
    if len(heading) > 72:
        raise Exception("The text box heading must not be longer than 72 " \
                        "characters.")
    if text == "":
        raise Exception("The text box text must not be empty.")

    text_box = "\n+" + ("-" * 76) + "+" + \
               "\n|" + (" " * 76) + "|"
    if not heading == "":
        padding = int((72 - len(heading)) / 2)
        heading = (" " * (padding + 2) + heading).ljust(76, " ")
        text_box += ("\n|%s|\n|" + (" " * 76) + "|") % heading
    list_text = text.split("\n")
    for text in list_text:
        list_words = text.split(" ")
        count = 1
        line = ""
        for word in list_words:
            if len(line + word + " ") > 73:
                text_box += "\n|  " + line.ljust(74, " ") + "|"
                line = word + " "
            else:
                line = line + word + " "
            count += 1
            if count > len(list_words):
                text_box +=  "\n|  " + line.ljust(74, " ") + "|"
    text_box += "\n|" + (" " * 76) + "|" \
                "\n+" + ("-" * 76) + "+\n"

    print text_box

def random_string(length, uppercase=True, lowercase=False, numbers=False,
                  unique=False):
    """
        Generate a random string out of literals and numbers.
    """
    literals = "ABCDEFGHIJLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    chars = ""
    string = ""

    if uppercase:
        chars += literals
    if lowercase:
        chars += literals.lower()
    if numbers:
        chars += numbers

    if len(chars) == 0:
        return string
    if len(chars) < length:
        length = len(chars)

    while len(string) < length:
        rnd = random.randint(0, len(chars) - 1)
        char = chars[rnd]
        if unique:
            if char in string:
                continue
        string += char

    return string


def rename(list_files, reverse=False):
    """
        Rename the files which have neither been excluded nor skipped.
    """
    list_skipped = []

    if len(list_files) > 0:
        if reverse:
            list_files = reversed(list_files)

        for item in list_files:
            if os.path.exists(item[0]):
                if os.path.exists(item[2]):
                    list_skipped.append([item[0], item[1], item[2]])
                    continue

                # In some cases the file will get a temporary name first and
                # then its name will be changed to what it should be.
                #
                # This behavior is required when using file systems that are
                # case-insensitive (such as FAT32 or NTFS) where e.g. the
                # file "FOOBAR.txt" would overwrite the file "foobar.txt"
                # inside the same directory.
                if item[1] == None or \
                   item[1] == "":
                    os.rename(item[0], item[2])
                else:
                    os.rename(item[0], item[1])
                    os.rename(item[1], item[2])

        if len(list_skipped) > 0:
            if not list_skipped == list_files:
                rename(list_skipped, reverse)

def report(report_file=None, list_header=[], list_renamed=[],
           list_excluded=[], list_skipped=[], time_start=None):
    """
        Write the details of the simulated rename process (simulation report)
        into a file.
    """
    files_total = str(len(list_renamed) + len(list_excluded) + \
                      len(list_skipped))
    just = len(files_total)
    files_renamed = str(len(list_renamed)).rjust(just, " ")
    files_excluded = str(len(list_excluded)).rjust(just, " ")
    files_skipped = str(len(list_skipped)).rjust(just, " ")
    time_end = dt.now()

    try:
        time_elapsed = str(time_end - time_start)
        time_start = str(time_start)
    except:
        raise Exception("An invalid start date was given.")

    output = "\r\n" + "=" * 78 + \
             "\r\nFile type:          " + list_header[0] + \
             "\r\n" + "-" * 78

    for i in range(1, len(list_header)):
        output += "\r\n" + list_header[i][0].ljust(20, " ") + \
                  str(list_header[i][1])

    output += "\r\n" + "-" * 78 + \
              "\r\nFiles renamed:      " + files_renamed + \
              "\r\nFiles excluded:     " + files_excluded + \
              "\r\nFiles skipped:      " + files_skipped + \
              "\r\nFiles total:        " + files_total + \
              "\r\n" + "-" * 78 + \
              "\r\nTimestamp:          " + time_start[:-7] + \
              "\r\nElapsed time:       " + time_elapsed + \
              "\r\nNomen version:      " + __version__ + \
              "\r\n" + "=" * 78 + "\r\n\r\n"

    if len(list_renamed) > 0:
        output += "\r\n  [Renamed]\r\n"
        for item in list_renamed:
            output += "    - Old: %s\r\n" % item[0]
            output += "    - New: %s\r\n\r\n" % item[2]
        output += "\r\n"

    if len(list_excluded) > 0:
        output += "\r\n  [Excluded]\r\n"
        for item in list_excluded:
            output += "    - %s\r\n" % item
        output += "\r\n"

    if len(list_skipped) > 0:
        output += "\r\n  [Skipped]\r\n"
        for item in list_skipped:
            output += "    - %s\r\n" % item
        output += "\r\n"

    fh_report = open(report_file, "wb")

    # Run the appropriate code for the Python framework used
    if sys.version_info[0] == 2:
        fh_report.write(output)
    elif sys.version_info[0] > 2:
        fh_report.write(output.encode(sys.getdefaultencoding()))

    fh_report.close()

def __get_files(directory, ignore_case, regex, regex_exclude, ignore_symlinks,
                recursive, list_content, list_excluded, order_by):
    """
        Core method to get the files from the given directory and its
        sub-directories.
    """
    list_dirs = []
    list_files = []

    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if ignore_symlinks:
            if os.path.islink(path):
                continue
        if os.path.isfile(path):
            if regex == None:
                list_files.append(path)
            else:
                if regex_exclude:
                    if ignore_case:
                        if regex.match(item.lower()):
                            list_excluded.append(path)
                        else:
                            list_files.append(path)
                    else:
                        if regex.match(item):
                            list_excluded.append(path)
                        else:
                            list_files.append(path)
                else:
                    if ignore_case:
                        if regex.match(item.lower()):
                            list_files.append(path)
                        else:
                            list_excluded.append(path)
                    else:
                        if regex.match(item):
                            list_files.append(path)
                        else:
                            list_excluded.append(path)
        else:
            list_dirs.append(path)

    if len(list_files) > 0:
        if order_by == None:
            list_files.sort()
        else:
            list_files = __set_order(list_files, order_by)
        list_content.append([directory, list_files])

    if recursive:
        for directory in list_dirs:
            list_content, list_excluded = \
                __get_files(directory, ignore_case, regex, regex_exclude,
                            ignore_symlinks, True, list_content,
                            list_excluded, order_by)

    return list_content, list_excluded

def __set_order(file_list, order_by):
    """
        Set a certain order of the files before renaming them.
    """
    list_files = []
    list_temp = []

    for file_name in file_list:
        if "." in file_name:
            file_ext = file_name.split(".")[-1]
        else:
            file_ext = ""

        time_access = format_timestamp(os.stat(file_name).st_atime)
        time_create = format_timestamp(os.stat(file_name).st_ctime)
        time_modify = format_timestamp(os.stat(file_name).st_mtime)

        if order_by == "accessed":
            list_temp.append([time_access, file_name, file_ext])
        elif order_by == "created":
            list_temp.append([time_create, file_name, file_ext])
        else:
            list_temp.append([time_modify, file_name, file_ext])

    list_temp.sort()
    for item in list_temp:
        list_files.append(item[1])

    return list_files

# EOF
