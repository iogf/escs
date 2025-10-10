
from cspkg.core import Namespace, Command, Plugin
from cspkg.plugins.python_mode import Python
from cspkg.plugins.normal_mode import Normal
from subprocess import Popen, STDOUT, PIPE
from os.path import relpath
from cspkg.fwin import LinePicker
from cspkg.tools import get_project_root
from cspkg.stderr import printd
from cspkg.start import root
from re import findall
import sys

class DeadCodeNS(Namespace):
    pass

class DeadCode(Plugin):
    options = LinePicker()
    path    = 'vulture'

    def  __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(DeadCodeNS, Python, 
        '<Key-d>', self.check_module)

        self.add_kmap(DeadCodeNS, Python, 
        '<Key-f>', lambda event: 
        self.options.display(self.xstr))

        self.add_kmap(DeadCodeNS, Python, 
        '<Key-g>', self.check_all)

    @classmethod
    def c_path(cls, path):
        printd('Deadcode - Setting Vulture path = ', cls.path)
        cls.path = path
    
    def check_all(self, event=None):
        path  = get_project_root(self.xstr.filename)
        child = Popen([self.path,  path],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        regex  = '(.+):([0-9]+):?[0-9]*:(.+)' 
        ranges = findall(regex, output)
        sys.stdout.write('Vulture found global errors:\n%s\n' % output)
        self.options.extend(ranges)

        root.status.set_msg('Vulture errors: %s' % len(ranges))
        self.chmode(Normal)
        if ranges:
            self.options.display(self.xstr)

    def check_module(self, event=None):
        path  = get_project_root(self.xstr.filename)
        child = Popen([self.path,  path],
        stdout=PIPE, stderr=STDOUT, encoding=self.xstr.charset)
        output = child.communicate()[0]

        regex  = '(%s):([0-9]+):?[0-9]*:(.+)' % relpath(self.xstr.filename)
        ranges = findall(regex, output)

        sys.stdout.write('%s errors:\n%s\n' % (self.xstr.filename, output))
        self.options.extend(ranges)

        root.status.set_msg('Vulture errors: %s' % len(ranges))
        self.chmode(Normal)
        if ranges:
            self.options.display(self.xstr)
        
install = DeadCode
@Command()
def py_analysis(xstr):
    python_analysis = DeadCode(xstr)
    python_analysis.check_all()

