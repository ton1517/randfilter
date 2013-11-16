randfilter
===========
This tool reads files or stdin and outputs random lines.

randfilter is tested with Python 2.6, 2.7, 3.2, 3.3.

Requirements
============
- Python 2.6 / 2.7 / 3.2 / 3.3 or higher
- docopt==0.6.1
- schema==0.2.0

Installation
============

Install from pypi
-----------------
::

    easy_install randfilter

or

::

    pip install randfilter

Install from github
-------------------
::

    git clone https://github.com/ton1517/randfilter.git
    cd randfilter
    python setup.py install


Usage
------
::

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

