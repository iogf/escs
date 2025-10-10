from cspkg.start import root
from tkinter import TclError
from cspkg.core import Namespace, Plugin, Main, Mode
from cspkg.plugins.normal_mode import Normal

class XleapsNS(Namespace):
    pass

class Drop(Mode):
    pass

class Jump(Mode):
    pass

class Xleaps(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(XleapsNS, Main, '<Alt-bracketright>', self.jump_mode)
        self.add_kmap(XleapsNS, Main, '<Alt-bracketleft>', self.drop_mode)
        self.add_kmap(XleapsNS, Drop, '<Key>', self.drop)
        self.add_kmap(XleapsNS, Jump, '<Key>', self.jump)

    def jump_mode(self, event):
        self.chmode(Jump)
        root.status.set_msg('Jump to:')

    def drop_mode(self, event):
        self.chmode(Drop)
        root.status.set_msg('Drop on:')

    def drop(self, event):
        self.xstr.mark_set('(Xleaps-%s)' % event.keysym, 'insert')
        index = self.xstr.index('insert')
        root.status.set_msg('Droped: (%s) at %s' % (event.keysym, index))
        self.chmode(Normal)

    def jump(self, event):
        index = '(Xleaps-%s)' % event.keysym

        try:
            self.xstr.mark_set('insert', index)
        except TclError as error:
            root.status.set_msg('Bad index: (%s)' % event.keysym)
        else:
            root.status.set_msg('Jumped: (%s)' % event.keysym)
        self.xstr.see('insert')
        self.chmode(Normal)

install = Xleaps