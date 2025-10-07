from cspkg.core import Namespace, Mode, Main, Plugin

class NormalModeNS(Namespace):
    pass

class Normal(Mode):
    pass

class NormalMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.chmode(Normal)

        self.add_kmap(NormalModeNS, 
        Main, '<Escape>', self.switch_normal, True)

    def switch_normal(self, event):
        """
        """
        self.chmode(Normal)
        self.xstr.clear_selection()

install = NormalMode