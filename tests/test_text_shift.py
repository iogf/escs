from cspkg.core import Normal
from cspkg.plugins.text_shift import TextShift
from cspkg.core import Mode, EscsApp, rcmod
from cspkg.start import root
from tkinter import TclError
import unittest
import time

class TestTextShift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.append((TextShift, (), {}))

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        xstr = root.note.create('Tests')
        root.note.select(0)
        xstr.focus_set()
        root.update() 
 
        xstr.insert('end', '381 123 321 932\n')
        xstr.mark_set('insert', '1.0')
        xstr.tag_add('sel', '1.0', '1.0 lineend')
        xstr.event_generate('<Key-greater>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith(' '), True)
        xstr.event_generate('<Key-greater>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith('  3'), True)

        xstr.tag_add('sel', '1.0', '1.0 lineend')
        xstr.event_generate('<Key-less>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith(' 3'), True)
        xstr.tag_add('sel', '1.0', '1.0 lineend')

        xstr.event_generate('<Key-less>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith('3'), True)

        xstr.insert('end', '413 412 942 414\n')
        xstr.insert('end', '913 512 442 211\n')

        xstr.tag_add('sel', '1.0', '2.0 lineend')
        xstr.event_generate('<Key-greater>')
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith(' '), True)

        xstr.tag_add('sel', '1.0', '2.0 lineend')
        xstr.event_generate('<Key-greater>')
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith('  '), True)

        xstr.tag_add('sel', '1.0', '2.0 lineend')
        xstr.event_generate('<Key-less>')
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith(' '), True)

        xstr.tag_add('sel', '1.0', '2.0 lineend')
        xstr.event_generate('<Key-less>')
        root.update() 

        for ind in range(0, 2):
            self.assertEqual(xstr.get('%s.0' % ind, 
                '%s.0 lineend' % ind).startswith('  '), False)

        xstr.tag_add('sel', '1.0', '1.0 lineend')
        xstr.event_generate('<Key-greater>')

        xstr.tag_add('sel', '3.0', '3.0 lineend')
        xstr.event_generate('<Key-greater>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith(' '), True)

        self.assertEqual(xstr.get('3.0', 
            '3.0 lineend').startswith(' '), True)


        xstr.tag_add('sel', '1.0', '1.0 lineend')
        xstr.event_generate('<Key-less>')

        xstr.tag_add('sel', '3.0', '3.0 lineend')
        xstr.event_generate('<Key-less>')
        root.update() 

        self.assertEqual(xstr.get('1.0', 
            '1.0 lineend').startswith(''), True)
        root.update() 

        self.assertEqual(xstr.get('3.0', 
            '3.0 lineend').startswith(''), True)
