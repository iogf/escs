
import os.path
from cspkg.core import Namespace, Plugin
from cspkg.plugins.extra_mode import Extra
from cspkg.plugins.normal_mode import Normal

class CodeCommentsNS(Namespace):
    pass

table   = { 
    '.py'   :'#',
    '.java'  :'//',
    '.c'    :'//',
    '.sh'   :'#',
    '.js'   :'//',
    '.cpp'  :'//',
    '.html' :'//',
    '.go'   :'//',
    '.rb' :'#',
}

class CodeComments(Plugin):
    default = '#'

    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(CodeCommentsNS, Extra, '<Key-C>', self.remove_comment)
        self.add_kmap(CodeCommentsNS, Extra, '<Key-c>', self.add_comment)
    
    def add_comment(self, event):
        """
        It adds inline comment to selected lines based on the file extesion.
        """
    
        comment = table.get(os.path.splitext(self.xstr.filename)[1], self.default)
        self.xstr.replace_ranges('sel', '^ *|^\t*', 
        lambda data, index0, index1: '%s%s ' % (data, comment))
        self.xstr.clear_selection()
        self.chmode(Normal)
    
    def remove_comment(self, event):
        """
        It removes the inline comments.
        """
    
        comment = table.get(os.path.splitext(self.xstr.filename)[1], self.default)
        self.xstr.replace_ranges('sel', '^ *%s ?|^\t*%s ?' % (comment, comment), 
        lambda data, index0, index1: data.replace(
            '%s ' % comment, '').replace(comment, ''))
        self.xstr.clear_selection()
        self.chmode(Normal)

install = CodeComments

