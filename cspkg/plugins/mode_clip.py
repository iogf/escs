from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal
from cspkg.start import root

class ModeClipNS(Namespace):
    pass

class ModeClip(Plugin):
    mode_ref = None
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(ModeClipNS, Main, 
        '<Control-b>', self.pin_mode)

        self.add_kmap(ModeClipNS, Normal, 
        '<Key-b>', self.unpin_mode)

    def pin_mode(self, event):
        taglist = self.xstr.bindtags()
        self.mode_ref = taglist[1]
        root.status.set_msg('ModeClip - Pinned mode.')
        self.chmode(Normal)

    def unpin_mode(self, event):
        taglist = self.xstr.bindtags()

        self.xstr.bindtags((taglist[0], 
        self.mode_ref if self.mode_ref else taglist[1], taglist[2]))
        self.xstr.event_generate('<<Chmode>>')
        root.status.set_msg('ModeClip - Unpinned mode.')

install = ModeClip