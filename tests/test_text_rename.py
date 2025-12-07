from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.text_rename import TextRename
from cspkg.start import root
from tkinter import TclError
import unittest
import os
from os.path import join, expanduser

class TestTextRename(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('null')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = TextRename(cls.xstr)

        cls.xstr.insert('end', 'TextRename plugin tests.\n' * 10)
        cls.xstr.focus_set()
        cls.xstr.save_data_as(join(expanduser('~'), 'escs-tests'))

        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        self.xstr.event_generate('<Escape>')
        self.assertEqual(self.mod0.mode, Normal)

        self.xstr.after(100, self.test0_helper)
        self.xstr.event_generate('<Alt-N>')

        home = os.path.expanduser('~')
        filename = os.path.join(home, 'escs-testing')

        self.assertEqual(filename, self.xstr.filename)
        self.assertEqual(True, os.path.exists(filename))
    
    def test0_helper(self):
        scan = root.focus_get()

        # self.assertEqual(type(read), )
        scan.insert('end', 'escs-testing')
        scan.event_generate('<Return>')

    def test1(self):
        pass

if __name__ == '__main__':
    unittest.main()
