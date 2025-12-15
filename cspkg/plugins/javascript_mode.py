from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class JavascriptModeNS(Namespace):
    pass

class Javascript(Mode):
    pass

class JavascriptMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(JavascriptModeNS, Normal, 
        '<Key-percent>', lambda event: self.chmode(Javascript))

install = JavascriptMode

