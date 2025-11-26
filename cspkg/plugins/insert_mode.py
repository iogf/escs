from cspkg.core import Namespace, Mode, Plugin
from cspkg.plugins.normal_mode import Normal

class InsertModeNS(Namespace):
    pass

class Insert(Mode):
    EDIT = True
    pass

class InsertMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(InsertModeNS, 
        Normal, '<Key-i>', self.switch_insert)

    def switch_insert(self, event):
        """
        """
        self.xstr.tag_remove('sel', '1.0', 'end')
        self.chmode(Insert)

install = InsertMode
