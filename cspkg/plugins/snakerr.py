from subprocess import Popen, STDOUT, PIPE
from os.path import relpath
from cspkg.fwin import LinePicker
from cspkg.core import Command, Namespace, Plugin
from cspkg.tools import get_project_root
from cspkg.plugins.python_mode import Python
from cspkg.plugins.normal_mode import Normal
from cspkg.start import root
from cspkg.stderr import printd
from re import findall
import sys

class SnakerrNS(Namespace):
    pass

class PythonChecker(Plugin):
    options = LinePicker()
    path    = 'pyflakes'

    def  __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(SnakerrNS, Python, '<Key-c>', self.check_module)
        self.add_kmap(SnakerrNS, Python, '<Key-h>', self.display_errors)
        self.add_kmap(SnakerrNS, Python, '<Key-l>', self.check_all)

    @classmethod
    def c_path(cls, path):
        printd('Snakerr - Setting Pyflakes path = ', cls.path)
        cls.path = path

    def display_errors(self, event=None):
        root.status.set_msg('Pyflakes previous errors!')
        self.options.display(self.xstr)
        self.chmode(Normal)

    def check_all(self, event=None):
        child = Popen([self.path,  get_project_root(self.xstr.filename)],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        # Pyflakes omit the column attribute when there are
        # syntax errors thus the (.+?) in the beggining of the
        # regex is necessary.
        regex  = '(.+?):([0-9]+):?[0-9]*:(.+)' 
        ranges = findall(regex, output)

        sys.stdout.write('Pyflakes found global errors:\n%s\n' % output)
        self.chmode(Normal)
        self.options.extend(ranges)
        root.status.set_msg('Pyflakes errors: %s' % len(ranges))

        if ranges:
            self.options.display(self.xstr)

    def check_module(self, event=None):
        child = Popen([self.path,  self.xstr.filename],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        regex  = '(%s):([0-9]+):?[0-9]*:(.+)' % relpath(self.xstr.filename)
        ranges = findall(regex, output)
        sys.stdout.write('Errors:\n%s\n' % output)
        self.chmode(Normal)
        self.options.extend(ranges)
        root.status.set_msg('Pyflakes errors: %s' % len(ranges))

        if ranges:
            self.options.display(self.xstr)
        
@Command()
def py_errors(xstr):
    python_checker = PythonChecker(xstr)
    python_checker.check_all()

install = PythonChecker

