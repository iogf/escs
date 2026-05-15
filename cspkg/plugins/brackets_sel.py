from cspkg.core import Plugin, Namespace
from cspkg.plugins.normal_mode import Normal

class BracketsSelNS(Namespace):
    pass

class BracketsSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(BracketsSelNS, Normal, '<Key-a>', self.sel_inner)
        self.add_kmap(BracketsSelNS, Normal, '<Key-A>', self.sel_all)
    
    def sel_inner(self, event):
        """
        Select inner text between pair tokens.
        """

        token = self.xstr.get('insert', 'insert +1c')
        if token in self.lhs:
            index = self.xstr.check_brackets(
                token, self.lhs[token], 'insert', self.MAX)
            if index is not None:
                self.xstr.tag_add('sel', 'insert +1c', index[0])
        elif token in self.rhs:
            index = self.xstr.check_brackets(self.rhs[token], 
                token, 'insert +1c', self.MAX, True)
            if index is not None:
                self.xstr.tag_add('sel', index[1], 'insert')

    def sel_all(self, event):
        """
        Select text between pair tokens also the tokens.
        """

        token = self.xstr.get('insert', 'insert +1c')
        if token in self.lhs:
            index = self.xstr.check_brackets(
                token,self.lhs[token], 'insert', self.MAX)
            if index is not None:
                self.xstr.tag_add('sel', 'insert', index[1])
        elif token in self.rhs:
            index = self.xstr.check_brackets(self.rhs[token], 
                    token, 'insert +1c', self.MAX, True)
            if index is not None:
                self.xstr.tag_add('sel', index[0], 'insert +1c')

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

install = BracketsSel
