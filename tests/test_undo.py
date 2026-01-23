from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.insert_mode import Insert, InsertMode
from cspkg.plugins.clipboard import Clipboard

from cspkg.plugins.undo import Undo
from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestUndo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((InsertMode, (), {}), (Clipboard, (), {}),
        (NormalMode, (), {}), (Undo, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        """
        """
        xstr = root.note.create('Tests')
        root.note.select(xstr.master.master.master)
        xstr.insert('end', '[ABEeD]')
        xstr.focus_set()
        root.update() 

        data0 = xstr.get('1.0', 'end')
        xstr.tag_add('sel', '1.0', 'end')
        xstr.event_generate('<Key-u>')
        xstr.event_generate('<Escape>')

        data0 = xstr.get('1.0', 'end')
        self.assertTrue(data0 == '\n')

        xstr.event_generate('<Key-q>')
        data1 = xstr.get('1.0', 'end')
        self.assertTrue(data1.startswith('[ABEeD]'))

        xstr.event_generate('<Key-Q>')
        data2 = xstr.get('1.0', 'end')
        self.assertTrue(data2 == '\n')

        xstr.mark_set('insert', 'end')
        xstr.event_generate('<Key-t>')
        data3 = xstr.get('1.0', 'end')
        self.assertTrue(data3.startswith('[ABEeD]'))

        xstr.mark_set('insert', 'end')
        xstr.event_generate('<Key-q>')

        data4 = xstr.get('1.0', 'end')
        self.assertTrue(data4 == '\n')

if __name__ == '__main__':
    unittest.main()
