from cspkg.core import Command
from cspkg.start import root

@Command()
def decode(xstr, name):
    try:
        xstr.decode(name)
    except UnicodeDecodeError:
        root.status.set_msg('Failed! Charset %s' % name)

@Command()
def charset(xstr, name):
    xstr.charset = name
    root.status.set_msg('Charset %s set.' % name)

