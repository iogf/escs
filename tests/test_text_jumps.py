from cspkg.core import Main, Mode
from cspkg.plugins.text_jumps import TextJumps
from cspkg.plugins.normal_mode import Normal
from cspkg.start import root
import unittest
import time

class TestMode(Mode):
    pass

class TestTextJumps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')

        cls.mod = TextJumps(cls.xstr)
        cls.mod.chmode(Normal)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        cls.xstr.insert('end', 'TextJumps plugin test.\n' * 10)
        root.update() 

        pass

    @classmethod
    def tearDownClass(cls):
        cls.xstr.update()
        root.note.forget(0)

    def test0(self):
        self.xstr.mark_set('insert', 'end')
        self.xstr.event_generate('<Alt-g>')
        self.assertEqual(self.xstr.index('insert'), '1.0')


    def test1(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Alt-b>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('end linestart -1c'))

    def test2(self):
        self.xstr.mark_set('insert', 'end')
        self.xstr.event_generate('<Key-s>')
        self.assertEqual(self.xstr.index('insert'), '1.0')

    def test3(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-c>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('end linestart -1c'))

    def test4(self):
        self.xstr.mark_set('insert', '1.0')

        self.xstr.event_generate('<Alt-e>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

    def test5(self):
        self.xstr.mark_set('insert', '1.0 lineend')

        self.xstr.event_generate('<Alt-a>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert linestart'))

    def test6(self):
        self.xstr.mark_set('insert', 'insert lineend')

        self.xstr.event_generate('<Alt-o>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert linestart'))

    def test7(self):
        self.xstr.mark_set('insert', '1.0')

        self.xstr.event_generate('<Key-p>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

    def test8(self):
        # Tests aren't executed orderely as it is created
        # so we make sure last column i.e (LC) mark is accordingly set.
        self.xstr.mark_set('(LC)', 'end linestart')
        self.xstr.mark_set('insert', 'end linestart')

        self.xstr.event_generate('<Key-k>')
        self.xstr.event_generate('<Alt-f>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('end -3l'))

    def test9(self):
        self.xstr.mark_set('(LC)', '1.0 linestart')
        self.xstr.mark_set('insert', '1.0 linestart')
        self.xstr.event_generate('<Key-j>')
        self.xstr.event_generate('<Alt-d>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 +2l'))
        pass

    def test10(self):
        self.xstr.mark_set('insert', '1.0 lineend')
        self.xstr.event_generate('<Key-h>')
        self.xstr.event_generate('<Alt-n>')

        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 lineend -2c'))

    def test11(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-l>')
        self.xstr.event_generate('<Alt-m>')

        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 +2c'))

if __name__ == '__main__':
    unittest.main()
