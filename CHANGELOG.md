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
