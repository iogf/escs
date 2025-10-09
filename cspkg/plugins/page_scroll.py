from tkinter import SCROLL
from cspkg.core import Namespace, Plugin, Main

class PageScrollNS(Namespace):
    pass

class PageScroll(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(PageScrollNS, Main, '<Alt-greater>', self.scroll_up)
        self.add_kmap(PageScrollNS, Main, '<Alt-less>', self.scroll_down)

    def scroll_up(self, event):
        """
        It scrolls one page up.
        """

        self.xstr.yview(SCROLL, -1, 'page')
        self.xstr.mark_set('insert', '@0,0')

    def scroll_down(self, event):
        """
        It scrolls one page down.
        """

        self.xstr.yview(SCROLL, 1, 'page')
        self.xstr.mark_set('insert', '@0,0')


install = PageScroll




