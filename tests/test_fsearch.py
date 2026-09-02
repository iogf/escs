from cspkg.core import Normal
from subprocess import Popen, PIPE
from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.plugins.fsearch import FSearch
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
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        xstr = root.note.create('Test0')
        mod = FSearch(xstr)
        mod.chmode(Normal)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Key-C>')
        root.update() 

        read = root.focus_get()
        read.insert('end', 'tests test_fsearch.py')
        read.event_generate('<Return>')
        root.update() 

        data0 = xstr.get('1.0', 'end')
        self.assertIn('tests/test_fsearch.py', data0)
