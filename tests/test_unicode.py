from __future__ import annotations

from . import (
    FilePairFactory,
    render_env,
    render_file,
)


def test_json(make_file_pair: FilePairFactory) -> None:
    # I'm using Russian language for unicode :)
    files = make_file_pair(
        "Проверка {{ a }} связи!",
        '{"a": "широкополосной"}',
        "json",
    )
    assert "Проверка широкополосной связи!" == render_file(files, [])


def test_env(make_file_pair: FilePairFactory) -> None:
    files = make_file_pair("Hello {{name}}!", "", "env")
    # Test case from issue #17 (in j2cli repo): unicode environment variables
    assert "Hello Jürgen!" == render_env(files, [], env={"name": "Jürgen"})
