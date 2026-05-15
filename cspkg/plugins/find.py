
from cspkg.scan import Read
from cspkg.stderr import printd
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class FindNS(Namespace):
    pass

class Find(Plugin):
    confs = {
        '(FIND)':{'background':'green', 'foreground':'red'}
    }

    nolinestop = False
    regexp = False
    nocase = False
    exact  = False
    elide  = False
    data   = ''
    regex  = ''

    def __init__(self, xstr):
        super().__init__(xstr)
        xstr.tag_update(**self.confs)

        self.add_kmap(FindNS, Normal,'<Alt-slash>', 
        lambda event: Read(events={
        '<Alt-q>': self.set_data,
        '<Alt-o>': self.up, '<Escape>': self.cancel, 
        '<Alt-p>': self.down, '<Return>': self.cancel,
        '<Alt-n>':  self.selection_matches,
        '<Alt-period>': self.sub_current,
        '<Alt-semicolon>': self.sub_selected, 
        '<Alt-comma>': self.sub_all, 
        '<Control-n>': self.toggle_nocase,
        '<Control-x>': self.toggle_regexp,

        '<Control-e>': self.toggle_exact,
        '<Control-i>': self.toggle_elide,
        '<Control-l>': self.toggle_nolinestop},
         default_data=Find.regex, msg='Type a Pattern:'))

    @classmethod
    def c_appearance(cls, confs):
        """
        """

        cls.confs.update(confs)
        printd('Find - Setting confs = ', cls.confs)

    def toggle_nocase(self, read):
        self.nocase = False if self.nocase else True
        root.status.set_msg('nocase=%s' % self.nocase)

    def toggle_regexp(self, read):
        self.regexp = False if self.regexp else True
        root.status.set_msg('regexp=%s' % self.regexp)

    def toggle_exact(self, read):
        self.exact = False if self.exact else True
        root.status.set_msg('exact=%s' % self.exact)

    def toggle_elide(self, read):
        self.elide = False if self.elide else True
        root.status.set_msg('elide=%s' % self.elide)

    def toggle_nolinestop(self, read):
        self.nolinestop = False if self.nolinestop else True
        root.status.set_msg('nolinestop=%s' % self.nolinestop)

    def set_data(self, read):
        Find.data = read.text(clear=True)
        root.status.set_msg('Set replacement: %s' % Find.data)

    def cancel(self, read):
        Find.regex = read.text()
        self.xstr.tag_remove('(FIND)', '1.0', 'end')
        read.done()

    def up(self, read):
        regex = read.text()
        index = self.xstr.ipick('(FIND)', regex, index='insert', 
        stopindex='1.0', backwards=True, regexp=self.regexp, 
        nocase=self.nocase, exact=self.exact, 
        elide=self.elide)

    def down(self, read):
        regex = read.text()
        index = self.xstr.ipick('(FIND)', regex, 
        index='insert', stopindex='end', regexp=self.regexp, 
        nocase=self.nocase, exact=self.exact, 
        elide=self.elide)

    def selection_matches(self, read):
        """
        """

        self.xstr.tag_remove('(FIND)', '1.0', 'end')
        regex = read.text()

        matches = self.xstr.check_ranges('sel', regex, 
        regexp=self.regexp, nocase=self.nocase, exact=self.exact, 
        elide=self.elide)

        for _, index0, index1 in matches:
            self.xstr.tag_add('(FIND)', index0, index1)

        count = len(self.xstr.tag_ranges('(FIND)'))
        root.status.set_msg('Found: %s' % count)

    def sub_current(self, read):
        """
        """

        regex = read.text()
        index = self.xstr.tag_nextrange('(FIND)', '1.0')
        self.xstr.replace(regex, Find.data, index[0], 
        regexp=self.regexp, nocase=self.nocase, 
        exact=self.exact, elide=self.elide)

    def sub_selected(self, read):
        """
        """
        regex = read.text()
        count = self.xstr.replace_ranges('sel',
        regex, Find.data, regexp=self.regexp, nocase=self.nocase, 
        exact=self.exact, elide=self.elide)

        root.status.set_msg('Replaced matches: %s' % count)

    def sub_all(self, read):
        """
        """
        regex = read.text()
        count = self.xstr.replace_all(regex, Find.data, 
        '1.0', 'end', regexp=self.regexp, nocase=self.nocase, 
        exact=self.exact, elide=self.elide)
        root.status.set_msg('Replaced matches: %s' % count)

install = Find



