
from traceback import print_exc as debug
from cspkg.core import Command
from cspkg.xscan import Xscan
from cspkg.core import rcenv
from cspkg.start import root
from cspkg.core import Namespace, Main, Plugin
import re
import sys

class CmdExecNS(Namespace):
    pass

class CmdExec(Plugin):
    TAGCONF = {'background':'#313131'}

    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(CmdExec, Main, '<Alt-semicolon>',  self.exec_cmd)
        self.add_kmap(CmdExec, Main, '<Control-z>',  self.set_target)
        self.add_kmap(CmdExec, Main, '<Control-semicolon>',  self.exec_all)

    def exec_cmd(self, event):
        xscan = Xscan()
        Command.set_target(self.xstr)
    
        data = xscan.data.encode('utf-8')

        print('\n(cmd) Executed code:\n>>> %s\n' % xscan.data)
        self.runcode(data, rcenv)

    def exec_all(self, event):
        data = self.xstr.get('1.0', 'end')    
        data = data.encode('utf-8')
        self.runcode(data, rcenv)

    def runcode(self, data, env):
        """
        """

        tmp = sys.stderr
        sys.stderr = sys.stdout
    
        try:
            exec(data, env)
        except Exception as e:
            debug()
            root.status.set_msg('Error: %s' % e)
        finally:
            sys.stderr = tmp

    def set_target(self, event):
        Command.set_target(self.xstr)

        root.status.set_msg('Set command target !')
    
install = CmdExec

