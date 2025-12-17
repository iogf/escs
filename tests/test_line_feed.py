from cspkg.plugins.line_feed import LineFeed
from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.insert_mode import Insert, InsertMode
from cspkg.core import Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestPythonMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = LineFeed(cls.xstr)
        cls.mod1 = NormalMode(cls.xstr)
        cls.mod2 = InsertMode(cls.xstr)

        cls.xstr.insert('end', 'LineFeed plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        pass

    def test0(self):
        self.xstr.mark_set('insert', '2.0')
        self.xstr.event_generate('<Key-m>')
        self.assertEqual(self.mod0.mode, Insert)
        self.assertEqual(self.xstr.get('3.0', 'insert lineend'), '')
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod1.mode, Normal)

    def test1(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-n>')
        self.assertEqual(self.mod0.mode, Insert)
        self.assertEqual(self.xstr.get('1.0', 'insert lineend'), '')
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod1.mode, Normal)

if __name__ == '__main__':
    unittest.main()
