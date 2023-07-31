from __future__ import annotations

from typing import Any

import pytest

import jinjanator.cli

from . import (
    FilePairFactory,
    render_file,
)


def test_quiet(make_file_pair: FilePairFactory, capsys: Any) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "env")
    render_file(files, ["--quiet"])
    captured = capsys.readouterr()
    assert 0 == len(captured.err)


def test_unavailable_suffix(make_file_pair: FilePairFactory, capsys: Any) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "xyz")
    with pytest.raises(
        SystemExit,
    ):
        render_file(files, [])
    assert (
        "No format which can read '.xyz' files available"
        == capsys.readouterr().err.strip()
    )


def test_main_normal(make_file_pair: FilePairFactory, capsys: Any) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "env")
    assert (
        jinjanator.cli.main(["", str(files.template_file), str(files.data_file)]) is None
    )
    assert "Hello Blart!" == capsys.readouterr().out


def test_main_failure(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "xyz")
    assert 1 == jinjanator.cli.main(["", str(files.template_file), str(files.data_file)])
