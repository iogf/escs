from cspkg.fwin import TextWindow
from cspkg.core import Namespace, Main, Plugin
from cspkg.start import root
import sys


class SyslogNS(Namespace):
    pass

class LogWrapper:
    """
    """

    def __init__(self, xstr=None):
        self.xwin = TextWindow('', title='Cmd Output')
        self.xwin.withdraw()
        
        self.xstr = xstr

    def write(self, data):
        self.xwin.text.insert('end', data)
        self.xwin.text.see('end')
        sys.__stdout__.write(data)

        if self.xstr is not None:
            self.update_xstr(data)

    def update_xstr(self, data):
        self.xstr.insert('end', data)
        self.xstr.see('insert')

    def set_xstr(self, xstr):
        self.xstr = xstr

    def unset_xstr(self):
        self.xstr = None

    def flush(self):
        pass

logwrapper = LogWrapper()
sys.stdout = logwrapper

class Syslog(Plugin):

    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(SyslogNS, Main, 
        '<Alt-q>', lambda event: 
        logwrapper.xwin.display())

        self.add_kmap(SyslogNS, Main, 
        '<Control-q>', self.add_chan)

        self.add_kmap(SyslogNS, Main, 
        '<Control-Q>', self.rm_chan)

    def add_chan(self, chan):
        logwrapper.set_xstr(self.xstr)
        root.status.set_msg('Output set: %s' % self.xstr.index('insert'))

    def rm_chan(self, chan):
        logwrapper.unset_xstr()
        root.status.set_msg('Output removed!')

install = Syslog
