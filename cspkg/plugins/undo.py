from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class UndoNS(Namespace):
    pass

class Undo(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(UndoNS, Normal, '<Key-bracketright>', 
        lambda event: event.widget.edit_undo())

        self.add_kmap(UndoNS, Normal, '<Key-bracketleft>', 
        lambda event: event.widget.edit_redo())

install = Undo
