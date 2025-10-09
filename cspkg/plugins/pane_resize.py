from cspkg.core import Namespace, Plugin, Main

class PaneResizeNS(Namespace):
    pass

class PaneResize(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)        
        self.add_kmap(PaneResizeNS, Main, '<Control-h>', self.dec_vsash)
        self.add_kmap(PaneResizeNS, Main, '<Control-l>', self.inc_vsash)
        self.add_kmap(PaneResizeNS, Main, '<Control-k>', self.dec_hsash)
        self.add_kmap(PaneResizeNS, Main, '<Control-j>', self.inc_hsash)


    def dec_vsash(self, event):
        wids  = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master))
        count = count - 1 if count > 0 else 0

        pos = self.xstr.master.master.sash_coord(count)
        self.xstr.master.master.sash_place(count, pos[0] - 15, 0)

    def inc_vsash(self, event):
        wids  = self.xstr.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master))
        count = count - 1 if count > 0 else 0

        pos = self.xstr.master.master.sash_coord(count)
        self.xstr.master.master.sash_place(count, pos[0] + 15, 0)

    def dec_hsash(self, event):
        wids  = self.xstr.master.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master.master))
        count = count - 1 if count > 0 else 0
        pos = self.xstr.master.master.master.sash_coord(count)
        self.xstr.master.master.master.sash_place(count, 0, pos[1] - 15)

    def inc_hsash(self, event):
        wids  = self.xstr.master.master.master.panes()
        wids  = [str(item) for item in wids]
        count = wids.index(str(self.xstr.master.master))
        count = count - 1 if count > 0 else 0

        pos = self.xstr.master.master.master.sash_coord(count)
        self.xstr.master.master.master.sash_place(count, 0, pos[1] + 15)


install = PaneResize