from __future__ import annotations

from . import (
    FilePairFactory,
    render_file,
)


def test_extension(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{% do [] %}", "", "env")
    assert render_file(files, []) == ""
