from __future__ import annotations

from typing import Mapping

from jinjanator_plugins import (
    Filters,
    Format,
    FormatOptionUnknownError,
    FormatOptionValueError,
    Formats,
    Globals,
    Identity,
    Tests,
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


def null_format(
    data_string: str,  # noqa: ARG001
    options: list[str] | None = None,
) -> Mapping[str, str]:
    if options:
        for option in options:
            if option == "val":
                raise FormatOptionValueError(option)

            raise FormatOptionUnknownError(option)

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
    return {"null": Format(parser=null_format, suffixes=[".null"])}


@plugin_globals_hook
def plugin_globals() -> Globals:
    return {"null": null_filter}
