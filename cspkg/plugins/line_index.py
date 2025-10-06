from cspkg.xscan import Xscan
from tkinter import TclError
from cspkg.start import root
from cspkg.core import Namespace, Main, Plugin
from regex import match

class LineIndexNS(Namespace):
    pass

class LineIndex(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr
        self.add_kmap(LineIndexNS, Main,'<Alt-w>', self.set_index)

    def set_index(self, xstr):
        root.status.set_msg('Line index:')
        xscan = Xscan()
        coords = match('([0-9]*) *([0-9]*)', xscan.data)

        try:
            self.xstr.setcur(coords.group(1), 
                    coords.group(2) if coords.group(2) else '0' )
        except Exception as e:
            root.status.set_msg('Bad index.')
        else:
            root.status.set_msg('Index set.')
    
install = LineIndex


