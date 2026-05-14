
from cspkg.scan import Read
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal
from subprocess import Popen, PIPE

class RunProcessNS(Namespace):
    pass

class RunProcess(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(RunProcessNS, Normal, '<Key-M>', 
         lambda event: Read(events={'<Escape>': lambda read: read.done(), 
        '<Return>': lambda read: self.run(read)}, 
        msg='Shell command:'))

    def run(self, read):
        data = read.text()
        read.done()

        process = Popen(data, stdout=PIPE, 
        stderr=PIPE, text=True, shell=True)

        output, err = process.communicate()
        self.xstr.append(output)
        self.xstr.append(err)
        root.status.set_msg('Executed shell command: %s' % data)
    
install = RunProcess

