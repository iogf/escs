from untwisted.file_writer import FileWriter
from untwisted.file_reader import FileReader
from untwisted.event import LOAD, CLOSE
from cspkg.core import Command
from untwisted.network import Device
from subprocess import Popen, PIPE, STDOUT
from os import environ, setsid, killpg
from cspkg.start import root
from cspkg.core import Namespace, Plugin, Main
from cspkg.plugins.normal_mode import Normal

class SpawnNS(Namespace):
    pass

class SpawnOutput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(SpawnNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

class SpawnInput(Plugin):
    def __init__(self, xstr, spawn):
        super().__init__(xstr)
        self.add_kmap(SpawnNS, Main, '<Destroy>',
        lambda event: spawn.terminate_process())

        self.add_kmap(SpawnNS, Normal, '<F1>', 
        lambda xstr: spawn.dump_line(), add=False)

class Spawn:
    def __init__(self, cmd, input, output):
        self.cmd = cmd
        self.input = input
        self.output = output

        self.child = Popen(cmd, 
        shell=True, stdout=PIPE, stdin=PIPE, preexec_fn=setsid, 
        stderr=STDOUT,  env=environ)

        self.stdout = Device(self.child.stdout)
        self.stdin = Device(self.child.stdin)
        FileReader(self.stdout)
        FileWriter(self.stdin)

        self.stdout.add_map(LOAD, lambda con, data: \
        self.output.append(data))

        self.stdin.add_map(CLOSE, self.handle_close)
        self.stdout.add_map(CLOSE, self.handle_close)

        SpawnOutput(self.output, self)
        SpawnInput(self.input, self)

        root.status.set_msg('(spawn) %s -> %s' % (self.input.filename, 
        self.output.filename))

    def dump_signal(self, num):
        killpg(self.child.pid, num)

    def terminate_process(self):
        self.child.kill()
        root.status.set_msg('(spawn) Killed process!')

    def dump_line(self):
        data = self.input.get('insert linestart', 'insert +1l linestart')
        data = data.encode(self.input.charset)
        self.stdin.dump(data)
        self.input.down()

    def handle_close(self, dev, err):
        root.status.set_msg('(spawn) Killed process!')
        self.stdout.destroy()
        self.stdin.destroy()

class HSpawn(Spawn):
    def __init__(self, cmd):
        Spawn.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.create())

class VSpawn(Spawn):
    def __init__(self, cmd):
        Spawn.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.master.create())

@Command('hspawn')
def hspawn(xstr, cmd):
    HSpawn(cmd)

@Command('vspawn')
def vspawn(xstr, cmd):
    VSpawn(cmd)

Command('vsbash')(lambda xstr: VSpawn('bash -i'))
Command('hsbash')(lambda xstr: HSpawn('bash -i'))