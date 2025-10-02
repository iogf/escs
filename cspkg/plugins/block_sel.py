from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class BlockSelNS(Namespace):
    pass

class BlockSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(BlockSelNS, Normal, '<Control-v>', self.sel_add)
        self.add_kmap(BlockSelNS, Normal, '<Control-x>', self.sel_del)

    def sel_del(self, event):
        index0 = self.xstr.index('(SEL_MARK)')

        index1, index2   = self.xstr.indexsplit('insert')

        index3 = self.xstr.min(index0, '%s.%s' % (index1, index2))
        index4 = self.xstr.max(index0, '%s.%s' % (index1, index2))

        a, b   = self.xstr.indexsplit(index3)
        c, d   = self.xstr.indexsplit(index4)

        for ind in range(a, c + 1):
            self.xstr.rmsel('%s.%s' % (ind, min(b, d)),  
                '%s.%s' % (ind, max(b, d)))

    def sel_add(self, event):
        """  
        """

        index0 = self.xstr.index('(SEL_MARK)')

        index1, index2   = self.xstr.indexsplit('insert')

        index3 = self.xstr.min(index0, '%s.%s' % (index1, index2))
        index4 = self.xstr.max(index0, '%s.%s' % (index1, index2))
        a, b   = self.xstr.indexsplit(index3)
        c, d   = self.xstr.indexsplit(index4)

        for ind in range(a, c + 1):
            self.xstr.addsel('%s.%s' % (ind, min(b, d)), 
                '%s.%s' % (ind, max(b, d)))

install = BlockSel


