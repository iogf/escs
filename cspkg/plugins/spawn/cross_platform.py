"""
"""

from untwisted.expect import Expect, LOAD, CLOSE
from cspkg.plugins.spawn.base_spawn import BaseSpawn
from cspkg.core import Command
from cspkg.start import root
from os import environ 

import shlex

class Spawn(BaseSpawn):
    def __init__(self, cmd):
        self.expect = Expect(cmd, env=environ)

    def install_events(self):
        super(Spawn, self).install_events()

        # When call.terminnate is called it may happen of having still data to be
        # processed. It would attempt to write on an xstrVi instance that no more exist.
        # So, it executes quietly the xstrVi.append method.
        self.expect.add_map(LOAD, lambda expect, data: self.output.append(data))
        self.expect.add_map(CLOSE, self.handle_close)
        
    def dump_signal(self, num):
        self.expect.child.send_signal(num)

    def terminate_process(self):
        # Exceptions should be written to sys.stdout for default.
        self.expect.terminate()
        root.status.set_msg('(spawn) Killed process!')

    def dump_line(self):
        data = self.input.get('insert linestart', 'insert +1l linestart')
        data = data.encode(self.input.charset)
        self.expect.send(data)
        line, col = self.input.indexsplit()
        self.input.setcur(line + 1, col)

    def handle_close(self, expect):
        root.status.set_msg('(spawn) Killed process!')
        expect.destroy()

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

@Command('hspawn')
def hspawn(xstr, cmd):
    HSpawn(cmd)

@Command('vspawn')
def hspawn(xstr, cmd):
    VSpawn(cmd)

Command('vbash')(lambda xstr: VSpawn('bash -i'))
Command('hbash')(lambda xstr: HSpawn('bash -i'))

