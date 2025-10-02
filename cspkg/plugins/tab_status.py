from cspkg.start import root
from os.path import basename
from cspkg.core import Namespace, Plugin, Main

class TabStatusNS(Namespace):
    pass

class TabStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(TabStatusNS, Main, 
        '<FocusIn>', self.update_tabname, True)

        self.add_kmap(TabStatusNS, Main, 
        '<<SaveData>>', self.update_tabname, True)

        self.add_kmap(TabStatusNS, Main, 
        '<<LoadData>>', self.update_tabname, True)

    def update_tabname(self, event):
        root.note.tab(self.xstr.master.master.master,
        text=basename(self.xstr.filename))

install = TabStatus

