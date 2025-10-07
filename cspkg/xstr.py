from re import escape
from tkinter import TclError
from tkinter import Text, IntVar
import os

class Xstr(Text):
    homedir   = ''
    def __init__(self, default_filename, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self.default_filename = default_filename
        self.filename  = os.path.abspath(default_filename)
        self.extension = os.path.splitext(self.filename)

        self.charset  = 'utf-8'
        self.project  = ''
        self.mark_set('(LC)', '1.0')
        self.tabchar = ' '
        self.tabsize = 4
        self.project  = ''

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

    def save_data_as(self, filename):
        """
        """

        self.filename = filename
        self.save_data()

    def save_data(self):
        """
        """
        _, self.extension = os.path.splitext(self.filename)
        self.event_generate('<<Pre-SaveData>>')
        self.event_generate('<<Pre-Save/*%s>>' % self.extension)

        data = self.get('1.0', 'end -1c')
        data = data.encode(self.charset)
        fd   = open(self.filename, 'wb')
        fd.write(data)
        fd.close()
        self.event_generate('<<SaveData>>')
        self.event_generate('<<Save/*%s>>' % self.extension)

    def replace_ranges(self, name, regex, data, exact=False, 
        regexp=True, nocase=False, elide=False, nolinestop=False):
        """
        """
    
        count = 0
        while True:
            map = self.tag_nextrange(name, '1.0', 'end')
            if map == (): 
                return count
            self.tag_remove(name, *map)
    
            inc = self.replace_all(regex, data, map[0], map[1], 
                    exact, regexp, nocase, elide, nolinestop)
            count = count + inc
        return count

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

    def clear_selection(self):
        """
        Unselect all text.
        """

        try:
            self.tag_remove('sel', 
                'sel.first', 'sel.last')
        except Exception:
            pass

    def check_ranges(self, name, regex, index='1.0', 
        stopindex='end', exact=False, regexp=True, nocase=False, 
        elide=False, nolinestop=False):
        """
        """
        
        map = self.tag_ranges(name)
        for indi in range(0, len(map) - 1, 2):
            seq = self.find(regex, map[indi], map[indi + 1], 
                exact=exact, regexp=regexp, nocase=nocase, 
                    elide=elide, nolinestop=nolinestop)
            yield from seq
    
    def isearch(self, pattern, index, stopindex='end', forwards=None,
        backwards=None, exact=None, regexp=None, nocase=None,
        count=None, elide=None, nolinestop=None):

        """
        Just AreaVi.search shortcut, in the sense it return the matched chunk
        the initial position and the end position.
        """
        count = IntVar()
        index = self.search(pattern, index, stopindex, 
        forwards, backwards, exact, regexp, nocase, count=count,
        elide=elide, nolinestop=nolinestop)

        if not index: return 

        len   = count.get()
        tmp   = '%s +%sc' % (index, len)
        chunk = self.get(index, tmp)

        pos0  = self.index(index)
        pos1  = self.index('%s +%sc' % (index, len))

        return chunk, pos0, pos1

    def replace_all(self, regex, data, index='1.0', stopindex='end', 
        exact=None, regexp=True, nocase=None, elide=None, nolinestop=None):
        """
        """
        matches = self.find(regex, index, stopindex, exact=exact, 
        regexp=regexp, nocase=nocase, elide=elide, nolinestop=nolinestop)
        count = 0

        for xstr, pos0, pos1 in matches:
            if callable(data):
                self.swap(data(xstr, pos0, pos1), pos0, pos1)
            else:
                self.swap(data, pos0, pos1)
            count = count + 1
        return count

    def search(self, pattern, index, stopindex='end', forwards=None,
        backwards=None, exact=None, regexp=None, nocase=None,
        count=None, elide=None, nolinestop=None):
            
        """
        """
    
        args = [self._w, 'search']
        if forwards: args.append('-forwards')
        if backwards: args.append('-backwards')
        if exact: args.append('-exact')
        if regexp: args.append('-regexp')
        if nocase: args.append('-nocase')
        if elide: args.append('-elide')
        if nolinestop: args.append("-nolinestop")
        if count: args.append('-count'); args.append(count)
        if pattern and pattern[0] == '-': args.append('--')
        args.append(pattern)
        args.append(index)
        if stopindex: args.append(stopindex)
    
        return str(self.tk.call(tuple(args)))

    def clear_data(self):
        """
        It clears all text inside an AreaVi instance.
        """
        
        self.delete('1.0', 'end')
        self.filename = os.path.abspath(self.default_filename)
        self.event_generate('<<ClearData>>')

    def rmsel(self, index0, index1):
        """
        It removes the tag sel from the range that is delimited by index0 and index1
        regardless whether index0 <= index1.
        """

        index2 = self.min(index0, index1)
        index3 = self.max(index0, index1)

        self.tag_remove('sel', index2, index3)

    def addsel(self, index0, index1):
        """
        It adds the tag sel to the range delimited by index0 and index1 regardless
        whether index0 <= index1.
        """

        index2 = self.min(index0, index1)
        index3 = self.max(index0, index1)

        self.tag_add('sel', index2, index3)

    def ipick(self, name, regex, index='insert', stopindex='end', 
        verbose=False, backwards=False, exact=False, regexp=True, 
        nocase=False, elide=False, nolinestop=False):

        """
        """

        # Force to do a search from index.
        if verbose is True: 
            self.tag_remove(name, '1.0', 'end')
        if backwards is False: 
            ranges = self.tag_nextrange(name, index, 'end')
        else: 
            ranges = self.tag_prevrange(name, index, '1.0')

        if ranges: 
            index0, index1 = ranges[:2]
        else: 
            index0 = index1 = index

        index = self.isearch(regex, index=index0 if backwards else index1, 
        stopindex=stopindex, backwards=backwards, exact=exact, regexp=regexp, 
        nocase=nocase, elide=elide, nolinestop=nolinestop)

        if not index: 
            return None
        _, start, end = index

        self.mark_set('insert', start if backwards else end)
        self.see('insert')

        self.tag_remove(name, '1.0', 'end')
        self.tag_add(name, start, end)
        return start, end

    def replace(self, regex, data, index=None, stopindex=None,  
        forwards=None, backwards=None, exact=None, regexp=True, 
        nocase=None, elide=None, nolinestop=None):

        """
        """
        if not regex: 
            raise TypeError('Regex should be non blank!')

        count = IntVar()

        index = self.search(regex, index, stopindex, forwards=forwards, 
        backwards=backwards, exact=exact, nocase=nocase,  nolinestop=nolinestop, 
        regexp=regexp, elide=elide, count=count)
            
        if not index:  
            return None

        index0 = self.index('%s +%sc' % (index, count.get()))

        if callable(data): 
            data = data(self.get(index, index0), index, index0)
        
        self.delete(index, index0)
        self.insert(index, data)
        
        return index, len(data)

    def find(self, regex, index='1.0', stopindex='end', 
        backwards=False, exact=False, regexp=True, nocase=False, 
        elide=False, nolinestop=False, step=''):

        """
        """
        if not regex: 
            raise TclError('Regex is blank!')
        self.mark_set('(FIND-POS)', index)

        while True:
            count = IntVar()
            index = self.search(regex, '(FIND-POS)', stopindex, 
                None, backwards, exact, regexp, nocase, count=count,
                    elide=elide, nolinestop=nolinestop)

            if not index: 
                return None
            len  = count.get()
            pos0 = self.index(index)
            pos1 = self.index('%s +%sc' % (index, len))
            data = self.get(pos0, pos1)

            self.mark_set('(FIND-POS)', 
            index if len and backwards else (
                pos1 if len else (('%s -1c'  
                    if backwards else '%s +1c') % pos1)))

            if step != '':
                self.mark_set('(FIND-POS)',
                    '%s %s' % (self.index('(FIND-POS)'), step))
            yield(data, pos0, pos1)

    def swap(self, data, index0, index1):
        """
        Swap the text in the range index0, index1 for data.
        """

        self.delete(index0, index1)
        self.insert(index0, data)

    def cpsel(self, sep=''):
        """
        Copy selected text to the clipboard.
        """

        data = self.join_ranges('sel', sep)
        self.clipboard_clear()
        self.clipboard_append(data)
        self.tag_remove('sel', 'sel.first', 'sel.last')

    def swap_ranges(self, name, data, index='1.0', stopindex='end'):
        """
        """

        count = 0
        self.mark_set('(SWAP)', index)

        while True:
            range = self.tag_nextrange(
                name, '(SWAP)', stopindex)

            if len(range) == 0: 
                return count

            self.mark_set('(SWAP)', range[1])
            self.swap(data, *range)
            count = count + 1

    def join_ranges(self, name, sep=''):
        """     
        """

        data = ''
        ranges = self.tag_ranges(name)
        for ind in range(0, len(ranges) - 1, 2):
            data += self.get(ranges[ind], ranges[ind + 1]) + sep
        return data

    def ctsel(self, sep=''):
        """
        It cuts the selected text.
        """

        data = self.join_ranges('sel', sep)
        self.clipboard_clear()
        self.clipboard_append(data)
        self.edit_separator()
        self.swap_ranges('sel', '', '1.0', 'end')

    def settab(self, tabsize, tabchar):
        self.tabchar = tabchar
        self.tabsize = tabsize

    def indent(self):
        self.edit_separator()
        self.insert('insert', self.tabchar * self.tabsize)

    def tag_toggle(self, name, index0, index1):
        """
        """

        index2 = index0
        index0 = self.min(index0, index1)
        index1 = self.max(index2, index1)

        if self.range_in(name, index0, index1):
            self.tag_remove(name, index0, index1)
        else:
            self.tag_add(name, index0, index1)

    def range_in(self, name, index0, index1):
        """
        """ 
        ranges = self.tag_ranges(name)
        for ind in range(0, len(ranges) - 1, 2):
            if self.index_in(index0, 
                    ranges[ind].string, ranges[ind + 1].string):
                if self.index_in(index1, 
                    ranges[ind].string, ranges[ind + 1].string):
                        return ranges[ind].string, ranges[ind + 1].string

    def index_in(self, index, index0, index1):
        """
        It returns True if index0 <= index <= index1 otherwise
        it returns False.
        """

        index2 = self.min(index0, index1)
        index3 = self.max(index0, index1)

        r1 = self.compare(index2, '<=', index)
        r2 = self.compare(index3, '>=', index)

        return r1 and r2

    def word_bounds(self, index='insert'):
        index1 = self.search('\W', index, regexp=True, 
        stopindex='%s linestart' % index, backwards=True)

        index2 = self.search('\W', index, regexp=True, 
        stopindex='%s lineend' % index)

        index1 = '%s linestart' % index if not index1 else '%s +1c' % index1
        index2 = '%s lineend' % index if not index2 else index2
        return index1, index2

    def seq_bounds(self, index='insert'):
        index1 = self.search(' ', index, regexp=True,
        stopindex='%s linestart' %index, backwards=True)

        index2 = self.search(' ', index, regexp=True, 
        stopindex='%s lineend' % index)

        index1 = '%s linestart' % index if not index1 else '%s +1c' % index1
        index2=  '%s lineend' % index if not index2 else index2
        return index1, index2

    @staticmethod
    def find_all(wid, regex, index='1.0', stopindex='end', *args, **kwargs):
        """
        """

        for indi in Xstr.xstr_widgets(wid):
            it = indi.find(regex, index, stopindex, *args, **kwargs)
    
            for indj in it:
                yield indi, indj

    def bck_check(self, lhs, rhs, index, max, backwards=False):
        """
        """

        sign  = '-' if backwards else '+'
        count = 0
        regex = '|'.join((escape(lhs), escape(rhs)))

        matches = self.find(regex, index, '%s %s%sc' % (
            index, sign, max), backwards, regexp=True)
        for data, pos0, pos1 in matches:
            count = count + (1 
                if data == lhs else -1)
            if count == 0: 
                return pos0, pos1

    def append(self, data, *args):
        """
        """

        # This is sort of odd, it seems that
        # i have to add -1l for it to work.
        # It shouldn't be necessary.
        index0 = self.index('end -1l')
        self.insert('end', data)

        for ind in args:
            self.tag_add(ind, index0, 'end -1c')

        # self.mark_set('insert', 'end')
        self.see('insert')

    def get_line(self, index='insert'):
        return self.get('%s linestart' % index, 
        '%s lineend' % index)

