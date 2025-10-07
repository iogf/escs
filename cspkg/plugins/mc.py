from subprocess import check_output, check_call
from os.path import expanduser, dirname, join
from cspkg.core import Namespace, Plugin
from cspkg.plugins.normal_mode import Normal
from cspkg.stderr import printd
from cspkg.tools import error
from cspkg.start import root
from cspkg.xscan import Xscan

# Wrapper around these functions to get the
# error shown on the statusbar.
check_output = error(check_output)
check_call  = error(check_call)

class McNS(Namespace):
    pass

class Mc(Plugin):
    confs = {'(MC-DIRECTORY)': {'foreground': 'red'},
    '(MC-FILE)': {'foreground': 'yellow'}}

    clipboard = []

    def __init__(self, xstr):
        super().__init__(xstr)
        self.ph   = expanduser('~')

        self.add_kmap(McNS, Normal, '<Key-H>', lambda e: self.up())
        self.add_kmap(McNS, Normal, '<Key-L>', lambda e: self.down())
        self.add_kmap(McNS, Normal, '<Key-Y>', lambda e: self.cp())
        self.add_kmap(McNS, Normal, '<Key-T>', lambda e: self.mv())
        self.add_kmap(McNS, Normal, '<Key-R>', lambda e: self.rm())
        self.add_kmap(McNS, Normal, '<Key-K>', lambda e: self.select())
        self.add_kmap(McNS, Normal, '<Key-B>', lambda e: self.clear_clipboard())
        self.add_kmap(McNS, Normal, '<Key-G>', lambda e: self.list_clipboard())
        self.add_kmap(McNS, Normal, '<Key-F>', lambda e: self.info())
        self.add_kmap(McNS, Normal, '<Key-N>', lambda e: self.rename())
        self.add_kmap(McNS, Normal, '<Key-E>', lambda e: self.create_dir())
        self.add_kmap(McNS, Normal, '<Key-I>', self.load_path)
        self.add_kmap(McNS, Normal, '<Key-J>', lambda e:self.ls(self.ph))

        for indi, indj in self.confs.items():
            self.xstr.tag_config(indi, **indj)

    @classmethod
    def c_appearance(cls, dir, file):
        """
        Used to configure foreground/background for directory entries.

        Check Tkinter Text widget tags for more info.
        """

        cls.confs['(MC-DIRECTORY)'] = dir
        cls.confs['(MC-FILE)']      = file

        printd('(Mc) Setting dir/file appearance confs = ', cls.confs)

    def list_clipboard(self):
        self.xstr.delete('1.0', 'end')
        self.xstr.insert('1.0', 'Files in the clipboard!\n\n')
        self.xstr.insert('end', '\n'.join(Mc.clipboard))

    def clear_clipboard(self):
        del Mc.clipboard[:]
        root.status.set_msg('Cleared mc clipboard!')

    def select(self):
        filename = self.xstr.get('insert linestart', 'insert lineend')
        Mc.clipboard.append('"%s"' % filename)
        root.status.set_msg('Appended %s!' % filename)

    def down(self):
        ph = self.xstr.get('insert linestart', 'insert lineend')
        self.ls(ph)

    def up(self):
        ph = dirname(self.ph)
        self.ls(ph)

    def info(self):
        filename = self.xstr.get(
        'insert linestart', 'insert lineend')

        data = check_output('stat "%s"' % filename, shell=1, encoding='utf8')
        self.xstr.delete('1.0', 'end')
        self.xstr.append(data, '(MC-FILE)')

    def ls(self, ph):
        """
        """

        self.xstr.delete('1.0', 'end')

        data = check_output('find "%s" -maxdepth 1 -type d' % 
        ph, shell=1, encoding='utf8')
        self.xstr.append(data, '(MC-DIRECTORY)')

        data = check_output('find "%s" -maxdepth 1 -type f' % 
        ph, shell=1, encoding='utf8')
        self.xstr.append(data, '(MC-FILE)')

        # If the previous commands ran succesfully
        # then set the path.
        self.ph = ph

    def cp(self):
        destin = self.xstr.get('insert linestart', 'insert lineend')
        code   = check_call('cp -R %s "%s"' % (
            ' '.join(Mc.clipboard), destin), shell=1)

        root.status.set_msg('Files copied!')
        del Mc.clipboard[:]
        self.ls(self.ph)

    def mv(self):
        destin = self.xstr.get('insert linestart', 'insert lineend')
        code   = check_call('mv %s "%s"' % (
            ' '.join(Mc.clipboard), destin), shell=1)

        root.status.set_msg('Files moved!')
        del Mc.clipboard[:]
        self.ls(self.ph)

    def rename(self):
        path = self.xstr.get(
        'insert linestart', 'insert lineend')

        root.status.set_msg('(Mc) Rename file:')
        xscan    = Xscan()
        destin = join(dirname(path), xscan.data)
        code   = check_call('mv "%s" %s' % (path, 
        destin), shell=1)

        root.status.set_msg('File renamed!')
        self.ls(self.ph)

    def rm(self):
        code = check_call('rm -fr %s' % ' '.join(Mc.clipboard), shell=1)
        del Mc.clipboard[:]
        root.status.set_msg('Deleted files!')
        self.ls(self.ph)

    def create_dir(self):
        path = self.xstr.get('insert linestart', 'insert lineend')


        root.status.set_msg('Type dir name:')
        xscan  = Xscan()
        path = join(path, xscan.data)
        code = check_call('mkdir "%s"' % path, shell=1)

        root.status.set_msg('Folder created!')
        self.ls(self.ph)

    def load_path(self, event):
        """
        Dump the contents of the file whose path is under the cursor.
        """
    
        filename = self.xstr.get(
            'insert linestart', 'insert lineend')
        root.note.load([[filename]])
    

install = Mc



