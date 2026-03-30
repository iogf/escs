from cspkg.fwin import TextWindow
from cspkg.core import Namespace, Main, Plugin
from cspkg.start import root
from cspkg.stdout import logwrapper
import sys

class SyslogNS(Namespace):
    pass

xwin = TextWindow('Interpreter output ...', title='Syslog')
xwin.withdraw()

class Syslog(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(SyslogNS, Main, 
        '<Alt-q>', lambda event: xwin.display(self.xstr))

logwrapper.add_chan(xwin.text)
install = Syslog
