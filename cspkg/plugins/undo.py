from cspkg.core import Namespace, Plugin, Normal

class UndoNS(Namespace):
    pass

class Undo(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(UndoNS, Normal, '<Key-q>', 
        lambda event: event.widget.edit_undo())

        self.add_kmap(UndoNS, Normal, '<Key-Q>', 
        lambda event: event.widget.edit_redo())

install = Undo
