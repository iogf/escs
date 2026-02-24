from os.path import exists, dirname, join
from cspkg.start import root
from re import split, escape
from untwisted.splits import Terminator
from re import search
import socket

class RegexEvent:
    def __init__(self, ssock, regstr, event, encoding='utf8'):
        self.encoding = encoding
        self.regstr   = regstr
        self.event    = event
        ssock.add_map(Terminator.FOUND, self.handle_found)

    def handle_found(self, ssock, data):
        data  = data.decode(self.encoding)
        regex = search(self.regstr, data)

        if regex is not None: 
            ssock.drive(self.event, *regex.groups())

def build_regex(data, delim='.+'):
    """

    """

    data    = split(' +', data)
    pattern = ''
    for ind in range(0, len(data)-1):
        pattern = pattern + escape(data[ind]) + delim
    pattern = pattern + escape(data[-1])
    return pattern

def match_sub_pattern(pattern, lst):
    # pattern = buffer(pattern)
    for indi in lst:
        for indj in range(0, len(pattern)):
                if indi.startswith(pattern[indj:]):
                    yield indi, indj
                    
def error(handle):
    def shell(*args, **kwargs):
        try:
            return handle(*args, **kwargs)
        except Exception as e:
            root.status.set_msg('Error :%s' % e)
            raise
    return shell

def get_project_root(path):
    """
    Return the project root or the file path.
    """

    # In case it receives '/file'
    # and there is '/__init__.py' file.
    if path == dirname(path):
        return path

    while True:
        tmp = dirname(path)
        if not exists(join(tmp, '__init__.py')):
            return path
        path = tmp

def psock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    host, port = sock.getsockname()
    sock.close() 
    return port    

