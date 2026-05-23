from cspkg.core import Main, Mode
from cspkg.plugins.word_jumps import WordJumps
from cspkg.plugins.normal_mode import Normal
from cspkg.start import root
import unittest
import time

class TestMode(Mode):
    pass

class TestWordJumps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')

        cls.mod = WordJumps(cls.xstr)
        cls.mod.chmode(Normal)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        cls.xstr.insert('end', 'WordJumps plugin test.\n' * 10)
        root.update() 
        pass

    @classmethod
    def tearDownClass(cls):
        cls.xstr.update()
        root.note.forget(0)

    def test0(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Alt-l>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.9')

        self.xstr.event_generate('<Alt-l>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.16')

    def test1(self):
        self.xstr.mark_set('insert', '1.0 lineend')

        self.xstr.event_generate('<Alt-h>')
        self.xstr.event_generate('<Alt-h>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.16')

        self.xstr.event_generate('<Alt-h>')
        root.update() 
        self.assertEqual(self.xstr.index('insert'), '1.9')
