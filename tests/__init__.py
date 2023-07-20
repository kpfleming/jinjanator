from __future__ import annotations

from pathlib import Path
from typing import Callable, Mapping, Sequence

from attrs import define

from jinjanator.cli import render_command


@define(kw_only=True)
class FilePair:
    template_file: Path
    data_file: Path


FilePairFactory = Callable[[str, str, str], FilePair]


def render_file(
    files: FilePair,
    options: Sequence[str],
) -> str:
    return render_command(
        Path.cwd(),
        {},
        None,
        ["", *options, str(files.template_file), str(files.data_file)],
    )


def render_implicit_stream(
    files: FilePair,
    options: Sequence[str],
) -> str:
    with files.data_file.open() as data:
        return render_command(
            Path.cwd(),
            {},
            data,
            ["", *options, str(files.template_file)],
        )


def render_explicit_stream(
    files: FilePair,
    options: Sequence[str],
) -> str:
    with files.data_file.open() as data:
        return render_command(
            Path.cwd(),
            {},
            data,
            ["", *options, str(files.template_file), "-"],
        )


def render_env(
    files: FilePair,
    options: Sequence[str],
    env: Mapping[str, str],
) -> str:
    return render_command(
        Path.cwd(),
        env,
        None,
        ["", *options, str(files.template_file)],
    )


def render_file_env(
    files: FilePair,
    options: Sequence[str],
    env: Mapping[str, str],
) -> str:
    return render_command(
        Path.cwd(),
        env,
        None,
        ["", *options, str(files.template_file), str(files.data_file)],
    )
