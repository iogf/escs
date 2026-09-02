from cspkg.plugins.line_feed import LineFeed
from cspkg.core import Mode, Normal, Insert
from cspkg.start import root
from tkinter import TclError
import unittest

class TestLineFeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = LineFeed(cls.xstr)

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
        root.update() 
        self.assertEqual(self.xstr.get('3.0', 'insert lineend'), '')
        self.xstr.event_generate('<Escape>')
        root.update() 

    def test1(self):
        self.xstr.mark_set('insert', '1.0')
        root.update() 
        self.xstr.event_generate('<Key-n>')

        root.update() 
        self.assertEqual(self.xstr.get('1.0', 'insert lineend'), '')
        self.xstr.event_generate('<Escape>')
        root.update() 

if __name__ == '__main__':
    unittest.main()
