"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.start import root
import os

from cspkg.core import Namespace, Plugin, Main
from cspkg.plugins.extra_mode import Extra

class IONS(Namespace):
    pass

class IO(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(IONS, Main, '<Alt-S>', self.save)
        self.add_kmap(IONS, Main, '<Alt-A>', self.save_as)
        self.add_kmap(IONS, Main, '<Alt-D>', self.ask_and_load)
        self.add_kmap(IONS, Extra, '<Key-n>', self.rename)
    
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
        self.xstr.chmode('NORMAL')
        return 'break'
        
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
    
    
    def save(self, event):
        """
        """
    
        try:
            self.xstr.save_data()
        except Exception:
            root.status.set_msg('It failed to save data.')
        else:
            root.status.set_msg('Data saved.')
        self.xstr.chmode('NORMAL')
        return 'break'
    
    def rename(self, event):
        """
        """

        root.status.set_msg('Type a filename:')
    
        ask = Ask()
        dir = os.path.dirname(self.xstr.filename)
        dst = os.path.join(dir, ask.data)
    
        try:
            os.rename(self.xstr.filename, dst)
        except OSError:
            root.status.set_msg('Failed to rename!')
        else:
            self.xstr.filename = dst
            root.status.set_msg('File renamed')
        self.xstr.chmode('NORMAL')
        return 'break'
    

install = IO
