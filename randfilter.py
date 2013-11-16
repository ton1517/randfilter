#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 ton1517 <tonton1517@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
randfilter

Usage:
    randfilter (-n <num> | -p <probability>) [-u | --unorder] [-i | --ignore-empty] [<files>...]
    randfilter -h | --help
    randfilter -v | --version

Options:
    <files>...          Choose and output lines at random in files. If omitted, use stdin.
    -n <num>            The choise number of lines.
    -p <probability>    The choise probability of lines. The value is 0.0 to 1.0.
    -u --unorder        Output lines are unordered.
    -i --ignore-empty   Ignore empty line.
    -h --help           Show this screen.
    -v --version        Show version.
"""

from __future__ import print_function
import sys
import itertools
import random

from docopt import docopt
from schema import Schema, SchemaError, And, Or, Use

#=======================================
# config
#=======================================

NAME = 'randfilter'
VERSION = '1.0.0'
LICENSE = 'MIT License'
DESCRIPTION = 'This tool reads files or stdin and outputs random lines.'
URL = 'https://github.com/ton1517/randfilter'
AUTHOR = 'ton1517'
AUTHOR_EMAIL = 'tonton1517@gmail.com'

#=======================================
# functions
#=======================================

def iter_files(opened_files, ignore_empty = False):
    """return generator includes all file's lines.
    Arg :
        opened_files: file object list
        ignore_empty: if ignore empty line, specify True.
    Return: iterator that includes all lines of files.
    """

    it = itertools.chain(*opened_files)

    for line in it:
        if ignore_empty and line.strip() == "":
            continue

        yield line

def validate_args(args):
    """validate arguments.
    Arg: dictionary of arguments.
    Return: validated dictionary.
    """

    schema = Schema({
        '-n': Or(None, And(Use(int), lambda n: 0 <= n), error="-n should be positive integer"),
        '-p': Or(None, And(Use(float), lambda n: 0.0 <= n <= 1.0), error="-p should be float 0 <= N <= 1.0"),
        '--unorder': bool,
        '--ignore-empty': bool,
        '--help': bool,
        '--version': bool,
        '<files>': [Use(open, error="Files should be readable")]
    })

    args = schema.validate(args)

    if len(args["<files>"]) == 0:
        args["<files>"].append(sys.stdin)

    return args

#=======================================
# random functions
#=======================================

def choose_random_lines_probability(files_iter, probability, unorder):
    """choose lines by random probability.
    Arg:
        files_iter: iterator by iter_files()
        probability: chosen probability. 0 <= n <= 1.0
        unorder: if you want fixed order, specify False.
    Return: list of lines chosen random.
    """
    lines = [line for line in files_iter if random.random() < probability]

    if unorder:
        random.shuffle(lines)

    return lines

def choose_random_lines_num(files_iter, num, unorder):
    """choose lines by random sampling.
    Arg:
        files_iter: iterator by iter_files()
        num: number of lines
        unorder: if you want fixed order, specify False.
    Return: list of lines chosen random.
    """
 
    lines = [line for line in files_iter]
    length = len(lines)
    num = length if num > length else num
    line_nums = random.sample(range(length), num)

    if not unorder:
        line_nums.sort()

    return [lines[i] for i in line_nums]

#=======================================
# main
#=======================================

def main():
    args = docopt(__doc__, version="{0} {1}".format(NAME, VERSION))

    try:
        args = validate_args(args)
    except SchemaError as e:
        print(e)
        sys.exit(1)

    it = iter_files(args["<files>"], args["--ignore-empty"])

    if not args["-n"] is None:
        lines = choose_random_lines_num(it, args["-n"], args["--unorder"])
    else:
        lines = choose_random_lines_probability(it, args["-p"], args["--unorder"])

    print("".join(lines), end="")

if __name__ == "__main__":
    main()
