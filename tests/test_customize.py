from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Callable

import pytest

from jinjanator.cli import render_command


DirMakerTool = Callable[..., Namespace]


@dataclass
class FileContent:
    """Holds filename and content"""

    filename: str
    content: str
    dedent: bool = True

    @property
    def clean_content(self) -> str:
        """Get cleaned up content"""
        return dedent(self.content) if self.dedent else self.content


@pytest.fixture
def dir_maker(tmp_path: Path) -> DirMakerTool:
    """Maker"""

    def _dir_maker(**kwargs: FileContent) -> Namespace:
        result = {}
        for name, file in kwargs.items():
            filename = tmp_path / f"{file.filename}"
            filename.write_text(file.clean_content)
            result[name] = str(filename)
        return Namespace(**result)

    return _dir_maker


def test_two_custom_filters(dir_maker: DirMakerTool) -> None:
    files = dir_maker(
        template=FileContent(
            "template.j2",
            """
            {{- key | with_parens  | my_reverse -}}
            """,
        ),
        data=FileContent("data.env", "key=Hello, World!"),
        filter=FileContent(
            "filter.py",
            """

            def with_parens(message):
                return f"({message})"

            """,
        ),
        filter2=FileContent(
            "filter2.py",
            """

            def my_reverse(message):
                return message[::-1]

            """,
        ),
    )

    assert ")!dlroW ,olleH(" == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--filters", files.filter, "--filters", files.filter2, files.template, files.data],
    )


@pytest.mark.parametrize(("key", "expected"), [("Hello, World!", "(Hello, World!)")])
def test_custom_filter(dir_maker: DirMakerTool, key: str, expected: str) -> None:
    files = dir_maker(
        template=FileContent(
            "template.j2",
            """
            {{- key | with_parens -}}
            """,
        ),
        data=FileContent(
            "data.env",
            f"""
            key="{key}"
            """,
        ),
        filter=FileContent(
            "filter.py",
            """

        def with_parens(message):
            return f"({message})"

        """,
        ),
    )

    assert expected == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--filter", files.filter, files.template, files.data],
    )


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("value", "NO"),
        ("(value)", "YES"),
    ],
)
def test_custom_test(dir_maker: DirMakerTool, key: str, expected: str) -> None:
    files = dir_maker(
        template=FileContent(
            "template.j2",
            """
            {%- if key is in_parens -%}
                YES
            {%- else -%}
                NO
            {%- endif -%}
            """,
        ),
        data=FileContent(
            "data.env",
            f"""
            key={key}
            """,
        ),
        test=FileContent(
            "test.py",
            """

        def in_parens(message):
            return message and message[0]=="(" and message[-1] == ")"

        """,
        ),
    )

    assert expected == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--tests", files.test, files.template, files.data],
    )


@pytest.mark.parametrize(("key", "expected"), [("something", "YES"), ("(something)", "YES")])
def test_custom_filter_and_test(dir_maker: DirMakerTool, key: str, expected: str) -> None:
    files = dir_maker(
        template=FileContent(
            "template.j2",
            """
            {%- if key | with_parens  is in_parens -%}
                YES
            {%- else %}
                NO
            {%- endif -%}
            """,
        ),
        data=FileContent("data.env", f"key={key}"),
        filter=FileContent(
            "filter.py",
            """

            def with_parens(message):
                return f"({message})"

            """,
        ),
        test=FileContent(
            "test.py",
            """

            def in_parens(message):
                return message and message[0]=="(" and message[-1] == ")"

            """,
        ),
    )

    assert expected == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--filters", files.filter, "--tests", files.test, files.template, files.data],
    )


def test_customize_file(dir_maker: DirMakerTool) -> None:
    files = dir_maker(
        template=FileContent("template.j2", "<<- key >> works, {{ key }} doesn't"),
        data=FileContent("data.env", "key=value"),
        customize=FileContent(
            "customize.py",
            """

            def j2_environment_params():
                return dict(
                    # Change block start/end strings
                    block_start_string='<%',
                    block_end_string='%>',
                    # Change variable strings
                    variable_start_string='<<',
                    variable_end_string='>>')

            """,
        ),
    )

    assert "value works, {{ key }} doesn't" == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--customize", files.customize, files.template, files.data],
    )
