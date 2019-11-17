.PHONY: test test-unit develop publish clean

PYTHON_VERSION ?= python3

test:
	$(PYTHON_VERSION) -m pytest -s tests/*.py --cov-report term-missing --cov=cloudburst

publish: test

develop:
	$(PYTHON_VERSION) setup.py develop

clean:
	rm -rf dist
	rm -rf build
	rm -rf src/*.egg-info
