from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
import unittest
import time

class TestXstr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')

        cls.xstr.insert('end', 'Xstr test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        index0 = self.xstr.min('2.4', '3.5')
        self.assertEqual(index0, '2.4')

        # When there is no data in the Xstr '4.4' and '3.7' both
        # evaluates to equal.
        index1 = self.xstr.min('4.4', '3.7')
        self.assertEqual(index1, '3.7')

        index1 = self.xstr.min('5.4', '5.4')
        self.assertEqual(index1, '5.4')

        pass

    def test1(self):
        index0 = self.xstr.max('2.4', '3.5')
        self.assertEqual(index0, '3.5')

        # When there is no data in the Xstr '4.4' and '3.7' both
        # evaluates to equal.
        index1 = self.xstr.max('4.4', '3.7')
        self.assertEqual(index1, '4.4')

        index2 = self.xstr.max('5.4', '5.4')
        self.assertEqual(index2, '5.4')

        pass

if __name__ == '__main__':
    unittest.main()


