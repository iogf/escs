from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.core import Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestMode(Mode):
    pass

class TestNormalMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod = NormalMode(cls.xstr)
        cls.xstr.insert('end', 'NormalMode plugin tests.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

    def test0(self):
        self.mod.chmode(TestMode)
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod.mode, Normal)
        self.mod.chmode(TestMode)
        self.assertEqual(self.mod.mode, TestMode)

        pass

    def test1(self):
        self.mod.chmode(TestMode)
        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.event_generate('<Escape>')
        root.update() 

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), ())
        self.assertEqual(self.mod.mode, Normal)
        
        pass

if __name__ == '__main__':
    unittest.main()
