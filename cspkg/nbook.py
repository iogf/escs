from cspkg.panes import PanedVerticalWindow
from os.path import abspath, exists
from cspkg.xstr import Xstr
from tkinter.ttk import Notebook
from os.path import exists
from tkinter import BOTH
import sys

class EscsBook(Notebook):
    def __init__(self, *args, **kwargs):
        Notebook.__init__(self, *args, **kwargs)
        self.bindtags((self, '.', 'all'))

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

    def on(self, *args):
        """
        """

        wid=self.focus_get()
        self.select(*args)
        self.after(30, lambda : wid.focus_set())

    def find_xstr(self, filename, auto_open=False):
        filename = abspath(filename)
        wids = Xstr.get_opened_files(self)
        xstr = wids.get(filename)

        if xstr is None:
            if exists(filename) and auto_open:
                return self.open(filename)
        return xstr

    def find_line(self, filename, line, col=0, auto_open=False):
        """
        """

        xstr = self.find_xstr(filename, auto_open)
        if xstr is not None:
            self.focus_line(xstr, line)
        return xstr

    def focus_line(self, xstr, line):
        self.select(xstr.master.master.master)
        xstr.focus()
        xstr.setcur(line, 0)

