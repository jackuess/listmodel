PYTHON=python3
ENVDIR=./env

env:
	virtualenv -p $(PYTHON) $(ENVDIR)

.PHONY: test
test: env
	$(ENVDIR)/bin/pip install tox
	$(ENVDIR)/bin/tox

.PHONY: html
html: env
	$(ENVDIR)/bin/pip install -e ".[docs]"
	$(MAKE) -C docs/ html SPHINXBUILD=../$(ENVDIR)/bin/sphinx-build

.PHONY: clean
clean:
	rm -rf docs/_build
	rm -rf $(ENVDIR)
