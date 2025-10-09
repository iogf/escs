
from cspkg.core import Command
from re import escape

@Command()
def strip(area, chars=' '):
    """
    Strip chars off the beginning of all selected lines.
    if chars is not given it removes spaces.
    """

    area.tag_xsub('sel', '^[%s]+' % escape(chars), '')

@Command()
def rstrip(area, chars=' '):
    """
    Strip chars off the end of all selected lines.
    if chars is not given it removes spaces.
    """

    area.tag_xsub('sel', '[%s]+$' % escape(chars), '')

