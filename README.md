# jinjanator

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![CI](https://github.com/kpfleming/jinjanator/workflows/CI%20checks/badge.svg)](https://github.com/kpfleming/jinjanator/actions?query=workflow%3ACI%20checks)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-3812/)
[![License - Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-9400d3.svg)](https://spdx.org/licenses/Apache-2.0.html)
[![Code Style - Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)
[![Types - Mypy](https://img.shields.io/badge/Types-Mypy-blue.svg)](https://github.com/python/mypy)
[![Code Quality - Ruff](https://img.shields.io/badge/Code%20Quality-Ruff-red.svg)](https://github.com/astral-sh/ruff)
[![Project Management - Hatch](https://img.shields.io/badge/Project%20Management-Hatch-purple.svg)](https://github.com/pypa/hatch)
[![Testing - Pytest](https://img.shields.io/badge/Testing-Pytest-orange.svg)](https://github.com/pytest-dev/pytest)

This repo contains `jinjanator`, a CLI tool to render
[Jinja2](https://github.com/pallets/jinja/) templates. It is a fork of
`j2cli`, which itself was a fork of `jinja2-cli`, both of which are no
longer actively maintained.

Open Source software: [Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)

## &nbsp;

Features:

* Jinja2 templating
* INI, YAML, JSON data sources supported
* Environment variables can be used with or without data files
* Plugins can provide additional formats, filters, tests, and global
  functions (see [Plugins](PLUGINS.md) for details).

## Installation

```
pip install jinjanator
```

## Tutorial

Suppose, you have an NGINX configuration file template, `nginx.j2`:

```jinja2
server {
  listen 80;
  server_name {{ nginx.hostname }};

  root {{ nginx.webroot }};
  index index.htm;
}
```

And you have a JSON file with the data, `nginx.json`:

```json
{
    "nginx":{
        "hostname": "localhost",
        "webroot": "/var/www/project"
    }
}
```

This is how you render it into a working configuration file:

```bash
$ jinjanate nginx.j2 nginx.json > nginx.conf
```

The output is saved to `nginx.conf`:

```
server {
  listen 80;
  server_name localhost;

  root /var/www/project;
  index index.htm;
}
```

Alternatively, you can use the `-o nginx.conf` or `--output-file
nginx.conf`options to write directly to the file.

## Tutorial with environment variables

Suppose, you have a very simple template, `person.xml.j2`:

```jinja2
<data><name>{{ name }}</name><age>{{ age }}</age></data>
```

What is the easiest way to use jinjanator here?
Use environment variables in your Bash script:

```bash
$ export name=Andrew
$ export age=31
$ jinjanate /tmp/person.xml.j2
<data><name>Andrew</name><age>31</age></data>
```

## Using environment variables

Even when you use a data file as the data source, you can always
access environment variables using the `env()` function:

```jinja2
Username: {{ login }}
Password: {{ env("APP_PASSWORD") }}
```

Or, if you prefer, as a filter:

```jinja2
Username: {{ login }}
Password: {{ "APP_PASSWORD" | env }}
```

## CLI Reference
`jinjanate` accepts the following arguments:

* `template`: Jinja2 template file to render
* `data`: (optional) path to the data used for rendering.
    The default is `-`: use stdin.

Options:

* `--format FMT, -f FMT`: format for the data file. The default is
  `?`: guess from file extension. Supported formats are YAML (.yaml or
  .yml), JSON (.json), INI (.ini), and dotenv (.env), plus any formats
  provided by plugins you have installed.
* `--format-option OPT`: option to be passed to the parser for the
  data format selected with `--format` (or auto-selected). This can be
  specified multiple times. Refer to the documentation for the format
  itself to learn whether it supports any options.
* `--help, -h`: generates a help message describing usage of the tool.
* `--import-env VAR, -e VAR`: import all environment variables into
    the template as `VAR`.  To import environment variables into the
    global scope, give it an empty string: `--import-env=`.  (This
    will overwrite any existing variables with the same names!)
* `--output-file OUTFILE, -o OUTFILE`: Write rendered template to a
  file.
* `--quiet`: Avoid generating any output on stderr.
* `--undefined`: Allow undefined variables to be used in templates (no
  error will be raised).
* `--version`: prints the version of the tool and the Jinja2 package installed.

There is some special behavior with environment variables:

* When `data` is not provided (data is `-`), `--format` defaults to
  `env` and thus reads environment variables.

## Usage Examples

Render a template using INI-file data source:

    $ jinjanate config.j2 data.ini

Render using JSON data source:

    $ jinjanate config.j2 data.json

Render using YAML data source:

    $ jinjanate config.j2 data.yaml

Render using JSON data on stdin:

    $ curl http://example.com/service.json | jinjanate --format=json config.j2 -

Render using environment variables:

    $ jinjanate config.j2

Or use environment variables from a file:

    $ jinjanate config.j2 data.env

Or pipe it: (note that you'll have to use "-" in this particular case):

    $ jinjanate --format=env config.j2 - < data.env


## Data Formats

### dotenv
Data input from environment variables. This format does not support any options.

Render directly from the current environment variable values:

    $ jinjanate config.j2

Or alternatively, read the values from a dotenv file:

```
NGINX_HOSTNAME=localhost
NGINX_WEBROOT=/var/www/project
NGINX_LOGS=/var/log/nginx/
```

And render with:

    $ jinjanate config.j2 data.env

Or:

    $ env | jinjanate --format=env config.j2

If you're going to pipe a dotenv file into `jinjanate`, you'll need to
use "-" as the second argument:

    $ jinjanate config.j2 - < data.env

### INI
INI data input format. This format does not support any options.

data.ini:

```
[nginx]
hostname=localhost
webroot=/var/www/project
logs=/var/log/nginx
```

Usage:

    $ jinjanate config.j2 data.ini

Or:

    $ cat data.ini | jinjanate --format=ini config.j2

### JSON
JSON data input format. This format does not support any options.

data.json:

```
{
    "nginx":{
        "hostname": "localhost",
        "webroot": "/var/www/project",
        "logs": "/var/log/nginx"
    }
}
```

Usage:

    $ jinjanate config.j2 data.json

Or:

    $ cat data.json | jinjanate --format=ini config.j2

### YAML
YAML data input format. This format does not support any options.

data.yaml:

```
nginx:
  hostname: localhost
  webroot: /var/www/project
  logs: /var/log/nginx
```

Usage:

    $ jinjanate config.j2 data.yml

Or:

    $ cat data.yml | jinjanate --format=yaml config.j2

## Filters

### `env(varname, default=None)`
Use an environment variable's value in the template.

This filter is available even when your data source is something other
than the environment.

Example:

```jinja2
User: {{ user_login }}
Pass: {{ "USER_PASSWORD" | env }}
```

You can provide a default value:

```jinja2
Pass: {{ "USER_PASSWORD" | env("-none-") }}
```

For your convenience, it's also available as a global function:

```jinja2
User: {{ user_login }}
Pass: {{ env("USER_PASSWORD") }}
```

Notice that there must be quotes around the environment variable name
when it is a literal string.

## Credits

This tool was created from [j2cli](https://github.com/kolypto/j2cli),
which itself was created from
[jinja2-cli](https://github.com/mattrobenolt/jinja2-cli). It was
created to bring the project up to 'modern' Python coding, packaging,
and project-management standards, and to support plugins to provide
extensibility.

["Standing on the shoulders of
giants"](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants)
could not be more true than it is in the Python community; this
project relies on many wonderful tools and libraries produced by the
global open source software community, in addition to Python
itself. I've listed many of them below, but if I've overlooked any
please do not be offended :-)

* [Attrs](https://github.com/python-attrs/attrs)
* [Black](https://github.com/psf/black)
* [Hatch-Fancy-PyPI-Readme](https://github.com/hynek/hatch-fancy-pypi-readme)
* [Hatch](https://github.com/pypa/hatch)
* [Jinja2](https://github.com/pallets/jinja/)
* [Mypy](https://github.com/python/mypy)
* [Pluggy](https://github.com/pytest-dev/pluggy)
* [Pytest](https://github.com/pytest-dev/pytest)
* [Ruff](https://github.com/astral-sh/ruff)
* [Towncrier](https://github.com/twisted/towncrier)
