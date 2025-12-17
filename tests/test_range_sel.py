from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.range_sel import RangeSel
from cspkg.start import root
import unittest
from os.path import join, expanduser

class TestWordSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = RangeSel(cls.xstr)

        cls.xstr.insert('end', 'RangeSel plugin test.\n' * 10)
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
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '4.5')
        self.xstr.event_generate('<Key-v>')

        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('2.0', '4.5'))

        self.xstr.mark_set('insert', '5.0')
        self.xstr.event_generate('<Key-v>')

        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('2.0', '5.0'))


        self.xstr.mark_set('insert', '7.0')
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '9.5')
        self.xstr.event_generate('<Key-v>')

        ranges = self.xstr.tag_nextrange('sel', '7.0')
        self.assertEqual(ranges, ('7.0', '9.5'))

        # Removes selection from '7.0' to '8.4'.
        self.xstr.mark_set('insert', '8.4')
        self.xstr.event_generate('<Key-x>')

        # Make sure selection was removed then checks selection on
        # '8.4' to '8.5'
        ranges = self.xstr.tag_nextrange('sel', '7.0')
        self.assertEqual(ranges, ('8.4', '9.5'))

        # The initial selection should remain intact.
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('2.0', '5.0'))

        # First drop the mark on '1.0'.
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-g>')

        # Remove the whole selection from '1.0' to '10.0'.
        self.xstr.mark_set('insert', '10.0')
        self.xstr.event_generate('<Key-x>')

        # Make sure no text is selected.
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ())

        # First drop the mark on '10.0'.
        self.xstr.mark_set('insert', '10.0')
        self.xstr.event_generate('<Key-g>')

        # Select from '1.0' to '10.0'
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-v>')

        # Make sure the range '1.0' to '10.0' is selected.
        ranges = self.xstr.tag_nextrange('sel', '1.0')
        self.assertEqual(ranges, ('1.0', '10.0'))

if __name__ == '__main__':
    unittest.main()
