# Changelog

All notable changes to this project will be documented in this file.

The format is based on [*Keep a
Changelog*](https://keepachangelog.com/en/1.0.0/) and this project
adheres to [*Calendar Versioning*](https://calver.org/).

The **first number** of the version is the year.

The **second number** is incremented with each release, starting at 1
for each year.

The **third number** is when we need to start branches for older
releases (only for emergencies).

Committed changes for the next release can be found in the ["changelog.d"
directory](https://github.com/kpfleming/jinjanator/tree/main/changelog.d)
in the project repository.

<!--
Do *NOT* add changelog entries here!

This changelog is managed by towncrier and is compiled at release time.

See https://github.com/kpfleming/jinjanator/blob/main/.github/CONTRIBUTING.md#changelog for details.
-->

<!-- towncrier release notes start -->

## [24.2.0](https://github.com/kpfleming/jinjanator/tree/24.2.0) - 2024-06-11

### Additions

- Added 'j2' CLI entrypoint, for users converting from 'j2cli'.
  [#25](https://github.com/kpfleming/jinjanator/issues/25)
- Added support for Python 3.13.
  [#31](https://github.com/kpfleming/jinjanator/issues/31)

## [24.1.0](https://github.com/kpfleming/jinjanator/tree/24.1.0) - 2024-04-27

### Additions

- Support for 'extensions' plugins which enable Jinja2 extensions (contributed by @llange)
  [#29](https://github.com/kpfleming/jinjanator/issues/29)

## [23.7.0](https://github.com/kpfleming/jinjanator/tree/23.7.0) - 2023-10-07

### Additions

- Added Python 3.12 support.
  [#23](https://github.com/kpfleming/jinjanator/issues/23)


## [23.6.0](https://github.com/kpfleming/jinjanator/tree/23.6.0) - 2023-08-01

### Backwards-incompatible Changes

- Upgraded to plugins API 23.4.
  


### Additions

- Added support for 'sequence' data in YAML-format input.
  [#14](https://github.com/kpfleming/jinjanator/issues/14)
- Added support for 'array' data in JSON-format input.
  [#15](https://github.com/kpfleming/jinjanator/issues/15)
- Added list of discovered plugins to '--version' output.
  [#16](https://github.com/kpfleming/jinjanator/issues/16)
- Options-related errors from format parsers are now handled.
  [#17](https://github.com/kpfleming/jinjanator/issues/17)


## [23.5.0](https://github.com/kpfleming/jinjanator/tree/23.5.0) - 2023-07-24

### Additions

- Added link to Ansible plugin.
  


### Fixes

- Corrected content of LICENSE file.
  
- Corrected formatting of README on PyPI.


## [23.4.0](https://github.com/kpfleming/jinjanator/tree/23.4.0) - 2023-07-24

### Backwards-incompatible Changes

- Moved plugin API to the jinjanator-plugins package.
  [#12](https://github.com/kpfleming/jinjanator/issues/12)


## [23.3.0](https://github.com/kpfleming/jinjanator/tree/23.3.0) - 2023-07-22

### Fixes

- Disabled Jinja2 'autoescape' feature since it can produce incorrect output.
  [#8](https://github.com/kpfleming/jinjanator/issues/8)
- Add missing 'attrs' package to project dependencies.
  [#9](https://github.com/kpfleming/jinjanator/issues/9)


## [23.2.0](https://github.com/kpfleming/jinjanator/tree/23.2.0) - 2023-07-22

### Fixes

- Resolved crash when writing final output. Increased test coverage to avoid regressions.
  [#7](https://github.com/kpfleming/jinjanator/issues/7)


## [23.1.0](https://github.com/kpfleming/jinjanator/tree/23.1.0) - 2023-07-22

### Added

- Initial release!
