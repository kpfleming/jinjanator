all:

SHELL := /bin/bash
.PHONY: clean build publish

# Package
clean:
	@rm -rf build/ dist/ *.egg-info/ README.md README.rst
	@pip install -e .  # have to reinstall because we are using self
README.md: $(shell find misc/ j2cli/)
	@python misc/_doc/README.py | python j2cli/__init__.py -f json misc/_doc/README.md.j2 > $@
README.rst: README.md
	@pandoc -f markdown -t rst -o README.rst README.md

build: README.rst
	@./setup.py build sdist bdist_wheel
publish-test: README.rst
	@twine upload --repository pypitest dist/*
publish: README.rst
	@twine upload dist/*



test-2.6:
	@docker run --rm -it -v $(realpath .):/app mrupgrade/deadsnakes:2.6 bash -c 'cd /app && pip install -e . && pip install nose argparse && nosetests'
