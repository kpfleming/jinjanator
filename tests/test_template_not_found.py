from __future__ import annotations

from pathlib import Path

import pytest

from jinja2.exceptions import TemplateNotFound

from . import (
    FilePairFactory,
    render_file,
)


def test_template_not_found(
    make_file_pair: FilePairFactory,
) -> None:
    files = make_file_pair("{{name}}", "", "env")
    files.template_file = Path("does-not-exist.j2")
    with pytest.raises(TemplateNotFound):
        render_file(files, [])
