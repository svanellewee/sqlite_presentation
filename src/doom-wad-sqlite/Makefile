EMACS?=/Applications/Emacs.app/Contents/MacOS/Emacs
PY3_VENV=./virtualenv
PYTHON=$(PY3_VENV)/bin/python
DOOM_SHAREWARE=doom1.wad

venv: | $(PY3_VENV)
	pyvenv $@
	@echo "Python version $$($@/bin/python --version)"

$(DOOM_SHAREWARE):
	cp ../../depdir/$(DOOM_SHAREWARE) .

doom-shareware: | $(DOOM_SHAREWARE)

deps: venv doom-shareware
	$(PY3_VENV)/bin/pip install -r requirements.txt

export-from-org: 
	$(EMACS) -Q --batch --eval "(progn (require 'ob) (org-babel-tangle-file \"doom.org\"))" 


