from __future__ import annotations

import pathlib

import pytest

from . import FilePair, FilePairFactory


@pytest.fixture()
def make_file_pair(tmp_path: pathlib.Path) -> FilePairFactory:
    def _make_file_pair(
        template_content: str,
        data_content: str,
        data_format: str,
    ) -> FilePair:
        template_file = tmp_path / "template.j2"
        template_file.write_text(template_content)
        data_file = tmp_path / f"data.{data_format}"
        data_file.write_text(data_content)
        return FilePair(template_file=template_file, data_file=data_file)

    return _make_file_pair
