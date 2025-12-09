from cspkg.plugins.normal_mode import Normal
from cspkg.core import Main, Mode
from cspkg.start import root
import unittest
import time

class TestXstr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('null')

        cls.xstr.insert('end', '')
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()


