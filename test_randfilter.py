# -*- coding: utf-8 -*-

import sys

from nose.tools import *
from docopt import docopt, DocoptExit

import randfilter


def make_docdict(f, n, p, u, i, h, v):
    return {
        '-n':n,
        '-p':p,
        '--unorder':u,
        '--ignore-empty':i,
        '--help':h,
        '--version':v,
        '<files>':f
    }

class TestCommandlineArgs(object):

    def parse_args(self, argv):
        return docopt(randfilter.__doc__, argv)

    def test_normal_case(self):
        argv = ["-n", "10", "LICENSE", "README.rst"]
        args = self.parse_args(argv)

        correct_dict = make_docdict(["LICENSE", "README.rst"], "10", None, False, False, False, False)
        eq_(args, correct_dict)

    def test_normal_case2(self):
        argv = ["-n", "2", "-u"]
        args = self.parse_args(argv)
        correct_dict = make_docdict([], "2", None, True, False, False, False)
        eq_(args, correct_dict)

    def test_normal_case3(self):
        argv = ["-p", "0.2", "-u", "-i"]
        args = self.parse_args(argv)
        correct_dict = make_docdict([], None, "0.2", True, True, False, False)
        eq_(args, correct_dict)

    @raises(DocoptExit)
    def test_duplicate_options(self):
        argv = ["-n", "10", "-n" "8", "LICENSE", "README.rst"]
        args = self.parse_args(argv)

    @raises(DocoptExit)
    def test_exclusive_options(self):
        argv = ["-n", "10", "-p" "0.8", "LICENSE", "README.rst"]
        args = self.parse_args(argv)

