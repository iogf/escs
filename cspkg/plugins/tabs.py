from cspkg.start import root
# from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
from cspkg.core import Namespace, Main, Plugin, Command
from cspkg.plugins.normal_mode import Normal
from cspkg.xstr import Xstr

class TabsNS(Namespace):
    pass

@Command('ot')
def load_tab(xstr, filename):
    """
    """

    root.note.load([[filename]])
    root.status.set_msg('Loaded %s' % filename)

class Tabs(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(TabsNS, Main, 
        '<Alt-E>', self.load_tab)

        self.add_kmap(TabsNS, Main, 
        '<Alt-R>', self.create_tab)

        self.add_kmap(TabsNS, Main, 
        '<Alt-x>', self.remove_tab)

        self.add_kmap(TabsNS, Main, 
        '<Alt-o>', self.select_left)

        self.add_kmap(TabsNS, Main, 
        '<Alt-p>', self.select_right)

    def load_tab(self, event):
        """
        """
    
        filename = askopenfilename()
    
        if not filename: 
            return None
    
        try:
            root.note.load([[filename]])
        except Exception:
            root.status.set_msg('It failed to load.')
        else:
            root.status.set_msg('File loaded.')
        self.chmode(Normal)

    def create_tab(self, event):
        root.note.create('none')
        self.chmode(Normal)
    
    def remove_tab(self, event):
        """
        It removes the selected tab.
        """
    
        tabs = root.note.tabs() 
        count = len(tabs) 

        if count <= 1: 
            return None

        name = root.note.select()
        wid  = root.note.nametowidget(name)
        wid.destroy()
        root.note.select(0)

        wid  = root.note.nametowidget(root.note.select())
        seq  = Xstr.xstr_widgets(wid)
        xstr = next(seq)
        wid.tab_xstr.focus_set()
    
        # We don't need to call forget after destroy.
        # It seems the method forget from note doesnt destroy
        # the widget at all consequently the event <Destroy> isn't
        # spreaded.
        # root.note.forget(wid)
    
    def select_left(self, event):
        """
        """
    
        root.note.select(root.note.index(root.note.select()) - 1)
        wid  = root.note.nametowidget(root.note.select())
        wid.tab_xstr.focus_set()
    
    def select_right(self, event):
        """
        """
    
        root.note.select(root.note.index(root.note.select()) + 1)
        wid  = root.note.nametowidget(root.note.select())
        wid.tab_xstr.focus_set()

install = Tabs
