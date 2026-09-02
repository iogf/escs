from cspkg.core import Extra, Normal, rcmod
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestExtraMode(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        xstr = root.note.create('Tests')
        
        xstr.insert('end', 'ExtraMode plugin test.\n')
        root.note.select(xstr.master.master.master)
        root.update() 
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Alt-v>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Extra')

        xstr.tag_add('sel', '1.0', 'end')
        xstr.event_generate('<Escape>')
        root.update() 

        self.assertEqual(xstr.tag_nextrange('sel', '1.0'), ())
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Normal')
        
        pass

if __name__ == '__main__':
    unittest.main()
