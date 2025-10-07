from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class SeqSelNS(Namespace):
    pass

class SeqSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(SeqSelNS, Normal, 
        '<Key-W>', self.select)

    def select(self, event):
        """
        """

        index1, index2 = self.xstr.seq_bounds()
        self.xstr.tag_add('sel', index1, index2)

install = SeqSel

