# *Nomen* <img src="nomen.png" alt="Nomen logo" height="48px" width="48px" align="right"/>

**Table of contents**
*   [Definition](#definition)
*   [Details](#details)
*   [Requirements](#requirements)
*   [Documentation](#documentation)
*   [Useless facts](#useless-facts)

----

## Definition

The *Nomen* project is a multi-purpose rename tool to consistently rename the base name as well as the extension of files in a variety of ways and also to remove unnecessary whitespaces from directory names.

[Top](#nomen-)

## Details

Basically, *Nomen* allows to consistently rename the base name as well as the extension of files and to remove unnecessary whitespaces from directory names.

For now, it is capable of the following, briefly stated:

*   Convert the case of the base name (prefix or stem) of files.
*   Convert the case of the extension (suffix) of files.
*   Adjust differently spelled extensions from files of the same file type.
*   Rename base names based on the name of the directory where the files are stored in.
*   Modify base names by adding, removing or replacing certain strings.
*   Remove leading, trailing and duplicate whitespaces from directory names.

It also comes with an integrated simulation mode that simulates the rename process and writes the details into a report file. This allows checking which files would have been renamed.

The project also consists of [multiple components](../../wiki#components).

Please be sure to read [this](../../wiki#important-notice) before using *Nomen*.

[Top](#nomen-)

## Requirements

In order to run the latest versions of *Nomen*, the *Python* 3.x framework must be installed on the system.

Version 2.3.6 is the last official release for the *Python* 2.x framework.

If you need a later version for the *Python* 2.x framework for whatever reason, you can try refactoring the syntax from *Python* 3.x to version 2.x using the *[3to2](https://pypi.python.org/pypi/3to2)* tool.

However, there is no guarantee that this works properly or at all.

Depending on which version of the framework you are using:

*   *Python* 2.x (version 2.7 or higher is recommended, may also work with earlier versions)
*   *Python* 3.x (version 3.2 or higher is recommended, may also work with earlier versions)

[Top](#nomen-)

## Documentation

In the corresponding `docs` sub-directories, there are plain text files containing a detailed documentation for each component with further information and usage examples.

[Top](#nomen-)

## Useless facts

Whoever cares can find them [here](../../wiki#useless-facts).

[Top](#nomen-)
