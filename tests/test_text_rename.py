from cspkg.core import Normal
from cspkg.plugins.text_rename import TextRename
from cspkg.start import root
from tkinter import TclError
import unittest
import os
from os.path import join, expanduser

class TestTextRename(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = TextRename(cls.xstr)

        cls.xstr.insert('end', 'TextRename plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        cls.xstr.save_data_as(join(expanduser('~'), 'escs-tests'))

        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass

    def test0(self):
        self.xstr.event_generate('<Escape>')
        root.update()


        self.xstr.event_generate('<Alt-N>')
        root.update()

        scan = root.focus_get()
        scan.insert('end', 'escs-testing')
        scan.event_generate('<Return>')

        home = os.path.expanduser('~')
        filename = os.path.join(home, 'escs-testing')
        root.update()

        self.assertEqual(filename, self.xstr.filename)
        self.assertEqual(True, os.path.exists(filename))
        os.remove(filename)

    def test1(self):
        self.xstr.event_generate('<Escape>')
        root.update()

        self.xstr.event_generate('<Alt-N>')
        root.update()

        scan = root.focus_get()
        scan.event_generate('<Escape>')
        home = os.path.expanduser('~')

        filename = os.path.join(home, 'escs-testing')
        root.update()
        self.assertEqual(filename, self.xstr.filename)


if __name__ == '__main__':
    unittest.main()
