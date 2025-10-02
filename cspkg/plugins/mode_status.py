from cspkg.start import root
from os.path import basename
from cspkg.core import Namespace, Plugin, Main

class ModeStatusNS(Namespace):
    pass

class ModeStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(ModeStatusNS, Main, '<<Chmode>>', self.update_mode, True)
        self.add_kmap(ModeStatusNS, Main, '<FocusIn>', self.update_mode, True)

    def update_mode(self, event):
        mode = self.xstr.bindtags()
        mode = mode[1].rsplit(':')
        mode = mode[-1].rsplit('.')
        root.status.set_mode(mode[-1])

install = ModeStatus
