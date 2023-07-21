import codecs
from typing import List, Mapping, Optional

from jinjanator.plugin import (
    Filters,
    Format,
    Formats,
    Tests,
    plugin_filters_hook,
    plugin_formats_hook,
    plugin_tests_hook,
)


def rot13_filter(value: str) -> str:
    return codecs.encode(value, "rot13")


def is_len12_test(value: str) -> bool:
    return len(value) == 12


def spam_format(
    data_string: str,
    options: Optional[List[str]] = None,
) -> Mapping[str, str]:
    if options and options[0] == "ham":
        return {
            "ham": "ham",
            "cheese": "ham and cheese",
            "potatoes": "ham and potatoes",
        }

    return {
        "spam": "spam",
        "cheese": "spam and cheese",
        "potatoes": "spam and potatoes",
    }


@plugin_filters_hook
def plugin_filters() -> Filters:
    return {"rot13": rot13_filter}


@plugin_tests_hook
def plugin_tests() -> Tests:
    return {"len12": is_len12_test}


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {"spam": Format(parser=spam_format, suffixes=[".spam"])}
