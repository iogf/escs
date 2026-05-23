from cspkg.plugins.html_mode import Html, HtmlMode
from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.core import rcmod
from cspkg.start import root
import unittest

class TestHtmlMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        xstr = root.note.create('Tests')
        mod0 = HtmlMode(xstr)
        mod1 = NormalMode(xstr)

        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        mod1.chmode(Normal)
        xstr.event_generate('<Key-at>')

        root.update() 
        self.assertEqual(mod0.mode, Html)
        mod1.chmode(Normal)

        root.update() 
        self.assertEqual(mod1.mode, Normal)

        xstr.tag_add('sel', '1.0', 'end')
        xstr.event_generate('<Key-at>')

        root.update() 
        self.assertEqual(xstr.tag_nextrange('sel', '1.0'), 
        ('1.0', xstr.index('end')))

        root.update() 
        self.assertEqual(mod0.mode, Html)
        xstr.event_generate('<Escape>')

        root.update() 
        self.assertEqual(mod1.mode, Normal)
        self.assertEqual(xstr.tag_nextrange('sel', '1.0'), ())
        pass

if __name__ == '__main__':
    unittest.main()
