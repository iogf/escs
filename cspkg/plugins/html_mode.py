from cspkg.core import Namespace, Main, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class HtmlModeNS(Namespace):
    pass

class Html(Mode):
    pass

class HtmlMode(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(HtmlModeNS, Normal, 
        '<Key-at>', self.Html_mode)

    def Html_mode(self, event):
        self.chmode(Html)

install = HtmlMode

