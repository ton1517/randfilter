# -*- coding: utf-8 -*-

import sys
import random

from nose.tools import *
from mock import patch
from docopt import docopt, DocoptExit
from schema import Schema, SchemaError, And, Or, Use

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

class TestIterFiles(object):

    def test_iter_files(self):
        files = [open("testfiles/testfile1"), open("testfiles/testfile2")]

        lines = files[0].readlines() + files[1].readlines()

        for i, line in enumerate(randfilter.iter_files(files)):
            eq_(line, lines[i])

    def test_iter_files_ignore_empty(self):
        files = [open("testfiles/testfile1"), open("testfiles/testfile2")]

        lines = []
        correct_length = 0

        for i in  range(20):
            lines.append(str(i+1)+"\n")
            correct_length += 1

        length = 0
        for i, line in enumerate(randfilter.iter_files(files, True)):
            length += 1
            eq_(line, lines[i])

        eq_(correct_length, length)

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
    def test_no_options(self):
        argv = ["LICENSE", "README.rst"]
        args = self.parse_args(argv)

    @raises(DocoptExit)
    def test_duplicate_options(self):
        argv = ["-n", "10", "-n" "8", "LICENSE", "README.rst"]
        args = self.parse_args(argv)

    @raises(DocoptExit)
    def test_exclusive_options(self):
        argv = ["-n", "10", "-p" "0.8", "LICENSE", "README.rst"]
        args = self.parse_args(argv)


class TestValidateArgValues(object):

    def validate(self, *k):
        args = make_docdict(*k)
        return randfilter.validate_args(args)

    def test_type(self):
        args = make_docdict([], "1", "0.5", False, False, False, False)
        args = randfilter.validate_args(args)

        eq_(type(args["<files>"]), list)
        eq_(type(args["-n"]), int)
        eq_(type(args["-p"]), float)
        eq_(type(args["--unorder"]), bool)
        eq_(type(args["--ignore-empty"]), bool)
        eq_(type(args["--help"]), bool)
        eq_(type(args["--version"]), bool)

    @raises(SchemaError)
    def test_validate_n_type(self):
        """should be interger"""
        args = self.validate([], "0.1", None, False, False, False, False)

    def test_validate_n_range(self):
        """should be positive interger"""
        args = self.validate([], "0", None, False, False, False, False)
        eq_(args["-n"], 0)

        args = self.validate([], "1000000000000", "0.5", False, False, False, False)
        eq_(args["-n"], 1000000000000)

    @raises(SchemaError)
    def test_validate_n_range2(self):
        args = self.validate([], "-1", None, False, False, False, False)

    def test_validate_p_type(self):
        """should be float"""

        args = self.validate([], None, "1", False, False, False, False)
        eq_(args["-p"], 1.0)

    @raises(SchemaError)
    def test_validate_p_type2(self):
        args = self.validate([], None, "hoge", False, False, False, False)

    def test_validate_p_range(self):
        """should be float 0 <= N <= 1.0"""
        args = self.validate([], None, "0.0", False, False, False, False)
        eq_(args["-p"], 0.0)

        args = self.validate([], None, "1.0", False, False, False, False)
        eq_(args["-p"], 1.0)

    @raises(SchemaError)
    def test_validate_p_range2(self):
        args = self.validate([], None, "-0.1", False, False, False, False)

    @raises(SchemaError)
    def test_validate_p_range2(self):
        args = self.validate([], None, "1.1", False, False, False, False)

    def test_validate_files(self):
        args = self.validate([], None, "0.1", False, False, False, False)
        eq_(args["<files>"], [sys.stdin])

        args = self.validate(["LICENSE"], None, "0.1", False, False, False, False)
        import io
        ok_(type(args["<files>"][0] is io.IOBase))

    @raises(SchemaError)
    def test_dummy_files(self):
        args = self.validate(["HOGE"], None, "0.1", False, False, False, False)
        print(args)

class TestChooseRandomLinesProbability(object):

    @patch("random.random", lambda: 0)
    def test_all(self):
        filename = "testfiles/testfile1"
        f = [open(filename)]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_probability(it, 0.5, False)

        lines = open(filename).readlines()

        for i, item in enumerate(l):
            eq_(item, lines[i])

    @patch("random.random", lambda: 0.5)
    def test_border(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_probability(it, 0.5, False)

        eq_(l, [])

    @patch("random.random", lambda: 0)
    def test_order(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, True)
        l = randfilter.choose_random_lines_probability(it, 0.5, False)

        for i, line in enumerate(l):
            eq_(line, str(i+1)+"\n")

    def test_unorder(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_probability(it, 1, True)

        correct_lines= open("testfiles/testfile1").readlines()

        ok_(l != correct_lines)

class TestChooseRandomLinesNum(object):

    def test_all(self):
        filename = "testfiles/testfile1"
        f = [open(filename)]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_num(it, 100, False)

        lines = open(filename).readlines()

        for i, item in enumerate(l):
            eq_(item, lines[i])

    def test_zero(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_num(it, 0, False)

        eq_(l, [])

    def test_order(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, True)
        l = randfilter.choose_random_lines_num(it, 100, False)

        for i, line in enumerate(l):
            eq_(line, str(i+1)+"\n")

    def test_unorder(self):
        f = [open("testfiles/testfile1")]
        it = randfilter.iter_files(f, False)
        l = randfilter.choose_random_lines_num(it, 100, True)

        correct_lines= open("testfiles/testfile1").readlines()

        ok_(l != correct_lines)

