"""
"""
from cspkg.tools import RegexEvent
from untwisted.splits import Terminator
from cspkg.core import Namespace, Plugin
from cspkg.plugins.python_mode import Python
from cspkg.xscan import Xscan
from cspkg.dap import DAP
from cspkg.start import root
import shlex
import sys
from cspkg.core import Namespace, Plugin, Mode

class PdbNS(Namespace):
    pass

class Pdb(Mode):
    pass

class DebuggerProcess(DAP):
    path = 'python'

    def __init__(self):
        super().__init__()

    def evaluate_expression(self, event):
        xscan  = Xscan()

        self.send("p %s\r\n" % xscan.data)
        root.status.set_msg('(pdb) Sent expression!')

    def set_auto_open(self, event):
        self.auto_open = False if self.auto_open else True
        root.status.set_msg('(pdb) Auto open files: %s!' % self.auto_open)

    def send(self, data):
        self.expect.send(data.encode(self.encoding))
        print('Pdb Cmd: ', data)

    def send_break(self, event):
        self.send('break %s:%s\r\n' % (event.widget.filename, 
        event.widget.indexsplit('insert')[0]))
        # event.widget.chmode('NORMAL')
        root.status.set_msg('(pdb) Command break sent !')

    def send_step(self, event):
        self.send('step\r\n')
        root.status.set_msg('(pdb) Command step sent !')

    def send_tbreak(self, event):
        self.send('tbreak %s:%s\r\n' % (event.widget.filename, 
        event.widget.indexsplit('insert')[0]))
        # event.widget.chmode('NORMAL')
        root.status.set_msg('(pdb) Command tbreak sent !')

    def send_continue(self, event):
        """
        """

        self.send('continue\r\n')
        root.status.set_msg('(pdb) Command continue sent !')

    def send_restart(self, event):
        """
        """

        self.send('restart\r\n')
        root.status.set_msg('(pdb) Sent restart !')

    def evaluate_selection(self, event):
        data = event.widget.tag_xjoin('sel', sep='\r\n')
        self.send('p %s' % data)
        # event.widget.chmode('NORMAL')
        root.status.set_msg('(pdb) Sent text selection!')

    def install_handles(self, expect):
        Terminator(expect, delim=b'\n')

        regstr0 = '\> (.+)\(([0-9]+)\).+'

        RegexEvent(expect, regstr0, 'LINE', self.encoding)
        expect.add_map('LINE', self.handle_line)

    def run(self, event):
        self.kill_process()
        self.create_process(' '.join([self.path, '-u', 
        '-m', 'pdb', event.widget.filename]))

        root.status.set_msg('(pdb) Started !')
        # event.widget.chmode('NORMAL')

    def run_args(self, event):
        xscan  = Xscan()
        ARGS = '%s -u -m pdb %s %s' % (self.path, 
        event.widget.filename, xscan.data)
        self.kill_process()

        ARGS = shlex.split(ARGS)
        self.create_process(ARGS)
        
        root.status.set_msg('(pdb) Started with Args: %s' % xscan.data)
        # event.widget.chmode('NORMAL')

    def dump_clear_all(self, event):
        self.send('clear\r\nyes\r\n')
        # event.widget.chmode('NORMAL')
        root.status.set_msg('(pdb) Command clearall sent!')

    def remove_breakpoint(self, event):
        """
        """
        line, col = event.widget.indexsplit('insert')
        self.send('clear %s:%s\r\n' % (event.widget.filename, line))
        # event.widget.chmode('NORMAL')
        root.status.set_msg('(pdb) Command clear sent!')

    def send_dcmd(self, event):
        xscan  = Xscan()

        self.send('%s\r\n' % xscan.data)
        root.status.set_msg('(pdb) Sent cmd!')

    def quit_db(self, event):
        self.kill_process()
        # event.widget.chmode('NORMAL')
        sys.stdout.write('(pdb) Sent quit!')

class PythonDebugger(Plugin):
    debugger = DebuggerProcess()

    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(PdbNS, Python, '<Key-exclam>', self.switch_pdb_mode)
        self.add_kmap(PdbNS, Pdb, '<Key-p>', self.debugger.evaluate_selection)
        self.add_kmap(PdbNS, Pdb, '<Key-x>', self.debugger.evaluate_expression)
        self.add_kmap(PdbNS, Pdb, '<Key-r>', self.debugger.run)
        self.add_kmap(PdbNS, Pdb, '<Control-R>', self.debugger.run_args)
        self.add_kmap(PdbNS, Pdb, '<Control-r>', self.debugger.send_restart)
        self.add_kmap(PdbNS, Pdb, '<Key-m>', self.debugger.send_dcmd)
        self.add_kmap(PdbNS, Pdb, '<Key-Q>', self.debugger.quit_db) 
        self.add_kmap(PdbNS, Pdb, '<Key-c>', self.debugger.send_continue)
        self.add_kmap(PdbNS, Pdb, '<Control-C>', self.debugger.dump_clear_all)
        self.add_kmap(PdbNS, Pdb, '<Control-c>', self.debugger.remove_breakpoint)
        self.add_kmap(PdbNS, Pdb, '<Key-B>',  self.debugger.send_tbreak)
        self.add_kmap(PdbNS, Pdb, '<Key-s>',  self.debugger.send_step)
        self.add_kmap(PdbNS, Pdb, '<Key-S>',  self.debugger.set_auto_open)
        self.add_kmap(PdbNS, Pdb, '<Key-b>', self.debugger.send_break)

    def c_path(self, path):
        DebuggerProcess.path = path

    def switch_pdb_mode(self, event):
        self.chmode(Pdb)
        root.status.set_msg('Pdb mode started.')

install = PythonDebugger
