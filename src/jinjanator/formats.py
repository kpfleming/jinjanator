from __future__ import annotations

import configparser
import json

from typing import Any, Mapping

import yaml

from jinjanator_plugins import (
    Format,
    Formats,
    plugin_formats_hook,
)


class INIFormat:
    @staticmethod
    def parser(
        data_string: str,
        options: list[str] | None = None,  # noqa: ARG004
    ) -> Mapping[str, Any]:
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
                for k in d:
                    d[k] = dict(self._defaults, **d[k])  # type: ignore[attr-defined]
                    d[k].pop("__name__", None)
                return d

        ini = MyConfigParser()
        ini.read_string(data_string)

        return ini.as_dict()

    fmt = Format(name="ini", parser=parser, suffixes=[".ini"], options=[])


class JSONFormat:
    @staticmethod
    def parser(
        data_string: str,
        options: list[str] | None = None,  # noqa: ARG004
    ) -> Mapping[str, Any]:
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

        context = json.loads(data_string)

        if not isinstance(context, dict):
            msg = "JSON input does not contain an object (dictionary)"
            raise TypeError(msg)

        return context

    fmt = Format(name="json", parser=parser, suffixes=[".json"], options=[])


class YAMLFormat:
    @staticmethod
    def parser(
        data_string: str,
        options: list[str] | None = None,  # noqa: ARG004
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

        if not isinstance(context, dict):
            msg = "YAML input does not contain a mapping (dictionary)"
            raise TypeError(msg)

        return context

    fmt = Format(name="yaml", parser=parser, suffixes=[".yaml", ".yml"], options=[])


class EnvFormat:
    @staticmethod
    def parser(
        data_string: str,
        options: list[str] | None = None,  # noqa: ARG004
    ) -> Mapping[str, str]:
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

        return dict(
            filter(
                lambda line: len(line) == 2,  # noqa: PLR2004
                (
                    list(map(str.strip, line.split("=", 1)))
                    for line in data_string.split("\n")
                ),
            ),
        )

    fmt = Format(name="env", parser=parser, suffixes=[".env"], options=[])


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {
        f.name: f for f in [INIFormat.fmt, JSONFormat.fmt, YAMLFormat.fmt, EnvFormat.fmt]
    }
