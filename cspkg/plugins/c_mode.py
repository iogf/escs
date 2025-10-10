from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class CNS(Namespace):
    pass

class C(Mode):
    pass

class CMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(CNS, Normal, '<Key-dollar>', self.c_mode)

    def c_mode(self, event):
        self.chmode(C)

install = CMode

