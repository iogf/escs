"""

"""

from cspkg.fwin import CompletionWindow, Option
from cspkg.start import root
from cspkg.core import Plugin, Namespace
from cspkg.plugins.insert_mode import Insert
from cspkg.plugins.extra_mode import Extra

class WordCompletionNS(Namespace):
    pass

class WordCompletionWindow(CompletionWindow):
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

class WordCompletion(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(WordCompletionNS, Extra, '<Key-comma>', self.complete)

    def complete(self, event):
        WordCompletionWindow(event.widget)
        self.chmode(Insert)

install = WordCompletion
