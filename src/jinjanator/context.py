from collections.abc import Mapping
from typing import Any, TextIO

from jinjanator_plugins import (
    Format,
)


def read_context_data(
    fmt: Format,
    f: TextIO | None,
    environ: Mapping[str, str],
    import_env: str | None = None,
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
