import os

from typing import Any

import pytest

from jinja2 import UndefinedError

from . import (
    FilePairFactory,
    render_file,
    render_file_env,
    render_implicit_stream,
)


def test_import(make_file_pair: FilePairFactory) -> None:
    # Import environment into a variable
    files = make_file_pair("{{ a }}/{{ env.B }}", '{"a":1}', "json")
    assert "1/2" == render_file_env(files, ["--import-env=env"], env={"B": "2"})

    # Import environment into global scope
    files = make_file_pair("{{ a }}/{{ B }}", '{"a":1, "B": 1}', "json")
    assert "1/2" == render_file_env(files, ["--import-env="], env={"B": "2"})


def test_equals_sign_in_file_value(make_file_pair: FilePairFactory) -> None:
    # A: key with out an equals sign should return an empty string.
    #  Slight drift from python-dotenv to maintain current plugin definition
    # B: C should return their assigned values
    # D: key with an equals sign and no value should return empty string
    # E: should interpolate the value of C
    # F: should fail to interpolate the value of G due to order
    # G: should be assigned value
    # Ref: https://pypi.org/project/python-dotenv/
    files = make_file_pair(
        "{{ A|default() }}/{{ B }}/{{ C }}/{{ D }}/{{ E }}/{{ F }}/{{ G }}",
        "A\nB=1\nC=val=1\nD=\nE=${C}\nF=${G}\nG=1",
        "env",
    )
    assert "/1/val=1//val=1//1" == render_file(files, [])


def test_filter(make_file_pair: FilePairFactory, monkeypatch: Any) -> None:
    assert "USER_PASS" not in os.environ

    files = make_file_pair(
        '{{ user_login }}:{{ "USER_PASS"|env }}',
        "user_login: kolypto",
        "yaml",
    )

    # Value provided by environment
    monkeypatch.setenv("USER_PASS", "qwerty123")
    assert "kolypto:qwerty123" == render_file(files, [])

    # Value not provided
    monkeypatch.delenv("USER_PASS")
    with pytest.raises(KeyError):
        assert "kolypto:qwerty123" == render_file(files, [])

    # Default value
    files = make_file_pair(
        '{{ user_login }}:{{ "USER_PASS"|env("-none-") }}',
        "user_login: kolypto",
        "yaml",
    )

    assert "kolypto:-none-" == render_file(files, [])


def test_function(make_file_pair: FilePairFactory, monkeypatch: Any) -> None:
    assert "USER_PASS" not in os.environ

    files = make_file_pair(
        '{{ user_login }}:{{ env("USER_PASS") }}',
        "user_login: kolypto",
        "yaml",
    )

    # Value provided by environment
    monkeypatch.setenv("USER_PASS", "qwerty123")
    assert "kolypto:qwerty123" == render_file(files, [])

    # Value not provided
    monkeypatch.delenv("USER_PASS")
    with pytest.raises(KeyError):
        assert "kolypto:qwerty123" == render_file(files, [])

    # Default value
    files = make_file_pair(
        '{{ user_login }}:{{ env("USER_PASS", "-none-") }}',
        "user_login: kolypto",
        "yaml",
    )
    assert "kolypto:-none-" == render_file(files, [])


def test_env_stream(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ a }}", "foo=bar", "env")
    with pytest.raises(UndefinedError, match="If you're trying to pipe a .env file"):
        render_implicit_stream(files, ["--format=env"])
