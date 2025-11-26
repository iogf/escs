from cspkg.plugins.insert_mode import Insert, InsertModeNS, InsertMode
from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.core import Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestInsertMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = InsertMode(cls.xstr)
        cls.mod1 = NormalMode(cls.xstr)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        self.mod0.chmode(Normal)
        self.assertEqual(self.mod0.mode, Normal)
        self.xstr.event_generate('<Key-i>')
        self.assertEqual(self.mod0.mode, Insert)

        pass

    def test1(self):
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod1.mode, Normal)

        self.xstr.event_generate('<Key-i>')
        self.assertEqual(self.mod0.mode, Insert)

        self.xstr.event_generate('<Key-a>')
        self.xstr.event_generate('<Key-b>')
        self.xstr.event_generate('<Key-c>')
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod1.mode, Normal)
        self.assertEqual(self.xstr.get('1.0', 'end'), 'abc\n')

    def test2(self):
        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.event_generate('<Key-i>')

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), ())
        self.assertEqual(self.mod0.mode, Insert)
        
        pass

if __name__ == '__main__':
    unittest.main()
