from cspkg.plugins.normal_mode import Normal, NormalMode

from cspkg.plugins.brackets_sel import BracketsSel
from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestBracketsSel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((NormalMode, (), {}), (BracketsSel, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.destroy()
        pass

    def test0(self):
        """
        Test tab size/tab type spacing.
        """
        xstr = root.note.create('Tests')
        xstr.insert('end', '({[ABEAD]}) [{{C23FE})\n[([H411E3)]\n')
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.mark_set('insert', '1.')
        data = xstr.get('1.', '1. lineend')
        # self.assertEqual(data.startswith('    ['), True)
