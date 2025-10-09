from cspkg.start import root
from cspkg.core import Namespace, Main, Plugin

class CursorStatusNS(Namespace):
    pass

class CursorStatus(Plugin):
    def __init__(self, xstr, timeout=1000):
        super().__init__(xstr)

        self.timeout = timeout
        self.funcid  = None
        self.add_kmap(CursorStatusNS, Main, '<FocusIn>', 
        lambda event: self.update())

        self.add_kmap(CursorStatusNS, Main, '<FocusOut>', 
        lambda event: self.xstr.after_cancel(self.funcid))

    def update(self):
        """
        It is used to update the line and col statusbar 
        in TIME interval.
        """
    
        row, col = self.xstr.indexsplit('insert')
        root.status.set_line(row)
        root.status.set_column(col)
        self.funcid = self.xstr.after(self.timeout, self.update)

install = CursorStatus
