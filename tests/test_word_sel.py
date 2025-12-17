from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.word_sel import WordSel
from cspkg.start import root
import unittest
from os.path import join, expanduser

class TestWordSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = WordSel(cls.xstr)

        cls.xstr.insert('end', 'WordSel    plugin    test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)

        cls.xstr.focus_set()

        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        # cls.xstr.master.master.master.destroy()
        pass

    def test0(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-w>')

        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('1.0', '1.7'))

        self.xstr.tag_remove('sel', '1.0', 'end')

        self.xstr.mark_set('insert', '1.7')
        self.xstr.event_generate('<Key-w>')

        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('1.0', '1.7'))

    def test1(self):
        # Place the cursor on the blank char then
        # generates <Key-w> i.e it selects the word on the cursor.
        self.xstr.tag_remove('sel', '1.0', 'end')
        self.xstr.mark_set('insert', '1.8')
        self.xstr.event_generate('<Key-w>')

        # The selected ranges should be the same.
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ())

    def test2(self):
        self.xstr.mark_set('insert', '1.11')
        self.xstr.event_generate('<Key-w>')

        # The selected ranges should be the same.
        ranges = self.xstr.tag_nextrange('sel', '1.7')
        self.assertEqual(ranges, ('1.11', '1.17'))

if __name__ == '__main__':
    unittest.main()
