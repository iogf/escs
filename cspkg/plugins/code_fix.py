
from cspkg.xscan import Xscan
from rope.base.project import Project
from cspkg.tools import get_project_root, error
from cspkg.xstr import Xstr
from rope.refactor.rename import Rename
from rope.base.libutils import path_to_resource
from rope.base.change import MoveResource
from cspkg.start import root
from rope.base import libutils
from rope.refactor.move import create_move
from cspkg.core import Namespace, Plugin, Mode
from cspkg.plugins.normal_mode import Normal
from os.path import dirname

class CodeFixNS(Namespace):
    pass

class Python(Mode):
    pass

class CodeFix(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.files = None
        self.add_kmap(CodeFixNS, Python, '<Key-r>', self.rename)
        self.add_kmap(CodeFixNS, Python, '<Key-a>', self.static_analysis)
        self.add_kmap(CodeFixNS, Python, '<Key-m>', self.move)

    def static_analysis(self, event):
        path = (self.xstr.project if self.xstr.project 
        else get_project_root(self.xstr.filename))

        project = Project(path)
        mod = path_to_resource(project, self.xstr.filename)

        libutils.analyze_module(project, mod)
        project.close()

    def rename_struct(self, change):
        """
        Should be called when self.files is updated.
        """
        for ind in change.get_changed_resources():
           xstr = self.files.get(ind.real_path)
           print('rename struct type:', type(ind))
           if xstr is not None: 
               xstr.load_data(ind.real_path)

    @error
    def move(self, event):
        """
        """
        xscan = Xscan()

        tmp0    = self.xstr.get('1.0', 'insert')
        offset  = len(tmp0)

        path = (self.xstr.project if self.xstr.project 
        else get_project_root(self.xstr.filename))
        project = Project(path)

        project = Project(path)
        mod     = path_to_resource(project, self.xstr.filename)
        mover   = create_move(project, mod, offset)
        destin  = path_to_resource(project, xscan.data)
        changes = mover.get_changes(destin)
        project.do(changes)

        self.update_instances(changes)
        project.close()

        self.chmode(Normal)
        root.status.set_msg('Resources moved!')

        
    def update_instances(self, changes):
        """
        """

        # Avoid having to calculate it multiple times.
        self.files = Xstr.get_opened_files(root)
        for ind in changes.changes:
            if isinstance(ind, (MoveResource,)):
                self.move_resource(ind)
            else:
                self.rename_struct(ind)

    def move_resource(self, change):
        """
        Should be called when self.files is updated.
        """
        old, new = change.get_changed_resources()
        xstr = self.files.get(old.real_path)
        print('move resource type:', type(change))

        # When the file is not updated then no need to load it.
        if  xstr is not None: 
            xstr.load_data(new.real_path)

    @error
    def rename(self, name):
        xscan = Xscan()

        tmp0    = self.xstr.get('1.0', 'insert')
        offset  = len(tmp0)
        path = (self.xstr.project if self.xstr.project 
        else get_project_root(self.xstr.filename))

        # Obs: It demand to have an __init__.ṕy 
        # in the directory to work.
        project = Project(path)
        mod     = path_to_resource(project, self.xstr.filename)
        renamer = Rename(project, mod, offset)
        changes = renamer.get_changes(xscan.data)
        project.do(changes)

        self.update_instances(changes)

        print('\nCodeFix - Renamed resource ..\n')
        print(changes.get_description())
        self.chmode(Normal)
        root.status.set_msg('Resources renamed!')
        project.close()

install = CodeFix

