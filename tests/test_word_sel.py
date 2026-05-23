from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.word_sel import WordSel
from cspkg.start import root
from cspkg.core import rcmod

import unittest
from os.path import join, expanduser

class TestWordSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((NormalMode, (), {}), (WordSel, (), {})))
        pass

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        # cls.xstr.master.master.master.destroy()
        pass

    def test0(self):
        xstr = root.note.create('Tests')
        xstr.insert('end', 'ABeD1EF    E3EsJE    RDE2d.\n' * 10)
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.mark_set('insert', '1.0')
        xstr.event_generate('<Key-w>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 
        self.assertEqual(ranges, ('1.0', '1.7'))

        xstr.tag_remove('sel', '1.0', 'end')

        xstr.mark_set('insert', '1.7')
        xstr.event_generate('<Key-w>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ('1.0', '1.7'))

        # Place the cursor on the blank char then
        # generates <Key-w> i.e it selects the word on the cursor.
        xstr.tag_remove('sel', '1.0', 'end')
        xstr.mark_set('insert', '1.8')
        xstr.event_generate('<Key-w>')

        # The selected ranges should be the same.
        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ())

        xstr.mark_set('insert', '1.11')
        xstr.event_generate('<Key-w>')

        # The selected ranges should be the same.
        ranges = xstr.tag_nextrange('sel', '1.7')
        root.update() 

        self.assertEqual(ranges, ('1.11', '1.17'))

    def test1(self):
        xstr = root.note.create('Tests')
        xstr.insert('end', '[ABCeD] (F23aE) (EBcE}  3123\n')
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.mark_set('insert', '1.0')
        xstr.event_generate('<Key-W>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ('1.0', '1.7'))
        xstr.tag_remove('sel', '1.0', 'end')

        xstr.mark_set('insert', '1.7')
        xstr.event_generate('<Key-W>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ('1.0', '1.7'))
        xstr.tag_remove('sel', '1.0', 'end')

        xstr.mark_set('insert', '1.8')
        xstr.event_generate('<Key-W>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ('1.8', '1.15'))
        xstr.tag_remove('sel', '1.0', 'end')

        xstr.mark_set('insert', '1.23')
        xstr.event_generate('<Key-W>')

        ranges = xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ())

if __name__ == '__main__':
    unittest.main()
