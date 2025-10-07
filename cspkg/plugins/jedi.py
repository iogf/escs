from cspkg.fwin import CompletionWindow
from cspkg.core import Command
from cspkg.core import Plugin, Namespace, Main
from cspkg.plugins.extra_mode import Extra
from cspkg.plugins.insert_mode import Insert
from jedi import Script

class JediNS(Namespace):
    pass

class PythonCompletionWindow(CompletionWindow):
    """
    """

    def __init__(self, area, *args, **kwargs):
        source      = area.get('1.0', 'end')
        line, col   = area.indexsplit()
        script      = Script(source, path=area.filename)
        completions = script.complete(line, col)
        CompletionWindow.__init__(self, area, completions, *args, **kwargs)

class Jedi(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        trigger = lambda event: self.add_kmap(JediNS, Extra, 
        '<Key-period>', self.complete, add=False)
    
        remove_trigger = lambda event: self.flush(JediNS, Extra)
    
        self.add_kmap(JediNS, Main, '<<Load/*.py>>', trigger, True)
        self.add_kmap(JediNS, Main, '<<Save/*.py>>', trigger, True)
        self.add_kmap(JediNS, Main, '<<LoadData>>', remove_trigger, True)
        self.add_kmap(JediNS, Main, '<<SaveData>>', remove_trigger, True)

    def complete(self, event):
        PythonCompletionWindow(event.widget)
        self.chmode(Insert)

@Command('acp')
class ActivateJedi(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        """
        Activate python completion when file extension is not 
        detected automatically.
        """
        self.add_kmap(JediNS, Extra, '<Key-period>', 
        lambda event: PythonCompletionWindow(event.widget), add=False)
        self.chmode(Insert)

install = Jedi