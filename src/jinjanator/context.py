from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, TextIO


if TYPE_CHECKING:  # pragma: no cover
    from .plugin import Format


def read_context_data(
    fmt: Format,
    f: TextIO | None,
    environ: Mapping[str, str],
    import_env: str | None = None,
    format_options: list[str] | None = None,
) -> Mapping[str, Any]:
    if not f:
        msg = "no input supplied"
        raise ValueError(msg)

    context: dict[str, Any] = {}

    context.update(fmt.parser(f.read(), format_options))

    if import_env is not None:
        if import_env == "":
            context.update(environ)
        else:
            context[import_env] = environ

    # Done
    return context
