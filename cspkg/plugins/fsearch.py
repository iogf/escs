"""
"""

from cspkg.tools import build_regex
from subprocess import Popen, STDOUT, PIPE
from cspkg.scan import Read
from cspkg.start import root
from cspkg.plugins.normal_mode import Normal
from cspkg.core import Namespace, Plugin

class FSearchNS(Namespace):
    pass

class FSearch(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.output = ''

        self.add_kmap(FSearchNS, Normal, '<Key-S>', self.reload_results)
        self.add_kmap(FSearchNS, Normal, '<Key-C>',  lambda event: 
        Read(events={'<Return>' : self.find, '<<Idle>>': self.update_pattern, 
        '<Escape>': lambda read: read.done()}))

    def reload_results(self, event):
        self.xstr.swap(self.output, '1.0', 'end')
        root.status.set_msg('Previous located files.')

    def update_pattern(self, read):
        pattern = build_regex(read.text(), '.*')
        root.status.set_msg('File pattern: %s' % pattern)

    def run_cmd(self, pattern):
        cmd   = ['locate', '--limit', '200']
        regex = build_regex(pattern, '.*')
        cmd.extend(['--regexp', regex])

        child = Popen(cmd, stdout=PIPE, stderr=STDOUT, 
        encoding=self.xstr.charset)

        output = child.communicate()[0]
        return output

    def find(self, read):
        pattern = read.text()
        self.output = self.run_cmd(pattern)
        self.xstr.swap(self.output, '1.0', 'end')
        root.status.set_msg('Locate results: %s' % self.output.count('\n'))
        read.done()

install = FSearch
