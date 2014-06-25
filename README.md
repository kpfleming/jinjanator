[![Build Status](https://travis-ci.org/kolypto/j2cli.svg?branch=v0.3.0-0)](https://travis-ci.org/kolypto/j2cli)

j2cli - Jinja2 Command-Line Tool
================================

`j2cli` is a command-line tool for templating in shell-scripts, 
leveraging the [Jinja2](http://jinja.pocoo.org/docs/) library.

Features:

* Jinja2 templating
* Allows to use environment variables! Hello [Docker](http://www.docker.com/) :)
* INI, YAML, JSON data sources supported

Inspired by [mattrobenolt/jinja2-cli](https://github.com/mattrobenolt/jinja2-cli)

## Installation

```
pip install j2cli
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
    
# Reference
`j2` accepts the following arguments:

* `template`: Jinja2 template file to render
* `data`: (optional) path to the data used for rendering. The default is `-`: use stdin

Options:

* `--format, -f`: format for the data file. The default is `?`: guess from file extension.

There is some special behavior with environment variables:

* When `data` is not provided (data is `-`), `--format` defaults to `env` and thus reads environment variables
* When `--format=env`, it can read a special "environment variables" file made like this: `env > /tmp/file.env`

## Formats

### ini

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

### env

Render directly from environment variable values:

    $ j2 config.j2
    
Or read them from a file:

```
NGINX_HOSTNAME=localhost
NGINX_WEBROOT=/var/www/project
NGINX_LOGS=/var/log/nginx/
```

And render with:
    
    $ j2 config.j2 data.env
    $ env | j2 --format=env config.j2.
