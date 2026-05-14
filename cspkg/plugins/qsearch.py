"""

"""

from cspkg.scan import Read
from cspkg.tools import build_regex
from cspkg.stderr import printd
from cspkg.start import root
from tkinter import Listbox, Toplevel,  BOTH, END, TOP, ACTIVE, Text, LEFT, SCROLL
from cspkg.core import Namespace, Main, Plugin

class QSearchNS(Namespace):
    pass

class QSearch(Plugin):
    confs = {
        '(QSEARCH)': {
        'background':'yellow', 'foreground':'black'}
    }

    nocase = True
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr   = xstr
        xstr.tag_update(**self.confs)

        self.add_kmap(QSearchNS, Main, '<Alt-k>', self.backwards)
        self.add_kmap(QSearchNS, Main, '<Alt-j>', self.forwards)

        # self.add_kmap(QSearchNS, Main, '<Key-bracketleft>', self.backwards)
        # self.add_kmap(QSearchNS, Main, '<Key-bracketright>', self.forwards)

    @classmethod
    def c_appearance(cls, confs):
        """
        """

        cls.confs.update(confs)
        printd('Quick Search - Setting confs = ', cls.confs)

    def forwards(self, event):
        self.index     = self.xstr.index('insert')
        self.stopindex = 'end'
        self.backwards = False

        Read(events = {
        '<Alt-p>':self.search_down, 
        '<Alt-o>': self.search_up, 
        '<Control-n>': self.toggle_nocase, 
        '<<Data>>': self.update, 
        '<BackSpace>': self.update,
        '<Escape>':  self.end_search})

    def toggle_nocase(self, read):
        self.nocase = False if self.nocase else True
        root.status.set_msg('nocase=%s' % self.nocase)

    def end_search(self, read):
        self.xstr.tag_remove('(QSEARCH)', '1.0', 'end')
        read.done()

    def backwards(self, event):
        self.index     = self.xstr.index('insert')
        self.backwards = True
        self.stopindex = '1.0'

        Read(events = {
        '<Alt-p>':self.search_down, 
        '<Alt-o>': self.search_up, 
        '<<Data>>': self.update, 
        '<BackSpace>': self.update,
        '<Escape>':  self.end_search})

    def update(self, read):
        """

        """
        data    = read.text()
        pattern = build_regex(data)
        root.status.set_msg('Pattern:%s' % pattern)
        self.xstr.ipick('(QSEARCH)', pattern,
        verbose=True, backwards=self.backwards, index=self.index, 
        nocase=self.nocase, stopindex=self.stopindex)

    def search_up(self, read):
        """

        """
        data    = read.text()
        pattern = build_regex(data)
        self.xstr.ipick('(QSEARCH)', pattern, index='insert', 
        nocase=self.nocase, stopindex='1.0', backwards=True)

    def search_down(self, read):
        """

        """
        data    = read.text()
        pattern = build_regex(data)
        self.xstr.ipick('(QSEARCH)', pattern, 
        nocase=self.nocase, stopindex='end', index='insert')

install = QSearch


