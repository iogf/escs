from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.line_index import LineIndex
from cspkg.scan import ScanCancel
from cspkg.start import root
from tkinter import TclError
import unittest

class TestLineIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('null')
        cls.mod0 = NormalMode(cls.xstr)
        cls.mod1 = LineIndex(cls.xstr)

        cls.xstr.insert('end', 'LineIndex plugin test.\n' * 10)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass

    def test0(self):
        self.xstr.after(100, self.test0_helper0)
        self.xstr.event_generate('<Alt-w>')
        self.assertEqual(self.xstr.index('insert'), '2.3')

    def test0_helper0(self):
        scan = root.focus_get()
        scan.insert('end', '2 3')
        scan.event_generate('<Return>')

    def test1(self):
        self.xstr.after(100, self.test1_helper0)
        self.xstr.event_generate('<Alt-w>')
        self.assertEqual(self.xstr.index('insert'), '5.0')

    def test1_helper0(self):
        scan = root.focus_get()
        scan.insert('end', '5')
        scan.event_generate('<Return>')

    def test2(self):
        self.xstr.mark_set('insert', '2.0')
        self.xstr.after(100, self.test2_helper0)
        self.xstr.event_generate('<Alt-w>')
        self.assertEqual(self.xstr.index('insert'), '2.0')

    def test2_helper0(self):
        scan = root.focus_get()
        scan.event_generate('<Escape>')

if __name__ == '__main__':
    unittest.main()
