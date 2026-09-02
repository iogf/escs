from cspkg.core import Namespace, Plugin, Normal

class TextShiftNS(Namespace):
    pass

class TextShift(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(TextShiftNS, Normal, 
        '<Key-greater>', self.shift_right)

        self.add_kmap(TextShiftNS, Normal, 
            '<Key-less>',  self.shift_left)

    def shift_right(self, event):
        """
        Shift ranges of selected text to the right.
        """
        srow, scol = self.xstr.indexsplit('sel.first')
        erow, ecol = self.xstr.indexsplit('sel.last')

        self.xstr.edit_separator()
        for ind in range(srow, erow + 1):
            self.xstr.insert('%s.0' % ind, self.xstr.tabchar) 
    
    def shift_left(self, event):
        """
        Shift ranges of selected text to the left.
        """

        srow, scol = self.xstr.indexsplit('sel.first')
        erow, ecol = self.xstr.indexsplit('sel.last')

        self.xstr.edit_separator()
        for ind in range(srow, erow + 1):
            self.xstr.delete('%s.0' % ind, '%s.%s' % (ind, 1)) 

install = TextShift



