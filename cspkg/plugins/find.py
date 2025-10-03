
from cspkg.xscan import Get
from cspkg.stderr import printd
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class FindNS(Namespace):
    pass

class Find(Plugin):
    confs = {
        'background':'green', 'foreground':'white'
    }

    opts  = {'nolinestop': False, 'regexp': False,
    'nocase': True, 'exact': False,'elide': False}

    data  = ''
    regex = ''

    def __init__(self, xstr):
        super().__init__(xstr)
        xstr.tag_config('(CATCHED)', self.confs)

        self.add_kmap(FindNS, Normal,
        '<Alt-slash>', lambda event: self.start())

    @classmethod
    def c_appearance(cls, **confs):
        """
        """

        cls.confs.update(confs)
        printd('Find - Setting confs = ', cls.confs)

    def start(self):
        get = Get(events={
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
        default_data=Find.regex)

    def toggle_nocase(self, wid):
        self.opts['nocase'] = False if self.opts['nocase'] else True
        root.status.set_msg('nocase=%s' % self.opts['nocase'])

    def toggle_regexp(self, wid):
        self.opts['regexp'] = False if self.opts['regexp'] else True
        root.status.set_msg('regexp=%s' % self.opts['regexp'])

    def toggle_exact(self, wid):
        self.opts['exact'] = False if self.opts['exact'] else True
        root.status.set_msg('exact=%s' % self.opts['exact'])

    def toggle_elide(self, wid):
        self.opts['elide'] = False if self.opts['elide'] else True
        root.status.set_msg('elide=%s' % self.opts['elide'])

    def toggle_nolinestop(self, wid):
        self.opts['nolinestop'] = False if self.opts['nolinestop'] else True
        root.status.set_msg('nolinestop=%s' % self.opts['nolinestop'])

    def set_data(self, wid):
        Find.data = wid.get()
        wid.delete(0, 'end')
        root.status.set_msg('Set replacement: %s' % Find.data)

    def cancel(self, wid):
        Find.regex = wid.get()
        self.xstr.tag_remove('(CATCHED)', '1.0', 'end')
        return True

    def up(self, wid):
        regex = wid.get()
        index = self.xstr.ipick('(CATCHED)', regex, index='insert', 
        stopindex='1.0', backwards=True, **self.opts)

    def down(self, wid):
        regex = wid.get()
        index = self.xstr.ipick('(CATCHED)', regex, 
        index='insert', stopindex='end', **self.opts)

    def selection_matches(self, wid):
        """
        """

        self.xstr.tag_remove('(CATCHED)', '1.0', 'end')
        regex = wid.get()

        matches = self.xstr.check_ranges(
        'sel', regex, **self.opts)

        for _, index0, index1 in matches:
            self.xstr.tag_add('(CATCHED)', index0, index1)

        count = len(self.xstr.tag_ranges('(CATCHED)'))
        root.status.set_msg('Found: %s' % count)

    def sub_current(self, wid):
        """
        """

        regex = wid.get()
        index = self.xstr.tag_nextrange('(CATCHED)', '1.0')
        self.xstr.replace(regex, Find.data, index[0], **self.opts)

    def sub_selected(self, wid):
        """
        """
        regex = wid.get()
        count = self.xstr.replace_ranges('sel',
        regex, Find.data, **self.opts)

        root.status.set_msg('Replaced matches: %s' % count)

    def sub_all(self, wid):
        """
        """
        regex = wid.get()
        count = self.xstr.replace_all(regex, 
            Find.data, '1.0', 'end', **self.opts)
        root.status.set_msg('Replaced matches: %s' % count)

install = Find



