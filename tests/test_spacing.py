from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.insert_mode import Insert, InsertMode

from cspkg.plugins.spacing import TabSpacing, tabset
from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestSpacing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((InsertMode, (), {}),
        (NormalMode, (), {}), (TabSpacing, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        """
        Test tab size/tab type spacing.
        """
        xstr0 = root.note.create('Tests')
        xstr0.insert('end', '[ABEeD] (C23aE) (EBcF} 4113\n')
        root.note.select(xstr0.master.master.master)
        xstr0.focus_set()
        root.update() 

        xstr0.mark_set('insert', '1.0')
        xstr0.event_generate('<Key-i>')
        xstr0.event_generate('<Tab>')
        xstr0.event_generate('<Escape>')

        data0 = xstr0.get('1.0', '1.0 lineend')
        root.update() 

        self.assertEqual(data0.startswith('    ['), True)

        xstr1 = root.note.create('Tests.ext')
        xstr1.insert('end', '[FBEeD] (U23aE) (DBcF} 41E3\n')
        root.note.select(xstr1.master.master.master)
        xstr1.focus_set()
        root.update() 

        TabSpacing.c_tabsize({'.ext': (2, ' ')})
        xstr1.event_generate('<<LoadData>>')
        xstr1.mark_set('insert', '1.0')
        xstr1.event_generate('<Key-i>')
        xstr1.event_generate('<Tab>')
        xstr1.event_generate('<Escape>')
        data1 = xstr1.get('1.0', '1.0 lineend')
        root.update() 

        self.assertEqual(data1.startswith('  ['), True)


        xstr2 = root.note.create('Tests.ext')
        xstr2.insert('end', '(FBEeD) (U23aE) (DBcF} 41E3\n')
        root.note.select(xstr2.master.master.master)
        xstr2.focus_set()
        root.update() 

        TabSpacing.c_tabsize({'.ext': (3, ' ')})
        xstr2.event_generate('<<SaveData>>')
        xstr2.mark_set('insert', '1.0')
        xstr2.event_generate('<Key-i>')
        xstr2.event_generate('<Tab>')
        xstr2.event_generate('<Escape>')
        data2 = xstr2.get('1.0', '1.0 lineend')
        root.update() 

        self.assertEqual(data2.startswith('   ('), True)

if __name__ == '__main__':
    unittest.main()
