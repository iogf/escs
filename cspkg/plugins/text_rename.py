"""
Overview
========

"""

# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cspkg.start import root
from cspkg.scan import Scan
import os

from cspkg.core import Namespace, Plugin, Main

class TextRenameNS(Namespace):
    pass

class TextRename(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(TextRenameNS, Main, 
        '<Alt-N>', self.rename)
    
    def rename(self, event):
        """
        """

        root.status.set_msg('Type a filename:')
    
        scan = Scan()
        dir = os.path.dirname(self.xstr.filename)
        dst = os.path.join(dir, scan.data)
    
        try:
            os.rename(self.xstr.filename, dst)
        except OSError:
            root.status.set_msg('Failed to rename!')
        else:
            self.xstr.filename = dst
            root.status.set_msg('File renamed!')
        return 'break'
    

install = TextRename









