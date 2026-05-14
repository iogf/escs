from cspkg.tools import build_regex
from subprocess import Popen, STDOUT, PIPE
from cspkg.fwin import LinePicker
from cspkg.scan import Read
from cspkg.start import root
from os.path import basename
from cspkg.core import Namespace, Plugin, Main

class FSnifferNS(Namespace):
    pass

class FSniffer(Plugin):
    options = LinePicker(title='Fsniffer')
    wide = True

    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(FSnifferNS, Main, '<Alt-y>', 
        lambda event: Read(events={'<Return>' : self.find,
        '<Control-w>':self.set_wide, '<<Idle>>': self.update_pattern,
        '<Escape>': lambda read: read.done()}, msg='Type a File/Path:'))

        self.add_kmap(FSnifferNS, Main, '<Alt-t>', 
        lambda event: self.options.display(self.xstr))
    
    @classmethod
    def set_wide(cls, read):
        FSniffer.wide = False if FSniffer.wide else True
        root.status.set_msg('Set wide search: %s' % FSniffer.wide)

    def update_pattern(self, read):
        pattern = build_regex(read.text(), '.*')
        root.status.set_msg('File pattern: %s' % pattern)

    def make_cmd(self, pattern):
        # When FSniffer.wide is False it searches in the current 
        # Xstr instance project.
        cmd   = ['locate', '--limit', '200']
        regex = build_regex(pattern, '.*')

        if self.wide or not self.xstr.project:
            cmd.extend(['--regexp', regex])
        else:
            cmd.extend(['--regexp', '%s.*%s' % (
                self.xstr.project, regex)])

        # Used to filter only files because locate doesn't support 
        # searching only for files.
        cmd = '%s | %s' % (' '.join(cmd), '''while read -r file; do
          [ -d "$file" ] || printf '%s\n' "$file"; done''')
        return cmd

    def run_cmd(self, pattern):
        cmd   = self.make_cmd(pattern)
        child = Popen(cmd, stdout=PIPE, stderr=STDOUT, 
        encoding=self.xstr.charset, shell=True)

        output = child.communicate()[0]
        return output

    def find(self, read):
        pattern = read.text()
        output = self.run_cmd(pattern)
        read.done()

        if output:
            self.fmt_output(output)
        else:
            root.status.set_msg('No results:%s!' % pattern)

    def fmt_output(self, output):
        output = output.strip('\n').rstrip('\n')
        ranges = output.split('\n')
        ranges = [ind for ind in ranges
            if ranges]

        ranges = [(ind, '0', basename(ind)) for ind in ranges]
        self.options.extend(ranges)
        self.options.display(self.xstr)

install = FSniffer

