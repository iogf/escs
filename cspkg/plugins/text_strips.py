
from cspkg.core import Command
from re import escape

@Command()
def strip(xstr, chars=' '):
    """
    Strip chars off the beginning of all selected lines.
    if chars is not given it removes spaces.
    """

    xstr.replace_ranges('sel', '^[%s]+' % escape(chars), '')

@Command()
def rstrip(xstr, chars=' '):
    """
    Strip chars off the end of all selected lines.
    if chars is not given it removes spaces.
    """

    xstr.replace_ranges('sel', '[%s]+$' % escape(chars), '')

