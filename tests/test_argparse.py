from __future__ import annotations

from typing import Any, Mapping

import pytest

from jinjanator.cli import parse_args
from jinjanator.plugin import Format


def fake_env_parser(
    data: str, options: list[str] | None = None  # noqa: ARG001
) -> Mapping[str, Any]:
    return {"foo": "bar"}


fake_env_format = Format(parser=fake_env_parser, suffixes=["env"])


def test_invalid_arg() -> None:
    """Ensure that an invalid argument is not accepted."""
    with pytest.raises(SystemExit):
        parse_args({}, ["--test-invalid-arg"])


@pytest.mark.parametrize(
    "args",
    [
        ["--format", "env"],
        ["--format-option", "opt"],
        ["--import-env", "env"],
        ["--output-file", "output"],
        ["--quiet"],
        ["--undefined"],
        ["-e", "env"],
        ["-f", "env"],
        ["-o", "output"],
    ],
)
def test_args(args: list[str]) -> None:
    """Ensure that known arguments are accepted."""
    parse_args({"env": fake_env_format}, [*args, "template"])


def test_version() -> None:
    """Ensure that '--version' argument is accepted and program exits without an error."""
    with pytest.raises(SystemExit) as excinfo:
        parse_args({}, ["--version"])
    assert excinfo.value.code == 0


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "args",
    [
        ["--format", "env", "-f", "env"],
        ["--import-env", "env", "-e", "env"],
    ],
)
def test_duplicate_args(args: list[str]) -> None:
    """Ensure that duplicate arguments are not accepted."""
    parse_args({"env": fake_env_format}, [*args, "template"])
