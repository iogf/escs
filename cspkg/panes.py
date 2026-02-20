from tkinter import PanedWindow, RAISED, BOTH, HORIZONTAL
from tkinter import Frame, Scrollbar, Y, VERTICAL, RAISED
from cspkg.xstr import Xstr
from os.path import basename

class PanedHorizontalWindow(PanedWindow):
    """
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=HORIZONTAL, 
        sashrelief=RAISED, showhandle=True, *args, **kwargs)

    def create(self, filename='null'):
        """
        """
        frame     = Frame(master=self)
        scrollbar = Scrollbar(master=frame)
        xstr      = Xstr(filename, frame , border=3, relief=RAISED, 
                           yscrollcommand=scrollbar.set, undo=True)
        scrollbar.config(command=xstr.yview)
        scrollbar.pack(side='right', fill=Y)

        from cspkg.core import rcmod
        for handle, args, kwargs in rcmod:
            handle(xstr, *args, **kwargs)

        xstr.pack(expand=True, side='left', fill=BOTH)
        self.add(frame)

        from cspkg.core import Main

        xstr.bind_class('MODE:%s:%s:%s' % (xstr, 
        Main.__module__, Main.__name__), '<FocusIn>', 
        lambda event: self.master.focus_save(xstr), add=True)
        self.master.focus_save(xstr)

        root = self.winfo_toplevel()
        hpanes  = self.panes()
        width = root.winfo_width()//(len(hpanes) + 1)
        root.update()
    
        for ind in range(0, len(hpanes) - 1):
            self.sash_place(ind,  (ind + 1) * width,  0)

        vpanes  = self.master.panes()
        height = root.winfo_height()//(len(vpanes) + 1)
        root.update()
    
        for ind in range(0, len(vpanes) - 1):
            self.master.sash_place(ind,  0,  (ind + 1) * height)
        return xstr

    def load(self, filename):
        """
        """

        xstr = self.create()
        xstr.load_data(filename)
        return xstr

class PanedVerticalWindow(PanedWindow):
    """
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=VERTICAL, 
        sashrelief=RAISED, showhandle=True, *args, **kwargs)
        self.fwidget = None

    def focus_save(self, widget):
        self.fwidget = widget

    def create(self, filename='null'):
        """
        """

        base = PanedHorizontalWindow(master=self)
        self.add(base)

        xstr = base.create(filename)
        return xstr

    def open(self, filename):
        base = PanedHorizontalWindow(master=self)
        self.add(base)
        xstr = base.load(filename)
        return xstr

    def load(self, *args):
        """
        """

        base = PanedHorizontalWindow(master=self)
        self.add(base)

        for ind in args:
            base.load(ind)
        return base


