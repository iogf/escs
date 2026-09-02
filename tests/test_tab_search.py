from cspkg.core import Main, Mode, Normal, Insert
from cspkg.start import root
from cspkg.plugins.tab_search import TabSearch
import unittest
import time

class TestTabSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr0 = root.note.create('TestA 0')
        cls.xstr1 = root.note.create('TestB 1')
        cls.xstr2 = root.note.create('TestC 2')
        cls.xstr3 = root.note.create('TestD 3')

        cls.mod0 = TabSearch(cls.xstr0)
        cls.mod1 = TabSearch(cls.xstr1)
        cls.mod2 = TabSearch(cls.xstr2)
        cls.mod3 = TabSearch(cls.xstr3)

        root.note.select(cls.xstr0.master.master.master)
        cls.xstr0.focus_set()

        root.update() 

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        self.xstr0.event_generate('<Alt-i>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-A>')
        read.event_generate('<Escape>')
        root.update() 

        tab0 = root.note.select()
        tab0_name = root.note.tab(tab0, 'text')
        root.update() 

        self.assertEqual(tab0_name, 'TestA 0')
        self.assertEqual(root.focus_get(), self.xstr0)

        self.xstr0.event_generate('<Alt-i>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-C>')
        read.event_generate('<Escape>')
        root.update() 

        tab1 = root.note.select()
        tab1_name = root.note.tab(tab1, 'text')
        root.update() 

        self.assertEqual(tab1_name, 'TestC 2')
        self.assertEqual(root.focus_get(), self.xstr2)

        self.xstr2.event_generate('<Alt-u>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-A>')
        read.event_generate('<Escape>')
        root.update() 

        tab2 = root.note.select()
        tab2_name = root.note.tab(tab2, 'text')
        self.assertEqual(tab2_name, 'TestA 0')

        self.assertEqual(root.focus_get(), self.xstr0)

        # The focus is on self.xstr0 at this point.
        self.xstr0.event_generate('<Alt-i>')
        root.update() 

        read = root.focus_get()
        read.event_generate('<Key-3>')
        read.event_generate('<Escape>')
        root.update() 

        tab3 = root.note.select()
        tab3_name = root.note.tab(tab3, 'text')

        self.assertEqual(tab3_name, 'TestD 3')

        pass

