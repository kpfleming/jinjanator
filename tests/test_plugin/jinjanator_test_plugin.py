from collections.abc import Iterable, Mapping
from typing import Optional

from jinjanator_plugins import (
    Extensions,
    Filters,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
    Formats,
    Globals,
    Identity,
    Tests,
    plugin_extensions_hook,
    plugin_filters_hook,
    plugin_formats_hook,
    plugin_globals_hook,
    plugin_identity_hook,
    plugin_tests_hook,
)


def null_filter(
    value: str,  # noqa: ARG001
) -> str:
    return ""


def null_test(
    value: str,  # noqa: ARG001
) -> bool:
    return False


class NullFormat:
    name = "null"
    suffixes: Optional[Iterable[str]] = (".null",)
    option_names: Optional[Iterable[str]] = ("val", "uns")

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        if options:
            for option in options:
                if option == "val":
                    raise FormatOptionValueError(self, option, "", "")
                if option == "uns":
                    raise FormatOptionUnsupportedError(self, option, "")

    def parse(
        self,
        data_string: str,  # noqa: ARG002
    ) -> Mapping[str, str]:
        return {}


@plugin_identity_hook
def plugin_identities() -> Identity:
    return "test"


@plugin_filters_hook
def plugin_filters() -> Filters:
    return {"null": null_filter}


@plugin_tests_hook
def plugin_tests() -> Tests:
    return {"null": null_test}


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {NullFormat.name: NullFormat}


@plugin_globals_hook
def plugin_globals() -> Globals:
    return {"null": null_filter}


@plugin_extensions_hook
def plugin_extensions() -> Extensions:
    return ["jinja2.ext.do"]
