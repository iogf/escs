
from cspkg.start import root
from cspkg.core import Namespace, Plugin, Mode
from cspkg.plugins.normal_mode import Normal

class SneakNS(Namespace):
    pass

class JumpNext(Mode):
    pass

class JumpBack(Mode):
    pass

def get_char(num):
    try:
        char = chr(num)
    except ValueError:
        return ''
    else:
        return char

class Sneak(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(SneakNS, Normal, '<Key-period>', self.next_mode)
        self.add_kmap(SneakNS, Normal, '<Key-comma>', self.back_mode)
        self.add_kmap(SneakNS, JumpBack, '<Key>', self.jump_back)
        self.add_kmap(SneakNS, JumpNext, '<Key>', self.jump_next)

    def next_mode(self, event):
        self.chmode(JumpNext)
        root.status.set_msg('Switched to JUMP_NEXT mode.')

    def back_mode(self, event):
        self.chmode(JumpBack)
        root.status.set_msg('Switched to JUMP_BACK mode.')

    def jump_next(self, event):
        char  = get_char(event.keysym_num)
        _, index0, index1 = self.xstr.isearch(char, index='insert', 
        stopindex='end', regexp=False)

        self.xstr.mark_set('insert', index1)
        self.xstr.see('insert')
        self.chmode(Normal)

    def jump_back(self, event):
        char  = get_char(event.keysym_num)
        _, index0, index1 = self.xstr.isearch(char, index='insert', 
        stopindex='1.0', regexp=False, backwards=True)

        self.xstr.mark_set('insert', index0)
        self.xstr.see('insert')
        self.chmode(Normal)

install = Sneak



