#!/usr/bin/env python
"""
_pylint_tools_

Wrapper for pylint execution


"""

import os
import re
import sys
from fabric.operations import local, settings, hide

import pep8


def find_modules(dirname):
    """
    _find_modules_

    recursively find python modules
    """
    result = []
    for f in os.listdir(dirname):
        abspath = os.path.join(dirname, f)
        # recurse into directories
        if os.path.isdir(abspath):
            result.extend(find_modules(abspath))
        # record py files:
        if f.endswith('.py'):
           result.append(abspath)
    return result


def pylint_file(filename, **kwargs):
    """
    apply pylint to the file specified,
    return the filename, score

    """
    command = "pylint "

    if 'rcfile' in kwargs:
        command += " --rcfile={0} ".format(kwargs['rcfile'])

    command += filename

    # we use fabric to run the pylint command, hiding the normal fab
    # output and warnings
    with hide('output','running','warnings'), settings(warn_only=True):
        result = local(command, capture=True)

    score = None
    # parse the output from pylint for the score
    for line in result.split('\n'):
        if  re.match("E....:.", line):
            print line
        if "Your code has been rated at" in line:
            score = re.findall("\d+.\d\d", line)[0]

    return filename, score


def pep8_file(filename, verbose=False):
    """
    _pep8_file_

    Run pep8 checker on a file, returning the filename, score
    as a tuple
    """
    pep8style = pep8.StyleGuide(quiet=True)
    result = pep8style.check_files([filename])
    if verbose:
        result.print_statistics()
    return filename, result.total_errors
