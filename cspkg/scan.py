
# from tkinter import *
from tkinter import Frame, Entry, BOTH
from cspkg.start import root
from cspkg.mixins import DataEvent, IdleEvent

class ScanCancel(Exception):
    pass

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
        self.entry.bind('<FocusOut>', lambda event: self.entry.focus_set())
        self.entry.bind('<Tab>', self.complete)

        self.entry.insert('end', default_data)
        self.entry.pack(side='left', expand=True, fill=BOTH)
        self.frame.grid(row=1, sticky='we')
        self.matches = None
        self.index = 0

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
        pattern = data[index1:index2].strip(' ')

        if self.index != index2:
            self.matches = self.init_completer(pattern)
        word = next(self.matches, '')

        # When there is no longer matches it deletes the cursor
        # pattern to restart again.
        self.entry.delete(index1, index2)
        self.entry.insert(index1, word)
        self.index  = self.entry.index('insert')

    def done(self):
        self.entry.destroy()
        self.frame.destroy()
        self.xstr.focus_set()

class Read(InputBox, DataEvent, IdleEvent):
    def __init__(self, events={}, default_data='', complete_words=[]):
        InputBox.__init__(self, default_data, complete_words)
        DataEvent.__init__(self, self.entry)
        IdleEvent.__init__(self, self.entry)

        self.entry.bindtags(('Entry', self.entry, '.', 'all'))
        for indi, indj in events.items():
            self.entry.bind(indi, lambda event, handle=indj: 
                        self.dispatch(handle) , add=True)

    def dispatch(self, handle):
        is_done = handle(self.entry)
        if is_done == True: 
            self.done()

class Scan(InputBox):
    """
    """

    def __init__(self, default_data ='', complete_words=[]):
        InputBox.__init__(self, default_data, complete_words)
        self.entry.bind('<Return>', lambda event: self.on_success())

        self.entry.bind('<Escape>', lambda event: self.cancel())
        self.data = None
        self.xstr.wait_window(self.frame)

        if self.data == None:
            raise ScanCancel('Canceled input!')

    def on_success(self):
        self.data = self.entry.get()
        InputBox.done(self)

    def cancel(self):
        """
        Called on <Escape>, the self.data attribute
        is set to None which means the user just canceled
        the action.
        """

        self.data = None
        InputBox.done(self)

    def __str__(self):
        return self.data

    __repr__ = __str__



