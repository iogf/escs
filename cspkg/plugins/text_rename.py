"""
Overview
========

"""

# from tkinter.messagebox import *
from cspkg.start import root
from cspkg.scan import Read
import os

from cspkg.core import Namespace, Plugin, Main

class TextRenameNS(Namespace):
    pass

class TextRename(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.xstr = xstr

        self.add_kmap(TextRenameNS, Main, '<Alt-N>', 
        lambda event: Read(events={'<Escape>': lambda read: read.done(), 
        '<Return>': lambda read: self.rename(read)}, 
        msg='Rename File:'))
    
    def rename(self, read):
        """
        """

        data = read.text()
        read.done()

        dir = os.path.dirname(self.xstr.filename)
        dst = os.path.join(dir, data)
    
        try:
            os.rename(self.xstr.filename, dst)
        except OSError:
            root.status.set_msg('Failed to rename!')
        else:
            self.xstr.filename = dst
            root.status.set_msg('File renamed!')

install = TextRename









