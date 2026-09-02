from cspkg.core import Mode, Normal
from cspkg.start import root
from tkinter import TclError
import unittest

class TestMode(Mode):
    pass

class TestNormalMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.xstr.insert('end', 'NormalMode plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

    def test0(self):
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Normal')
        self.xstr.event_generate('<Key-i>')
        root.update() 
        self.xstr.event_generate('<Escape>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Normal')

        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.event_generate('<Escape>')
        root.update() 

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), ())

if __name__ == '__main__':
    unittest.main()
