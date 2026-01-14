from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
import random
import unittest
import time

class TestXstr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test0(self):
        xstr = root.note.create('Tests0')
        xstr.insert('end', 'Xstr test.\n' * 10)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        index0 = xstr.min('2.4', '3.5')
        self.assertEqual(index0, '2.4')

        # When there is no data in the Xstr '4.4' and '3.7' both
        # evaluates to equal.
        index1 = xstr.min('4.4', '3.7')
        self.assertEqual(index1, '3.7')

        index1 = xstr.min('5.4', '5.4')
        self.assertEqual(index1, '5.4')

        pass

    def test1(self):
        xstr = root.note.create('Tests1')
        xstr.insert('end', 'Xstr test.\n' * 10)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        index0 = xstr.max('2.4', '3.5')
        self.assertEqual(index0, '3.5')

        # When there is no data in the Xstr '4.4' and '3.7' both
        # evaluates to equal.
        index1 = xstr.max('4.4', '3.7')
        self.assertEqual(index1, '4.4')

        index2 = xstr.max('5.4', '5.4')
        self.assertEqual(index2, '5.4')

        pass

    """
    def test2(self):
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
    """

    def test3(self):
        """
        Test Xstr.replace_ranges method. Such a method is used to replace
        ranges of text that belong to a given tag name.
        """
        xstr = root.note.create('Tests3')
        xstr.insert('end', 'Xstr test.\n' * 10)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.delete('1.0', 'end')
        xstr.append('9985', 'sel')
        xstr.insert('end', '1234')
        xstr.append('9985', 'sel')
        xstr.insert('end', '8472')
        xstr.append('9985', 'sel')
        xstr.replace_ranges('sel', '9985', '*')

        data0 = xstr.get('1.0', 'end')
        self.assertEqual(data0, '*1234*8472*\n')

        xstr.tag_add('sel', '1.0', 'end')
        xstr.replace_ranges('sel', '\*', '9985')

        data1 = xstr.get('1.0', 'end')
        self.assertEqual(data1, '99851234998584729985\n')

        xstr.insert('end', '\n')
        xstr.append('5', 'sel')
        xstr.insert('end', '1232')
        xstr.append('6', 'sel')
        xstr.insert('end', '9421')
        xstr.append('7', 'sel')

        xstr.replace_ranges('sel', '5|6|7', '*')
        data2 = xstr.get('2.0', 'end')

        self.assertEqual(data2, '*1232*9421*\n')
        self.assertEqual(xstr.tag_ranges('sel'), ())

    def test4(self):
        xstr = root.note.create('Tests4')
        xstr.insert('end', '9985 3219 3212 9321\n')
        xstr.insert('end', '2391 3123 4212 3421\n')

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 
        xstr.mark_set('insert', '1.0')
        xstr.ipick('(IPICK)', '2391')

        ranges0 = xstr.tag_ranges('(IPICK)')
        self.assertEqual(tuple(map(str, ranges0)), ('2.0', '2.4'))
        xstr.tag_remove('(IPICK)', '1.0', 'end')

        xstr.ipick('(IPICK)', '4212')
        ranges1 = xstr.tag_ranges('(IPICK)')
        self.assertEqual(tuple(map(str, ranges1)), ('2.10', '2.14'))
        xstr.tag_remove('(IPICK)', '1.0', 'end')

        # When it is backwards we gotta invert stopindex and index.
        # That means we will be looking for a pattern from the end to the
        # beginning of the given range of text.
        xstr.mark_set('insert', 'end')
        xstr.ipick('(IPICK)', '3219', stopindex='1.0', 
        index='end', backwards=True)
    
        ranges2 = xstr.tag_ranges('(IPICK)')
        self.assertEqual(tuple(map(str, ranges2)), ('1.5', '1.9'))
        xstr.tag_remove('(IPICK)', '1.0', 'end')

        xstr.mark_set('insert', 'end')
        xstr.ipick('(IPICK)', '3421', stopindex='1.0', 
        index='end', backwards=True)
    
        ranges3 = xstr.tag_ranges('(IPICK)')
        self.assertEqual(tuple(map(str, ranges3)), 
        (xstr.index('2.0 lineend -4c'), xstr.index('2.0 lineend')))

        pass

if __name__ == '__main__':
    unittest.main()


