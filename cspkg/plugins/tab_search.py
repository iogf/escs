from cspkg.core import Plugin, Namespace, Main
from cspkg.xscan import Get
from cspkg.start import root

class TabSearchNS(Namespace):
    pass

class TabSearch(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(TabSearchNS, Main, 
        '<Alt-i>', self.on_next_mode, True)

        self.add_kmap(TabSearchNS, Main, 
        '<Alt-u>', self.on_back_mode, True)

    def on_next_mode(self, event):
        get = Get(events={'<<Data>>': self.switch_next, 
        '<Alt-p>': self.switch_next, 
        '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop, 
        '<Return>': self.stop})

    def on_back_mode(self, event):
        get = Get(events={
        '<<Data>>': self.switch_back, 
        '<Alt-p>': self.switch_next, 
        '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop, 
        '<Return>': self.stop})

    def switch_next(self, wid):
        """
        """
        data = wid.get()
        seq  = root.note.next(lambda text: data in text)
        elem = next(seq)
        root.note.on(elem)

        wid  = root.note.nametowidget(root.note.select())
        root.title('Vy %s' % wid.focused_xstr.filename)

    def switch_back(self, wid):
        """
        """

        data = wid.get()
        seq  = root.note.back(lambda text: data in text)
        elem = next(seq)
        root.note.on(elem)

        wid  = root.note.nametowidget(root.note.select())
        root.title('Vy %s' % wid.focused_xstr.filename)

    def stop(self, wid):
        wid  = root.note.nametowidget(root.note.select())
        wid.focused_xstr.focus_set()

        return True

install = TabSearch




