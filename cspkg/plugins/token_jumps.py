from re import escape
from cspkg.core import Plugin, Namespace, Normal

class TokenJumpsNS(Namespace):
    pass

class TokenJumps(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(TokenJumpsNS, Normal, 
        '<Key-bracketright>', self.next_sym)
        self.add_kmap(TokenJumpsNS, Normal, 
        '<Key-bracketleft>', self.prev_sym)

        self.chars = ('(', ')', '[', ']', '{', '}')

    def next_sym(self, event):
        """
        Place the cursor at the next occurrence of one of the chars.
        """
        
        chars = [escape(ind) for ind in self.chars]
        REG   = '|'.join(chars)

        _, index0, index1 = self.xstr.isearch(REG, index='insert',
        stopindex='end', regexp=True)

        self.xstr.mark_set('insert', index1)
        self.xstr.see('insert')

    def prev_sym(self, event):
        """
        Place the cursor at the previous occurrence of one of the chars.
        """

        chars = [escape(ind) for ind in self.chars]
        REG   = '|'.join(chars)

        _, index0, index1 = self.xstr.isearch(REG,  index='insert', 
        backwards=True, stopindex='1.0', regexp=True)

        self.xstr.mark_set('insert', index0)
        self.xstr.see('insert')

install = TokenJumps


