from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.block_sel import BlockSel
from cspkg.plugins.range_sel import RangeSel

from cspkg.start import root
import unittest
from os.path import join, expanduser

class TestBlockSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = BlockSel(cls.xstr)
        cls.mod2 = RangeSel(cls.xstr)

        cls.xstr.insert('end', 'BlockSel plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()

        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass

    def test0(self):
        self.xstr.mark_set('insert', '2.0')
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '4.5')
        self.xstr.event_generate('<Key-V>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        for ind in range(0, len(ranges), 2):
            self.assertEqual(len(self.xstr.get(
                    ranges[ind], ranges[ind+1])), 5)
        self.assertEqual(len(ranges)/2, 3)

        # It removes selection in block from '2.0' to '4.3'.
        self.xstr.mark_set('insert', '2.0')
        self.xstr.mark_set('insert', '4.3')
        self.xstr.event_generate('<Key-X>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        for ind in range(0, len(ranges), 2):
            self.assertEqual(len(self.xstr.get(
                ranges[ind], ranges[ind+1])), 2)
        self.assertEqual(len(ranges)/2, 3)

        # It adds selection in block from '5.3' to '8.5'.
        self.xstr.mark_set('insert', '5.3')
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '8.5')
        self.xstr.event_generate('<Key-V>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        # Make sure it has length 2.
        for ind in range(0, len(ranges), 2):
            self.assertEqual(len(self.xstr.get(
                ranges[ind], ranges[ind+1])), 2)
        self.assertEqual(len(ranges)/2, 7)

        self.xstr.mark_set('insert', '2.0')
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '9.6')
        self.xstr.event_generate('<Key-V>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        # Make sure it has length 6.
        for ind in range(0, len(ranges), 2):
            self.assertEqual(len(self.xstr.get(
                ranges[ind], ranges[ind+1])), 6)
        self.assertEqual(len(ranges)/2, 8)

        self.xstr.event_generate('<Escape>')

    def test1(self):
        self.xstr.mark_set('insert', '9.8')
        self.xstr.event_generate('<Key-g>')

        self.xstr.mark_set('insert', '3.5')
        self.xstr.event_generate('<Key-V>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        # Make sure it has length 6.
        for ind in range(0, len(ranges), 2):
            self.assertEqual(len(self.xstr.get(
                ranges[ind], ranges[ind+1])), 3)
        self.assertEqual(len(ranges)/2, 7)

        # Removes all block selection.
        self.xstr.mark_set('insert', '3.5')
        self.xstr.event_generate('<Key-X>')

        ranges = self.xstr.tag_ranges('sel')
        root.update() 

        self.assertEqual(ranges, ())

if __name__ == '__main__':
    unittest.main()
