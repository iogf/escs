from cspkg.plugins.golang_mode import Golang, GolangModeNS, GolangMode
from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.core import Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestGolangMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = GolangMode(cls.xstr)
        cls.mod1 = NormalMode(cls.xstr)
        cls.xstr.insert('end', 'GolangMode plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        pass

    def test0(self):
        self.mod1.chmode(Normal)
        self.xstr.event_generate('<Key-numbersign>')
        self.assertEqual(self.mod0.mode, Golang)
        self.mod1.chmode(Normal)
        self.assertEqual(self.mod1.mode, Normal)

        pass

    def test1(self):
        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.event_generate('<Key-numbersign>')

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), 
        ('1.0', self.xstr.index('end')))

        self.assertEqual(self.mod0.mode, Golang)
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod1.mode, Normal)

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), ())
        
        pass

if __name__ == '__main__':
    unittest.main()
