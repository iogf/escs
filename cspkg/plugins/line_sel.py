from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class LineSelNS(Namespace):
    pass

class LineSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(LineSelNS, Normal, '<Key-f>', 
        lambda event: self.xstr.tag_toggle('sel', 
            'insert linestart', 'insert +1l linestart'))

install = LineSel



