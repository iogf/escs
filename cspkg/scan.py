
# from tkinter import *
from tkinter import Frame, Entry, BOTH
from cspkg.start import root
from cspkg.mixins import DataEvent, IdleEvent

class InputBox:
    def __init__(self, default_data='', complete_words=[]):
        self.default_data = default_data
        self.complete_words = complete_words

        self.xstr  = root.focus_get()
        self.frame = Frame(root, border=1, padx=3, pady=3)
        self.entry = Entry(self.frame)
        self.entry.config(background='grey')
        self.entry.focus_set()

        # Maybe there is a more elegant way.
        # self.entry.bind('<FocusOut>', lambda event: self.entry.focus_set())
        self.entry.bind('<Tab>', self.complete)

        self.entry.insert('end', default_data)
        self.entry.pack(side='left', expand=True, fill=BOTH)
        self.frame.grid(row=1, sticky='we')
        self.matches = None
        self.pattern = ''

    def init_completer(self, pattern):
        for ind in self.complete_words:
            if ind.startswith(pattern):
                yield(ind)

    def complete(self, event):
        data    = self.entry.get()
        index0  = self.entry.index('insert')
        index1  = data.rfind(' ', 0, index0) + 1
        index2  = data.find(' ', index0)
        index2  = index2 if index2 > -1 else len(data)
        pattern = data[index1:index2]

        if self.pattern != pattern or pattern == '':
            self.matches = self.init_completer(pattern)
        word = next(self.matches, '')

        # When there is no longer matches it deletes the cursor
        # pattern to restart again.
        self.entry.delete(index1, index2)
        self.entry.insert(index1, word)
        self.pattern = word
        return 'break'

    def done(self):
        self.entry.destroy()
        self.frame.destroy()
        # self.xstr.focus_set()
        root.note.focus_restore()

class Read(InputBox, DataEvent, IdleEvent):
    def __init__(self, events={}, default_data='', complete_words=[], msg=''):
        InputBox.__init__(self, default_data, complete_words)
        DataEvent.__init__(self, self.entry)
        IdleEvent.__init__(self, self.entry)

        self.entry.bindtags(('Entry', self.entry, '.', 'all'))
        for indi, indj in events.items():
            self.entry.bind(indi, lambda event, handle=indj: 
                        self.dispatch(handle) , add=True)
        root.status.set_msg(msg)

    def text(self, clear=False):
        data = self.entry.get()
        if clear is True:
            self.entry.delete(0, 'end')
        return data

    def dispatch(self, handle):
        handle(self)




