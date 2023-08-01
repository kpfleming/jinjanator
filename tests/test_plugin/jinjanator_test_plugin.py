from __future__ import annotations

from typing import Mapping

from jinjanator_plugins import (
    Filters,
    Format,
    FormatOptionUnsupportedError,
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


class NullFormat:
    @staticmethod
    def parser(
        data_string: str,  # noqa: ARG004
        options: list[str] | None = None,
    ) -> Mapping[str, str]:
        if options:
            for option in options:
                if option == "val":
                    raise FormatOptionValueError(NullFormat.fmt, option, "", "")
                if option == "uns":
                    raise FormatOptionUnsupportedError(NullFormat.fmt, option, "")

        return {}

    fmt = Format(name="null", parser=parser, suffixes=[".null"], options=["val", "uns"])


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
    return {NullFormat.fmt.name: NullFormat.fmt}


@plugin_globals_hook
def plugin_globals() -> Globals:
    return {"null": null_filter}
