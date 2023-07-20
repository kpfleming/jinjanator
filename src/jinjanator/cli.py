import argparse
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, TextIO, Tuple, Union

import jinja2

from . import filters, version
from .context import FORMATS, read_context_data


class FilePathLoader(jinja2.BaseLoader):
    def __init__(self, cwd: Path, encoding: str = "utf-8"):
        self.cwd = cwd
        self.encoding = encoding

    def get_source(
        self,
        environment: jinja2.Environment,
        template_name: str,
    ) -> Tuple[str, str, Callable[[], bool]]:
        template_path = Path(template_name)

        if not template_path.is_absolute():
            template_path = self.cwd / template_name

        if not template_path.is_file():
            raise jinja2.TemplateNotFound(template_name)

        mtime = template_path.stat().st_mtime

        return (
            template_path.read_text(encoding=self.encoding),
            str(template_path),
            lambda: template_path.stat().st_mtime == mtime,
        )


class Jinja2TemplateRenderer:
    ENABLED_EXTENSIONS = (
        "jinja2.ext.i18n",
        "jinja2.ext.do",
        "jinja2.ext.loopcontrols",
    )

    def __init__(self, cwd: Path, allow_undefined: bool, j2_env_params: Dict[str, Any]):
        j2_env_params.setdefault("keep_trailing_newline", True)
        j2_env_params.setdefault(
            "undefined",
            jinja2.Undefined if allow_undefined else jinja2.StrictUndefined,
        )
        j2_env_params.setdefault("extensions", self.ENABLED_EXTENSIONS)
        j2_env_params.setdefault("loader", FilePathLoader(cwd))

        self._env = jinja2.Environment(**j2_env_params)
        self._env.globals.update({"env": filters.env})

    def register_filters(self, filters: Mapping[str, Callable[..., Any]]) -> None:
        self._env.filters.update(filters)

    def render(self, template_name: str, context: Mapping[str, str]) -> str:
        return self._env.get_template(template_name).render(context)


class UniqueStore(argparse.Action):
    """argparse action to restrict options to appearing only once."""

    def __init__(self, option_strings: Sequence[str], dest: str, **kwargs: Any) -> None:
        self.already_seen = False
        super().__init__(option_strings, dest, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Optional[Union[str, Sequence[Any]]],
        option_string: Optional[str] = None,
    ) -> None:
        if self.already_seen and option_string:
            parser.error(option_string + " cannot be specified more than once.")
        setattr(namespace, self.dest, values)
        self.already_seen = True


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="j2",
        description="Command-line interface to Jinja2 for templating in shell scripts.",
        epilog="",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"jinjanate {version}, Jinja2 {jinja2.__version__}",
        help="display version of this program",
    )

    parser.add_argument(
        "-f",
        "--format",
        action=UniqueStore,
        default="?",
        help="Input data format",
        choices=["?", *list(FORMATS.keys())],
    )

    parser.add_argument(
        "-e",
        "--import-env",
        action=UniqueStore,
        default=None,
        metavar="VAR",
        dest="import_env",
        help=(
            "Import environment variables as `VAR` variable. Use empty string to import"
            " into the global scope"
        ),
    )

    parser.add_argument(
        "--undefined",
        action="store_true",
        dest="undefined",
        help="Allow undefined variables to be used in templates (suppress errors)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        dest="quiet",
        help="Suppress informational messages",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="outfile",
        dest="output_file",
        type=Path,
        help="Output to a file instead of stdout",
    )

    parser.add_argument("template", help="Template file to process")

    parser.add_argument(
        "data",
        nargs="?",
        default=None,
        type=Path,
        help='Input data file name/path; "-" to use stdin',
    )

    return parser.parse_args(argv)


def render_command(
    cwd: Path,
    environ: Mapping[str, str],
    stdin: Optional[TextIO],
    argv: Sequence[str],
) -> str:
    args = parse_args(argv[1:])

    if not args.quiet:
        print(
            f"{Path(argv[0]).name} {version}, Jinja2 {jinja2.__version__}",
            file=sys.stderr,
        )

    if args.format == "?":
        if args.data is None or str(args.data) == "-":
            args.format = "env"
        else:
            suffix = args.data.suffix
            for k, v in FORMATS.items():
                if suffix in v.suffixes:
                    args.format = k
                    break
            if args.format == "?":
                raise ValueError(f"{suffix} format unavailable")

    # We always expect a file;
    # unless the user wants 'env', and there's no input file provided.
    if args.format == "env":
        """
        With the "env" format, if no dotenv filename is provided,
        we have two options: 1. The user wants to use the current
        environment 2. The user is feeding a dotenv file at stdin.
        Depending on whether we have data at stdin, we'll need to
        choose between the two.

        The problem is that in Linux, you can't reliably determine
        whether there is any data at stdin: some environments would
        open the descriptor even though they're not going to feed any
        data in.  That's why many applications would ask you to
        explicitly specify a '-' when stdin should be used.

        And this is what we're going to do here as well. The script,
        however, would give the user a hint that they should use '-'.
        """
        if str(args.data) == "-":
            input_data_f = stdin
        elif args.data is None:
            input_data_f = None
        else:
            input_data_f = args.data.open()
    else:
        input_data_f = (
            stdin if args.data is None or str(args.data) == "-" else args.data.open()
        )

    context = read_context_data(args.format, input_data_f, environ, args.import_env)

    renderer = Jinja2TemplateRenderer(
        cwd,
        args.undefined,
        j2_env_params={},
    )

    renderer.register_filters(
        {
            "env": filters.env,
        },
    )

    try:
        result = renderer.render(args.template, context)
    except jinja2.exceptions.UndefinedError as e:
        # When there's data at stdin, tell the user they should use '-'
        try:
            stdin_has_data = stdin is not None and not stdin.isatty()
            if args.format == "env" and args.data is None and stdin_has_data:
                extra_info = (
                    "\n\nIf you're trying to pipe a .env file, please run me with a '-'"
                    " as the data file name:\n$ {cmd} {argv} -".format(
                        cmd=Path(sys.argv[0]).name,
                        argv=" ".join(sys.argv[1:]),
                    )
                )
                e.args = (e.args[0] + extra_info,) + e.args[1:]
        except:  # noqa: E722
            # The above code is so optional that any, ANY, error, is ignored
            pass

        # Proceed
        raise

    if args.output_file:
        with args.output_file.open("w") as f:
            f.write(result)
            f.close()
        return ""

    return result


def main() -> Optional[int]:
    try:
        output = render_command(Path.cwd(), os.environ, sys.stdin, sys.argv)
    except SystemExit:
        return 1
    outstream = getattr(sys.stdout, "buffer", sys.stdout)
    outstream.write(output)
    return None
