"""Custom Jinja2 filters."""
import os
from typing import Optional


def env(varname: str, default: Optional[Optional[str]] = None) -> str:
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
