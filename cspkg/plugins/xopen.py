"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.start import root
import os

from cspkg.core import Namespace, Plugin, Main, Command

class XopenNS(Namespace):
    pass

@Command('ox')
def load_path(xstr, filename):
    """
    """

    xstr.load_data(filename)
    root.status.set_msg('Loaded %s' % filename)

class Xopen(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(XopenNS, Main, 
        '<Alt-D>', self.ask_and_load)
    
    def ask_and_load(self, event):
        """
        """
    
        filename = askopenfilename()
    
        if not filename: 
            return 'break'
    
        try:
            self.xstr.load_data(filename)
        except Exception:
            root.status.set_msg('It failed to load.')
        else:
            root.status.set_msg('File loaded.')
        return 'break'
    
install = Xopen










