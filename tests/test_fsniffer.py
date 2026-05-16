from cspkg.plugins.normal_mode import Normal
from subprocess import Popen, PIPE
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
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        xstr = root.note.create('Test0')
        mod = FSniffer(xstr)
        mod.chmode(Normal)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Alt-t>')
        root.update() 

        picker = root.focus_get()
        self.assertEqual(picker.master.title(), 'Fsniffer')
        picker.event_generate('<Escape>')
        root.update()

    def test1(self):
        xstr = root.note.create('Test1')
        mod = FSniffer(xstr)
        mod.chmode(Normal)
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Alt-y>')
        root.update() 

        read = root.focus_get()
        # Locate cpskg files i.e escs pkg.
        read.insert('end', 'cspkg')
        root.update() 

        read.event_generate('<Return>')
        root.update() 

        picker = root.focus_get()
        data0 = picker.get(0, 'end')
        picker.event_generate('<Return>')
        root.update() 

        # Make sure focus is back to the xstr instance.
        self.assertTrue(xstr, root.focus_get())
    
        # Attempt to locate cspkg files to compare with previous
        # results.
        process = Popen('locate cspkg', stdout=PIPE, 
        stderr=PIPE, text=True, shell=True)

        output, err = process.communicate()
        data1 = output.split('\n')

        # The results of fsniffer should be equal in length
        # to the results of locate command.
        self.assertTrue(len(data0), len(data1))
