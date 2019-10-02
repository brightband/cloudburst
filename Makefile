.PHONY: test build publish clean

PYTHON_VERSION ?= python3

test: build

build:

publish: test

develop:
	$(PYTHON_VERSION) setup.py install

clean:
	rm -rf dist
	rm -rf build
	rm -rf src/*.egg-info
