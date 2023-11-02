from __future__ import annotations

from typing import Iterable, Mapping

import pytest

from jinjanator.cli import parse_args


class FakeFormat:
    name = "env"
    suffixes: Iterable[str] | None = (".env",)
    option_names: Iterable[str] | None = ()

    def __init__(self, options: Iterable[str] | None) -> None:
        pass

    def parse(
        self,
        data_string: str,  # noqa: ARG002
    ) -> Mapping[str, str]:
        return {"foo": "bar"}


def test_invalid_arg() -> None:
    """
    Ensure that an invalid argument is not accepted.
    """
    with pytest.raises(SystemExit):
        parse_args({}, [], ["--test-invalid-arg"])


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
    """
    Ensure that known arguments are accepted.
    """
    parse_args({"env": FakeFormat}, [], [*args, "template"])


def test_version() -> None:
    """
    Ensure that '--version' argument is accepted and program exits without an error.
    """
    with pytest.raises(SystemExit) as excinfo:
        parse_args({}, [], ["--version"])
    assert 0 == excinfo.value.code


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "args",
    [
        ["--format", "env", "-f", "env"],
        ["--import-env", "env", "-e", "env"],
    ],
)
def test_duplicate_args(args: list[str]) -> None:
    """
    Ensure that duplicate arguments are not accepted.
    """
    parse_args({"env": FakeFormat}, [], [*args, "template"])
