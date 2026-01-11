from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.plugins.bracket_jumps import BracketJumps
from cspkg.core import Mode, EscsApp
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestBracketJumps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = BracketJumps(cls.xstr)

        root.note.select(0)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
       root.destroy()

    def test0(self):
        self.xstr.insert('end', '381 (123) [321] 932\n')
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-bracketright>')
        self.assertEqual(self.xstr.index('insert'), '1.5')

        self.xstr.event_generate('<Key-bracketright>')
        self.assertEqual(self.xstr.index('insert'), '1.9')

        self.xstr.event_generate('<Key-bracketright>')
        self.assertEqual(self.xstr.index('insert'), '1.11')

        self.xstr.event_generate('<Key-bracketleft>')
        self.assertEqual(self.xstr.index('insert'), '1.10')

        self.xstr.event_generate('<Key-bracketleft>')
        self.assertEqual(self.xstr.index('insert'), '1.8')

        self.xstr.event_generate('<Key-bracketleft>')
        self.assertEqual(self.xstr.index('insert'), '1.4')

        pass

    def test1(self):
        pass

if __name__ == '__main__':
    unittest.main()
