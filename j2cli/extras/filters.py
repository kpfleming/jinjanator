""" Custom Jinja2 filters """
import os

from jinja2 import is_undefined
import re


def docker_link(value, format='{addr}:{port}'):
    """ Given a Docker Link environment variable value, format it into something else.

    This first parses a Docker Link value like this:

        DB_PORT=tcp://172.17.0.5:5432

    Into a dict:

    ```python
    {
      'proto': 'tcp',
      'addr': '172.17.0.5',
      'port': '5432'
    }
    ```

    And then uses `format` to format it, where the default format is '{addr}:{port}'.

    More info here: [Docker Links](https://docs.docker.com/userguide/dockerlinks/)

    :param value: Docker link (from an environment variable)
    :param format: The format to apply. Supported placeholders: `{proto}`, `{addr}`, `{port}`
    :return: Formatted string
    """
    # pass undefined values on down the pipeline
    if is_undefined(value):
        return value

    # Parse the value
    m = re.match(r'(?P<proto>.+)://' r'(?P<addr>.+):' r'(?P<port>.+)$', value)
    if not m:
        raise ValueError('The provided value does not seems to be a Docker link: {0}'.format(value))
    d = m.groupdict()

    # Format
    return format.format(**d)


def env(varname, default=None):
    """ Use an environment variable's value inside your template.

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
    """
    if default is not None:
        # With the default, there's never an error
        return os.getenv(varname, default)
    else:
        # Raise KeyError when not provided
        return os.environ[varname]
