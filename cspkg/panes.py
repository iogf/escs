from tkinter import PanedWindow, RAISED, BOTH, HORIZONTAL
from tkinter import Frame, Scrollbar, Y, VERTICAL
from cspkg.xstr import Xstr

class PanedHorizontalWindow(PanedWindow):
    """
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=HORIZONTAL, *args, **kwargs)

    def create(self, filename='none'):
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

        xstr.focus_set()
        xstr.pack(expand=True, side='left', fill=BOTH)
        self.add(frame)

        def save_focus(event):
            self.master.focused_xstr = xstr

        self.master.focused_xstr = xstr
        xstr.bind('<FocusIn>', save_focus)
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
        self.focused_xstr = None

    def create(self, filename='none'):
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


