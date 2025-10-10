from cspkg.xstr import Xstr
from tkinter import Tk, BOTH

import unittest

class TestEscsApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.xstr = Xstr('', master=self.root)
        self.xstr.pack(expand=True, side='left', fill=BOTH)
        # self.xstr.insert('1.0', 'test')
        # self.assertEqual(self.xstr.get('1.0', 'end'), 'test\n')

    def tearDown(self):
        self.root.destroy()
        pass

    def test0(self):
        # self.assertEqual()
        # self.app.button.invoke() 
        # self.root.update_idletasks()
        pass

if __name__ == '__main__':
    unittest.main()


