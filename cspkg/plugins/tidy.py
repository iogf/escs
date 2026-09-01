"""
"""

from subprocess import Popen, STDOUT, PIPE
from cspkg.plugins.normal_mode import Normal
from cspkg.plugins.prog import Html
from cspkg.fwin import LinePicker
from cspkg.core import Plugin, Namespace
from cspkg.stderr import printd
from cspkg.start import root
from re import findall
import sys

class TidyNS(Namespace):
    pass

class Tidy(Plugin):
    options = LinePicker(title='Tidy')
    path = 'tidy'

    def  __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(TidyNS, Html, '<Key-f>', self.check_code)
        self.add_kmap(TidyNS, Html, '<Key-h>', lambda event: 
        self.options.display(self.xstr))

    @classmethod
    def c_path(cls, path):
        printd('Tidy - Setting tidy path = ', cls.path)
        cls.path = path

    def check_code(self, event):
        child  = Popen([self.path, '--show-body-only', '1', '-e', '-quiet',
        self.xstr.filename], stdout=PIPE, stderr=STDOUT, 
        encoding=self.xstr.charset)

        output = child.communicate()[0]
        regex  = 'line ([0-9]+) column ([0-9]+) - (.+)'
        ranges = findall(regex, output)
        ranges = map(lambda ind: (self.xstr.filename, ind[0], ind[2]), ranges)
        ranges = tuple(ranges)

        sys.stdout.write('Errors:\n%s\n' % output)
        self.chmode(Normal)
        self.options.extend(ranges)
        root.status.set_msg('Tidy errors: %s' % len(ranges))

        if child.returncode:
            self.options.display(self.xstr)

install = Tidy
