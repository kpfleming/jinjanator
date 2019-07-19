## 0.3.12 (2019-08-18)
* Fix: use `env` format from stdin

## 0.3.10 (2019-06-07)
* New: `env()` is now available as a function
* New: can now customize the `Environment` object
* Fixed documentation

## 0.3.9 (2019-06-04)
* New: customize.py that lets you customize :)
* Fixed a bug with setup.py and yaml

## 0.3.8 (2019-04-29)
* Enabled Jinja2 extensions: i18n, do, loopcontrols

## 0.3.7 (2019-04-23)
* The new `{{ VAR_NAME |env }}` filter lets you use environment variables in every template.

## 0.3.6 (2019-03-21)
* Fixed support for Python 2.6
* Dropped Python 2.6 from unit-tests~~~~
* Fixed a warning issued by PyYAML. 
  See [issue #33](https://github.com/kolypto/j2cli/issues/33)

## 0.3.5 (2019-01-03)
* New option: `--undefined` that allows undefined variables
* Fix: unicode support in environment variables

## 0.3.4 (2018-12-26)
* `-o outfile` option writes to a file

## 0.3.3
* Python 3 support. 
  Supported versions: 2.6, 2.7, 3.6, 3.7
* New CLI option: `--import-env` that imports environment variables into the template
* New options: `--filters` and `--tests` that import custom Jinja2 filters from a Python file
* Fix: trailing newline is not removed anymore
* Fix: env vars with "=" in values are now parsed correctly
* Fix: now unicode templates & contexts are fully supported
