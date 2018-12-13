all:

SHELL := /bin/bash
.PHONY: clean build publish

# Package
clean:
	@rm -rf build/ dist/ *.egg-info/ README.md README.rst
README.md: $(shell find misc/ j2cli/)
	@python misc/_doc/README.py | j2 -f json misc/_doc/README.md.j2 > $@
README.rst: README.md
	@pandoc -f markdown -t rst -o README.rst README.md
build: README.rst
	@./setup.py build sdist bdist_wheel
publish-test: README.rst
	@twine upload --repository testpypi dist/*
publish: README.rst
	@twine upload dist/*
