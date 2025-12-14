from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class GolangModeNS(Namespace):
    pass

class Golang(Mode):
    pass

class GolangMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(GolangModeNS, Normal, 
        '<Key-numbersign>', lambda event: self.chmode(Golang))

install = GolangMode

