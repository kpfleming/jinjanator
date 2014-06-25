import sys

#region Parsers

def _parse_ini(data_string):
    """ Parse INI
    :type data_string: basestring
    :rtype: dict
    """
    from io import BytesIO

    # Override
    class MyConfigParser(ConfigParser.ConfigParser):
        def as_dict(self):
            """ Export as dict
            :rtype: dict
            """
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop('__name__', None)
            return d

    # Parse
    ini = MyConfigParser()
    ini.readfp(BytesIO(data_string))

    # Export
    return ini.as_dict()

def _parse_json(data_string):
    """ Parse JSON
    :type data_string: basestring
    :rtype: dict
    """
    return json.loads(data_string)

def _parse_yaml(data_string):
    """ Parse YAML
    :type data_string: basestring
    :rtype: dict
    """
    return yaml.load(data_string)

def _parse_env(data_string):
    """ Parse environment variables file
    :type data_string: str|dict
    :rtype: dict
    """
    # Parse
    if isinstance(data_string, basestring):
        data = filter(
            lambda l: len(l) == 2 ,
            (
                map(
                    str.strip,
                    line.split('=')
                )
                for line in data_string.split("\n"))
        )
    else:
        data = data_string

    # Finish
    return data


FORMATS = {
    'ini':  _parse_ini,
    'json': _parse_json,
    'yaml': _parse_yaml,
    'env': _parse_env
}

#endregion



#region Imports

# JSON: simplejson | json
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
         del FORMATS['json']

# INI: Python 2 | Python 3
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

# YAML
try:
    import yaml
except ImportError:
    del FORMATS['yaml']

#endregion



def read_context_data(format, f, environ):
    """ Read context data into a dictionary
    :param format: Data format
    :type format: str
    :param f: Data file stream, or None
    :type f: file|None
    :return: Dictionary with the context data
    :rtype: dict
    """
    # Special case: environment variables
    if format == 'env' and f is None:
        return _parse_env(environ)

    # Read data string stream
    data_string = f.read()

    # Parse it
    if format not in FORMATS:
        raise ValueError('{} format unavailable'.format(format))
    return FORMATS[format](data_string)
