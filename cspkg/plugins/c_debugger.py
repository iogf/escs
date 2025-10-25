"""
"""
from untwisted.expect import Expect, LOAD, CLOSE
from tkinter.filedialog import askopenfilename
from untwisted.splits import Terminator
from cspkg.tools import RegexEvent
from cspkg.scan import Scan
from cspkg.start import root
from cspkg.core import Namespace, Plugin, Mode
from os.path import abspath
from cspkg.plugins.c_mode import C
import shlex
import sys

class GDBNS(Namespace):
    pass

class GDB(Mode):
    pass

class CDebugger(Plugin):
    expect  = None
    bp_appearence={'background':'blue', 'foreground':'yellow'}
    encoding='utf8'

    def __init__(self, xstr):
        super().__init__(xstr)
        
        self.add_kmap(GDBNS, C, '<Key-p>', self.evaluate_selection)
        self.add_kmap(GDBNS, C, '<Key-R>', self.ask_gdb_exec)
        self.add_kmap(GDBNS, C, '<Key-r>', self.run)
        self.add_kmap(GDBNS, C, '<Key-x>', self.evaluate_expression)
        self.add_kmap(GDBNS, C, '<Key-Q>', self.quit_db)
        self.add_kmap(GDBNS, C, '<Key-c>', self.send_continue)
        self.add_kmap(GDBNS, C, '<Key-m>', self.send_dcmd)
        self.add_kmap(GDBNS, C, '<Key-s>',  self.send_step)
        self.add_kmap(GDBNS, C, '<Key-A>',  self.set_auto_open)
        self.add_kmap(GDBNS, C, '<Key-C>', self.clear_breakpoint)
        self.add_kmap(GDBNS, C, '<Key-b>', self.send_break)
        self.auto_open = False

    def switch_gdb_mode(self, event):
        self.chmode(GDB)

    def send_step(self, event):
        self.send('step\r\n')
        root.status.set_msg('(GDB) Command step sent !')

    def set_auto_open(self, event):
        self.auto_open = False if self.auto_open else True
        root.status.set_msg('(GDB) Auto open files: %s!' % self.auto_open)

    def evaluate_expression(self, event):
        scan  = Scan()

        self.send("print %s\r\n" % scan.data)
        root.status.set_msg('(GDB) Sent expression!')

    def run(self, event):
        self.send('run\r\n')
        root.status.set_msg('(GDB) Sent run!')

    def send_dcmd(self, event):
        scan  = Scan()
        self.send('%s\r\n' % scan.data)
        root.status.set_msg('(GDB) Sent cmd!')

    def evaluate_selection(self, event):
        data = event.widget.join_ranges('sel', sep='\r\n')
        self.send('print %s' % data)
        root.status.set_msg('(GDB) Sent selection !')

    def install_handles(self, expect):
        Terminator(expect, delim=b'\n')
        regstr = '(\032\032|\(gdb\) \032\032)(.+):([0-9]+):[0-9]+:.+:.+'
        RegexEvent(expect, regstr, 'LINE', self.encoding)
        expect.add_map('LINE', self.handle_line)

    def ask_gdb_exec(self, event):
        root.status.set_msg('(GDB) Select a compiled file:')
        filename = askopenfilename()
        if filename: 
            self.init_gdb(filename)

    def init_gdb(self, filename):
        if self.expect:
            self.expect.terminate()
        self.create_process('gdb -f %s' % filename)
        root.status.set_msg('(GDB) Started: %s' % filename)
        self.send('set style enabled off\r\n')

    def send_break(self, event):
        line, col = event.widget.indexsplit('insert')

        # Make sure the name will be unique for removing it later.
        self.send('break %s:%s\r\n' % (event.widget.filename, line))

        root.status.set_msg('(GDB) Sent breakpoint !')

    def send(self, data):
        self.expect.send(data.encode(self.encoding))
        print('GDB Cmd: ', data)

    def send_continue(self, event):
        """
        """

        self.send('continue\r\n')
        root.status.set_msg('(GDB) Sent continue !')

    def clear_breakpoint(self, event):
        """
        """

        line, col = event.widget.indexsplit('insert')
        self.send('clear %s:%s\r\n' % (event.widget.filename, line))

        root.status.set_msg('(GDB) Sent clear !')

    def quit_db(self, event):
        if not self.expect:
            root.status.set_msg('GDB not started.')
        else:
            self.expect.terminate()
        sys.stdout.write('(GDB) Sent quit!')

    def create_process(self, cmd):
        CDebugger.expect = Expect(cmd)

        self.expect.add_map(LOAD, lambda con, 
        data: sys.stdout.write(data.decode(self.encoding)))

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
        """
        self.expect.terminate()
        root.destroy()

    def handle_line(self, expect, token, filename, line):
        xstr = root.note.lseek(filename, line, self.auto_open)
        if xstr is not None:
            xstr.set_breakpoint(line, self.bp_appearence)
        root.status.set_msg('Debugger stopped at: %s:%s' % (filename, line))

install = CDebugger
