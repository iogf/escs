
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

        self.add_kmap(TabSpacingNS, 
        Main, '<<LoadData>>', self.update_tabtsize, True)

        self.add_kmap(TabSpacingNS, 
        Main, '<<SaveData>>', self.update_tabtsize, True)

        self.add_kmap(TabSpacingNS, Insert, '<Tab>',  
        lambda event: self.xstr.indent())
    
    def update_tabtsize(self, event):
        path, extension = splitext(self.xstr.filename.lower())

        # When no '' default is specified it uses size = 4 and char = ' '.
        size, char = self.scheme.get(extension, 
        self.scheme.get('', (4, ' ')))

        self.xstr.settab(size, char)

    @classmethod
    def c_tabsize(cls, scheme={}):
        cls.scheme.update(scheme)

@Command()
def tabset(xstr, size, char):
    """
    """

    path, extension = splitext(xstr.filename.lower())
    TabSpacing.scheme[extension] = size, char 
    xstr.tabsize = size
    xstr.tabchar = char
    root.status.set_msg('Tab size:char:%s:%s' % (size, repr(char)))

install = TabSpacing

