from cspkg.core import Normal, Extra
from cspkg.plugins.code_comments import CodeComments
from cspkg.core import Mode, EscsApp, rcmod
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestCodeComments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.append((CodeComments, (), {}))

    @classmethod
    def tearDownClass(cls):
       root.destroy()

    def test0(self):
        # Test for python files.
        xstr0 = root.note.create('Tests.py')
        root.note.select(0)
        xstr0.focus_set()
        root.update() 
 
        xstr0.insert('end', '381 123 321 932\n')
        xstr0.mark_set('insert', '1.0')
        xstr0.tag_add('sel', '1.0', '1.0 lineend')

        xstr0.event_generate('<Key-b>')
        xstr0.event_generate('<Key-c>')

        data0 = xstr0.get('1.0', 'end') 
        root.update() 

        self.assertEqual(data0.startswith('#'), True)
        
        # Test for removing python comments.
        xstr0.tag_add('sel', '1.0', '1.0 lineend')
        xstr0.event_generate('<Key-b>')
        xstr0.event_generate('<Key-C>')

        data0 = xstr0.get('1.0', 'end') 
        root.update() 

        self.assertEqual(data0.startswith('#'), False)

        # Test for cpp files.
        xstr1 = root.note.create('Tests.cpp')
        root.note.select(1)
        xstr1.focus_set()
        root.update() 

        # Create three lines in the Xstr instance to be commented.
        xstr1.insert('end', '321 921 421 332\n' * 3)
        xstr1.tag_add('sel', '1.0', 'end')

        xstr1.event_generate('<Key-b>')
        xstr1.event_generate('<Key-c>')

        # Check whether comments were added in all selected lines.
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr1.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith('//'), True)

        # Test for removing cpp comments.
        xstr1.tag_add('sel', '1.0', 'end')
        xstr1.event_generate('<Key-b>')
        xstr1.event_generate('<Key-C>')

        # Check whether comments were removed correctly.
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr1.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith('//'), False)

