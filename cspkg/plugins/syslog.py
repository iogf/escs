from cspkg.fwin import TextWindow
from cspkg.core import Namespace, Main, Plugin
from cspkg.start import root
import sys

class SyslogNS(Namespace):
    pass

class LogWrapper:
    """
    """

    def __init__(self, stdout, logwin):
        self.logwin = logwin
        self.stdout = stdout

    def write(self, data):
        self.logwin.text.insert('end', data)
        self.logwin.text.see('end')
        self.stdout.write(data)

class Syslog(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(SyslogNS, Main, 
        '<Alt-q>', lambda event: logwin.display())

logwin = TextWindow('', title='Cmd Output')
logwin.withdraw()
logwrapper = LogWrapper(sys.__stdout__, logwin)
sys.stdout = logwrapper

install = Syslog
