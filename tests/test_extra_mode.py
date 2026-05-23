from cspkg.plugins.extra_mode import Extra, ExtraModeNS, ExtraMode
from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.core import rcmod
from cspkg.core import Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestExtraMode(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        xstr = root.note.create('Tests')
        mod0 = ExtraMode(xstr)
        mod1 = NormalMode(xstr)
        
        xstr.insert('end', 'ExtraMode plugin test.\n')
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Alt-v>')
        root.update() 
        self.assertEqual(mod0.mode, Extra)

        xstr.tag_add('sel', '1.0', 'end')
        xstr.event_generate('<Escape>')
        root.update() 

        self.assertEqual(xstr.tag_nextrange('sel', '1.0'), ())
        self.assertEqual(mod1.mode, Normal)
        
        pass

if __name__ == '__main__':
    unittest.main()
