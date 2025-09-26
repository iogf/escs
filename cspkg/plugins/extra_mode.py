from cspkg.core import Namespace, Mode, Plugin, Main

class ExtraModeNS(Namespace):
    pass

class Extra(Mode):
    pass


class ExtraMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(ExtraModeNS, 
        Main, '<Alt-v>', self.switch_extra, True)

    def switch_extra(self, event):
        """
        """
        self.chmode(Extra)

install = ExtraMode

