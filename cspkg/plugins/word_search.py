from cspkg.fwin import LinePicker
from cspkg.core import Plugin, Namespace
from cspkg.plugins.normal_mode import Normal
from cspkg.xscan import Xscan
from itertools import groupby
from re import escape
from cspkg.start import root

class WordSearchNS(Namespace):
    pass

class WordSearch(Plugin):
    options = LinePicker()

    def __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(WordSearchNS, Normal, '<Key-M>', self.match)
        self.add_kmap(WordSearchNS, Normal, '<Key-V>', 
        lambda event: self.options.display(self.xstr))

    def match(self, event):
        """

        """

        xscan  = Xscan()
        data = xscan.data.split(' ')
        find = lambda ind: self.xstr.find(
        escape(ind).lower(), '1.0', step='+1l linestart')

        seq = self.match_regions(find, data)
        if not seq:
            root.status.set_msg('No pattern found!')
        else:
            self.fmt_details(seq)

    def fmt_details(self, seq):
        matches = ((self.xstr.filename, line, 
            self.xstr.get_line('%s.0' % line)) 
                for count, line in seq)
        matches = tuple(matches)
        self.options.extend(matches)
        self.options.display(self.xstr)
        root.status.set_msg('Found: %s' % len(matches))
 
    def match_regions(self, find, data):
        regions = []
    
        for ind in data:
            for ch, index0, index1 in find(ind):
                regions.append((int(index0.split('.')[0]),  ch))

        regions.sort()
        seq = groupby(regions, lambda ind: ind[0])
        matches = self.sort_matches(seq, data)
        return matches

    def sort_matches(self, seq, data):
        matches = []

        for line, group in seq:
            count = 0
            for line, word in group:
                if word in data:
                    count = count + 1
            matches.append((count, line))
        matches.sort(reverse=True)
        return matches

install = WordSearch

