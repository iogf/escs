"""
"""

from os.path import expanduser, join
from cspkg.fwin import OptionWindow
from cspkg.core import Plugin, Namespace
from cspkg.plugins.normal_mode import Normal
from tkinter import ACTIVE
from cspkg.scan import Scan
from re import split
from cspkg.start import root
import sqlite3

class CodeSnippetNS(Namespace):
    pass

class SnippetPicker(OptionWindow):
    def __init__(self, conn, cur):
        self.cur  = cur
        self.conn = conn
        OptionWindow.__init__(self)

        self.listbox.bind('<Return>', self.read_snippet)
        self.listbox.bind('<Key-d>', self.delete)

    def extend(self, options=[]):
        options = zip(map(lambda ind: ind[1], options),
        map(lambda ind: (ind[0], ind[2]), options))
        options = list(options)
        super().extend(options)
        print(options)

    def read_snippet(self, event):
        index   = self.listbox.index(ACTIVE)
        snippet = self.options[index][1][1]

        self.xstr.insert('insert', snippet)
        self.xstr.see('insert')
        root.status.set_msg('Snippet: %s!' % self.options[index][0])

        self.close()

    def delete(self, event):
        index   = self.listbox.index(ACTIVE)
        values = (self.options[index][1][0],)

        self.cur.execute('''DELETE FROM snippet where id=?''', values)
        self.conn.commit()
        root.status.set_msg('Snippet deleted!')
        self.listbox.delete(index)
        
        # Otherwise it gets messed up.
        del self.options[index]

class CodeSnippet(Plugin):
    nocas   = True
    db_name = join(expanduser('~'), '.ysnippet.db')
    conn    = sqlite3.connect(db_name)
    cur     = conn.cursor()
    picker  = SnippetPicker(conn, cur)

    def __init__(self, xstr):
        """

        """

        super().__init__(xstr)

        self.add_kmap(CodeSnippetNS, Normal, '<Control-r>', self.ask_title)
        self.add_kmap(CodeSnippetNS, Normal, '<Control-e>', self.reload)
        self.add_kmap(CodeSnippetNS, Normal, '<Control-f>', self.ask_pattern)

        # Create table
        self.cur.execute('''CREATE TABLE if not exists 
        snippet (id integer PRIMARY KEY, title text, data text);''')

    def ask_title(self, event):
        root.status.set_msg('Snippet title:')
        scan = Scan()

        self.store(scan.data)

    def ask_pattern(self, event):
        root.status.set_msg('Snippet pattern:')
        scan = Scan()

        self.find(scan.data)

    def store(self, data):
        """
        In order to update a snippet it has to contain
        a field @(id)
        """

        values = (data, self.xstr.join_ranges('sel', '\n'))

        self.xstr.tag_remove('sel', 'sel.first', 'sel.last')
        
        self.cur.execute('''INSERT INTO snippet 
        (title, data) VALUES (?, ?)''', values)

        self.conn.commit()

        root.status.set_msg('Snippet saved!')

    def find(self, data):
        """
        """
        
        matches = self.build_sql(data)

        if not len(matches):
            root.status.set_msg('No snippet found')
        else:
            self.choices(matches)

    def build_sql(self, pattern):
        tmp = '(title LIKE ? or data LIKE ?)'
        chks = split(' *\+ *', pattern)

        attrs = ['%' + '%s' % indi + '%' for indi in chks
            for indj in range(0, 2)]

        sql = "SELECT * FROM snippet WHERE %s" % ' and '.join([tmp] * len(chks))

        self.cur.execute(sql, attrs)
        matches = self.cur.fetchall()
        return matches

    def reload(self, event):
        self.picker.display(self.xstr)

    def choices(self, matches):
        root.status.set_msg('Found snippets!')
        self.picker.extend(matches)
        self.picker.display(self.xstr)

install = CodeSnippet

