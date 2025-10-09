
from cspkg.start import root
from cspkg.core import Plugin, Namespace, Main
from cspkg.core import Command
from cspkg.xstr import Xstr

class SplitsNS(Namespace):
    pass

@Command('vsplit')
def vsplit(xstr):
    """
    """
    xstr.master.master.master.create()

@Command('hsplit')
def hsplit(xstr):
    """    
    """
    xstr.master.master.create()

class Splits(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(SplitsNS, Main, 
        '<Alt-V>', self.add_horizontal_xstr)

        self.add_kmap(SplitsNS, Main, 
        '<Alt-C>', self.add_vertical_xstr)

        self.add_kmap(SplitsNS, Main, 
        '<Alt-X>', self.remove_xstr)
    
    def add_vertical_xstr(self, event):
        """
        It opens a vertical xstr.
        """
    
        vpane = self.xstr.master.master.master
        vpane.create()
    
        wids  = vpane.panes()
        height = root.winfo_height()//(len(wids) + 1)
        root.update()
    
        for ind in range(0, len(wids) - 1):
            vpane.sash_place(ind,  0,  (ind + 1) * height)
        # self.xstr.chmode('EXTRA')

    def add_horizontal_xstr(self, event):
        """
        It creates a new horizontal xstr.
        """
    
        hpane = self.xstr.master.master
        hpane.create()
    
        wids  = hpane.panes()
        width = root.winfo_width()//(len(wids) + 1)
        root.update()
    
        for ind in range(0, len(wids) - 1):
            hpane.sash_place(ind,  (ind + 1) * width,  0)
    
    def remove_xstr(self, event):
        """
        It removes the focused xstr.
        """
    
        vpanes = len(self.xstr.master.master.master.panes())
        hpanes = len(self.xstr.master.master.panes())
    
        if vpanes == 1 and hpanes == 1: return
        self.xstr.master.destroy()
    
        if not self.xstr.master.master.panes(): 
            self.xstr.master.master.destroy()
    
        wid  = root.note.nametowidget(root.note.select())
        seq  = Xstr.xstr_widgets(wid)
        xstr = next(seq)
        xstr.focus_set()

install = Splits
