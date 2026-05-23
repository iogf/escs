from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode, EscsApp
from cspkg.start import root

import random
import unittest
import time

class TestXstrWidgets(unittest.TestCase):
    """
    Test Xstr.xstr_widgets separately to avoid
    conflicts with other tests. The Xstr.xstr_widgets 
    returns the number of Xstr instances.

    When testing such a method with others it turns out necessary
    to keep track of the number of Xstr instances that were created.
    It makes testing slightly more complicated.
    """

    def test0(self):
        xstr = root.note.create('Tests')
        xstr0 = xstr.master.master.create('Xstr0')
        xstr1 = xstr.master.master.create('Xstr1')

        xstr2 = xstr.master.master.master.create('Xstr2')

        xstr3 = xstr2.master.master.create('Xstr3')
        lst0 = list(xstr.xstr_widgets(root))
        self.update()
        self.assertEqual(len(lst0), 5)

        self.assertIn(xstr0, lst0)
        self.assertIn(xstr1, lst0)
        self.assertIn(xstr2, lst0)
        self.assertIn(xstr3, lst0)

        # Create tabs and check if if Xstr.xstr_widgets returns
        # the correct Xstr instances.
        xstr4 = root.note.create('Xstr4')
        xstr5 = root.note.create('Xstr5')

        lst1 = list(xstr.xstr_widgets(root))
        self.update()

        self.assertIn(xstr4, lst1)
        self.assertIn(xstr5, lst1)
        self.assertEqual(len(lst1), 7)

        lst2 = xstr.get_opened_files(root)
        self.assertEqual(len(lst1), 7)

        for indi, indj in lst2.items():
            self.assertIn(indj, lst1)

        xstr0.master.destroy()
        xstr1.master.destroy()

        xstr2.master.master.destroy()
        xstr3.master.destroy()
        
        xstr4.master.master.master.destroy()
        xstr5.master.master.master.destroy()
        self.update()

        lst3 = list(xstr.xstr_widgets(root))

        self.assertEqual(len(lst3), 1)
        self.assertIn(xstr, lst3)

if __name__ == '__main__':
    unittest.main()

