from __future__ import annotations

import jinjanator_plugins
import pytest

from . import (
    FilePairFactory,
    render_file,
)


def test_ini_unknown(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "ini")

    with pytest.raises(jinjanator_plugins.FormatOptionUnknownError):
        assert render_file(files, ["--format-option", "midge"])


def test_json_unknown(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "json")

    with pytest.raises(jinjanator_plugins.FormatOptionUnknownError):
        assert render_file(files, ["--format-option", "midge"])


def test_yaml_unknown(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionUnknownError):
        assert render_file(files, ["--format-option", "midge"])


def test_env_unknown(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("", "", "env")

    with pytest.raises(jinjanator_plugins.FormatOptionUnknownError):
        assert render_file(files, ["--format-option", "midge"])
