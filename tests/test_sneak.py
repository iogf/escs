from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.plugins.sneak import Sneak, JumpNext, JumpBack
from cspkg.core import Mode, EscsApp
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestSneak(unittest.TestCase):
    def test0(self):
        xstr = root.note.create('Tests')

        mod0 = NormalMode(xstr)
        mod1 = Sneak(xstr)

        root.note.select(0)
        xstr.focus_set()
        root.update() 

        xstr.insert('end', '381 123 321 932\n')
        xstr.mark_set('insert', '1.0')

        xstr.event_generate('<Key-period>')
        self.assertEqual(mod1.mode, JumpNext)

        xstr.event_generate('<Key-2>')
        xstr.mark_set('insert', '1.6')
        self.assertEqual(mod0.mode, Normal)
    
        xstr.event_generate('<Key-period>')
        self.assertEqual(mod1.mode, JumpNext)

        xstr.event_generate('<Key-9>')
        self.assertEqual(xstr.index('insert'), '1.13')
        self.assertEqual(mod0.mode, Normal)

        xstr.insert('end', '711 143 331 231\n')
        xstr.event_generate('<Key-period>')
        self.assertEqual(mod1.mode, JumpNext)
        xstr.event_generate('<Key-7>')
        self.assertEqual(xstr.index('insert'), '2.1')
        self.assertEqual(mod0.mode, Normal)

        xstr.event_generate('<Key-comma>')
        self.assertEqual(mod1.mode, JumpBack)
        xstr.event_generate('<Key-2>')
        self.assertEqual(xstr.index('insert'), '1.14')
        self.assertEqual(mod0.mode, Normal)

        xstr.event_generate('<Key-comma>')
        self.assertEqual(mod1.mode, JumpBack)
        xstr.event_generate('<Key-8>')
        self.assertEqual(xstr.index('insert'), '1.1')
        self.assertEqual(mod0.mode, Normal)

        xstr.insert('end', '881 823 821 982\n')
        xstr.mark_set('insert', '3.0')

        xstr.event_generate('<Key-period>')
        xstr.event_generate('<Key-8>')
        self.assertEqual(xstr.index('insert'), '3.1')

        xstr.event_generate('<Key-semicolon>')
        self.assertEqual(xstr.index('insert'), '3.2')

        xstr.event_generate('<Key-semicolon>')
        self.assertEqual(xstr.index('insert'), '3.5')

        xstr.mark_set('insert', 'end')

        xstr.event_generate('<Key-comma>')
        xstr.event_generate('<Key-8>')
        self.assertEqual(xstr.index('insert'), 
        xstr.index('3.0 lineend -2c'))

        xstr.event_generate('<Key-comma>')
        xstr.event_generate('<Key-8>')
        self.assertEqual(xstr.index('insert'), 
        xstr.index('3.0 lineend -7c'))

        xstr.event_generate('<Key-comma>')
        xstr.event_generate('<Key-8>')
        self.assertEqual(xstr.index('insert'), 
        xstr.index('3.0 lineend -11c'))

        pass

if __name__ == '__main__':
    unittest.main()
