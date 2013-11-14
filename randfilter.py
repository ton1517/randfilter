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
    randfilter [-n <num> | -p <probability>] [-u | --unorder] [<files>...]
    randfilter -h | --help
    randfilter -v | --version

Options:
    <files>...          Choose and output lines at random in files. If omitted, use stdin.
    -n <num>            The choise number of lines.
    -p <probability>    The choise probability of lines. The value is 0.0 to 1.0.
    -u --unorder        Output lines are unordered.
    -h --help           Show this screen.
    -v --version        Show version.
"""

import sys

from docopt import docopt
from schema import Schema, SchemaError, And, Or, Use

#=======================================
# config
#=======================================

NAME = 'randfilter'
VERSION = '0.0.1'
LICENSE = 'MIT License'
DESCRIPTION = ''
URL = 'https://github.com/ton1517/randfilter'
AUTHOR = 'ton1517'
AUTHOR_EMAIL = 'tonton1517@gmail.com'

#=======================================
# functions
#=======================================

def validate_args(args):
    """validate arguments."""

    schema = Schema({
        '-n': Or(None, And(Use(int), lambda n: 0 <= n), error="-n should be positive integer"),
        '-p': Or(None, And(Use(float), lambda n: 0.0 <= n <= 1.0), error="-p should be float 0 <= N <= 1.0"),
        '--unorder': bool,
        '--help': bool,
        '--version': bool,
        '<files>': [Use(open, error="Files should be readable")]
    })

    try:
        args = schema.validate(args)
    except SchemaError as e:
        print(e)
        sys.exit(1)

    return args

#=======================================
# main
#=======================================

def main():
    args = docopt(__doc__, version="{0} {1}".format(NAME, VERSION))
    args = validate_args(args)

if __name__ == "__main__":
    main()
