from __future__ import annotations

from typing import Any

import pytest

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
        ValueError,
        match="no format which can read '.xyz' files available",
    ):
        render_file(files, [])
