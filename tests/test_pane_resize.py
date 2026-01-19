from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.insert_mode import Insert, InsertMode
from cspkg.core import Main, Mode
from cspkg.start import root
from cspkg.plugins.pane_resize import PaneResize
import unittest
import time

class TestPaneResize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xstr = root.note.create('Test')

        cls.mod = PaneResize(cls.xstr0)
        root.note.select(cls.xstr.master.master.master)
        cls.xstr.focus_set()
        root.update() 

    @classmethod
    def tearDownClass(cls):
        root.note.forget(0)
        pass
