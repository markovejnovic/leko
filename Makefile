PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PIP_DIST = $(PYTHON) -m pip

.PHONY: clean install

dist: clean leko/
	$(PYTHON) setup.py bdist_wheel

install: dist
	$(PIP_DIST) install ./dist/leko-0.1.0-py3-none-any.whl --force-reinstall

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m virtualenv $(VENV)
	$(PIP) install -r requirements.txt
