"""
"""
from cspkg.tools import RegexEvent
from untwisted.splits import Terminator
from cspkg.plugins.python_mode import Python
from cspkg.scan import Read
from cspkg.start import root
import shlex
import sys
from cspkg.core import Namespace, Plugin, Mode
from untwisted.expect import Expect, LOAD, CLOSE
from os.path import abspath

class PdbNS(Namespace):
    pass

class Pdb(Plugin):
    path = 'python'

    bp_appearence={'background':'blue', 'foreground':'yellow'}
    encoding='utf8'
    expect = None

    def __init__(self, xstr):
        super().__init__(xstr)
        self.auto_open = False

        self.add_kmap(PdbNS, Python, '<Key-p>', self.evaluate_selection)
        self.add_kmap(PdbNS, Python, '<Key-r>', self.run)
        self.add_kmap(PdbNS, Python, '<Key-exclam>', self.send_restart)
        self.add_kmap(PdbNS, Python, '<Key-Q>', self.quit_db) 
        self.add_kmap(PdbNS, Python, '<Key-c>', self.send_continue)
        self.add_kmap(PdbNS, Python, '<Key-S>', self.dump_clear_all)
        self.add_kmap(PdbNS, Python, '<Key-C>', self.remove_breakpoint)
        self.add_kmap(PdbNS, Python, '<Key-B>',  self.send_tbreak)
        self.add_kmap(PdbNS, Python, '<Key-s>',  self.send_step)
        self.add_kmap(PdbNS, Python, '<Key-A>',  self.set_auto_open)
        self.add_kmap(PdbNS, Python, '<Key-b>', self.send_break)

        self.add_kmap(PdbNS, Python, '<Key-R>', 
        lambda event: Read(events={'<Escape>': lambda read: read.done(), 
        '<Return>': self.run_args}, msg='Run with Args'))

        self.add_kmap(PdbNS, Python, '<Key-m>', 
        lambda event: Read(events={'<Escape>': lambda read: read.done(),
        '<Return>': self.send_dcmd}, msg='Send command:'))

        self.add_kmap(PdbNS, Python, '<Key-x>', 
        lambda event: Read(events={'<Escape>': lambda read: read.done(), 
        '<Return>': self.evaluate_expression}, msg='Evaluate Expression:'))

    def c_path(self, path):
        DebuggerProcess.path = path

    def create_process(self, cmd):

        # Note: The data has to be decoded using the xstr charset
        # because the xstr contents would be sometimes printed along
        # the debugging.
        Pdb.expect = Expect(cmd)
        self.expect.add_map(LOAD, lambda con, 
        data: sys.stdout.write(data.decode(self.encoding)))

        # The expect has to be passed here otherwise when 
        # starting the new one gets terminated.

        self.expect.add_map(CLOSE, self.on_bkpipe)

        self.install_handles(self.expect)
        root.protocol("WM_DELETE_WINDOW", self.on_tk_quit)

    def on_bkpipe(self, expect):
        """
        On broken pipe.
        """
        expect.terminate()
        root.status.set_msg('Debugger: CLOSED!')

    def on_tk_quit(self):
        """
        Necessary otherwise the thread hangs.
        """
        self.expect.terminate()
        root.destroy()

    def handle_line(self, expect, filename, line):
        xstr = root.note.lseek(filename, line, self.auto_open)

        if xstr is not None:
            xstr.set_breakpoint(line, self.bp_appearence)
        root.status.set_msg('Debugger stopped at: %s:%s' % (filename, line))

    def evaluate_expression(self, read):
        data = read.text()
        read.done()

        self.send("p %s\r\n" % data)
        root.status.set_msg('Pdb - Sent expression!')

    def set_auto_open(self, event):
        self.auto_open = False if self.auto_open else True
        root.status.set_msg('(pdb) Auto open files: %s!' % self.auto_open)

    def send(self, data):
        self.expect.send(data.encode(self.encoding))
        print('Pdb Cmd: ', data)

    def send_break(self, event):
        self.send('break %s:%s\r\n' % (self.xstr.filename, 
        self.xstr.indexsplit('insert')[0]))
        root.status.set_msg('Pdb - Command break sent !')

    def send_step(self, event):
        self.send('step\r\n')
        root.status.set_msg('Pdb - Command step sent !')

    def send_tbreak(self, event):
        self.send('tbreak %s:%s\r\n' % (self.xstr.filename, 
        self.xstr.indexsplit('insert')[0]))
        root.status.set_msg('Pdb - Command tbreak sent !')

    def send_continue(self, event):
        """
        """

        self.send('continue\r\n')
        root.status.set_msg('Pdb - Command continue sent !')

    def send_restart(self, event):
        """
        """

        self.send('restart\r\n')
        root.status.set_msg('Pdb - Sent restart !')

    def evaluate_selection(self, event):
        data = self.xstr.tag_xjoin('sel', sep='\r\n')
        self.send('p %s' % data)
        root.status.set_msg('Pdb - Sent text selection!')

    def install_handles(self, expect):
        Terminator(expect, delim=b'\n')

        regstr = '\> (.+)\(([0-9]+)\).+'

        RegexEvent(expect, regstr, 'LINE', self.encoding)
        expect.add_map('LINE', self.handle_line)

    def run(self, event):
        if self.expect:
            self.expect.terminate()
        self.create_process(' '.join([self.path, '-u', 
        '-m', 'pdb', self.xstr.filename]))

        root.status.set_msg('Pdb - Started !')

    def run_args(self, read):
        data = read.text()
        read.done()
        args = '%s -u -m pdb %s %s' % (self.path, 
        self.xstr.filename, data)

        if self.expect:
            self.expect.terminate()
        self.create_process(args)
        root.status.set_msg('Pdb - Started with Args: %s' % data)

    def dump_clear_all(self, event):
        self.send('clear\r\nyes\r\n')
        root.status.set_msg('Pdb - Command clearall sent!')

    def remove_breakpoint(self, event):
        """
        """
        line, col = self.xstr.indexsplit('insert')
        self.send('clear %s:%s\r\n' % (self.xstr.filename, line))
        root.status.set_msg('Pdb - Command clear sent!')

    def send_dcmd(self, read):
        data = read.text()
        read.done()

        self.send('%s\r\n' % data)
        root.status.set_msg('Pdb - Sent cmd!')

    def quit_db(self, event):
        if not self.expect:
            root.status.set_msg('Debugger not started.')
        else:
            self.expect.terminate()
        sys.stdout.write('Pdb - Sent quit!')

install = Pdb
