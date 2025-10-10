"""
"""

from cspkg.core import Command, Plugin, Namespace
from subprocess import Popen, STDOUT, PIPE
from cspkg.plugins.python_mode import Python
from cspkg.plugins.normal_mode import Normal
from os.path import relpath
from cspkg.fwin import LinePicker
from cspkg.tools import get_project_root
from cspkg.start import root
from cspkg.stderr import printd
from re import findall
import sys

class TypeCheckerNS(Namespace):
    pass

class TypeChecker(Plugin):
    options = LinePicker()
    path    = 'mypy'

    def  __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(TypeCheckerNS, Python, 
        '<Key-k>', self.check_module)

        self.add_kmap(TypeCheckerNS, Python, 
        '<Key-o>', lambda event: self.options.display(self.xstr))

        self.add_kmap(TypeCheckerNS, Python, 
        '<Key-p>', self.check_all)

    @classmethod
    def c_path(cls, path):
        printd('Snakerr - Setting Mypy path = ', cls.path)
        cls.path = path

    def check_all(self, event=None):
        path  = get_project_root(self.xstr.filename)
        child = Popen([self.path,  path],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        regex  = '(.+?):([0-9]+):(.+)' 
        ranges = findall(regex, output)

        sys.stdout.write('Mypy errors: \n%s\n' % output)
        self.chmode(Normal)

        root.status.set_msg('Mypy errors: %s' % len(ranges))
        self.options.extend(ranges)
        if ranges:
            self.options.display(self.xstr)

    def check_module(self, event=None):
        path  = get_project_root(self.xstr.filename)
        child = Popen([self.path,  path],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        regex  = '(%s):([0-9]+):(.+)' % relpath(self.xstr.filename)
        ranges = findall(regex, output)
        sys.stdout.write('Mypy errors: \n%s\n' % output)
        self.chmode(Normal)

        root.status.set_msg('Mypy errors: %s' % len(ranges))
        self.options.extend(ranges)
        if ranges:
            self.options.display(self.xstr)


install = TypeChecker
@Command()
def py_static(xstr):
    checker = TypeChecker(xstr)
    checker.check_all()
