"""
"""

from cspkg.stderr import QUIET, logger
from itertools import groupby
from cspkg.core import EscsApp
import argparse
import logging
import sys

parser = argparse.ArgumentParser()

parser.add_argument('files', nargs='*', help='Files')
parser.add_argument('-t', '--tab', dest='scheme', 
action='append_const', const=None, default=[], 
help='Instantiate a new tab. Ex: -t -p file0 file1')

parser.add_argument('-p', '--pane', 
action='append', dest='scheme', default=[], nargs='+',  
help='Open files in vertical/horizontal ways -p file0 file1 -p file2')

parser.add_argument('-v', '--verbose', action='store_true',
help='Show exceptions and messages.')

args = parser.parse_args()

lst = [list(g) for k, g in groupby(args.scheme, 
lambda x: not x) if not k]

print('Loading escsrc...')
root = EscsApp()
lst  = lst + [[[ind]] for ind in args.files]

if not args.verbose: 
    logger.setLevel(logging.ERROR)

root.create_escsrc()

if not lst: 
    root.note.create('none')
else: 
    root.note.load(*lst)

root.event_generate('<<Started>>')

def tk_xhook(exctype, value, tb):
    logger.exception('', exc_info=(exctype, value, tb))
root.report_callback_exception = tk_xhook

if args.verbose: 
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(QUIET)
