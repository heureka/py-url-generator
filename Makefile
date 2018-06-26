
PYTHON:="$(shell which python3)"
VENV_DIR=.venv
pip_install:=$(VENV_DIR)/bin/pip install

.PHONY: build
build: vendor

vendor:
	$(PYTHON) -m venv --copies $(VENV_DIR)
	$(pip_install) -r requirements-dev.txt

.PHONY: test
test: vendor
	$(VENV_DIR)/bin/py.test tests

.PHONY: clean
clean:
	rm -rf vendor $(VENV_DIR)

.PHONY: pip-update
pip-update: $(VENV_DIR)
	$(pip_install) --upgrade pip
	$(pip_install) pip-tools
	$(VENV_DIR)/bin/pip-compile -U requirements-dev.in
