from cspkg.core import Normal, NormalMode
from cspkg.plugins.line_sel import LineSel
from cspkg.start import root
import unittest
from os.path import join, expanduser

class TestLineSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = LineSel(cls.xstr)

        cls.xstr.insert('end', 'LineSel plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()

        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)

        # cls.xstr.master.master.master.destroy()
        pass

    def test0(self):
        self.xstr.mark_set('insert', '2.0')
        self.xstr.event_generate('<Key-f>')

        ranges = self.xstr.tag_nextrange('sel', '1.0')
        root.update() 
        self.assertEqual(ranges, ('2.0', self.xstr.index('2.0 +1l')))

        # Sending Key-f it removes the selection on the line.
        self.xstr.event_generate('<Key-f>')
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ())

        self.xstr.mark_set('insert', '4.0')
        self.xstr.event_generate('<Key-f>')

        ranges = self.xstr.tag_nextrange('sel', '4.0')
        root.update() 
        self.assertEqual(ranges, ('4.0', self.xstr.index('4.0 +1l')))

        self.xstr.event_generate('<Key-f>')
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        root.update() 
        self.assertEqual(ranges, ())

        # Add selection from 1.0 to 4.0 then place the cursor at the
        # position 2.0 and sends <Key-f> to remove the selection from the line.
        self.xstr.tag_add('sel', '1.0', '4.0')
        self.xstr.mark_set('insert', '2.0')
        self.xstr.event_generate('<Key-f>')

        # Make sure it has left to ranges of text selection.
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        root.update() 

        self.assertEqual(ranges, ('1.0', self.xstr.index('1.0 +1l')))

        ranges = self.xstr.tag_nextrange('sel', '2.0')
        root.update() 
        self.assertEqual(ranges, ('3.0', self.xstr.index('3.0 +1l')))

if __name__ == '__main__':
    unittest.main()
