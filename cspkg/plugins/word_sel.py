from cspkg.core import Namespace, Plugin, Normal

class WordSelNS(Namespace):
    pass

class WordSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(WordSelNS, 
        Normal, '<Key-w>', self.select_word)
        self.add_kmap(WordSelNS, 
            Normal, '<Key-W>', self.select_nonblank)

    def select_word(self, event):
        """
        """

        index1, index2 = self.xstr.word_bounds()
        self.xstr.tag_add('sel', index1, index2)

    def select_nonblank(self, event):
        index1, index2 = self.xstr.seq_bounds()
        self.xstr.tag_add('sel', index1, index2)

install = WordSel

