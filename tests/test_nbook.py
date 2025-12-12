from cspkg.start import root
from cspkg.core import TabStatus
from os.path import join, expanduser, basename
import os
import unittest
import time

class TestEscsBook(unittest.TestCase):
    def test0(self):
        self.xstr0 = root.note.create('test0')
        root.note.select(self.xstr0.master.master.master)

        tab_name = root.nametowidget(self.xstr0.master.master.master)
        self.assertEqual(root.note.tab(tab_name, 'text'), 'test0')

    def test1(self):
        self.xstr2 = root.note.create('test1')
        root.note.select(self.xstr2.master.master.master)
        self.xstr2.focus_set()

        home = os.path.expanduser('~')
        filename = os.path.join(home, 'escs-tests')
        self.xstr2.insert('end', 'Escs tests\n')
        self.xstr2.save_data_as(filename)

        self.xstr3 = root.note.open(filename)
        root.note.select(self.xstr3.master.master.master)

        tab_name = root.nametowidget(self.xstr3.master.master.master)
        self.assertEqual(root.note.tab(tab_name, 'text'), 'escs-tests')

if __name__ == '__main__':
    unittest.main()



