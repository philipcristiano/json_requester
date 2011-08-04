#
# Basic makefile for general targets
#

EASY_INSTALL = bin/easy_install
NOSE = bin/nosetests
NOSYD = bin/nosyd
PIP = bin/pip
PYTHON = bin/python

## Testing ##
.PHONY: test tdd dist clean requirements virtualenv
test:
	$(NOSE) tests

tdd:
	$(NOSYD) -1

clean:
	-$(PYTHON) setup.py clean
	# clean python bytecode files
	-find . -type f -name '*.pyc' -o -name '*.tar.gz' -delete
	-rm -f nosetests.xml
	-rm -f pip-log.txt
	-rm -f .nose-stopwatch-times
	-rm -rf build dist *.egg-info

dist: clean
	$(shell export COPYFILE_DISABLE=true)

	$(PYTHON) setup.py sdist

requirements: virtualenv
	$(EASY_INSTALL) -U distribute
	$(PIP) install -r requirements.pip
	-rm README.txt
	# These libs don't work when installed via pip.
	$(EASY_INSTALL) nose_machineout
	$(EASY_INSTALL) readline

virtualenv:
	virtualenv --distribute --no-site-packages --python=python2.6 .
