"""
Overview
========


Commands
========


"""
from cspkg.xstr import Xstr
from cspkg.start import root
from cspkg.core import Plugin, Main, Namespace

class PaneJumpsNS(Namespace):
    pass

class PaneJumps(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(PaneJumpsNS, Main, 
        '<Alt-H>', self.jump_left)

        self.add_kmap(PaneJumpsNS, Main, 
        '<Alt-L>', self.jump_right)

        self.add_kmap(PaneJumpsNS, Main, 
        '<Alt-K>', self.jump_up)

        self.add_kmap(PaneJumpsNS, Main, 
        '<Alt-J>', self.jump_down)

    def jump_left(self, event):
        wids  = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master))
        count = count - 1
        wid   = self.xstr.nametowidget(wids[count])
        wid   = [ind for ind in wid.winfo_children() 
            if isinstance(ind, Xstr)]
        
        # as there is only one.
        wid[0].focus_set()
    
    def jump_right(self, event):
        wids   = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master))
        count = (count + 1) % len(wids)
        wid   = self.xstr.nametowidget(wids[count])
        wid   = [ind for ind in wid.winfo_children() 
        if isinstance(ind, Xstr)]
        
        # as there is only one.
        wid[0].focus_set()
    
    def jump_down(self, event):
        wids   = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        index = wids.index(str(self.xstr.master))
    
        wids  = self.xstr.master.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master.master))
        count = (count + 1) % len(wids)
    
        wid   = self.xstr.nametowidget(wids[count])
        size  = len(wid.panes())
        wid   = self.xstr.nametowidget(wid.panes()[
            index if index < size else (size - 1)])
    
        wid   = [ind for ind in wid.winfo_children() 
        if isinstance(ind, Xstr)]
    
        # as there is only one.
        wid[0].focus_set()
    
    def jump_up(self, event):
        wids   = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        index = wids.index(str(self.xstr.master))
    
        wids  = self.xstr.master.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master.master))
        count = count - 1
    
        wid   = self.xstr.nametowidget(wids[count])
        size  = len(wid.panes())
        wid   = self.xstr.nametowidget(wid.panes()[
        index if index < size else (size - 1)])

        wid = [ind for ind in wid.winfo_children() 
        if isinstance(ind, Xstr)]
    
        # as there is only one.
        wid[0].focus_set()
    
install = PaneJumps

