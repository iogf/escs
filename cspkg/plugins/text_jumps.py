from cspkg.core import Namespace, Main, Plugin
from cspkg.plugins.normal_mode import Normal

class TextJumpsNS(Namespace):
    pass

class TextJumps(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.chmode(Normal)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-g>', self.text_start)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-s>', self.text_start)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-b>', self.text_end)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-c>', self.text_end)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-a>', self.line_start)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-o>', self.line_start)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-e>', self.line_end)

        self.add_kmap(TextJumpsNS, Normal,
        '<Key-p>', self.line_end)

        self.add_kmap(TextJumpsNS, Main, 
        '<Control-period>', self.next_word)

        self.add_kmap(TextJumpsNS, Main, 
        '<Control-comma>', self.prev_word)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-d>', self.down)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-j>', self.down)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-f>', self.up)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-k>', self.up)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-n>', self.left)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-h>', self.left)

        self.add_kmap(TextJumpsNS, Main, 
        '<Alt-m>', self.right)

        self.add_kmap(TextJumpsNS, Normal, 
        '<Key-l>', self.right)
    
    def down(self, event):
        event.widget.down()

    def up(self, event):
        event.widget.up()

    def left(self, event):
        event.widget.left()

    def right(self, event):
        event.widget.right()

    def text_start(self, event):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.see('insert')
    
    def text_end(self, event):
        self.xstr.mark_set('insert', 'end linestart')
        self.xstr.see('insert')

    def line_start(self, event):
        """
        Place the cursor at the beginning of the line.
        """

        self.xstr.mark_set('insert', 'insert linestart')

    def line_end(self, event):
        """
        Place the cursor at the end of the line.
        """

        self.xstr.mark_set('insert', 'insert lineend')

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

install = TextJumps


