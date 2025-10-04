
from os.path import exists, dirname, join
from cspkg.stderr import printd
from cspkg.core import Namespace, Main, Plugin

class ProjectNS(Namespace):
    pass

def get_sentinel_file(path, *args):
    """
    """

    tmp = path
    while True:
        tmp = dirname(tmp)
        for ind in args:
            if exists(join(tmp, ind)):
                return tmp
            elif tmp == dirname(tmp):
                return ''
            
class Project(Plugin):
    sentinels = ('.git', '.svn', '.hg', '._')

    def  __init__(self, xstr):
        super().__init__(xstr)
        self.add_kmap(ProjectNS, Main, '<<LoadData>>', self.set_path, True)
        self.add_kmap(ProjectNS, Main, '<<SaveData>>', self.set_path, True)

    @classmethod
    def c_sentinels(cls, *sentinels):
        cls.sentinels = sentinels
        printd('Project - Setting sentinels = ', cls.sentinels)

    def set_path(self, event):
        """    
        Set the project root automatically.
        """

        self.xstr.project = get_sentinel_file(
        self.xstr.filename, *Project.sentinels)
        printd('Project - Setting project path = ', self.xstr.project)

install = Project


