
from subprocess import Popen, STDOUT, PIPE
from os.path import dirname
from cspkg.tools import build_regex
from cspkg.core import Namespace, Plugin, Main
from cspkg.tools import error
from cspkg.fwin import LinePicker
from cspkg.xstr import Xstr
from cspkg.stderr import printd
from cspkg.start import root
from cspkg.xscan import Get
from re import findall

class SniperNS(Namespace):
    pass

class Sniper(Plugin):
    options = LinePicker()
    # Path to ag program.
    path = 'ag'

    # Dirs where ag will search when in 
    # wide mode.
    dirs = ()

    # Sniper search options.
    file_regex = ''
    ignore     = ''
    multiline  = True

    # Either lax(1), literal(0), regex(2).
    type   = 1
    nocase = False
    wide   = True

    def  __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(SniperNS, Main, '<Alt-s>', self.display_matches)
        self.add_kmap(SniperNS, Main, '<Alt-r>', self.find_matches)

        if not self.dirs:
            printd('Sniper - Sniper.dirs is not set.')

    def display_matches(self, event):
        self.options.display(self.xstr)

    def find_matches(self, event):
        wid = Get(events = {
        '<Return>':self.find, 
        '<Control-i>':self.set_ignore_regex, 
        '<Control-x>':self.set_type_lax, 
        '<Control-r>':self.set_type_regex, 
        '<Control-l>':self.set_type_literal, 
        '<Control-g>':self.set_file_regex, 
        '<Control-s>':self.set_nocase, 
        '<Control-w>':self.set_wide, 
        '<Control-m>':self.set_multiline, 
        '<Escape>':  lambda wid: True})
        
    @classmethod
    def c_path(cls, path='ag'):
        """
        Set the ag path. If ag is known to your environment then
        there is no need to set it.
        """
        pass
        cls.path = path
        printd('Sniper - Setting ag path = ', path)

    @classmethod
    def c_dirs(cls, *dirs):
        """
        Folders where ag will be searching for data.
        """
        cls.dirs = dirs
        printd('Sniper - Setting dirs =', *dirs)

    def set_wide(self, wid):
        Sniper.wide = False if Sniper.wide else True
        root.status.set_msg('Set wide search: %s' % Sniper.wide)

    def set_multiline(self, wid):
        Sniper.multiline = False if Sniper.multiline else True
        root.status.set_msg('Set multiline search: %s' % Sniper.multiline)

    def set_nocase(self, wid):
        Sniper.nocase = False if Sniper.nocase else True
        root.status.set_msg('Set nocase search: %s' % Sniper.nocase)

    def set_ignore_regex(self, wid):
        Sniper.ignore = wid.get()
        root.status.set_msg('Set ignore file regex:%s' % Sniper.ignore)
        wid.delete(0, 'end')

    def set_type_literal(self, wid):
        root.status.set_msg('Set search type: LITERAL')
        Sniper.type = 0

    def set_type_lax(self, wid):
        root.status.set_msg('Set search type: LAX')
        Sniper.type = 1

    def set_type_regex(self, wid):
        root.status.set_msg('Set search type: REGEX')
        Sniper.type = 2

    def set_file_regex(self, wid):
        self.file_regex = wid.get()
        root.status.set_msg('Set file regex:%s' % self.file_regex)
        wid.delete(0, 'end')

    def make_cmd(self, pattern):
        cmd = [self.path, '--nocolor', '--nogroup',
        '--vimgrep', '--noheading']

        if self.ignore:
            cmd.extend(['--ignore', self.ignore])
        if self.file_regex:
            cmd.extend(['-G', self.file_regex])
        if self.nocase:
            cmd.append('-s')
        if not self.multiline:
            cmd.append('--nomultiline')
        else:
            cmd.append('--multiline')

        if self.type == 1:
            cmd.append(build_regex(pattern))
        elif self.type == 2:
            cmd.append(pattern)
        else:
            cmd.extend(['-Q', pattern])

        # When the project path isn't set it searches in the
        # xstr filename dir.
        if not Sniper.wide:
            cmd.append(self.xstr.project 
                if self.xstr.project else 
                    dirname(self.xstr.filename))
        else:
            cmd.extend(Sniper.dirs)
        return cmd

    def run_cmd(self, pattern):
        cmd = self.make_cmd(pattern)
        child = Popen(cmd, stdout=PIPE, stderr=STDOUT, 
        encoding=self.xstr.charset)
        return child.communicate()[0]

    @error
    def find(self, wid):
        """
        """

        pattern = wid.get()
        root.status.set_msg('Set pattern:%s!' % pattern)
        output = self.run_cmd(pattern)
        print(output)

        if output:
            self.fmt_output(output)
        else:
            root.status.set_msg('No results:%s!' % pattern)
        return True

    def fmt_output(self, output):
        regex  = '(.+):([0-9]+):[0-9]+:(.+)' 
        ranges = findall(regex, output)

        self.options.extend(ranges)
        self.options.display(self.xstr)

install = Sniper


