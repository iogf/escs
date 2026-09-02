from cspkg.core import Normal

from cspkg.plugins.brackets_sel import BracketsSel
from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestBracketsSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.append((BracketsSel, (), {}))

    @classmethod
    def tearDownClass(cls):
        root.destroy()
        pass

    def test0(self):
        """
        Test tab size/tab type spacing.
        """
        xstr = root.note.create('Tests')
        xstr.insert('end', '({[ABEAD]}) [{{C23FE}) [([H41\n\n1E3)]\n')
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.mark_set('insert', '1.0')
        xstr.event_generate('<Key-a>')
        ranges0 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges0, ('1.1', '1.10'))
        xstr.event_generate('<Escape>')


        xstr.mark_set('insert', '1.0')
        xstr.event_generate('<Key-A>')
        ranges1 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges1, ('1.0', '1.11'))
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.12')
        xstr.event_generate('<Key-a>')
        ranges2 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges2, ())
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.13')
        xstr.event_generate('<Key-A>')
        ranges3 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges3, ())
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.14')
        xstr.event_generate('<Key-a>')
        ranges4 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges4, ('1.15', '1.20'))
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.20')
        xstr.event_generate('<Key-a>')
        ranges5 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges5, ('1.15', '1.20'))
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.25')
        xstr.event_generate('<Key-A>')
        ranges6 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges6, ('1.25', '3.5'))
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '1.25')
        xstr.event_generate('<Key-a>')
        ranges7 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges7, ('1.26', '3.4'))
        xstr.event_generate('<Escape>')

        xstr.mark_set('insert', '3.4')
        xstr.event_generate('<Key-a>')
        ranges8 = xstr.tag_nextrange('sel', '1.0', 'end')
        root.update() 

        self.assertEqual(ranges8, ('1.26', '3.4'))
        xstr.event_generate('<Escape>')

if __name__ == '__main__':
    unittest.main()
