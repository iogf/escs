
from cspkg.core import Command
from cspkg.start import root
from re import findall

@Command()
def wc(xstr):
    data = xstr.get('1.0', 'end')
    root.status.set_msg('Count of words:%s' % len(findall('\W+', data)))

@Command()
def cpsel(xstr, sep='\n'):
    """
    """

    xstr.cpsel(sep)

@Command()
def ctsel(xstr, sep='\n'):
    """
    """
    xstr.ctsel(sep)

