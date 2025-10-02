from cspkg.start import root
from os.path import basename
from cspkg.core import Namespace, Plugin, Main

class TopbarStatusNS(Namespace):
    pass

class TopbarStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(TopbarStatus, Main, 
        '<FocusIn>', self.update_title, True)

        self.add_kmap(TopbarStatus, Main, 
        '<<LoadData>>', self.update_title, True)

        self.add_kmap(TopbarStatus, Main, 
        '<<SaveData>>', self.update_title, True)

    def update_title(self, event):
        root.title('Escs %s' % self.xstr.filename)

install = TopbarStatus
