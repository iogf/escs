
from cspkg.start import root
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal
from cspkg.plugins.extra_mode import Extra

class ClipboardNS(Namespace):
    pass

class Clipboard(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)

        self.add_kmap(ClipboardNS, Normal, '<Key-r>', self.paste_after)
        self.add_kmap(ClipboardNS, Normal, '<Key-e>', self.paste_before)
        
        self.add_kmap(ClipboardNS, Normal, '<Key-y>', self.copy)
        self.add_kmap(ClipboardNS, Normal, '<Key-u>', self.cut)
        self.add_kmap(ClipboardNS, Normal, '<Key-t>', self.paste)
        self.add_kmap(ClipboardNS, Extra, '<Key-y>', self.copy_with_sep)
        self.add_kmap(ClipboardNS, Extra, '<Key-t>', self.paste_block)
        self.add_kmap(ClipboardNS, Extra, '<Key-u>', self.cut_with_sep)
        self.add_kmap(ClipboardNS, Normal, '<Key-d>', self.del_sel),
        self.add_kmap(ClipboardNS, Normal, '<Key-D>', self.del_line),

    def del_line(self, event):
        self.xstr.edit_separator()
        self.xstr.delete('insert linestart', 'insert +1l linestart')
        self.xstr.see('insert')

    def del_sel(self, event):
        """
        It deletes all selected text.
        """
        self.xstr.edit_separator()
        self.xstr.swap_ranges('sel', '', '1.0', 'end')

    def cut(self, event):
        """
        """

        self.xstr.ctsel()
        root.status.set_msg('Text was cut!')

    def copy(self, event):
        """
        """

        self.xstr.cpsel()
        root.status.set_msg('Text was copied!')

    def copy_with_sep(self, event):
        """
        """
        self.xstr.cpsel('\n')
        root.status.set_msg('Text was copied with sep: \\n!')
        self.chmode(Normal)

    def cut_with_sep(self, event):
        self.xstr.ctsel('\n')
        root.status.set_msg('Text was cut with sep: \\n!')
        self.chmode(Normal)

    def paste(self, event):
        """
        Paste text at the cursor position.
        """

        data = self.xstr.clipboard_get()
        self.xstr.edit_separator()
        self.xstr.insert('insert', data)
        root.status.set_msg('Text was pasted!')

    def paste_after(self, event):
        """
        Paste text one line down the cursor position.
        """

        data = self.xstr.clipboard_get()
        self.xstr.edit_separator()
        self.xstr.insert('insert +1l linestart', data)
        root.status.set_msg('Text was pasted!')


    def paste_before(self, event):
        """
        Paste text one line up the cursor position.
        """

        data = self.xstr.clipboard_get()
        self.xstr.edit_separator()
        self.xstr.insert('insert linestart', data)
        root.status.set_msg('Text was pasted!')

    def paste_block(self, event):
        data      = self.xstr.clipboard_get()
        data      = data.split('\n')
        line, col = self.xstr.indexsplit()

        self.xstr.edit_separator()
        for ind in range(0, len(data)):
            self.xstr.insert('%s.%s' % (line + ind, col), data[ind])

        self.chmode(Normal)
        root.status.set_msg('Text block was pasted')

install = Clipboard


