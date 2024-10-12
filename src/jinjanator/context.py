from collections.abc import Mapping
from typing import Any, Optional, TextIO

from jinjanator_plugins import (
    Format,
)


def read_context_data(
    fmt: Format,
    f: Optional[TextIO],
    environ: Mapping[str, str],
    import_env: Optional[str] = None,
) -> Mapping[str, Any]:
    if not f:
        msg = "no input supplied"
        raise ValueError(msg)

    context: dict[str, Any] = {}

    result = fmt.parse(f.read())

    context |= result

    if import_env is not None:
        if import_env == "":
            context |= environ
        else:
            context[import_env] = environ

    return context
