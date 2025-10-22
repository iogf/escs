from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class GolangNS(Namespace):
    pass

class Golang(Mode):
    pass

class GolangMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(GolangNS, Normal, 
        '<Key-numbersign>', self.golang_mode)

    def golang_mode(self, event):
        self.chmode(Golang)

install = GolangMode

