"""
"""

from cspkg.fwin import CompletionWindow, Option
from os.path import expanduser, join, exists, dirname
from base64 import b64encode, b64decode
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE
from shutil import copyfile
from cspkg.core import Plugin, Namespace, Command, rcenv, Main
from requests.exceptions import RequestException
from cspkg.plugins.extra_mode import Extra
from cspkg.plugins.insert_mode import Insert
from cspkg.start import root
from cspkg.stderr import printd
from cspkg.tools import psock
import atexit
import requests
import pprint
# import random
import hashlib
import hmac
import json
import os

HMAC_LENGTH  = 32

# Vim filetypes mapping.
FILETYPES = {
'.c': 'c',
'.py': 'python',
'.go': 'go',
'.c++':'cpp',
'.js':'javascript',
'.java': 'java',
}

DEFAULT_FILETYPE = None

class YcmdNS(Namespace):
    pass

class YcmdServer:
    def __init__(self, path, port, settings_file, idle_suicide=300):
        """
        """

        self.settings_file = settings_file
        self.settings = None
        self.path = path
        self.port = port
        self.url = 'http://127.0.0.1:%s' % port 
        self.idle_suicide = idle_suicide
        self.hmac_secret = os.urandom(HMAC_LENGTH)

        with open(self.settings_file) as fd:
          self.settings = json.loads(fd.read())

        hmac_secret = b64encode(self.hmac_secret).decode('utf8 ')
        self.settings['hmac_secret'] = hmac_secret

        with NamedTemporaryFile(mode = 'w+', delete = False) as tmpfile:
            json.dump(self.settings, tmpfile)

        # It is necessary to use stdout=PIPE, stderr=PIPE otherwise
        # we get ycmd outputing stuff even in non verbose mode.
        self.cmd = ['python', '-m', 'ycmd', 
        '--port', str(self.port), '--options_file', tmpfile.name, 
        '--idle_suicide_seconds', str(self.idle_suicide)]

        self.daemon = Popen(self.cmd,  cwd=self.path, 
        stdout=PIPE, stdin=PIPE, stderr=PIPE)
        atexit.register(self.kill)

    def kill(self):
        self.daemon.kill()

    def reject_xconf(self, path):
        data = {
           'filepath': path,
        }

        url = '%s/ignore_extra_conf_file' % self.url
        hmac_secret = self.hmac_req('POST', 
        '/ignore_extra_conf_file', data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers)
        printd('Ycmd - xconf rejected...', path)
        printd('Ycmd - /ignore_extra_conf_file response:')
        printd(pprint.pformat(req.json()))

    def load_xconf(self, path):
        """
        """

        data = {
           'filepath': path,
        }

        url = '%s/load_extra_conf_file' % self.url
        hmac_secret = self.hmac_req('POST', 
        '/load_extra_conf_file', data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers)

        printd('Ycmd - Loading extra conf...', path)
        printd('Ycmd - /load_extra_conf_file response:')
        printd(pprint.pformat(req.json()))

    def is_alive(self):
        """
        """
        hmac_secret = self.hmac_req('GET', 
        '/healthy', '', self.hmac_secret)

        url = '%s/healthy' % self.url
        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.get(url, headers=headers)
 
        printd('Ycmd - /healthy response status..\n', req.status_code)
        printd('Ycmd - /healthy response.\n') 
        printd(pprint.pformat(req.json()))

        return req

    def debug_info(self, line, col, path, data):
        data = {'line_num': line,
       'column_num': col, 'filepath': path, 'file_data': data}

        url = '%s/debug_info' % self.url
        hmac_secret = self.hmac_req('POST', '/debug_info', 
        data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers, timeout=7)
        printd('Ycmd - debug_info response.\n')
        printd(pprint.pformat(req.json()))

        return req

    def detailed_diagnostic(self, line, col, path, data):
        data = {'line_num': line,
       'column_num': col, 'filepath': path, 'file_data': data}

        url = '%s/detailed_diagnostic' % self.url
        hmac_secret = self.hmac_req('POST', '/detailed_diagnostic', 
        data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers, timeout=7)
        printd('Ycmd - detailed_diagnostic response.\n')
        printd(pprint.pformat(req.json()))

        return req

    def e_send(self, name,  line, col, path, data):
        """
        Send event notification.
        """

        data = {'line_num': line,
       'column_num': col,'filepath': path,
       'file_data': data, 'event_name': name}

        url = '%s/event_notification' % self.url
        hmac_secret = self.hmac_req('POST', '/event_notification', 
        data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers, timeout=7)
        printd('Ycmd - /event_notification', name)
        printd('Ycmd - /event_notification status', req.status_code)
        printd('Ycmd - /event_notification response.\n')
        printd(pprint.pformat(req.json()))

        return req

    def post(self, *args, **kwargs):
        """
        Abstract the workings of HTTP POST method to validate
        HMAC in responses.
        """

        req = requests.post(*args, **kwargs)
        is_valid = self.is_vhmac(req.text, 
        req.headers['X-YCM-HMAC'], self.hmac_secret)

        if not is_valid:
            raise RuntimeError('Invalid HMAC response')
        return req

    def get(self, *args, **kwargs):
        """
        Abstract the workings of HTTP GET method to validate
        HMAC in responses.
        """
        
        req = requests.get(*args, **kwargs)
        is_valid = self.is_vhmac(req.text, 
        req.headers['X-YCM-HMAC'], self.hmac_secret)

        if not is_valid:
            raise RuntimeError('Invalid HMAC response')
        return req

    def completions(self, line, col, path, data, 
        dir, target=None, cmdargs=None):

        data = {'line_num': line, 'column_num': col,
        'filepath': path, 'file_data': data}

        url = '%s/completions' % self.url

        hmac_secret = self.hmac_req('POST', '/completions', 
        data, self.hmac_secret)

        headers = {
            'X-YCM-HMAC': hmac_secret,
        }

        req = self.post(url, json=data, headers=headers, timeout=7)
        printd('Ycmd - /completions response..')
        printd(pprint.pformat(req.json()))

        return self.build_docs(req.json())

    def build_docs(self, data):
        return [Option(ind.get('insertion_text', ''), 
            self.fmt_option(ind)) for ind in data['completions']]

    def fmt_option(self, option):
        kind = option.get('kind', '')
        details = option.get('detailed_info', '')
        data = option.get('extra_data', {})
        location = data.get('location', {})
        path = location.get('filepath', '')
        line = location.get('line_num', '')

        return '\n\n'.join(('Kind: %s' % kind, 
        'Details: %s' % details, 'Path: %s\nLine:%s' % (path, line)))
            
    def hmac_req(self, method, path, body, hmac_secret):
        """
        Calculate hmac for request. The algorithm is based on what is seen in
        https://github.com/ycm-core/ycmd/blob/master/examples/example_client.py
        at CreateHmacForRequest function.
        """

        method = bytes(method, encoding = 'utf8' )
        path   = bytes(path, encoding = 'utf8' )

        # In case of HTTP GET it can't use json.dumps because it returns
        # "''" that makes the hmac be calculated wrongly.
        body = json.dumps(body, ensure_ascii = False) if body else ''
        body = bytes(body, encoding = 'utf8' )

        method = bytes(hmac.new(hmac_secret, 
        method, digestmod = hashlib.sha256).digest())

        path = bytes(hmac.new(hmac_secret, 
        path, digestmod = hashlib.sha256).digest())

        body = bytes(hmac.new(hmac_secret, 
        body, digestmod = hashlib.sha256).digest())

        joined = bytes().join((method, path, body))

        data = bytes(hmac.new(hmac_secret, joined, 
        digestmod = hashlib.sha256).digest())

        return str(b64encode(data), encoding='utf8 ')

    def is_vhmac(self, body, hmac_header, hmac_secret):
        """
        Check the response hmac.
        """

        body = body.encode('utf8')
        a = b64decode(hmac_header)
        b = bytes(hmac.new(hmac_secret,
        msg = body, digestmod = hashlib.sha256).digest())

        if len(a) != len(b):
            return False
       
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0
       
