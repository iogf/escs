from cspkg.core import Namespace, Plugin, Main
from cspkg.plugins.normal_mode import Normal
from untwisted.expect import Expect, LOAD, CLOSE
from cspkg.core import Command
from cspkg.start import root
from os import environ 

class CallNS(Namespace):
    pass

class CallOutput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(CallNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

class CallInput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(CallNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

        self.add_kmap(CallNS, Normal, '<F2>', 
        lambda xstr: spawn.dump_line(), add=False)

class Call:
    def __init__(self, cmd, input, output):
        self.cmd = cmd
        self.input = input
        self.output = output

        self.expect = Expect(cmd, env=environ)

        # When call.terminnate is called it may happen of having still data to be
        # processed. It would attempt to write on an xstrVi instance that no more exist.
        # So, it executes quietly the xstrVi.append method.
        self.expect.add_map(LOAD, lambda expect, data: self.output.append(data))
        self.expect.add_map(CLOSE, self.handle_close)

        CallOutput(self.output, self)
        CallInput(self.input, self)
        root.status.set_msg('(call) %s -> %s' % (self.input.filename, 
        self.output.filename))
        
    def dump_signal(self, num):
        self.expect.child.send_signal(num)

    def terminate_process(self):
        # Exceptions should be written to sys.stdout for default.
        self.expect.terminate()
        root.status.set_msg('(call) Killed process!')

    def dump_line(self):
        data = self.input.get('insert linestart', 'insert +1l linestart')
        data = data.encode(self.input.charset)
        self.expect.send(data)
        self.input.down()

    def handle_close(self, expect):
        root.status.set_msg('(call) Killed process!')
        expect.destroy()

class HCall(Call):
    def __init__(self, cmd):
        Call.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.create())

class VCall(Call):
    def __init__(self, cmd):
        Call.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.master.create())

@Command('hcall')
def hcall(xstr, cmd):
    HCall(cmd)

@Command('vcall')
def vcall(xstr, cmd):
    VCall(cmd)

Command('vcbash')(lambda xstr: VCall('bash -i'))
Command('hcbash')(lambda xstr: HCall('bash -i'))