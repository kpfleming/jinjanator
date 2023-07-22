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
    assert len(captured.err) == 0


def test_unavailable_suffix(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "xyz")
    with pytest.raises(
        SystemExit,
        match="no format which can read '.xyz' files available",
    ):
        render_file(files, [])


def test_main_normal(make_file_pair: FilePairFactory, capsys: Any) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "env")
    assert (
        jinjanator.cli.main(["--quiet", str(files.template_file), str(files.data_file)])
        is None
    )
    captured = capsys.readouterr()
    assert captured.out == "Hello Blart!"


def test_main_failure(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("Hello {{name}}!", "name=Blart", "xyz")
    assert (
        jinjanator.cli.main(["--quiet", str(files.template_file), str(files.data_file)])
        == 1
    )
