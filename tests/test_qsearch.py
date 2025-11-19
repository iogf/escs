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

    @classmethod
    def tearDownClass(cls):
        root.destroy()

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

    def test1(self):
        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Alt-k>')
        root.update() 

        read = root.focus_get()
        read.insert('end', 'Se p t')

        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Escape>')

        self.assertEqual(self.xstr.index('insert'), '1.1')

    def test2(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Alt-j>')
        root.update() 

        read = root.focus_get()
        read.insert('end', 'S')
        read.event_generate('<<Data>>')
        self.assertEqual(self.xstr.index('insert'), '1.2')

        read.insert('end', ' h')
        read.event_generate('<<Data>>')
        self.assertEqual(self.xstr.index('insert'), '1.7')

        read.insert('end', ' .')
        read.event_generate('<<Data>>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

        read.event_generate('<Escape>')

    def test3(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Alt-j>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-h>')
        self.assertEqual(self.xstr.index('insert'), '1.7')
        read.event_generate('<Key-space>')

        read.event_generate('<Key-period>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

        read.event_generate('<Escape>')

    def test4(self):
        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Alt-k>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-S>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')

        self.assertEqual(self.xstr.index('insert'), '2.1')
        read.event_generate('<Key-space>')
        read.event_generate('<Key-h>')

        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')

        self.assertEqual(self.xstr.index('insert'), '10.7')

        read.event_generate('<Escape>')

    def test5(self):
        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Alt-k>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-S>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')

        self.assertEqual(self.xstr.index('insert'), '2.1')
        read.event_generate('<Key-space>')
        read.event_generate('<Key-h>')

        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')

        self.assertEqual(self.xstr.index('insert'), '10.7')

        read.event_generate('<Escape>')

    def test6(self):
        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Alt-k>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-S>')
        read.event_generate('<Key-space>')
        read.event_generate('<Key-period>')

        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')
        read.event_generate('<Alt-p>')

        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')
        read.event_generate('<Alt-o>')

        # It looks that xstr.isearch regex is consuming as much as
        # chars for .+ thus it is not 3.20 but 3.1. It is matching
        # S.+\. instead of s.+?\. that is at the end of each line.
        self.assertEqual(self.xstr.index('insert'), '3.1')

        read.event_generate('<Escape>')

