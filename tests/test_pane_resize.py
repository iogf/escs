from cspkg.core import Normal, NormalMode
from cspkg.plugins.splits import Splits

from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.core import rcmod
from cspkg.plugins.pane_resize import PaneResize
import unittest
import time

class TestPaneResize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((NormalMode, (), {}), (Splits, (), {}), (PaneResize, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass

    def test0(self):
        """
        Create several panes v/h through splits plugin then resizes these panes through
        pane_rize keystrokes.
        """

        # Create a horizontal pane.
        xstr0 = root.note.create('Tests')
        # xstr0.insert('end', '[ABEeD] (C23aE) (EBcF} 4113\n')
        root.note.select(xstr0.master.master.master)
        xstr0.focus_set()
        root.update() 

        # Create another horizontal pane.
        xstr0.event_generate('<Alt-V>')
        root.update() 

        # Grab the Xstr instance.
        xstr1 = root.focus_get()

        xstr0_width0 = xstr0.winfo_width()
        xstr1.event_generate('<Control-h>')
        root.update() 
        xstr0_width1 = xstr0.winfo_width()
        root.update() 

        self.assertEqual(xstr0_width0 - 15, xstr0_width1)

        xstr0_width2 = xstr0.winfo_width()
        xstr1.event_generate('<Control-h>')
        root.update() 
        xstr0_width3 = xstr0.winfo_width()
        root.update() 

        self.assertEqual(xstr0_width2 - 15, xstr0_width3)

        # Create a vertical pane.
        xstr1.event_generate('<Alt-C>')
        root.update() 
    
        # Grab the Xstr instance.
        xstr2 = root.focus_get()

        xstr2_height0 = xstr2.winfo_height()
        xstr2.event_generate('<Control-j>')
        root.update() 
        xstr2_height1 = xstr2.winfo_height()
        root.update() 

        self.assertEqual(xstr2_height0 - 15, xstr2_height1)


        # Create another vertical pane then grab the Xstr instance.
        # It checks v/h size for the created Xstr instances through
        # pane_resize keystrokes.
        xstr2.event_generate('<Alt-C>')
        root.update() 
        xstr3 = root.focus_get()

        xstr3_height0 = xstr3.winfo_height()
        xstr3.event_generate('<Control-j>')
        root.update() 
        xstr3_height1 = xstr3.winfo_height()

        self.assertEqual(xstr3_height0 - 15, xstr3_height1)

        xstr3_height2 = xstr3.winfo_height()
        xstr3.event_generate('<Control-k>')
        root.update() 
        xstr3_height3 = xstr3.winfo_height()
        self.assertEqual(xstr3_height2, xstr3_height3 - 15)

        # Set the focus to the first Xstr instance.
        xstr0.focus_set()
    
        # Create a third pane in the PanedWindow that is horizontal.
        xstr0.event_generate('<Alt-V>')
        root.update() 

        # Grab the Xstr instance.
        xstr4 = root.focus_get()

        # Finally check the width for the third pane in the first row
        # of Xstr instances.
        xstr1_width3 = xstr1.winfo_width()
        xstr4.event_generate('<Control-h>')
        root.update() 
        xstr1_width4 = xstr1.winfo_width()
        self.assertEqual(xstr1_width3 - 15, xstr1_width4)

        xstr1_width5 = xstr1.winfo_width()
        xstr4.event_generate('<Control-h>')
        root.update() 
        xstr1_width6 = xstr1.winfo_width()
        self.assertEqual(xstr1_width5 - 15, xstr1_width6)

        xstr1_width7 = xstr1.winfo_width()
        xstr4.event_generate('<Control-l>')
        root.update() 
        xstr1_width8 = xstr1.winfo_width()
        self.assertEqual(xstr1_width7, xstr1_width8 - 15)

