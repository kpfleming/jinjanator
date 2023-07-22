from __future__ import annotations

import pytest

from . import (
    FilePairFactory,
    render_env,
    render_file,
)


def test_invalid_json(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", '["one", "two"]', "json")

    with pytest.raises(TypeError, match="JSON input does not contain an object"):
        assert render_file(files, [])


def test_invalid_yaml(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "-one\n-two", "yaml")

    with pytest.raises(TypeError, match="YAML input does not contain a mapping"):
        assert render_file(files, [])


def test_no_input_data(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "yaml")

    with pytest.raises(ValueError, match="no input supplied"):
        assert render_env(files, ["--format", "yaml"], {})
