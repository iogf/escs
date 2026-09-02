from cspkg.core import Insert, Normal, Mode
from cspkg.start import root
from tkinter import TclError
import unittest

class TestInsertMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        pass

    def test0(self):
        self.xstr.event_generate('<Key-i>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Insert')
        self.xstr.event_generate('<Escape>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Normal')

        self.xstr.event_generate('<Key-i>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Insert')

        self.xstr.event_generate('<Key-a>')
        root.update() 

        self.xstr.event_generate('<Key-b>')
        root.update() 

        self.xstr.event_generate('<Key-c>')
        root.update() 

        self.xstr.event_generate('<Escape>')
        root.update() 
        self.assertEqual(root.status.mode.cget('text'), 'Mode: Normal')
        self.assertEqual(self.xstr.get('1.0', 'end'), 'abc\n')

        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.event_generate('<Key-i>')
        root.update() 

        self.assertEqual(self.xstr.tag_nextrange('sel', '1.0'), ())
        
        pass

if __name__ == '__main__':
    unittest.main()
