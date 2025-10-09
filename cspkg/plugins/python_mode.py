from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class PythonModeNS(Namespace):
    pass

class Python(Mode):
    pass

class PythonMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(PythonModeNS, Normal, 
        '<Key-exclam>', self.python_mode)

    def python_mode(self, event):
        self.chmode(Python)

install = PythonMode

