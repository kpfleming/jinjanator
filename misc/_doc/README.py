#! /usr/bin/env python

import json
import inspect
from exdoc import doc, getmembers

import j2cli
import j2cli.context
import j2cli.extras.filters


README = {
    'formats': {
        name: doc(f)
        for name, f in j2cli.context.FORMATS.items()
    },
    'extras': {
        'filters': {k: doc(v)
                    for k, v in getmembers(j2cli.extras.filters)
                    if inspect.isfunction(v) and inspect.getmodule(v) is j2cli.extras.filters}
    }
}

assert 'yaml' in README['formats'], 'Looks like the YAML library is not installed!'

print(json.dumps(README))
