
from cspkg.core import Command
from os.path import splitext
from cspkg.start import root
from cspkg.core import Plugin, Namespace, Main
from cspkg.plugins.insert_mode import Insert

class TabSpacingNS(Namespace):
    pass

class TabSpacing(Plugin):
    scheme = {}

    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(TabSpacingNS, Main, '<<LoadData>>', self.set_scm, True)
        self.add_kmap(TabSpacingNS, Main, '<<SaveData>>', self.set_scm, True)
        self.add_kmap(TabSpacingNS, Insert, '<Tab>',  self.insert_tabchar)
    
    def set_scm(self, event):
        ph, ext    = splitext(self.xstr.filename.lower())
        # When no '' default is specified it uses size = 4 and char = ' '.
        size, char = self.scheme.get(ext, self.scheme.get('', (4, ' ')))

        self.xstr.settab(size, char)

    def insert_tabchar(self, event):
        self.xstr.indent()
        return 'break'

    @classmethod
    def set_scheme(cls, scheme={}):
        cls.scheme.update(scheme)

@Command()
def tabset(xstr, size, char):
    """
    """

    ph, ext = splitext(xstr.filename.lower())
    Tab.scheme[ext] = size, char 
    xstr.tabsize = size
    xstr.tabchar = char
    root.status.set_msg('Tab size:char:%s:%s' % (size, repr(char)))

install = TabSpacing

