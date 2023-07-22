# Plugins

Jinjanator can be extended through the use of plugins; these are
Python packages installed into the same environment as the tool
itself, which use special markers to 'hook' into various
features. There is an example in the [plugin_example](plugin_example)
directory which demonstrates three of the four possible hooks.

Plugins can provide:

* *formats*: data parsers used to extract data from input files.

* *filters*: functions used in Jinja2 templates to transform data.

* *tests*: functions used in Jinja2 templates to make decisions in
  conditional logic.

* *globals*: functions used in Jinja2 templates to obtain data from
  external sources.

For more details on the functionality and requirements for 'filters',
'tests', and 'globals', refer to the Jinja2 documentation.

## Basic structure

A minimal plugin consists of two files:

* `pyproject.toml`: provides package and project information, and
  build instructions

* Python source: provides functions to implement the desired features,
  and hook markers to plug them into Jinjanator

### pyproject.toml

```toml
[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=61",
]

[project]
name = "jinjanator-plugin-example"
version = "0.0.0"
dependencies = [
  "jinjanator",
]

[tool.setuptools]
py-modules = ["jinjanator_plugin_example"]

[project.entry-points.jinjanator]
example = "jinjanator_plugin_example"
```

#### build-system

Any PEP517-compatible build system can be used, for this simple
example `setuptools` is being used.

#### project

The `name` and `version` are required to build a package containing
the plugin; the `dependencies` are required because the plugin will
import code from `jinjanator` itself.

#### tool.setuptools

This section tells `setuptools` to include a single source file (not a package
directoy) into the distribution. Note that this is a *module name*,
not a *file name*, so there is no `.py` extension.

#### project.entry-points.jinjanator

This is the first part of the 'magic' mechanism which allows
Jinjanator to find the plugin. The entry here (which can use any name,
but should be related to the project name in order to avoid conflicts)
creates an 'entry point' which Jinjanator can use to find the plugin;
the value is the name of the module which Jinjanator should import to
find the plugin's hooks (and must match the name specified in the
`tool.setuptools` section).

### jinjanator_plugin_example.py

```python
import codecs

from jinjanator.plugin import (
    Format,
    plugin_filters_hook,
    plugin_formats_hook,
    plugin_tests_hook,
)


def rot13_filter(value):
    return codecs.encode(value, "rot13")


def is_len12_test(value):
    return len(value) == 12


def spam_format(data_string, options):
    if options and options[0] == "ham":
        return {
            "ham": "ham",
            "cheese": "ham and cheese",
            "potatoes": "ham and potatoes",
        }

    return {
        "spam": "spam",
        "cheese": "spam and cheese",
        "potatoes": "spam and potatoes",
    }


@plugin_filters_hook
def plugin_filters():
    return {"rot13": rot13_filter}


@plugin_tests_hook
def plugin_tests():
    return {"len12": is_len12_test}


@plugin_formats_hook
def plugin_formats():
    return {"spam": Format(parser=spam_format, suffixes=[".spam"])}
```

Note that the real example makes use of type annotations, but they
have been removed here for simplicity.

#### Imports

The imports from `jinjanator.plugin` are necessary for the plugin to
mark the hooks it wishes to use to provide additional features.

#### rot13_filter

A simple filter function which applies the `rot13` transformation to
the string value it receives.

#### is_len12_test

A simple test function which returns `True` if the value it receives
has length 12.

#### spam_format

A simple format function which ignores the content provided (which
Jinjanator would have read from a data file), and instead returns one
of two canned responses based on whether the `ham` option has been
provided by the user.

#### plugin_filters

The hook function which will be called by Jinjanator to allow this
plugin to register any filter functions it provides; the
`@plugin_filters_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a filter
function name (the name which will be used in the Jinja2 template to
invoke the function) and the corresponding value being a reference to
the function itself.

Note that the function *must* be named `plugin_filters`; it is the
second part of the 'magic' mechanism mentioned above.

#### plugin_tests

The hook function which will be called by Jinjanator to allow this
plugin to register any test functions it provides; the
`@plugin_tests_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a test
function name (the name which will be used in the Jinja2 template to
invoke the function) and the corresponding value being a reference to
the function itself.

Note that the function *must* be named `plugin_tests`; it is the
second part of the 'magic' mechanism mentioned above.

#### plugin_formats

The hook function which will be called by Jinjanator to allow this
plugin to register any format functions it provides; the
`@plugin_formats_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a format
function name (the name which will be used in the `--format` argument
to Jinjanator, if needed) and the corresponding value being a Format
object containing a reference to the format function itself and an
optional list of file suffixes which can be matched to this format
during format auto-detection.

Note that the function *must* be named `plugin_formats`; it is the
second part of the 'magic' mechanism mentioned above.
