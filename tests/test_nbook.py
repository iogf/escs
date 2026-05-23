from cspkg.start import root
from cspkg.core import TabStatus
from cspkg.xstr import Xstr
from os.path import join, expanduser, basename
import tempfile
import os
import unittest

class TestEscsBook(unittest.TestCase):
    def test0(self):
        xstr = root.note.create('Test0')
        root.note.select(xstr.master.master.master)

        tab_name = root.nametowidget(xstr.master.master.master)
        root.update()
        self.assertEqual(root.note.tab(tab_name, 'text'), 'Test0')
        root.note.forget(0)

    def test1(self):
        file = tempfile.NamedTemporaryFile()

        xstr = root.note.open(file.name)
        root.note.select(xstr.master.master.master)

        tab_name = root.nametowidget(xstr.master.master.master)
        root.update()
        self.assertEqual(root.note.tab(tab_name, 'text'), basename(file.name))
        file.close()
        root.note.forget(0)

    def test2(self):
        """
        Create 2 tabs with 2 panes each ones. Each tab contains three files.
        It uses named temporary files to test loading files into Xstr's instances.

        When the files are loaded it asserts it has loaded the files correctly
        according to the layout that was specified in the list of files.

        [...tabs...[...vertical panes...[...horizontal panes...]]]     
        """

        file0 = tempfile.NamedTemporaryFile()
        file1 = tempfile.NamedTemporaryFile()
        file2 = tempfile.NamedTemporaryFile()
        file3 = tempfile.NamedTemporaryFile()
        file4 = tempfile.NamedTemporaryFile()
        file5 = tempfile.NamedTemporaryFile()

        files0 = [[[file0.name, file1.name], [file2.name]], 
        [[file3.name], [file4.name, file5.name]]]
        root.note.load(*files0)
        root.update()

        self.assertEqual(root.note.tab(0, 'text'), 
        basename(file2.name))
        root.update()

        self.assertEqual(root.note.tab(1, 'text'), 
        basename(file5.name))

        tabs = root.note.tabs()
        tab0 = root.nametowidget(tabs[0])
        hpanes0 = [root.nametowidget(ind) 
        for ind in tab0.panes()]

        frames0 = [root.nametowidget(ind) 
        for ind in hpanes0[0].panes()]

        xinsts0 = [indj for indi in frames0
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]
        root.update()

        self.assertEqual(xinsts0[0].filename, file0.name)
        self.assertEqual(xinsts0[1].filename, file1.name)

        frames1 = [root.nametowidget(ind) 
        for ind in hpanes0[1].panes()]

        xinsts1 = [indj for indi in frames1
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]
        root.update()

        self.assertEqual(xinsts1[0].filename, file2.name)


        tab1 = root.nametowidget(tabs[1])
        hpanes0 = [root.nametowidget(ind) 
        for ind in tab1.panes()]

        frames0 = [root.nametowidget(ind) 
        for ind in hpanes0[0].panes()]

        xinsts0 = [indj for indi in frames0
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]
        root.update()

        self.assertEqual(xinsts0[0].filename, file3.name)

        frames1 = [root.nametowidget(ind) 
        for ind in hpanes0[1].panes()]

        xinsts1 = [indj for indi in frames1
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]
        root.update()

        self.assertEqual(xinsts1[0].filename, file4.name)
        self.assertEqual(xinsts1[1].filename, file5.name)
        file0.close()
        file1.close()
        file2.close()
        file3.close()
        file4.close()
        file5.close()
        
        # os.remove(file0.name)
        # os.remove(file1.name)
        # os.remove(file2.name)
        # os.remove(file3.name)
        # os.remove(file4.name)
        # os.remove(file5.name)

        # files1 = []
        # for indi in tabs:
            # vpane = root.nametowidget(indi)
            # for indj in vpane.panes():
                # hpane = root.nametowidget(indj)
                # for indz in hpane.panes():
                    # frame = root.nametowidget(indz)
                    # for indn in frame.winfo_children():
                        # if isinstance(indn, Xstr):
                            # files1.append(indn.filename)
# 
        # files2 = []
        # for indi in files0:
            # for indj in indi:
                # for indz in indj:
                    # files2.append(indz)
# 
        # self.assertEqual(files1, files2)

    def test3(self):
        xstr0 = root.note.create('Test1')
        xstr1 = root.note.create('Test2')
        xstr2 = root.note.create('Test3')
        xstr3 = root.note.create('Test4')
        lm0 = lambda data: 'a' in data

        tab_names0 = (root.note.tab(ind, 'text') 
        for ind in root.note.next(lm0))

        tab_names1 = ('Test1', 'Test2', 'Test3', 'Test4')
        self.assertTrue(tab_names0, tab_names1)

        root.note.select(1)
        lm1 = lambda data: 'ta' in data

        tab_names1 = (root.note.tab(ind, 'text') 
        for ind in root.note.next(lm1))

        tab_names2 = ('Test2', 'Test4')
        self.assertTrue(tab_names1, tab_names2)

    def test4(self):
        xstr0 = root.note.create('Test5')
        xstr1 = root.note.create('Test6')
        xstr2 = root.note.create('Test7')
        xstr3 = root.note.create('Test8')

        root.note.select(4)
        lm0 = lambda data: 'a' in data

        tab_names0 = (root.note.tab(ind, 'text') 
        for ind in root.note.next(lm0))

        tab_names1 = ('Test8', 'Test7', 'Test6', 'Test5')
        self.assertTrue(tab_names0, tab_names1)

        root.note.select(1)
        lm1 = lambda data: 'ta' in data

        tab_names1 = (root.note.tab(ind, 'text') 
        for ind in root.note.next(lm1))

        tab_names2 = ('Test8', 'Test6')
        self.assertTrue(tab_names1, tab_names2)

if __name__ == '__main__':
    unittest.main()
