"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.start import root
from cspkg.xscan import Xscan
import os

from cspkg.core import Namespace, Plugin, Main

class XrenameNS(Namespace):
    pass

class Xrename(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(XrenameNS, Main, 
        '<Alt-N>', self.rename)
    
    def rename(self, event):
        """
        """

        root.status.set_msg('Type a filename:')
    
        xscan = Xscan()
        dir = os.path.dirname(self.xstr.filename)
        dst = os.path.join(dir, xscan.data)
    
        try:
            os.rename(self.xstr.filename, dst)
        except OSError:
            root.status.set_msg('Failed to rename!')
        else:
            self.xstr.filename = dst
            root.status.set_msg('File renamed!')
        return 'break'
    

install = Xrename









