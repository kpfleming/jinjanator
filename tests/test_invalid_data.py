from __future__ import annotations

import pytest

from . import (
    FilePairFactory,
    render_env,
    render_file,
)


def test_invalid_json(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "midge", "json")

    with pytest.raises(TypeError, match="JSON input is neither an object nor an array"):
        assert render_file(files, [])


def test_invalid_yaml(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "midge", "yaml")

    with pytest.raises(
        TypeError,
        match="YAML input is neither a mapping nor a sequence",
    ):
        assert render_file(files, [])


def test_no_input_data(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "yaml")

    with pytest.raises(ValueError, match="no input supplied"):
        assert render_env(files, ["--format", "yaml"], {})
