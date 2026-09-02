from cspkg.core import Namespace, Main, Plugin, Normal

class WordJumpsNS(Namespace):
    pass

class WordJumps(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(WordJumpsNS, Main, 
        '<Alt-l>', self.next_word)

        self.add_kmap(WordJumpsNS, Main, 
        '<Alt-h>', self.prev_word)

    def next_word(self, event):
        """
        Place the cursor at the next word.
        """

        _, index0, index1 = self.xstr.isearch('\M', index='insert', 
        regexp=True, stopindex='end')

        self.xstr.mark_set('insert', index0)
        self.xstr.see('insert')

    def prev_word(self, event):
        """
        Place the cursor at the previous word.
        """

        _, index0, index1 = self.xstr.isearch('\M', backwards=True, 
        regexp=True, index='insert', stopindex='1.0')

        self.xstr.mark_set('insert', index1)
        self.xstr.see('insert')

install = WordJumps

