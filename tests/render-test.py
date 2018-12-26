# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import os, io, os.path, tempfile
from contextlib import contextmanager

from j2cli.cli import render_command

@contextmanager
def mktemp(contents):
    """ Create a temporary file with the given contents, and yield its path """
    _, path = tempfile.mkstemp()
    fp = io.open(path, 'wt+', encoding='utf-8')
    fp.write(contents)
    fp.flush()
    try:
        yield path
    finally:
        fp.close()
        os.unlink(path)


class RenderTest(unittest.TestCase):
    def setUp(self):
        os.chdir(
            os.path.dirname(__file__)
        )

    def _testme(self, argv, expected_output, stdin=None, env=None):
        """ Helper test shortcut """
        result = render_command(os.getcwd(), env or {}, stdin, argv)
        if isinstance(result, bytes):
            result = result.decode('utf-8')
        self.assertEqual(result, expected_output)

    #: The expected output
    expected_output = """server {
  listen 80;
  server_name localhost;

  root /var/www/project;
  index index.htm;

  access_log /var/log/nginx//http.access.log combined;
  error_log  /var/log/nginx//http.error.log;
}
"""

    def _testme_std(self, argv, stdin=None, env=None):
        self._testme(argv, self.expected_output, stdin, env)

    def test_ini(self):
        # Filename
        self._testme_std(['resources/nginx.j2', 'resources/data.ini'])
        # Format
        self._testme_std(['--format=ini', 'resources/nginx.j2', 'resources/data.ini'])
        # Stdin
        self._testme_std(['--format=ini', 'resources/nginx.j2'], stdin=open('resources/data.ini'))

    def test_json(self):
        # Filename
        self._testme_std(['resources/nginx.j2', 'resources/data.json'])
        # Format
        self._testme_std(['--format=json', 'resources/nginx.j2', 'resources/data.json'])
        # Stdin
        self._testme_std(['--format=json', 'resources/nginx.j2'], stdin=open('resources/data.json'))

    def test_yaml(self):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest('Yaml lib not installed')

        # Filename
        self._testme_std(['resources/nginx.j2', 'resources/data.yml'])
        self._testme_std(['resources/nginx.j2', 'resources/data.yaml'])
        # Format
        self._testme_std(['--format=yaml', 'resources/nginx.j2', 'resources/data.yml'])
        # Stdin
        self._testme_std(['--format=yaml', 'resources/nginx.j2'], stdin=open('resources/data.yml'))

    def test_env(self):
        # Filename
        self._testme_std(['resources/nginx-env.j2', 'resources/data.env'])
        # Format
        self._testme_std(['--format=env', 'resources/nginx-env.j2', 'resources/data.env'])

        # Environment!
        env = dict(NGINX_HOSTNAME='localhost', NGINX_WEBROOT='/var/www/project', NGINX_LOGS='/var/log/nginx/')
        self._testme_std(['--format=env', 'resources/nginx-env.j2'], env=env)
        self._testme_std(['--format=env', 'resources/nginx-env.j2'], env=env)

    def test_import_env(self):
        # Import environment into a variable
        with mktemp('{{ a }}/{{ env.B }}') as template:
            with mktemp('{"a":1}') as context:
                self._testme(['--format=json', '--import-env=env', template, context], '1/2', env=dict(B='2'))
        # Import environment into global scope
        with mktemp('{{ a }}/{{ B }}') as template:
            with mktemp('{"a":1,"B":1}') as context:
                self._testme(['--format=json', '--import-env=', template, context], '1/2', env=dict(B='2'))

    def test_env_file__equals_sign_in_value(self):
        # Test whether environment variables with "=" in the value are parsed correctly
        with mktemp('{{ A|default('') }}/{{ B }}/{{ C }}') as template:
            with mktemp('A\nB=1\nC=val=1\n') as context:
                self._testme(['--format=env', template, context], '/1/val=1')

    def test_unicode(self):
        # Test how unicode is handled
        # I'm using Russian language for unicode :)
        with mktemp('Проверка {{ a }} связи!') as template:
            with mktemp('{"a": "широкополосной"}') as context:
                self._testme(['--format=json', template, context], 'Проверка широкополосной связи!')

    def test_custom_filters(self):
        with mktemp('{{ a|parentheses }}') as template:
            self._testme(['--format=env', '--filters=resources/custom_filters.py', template], '(1)', env=dict(a='1'))

    def test_custom_tests(self):
        with mktemp('{% if a|int is custom_odd %}odd{% endif %}') as template:
            self._testme(['--format=env', '--tests=resources/custom_tests.py', template], 'odd', env=dict(a='1'))

    def test_output_file(self):
        with mktemp('{{ a }}') as template:
            try:
                self._testme(['-o', '/tmp/j2-out', template], '', env=dict(a='123'))
                self.assertEqual('123', io.open('/tmp/j2-out', 'r').read())
            finally:
                os.unlink('/tmp/j2-out')
