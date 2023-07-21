from typing import Any, Dict, List, Mapping, Optional, TextIO

from .plugin import Format


def read_context_data(
    fmt: Format,
    f: Optional[TextIO],
    environ: Mapping[str, str],
    import_env: Optional[str] = None,
    format_options: Optional[List[str]] = None,
) -> Mapping[str, Any]:
    if not f:
        raise ValueError("no input supplied")

    context: Dict[str, Any] = {}

    context.update(fmt.parser(f.read(), format_options))

    if import_env is not None:
        if import_env == "":
            context.update(environ)
        else:
            context[import_env] = environ

    # Done
    return context
