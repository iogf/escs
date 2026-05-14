from cspkg.core import Plugin, Namespace, Main
from cspkg.scan import Read
from cspkg.start import root

class TabSearchNS(Namespace):
    pass

class TabSearch(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(TabSearchNS, Main, '<Alt-i>', 
        lambda event: Read(events={'<<Data>>': self.switch_next, 
        '<Alt-p>': self.switch_next, '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop}, msg='Type a Tab/Name:'))

        self.add_kmap(TabSearchNS, Main, '<Alt-u>', 
        lambda event: Read(events={'<<Data>>': self.switch_back, 
        '<Alt-p>': self.switch_next, '<Alt-o>': self.switch_back, 
        '<Escape>': self.stop}, msg='Type a Tab/Name:'))

    def switch_next(self, read):
        """
        """
        data = read.text()
        seq  = root.note.next(lambda text: data in text)
        elem = next(seq)
        root.note.select(elem)

        wid  = root.note.nametowidget(root.note.select())
        # The wid is a PanedVerticalWindow
        root.title('Escs %s' % wid.fwidget.filename)

    def switch_back(self, read):
        """
        """

        data = read.text()
        seq  = root.note.back(lambda text: data in text)
        elem = next(seq)
        root.note.select(elem)

        wid  = root.note.nametowidget(root.note.select())
        root.title('Escs %s' % wid.fwidget.filename)

    def stop(self, read):
        read.done()

install = TabSearch




