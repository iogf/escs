
from cspkg.scan import Scan
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal
from subprocess import Popen, PIPE
import shlex

class RunProcNS(Namespace):
    pass

class RunProc(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(RunProc, Normal, 
        '<Key-Z>',  self.run)

    def run(self, event):
        scan = Scan()
        process = Popen(scan.data, 
        stdout=PIPE, stderr=PIPE, text=True, shell=True)

        output, err = process.communicate()
        self.xstr.append(output)
        self.xstr.append(err)
        root.status.set_msg('Executed shell command: %s' % scan.data)
    
install = RunProc

