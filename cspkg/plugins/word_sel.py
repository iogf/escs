from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class WordSelNS(Namespace):
    pass

class WordSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(WordSelNS, Normal, 
        '<Key-w>', self.select)

    def select(self, event):
        """
        """

        index1, index2 = self.xstr.word_bounds()
        self.xstr.tag_add('sel', index1, index2)

install = WordSel

