DESTDIR=
MANPATH=/usr/share/man
NAME=serviceAccessConfig
dirs = etc lib man tests usr
files = LICENSE Makefile README.md setup.py

nv = $(shell rpm -q --specfile --qf '%{NAME}-%{VERSION}|' *.spec | cut -d'|' -f1)
verSpec = $(shell rpm -q --specfile --qf '%{VERSION}|' *.spec | cut -d'|' -f1)
verSrc = $(shell cat lib/serviceAccessConfig/VERSION)

ifneq "$(verSpec)" "$(verSrc)"
$(error "Version mismatch, will not take any action")
endif

clean:
	@find . -name "*.pyc" | xargs rm -f 
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name "*.cache" | xargs rm -rf
	@find . -name "*.egg-info" | xargs rm -rf

install:
	python setup.py install --prefix="$(PREFIX)" --root="$(DESTDIR)"
	install -d -m 755 "$(DESTDIR)"/"$(MANDIR)"/man1
	install -m 644 man/man1/serviceAccessConfig.1 "$(DESTDIR)"/"$(MANDIR)"/man1
	gzip "$(DESTDIR)"/"$(MANDIR)"/man1/serviceAccessConfig.1

pep8:
	@python -m pycodestyle lib/serviceAccessConfig/*.py
	@python -m pycodestyle --ignore=E402 tests/unit/*.py
	@flake8 lib/serviceAccessConfig/*.py
	@flake8 --ignore=E402 tests/unit/*.py
	@flake8 setup.py

test:
	py.test tests/unit/test_*.py

tar: clean
	mkdir -p "$(NAME)-$(verSrc)"/man/man1
	cp -r $(dirs) $(files) "$(NAME)-$(verSrc)"
	tar -cjf "$(NAME)-$(verSrc).tar.bz2" "$(NAME)-$(verSrc)"
	rm -rf "$(NAME)-$(verSrc)"
