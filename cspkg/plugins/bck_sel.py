from cspkg.core import Plugin, Namespace
from cspkg.plugins.normal_mode import Normal

class BckSelNS(Namespace):
    pass

class BckSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(BckSelNS, Normal, '<Key-a>', self.sel_inner)
        self.add_kmap(BckSelNS, Normal, '<Key-A>', self.sel_all)
    
    def sel_inner(self, event):
        """
        Select inner text between pair tokens.
        """

        token = self.xstr.get('insert', 'insert +1c')
        if token in self.lhs:
            self.xstr.tag_add('sel', 'insert +1c', 
                self.xstr.bck_check(token, self.lhs[token], 
                    'insert', self.MAX)[0])
        elif token in self.rhs:
            self.xstr.tag_add('sel', self.xstr.bck_check(self.rhs[token], 
                token, 'insert +1c', 
                    self.MAX, True)[1], 'insert')

    def sel_all(self, event):
        """
        Select text between pair tokens also the tokens.
        """

        token = self.xstr.get('insert', 'insert +1c')
        if token in self.lhs:
            self.xstr.tag_add('sel', 'insert', self.xstr.bck_check(
                token,self.lhs[token], 'insert', self.MAX)[1])
        elif token in self.rhs:
            self.xstr.tag_add('sel', self.xstr.bck_check(self.rhs[token], 
                token, 'insert +1c', self.MAX, True)[0], 'insert +1c')

    lhs = {
        '(': ')',
        '[': ']',
        '{': '}'
    }

    rhs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    MAX = 2500

install = BckSel
