from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.plugins.qsearch import QSearch
import unittest
import time

class TestMode(Mode):
    pass

class TestQSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('None')
        cls.mod = QSearch(cls.xstr)
        cls.mod.chmode(Normal)
        cls.xstr.insert('end', 'QSearch plugin test.\n' * 10)

        cls.xstr.focus_set()
        root.update() 

    def setUP(self):
        pass

    def tearDown(self):
        pass

    def test0(self):
        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Alt-j>')
        root.update() 

        read = root.focus_get()
        read.insert('end', 'pl te')

        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Escape>')

        self.assertEqual(self.xstr.index('insert'), '8.17')
