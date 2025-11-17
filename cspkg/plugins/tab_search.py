from cspkg.core import Plugin, Namespace, Main
from cspkg.scan import Read
from cspkg.start import root

class TabSearchNS(Namespace):
    pass

class TabSearch(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(TabSearchNS, Main, 
        '<Alt-i>', self.on_next_mode)

        self.add_kmap(TabSearchNS, Main, 
        '<Alt-u>', self.on_back_mode)

    def on_next_mode(self, event):
        read = Read(events={'<<Data>>': self.switch_next, 
        '<Alt-p>': self.switch_next, 
        '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop})

    def on_back_mode(self, event):
        read = Read(events={
        '<<Data>>': self.switch_back, 
        '<Alt-p>': self.switch_next, 
        '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop})

    def switch_next(self, wid):
        """
        """
        data = wid.get()
        seq  = root.note.next(lambda text: data in text)
        elem = next(seq)

        # The wid is an Entry/Read instance.
        # wid=root.note.focus_get()
        root.note.select(elem)

        # Looks like in some Tk versions it loses
        # focus in the Entry widget after a tab is selected.
        # wid.focus_set()
        # root.after(30, lambda : wid.focus_set())

        wid  = root.note.nametowidget(root.note.select())
        # The wid is a PanedVerticalWindow
        root.title('Escs %s' % wid.active_xstr.filename)

    def switch_back(self, wid):
        """
        """

        data = wid.get()
        seq  = root.note.back(lambda text: data in text)
        elem = next(seq)

        # wid=root.note.focus_get()
        root.note.select(elem)

        # wid.focus_set()
        # root.after(30, lambda : wid.focus_set())

        wid  = root.note.nametowidget(root.note.select())
        root.title('Escs %s' % wid.active_xstr.filename)

    def stop(self, wid):
        wid  = root.note.nametowidget(root.note.select())
        wid.active_xstr.focus_set()
        return True

install = TabSearch