class YcmdWindow(CompletionWindow):
    """
    """

    def __init__(self, xstr, server, *args, **kwargs):
        source    = xstr.get('1.0', 'end')
        line, col = xstr.indexsplit()

        code = FILETYPES.get(xstr.extension, DEFAULT_FILETYPE)
        data = {xstr.filename: 
        {'filetypes': [code], 
        'contents': source}}

        completions = server.completions(line, col + 1, 
        xstr.filename, data, dirname(xstr.filename))
        CompletionWindow.__init__(self, xstr, completions, *args, **kwargs)

class YcmdCompletion(Plugin):
    server = None
    autoload_xconf = False
    path = None
    port = None
    dconf = None

    def __init__(self, xstr):
        super().__init__(xstr)
        self.enabled = False
        self.add_kmap(YcmdNS, Extra, '<Key-n>', 
        self.on_ready, spread=True, add=True)

        self.add_kmap(YcmdNS, Extra, '<Key-n>', 
        self.enable_completion, spread=True, add=True)

    def enable_completion(self, event):
        if self.enabled == False:
            self.install_handles()
        return self.enabled

    def install_handles(self):
        self.add_kmap(YcmdNS, Main, '<Destroy>', self.on_unload, True)
        self.add_kmap(YcmdNS, Extra, '<Key-period>', self.complete)
        self.add_kmap(YcmdNS, Main, '<<LoadData>>', self.on_ready, True)
        
        # self.add_kmap(YcmdNS, Main, '<FocusIn>', self.on_buffervisit, True)
        # It seems when FileReadyToParse is sent many times ycmd hangs
        # then the request is not sent due to requests timeout.
        self.add_kmap(YcmdNS, Main, '<<SaveData>>', self.on_filesave, True)
        root.status.set_msg('Ycmd - Enabled on  %s' % self.xstr.filename)
        self.enabled = True

    def complete(self, event):
        YcmdWindow(event.widget, self.server)
        self.chmode(Insert)

    def on_unload(self, event):
        """
        """

        code = FILETYPES.get(self.xstr.extension, DEFAULT_FILETYPE)
        data = {self.xstr.filename:  
        {'filetypes': [code], 'contents': ''}}
        req = self.server.e_send('BufferUnload', 1, 1, self.xstr.filename, data)

    def on_buffervisit(self, event):
        code = FILETYPES.get(self.xstr.extension, DEFAULT_FILETYPE)
        data = {self.xstr.filename:  
        {'filetypes': [code], 'contents': self.xstr.get('1.0', 'end')}}

        line, col = self.xstr.indexsplit()
        req = self.server.e_send('BufferVisit', line, 
        col + 1, self.xstr.filename, data)

    def on_filesave(self, event):
        """
        """
        code = FILETYPES.get(self.xstr.extension, DEFAULT_FILETYPE)
        data = {self.xstr.filename:  
        {'filetypes': [code], 'contents': self.xstr.get('1.0', 'end')}}

        line, col = self.xstr.indexsplit()
        req = self.server.e_send('FileSave', line, 
        col + 1, self.xstr.filename, data)

    def on_ready(self, event):
        """
        This method sends the ReadyToParseEvent to ycmd whenever a file is
        opened or saved. It is necessary to start some 
        ycmd language completers.

        When there is a global .ycm_extra_conf.py in the home dir
        then it is loaded automatically otherwise a message is
        displayed to the user to load it using lycm.
        """
        code = FILETYPES.get(self.xstr.extension, DEFAULT_FILETYPE)
        data = {self.xstr.filename:  
        {'filetypes': [code], 'contents': self.xstr.get('1.0', 'end')}}

        line, col = self.xstr.indexsplit()
        req = self.server.e_send('FileReadyToParse', line, 
        col + 1, self.xstr.filename, data)

        rsp = req.json()
        if req.status_code == 500:
            self.on_exception(rsp)

    def on_exception(self, rsp):
        exc = rsp.get('exception')
        if exc and exc.get('TYPE') == 'UnknownExtraConf':
            self.on_unknown_xconf(exc['extra_conf_file'])
    
    def on_unknown_xconf(self, xconf):
        """
        """

        # When ycmd finds a .ycm_extra_conf.py it is ignored automatically.
        if not self.autoload_xconf:
            self.server.reject_xconf(xconf)
        else:
            self.server.load_xconf(xconf)

        # When extension is not detected it should still send
        # FileReadyToParse?
        code = FILETYPES.get(self.xstr.extension, DEFAULT_FILETYPE)

        # We send FileReadyToParse again.
        data = {self.xstr.filename:  
        {'filetypes': [code], 
        'contents': self.xstr.get('1.0', 'end')}}

        line, col = self.xstr.indexsplit()
        req = self.server.e_send('FileReadyToParse', line, 
        col + 1, self.xstr.filename, data)

    @classmethod
    def c_autoload_xconf(cls, value):
        cls.autoload_xconf = value
        printd('Ycmd - Option autoload_xconf set: ', cls.autoload_xconf)

    @classmethod
    def c_path(cls, path):
        cls.path = path

    @classmethod
    def c_port(cls, port):
        cls.port = port if port else psock()
        printd('Ycmd - Port set %s.' % port) 

    @classmethod
    def setup(cls):
        """ 
        Create the default_settings.json file in case it doesn't exist.
        The file is located in the home dir. It also starts ycmd server.

        Check ycmd docs for details.
        """

        cls.server = YcmdServer(cls.path, cls.port,  cls.dconf)
        printd('Ycmd - Starting server ...')

        root.after(250000, cls.keep_alive)
        rcenv['lycm'] = cls.lycm
        rcenv['dycm'] = cls.dycm
        rcenv['rycm'] = cls.rycm

    @classmethod
    def init_dconf(cls):
        cls.dconf = join(expanduser('~'), '.default_settings.json')
        if not exists(cls.dconf): 
            copyfile(join(dirname(__file__), 
                'default_settings.json'), cls.dconf)

    @classmethod
    def keep_alive(cls):
        freq = 250000
        if cls.server is not None:
            root.after(freq, cls.keep_alive)
        cls.server.is_alive()

    @classmethod
    def rycm(cls):
        cls.server.daemon.kill()
        cls.server  = YcmdServer(cls.path, cls.port,  cls.dconf)
        root.status.set_msg('Ycmd - Restarted.')
        
    @classmethod
    def dycm(cls):
        """
        """
        code = FILETYPES.get(Command.xstr.extension, DEFAULT_FILETYPE)
        data = {Command.xstr.filename:  
        {'filetypes': [code], 
        'contents': Command.xstr.get('1.0', 'end')}}

        cls.server.debug_info(1, 1, Command.xstr.filename, data)

    @classmethod
    def lycm(cls, path=None):
        """
        """

        home = expanduser('~')
        path = path if path else join(home, '.ycm_extra_conf.py')

        cls.server.load_xconf(path)
        root.status.set_msg('Loaded %s' % path)

@Command('init_ycm')
def init_ycm(xstr, path):
    """ 
    Generate a ycm_extra_conf.py file in the given path dir to specify
    compilation flags for a project. This is necessary to get
    semantic analysis for c-family languages.

    Check ycmd docs for more details.
    """

    conf = join(path, '.ycm_extra_conf.py')
    if exists(conf):
        root.status.set_msg('File overwritten: %s' % conf)
    copyfile(join(dirname(__file__), 'ycm_extra_conf.py'), conf)
    return conf

install = YcmdCompletion

