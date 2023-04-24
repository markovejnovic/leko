PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip

.PHONY: clean

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m virtualenv $(VENV)
	$(PIP) install -r requirements.txt

dist: clean
	$(PYTHON) setup.py bdist_wheel
