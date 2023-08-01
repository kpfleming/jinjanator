from __future__ import annotations

import jinjanator_plugins
import pytest

from . import (
    FilePairFactory,
    render_file,
)


def test_mapping_normal(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ foo }}", '{"foo": "bar"}', "json")

    assert "bar" == render_file(files, [])


def test_mapping_with_array_name_option(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ foo }}", '{"foo": "bar"}', "json")

    with pytest.raises(jinjanator_plugins.FormatOptionUnsupportedError):
        assert render_file(files, ["--format-option", "array-name=seq"])


def test_array_normal(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[1,2,3]", "json")

    assert "1" == render_file(files, ["--format-option", "array-name=seq"])


def test_array_without_array_name_option(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[1,2,3]", "json")

    with pytest.raises(jinjanator_plugins.FormatOptionUnsupportedError):
        assert render_file(files, [])


def test_array_invalid_name(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[1,2,3]", "json")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "array-name=334seq"])


def test_array_invalid_value(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[1,2,3]", "json")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "array-name=abc=def"])


def test_array_keyword_name(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[1,2,3]", "json")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "array-name=raise"])
