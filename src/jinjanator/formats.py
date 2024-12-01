import configparser
import json
import keyword

from collections.abc import Iterable, Mapping
from io import StringIO
from typing import Any, Optional

import yaml

from dotenv import dotenv_values
from jinjanator_plugins import (
    FormatOptionUnsupportedError,
    FormatOptionValueError,
    Formats,
    plugin_formats_hook,
)


class INIFormat:
    name = "ini"
    suffixes: Optional[Iterable[str]] = (".ini",)
    option_names: Optional[Iterable[str]] = ()

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        pass

    def parse(self, data_string: str) -> Mapping[str, Any]:
        """INI data input format.

        data.ini:

        ```
        [nginx]
        hostname=localhost
        webroot=/var/www/project
        logs=/var/log/nginx
        ```

        Usage:

        $ j2 config.j2 data.ini
        $ cat data.ini | j2 --format=ini config.j2
        """

        class MyConfigParser(configparser.ConfigParser):
            def as_dict(self) -> Mapping[str, Any]:
                d = dict(self._sections)  # type: ignore[attr-defined]
                for k, v in d.items():
                    d[k] = self._defaults | v  # type: ignore[attr-defined]
                    d[k].pop("__name__", None)
                return d

        ini = MyConfigParser()
        ini.read_string(data_string)

        return ini.as_dict()


class JSONFormat:
    name = "json"
    suffixes: Optional[Iterable[str]] = (".json",)
    option_names: Optional[Iterable[str]] = "array-name"

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        self.array_name: Optional[str] = None
        if options:
            for option in options:
                try:
                    opt, val = option.split("=")
                except ValueError as exc:
                    raise FormatOptionValueError(
                        self,
                        option,
                        "",
                        "contains more than one '='",
                    ) from exc

                if not val.isidentifier():
                    raise FormatOptionValueError(
                        self,
                        opt,
                        val,
                        "is not a valid Python identifier",
                    )

                if keyword.iskeyword(val):
                    raise FormatOptionValueError(self, opt, val, "is a Python keyword")

                self.array_name = val

    def parse(self, data_string: str) -> Mapping[str, Any]:
        """JSON data input format.

        data.json:

        ```
        {
            "nginx":{
                "hostname": "localhost",
                "webroot": "/var/www/project",
                "logs": "/var/log/nginx"
            }
        }
        ```

        Usage:

        $ j2 config.j2 data.json
        $ cat data.json | j2 --format=ini config.j2
        """

        try:
            context = json.loads(data_string)
        except json.decoder.JSONDecodeError as exc:
            msg = "JSON input is neither an object nor an array"
            raise TypeError(msg) from exc

        if isinstance(context, dict):
            if self.array_name:
                raise FormatOptionUnsupportedError(
                    self,
                    "array-name",
                    "cannot be used with object (dictionary) input",
                )

            return context

        if not self.array_name:
            raise FormatOptionUnsupportedError(
                self,
                "array-name",
                "must be specified for array (list) input",
            )

        return {self.array_name: context}


class YAMLFormat:
    name = "yaml"
    suffixes: Optional[Iterable[str]] = (".yaml", ".yml")
    option_names: Optional[Iterable[str]] = "sequence-name"

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        self.sequence_name: Optional[str] = None
        if options:
            for option in options:
                try:
                    opt, val = option.split("=")
                except ValueError as exc:
                    raise FormatOptionValueError(
                        self,
                        option,
                        "",
                        "contains more than one '='",
                    ) from exc

                if not val.isidentifier():
                    raise FormatOptionValueError(
                        self,
                        opt,
                        val,
                        "is not a valid Python identifier",
                    )

                if keyword.iskeyword(val):
                    raise FormatOptionValueError(self, opt, val, "is a Python keyword")

                self.sequence_name = val

    def parse(
        self,
        data_string: str,
    ) -> Mapping[str, Any]:
        """YAML data input format.

        data.yaml:

        ```
        nginx:
            hostname: localhost
            webroot: /var/www/project
            logs: /var/log/nginx
        ```

        Usage:

        $ j2 config.j2 data.yml
        $ cat data.yml | j2 --format=yaml config.j2
        """

        context = yaml.safe_load(data_string)

        if isinstance(context, dict):
            if self.sequence_name:
                raise FormatOptionUnsupportedError(
                    self,
                    "sequence-name",
                    "cannot be used with mapping (dictionary) input",
                )

            return context

        if isinstance(context, list):
            if not self.sequence_name:
                raise FormatOptionUnsupportedError(
                    self,
                    "sequence-name",
                    "must be specified for sequence (array) input",
                )

            return {self.sequence_name: context}

        msg = "YAML input is neither a mapping nor a sequence"
        raise TypeError(msg)


class EnvFormat:
    name = "env"
    suffixes: Optional[Iterable[str]] = (".env",)
    option_names: Optional[Iterable[str]] = ()

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        pass

    def parse(self, data_string: str) -> Mapping[str, str]:
        """Data input from environment variables.

        Render directly from the current environment variable values:

        $ j2 config.j2

        Or alternatively, read the values from a dotenv file:

        ```
        NGINX_HOSTNAME=localhost
        NGINX_WEBROOT=/var/www/project
        NGINX_LOGS=/var/log/nginx/
        ```

        And render with:

        $ j2 config.j2 data.env
        $ env | j2 --format=env config.j2

        If you're going to pipe a dotenv file into `j2`, you'll need to
        use "-" as the second argument to explicitly:

        $ j2 config.j2 - < data.env
        """

        data = StringIO(data_string)
        results_dict = dotenv_values(stream=data)

        return {k: v if v is not None else "" for (k, v) in results_dict.items()}


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {
        INIFormat.name: INIFormat,
        JSONFormat.name: JSONFormat,
        YAMLFormat.name: YAMLFormat,
        EnvFormat.name: EnvFormat,
    }
