from cspkg.panes import PanedVerticalWindow
from os.path import abspath, exists
from cspkg.xstr import Xstr
from tkinter.ttk import Notebook
from tkinter import BOTH

class EscsBook(Notebook):
    def __init__(self, *args, **kwargs):
        Notebook.__init__(self, *args, **kwargs)
        self.bindtags((self, '.', 'all'))

    def focus_restore(self):
        wid  = self.nametowidget(self.select())
        wid.fwidget.focus_set()

    def create(self, filename):
        """
        """

        base = PanedVerticalWindow(master=self)
        xstr = base.create(filename)
        self.add(base, text=filename)
        return xstr

    def open(self, filename):
        base = PanedVerticalWindow(master=self)
        self.add(base)
        xstr = base.open(filename)
        return xstr

    def load(self, *args):
        """
        """

        for indi in args:
            base = PanedVerticalWindow(master=self)
            base.pack(side='left', expand=True, fill=BOTH)
            self.add(base)        
            for indj in indi:
                base.load(*indj)

    def next(self, func):
        """
        """

        tabs  = self.tabs()
        index = self.index(self.select())

        for ind in tabs[index + 1:]:
            if func(self.tab(ind, 'text')): 
                yield ind
    
    def back(self, func):
        """
        """

        tabs  = self.tabs()
        index = self.index(self.select())
        tabs  = tabs[:index]

        for ind in reversed(tabs):
            if func(self.tab(ind, 'text')): 
                yield ind

    def find(self, func):
        for ind in self.tabs():
            if func(self.tab(ind, 'text')):
                yield ind

    def xseek(self, filename, auto_open=False):
        filename = abspath(filename)
        wids = Xstr.get_opened_files(self)
        xstr = wids.get(filename)

        if xstr is None:
            if exists(filename) and auto_open:
                return self.open(filename)
        return xstr

    def lseek(self, filename, line, auto_open=False):
        """
        """

        xstr = self.xseek(filename, auto_open)
        if xstr is not None:
            self.focus_line(xstr, line)
        return xstr

    def focus_line(self, xstr, line):
        self.select(xstr.master.master.master)
        xstr.focus()
        xstr.setcur(line, 0)

