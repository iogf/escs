from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.plugins.xleaps import Xleaps, Drop, Jump
from cspkg.core import Mode, EscsApp
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestXleaps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')

        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = Xleaps(cls.xstr)

        root.note.select(0)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
       root.destroy()

    def test0(self):
        self.xstr.insert('end', '381 123 321 932\n')
        self.xstr.mark_set('insert', '1.0')

        # Create an anchor at 1.0 whose label is a.
        self.xstr.event_generate('<Alt-bracketleft>')
        self.assertEqual(self.mod1.mode, Drop)

        self.xstr.event_generate('<Key-a>')
        self.xstr.mark_set('insert', '1.10')
        self.assertEqual(self.mod0.mode, Normal)
    
        # Check whether anchor a is at 1.0.
        self.xstr.event_generate('<Alt-bracketright>')
        self.assertEqual(self.mod1.mode, Jump)

        self.xstr.event_generate('<Key-a>')
        self.assertEqual(self.xstr.index('insert'), '1.0')
        self.assertEqual(self.mod0.mode, Normal)

        self.xstr.insert('end', '311 143 331 231\n')
        self.xstr.mark_set('insert', '2.11')

        # Create an anchor whose label is b.
        self.xstr.event_generate('<Alt-bracketleft>')
        self.assertEqual(self.mod1.mode, Drop)

        self.xstr.event_generate('<Key-b>')
        self.xstr.mark_set('insert', 'end')
        self.assertEqual(self.mod0.mode, Normal)

        # check the anchor b index.
        self.xstr.event_generate('<Alt-bracketright>')
        self.assertEqual(self.mod1.mode, Jump)

        self.xstr.event_generate('<Key-b>')
        self.assertEqual(self.xstr.index('insert'), '2.11')
        self.assertEqual(self.mod0.mode, Normal)

        # Check anchor a index again.
        self.xstr.event_generate('<Alt-bracketright>')
        self.assertEqual(self.mod1.mode, Jump)
        self.xstr.event_generate('<Key-a>')
        self.assertEqual(self.xstr.index('insert'), '1.0')
        self.assertEqual(self.mod0.mode, Normal)

        pass

if __name__ == '__main__':
    unittest.main()
