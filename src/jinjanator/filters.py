from __future__ import annotations

import os

from .plugin import Filters, Globals, plugin_filters_hook, plugin_globals_hook


def env(varname: str, default: str | None = None) -> str:
    """Use an environment variable's value inside your template.

    This filter is available even when your data source is something other that the environment.

    Example:
    -------
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

    # Raise KeyError when not provided
    return os.environ[varname]


@plugin_filters_hook
def plugin_filters() -> Filters:
    return {"env": env}


@plugin_globals_hook
def plugin_globals() -> Globals:
    return {"env": env}
