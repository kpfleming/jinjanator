all:

SHELL := /bin/bash

# Package
.PHONY: clean
clean:
	@rm -rf build/ dist/ *.egg-info/ README.md README.rst
	@pip install -e .  # have to reinstall because we are using self
README.md: $(shell find j2cli/) $(wildcard misc/_doc/**)
	@python misc/_doc/README.py | python j2cli/__init__.py -f json -o $@ misc/_doc/README.md.j2


.PHONY: build publish-test publish
build: README.md
	@./setup.py build sdist bdist_wheel
publish-test: README.md
	@twine upload --repository pypitest dist/*
publish: README.md
	@twine upload dist/*


.PHONY: test test-tox
test:
	@nosetests
test-tox:
	@tox
