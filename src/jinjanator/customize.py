"""
Add Customize/Filters/Tests functionality from J2CLI

This code was ported from https://github.com/kolypto/j2cli

"""
import inspect
import types
from argparse import ArgumentParser
from importlib.machinery import SourceFileLoader
from typing import List, Dict

import jinja2


def imp_load_source(module_name, module_path):
    """
    Drop-in Replacement for imp.load_source() function in pre-3.12 python

    Source: https://github.com/python/cpython/issues/104212
    """
    loader = SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


class CustomizationModule(object):
    """ The interface for customization functions, defined as module-level
    functions """

    def __init__(self, module=None):
        if module is not None:
            def howcall(*args):
                print(args)
                exit(1)

            # Import every module function as a method on ourselves
            for name in self._IMPORTED_METHOD_NAMES:
                try:
                    setattr(self, name, getattr(module, name))
                except AttributeError:
                    pass

    # stubs

    def j2_environment_params(self):
        return {}

    def j2_environment(self, env):
        return env

    def alter_context(self, context):
        return context

    def extra_filters(self):
        return {}

    def extra_tests(self):
        return {}

    _IMPORTED_METHOD_NAMES = [
        f.__name__
        for f in (
            j2_environment_params, j2_environment, alter_context, extra_filters,
            extra_tests)]


def from_file(filename: str) -> CustomizationModule:
    """ Create Customize object """
    if filename is not None:
        return CustomizationModule(
            imp_load_source('customize-module', filename)
        )
    return CustomizationModule(None)


def import_functions(filename: str):
    """ Import functions from file, return as a dictionary """
    m = imp_load_source('imported-funcs', filename)
    return dict((name, func)
                for name, func in inspect.getmembers(m)
                if inspect.isfunction(func))


def register_filters(renderer_env: jinja2.Environment, filters: Dict):
    """ Register additional filters """
    renderer_env.filters.update(filters)


def register_tests(renderer_env: jinja2.Environment, tests: Dict):
    """ Register additional tests """
    renderer_env.tests.update(tests)


def import_filters(renderer_env: jinja2.Environment, filename: str):
    """ Import filters from a file """
    register_filters(renderer_env, import_functions(filename))


def import_tests(renderer_env: jinja2.Environment, filename: str):
    """ Import tests from a file """
    register_tests(renderer_env, import_functions(filename))


def apply(customize: CustomizationModule,
          renderer_env: jinja2.Environment,
          filters: List[str],
          tests: List[str]):
    """ Apply customizations """
    customize.j2_environment(renderer_env)

    for fname in filters:
        import_filters(renderer_env, fname)

    for fname in tests:
        import_tests(renderer_env, fname)

    register_filters(renderer_env, customize.extra_filters())

    register_tests(renderer_env, customize.extra_tests())


def add_args(parser: ArgumentParser) -> ArgumentParser:
    """ Add args to the parser """
    parser.add_argument(
        '--customize',
        default=None,
        metavar='python-file.py',
        dest='customize',
        help='A Python file that implements hooks to '
             'fine-tune the jinjanator behavior')

    parser.add_argument(
        '--filters',
        nargs='+',
        default=[],
        metavar='python-file',
        dest='filters',
        help='Load custom Jinja2 filters from a Python file: '
             'all top-level functions are imported.')

    parser.add_argument(
        '--tests',
        nargs='+',
        default=[],
        metavar='python-file',
        dest='tests',
        help='Load custom Jinja2 tests from a Python file.')
    return parser
