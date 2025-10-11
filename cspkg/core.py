from os.path import expanduser, join, exists, dirname
from untwisted.tkinter import extern
from cspkg.stderr import printd
from tkinter import Tk, Grid
from functools import wraps
from cspkg.cmdout import CmdOut
from cspkg.nbook import EscsBook
from shutil import copyfile
from functools import wraps
from os import mkdir
from os.path import basename

rcenv = dict()
rcmod = list()
kscheme = dict()

def load_module(module, *args, **kwargs):
    rcmod.append((module.install, args, kwargs))

def load_cls(handle, *args, **kwargs):
    rcmod.append((handle, args, kwargs))

class Namespace(tuple):
    def __new__(self):
        return tuple.__new__(Namespace, 
            (Namespace.__module__, Namespace.__name__))

class CoreNS(Namespace):
    pass

class Mode(tuple):
    EDIT = False

    def __new__(self):
        return tuple.__new__(Namespace, 
            (Namespace.__module__, Namespace.__name__))

class Main(Mode):
    pass

def mkwrapper(handle):
    def handle_caller(event):
        handle(event)
        return 'break'
    return handle_caller

class Plugin:
    def __init__(self, xstr):
        self.xstr = xstr
        self.mode = None

    def flush_kmap(self, mode, seq):
        """
        """
        code = 'MODE:%s:%s' % (self.xstr, mode.__name__)
        self.xstr.unbind_class(code, seq)

    def add_kmap(self, namespace, mode, seq, handle, 
        spread=False, add=True):
        """
        """

        if spread is False:
            handle = mkwrapper(handle)

        data = kscheme.setdefault(namespace, 
        {(mode, seq):((mode, seq), )})
        for mode, seq in data.setdefault((mode, seq), ((mode, seq), )):
            self.hook_class(mode, seq, handle, spread, add)

    def hook_class(self, mode, seq, handle, 
        spread=False, add=True):
        code = 'MODE:%s:%s' % (self.xstr, mode.__name__)

        if self.xstr.bind_class(code, seq):
            printd('Warning: %s %s already binded!' % (mode, seq))
        self.xstr.bind_class(code, seq, handle, add)

    def chmode(self, mode):
        code0 = 'MODE:%s:%s' % (self.xstr, Main.__name__)
        code1 = 'MODE:%s:%s' % (self.xstr, mode.__name__)

        taglist = [code0, code1, self]
        if mode.EDIT is True:
            taglist.append('Text')
        taglist.append('.')
        self.xstr.bindtags(taglist)
        self.mode = mode
        self.xstr.event_generate('<<Chmode>>')

def chkmap(namespace, kmap):
    kscheme[namespace] = kmap

class EscsApp(Tk):
    def __init__(self, *args, **kwargs):
        """
        """

        Tk.__init__(self, *args, **kwargs)
        self.note   = None
        self.status = None
        self.title('Escs')
        self.create_widgets()
        
    def create_escsrc(self):
        self.dir = join(expanduser('~'), '.escs')
        self.rc  = join(self.dir, 'escsrc')
        
        if not exists(self.dir):
            mkdir(self.dir)
        
        if not exists(self.rc):
            copyfile(join(dirname(__file__), 'escsrc'), self.rc)
        exec(compile(open(self.rc).read(), self.rc, 'exec'), rcenv)

    def create_widgets(self):
        self.note = EscsBook(master=self, takefocus=0)
        self.note.grid(row=0, sticky='wens')

        self.status = CmdOut(master=self)
        self.status.grid(row=2, sticky='we')
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

class Command:
    xstr = None
    def __init__(self, name=None):
        self.name = name

    def __call__(self, handle):
        name = self.name if self.name else handle.__name__
        @wraps(handle)
        def wrapper(*args, **kwargs):
            return handle(Command.xstr, *args, **kwargs)
        rcenv[name] = wrapper
        return wrapper

    @classmethod
    def set_target(cls, xstr):
        cls.xstr = xstr

class TopbarStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(CoreNS, Main, 
        '<FocusIn>', self.update_title, True)

        self.add_kmap(CoreNS, Main, 
        '<<LoadData>>', self.update_title, True)

        self.add_kmap(CoreNS, Main, 
        '<<SaveData>>', self.update_title, True)

    def update_title(self, event):
        root = self.xstr.winfo_toplevel()
        root.title('Escs %s' % self.xstr.filename)

class InstallReactor(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        root = self.xstr.winfo_toplevel()
        extern(root)

class ModeStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(CoreNS, Main, '<<Chmode>>', self.update_mode, True)
        self.add_kmap(CoreNS, Main, '<FocusIn>', self.update_mode, True)

    def update_mode(self, event):
        root = self.xstr.winfo_toplevel()
        mode = self.xstr.bindtags()
        mode = mode[1].rsplit(':')
        mode = mode[-1].rsplit('.')
        root.status.set_mode(mode[-1])

class CursorStatus(Plugin):
    def __init__(self, xstr, timeout=1000):
        super().__init__(xstr)

        self.timeout = timeout
        self.funcid  = None
        self.add_kmap(CoreNS, Main, '<FocusIn>', 
        lambda event: self.update(), True)

        self.add_kmap(CoreNS, Main, '<FocusOut>', 
        lambda event: self.xstr.after_cancel(self.funcid), True)

    def update(self):
        """
        It is used to update the line and col statusbar 
        in TIME interval.
        """
        root = self.xstr.winfo_toplevel()

        row, col = self.xstr.indexsplit('insert')
        root.status.set_line(row)
        root.status.set_column(col)
        self.funcid = self.xstr.after(self.timeout, self.update)

class TabStatus(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(CoreNS, Main, 
        '<FocusIn>', self.update_tabname, True)

        self.add_kmap(CoreNS, Main, 
        '<<SaveData>>', self.update_tabname, True)

        self.add_kmap(CoreNS, Main, 
        '<<LoadData>>', self.update_tabname, True)

    def update_tabname(self, event):
        root = self.xstr.winfo_toplevel()

        root.note.tab(self.xstr.master.master.master,
        text=basename(self.xstr.filename))

rcmod.extend(((TopbarStatus, (), {}), (ModeStatus, (), {}), 
(CursorStatus, (), {}), (TabStatus, (), {}), (InstallReactor, (), {})))

