from __future__ import annotations

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
    assert render_file_env(files, ["--import-env=env"], env={"B": "2"}) == "1/2"

    # Import environment into global scope
    files = make_file_pair("{{ a }}/{{ B }}", '{"a":1, "B": 1}', "json")
    assert render_file_env(files, ["--import-env="], env={"B": "2"}) == "1/2"


def test_equals_sign_in_file_value(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair(
        "{{ A|default() }}/{{ B }}/{{ C }}",
        "A\nB=1\nC=val=1\n",
        "env",
    )
    assert render_file(files, []) == "/1/val=1"


def test_filter(make_file_pair: FilePairFactory, monkeypatch: Any) -> None:
    assert "USER_PASS" not in os.environ

    files = make_file_pair(
        '{{ user_login }}:{{ "USER_PASS"|env }}',
        "user_login: kolypto",
        "yaml",
    )

    # Value provided by environment
    monkeypatch.setenv("USER_PASS", "qwerty123")
    assert render_file(files, []) == "kolypto:qwerty123"

    # Value not provided
    monkeypatch.delenv("USER_PASS")
    with pytest.raises(KeyError):
        assert render_file(files, []) == "kolypto:qwerty123"

    # Default value
    files = make_file_pair(
        '{{ user_login }}:{{ "USER_PASS"|env("-none-") }}',
        "user_login: kolypto",
        "yaml",
    )

    assert render_file(files, []) == "kolypto:-none-"


def test_function(make_file_pair: FilePairFactory, monkeypatch: Any) -> None:
    assert "USER_PASS" not in os.environ

    files = make_file_pair(
        '{{ user_login }}:{{ env("USER_PASS") }}',
        "user_login: kolypto",
        "yaml",
    )

    # Value provided by environment
    monkeypatch.setenv("USER_PASS", "qwerty123")
    assert render_file(files, []) == "kolypto:qwerty123"

    # Value not provided
    monkeypatch.delenv("USER_PASS")
    with pytest.raises(KeyError):
        assert render_file(files, []) == "kolypto:qwerty123"

    # Default value
    files = make_file_pair(
        '{{ user_login }}:{{ env("USER_PASS", "-none-") }}',
        "user_login: kolypto",
        "yaml",
    )
    assert render_file(files, []) == "kolypto:-none-"


def test_env_stream(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("{{ a }}", "foo=bar", "env")
    with pytest.raises(UndefinedError, match="If you're trying to pipe a .env file"):
        render_implicit_stream(files, ["--format=env"])
