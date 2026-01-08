from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
import random
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

    def test2(self):
        """ 
        Create multiple Xstr instances along panes and tabs then
        check whether Xstr.xstr_widgets and Xstr.get_opened_files work correctly.
        """

        xstr0 = self.xstr.master.master.create('Xstr0')
        xstr1 = self.xstr.master.master.create('Xstr1')

        xstr2 = self.xstr.master.master.master.create('Xstr2')

        xstr3 = xstr2.master.master.create('Xstr3')
        lst0 = list(self.xstr.xstr_widgets(root))

        self.assertEqual(len(lst0), 5)

        self.assertIn(xstr0, lst0)
        self.assertIn(xstr1, lst0)
        self.assertIn(xstr2, lst0)
        self.assertIn(xstr3, lst0)

        # Create tabs and check if if Xstr.xstr_widgets returns
        # the correct Xstr instances.
        xstr4 = root.note.create('Xstr4')
        xstr5 = root.note.create('Xstr5')

        lst1 = list(self.xstr.xstr_widgets(root))
        self.assertIn(xstr4, lst1)
        self.assertIn(xstr5, lst1)
        self.assertEqual(len(lst1), 7)

        lst2 = self.xstr.get_opened_files(root)
        self.assertEqual(len(lst1), 7)

        for indi, indj in lst2.items():
            self.assertIn(indj, lst1)

        xstr0.master.destroy()
        xstr1.master.destroy()

        xstr2.master.master.destroy()
        xstr3.master.destroy()
        
        xstr4.master.master.master.destroy()
        xstr5.master.master.master.destroy()

        lst3 = list(self.xstr.xstr_widgets(root))
        self.assertEqual(len(lst3), 1)
        self.assertIn(self.xstr, lst3)

    def test3(self):
        """
        Test Xstr.replace_ranges method. Such a method is used to replace
        ranges of text that belong to a given tag name.
        """

        self.xstr.delete('1.0', 'end')
        self.xstr.append('9985', 'sel')
        self.xstr.insert('end', '1234')
        self.xstr.append('9985', 'sel')
        self.xstr.insert('end', '8472')
        self.xstr.append('9985', 'sel')
        self.xstr.replace_ranges('sel', '9985', '*')

        data0 = self.xstr.get('1.0', 'end')
        self.assertEqual(data0, '*1234*8472*\n')

        self.xstr.tag_add('sel', '1.0', 'end')
        self.xstr.replace_ranges('sel', '\*', '9985')

        data1 = self.xstr.get('1.0', 'end')
        self.assertEqual(data1, '99851234998584729985\n')

        self.xstr.insert('end', '\n')
        self.xstr.append('5', 'sel')
        self.xstr.insert('end', '1232')
        self.xstr.append('6', 'sel')
        self.xstr.insert('end', '9421')
        self.xstr.append('7', 'sel')

        self.xstr.replace_ranges('sel', '5|6|7', '*')
        data2 = self.xstr.get('2.0', 'end')

        self.assertEqual(data2, '*1232*9421*\n')
        self.assertEqual(self.xstr.tag_ranges('sel'), ())

if __name__ == '__main__':
    unittest.main()


