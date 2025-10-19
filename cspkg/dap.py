from untwisted.expect import Expect, LOAD, CLOSE
from os.path import abspath
from cspkg.xstr import Xstr
from cspkg.start import root
import sys

class DAP:
    """
    Debugger adapter pattern.

    This class makes it simple to implement new debuggers in vy.
    It follows a specific approach that is not necessarily strict.

    It makes usage of Untwisted Framework's usage to implement its basic
    logic.
    """
    
    bp_appearence={'background':'blue', 'foreground':'yellow'}
    encoding='utf8'

    def __init__(self):
        self.expect  = None
        self.auto_open = False
        self.charset = 'utf8'

    def create_process(self, cmd):
        self.expect = Expect(cmd)

        # Note: The data has to be decoded using the xstr charset
        # because the xstr contents would be sometimes printed along
        # the debugging.
        self.expect.add_map(LOAD, lambda con, 
        data: sys.stdout.write(data.decode(self.charset)))

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
        self.kill_process()
        event.widget.chmode('NORMAL')

    def run(self, event):
        """
        To be implemented.
        """

    def run_args(self, event):
        """
        To be implemented.
        """

    def kill_process(self):
        if self.expect:
            self.expect.terminate()

    def install_handles(self, expect):
        """
        This method is meant to be implemented. It is supposed to 
        extract necessary attributes from the underlying debugger output
        to be dispatched to these methods: 

        Debugger has hit a given line:

            self.handle_line
    
        """

    def send(self, data):
        """
        To implement:

        Example:
            self.expect.send(data.encode(self.encoding))

        """
        pass

    def handle_line(self, expect, filename, line):
        xstr = root.note.find_line(filename, line, self.auto_open)

        if xstr is not None:
            xstr.set_breakpoint(line, self.bp_appearence)
        root.status.set_msg('Debugger stopped at: %s:%s' % (filename, line))
