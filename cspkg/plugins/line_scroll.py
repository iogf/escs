"""
"""

from tkinter import SCROLL
from cspkg.core import Namespace, Plugin, Main

class LineScrollNS(Namespace):
    pass

class LineScroll(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(LineScrollNS, Main, '<Alt-period>', self.scroll_up)

        self.add_kmap(LineScrollNS, Main, '<Alt-comma>', self.scroll_down)

    def scroll_up(self, event):
        """
        """

        self.xstr.yview(SCROLL, -1, 'units')
        is_visible = self.xstr.dlineinfo('insert')

        if not is_visible:
            self.xstr.mark_set('insert', 'insert -1l')

    def scroll_down(self, event):
        """
        It scrolls one line down.
        """

        self.xstr.yview(SCROLL, 1, 'units')
        is_visible = self.xstr.dlineinfo('insert')

        if not is_visible:
            self.xstr.mark_set('insert', 'insert +1l')

install = LineScroll

