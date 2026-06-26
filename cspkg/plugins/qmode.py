from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal
from cspkg.start import root

class QModeNS(Namespace):
    pass

class QMode(Plugin):
    pinned_mode = None
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(QModeNS, Main, 
        '<Control-b>', self.pin_mode)

        self.add_kmap(QModeNS, Normal, 
        '<Key-b>', self.unpin_mode)

    def pin_mode(self, event):
        taglist = self.xstr.bindtags()
        self.pinned_mode = taglist[1]
        root.status.set_msg('QMode - Pinned mode.')
        self.chmode(Normal)

    def unpin_mode(self, event):
        taglist = self.xstr.bindtags()

        self.xstr.bindtags((taglist[0], 
        self.pinned_mode, taglist[2]))
        self.xstr.event_generate('<<Chmode>>')
        root.status.set_msg('QMode - Unpinned mode.')

install = QMode

