from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Mapping,
    Protocol,
    Sequence,
    TypeVar,
    cast,
)

import pluggy  # type: ignore[import]

from attrs import define


if TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import TypeAlias


@define(kw_only=True)
class Format:
    parser: Callable[[str, list[str] | None], Mapping[str, Any]]
    suffixes: list[str]


F = TypeVar("F", bound=Callable[..., Any])
hookspec = cast(Callable[[F], F], pluggy.HookspecMarker("jinjanator"))

Formats: TypeAlias = Mapping[str, Format]
Filters: TypeAlias = Mapping[str, Callable[..., Any]]
Globals: TypeAlias = Mapping[str, Callable[..., Any]]
Tests: TypeAlias = Mapping[str, Callable[..., Any]]

PluginFormatsHook: TypeAlias = Callable[[], Formats]
PluginFiltersHook: TypeAlias = Callable[[], Filters]
PluginTestsHook: TypeAlias = Callable[[], Tests]
PluginGlobalsHook: TypeAlias = Callable[[], Globals]

plugin_formats_hook = cast(
    Callable[[PluginFormatsHook], PluginFormatsHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_filters_hook = cast(
    Callable[[PluginFiltersHook], PluginFiltersHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_tests_hook = cast(
    Callable[[PluginTestsHook], PluginTestsHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_globals_hook = cast(
    Callable[[PluginGlobalsHook], PluginGlobalsHook],
    pluggy.HookimplMarker("jinjanator"),
)


class PluginHooks(Protocol):
    @staticmethod
    @hookspec
    def plugin_formats() -> Formats:
        """Returns dict of formats"""

    @staticmethod
    @hookspec
    def plugin_filters() -> Filters:
        """Returns dict of filter functions"""

    @staticmethod
    @hookspec
    def plugin_globals() -> Globals:
        """Returns dict of global functions"""

    @staticmethod
    @hookspec
    def plugin_tests() -> Tests:
        """Returns dict of test functions"""


class PluginHookCallers(Protocol):
    @staticmethod
    def plugin_formats() -> Sequence[Formats]:
        """Returns list of dicts of formats"""

    @staticmethod
    def plugin_filters() -> Sequence[Filters]:
        """Returns list of dicts of filter functions"""

    @staticmethod
    def plugin_globals() -> Sequence[Globals]:
        """Returns list of dicts of global functions"""

    @staticmethod
    def plugin_tests() -> Sequence[Tests]:
        """Returns list of dicts of test functions"""
