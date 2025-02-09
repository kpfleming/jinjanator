"""
Add Customize/Filters/Tests functionality from J2CLI

This code was ported from https://github.com/kolypto/j2cli
"""

import contextlib
import inspect

from argparse import ArgumentParser
from collections.abc import Mapping
from importlib.machinery import SourceFileLoader
from types import FunctionType, ModuleType
from typing import Any, ClassVar, Optional

import jinja2


def imp_load_source(module_name: str, module_path: str) -> ModuleType:
    """
    Drop-in Replacement for imp.load_source() function in pre-3.12 python

    Source: https://github.com/python/cpython/issues/104212
    """
    loader = SourceFileLoader(module_name, module_path)
    module = ModuleType(loader.name)
    loader.exec_module(module)
    return module


class CustomizationModule:
    """The interface for customization functions, defined as module-level
    functions"""

    def __init__(self, module: Optional[ModuleType] = None):
        if module is not None:
            # Import every module function as a method on ourselves
            with contextlib.suppress(AttributeError):
                for name in self._IMPORTED_METHOD_NAMES:
                    setattr(self, name, getattr(module, name))

    # stubs

    def j2_environment_params(self) -> dict[str, Any]:
        return {}

    def j2_environment(self, env: jinja2.Environment) -> jinja2.Environment:
        return env

    def alter_context(self, context: Mapping[str, Any]) -> Mapping[str, Any]:
        return context

    def extra_filters(self) -> Mapping[str, FunctionType]:
        return {}

    def extra_tests(self) -> Mapping[str, FunctionType]:
        return {}

    _IMPORTED_METHOD_NAMES: ClassVar = [
        f.__name__
        for f in (j2_environment_params, j2_environment, alter_context, extra_filters, extra_tests)
    ]

    @classmethod
    def from_file(cls, filename: str) -> "CustomizationModule":
        """Create Customize object"""
        if filename is not None:
            return cls(imp_load_source("customize-module", filename))
        return cls(None)


def import_functions(filename: str) -> Mapping[str, FunctionType]:
    """Import functions from file, return as a dictionary"""
    m = imp_load_source("imported-funcs", filename)
    return {name: func for name, func in inspect.getmembers(m) if inspect.isfunction(func)}


def register_filters(j2env: jinja2.Environment, filters: Mapping[str, FunctionType]) -> None:
    """Register additional filters"""
    j2env.filters.update(filters)


def register_tests(j2env: jinja2.Environment, tests: Mapping[str, FunctionType]) -> None:
    """Register additional tests"""
    j2env.tests.update(tests)  # type: ignore[arg-type]


def import_filters(renderer_env: jinja2.Environment, filename: str) -> None:
    """Import filters from a file"""
    register_filters(renderer_env, import_functions(filename))


def import_tests(renderer_env: jinja2.Environment, filename: str) -> None:
    """Import tests from a file"""
    register_tests(renderer_env, import_functions(filename))


def apply(
    customize: CustomizationModule,
    renderer_env: jinja2.Environment,
    filters: list[str],
    tests: list[str],
) -> None:
    """Apply customizations"""
    customize.j2_environment(renderer_env)

    for fname in filters:
        import_filters(renderer_env, fname)

    for fname in tests:
        import_tests(renderer_env, fname)

    register_filters(renderer_env, customize.extra_filters())

    register_tests(renderer_env, customize.extra_tests())


def add_args(parser: ArgumentParser) -> ArgumentParser:
    """Add args to the parser"""

    parser.add_argument(
        "--customize",
        default=None,
        metavar="python-file.py",
        dest="customize",
        help="A file of Python source code that implements hooks to fine-tune Jinja2 behavior",
    )

    parser.add_argument(
        "--filters",
        action="append",
        default=[],
        metavar="filters-file.py",
        dest="filters",
        help="Load custom Jinja2 filters from a file of Python source code."
        " All top-level functions in the file are imported as Jinja2 filters.",
    )

    parser.add_argument(
        "--tests",
        action="append",
        default=[],
        metavar="tests-file.py",
        dest="tests",
        help="Load custom Jinja2 tests from file of Python source code."
        " All top-level functions in the file are imported as Jinja2 tests.",
    )
    return parser
