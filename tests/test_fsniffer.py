from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.plugins.fsniffer import FSniffer
import unittest
import time
import os

class TestMode(Mode):
    pass

class TestFSniffer(unittest.TestCase):
    """
    In order to have this test running it demands having
    locate database updated. Run the command below.

        updatedb
    
    """
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Test')
        cls.mod = FSniffer(cls.xstr)
        cls.mod.chmode(Normal)

        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        self.xstr.event_generate('<Alt-t>')
        root.update() 

        picker = root.focus_get()

        self.assertEqual(picker.title(), 'Fsniffer')
        picker.listbox.focus_set() 
        picker.listbox.event_generate('<Escape>')

    def test1(self):
        self.xstr.event_generate('<Alt-y>')
        root.update() 

        read = root.focus_get()
        read.insert('end', 'test fsni')

        read.event_generate('<Return>')
        root.after(1000, self.test1_helper0)
        root.update() 

        # picker = root.focus_get()

        # self.assertEqual(picker.title(), 'Fsniffer')
        # picker.event_generate('<Escape>')

    def test1_helper0(self):
        print('Focus:', root.focus_get())

    