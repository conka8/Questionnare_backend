ROOT_DIR := $(shell pwd)
PROJECT_NAME := $(notdir $(ROOT_DIR))
RELEASE_VERSION ?= $(shell git describe --always)
RELEASE_DATE := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

.PHONY: clean
clean: clean-build clean-pyc clean-pycache

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__/ .eggs/ .cache/
	rm -rf .tox/ .pytest_cache/ .benchmarks/ .mypy_cache htmlcov

.PHONY: clean-pycache
clean-pycache:
	find . -name __pycache__ -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: lint
lint:
	flake8 $(PACKAGE_DIR)

.PHONY: test
test:
	python3 setup.py test

.PHONY: tox
tox:
	tox

.PHONY: build
build:
	python3 setup.py build

.PHONY: install
install: build
	python3 setup.py install

.PHONY: install-user
install-user: build
	python3 setup.py install --user

.PHONY: git
git:
	git push --all
	git push --tags

.PHONY: check
check:
	python3 setup.py check

.PHONY: docs
docs:
	poetry run mkdocs serve

.PHONY: release
release:
	git diff-index --quiet HEAD || { echo "untracked files! Aborting"; exit 1; }
	git checkout develop
	git checkout -b release/$(shell date +'%Y%m%d%H%m')
	git push origin release/$(shell date +'%Y%m%d%H%m')
	git checkout develop
