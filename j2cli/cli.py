"""
jinja2-cli
==========

License: BSD, see LICENSE for more details.
"""

from j2cli import __version__

class InvalidDataFormat(Exception): pass
class InvalidInputData(Exception): pass
class MalformedJSON(InvalidInputData): pass
class MalformedINI(InvalidInputData): pass
class MalformedYAML(InvalidInputData): pass
class MalformedQuerystring(InvalidInputData): pass


# Global list of available format parsers on your system
# mapped to the callable/Exception to parse a string into a dict
formats = {}

# json - simplejson or packaged json as a fallback
try:
    import simplejson
    formats['json'] = (simplejson.loads, simplejson.decoder.JSONDecodeError, MalformedJSON)
except ImportError:
    try:
        import json
        formats['json'] = (json.loads, ValueError, MalformedJSON)
    except ImportError:
        pass


# ini - Nobody likes you.
try:
    # Python 2
    import ConfigParser
except ImportError:
    # Python 3
    import configparser as ConfigParser

def _parse_ini(data):
    import StringIO
    class MyConfigParser(ConfigParser.ConfigParser):
        def as_dict(self):
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop('__name__', None)
            return d
    p = MyConfigParser()
    p.readfp(StringIO.StringIO(data))
    return p.as_dict()
formats['ini'] = (_parse_ini, ConfigParser.Error, MalformedINI)


# yaml - with PyYAML
try:
    import yaml
    formats['yaml'] = (yaml.load, yaml.YAMLError, MalformedYAML)
except ImportError:
    pass


# querystring - querystring parsing
def _parse_qs(data):
    """ Extend urlparse to allow objects in dot syntax.

    >>> _parse_qs('user.first_name=Matt&user.last_name=Robenolt')
    {'user': {'first_name': 'Matt', 'last_name': 'Robenolt'}}
    """
    try:
        import urlparse
    except ImportError:
        import urllib.parse as urlparse
    dict_ = {}
    for k, v in urlparse.parse_qs(data).items():
        v = map(lambda x: x.strip(), v)
        v = v[0] if len(v) == 1 else v
        if '.' in k:
            pieces = k.split('.')
            cur = dict_
            for idx, piece in enumerate(pieces):
                if piece not in cur:
                    cur[piece] = {}
                if idx == len(pieces) - 1:
                    cur[piece] = v
                cur = cur[piece]
        else:
            dict_[k] = v
    return dict_
formats['querystring'] = (_parse_qs, Exception, MalformedQuerystring)


import os
import sys
from argparse import ArgumentParser

import jinja2
from jinja2 import Environment, FileSystemLoader


def cli(args):
    if args.data == '-':
        data = sys.stdin.read()
    else:
        data = open(os.path.join(os.getcwd(), os.path.expanduser(args.data))).read()

    try:
        data = formats[args.format][0](data)
    except formats[args.format][1]:
        raise formats[args.format][2](u'%s ...' % data[:60])
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(os.getcwd()))
    sys.stdout.write(env.get_template(args.template).render(data).encode('utf-8'))
    sys.exit(0)


def main():
    default_format = 'json'
    if default_format not in formats:
        default_format = sorted(formats.keys())[0]

    parser = ArgumentParser()
    parser.add_argument('template')
    parser.add_argument('data', nargs='?', default='-',
            help='input data. Defaults to stdin if none specified')
    parser.add_argument('--format', default=default_format,
            choices=formats.keys(),
            help='format of input variables')
    parser.add_argument('--version', action='version',
            version='jinja2-cli {} - Jinja2 {}'.format(__version__, jinja2.__version__))
    args = parser.parse_args()

    if args.template == 'help':
        parser.print_help()
        sys.exit(1)

    if args.format not in formats:
        raise InvalidDataFormat(args.format)

    cli(args)
    sys.exit(0)
