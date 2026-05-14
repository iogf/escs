
from traceback import print_exc as debug
from cspkg.core import Command
from cspkg.scan import Read
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

        self.add_kmap(CmdExec, Main, '<Alt-semicolon>',  
        lambda event: Read(events={'<Escape>' : lambda read: read.done(),
        '<Return>': lambda read: self.exec_cmd(read)}, msg='Command:'))

        self.add_kmap(CmdExec, Main, '<Control-z>',  self.set_target)
        self.add_kmap(CmdExec, Main, '<Control-semicolon>',  self.exec_all)

    def exec_cmd(self, read):
        Command.set_target(self.xstr)
        data = read.text()
        read.done()

        print('\n(cmd) Executed code:\n>>> %s\n' % data)
        self.runcode(data.encode('utf-8'), rcenv)

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

