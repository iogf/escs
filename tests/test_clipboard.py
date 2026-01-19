from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.extra_mode import Extra, ExtraMode
from cspkg.plugins.insert_mode import Insert, InsertMode
from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.plugins.clipboard import Clipboard
import unittest
import time

class TestClipboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Test')

        cls.mod0 = Clipboard(cls.xstr)
        cls.mod1 = NormalMode(cls.xstr)
        cls.mod2 = InsertMode(cls.xstr)
        cls.mod3 = ExtraMode(cls.xstr)

        root.note.select(0)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        self.xstr.insert('end', '2123\n')
        self.xstr.insert('end', '1231\n')
        self.xstr.insert('end', '4921\n')
        self.xstr.tag_add('sel', '1.0', '1.4')
        self.xstr.event_generate('<Key-y>')
        data0 = self.xstr.clipboard_get()
        self.assertEqual(data0, '2123')

        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-r>')

        data1 = self.xstr.get('1.0', '2.0 lineend')
        self.assertEqual(data1, '2123\n21231231')

        self.xstr.tag_add('sel', '3.0', '3.4')
        self.xstr.event_generate('<Key-u>')
        data2 = self.xstr.clipboard_get()
        self.assertEqual(data2, '4921')

        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-e>')

        data3 = self.xstr.get('1.0', '2.0 linestart')
        self.assertEqual(data3, '49212123\n')
        self.xstr.delete('1.0', 'end')

        self.xstr.insert('end', '4213\n')
        self.xstr.insert('end', '9312\n')
        self.xstr.insert('end', '4212\n')
        self.xstr.tag_add('sel', '1.0', '1.0 lineend')
        self.xstr.tag_add('sel', '3.0', '3.0 lineend')

        self.xstr.event_generate('<Alt-v>')
        self.xstr.event_generate('<Key-y>')

        data4 = self.xstr.clipboard_get()
        self.assertEqual(data4, '4213\n4212\n')

        self.xstr.tag_add('sel', '1.0', '1.0 lineend')
        self.xstr.tag_add('sel', '3.0', '3.0 lineend')

        self.xstr.event_generate('<Alt-v>')
        self.xstr.event_generate('<Key-u>')

        data5 = self.xstr.clipboard_get()

        # As it was already tested paste before and paste after then
        # no need to repaste it again.
        self.assertEqual(data5, '4213\n4212\n')
        
        # It tests paste block. First it copies the block region        
        # with seprator '\n' then pastes it at the end of the text lines.
        self.xstr.delete('1.0', 'end')
        self.xstr.insert('end', '1234\n')
        self.xstr.insert('end', '5321\n')
        self.xstr.insert('end', '5731')

        self.xstr.tag_add('sel', '1.0', '1.1')
        self.xstr.tag_add('sel', '2.0', '2.1')
        self.xstr.tag_add('sel', '3.0', '3.1')

        self.xstr.event_generate('<Alt-v>')
        self.xstr.event_generate('<Key-y>')
        self.assertEqual(self.xstr.clipboard_get(), '1\n5\n5\n')
        self.xstr.mark_set('insert', '1.0 lineend')

        self.xstr.event_generate('<Alt-v>')
        self.xstr.event_generate('<Key-t>')
        data6 = self.xstr.get('1.0', 'end')
        self.assertEqual(data6, '12341\n53215\n57315\n')

        self.xstr.mark_set('insert', '1.1')

        self.xstr.event_generate('<Alt-v>')
        self.xstr.event_generate('<Key-t>')
        data6 = self.xstr.get('1.0', 'end')
        self.assertEqual(data6, '112341\n553215\n557315\n')

        pass

