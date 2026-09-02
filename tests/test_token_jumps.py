from cspkg.core import Normal
from cspkg.plugins.token_jumps import TokenJumps
from cspkg.core import Mode, EscsApp
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestTokenJumps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Tests')
        cls.mod0 = TokenJumps(cls.xstr)

        root.note.select(0)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
       root.destroy()

    def test0(self):
        self.xstr.insert('end', '381 (123) [321] 932\n')
        self.xstr.mark_set('insert', '1.0')
        self.xstr.event_generate('<Key-bracketright>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.5')

        self.xstr.event_generate('<Key-bracketright>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.9')

        self.xstr.event_generate('<Key-bracketright>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.11')

        self.xstr.event_generate('<Key-bracketleft>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.10')

        self.xstr.event_generate('<Key-bracketleft>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.8')

        self.xstr.event_generate('<Key-bracketleft>')
        root.update() 

        self.assertEqual(self.xstr.index('insert'), '1.4')

        pass

    def test1(self):
        pass

if __name__ == '__main__':
    unittest.main()
