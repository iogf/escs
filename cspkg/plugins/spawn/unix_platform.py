"""
"""

from untwisted.file_writer import FileWriter
from untwisted.file_reader import FileReader
from untwisted.event import LOAD, CLOSE
from cspkg.core import Command
from untwisted.network import Device
from subprocess import Popen, PIPE, STDOUT
from os import environ, setsid, killpg
from cspkg.plugins.spawn.base_spawn import BaseSpawn
from cspkg.start import root

class Spawn(BaseSpawn):
    def __init__(self, cmd):
        self.child   = Popen(cmd, 
        shell=True, stdout=PIPE, stdin=PIPE, preexec_fn=setsid, 
        stderr=STDOUT,  env=environ)

        self.stdout  = Device(self.child.stdout)
        self.stdin   = Device(self.child.stdin)

    def install_events(self):
        super(Spawn, self).install_events()

        FileReader(self.stdout)
        FileWriter(self.stdin)

        self.stdout.add_map(LOAD, lambda con, data: \
        self.output.append(data))

        self.stdin.add_map(CLOSE, self.handle_close)
        self.stdout.add_map(CLOSE, self.handle_close)

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
        Spawn.__init__(self, cmd)
        BaseSpawn.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.create())

class VSpawn(Spawn):
    def __init__(self, cmd):
        Spawn.__init__(self, cmd)
        BaseSpawn.__init__(self, cmd, Command.xstr, 
        Command.xstr.master.master.master.create())


Command('hspawn')(HSpawn)
Command('vspawn')(VSpawn)

Command('vbash')(lambda xstr: VSpawn('bash -i'))
Command('hbash')(lambda xstr: HSpawn('bash -i'))
# ENV['hpy'] = lambda : HSpawn('bash -c "tee -i >(stdbuf -o 0 python -i -u)"')
# ENV['vpy'] = lambda : VSpawn('bash -c "tee -i >(stdbuf -o 0 python -i -u)"')

# ENV['hrb'] = lambda : HSpawn('bash -c "stdbuf -o 0 irb --inf-ruby-mode"')
# ENV['vrb'] = lambda : VSpawn('bash -c "stdbuf -o 0 irb --inf-ruby-mode"')






