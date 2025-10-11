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
        lambda event: self.spawn.terminate_process())

        self.add_kmap(SpawnNS, Normal, '<Key-b>', 
        lambda xstr: spawn.dump_line(), add=False)

class BaseSpawn:
    def __init__(self, cmd, input, output):
        self.cmd    = cmd
        self.input  = input
        self.output = output
        self.install_events()

    def install_events(self):
        """

        """
        # self.input.hook('spawn', 'NORMAL', '<Control-c>', 
        # lambda event: self.dump_signal(signal.SIGINT), add=False)
        # sigint = lambda: self.dump_signal(signal.SIGINT)
        # ENV['sigint'] = sigint

        # self.input.hook('spawn', 'NORMAL', '<Control-backslash>', 
        # lambda event: self.dump_signal(signal.SIGQUIT), add=False)
        # sigquit = lambda: self.dump_signal(signal.SIGQUIT)
        # ENV['sigquit'] = sigquit

        # When one of the Xstr instances are destroyed then
        # the process is killed.

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

