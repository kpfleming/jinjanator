from __future__ import annotations

import jinjanator_plugins
import pytest

from . import (
    FilePairFactory,
    render_file,
)


def test_mapping_normal(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ foo }}", "foo: bar", "yaml")

    assert "bar" == render_file(files, [])


def test_mapping_with_sequence_name_option(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ foo }}", "foo: bar", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionUnsupportedError):
        assert render_file(files, ["--format-option", "sequence-name=seq"])


def test_sequence_normal(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[ bar ]", "yaml")

    assert "bar" == render_file(files, ["--format-option", "sequence-name=seq"])


def test_sequence_without_sequence_name_option(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[ bar ]", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionUnsupportedError):
        assert render_file(files, [])


def test_sequence_invalid_name(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[ bar ]", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "sequence-name=334seq"])


def test_sequence_invalid_value(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[ bar ]", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "sequence-name=abc=def"])


def test_sequence_keyword_name(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ seq[0] }}", "[ bar ]", "yaml")

    with pytest.raises(jinjanator_plugins.FormatOptionValueError):
        render_file(files, ["--format-option", "sequence-name=raise"])
