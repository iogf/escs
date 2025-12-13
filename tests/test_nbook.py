from cspkg.start import root
from cspkg.core import TabStatus
from cspkg.xstr import Xstr
from os.path import join, expanduser, basename
import tempfile
import os
import unittest

class TestEscsBook(unittest.TestCase):
    def test0(self):
        self.xstr0 = root.note.create('test0')
        root.note.select(self.xstr0.master.master.master)

        tab_name = root.nametowidget(self.xstr0.master.master.master)
        self.assertEqual(root.note.tab(tab_name, 'text'), 'test0')
        root.note.forget(0)

    def test1(self):
        self.xstr2 = root.note.create('test1')
        root.note.select(self.xstr2.master.master.master)

        home = os.path.expanduser('~')
        filename = os.path.join(home, 'escs-tests')
        self.xstr2.insert('end', 'Escs tests\n')
        self.xstr2.save_data_as(filename)

        self.xstr3 = root.note.open(filename)
        root.note.select(self.xstr3.master.master.master)

        tab_name = root.nametowidget(self.xstr3.master.master.master)
        self.assertEqual(root.note.tab(tab_name, 'text'), 'escs-tests')
        root.note.forget(0)
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

        self.assertEqual(root.note.tab(0, 'text'), 
        os.path.basename(file2.name))

        self.assertEqual(root.note.tab(1, 'text'), 
        os.path.basename(file5.name))

        tabs = root.note.tabs()
        tab0 = root.nametowidget(tabs[0])
        hpanes0 = [root.nametowidget(ind) 
        for ind in tab0.panes()]

        frames0 = [root.nametowidget(ind) 
        for ind in hpanes0[0].panes()]

        xinsts0 = [indj for indi in frames0
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]

        self.assertEqual(xinsts0[0].filename, file0.name)
        self.assertEqual(xinsts0[1].filename, file1.name)

        frames1 = [root.nametowidget(ind) 
        for ind in hpanes0[1].panes()]

        xinsts1 = [indj for indi in frames1
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]

        self.assertEqual(xinsts1[0].filename, file2.name)


        tab1 = root.nametowidget(tabs[1])
        hpanes0 = [root.nametowidget(ind) 
        for ind in tab1.panes()]

        frames0 = [root.nametowidget(ind) 
        for ind in hpanes0[0].panes()]

        xinsts0 = [indj for indi in frames0
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]

        self.assertEqual(xinsts0[0].filename, file3.name)

        frames1 = [root.nametowidget(ind) 
        for ind in hpanes0[1].panes()]

        xinsts1 = [indj for indi in frames1
        for indj in indi.winfo_children() 
        if isinstance(indj, Xstr)]

        self.assertEqual(xinsts1[0].filename, file4.name)
        self.assertEqual(xinsts1[1].filename, file5.name)

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

if __name__ == '__main__':
    unittest.main()
