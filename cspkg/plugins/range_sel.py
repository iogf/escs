
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal

class RangeSelNS(Namespace):
    pass

class RangeSel(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(RangeSelNS, Normal, '<Key-v>', self.sel_add)
        self.add_kmap(RangeSelNS, Normal, '<Key-x>', self.sel_del)
        self.add_kmap(RangeSelNS, Normal, '<Key-g>', self.sel_mark)
        self.xstr.mark_set('(SEL_MARK)', '1.0')

    def sel_mark(self, event):
        """  
        """

        self.xstr.mark_set('(SEL_MARK)', 'insert')
        index = self.xstr.index('(SEL_MARK)')
        root.status.set_msg('Dropped selection mark: %s' % index)

    def sel_add(self, event):
        """
        """

        self.xstr.addsel('(SEL_MARK)', 'insert')
        index0 = self.xstr.index('(SEL_MARK)')
        index1 = self.xstr.index('insert')
        root.status.set_msg('Added selection: (%s, %s) ' % (index0, index1))

    def sel_del(self, event):
        """ 
        """

        self.xstr.rmsel('(SEL_MARK)', 'insert')
        index0 = self.xstr.index('(SEL_MARK)')
        index1 = self.xstr.index('insert')
        root.status.set_msg('Removed selection: (%s, %s) ' % (index0, index1))

install = RangeSel

