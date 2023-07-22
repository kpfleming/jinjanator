from __future__ import annotations

import pytest

from jinja2.exceptions import UndefinedError

from . import (
    FilePairFactory,
    render_file,
)


def test_normal(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{name}}", "", "env")
    with pytest.raises(UndefinedError):
        render_file(files, [])


def test_suppressed(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{name}}", "", "env")
    assert render_file(files, ["--undefined"]) == ""
