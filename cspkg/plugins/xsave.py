"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.start import root
import os

from cspkg.core import Namespace, Plugin, Main

class XsaveNS(Namespace):
    pass

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







