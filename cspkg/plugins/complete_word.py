"""

"""

from cspkg.fwin import CompletionWindow, Option
from cspkg.start import root
from cspkg.core import Plugin, Namespace
from cspkg.plugins.insert_mode import Insert
from cspkg.plugins.extra_mode import Extra

class CompleteWordNS(Namespace):
    pass

class CompleteWordWindow(CompletionWindow):
    """
    """

    def __init__(self, xstr, *args, **kwargs):
        pattern     = xstr.get(*xstr.seq_bounds())
        completions = [ind[1][0] for ind in xstr.find_all(root, '[^ ]*%s[^ ]*' % pattern 
        if pattern else '[^ ]+', nocase=True)]

        completions = set(completions)
        completions = [Option(ind) for ind in completions]

        CompletionWindow.__init__(self, xstr, 
        completions, *args, **kwargs)

class CompleteWord(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(CompleteWordNS, Extra, '<Key-comma>', self.complete)

    def complete(self, event):
        CompleteWordWindow(event.widget)
        self.chmode(Insert)

install = CompleteWord
