from cspkg.plugins.normal_mode import Normal, NormalModeNS, NormalMode
from cspkg.core import rcmod
from cspkg.start import root
from cspkg.plugins.tabs import Tabs
from cspkg.xstr import Xstr
from os.path import join, expanduser, basename
import tempfile
import os
import unittest
import time

class TestTabs(unittest.TestCase):
    def test0(self):
        rcmod.extend(((Tabs, (), {}), (NormalMode, (), {})))
        xstr = root.note.create('Test')
        root.note.select(0)

        xstr.focus_set()
        root.update() 

        tab_id0 = root.note.select()

        # It also works generating events on root window
        # these are propagated to the focused instance 
        # that is Xstr class.
        root.event_generate('<Alt-R>')
        root.note.select(1)
        tab_id1 = root.note.select()

        tab = root.nametowidget(tab_id1)
        root.update() 

        self.assertEqual(root.note.tab(tab_id1, 'text'), 'null')

        root.event_generate('<Alt-R>')
        root.event_generate('<Alt-R>')
        tab_id2 = root.note.select()
        
        # When a new tab is created it is not selected automatically
        # thus the focus shoud remain on tab_id1.
        root.update() 

        self.assertEqual(tab_id2, tab_id1)
        self.assertEqual(len(root.note.tabs()), 4)

        root.note.select(0)
        
        # Test select left and select right keystrokes.
        root.event_generate('<Alt-p>')
        root.update() 

        self.assertEqual(root.note.index('current'), 1)

        root.event_generate('<Alt-p>')
        root.update() 

        self.assertEqual(root.note.index('current'), 2)

        root.event_generate('<Alt-p>')
        root.update() 

        self.assertEqual(root.note.index('current'), 3)
    
        root.event_generate('<Alt-o>')
        root.update() 

        self.assertEqual(root.note.index('current'), 2)

        root.event_generate('<Alt-o>')
        root.update() 

        self.assertEqual(root.note.index('current'), 1)

        root.event_generate('<Alt-o>')
        root.update() 

        self.assertEqual(root.note.index('current'), 0)

        # Test Alt-x i.e removing tabs.
        root.event_generate('<Alt-x>')
        root.update()

        tab_id3 = root.note.select()
        index0 = root.note.index(tab_id3)
            
        # # Check focus has returned to the first tab.
        root.update() 

        self.assertEqual(index0, 0)

        root.event_generate('<Alt-x>')
        root.update()

        root.event_generate('<Alt-x>')
        root.update()

        root.event_generate('<Alt-x>')
        root.update()
        self.assertEqual(len(root.note.tabs()), 1)

    # def test3(self):
        # It is not working when root.focus_get is called.
        # The focused filedialog Entry instance should be returned but it
        # occurs an exception.
        # file = tempfile.NamedTemporaryFile()
# 
        # def shell():
            # widget = root.focus_get()
            # print('widget:', widget)
            # widget.insert('end', file.name)
            # widget.event_generate('<Return>')
# 
        # root.after(1000, shell)
        # xstr.event_generate('<Alt-E>')
        # root.update()
        # root.update_idletasks()
# 
# 
        # root.update() 
        # file.close()
# 
        # self.assertEqual(xstr.filename, file.name)

