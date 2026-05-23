from cspkg.start import root
from cspkg.core import Namespace, Plugin, Main
from cspkg.plugins.normal_mode import Normal

import signal

class SpawnNS(Namespace):
    pass

class HandleOutput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(SpawnNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

class HandleInput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(SpawnNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

        self.add_kmap(SpawnNS, Normal, '<Key-z>', 
        lambda xstr: spawn.dump_line(), add=False)

        self.add_kmap(SpawnNS, Normal, '<Control-i>', 
        lambda event: spawn.dump_signal(signal.SIGINT), add=False)

        self.add_kmap(SpawnNS, Normal, '<Control-backslash>', 
        lambda event: spawn.dump_signal(signal.SIGQUIT), add=False)

        self.add_kmap(SpawnNS, Normal, '<Control-q>', 
        lambda event: spawn.dump_signal(signal.SIGKILL), add=False)

class BaseSpawn:
    def __init__(self, cmd, input, output):
        self.cmd    = cmd
        self.input  = input
        self.output = output
        self.install_events()

    def install_events(self):
        """

        """

        HandleOutput(self.output, self)
        HandleInput(self.input, self)
        root.status.set_msg('(spawn) %s -> %s' % (self.input.filename, 
        self.output.filename))

    def dump_signal(self, num):
        pass

    def terminate_process(self):
        pass

    def dump_line(self):
        pass

    def handle_close(self, expect):
        pass

