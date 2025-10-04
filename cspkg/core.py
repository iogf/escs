from os.path import expanduser, join, exists, dirname
from tkinter import Tk, Grid
from functools import wraps
from cspkg.cmdout import CmdOut
from cspkg.nbook import EscsBook
from shutil import copyfile
from functools import wraps
from os import mkdir

rcenv = dict()
rcmod = list()

def load_module(module, *args, **kwargs):
    rcmod.append((module.install, args, kwargs))

def load_cls(handle, *args, **kwargs):
    rcmod.append((handle, args, kwargs))

class Namespace(tuple):
    def __new__(self):
        return tuple.__new__(Namespace, 
            (Namespace.__module__, Namespace.__name__))

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
        self.kmaps = dict()
        self.mode = None

    def del_kmap(self, namespace, mode, seq, handle=None):
        """
        """
        pass

    def add_kmap(self, namespace, mode, seq, handle, 
        spread=False, add=True):
        """
        """

        code = 'MODE:%s:%s' % (self.xstr, mode.__name__)

        # if self.bind_class(code, seq):
            # printd('Warning: %s %s already binded!' % (mode, seq))
        if spread is False:
            handle = mkwrapper(handle)
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
        # self.xstr.event_generate('<<Chmode-%s>>' % mode.__name__)

def lsmap(namespace=None, mode=None, seqcode=None):
    """
    """
    pass

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


