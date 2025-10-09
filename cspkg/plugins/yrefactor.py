
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

class YrefactorNS(Namespace):
    pass

class Python(Mode):
    pass

class PythonRefactor(Plugin):
    def __init__(self, xstr):
        super().__init__(xstr)
        self.files = None
        self.add_kmap(YrefactorNS, Python, '<Key-R>', self.rename)
        self.add_kmap(YrefactorNS, Python, '<Key-A>', self.static_analysis)
        self.add_kmap(YrefactorNS, Python, '<Key-M>', self.move)

    def static_analysis(self, event):
        path = (self.xstr.project if self.xstr.project 
        else get_project_root(self.xstr.filename))

        project = Project(path)
        mod     = path_to_resource(project, self.xstr.filename)

        libutils.analyze_module(project, mod)
        project.close()

    def on_general_case(self, change):
        """
        Should be called when self.files is updated.
        """

        for ind in change.get_changed_resources():
           instance = self.files.get(ind.real_path)
           if instance is not None: 
               instance.load_data(ind.real_path)

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

        self.xstr.chmode(Normal)
        root.status.set_msg('Resources moved!')

        
    def update_instances(self, changes):
        """
        """

        # Avoid having to calculate it multiple times.
        self.files = Xstr.get_opened_files(root)
        for ind in changes.changes:
            if isinstance(ind, (MoveResource,)):
                self.on_move_resource(ind)
            else:
                self.on_general_case(ind)

    def on_move_resource(self, change):
        """
        Should be called when self.files is updated.
        """
        old, new = change.get_changed_resources()
        instance = self.files.get(old.real_path)

        # When the file is not updated then no need to load it.
        if instance: instance.load_data(new.real_path)

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

        print('\nRope - Renamed resource ..\n')
        print(changes.get_description())
        self.chmode(Normal)
        root.status.set_msg('Resources renamed!')
        project.close()

install = PythonRefactor

