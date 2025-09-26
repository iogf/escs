from re import escape
from tkinter import TclError
from tkinter import Text, IntVar
import os

class Xstr(Text):
    def __init__(self, default_filename, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self.default_filename = default_filename
        self.filename  = os.path.abspath(default_filename)
        self.extension = os.path.splitext(self.filename)

        self.charset  = 'utf-8'
        self.project  = ''
        self.mark_set('(LC)', '1.0')

    def settab(self, tabsize, tabchar):
        self.tabchar = tabchar
        self.tabsize = tabsize

    def min(self, index0, index1):
        """
        """

        if self.compare(index0, '<=', index1):
            return index0
        else:
            return index1

    def max(self, index0, index1):
        """
        """

        if self.compare(index0, '<=', index1):
            return index1
        else:
            return index0

    @staticmethod
    def xstr_widgets(wid):
        """
        """

        for ind in wid.winfo_children():
            if isinstance(ind, Xstr):
                yield ind
            else:
                for ind in Xstr.xstr_widgets(ind):
                    yield ind

    @staticmethod
    def get_opened_files(wid):
        """
        """

        map = dict()
        for ind in Xstr.xstr_widgets(wid):
            map[ind.filename] = ind
        return map

    def decode(self, name):
        """
        """
        self.charset = name
        self.load_data(self.filename)

    def load_data(self, filename):
        """
        """

        self.filename     = os.path.abspath(filename)
        _, self.extension = os.path.splitext(self.filename)

        self.event_generate('<<Pre-LoadData>>')
        self.event_generate('<<Pre-LoadData/*%s>>' % self.extension)

        fd   = open(self.filename, 'rb')
        data = fd.read()
        fd.close()

        try:
            data = data.decode(self.charset)
        except UnicodeDecodeError:
            self.charset = ''

        self.delete('1.0', 'end')
        self.insert('end', data)
        self.mark_set('insert', '1.0')
        self.see('insert')

        self.event_generate('<<LoadData>>')
        self.event_generate('<<Load/*%s>>' % self.extension)


    def indexsplit(self, index='insert'):
        """ 
        """

        index = self.index(index)
        a, b = index.split('.')
        return int(a), int(b)

    def down(self):
        """  
        """

        a, b = self.indexsplit('(LC)')
        c, d = self.indexsplit()
        self.setcur(c + 1, b)        
    
    def up(self):   
        """  
        """

        a, b = self.indexsplit('(LC)')
        c, d = self.indexsplit()
        self.setcur(c - 1, b)
    
    def left(self):
        """  
        """

        self.mark_set('insert', 'insert -1c')
        self.mark_set('(LC)', 'insert')
    
    def right(self):
        """  
        It moves the cursor one character right.
        """

        self.mark_set('insert', 'insert +1c')
        self.mark_set('(LC)', 'insert')

    def setcur(self, line, col='0'):
        """
        """


        self.mark_set('insert', '%s.%s' % (line, col))
        self.see('insert')

    