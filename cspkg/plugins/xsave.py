"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.core import Namespace, Plugin, Main
from cspkg.core import Command
from cspkg.start import root
import os

class XsaveNS(Namespace):
    pass

@Command('s')
def save(xstr):
    """
    Save the contents of the targeted areavi to disk.
    """
    xstr.save_data()
    root.status.set_msg('File saved!')

@Command('ss')
def save_as(xstr, filename):
    """
    """

    xstr.save_data_as(filename)
    root.status.set_msg('File saved as %s!' % filename)

class Xsave(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(XsaveNS, Main, '<Alt-S>', self.save)
        self.add_kmap(XsaveNS, Main, '<Alt-A>', self.save_as)
    
    def save_as(self, event):
        """
        """
    
        filename = asksaveasfilename()
    
        if not filename: 
            return 'break'

        try:
            self.xstr.save_data_as(filename)
        except Exception:
            root.status.set_msg('It failed to save data.')
        else:
            root.status.set_msg('Data saved.')
        return 'break'
        
    def save(self, event):
        """
        """
    
        try:
            self.xstr.save_data()
        except Exception:
            root.status.set_msg('It failed to save data.')
        else:
            root.status.set_msg('Data saved.')
        return 'break'
    
install = Xsave







