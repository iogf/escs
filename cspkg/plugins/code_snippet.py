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
    def __init__(self, conn, cursor):
        self.cursor  = cursor
        self.conn = conn
        OptionWindow.__init__(self)

        self.listbox.bind('<Return>', self.fetch_snippet)
        self.listbox.bind('<Key-d>', self.delete)

    def fetch_snippet(self, event):
        index   = self.listbox.index(ACTIVE)
        elem_id = self.options[index][1]

        query = f"SELECT data FROM snippet WHERE id = ?"
        self.cursor.execute(query, (elem_id,))
        elem = self.cursor.fetchone()

        if not elem:
            root.status.set_msg('Unavailable snippet!')
        else:
            self.create_tab(self.options[index][0], elem[0])
        self.close()

    def create_tab(self, title, data):
        xstr = root.note.create(title[0:8])

        xstr.insert('insert', data)
        xstr.see('insert')
        root.note.select(xstr.master.master.master)

    def delete(self, event):
        index   = self.listbox.index(ACTIVE)
        values = (self.options[index][1],)

        self.cursor.execute('''DELETE FROM snippet where id=?''', values)
        self.conn.commit()
        root.status.set_msg('Snippet deleted!')
        self.listbox.delete(index)
        
        # Otherwise it gets messed up.
        del self.options[index]

class CodeSnippet(Plugin):
    nocas   = True
    db_name = join(expanduser('~'), '.ysnippet.db')
    conn    = sqlite3.connect(db_name)
    cursor     = conn.cursor()
    picker  = SnippetPicker(conn, cursor)

    def __init__(self, xstr):
        """

        """

        super().__init__(xstr)

        self.add_kmap(CodeSnippetNS, Normal, '<Control-r>', self.ask_title)
        self.add_kmap(CodeSnippetNS, Normal, '<Control-e>', self.reload)
        self.add_kmap(CodeSnippetNS, Normal, '<Control-f>', self.ask_pattern)

        # Create table
        self.cursor.execute('''CREATE TABLE if not exists 
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
        
        self.cursor.execute('''INSERT INTO snippet 
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

        sql = "SELECT title, id FROM snippet WHERE %s" % ' and '.join([tmp] * len(chks))

        self.cursor.execute(sql, attrs)
        matches = self.cursor.fetchall()
        return matches

    def reload(self, event):
        self.picker.display(self.xstr)

    def choices(self, matches):
        root.status.set_msg('Found snippets!')
        self.picker.extend(matches)
        self.picker.display(self.xstr)

install = CodeSnippet

