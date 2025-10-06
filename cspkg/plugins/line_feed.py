from cspkg.core import Namespace, Main, Plugin
from cspkg.plugins.normal_mode import Normal
from cspkg.plugins.insert_mode import Insert

class LineFeedNS(Namespace):
    pass

class LineFeed(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(LineFeedNS, Normal, '<Key-m>', self.insert_down)
        self.add_kmap(LineFeedNS, Normal, '<Key-n>', self.insert_up)

    def insert_down(self, event):
        """
        """

        self.xstr.edit_separator()
        self.xstr.insert('insert +1l linestart', '\n', '')
        self.xstr.mark_set('insert', 'insert +1l linestart')
        self.xstr.clear_selection()

        self.xstr.see('insert')
        self.chmode(Insert)

    def insert_up(self, event):
        """
        """

        self.xstr.edit_separator()
        self.xstr.insert('insert linestart', '\n', '')
        self.xstr.mark_set('insert', 'insert -1l linestart')
        self.xstr.clear_selection()

        self.xstr.see('insert')
        self.chmode(Insert)

install = LineFeed

