from cspkg.core import Namespace, Main, Plugin, Command
from cspkg.stdout import logwrapper

class OutputsNS(Namespace):
    pass

class OutputController(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(OutputsNS, Main, '<Destroy>', self.del_output)

    def del_output(self, event):
        logwrapper.del_chan(self.xstr)

class Outputs(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(OutputsNS, Main, 
        '<Control-n>', self.create_vsplit_logger)

        self.add_kmap(OutputsNS, Main, 
        '<Control-m>', self.create_hsplit_logger)

    def create_vsplit_logger(self, event):
        xstr = self.xstr.master.master.master.create()
        logwrapper.add_chan(xstr)
        OutputController(xstr)
    
    def create_hsplit_logger(self, event):
        xstr = self.xstr.master.master.create()
        logwrapper.add_chan(xstr)
        OutputController(xstr)

@Command('vlsplit')
def vlsplit(xstr):
    """
    """
    xstr = xstr.master.master.master.create()
    logwrapper.add_chan(xstr)
    OutputController(xstr)

@Command('hlsplit')
def hlsplit(xstr):
    """    
    """
    xstr = xstr.master.master.create()
    logwrapper.add_chan(xstr)
    OutputController(xstr)

install = Outputs
