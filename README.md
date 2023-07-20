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

This repo contains `jinjanator`, a CLI tool to render [Jinja2][2]
templates. It is a fork of `j2cli`, which itself was a fork of
`jinja2-cli`, both of which are no longer maintained.

Open Source software: [Apache License 2.0][3]

## &nbsp;

Features:

* Jinja2 templating
* INI, YAML, JSON data sources supported
* Allows the use of environment variables in templates!

## Installation

```
pip install j2cli
```

## Tutorial

Suppose, you want to have an nginx configuration file template, `nginx.j2`:

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
$ j2 -f json nginx.j2 nginx.json > nginx.conf
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

Alternatively, you can use the `-o nginx.conf` option.

## Tutorial with environment variables

Suppose, you have a very simple template, `person.xml`:

```jinja2
<data><name>{{ name }}</name><age>{{ age }}</age></data>
```

What is the easiest way to use j2 here?
Use environment variables in your bash script:

```bash
$ export name=Andrew
$ export age=31
$ j2 /tmp/person.xml
<data><name>Andrew</name><age>31</age></data>
```

## Using environment variables

Even when you use yaml or json as the data source, you can always access environment variables
using the `env()` function:

```jinja2
Username: {{ login }}
Password: {{ env("APP_PASSWORD") }}
```


## Usage

Compile a template using INI-file data source:

    $ j2 config.j2 data.ini

Compile using JSON data source:

    $ j2 config.j2 data.json

Compile using YAML data source (requires PyYAML):

    $ j2 config.j2 data.yaml

Compile using JSON data on stdin:

    $ curl http://example.com/service.json | j2 --format=json config.j2

Compile using environment variables (hello Docker!):

    $ j2 config.j2

Or even read environment variables from a file:

    $ j2 --format=env config.j2 data.env

Or pipe it: (note that you'll have to use the "-" in this particular case):

    $ j2 --format=env config.j2 - < data.env


# Reference
`j2` accepts the following arguments:

* `template`: Jinja2 template file to render
* `data`: (optional) path to the data used for rendering.
    The default is `-`: use stdin. Specify it explicitly when using env!

Options:

* `--format FMT, -f FMT`: format for the data file. The default is `?`: guess from file extension.
* `--import-env VAR, -e VAR`: import all environment variables into the template as `VAR`.
    To import environment variables into the global scope, give it an empty string: `--import-env=`.
    (This will overwrite any existing variables!)
* `--output-file OUTFILE, -o OUTFILE`: Write rendered template to a file
* `--undefined`: Allow undefined variables to be used in templates (no error will be raised)

There is some special behavior with environment variables:

* When `data` is not provided (data is `-`), `--format` defaults to `env` and thus reads environment variables
* When `--format=env`, it can read a special "environment variables" file made like this: `env > /tmp/file.env`

## Formats


### env
Data input from environment variables.

Render directly from the current environment variable values:

    $ j2 config.j2

Or alternatively, read the values from a dotenv file:

```
NGINX_HOSTNAME=localhost
NGINX_WEBROOT=/var/www/project
NGINX_LOGS=/var/log/nginx/
```

And render with:

    $ j2 config.j2 data.env
    $ env | j2 --format=env config.j2

If you're going to pipe a dotenv file into `j2`, you'll need to use "-" as the second argument to explicitly:

    $ j2 config.j2 - < data.env

### ini
INI data input format.

data.ini:

```
[nginx]
hostname=localhost
webroot=/var/www/project
logs=/var/log/nginx/
```

Usage:

    $ j2 config.j2 data.ini
    $ cat data.ini | j2 --format=ini config.j2

### json
JSON data input format

data.json:

```
{
    "nginx":{
        "hostname": "localhost",
        "webroot": "/var/www/project",
        "logs": "/var/log/nginx/"
    }
}
```

Usage:

    $ j2 config.j2 data.json
    $ cat data.json | j2 --format=ini config.j2

### yaml
YAML data input format.

data.yaml:

```
nginx:
  hostname: localhost
  webroot: /var/www/project
  logs: /var/log/nginx
```

Usage:

    $ j2 config.j2 data.yml
    $ cat data.yml | j2 --format=yaml config.j2


## Filters

### `env(varname, default=None)`
Use an environment variable's value inside your template.

This filter is available even when your data source is something other that the environment.

Example:

```jinja2
User: {{ user_login }}
Pass: {{ "USER_PASSWORD"|env }}
```

You can provide the default value:

```jinja2
Pass: {{ "USER_PASSWORD"|env("-none-") }}
```

For your convenience, it's also available as a function:

```jinja2
User: {{ user_login }}
Pass: {{ env("USER_PASSWORD") }}
```

Notice that there must be quotes around the environment variable name

[2]: https://github.com/pallets/jinja/
[3]: https://spdx.org/licenses/Apache-2.0.html
