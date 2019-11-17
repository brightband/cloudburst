.PHONY: test test-unit develop publish clean

PYTHON_VERSION ?= python3.7

test-unit:
	python3 -m pytest -s tests/unit/*.py --cov-report term-missing --cov=cloudburst

test: test-unit

publish: test

develop:
	$(PYTHON_VERSION) setup.py develop

clean:
	rm -rf dist
	rm -rf build
	rm -rf src/*.egg-info
