from cspkg.core import Normal, NormalMode, Insert, InsertMode
from cspkg.plugins.splits import Splits
from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestSpacing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((InsertMode, (), {}),
        (NormalMode, (), {}), (Splits, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass

    def test0(self):
        """
        Test tab size/tab type spacing.
        """
        xstr0 = root.note.create('Tests')
        root.note.select(xstr0.master.master.master)
        xstr0.focus_set()
        root.update() 

        # Create horizontal panes.
        xstr0.event_generate('<Alt-V>')
        xstr0.event_generate('<Alt-V>')
        xstr0.event_generate('<Escape>')

        # Check whether they were created.
        panes0 = xstr0.master.master.panes()
        root.update() 

        self.assertEqual(len(panes0), 3)
        xstr0.event_generate('<Alt-V>')

        xstr1 = root.focus_get()
        panes1 = xstr1.master.master.panes()
        root.update() 

        self.assertEqual(len(panes1), 4)

        # Create vertical panes for such it grabs the focus from
        # the previous Xstr instance that is active then it generates 
        # the event.
        xstr2 = root.focus_get()
        xstr2.event_generate('<Alt-C>')
        panes2 = xstr2.master.master.master.panes()
        root.update() 

        self.assertEqual(len(panes2), 2)

        xstr2.event_generate('<Alt-C>')

        xstr3 = root.focus_get()
        panes3 = xstr3.master.master.master.panes()
        root.update() 

        self.assertEqual(len(panes3), 3)

        xstr4 = root.focus_get()
        xstr4.event_generate('<Alt-C>')

        panes5 = xstr4.master.master.master.panes()
        root.update() 

        self.assertEqual(len(panes5), 4)

if __name__ == '__main__':
    unittest.main()

