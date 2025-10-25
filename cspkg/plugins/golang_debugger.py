"""
"""

from untwisted.splits import Terminator
from untwisted.expect import Expect, LOAD, CLOSE
from cspkg.tools import RegexEvent
from cspkg.plugins.golang_mode import Golang
from cspkg.core import Plugin, Namespace
from re import findall
from cspkg.scan import Scan
from cspkg.start import root
import shlex
import sys

class GolangDebuggerNS(Namespace):
    pass

class GolangDebugger(Plugin):
    expect = None
    encoding='utf8'
    bp_appearence={'background':'blue', 'foreground':'yellow'}

    def __init__(self, xstr):
        super().__init__(xstr)        
        self.auto_open = False

        self.add_kmap(GolangDebuggerNS, Golang, '<Key-p>', self.evaluate_selection)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-r>', self.run)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-exclam>', self.send_restart)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-x>', self.evaluate_expression)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-R>', self.run_args)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-Q>', self.quit_db)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-c>', self.send_continue)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-m>', self.send_dcmd)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-S>', self.dump_clear_all)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-C>', self.remove_breakpoint)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-b>', self.send_break)
        self.add_kmap(GolangDebuggerNS, Golang, '<Key-A>',  self.set_auto_open)

    def set_auto_open(self, event):
        self.auto_open = False if self.auto_open else True
        root.status.set_msg('(Delve) Auto open files: %s!' % self.auto_open)

    def evaluate_expression(self, event):
        ask  = Scan()

        self.send("print %s\r\n" % ask.data)
        root.status.set_msg('(delve) Sent expression!')

    def send_restart(self, event):
        self.send('restart\r\n')
        root.status.set_msg('(delve) Sent restart!')

    def send_dcmd(self, event):
        ask  = Scan()
        self.send('%s\r\n' % ask.data)
        root.status.set_msg('(delve) Sent cmd!')

    def evaluate_selection(self, event):
        data = self.xstr.join_ranges('sel', sep='\r\n')
        self.send('print %s' % data)
        root.status.set_msg('(delve) Sent selection !')

    def install_handles(self, expect):
        Terminator(expect, delim=b'\n')

        regstr = '\> [^ ]* ?[^ ]+ ([^ ]+):([0-9]+).+'
        RegexEvent(expect, regstr, 'LINE', self.encoding)
        expect.add_map('LINE', self.handle_line)

    def run(self, event):
        if self.expect:
            self.expect.terminate()

        self.create_process(' '.join(['dlv', 'debug', 
        '--allow-non-terminal-interactive', self.xstr.filename]))

        root.status.set_msg('(delve) Started !')

    def run_args(self, event):
        ask  = Scan()

        if self.expect:
            self.expect.terminate()
        cmd = 'dlv debug --allow-non-terminal-interactive %s -- %s' % (
            self.xstr.filename, ask.data)
        self.create_process(shlex.split(cmd))
        
        root.status.set_msg('(delve) Started: %s' % ask.data)

    def send_break(self, event):
        line, col = self.xstr.indexsplit('insert')

        # Make sure the name will be unique for removing it later.
        bname = findall('[a-zA-Z]+', self.xstr.filename)
        bname = '%s%s' % (''.join(bname), line)
        self.send('break %s %s:%s\r\n' % (bname, self.xstr.filename, line))

        root.status.set_msg('(delve) Sent breakpoint !')

    def send(self, data):
        self.expect.send(data.encode(self.encoding))
        print('Delve Cmd: ', data)

    def send_continue(self, event):
        """
        """

        self.send('continue\r\n')
        root.status.set_msg('(delve) Sent continue !')

    def dump_clear_all(self, event):
        self.send('clearall\r\n')

        root.status.set_msg('(delve) Sent clearall !')

    def remove_breakpoint(self, event):
        """
        """

        line, col = self.xstr.indexsplit('insert')
        bname = findall('[a-zA-Z]+', self.xstr.filename)
        bname = '%s%s' % (''.join(bname), line)
        self.send('clear %s\r\n' % bname)

        root.status.set_msg('(delve) Sent clear !')

    def create_process(self, args):
        self.expect = Expect(args)

        # Note: The data has to be decoded using the xstr charset
        # because the xstr contents would be sometimes printed along
        # the debugging.
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

    def quit_db(self, event):
        if not self.expect:
            root.status.set_msg('Delve debugger not started.')
        else:
            self.expect.terminate()
        sys.stdout.write('(Delve) Sent quit!')

    def handle_line(self, expect, filename, line):
        xstr = root.note.lseek(filename, line, self.auto_open)
        if xstr is not None:
            xstr.set_breakpoint(line, self.bp_appearence)
        root.status.set_msg('Debugger stopped at: %s:%s' % (filename, line))

install = GolangDebugger

