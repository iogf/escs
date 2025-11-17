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
        cls.xstr = root.note.create('None')
        root.update() 

        cls.mod = TextJumps(cls.xstr)
        cls.mod.chmode(Normal)
        cls.xstr.focus_set()

    def setUp(self):
        pass

    def tearDown(self):
        self.xstr.delete('1.0', 'end')
        self.xstr.update()

    def test0(self):
        self.xstr.insert('end', 'Text start test.\n' * 10)
        self.xstr.mark_set('insert', 'end')
        self.xstr.update()

        self.xstr.event_generate('<Alt-g>')
        self.assertEqual(self.xstr.index('insert'), '1.0')


    def test1(self):
        self.xstr.insert('end', 'Text end test.\n' * 10)
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Alt-b>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('end linestart -1c'))

    def test2(self):
        self.xstr.insert('end', 'Text start test.\n' * 10)
        self.xstr.mark_set('insert', 'end')
        self.xstr.event_generate('<Key-s>')
        self.assertEqual(self.xstr.index('insert'), '1.0')

    def test3(self):
        self.xstr.mark_set('insert', '1.0')
        self.xstr.insert('end', 'Text end test.\n' * 10)
        self.xstr.event_generate('<Key-c>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('end linestart -1c'))

    def test4(self):
        self.xstr.insert('end', 'Line end test.\n')
        self.xstr.mark_set('insert', '1.0')

        self.xstr.event_generate('<Alt-e>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

    def test5(self):
        self.xstr.insert('end', 'Line start test.\n')
        self.xstr.mark_set('insert', '1.0 lineend')

        self.xstr.event_generate('<Alt-a>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert linestart'))

    def test6(self):
        self.xstr.insert('end', 'Line end test.\n')

        self.xstr.mark_set('insert', 'insert lineend')

        self.xstr.event_generate('<Alt-o>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert linestart'))

    def test7(self):
        self.xstr.insert('end', 'Line start test.\n')

        self.xstr.mark_set('insert', '1.0')

        self.xstr.event_generate('<Key-p>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('insert lineend'))

    def test8(self):
        self.xstr.insert('end', 'Next word test.\n')

        self.xstr.mark_set('insert', '1.0')

        self.xstr.event_generate('<Alt-l>')
        self.assertEqual(self.xstr.index('insert'), '1.4')

        self.xstr.event_generate('<Alt-l>')
        self.assertEqual(self.xstr.index('insert'), '1.9')

    def test9(self):
        self.xstr.insert('end', 'Next word test.\n')
        self.xstr.mark_set('insert', 'end')

        self.xstr.event_generate('<Alt-h>')
        self.assertEqual(self.xstr.index('insert'), '1.14')

        self.xstr.event_generate('<Alt-h>')
        self.assertEqual(self.xstr.index('insert'), '1.9')

    def test10(self):
        self.xstr.insert('end', 'Line up test.\n' * 10)
        self.xstr.mark_set('insert', 'end linestart')
        self.xstr.event_generate('<Key-k>')
        self.xstr.event_generate('<Alt-f>')

        self.assertEqual(self.xstr.index('insert'), '9.0')

    def test11(self):
        self.xstr.insert('end', 'Test slightly mode mechanism\n')

        self.mod.chmode(TestMode)
        self.xstr.mark_set('insert', '1.0 lineend')
        self.xstr.event_generate('<Key-o>')
        self.mod.chmode(Normal)
        self.xstr.event_generate('<Key-o>')
        self.assertEqual(self.xstr.index('insert'), self.xstr.index('1.0'))

    def test12(self):
        self.xstr.insert('end', 'Test slightly mode mechanism.\n')

        self.mod.chmode(TestMode)
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-p>')

        self.mod.chmode(Normal)
        self.xstr.event_generate('<Key-p>')
        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 lineend'))

    def test13(self):
        self.xstr.insert('end', 'Line down test.\n' * 10)
        self.xstr.mark_set('insert', '1.0 linestart')
        self.xstr.event_generate('<Key-j>')
        self.xstr.event_generate('<Alt-d>')

        self.assertEqual(self.xstr.index('insert'), '3.0')

        pass

    def test14(self):
        self.xstr.insert('end', 'Line left test.\n')
        self.xstr.mark_set('insert', '1.0 lineend')
        self.xstr.event_generate('<Key-h>')
        self.xstr.event_generate('<Alt-n>')

        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 lineend -2c'))

    def test15(self):
        self.xstr.insert('end', 'Line right test.\n')
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-l>')
        self.xstr.event_generate('<Alt-m>')

        self.assertEqual(self.xstr.index('insert'), 
        self.xstr.index('1.0 +2c'))

if __name__ == '__main__':
    unittest.main()