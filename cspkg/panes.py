from tkinter import PanedWindow, RAISED, BOTH, HORIZONTAL
from tkinter import Frame, Scrollbar, Y, VERTICAL
from cspkg.xstr import Xstr
from os.path import basename

class PanedHorizontalWindow(PanedWindow):
    """
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=HORIZONTAL, *args, **kwargs)

    def create(self, filename='null'):
        """
        """
        frame     = Frame(master=self)
        scrollbar = Scrollbar(master=frame)
        xstr      = Xstr(filename, frame , border=3, relief=RAISED, 
                           yscrollcommand=scrollbar.set)
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
        PanedWindow.__init__(self, orient=VERTICAL, *args, **kwargs)
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


