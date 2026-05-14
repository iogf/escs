from cspkg.scan import Read
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
        self.add_kmap(LineIndexNS, Main,'<Alt-w>', 
        lambda event: Read(events={'<Escape>': lambda read: read.done(),
        '<Return>': lambda read: self.set_index(read)}, msg='Line/Col:'))

    def set_index(self, read):
        data = read.text()
        read.done()
        coords = match('([0-9]*) *([0-9]*)', data)
        
        try:
            self.xstr.setcur(coords.group(1), 
                    coords.group(2) if coords.group(2) else '0' )
        except Exception as e:
            root.status.set_msg('Bad index.')
        else:
            root.status.set_msg('Index set.')
    
install = LineIndex


