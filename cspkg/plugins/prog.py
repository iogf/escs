from cspkg.core import Namespace, Mode, Plugin
from cspkg.plugins.normal_mode import Normal

from os.path import splitext

class ProgNS(Namespace):
    pass

class Html(Mode):
    pass

class C(Mode):
    pass

class Javascript(Mode):
    pass

class Golang(Mode):
    pass

class Python(Mode):
    pass

class Tcl(Mode):
    pass

class Perl(Mode):
    pass

EXTS = {
    '.c' : C,
    '.py': Python,
    '.js': Javascript,
    '.go': Golang,
    '.html': Html,
    '.tcl': Tcl
}

class Prog(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(ProgNS, Normal, 
        '<Key-slash>', self.setmode)

    def setmode(self, event):
        filename = self.xstr.filename.lower()
        path, ext = splitext(filename)
        mode = EXTS.get(ext)

        if mode is not None:
            self.chmode(mode)
